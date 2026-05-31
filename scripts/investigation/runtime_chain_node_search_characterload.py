#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


NODES = Path("manifests/normalized/runtime_topology_nodes.json")
OUT_MD = Path("investigations/validation/runtime_chain_node_search_characterload_v1.md")

TERMS = [
    "CharacterLoaded",
    "PlayerLoadedChar",
    "PrePlayerLoadedChar",
    "PlayerLoadout",
    "PostPlayerLoadout",
    "inventoryOpen",
    "inventorySetPanelStatus",
    "nutInventoryInit",
    "nutInventoryAdd",
    "CreateNewInventoryPanel",
    "CreateInventoryPanel",
]


def text_of(node: dict) -> str:
    parts = []
    for key, value in node.items():
        if isinstance(value, (str, int, float, bool)):
            parts.append(f"{key}={value}")
        elif isinstance(value, list):
            parts.extend(str(v) for v in value if isinstance(v, (str, int, float, bool)))
        elif isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, (str, int, float, bool)):
                    parts.append(f"{k}={v}")
    return " ".join(parts)


def main() -> int:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)

    data = json.loads(NODES.read_text(encoding="utf-8"))
    if isinstance(data, list):
        nodes = data
    elif isinstance(data, dict):
        nodes = data.get("nodes", [])
    else:
        nodes = []

    lines: list[str] = [
        "# CharacterLoad Runtime Node Search",
        "",
        f"- Nodes scanned: `{len(nodes)}`",
        "",
    ]

    for term in TERMS:
        matches = []
        low = term.lower()

        for node in nodes:
            blob = text_of(node)
            if low in blob.lower():
                matches.append(node)

        lines += [
            f"## {term}",
            "",
            f"- Matches: `{len(matches)}`",
            "",
        ]

        for node in matches[:25]:
            node_id = node.get("id") or node.get("node_id") or node.get("key") or ""
            node_type = node.get("type") or node.get("node_type") or ""
            label = node.get("label") or node.get("name") or node.get("display") or ""
            file_path = node.get("file") or node.get("path") or node.get("source_file") or ""

            lines.append(f"- `{node_type}` | `{node_id}` | `{label}` | `{file_path}`")

        if len(matches) > 25:
            lines.append(f"- ... truncated `{len(matches) - 25}` more")

        lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote: {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())