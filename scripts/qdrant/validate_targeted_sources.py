#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class ResolvedFile:
    requested: str
    resolved_path: str | None
    status: str
    candidates: list[str]


@dataclass
class SourceHit:
    check_id: str
    hypothesis: str
    priority: str
    file: str
    resolved_path: str | None
    resolution_status: str
    pattern: str
    line_start: int
    line_end: int
    snippet: str
    found: bool


def norm_path(value: str) -> str:
    return value.strip().strip("`'\"").replace("\\", "/").lstrip("./").lower()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def resolve_workspace_config(path: Path, workspace: Path | None) -> Path:
    candidates = [path]

    if workspace:
        candidates.extend([
            workspace / path,
            workspace / "config" / path.name,
        ])

    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    raise FileNotFoundError(f"Could not find workspace config: {path}")


def load_source_roots(config_path: Path, workspace: Path | None) -> list[Path]:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    roots = config.get("source_roots", [])

    resolved: list[Path] = []
    for root in roots:
        p = Path(str(root))
        if not p.is_absolute():
            base = workspace or config_path.parent
            p = base / p
        if p.exists():
            resolved.append(p.resolve())

    if workspace and workspace.exists():
        resolved.append(workspace.resolve())

    # preserve order, remove duplicates
    out: list[Path] = []
    seen: set[str] = set()
    for p in resolved:
        key = p.as_posix().lower()
        if key not in seen:
            seen.add(key)
            out.append(p)

    return out


class SourceIndex:
    def __init__(self, roots: list[Path]) -> None:
        self.roots = roots
        self.lua_files: list[Path] = []
        self.by_name: dict[str, list[Path]] = {}

        for root in roots:
            for path in root.rglob("*.lua"):
                if path.is_file():
                    self.lua_files.append(path.resolve())
                    self.by_name.setdefault(path.name.lower(), []).append(path.resolve())

    def resolve(self, file_path: str) -> ResolvedFile:
        requested = norm_path(file_path)
        raw = Path(file_path)

        if raw.is_absolute() and raw.exists():
            return ResolvedFile(file_path, str(raw.resolve()), "direct_absolute", [])

        for root in self.roots:
            direct = root / file_path
            if direct.exists():
                return ResolvedFile(file_path, str(direct.resolve()), "direct_root_join", [])

            direct_norm = root / requested
            if direct_norm.exists():
                return ResolvedFile(file_path, str(direct_norm.resolve()), "direct_normalized_join", [])

        suffix_matches = [
            p for p in self.lua_files
            if norm_path(p.as_posix()).endswith(requested)
        ]
        if len(suffix_matches) == 1:
            return ResolvedFile(file_path, str(suffix_matches[0]), "unique_suffix", [])
        if len(suffix_matches) > 1:
            return ResolvedFile(file_path, str(suffix_matches[0]), "ambiguous_suffix_first", [str(p) for p in suffix_matches[:10]])

        basename = Path(requested).name.lower()
        name_matches = self.by_name.get(basename, [])
        if len(name_matches) == 1:
            return ResolvedFile(file_path, str(name_matches[0]), "unique_basename", [])
        if len(name_matches) > 1:
            scored = sorted(
                ((tail_score(requested, norm_path(p.as_posix())), p) for p in name_matches),
                key=lambda x: x[0],
                reverse=True,
            )
            best_score, best = scored[0]
            if best_score > 0:
                return ResolvedFile(file_path, str(best), "basename_tail_score", [str(p) for _, p in scored[:10]])
            return ResolvedFile(file_path, None, "ambiguous_basename_unresolved", [str(p) for p in name_matches[:10]])

        return ResolvedFile(file_path, None, "unresolved", [])


