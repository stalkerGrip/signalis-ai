#!/usr/bin/env python3
"""
build_network_graph.py

Normalization Phase V1/V2 helper for Signalis AI Orchestration Pipeline.

Builds a deterministic networking graph from existing manifests:
  manifests/networking/netstream_hooks.json
  manifests/networking/netstream_starts.json
  manifests/networking/net_receives.json
  manifests/networking/net_starts.json
  manifests/networking/util_add_network_strings.json
  manifests/networking/net_reads.json
  manifests/networking/net_writes.json
  manifests/networking/net_messages_deep.json

Outputs:
  manifests/normalized/network_graph_nodes.json
  manifests/normalized/network_graph_edges.json
  manifests/normalized/network_graph_summary.md
  manifests/normalized/network_graph.json

Design:
  - Manifest-first, no source scan.
  - Stable IDs.
  - File-level edges.
  - Supports both netstream and raw Garry's Mod net library.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

SCHEMA = "network_graph.v1"


def norm_path(value: Optional[str]) -> str:
    if not value:
        return "unknown"
    return str(value).replace("/", "\\").strip()


def slug(value: Any) -> str:
    s = str(value if value is not None else "unknown").strip()
    s = s.replace("\\", "/")
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^A-Za-z0-9_./:#@+-]+", "_", s)
    s = s.strip("_")
    return s or "unknown"


def realm_from_file(file: str, manifest_realm: Optional[str] = None) -> str:
    if manifest_realm and manifest_realm not in ("", "unknown", None):
        return str(manifest_realm)
    f = norm_path(file).lower().replace("/", "\\")
    base = f.split("\\")[-1]
    if base.startswith("cl_") or "\\cl_" in f:
        return "client"
    if base.startswith("sv_") or "\\sv_" in f:
        return "server"
    if base.startswith("sh_") or "\\sh_" in f:
        return "shared"
    return "shared"


def plugin_from_file(file: str) -> Optional[str]:
    f = norm_path(file)
    parts = [p for p in re.split(r"[\\/]+", f) if p]
    if not parts:
        return None
    if parts[0] == "plugins" and len(parts) >= 2:
        name = parts[1]
        if name.endswith(".lua"):
            name = name[:-4]
        return name
    if parts[0] == "schema":
        return "schema"
    if parts[0] == "gamemode":
        return "gamemode"
    if parts[0] == "entities":
        return "entities"
    return None


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return json.loads(path.read_text(encoding="utf-8-sig"))


@dataclass
class Node:
    id: str
    type: str
    label: str
    props: Dict[str, Any]


@dataclass
class Edge:
    id: str
    type: str
    source: str
    target: str
    props: Dict[str, Any]


class GraphBuilder:
    def __init__(self) -> None:
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}
        self.edge_counts: Counter[str] = Counter()

    def node(self, node_id: str, node_type: str, label: str, **props: Any) -> str:
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, node_type, label, dict(props))
        else:
            # Preserve first label/type but merge non-empty props.
            existing = self.nodes[node_id].props
            for k, v in props.items():
                if k not in existing or existing[k] in (None, "", [], {}):
                    existing[k] = v
        return node_id

    def edge(self, edge_type: str, source: str, target: str, **props: Any) -> str:
        base = f"{edge_type}:{source}->{target}"
        # Keep repeated occurrences as separate edges if line/file/context differs.
        line = props.get("line")
        file = props.get("file")
        ctx = props.get("context") or props.get("method_name") or props.get("message_direction") or props.get("protocol")
        key = f"{base}@{slug(file)}:{line}:{slug(ctx)}"
        if key in self.edges:
            self.edge_counts[key] += 1
            key2 = f"{key}#{self.edge_counts[key]}"
            self.edges[key2] = Edge(key2, edge_type, source, target, dict(props))
            return key2
        self.edges[key] = Edge(key, edge_type, source, target, dict(props))
        return key


def message_id(protocol: str, name: str) -> str:
    return f"netmsg:{slug(protocol)}:{slug(name)}"


def file_id(file: str) -> str:
    return f"file:{slug(norm_path(file))}"


def plugin_id(plugin: str) -> str:
    return f"plugin:{slug(plugin)}"


def op_id(kind: str, protocol: str, item: Dict[str, Any], idx: int) -> str:
    name = item.get("message_name") or item.get("message_expr") or "unknown"
    file = norm_path(item.get("file"))
    line = item.get("line", "?")
    return f"netop:{slug(kind)}:{slug(protocol)}:{slug(name)}:{slug(file)}:{line}:{idx}"


def infer_direction(protocol: str, op_kind: str, item: Dict[str, Any]) -> str:
    if op_kind in ("receive", "hook"):
        return "receive"
    if op_kind in ("start", "register"):
        return "send" if op_kind == "start" else "register"
    d = item.get("message_direction")
    if d:
        d = str(d).lower()
        if d == "start":
            return "send"
        if d == "receive":
            return "receive"
        return d
    return "unknown"


def add_file_plugin_realm(g: GraphBuilder, file: str, realm: str) -> Tuple[str, Optional[str], str]:
    fid = g.node(file_id(file), "file", norm_path(file), path=norm_path(file))
    rid = g.node(f"realm:{slug(realm)}", "realm", realm)
    g.edge("runs_in_realm", fid, rid, file=norm_path(file), realm=realm)
    plugin = plugin_from_file(file)
    if plugin:
        pid = g.node(plugin_id(plugin), "plugin", plugin)
        g.edge("owns_file", pid, fid, file=norm_path(file), plugin=plugin)
    else:
        pid = None
    return fid, pid, rid


def add_message(g: GraphBuilder, protocol: str, name: str, **props: Any) -> str:
    mid = message_id(protocol, name)
    return g.node(mid, "network_message", name, protocol=protocol, **props)


def load_manifest_set(manifest_root: Path) -> Dict[str, List[Dict[str, Any]]]:
    netdir = manifest_root / "networking"
    files = {
        "netstream_hooks": "netstream_hooks.json",
        "netstream_starts": "netstream_starts.json",
        "net_receives": "net_receives.json",
        "net_starts": "net_starts.json",
        "util_add_network_strings": "util_add_network_strings.json",
        "net_reads": "net_reads.json",
        "net_writes": "net_writes.json",
        "net_messages_deep": "net_messages_deep.json",
    }
    return {k: read_json(netdir / fname, []) for k, fname in files.items()}


def build_graph(manifest_root: Path) -> Tuple[GraphBuilder, Dict[str, Any]]:
    manifests = load_manifest_set(manifest_root)
    g = GraphBuilder()

    stats: Dict[str, Any] = {
        "schema": SCHEMA,
        "inputs": {k: len(v) for k, v in manifests.items()},
        "missing_inputs": [],
    }

    for k, v in manifests.items():
        if len(v) == 0:
            # Could be valid empty, but report for QA.
            pass

    # util.AddNetworkString: raw net registration, server side.
    for i, item in enumerate(manifests["util_add_network_strings"]):
        name = item.get("message_name") or "unknown"
        file = norm_path(item.get("file"))
        realm = realm_from_file(file, item.get("realm"))
        fid, _, _ = add_file_plugin_realm(g, file, realm)
        mid = add_message(g, "gmod_net", name, registered=True)
        oid = g.node(op_id("register", "gmod_net", item, i), "network_operation", f"register {name}",
                     operation="register", protocol="gmod_net", message=name, file=file, line=item.get("line"), realm=realm)
        g.edge("contains_network_operation", fid, oid, file=file, line=item.get("line"), protocol="gmod_net")
        g.edge("registers_network_message", oid, mid, file=file, line=item.get("line"), protocol="gmod_net")
        g.edge("file_registers_network_message", fid, mid, file=file, line=item.get("line"), protocol="gmod_net")

    # Raw net.Receive listeners.
    for i, item in enumerate(manifests["net_receives"]):
        name = item.get("message_name") or "unknown"
        file = norm_path(item.get("file"))
        realm = realm_from_file(file, item.get("realm"))
        fid, _, _ = add_file_plugin_realm(g, file, realm)
        mid = add_message(g, "gmod_net", name)
        oid = g.node(op_id("receive", "gmod_net", item, i), "network_operation", f"receive {name}",
                     operation="receive", protocol="gmod_net", message=name, file=file, line=item.get("line"), realm=realm)
        g.edge("contains_network_operation", fid, oid, file=file, line=item.get("line"), protocol="gmod_net")
        g.edge("receives_network_message", oid, mid, file=file, line=item.get("line"), protocol="gmod_net")
        g.edge("file_receives_network_message", fid, mid, file=file, line=item.get("line"), protocol="gmod_net")

    # Raw net.Start emitters.
    for i, item in enumerate(manifests["net_starts"]):
        name = item.get("message_name") or "unknown"
        file = norm_path(item.get("file"))
        realm = realm_from_file(file, item.get("realm"))
        fid, _, _ = add_file_plugin_realm(g, file, realm)
        mid = add_message(g, "gmod_net", name)
        oid = g.node(op_id("start", "gmod_net", item, i), "network_operation", f"send {name}",
                     operation="send", protocol="gmod_net", message=name, file=file, line=item.get("line"), realm=realm)
        g.edge("contains_network_operation", fid, oid, file=file, line=item.get("line"), protocol="gmod_net")
        g.edge("sends_network_message", oid, mid, file=file, line=item.get("line"), protocol="gmod_net")
        g.edge("file_sends_network_message", fid, mid, file=file, line=item.get("line"), protocol="gmod_net")

    # netstream.Hook listeners.
    for i, item in enumerate(manifests["netstream_hooks"]):
        name = item.get("message_name") or "unknown"
        file = norm_path(item.get("file"))
        realm = realm_from_file(file, item.get("realm"))
        fid, _, _ = add_file_plugin_realm(g, file, realm)
        mid = add_message(g, "netstream", name)
        oid = g.node(op_id("hook", "netstream", item, i), "network_operation", f"netstream hook {name}",
                     operation="receive", protocol="netstream", message=name, file=file, line=item.get("line"), realm=realm)
        g.edge("contains_network_operation", fid, oid, file=file, line=item.get("line"), protocol="netstream")
        g.edge("receives_network_message", oid, mid, file=file, line=item.get("line"), protocol="netstream")
        g.edge("file_receives_network_message", fid, mid, file=file, line=item.get("line"), protocol="netstream")

    # netstream.Start emitters.
    unresolved_netstream_symbols = []
    for i, item in enumerate(manifests["netstream_starts"]):
        name = item.get("message_expr") or item.get("message_name") or "unknown"
        resolution = item.get("resolution")
        if resolution not in (None, "literal", "resolved") and str(name).find(".") >= 0:
            unresolved_netstream_symbols.append(item)
        file = norm_path(item.get("file"))
        realm = realm_from_file(file, item.get("realm"))
        fid, _, _ = add_file_plugin_realm(g, file, realm)
        mid = add_message(g, "netstream", str(name), resolution=resolution)
        oid = g.node(op_id("start", "netstream", item, i), "network_operation", f"netstream send {name}",
                     operation="send", protocol="netstream", message=name, resolution=resolution, file=file, line=item.get("line"), realm=realm)
        g.edge("contains_network_operation", fid, oid, file=file, line=item.get("line"), protocol="netstream")
        g.edge("sends_network_message", oid, mid, file=file, line=item.get("line"), protocol="netstream", resolution=resolution)
        g.edge("file_sends_network_message", fid, mid, file=file, line=item.get("line"), protocol="netstream", resolution=resolution)

    # Reads/writes attach payload operations to message and file.
    for kind, collection, edge_type in [
        ("read", manifests["net_reads"], "reads_network_payload"),
        ("write", manifests["net_writes"], "writes_network_payload"),
    ]:
        for i, item in enumerate(collection):
            name = item.get("message_name") or "unknown"
            direction = infer_direction("gmod_net", kind, item)
            protocol = "gmod_net"
            file = norm_path(item.get("file"))
            realm = realm_from_file(file, item.get("realm"))
            fid, _, _ = add_file_plugin_realm(g, file, realm)
            mid = add_message(g, protocol, name)
            payload_label = f"{kind} {item.get('method_name','unknown')} {name}"
            oid = g.node(op_id(kind, protocol, item, i), "network_payload_operation", payload_label,
                         operation=kind, method_name=item.get("method_name"), raw_args=item.get("raw_args"),
                         protocol=protocol, message=name, direction=direction, file=file, line=item.get("line"), realm=realm,
                         context_confidence=item.get("context_confidence"))
            g.edge("contains_network_payload_operation", fid, oid, file=file, line=item.get("line"), protocol=protocol)
            g.edge(edge_type, oid, mid, file=file, line=item.get("line"), method_name=item.get("method_name"),
                   message_direction=item.get("message_direction"), context_confidence=item.get("context_confidence"), protocol=protocol)

    # Deep contexts: useful as provenance/context nodes but do not duplicate send/receive if already present too much.
    for i, item in enumerate(manifests["net_messages_deep"]):
        name = item.get("message_name") or "unknown"
        direction_raw = item.get("message_direction") or "unknown"
        direction = "send" if str(direction_raw).lower() == "start" else "receive" if str(direction_raw).lower() == "receive" else "unknown"
        file = norm_path(item.get("file"))
        realm = realm_from_file(file, item.get("realm"))
        fid, _, _ = add_file_plugin_realm(g, file, realm)
        mid = add_message(g, "gmod_net", name)
        cid = g.node(op_id("context", "gmod_net", item, i), "network_context", f"{direction_raw} {name}",
                     operation=direction, protocol="gmod_net", message=name, file=file, line=item.get("line"), realm=realm)
        g.edge("contains_network_context", fid, cid, file=file, line=item.get("line"), protocol="gmod_net")
        g.edge("context_references_network_message", cid, mid, file=file, line=item.get("line"), message_direction=direction_raw, protocol="gmod_net")

    # Derive send->receive message links and QA counters.
    sends_by_msg: Dict[str, List[str]] = defaultdict(list)
    recvs_by_msg: Dict[str, List[str]] = defaultdict(list)
    regs_by_msg: Dict[str, List[str]] = defaultdict(list)
    for eid, e in list(g.edges.items()):
        if e.type == "sends_network_message":
            sends_by_msg[e.target].append(e.source)
        elif e.type == "receives_network_message":
            recvs_by_msg[e.target].append(e.source)
        elif e.type == "registers_network_message":
            regs_by_msg[e.target].append(e.source)

    for mid, send_ops in sends_by_msg.items():
        for recv_op in recvs_by_msg.get(mid, []):
            for send_op in send_ops:
                g.edge("network_dispatches_to", send_op, recv_op, protocol=g.nodes[mid].props.get("protocol"), message=g.nodes[mid].label)

    all_msg_ids = {nid for nid, n in g.nodes.items() if n.type == "network_message"}
    messages_no_receivers = sorted([g.nodes[mid].label for mid in all_msg_ids if not recvs_by_msg.get(mid)])
    messages_no_senders = sorted([g.nodes[mid].label for mid in all_msg_ids if not sends_by_msg.get(mid)])
    raw_unregistered_sent = sorted([
        g.nodes[mid].label for mid in all_msg_ids
        if g.nodes[mid].props.get("protocol") == "gmod_net" and sends_by_msg.get(mid) and not regs_by_msg.get(mid)
    ])

    stats.update({
        "unresolved_netstream_symbol_starts": len(unresolved_netstream_symbols),
        "messages_no_receivers": messages_no_receivers,
        "messages_no_senders": messages_no_senders,
        "raw_gmod_sent_without_registration": raw_unregistered_sent,
    })
    return g, stats


def summarize(g: GraphBuilder, stats: Dict[str, Any]) -> str:
    node_types = Counter(n.type for n in g.nodes.values())
    edge_types = Counter(e.type for e in g.edges.values())
    msg_protocols = Counter(n.props.get("protocol", "unknown") for n in g.nodes.values() if n.type == "network_message")
    sent = Counter(e.props.get("message") or g.nodes.get(e.target, Node("", "", "", {})).label for e in g.edges.values() if e.type == "sends_network_message")
    recv = Counter(e.props.get("message") or g.nodes.get(e.target, Node("", "", "", {})).label for e in g.edges.values() if e.type == "receives_network_message")
    dispatch = Counter(e.props.get("message", "unknown") for e in g.edges.values() if e.type == "network_dispatches_to")
    hot_files = Counter()
    for e in g.edges.values():
        if e.type in {"contains_network_operation", "contains_network_payload_operation", "contains_network_context"}:
            hot_files[e.props.get("file", "unknown")] += 1

    lines: List[str] = []
    lines.append("# Network graph summary")
    lines.append("")
    lines.append(f"Schema: `{SCHEMA}`")
    lines.append("")
    lines.append("## Inputs")
    for k, v in stats.get("inputs", {}).items():
        lines.append(f"- `{k}`: **{v}**")
    lines.append("")
    lines.append("## Totals")
    lines.append(f"- Nodes: **{len(g.nodes)}**")
    lines.append(f"- Edges: **{len(g.edges)}**")
    lines.append(f"- Network messages: **{node_types.get('network_message', 0)}**")
    lines.append(f"- Network operations: **{node_types.get('network_operation', 0)}**")
    lines.append(f"- Payload operations: **{node_types.get('network_payload_operation', 0)}**")
    lines.append(f"- Dispatch edges: **{edge_types.get('network_dispatches_to', 0)}**")
    lines.append(f"- Unresolved netstream symbolic starts: **{stats.get('unresolved_netstream_symbol_starts', 0)}**")
    lines.append("")
    lines.append("## Message protocols")
    for k, v in msg_protocols.most_common():
        lines.append(f"- `{k}`: **{v}**")
    lines.append("")
    lines.append("## Node types")
    for k, v in node_types.most_common():
        lines.append(f"- `{k}`: **{v}**")
    lines.append("")
    lines.append("## Edge types")
    for k, v in edge_types.most_common():
        lines.append(f"- `{k}`: **{v}**")
    lines.append("")
    lines.append("## Top sent messages")
    for k, v in sent.most_common(30):
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append("## Top received messages")
    for k, v in recv.most_common(30):
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append("## Top network dispatch pairs by message")
    for k, v in dispatch.most_common(30):
        lines.append(f"- `{k}`: {v} dispatch edge(s)")
    lines.append("")
    lines.append("## Messages with senders but no receivers")
    for name in stats.get("messages_no_receivers", [])[:50]:
        lines.append(f"- `{name}`")
    if len(stats.get("messages_no_receivers", [])) > 50:
        lines.append(f"- ... {len(stats['messages_no_receivers']) - 50} more")
    lines.append("")
    lines.append("## Messages with receivers but no senders")
    for name in stats.get("messages_no_senders", [])[:50]:
        lines.append(f"- `{name}`")
    if len(stats.get("messages_no_senders", [])) > 50:
        lines.append(f"- ... {len(stats['messages_no_senders']) - 50} more")
    lines.append("")
    lines.append("## Raw GMod net messages sent without util.AddNetworkString in manifests")
    for name in stats.get("raw_gmod_sent_without_registration", [])[:50]:
        lines.append(f"- `{name}`")
    if len(stats.get("raw_gmod_sent_without_registration", [])) > 50:
        lines.append(f"- ... {len(stats['raw_gmod_sent_without_registration']) - 50} more")
    lines.append("")
    lines.append("## Hot files by networking declarations")
    for k, v in hot_files.most_common(30):
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, help="Workspace root, e.g. E:/signalis_ai")
    parser.add_argument("--write", action="store_true", help="Write output files")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    manifest_root = workspace / "manifests"
    outdir = manifest_root / "normalized"

    g, stats = build_graph(manifest_root)
    nodes = [asdict(n) for n in sorted(g.nodes.values(), key=lambda x: x.id)]
    edges = [asdict(e) for e in sorted(g.edges.values(), key=lambda x: x.id)]
    summary = summarize(g, stats)

    print(summary)

    if args.write:
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "network_graph_nodes.json").write_text(json.dumps(nodes, indent=2, ensure_ascii=False), encoding="utf-8")
        (outdir / "network_graph_edges.json").write_text(json.dumps(edges, indent=2, ensure_ascii=False), encoding="utf-8")
        (outdir / "network_graph.json").write_text(json.dumps({"schema": SCHEMA, "nodes": nodes, "edges": edges, "qa": stats}, indent=2, ensure_ascii=False), encoding="utf-8")
        (outdir / "network_graph_summary.md").write_text(summary, encoding="utf-8")
        print(f"\nWrote network graph outputs to: {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
