#!/usr/bin/env python3
"""
SIGNALIS AI — Targeted Source Validator V1

Input:
  *_targeted_validation.json

Output:
  *_source_validation.json
  *_source_validation.md

Usage:
  python -m scripts.qdrant.validate_targeted_sources `
    --workspace E:/signalis_ai `
    --targeted investigations/validation/vendor_stale_price_label_after_purchase_validation_targeted_validation.json
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import yaml

@dataclass
class SourceHit:
    check_id: str
    hypothesis: str
    priority: str
    file: str
    resolved_path: str | None
    pattern: str
    line_start: int
    line_end: int
    snippet: str
    found: bool

def load_source_roots(config_path: Path) -> list[Path]:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    roots = config.get("source_roots", [])

    return [Path(root).resolve() for root in roots]

def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def resolve_file(source_roots: list[Path], file_path: str) -> Path | None:
    normalized = file_path.replace("\\", "/").lower()

    for root in source_roots:
        direct = root / file_path
        if direct.exists():
            return direct

    candidates: list[Path] = []

    for root in source_roots:
        candidates.extend(root.rglob("*.lua"))

    exact = [
        p for p in candidates
        if p.as_posix().lower().endswith(normalized)
    ]

    if exact:
        return exact[0]

    wanted_parts = normalized.split("/")
    scored: list[tuple[int, Path]] = []

    for path in candidates:
        parts = path.as_posix().lower().split("/")
        score = 0

        for wanted in wanted_parts:
            if wanted in parts:
                score += 1

        if parts[-1] == wanted_parts[-1]:
            score += 5

        if score > 0:
            scored.append((score, path))

    if not scored:
        return None

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def find_pattern_hits(lines: list[str], pattern: str, context: int) -> list[tuple[int, int, str]]:
    hits: list[tuple[int, int, str]] = []

    escaped = re.escape(pattern)
    regex = re.compile(escaped, re.IGNORECASE)

    for index, line in enumerate(lines):
        if not regex.search(line):
            continue

        start = max(0, index - context)
        end = min(len(lines), index + context + 1)

        snippet_lines = []
        for line_no in range(start, end):
            snippet_lines.append(f"{line_no + 1}: {lines[line_no]}")

        hits.append((start + 1, end, "\n".join(snippet_lines)))

    return hits


def validate_check(source_roots: list[Path], check: dict[str, Any], context: int, max_hits_per_pattern: int) -> list[SourceHit]:
    file_path = str(check.get("file", ""))
    resolved = resolve_file(source_roots, file_path)

    hits: list[SourceHit] = []

    if resolved is None:
        for pattern in check.get("required_patterns", []):
            hits.append(
                SourceHit(
                    check_id=str(check.get("check_id", "")),
                    hypothesis=str(check.get("hypothesis", "")),
                    priority=str(check.get("priority", "")),
                    file=file_path,
                    resolved_path=None,
                    pattern=str(pattern),
                    line_start=0,
                    line_end=0,
                    snippet="",
                    found=False,
                )
            )
        return hits

    lines = read_lines(resolved)

    for pattern in check.get("required_patterns", []):
        pattern_hits = find_pattern_hits(lines, str(pattern), context)

        if not pattern_hits:
            hits.append(
                SourceHit(
                    check_id=str(check.get("check_id", "")),
                    hypothesis=str(check.get("hypothesis", "")),
                    priority=str(check.get("priority", "")),
                    file=file_path,
                    resolved_path=str(resolved),
                    pattern=str(pattern),
                    line_start=0,
                    line_end=0,
                    snippet="",
                    found=False,
                )
            )
            continue

        for line_start, line_end, snippet in pattern_hits[:max_hits_per_pattern]:
            hits.append(
                SourceHit(
                    check_id=str(check.get("check_id", "")),
                    hypothesis=str(check.get("hypothesis", "")),
                    priority=str(check.get("priority", "")),
                    file=file_path,
                    resolved_path=str(resolved),
                    pattern=str(pattern),
                    line_start=line_start,
                    line_end=line_end,
                    snippet=snippet,
                    found=True,
                )
            )

    return hits


def summarize(hits: list[SourceHit]) -> dict[str, Any]:
    total = len(hits)
    found = len([h for h in hits if h.found])
    missing = total - found

    by_file: dict[str, dict[str, int]] = {}
    by_check: dict[str, dict[str, int]] = {}

    for hit in hits:
        by_file.setdefault(hit.file, {"found": 0, "missing": 0})
        by_check.setdefault(hit.check_id, {"found": 0, "missing": 0})

        key = "found" if hit.found else "missing"
        by_file[hit.file][key] += 1
        by_check[hit.check_id][key] += 1

    return {
        "total_pattern_results": total,
        "found": found,
        "missing": missing,
        "by_file": by_file,
        "by_check": by_check,
    }


def format_md(targeted_path: Path, payload: dict[str, Any], hits: list[SourceHit]) -> str:
    summary = summarize(hits)

    lines: list[str] = []
    lines.append("# SIGNALIS AI — Targeted Source Validation")
    lines.append("")
    lines.append(f"- Targeted plan: `{targeted_path}`")
    lines.append(f"- Query: `{payload.get('query', '')}`")
    lines.append(f"- Pattern results: `{summary['total_pattern_results']}`")
    lines.append(f"- Found: `{summary['found']}`")
    lines.append(f"- Missing: `{summary['missing']}`")
    lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("This report validates targeted hypothesis checks against exact source files.")
    lines.append("")
    lines.append("Use found patterns as source anchors. Missing patterns are not automatically bugs; they may mean the targeted plan expected the wrong file or naming.")
    lines.append("")

    lines.append("## File Summary")
    lines.append("")
    for file_path, counts in summary["by_file"].items():
        lines.append(f"- `{file_path}`: found `{counts['found']}`, missing `{counts['missing']}`")
    lines.append("")

    checks = payload.get("checks", [])
    check_lookup = {str(c.get("check_id", "")): c for c in checks}

    for check_id, counts in summary["by_check"].items():
        check = check_lookup.get(check_id, {})
        lines.append(f"## {check_id} — `{check.get('file', '')}`")
        lines.append("")
        lines.append(f"- Priority: `{check.get('priority', '')}`")
        lines.append(f"- Hypothesis: {check.get('hypothesis', '')}")
        lines.append(f"- Expected runtime relation: {check.get('expected_runtime_relation', '')}")
        lines.append(f"- Found: `{counts['found']}`")
        lines.append(f"- Missing: `{counts['missing']}`")
        lines.append("")

        check_hits = [h for h in hits if h.check_id == check_id]

        missing = [h for h in check_hits if not h.found]
        if missing:
            lines.append("### Missing Patterns")
            lines.append("")
            for hit in missing:
                lines.append(f"- `{hit.pattern}`")
            lines.append("")

        found = [h for h in check_hits if h.found]
        if found:
            lines.append("### Found Evidence")
            lines.append("")
            for idx, hit in enumerate(found, start=1):
                lines.append(f"#### {idx}. `{hit.pattern}` lines `{hit.line_start}-{hit.line_end}`")
                lines.append("")
                lines.append("```lua")
                lines.append(hit.snippet)
                lines.append("```")
                lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-config", type=Path, default=Path("workspace.yaml"))
    parser.add_argument("--targeted", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--context", type=int, default=6)
    parser.add_argument("--max-hits-per-pattern", type=int, default=5)
    args = parser.parse_args()

    source_roots = load_source_roots(args.workspace_config)
    targeted_path = args.targeted.resolve()
    payload = read_json(targeted_path)

    hits: list[SourceHit] = []

    for check in payload.get("checks", []):
        hits.extend(
            validate_check(
                source_roots=source_roots,
                check=check,
                context=args.context,
                max_hits_per_pattern=args.max_hits_per_pattern,
            )
        )

    out_dir = args.out_dir.resolve() if args.out_dir else targeted_path.parent

    stem = targeted_path.stem
    for suffix in ["_source_validation", "_targeted_validation"]:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]

    stem = f"{stem}_source_validation"

    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"

    output = {
        "source_targeted_validation": str(targeted_path),
        "query": payload.get("query"),
        "summary": summarize(hits),
        "hits": [asdict(h) for h in hits],
    }

    write_json(json_path, output)
    write_text(md_path, format_md(targeted_path, payload, hits))

    print(f"Wrote targeted source validation json: {json_path}")
    print(f"Wrote targeted source validation report: {md_path}")
    print("")
    print("Summary:")
    print(f"  found: {output['summary']['found']}")
    print(f"  missing: {output['summary']['missing']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())