from __future__ import annotations

import argparse
import heapq
import json
from pathlib import Path
from typing import Any


IGNORE_EDGE_TYPES = {
    "classified_as",
    "runs_in_realm",
    "belongs_to_subsystem",
    "owns_file",
    "has_timer_risk",
    "references_timer",
}

EDGE_COSTS = {
    "emits": 0.5,
    "emits_event": 0.5,
    "dispatches_to": 0.6,
    "network_dispatches_to": 0.6,
    "listens_to": 0.8,
    "listens_to_event": 0.8,
    "contains_listener": 1.2,
    "contains_emitter": 1.2,
    "contains_network_operation": 1.2,
    "file_sends_network_message": 1.4,
    "file_receives_network_message": 1.4,
    "sends_network_message": 1.0,
    "receives_network_message": 1.0,
    "contains_timer_operation": 2.0,
}

NODE_BONUS = {
    "hook_event": -0.25,
    "hook_emitter": -0.15,
    "hook_listener": -0.15,
    "network_message": -0.20,
    "network_operation": -0.10,
    "file": 0.15,
    "plugin": 0.30,
    "timer": 0.50,
    "timer_operation": 0.50,
}

ANCHOR_TERMS = {
    "CharacterLoaded",
    "PrePlayerLoadedChar",
    "PlayerLoadedChar",
    "PlayerLoadout",
    "PostPlayerLoadout",
    "CharacterPreSave",
    "inventoryOpen",
    "inventorySetPanelStatus",
    "invsRuleSet",
    "nutInventoryInit",
    "nutInventoryAdd",
    "nutInventoryRemove",
    "nutInventoryDelete",
    "nutTransferItem",
    "invAct",
}


