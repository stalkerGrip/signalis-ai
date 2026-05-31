from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


CATEGORY_ORDER = {
    "lifecycle": 10,
    "event": 20,
    "state_mutation": 30,
    "sync": 40,
    "network": 50,
    "ui": 60,
    "timer": 70,
}


@dataclass
class FactGraphNode:
    node_id: str
    fact_key: str
    category: str
    kind: str
    name: str
    confidence: str
    realms: list[str]
    files: list[str]
    occurrences_count: int


@dataclass
class RuntimeFactGraph:
    schema: str
    source_runtime_facts: str
    nodes_count: int
    edges_count: int
    nodes: list[FactGraphNode] = field(default_factory=list)
    edges: list[dict[str, Any]] = field(default_factory=list)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_node_id(category: str, kind: str, name: str) -> str:
    safe_name = (
        name.replace("\\", "/")
        .replace(" ", "_")
        .replace('"', "")
        .replace("'", "")
        .replace(":", "_")
    )
    return f"fact:{category}:{kind}:{safe_name}"


def ordered_facts(facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        facts,
        key=lambda fact: (
            CATEGORY_ORDER.get(fact.get("category", ""), 999),
            fact.get("name", ""),
            fact.get("kind", ""),
            fact.get("fact_key", ""),
        ),
    )


def build_nodes(facts: list[dict[str, Any]]) -> list[FactGraphNode]:
    nodes: list[FactGraphNode] = []

    for fact in ordered_facts(facts):
        occurrences = fact.get("occurrences", [])

        realms = sorted(
            {
                occurrence.get("realm", "unknown")
                for occurrence in occurrences
                if occurrence.get("realm")
            }
        )

        files = sorted(
            {
                occurrence.get("file")
                for occurrence in occurrences
                if occurrence.get("file")
            }
        )

        nodes.append(
            FactGraphNode(
                node_id=stable_node_id(
                    fact.get("category", "unknown"),
                    fact.get("kind", "unknown"),
                    fact.get("name", "unknown"),
                ),
                fact_key=fact.get("fact_key", ""),
                category=fact.get("category", "unknown"),
                kind=fact.get("kind", "unknown"),
                name=fact.get("name", "unknown"),
                confidence=fact.get("confidence", "unknown"),
                realms=realms or ["unknown"],
                files=files,
                occurrences_count=len(occurrences),
            )
        )

    return nodes


def write_md(path: Path, graph: RuntimeFactGraph) -> None:
    lines: list[str] = [
        "# Runtime Fact Graph",
        "",
        f"- Schema: `{graph.schema}`",
        f"- Source runtime facts: `{graph.source_runtime_facts}`",
        f"- Nodes: `{graph.nodes_count}`",
        f"- Edges: `{graph.edges_count}`",
        "",
        "## Rule",
        "",
        "Runtime Fact Graph V2 is node-only.",
        "",
        "It does not infer ordering, causality, or runtime propagation.",
        "",
        "Edges must be created later by topology mapping and validated runtime chain reconstruction.",
        "",
        "## Nodes",
        "",
    ]

    by_category: dict[str, list[FactGraphNode]] = {}
    for node in graph.nodes:
        by_category.setdefault(node.category, []).append(node)

    for category in sorted(by_category, key=lambda c: CATEGORY_ORDER.get(c, 999)):
        lines += [
            f"### Category: `{category}`",
            "",
        ]

        for node in sorted(by_category[category], key=lambda n: n.name):
            lines += [
                f"- `{node.node_id}`",
                f"  - Name: `{node.name}`",
                f"  - Kind: `{node.kind}`",
                f"  - Confidence: `{node.confidence}`",
                f"  - Realms: `{', '.join(node.realms)}`",
                f"  - Files: `{len(node.files)}`",
                f"  - Occurrences: `{node.occurrences_count}`",
            ]

        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a node-only runtime fact graph from normalized runtime facts."
    )
    parser.add_argument("--runtime-facts", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)

    args = parser.parse_args()

    data = load_json(args.runtime_facts)

    if data.get("schema") != "runtime_facts.v2":
        raise ValueError(
            f"Expected schema runtime_facts.v2, got {data.get('schema')!r}"
        )

    facts = data.get("facts", [])
    nodes = build_nodes(facts)

    graph = RuntimeFactGraph(
        schema="runtime_fact_graph.v2",
        source_runtime_facts=str(args.runtime_facts),
        nodes_count=len(nodes),
        edges_count=0,
        nodes=nodes,
        edges=[],
    )

    payload = {
        **asdict(graph),
        "nodes": [asdict(node) for node in graph.nodes],
        "edges": [],
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_md(args.out_md, graph)

    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")
    print(f"Nodes:      {len(nodes)}")
    print("Edges:      0")


if __name__ == "__main__":
    main()