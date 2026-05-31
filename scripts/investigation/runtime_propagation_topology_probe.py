from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def edge_source(edge: dict[str, Any]) -> str | None:
    return edge.get("source") or edge.get("from") or edge.get("src")


def edge_target(edge: dict[str, Any]) -> str | None:
    return edge.get("target") or edge.get("to") or edge.get("dst")


def edge_type(edge: dict[str, Any]) -> str:
    return edge.get("type") or edge.get("edge_type") or edge.get("relation") or "unknown"


def shortest_path(adj: dict[str, list[str]], source: str, target: str, max_depth: int) -> list[str] | None:
    q = deque([(source, [source])])
    seen = {source}

    while q:
        node, path = q.popleft()

        if len(path) > max_depth + 1:
            continue

        for nxt in adj.get(node, []):
            if nxt in seen:
                continue

            new_path = path + [nxt]

            if nxt == target:
                return new_path

            seen.add(nxt)
            q.append((nxt, new_path))

    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-topology", required=True, type=Path)
    parser.add_argument("--source", required=True)
    parser.add_argument("--target", default="")
    parser.add_argument("--max-depth", type=int, default=8)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    topology = load_json(args.runtime_topology)

    nodes = {node["id"]: node for node in topology.get("nodes", []) if node.get("id")}
    incoming = defaultdict(list)
    outgoing = defaultdict(list)
    adj = defaultdict(list)

    for edge in topology.get("edges", []):
        src = edge_source(edge)
        dst = edge_target(edge)
        if not src or not dst:
            continue

        incoming[dst].append(edge)
        outgoing[src].append(edge)
        adj[src].append(dst)

    source_node = nodes.get(args.source)
    lines = [
        "# Runtime Propagation Topology Probe",
        "",
        f"- Topology: `{args.runtime_topology}`",
        f"- Source: `{args.source}`",
        f"- Source found: `{source_node is not None}`",
    ]

    if source_node:
        lines += [
            f"- Source type: `{source_node.get('type') or source_node.get('node_type')}`",
            f"- Source name: `{source_node.get('name')}`",
            f"- Incoming edges: `{len(incoming[args.source])}`",
            f"- Outgoing edges: `{len(outgoing[args.source])}`",
            "",
            "## Outgoing Edge Types",
            "",
        ]

        for t, c in Counter(edge_type(e) for e in outgoing[args.source]).most_common():
            lines.append(f"- `{t}`: `{c}`")

        lines += ["", "## Outgoing Edges", ""]

        for edge in outgoing[args.source][:100]:
            dst = edge_target(edge)
            dst_node = nodes.get(dst, {})
            lines += [
                f"- `{args.source}` → `{dst}`",
                f"  - Edge type: `{edge_type(edge)}`",
                f"  - Target type: `{dst_node.get('type') or dst_node.get('node_type')}`",
                f"  - Target name: `{dst_node.get('name')}`",
            ]

        listener_targets = [
            edge_target(e)
            for e in outgoing[args.source]
            if edge_type(e) == "hook_event_dispatches_to_listener"
        ]
        listener_targets = [x for x in listener_targets if x]

        if listener_targets:
            lines += ["", "## Listener Exit Audit", ""]

            dead = 0
            for listener in listener_targets:
                exits = outgoing[listener]
                if not exits:
                    dead += 1

                listener_node = nodes.get(listener, {})
                lines += [
                    f"### `{listener}`",
                    "",
                    f"- Name: `{listener_node.get('name')}`",
                    f"- Outgoing edges: `{len(exits)}`",
                ]

                for e in exits[:20]:
                    dst = edge_target(e)
                    dst_node = nodes.get(dst, {})
                    lines += [
                        f"  - `{edge_type(e)}` → `{dst}`",
                        f"    - Target type: `{dst_node.get('type') or dst_node.get('node_type')}`",
                        f"    - Target name: `{dst_node.get('name')}`",
                    ]

                lines.append("")

            lines += [
                "## Listener Exit Summary",
                "",
                f"- Listener targets: `{len(listener_targets)}`",
                f"- Dead-end listeners: `{dead}`",
            ]

    if args.target:
        path = shortest_path(adj, args.source, args.target, args.max_depth)
        lines += [
            "",
            "## Path Search",
            "",
            f"- Target: `{args.target}`",
            f"- Path found: `{path is not None}`",
            f"- Max depth: `{args.max_depth}`",
        ]

        if path:
            lines += [
                f"- Path length: `{len(path) - 1}`",
                "",
                "```text",
                "\n→ ".join(path),
                "```",
            ]

    args.out_md.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote MD: {args.out_md}")


if __name__ == "__main__":
    main()