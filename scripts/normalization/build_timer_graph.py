#!/usr/bin/env python3
"""
build_timer_graph.py

Timer/runtime scheduler graph builder for Signalis AI Orchestration Pipeline.

Manifest-first normalizer over existing timer manifests:
  manifests/timers/timer_creates.json
  manifests/timers/timer_simples.json
  manifests/timers/timer_operations.json
  manifests/timers/entity_timer_calls.json
  manifests/timers/player_action_timers.json
  manifests/entities/entity_timer_calls.json  (optional legacy/duplicate source)

Outputs:
  manifests/normalized/timer_graph_nodes.json
  manifests/normalized/timer_graph_edges.json
  manifests/normalized/timer_graph.json
  manifests/normalized/timer_graph_summary.md

Design goals:
  - Stable IDs for Qdrant/graph ingestion.
  - File/plugin/subsystem ownership edges.
  - Timer semantics classification: repeating/infinite, one-shot, entity simulation, player action, etc.
  - QA flags for dynamic timer names and high-frequency/infinite timers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

SCHEMA = "timer_graph.v1"


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=False)


def norm_path(value: Optional[str]) -> str:
    if not value:
        return "unknown"
    return str(value).replace("/", "\\").strip()


def stable_hash(*parts: Any, n: int = 12) -> str:
    text = "|".join(str(p) for p in parts)
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()[:n]


def stable_id(kind: str, *parts: Any) -> str:
    safe = [str(p).strip().replace("\\", "/") for p in parts if p is not None and str(p).strip() != ""]
    if not safe:
        return f"{kind}:unknown"
    raw = ":".join(safe)
    # Keep readable IDs for simple values; hash long/source-position IDs.
    if len(raw) <= 96 and re.fullmatch(r"[A-Za-z0-9_./:\-]+", raw):
        return f"{kind}:{raw}"
    return f"{kind}:{stable_hash(kind, raw)}"


def add_node(nodes: Dict[str, Dict[str, Any]], node_id: str, node_type: str, label: str, **props: Any) -> str:
    if node_id not in nodes:
        node = {"id": node_id, "type": node_type, "label": label}
        node.update({k: v for k, v in props.items() if v is not None})
        nodes[node_id] = node
    else:
        # Merge non-conflicting metadata; preserve original label/type.
        for k, v in props.items():
            if v is not None and k not in nodes[node_id]:
                nodes[node_id][k] = v
    return node_id


def add_edge(edges: List[Dict[str, Any]], seen: set, src: str, dst: str, edge_type: str, **props: Any) -> None:
    key = (src, dst, edge_type, json.dumps(props, ensure_ascii=False, sort_keys=True, default=str))
    if key in seen:
        return
    seen.add(key)
    edge = {"source": src, "target": dst, "type": edge_type}
    edge.update({k: v for k, v in props.items() if v is not None})
    edges.append(edge)


def infer_realm(file: str, explicit: Optional[str] = None) -> str:
    explicit = (explicit or "").lower().strip()
    if explicit in {"server", "client", "shared"}:
        return explicit
    low = file.replace("\\", "/").lower()
    name = low.rsplit("/", 1)[-1]
    if name.startswith("sv_") or "/sv_" in low or low.endswith("/init.lua"):
        return "server"
    if name.startswith("cl_") or "/cl_" in low or low.endswith("/cl_init.lua"):
        return "client"
    if name.startswith("sh_") or "/sh_" in low or name in {"shared.lua"}:
        return "shared"
    return "shared"


def infer_plugin(file: str) -> Optional[str]:
    p = file.replace("/", "\\")
    parts = [x for x in p.split("\\") if x]
    if "plugins" in parts:
        i = parts.index("plugins")
        if i + 1 < len(parts):
            name = parts[i + 1]
            # Single-file plugin: plugins\recognition.lua => recognition
            return re.sub(r"\.lua$", "", name, flags=re.I)
    if parts and parts[0] == "schema":
        return "schema"
    if parts and parts[0] == "gamemode":
        return "gamemode"
    if parts and parts[0] == "entities":
        return "entities"
    return None


def classify_subsystem(file: str, name_expr: str = "", method: str = "") -> str:
    text = f"{file} {name_expr} {method}".lower()
    rules = [
        ("disease", "health_status"), ("health", "health_status"), ("pain", "health_status"),
        ("hud", "ui_hud"), ("interface", "ui_hud"), ("3d2d", "ui_hud"),
        ("inventory", "inventory_item_storage"), ("inv", "inventory_item_storage"), ("storage", "inventory_item_storage"),
        ("ore", "entity_production"), ("smelter", "entity_production"), ("craft", "crafting"),
        ("food", "food_spoilage"), ("cooking", "food_spoilage"),
        ("loot", "loot_spawn"),
        ("vendor", "vendor"),
        ("char", "character"), ("player", "player_action"), ("ragdoll", "player_action"),
        ("save", "persistence"), ("persist", "persistence"), ("database", "persistence"),
        ("nextbot", "ai_entity"), ("npc", "ai_entity"), ("terminator", "ai_entity"),
    ]
    for needle, cls in rules:
        if needle in text:
            return cls
    return "misc"


def is_dynamic_expr(expr: Optional[str]) -> bool:
    if expr is None:
        return False
    s = str(expr).strip()
    if not s:
        return False
    # If already a clean literal captured without quotes, treat as literal-ish unless it has operators/calls.
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_:\-.]*", s):
        # common variable names are dynamic, not literal timer names
        return s in {"timerName", "uniqueID", "timerID", "id", "name", "key", "k", "v", "self", "client", "ply", "entity"}
    return True


def parse_num(expr: Optional[str]) -> Optional[float]:
    if expr is None:
        return None
    s = str(expr).strip().strip('"\'')
    try:
        return float(s)
    except Exception:
        return None


def classify_timer(entry: Dict[str, Any]) -> Tuple[str, List[str]]:
    typ = entry.get("type", "")
    file = norm_path(entry.get("file"))
    name = str(entry.get("timer_name") or entry.get("timer_name_expr") or entry.get("method_name") or "")
    delay_expr = entry.get("delay_expr")
    rep_expr = entry.get("repetitions_expr")
    delay = parse_num(delay_expr)
    reps = parse_num(rep_expr)
    reasons: List[str] = []

    if typ == "timer_simple":
        reasons.append("timer.Simple is one-shot delayed callback")
        if delay is not None and delay <= 0.05:
            return "next_tick_delay", reasons
        if classify_subsystem(file, name) in {"ui_hud"}:
            return "ui_delay_timer", reasons
        return "one_shot_delay", reasons

    if typ == "timer_create":
        if reps == 0:
            reasons.append("timer.Create repetitions=0 means infinite repeating timer")
            if delay is not None and delay <= 0.1:
                reasons.append("sub-0.1s infinite timer is high frequency")
                return "high_frequency_infinite_timer", reasons
            return "infinite_loop_timer", reasons
        if reps == 1:
            reasons.append("timer.Create repetitions=1 is one-shot")
            return "one_shot_delay", reasons
        if reps is not None and reps > 1:
            reasons.append("timer.Create repetitions>1 is finite repeating scheduler")
            return "finite_repeating_scheduler", reasons
        return "repeating_scheduler", reasons

    if typ.startswith("entity_timer") or entry.get("scope") == "entity":
        reasons.append("entity scoped timer/action helper")
        return "entity_simulation_timer", reasons

    if "action_timer" in typ or entry.get("scope") == "player":
        reasons.append("player action/progress timer helper")
        return "player_action_timer", reasons

    if typ.startswith("timer_remove"):
        reasons.append("timer lifecycle removal operation")
        return "timer_lifecycle_operation", reasons

    if typ.startswith("timer_adjust"):
        reasons.append("timer lifecycle adjustment operation")
        return "timer_lifecycle_operation", reasons

    return "unknown_timer", reasons


def risk_flags(entry: Dict[str, Any], timer_class: str) -> List[str]:
    flags: List[str] = []
    name = entry.get("timer_name") or entry.get("timer_name_expr")
    delay = parse_num(entry.get("delay_expr"))
    reps = parse_num(entry.get("repetitions_expr"))
    if is_dynamic_expr(name):
        flags.append("dynamic_timer_name")
    if timer_class == "high_frequency_infinite_timer":
        flags.append("high_frequency_infinite_timer")
    elif reps == 0:
        flags.append("infinite_timer")
    if delay is not None and delay <= 0.05:
        flags.append("next_tick_or_subframe_delay")
    if entry.get("validity_guard_expected") is True:
        flags.append("entity_validity_guard_expected")
    return flags


def load_manifest_inputs(root: Path) -> Dict[str, List[Dict[str, Any]]]:
    timers = root / "manifests" / "timers"
    entities = root / "manifests" / "entities"
    inputs = {
        "timer_creates": read_json(timers / "timer_creates.json", []),
        "timer_simples": read_json(timers / "timer_simples.json", []),
        "timer_operations": read_json(timers / "timer_operations.json", []),
        "entity_timer_calls": read_json(timers / "entity_timer_calls.json", []),
        "player_action_timers": read_json(timers / "player_action_timers.json", []),
        "legacy_entity_timer_calls": read_json(entities / "entity_timer_calls.json", []),
    }
    # Normalize to list only.
    return {k: v if isinstance(v, list) else [] for k, v in inputs.items()}


def build_graph(workspace: Path) -> Dict[str, Any]:
    inputs = load_manifest_inputs(workspace)
    nodes: Dict[str, Dict[str, Any]] = {}
    edges: List[Dict[str, Any]] = []
    seen_edges: set = set()

    add_node(nodes, "realm:server", "realm", "server")
    add_node(nodes, "realm:client", "realm", "client")
    add_node(nodes, "realm:shared", "realm", "shared")

    operation_entries: List[Tuple[str, Dict[str, Any]]] = []
    for source, rows in inputs.items():
        for row in rows:
            if isinstance(row, dict):
                operation_entries.append((source, row))

    # Dedup obvious duplicate legacy entity rows by type/file/line/method.
    dedup: Dict[Tuple[Any, ...], Tuple[str, Dict[str, Any]]] = {}
    for source, e in operation_entries:
        key = (e.get("type"), norm_path(e.get("file")), e.get("line"), e.get("method_name"), e.get("timer_name"), e.get("timer_name_expr"))
        if key not in dedup or not source.startswith("legacy"):
            dedup[key] = (source, e)
    operation_entries = list(dedup.values())

    timer_name_counts = Counter()
    timer_class_counts = Counter()
    subsystem_counts = Counter()
    risk_counts = Counter()
    file_decl_counts = Counter()
    source_counts = Counter()

    dynamic_timers: List[Dict[str, Any]] = []
    high_risk_timers: List[Dict[str, Any]] = []

    for idx, (source, e) in enumerate(operation_entries):
        typ = str(e.get("type") or "timer_operation")
        file = norm_path(e.get("file"))
        line = e.get("line")
        realm = infer_realm(file, e.get("realm"))
        plugin = infer_plugin(file)
        method = str(e.get("method_name") or typ)
        raw_name = e.get("timer_name") or e.get("timer_name_expr") or e.get("method_name") or typ
        timer_label = str(raw_name or typ)
        timer_class, reasons = classify_timer(e)
        subsystem = classify_subsystem(file, timer_label, method)
        flags = risk_flags(e, timer_class)

        source_counts[source] += 1
        timer_name_counts[timer_label] += 1
        timer_class_counts[timer_class] += 1
        subsystem_counts[subsystem] += 1
        file_decl_counts[file] += 1
        for f in flags:
            risk_counts[f] += 1

        file_id = stable_id("file", file)
        op_id = stable_id("timer_op", file, line, typ, timer_label, idx)
        timer_id = stable_id("timer", timer_label) if not is_dynamic_expr(raw_name) else stable_id("timer_dynamic", file, line, timer_label)
        class_id = stable_id("timer_class", timer_class)
        subsystem_id = stable_id("subsystem", subsystem)
        realm_id = f"realm:{realm}"

        add_node(nodes, file_id, "file", file, path=file)
        add_node(nodes, op_id, "timer_operation", f"{typ}@{file}:{line}", operation_type=typ, file=file, line=line, realm=realm, source_manifest=source)
        add_node(nodes, timer_id, "timer", timer_label, name_expr=timer_label, dynamic_name=is_dynamic_expr(raw_name))
        add_node(nodes, class_id, "timer_class", timer_class)
        add_node(nodes, subsystem_id, "subsystem", subsystem)
        if plugin:
            plugin_id = stable_id("plugin", plugin)
            add_node(nodes, plugin_id, "plugin", plugin)
            add_edge(edges, seen_edges, plugin_id, file_id, "owns_file")
            add_edge(edges, seen_edges, plugin_id, op_id, "owns_timer_operation")

        add_edge(edges, seen_edges, file_id, op_id, "contains_timer_operation")
        add_edge(edges, seen_edges, op_id, timer_id, "references_timer")
        add_edge(edges, seen_edges, op_id, class_id, "classified_as", reasons=reasons)
        add_edge(edges, seen_edges, op_id, subsystem_id, "belongs_to_subsystem")
        add_edge(edges, seen_edges, op_id, realm_id, "runs_in_realm")
        add_edge(edges, seen_edges, file_id, realm_id, "runs_in_realm")

        # Lifecycle semantics.
        if typ == "timer_create":
            add_edge(edges, seen_edges, op_id, timer_id, "creates_timer", delay_expr=e.get("delay_expr"), repetitions_expr=e.get("repetitions_expr"))
        elif typ == "timer_simple":
            add_edge(edges, seen_edges, op_id, timer_id, "schedules_delay", delay_expr=e.get("delay_expr"))
        elif "remove" in typ:
            add_edge(edges, seen_edges, op_id, timer_id, "removes_timer")
        elif "adjust" in typ:
            add_edge(edges, seen_edges, op_id, timer_id, "adjusts_timer")
        elif e.get("scope") == "entity" or typ.startswith("entity_timer"):
            add_edge(edges, seen_edges, op_id, timer_id, "schedules_entity_action")
        elif e.get("scope") == "player" or "action_timer" in typ:
            add_edge(edges, seen_edges, op_id, timer_id, "schedules_player_action", cancelable=e.get("cancelable"), uses_busy_state=e.get("uses_busy_state"))

        if flags:
            for flag in flags:
                flag_id = stable_id("timer_risk", flag)
                add_node(nodes, flag_id, "timer_risk", flag)
                add_edge(edges, seen_edges, op_id, flag_id, "has_timer_risk")

        if is_dynamic_expr(raw_name):
            dynamic_timers.append({
                "timer": timer_label,
                "type": typ,
                "file": file,
                "line": line,
                "realm": realm,
                "class": timer_class,
                "subsystem": subsystem,
                "source": source,
            })
        if any(f in flags for f in ("high_frequency_infinite_timer", "infinite_timer", "next_tick_or_subframe_delay")):
            high_risk_timers.append({
                "timer": timer_label,
                "type": typ,
                "file": file,
                "line": line,
                "realm": realm,
                "delay_expr": e.get("delay_expr"),
                "repetitions_expr": e.get("repetitions_expr"),
                "class": timer_class,
                "flags": flags,
            })

    summary = {
        "schema": SCHEMA,
        "inputs": {k: len(v) for k, v in inputs.items()},
        "totals": {
            "nodes": len(nodes),
            "edges": len(edges),
            "timer_operations": len(operation_entries),
            "timers": sum(1 for n in nodes.values() if n["type"] == "timer"),
            "files": sum(1 for n in nodes.values() if n["type"] == "file"),
            "plugins": sum(1 for n in nodes.values() if n["type"] == "plugin"),
        },
        "node_types": Counter(n["type"] for n in nodes.values()),
        "edge_types": Counter(e["type"] for e in edges),
        "source_counts": source_counts,
        "timer_classes": timer_class_counts,
        "subsystems": subsystem_counts,
        "risk_flags": risk_counts,
        "top_timer_names": timer_name_counts.most_common(30),
        "hot_files": file_decl_counts.most_common(30),
        "dynamic_timers": dynamic_timers[:80],
        "high_risk_timers": high_risk_timers[:80],
    }

    # Convert Counters to normal dicts for JSON.
    for key in ["node_types", "edge_types", "source_counts", "timer_classes", "subsystems", "risk_flags"]:
        summary[key] = dict(summary[key])

    return {
        "schema": SCHEMA,
        "nodes": list(nodes.values()),
        "edges": edges,
        "summary": summary,
    }


def md_list_counts(counter_dict: Dict[str, int], limit: int = 30) -> str:
    if not counter_dict:
        return "- none\n"
    items = sorted(counter_dict.items(), key=lambda kv: (-kv[1], kv[0]))[:limit]
    return "".join(f"- `{k}`: **{v}**\n" for k, v in items)


def build_markdown(summary: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Timer graph summary\n")
    lines.append(f"Schema: `{summary['schema']}`\n")
    lines.append("## Inputs\n")
    for k, v in summary["inputs"].items():
        lines.append(f"- `{k}`: **{v}**\n")
    lines.append("\n## Totals\n")
    for k, v in summary["totals"].items():
        lines.append(f"- {k.replace('_', ' ').title()}: **{v}**\n")
    lines.append("\n## Node types\n")
    lines.append(md_list_counts(summary["node_types"]))
    lines.append("\n## Edge types\n")
    lines.append(md_list_counts(summary["edge_types"]))
    lines.append("\n## Timer classes\n")
    lines.append(md_list_counts(summary["timer_classes"]))
    lines.append("\n## Subsystems\n")
    lines.append(md_list_counts(summary["subsystems"]))
    lines.append("\n## Risk flags\n")
    lines.append(md_list_counts(summary["risk_flags"]))
    lines.append("\n## Top timer names / expressions\n")
    if summary["top_timer_names"]:
        for name, count in summary["top_timer_names"]:
            lines.append(f"- `{name}`: {count}\n")
    else:
        lines.append("- none\n")
    lines.append("\n## Hot files by timer declarations\n")
    if summary["hot_files"]:
        for file, count in summary["hot_files"]:
            lines.append(f"- `{file}`: {count}\n")
    else:
        lines.append("- none\n")
    lines.append("\n## High-risk timer candidates\n")
    if summary["high_risk_timers"]:
        for t in summary["high_risk_timers"][:40]:
            lines.append(
                f"- `{t['timer']}` at `{t['file']}:{t['line']}` "
                f"class=`{t['class']}` delay=`{t.get('delay_expr')}` reps=`{t.get('repetitions_expr')}` flags={t.get('flags')}\n"
            )
    else:
        lines.append("- none\n")
    lines.append("\n## Dynamic timer name examples\n")
    if summary["dynamic_timers"]:
        for t in summary["dynamic_timers"][:40]:
            lines.append(f"- `{t['timer']}` at `{t['file']}:{t['line']}` type=`{t['type']}` class=`{t['class']}` subsystem=`{t['subsystem']}`\n")
    else:
        lines.append("- none\n")
    return "".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build normalized timer/scheduler graph from manifests.")
    parser.add_argument("--workspace", required=True, help="Project workspace root, e.g. E:/signalis_ai")
    parser.add_argument("--write", action="store_true", help="Write outputs to manifests/normalized")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    result = build_graph(workspace)
    summary = result["summary"]

    out_dir = workspace / "manifests" / "normalized"
    if args.write:
        write_json(out_dir / "timer_graph_nodes.json", result["nodes"])
        write_json(out_dir / "timer_graph_edges.json", result["edges"])
        write_json(out_dir / "timer_graph.json", result)
        (out_dir / "timer_graph_summary.md").write_text(build_markdown(summary), encoding="utf-8")

    print(json.dumps({
        "schema": SCHEMA,
        "timer_operations": summary["totals"]["timer_operations"],
        "nodes": summary["totals"]["nodes"],
        "edges": summary["totals"]["edges"],
        "timer_classes": summary["timer_classes"],
        "risk_flags": summary["risk_flags"],
        "wrote": bool(args.write),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
