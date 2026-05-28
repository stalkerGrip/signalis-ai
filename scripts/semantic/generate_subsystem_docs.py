from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

LIFECYCLE_TERMS = {
    "CharacterLoaded",
    "PlayerLoadedChar",
    "PrePlayerLoadedChar",
    "PlayerLoadout",
    "PostPlayerLoadout",
    "CharacterPreSave",
    "CharacterPostSave",
    "LoadData",
    "SaveData",
}

SYNC_TERMS = {
    "inventorySetPanelStatus",
    "inventoryOpen",
    "invsRuleSet",
    "nutInventoryInit",
    "nutInventoryAdd",
    "nutInventoryRemove",
    "nutInventoryDelete",
    "nutTransferItem",
    "invAct",
    "storageInventory",
    "nutStorageOpen",
    "nutVendorOpen",
}

IGNORE_HUB_NODE_TYPES = {
    "realm",
    "timer",
    "timer_class",
    "event_class",
    "timer_risk",
    "gamemode",
    "subsystem",
}

PROPAGATION_NODE_TYPES = {
    "hook_event",
    "hook_emitter",
    "hook_listener",
    "network_message",
    "network_operation",
    "timer",
    "timer_operation",
    "file",
    "plugin",
}

DEFAULT_SUBSYSTEMS = [
    "inventory",
    "storage",
    "vendor",
    "multichar",
    "gridinv",
    "healthproblems",
    "needs",
    "lightitems",
    "nextbots",
]


