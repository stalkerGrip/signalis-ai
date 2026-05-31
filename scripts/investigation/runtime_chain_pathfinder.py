from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


GENERIC_NODE_PATTERNS = (
    "hook:LoadData",
    "hook:SaveData",
    "plugin:gamemode",
    "plugin:vendor",
    "plugin:inventory",
    "plugin:gridinv",
    "subsystem:",
    "realm:",
)

HIGH_VALUE_EDGE_TYPES = {
    "emits": 0.20,
    "emits_event": 0.20,
    "dispatches_to": 0.18,
    "network_dispatches_to": 0.22,
    "sends_network_message": 0.25,
    "receives_network_message": 0.25,
    "file_sends_network_message": 0.20,
    "file_receives_network_message": 0.20,
    "contains_network_operation": 0.12,
    "contains_listener": 0.12,
    "contains_emitter": 0.12,
    "runs_in_realm": 0.10,
}

HIGH_VALUE_NODE_TERMS = {
    "sv_": 0.10,
    "cl_": 0.10,
    "netmsg:": 0.18,
    "netop:": 0.18,
    "hook:": 0.14,
    "listener:": 0.14,
    "emitter:": 0.14,
    "ItemDataChanged": 0.35,
    "InventoryItemDataChanged": 0.30,
    "InventoryDataChanged": 0.25,
    "nutInventoryAdd": 0.30,
    "nutInventoryData": 0.25,
    "invData": 0.35,
    "setData": 0.30,
    "populateItems": 0.30,
    "sv_transfer.lua": 0.30,
    "cl_networking.lua": 0.20,
    "cl_base_inventory.lua": 0.20,
    "cl_vendor.lua": 0.18,
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_md(path: Path, report: Dict[str, Any]) -> None:
    lines: List[str] = []
    lines.append(f"# Runtime Chain Pathfinder: {report.get('title', 'candidate')}")
    lines.append("")
    lines.append(f"- Schema: `{report['schema']}`")
    lines.append(f"- Source graph audit: `{report.get('source_graph_audit')}`")
    lines.append(f"- Candidate paths: **{len(report.get('paths', []))}**")
    lines.append("")

    lines.append("## Best runtime chain candidate")
    best = report.get("best_chain")
    if not best:
        lines.append("- none")
    else:
        lines.append(f"- Confidence: **{best.get('confidence')}**")
        lines.append(f"- Score: **{best.get('score')}**")
        lines.append(f"- Path mode: `{best.get('path_mode')}`")
        lines.append(f"- Path length: **{best.get('path_length')}**")
        lines.append("")
        lines.append("### Missing causal categories")
        missing = best.get("missing_categories") or []
        if missing:
            for item in missing:
                lines.append(f"- {item}")
        else:
            lines.append("- none")
        lines.append("")
        lines.append("### Steps")
        for idx, step in enumerate(best.get("steps", []), start=1):
            lines.append(f"{idx}. `{step.get('node_type', 'unknown')}` `{step.get('realm', 'unknown')}` — **{step.get('label') or step.get('id')}**")
            lines.append(f"   - id: `{step.get('id')}`")
            if step.get("file"):
                lines.append(f"   - file: `{step['file']}`")
        lines.append("")
        lines.append("### Causal edges")
        for edge in best.get("causal_edges", []):
            lines.append(
                f"- `{edge.get('source')}` → `{edge.get('target')}` via `{', '.join(edge.get('edge_types', []))}`"
            )

    lines.append("")
    lines.append("## Ranked paths")
    for idx, p in enumerate(report.get("paths", []), start=1):
        lines.append(f"### Path {idx}")
        lines.append("")
        lines.append(f"- Score: **{p.get('score')}**")
        lines.append(f"- Confidence: **{p.get('confidence')}**")
        lines.append(f"- Mode: `{p.get('mode')}`")
        lines.append(f"- Length: **{p.get('length')}**")
        lines.append(f"- Missing categories: `{', '.join(p.get('missing_categories', [])) or 'none'}`")
        lines.append("")
        for node in p.get("nodes", []):
            lines.append(f"- `{node.get('type', 'unknown')}` `{node.get('realm', 'unknown')}` — `{node.get('label') or node.get('id')}`")
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def text_blob(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def classify_node(node: Dict[str, Any]) -> Dict[str, bool]:
    blob = text_blob(node).lower()
    nid = str(node.get("id") or "").lower()
    label = str(node.get("label") or "").lower()
    ntype = str(node.get("type") or node.get("node_type") or "").lower()
    realm = str(node.get("realm") or "").lower()

    return {
        "server": realm == "server" or "/sv_" in blob or "sv_" in label or "sv_" in nid,
        "client": realm == "client" or "/cl_" in blob or "cl_" in label or "cl_" in nid,
        "network": "netmsg:" in nid or "netop:" in nid or "network" in ntype or "netstream" in blob or "nutinventory" in blob or "invdata" in blob,
        "hook": "hook:" in nid or "listener:" in nid or "emitter:" in nid or "hook" in ntype or "itemdatachanged" in blob,
        "ui": "derma" in blob or "panel" in blob or "populateitems" in blob or "cl_vendor" in blob or "cl_base_inventory" in blob,
        "state_mutation": "setdata" in blob or "sync" in blob or "sv_transfer" in blob or "inventory" in blob,
    }


def score_node(node: Dict[str, Any]) -> Tuple[float, List[str]]:
    blob = text_blob(node)
    score = 0.0
    reasons: List[str] = []

    for term, value in HIGH_VALUE_NODE_TERMS.items():
        if term.lower() in blob.lower():
            score += value
            reasons.append(f"node contains {term}")

    nid = str(node.get("id") or "")
    for pattern in GENERIC_NODE_PATTERNS:
        if nid.startswith(pattern) or nid == pattern:
            score -= 0.15
            reasons.append(f"generic hub penalty: {pattern}")

    degree = node.get("degree")
    try:
        degree_int = int(degree)
    except Exception:
        degree_int = 0

    if degree_int >= 100:
        score -= 0.20
        reasons.append("very high-degree hub penalty")
    elif degree_int >= 50:
        score -= 0.10
        reasons.append("high-degree hub penalty")

    return score, reasons


def score_edges(edges: List[Dict[str, Any]]) -> Tuple[float, List[str]]:
    score = 0.0
    reasons: List[str] = []

    for edge in edges:
        for etype in edge.get("edge_types", []):
            value = HIGH_VALUE_EDGE_TYPES.get(str(etype), 0.0)
            if value:
                score += value
                reasons.append(f"edge type {etype}")

    return score, reasons


def confidence_from_score(score: float, missing: List[str], mode: str) -> str:
    # Directed paths can be promoted as causal.
    # Undirected paths are topology-associated only and need source validation.
    if not missing and score >= 0.70 and mode == "directed":
        return "high"

    if not missing and score >= 0.60:
        return "medium"

    if len(missing) <= 1 and score >= 0.55:
        return "medium"

    return "low"


def score_path(path: Dict[str, Any]) -> Dict[str, Any]:
    nodes = path.get("nodes", [])
    edges = path.get("edges", [])
    mode = path.get("mode", "unknown")

    node_score = 0.0
    reasons: List[str] = []

    categories = {
        "server": False,
        "client": False,
        "network": False,
        "hook": False,
        "ui": False,
        "state_mutation": False,
    }

    for node in nodes:
        s, r = score_node(node)
        node_score += s
        reasons.extend(r)

        node_categories = classify_node(node)
        for key, value in node_categories.items():
            categories[key] = categories[key] or value

    edge_score, edge_reasons = score_edges(edges)
    reasons.extend(edge_reasons)

    length = int(path.get("length") or max(len(nodes) - 1, 0))
    length_score = max(0.0, 0.35 - (length * 0.025))

    mode_score = 0.15 if mode == "directed" else 0.02

    category_score = sum(0.10 for value in categories.values() if value)

    missing = [key for key, value in categories.items() if not value]

    raw_score = node_score + edge_score + length_score + mode_score + category_score
    normalized = max(0.0, min(raw_score / 3.0, 1.0))

    if missing:
        normalized = min(normalized, 0.74)

    return {
        **path,
        "score": round(normalized, 4),
        "confidence": confidence_from_score(normalized, missing, mode),
        "categories": categories,
        "missing_categories": missing,
        "score_reasons": reasons[:40],
    }


def runtime_step_from_node(node: Dict[str, Any]) -> Dict[str, Any]:
    nid = node.get("id")
    return {
        "id": nid,
        "node_type": node.get("type") or node.get("node_type") or "unknown",
        "label": node.get("label") or node.get("name") or nid,
        "realm": node.get("realm") or "unknown",
        "file": node.get("file") or node.get("path") or node.get("source_file"),
        "degree": node.get("degree"),
        "raw": node,
    }


def build_chain(title: str, path: Dict[str, Any]) -> Dict[str, Any]:
    steps = [runtime_step_from_node(node) for node in path.get("nodes", [])]

    return {
        "schema": "runtime_chain.v2",
        "title": title,
        "confidence": path.get("confidence"),
        "score": path.get("score"),
        "path_mode": path.get("mode"),
        "path_length": path.get("length"),
        "missing_categories": path.get("missing_categories", []),
        "score_reasons": path.get("score_reasons", []),
        "steps": steps,
        "causal_edges": path.get("edges", []),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Score topology candidate paths and export runtime_chain.v2 candidate.")
    parser.add_argument("--graph-audit", required=True, type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--top-k", type=int, default=10)

    args = parser.parse_args()

    audit = load_json(args.graph_audit)
    paths = audit.get("paths") or []

    scored = [score_path(path) for path in paths]
    scored.sort(key=lambda p: (p.get("confidence") == "high", p.get("score", 0), -p.get("length", 999)), reverse=True)
    scored = scored[: args.top_k]

    best_chain = build_chain(args.title, scored[0]) if scored else None

    report = {
        "schema": "runtime_chain_pathfinder_report.v1",
        "title": args.title,
        "source_graph_audit": str(args.graph_audit),
        "best_chain": best_chain,
        "paths": scored,
    }

    write_json(args.out_json, report)
    write_md(args.out_md, report)

    print(f"Wrote pathfinder JSON: {args.out_json}")
    print(f"Wrote pathfinder MD:   {args.out_md}")

    if best_chain:
        print(f"Best confidence: {best_chain['confidence']}")
        print(f"Best score: {best_chain['score']}")
        print(f"Missing categories: {', '.join(best_chain['missing_categories']) or 'none'}")
    else:
        print("No candidate chain produced.")


if __name__ == "__main__":
    main()