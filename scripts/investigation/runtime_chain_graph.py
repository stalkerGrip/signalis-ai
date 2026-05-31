from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import networkx as nx


@dataclass(frozen=True)
class GraphPaths:
    nodes: Path
    edges: Path
    out_json: Path
    out_md: Path


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def as_records(data: Any) -> List[Dict[str, Any]]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        for key in ("nodes", "edges", "records", "items"):
            value = data.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
    return []


def node_id(node: Dict[str, Any]) -> Optional[str]:
    for key in ("id", "node_id", "stable_id"):
        value = node.get(key)
        if value:
            return str(value)
    return None


def edge_end(edge: Dict[str, Any], *keys: str) -> Optional[str]:
    for key in keys:
        value = edge.get(key)
        if value:
            return str(value)
    return None


def edge_type(edge: Dict[str, Any]) -> str:
    for key in ("type", "edge_type", "relation", "label"):
        value = edge.get(key)
        if value:
            return str(value)
    return "unknown"


def normalize_path(value: Any) -> str:
    return str(value or "").replace("\\", "/")


def build_graph(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()

    for node in nodes:
        nid = node_id(node)
        if not nid:
            continue
        graph.add_node(nid, **node)

    skipped_edges = 0

    for idx, edge in enumerate(edges):
        src = edge_end(edge, "source", "from", "src", "source_id", "source_node", "sourceId")
        dst = edge_end(edge, "target", "to", "dst", "target_id", "target_node", "targetId")

        if not src or not dst:
            skipped_edges += 1
            continue

        etype = edge_type(edge)
        graph.add_edge(src, dst, key=f"{idx}:{etype}", edge_type=etype, **edge)

    graph.graph["skipped_edges"] = skipped_edges
    return graph


def index_graph(graph: nx.MultiDiGraph) -> Dict[str, Any]:
    node_type_counts = Counter()
    edge_type_counts = Counter()
    realm_counts = Counter()
    file_nodes = []
    hook_nodes = []
    network_nodes = []
    timer_nodes = []
    subsystem_nodes = []

    for nid, data in graph.nodes(data=True):
        ntype = str(data.get("type") or data.get("node_type") or "unknown")
        node_type_counts[ntype] += 1

        realm = data.get("realm")
        if realm:
            realm_counts[str(realm)] += 1

        blob = f"{nid} {data}".lower()

        if ntype == "file" or nid.startswith("file:"):
            file_nodes.append(nid)
        if "hook" in ntype or nid.startswith("hook:"):
            hook_nodes.append(nid)
        if "network" in ntype or nid.startswith("netmsg:") or nid.startswith("netop:"):
            network_nodes.append(nid)
        if "timer" in ntype or nid.startswith("timer:") or nid.startswith("timer_op:"):
            timer_nodes.append(nid)
        if ntype == "subsystem" or nid.startswith("subsystem:"):
            subsystem_nodes.append(nid)

    for _, _, data in graph.edges(data=True):
        edge_type_counts[str(data.get("edge_type") or "unknown")] += 1

    degree = dict(graph.degree())
    top_degree = sorted(degree.items(), key=lambda kv: kv[1], reverse=True)[:50]

    return {
        "node_type_counts": dict(node_type_counts.most_common()),
        "edge_type_counts": dict(edge_type_counts.most_common()),
        "realm_counts": dict(realm_counts.most_common()),
        "file_nodes": sorted(file_nodes),
        "hook_nodes": sorted(hook_nodes),
        "network_nodes": sorted(network_nodes),
        "timer_nodes": sorted(timer_nodes),
        "subsystem_nodes": sorted(subsystem_nodes),
        "top_degree_nodes": [{"id": nid, "degree": deg} for nid, deg in top_degree],
    }


def find_nodes(graph: nx.MultiDiGraph, query: str, limit: int = 25) -> List[Dict[str, Any]]:
    q = query.lower()
    matches = []

    for nid, data in graph.nodes(data=True):
        blob = f"{nid} {json.dumps(data, ensure_ascii=False)}".lower()
        if q in blob:
            matches.append(
                {
                    "id": nid,
                    "type": data.get("type") or data.get("node_type"),
                    "label": data.get("label") or data.get("name") or data.get("title"),
                    "file": normalize_path(data.get("file") or data.get("path") or data.get("source_file")),
                    "realm": data.get("realm"),
                    "degree": graph.degree(nid),
                }
            )

    return sorted(matches, key=lambda x: x["degree"], reverse=True)[:limit]


def shortest_paths(
    graph: nx.MultiDiGraph,
    source_query: str,
    target_query: str,
    max_paths: int,
    cutoff: int,
) -> List[Dict[str, Any]]:
    sources = [x["id"] for x in find_nodes(graph, source_query, limit=50)]
    targets = [x["id"] for x in find_nodes(graph, target_query, limit=50)]

    simple_directed = nx.DiGraph()
    simple_undirected = nx.Graph()

    for src, dst, data in graph.edges(data=True):
        etype = data.get("edge_type") or "unknown"
        simple_directed.add_edge(src, dst, edge_type=etype)
        simple_undirected.add_edge(src, dst, edge_type=etype)

    results = []

    for mode, g in (("directed", simple_directed), ("undirected", simple_undirected)):
        for src in sources:
            for dst in targets:
                if src == dst:
                    continue

                try:
                    paths = nx.shortest_simple_paths(g, src, dst)
                    for path in paths:
                        if len(path) - 1 > cutoff:
                            break

                        results.append(
                            {
                                "mode": mode,
                                "source": src,
                                "target": dst,
                                "length": len(path) - 1,
                                "path": path,
                            }
                        )

                        if len(results) >= max_paths:
                            return results

                except (nx.NetworkXNoPath, nx.NodeNotFound):
                    continue
                except nx.NetworkXNotImplemented:
                    continue

    return results


def path_edges(graph: nx.MultiDiGraph, path: List[str]) -> List[Dict[str, Any]]:
    out = []
    for src, dst in zip(path, path[1:]):
        edge_datas = graph.get_edge_data(src, dst) or {}
        edge_types = sorted(
            str(data.get("edge_type") or key)
            for key, data in edge_datas.items()
            if isinstance(data, dict)
        )
        out.append({"source": src, "target": dst, "edge_types": edge_types})
    return out


def summarize_node(graph: nx.MultiDiGraph, nid: str) -> Dict[str, Any]:
    data = dict(graph.nodes[nid])
    return {
        "id": nid,
        "type": data.get("type") or data.get("node_type"),
        "label": data.get("label") or data.get("name") or data.get("title"),
        "file": normalize_path(data.get("file") or data.get("path") or data.get("source_file")),
        "realm": data.get("realm"),
        "degree": graph.degree(nid),
    }


def make_report(
    graph: nx.MultiDiGraph,
    index: Dict[str, Any],
    source_query: Optional[str],
    target_query: Optional[str],
    paths: List[Dict[str, Any]],
) -> Dict[str, Any]:
    enriched_paths = []

    for item in paths:
        enriched_paths.append(
            {
                **item,
                "nodes": [summarize_node(graph, nid) for nid in item["path"]],
                "edges": path_edges(graph, item["path"]),
            }
        )

    return {
        "schema": "runtime_chain_graph_audit.v1",
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "skipped_edges": graph.graph.get("skipped_edges", 0),
        "node_type_counts": index["node_type_counts"],
        "edge_type_counts": index["edge_type_counts"],
        "realm_counts": index["realm_counts"],
        "top_degree_nodes": index["top_degree_nodes"][:25],
        "queries": {
            "source": source_query,
            "target": target_query,
        },
        "paths": enriched_paths,
    }


def write_md(path: Path, report: Dict[str, Any]) -> None:
    lines = []
    lines.append("# Runtime Chain Graph Audit")
    lines.append("")
    lines.append(f"- Schema: `{report['schema']}`")
    lines.append(f"- Nodes: **{report['nodes']}**")
    lines.append(f"- Edges: **{report['edges']}**")
    lines.append(f"- Skipped edges: **{report.get('skipped_edges', 0)}**")
    lines.append("")

    lines.append("## Node types")
    for k, v in list(report["node_type_counts"].items())[:25]:
        lines.append(f"- `{k}`: **{v}**")
    lines.append("")

    lines.append("## Edge types")
    for k, v in list(report["edge_type_counts"].items())[:35]:
        lines.append(f"- `{k}`: **{v}**")
    lines.append("")

    lines.append("## Realm counts")
    if report["realm_counts"]:
        for k, v in report["realm_counts"].items():
            lines.append(f"- `{k}`: **{v}**")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Top degree nodes")
    for item in report["top_degree_nodes"]:
        lines.append(f"- degree `{item['degree']}` | `{item['id']}`")
    lines.append("")

    lines.append("## Candidate paths")
    if not report["paths"]:
        lines.append("- none")
    else:
        for idx, p in enumerate(report["paths"], start=1):
            lines.append(f"### Path {idx}")
            lines.append("")
            lines.append(f"- Source: `{p['source']}`")
            lines.append(f"- Target: `{p['target']}`")
            lines.append(f"- Length: `{p['length']}`")
            lines.append("")
            for n in p["nodes"]:
                label = n.get("label") or n["id"]
                ntype = n.get("type") or "unknown"
                realm = n.get("realm") or "unknown"
                lines.append(f"- `{ntype}` `{realm}` — `{label}`")
                if n.get("file"):
                    lines.append(f"  - file: `{n['file']}`")
            lines.append("")
            lines.append("Edges:")
            for e in p["edges"]:
                lines.append(f"- `{e['source']}` → `{e['target']}` via `{', '.join(e['edge_types'])}`")
            lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def default_paths(workspace: Path) -> GraphPaths:
    return GraphPaths(
        nodes=workspace / "manifests" / "normalized" / "runtime_topology_nodes.json",
        edges=workspace / "manifests" / "normalized" / "runtime_topology_edges.json",
        out_json=workspace / "investigations" / "validation" / "runtime_chain_graph_audit_v1.json",
        out_md=workspace / "investigations" / "validation" / "runtime_chain_graph_audit_v1.md",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Runtime Chain Builder V4 graph foundation.")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--nodes", type=Path, default=None)
    parser.add_argument("--edges", type=Path, default=None)
    parser.add_argument("--out-json", type=Path, default=None)
    parser.add_argument("--out-md", type=Path, default=None)
    parser.add_argument("--source-query", default=None)
    parser.add_argument("--target-query", default=None)
    parser.add_argument("--max-paths", type=int, default=10)
    parser.add_argument("--cutoff", type=int, default=8)

    args = parser.parse_args()
    workspace = args.workspace.resolve()
    paths = default_paths(workspace)

    nodes_path = args.nodes or paths.nodes
    edges_path = args.edges or paths.edges
    out_json = args.out_json or paths.out_json
    out_md = args.out_md or paths.out_md

    nodes = as_records(load_json(nodes_path))
    edges = as_records(load_json(edges_path))

    graph = build_graph(nodes, edges)
    index = index_graph(graph)

    candidate_paths = []
    if args.source_query and args.target_query:
        candidate_paths = shortest_paths(
            graph=graph,
            source_query=args.source_query,
            target_query=args.target_query,
            max_paths=args.max_paths,
            cutoff=args.cutoff,
        )

    report = make_report(
        graph=graph,
        index=index,
        source_query=args.source_query,
        target_query=args.target_query,
        paths=candidate_paths,
    )

    write_json(out_json, report)
    write_md(out_md, report)

    print(f"Wrote graph audit JSON: {out_json}")
    print(f"Wrote graph audit MD:   {out_md}")
    print(f"Nodes: {graph.number_of_nodes()}")
    print(f"Edges: {graph.number_of_edges()}")
    print(f"Candidate paths: {len(candidate_paths)}")


if __name__ == "__main__":
    main()