def tail_score(requested: str, actual: str) -> int:
    req_parts = requested.split("/")
    act_parts = actual.split("/")
    score = 0

    for i in range(1, min(len(req_parts), len(act_parts)) + 1):
        if req_parts[-i] == act_parts[-i]:
            score += 10 * i
        else:
            break

    for part in req_parts:
        if part in act_parts:
            score += 1

    return score


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def find_pattern_hits(lines: list[str], pattern: str, context: int) -> list[tuple[int, int, str]]:
    hits: list[tuple[int, int, str]] = []
    regex = re.compile(re.escape(pattern), re.IGNORECASE)

    for index, line in enumerate(lines):
        if not regex.search(line):
            continue

        start = max(0, index - context)
        end = min(len(lines), index + context + 1)
        snippet = "\n".join(f"{i + 1}: {lines[i]}" for i in range(start, end))
        hits.append((start + 1, end, snippet))

    return hits


def validate_check(index: SourceIndex, check: dict[str, Any], context: int, max_hits: int) -> list[SourceHit]:
    file_path = str(check.get("file", ""))
    resolved = index.resolve(file_path)
    patterns = [str(p) for p in check.get("required_patterns", [])]

    hits: list[SourceHit] = []

    if not resolved.resolved_path:
        for pattern in patterns:
            hits.append(SourceHit(
                check_id=str(check.get("check_id", "")),
                hypothesis=str(check.get("hypothesis", "")),
                priority=str(check.get("priority", "")),
                file=file_path,
                resolved_path=None,
                resolution_status=resolved.status,
                pattern=pattern,
                line_start=0,
                line_end=0,
                snippet="",
                found=False,
            ))
        return hits

    lines = read_lines(Path(resolved.resolved_path))

    for pattern in patterns:
        pattern_hits = find_pattern_hits(lines, pattern, context)

        if not pattern_hits:
            hits.append(SourceHit(
                check_id=str(check.get("check_id", "")),
                hypothesis=str(check.get("hypothesis", "")),
                priority=str(check.get("priority", "")),
                file=file_path,
                resolved_path=resolved.resolved_path,
                resolution_status=resolved.status,
                pattern=pattern,
                line_start=0,
                line_end=0,
                snippet="",
                found=False,
            ))
            continue

        for line_start, line_end, snippet in pattern_hits[:max_hits]:
            hits.append(SourceHit(
                check_id=str(check.get("check_id", "")),
                hypothesis=str(check.get("hypothesis", "")),
                priority=str(check.get("priority", "")),
                file=file_path,
                resolved_path=resolved.resolved_path,
                resolution_status=resolved.status,
                pattern=pattern,
                line_start=line_start,
                line_end=line_end,
                snippet=snippet,
                found=True,
            ))

    return hits


def summarize(hits: list[SourceHit]) -> dict[str, Any]:
    found = sum(1 for h in hits if h.found)
    missing = len(hits) - found

    requested_files = sorted({h.file for h in hits})
    resolved_files = sorted({h.resolved_path for h in hits if h.resolved_path})
    unresolved_files = sorted({h.file for h in hits if not h.resolved_path})

    duplicate_keys: set[tuple[str, str, int, int]] = set()
    duplicates = 0
    for h in hits:
        if not h.found:
            continue
        key = (h.resolved_path or "", h.pattern, h.line_start, h.line_end)
        if key in duplicate_keys:
            duplicates += 1
        duplicate_keys.add(key)

    causal_terms = [
        "hook.Run", "netstream.Start", "net.Receive", "inventory:add", "removeItem",
        "setData", "sync", "ItemDataChanged", "InventoryDataChanged", "SetUpPanel",
    ]
    causal = sum(1 for h in hits if h.found and any(t.lower() in h.snippet.lower() for t in causal_terms))

    return {
        "pattern_results_total": len(hits),
        "found": found,
        "missing": missing,
        "requested_files": len(requested_files),
        "resolved_files": len(resolved_files),
        "unresolved_files": unresolved_files,
        "duplicate_fragments": duplicates,
        "causal_fragments": causal,
        "quality": {
            "resolution_rate": round(len(resolved_files) / max(1, len(requested_files)), 3),
            "pattern_hit_rate": round(found / max(1, len(hits)), 3),
            "causal_hit_rate": round(causal / max(1, found), 3),
        },
    }


