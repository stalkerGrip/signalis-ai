#!/usr/bin/env python3
"""
merge_runtime_graphs.py

Merges normalized runtime subgraphs into one canonical topology graph.

Inputs, if present:
  manifests/normalized/runtime_graph_nodes.json
  manifests/normalized/runtime_graph_edges.json
  manifests/normalized/network_graph_nodes.json
  manifests/normalized/network_graph_edges.json
  manifests/normalized/timer_graph_nodes.json
  manifests/normalized/timer_graph_edges.json

Outputs:
  manifests/normalized/runtime_topology_nodes.json
  manifests/normalized/runtime_topology_edges.json
  manifests/normalized/runtime_topology.json
  manifests/normalized/runtime_topology_summary.md

Design:
  - Manifest-first, no source scan.
  - Stable node IDs are preserved where possible.
  - Duplicate nodes/edges are deduplicated by stable identity.
  - Adds graph_layer metadata: hook, network, timer.
  - Adds lightweight cross-layer bridge edges through shared file/plugin/realm nodes.
"""

from __future__ import annotations

import argparse
import json
import hashlib
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

JsonObj = Dict[str, Any]


GRAPH_INPUTS = [
    {
        "layer": "hook",
        "nodes": "runtime_graph_nodes.json",
        "edges": "runtime_graph_edges.json",
        "label": "Hook/event runtime graph",
    },
    {
        "layer": "network",
        "nodes": "network_graph_nodes.json",
        "edges": "network_graph_edges.json",
        "label": "Network graph",
    },
    {
        "layer": "timer",
        "nodes": "timer_graph_nodes.json",
        "edges": "timer_graph_edges.json",
        "label": "Timer graph",
    },
]


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)


def as_list(data: Any) -> List[Any]:
    """Accept list, dict with common list keys, or dict-as-map."""
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("nodes", "edges", "items", "data"):
            if isinstance(data.get(key), list):
                return data[key]
        # dict keyed by ID -> object
        if all(isinstance(v, dict) for v in data.values()):
            return list(data.values())
    return []


def stable_hash(value: Any) -> str:
    blob = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:16]


def pick_first(obj: JsonObj, keys: Iterable[str]) -> Optional[Any]:
    for key in keys:
        val = obj.get(key)
        if val not in (None, ""):
            return val
    return None


def normalize_path(value: Any) -> Optional[str]:
    if value in (None, ""):
        return None
    text = str(value).replace("/", "\\")
    while "\\\\" in text:
        text = text.replace("\\\\", "\\")
    return text.strip("\\")


def infer_node_id(node: JsonObj, layer: str) -> str:
    existing = pick_first(node, ("id", "node_id", "stable_id", "uid"))
    if existing:
        return str(existing)

    ntype = str(pick_first(node, ("type", "node_type", "kind")) or "unknown")
    name = pick_first(node, ("name", "label", "event", "message", "timer", "file", "plugin", "realm"))

    if ntype == "file" or "file" in node:
        f = normalize_path(pick_first(node, ("file", "path", "relative_path", "name", "label")))
        if f:
            return f"file:{f}"
    if ntype == "plugin" or "plugin" in node:
        p = pick_first(node, ("plugin", "plugin_id", "unique_id", "name", "label"))
        if p:
            return f"plugin:{p}"
    if ntype == "realm" or "realm" in node:
        r = pick_first(node, ("realm", "name", "label"))
        if r:
            return f"realm:{r}"
    if ntype in ("hook_event", "event"):
        e = pick_first(node, ("event", "hook", "name", "label"))
        if e:
            return f"hook:{e}"
    if ntype == "network_message":
        proto = pick_first(node, ("protocol", "message_protocol")) or "network"
        msg = pick_first(node, ("message", "name", "label"))
        if msg:
            return f"net:{proto}:{msg}"
    if ntype == "timer":
        t = pick_first(node, ("timer", "timer_name", "name", "label"))
        if t:
            return f"timer:{t}"

    if name:
        return f"{layer}:{ntype}:{name}"
    return f"{layer}:{ntype}:{stable_hash(node)}"