def load_topology(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    data = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(data, dict):
        nodes = data.get("nodes", [])
        edges = data.get("edges", [])
        return nodes, edges

    raise ValueError(f"Unsupported topology format: {path}")


def node_id(node: dict[str, Any]) -> str:
    return str(node.get("id") or node.get("node_id") or node.get("source_id") or "")


def node_label(node: dict[str, Any]) -> str:
    return str(
        node.get("label")
        or node.get("name")
        or node.get("event")
        or node.get("message")
        or node_id(node)
    )


def node_type(node: dict[str, Any]) -> str:
    return str(node.get("node_type") or node.get("type") or "")


def edge_source(edge: dict[str, Any]) -> str:
    return str(edge.get("source") or edge.get("from") or edge.get("src") or "")


def edge_target(edge: dict[str, Any]) -> str:
    return str(edge.get("target") or edge.get("to") or edge.get("dst") or "")


def edge_type(edge: dict[str, Any]) -> str:
    return str(edge.get("type") or edge.get("edge_type") or edge.get("relationship") or "")


def contains_subsystem(text: str, subsystem: str) -> bool:
    return subsystem.lower() in text.lower()


def collect_subsystem(
    subsystem: str,
    nodes: list[dict[str, Any]],
    edges: list[dict[str, Any]],
) -> dict[str, Any]:
    by_id = {node_id(n): n for n in nodes if node_id(n)}

    selected_ids: set[str] = set()

    for n in nodes:
        packed = json.dumps(n, ensure_ascii=False).lower()
        if contains_subsystem(packed, subsystem):
            selected_ids.add(node_id(n))

    for e in edges:
        packed = json.dumps(e, ensure_ascii=False).lower()
        if contains_subsystem(packed, subsystem):
            selected_ids.add(edge_source(e))
            selected_ids.add(edge_target(e))

    selected_ids = {sid for sid in selected_ids if sid in by_id}

    selected_edges = [
        e for e in edges
        if edge_source(e) in selected_ids or edge_target(e) in selected_ids
    ]

    type_counts = Counter(node_type(by_id[sid]) for sid in selected_ids)
    edge_counts = Counter(edge_type(e) for e in selected_edges)

    files = Counter()
    hooks = Counter()
    networks = Counter()
    timers = Counter()
    realms = Counter()
    plugins = Counter()
    connected = Counter()
    lifecycle = Counter()
    sync_hotspots = Counter()

    for sid in selected_ids:
        n = by_id[sid]
        label = node_label(n)
        packed_node = json.dumps(n, ensure_ascii=False)

        for term in LIFECYCLE_TERMS:
            if term in packed_node:
                lifecycle[label] += 1

        for term in SYNC_TERMS:
            if term in packed_node:
                sync_hotspots[label] += 1
        ntype = node_type(n)

        file_value = n.get("file") or n.get("path")
        realm_value = n.get("realm")
        plugin_value = n.get("plugin")
        subsystem_value = n.get("subsystem")

        if file_value:
            files[str(file_value)] += 1
        if realm_value:
            realms[str(realm_value)] += 1
        if plugin_value:
            plugins[str(plugin_value)] += 1
        if subsystem_value and str(subsystem_value) != subsystem:
            connected[str(subsystem_value)] += 1

        if ntype in {"hook_event", "hook_emitter", "hook_listener"}:
            hooks[label] += 1
        elif ntype in {"network_message", "network_operation", "network_context"}:
            networks[label] += 1
        elif ntype in {"timer", "timer_operation", "timer_class", "timer_risk"}:
            timers[label] += 1

    for e in selected_edges:
        for endpoint in [edge_source(e), edge_target(e)]:
            n = by_id.get(endpoint)
            if not n:
                continue

            plugin_value = n.get("plugin")
            subsystem_value = n.get("subsystem")

            if plugin_value and str(plugin_value) != subsystem:
                connected[str(plugin_value)] += 1
            if subsystem_value and str(subsystem_value) != subsystem:
                connected[str(subsystem_value)] += 1

    hubs = []
    propagation_hubs = []

    for sid in selected_ids:
        n = by_id[sid]
        ntype = node_type(n)

        degree = 0
        for e in selected_edges:
            if edge_source(e) == sid or edge_target(e) == sid:
                degree += 1

        entry = (degree, ntype, node_label(n), sid)

        if ntype not in IGNORE_HUB_NODE_TYPES:
            hubs.append(entry)

        if ntype in PROPAGATION_NODE_TYPES and ntype not in IGNORE_HUB_NODE_TYPES:
            propagation_hubs.append(entry)

    hubs.sort(reverse=True)
    propagation_hubs.sort(reverse=True)

    return {
        "subsystem": subsystem,
        "node_count": len(selected_ids),
        "edge_count": len(selected_edges),
        "node_type_counts": type_counts,
        "edge_type_counts": edge_counts,
        "files": files,
        "hooks": hooks,
        "networks": networks,
        "timers": timers,
        "realms": realms,
        "plugins": plugins,
        "connected": connected,
        "hubs": hubs,
        "propagation_hubs": propagation_hubs,
        "lifecycle": lifecycle,
        "sync_hotspots": sync_hotspots,
    }


def top_list(counter: Counter, limit: int = 20) -> list[str]:
    if not counter:
        return ["- none detected"]

    return [f"- `{name}`: {count}" for name, count in counter.most_common(limit)]


def render_doc(data: dict[str, Any]) -> str:
    subsystem = data["subsystem"]

    lines = [
        f"# Subsystem: {subsystem}",
        "",
        "## Purpose",
        "",
        "Deterministic subsystem summary generated from runtime topology.",
        "",
        "## Topology Summary",
        "",
        f"- Nodes: **{data['node_count']}**",
        f"- Edges: **{data['edge_count']}**",
        "",
        "## Node Types",
        "",
        *top_list(data["node_type_counts"]),
        "",
        "## Edge Types",
        "",
        *top_list(data["edge_type_counts"]),
        "",
        "## Major Hooks",
        "",
        *top_list(data["hooks"]),
        "",
        "## Major Network Signals",
        "",
        *top_list(data["networks"]),
        "",
        "## Lifecycle Propagation",
        "",
        *top_list(data["lifecycle"]),
        "",
        "## Synchronization Hotspots",
        "",
        *top_list(data["sync_hotspots"]),
        "",
        "## Important Timers",
        "",
        *top_list(data["timers"]),
        "",
        "## Realms",
        "",
        *top_list(data["realms"]),
        "",
        "## Major Files",
        "",
        *top_list(data["files"]),
        "",
        "## Connected Plugins / Subsystems",
        "",
        *top_list(data["connected"]),
        "",
        "## Runtime Propagation Hubs",
        "",
    ]

    if not data["propagation_hubs"]:
        lines.append("- none detected")
    else:
        for degree, ntype, label, sid in data["propagation_hubs"][:25]:
            lines.append(f"- degree `{degree}` | `{ntype}` | `{label}` | `{sid}`")

    lines.extend([
        "",
        "## Topology Hubs",
        "",
    ])

    if not data["hubs"]:
        lines.append("- none detected")
    else:
        for degree, ntype, label, sid in data["hubs"][:25]:
            lines.append(f"- degree `{degree}` | `{ntype}` | `{label}` | `{sid}`")

    lines.extend([
        "",
        "## Runtime Risks",
        "",
        "- Review high-degree hubs for hidden coupling.",
        "- Review network signals for synchronization ownership.",
        "- Review timers for scheduler or debounce behavior.",
        "- Review realm crossings for client/server authority issues.",
        "",
        "## Notes",
        "",
        "This document is generated from topology only. Use raw Lua only for exact validation.",
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate subsystem semantic docs from runtime topology.")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--topology")
    parser.add_argument("--output-dir")
    parser.add_argument("--subsystems", nargs="*", default=DEFAULT_SUBSYSTEMS)

    args = parser.parse_args()

    workspace = Path(args.workspace)

    topology_path = (
        Path(args.topology)
        if args.topology
        else workspace / "manifests" / "normalized" / "runtime_topology.json"
    )

    output_dir = (
        Path(args.output_dir)
        if args.output_dir
        else workspace / "docs" / "subsystems"
    )

    nodes, edges = load_topology(topology_path)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loaded topology: {len(nodes)} nodes, {len(edges)} edges")
    print(f"Writing subsystem docs to: {output_dir}")

    for subsystem in args.subsystems:
        data = collect_subsystem(subsystem, nodes, edges)
        doc = render_doc(data)

        out_path = output_dir / f"{subsystem}.md"
        out_path.write_text(doc, encoding="utf-8")

        print(f"- {subsystem}: {data['node_count']} nodes, {data['edge_count']} edges -> {out_path}")


if __name__ == "__main__":
    main()