def format_md(targeted_path: Path, payload: dict[str, Any], hits: list[SourceHit]) -> str:
    s = summarize(hits)
    lines = [
        "# SIGNALIS AI — Targeted Source Validation",
        "",
        f"- Targeted plan: `{targeted_path}`",
        f"- Query: `{payload.get('query', '')}`",
        f"- Pattern results: `{s['pattern_results_total']}`",
        f"- Found: `{s['found']}`",
        f"- Missing: `{s['missing']}`",
        f"- Requested files: `{s['requested_files']}`",
        f"- Resolved files: `{s['resolved_files']}`",
        f"- Duplicate fragments: `{s['duplicate_fragments']}`",
        f"- Causal fragments: `{s['causal_fragments']}`",
        f"- Resolution rate: `{s['quality']['resolution_rate']}`",
        f"- Pattern hit rate: `{s['quality']['pattern_hit_rate']}`",
        f"- Causal hit rate: `{s['quality']['causal_hit_rate']}`",
        "",
    ]

    if s["unresolved_files"]:
        lines += ["## Unresolved Files", ""]
        for f in s["unresolved_files"]:
            lines.append(f"- `{f}`")
        lines.append("")

    checks = payload.get("checks", [])
    check_lookup = {str(c.get("check_id", "")): c for c in checks}

    for check_id in sorted({h.check_id for h in hits}):
        check = check_lookup.get(check_id, {})
        check_hits = [h for h in hits if h.check_id == check_id]
        found = [h for h in check_hits if h.found]
        missing = [h for h in check_hits if not h.found]

        lines += [
            f"## {check_id} — `{check.get('file', '')}`",
            "",
            f"- Priority: `{check.get('priority', '')}`",
            f"- Hypothesis: {check.get('hypothesis', '')}",
            f"- Expected runtime relation: {check.get('expected_runtime_relation', '')}",
            f"- Resolution: `{check_hits[0].resolution_status if check_hits else ''}`",
            f"- Found: `{len(found)}`",
            f"- Missing: `{len(missing)}`",
            "",
        ]

        if missing:
            lines += ["### Missing Patterns", ""]
            for h in missing:
                lines.append(f"- `{h.pattern}`")
            lines.append("")

        if found:
            lines += ["### Found Evidence", ""]
            for i, h in enumerate(found, 1):
                lines += [
                    f"#### {i}. `{h.pattern}` lines `{h.line_start}-{h.line_end}`",
                    "",
                    "```lua",
                    h.snippet,
                    "```",
                    "",
                ]

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, default=None)
    parser.add_argument("--workspace-config", type=Path, default=Path("workspace.yaml"))
    parser.add_argument("--targeted", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--context", type=int, default=6)
    parser.add_argument("--max-hits-per-pattern", type=int, default=5)
    args = parser.parse_args()

    workspace = args.workspace.resolve() if args.workspace else None
    config_path = resolve_workspace_config(args.workspace_config, workspace)
    source_roots = load_source_roots(config_path, workspace)
    index = SourceIndex(source_roots)

    targeted_path = args.targeted.resolve()
    payload = read_json(targeted_path)

    hits: list[SourceHit] = []
    for check in payload.get("checks", []):
        hits.extend(validate_check(index, check, args.context, args.max_hits_per_pattern))

    out_dir = args.out_dir.resolve() if args.out_dir else targeted_path.parent

    stem = targeted_path.stem
    for suffix in ["_source_validation", "_targeted_validation"]:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    stem = f"{stem}_source_validation"

    output = {
        "source_targeted_validation": str(targeted_path),
        "query": payload.get("query"),
        "summary": summarize(hits),
        "hits": [asdict(h) for h in hits],
    }

    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"

    write_json(json_path, output)
    write_text(md_path, format_md(targeted_path, payload, hits))

    print(f"Wrote targeted source validation json: {json_path}")
    print(f"Wrote targeted source validation report: {md_path}")
    print("")
    print("Summary:")
    for k, v in output["summary"].items():
        if k != "quality":
            print(f"  {k}: {v}")
    print(f"  quality: {output['summary']['quality']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())