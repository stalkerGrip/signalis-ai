#!/usr/bin/env python3
"""
build_hook_event_bus.py

Builds a deterministic event-bus model for Garry's Mod / NutScript hook usage.

Conceptual model:
  hook.Run("Event") / hook.Call("Event", ...) -> event emitter
  PLUGIN:Event(...), SCHEMA:Event(...), GM:Event(...), hook.Add("Event", id, fn) -> event listener

Inputs are manifest-first, with optional source scanning for GM/PLUGIN/SCHEMA methods.

Expected outputs:
  manifests/normalized/hook_event_emitters.json
  manifests/normalized/hook_event_listeners.json
  manifests/normalized/hook_event_graph.json
  manifests/normalized/hook_event_bus_qa.md
"""
from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

RETURN_PREFIXES = ("Can", "Should", "Get", "Is", "Check", "Allow", "Has", "PlayerCan")
LIFECYCLE_NAMES = {
    "InitializedSchema", "InitializedPlugins", "InitializedItems", "InitializedConfig",
    "PluginLoaded", "OnLoaded", "LoadData", "PostLoadData", "SaveData",
    "PersistenceSave", "PersistenceLoad", "SetupDatabase", "DatabaseConnected",
    "NutScriptLoaded", "PlayerInitialSpawn", "PostPlayerInitialSpawn",
    "PlayerLoadedChar", "PrePlayerLoadedChar", "CharacterLoaded", "CharacterPreSave",
}
UI_WORDS = ("HUD", "Tooltip", "Panel", "Menu", "Font", "Draw", "Paint", "Blur", "View", "LoadingScreen")
ENTITY_WORDS = ("Entity", "Storage", "Item", "Inventory", "Door", "Object", "Outfit", "Weapon", "Ragdoll", "NPC")
NETWORK_WORDS = ("Network", "Net", "Sync", "Message", "Send", "Receive")


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


def norm_path(p: Optional[str]) -> str:
    return (p or "").replace("/", "\\")


def infer_realm_from_file(file: str, fallback: str = "unknown") -> str:
    f = norm_path(file).lower()
    base = os.path.basename(f)
    if base.startswith("cl_") or "\\cl_" in f or "\\client\\" in f:
        return "client"
    if base.startswith("sv_") or "\\sv_" in f or "\\server\\" in f:
        return "server"
    if base.startswith("sh_") or "\\shared\\" in f:
        return "shared"
    return fallback if fallback and fallback != "unknown" else "shared"


def event_return_policy(name: str) -> str:
    if not name:
        return "unknown"
    if name.startswith(RETURN_PREFIXES):
        return "likely_returns"
    return "maybe_returns"


def classify_event(name: str, emitters: int = 0, listeners: int = 0) -> str:
    if not name:
        return "unknown"
    if name in LIFECYCLE_NAMES:
        return "framework_lifecycle"
    if name.startswith(("Can", "Should", "Get", "Is", "Check", "Allow", "Has")):
        return "query_or_gate"
    if any(w in name for w in NETWORK_WORDS):
        return "network_or_sync"
    if any(w in name for w in UI_WORDS):
        return "ui_extension_point"
    if any(w in name for w in ENTITY_WORDS):
        return "entity_inventory_domain"
    if name.startswith("Player") or name.startswith("OnPlayer") or name.startswith("PostPlayer"):
        return "player_lifecycle_or_action"
    if name[:1].islower():
        return "ad_hoc_lowercase_event"
    if emitters > 1 or listeners > 1:
        return "global_runtime_event"
    return "domain_event"


def stable_id(prefix: str, *parts: Any) -> str:
    raw = "|".join(str(p or "") for p in parts)
    # readable deterministic id, not cryptographic
    import hashlib
    return prefix + "_" + hashlib.sha1(raw.encode("utf-8", errors="ignore")).hexdigest()[:12]


