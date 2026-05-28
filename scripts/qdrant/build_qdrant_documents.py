#!/usr/bin/env python3
"""
build_qdrant_documents.py

Generate semantic architecture documents for later Qdrant ingestion.

Input:
  E:/signalis_ai/manifests/normalized/runtime_topology_nodes.json
  E:/signalis_ai/manifests/normalized/runtime_topology_edges.json
  optional docs under subsystem_docs/

Output:
  E:/signalis_ai/manifests/semantic/qdrant_documents.jsonl
  E:/signalis_ai/manifests/semantic/qdrant_documents_summary.md

This script does NOT require Qdrant or embeddings.
It prepares ontology-rich text chunks + metadata.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


TEXT_EXTS = {".md", ".txt"}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[WARN] Failed to load {path}: {exc}")
        return default


def write_jsonl(path: Path, docs: Iterable[Dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as f:
        for doc in docs:
            f.write(json.dumps(doc, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def stable_hash(value: str) -> str:
    return hashlib.sha1(value.encode("utf-8", errors="ignore")).hexdigest()[:16]


def norm_id(prefix: str, value: str) -> str:
    value = value.strip().replace("\\", "/")
    safe = re.sub(r"[^A-Za-z0-9_./:@#-]+", "_", value)
    return f"{prefix}:{safe}"


def node_id(node: Dict[str, Any]) -> str:
    return str(node.get("id") or node.get("node_id") or node.get("key") or stable_hash(json.dumps(node, sort_keys=True)))


def edge_source(edge: Dict[str, Any]) -> str:
    return str(edge.get("source") or edge.get("from") or edge.get("src") or "")


def edge_target(edge: Dict[str, Any]) -> str:
    return str(edge.get("target") or edge.get("to") or edge.get("dst") or "")


def edge_type(edge: Dict[str, Any]) -> str:
    return str(edge.get("type") or edge.get("edge_type") or edge.get("relation") or "unknown")


def node_type(node: Dict[str, Any]) -> str:
    return str(node.get("type") or node.get("node_type") or "unknown")


def node_label(node: Dict[str, Any]) -> str:
    for k in ("label", "name", "event", "message", "timer", "file", "plugin", "id"):
        if node.get(k) is not None:
            return str(node[k])
    return node_id(node)


def node_file(node: Dict[str, Any]) -> Optional[str]:
    for k in ("file", "path", "source_file", "relative_path"):
        if node.get(k):
            return str(node[k]).replace("\\", "/")
    return None


def short(v: Any, limit: int = 240) -> str:
    s = str(v) if v is not None else ""
    s = re.sub(r"\s+", " ", s).strip()
    return s[:limit] + ("..." if len(s) > limit else "")


@dataclass
class GraphIndex:
    nodes: Dict[str, Dict[str, Any]]
    edges: List[Dict[str, Any]]
    outgoing: Dict[str, List[Dict[str, Any]]]
    incoming: Dict[str, List[Dict[str, Any]]]


def build_index(nodes_raw: Any, edges_raw: Any) -> GraphIndex:
    if isinstance(nodes_raw, dict):
        nodes_iter = nodes_raw.get("nodes", nodes_raw.values())
    else:
        nodes_iter = nodes_raw or []

    if isinstance(edges_raw, dict):
        edges_iter = edges_raw.get("edges", edges_raw.values())
    else:
        edges_iter = edges_raw or []

    nodes: Dict[str, Dict[str, Any]] = {}
    for n in nodes_iter:
        if not isinstance(n, dict):
            continue
        nid = node_id(n)
        n = dict(n)
        n.setdefault("id", nid)
        nodes[nid] = n

    edges: List[Dict[str, Any]] = []
    outgoing: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    incoming: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for e in edges_iter:
        if not isinstance(e, dict):
            continue
        src, dst = edge_source(e), edge_target(e)
        if not src or not dst:
            continue
        e = dict(e)
        e.setdefault("source", src)
        e.setdefault("target", dst)
        e.setdefault("type", edge_type(e))
        edges.append(e)
        outgoing[src].append(e)
        incoming[dst].append(e)

    return GraphIndex(nodes, edges, outgoing, incoming)


def make_doc(doc_type: str, title: str, text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    base = f"{doc_type}|{title}|{metadata.get('source_id','')}|{metadata.get('chunk_index','')}"
    return {
        "id": f"doc:{doc_type}:{stable_hash(base)}",
        "doc_type": doc_type,
        "title": title,
        "text": text.strip(),
        "metadata": metadata,
    }


def doc_for_node(nid: str, node: Dict[str, Any], idx: GraphIndex) -> Dict[str, Any]:
    ntype = node_type(node)
    label = node_label(node)
    out = idx.outgoing.get(nid, [])
    inc = idx.incoming.get(nid, [])
    out_counts = Counter(edge_type(e) for e in out)
    inc_counts = Counter(edge_type(e) for e in inc)

    neighbor_lines: List[str] = []
    for direction, edges in (("outgoing", out[:12]), ("incoming", inc[:12])):
        for e in edges:
            other_id = edge_target(e) if direction == "outgoing" else edge_source(e)
            other = idx.nodes.get(other_id, {})
            neighbor_lines.append(f"- {direction} {edge_type(e)} -> {node_type(other)} {node_label(other)}")

    interesting = {
        k: v for k, v in node.items()
        if k not in {"id", "type", "node_type"} and v not in (None, "", [], {})
    }

    text = f"""
