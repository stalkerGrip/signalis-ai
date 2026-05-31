from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SOURCE_ROOT_KEYS = {
    "source_root",
    "source_roots",
    "raw_source_root",
    "raw_source_roots",
    "lua_root",
    "lua_roots",
    "schema_root",
    "schema_roots",
    "gamemode_root",
    "gamemode_roots",
}


def load_workspace_config(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "PyYAML is required to read workspace.yaml. Install with: pip install pyyaml"
        ) from exc

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if not isinstance(data, dict):
        raise SystemExit(f"workspace config must be a YAML mapping: {path}")

    return data


def collect_paths(value: Any) -> list[str]:
    paths: list[str] = []

    if isinstance(value, str):
        paths.append(value)

    elif isinstance(value, list):
        for item in value:
            paths.extend(collect_paths(item))

    elif isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key).lower()
            if key_text in SOURCE_ROOT_KEYS or "root" in key_text or "source" in key_text:
                paths.extend(collect_paths(child))
            else:
                paths.extend(collect_paths(child))

    return paths


def resolve_source_roots(config_path: Path, config: dict[str, Any]) -> list[Path]:
    config_dir = config_path.parent
    candidates = collect_paths(config)

    roots: list[Path] = []
    seen: set[str] = set()

    for raw in candidates:
        if not raw:
            continue

        path = Path(raw)

        if not path.is_absolute():
            path = (config_dir / path).resolve()

        if not path.exists() or not path.is_dir():
            continue

        key = str(path).lower()
        if key in seen:
            continue

        seen.add(key)
        roots.append(path)

    if not roots:
        raise SystemExit(
            f"No existing source roots found in {config_path}. "
            "Check config/workspace.yaml."
        )

    return roots


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def line_number_for_offset(text: str, offset: int) -> int:
    return text[:offset].count("\n") + 1


def extract_context(lines: list[str], line_no: int, radius: int = 8) -> str:
    start = max(1, line_no - radius)
    end = min(len(lines), line_no + radius)

    return "\n".join(
        f"{idx}: {lines[idx - 1]}"
        for idx in range(start, end + 1)
    )


def find_source_file(source_roots: list[Path], rel_path: str) -> Path | None:
    normalized = rel_path.replace("\\", "/")

    for root in source_roots:
        direct = root / normalized
        if direct.exists():
            return direct

    filename = Path(normalized).name
    suffix = normalized.lower()

    for root in source_roots:
        for match in root.rglob(filename):
            match_norm = str(match).replace("\\", "/").lower()
            if match_norm.endswith(suffix):
                return match

    return None


def validate_target(source_roots: list[Path], target: dict[str, Any]) -> dict[str, Any]:
    rel_path = target.get("path") or target.get("file") or target.get("source_file")

    if not rel_path:
        return {
            "target": target,
            "found": False,
            "error": "target missing path/file/source_file",
            "matches": [],
        }
    source_path = find_source_file(source_roots, rel_path)

    result: dict[str, Any] = {
        "path": rel_path,
        "resolved_path": str(source_path) if source_path else None,
        "exists": source_path is not None,
        "reason": target.get("reason", ""),
        "needles": [],
    }

    if source_path is None:
        return result

    text = read_text(source_path)
    lowered = text.lower()
    lines = text.splitlines()

    for needle in target.get("needles", []):
        needle_lower = str(needle).lower()
        offset = lowered.find(needle_lower)

        if offset < 0:
            result["needles"].append(
                {
                    "needle": needle,
                    "found": False,
                    "line": None,
                    "context": "",
                }
            )
            continue

        line_no = line_number_for_offset(text, offset)

        result["needles"].append(
            {
                "needle": needle,
                "found": True,
                "line": line_no,
                "context": extract_context(lines, line_no),
            }
        )

    return result


def build_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    files_total = len(results)
    files_found = sum(1 for r in results if r["exists"])
    needles_total = sum(len(r["needles"]) for r in results)
    needles_found = sum(
        1
        for r in results
        for n in r["needles"]
        if n["found"]
    )

    return {
        "files_total": files_total,
        "files_found": files_found,
        "needles_total": needles_total,
        "needles_found": needles_found,
        "all_needles_found": needles_total > 0 and needles_total == needles_found,
    }


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines: list[str] = []

    lines.append("# Targeted Validation Result")
    lines.append("")
    lines.append(f"Question: `{report.get('question', '')}`")
    lines.append(f"Chain: `{report.get('chain_name', '')}`")
    lines.append("")
    lines.append("## Workspace")
    lines.append("")
    lines.append(f"- Config: `{report['workspace_config']}`")
    lines.append("")
    lines.append("### Source Roots")
    lines.append("")
    for root in report["source_roots"]:
        lines.append(f"- `{root}`")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    for key, value in report["summary"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")

    lines.append("## Results")
    lines.append("")

    for result in report["results"]:
        lines.append(f"### `{result['path']}`")
        lines.append("")
        lines.append(f"- Exists: `{result['exists']}`")
        lines.append(f"- Resolved path: `{result.get('resolved_path')}`")
        lines.append(f"- Reason: {result.get('reason', '')}")
        lines.append("")

        for needle in result["needles"]:
            lines.append(f"#### `{needle['needle']}`")
            lines.append("")
            lines.append(f"- Found: `{needle['found']}`")
            lines.append(f"- Line: `{needle['line']}`")
            lines.append("")

            if needle["context"]:
                lines.append("```lua")
                lines.append(needle["context"])
                lines.append("```")
                lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace-config", required=True, type=Path)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    config = load_workspace_config(args.workspace_config)
    source_roots = resolve_source_roots(args.workspace_config, config)

    request = json.loads(args.request.read_text(encoding="utf-8"))

    results = [
        validate_target(source_roots, target)
        for target in request.get("targets", [])
    ]

    report = {
        "schema": "targeted_validation_result.v2",
        "source_request": str(args.request),
        "workspace_config": str(args.workspace_config),
        "source_roots": [str(path) for path in source_roots],
        "question": request.get("question", ""),
        "chain_name": request.get("chain_name", ""),
        "missing_steps": request.get("missing_steps", []),
        "summary": build_summary(results),
        "results": results,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(args.out_md, report)

    print(f"Wrote targeted validation JSON: {args.out_json}")
    print(f"Wrote targeted validation MD:   {args.out_md}")
    print("")
    for key, value in report["summary"].items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()