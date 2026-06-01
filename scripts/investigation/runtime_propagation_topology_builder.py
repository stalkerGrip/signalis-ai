from __future__ import annotations

import argparse
import json
import re
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

LISTENER_REL_EDGE_TYPES = {
    "contains_listener",
    "registers_listener",
}

NETWORK_OWNER_EDGE_TYPES = {
    "contains_network_operation",
}

CALLBACK_OWNER_EDGE_TYPES = {
    "contains_listener",
    "registers_listener",
    "contains_network_operation",
}

LINE_RE = re.compile(r"([A-Za-z0-9_/\-\\]+\.lua):(\d+)")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


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


def parse_file_line(*values):
    for value in values:
        if not value:
            continue

        normalized = value.replace("\\", "/")

        matches = LINE_RE.findall(normalized)

        if not matches:
            continue

        file_path, line = matches[-1]

        file_path = normalize_path(file_path)

        return file_path, int(line)

    return None, None


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


def node_file_line(nodes_by_id: dict[str, dict[str, Any]], node_id: str) -> tuple[str | None, int | None]:
    node = nodes_by_id.get(node_id, {})
    return parse_file_line(
        node_id,
        str(node.get("name") or ""),
        str(node.get("label") or ""),
        str(node.get("file") or ""),
        str(node.get("path") or ""),
        str(node.get("source") or ""),
    )


def normalize_edge(raw: dict[str, Any], idx: int) -> dict[str, Any] | None:
    src = edge_source(raw)
    dst = edge_target(raw)

    if not src or not dst:
        return None

    return {
        "source": src,
        "target": dst,
        "type": edge_type(raw),
        "source_edge": idx,
        "evidence": raw,
    }


def add_edge(
    edges: list[dict[str, Any]],
    seen: set[tuple[str, str, str]],
    source: str,
    target: str,
    edge_type_value: str,
    source_edge: int | None,
    reason: str,
) -> bool:
    key = (source, target, edge_type_value)

    if key in seen:
        return False

    seen.add(key)
    edges.append(
        {
            "source": source,
            "target": target,
            "type": edge_type_value,
            "source_edge": source_edge,
            "generated": True,
            "reason": reason,
        }
    )
    return True


def copy_edge(
    edges: list[dict[str, Any]],
    seen: set[tuple[str, str, str]],
    edge: dict[str, Any],
    reason: str,
) -> bool:
    return add_edge(
        edges,
        seen,
        edge["source"],
        edge["target"],
        edge["type"],
        edge["source_edge"],
        reason,
    )


def build_owner_index(
    normalized_edges: list[dict[str, Any]],
    nodes_by_id: dict[str, dict[str, Any]],
) -> dict[str, set[str]]:
    owners: dict[str, set[str]] = {}

    for edge in normalized_edges:
        src = edge["source"]
        dst = edge["target"]
        etype = edge["type"]

        if etype not in CALLBACK_OWNER_EDGE_TYPES:
            continue

        src_type = node_type(nodes_by_id, src)
        dst_type = node_type(nodes_by_id, dst)

        if src_type in {"file", "plugin", "gamemode"} and dst_type in {
            "hook_listener",
            "network_operation",
            "hook_emitter",
        }:
            owners.setdefault(dst, set()).add(src)

    return owners


def build_file_emitters(
    normalized_edges: list[dict[str, Any]],
    nodes_by_id: dict[str, dict[str, Any]],
) -> dict[str, list[tuple[str, str, int | None]]]:
    """
    Returns:
      file_path -> [(emitter_id, emitted_hook_id, emitter_line)]
    """

    emitters: dict[str, str] = {}
    result: dict[str, list[tuple[str, str, int | None]]] = {}

    for edge in normalized_edges:
        src = edge["source"]
        dst = edge["target"]
        etype = edge["type"]

        if etype in {"emits", "emits_event"}:
            if node_type(nodes_by_id, src) == "hook_emitter" and node_type(nodes_by_id, dst) == "hook_event":
                emitters[src] = dst

    for emitter_id, hook_id in emitters.items():
        file_path, line = node_file_line(nodes_by_id, emitter_id)

        if not file_path:
            continue

        result.setdefault(file_path, []).append((emitter_id, hook_id, line))

    for file_path in result:
        result[file_path].sort(key=lambda item: item[2] if item[2] is not None else 10**9)

    return result


def build_network_message_index(
    normalized_edges: list[dict[str, Any]],
    nodes_by_id: dict[str, dict[str, Any]],
) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    message_to_receivers: dict[str, set[str]] = {}
    sender_to_messages: dict[str, set[str]] = {}

    for edge in normalized_edges:
        src = edge["source"]
        dst = edge["target"]
        etype = edge["type"]

        src_type = node_type(nodes_by_id, src)
        dst_type = node_type(nodes_by_id, dst)

        if etype in {"network_dispatches_to", "dispatches_to", "receives_network_message"}:
            if src_type == "network_message" and dst_type == "network_operation":
                message_to_receivers.setdefault(src, set()).add(dst)
            elif src_type == "network_operation" and dst_type == "network_message":
                message_to_receivers.setdefault(dst, set()).add(src)

        if etype in {"sends_network_message", "file_sends_network_message"}:
            if dst_type == "network_message":
                sender_to_messages.setdefault(src, set()).add(dst)

    return message_to_receivers, sender_to_messages


