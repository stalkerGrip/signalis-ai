from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from scripts.investigation.evidence_ranker import get_text, rank_evidence_list


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def collect_dicts(value: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []

    if isinstance(value, dict):
        found.append(value)
        for child in value.values():
            found.extend(collect_dicts(child))

    elif isinstance(value, list):
        for child in value:
            found.extend(collect_dicts(child))

    return found


def likely_evidence_dict(item: dict[str, Any]) -> bool:
    evidence_keys = {
        "text",
        "content",
        "fragment",
        "snippet",
        "source_text",
        "matched_text",
        "file",
        "path",
        "source",
    }
    return bool(set(item.keys()) & evidence_keys)


def extract_evidence(*documents: Any) -> list[dict[str, Any]]:
    evidence: list[dict[str, Any]] = []

    for doc in documents:
        for item in collect_dicts(doc):
            if likely_evidence_dict(item):
                evidence.append(item)

    return evidence


def path_of(item: dict[str, Any]) -> str:
    return str(item.get("path") or item.get("file") or item.get("source") or "").replace("\\", "/")


def line_of(item: dict[str, Any]) -> int | str | None:
    for key in ("line", "line_start", "start_line"):
        value = item.get(key)
        if value:
            return value

    text = get_text(item)
    match = re.search(r"^\s*(\d+)\s*:", text, flags=re.MULTILINE)
    if match:
        return int(match.group(1))

    return None


def stable_key(item: dict[str, Any]) -> str:
    path = path_of(item).lower()
    line = str(line_of(item) or "")
    text = get_text(item)
    compact = re.sub(r"\s+", " ", text.lower()).strip()
    return f"{path}:{line}:{compact[:260]}"


def dedupe_raw(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    output: list[dict[str, Any]] = []

    for item in items:
        key = stable_key(item)
        if key in seen:
            continue
        seen.add(key)
        output.append(item)

    return output


def classify_chain_roles(item: dict[str, Any]) -> list[str]:
    text = get_text(item).lower()
    path = path_of(item).lower()

    roles: list[str] = []

    if "plugins/gridinv/sv_transfer.lua" in path or "vendorsellitem" in text or "oldinventory.vendor" in text:
        roles.append("purchase_transfer")

    if "syncitemadded" in text or "nutinventoryadd" in text:
        roles.append("inventory_membership_sync")

    if "item:sync" in text or "invdata" in text or "itemdatachanged" in text or "setdata" in text:
        roles.append("item_metadata_sync")

    if ("server" in text and "client" in text) or "netstream" in text or "net.start" in text or "net.receive" in text:
        roles.append("realm_or_network_transition")

    if "inventoryitemdatachanged" in text or "populateitems" in text:
        roles.append("client_ui_refresh")

    if "vendor" in text or "vendor" in path:
        roles.append("vendor_context")

    return roles or ["unclassified"]


CHAIN_ROLE_ORDER = [
    "purchase_transfer",
    "inventory_membership_sync",
    "item_metadata_sync",
    "realm_or_network_transition",
    "client_ui_refresh",
    "vendor_context",
]


def evidence_summary(item: dict[str, Any], limit: int = 900) -> str:
    return get_text(item).strip()[:limit]


def build_runtime_chain_candidate(ranked: list[dict[str, Any]]) -> list[dict[str, Any]]:
    chain: list[dict[str, Any]] = []
    used_cluster_keys: set[str] = set()
    used_sources_by_role: set[str] = set()

    for role in CHAIN_ROLE_ORDER:
        candidates = [
            item for item in ranked
            if role in classify_chain_roles(item)
            and item.get("evidence_cluster_key") not in used_cluster_keys
        ]

        if not candidates:
            continue

        # Prefer distinct source files across adjacent roles when possible.
        distinct = [
            item for item in candidates
            if path_of(item).lower() not in used_sources_by_role
        ]

        chosen_pool = distinct or candidates
        chosen = chosen_pool[0]

        used_cluster_keys.add(str(chosen.get("evidence_cluster_key")))
        used_sources_by_role.add(path_of(chosen).lower())

        chain.append(
            {
                "role": role,
                "score": chosen.get("evidence_rank_score", 0),
                "reasons": chosen.get("evidence_rank_reasons", []),
                "source": path_of(chosen),
                "line": line_of(chosen),
                "summary": evidence_summary(chosen),
            }
        )

    return chain


def infer_findings(chain: list[dict[str, Any]]) -> list[str]:
    roles = {step["role"] for step in chain}
    findings: list[str] = []

    if "purchase_transfer" in roles:
        findings.append(
            "The synthesis found a purchase-transfer step, so vendor cleanup should be evaluated inside grid inventory transfer, not only vendor exit cleanup."
        )

    if "inventory_membership_sync" in roles and "item_metadata_sync" in roles:
        findings.append(
            "Inventory membership sync and item metadata sync appear in the same causal chain but remain separate synchronization systems."
        )

    if "client_ui_refresh" in roles:
        findings.append(
            "Client UI refresh depends on item/inventory data change callbacks reaching the grid inventory panel."
        )

    return findings


def write_markdown(path: Path, synthesis: dict[str, Any]) -> None:
    lines: list[str] = []

    lines.append("# Investigation Synthesis V2")
    lines.append("")
    lines.append(f"Question: `{synthesis['question']}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(synthesis["summary"])
    lines.append("")

    lines.append("## Input Counts")
    lines.append("")
    for key, value in synthesis["input_counts"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")

    lines.append("## Findings")
    lines.append("")
    for finding in synthesis["findings"]:
        lines.append(f"- {finding}")
    lines.append("")

    lines.append("## Runtime Chain Candidate")
    lines.append("")
    for idx, step in enumerate(synthesis["runtime_chain_candidate"], start=1):
        lines.append(f"### {idx}. {step['role']}")
        lines.append("")
        lines.append(f"- Score: `{step['score']}`")
        lines.append(f"- Source: `{step.get('source')}`")
        lines.append(f"- Line: `{step.get('line')}`")
        lines.append(f"- Reasons: `{', '.join(step.get('reasons', []))}`")
        lines.append("")
        if step.get("summary"):
            lines.append("```text")
            lines.append(str(step["summary"]).strip())
            lines.append("```")
            lines.append("")

    lines.append("## Top Ranked Evidence")
    lines.append("")
    for idx, item in enumerate(synthesis["ranked_evidence"][:25], start=1):
        lines.append(f"### Evidence {idx}")
        lines.append("")
        lines.append(f"- Score: `{item.get('evidence_rank_score')}`")
        lines.append(f"- Source: `{path_of(item)}`")
        lines.append(f"- Line: `{line_of(item)}`")
        lines.append(f"- Cluster: `{item.get('evidence_cluster_key')}`")
        lines.append(f"- Reasons: `{', '.join(item.get('evidence_rank_reasons', []))}`")
        lines.append("")

        text = evidence_summary(item, limit=1200)
        if text:
            lines.append("```text")
            lines.append(text)
            lines.append("```")
            lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--source-validation", type=Path)
    parser.add_argument("--runtime-facts", type=Path)
    parser.add_argument("--runtime-chain-evidence", type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    docs = []
    for input_path in [args.source_validation, args.runtime_facts, args.runtime_chain_evidence]:
        if input_path and input_path.exists():
            docs.append(load_json(input_path))

    raw_evidence = extract_evidence(*docs)
    deduped_raw = dedupe_raw(raw_evidence)
    ranked = rank_evidence_list(deduped_raw, args.question)
    chain_candidate = build_runtime_chain_candidate(ranked)

    synthesis = {
        "schema": "investigation_synthesis.v2",
        "question": args.question,
        "summary": (
            "Evidence was deduplicated with overlapping source-window clustering, ranked for causal-chain relevance, "
            "and organized into a runtime-chain candidate. This artifact is intended for targeted validation and "
            "possible runtime-chain promotion."
        ),
        "input_counts": {
            "raw_evidence": len(raw_evidence),
            "deduped_raw_evidence": len(deduped_raw),
            "ranked_clustered_evidence": len(ranked),
            "runtime_chain_candidate_steps": len(chain_candidate),
        },
        "findings": infer_findings(chain_candidate),
        "runtime_chain_candidate": chain_candidate,
        "ranked_evidence": ranked,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(json.dumps(synthesis, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(args.out_md, synthesis)

    print(f"Wrote synthesis JSON: {args.out_json}")
    print(f"Wrote synthesis MD:   {args.out_md}")
    print("")
    print("Summary:")
    for key, value in synthesis["input_counts"].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()