def canonical_node(node: JsonObj, layer: str) -> JsonObj:
    out = dict(node)
    node_id = infer_node_id(out, layer)
    ntype = str(pick_first(out, ("type", "node_type", "kind")) or "unknown")
    out["id"] = node_id
    out["type"] = ntype
    out.setdefault("graph_layers", [])
    if isinstance(out["graph_layers"], list) and layer not in out["graph_layers"]:
        out["graph_layers"].append(layer)
    out.setdefault("source_graph", layer)
    if "file" in out:
        out["file"] = normalize_path(out["file"])
    return out


def infer_edge_source(edge: JsonObj) -> Optional[str]:
    return pick_first(edge, ("source", "src", "from", "from_id", "source_id"))


def infer_edge_target(edge: JsonObj) -> Optional[str]:
    return pick_first(edge, ("target", "dst", "to", "to_id", "target_id"))


def infer_edge_type(edge: JsonObj) -> str:
    return str(pick_first(edge, ("type", "edge_type", "kind", "relation")) or "related_to")


def canonical_edge(edge: JsonObj, layer: str, node_alias: Dict[str, str]) -> Optional[JsonObj]:
    source = infer_edge_source(edge)
    target = infer_edge_target(edge)
    if source is None or target is None:
        return None

    source = node_alias.get(str(source), str(source))
    target = node_alias.get(str(target), str(target))
    etype = infer_edge_type(edge)

    out = dict(edge)
    out["source"] = source
    out["target"] = target
    out["type"] = etype
    out.setdefault("graph_layers", [])
    if isinstance(out["graph_layers"], list) and layer not in out["graph_layers"]:
        out["graph_layers"].append(layer)
    out.setdefault("source_graph", layer)
    out.setdefault("id", f"edge:{etype}:{source}:{target}:{stable_hash(edge.get('properties', edge))}")
    return out


def merge_nodes(existing: JsonObj, incoming: JsonObj) -> JsonObj:
    merged = dict(existing)
    for key, val in incoming.items():
        if key == "graph_layers":
            layers = list(dict.fromkeys((existing.get(key) or []) + (val or [])))
            merged[key] = layers
        elif key not in merged or merged[key] in (None, "", [], {}):
            merged[key] = val
        elif merged[key] == val:
            continue
        else:
            # Preserve conflicting details without breaking stable top-level fields.
            conflicts = merged.setdefault("merge_conflicts", {})
            if key not in conflicts:
                conflicts[key] = [merged[key]]
            if val not in conflicts[key]:
                conflicts[key].append(val)
    return merged


def edge_key(edge: JsonObj) -> Tuple[str, str, str, str]:
    props = dict(edge)
    props.pop("id", None)
    props.pop("graph_layers", None)
    props.pop("source_graph", None)
    return (
        str(edge.get("source")),
        str(edge.get("target")),
        str(edge.get("type")),
        stable_hash(props),
    )


def add_bridge_edges(nodes: Dict[str, JsonObj], edges: Dict[Tuple[str, str, str, str], JsonObj]) -> int:
    """Add file/plugin/realm bridge edges for cross-layer traversal when obvious."""
    added = 0

    def add(source: str, target: str, etype: str, props: Optional[JsonObj] = None) -> None:
        nonlocal added
        if not source or not target or source not in nodes or target not in nodes:
            return
        e = {
            "id": f"edge:{etype}:{source}:{target}",
            "source": source,
            "target": target,
            "type": etype,
            "graph_layers": ["topology_bridge"],
            "source_graph": "topology_bridge",
        }
        if props:
            e.update(props)
        k = edge_key(e)
        if k not in edges:
            edges[k] = e
            added += 1

    for node_id, node in list(nodes.items()):
        ntype = node.get("type")
        file_path = normalize_path(node.get("file") or node.get("source_file"))
        if file_path:
            file_id = f"file:{file_path}"
            if file_id in nodes and node_id != file_id:
                add(file_id, node_id, "contains_runtime_node")

        plugin = node.get("plugin") or node.get("plugin_id") or node.get("owner_plugin")
        if plugin:
            plugin_id = f"plugin:{plugin}"
            if plugin_id in nodes and node_id != plugin_id:
                add(plugin_id, node_id, "owns_runtime_node")

        realm = node.get("realm")
        if realm:
            realm_id = f"realm:{realm}"
            if realm_id in nodes and node_id != realm_id:
                add(node_id, realm_id, "runs_in_realm")

        # Tag high-level runtime assets as topology nodes.
        if ntype in {"hook_event", "network_message", "timer"}:
            node.setdefault("topology_role", "runtime_signal")

    return added


