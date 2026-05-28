from __future__ import annotations

import argparse
import json
from collections import deque, defaultdict
from pathlib import Path
from typing import Any


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


def packed_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False).lower()


def find_nodes(nodes: list[dict[str, Any]], term: str, limit: int = 30) -> list[str]:
    term_l = term.lower()
    matches: list[tuple[int, str]] = []

    for node in nodes:
        nid = node_id(node)
        if not nid:
            continue

        label = node_label(node).lower()
        ntype = node_type(node).lower()
        full = packed_text(node)

        score = 0

        if label == term_l:
            score += 100
        if term_l in label:
            score += 50
        if term_l in nid.lower():
            score += 40
        if term_l in full:
            score += 10

        if ntype in {"hook_event", "network_message"}:
            score += 8
        elif ntype in {"hook_emitter", "hook_listener", "network_operation"}:
            score += 4

        if score > 0:
            matches.append((score, nid))

    matches.sort(reverse=True)
    return [nid for _, nid in matches[:limit]]


def build_graph(edges: list[dict[str, Any]]) -> dict[str, list[tuple[str, str]]]:
    graph: dict[str, list[tuple[str, str]]] = defaultdict(list)

    for edge in edges:
        src = edge_source(edge)
        dst = edge_target(edge)
        etype = edge_type(edge)

        if not src or not dst:
            continue

        graph[src].append((dst, etype))
        graph[dst].append((src, f"reverse:{etype}"))

    return graph


def find_paths(
    graph: dict[str, list[tuple[str, str]]],
    start_ids: list[str],
    target_ids: set[str],
    *,
    max_depth: int,
    max_paths: int,
) -> list[list[tuple[str, str | None]]]:
    paths: list[list[tuple[str, str | None]]] = []
    queue = deque()

    for start in start_ids:
        queue.append([(start, None)])

    while queue and len(paths) < max_paths:
        path = queue.popleft()
        current = path[-1][0]

        if current in target_ids and len(path) > 1:
            paths.append(path)
            continue

        depth = len(path) - 1
        if depth >= max_depth:
            continue

        seen = {node for node, _ in path}

        for neighbor, rel in graph.get(current, []):
            if neighbor in seen:
                continue

            queue.append(path + [(neighbor, rel)])

    return paths


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
    query_from: str,
    query_to: str,
    paths: list[list[tuple[str, str | None]]],
    by_id: dict[str, dict[str, Any]],
    start_matches: list[str],
    target_matches: list[str],
) -> str:
    lines = [
        "# Runtime Path Reconstruction",
        "",
        f"From: `{query_from}`",
        f"To: `{query_to}`",
        "",
        "## Resolved Start Nodes",
        "",
    ]

    for nid in start_matches[:10]:
        lines.append(f"- {render_node(nid, by_id)}")

    lines.extend([
        "",
        "## Resolved Target Nodes",
        "",
    ])

    for nid in target_matches[:10]:
        lines.append(f"- {render_node(nid, by_id)}")

    lines.extend([
        "",
        "## Candidate Paths",
        "",
    ])

    if not paths:
        lines.append("- no paths found")
        return "\n".join(lines)

    for index, path in enumerate(paths, start=1):
        lines.append(f"### Path {index}")
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
        "- This is topology-only path reconstruction.",
        "- Paths are candidate runtime relationships, not guaranteed chronological execution order.",
        "- Use raw Lua only to validate exact ordering and control flow.",
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Reconstruct candidate runtime topology paths.")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--topology")
    parser.add_argument("--from", dest="from_term", required=True)
    parser.add_argument("--to", dest="to_term", required=True)
    parser.add_argument("--max-depth", type=int, default=5)
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
        else workspace / "investigations" / f"paths_{args.from_term}_to_{args.to_term}.md"
    )

    if not output_path.is_absolute():
        output_path = workspace / output_path

    nodes, edges = load_topology(topology_path)
    by_id = {node_id(n): n for n in nodes if node_id(n)}
    graph = build_graph(edges)

    start_matches = find_nodes(nodes, args.from_term)
    target_matches = find_nodes(nodes, args.to_term)
    target_set = set(target_matches)

    paths = find_paths(
        graph,
        start_matches,
        target_set,
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