#!/usr/bin/env python3
"""
SIGNALIS AI — Validation Fragment Deduplication

Input:
  investigations/validation/*_validation.json
  or
  investigations/validation/*_validation_scored.json

Output:
  *_deduped.json
  *_deduped.md

Purpose:
  Collapse overlapping validation fragments into unique evidence groups.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class EvidenceGroup:
    file: str
    realm: str
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


def normalize_snippet(snippet: str) -> str:
    lines = []
    for raw in snippet.splitlines():
        # remove line numbers emitted by validate_sources.py: "  215: code"
        line = re.sub(r"^\s*\d+\s*:\s*", "", raw)
        line = line.strip()
        if line:
            lines.append(line)
    return "\n".join(lines)


def content_hash(snippet: str) -> str:
    text = normalize_snippet(snippet)
    return hashlib.sha1(text.encode("utf-8", errors="replace")).hexdigest()[:12]


def ranges_overlap_or_touch(a_start: int, a_end: int, b_start: int, b_end: int, tolerance: int) -> bool:
    return not (a_end + tolerance < b_start or b_end + tolerance < a_start)


def extract_fragments(payload: dict[str, Any]) -> list[dict[str, Any]]:
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


def should_merge(a: EvidenceGroup, frag: dict[str, Any], tolerance: int) -> bool:
    if normalize_file(a.file) != normalize_file(str(frag.get("file", ""))):
        return False

    if a.match_type != str(frag.get("match_type", "")):
        return False

    if a.classification != str(frag.get("classification", "")):
        return False

    # Same semantic target or same overlapping location is enough.
    same_match = normalize_match_value(a.match_value) == normalize_match_value(str(frag.get("match_value", "")))

    f_start = int(frag.get("line_start", 0))
    f_end = int(frag.get("line_end", 0))
    overlapping = ranges_overlap_or_touch(a.line_start, a.line_end, f_start, f_end, tolerance)

    return same_match and overlapping


def merge_fragment(group: EvidenceGroup, frag: dict[str, Any]) -> None:
    group.line_start = min(group.line_start, int(frag.get("line_start", group.line_start)))
    group.line_end = max(group.line_end, int(frag.get("line_end", group.line_end)))
    group.score = max(group.score, fragment_score(frag))
    group.duplicate_count += 1
    group.source_fragments.append(frag)

    for reason in fragment_reasons(frag):
        if reason not in group.reasons:
            group.reasons.append(reason)

    # Keep highest scoring snippet as representative.
    if fragment_score(frag) >= group.score:
        group.snippet = str(frag.get("snippet", group.snippet))

    # Promote bucket if any duplicate is stronger.
    bucket_rank = {"noise": 0, "supporting": 1, "critical": 2, "unscored": -1}
    current = bucket_rank.get(group.bucket, -1)
    incoming = bucket_rank.get(fragment_bucket(frag), -1)
    if incoming > current:
        group.bucket = fragment_bucket(frag)


def make_group(frag: dict[str, Any]) -> EvidenceGroup:
    return EvidenceGroup(
        file=str(frag.get("file", "")),
        realm=str(frag.get("realm", "")),
        match_type=str(frag.get("match_type", "")),
        match_value=str(frag.get("match_value", "")),
        classification=str(frag.get("classification", "")),
        line_start=int(frag.get("line_start", 0)),
        line_end=int(frag.get("line_end", 0)),
        score=fragment_score(frag),
        bucket=fragment_bucket(frag),
        duplicate_count=1,
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

    for g in groups:
        buckets[g.bucket] = buckets.get(g.bucket, 0) + 1
        files[g.file] = files.get(g.file, 0) + 1
        classes[g.classification] = classes.get(g.classification, 0) + 1

    return {
        "original_fragments": original_count,
        "deduped_evidence": len(groups),
        "removed_duplicates": original_count - len(groups),
        "buckets": dict(sorted(buckets.items(), key=lambda x: x[1], reverse=True)),
        "files": dict(sorted(files.items(), key=lambda x: x[1], reverse=True)),
        "classifications": dict(sorted(classes.items(), key=lambda x: x[1], reverse=True)),
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

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--line-tolerance", type=int, default=3)
    parser.add_argument("--max-items", type=int, default=50)
    args = parser.parse_args()

    source = args.validation.resolve()
    payload = read_json(source)
    fragments = extract_fragments(payload)

    groups = deduplicate(fragments, args.line_tolerance)
    summary = summarize(groups, len(fragments))

    out_dir = args.out_dir.resolve() if args.out_dir else source.parent
    stem = source.stem
    if stem.endswith("_scored"):
        stem = stem[:-7]
    if not stem.endswith("_deduped"):
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
    for k, v in summary.items():
        if isinstance(v, dict):
            continue
        print(f"  {k}: {v}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())