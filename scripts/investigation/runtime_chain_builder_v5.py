from __future__ import annotations

import argparse
import json
from collections import deque
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ChainLink:
    source_fact: str
    target_fact: str
    source_topology_node: str
    target_topology_node: str
    path_found: bool
    path_length: int | None
    path: list[str]
    confidence: str
    reason: str


@dataclass
class RuntimeChainCandidate:
    schema: str
    title: str
    runtime_facts: str
    runtime_fact_topology: str
    runtime_topology: str
    facts_count: int
    mapped_facts_count: int
    links_count: int
    supported_links_count: int
    confidence: str
    links: list[ChainLink] = field(default_factory=list)


CATEGORY_ORDER = {
    "lifecycle": 10,
    "event": 20,
    "state_mutation": 30,
    "sync": 40,
    "network": 50,
    "ui": 60,
    "timer": 70,
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def get_edges(topology: dict[str, Any]) -> list[dict[str, Any]]:
    edges = topology.get("edges", [])
    if isinstance(edges, list):
        return edges
    return []


def edge_source(edge: dict[str, Any]) -> str | None:
    for key in ("source", "from", "src"):
        value = edge.get(key)
        if isinstance(value, str):
            return value
    return None


def edge_target(edge: dict[str, Any]) -> str | None:
    for key in ("target", "to", "dst"):
        value = edge.get(key)
        if isinstance(value, str):
            return value
    return None


def build_adjacency(topology: dict[str, Any]) -> dict[str, list[str]]:
    adjacency: dict[str, list[str]] = {}

    for edge in get_edges(topology):
        src = edge_source(edge)
        dst = edge_target(edge)

        if not src or not dst:
            continue

        adjacency.setdefault(src, []).append(dst)

    return adjacency


def shortest_path(
    adjacency: dict[str, list[str]],
    source: str,
    target: str,
    max_depth: int,
) -> list[str] | None:
    if source == target:
        return [source]

    queue = deque([(source, [source])])
    visited = {source}

    while queue:
        node, path = queue.popleft()

        if len(path) > max_depth + 1:
            continue

        for nxt in adjacency.get(node, []):
            if nxt in visited:
                continue

            new_path = path + [nxt]

            if nxt == target:
                return new_path

            visited.add(nxt)
            queue.append((nxt, new_path))

    return None


def mapped_bindings(fact_topology: dict[str, Any]) -> list[dict[str, Any]]:
    bindings = []

    for binding in fact_topology.get("bindings", []):
        if binding.get("mapping_status") != "mapped":
            continue
        if not binding.get("matches"):
            continue
        bindings.append(binding)

    return bindings


def primary_topology_node(binding: dict[str, Any]) -> str | None:
    matches = binding.get("matches", [])
    if not matches:
        return None
    return matches[0].get("topology_node_id")


def ordered_bindings(
    bindings: list[dict[str, Any]],
    stage_facts: list[str],
) -> list[dict[str, Any]]:
    if stage_facts:
        by_name: dict[str, list[dict[str, Any]]] = {}
        for binding in bindings:
            by_name.setdefault(str(binding.get("fact_name", "")), []).append(binding)

        ordered: list[dict[str, Any]] = []
        for name in stage_facts:
            matches = by_name.get(name, [])
            if matches:
                ordered.append(matches[0])

        return ordered

    return sorted(
        bindings,
        key=lambda b: (
            CATEGORY_ORDER.get(str(b.get("fact_category", "")), 999),
            str(b.get("fact_name", "")),
            str(b.get("fact_kind", "")),
            str(b.get("fact_key", "")),
        ),
    )


def confidence_for_link(path: list[str] | None) -> str:
    if not path:
        return "none"
    if len(path) <= 2:
        return "high"
    if len(path) <= 5:
        return "medium"
    return "low"


def build_links(
    bindings: list[dict[str, Any]],
    adjacency: dict[str, list[str]],
    max_depth: int,
    stage_facts: list[str],
) -> list[ChainLink]:
    links: list[ChainLink] = []
    ordered = ordered_bindings(bindings, stage_facts)

    for left, right in zip(ordered, ordered[1:]):
        left_node = primary_topology_node(left)
        right_node = primary_topology_node(right)

        if not left_node or not right_node:
            continue

        path = shortest_path(adjacency, left_node, right_node, max_depth=max_depth)

        if path:
            links.append(
                ChainLink(
                    source_fact=str(left.get("fact_name")),
                    target_fact=str(right.get("fact_name")),
                    source_topology_node=left_node,
                    target_topology_node=right_node,
                    path_found=True,
                    path_length=len(path) - 1,
                    path=path,
                    confidence=confidence_for_link(path),
                    reason="Topology path found between primary mapped fact nodes.",
                )
            )
        else:
            links.append(
                ChainLink(
                    source_fact=str(left.get("fact_name")),
                    target_fact=str(right.get("fact_name")),
                    source_topology_node=left_node,
                    target_topology_node=right_node,
                    path_found=False,
                    path_length=None,
                    path=[],
                    confidence="none",
                    reason="No topology path found within max depth.",
                )
            )

    return links


def candidate_confidence(links: list[ChainLink]) -> str:
    if not links:
        return "none"

    supported = [link for link in links if link.path_found]
    ratio = len(supported) / len(links)

    if ratio >= 0.8:
        return "high"
    if ratio >= 0.5:
        return "medium"
    if ratio > 0:
        return "low"
    return "none"


def write_md(path: Path, candidate: RuntimeChainCandidate) -> None:
    lines = [
        "# Runtime Chain Candidate V5",
        "",
        f"- Title: `{candidate.title}`",
        f"- Schema: `{candidate.schema}`",
        f"- Facts: `{candidate.facts_count}`",
        f"- Mapped facts: `{candidate.mapped_facts_count}`",
        f"- Links: `{candidate.links_count}`",
        f"- Supported links: `{candidate.supported_links_count}`",
        f"- Confidence: `{candidate.confidence}`",
        "",
        "## Important Rule",
        "",
        "This is a generic topology-supported candidate.",
        "",
        "It is not promoted.",
        "It is not proof of causality.",
        "It must pass regression and targeted validation before promotion.",
        "",
        "## Links",
        "",
    ]

    for link in candidate.links:
        lines += [
            f"### `{link.source_fact}` → `{link.target_fact}`",
            "",
            f"- Path found: `{link.path_found}`",
            f"- Path length: `{link.path_length}`",
            f"- Confidence: `{link.confidence}`",
            f"- Source topology node: `{link.source_topology_node}`",
            f"- Target topology node: `{link.target_topology_node}`",
            f"- Reason: {link.reason}",
            "",
        ]

        if link.path:
            lines += [
                "```text",
                "\n→ ".join(link.path),
                "```",
                "",
            ]

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build generic runtime chain candidate from runtime facts and fact-topology bindings."
    )
    parser.add_argument("--title", required=True)
    parser.add_argument("--runtime-facts", required=True, type=Path)
    parser.add_argument("--runtime-fact-topology", required=True, type=Path)
    parser.add_argument("--runtime-topology", required=True, type=Path)
    parser.add_argument(
        "--stage-facts",
        default="",
        help="Comma-separated ordered fact names to build chain links from.",
    )
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--max-depth", type=int, default=8)

    args = parser.parse_args()

    runtime_facts = load_json(args.runtime_facts)
    fact_topology = load_json(args.runtime_fact_topology)
    runtime_topology = load_json(args.runtime_topology)

    if runtime_facts.get("schema") != "runtime_facts.v2":
        raise ValueError(f"Expected runtime_facts.v2, got {runtime_facts.get('schema')!r}")

    if fact_topology.get("schema") != "runtime_fact_topology.v3":
        raise ValueError(
            f"Expected runtime_fact_topology.v3, got {fact_topology.get('schema')!r}"
        )

    adjacency = build_adjacency(runtime_topology)
    bindings = mapped_bindings(fact_topology)

    stage_facts = [
        item.strip()
        for item in args.stage_facts.split(",")
        if item.strip()
    ]

    links = build_links(
        bindings=bindings,
        adjacency=adjacency,
        max_depth=args.max_depth,
        stage_facts=stage_facts,
    )

    supported = sum(1 for link in links if link.path_found)

    candidate = RuntimeChainCandidate(
        schema="runtime_chain_candidate.v5",
        title=args.title,
        runtime_facts=str(args.runtime_facts),
        runtime_fact_topology=str(args.runtime_fact_topology),
        runtime_topology=str(args.runtime_topology),
        facts_count=int(runtime_facts.get("unique_facts_count", len(runtime_facts.get("facts", [])))),
        mapped_facts_count=len(bindings),
        links_count=len(links),
        supported_links_count=supported,
        confidence=candidate_confidence(links),
        links=links,
    )

    payload = {
        **asdict(candidate),
        "links": [asdict(link) for link in candidate.links],
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_md(args.out_md, candidate)

    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")
    print(f"Facts:      {candidate.facts_count}")
    print(f"Mapped:     {candidate.mapped_facts_count}")
    print(f"Links:      {candidate.links_count}")
    print(f"Supported:  {candidate.supported_links_count}")
    print(f"Confidence: {candidate.confidence}")


if __name__ == "__main__":
    main()