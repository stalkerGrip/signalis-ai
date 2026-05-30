#!/usr/bin/env python3
"""
SIGNALIS AI — Source Validation Scoring

Location:
    scripts/qdrant/score_validation_report.py

Purpose:
    Post-process validate_sources.py JSON output into scored evidence buckets.

Input:
    investigations/validation/<topic>_validation.json

Output:
    investigations/validation/<topic>_validation_scored.json
    investigations/validation/<topic>_validation_scored.md

Usage:
    python -m scripts.qdrant.score_validation_report ^
      --validation investigations/validation/vendor_stale_price_label_after_purchase_validation.json
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


CRITICAL_CLASSES = {
    "hook_emitter",
    "hook_listener_explicit",
    "hook_listener_plugin_method",
    "network_send_or_start",
    "network_receiver",
    "network_registration",
    "item_data_mutation",
    "networked_var_mutation",
}

SUPPORTING_CLASSES = {
    "item_data_read",
    "networked_var_read",
    "ui_presentation_logic",
    "network_payload_write",
    "network_payload_read",
}

NOISE_CLASSES = {
    "state_or_ui_reference",
    "reference",
    "hook_reference",
    "network_reference",
}


IMPORTANT_TERMS = [
    "VendorItemPriceUpdated",
    "VendorItemStockUpdated",
    "VendorMoneyUpdated",
    "nutVendorTrade",
    "nutVendorExit",
    "nutInventoryData",
    "vendorTradeInterface",
    "inventorySetPanelStatus",
    "CreateNewInventoryPanel",
    "CreateInventoryPanel",
    "updatePrice",
    "setPrice",
    "SetText",
    "ItemDataChanged",
    "StorageOpen",
    "storageInventory",
    "nutListenForInventoryChanges",
]


@dataclass
class ScoredFragment:
    file: str
    resolved_path: str | None
    source_root: str | None
    line_start: int
    line_end: int
    match_type: str
    match_value: str
    realm: str
    classification: str
    score: int
    bucket: str
    reasons: list[str]
    snippet: str


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def lower_blob(fragment: dict[str, Any]) -> str:
    return "\n".join([
        str(fragment.get("file", "")),
        str(fragment.get("match_type", "")),
        str(fragment.get("match_value", "")),
        str(fragment.get("classification", "")),
        str(fragment.get("realm", "")),
        str(fragment.get("snippet", "")),
    ]).lower()


def score_fragment(fragment: dict[str, Any], query: str) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    classification = str(fragment.get("classification", ""))
    match_type = str(fragment.get("match_type", ""))
    realm = str(fragment.get("realm", ""))
    file_path = str(fragment.get("file", ""))
    match_value = str(fragment.get("match_value", ""))
    snippet = str(fragment.get("snippet", ""))
    blob = lower_blob(fragment)

    if classification in CRITICAL_CLASSES:
        score += 50
        reasons.append(f"critical classification: {classification}")
    elif classification in SUPPORTING_CLASSES:
        score += 25
        reasons.append(f"supporting classification: {classification}")
    elif classification in NOISE_CLASSES:
        score -= 10
        reasons.append(f"low-signal classification: {classification}")

    if match_type == "hook":
        score += 20
        reasons.append("hook evidence")
    elif match_type == "network":
        score += 20
        reasons.append("network evidence")
    elif match_type == "state":
        score += 5
        reasons.append("state/UI evidence")

    if realm.startswith("server"):
        score += 20
        reasons.append("server-side evidence")
    elif realm.startswith("client"):
        score += 8
        reasons.append("client-side evidence")

    if "cl_networking.lua" in file_path.replace("\\", "/"):
        score += 15
        reasons.append("client networking file")
    if "sv_networking.lua" in file_path.replace("\\", "/"):
        score += 20
        reasons.append("server networking file")
    if "derma" in file_path.replace("\\", "/").lower():
        score += 8
        reasons.append("Derma/UI file")
    if "entities/entities/nut_vendor/init.lua" in file_path.replace("\\", "/"):
        score += 20
        reasons.append("vendor entity server init")
    if "inventory/cl_hooks.lua" in file_path.replace("\\", "/"):
        score += 15
        reasons.append("inventory client UI hook file")
    if "cl_base_inventory.lua" in file_path.replace("\\", "/"):
        score += 15
        reasons.append("client base inventory sync file")

    for term in IMPORTANT_TERMS:
        if term.lower() in blob:
            score += 12
            reasons.append(f"important term: {term}")

    if re.search(r"\bhook\.Run\s*\(", snippet):
        score += 15
        reasons.append("hook emitter call")
    if re.search(r"\bhook\.Add\s*\(", snippet):
        score += 12
        reasons.append("explicit hook listener")
    if re.search(r"\bfunction\s+(PLUGIN|SCHEMA|GM)\s*:", snippet):
        score += 12
        reasons.append("plugin/schema/gamemode hook listener")
    if re.search(r"\bnet\.(Start|Receive)\s*\(", snippet):
        score += 12
        reasons.append("raw net operation")
    if re.search(r"\bnetstream\.(Start|Hook)\s*\(", snippet):
        score += 12
        reasons.append("netstream operation")

    if re.search(r"\b(setData|SetData|getData|GetData)\s*\(", snippet, flags=re.I):
        score += 18
        reasons.append("item/inventory data access")
    if re.search(r"\b(updatePrice|SetText|label|price)\b", snippet, flags=re.I):
        score += 10
        reasons.append("price label/UI presentation evidence")

    if match_value in {"\\bvendor\\b", r"\bvendor\b", "\\bprice\\b", r"\bprice\b"}:
        score -= 15
        reasons.append("generic keyword match")

    query_terms = [t for t in re.split(r"\W+", query.lower()) if len(t) >= 4]
    matched_terms = [t for t in query_terms if t in blob]
    if matched_terms:
        score += min(20, len(matched_terms) * 5)
        reasons.append("query term overlap: " + ", ".join(sorted(set(matched_terms))))

    return score, reasons


def assign_bucket(score: int, fragment: dict[str, Any]) -> str:
    classification = str(fragment.get("classification", ""))

    if score >= 70:
        return "critical"
    if score >= 35:
        return "supporting"
    if classification in NOISE_CLASSES:
        return "noise"
    return "supporting"


def collect_fragments(validation: dict[str, Any]) -> list[ScoredFragment]:
    query = str(validation.get("query", ""))
    scored: list[ScoredFragment] = []

    for file_result in validation.get("files", []):
        for fragment in file_result.get("fragments", []):
            score, reasons = score_fragment(fragment, query)
            bucket = assign_bucket(score, fragment)

            scored.append(
                ScoredFragment(
                    file=str(fragment.get("file", "")),
                    resolved_path=fragment.get("resolved_path"),
                    source_root=fragment.get("source_root"),
                    line_start=int(fragment.get("line_start", 0)),
                    line_end=int(fragment.get("line_end", 0)),
                    match_type=str(fragment.get("match_type", "")),
                    match_value=str(fragment.get("match_value", "")),
                    realm=str(fragment.get("realm", "")),
                    classification=str(fragment.get("classification", "")),
                    score=score,
                    bucket=bucket,
                    reasons=reasons,
                    snippet=str(fragment.get("snippet", "")),
                )
            )

    scored.sort(key=lambda f: (f.score, -f.line_start), reverse=True)
    return scored


def summarize(scored: list[ScoredFragment]) -> dict[str, Any]:
    buckets = {"critical": 0, "supporting": 0, "noise": 0}
    realms: dict[str, int] = {}
    classes: dict[str, int] = {}
    files: dict[str, int] = {}

    for frag in scored:
        buckets[frag.bucket] = buckets.get(frag.bucket, 0) + 1
        realms[frag.realm] = realms.get(frag.realm, 0) + 1
        classes[frag.classification] = classes.get(frag.classification, 0) + 1
        files[frag.file] = files.get(frag.file, 0) + 1

    return {
        "total_fragments": len(scored),
        "buckets": buckets,
        "realms": dict(sorted(realms.items(), key=lambda x: x[1], reverse=True)),
        "classifications": dict(sorted(classes.items(), key=lambda x: x[1], reverse=True)),
        "files": dict(sorted(files.items(), key=lambda x: x[1], reverse=True)),
    }


def format_markdown(validation: dict[str, Any], scored: list[ScoredFragment], max_per_bucket: int) -> str:
    summary = summarize(scored)

    lines: list[str] = []
    lines.append("# SIGNALIS AI — Scored Source Validation")
    lines.append("")
    lines.append(f"- Source validation: `{validation.get('source_report', 'unknown')}`")
    lines.append(f"- Query: `{validation.get('query', 'unknown')}`")
    lines.append(f"- Total fragments: `{summary['total_fragments']}`")
    lines.append(f"- Critical evidence: `{summary['buckets'].get('critical', 0)}`")
    lines.append(f"- Supporting evidence: `{summary['buckets'].get('supporting', 0)}`")
    lines.append(f"- Noise evidence: `{summary['buckets'].get('noise', 0)}`")
    lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("This is a ranking layer over exact source fragments.")
    lines.append("")
    lines.append("Use `critical` first for investigation orchestration.")
    lines.append("Use `supporting` for UI/sync context.")
    lines.append("Use `noise` only when checking broad coverage.")
    lines.append("")

    for bucket in ["critical", "supporting", "noise"]:
        bucket_items = [f for f in scored if f.bucket == bucket]
        lines.append(f"## {bucket.title()} Evidence")
        lines.append("")
        if not bucket_items:
            lines.append("- none")
            lines.append("")
            continue

        for idx, frag in enumerate(bucket_items[:max_per_bucket], start=1):
            lines.append(f"### {idx}. `{frag.file}` lines `{frag.line_start}-{frag.line_end}`")
            lines.append("")
            lines.append(f"- Score: `{frag.score}`")
            lines.append(f"- Realm: `{frag.realm}`")
            lines.append(f"- Match: `{frag.match_type}` / `{frag.match_value}`")
            lines.append(f"- Classification: `{frag.classification}`")
            lines.append(f"- Reasons: {', '.join(frag.reasons)}")
            lines.append("")
            lines.append("```lua")
            lines.append(frag.snippet)
            lines.append("```")
            lines.append("")

        remaining = len(bucket_items) - max_per_bucket
        if remaining > 0:
            lines.append(f"_Omitted {remaining} lower-ranked `{bucket}` fragments._")
            lines.append("")

    lines.append("## File Evidence Counts")
    lines.append("")
    for file_path, count in summary["files"].items():
        lines.append(f"- `{file_path}`: `{count}`")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--max-per-bucket", type=int, default=25)
    args = parser.parse_args()

    validation_path = args.validation.resolve()
    validation = read_json(validation_path)

    scored = collect_fragments(validation)
    payload = {
        "source_validation": str(validation_path),
        "query": validation.get("query"),
        "summary": summarize(scored),
        "fragments": [asdict(f) for f in scored],
    }

    out_dir = args.out_dir.resolve() if args.out_dir else validation_path.parent
    stem = validation_path.stem
    if not stem.endswith("_scored"):
        stem = f"{stem}_scored"

    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"

    write_json(json_path, payload)
    write_text(md_path, format_markdown(validation, scored, args.max_per_bucket))

    print(f"Wrote scored validation json: {json_path}")
    print(f"Wrote scored validation report: {md_path}")
    print("")
    print("Summary:")
    for key, value in payload["summary"]["buckets"].items():
        print(f"  {key}: {value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())