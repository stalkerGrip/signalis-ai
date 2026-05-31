#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "runtime_chain"


def get_chain(payload: dict[str, Any], chain_id: str | None) -> dict[str, Any]:
    chains = payload.get("chains")
    if isinstance(chains, list) and chains:
        if chain_id:
            for chain in chains:
                if str(chain.get("chain_id", chain.get("id", ""))) == chain_id:
                    return chain
            raise SystemExit(f"Could not find chain id: {chain_id}")
        return chains[0]

    chain = payload.get("chain")
    if isinstance(chain, dict):
        return chain

    # Compatibility with current build_runtime_chain_evidence output.
    return {
        "chain_id": payload.get("chain_id", "CHAIN-001"),
        "title": payload.get("title", "Runtime Chain"),
        "confidence": payload.get("chain_confidence") or payload.get("summary", {}).get("chain_confidence", "unknown"),
        "score": payload.get("chain_score") or payload.get("summary", {}).get("chain_score"),
        "steps": payload.get("steps") or payload.get("chain_steps") or payload.get("present_steps") or [],
        "missing_steps": payload.get("missing_steps") or [],
    }


def get_summary(payload: dict[str, Any]) -> dict[str, Any]:
    summary = payload.get("summary")
    if isinstance(summary, dict):
        return summary
    return {
        "chain_confidence": payload.get("chain_confidence"),
        "chain_score": payload.get("chain_score"),
        "chain_steps_present": payload.get("chain_steps_present"),
        "chain_steps_missing": payload.get("chain_steps_missing"),
        "raw_evidence_total": payload.get("raw_evidence_total"),
        "deduped_evidence_total": payload.get("deduped_evidence_total"),
        "duplicates_removed": payload.get("duplicates_removed"),
    }