def event_from_run(row: Dict[str, Any], resolved_index: Dict[Tuple[str, int, str, str], Dict[str, Any]]) -> Tuple[Optional[str], Dict[str, Any]]:
    file = norm_path(row.get("file"))
    line = int(row.get("line") or 0)
    hook_name = row.get("hook_name")
    symbol = row.get("symbol")
    key = (file, line, hook_name or "", symbol or "")
    resolved = resolved_index.get(key)
    meta: Dict[str, Any] = {}
    if resolved:
        meta.update({
            "normalization_status": "resolved",
            "resolution_source": resolved.get("resolution_source"),
            "resolution_confidence": resolved.get("resolution_confidence"),
            "resolved_symbol_value": resolved.get("resolved_symbol_value"),
        })
        return resolved.get("normalized_hook_name") or hook_name, meta
    if hook_name:
        meta["normalization_status"] = "literal"
        return hook_name, meta
    if symbol:
        meta["normalization_status"] = "unresolved_symbol"
        meta["symbol"] = symbol
        return None, meta
    meta["normalization_status"] = "unknown"
    return None, meta


def build_resolved_index(normalized_dir: Path) -> Dict[Tuple[str, int, str, str], Dict[str, Any]]:
    idx: Dict[Tuple[str, int, str, str], Dict[str, Any]] = {}
    for fn in ("resolved_hook_runs.json", "unresolved_hook_runs.json"):
        for row in read_json(normalized_dir / fn, []):
            file = norm_path(row.get("file"))
            line = int(row.get("line") or 0)
            key = (file, line, row.get("hook_name") or "", row.get("symbol") or "")
            idx[key] = row
    return idx


def load_hook_runs(manifests_dir: Path) -> List[Dict[str, Any]]:
    candidates = [
        manifests_dir / "plugins" / "hook_runs.json",
        manifests_dir / "custom_hooks" / "hook_runs.json",
    ]
    seen = set()
    out: List[Dict[str, Any]] = []
    for path in candidates:
        for r in read_json(path, []):
            key = (norm_path(r.get("file")), int(r.get("line") or 0), r.get("hook_name") or "", r.get("symbol") or "")
            if key in seen:
                continue
            seen.add(key)
            out.append(r)
    return out


def load_plugin_methods(manifests_dir: Path) -> List[Dict[str, Any]]:
    candidates = [
        manifests_dir / "plugins" / "plugin_methods.json",
        manifests_dir / "custom_hooks" / "plugin_methods.json",
    ]
    seen = set()
    out: List[Dict[str, Any]] = []
    for path in candidates:
        for r in read_json(path, []):
            name = r.get("method_name")
            if not name:
                continue
            file = norm_path(r.get("file"))
            line = int(r.get("line") or 0)
            key = (file, line, name, r.get("args") or "")
            if key in seen:
                continue
            seen.add(key)
            out.append(r)
    return out


def load_hook_adds(manifests_dir: Path) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    seen = set()
    for rel in ["cl_hooks.json", "sv_hooks.json", "sh_hooks.json", "unknown_hooks.json"]:
        path = manifests_dir / "hooks" / rel
        for r in read_json(path, []):
            name = r.get("hook_name")
            if not name:
                continue
            key = (norm_path(r.get("file")), int(r.get("line") or 0), name, r.get("identifier") or "")
            if key in seen:
                continue
            seen.add(key)
            out.append(r)
    return out


METHOD_RE = re.compile(r"^\s*function\s+(GM|PLUGIN|SCHEMA)\s*:\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)", re.M)
ASSIGN_METHOD_RE = re.compile(r"^\s*(GM|PLUGIN|SCHEMA)\s*\.\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*function\s*\(([^)]*)\)", re.M)


def iter_lua_files(root: Path) -> Iterable[Path]:
    if not root or not root.exists():
        return []
    return root.rglob("*.lua")


def relative_to_any(path: Path, roots: List[Path]) -> str:
    for root in roots:
        try:
            return norm_path(str(path.relative_to(root)))
        except ValueError:
            pass
    return norm_path(str(path))


