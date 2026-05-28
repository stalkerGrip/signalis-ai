#!/usr/bin/env python3
"""
build_runtime_graph.py

Runtime Graph V1 for the Signalis AI Orchestration Pipeline.

V1 scope:
  - Consumes normalized hook event-bus artifacts.
  - Produces stable graph nodes and edges suitable for QA, graph analysis, and Qdrant ingestion.
  - Uses stable semantic IDs such as hook:SaveData, file:plugins/foo/sv_hooks.lua,
    plugin:healthproblems, listener:<hash>, emitter:<hash>.

Expected inputs:
  manifests/normalized/hook_event_emitters.json
  manifests/normalized/hook_event_listeners.json
  manifests/normalized/hook_event_graph.json

Expected outputs:
  manifests/normalized/runtime_graph_nodes.json
  manifests/normalized/runtime_graph_edges.json
  manifests/normalized/runtime_graph_summary.md

Design:
  - Manifest-first. No source scanning here.
  - Source scanning and extractor-gap detection belong to QA/extractor phases, not runtime graph assembly.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

SCHEMA_VERSION = "runtime_graph.v1"


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def norm_path(value: Optional[str]) -> str:
    return (value or "").replace("/", "\\")


def sha12(*parts: Any) -> str:
    raw = "|".join(str(p or "") for p in parts)
    return hashlib.sha1(raw.encode("utf-8", errors="ignore")).hexdigest()[:12]


def slug(value: Any) -> str:
    text = str(value or "unknown").strip().replace("\\", "/")
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^A-Za-z0-9_./:-]+", "_", text)
    return text or "unknown"


def node_id(kind: str, value: Any) -> str:
    # Keep human-readable IDs for canonical runtime concepts.
    if kind in {"hook", "file", "plugin", "schema", "gamemode", "realm", "event_class"}:
        return f"{kind}:{slug(value)}"
    return f"{kind}:{sha12(value)}"


def infer_plugin_from_file(file: str, plugin_context: Optional[str] = None) -> Optional[str]:
    if plugin_context and plugin_context not in {"unknown", "unknown_file", "plugin_file"}:
        return str(plugin_context)

    f = norm_path(file)
    parts = [p for p in f.split("\\") if p]
    lower = [p.lower() for p in parts]

    # schema files are not plugins.
    if parts and parts[0].lower() == "schema":
        return None
    if parts and parts[0].lower() == "gamemode":
        return None

    # plugins/foo/...
    if "plugins" in lower:
        idx = lower.index("plugins")
        if idx + 1 < len(parts):
            return parts[idx + 1]

    # nutscript/plugins/foo/...
    if len(parts) >= 3 and parts[-3].lower() == "plugins":
        return parts[-2]

    return None


def infer_owner_node(listener: Dict[str, Any]) -> Optional[Tuple[str, str]]:
    listener_type = listener.get("listener_type")
    owner = listener.get("owner")
    file = norm_path(listener.get("file"))

    if listener_type == "gamemode_method" or owner == "GM":
        return (node_id("gamemode", "GM"), "gamemode")
    if listener_type == "schema_method" or owner == "SCHEMA" or file.lower().startswith("schema\\"):
        return (node_id("schema", "schema"), "schema")

    plugin = infer_plugin_from_file(file, listener.get("plugin_context"))
    if plugin:
        return (node_id("plugin", plugin), "plugin")

    if owner and owner not in {"PLUGIN", "SCHEMA", "GM"}:
        # hook.Add identifier can be table/string; keep as hook_listener_owner if useful.
        return (f"hook_owner:{slug(owner)}", "hook_owner")

    return None


def add_node(nodes: Dict[str, Dict[str, Any]], node: Dict[str, Any]) -> None:
    nid = node["id"]
    if nid not in nodes:
        nodes[nid] = node
        return

    # Merge simple counters/sets deterministically.
    existing = nodes[nid]
    for k, v in node.items():
        if k in {"id", "type", "label"}:
            continue
        if v is None or v == "":
            continue
        if k not in existing or existing[k] is None or existing[k] == "" or existing[k] == [] or existing[k] == {}:
            existing[k] = v
        elif existing[k] != v:
            if k.endswith("s") and isinstance(existing[k], list):
                values = set(map(str, existing[k]))
                if isinstance(v, list):
                    values.update(map(str, v))
                else:
                    values.add(str(v))
                existing[k] = sorted(values)


def add_edge(edges: Dict[str, Dict[str, Any]], edge: Dict[str, Any]) -> None:
    eid = edge.get("id") or f"edge:{sha12(edge.get('source'), edge.get('target'), edge.get('type'), edge.get('event'))}"
    edge["id"] = eid
    if eid not in edges:
        edges[eid] = edge


def event_node_from_graph_event(row: Dict[str, Any]) -> Dict[str, Any]:
    event = row.get("event")
    return {
        "id": node_id("hook", event),
        "type": "hook_event",
        "label": event,
        "event": event,
        "event_class": row.get("event_class"),
        "return_policy": row.get("return_policy"),
        "emitter_count": row.get("emitter_count", 0),
        "listener_count": row.get("listener_count", 0),
        "realms_emitted": row.get("realms_emitted", []),
        "realms_listened": row.get("realms_listened", []),
        "has_emitters": row.get("has_emitters", False),
        "has_listeners": row.get("has_listeners", False),
        "source": "hook_event_graph",
    }


def build_runtime_graph(normalized_dir: Path) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    emitters = read_json(normalized_dir / "hook_event_emitters.json", [])
    listeners = read_json(normalized_dir / "hook_event_listeners.json", [])
    hook_graph = read_json(normalized_dir / "hook_event_graph.json", {})
    event_rows = hook_graph.get("events", []) if isinstance(hook_graph, dict) else []
    hook_edges = hook_graph.get("edges", []) if isinstance(hook_graph, dict) else []

    if not emitters and not listeners and not event_rows:
        raise FileNotFoundError(
            f"Missing hook event-bus inputs in {normalized_dir}. Run build_hook_event_bus.py first."
        )

    nodes: Dict[str, Dict[str, Any]] = {}
    edges: Dict[str, Dict[str, Any]] = {}

    # Event class nodes, useful for taxonomy-level filtering.
    for er in event_rows:
        event = er.get("event")
        if not event:
            continue
        event_id = node_id("hook", event)
        add_node(nodes, event_node_from_graph_event(er))
        cls = er.get("event_class") or "unknown"
        class_id = node_id("event_class", cls)
        add_node(nodes, {
            "id": class_id,
            "type": "event_class",
            "label": cls,
            "event_class": cls,
            "source": "derived_taxonomy",
        })
        add_edge(edges, {
            "source": event_id,
            "target": class_id,
            "type": "classified_as",
            "event": event,
            "confidence": "medium",
            "source_artifact": "hook_event_graph",
        })

    # Emitters: file -> emitter -> hook event, plus plugin/file ownership.
    for e in emitters:
        event = e.get("event")
        file = norm_path(e.get("file"))
        line = e.get("line")
        realm = e.get("realm") or "unknown"
        emitter_id = f"emitter:{e.get('id') or sha12(file, line, event, e.get('unresolved_symbol'))}"
        file_id = node_id("file", file)
        event_id = node_id("hook", event) if event else f"unresolved_hook_symbol:{sha12(e.get('unresolved_symbol'), file, line)}"

        add_node(nodes, {
            "id": file_id,
            "type": "file",
            "label": file,
            "path": file,
            "realm": realm,
            "framework_layer": e.get("framework_layer"),
            "source": "emitter_file",
        })
        add_node(nodes, {
            "id": emitter_id,
            "type": "hook_emitter",
            "label": f"emit {event or e.get('unresolved_symbol')} @ {file}:{line}",
            "event": event,
            "unresolved_symbol": e.get("unresolved_symbol"),
            "file": file,
            "line": line,
            "realm": realm,
            "call_type": e.get("call_type"),
            "return_policy": e.get("return_policy"),
            "normalization_status": e.get("normalization_status"),
            "resolution_source": e.get("resolution_source"),
            "resolution_confidence": e.get("resolution_confidence"),
            "source_artifact": "hook_event_emitters",
        })
        if event:
            add_node(nodes, {
                "id": event_id,
                "type": "hook_event",
                "label": event,
                "event": event,
                "return_policy": e.get("return_policy"),
                "source": "hook_event_emitters",
            })
        else:
            add_node(nodes, {
                "id": event_id,
                "type": "unresolved_hook_symbol",
                "label": str(e.get("unresolved_symbol")),
                "symbol": e.get("unresolved_symbol"),
                "source": "hook_event_emitters",
            })

        add_edge(edges, {
            "source": file_id,
            "target": emitter_id,
            "type": "contains_emitter",
            "event": event,
            "file": file,
            "line": line,
            "realm": realm,
            "confidence": "high",
            "source_artifact": "runtime_graph_builder",
        })
        add_edge(edges, {
            "source": emitter_id,
            "target": event_id,
            "type": "emits",
            "event": event,
            "file": file,
            "line": line,
            "realm": realm,
            "confidence": "high" if event else "low",
            "source_artifact": "hook_event_emitters",
        })

        plugin = infer_plugin_from_file(file, e.get("plugin_context"))
        if plugin:
            plugin_id = node_id("plugin", plugin)
            add_node(nodes, {
                "id": plugin_id,
                "type": "plugin",
                "label": plugin,
                "plugin": plugin,
                "source_artifact": "derived_from_file_path",
            })
            add_edge(edges, {
                "source": plugin_id,
                "target": file_id,
                "type": "owns_file",
                "confidence": "medium",
                "source_artifact": "derived_from_file_path",
            })
            add_edge(edges, {
                "source": plugin_id,
                "target": event_id,
                "type": "emits_event",
                "event": event,
                "confidence": "medium" if event else "low",
                "source_artifact": "derived_from_emitter_file",
            })

    # Listeners: file/owner -> listener -> hook event.
    for l in listeners:
        event = l.get("event")
        file = norm_path(l.get("file"))
        line = l.get("line")
        realm = l.get("realm") or "unknown"
        listener_id = f"listener:{l.get('id') or sha12(file, line, event, l.get('listener_type'), l.get('owner'))}"
        file_id = node_id("file", file)
        event_id = node_id("hook", event)

        add_node(nodes, {
            "id": file_id,
            "type": "file",
            "label": file,
            "path": file,
            "realm": realm,
            "framework_layer": l.get("framework_layer"),
            "source": "listener_file",
        })
        add_node(nodes, {
            "id": listener_id,
            "type": "hook_listener",
            "label": f"listen {event} @ {file}:{line}",
            "event": event,
            "listener_type": l.get("listener_type"),
            "owner": l.get("owner"),
            "identifier": l.get("identifier"),
            "method_name": l.get("method_name"),
            "file": file,
            "line": line,
            "realm": realm,
            "registration_mechanism": l.get("registration_mechanism"),
            "source_artifact": "hook_event_listeners",
        })
        add_node(nodes, {
            "id": event_id,
            "type": "hook_event",
            "label": event,
            "event": event,
            "source_artifact": "hook_event_listeners",
        })

        add_edge(edges, {
            "source": file_id,
            "target": listener_id,
            "type": "contains_listener",
            "event": event,
            "file": file,
            "line": line,
            "realm": realm,
            "confidence": "high",
            "source_artifact": "runtime_graph_builder",
        })
        add_edge(edges, {
            "source": listener_id,
            "target": event_id,
            "type": "listens_to",
            "event": event,
            "file": file,
            "line": line,
            "realm": realm,
            "confidence": "high",
            "source_artifact": "hook_event_listeners",
        })

        owner = infer_owner_node(l)
        if owner:
            owner_id, owner_type = owner
            label = owner_id.split(":", 1)[1]
            add_node(nodes, {
                "id": owner_id,
                "type": owner_type,
                "label": label,
                "source_artifact": "derived_listener_owner",
            })
            add_edge(edges, {
                "source": owner_id,
                "target": listener_id,
                "type": "registers_listener",
                "event": event,
                "confidence": "high" if owner_type in {"plugin", "schema", "gamemode"} else "medium",
                "source_artifact": "derived_listener_owner",
            })
            add_edge(edges, {
                "source": owner_id,
                "target": event_id,
                "type": "listens_to_event",
                "event": event,
                "confidence": "medium",
                "source_artifact": "derived_listener_owner",
            })
            if owner_type == "plugin":
                add_edge(edges, {
                    "source": owner_id,
                    "target": file_id,
                    "type": "owns_file",
                    "confidence": "medium",
                    "source_artifact": "derived_from_file_path",
                })

    # Direct emitter -> listener propagation edges copied from hook_event_graph.
    # These are the useful runtime topology edges.
    for he in hook_edges:
        event = he.get("event")
        src = f"emitter:{he.get('from_emitter_id')}"
        dst = f"listener:{he.get('to_listener_id')}"
        if src not in nodes or dst not in nodes:
            # Keep edge only when endpoints exist; avoids dangling topology if inputs are inconsistent.
            continue
        add_edge(edges, {
            "source": src,
            "target": dst,
            "type": "dispatches_to",
            "event": event,
            "realm_compatible": he.get("realm_compatible"),
            "return_policy": he.get("return_policy"),
            "confidence": he.get("edge_confidence") or "medium",
            "from_file": he.get("from_file"),
            "from_line": he.get("from_line"),
            "to_file": he.get("to_file"),
            "to_line": he.get("to_line"),
            "source_artifact": "hook_event_graph",
        })

    # Add realm nodes for filtering.
    for n in list(nodes.values()):
        realm = n.get("realm")
        if not realm or realm == "unknown":
            continue
        rid = node_id("realm", realm)
        add_node(nodes, {
            "id": rid,
            "type": "realm",
            "label": realm,
            "realm": realm,
            "source_artifact": "derived_realm",
        })
        add_edge(edges, {
            "source": n["id"],
            "target": rid,
            "type": "runs_in_realm",
            "confidence": "medium",
            "source_artifact": "derived_realm",
        })

    node_list = sorted(nodes.values(), key=lambda x: (x.get("type", ""), x.get("id", "")))
    edge_list = sorted(edges.values(), key=lambda x: (x.get("type", ""), x.get("source", ""), x.get("target", ""), x.get("event") or ""))

    summary = summarize(node_list, edge_list)
    return node_list, edge_list, summary


def summarize(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_node_type = Counter(n.get("type", "unknown") for n in nodes)
    by_edge_type = Counter(e.get("type", "unknown") for e in edges)
    events = [n for n in nodes if n.get("type") == "hook_event"]
    files = [n for n in nodes if n.get("type") == "file"]
    plugins = [n for n in nodes if n.get("type") == "plugin"]

    emit_edges = [e for e in edges if e.get("type") == "emits"]
    listen_edges = [e for e in edges if e.get("type") == "listens_to"]
    dispatch_edges = [e for e in edges if e.get("type") == "dispatches_to"]

    event_emit_count = Counter(e.get("event") for e in emit_edges if e.get("event"))
    event_listen_count = Counter(e.get("event") for e in listen_edges if e.get("event"))
    file_activity = Counter()
    for e in edges:
        if e.get("type") in {"contains_emitter", "contains_listener"}:
            file_activity[e.get("source")] += 1

    hot_files = []
    file_by_id = {n["id"]: n for n in files}
    for fid, count in file_activity.most_common(25):
        hot_files.append({"file": file_by_id.get(fid, {}).get("path", fid), "activity": count})

    return {
        "schema_version": SCHEMA_VERSION,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "node_type_counts": dict(by_node_type),
        "edge_type_counts": dict(by_edge_type),
        "hook_event_count": len(events),
        "file_count": len(files),
        "plugin_count": len(plugins),
        "dispatch_edge_count": len(dispatch_edges),
        "top_emitted_events": [{"event": k, "count": v} for k, v in event_emit_count.most_common(30)],
        "top_listened_events": [{"event": k, "count": v} for k, v in event_listen_count.most_common(30)],
        "top_runtime_dispatch_events": [
            {"event": k, "edges": v}
            for k, v in Counter(e.get("event") for e in dispatch_edges if e.get("event")).most_common(30)
        ],
        "hot_files": hot_files,
    }


def write_summary_md(path: Path, summary: Dict[str, Any]) -> None:
    lines: List[str] = []
    lines.extend([
        "# Runtime graph summary",
        "",
        f"Schema: `{summary['schema_version']}`",
        "",
        "## Totals",
        f"- Nodes: **{summary['node_count']}**",
        f"- Edges: **{summary['edge_count']}**",
        f"- Hook events: **{summary['hook_event_count']}**",
        f"- Files: **{summary['file_count']}**",
        f"- Plugins: **{summary['plugin_count']}**",
        f"- Runtime dispatch edges: **{summary['dispatch_edge_count']}**",
        "",
        "## Node types",
    ])
    for k, v in sorted(summary["node_type_counts"].items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- `{k}`: **{v}**")

    lines.extend(["", "## Edge types"])
    for k, v in sorted(summary["edge_type_counts"].items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- `{k}`: **{v}**")

    lines.extend(["", "## Top emitted events"])
    for row in summary["top_emitted_events"][:30]:
        lines.append(f"- `{row['event']}`: {row['count']}")

    lines.extend(["", "## Top listened events"])
    for row in summary["top_listened_events"][:30]:
        lines.append(f"- `{row['event']}`: {row['count']}")

    lines.extend(["", "## Top runtime dispatch events"])
    for row in summary["top_runtime_dispatch_events"][:30]:
        lines.append(f"- `{row['event']}`: {row['edges']} dispatch edge(s)")

    lines.extend(["", "## Hot files by emitter/listener declarations"])
    for row in summary["hot_files"][:25]:
        lines.append(f"- `{row['file']}`: {row['activity']}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Runtime Graph V1 from normalized hook event-bus manifests.")
    parser.add_argument("--workspace", default=".", help="Workspace root, e.g. E:/signalis_ai")
    parser.add_argument("--normalized-dir", default=None, help="Override normalized dir. Default: <workspace>/manifests/normalized")
    parser.add_argument("--write", action="store_true", help="Write output files. Without this, prints summary only.")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    normalized_dir = Path(args.normalized_dir) if args.normalized_dir else workspace / "manifests" / "normalized"

    nodes, edges, summary = build_runtime_graph(normalized_dir)
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if args.write:
        normalized_dir.mkdir(parents=True, exist_ok=True)
        write_json(normalized_dir / "runtime_graph_nodes.json", nodes)
        write_json(normalized_dir / "runtime_graph_edges.json", edges)
        write_summary_md(normalized_dir / "runtime_graph_summary.md", summary)
        print(f"Wrote: {normalized_dir / 'runtime_graph_nodes.json'}")
        print(f"Wrote: {normalized_dir / 'runtime_graph_edges.json'}")
        print(f"Wrote: {normalized_dir / 'runtime_graph_summary.md'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