def summarize(nodes: List[JsonObj], edges: List[JsonObj], loaded_inputs: List[JsonObj], bridge_edges_added: int) -> str:
    node_types = Counter(str(n.get("type", "unknown")) for n in nodes)
    edge_types = Counter(str(e.get("type", "unknown")) for e in edges)
    layers = Counter()
    for n in nodes:
        for layer in n.get("graph_layers", []) or []:
            layers[layer] += 1

    signal_counts = {
        "hook_events": sum(1 for n in nodes if n.get("type") == "hook_event"),
        "network_messages": sum(1 for n in nodes if n.get("type") == "network_message"),
        "timers": sum(1 for n in nodes if n.get("type") == "timer"),
        "files": sum(1 for n in nodes if n.get("type") == "file"),
        "plugins": sum(1 for n in nodes if n.get("type") == "plugin"),
    }

    hot_files = Counter()
    hot_plugins = Counter()
    for e in edges:
        for endpoint in (e.get("source"), e.get("target")):
            if isinstance(endpoint, str):
                if endpoint.startswith("file:"):
                    hot_files[endpoint[5:]] += 1
                elif endpoint.startswith("plugin:"):
                    hot_plugins[endpoint[7:]] += 1

    high_risk_timers = [
        n for n in nodes
        if n.get("type") == "timer_operation" and (
            "high_frequency_infinite_timer" in (n.get("risk_flags") or [])
            or n.get("timer_class") == "high_frequency_infinite_timer"
        )
    ]

    lines = []
    lines.append("# Runtime topology summary")
    lines.append("")
    lines.append("Schema: `runtime_topology.v1`")
    lines.append("")
    lines.append("## Inputs")
    for item in loaded_inputs:
        status = "loaded" if item["loaded"] else "missing"
        lines.append(f"- {item['label']}: **{status}** nodes={item.get('nodes', 0)} edges={item.get('edges', 0)}")
    lines.append("")
    lines.append("## Totals")
    lines.append(f"- Nodes: **{len(nodes)}**")
    lines.append(f"- Edges: **{len(edges)}**")
    lines.append(f"- Bridge edges added: **{bridge_edges_added}**")
    for key, val in signal_counts.items():
        lines.append(f"- {key.replace('_', ' ').title()}: **{val}**")
    lines.append("")
    lines.append("## Graph layers by node participation")
    for key, val in layers.most_common():
        lines.append(f"- `{key}`: **{val}**")
    lines.append("")
    lines.append("## Node types")
    for key, val in node_types.most_common(40):
        lines.append(f"- `{key}`: **{val}**")
    lines.append("")
    lines.append("## Edge types")
    for key, val in edge_types.most_common(50):
        lines.append(f"- `{key}`: **{val}**")
    lines.append("")
    lines.append("## Top connected files")
    for key, val in hot_files.most_common(30):
        lines.append(f"- `{key}`: {val}")
    lines.append("")
    lines.append("## Top connected plugins")
    for key, val in hot_plugins.most_common(30):
        lines.append(f"- `{key}`: {val}")
    lines.append("")
    lines.append("## High-frequency timer operation candidates")
    if high_risk_timers:
        for n in high_risk_timers[:30]:
            name = n.get("name") or n.get("timer") or n.get("timer_name") or n.get("id")
            file = n.get("file") or n.get("source_file") or "?"
            line = n.get("line") or n.get("lineno") or "?"
            cls = n.get("timer_class") or n.get("class") or "?"
            lines.append(f"- `{name}` at `{file}:{line}` class=`{cls}`")
    else:
        lines.append("- none detected")
    lines.append("")
    lines.append("## Notes")
    lines.append("- This merge is manifest-first and does not scan source code.")
    lines.append("- High-frequency timers are not automatically defects; animation, sprint/stamina, and short-lived UI loops may be intentional.")
    lines.append("- Use this topology as the first canonical graph for Qdrant ingestion and external architect reasoning.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Merge normalized hook/network/timer graphs into runtime topology.")
    parser.add_argument("--workspace", required=True, help="Workspace root, e.g. E:/signalis_ai")
    parser.add_argument("--normalized-dir", default=None, help="Override normalized manifest directory")
    parser.add_argument("--write", action="store_true", help="Write outputs")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    normalized_dir = Path(args.normalized_dir) if args.normalized_dir else workspace / "manifests" / "normalized"

    nodes_by_id: Dict[str, JsonObj] = {}
    node_alias: Dict[str, str] = {}
    edges_by_key: Dict[Tuple[str, str, str, str], JsonObj] = {}
    loaded_inputs: List[JsonObj] = []

    for cfg in GRAPH_INPUTS:
        layer = cfg["layer"]
        node_path = normalized_dir / cfg["nodes"]
        edge_path = normalized_dir / cfg["edges"]
        raw_nodes = as_list(read_json(node_path, []))
        raw_edges = as_list(read_json(edge_path, []))
        loaded = node_path.exists() or edge_path.exists()
        loaded_inputs.append({
            "label": cfg["label"],
            "layer": layer,
            "loaded": loaded,
            "nodes": len(raw_nodes),
            "edges": len(raw_edges),
            "node_file": str(node_path),
            "edge_file": str(edge_path),
        })

        for raw in raw_nodes:
            if not isinstance(raw, dict):
                continue
            old_id = pick_first(raw, ("id", "node_id", "stable_id", "uid"))
            node = canonical_node(raw, layer)
            node_id = node["id"]
            if old_id:
                node_alias[str(old_id)] = node_id
            node_alias[node_id] = node_id
            if node_id in nodes_by_id:
                nodes_by_id[node_id] = merge_nodes(nodes_by_id[node_id], node)
            else:
                nodes_by_id[node_id] = node

        # Second pass: edges after alias collection for this graph.
        for raw in raw_edges:
            if not isinstance(raw, dict):
                continue
            edge = canonical_edge(raw, layer, node_alias)
            if edge is None:
                continue
            k = edge_key(edge)
            if k in edges_by_key:
                existing_layers = edges_by_key[k].setdefault("graph_layers", [])
                for l in edge.get("graph_layers", []) or []:
                    if l not in existing_layers:
                        existing_layers.append(l)
            else:
                edges_by_key[k] = edge

    bridge_edges_added = add_bridge_edges(nodes_by_id, edges_by_key)

    nodes = sorted(nodes_by_id.values(), key=lambda n: (str(n.get("type", "")), str(n.get("id", ""))))
    edges = sorted(edges_by_key.values(), key=lambda e: (str(e.get("type", "")), str(e.get("source", "")), str(e.get("target", ""))))

    topology = {
        "schema": "runtime_topology.v1",
        "inputs": loaded_inputs,
        "nodes": nodes,
        "edges": edges,
        "summary": {
            "node_count": len(nodes),
            "edge_count": len(edges),
            "bridge_edges_added": bridge_edges_added,
        },
    }
    summary_md = summarize(nodes, edges, loaded_inputs, bridge_edges_added)

    if args.write:
        write_json(normalized_dir / "runtime_topology_nodes.json", nodes)
        write_json(normalized_dir / "runtime_topology_edges.json", edges)
        write_json(normalized_dir / "runtime_topology.json", topology)
        (normalized_dir / "runtime_topology_summary.md").write_text(summary_md, encoding="utf-8")
        print(f"Wrote runtime topology to: {normalized_dir}")
    else:
        print(summary_md)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