def load_topology(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("nodes", []), data.get("edges", [])


def node_id(node: dict[str, Any]) -> str:
    return str(node.get("id") or node.get("node_id") or node.get("source_id") or "")


def node_label(node: dict[str, Any]) -> str:
    return str(
        node.get("label")
        or node.get("event")
        or node.get("message")
        or node.get("name")
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


def packed(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False).lower()


def find_nodes(nodes: list[dict[str, Any]], term: str, limit: int = 20) -> list[str]:
    term_l = term.lower()
    matches: list[tuple[int, str]] = []

    for node in nodes:
        nid = node_id(node)
        if not nid:
            continue

        label = node_label(node).lower()
        ntype = node_type(node).lower()
        full = packed(node)

        score = 0

        if label == term_l:
            score += 100
        if term_l in label:
            score += 60
        if term_l in nid.lower():
            score += 40
        if term_l in full:
            score += 10

        if ntype in {"hook_event", "network_message"}:
            score += 20
        elif ntype in {"hook_emitter", "hook_listener", "network_operation"}:
            score += 8
        elif ntype == "file":
            score -= 5

        if score > 0:
            matches.append((score, nid))

    matches.sort(reverse=True)
    return [nid for _, nid in matches[:limit]]


def build_graph(edges: list[dict[str, Any]]) -> dict[str, list[tuple[str, str]]]:
    graph: dict[str, list[tuple[str, str]]] = {}

    for edge in edges:
        src = edge_source(edge)
        dst = edge_target(edge)
        etype = edge_type(edge)

        if not src or not dst:
            continue

        if etype in IGNORE_EDGE_TYPES:
            continue

        graph.setdefault(src, []).append((dst, etype))
        graph.setdefault(dst, []).append((src, f"reverse:{etype}"))

    return graph


def relation_base(rel: str) -> str:
    if rel.startswith("reverse:"):
        return rel.removeprefix("reverse:")
    return rel


def node_cost(nid: str, by_id: dict[str, dict[str, Any]], query_terms: set[str]) -> float:
    node = by_id.get(nid)
    if not node:
        return 0.5

    ntype = node_type(node)
    label = node_label(node)
    text = packed(node)

    cost = NODE_BONUS.get(ntype, 0.0)

    if any(term.lower() in text for term in query_terms):
        cost -= 0.35

    if any(term.lower() in label.lower() for term in ANCHOR_TERMS):
        cost -= 0.25

    if ntype == "network_message":
        if not any(term.lower() in text for term in query_terms) and not any(
            term.lower() in text for term in ANCHOR_TERMS
        ):
            cost += 1.0

    return cost


def edge_cost(rel: str) -> float:
    base = relation_base(rel)
    cost = EDGE_COSTS.get(base, 2.5)

    if rel.startswith("reverse:"):
        cost += 0.25

    return cost


def search_paths(
    graph: dict[str, list[tuple[str, str]]],
    by_id: dict[str, dict[str, Any]],
    start_ids: list[str],
    target_ids: set[str],
    query_terms: set[str],
    *,
    max_depth: int,
    max_paths: int,
) -> list[tuple[float, list[tuple[str, str | None]]]]:
    heap: list[tuple[float, int, list[tuple[str, str | None]]]] = []
    counter = 0
    results: list[tuple[float, list[tuple[str, str | None]]]] = []
    seen_signatures: set[tuple[str, ...]] = set()

    for start in start_ids:
        heapq.heappush(heap, (0.0, counter, [(start, None)]))
        counter += 1

    visited_best: dict[tuple[str, int], float] = {}

    while heap and len(results) < max_paths:
        score, _, path = heapq.heappop(heap)
        current = path[-1][0]
        depth = len(path) - 1

        sig = tuple(nid for nid, _ in path)

        if current in target_ids and depth > 0:
            if sig not in seen_signatures:
                seen_signatures.add(sig)
                results.append((score, path))
            continue

        if depth >= max_depth:
            continue

        state = (current, depth)
        if state in visited_best and visited_best[state] <= score:
            continue
        visited_best[state] = score

        path_nodes = {nid for nid, _ in path}

        for neighbor, rel in graph.get(current, []):
            if neighbor in path_nodes:
                continue

            step_cost = edge_cost(rel) + node_cost(neighbor, by_id, query_terms)

            new_score = score + max(step_cost, 0.05)
            new_path = path + [(neighbor, rel)]

            heapq.heappush(heap, (new_score, counter, new_path))
            counter += 1

    return results


def render_node(nid: str, by_id: dict[str, dict[str, Any]]) -> str:
    node = by_id.get(nid)

    if not node:
        return f"`{nid}`"

    label = node_label(node)
    ntype = node_type(node)
    file_value = node.get("file") or node.get("path")
    realm = node.get("realm")
    plugin = node.get("plugin")
    subsystem = node.get("subsystem")

    extras = []
    if file_value:
        extras.append(f"file={file_value}")
    if realm:
        extras.append(f"realm={realm}")
    if plugin:
        extras.append(f"plugin={plugin}")
    if subsystem:
        extras.append(f"subsystem={subsystem}")

    suffix = ""
    if extras:
        suffix = " — " + ", ".join(str(x) for x in extras)

    return f"`{label}` ({ntype}){suffix}"


def render_report(
    from_term: str,
    to_term: str,
    paths: list[tuple[float, list[tuple[str, str | None]]]],
    by_id: dict[str, dict[str, Any]],
    start_matches: list[str],
    target_matches: list[str],
) -> str:
    lines = [
        "# Runtime Path Reconstruction V2",
        "",
        f"From: `{from_term}`",
        f"To: `{to_term}`",
        "",
        "## Resolved Start Nodes",
        "",
    ]

    for nid in start_matches[:10]:
        lines.append(f"- {render_node(nid, by_id)}")

    lines.extend(["", "## Resolved Target Nodes", ""])

    for nid in target_matches[:10]:
        lines.append(f"- {render_node(nid, by_id)}")

    lines.extend(["", "## Candidate Paths", ""])

    if not paths:
        lines.append("- no paths found")
    else:
        for index, (score, path) in enumerate(paths, start=1):
            lines.append(f"### Path {index}")
            lines.append("")
            lines.append(f"- Path score: `{score:.3f}`")
            lines.append("")

            for i, (nid, rel) in enumerate(path):
                if i == 0:
                    lines.append(f"1. {render_node(nid, by_id)}")
                else:
                    lines.append(f"{i + 1}. via `{rel}` → {render_node(nid, by_id)}")

            lines.append("")

    lines.extend([
        "## Notes",
        "",
        "- V2 uses weighted topology traversal.",
        "- Lower path score means stronger candidate.",
        "- This is still topology-only, not chronological proof.",
        "- Use raw Lua only after a meaningful candidate path is found.",
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Weighted runtime topology path reconstruction.")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--topology")
    parser.add_argument("--from", dest="from_term", required=True)
    parser.add_argument("--to", dest="to_term", required=True)
    parser.add_argument("--terms", nargs="*", default=[])
    parser.add_argument("--max-depth", type=int, default=7)
    parser.add_argument("--max-paths", type=int, default=20)
    parser.add_argument("--output")

    args = parser.parse_args()

    workspace = Path(args.workspace)

    topology_path = (
        Path(args.topology)
        if args.topology
        else workspace / "manifests" / "normalized" / "runtime_topology.json"
    )

    output_path = (
        Path(args.output)
        if args.output
        else workspace / "investigations" / f"paths_v2_{args.from_term}_to_{args.to_term}.md"
    )

    if not output_path.is_absolute():
        output_path = workspace / output_path

    nodes, edges = load_topology(topology_path)
    by_id = {node_id(node): node for node in nodes if node_id(node)}
    graph = build_graph(edges)

    start_matches = find_nodes(nodes, args.from_term)
    target_matches = find_nodes(nodes, args.to_term)

    query_terms = set(args.terms)
    query_terms.add(args.from_term)
    query_terms.add(args.to_term)

    paths = search_paths(
        graph,
        by_id,
        start_matches,
        set(target_matches),
        query_terms,
        max_depth=args.max_depth,
        max_paths=args.max_paths,
    )

    report = render_report(
        args.from_term,
        args.to_term,
        paths,
        by_id,
        start_matches,
        target_matches,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    print(f"Loaded topology: {len(nodes)} nodes, {len(edges)} edges")
    print(f"Start matches: {len(start_matches)}")
    print(f"Target matches: {len(target_matches)}")
    print(f"Paths found: {len(paths)}")
    print(f"Wrote: {output_path}")


if __name__ == "__main__":
    main()