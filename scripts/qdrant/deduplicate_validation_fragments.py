#!/usr/bin/env python3
"""
SIGNALIS AI — Validation Fragment Deduplication V2

Purpose:
  Collapse overlapping validation fragments into unique evidence groups.

Adds:
  - line overlap dedup
  - semantic target dedup
  - hook/net/function/data-operation target extraction

Usage:
  python -m scripts.qdrant.deduplicate_validation_fragments `
    --validation investigations/validation/vendor_stale_price_label_after_purchase_validation_scored.json
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


BUCKET_RANK = {
    "noise": 0,
    "supporting": 1,
    "critical": 2,
    "unscored": -1,
}


@dataclass
class EvidenceGroup:
    file: str
    realm: str
    semantic_target: str
    match_type: str
    match_value: str
    classification: str
    line_start: int
    line_end: int
    score: int
    bucket: str
    duplicate_count: int
    reasons: list[str]
    snippet: str
    source_fragments: list[dict[str, Any]]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def normalize_file(path: str) -> str:
    return path.replace("\\", "/").strip().lower()


def normalize_match_value(value: str) -> str:
    return re.sub(r"\s+", "", value or "").lower()


def strip_line_numbers(snippet: str) -> str:
    lines: list[str] = []
    for raw in snippet.splitlines():
        line = re.sub(r"^\s*\d+\s*:\s*", "", raw)
        lines.append(line)
    return "\n".join(lines)


def clean_target(value: str) -> str:
    return value.strip().replace('"', "").replace("'", "")


def extract_semantic_target(fragment: dict[str, Any]) -> str:
    snippet = strip_line_numbers(str(fragment.get("snippet", "")))
    match_type = str(fragment.get("match_type", ""))
    match_value = str(fragment.get("match_value", ""))

    # Prefer explicit hook/network/data targets.
    priority_patterns = [
        (r'hook\.Run\s*\(\s*["\']([^"\']+)["\']', "hook"),
        (r'hook\.Add\s*\(\s*["\']([^"\']+)["\']', "hook"),
        (r'net\.Receive\s*\(\s*["\']([^"\']+)["\']', "net"),
        (r'net\.Start\s*\(\s*["\']([^"\']+)["\']', "net"),
        (r'netstream\.Hook\s*\(\s*["\']([^"\']+)["\']', "netstream"),
        (r'netstream\.Start\s*\([^,\n]+,\s*["\']([^"\']+)["\']', "netstream"),
        (r'netstream\.Start\s*\(\s*["\']([^"\']+)["\']', "netstream"),
        (r'addNetHandler\s*\(\s*["\']([^"\']+)["\']', "vendor_net_handler"),
        (r':setData\s*\(\s*["\']([^"\']+)["\']', "item_data"),
        (r':SetData\s*\(\s*["\']([^"\']+)["\']', "item_data"),
        (r'\bsetData\s*\(\s*["\']([^"\']+)["\']', "item_data"),
        (r'\bSetData\s*\(\s*["\']([^"\']+)["\']', "item_data"),
        (r':getData\s*\(\s*["\']([^"\']+)["\']', "item_data_read"),
        (r':GetData\s*\(\s*["\']([^"\']+)["\']', "item_data_read"),
        (r':(updatePrice)\s*\(', "ui_call"),
        (r'\b(updatePrice)\s*\(', "ui_call"),
    ]

    for pattern, prefix in priority_patterns:
        match = re.search(pattern, snippet)
        if match:
            return f"{prefix}:{clean_target(match.group(1))}"

    # Function target fallback:
    # choose the nearest function declaration BEFORE the matched line range,
    # not a later function that appears after the evidence.
    function_patterns = [
        r'function\s+([A-Za-z_][\w\.]*:[A-Za-z_][\w]*)\s*\(',
        r'function\s+([A-Za-z_][\w\.]*)\s*\(',
        r'([A-Za-z_][\w\.]*:[A-Za-z_][\w]*)\s*=\s*function\s*\(',
    ]

    line_start = int(fragment.get("line_start", 0))
    best_function: str | None = None
    best_line = -1

    for raw in str(fragment.get("snippet", "")).splitlines():
        line_match = re.match(r"^\s*(\d+)\s*:\s*(.*)$", raw)
        if line_match:
            source_line = int(line_match.group(1))
            code = line_match.group(2)
        else:
            source_line = 0
            code = raw

        if source_line > line_start:
            continue

        for pattern in function_patterns:
            fn_match = re.search(pattern, code)
            if fn_match and source_line >= best_line:
                best_function = clean_target(fn_match.group(1))
                best_line = source_line

    if best_function:
        return f"function:{best_function}"

    if match_type in {"hook", "network"} and match_value:
        return f"{match_type}:{clean_target(match_value)}"

    if match_value:
        return f"{match_type}:{clean_target(match_value)}"

    return "unknown"


def extract_fragments(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if "evidence" in payload:
        return list(payload["evidence"])

    if "fragments" in payload:
        return list(payload["fragments"])

    fragments: list[dict[str, Any]] = []
    for file_entry in payload.get("files", []):
        for frag in file_entry.get("fragments", []):
            fragments.append(frag)
    return fragments


def fragment_score(frag: dict[str, Any]) -> int:
    return int(frag.get("score", 0))


def fragment_bucket(frag: dict[str, Any]) -> str:
    return str(frag.get("bucket", "unscored"))


def fragment_reasons(frag: dict[str, Any]) -> list[str]:
    reasons = frag.get("reasons", [])
    if isinstance(reasons, list):
        return [str(r) for r in reasons]
    return []


def ranges_overlap_or_touch(a_start: int, a_end: int, b_start: int, b_end: int, tolerance: int) -> bool:
    return not (a_end + tolerance < b_start or b_end + tolerance < a_start)


def same_file(a: EvidenceGroup, frag: dict[str, Any]) -> bool:
    return normalize_file(a.file) == normalize_file(str(frag.get("file", "")))


def should_merge(group: EvidenceGroup, frag: dict[str, Any], tolerance: int) -> bool:
    if not same_file(group, frag):
        return False

    incoming_target = extract_semantic_target(frag)

    f_start = int(frag.get("line_start", 0))
    f_end = int(frag.get("line_end", 0))

    overlapping = ranges_overlap_or_touch(
        group.line_start,
        group.line_end,
        f_start,
        f_end,
        tolerance,
    )

    same_semantic_target = (
        group.semantic_target != "unknown"
        and incoming_target != "unknown"
        and group.semantic_target == incoming_target
    )

    same_match = (
        group.match_type == str(frag.get("match_type", ""))
        and group.classification == str(frag.get("classification", ""))
        and normalize_match_value(group.match_value)
        == normalize_match_value(str(frag.get("match_value", "")))
    )

    # Strong merge:
    # Same file + same semantic target + nearby or overlapping.
    if same_semantic_target and overlapping:
        return True

    # Fallback old behavior.
    if same_match and overlapping:
        return True

    return False


def merge_fragment(group: EvidenceGroup, frag: dict[str, Any]) -> None:
    group.line_start = min(group.line_start, int(frag.get("line_start", group.line_start)))
    group.line_end = max(group.line_end, int(frag.get("line_end", group.line_end)))
    group.duplicate_count += int(frag.get("duplicate_count", 1))
    group.source_fragments.append(frag)

    incoming_score = fragment_score(frag)

    if incoming_score > group.score:
        group.score = incoming_score
        group.snippet = str(frag.get("snippet", group.snippet))
        group.match_type = str(frag.get("match_type", group.match_type))
        group.match_value = str(frag.get("match_value", group.match_value))
        group.classification = str(frag.get("classification", group.classification))

    for reason in fragment_reasons(frag):
        if reason not in group.reasons:
            group.reasons.append(reason)

    incoming_bucket = fragment_bucket(frag)
    if BUCKET_RANK.get(incoming_bucket, -1) > BUCKET_RANK.get(group.bucket, -1):
        group.bucket = incoming_bucket


def make_group(frag: dict[str, Any]) -> EvidenceGroup:
    return EvidenceGroup(
        file=str(frag.get("file", "")),
        realm=str(frag.get("realm", "")),
        semantic_target=extract_semantic_target(frag),
        match_type=str(frag.get("match_type", "")),
        match_value=str(frag.get("match_value", "")),
        classification=str(frag.get("classification", "")),
        line_start=int(frag.get("line_start", 0)),
        line_end=int(frag.get("line_end", 0)),
        score=fragment_score(frag),
        bucket=fragment_bucket(frag),
        duplicate_count=int(frag.get("duplicate_count", 1)),
        reasons=fragment_reasons(frag),
        snippet=str(frag.get("snippet", "")),
        source_fragments=[frag],
    )


def deduplicate(fragments: list[dict[str, Any]], tolerance: int) -> list[EvidenceGroup]:
    groups: list[EvidenceGroup] = []

    ordered = sorted(
        fragments,
        key=lambda f: (
            normalize_file(str(f.get("file", ""))),
            extract_semantic_target(f),
            int(f.get("line_start", 0)),
            int(f.get("line_end", 0)),
            str(f.get("classification", "")),
            str(f.get("match_type", "")),
        ),
    )

    for frag in ordered:
        merged = False

        for group in groups:
            if should_merge(group, frag, tolerance):
                merge_fragment(group, frag)
                merged = True
                break

        if not merged:
            groups.append(make_group(frag))

    groups.sort(key=lambda g: (g.score, g.duplicate_count), reverse=True)
    return groups


def summarize(groups: list[EvidenceGroup], original_count: int) -> dict[str, Any]:
    buckets: dict[str, int] = {}
    files: dict[str, int] = {}
    classes: dict[str, int] = {}
    targets: dict[str, int] = {}

    for g in groups:
        buckets[g.bucket] = buckets.get(g.bucket, 0) + 1
        files[g.file] = files.get(g.file, 0) + 1
        classes[g.classification] = classes.get(g.classification, 0) + 1
        targets[g.semantic_target] = targets.get(g.semantic_target, 0) + 1

    return {
        "original_fragments": original_count,
        "deduped_evidence": len(groups),
        "removed_duplicates": original_count - len(groups),
        "buckets": dict(sorted(buckets.items(), key=lambda x: x[1], reverse=True)),
        "files": dict(sorted(files.items(), key=lambda x: x[1], reverse=True)),
        "classifications": dict(sorted(classes.items(), key=lambda x: x[1], reverse=True)),
        "semantic_targets": dict(sorted(targets.items(), key=lambda x: x[1], reverse=True)),
    }


def format_md(source_path: Path, payload: dict[str, Any], groups: list[EvidenceGroup], max_items: int) -> str:
    summary = summarize(groups, len(extract_fragments(payload)))

    lines: list[str] = []
    lines.append("# SIGNALIS AI — Deduplicated Validation Evidence")
    lines.append("")
    lines.append(f"- Source: `{source_path}`")
    lines.append(f"- Query: `{payload.get('query', 'unknown')}`")
    lines.append(f"- Original fragments: `{summary['original_fragments']}`")
    lines.append(f"- Deduped evidence: `{summary['deduped_evidence']}`")
    lines.append(f"- Removed duplicates: `{summary['removed_duplicates']}`")
    lines.append("")
    lines.append("## Evidence")
    lines.append("")

    for idx, g in enumerate(groups[:max_items], start=1):
        lines.append(f"### {idx}. `{g.file}` lines `{g.line_start}-{g.line_end}`")
        lines.append("")
        lines.append(f"- Bucket: `{g.bucket}`")
        lines.append(f"- Score: `{g.score}`")
        lines.append(f"- Realm: `{g.realm}`")
        lines.append(f"- Semantic target: `{g.semantic_target}`")
        lines.append(f"- Classification: `{g.classification}`")
        lines.append(f"- Match: `{g.match_type}` / `{g.match_value}`")
        lines.append(f"- Duplicate count: `{g.duplicate_count}`")
        if g.reasons:
            lines.append(f"- Reasons: {', '.join(g.reasons)}")
        lines.append("")
        lines.append("```lua")
        lines.append(g.snippet)
        lines.append("```")
        lines.append("")

    omitted = len(groups) - max_items
    if omitted > 0:
        lines.append(f"_Omitted {omitted} lower-ranked deduped evidence groups._")
        lines.append("")

    lines.append("## File Counts")
    lines.append("")
    for file_path, count in summary["files"].items():
        lines.append(f"- `{file_path}`: `{count}`")

    lines.append("")
    lines.append("## Semantic Target Counts")
    lines.append("")
    for target, count in summary["semantic_targets"].items():
        lines.append(f"- `{target}`: `{count}`")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--line-tolerance", type=int, default=8)
    parser.add_argument("--max-items", type=int, default=50)
    args = parser.parse_args()

    source = args.validation.resolve()
    payload = read_json(source)
    fragments = extract_fragments(payload)

    groups = deduplicate(fragments, args.line_tolerance)
    summary = summarize(groups, len(fragments))

    out_dir = args.out_dir.resolve() if args.out_dir else source.parent
    stem = source.stem

    for suffix in ["_deduped", "_scored"]:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]

    stem = f"{stem}_deduped"

    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"

    output = {
        "source": str(source),
        "query": payload.get("query"),
        "summary": summary,
        "evidence": [asdict(g) for g in groups],
    }

    write_json(json_path, output)
    write_text(md_path, format_md(source, payload, groups, args.max_items))

    print(f"Wrote deduped json: {json_path}")
    print(f"Wrote deduped report: {md_path}")
    print("")
    print("Summary:")
    print(f"  original_fragments: {summary['original_fragments']}")
    print(f"  deduped_evidence: {summary['deduped_evidence']}")
    print(f"  removed_duplicates: {summary['removed_duplicates']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())