def scan_source_methods(roots: List[Path]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    seen = set()
    existing_roots = [r for r in roots if r and r.exists()]
    for root in existing_roots:
        for p in root.rglob("*.lua"):
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            rel = relative_to_any(p, existing_roots)
            for regex in (METHOD_RE, ASSIGN_METHOD_RE):
                for m in regex.finditer(text):
                    owner, name, args = m.group(1), m.group(2), m.group(3)
                    line = text.count("\n", 0, m.start()) + 1
                    key = (rel, line, owner, name)
                    if key in seen:
                        continue
                    seen.add(key)
                    rows.append({
                        "type": "source_method",
                        "owner": owner,
                        "method_name": name,
                        "args": args.strip(),
                        "file": rel,
                        "line": line,
                        "realm": infer_realm_from_file(rel),
                        "framework_layer": "framework" if rel.startswith("gamemode\\") or rel.startswith("nutscript\\") else "domain",
                        "source": "source_scan",
                    })
    return rows


def make_emitters(hook_runs: List[Dict[str, Any]], resolved_index: Dict[Tuple[str, int, str, str], Dict[str, Any]]) -> List[Dict[str, Any]]:
    emitters: List[Dict[str, Any]] = []
    for r in hook_runs:
        event, meta = event_from_run(r, resolved_index)
        file = norm_path(r.get("file"))
        line = int(r.get("line") or 0)
        realm = r.get("realm") if r.get("realm") != "unknown" else infer_realm_from_file(file)
        emitter = {
            "id": stable_id("emitter", file, line, event or meta.get("symbol"), r.get("call_type")),
            "event": event,
            "unresolved_symbol": meta.get("symbol") if not event else None,
            "call_type": r.get("call_type") or "Run",
            "file": file,
            "line": line,
            "realm": realm,
            "framework_layer": r.get("framework_layer") or "unknown",
            "plugin_context": r.get("plugin_context") or "unknown_file",
            "return_policy": event_return_policy(event or ""),
            "source_manifest_type": r.get("type"),
            **meta,
        }
        emitters.append(emitter)
    return emitters


def method_owner_from_file(file: str) -> str:
    f = norm_path(file).lower()
    if "\\schema\\" in f or f.startswith("schema\\"):
        return "SCHEMA"
    return "PLUGIN"


def make_listeners(manifests_dir: Path, source_roots: List[Path]) -> List[Dict[str, Any]]:
    listeners: List[Dict[str, Any]] = []
    seen = set()

    for r in load_plugin_methods(manifests_dir):
        event = r.get("method_name")
        file = norm_path(r.get("file"))
        line = int(r.get("line") or 0)
        owner = r.get("owner") or method_owner_from_file(file)
        key = (event, file, line, owner, "auto_registered_method")
        if key in seen:
            continue
        seen.add(key)
        listeners.append({
            "id": stable_id("listener", *key),
            "event": event,
            "listener_type": "schema_method" if owner == "SCHEMA" else "plugin_method",
            "owner": owner,
            "method_name": event,
            "args": r.get("args"),
            "file": file,
            "line": line,
            "realm": r.get("realm") if r.get("realm") != "unknown" else infer_realm_from_file(file),
            "framework_layer": r.get("framework_layer") or "unknown",
            "plugin_context": r.get("plugin_context") or "unknown_file",
            "registration_mechanism": "nut.plugin.load_auto_hook_add",
            "source": "manifest_plugin_methods",
        })

    for r in load_hook_adds(manifests_dir):
        event = r.get("hook_name")
        file = norm_path(r.get("file"))
        line = int(r.get("line") or 0)
        identifier = r.get("identifier")
        key = (event, file, line, identifier, "hook_add")
        if key in seen:
            continue
        seen.add(key)
        listeners.append({
            "id": stable_id("listener", *key),
            "event": event,
            "listener_type": "hook_add",
            "owner": identifier,
            "identifier": identifier,
            "file": file,
            "line": line,
            "realm": r.get("realm") if r.get("realm") != "unknown" else infer_realm_from_file(file),
            "framework_layer": r.get("framework_layer") or "unknown",
            "frequency_class": r.get("frequency_class"),
            "risk_class": r.get("risk_class"),
            "registration_mechanism": "hook.Add",
            "source": "manifest_hook_adds",
        })

    # Optional but important: GM methods are normal hook.Call fallback listeners and are often absent from manifests.
    for r in scan_source_methods(source_roots):
        event = r.get("method_name")
        owner = r.get("owner")
        file = norm_path(r.get("file"))
        line = int(r.get("line") or 0)
        listener_type = {"GM": "gamemode_method", "SCHEMA": "schema_method", "PLUGIN": "plugin_method"}.get(owner, "method")
        key = (event, file, line, owner, "source_method")
        if key in seen:
            continue
        seen.add(key)
        listeners.append({
            "id": stable_id("listener", *key),
            "event": event,
            "listener_type": listener_type,
            "owner": owner,
            "method_name": event,
            "args": r.get("args"),
            "file": file,
            "line": line,
            "realm": r.get("realm"),
            "framework_layer": r.get("framework_layer"),
            "registration_mechanism": "GM_hook_call_fallback" if owner == "GM" else "source_declared_auto_hook_add",
            "source": "source_scan",
        })

    return listeners


def realm_compatible(emitter_realm: str, listener_realm: str) -> bool:
    if not emitter_realm or emitter_realm == "unknown" or listener_realm == "unknown":
        return True
    if emitter_realm == "shared" or listener_realm == "shared":
        return True
    return emitter_realm == listener_realm


def build_graph(emitters: List[Dict[str, Any]], listeners: List[Dict[str, Any]]) -> Dict[str, Any]:
    emit_by_event: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    listen_by_event: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    unresolved_emitters: List[Dict[str, Any]] = []
    for e in emitters:
        if e.get("event"):
            emit_by_event[e["event"]].append(e)
        else:
            unresolved_emitters.append(e)
    for l in listeners:
        if l.get("event"):
            listen_by_event[l["event"]].append(l)

    events = sorted(set(emit_by_event) | set(listen_by_event))
    nodes = []
    edges = []
    for event in events:
        es = emit_by_event.get(event, [])
        ls = listen_by_event.get(event, [])
        nodes.append({
            "event": event,
            "event_class": classify_event(event, len(es), len(ls)),
            "return_policy": event_return_policy(event),
            "emitter_count": len(es),
            "listener_count": len(ls),
            "realms_emitted": sorted({e.get("realm") or "unknown" for e in es}),
            "realms_listened": sorted({l.get("realm") or "unknown" for l in ls}),
            "has_emitters": bool(es),
            "has_listeners": bool(ls),
        })
        for e in es:
            for l in ls:
                compatible = realm_compatible(e.get("realm", "unknown"), l.get("realm", "unknown"))
                edges.append({
                    "id": stable_id("edge", e["id"], l["id"]),
                    "event": event,
                    "from_emitter_id": e["id"],
                    "to_listener_id": l["id"],
                    "from_file": e.get("file"),
                    "from_line": e.get("line"),
                    "to_file": l.get("file"),
                    "to_line": l.get("line"),
                    "listener_type": l.get("listener_type"),
                    "realm_compatible": compatible,
                    "edge_confidence": "high" if compatible else "low",
                    "return_policy": event_return_policy(event),
                })

    return {
        "schema_version": "hook_event_bus.v1",
        "summary": {
            "event_count": len(events),
            "emitter_count": len(emitters),
            "resolved_emitter_count": sum(1 for e in emitters if e.get("event")),
            "unresolved_symbol_emitter_count": len(unresolved_emitters),
            "listener_count": len(listeners),
            "edge_count": len(edges),
            "events_with_emitters_no_listeners": sum(1 for n in nodes if n["has_emitters"] and not n["has_listeners"]),
            "events_with_listeners_no_emitters": sum(1 for n in nodes if n["has_listeners"] and not n["has_emitters"]),
        },
        "events": nodes,
        "edges": edges,
        "unresolved_symbol_emitters": unresolved_emitters,
    }


def write_qa(path: Path, graph: Dict[str, Any], emitters: List[Dict[str, Any]], listeners: List[Dict[str, Any]]) -> None:
    events = graph["events"]
    top_emit = Counter(e.get("event") or e.get("unresolved_symbol") or "<unknown>" for e in emitters).most_common(30)
    top_listen = Counter(l.get("event") or "<unknown>" for l in listeners).most_common(30)
    no_listeners = [e for e in events if e["has_emitters"] and not e["has_listeners"]]
    no_emitters = [e for e in events if e["has_listeners"] and not e["has_emitters"]]
    by_class = Counter(e["event_class"] for e in events)
    by_listener_type = Counter(l.get("listener_type") for l in listeners)

    lines = []
    s = graph["summary"]
    lines += [
        "# Hook event bus QA",
        "",
        "## Summary",
        f"- Events: **{s['event_count']}**",
        f"- Emitters: **{s['emitter_count']}**",
        f"- Resolved emitters: **{s['resolved_emitter_count']}**",
        f"- Unresolved symbol emitters: **{s['unresolved_symbol_emitter_count']}**",
        f"- Listeners: **{s['listener_count']}**",
        f"- Emitter → listener edges: **{s['edge_count']}**",
        f"- Events with emitters but no listeners: **{s['events_with_emitters_no_listeners']}**",
        f"- Events with listeners but no emitters: **{s['events_with_listeners_no_emitters']}**",
        "",
        "## Event classes",
    ]
    for k, v in by_class.most_common():
        lines.append(f"- `{k}`: **{v}**")
    lines += ["", "## Listener types"]
    for k, v in by_listener_type.most_common():
        lines.append(f"- `{k}`: **{v}**")
    lines += ["", "## Top emitted events"]
    for k, v in top_emit:
        lines.append(f"- `{k}`: {v}")
    lines += ["", "## Top listened events"]
    for k, v in top_listen:
        lines.append(f"- `{k}`: {v}")
    lines += ["", "## Top events with emitters but no listeners"]
    for e in sorted(no_listeners, key=lambda x: (-x["emitter_count"], x["event"]))[:50]:
        lines.append(f"- `{e['event']}`: emitters={e['emitter_count']}, class={e['event_class']}, return={e['return_policy']}")
    lines += ["", "## Top events with listeners but no emitters"]
    for e in sorted(no_emitters, key=lambda x: (-x["listener_count"], x["event"]))[:50]:
        lines.append(f"- `{e['event']}`: listeners={e['listener_count']}, class={e['event_class']}, return={e['return_policy']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build normalized NutScript/GMod hook event-bus graph.")
    ap.add_argument("--workspace", default=".", help="Workspace root, e.g. E:/signalis_ai")
    ap.add_argument("--manifests-dir", default=None, help="Override manifests dir. Default: <workspace>/manifests")
    ap.add_argument("--normalized-dir", default=None, help="Override normalized dir. Default: <manifests-dir>/normalized")
    ap.add_argument("--source-root", action="append", default=[], help="Optional source root to scan for GM/PLUGIN/SCHEMA methods. Can be repeated.")
    ap.add_argument("--nutscript-root", default=None, help="Optional NutScript source root to scan.")
    ap.add_argument("--write", action="store_true", help="Write output files. Without this, prints summary only.")
    args = ap.parse_args()

    workspace = Path(args.workspace)
    manifests_dir = Path(args.manifests_dir) if args.manifests_dir else workspace / "manifests"
    normalized_dir = Path(args.normalized_dir) if args.normalized_dir else manifests_dir / "normalized"
    source_roots = [Path(x) for x in args.source_root]
    if args.nutscript_root:
        source_roots.append(Path(args.nutscript_root))

    resolved_index = build_resolved_index(normalized_dir)
    hook_runs = load_hook_runs(manifests_dir)
    emitters = make_emitters(hook_runs, resolved_index)
    listeners = make_listeners(manifests_dir, source_roots)
    graph = build_graph(emitters, listeners)

    summary = graph["summary"]
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if args.write:
        normalized_dir.mkdir(parents=True, exist_ok=True)
        write_json(normalized_dir / "hook_event_emitters.json", emitters)
        write_json(normalized_dir / "hook_event_listeners.json", listeners)
        write_json(normalized_dir / "hook_event_graph.json", graph)
        write_qa(normalized_dir / "hook_event_bus_qa.md", graph, emitters, listeners)
        print(f"Wrote: {normalized_dir / 'hook_event_emitters.json'}")
        print(f"Wrote: {normalized_dir / 'hook_event_listeners.json'}")
        print(f"Wrote: {normalized_dir / 'hook_event_graph.json'}")
        print(f"Wrote: {normalized_dir / 'hook_event_bus_qa.md'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