Runtime topology node: {label}
Node ID: {nid}
Node type: {ntype}
File: {node_file(node) or 'n/a'}
Realm: {node.get('realm', 'unknown')}
Plugin/subsystem: {node.get('plugin', node.get('subsystem', 'unknown'))}
Outgoing edge counts: {dict(out_counts)}
Incoming edge counts: {dict(inc_counts)}
Selected properties: {short(json.dumps(interesting, ensure_ascii=False, sort_keys=True), 900)}
Selected neighboring relationships:
{chr(10).join(neighbor_lines) if neighbor_lines else '- none'}
"""
    return make_doc(
        "runtime_node",
        f"{ntype}: {label}",
        text,
        {
            "source_id": nid,
            "node_type": ntype,
            "label": label,
            "file": node_file(node),
            "realm": node.get("realm"),
            "plugin": node.get("plugin"),
            "subsystem": node.get("subsystem"),
            "out_degree": len(out),
            "in_degree": len(inc),
            "degree": len(out) + len(inc),
        },
    )


def docs_for_hot_files(idx: GraphIndex, top_n: int = 80) -> List[Dict[str, Any]]:
    file_nodes = {nid: n for nid, n in idx.nodes.items() if node_type(n) == "file"}
    ranked = sorted(file_nodes.items(), key=lambda kv: len(idx.outgoing.get(kv[0], [])) + len(idx.incoming.get(kv[0], [])), reverse=True)[:top_n]
    docs: List[Dict[str, Any]] = []
    for fid, node in ranked:
        label = node_label(node).replace("\\", "/")
        out = idx.outgoing.get(fid, [])
        inc = idx.incoming.get(fid, [])
        counts = Counter(edge_type(e) for e in out + inc)
        related: List[str] = []
        for e in (out + inc)[:35]:
            other_id = edge_target(e) if edge_source(e) == fid else edge_source(e)
            other = idx.nodes.get(other_id, {})
            related.append(f"- {edge_type(e)}: {node_type(other)} {node_label(other)}")
        text = f"""