def should_bridge_body_to_emitter(
    body_line: int | None,
    emitter_line: int | None,
    max_forward_lines: int,
    max_backward_lines: int,
) -> bool:
    if body_line is None or emitter_line is None:
        return False

    delta = emitter_line - body_line

    if 0 <= delta <= max_forward_lines:
        return True

    if -max_backward_lines <= delta < 0:
        return True

    return False


def build_propagation_topology(
    topology: dict[str, Any],
    max_callback_forward_lines: int,
    max_callback_backward_lines: int,
) -> tuple[dict[str, Any], dict[str, int]]:
    raw_nodes = topology.get("nodes", [])
    raw_edges = topology.get("edges", [])

    nodes = [node for node in raw_nodes if node.get("id")]
    nodes_by_id = {node["id"]: node for node in nodes}

    normalized_edges: list[dict[str, Any]] = []

    for idx, raw_edge in enumerate(raw_edges):
        edge = normalize_edge(raw_edge, idx)
        if edge:
            normalized_edges.append(edge)

    propagation_edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()

    stats = Counter()

    # V1: copy already-propagation-like edges.
    for edge in normalized_edges:
        if edge["type"] in PROPAGATION_EDGE_TYPES:
            if copy_edge(propagation_edges, seen, edge, "copied propagation-compatible relationship edge"):
                stats["copied"] += 1

    # V1: hook_event -> listener fanout.
    for edge in normalized_edges:
        src = edge["source"]
        dst = edge["target"]
        etype = edge["type"]

        src_type = node_type(nodes_by_id, src)
        dst_type = node_type(nodes_by_id, dst)

        if etype in {"listens_to", "listens_to_event"}:
            if src_type == "hook_listener" and dst_type == "hook_event":
                if add_edge(
                    propagation_edges,
                    seen,
                    dst,
                    src,
                    "hook_event_dispatches_to_listener",
                    edge["source_edge"],
                    f"generated hook dispatch from relationship edge {etype}",
                ):
                    stats["generated_hook_dispatch"] += 1

        if etype == "dispatches_to":
            if src_type == "hook_event" and dst_type == "hook_listener":
                if add_edge(
                    propagation_edges,
                    seen,
                    src,
                    dst,
                    "hook_event_dispatches_to_listener",
                    edge["source_edge"],
                    "normalized hook dispatch edge",
                ):
                    stats["generated_hook_dispatch"] += 1

    # V1: network_message -> receiver fanout.
    for edge in normalized_edges:
        src = edge["source"]
        dst = edge["target"]
        etype = edge["type"]

        src_type = node_type(nodes_by_id, src)
        dst_type = node_type(nodes_by_id, dst)

        if etype in {"network_dispatches_to", "dispatches_to"}:
            if src_type == "network_message" and dst_type == "network_operation":
                if add_edge(
                    propagation_edges,
                    seen,
                    src,
                    dst,
                    "network_message_dispatches_to_receiver",
                    edge["source_edge"],
                    f"generated network dispatch from relationship edge {etype}",
                ):
                    stats["generated_network_dispatch"] += 1

        if etype in {"receives_network_message", "file_receives_network_message"}:
            if src_type == "network_operation" and dst_type == "network_message":
                if add_edge(
                    propagation_edges,
                    seen,
                    dst,
                    src,
                    "network_message_dispatches_to_receiver",
                    edge["source_edge"],
                    f"generated network dispatch from receiver relationship edge {etype}",
                ):
                    stats["generated_network_dispatch"] += 1

    # V2: listener/network operation owner exits.
    for edge in normalized_edges:
        src = edge["source"]
        dst = edge["target"]
        etype = edge["type"]

        if etype in LISTENER_REL_EDGE_TYPES:
            if node_type(nodes_by_id, dst) == "hook_listener":
                if add_edge(
                    propagation_edges,
                    seen,
                    dst,
                    src,
                    "listener_exits_to_owner",
                    edge["source_edge"],
                    f"generated listener exit from relationship edge {etype}",
                ):
                    stats["generated_listener_owner_exit"] += 1

        if etype in NETWORK_OWNER_EDGE_TYPES:
            if node_type(nodes_by_id, dst) == "network_operation":
                if add_edge(
                    propagation_edges,
                    seen,
                    dst,
                    src,
                    "network_operation_exits_to_owner",
                    edge["source_edge"],
                    f"generated network operation exit from relationship edge {etype}",
                ):
                    stats["generated_network_owner_exit"] += 1

    owners = build_owner_index(normalized_edges, nodes_by_id)
    file_emitters = build_file_emitters(normalized_edges, nodes_by_id)

    # V3: callback body -> emitted hook_event.
    #
    # Conservative rule:
    # - callback node and hook emitter must be in same Lua file
    # - emitter line must be near callback line
    # - emitted hook_event must already exist in topology
    #
    # This supports:
    # netstream:invData receiver -> ItemDataChanged
    # GM:PlayerLoadedChar listener -> PlayerLoadout
    # GM:PlayerLoadout listener -> PostPlayerLoadout
    for node_id, node in nodes_by_id.items():
        ntype = node_type(nodes_by_id, node_id)

        if ntype not in {"hook_listener", "network_operation"}:
            continue

        body_file, body_line = node_file_line(nodes_by_id, node_id)

        if not body_file:
            # Fallback through owning file node if callback itself has no parseable file.
            owner_files = [
                owner
                for owner in owners.get(node_id, set())
                if node_type(nodes_by_id, owner) == "file"
            ]

            for owner in owner_files:
                body_file, _ = node_file_line(nodes_by_id, owner)
                if body_file:
                    break

        if not body_file:
            continue

        for emitter_id, hook_id, emitter_line in file_emitters.get(body_file, []):
            if not should_bridge_body_to_emitter(
                body_line,
                emitter_line,
                max_callback_forward_lines,
                max_callback_backward_lines,
            ):
                continue

            if ntype == "hook_listener":
                bridge_type = "hook_listener_emits_hook_event"
            else:
                bridge_type = "network_receiver_emits_hook_event"

            print(
                "MATCH",
                node_id,
                body_file,
                body_line,
                "->",
                hook_id,
                emitter_line,
            )

            if add_edge(
                propagation_edges,
                seen,
                node_id,
                hook_id,
                bridge_type,
                None,
                (
                    "generated callback-body emission bridge "
                    f"via same-file line proximity; emitter={emitter_id}"
                ),
            ):
                stats[f"generated_{bridge_type}"] += 1

    propagation = {
        "schema": "runtime_propagation_topology.v3",
        "source_schema": topology.get("schema") or topology.get("type"),
        "description": (
            "Traversal-oriented runtime propagation topology generated from "
            "relationship-oriented runtime topology."
        ),
        "nodes": nodes,
        "edges": propagation_edges,
        "generation": {
            "copied_edges": stats["copied"],
            "generated_edges": sum(v for k, v in stats.items() if k.startswith("generated_")),
            "max_callback_forward_lines": max_callback_forward_lines,
            "max_callback_backward_lines": max_callback_backward_lines,
        },
    }

    return propagation, dict(stats)


