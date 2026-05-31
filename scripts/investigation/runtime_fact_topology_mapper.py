from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


PREFERRED_TYPES = {
    "lifecycle": {"hook_event", "hook_emitter", "hook_listener"},
    "event": {"hook_event", "hook_emitter", "hook_listener"},
    "network": {"network_message", "network_operation"},
    "ui": {"network_message", "network_operation"},
    "timer": {"timer", "timer_operation"},
}


EXPECTED_UNMAPPED = {
    ("sync", "sync_call", "sync"),
}


@dataclass
class TopologyMatch:
    topology_node_id: str
    node_type: str | None
    name: str | None
    label: str | None
    realm: str | None
    score: float
    quality: str
    reason: str


@dataclass
class FactTopologyBinding:
    fact_node_id: str
    fact_key: str
    fact_category: str
    fact_kind: str
    fact_name: str
    fact_realms: list[str]
    mapping_status: str
    top_match_score: float
    matches: list[TopologyMatch] = field(default_factory=list)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def get_topology_nodes(topology: dict[str, Any]) -> list[dict[str, Any]]:
    nodes = topology.get("nodes", [])
    if isinstance(nodes, dict):
        return [
            {"id": node_id, **payload}
            for node_id, payload in nodes.items()
            if isinstance(payload, dict)
        ]
    if isinstance(nodes, list):
        return nodes
    return []


def node_id(node: dict[str, Any]) -> str:
    return str(node.get("id") or node.get("node_id") or "")


def node_type(node: dict[str, Any]) -> str:
    return str(node.get("type") or node.get("node_type") or "")


def node_name(node: dict[str, Any]) -> str:
    for key in ("name", "label", "event", "message", "timer", "hook", "title"):
        value = node.get(key)
        if isinstance(value, str) and value:
            return value
    return node_id(node)


def node_label(node: dict[str, Any]) -> str:
    for key in ("label", "display", "title", "name"):
        value = node.get(key)
        if isinstance(value, str) and value:
            return value
    return node_id(node)


def node_realm(node: dict[str, Any]) -> str | None:
    value = node.get("realm")
    if isinstance(value, str) and value:
        return value
    return None


def normalize(value: str) -> str:
    return value.lower().replace("\\", "/").strip()


def quality_from_score(score: float) -> str:
    if score >= 1.0:
        return "strong"
    if score >= 0.75:
        return "medium"
    return "weak"


def is_expected_unmapped(fact: dict[str, Any]) -> bool:
    return (
        str(fact.get("category", "")),
        str(fact.get("kind", "")),
        str(fact.get("name", "")),
    ) in EXPECTED_UNMAPPED


def score_match(fact: dict[str, Any], node: dict[str, Any]) -> TopologyMatch | None:
    fact_name = str(fact.get("name", ""))
    fact_category = str(fact.get("category", ""))
    fact_realms = set(fact.get("realms", []))

    tid = node_id(node)
    ttype = node_type(node)
    tname = node_name(node)
    tlabel = node_label(node)
    trealm = node_realm(node)

    n_fact = normalize(fact_name)
    n_id = normalize(tid)
    n_name = normalize(tname)
    n_label = normalize(tlabel)

    if not n_fact:
        return None

    score = 0.0
    reasons: list[str] = []

    preferred = PREFERRED_TYPES.get(fact_category, set())

    exact_identity = False

    if n_fact == n_name:
        score += 0.55
        reasons.append("exact name match")
        exact_identity = True

    if n_fact == n_label:
        score += 0.45
        reasons.append("exact label match")
        exact_identity = True

    # Strict identity suffix only.
    # Allows:
    #   hook:PlayerLoadedChar
    #   netmsg:netstream:item
    # Rejects:
    #   ItemFound
    #   RemoveItem
    #   adminSpawnItem
    id_parts = [part for part in n_id.replace("\\", "/").split(":") if part]
    if id_parts and id_parts[-1] == n_fact:
        score += 0.35
        reasons.append("exact topology id suffix match")
        exact_identity = True

    if not exact_identity:
        return None

    if ttype in preferred:
        score += 0.30
        reasons.append("preferred topology node type")
    elif preferred:
        score -= 0.20
        reasons.append("non-preferred topology node type")

    if trealm and trealm in fact_realms:
        score += 0.10
        reasons.append("realm match")

    if fact_category in {"network", "ui"}:
        if ttype == "network_message":
            score += 0.20
            reasons.append("network message preferred over operation")
        elif ttype == "network_operation":
            score += 0.05
            reasons.append("network operation secondary match")

    if fact_category in {"event", "lifecycle"}:
        if ttype == "hook_event":
            score += 0.20
            reasons.append("hook event preferred over listener/emitter")
        elif ttype in {"hook_emitter", "hook_listener"}:
            score += 0.05
            reasons.append("hook emitter/listener secondary match")

    if score < 0.65:
        return None

    return TopologyMatch(
        topology_node_id=tid,
        node_type=ttype or None,
        name=tname or None,
        label=tlabel or None,
        realm=trealm,
        score=round(score, 4),
        quality=quality_from_score(score),
        reason="; ".join(reasons),
    )