Runtime topology file summary: {label}
This source file participates in {len(out) + len(inc)} topology relationships.
Relationship counts: {dict(counts)}
Plugin/subsystem guess: {node.get('plugin', node.get('subsystem', 'unknown'))}
Realm: {node.get('realm', 'unknown')}
Selected relationships:
{chr(10).join(related) if related else '- none'}
Use this document to retrieve architectural context for this file without loading raw Lua by default.
"""
        docs.append(make_doc("file_topology", f"File topology: {label}", text, {
            "source_id": fid,
            "file": label,
            "degree": len(out) + len(inc),
            "node_type": "file",
        }))
    return docs


def docs_for_plugins(idx: GraphIndex) -> List[Dict[str, Any]]:
    plugin_to_nodes: Dict[str, List[Tuple[str, Dict[str, Any]]]] = defaultdict(list)
    for nid, n in idx.nodes.items():
        plugin = n.get("plugin")
        if not plugin and node_type(n) == "plugin":
            plugin = node_label(n)
        if plugin:
            plugin_to_nodes[str(plugin)].append((nid, n))

    docs: List[Dict[str, Any]] = []
    for plugin, members in sorted(plugin_to_nodes.items(), key=lambda kv: len(kv[1]), reverse=True):
        if plugin in {"unknown", "None"}:
            continue
        type_counts = Counter(node_type(n) for _, n in members)
        edge_counts: Counter[str] = Counter()
        hot_members: List[str] = []
        for nid, n in members:
            degree = len(idx.outgoing.get(nid, [])) + len(idx.incoming.get(nid, []))
            if degree:
                hot_members.append(f"- {node_type(n)} {node_label(n)} degree={degree}")
            for e in idx.outgoing.get(nid, []) + idx.incoming.get(nid, []):
                edge_counts[edge_type(e)] += 1
        text = f"""
Plugin/subsystem topology summary: {plugin}
Member node counts by type: {dict(type_counts)}
Relationship counts: {dict(edge_counts.most_common(25))}
Hot members:
{chr(10).join(hot_members[:35]) if hot_members else '- none'}
Architectural use: retrieve this when analyzing coupling, responsibilities, runtime load, networking, timers, hooks, or refactoring boundaries for {plugin}.
"""
        docs.append(make_doc("plugin_topology", f"Plugin topology: {plugin}", text, {
            "source_id": norm_id("plugin", plugin),
            "plugin": plugin,
            "node_count": len(members),
            "node_type": "plugin_summary",
        }))
    return docs


def docs_for_subsystems(idx: GraphIndex) -> List[Dict[str, Any]]:
    subsystem_to_nodes: Dict[str, List[Tuple[str, Dict[str, Any]]]] = defaultdict(list)
    for nid, n in idx.nodes.items():
        subsystem = n.get("subsystem")
        if subsystem:
            subsystem_to_nodes[str(subsystem)].append((nid, n))
    docs: List[Dict[str, Any]] = []
    for subsystem, members in sorted(subsystem_to_nodes.items(), key=lambda kv: len(kv[1]), reverse=True):
        type_counts = Counter(node_type(n) for _, n in members)
        files = sorted({node_file(n) for _, n in members if node_file(n)})[:40]
        labels = [f"- {node_type(n)} {node_label(n)}" for _, n in members[:50]]
        text = f"""
