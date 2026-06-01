from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


LINE_RE = re.compile(r"(.+?\.lua):(\d+)")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def edge_source(edge: dict[str, Any]) -> str | None:
    return edge.get("source") or edge.get("from") or edge.get("src")


def edge_target(edge: dict[str, Any]) -> str | None:
    return edge.get("target") or edge.get("to") or edge.get("dst")


def edge_type(edge: dict[str, Any]) -> str:
    return edge.get("type") or edge.get("edge_type") or edge.get("relation") or "unknown"


def normalize_path(value: str | None) -> str | None:
    if not value:
        return None
    return value.replace("\\", "/").strip().lower()


def parse_file_line(*values: str | None) -> tuple[str | None, int | None, str | None]:
    for value in values:
        if not value:
            continue

        normalized = value.replace("\\", "/")
        matches = LINE_RE.findall(normalized)

        if matches:
            file_path, line = matches[-1]
            return normalize_path(file_path), int(line), value

    return None, None, None


def node_type(nodes_by_id: dict[str, dict[str, Any]], node_id: str | None) -> str:
    if not node_id:
        return ""
    node = nodes_by_id.get(node_id, {})
    return node.get("type") or node.get("node_type") or ""


def node_name(nodes_by_id: dict[str, dict[str, Any]], node_id: str | None) -> str:
    if not node_id:
        return ""
    node = nodes_by_id.get(node_id, {})
    return node.get("name") or node.get("label") or node_id


def node_file_line(nodes_by_id: dict[str, dict[str, Any]], node_id: str) -> tuple[str | None, int | None, str | None]:
    node = nodes_by_id.get(node_id, {})

    candidates = [
        node_id,
        str(node.get("name") or ""),
        str(node.get("label") or ""),
        str(node.get("file") or ""),
        str(node.get("path") or ""),
        str(node.get("source") or ""),
    ]

    return parse_file_line(*candidates)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-topology", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--max-forward-lines", type=int, default=120)
    parser.add_argument("--max-backward-lines", type=int, default=5)
    parser.add_argument("--focus-file", default="")
    args = parser.parse_args()

    topology = load_json(args.runtime_topology)

    nodes = [n for n in topology.get("nodes", []) if n.get("id")]
    edges = topology.get("edges", [])
    nodes_by_id = {n["id"]: n for n in nodes}

    normalized_edges: list[dict[str, Any]] = []
    for idx, edge in enumerate(edges):
        src = edge_source(edge)
        dst = edge_target(edge)
        if not src or not dst:
            continue
        normalized_edges.append(
            {
                "source": src,
                "target": dst,
                "type": edge_type(edge),
                "source_edge": idx,
                "raw": edge,
            }
        )

    emitters_by_file: dict[str, list[tuple[str, str, int | None, str | None]]] = defaultdict(list)

    for edge in normalized_edges:
        src = edge["source"]
        dst = edge["target"]

        if edge["type"] not in {"emits", "emits_event"}:
            continue

        if node_type(nodes_by_id, src) != "hook_emitter":
            continue

        if node_type(nodes_by_id, dst) != "hook_event":
            continue

        file_path, line, parsed_from = node_file_line(nodes_by_id, src)
        if file_path:
            emitters_by_file[file_path].append((src, dst, line, parsed_from))

    callbacks: list[tuple[str, str, str | None, int | None, str | None]] = []

    for node in nodes:
        node_id = node["id"]
        ntype = node_type(nodes_by_id, node_id)

        if ntype not in {"hook_listener", "network_operation"}:
            continue

        file_path, line, parsed_from = node_file_line(nodes_by_id, node_id)
        callbacks.append((node_id, ntype, file_path, line, parsed_from))

    focus = normalize_path(args.focus_file) if args.focus_file else ""

    lines = [
        "# Runtime Propagation V3 Bridge Debug",
        "",
        f"- Runtime topology: `{args.runtime_topology}`",
        f"- Nodes: `{len(nodes)}`",
        f"- Edges: `{len(edges)}`",
        f"- Callback candidates: `{len(callbacks)}`",
        f"- Files with hook emitters: `{len(emitters_by_file)}`",
        f"- Max forward lines: `{args.max_forward_lines}`",
        f"- Max backward lines: `{args.max_backward_lines}`",
        f"- Focus file: `{focus or 'none'}`",
        "",
    ]

    target_ids = {
        "netmsg:netstream:invData",
        "netop:hook:netstream:invData:gamemode/core/libs/item/cl_networking.lua:13:249",
        "hook:ItemDataChanged",
        "hook:PlayerLoadedChar",
        "hook:PlayerLoadout",
        "hook:PostPlayerLoadout",
    }

    lines += ["## Target Node Location Parse", ""]

    for node_id in sorted(target_ids):
        found = node_id in nodes_by_id
        file_path, line, parsed_from = node_file_line(nodes_by_id, node_id) if found else (None, None, None)
        lines += [
            f"### `{node_id}`",
            "",
            f"- Found: `{found}`",
            f"- Type: `{node_type(nodes_by_id, node_id)}`",
            f"- Name: `{node_name(nodes_by_id, node_id)}`",
            f"- Parsed file: `{file_path}`",
            f"- Parsed line: `{line}`",
            f"- Parsed from: `{parsed_from}`",
            "",
        ]

    lines += ["## Callback / Emitter Candidate Matches", ""]

    match_count = 0
    rejected_count = 0

    for callback_id, callback_type, callback_file, callback_line, callback_parsed_from in callbacks:
        if not callback_file:
            continue

        if focus and callback_file != focus:
            continue

        emitters = emitters_by_file.get(callback_file, [])
        if not emitters:
            continue

        interesting = (
            "invData" in callback_id
            or "PlayerLoadedChar" in callback_id
            or "PlayerLoadout" in callback_id
            or "cl_networking.lua" in callback_id
            or "sv_hooks.lua" in callback_id
            or callback_file.endswith("gamemode/core/hooks/sv_hooks.lua")
            or callback_file.endswith("gamemode/core/libs/item/cl_networking.lua")
        )

        if not interesting and not focus:
            continue

        lines += [
            f"### Callback `{callback_id}`",
            "",
            f"- Type: `{callback_type}`",
            f"- File: `{callback_file}`",
            f"- Line: `{callback_line}`",
            f"- Parsed from: `{callback_parsed_from}`",
            "",
        ]

        for emitter_id, hook_id, emitter_line, emitter_parsed_from in emitters:
            delta = None
            accepted = False

            if callback_line is not None and emitter_line is not None:
                delta = emitter_line - callback_line
                accepted = (
                    0 <= delta <= args.max_forward_lines
                    or -args.max_backward_lines <= delta < 0
                )

            if accepted:
                match_count += 1
            else:
                rejected_count += 1

            lines += [
                f"- Emitter: `{emitter_id}`",
                f"  - Hook: `{hook_id}`",
                f"  - Emitter line: `{emitter_line}`",
                f"  - Parsed from: `{emitter_parsed_from}`",
                f"  - Delta: `{delta}`",
                f"  - Accepted: `{accepted}`",
            ]

        lines.append("")

    lines += [
        "## Summary",
        "",
        f"- Accepted matches shown: `{match_count}`",
        f"- Rejected matches shown: `{rejected_count}`",
    ]

    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote MD: {args.out_md}")
    print(f"Accepted shown: {match_count}")
    print(f"Rejected shown: {rejected_count}")


if __name__ == "__main__":
    main()