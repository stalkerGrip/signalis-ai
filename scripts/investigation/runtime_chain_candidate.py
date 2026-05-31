from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


CHAIN_PATTERNS = [
    {
        "step": "purchase_transfer",
        "required_any": [
            "plugins/gridinv/sv_transfer.lua",
            "vendorsellitem",
            "oldinventory.vendor",
            "item:setdata(\"vendorsprice\", nil, client)",
            "item:setdata(\"vendorqty\", nil, client)",
            "item:setdata(\"vendormqty\", nil, client)",
            "inventory:add",
        ],
        "description": "Vendor purchase transfer path in grid inventory.",
    },
    {
        "step": "inventory_membership_sync",
        "required_any": [
            "syncitemadded",
            "nutinventoryadd",
            "inventory:additem",
            "inventory.items",
        ],
        "description": "Server inventory membership update and item-add replication.",
    },
    {
        "step": "item_initial_sync",
        "required_any": [
            "item:sync",
            "item.sync",
            "sync(recipients)",
        ],
        "description": "Initial item sync to inventory recipients.",
    },
    {
        "step": "purchase_metadata_cleanup",
        "required_any": [
            "vendorsprice",
            "vendorqty",
            "vendormqty",
            "vendorbprice",
            "setdata",
        ],
        "description": "Vendor presentation metadata mutation on transferred item.",
    },
    {
        "step": "item_metadata_network_sync",
        "required_any": [
            "invdata",
            "netstream.start",
            "item:setdata",
            "itemdatachanged",
        ],
        "description": "Item metadata sync crosses server/client boundary.",
    },
    {
        "step": "client_item_data_apply",
        "required_any": [
            "item.data[key]",
            "itemdatachanged",
            "oldvalue",
            "newvalue",
        ],
        "description": "Client item instance receives changed item data.",
    },
    {
        "step": "grid_inventory_ui_refresh",
        "required_any": [
            "inventoryitemdatachanged",
            "populateitems",
            "cl_grid_inventory_panel.lua",
        ],
        "description": "Grid inventory panel refreshes visible item presentation.",
    },
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_of(item: dict[str, Any]) -> str:
    parts: list[str] = []

    for key in (
        "summary",
        "text",
        "content",
        "fragment",
        "snippet",
        "source_text",
        "matched_text",
        "context",
        "evidence_summary",
    ):
        value = item.get(key)
        if isinstance(value, str):
            parts.append(value)

    for key in ("source", "path", "file", "resolved_path"):
        value = item.get(key)
        if isinstance(value, str):
            parts.append(value)

    return "\n".join(parts)


def path_of(item: dict[str, Any]) -> str:
    return str(
        item.get("source")
        or item.get("path")
        or item.get("file")
        or item.get("resolved_path")
        or ""
    ).replace("\\", "/")


def line_of(item: dict[str, Any]) -> int | str | None:
    for key in ("line", "line_start", "start_line"):
        value = item.get(key)
        if value:
            return value

    text = text_of(item)
    match = re.search(r"^\s*(\d+)\s*:", text, flags=re.MULTILINE)
    if match:
        return int(match.group(1))

    return None


def synthesis_evidence_pool(synthesis: dict[str, Any]) -> list[dict[str, Any]]:
    pool: list[dict[str, Any]] = []

    for key in ("runtime_chain_candidate", "ranked_evidence"):
        value = synthesis.get(key)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    pool.append(item)

    return pool


def targeted_validation_pool(validation: dict[str, Any]) -> list[dict[str, Any]]:
    pool: list[dict[str, Any]] = []

    for result in validation.get("results", []):
        if not isinstance(result, dict):
            continue

        source_path = result.get("resolved_path") or result.get("path")

        for needle in result.get("needles", []):
            if not isinstance(needle, dict) or not needle.get("found"):
                continue

            pool.append(
                {
                    "source": source_path,
                    "path": result.get("path"),
                    "resolved_path": result.get("resolved_path"),
                    "line": needle.get("line"),
                    "summary": needle.get("context", ""),
                    "matched_needle": needle.get("needle"),
                    "evidence_rank_score": 99,
                    "evidence_source_type": "targeted_validation",
                }
            )

    return pool


def match_score(item: dict[str, Any], pattern: dict[str, Any]) -> tuple[float, list[str]]:
    text = text_of(item).lower()
    source = path_of(item).lower()
    matched: list[str] = []

    for token in pattern["required_any"]:
        token_lower = token.lower()
        if token_lower in text or token_lower in source:
            matched.append(token)

    score = float(len(matched))

    if pattern["step"] == "purchase_transfer" and "plugins/gridinv/sv_transfer.lua" in source:
        score += 8

    if item.get("evidence_source_type") == "targeted_validation":
        score += 4

    if "removereceiverfromvendor" in text:
        score -= 3

    if "vendoritemsetdata" in text:
        score -= 1

    return score, matched


def build_chain(
    synthesis: dict[str, Any],
    targeted_validations: list[dict[str, Any]],
) -> dict[str, Any]:
    pool = synthesis_evidence_pool(synthesis)

    for validation in targeted_validations:
        pool.extend(targeted_validation_pool(validation))

    steps: list[dict[str, Any]] = []

    for pattern in CHAIN_PATTERNS:
        candidates: list[tuple[float, list[str], dict[str, Any]]] = []

        for item in pool:
            score, matched = match_score(item, pattern)
            if score <= 0:
                continue
            candidates.append((score, matched, item))

        candidates.sort(
            key=lambda entry: (
                entry[0],
                float(entry[2].get("evidence_rank_score", entry[2].get("score", 0)) or 0),
            ),
            reverse=True,
        )

        if not candidates:
            steps.append(
                {
                    "step": pattern["step"],
                    "status": "missing_evidence",
                    "description": pattern["description"],
                    "source": None,
                    "line": None,
                    "matched_terms": [],
                    "evidence_summary": "",
                }
            )
            continue

        chosen_score, matched, chosen = candidates[0]

        steps.append(
            {
                "step": pattern["step"],
                "status": "evidence_found",
                "description": pattern["description"],
                "source": path_of(chosen),
                "line": line_of(chosen),
                "match_score": chosen_score,
                "evidence_rank_score": chosen.get("evidence_rank_score", chosen.get("score")),
                "evidence_source_type": chosen.get("evidence_source_type", "synthesis"),
                "matched_terms": matched,
                "evidence_summary": text_of(chosen).strip()[:1200],
            }
        )

    return {
        "schema": "runtime_chain_candidate.v2",
        "question": synthesis.get("question", ""),
        "source_synthesis_schema": synthesis.get("schema"),
        "chain_name": "vendor_purchase_price_label_cleanup",
        "confidence": classify_confidence(steps),
        "confidence_reasons": confidence_reasons(steps),
        "steps": steps,
        "missing_steps": [step["step"] for step in steps if step["status"] != "evidence_found"],
        "notes": [
            "This artifact is a deterministic candidate, not final truth.",
            "Targeted validation evidence is allowed to satisfy previously missing causal-chain steps.",
            "Promotion is allowed only when authoritative purchase_transfer and downstream sync steps are present.",
        ],
    }


def classify_confidence(steps: list[dict[str, Any]]) -> str:
    missing = [step for step in steps if step["status"] != "evidence_found"]

    has_purchase_transfer = any(
        step["step"] == "purchase_transfer"
        and step["status"] == "evidence_found"
        and "plugins/gridinv/sv_transfer.lua" in str(step.get("source", "")).lower()
        for step in steps
    )

    has_metadata_cleanup = any(
        step["step"] == "purchase_metadata_cleanup"
        and step["status"] == "evidence_found"
        for step in steps
    )

    has_item_sync = any(
        step["step"] == "item_metadata_network_sync"
        and step["status"] == "evidence_found"
        for step in steps
    )

    has_ui_refresh = any(
        step["step"] == "grid_inventory_ui_refresh"
        and step["status"] == "evidence_found"
        for step in steps
    )

    if not has_purchase_transfer:
        return "low_missing_authoritative_purchase_transfer"

    if missing:
        return "medium_missing_downstream_steps"

    if has_metadata_cleanup and has_item_sync and has_ui_refresh:
        return "high"

    return "medium"


def confidence_reasons(steps: list[dict[str, Any]]) -> list[str]:
    reasons: list[str] = []

    for step in steps:
        if step["status"] != "evidence_found":
            reasons.append(f"missing:{step['step']}")
            continue

        if step.get("evidence_source_type") == "targeted_validation":
            reasons.append(f"targeted_validation:{step['step']}")

        if "plugins/gridinv/sv_transfer.lua" in str(step.get("source", "")).lower():
            reasons.append("authoritative_purchase_transfer_source_validated")

        if step["step"] == "item_metadata_network_sync":
            reasons.append("item_metadata_sync_boundary_present")

        if step["step"] == "grid_inventory_ui_refresh":
            reasons.append("client_ui_refresh_present")

    return sorted(set(reasons))


def write_markdown(path: Path, candidate: dict[str, Any]) -> None:
    lines: list[str] = []

    lines.append("# Runtime Chain Candidate V2")
    lines.append("")
    lines.append(f"Question: `{candidate.get('question', '')}`")
    lines.append("")
    lines.append(f"Chain: `{candidate['chain_name']}`")
    lines.append(f"Confidence: `{candidate['confidence']}`")
    lines.append("")

    lines.append("## Confidence Reasons")
    lines.append("")
    for reason in candidate["confidence_reasons"]:
        lines.append(f"- `{reason}`")
    lines.append("")

    lines.append("## Chain")
    lines.append("")

    for index, step in enumerate(candidate["steps"], start=1):
        lines.append(f"### {index}. {step['step']}")
        lines.append("")
        lines.append(f"- Status: `{step['status']}`")
        lines.append(f"- Description: {step['description']}")
        lines.append(f"- Source: `{step.get('source')}`")
        lines.append(f"- Line: `{step.get('line')}`")
        lines.append(f"- Evidence source type: `{step.get('evidence_source_type')}`")
        lines.append(f"- Matched terms: `{', '.join(step.get('matched_terms', []))}`")
        lines.append("")

        if step.get("evidence_summary"):
            lines.append("```text")
            lines.append(step["evidence_summary"])
            lines.append("```")
            lines.append("")

    lines.append("## Missing Steps")
    lines.append("")
    if candidate["missing_steps"]:
        for step in candidate["missing_steps"]:
            lines.append(f"- `{step}`")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Notes")
    lines.append("")
    for note in candidate["notes"]:
        lines.append(f"- {note}")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--synthesis", required=True, type=Path)
    parser.add_argument("--targeted-validation", action="append", type=Path, default=[])
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    synthesis = load_json(args.synthesis)
    targeted_validations = [load_json(path) for path in args.targeted_validation]

    candidate = build_chain(synthesis, targeted_validations)

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(json.dumps(candidate, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(args.out_md, candidate)

    print(f"Wrote runtime chain candidate JSON: {args.out_json}")
    print(f"Wrote runtime chain candidate MD:   {args.out_md}")
    print("")
    print(f"Confidence: {candidate['confidence']}")
    print("Missing steps:")
    for step in candidate["missing_steps"]:
        print(f"  - {step}")


if __name__ == "__main__":
    main()