Subsystem topology summary: {subsystem}
Node counts by type: {dict(type_counts)}
Representative files:
{chr(10).join('- ' + f for f in files) if files else '- none'}
Representative nodes:
{chr(10).join(labels) if labels else '- none'}
Architectural use: retrieve this for subsystem-level questions, optimization, responsibility boundaries, and runtime propagation analysis.
"""
        docs.append(make_doc("subsystem_topology", f"Subsystem topology: {subsystem}", text, {
            "source_id": norm_id("subsystem", subsystem),
            "subsystem": subsystem,
            "node_count": len(members),
            "node_type": "subsystem_summary",
        }))
    return docs


def chunk_text(text: str, max_chars: int = 3500, overlap: int = 300) -> List[str]:
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        cut = text.rfind("\n\n", start, end)
        if cut > start + max_chars // 2:
            end = cut
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(0, end - overlap)
    return chunks


def docs_for_doctrine(workspace: Path) -> List[Dict[str, Any]]:
    roots = [workspace / "subsystem_docs", workspace / "docs", workspace / "manifests" / "docs"]
    docs: List[Dict[str, Any]] = []
    seen: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path in seen or not path.is_file() or path.suffix.lower() not in TEXT_EXTS:
                continue
            seen.add(path)
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue
            rel = str(path.relative_to(workspace)).replace("\\", "/")
            chunks = chunk_text(text)
            for i, chunk in enumerate(chunks):
                docs.append(make_doc("doctrine", f"Doctrine: {rel}#{i}", chunk, {
                    "source_id": rel,
                    "file": rel,
                    "chunk_index": i,
                    "node_type": "doctrine",
                }))
    return docs


def build_summary(path: Path, docs: List[Dict[str, Any]], idx: GraphIndex) -> None:
    doc_counts = Counter(d["doc_type"] for d in docs)
    node_counts = Counter(node_type(n) for n in idx.nodes.values())
    edge_counts = Counter(edge_type(e) for e in idx.edges)
    lines = [
        "# Qdrant document generation summary",
        "",
        "Schema: `qdrant_documents.v1`",
        "",
        "## Inputs",
        f"- Runtime topology nodes: **{len(idx.nodes)}**",
        f"- Runtime topology edges: **{len(idx.edges)}**",
        "",
        "## Documents",
        f"- Total documents: **{len(docs)}**",
        "",
        "## Document types",
    ]
    for k, v in doc_counts.most_common():
        lines.append(f"- `{k}`: **{v}**")
    lines += ["", "## Top node types"]
    for k, v in node_counts.most_common(25):
        lines.append(f"- `{k}`: **{v}**")
    lines += ["", "## Top edge types"]
    for k, v in edge_counts.most_common(25):
        lines.append(f"- `{k}`: **{v}**")
    lines += [
        "", 
        "## Notes",
        "- This step prepares semantic text documents only; it does not call an embedding model or Qdrant.",
        "- Raw Lua should remain a secondary retrieval layer; these documents are the primary architecture-reasoning layer.",
        "- Use metadata fields such as `doc_type`, `node_type`, `plugin`, `subsystem`, `file`, and `degree` for filtered retrieval.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", default="E:/signalis_ai")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--include-node-docs", action="store_true", help="Include per-node documents for all nodes. Can be large.")
    ap.add_argument("--top-node-docs", type=int, default=900, help="Include this many high-degree node docs by default.")
    args = ap.parse_args()

    workspace = Path(args.workspace)
    norm = workspace / "manifests" / "normalized"
    sem = workspace / "manifests" / "semantic"

    nodes_raw = load_json(norm / "runtime_topology_nodes.json", [])
    edges_raw = load_json(norm / "runtime_topology_edges.json", [])
    idx = build_index(nodes_raw, edges_raw)

    docs: List[Dict[str, Any]] = []
    docs.extend(docs_for_plugins(idx))
    docs.extend(docs_for_subsystems(idx))
    docs.extend(docs_for_hot_files(idx))
    docs.extend(docs_for_doctrine(workspace))

    ranked_nodes = sorted(idx.nodes.items(), key=lambda kv: len(idx.outgoing.get(kv[0], [])) + len(idx.incoming.get(kv[0], [])), reverse=True)
    if args.include_node_docs:
        selected_nodes = ranked_nodes
    else:
        selected_nodes = ranked_nodes[: max(0, args.top_node_docs)]
    docs.extend(doc_for_node(nid, n, idx) for nid, n in selected_nodes)

    # Deduplicate by text hash while preserving IDs if possible.
    unique: Dict[str, Dict[str, Any]] = {}
    for d in docs:
        key = stable_hash(d["doc_type"] + "|" + d["title"] + "|" + d["text"])
        unique[key] = d
    docs = list(unique.values())

    if args.write:
        out_jsonl = sem / "qdrant_documents.jsonl"
        out_md = sem / "qdrant_documents_summary.md"
        write_jsonl(out_jsonl, docs)
        build_summary(out_md, docs, idx)
        print(f"Wrote {out_jsonl}")
        print(f"Wrote {out_md}")
    else:
        print(json.dumps({
            "documents": len(docs),
            "nodes": len(idx.nodes),
            "edges": len(idx.edges),
            "doc_types": Counter(d["doc_type"] for d in docs),
        }, ensure_ascii=False, indent=2, default=dict))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