def evidence_list(payload: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ["ranked_chain_evidence", "chain_evidence", "evidence", "deduped_evidence", "classified_evidence"]:
        value = payload.get(key)
        if isinstance(value, list):
            return [x for x in value if isinstance(x, dict)]
    chain = payload.get("chain")
    if isinstance(chain, dict):
        value = chain.get("evidence") or chain.get("ranked_evidence")
        if isinstance(value, list):
            return [x for x in value if isinstance(x, dict)]
    return []


def step_text(step: Any) -> str:
    if isinstance(step, str):
        return step
    if isinstance(step, dict):
        return str(step.get("label") or step.get("name") or step.get("step") or step.get("description") or step)
    return str(step)


def evidence_class(e: dict[str, Any]) -> str:
    return str(e.get("class") or e.get("evidence_class") or e.get("semantic_class") or "unknown")


def evidence_file(e: dict[str, Any]) -> str:
    return str(e.get("file") or e.get("file_path") or e.get("path") or "unknown")


def evidence_lines(e: dict[str, Any]) -> str:
    start = e.get("start_line") or e.get("line_start") or e.get("start")
    end = e.get("end_line") or e.get("line_end") or e.get("end")
    if start and end:
        return f"{start}-{end}"
    if start:
        return str(start)
    lines = e.get("lines")
    return str(lines or "unknown")


def evidence_pattern(e: dict[str, Any]) -> str:
    return str(e.get("pattern") or e.get("matched_pattern") or e.get("query") or "unknown")


def evidence_score(e: dict[str, Any]) -> str:
    score = e.get("score") or e.get("rank_score") or e.get("weight")
    return "" if score is None else str(score)


def representative_evidence(evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_class: dict[str, dict[str, Any]] = {}
    for e in evidence:
        klass = evidence_class(e)
        current = by_class.get(klass)
        if current is None:
            by_class[klass] = e
            continue
        cur_score = float(current.get("score") or current.get("rank_score") or 0)
        new_score = float(e.get("score") or e.get("rank_score") or 0)
        if new_score > cur_score:
            by_class[klass] = e
    return list(by_class.values())


def build_chain_form(steps: list[Any], fallback_name: str) -> str:
    labels = [step_text(s) for s in steps if step_text(s).strip()]
    if labels:
        return "\n→ ".join(labels)
    return fallback_name


def format_doc(
    payload: dict[str, Any],
    source: Path,
    subsystem: str,
    name: str,
    title: str | None,
    chain_id: str | None,
) -> str:
    summary = get_summary(payload)
    chain = get_chain(payload, chain_id)
    evidence = representative_evidence(evidence_list(payload))

    resolved_chain_id = str(chain.get("chain_id") or chain.get("id") or chain_id or "CHAIN-001")
    resolved_title = title or str(chain.get("title") or name.replace("_", " ").title())
    confidence = str(chain.get("confidence") or summary.get("chain_confidence") or "unknown")
    score = chain.get("score") or summary.get("chain_score")
    steps = chain.get("steps") or chain.get("present_steps") or payload.get("steps") or []
    missing_steps = chain.get("missing_steps") or payload.get("missing_steps") or []
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    lines: list[str] = [
        f"# {resolved_title}",
        "",
        "Status: source-validated runtime chain." if confidence == "validated" else "Status: runtime chain evidence artifact.",
        "",
        f"- Generated at: `{generated_at}`",
        f"- Source evidence JSON: `{source}`",
        f"- Subsystem: `{subsystem}`",
        f"- Chain ID: `{resolved_chain_id}`",
        f"- Confidence: `{confidence}`",
    ]
    if score is not None:
        lines.append(f"- Score: `{score}`")
    if summary.get("raw_evidence_total") is not None:
        lines.append(f"- Raw evidence total: `{summary.get('raw_evidence_total')}`")
    if summary.get("deduped_evidence_total") is not None:
        lines.append(f"- Deduped evidence total: `{summary.get('deduped_evidence_total')}`")
    if summary.get("duplicates_removed") is not None:
        lines.append(f"- Duplicates removed: `{summary.get('duplicates_removed')}`")

    lines += ["", "## Runtime Chain", ""]
    if steps:
        for index, step in enumerate(steps, start=1):
            lines.append(f"{index}. {step_text(step)}")
    else:
        lines.append("No explicit steps found in the chain evidence JSON.")

    if missing_steps:
        lines += ["", "## Missing Steps", ""]
        for step in missing_steps:
            lines.append(f"- {step_text(step)}")

    lines += [
        "",
        "## Architecture Meaning",
        "",
        "This chain records source-validated runtime propagation. It should be used as a durable semantic anchor for retrieval-guided architecture reasoning, not as a replacement for raw source validation when changing code.",
        "",
        "When investigating related bugs, prefer this chain as compact context before opening raw Lua.",
        "",
        "## Validated Chain Form",
        "",
        "```text",
        build_chain_form(steps, name),
        "```",
        "",
        "## Representative Evidence",
        "",
    ]

    if not evidence:
        lines.append("No representative evidence entries found.")
    else:
        for e in evidence:
            klass = evidence_class(e)
            lines += [
                f"### {klass}",
                "",
                f"- File: `{evidence_file(e)}`",
                f"- Lines: `{evidence_lines(e)}`",
                f"- Pattern: `{evidence_pattern(e)}`",
            ]
            score_text = evidence_score(e)
            if score_text:
                lines.append(f"- Score: `{score_text}`")
            lines.append("")

    lines += [
        "## Promotion Notes",
        "",
        "Promote this document to Qdrant/retrieval corpus only after the chain is source-validated and reviewed.",
        "Do not promote speculative or partial chains as authoritative subsystem knowledge.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote validated runtime chain evidence into durable runtime-chain documentation.")
    parser.add_argument("--chain", required=True, type=Path, help="Runtime chain evidence JSON")
    parser.add_argument("--subsystem", required=True, help="Subsystem name, e.g. vendor")
    parser.add_argument("--name", required=True, help="Output slug/name, e.g. vendor_purchase_item_metadata_sync")
    parser.add_argument("--out-dir", type=Path, default=Path("docs/runtime/runtime_chains"))
    parser.add_argument("--out", type=Path, default=None, help="Optional exact output markdown path")
    parser.add_argument("--title", default=None, help="Optional document title")
    parser.add_argument("--chain-id", default=None, help="Optional chain id to select from multi-chain evidence JSON")
    args = parser.parse_args()

    source = args.chain.resolve()
    payload = read_json(source)
    name = slugify(args.name)
    out_path = args.out.resolve() if args.out else (args.out_dir / f"{name}.md").resolve()

    doc = format_doc(
        payload=payload,
        source=source,
        subsystem=args.subsystem,
        name=name,
        title=args.title,
        chain_id=args.chain_id,
    )
    write_text(out_path, doc)
    print(f"Wrote runtime chain doc: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
