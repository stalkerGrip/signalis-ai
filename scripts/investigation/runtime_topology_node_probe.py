from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def get_nodes(topology: dict[str, Any]) -> dict[str, dict[str, Any]]:
    nodes = topology.get("nodes", {})

    if isinstance(nodes, dict):
        return {
            str(node_id): payload
            for node_id, payload in nodes.items()
            if isinstance(payload, dict)
        }

    if isinstance(nodes, list):
        result: dict[str, dict[str, Any]] = {}
        for node in nodes:
            if not isinstance(node, dict):
                continue
            node_id = str(node.get("id") or node.get("node_id") or "")
            if node_id:
                result[node_id] = node
        return result

    return {}


def get_edges(topology: dict[str, Any]) -> list[dict[str, Any]]:
    edges = topology.get("edges", [])
    if isinstance(edges, list):
        return [edge for edge in edges if isinstance(edge, dict)]
    return []


def edge_source(edge: dict[str, Any]) -> str | None:
    for key in ("source", "from", "src"):
        value = edge.get(key)
        if isinstance(value, str):
            return value
    return None


def edge_target(edge: dict[str, Any]) -> str | None:
    for key in ("target", "to", "dst"):
        value = edge.get(key)
        if isinstance(value, str):
            return value
    return None


def edge_type(edge: dict[str, Any]) -> str:
    for key in ("type", "edge_type", "kind"):
        value = edge.get(key)
        if isinstance(value, str):
            return value
    return "unknown"


def node_type(node: dict[str, Any] | None) -> str:
    if not node:
        return "unknown"
    for key in ("type", "node_type"):
        value = node.get(key)
        if isinstance(value, str):
            return value
    return "unknown"


def node_name(node: dict[str, Any] | None, fallback: str) -> str:
    if not node:
        return fallback
    for key in ("name", "label", "title", "message", "event"):
        value = node.get(key)
        if isinstance(value, str) and value:
            return value
    return fallback


def compact_node_info(node_id: str, nodes: dict[str, dict[str, Any]]) -> str:
    node = nodes.get(node_id)
    return f"`{node_id}` | type=`{node_type(node)}` | name=`{node_name(node, node_id)}`"


def write_md(
    path: Path,
    node_id: str,
    nodes: dict[str, dict[str, Any]],
    incoming: list[dict[str, Any]],
    outgoing: list[dict[str, Any]],
    max_edges: int,
) -> None:
    node = nodes.get(node_id)

    incoming_types = Counter(edge_type(edge) for edge in incoming)
    outgoing_types = Counter(edge_type(edge) for edge in outgoing)

    lines: list[str] = [
        "# Runtime Topology Node Probe",
        "",
        f"- Node ID: `{node_id}`",
        f"- Found: `{node is not None}`",
        f"- Node type: `{node_type(node)}`",
        f"- Node name: `{node_name(node, node_id)}`",
        f"- Incoming edges: `{len(incoming)}`",
        f"- Outgoing edges: `{len(outgoing)}`",
        "",
        "## Incoming Edge Types",
        "",
    ]

    if incoming_types:
        for kind, count in incoming_types.most_common():
            lines.append(f"- `{kind}`: `{count}`")
    else:
        lines.append("- none")

    lines += [
        "",
        "## Outgoing Edge Types",
        "",
    ]

    if outgoing_types:
        for kind, count in outgoing_types.most_common():
            lines.append(f"- `{kind}`: `{count}`")
    else:
        lines.append("- none")

    lines += [
        "",
        "## Incoming Edges",
        "",
    ]

    for edge in incoming[:max_edges]:
        src = edge_source(edge) or ""
        dst = edge_target(edge) or ""

        lines += [
            f"- {compact_node_info(src, nodes)}",
            f"  → {compact_node_info(dst, nodes)}",
            f"  - Edge type: `{edge_type(edge)}`",
        ]

    if len(incoming) > max_edges:
        lines.append(f"- _Additional incoming edges omitted: {len(incoming) - max_edges}_")

    lines += [
        "",
        "## Outgoing Edges",
        "",
    ]

    for edge in outgoing[:max_edges]:
        src = edge_source(edge) or ""
        dst = edge_target(edge) or ""

        lines += [
            f"- {compact_node_info(src, nodes)}",
            f"  → {compact_node_info(dst, nodes)}",
            f"  - Edge type: `{edge_type(edge)}`",
        ]

    if len(outgoing) > max_edges:
        lines.append(f"- _Additional outgoing edges omitted: {len(outgoing) - max_edges}_")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Inspect incoming/outgoing edges around a runtime topology node."
    )
    parser.add_argument("--runtime-topology", required=True, type=Path)
    parser.add_argument("--node-id", required=True)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--max-edges", type=int, default=80)

    args = parser.parse_args()

    topology = load_json(args.runtime_topology)
    nodes = get_nodes(topology)
    edges = get_edges(topology)

    incoming: list[dict[str, Any]] = []
    outgoing: list[dict[str, Any]] = []

    for edge in edges:
        src = edge_source(edge)
        dst = edge_target(edge)

        if dst == args.node_id:
            incoming.append(edge)
        if src == args.node_id:
            outgoing.append(edge)

    write_md(
        path=args.out_md,
        node_id=args.node_id,
        nodes=nodes,
        incoming=incoming,
        outgoing=outgoing,
        max_edges=args.max_edges,
    )

    print(f"Wrote:    {args.out_md}")
    print(f"Found:    {args.node_id in nodes}")
    print(f"Incoming: {len(incoming)}")
    print(f"Outgoing: {len(outgoing)}")


if __name__ == "__main__":
    main()