def build_bindings(
    fact_graph: dict[str, Any],
    topology: dict[str, Any],
    max_matches: int,
) -> list[FactTopologyBinding]:
    facts = fact_graph.get("nodes", [])
    topology_nodes = get_topology_nodes(topology)

    bindings: list[FactTopologyBinding] = []

    for fact in facts:
        matches: list[TopologyMatch] = []

        if not is_expected_unmapped(fact):
            for node in topology_nodes:
                match = score_match(fact, node)
                if match:
                    matches.append(match)

        matches.sort(
            key=lambda m: (
                -m.score,
                0 if m.node_type in PREFERRED_TYPES.get(str(fact.get("category", "")), set()) else 1,
                m.topology_node_id,
            )
        )

        matches = matches[:max_matches]
        top_score = matches[0].score if matches else 0.0

        if matches:
            status = "mapped"
        elif is_expected_unmapped(fact):
            status = "expected_unmapped"
        else:
            status = "unmapped"

        bindings.append(
            FactTopologyBinding(
                fact_node_id=str(fact.get("node_id", "")),
                fact_key=str(fact.get("fact_key", "")),
                fact_category=str(fact.get("category", "")),
                fact_kind=str(fact.get("kind", "")),
                fact_name=str(fact.get("name", "")),
                fact_realms=list(fact.get("realms", [])),
                mapping_status=status,
                top_match_score=round(top_score, 4),
                matches=matches,
            )
        )

    return bindings


def write_md(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Runtime Fact Topology Mapping",
        "",
        f"- Schema: `{payload['schema']}`",
        f"- Runtime fact graph: `{payload['runtime_fact_graph']}`",
        f"- Runtime topology: `{payload['runtime_topology']}`",
        f"- Facts: `{payload['facts_count']}`",
        f"- Mapped: `{payload['mapped_count']}`",
        f"- Expected unmapped: `{payload['expected_unmapped_count']}`",
        f"- Unmapped: `{payload['unmapped_count']}`",
        "",
        "## Bindings",
        "",
    ]

    for binding in payload["bindings"]:
        lines += [
            f"### `{binding['fact_name']}`",
            "",
            f"- Fact key: `{binding['fact_key']}`",
            f"- Category: `{binding['fact_category']}`",
            f"- Kind: `{binding['fact_kind']}`",
            f"- Realms: `{', '.join(binding['fact_realms'])}`",
            f"- Mapping status: `{binding['mapping_status']}`",
            f"- Top match score: `{binding['top_match_score']}`",
            f"- Matches: `{len(binding['matches'])}`",
            "",
        ]

        if not binding["matches"]:
            if binding["mapping_status"] == "expected_unmapped":
                lines += ["_Expected unmapped generic fact._", ""]
            else:
                lines += ["_No topology matches found._", ""]
            continue

        for match in binding["matches"]:
            lines += [
                f"- `{match['topology_node_id']}`",
                f"  - Type: `{match['node_type']}`",
                f"  - Name: `{match['name']}`",
                f"  - Realm: `{match['realm']}`",
                f"  - Score: `{match['score']}`",
                f"  - Quality: `{match['quality']}`",
                f"  - Reason: {match['reason']}",
            ]

        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Map runtime fact graph nodes to runtime topology nodes with stricter quality scoring."
    )
    parser.add_argument("--runtime-fact-graph", required=True, type=Path)
    parser.add_argument("--runtime-topology", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--max-matches", type=int, default=5)

    args = parser.parse_args()

    fact_graph = load_json(args.runtime_fact_graph)
    topology = load_json(args.runtime_topology)

    if fact_graph.get("schema") != "runtime_fact_graph.v2":
        raise ValueError(
            f"Expected runtime_fact_graph.v2, got {fact_graph.get('schema')!r}"
        )

    bindings = build_bindings(
        fact_graph=fact_graph,
        topology=topology,
        max_matches=args.max_matches,
    )

    mapped = sum(1 for b in bindings if b.mapping_status == "mapped")
    expected_unmapped = sum(1 for b in bindings if b.mapping_status == "expected_unmapped")
    unmapped = sum(1 for b in bindings if b.mapping_status == "unmapped")

    payload = {
        "schema": "runtime_fact_topology.v3",
        "runtime_fact_graph": str(args.runtime_fact_graph),
        "runtime_topology": str(args.runtime_topology),
        "facts_count": len(bindings),
        "mapped_count": mapped,
        "expected_unmapped_count": expected_unmapped,
        "unmapped_count": unmapped,
        "bindings": [
            {
                **asdict(binding),
                "matches": [asdict(match) for match in binding.matches],
            }
            for binding in bindings
        ],
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    write_md(args.out_md, payload)

    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")
    print(f"Facts:      {len(bindings)}")
    print(f"Mapped:     {mapped}")
    print(f"Expected:   {expected_unmapped}")
    print(f"Unmapped:   {unmapped}")


if __name__ == "__main__":
    main()