from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    ".qdrant",
    "qdrant_storage",
}

IMPORTANT_PATTERNS = [
    "*topology*.json",
    "*runtime*.json",
    "*qdrant*.jsonl",
    "*qdrant*.md",
    "*summary*.md",
    "*doctrine*.md",
    "*taxonomy*.md",
    "*model*.md",
    "*intent*.py",
    "*rerank*.py",
    "*context_pack*.py",
    "*subsystem*.py",
]


def should_skip(path: Path, workspace: Path) -> bool:
    rel_parts = path.relative_to(workspace).parts
    return any(part in DEFAULT_EXCLUDE_DIRS for part in rel_parts)


def list_dirs(workspace: Path, max_depth: int) -> list[Path]:
    result = []

    for path in workspace.rglob("*"):
        if not path.is_dir():
            continue
        if should_skip(path, workspace):
            continue

        rel = path.relative_to(workspace)
        if len(rel.parts) <= max_depth:
            result.append(path)

    return sorted(result)


def list_matching_files(workspace: Path) -> list[Path]:
    found: set[Path] = set()

    for pattern in IMPORTANT_PATTERNS:
        for path in workspace.rglob(pattern):
            if path.is_file() and not should_skip(path, workspace):
                found.add(path)

    return sorted(found)


def find_known_paths(workspace: Path) -> dict[str, list[Path]]:
    groups = {
        "Runtime Topology Files": list(workspace.rglob("*topology*.json")),
        "Qdrant Files": list(workspace.rglob("*qdrant*")),
        "Investigation Files": list((workspace / "investigations").rglob("*")) if (workspace / "investigations").exists() else [],
        "Subsystem Docs": list((workspace / "docs" / "subsystems").rglob("*.md")) if (workspace / "docs" / "subsystems").exists() else [],
        "Qdrant Scripts": list((workspace / "scripts" / "qdrant").rglob("*.py")) if (workspace / "scripts" / "qdrant").exists() else [],
        "Semantic Scripts": list((workspace / "scripts" / "semantic").rglob("*.py")) if (workspace / "scripts" / "semantic").exists() else [],
    }

    return {
        name: sorted([p for p in paths if p.exists() and not should_skip(p, workspace)])
        for name, paths in groups.items()
    }


def rel(path: Path, workspace: Path) -> str:
    return str(path.relative_to(workspace)).replace("\\", "/")


def render_project_structure(workspace: Path, max_depth: int) -> str:
    now = datetime.now().isoformat(timespec="seconds")

    dirs = list_dirs(workspace, max_depth)
    important_files = list_matching_files(workspace)
    known_groups = find_known_paths(workspace)

    lines: list[str] = [
        "# SIGNALIS AI — Project Structure",
        "",
        f"Generated: `{now}`",
        "",
        "## Workspace",
        "",
        "```text",
        str(workspace).replace("\\", "/"),
        "```",
        "",
        "## Directory Tree",
        "",
        "```text",
    ]

    for directory in dirs:
        depth = len(directory.relative_to(workspace).parts)
        indent = "  " * max(depth - 1, 0)
        lines.append(f"{indent}{directory.name}/")

    lines.extend([
        "```",
        "",
        "## Known Important Paths",
        "",
    ])

    for group_name, paths in known_groups.items():
        lines.append(f"### {group_name}")
        lines.append("")

        if not paths:
            lines.append("- none found")
        else:
            for path in paths:
                if path.is_file():
                    size_kb = path.stat().st_size / 1024
                    lines.append(f"- `{rel(path, workspace)}` ({size_kb:.1f} KB)")
                else:
                    lines.append(f"- `{rel(path, workspace)}/`")

        lines.append("")

    lines.extend([
        "## Important Matched Files",
        "",
    ])

    if not important_files:
        lines.append("- none found")
    else:
        for path in important_files[:300]:
            size_kb = path.stat().st_size / 1024
            lines.append(f"- `{rel(path, workspace)}` ({size_kb:.1f} KB)")

    lines.extend([
        "",
        "## Active Investigation",
        "",
        "```text",
        "inventory desync after character load",
        "```",
        "",
        "## Current Runtime Chain Under Investigation",
        "",
        "```text",
        "CharacterLoaded",
        "→ PlayerLoadedChar",
        "→ PlayerLoadout",
        "→ PostPlayerLoadout",
        "→ inventory initialization / sync",
        "→ inventoryOpen",
        "→ inventorySetPanelStatus",
        "→ client inventory UI",
        "```",
        "",
        "## Notes",
        "",
        "This file is generated on demand. Re-run this script after adding scripts, manifests, subsystem docs, or investigation reports.",
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate SIGNALIS AI project structure manifest.")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--output", default="project_structure.md")
    parser.add_argument("--max-depth", type=int, default=4)

    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    output = Path(args.output)

    if not output.is_absolute():
        output = workspace / output

    report = render_project_structure(workspace, args.max_depth)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")

    print(f"Wrote project structure to: {output}")


if __name__ == "__main__":
    main()