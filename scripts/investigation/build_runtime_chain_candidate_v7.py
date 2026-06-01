from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PIPELINE_CONTRACT = {
    "script_id": "scripts.investigation.build_runtime_chain_candidate_v7",
    "purpose": "Build generic runtime_chain_candidate.v7 from ordered_runtime_facts.v1 without benchmark-specific stage constants.",
    "pipeline_stage": "runtime_chain_candidate",
    "input_schemas": ["ordered_runtime_facts.v1"],
    "output_schemas": ["runtime_chain_candidate.v7"],
    "artifact_patterns": [
        "investigations/validation/*_runtime_chain_candidate_v7.json",
        "investigations/validation/*_runtime_chain_candidate_v7.md",
    ],
    "promotion_role": "promotion_core",
    "canonical_status": "active",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_schema(data: dict[str, Any], expected: str, path: Path) -> None:
    actual = data.get("schema")
    if actual != expected:
        raise ValueError(f"{path}: expected schema {expected!r}, got {actual!r}")


def unique_sorted(values: list[Any]) -> list[str]:
    return sorted({str(v) for v in values if v not in (None, "", [])})


def first_occurrence(fact: dict[str, Any]) -> dict[str, Any]:
    occurrences = fact.get("occurrences")
    if isinstance(occurrences, list) and occurrences and isinstance(occurrences[0], dict):
        return occurrences[0]
    return {}


def fact_file(fact: dict[str, Any]) -> str:
    occurrence = first_occurrence(fact)
    return str(
        fact.get("source_file")
        or fact.get("file")
        or occurrence.get("file")
        or ""
    )


def fact_line(fact: dict[str, Any]) -> Any:
    occurrence = first_occurrence(fact)
    return fact.get("line") or occurrence.get("line")


def fact_realm(fact: dict[str, Any]) -> str:
    occurrence = first_occurrence(fact)
    return str(fact.get("realm") or occurrence.get("realm") or "unknown")


def fact_id(fact: dict[str, Any]) -> str:
    return str(fact.get("id") or fact.get("fact_key") or "")


def build_stage(stage_id: str, facts: list[dict[str, Any]], stage_groups: list[dict[str, Any]]) -> dict[str, Any]:
    stage_facts = [fact for fact in facts if fact.get("stage") == stage_id]

    group = next(
        (candidate for candidate in stage_groups if candidate.get("stage") == stage_id),
        {},
    )

    return {
        "stage": stage_id,
        "description": group.get("reason", ""),
        "present": bool(stage_facts),
        "fact_ids": [fact_id(fact) for fact in stage_facts],
        "supporting_facts_count": len(stage_facts),
        "realms": unique_sorted([fact_realm(fact) for fact in stage_facts]),
        "kinds": unique_sorted([fact.get("kind") for fact in stage_facts]),
        "categories": unique_sorted([fact.get("category") for fact in stage_facts]),
        "names": unique_sorted([fact.get("name") for fact in stage_facts]),
        "source_files": unique_sorted([fact_file(fact) for fact in stage_facts]),
        "lines": unique_sorted([fact_line(fact) for fact in stage_facts]),
    }


def build_edges(stages: list[dict[str, Any]], rule_set_id: str) -> list[dict[str, Any]]:
    present_stages = [stage["stage"] for stage in stages if stage["present"]]

    edges = []

    for from_stage, to_stage in zip(present_stages, present_stages[1:]):
        edges.append({
            "from_stage": from_stage,
            "to_stage": to_stage,
            "type": "runtime_stage_precedence",
            "support": f"ordered_runtime_facts.v1:{rule_set_id}",
        })

    return edges


def confidence_and_score(required_stage_ids: list[str], missing_required_stages: list[str]) -> tuple[str, float]:
    if not required_stage_ids:
        return "medium", 0.5

    total = len(required_stage_ids)
    missing = len(missing_required_stages)
    score = round((total - missing) / total, 4)

    if missing == 0:
        return "high", score

    if score >= 0.75:
        return "medium", score

    if score > 0:
        return "low", score

    return "none", score


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build generic runtime chain candidate V7 from ordered runtime facts."
    )
    parser.add_argument("--ordered-facts", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    ordered = load_json(args.ordered_facts)
    require_schema(ordered, "ordered_runtime_facts.v1", args.ordered_facts)

    facts = ordered.get("ordered_facts")
    if not isinstance(facts, list):
        raise ValueError("ordered facts JSON must contain list field: ordered_facts")

    facts = [fact for fact in facts if isinstance(fact, dict)]

    stage_order = ordered.get("stage_order")
    if not isinstance(stage_order, list) or not all(isinstance(stage, str) for stage in stage_order):
        raise ValueError("ordered facts JSON must contain list field: stage_order")

    required_stage_ids = ordered.get("required_stage_ids", [])
    if not isinstance(required_stage_ids, list):
        raise ValueError("ordered facts JSON field required_stage_ids must be a list")

    optional_stage_ids = ordered.get("optional_stage_ids", [])
    if not isinstance(optional_stage_ids, list):
        raise ValueError("ordered facts JSON field optional_stage_ids must be a list")

    stage_rule_set = ordered.get("stage_rule_set", {})
    if not isinstance(stage_rule_set, dict):
        stage_rule_set = {}

    rule_set_id = str(stage_rule_set.get("rule_set_id") or "unknown_stage_rule_set")
    title = str(stage_rule_set.get("title") or rule_set_id)

    stage_groups = ordered.get("stage_groups", [])
    if not isinstance(stage_groups, list):
        stage_groups = []

    stages = [
        build_stage(stage_id, facts, stage_groups)
        for stage_id in stage_order
    ]

    present_stage_ids = {
        stage["stage"]
        for stage in stages
        if stage["present"]
    }

    missing_required_stages = [
        stage_id
        for stage_id in required_stage_ids
        if stage_id not in present_stage_ids
    ]

    missing_stages = [
        stage_id
        for stage_id in stage_order
        if stage_id not in present_stage_ids
    ]

    confidence, score = confidence_and_score(
        [str(stage) for stage in required_stage_ids],
        [str(stage) for stage in missing_required_stages],
    )

    edges = build_edges(stages, rule_set_id)

    source_files = unique_sorted([
        source_file
        for stage in stages
        for source_file in stage["source_files"]
    ])

    realms = unique_sorted([
        realm
        for stage in stages
        for realm in stage["realms"]
    ])

    result = {
        "schema": "runtime_chain_candidate.v7",
        "producer_script": PIPELINE_CONTRACT["script_id"],
        "pipeline_stage": PIPELINE_CONTRACT["pipeline_stage"],
        "promotion_role": PIPELINE_CONTRACT["promotion_role"],
        "canonical_status": "intermediate",
        "title": title,
        "source_ordered_facts": str(args.ordered_facts),
        "stage_rule_set": stage_rule_set,
        "confidence": confidence,
        "score": score,
        "stage_order": stage_order,
        "required_stage_ids": required_stage_ids,
        "optional_stage_ids": optional_stage_ids,
        "missing_stages": missing_stages,
        "missing_required_stages": missing_required_stages,
        "facts_total": len(facts),
        "stages_total": len(stages),
        "present_stages_total": len(present_stage_ids),
        "source_files": source_files,
        "realms": realms,
        "stages": stages,
        "stage_edges": edges,
        "invalid_conflations": ordered.get("invalid_conflations", []),
        "reason": (
            "All required runtime stages are present."
            if not missing_required_stages
            else "One or more required runtime stages are missing."
        ),
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines: list[str] = []
    lines.append(f"# {title} Runtime Chain Candidate V7")
    lines.append("")
    lines.append(f"- Source ordered facts: `{args.ordered_facts}`")
    lines.append(f"- Rule set: `{rule_set_id}`")
    lines.append(f"- Confidence: `{confidence}`")
    lines.append(f"- Score: `{score}`")
    lines.append(f"- Facts total: `{len(facts)}`")
    lines.append(f"- Stages total: `{len(stages)}`")
    lines.append(f"- Present stages total: `{len(present_stage_ids)}`")
    lines.append(f"- Missing stages: `{missing_stages}`")
    lines.append(f"- Missing required stages: `{missing_required_stages}`")
    lines.append("")
    lines.append("## Stage Edges")
    lines.append("")

    for edge in edges:
        lines.append(
            f"- `{edge['from_stage']}` → `{edge['to_stage']}` "
            f"type=`{edge['type']}` support=`{edge['support']}`"
        )

    lines.append("")
    lines.append("## Stages")
    lines.append("")

    for index, stage in enumerate(stages, start=1):
        status = "present" if stage["present"] else "missing"
        lines.append(f"### {index}. `{stage['stage']}` — {status}")
        lines.append("")

        if stage["description"]:
            lines.append(str(stage["description"]))
            lines.append("")

        lines.append(f"- Supporting facts: `{stage['supporting_facts_count']}`")
        lines.append(f"- Realms: `{stage['realms']}`")
        lines.append(f"- Kinds: `{stage['kinds']}`")
        lines.append(f"- Categories: `{stage['categories']}`")
        lines.append(f"- Names: `{stage['names']}`")
        lines.append(f"- Source files: `{stage['source_files']}`")
        lines.append(f"- Lines: `{stage['lines']}`")
        lines.append("")

    lines.append("## Invalid Conflations")
    lines.append("")

    for conflation in ordered.get("invalid_conflations", []):
        if not isinstance(conflation, dict):
            continue

        lines.append(
            f"- `{conflation.get('left')}` must not be conflated with "
            f"`{conflation.get('right')}` — {conflation.get('reason', '')}"
        )

    args.out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Confidence: {confidence}")
    print(f"Score: {score}")
    print(f"Facts total: {len(facts)}")
    print(f"Stages total: {len(stages)}")
    print(f"Present stages total: {len(present_stage_ids)}")
    print(f"Missing stages: {missing_stages}")
    print(f"Missing required stages: {missing_required_stages}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")


if __name__ == "__main__":
    main()