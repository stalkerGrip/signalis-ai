#!/usr/bin/env python3
"""
SIGNALIS AI — Evidence Graph Builder V1

Purpose:
  Convert deduplicated validation evidence into simple runtime propagation chains.

Input:
  investigations/validation/*_validation_deduped.json

Output:
  *_evidence_graph.json
  *_evidence_graph.md

Usage:
  python -m scripts.qdrant.build_evidence_graph `
    --deduped investigations/validation/vendor_stale_price_label_after_purchase_validation_deduped.json
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


TARGET_RANK = {
    "net": 90,
    "netstream": 85,
    "vendor_net_handler": 82,
    "hook": 80,
    "item_data": 75,
    "item_data_read": 65,
    "function": 60,
    "ui_call": 55,
    "state": 20,
    "unknown": 0,
}


@dataclass
class EvidenceNode:
    id: str
    target: str
    kind: str
    label: str
    file: str
    realm: str
    line_start: int
    line_end: int
    score: int
    bucket: str
    classification: str
    snippet: str


@dataclass
class EvidenceEdge:
    source: str
    target: str
    kind: str
    confidence: str
    reason: str


@dataclass
class EvidenceChain:
    id: str
    title: str
    nodes: list[str]
    edges: list[EvidenceEdge]
    confidence: str
    reason: str


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def normalize_file(path: str) -> str:
    return path.replace("\\", "/").lower()


def target_kind(target: str) -> str:
    if ":" not in target:
        return "unknown"
    return target.split(":", 1)[0]


def target_label(target: str) -> str:
    if ":" not in target:
        return target
    return target.split(":", 1)[1]


def node_id(target: str, file: str, line_start: int) -> str:
    safe = re.sub(r"[^A-Za-z0-9_:-]+", "_", f"{target}@{file}:{line_start}")
    return safe[:180]


def extract_nodes(payload: dict[str, Any]) -> list[EvidenceNode]:
    nodes: list[EvidenceNode] = []

    for item in payload.get("evidence", []):
        target = str(item.get("semantic_target", "unknown"))
        kind = target_kind(target)

        nodes.append(
            EvidenceNode(
                id=node_id(target, str(item.get("file", "")), int(item.get("line_start", 0))),
                target=target,
                kind=kind,
                label=target_label(target),
                file=str(item.get("file", "")),
                realm=str(item.get("realm", "")),
                line_start=int(item.get("line_start", 0)),
                line_end=int(item.get("line_end", 0)),
                score=int(item.get("score", 0)),
                bucket=str(item.get("bucket", "unscored")),
                classification=str(item.get("classification", "")),
                snippet=str(item.get("snippet", "")),
            )
        )

    nodes.sort(key=lambda n: (n.score, TARGET_RANK.get(n.kind, 0)), reverse=True)
    return nodes


def find_nodes(nodes: list[EvidenceNode], *, kind: str | None = None, label_contains: str | None = None) -> list[EvidenceNode]:
    result: list[EvidenceNode] = []

    for node in nodes:
        if kind is not None and node.kind != kind:
            continue
        if label_contains is not None and label_contains.lower() not in node.label.lower():
            continue
        result.append(node)

    return result


def has_text(node: EvidenceNode, text: str) -> bool:
    blob = "\n".join([node.target, node.label, node.file, node.classification, node.snippet]).lower()
    return text.lower() in blob


def add_edge(edges: list[EvidenceEdge], source: EvidenceNode, target: EvidenceNode, kind: str, confidence: str, reason: str) -> None:
    if source.id == target.id:
        return

    for edge in edges:
        if edge.source == source.id and edge.target == target.id and edge.kind == kind:
            return

    edges.append(
        EvidenceEdge(
            source=source.id,
            target=target.id,
            kind=kind,
            confidence=confidence,
            reason=reason,
        )
    )


def infer_edges(nodes: list[EvidenceNode]) -> list[EvidenceEdge]:
    edges: list[EvidenceEdge] = []

    # Generic file-local ordering edges.
    by_file: dict[str, list[EvidenceNode]] = {}
    for node in nodes:
        by_file.setdefault(normalize_file(node.file), []).append(node)

    for file_nodes in by_file.values():
        ordered = sorted(file_nodes, key=lambda n: n.line_start)
        for prev, nxt in zip(ordered, ordered[1:]):
            if prev.line_end <= nxt.line_start:
                add_edge(
                    edges,
                    prev,
                    nxt,
                    "file_order",
                    "low",
                    "same file and source order",
                )

    # Hook emit/listen relationship by hook name.
    hook_nodes = find_nodes(nodes, kind="hook")
    for a in hook_nodes:
        for b in hook_nodes:
            if a.id == b.id:
                continue
            if a.label != b.label:
                continue

            a_emit = "hook.Run" in a.snippet
            b_listen = "hook.Add" in b.snippet or "function PLUGIN:" in b.snippet or "function PANEL:" in b.snippet

            if a_emit and b_listen:
                add_edge(
                    edges,
                    a,
                    b,
                    "hook_dispatch",
                    "high",
                    f"hook.Run dispatches to listener for {a.label}",
                )

    # Vendor client network handler -> hook emission.
    handler_nodes = [n for n in nodes if n.kind in {"vendor_net_handler", "net", "netstream"} or "cl_networking.lua" in normalize_file(n.file)]
    for source in handler_nodes:
        for target in hook_nodes:
            if normalize_file(source.file) == normalize_file(target.file):
                if source.line_start <= target.line_start <= source.line_end + 20:
                    add_edge(
                        edges,
                        source,
                        target,
                        "network_handler_emits_hook",
                        "medium",
                        "network handler and hook emission are local in client networking file",
                    )

    # Vendor item data mutation -> vendor price/stock hook.
    item_data_nodes = find_nodes(nodes, kind="item_data")
    price_hooks = [
        n for n in hook_nodes
        if n.label in {
            "VendorItemPriceUpdated",
            "VendorItemStockUpdated",
            "VendorMoneyUpdated",
            "VendorSynchronized",
        }
    ]

    for data_node in item_data_nodes:
        for hook_node in price_hooks:
            if "vendor" in data_node.label.lower() and "vendor" in hook_node.label.lower():
                add_edge(
                    edges,
                    data_node,
                    hook_node,
                    "state_mutation_to_sync_event",
                    "medium",
                    "vendor item data mutation is related to vendor sync/update hook",
                )

    # Price hook -> UI updatePrice.
    ui_update_nodes = [n for n in nodes if n.kind == "ui_call" and "updatePrice" in n.label]
    price_related_hooks = [
        n for n in hook_nodes
        if n.label in {
            "VendorItemPriceUpdated",
            "VendorItemStockUpdated",
            "VendorMoneyUpdated",
            "VendorSynchronized",
        }
    ]

    for hook_node in price_related_hooks:
        for ui_node in ui_update_nodes:
            if "cl_vendor.lua" in normalize_file(ui_node.file):
                add_edge(
                    edges,
                    hook_node,
                    ui_node,
                    "hook_to_ui_refresh",
                    "high",
                    "vendor update hook leads to vendor panel price refresh",
                )

    # Trade network -> server item data mutations.
    trade_nodes = [n for n in nodes if n.target in {"net:nutVendorTrade", "netstream:vendorTradeInterface"}]
    vendor_data_nodes = [
        n for n in nodes
        if (
            "plugins/vendor/entities/entities/nut_vendor/init.lua" in normalize_file(n.file)
            and n.kind in {"item_data", "function", "state"}
        )
    ]

    for trade_node in trade_nodes:
        for data_node in vendor_data_nodes:
            if data_node.score >= 70:
                add_edge(
                    edges,
                    trade_node,
                    data_node,
                    "trade_to_vendor_state",
                    "medium",
                    "vendor trade path connects to server-side vendor item data evidence",
                )

    # Inventory data network -> UI-related hooks.
    inv_data_nodes = [n for n in nodes if n.target == "net:nutInventoryData"]
    inv_ui_nodes = [
        n for n in nodes
        if "plugins/inventory/cl_hooks.lua" in normalize_file(n.file)
        or n.target in {"hook:CreateNewInventoryPanel", "netstream:vendorTradeInterface"}
    ]

    for inv_data in inv_data_nodes:
        for ui_node in inv_ui_nodes:
            add_edge(
                edges,
                inv_data,
                ui_node,
                "inventory_sync_to_ui",
                "medium",
                "inventory data receiver is related to client inventory UI evidence",
            )

    return edges


def make_chain(
    chain_id: str,
    title: str,
    nodes_by_target: dict[str, EvidenceNode],
    target_order: list[str],
    edge_kind: str,
    reason: str,
) -> EvidenceChain | None:
    chain_nodes: list[str] = []
    chain_edges: list[EvidenceEdge] = []

    for target in target_order:
        node = nodes_by_target.get(target)
        if node:
            chain_nodes.append(node.id)

    if len(chain_nodes) < 2:
        return None

    for src_id, dst_id in zip(chain_nodes, chain_nodes[1:]):
        chain_edges.append(
            EvidenceEdge(
                source=src_id,
                target=dst_id,
                kind=edge_kind,
                confidence="medium",
                reason=reason,
            )
        )

    return EvidenceChain(
        id=chain_id,
        title=title,
        nodes=chain_nodes,
        edges=chain_edges,
        confidence="medium",
        reason=reason,
    )


def choose_best_by_target(nodes: list[EvidenceNode]) -> dict[str, EvidenceNode]:
    best: dict[str, EvidenceNode] = {}

    for node in nodes:
        old = best.get(node.target)
        if old is None or node.score > old.score:
            best[node.target] = node

    return best


def build_chains(nodes: list[EvidenceNode], edges: list[EvidenceEdge]) -> list[EvidenceChain]:
    best = choose_best_by_target(nodes)
    chains: list[EvidenceChain] = []

    candidates = [
        (
            "vendor_price_update",
            "Vendor Price Update / UI Refresh",
            [
                "net:nutVendorTrade",
                "item_data:vendorQty",
                "hook:VendorItemPriceUpdated",
                "ui_call:updatePrice",
            ],
            "inferred_runtime_chain",
            "trade and item metadata evidence connect to vendor price hook and UI refresh",
        ),
        (
            "vendor_exit_metadata_clear",
            "Vendor Exit / Metadata Clear",
            [
                "net:nutVendorExit",
                "item_data:vendorBPrice",
                "hook:VendorExited",
            ],
            "inferred_runtime_chain",
            "vendor exit evidence connects to vendor presentation metadata clearing",
        ),
        (
            "vendor_open_sync",
            "Vendor Open / Initial Sync",
            [
                "netstream:sendVendorInfo",
                "hook:VendorSynchronized",
                "hook:VendorOpened",
            ],
            "inferred_runtime_chain",
            "vendor info sync and vendor opened hook are both client-side sync/open evidence",
        ),
        (
            "inventory_ui_sync",
            "Inventory UI Sync",
            [
                "net:nutInventoryData",
                "hook:CreateNewInventoryPanel",
                "netstream:vendorTradeInterface",
            ],
            "inferred_runtime_chain",
            "inventory data and inventory panel creation connect to vendor trade interface",
        ),
    ]

    for chain_id, title, target_order, edge_kind, reason in candidates:
        chain = make_chain(chain_id, title, best, target_order, edge_kind, reason)
        if chain:
            chains.append(chain)

    # Include high-confidence direct hook dispatches as chains.
    node_lookup = {node.id: node for node in nodes}
    for edge in edges:
        if edge.kind != "hook_dispatch":
            continue

        src = node_lookup.get(edge.source)
        dst = node_lookup.get(edge.target)
        if not src or not dst:
            continue

        chains.append(
            EvidenceChain(
                id=f"hook_dispatch_{src.label}",
                title=f"Hook Dispatch: {src.label}",
                nodes=[src.id, dst.id],
                edges=[edge],
                confidence=edge.confidence,
                reason=edge.reason,
            )
        )

    return chains


def format_node_line(node: EvidenceNode) -> str:
    return f"`{node.target}` — `{node.file}:{node.line_start}-{node.line_end}` ({node.realm}, score {node.score})"


def format_md(source_path: Path, query: str, nodes: list[EvidenceNode], edges: list[EvidenceEdge], chains: list[EvidenceChain]) -> str:
    node_lookup = {node.id: node for node in nodes}

    lines: list[str] = []
    lines.append("# SIGNALIS AI — Evidence Graph")
    lines.append("")
    lines.append(f"- Source: `{source_path}`")
    lines.append(f"- Query: `{query}`")
    lines.append(f"- Nodes: `{len(nodes)}`")
    lines.append(f"- Edges: `{len(edges)}`")
    lines.append(f"- Chains: `{len(chains)}`")
    lines.append("")

    lines.append("## Runtime Chains")
    lines.append("")

    if not chains:
        lines.append("- No chains inferred.")
        lines.append("")

    for chain in chains:
        lines.append(f"### {chain.title}")
        lines.append("")
        lines.append(f"- Confidence: `{chain.confidence}`")
        lines.append(f"- Reason: {chain.reason}")
        lines.append("")
        for index, node_id_value in enumerate(chain.nodes):
            node = node_lookup.get(node_id_value)
            if not node:
                continue
            prefix = "1." if index == 0 else "   ↓"
            lines.append(f"{prefix} {format_node_line(node)}")
        lines.append("")

    lines.append("## Edges")
    lines.append("")
    for edge in edges:
        src = node_lookup.get(edge.source)
        dst = node_lookup.get(edge.target)
        if not src or not dst:
            continue

        lines.append(f"- `{src.target}` → `{dst.target}`")
        lines.append(f"  - Kind: `{edge.kind}`")
        lines.append(f"  - Confidence: `{edge.confidence}`")
        lines.append(f"  - Reason: {edge.reason}")

    lines.append("")
    lines.append("## Nodes")
    lines.append("")
    for node in nodes:
        lines.append(f"### {node.target}")
        lines.append("")
        lines.append(f"- File: `{node.file}`")
        lines.append(f"- Lines: `{node.line_start}-{node.line_end}`")
        lines.append(f"- Realm: `{node.realm}`")
        lines.append(f"- Score: `{node.score}`")
        lines.append(f"- Classification: `{node.classification}`")
        lines.append("")
        lines.append("```lua")
        lines.append(node.snippet)
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deduped", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source = args.deduped.resolve()
    payload = read_json(source)

    nodes = extract_nodes(payload)
    edges = infer_edges(nodes)
    chains = build_chains(nodes, edges)

    out_dir = args.out_dir.resolve() if args.out_dir else source.parent

    stem = source.stem
    for suffix in ["_evidence_graph", "_deduped", "_scored"]:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]

    stem = f"{stem}_evidence_graph"

    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"

    output = {
        "source": str(source),
        "query": payload.get("query"),
        "summary": {
            "nodes": len(nodes),
            "edges": len(edges),
            "chains": len(chains),
        },
        "nodes": [asdict(node) for node in nodes],
        "edges": [asdict(edge) for edge in edges],
        "chains": [asdict(chain) for chain in chains],
    }

    write_json(json_path, output)
    write_text(md_path, format_md(source, str(payload.get("query", "")), nodes, edges, chains))

    print(f"Wrote evidence graph json: {json_path}")
    print(f"Wrote evidence graph report: {md_path}")
    print("")
    print("Summary:")
    print(f"  nodes: {len(nodes)}")
    print(f"  edges: {len(edges)}")
    print(f"  chains: {len(chains)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())