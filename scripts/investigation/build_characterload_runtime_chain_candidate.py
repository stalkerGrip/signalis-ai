#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ORDER = [
    "lifecycle_event",
    "inventory_initialization",
    "inventory_network_sync",
    "inventory_client_apply",
    "inventory_ui_open",
]

LABELS = {
    "lifecycle_event": "Character lifecycle propagation",
    "inventory_initialization": "Inventory loadout initialization",
    "inventory_network_sync": "Server inventory initialization sync",
    "inventory_client_apply": "Client inventory initialization apply",
    "inventory_ui_open": "Client inventory UI open/status sync",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def facts_by_category(facts: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for fact in facts:
        category = str(fact.get("category", "unknown"))
        grouped.setdefault(category, []).append(fact)
    return grouped


def build_stage(category: str, facts: list[dict[str, Any]], order: int) -> dict[str, Any]:
    files = sorted(set(str(f.get("file", "")) for f in facts if f.get("file")))
    realms = sorted(set(str(f.get("realm", "")) for f in facts if f.get("realm")))
    patterns = [str(f.get("pattern", "")) for f in facts if f.get("pattern")]

    return {
        "order": order,
        "category": category,
        "label": LABELS.get(category, category),
        "facts": [f.get("fact_id") for f in facts],
        "evidence_count": len(facts),
        "files": files,
        "realms": realms,
        "representative_patterns": patterns[:5],
    }


def score_chain(stages: list[dict[str, Any]], missing: list[str]) -> float:
    if not ORDER:
        return 0.0
    coverage = (len(ORDER) - len(missing)) / len(ORDER)
    evidence_bonus = min(sum(s["evidence_count"] for s in stages) / 20.0, 0.25)
    return round(min(coverage + evidence_bonus, 1.0), 4)


def confidence_for(score: float, missing: list[str]) -> str:
    if missing:
        return "medium" if score >= 0.75 else "low"
    if score >= 0.95:
        return "high"
    if score >= 0.75:
        return "medium"
    return "low"


def write_md(chain: dict[str, Any], out_md: Path) -> None:
    lines = [
        "# CharacterLoaded Inventory Runtime Chain Candidate",
        "",
        f"- Title: `{chain['title']}`",
        f"- Confidence: `{chain['confidence']}`",
        f"- Score: `{chain['score']}`",
        f"- Missing required stages: `{', '.join(chain['missing_required_stages']) if chain['missing_required_stages'] else 'none'}`",
        "",
        "## Runtime Chain",
        "",
        "```text",
    ]

    for stage in chain["stages"]:
        lines.append(f"{stage['order']}. {stage['category']} — {stage['label']}")

    lines += [
        "```",
        "",
        "## Stages",
        "",
    ]

    for stage in chain["stages"]:
        lines += [
            f"### {stage['order']}. {stage['category']}",
            "",
            f"- Label: `{stage['label']}`",
            f"- Evidence count: `{stage['evidence_count']}`",
            f"- Realms: `{', '.join(stage['realms']) if stage['realms'] else 'unknown'}`",
            f"- Files: `{', '.join(stage['files']) if stage['files'] else 'unknown'}`",
            "",
            "Representative patterns:",
            "",
        ]

        for pattern in stage["representative_patterns"]:
            lines.append(f"- `{pattern}`")

        lines.append("")

    out_md.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build CharacterLoaded inventory lifecycle runtime-chain candidate from normalized runtime facts."
    )
    parser.add_argument(
        "--runtime-facts",
        type=Path,
        default=Path("investigations/validation/characterload_inventory_runtime_facts.json"),
    )
    parser.add_argument(
        "--out-json",
        type=Path,
        default=Path("investigations/validation/characterload_inventory_runtime_chain_candidate_v1.json"),
    )
    parser.add_argument(
        "--out-md",
        type=Path,
        default=Path("investigations/validation/characterload_inventory_runtime_chain_candidate_v1.md"),
    )

    args = parser.parse_args()
    args.out_json.parent.mkdir(parents=True, exist_ok=True)

    data = load_json(args.runtime_facts)
    facts = data.get("facts", [])
    grouped = facts_by_category(facts)

    missing = [category for category in ORDER if not grouped.get(category)]

    stages = [
        build_stage(category, grouped[category], index + 1)
        for index, category in enumerate(ORDER)
        if grouped.get(category)
    ]

    score = score_chain(stages, missing)
    confidence = confidence_for(score, missing)

    chain = {
        "schema": "characterload_inventory_runtime_chain_candidate.v1",
        "title": "characterload inventory initialization lifecycle chain",
        "source_runtime_facts": str(args.runtime_facts),
        "root": "CharacterLoaded / PlayerLoadedChar",
        "join": "client inventory UI open/status sync",
        "confidence": confidence,
        "score": score,
        "missing_required_stages": missing,
        "stages": stages,
        "noise_categories": sorted(
            category for category in grouped
            if category not in ORDER
        ),
    }

    args.out_json.write_text(json.dumps(chain, indent=2, ensure_ascii=False), encoding="utf-8")
    write_md(chain, args.out_md)

    print(f"Runtime chain confidence: {confidence}")
    print(f"Runtime chain score: {score}")
    print(f"Missing required stages: {missing if missing else 'none'}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())