def write_summary(path: Path, propagation: dict[str, Any], stats: dict[str, int]) -> None:
    edge_counts = Counter(edge["type"] for edge in propagation["edges"])

    lines = [
        "# Runtime Propagation Topology Summary",
        "",
        f"- Schema: `{propagation['schema']}`",
        f"- Nodes: `{len(propagation['nodes'])}`",
        f"- Edges: `{len(propagation['edges'])}`",
        f"- Copied: `{propagation['generation']['copied_edges']}`",
        f"- Generated: `{propagation['generation']['generated_edges']}`",
        "",
        "## Generated Edge Stats",
        "",
    ]

    for key, value in sorted(stats.items()):
        lines.append(f"- `{key}`: `{value}`")

    lines += [
        "",
        "## Edge Types",
        "",
    ]

    for edge_type_value, count in edge_counts.most_common():
        lines.append(f"- `{edge_type_value}`: `{count}`")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def default_runtime_topology(workspace: Path) -> Path:
    return workspace / "manifests" / "normalized" / "runtime_topology.json"


def default_out_json(workspace: Path) -> Path:
    return workspace / "manifests" / "normalized" / "runtime_propagation_topology.json"


def default_out_md(workspace: Path) -> Path:
    return workspace / "manifests" / "normalized" / "runtime_propagation_topology_summary.md"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build traversal-oriented runtime propagation topology from runtime_topology.json."
    )
    parser.add_argument("--workspace", type=Path, default=Path("."))
    parser.add_argument("--runtime-topology", type=Path)
    parser.add_argument("--out-json", type=Path)
    parser.add_argument("--out-md", type=Path)
    parser.add_argument("--max-callback-forward-lines", type=int, default=120)
    parser.add_argument("--max-callback-backward-lines", type=int, default=5)
    args = parser.parse_args()

    workspace = args.workspace
    runtime_topology = args.runtime_topology or default_runtime_topology(workspace)
    out_json = args.out_json or default_out_json(workspace)
    out_md = args.out_md or default_out_md(workspace)

    topology = load_json(runtime_topology)

    propagation, stats = build_propagation_topology(
        topology,
        max_callback_forward_lines=args.max_callback_forward_lines,
        max_callback_backward_lines=args.max_callback_backward_lines,
    )

    write_json(out_json, propagation)
    write_summary(out_md, propagation, stats)

    print(f"Wrote JSON: {out_json}")
    print(f"Wrote MD:   {out_md}")
    print(f"Nodes:      {len(propagation['nodes'])}")
    print(f"Edges:      {len(propagation['edges'])}")
    print(f"Copied:     {propagation['generation']['copied_edges']}")
    print(f"Generated:  {propagation['generation']['generated_edges']}")

if __name__ == "__main__":
    main()