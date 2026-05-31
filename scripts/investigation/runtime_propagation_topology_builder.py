from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


PROPAGATION_EDGE_TYPES = {
    "emits",
    "emits_event",
    "dispatches_to",

    "sends_network_message",
    "file_sends_network_message",
    "network_dispatches_to",

    "creates_timer",
    "references_timer",
    "schedules_delay",
    "schedules_player_action",
    "schedules_entity_action",
}


REVERSE_TO_PROPAGATION = {
    # hook relationship -> event fanout
    "listens_to": "hook_event_dispatches_to_listener",
    "listens_to_event": "hook_event_dispatches_to_listener",

    # network relationship -> message fanout
    "receives_network_message": "network_message_dispatches_to_receiver",
    "file_receives_network_message": "network_message_dispatches_to_receiver",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def normalize_edge(edge: dict[str, Any], idx: int) -> dict[str, Any] | None:
    source = edge.get("source") or edge.get("from")
    target = edge.get("target") or edge.get("to")
    edge_type = edge.get("type") or edge.get("edge_type") or edge.get("relation")

    if not source or not target or not edge_type:
        return None

    return {
        "id": edge.get("id") or f"edge:{idx}",
        "source": source,
        "target": target,
        "type": edge_type,
        "label": edge.get("label") or edge_type,
        "source_edge": edge.get("id") or f"edge:{idx}",
        "generated": False,
    }


def node_type(nodes_by_id: dict[str, dict[str, Any]], node_id: str) -> str:
    node = nodes_by_id.get(node_id, {})
    return node.get("type") or node.get("node_type") or ""


def add_edge(
    edges: list[dict[str, Any]],
    seen: set[tuple[str, str, str]],
    source: str,
    target: str,
    edge_type: str,
    source_edge: str,
    reason: str,
) -> None:
    key = (source, target, edge_type)
    if key in seen:
        return

    seen.add(key)
    edges.append(
        {
            "id": f"prop:{len(edges) + 1}",
            "source": source,
            "target": target,
            "type": edge_type,
            "label": edge_type,
            "source_edge": source_edge,
            "generated": True,
            "reason": reason,
        }
    )


def build_propagation_topology(topology: dict[str, Any]) -> dict[str, Any]:
    raw_nodes = topology.get("nodes", [])
    raw_edges = topology.get("edges", [])

    nodes = []
    nodes_by_id: dict[str, dict[str, Any]] = {}

    for node in raw_nodes:
        node_id = node.get("id")
        if not node_id:
            continue
        nodes.append(node)
        nodes_by_id[node_id] = node

    propagation_edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()

    normalized_edges = []
    for idx, raw_edge in enumerate(raw_edges):
        edge = normalize_edge(raw_edge, idx)
        if edge:
            normalized_edges.append(edge)

    # V2: listener exit bridges.
    #
    # Raw topology has owner -> listener relationships:
    # file/plugin -> hook_listener
    #
    # Propagation traversal needs the listener to exit back into its owning
    # source context, otherwise hook_event -> listener becomes a dead end.
    for edge in normalized_edges:
        src = edge["source"]
        dst = edge["target"]
        etype = edge["type"]

        if etype in {"contains_listener", "registers_listener"}:
            if node_type(nodes_by_id, dst) == "hook_listener":
                add_edge(
                    propagation_edges,
                    seen,
                    dst,
                    src,
                    "listener_exits_to_owner",
                    edge["source_edge"],
                    f"generated listener exit from relationship edge {etype}",
                )

        if etype == "contains_network_operation":
            if node_type(nodes_by_id, dst) == "network_operation":
                add_edge(
                    propagation_edges,
                    seen,
                    dst,
                    src,
                    "network_operation_exits_to_owner",
                    edge["source_edge"],
                    "generated network operation exit from containing file edge",
                )

    for edge in normalized_edges:
        src = edge["source"]
        dst = edge["target"]
        etype = edge["type"]

        if etype in PROPAGATION_EDGE_TYPES:
            key = (src, dst, etype)
            if key not in seen:
                seen.add(key)
                propagation_edges.append(edge)

        if etype in REVERSE_TO_PROPAGATION:
            src_type = node_type(nodes_by_id, src)
            dst_type = node_type(nodes_by_id, dst)
            prop_type = REVERSE_TO_PROPAGATION[etype]

            # listener -> hook_event becomes hook_event -> listener
            if dst_type == "hook_event":
                add_edge(
                    propagation_edges,
                    seen,
                    dst,
                    src,
                    prop_type,
                    edge["source_edge"],
                    f"reversed relationship edge {etype}",
                )

            # receiver operation/file -> network_message becomes message -> receiver
            elif dst_type == "network_message":
                add_edge(
                    propagation_edges,
                    seen,
                    dst,
                    src,
                    prop_type,
                    edge["source_edge"],
                    f"reversed relationship edge {etype}",
                )

    edge_counts = Counter(edge["type"] for edge in propagation_edges)
    node_counts = Counter(node_type(nodes_by_id, node["id"]) for node in nodes)

    return {
        "schema": "runtime_propagation_topology.v1",
        "source_schema": topology.get("schema"),
        "source": "manifests/normalized/runtime_topology.json",
        "nodes": nodes,
        "edges": propagation_edges,
        "summary": {
            "nodes": len(nodes),
            "edges": len(propagation_edges),
            "generated_edges": sum(1 for e in propagation_edges if e.get("generated")),
            "copied_edges": sum(1 for e in propagation_edges if not e.get("generated")),
            "node_types": dict(node_counts.most_common()),
            "edge_types": dict(edge_counts.most_common()),
        },
    }


def write_summary(path: Path, data: dict[str, Any]) -> None:
    summary = data["summary"]

    lines = [
        "# Runtime Propagation Topology Summary",
        "",
        f"Schema: `{data['schema']}`",
        "",
        "## Totals",
        "",
        f"- Nodes: **{summary['nodes']}**",
        f"- Edges: **{summary['edges']}**",
        f"- Copied propagation edges: **{summary['copied_edges']}**",
        f"- Generated propagation edges: **{summary['generated_edges']}**",
        "",
        "## Edge Types",
        "",
    ]

    for edge_type, count in summary["edge_types"].items():
        lines.append(f"- `{edge_type}`: **{count}**")

    lines.extend(["", "## Node Types", ""])

    for node_type_name, count in summary["node_types"].items():
        lines.append(f"- `{node_type_name}`: **{count}**")

    lines.extend(
        [
            "",
            "## Purpose",
            "",
            "This artifact transforms the relationship-oriented runtime topology into a traversal-oriented propagation topology.",
            "",
            "Primary generated propagation rules:",
            "",
            "- `listener -> hook_event` relationships become `hook_event -> listener` fanout edges.",
            "- `receiver -> network_message` relationships become `network_message -> receiver` dispatch edges.",
            "- Existing deterministic propagation edges are preserved.",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build traversal-oriented runtime propagation topology from runtime_topology.json."
    )
    parser.add_argument(
        "--workspace",
        default=".",
        type=Path,
        help="SIGNALIS AI workspace root. Not a raw Lua source root.",
    )
    parser.add_argument(
        "--input",
        default=Path("manifests/normalized/runtime_topology.json"),
        type=Path,
    )
    parser.add_argument(
        "--out-json",
        default=Path("manifests/normalized/runtime_propagation_topology.json"),
        type=Path,
    )
    parser.add_argument(
        "--out-md",
        default=Path("manifests/normalized/runtime_propagation_topology_summary.md"),
        type=Path,
    )

    args = parser.parse_args()
    workspace = args.workspace.resolve()

    input_path = args.input if args.input.is_absolute() else workspace / args.input
    out_json = args.out_json if args.out_json.is_absolute() else workspace / args.out_json
    out_md = args.out_md if args.out_md.is_absolute() else workspace / args.out_md

    topology = load_json(input_path)
    propagation_topology = build_propagation_topology(topology)

    write_json(out_json, propagation_topology)
    write_summary(out_md, propagation_topology)

    summary = propagation_topology["summary"]
    print(f"Wrote JSON: {out_json}")
    print(f"Wrote MD:   {out_md}")
    print(f"Nodes:      {summary['nodes']}")
    print(f"Edges:      {summary['edges']}")
    print(f"Copied:     {summary['copied_edges']}")
    print(f"Generated:  {summary['generated_edges']}")


if __name__ == "__main__":
    main()