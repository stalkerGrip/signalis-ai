from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PIPELINE_CONTRACT = {
    "script_id": "scripts.investigation.runtime_fact_sequencer",
    "purpose": "Classify and order neutral runtime_facts.v2 using an external stage_rule_set.v1 artifact.",
    "pipeline_stage": "ordered_runtime_facts",
    "input_schemas": [
        "runtime_facts.v2",
        "stage_rule_set.v1",
    ],
    "output_schemas": [
        "ordered_runtime_facts.v1",
    ],
    "artifact_patterns": [
        "investigations/validation/*_ordered_runtime_facts_v1.json",
        "investigations/validation/*_ordered_runtime_facts_v1.md",
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


def flatten(value: Any) -> str:
    parts: list[str] = []

    def walk(v: Any) -> None:
        if isinstance(v, dict):
            for vv in v.values():
                walk(vv)
        elif isinstance(v, list):
            for vv in v:
                walk(vv)
        elif v is not None:
            parts.append(str(v))

    walk(value)
    return " ".join(parts)


def first_occurrence(fact: dict[str, Any]) -> dict[str, Any]:
    occurrences = fact.get("occurrences")
    if isinstance(occurrences, list) and occurrences and isinstance(occurrences[0], dict):
        return occurrences[0]
    return {}


def fact_line(fact: dict[str, Any]) -> int:
    value = fact.get("line") or first_occurrence(fact).get("line")
    try:
        return int(value)
    except (TypeError, ValueError):
        return 999999


def fact_file(fact: dict[str, Any]) -> str:
    occurrence = first_occurrence(fact)
    return str(
        fact.get("source_file")
        or fact.get("file")
        or occurrence.get("file")
        or ""
    )


def fact_realm(fact: dict[str, Any]) -> str:
    occurrence = first_occurrence(fact)
    return str(fact.get("realm") or occurrence.get("realm") or "unknown")


def fact_id(fact: dict[str, Any], index: int) -> str:
    return str(fact.get("id") or fact.get("fact_key") or f"runtime_fact:{index}")


def fact_text(fact: dict[str, Any]) -> str:
    return flatten(fact).lower()


def stage_rank(stage: str, stage_order: list[str]) -> int:
    try:
        return stage_order.index(stage)
    except ValueError:
        return 999


def fact_sort_key(fact: dict[str, Any], stage_order: list[str]) -> tuple[int, str, int, str]:
    return (
        stage_rank(str(fact.get("stage", "")), stage_order),
        fact_file(fact),
        fact_line(fact),
        str(fact.get("id") or fact.get("fact_key") or ""),
    )


def validate_rule_set(rule_set: dict[str, Any], path: Path) -> None:
    require_schema(rule_set, "stage_rule_set.v1", path)

    stage_order = rule_set.get("stage_order")
    if not isinstance(stage_order, list) or not all(isinstance(item, str) for item in stage_order):
        raise ValueError(f"{path}: stage_order must be a list of strings")

    if not stage_order:
        raise ValueError(f"{path}: stage_order must not be empty")

    for key in ("required_stage_ids", "optional_stage_ids"):
        value = rule_set.get(key, [])
        if not isinstance(value, list):
            raise ValueError(f"{path}: {key} must be a list")

    known = set(stage_order)

    unknown_required = [
        stage for stage in rule_set.get("required_stage_ids", [])
        if stage not in known
    ]
    unknown_optional = [
        stage for stage in rule_set.get("optional_stage_ids", [])
        if stage not in known
    ]

    if unknown_required:
        raise ValueError(f"{path}: required_stage_ids not in stage_order: {unknown_required}")

    if unknown_optional:
        raise ValueError(f"{path}: optional_stage_ids not in stage_order: {unknown_optional}")


def stage_rule_entries(rule_set: dict[str, Any]) -> list[dict[str, Any]]:
    stages = rule_set.get("stages")
    if isinstance(stages, list):
        return [stage for stage in stages if isinstance(stage, dict)]

    entries = []
    for stage_id in rule_set.get("stage_order", []):
        entries.append({
            "stage_id": stage_id,
            "description": "",
            "match": {},
        })
    return entries


def stage_reason_map(rule_set: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}

    for stage in stage_rule_entries(rule_set):
        stage_id = stage.get("stage_id")
        if not stage_id:
            continue

        result[str(stage_id)] = str(stage.get("description") or stage.get("reason") or "")

    return result


def list_value(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value if v is not None]
    if value is None:
        return []
    return [str(value)]


def match_any_text(text: str, needles: list[str]) -> tuple[bool, list[str]]:
    if not needles:
        return True, []

    matched = [needle for needle in needles if needle.lower() in text]
    return bool(matched), matched


def match_any_file(path: str, patterns: list[str]) -> tuple[bool, list[str]]:
    if not patterns:
        return True, []

    normalized_path = path.replace("\\", "/").lower()
    matched = [
        pattern for pattern in patterns
        if pattern.replace("\\", "/").lower() in normalized_path
    ]
    return bool(matched), matched


def match_expected_kinds(fact: dict[str, Any], expected_kinds: list[str]) -> tuple[bool, list[str]]:
    if not expected_kinds:
        return True, []

    kind = str(fact.get("kind") or "").lower()
    category = str(fact.get("category") or "").lower()
    text = fact_text(fact)

    matched = [
        expected for expected in expected_kinds
        if expected.lower() == kind
        or expected.lower() == category
        or expected.lower() in text
    ]

    return bool(matched), matched


def match_expected_realm(fact: dict[str, Any], expected_realm: str | None) -> bool:
    if not expected_realm:
        return True

    actual = fact_realm(fact).lower()
    expected = expected_realm.lower()

    if actual == "unknown":
        return True

    return actual == expected


def classify_fact(
    fact: dict[str, Any],
    index: int,
    rule_set: dict[str, Any],
    stage_order: list[str],
) -> list[dict[str, Any]]:
    existing_stage = fact.get("stage")
    if isinstance(existing_stage, str) and existing_stage in stage_order:
        copied = dict(fact)
        copied["id"] = fact_id(copied, index)
        copied["stage"] = existing_stage
        copied["stage_match"] = {
            "source": "existing_fact_stage",
            "matched_needles": [],
            "matched_files": [],
            "matched_kinds": [],
        }
        return [copied]

    classified: list[dict[str, Any]] = []
    text = fact_text(fact)
    path = fact_file(fact)

    for stage in stage_rule_entries(rule_set):
        stage_id = stage.get("stage_id")
        if not isinstance(stage_id, str) or stage_id not in stage_order:
            continue

        match = stage.get("match")
        if not isinstance(match, dict):
            match = {}

        any_needles = list_value(match.get("any_needles"))
        any_files = list_value(match.get("any_files"))
        expected_kinds = list_value(stage.get("expected_kinds") or match.get("expected_kinds"))
        expected_realm = stage.get("expected_realm") or match.get("expected_realm")

        has_match_criteria = (
            bool(any_needles)
            or bool(any_files)
            or bool(expected_kinds)
            or bool(expected_realm)
        )

        if not has_match_criteria:
            continue

        text_ok, matched_needles = match_any_text(text, any_needles)
        file_ok, matched_files = match_any_file(path, any_files)
        kind_ok, matched_kinds = match_expected_kinds(fact, expected_kinds)
        realm_ok = match_expected_realm(fact, str(expected_realm) if expected_realm else None)

        if text_ok and file_ok and kind_ok and realm_ok:
            copied = dict(fact)
            copied["id"] = fact_id(copied, index)
            copied["stage"] = stage_id
            copied["source_file"] = fact_file(copied)
            copied["line"] = first_occurrence(copied).get("line") or copied.get("line")
            copied["realm"] = fact_realm(copied)
            copied["stage_match"] = {
                "source": "stage_rule_set",
                "matched_needles": matched_needles,
                "matched_files": matched_files,
                "matched_kinds": matched_kinds,
            }
            classified.append(copied)

    return classified


def classify_facts(
    facts: list[dict[str, Any]],
    rule_set: dict[str, Any],
    stage_order: list[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    staged: list[dict[str, Any]] = []
    unmatched: list[dict[str, Any]] = []

    for index, fact in enumerate(facts):
        matches = classify_fact(fact, index, rule_set, stage_order)
        if matches:
            staged.extend(matches)
        else:
            copied = dict(fact)
            copied["id"] = fact_id(copied, index)
            unmatched.append(copied)

    return staged, unmatched


def build_stage_groups(
    staged_facts: list[dict[str, Any]],
    unmatched_facts: list[dict[str, Any]],
    stage_order: list[str],
    reasons: dict[str, str],
) -> list[dict[str, Any]]:
    groups = []

    for stage in stage_order:
        stage_facts = [fact for fact in staged_facts if fact.get("stage") == stage]
        stage_facts = sorted(stage_facts, key=lambda fact: fact_sort_key(fact, stage_order))

        groups.append({
            "stage": stage,
            "present": bool(stage_facts),
            "reason": reasons.get(stage, ""),
            "facts": stage_facts,
        })

    if unmatched_facts:
        groups.append({
            "stage": "unknown_or_unordered",
            "present": True,
            "reason": "Facts not matched by this stage_rule_set.",
            "facts": sorted(unmatched_facts, key=lambda fact: fact_sort_key(fact, stage_order)),
        })

    return groups


def build_edges(groups: list[dict[str, Any]], stage_order: list[str], rule_set_id: str) -> list[dict[str, Any]]:
    present_stages = [
        group["stage"]
        for group in groups
        if group["present"] and group["stage"] in stage_order
    ]

    edges = []

    for before, after in zip(present_stages, present_stages[1:]):
        edges.append({
            "from_stage": before,
            "to_stage": after,
            "type": "stage_precedence",
            "support": f"stage_rule_set:{rule_set_id}",
        })

    return edges


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Classify and order runtime facts using an external stage_rule_set.v1 artifact."
    )
    parser.add_argument("--runtime-facts", required=True, type=Path)
    parser.add_argument("--stage-rules", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    data = load_json(args.runtime_facts)
    rule_set = load_json(args.stage_rules)

    require_schema(data, "runtime_facts.v2", args.runtime_facts)
    validate_rule_set(rule_set, args.stage_rules)

    facts = data.get("facts", [])
    if not isinstance(facts, list):
        raise ValueError("runtime facts JSON must contain a list field named 'facts'")

    facts = [fact for fact in facts if isinstance(fact, dict)]

    stage_order = [str(stage) for stage in rule_set["stage_order"]]
    required_stage_ids = [str(stage) for stage in rule_set.get("required_stage_ids", [])]
    optional_stage_ids = [str(stage) for stage in rule_set.get("optional_stage_ids", [])]
    rule_set_id = str(rule_set.get("rule_set_id") or args.stage_rules.stem)
    reasons = stage_reason_map(rule_set)

    staged_facts, unmatched_facts = classify_facts(facts, rule_set, stage_order)
    groups = build_stage_groups(staged_facts, unmatched_facts, stage_order, reasons)
    edges = build_edges(groups, stage_order, rule_set_id)

    present_stage_ids = {
        group["stage"]
        for group in groups
        if group["present"] and group["stage"] in stage_order
    }

    missing_stages = [
        stage for stage in stage_order
        if stage not in present_stage_ids
    ]

    missing_required_stages = [
        stage for stage in required_stage_ids
        if stage not in present_stage_ids
    ]

    ordered_facts = []
    sequence_index = 0

    for group in groups:
        if group["stage"] not in stage_order:
            continue

        for fact in group["facts"]:
            stage = str(fact.get("stage", ""))
            new_fact = dict(fact)
            new_fact["sequence_index"] = sequence_index
            new_fact["stage_rank"] = stage_rank(stage, stage_order)
            new_fact["stage_reason"] = reasons.get(stage, "")
            new_fact["stage_rule_set"] = rule_set_id
            ordered_facts.append(new_fact)
            sequence_index += 1

    result = {
        "schema": "ordered_runtime_facts.v1",
        "producer_script": PIPELINE_CONTRACT["script_id"],
        "pipeline_stage": PIPELINE_CONTRACT["pipeline_stage"],
        "promotion_role": PIPELINE_CONTRACT["promotion_role"],
        "canonical_status": "intermediate",
        "source_runtime_facts": str(args.runtime_facts),
        "stage_rule_set": {
            "path": str(args.stage_rules),
            "rule_set_id": rule_set_id,
            "title": rule_set.get("title", ""),
            "version": rule_set.get("version"),
            "promotion_compatible": bool(rule_set.get("promotion_compatible", False)),
        },
        "facts_total": len(facts),
        "staged_facts_total": len(staged_facts),
        "unmatched_facts_total": len(unmatched_facts),
        "ordered_facts_total": len(ordered_facts),
        "stages_total": len(stage_order),
        "missing_stages": missing_stages,
        "missing_required_stages": missing_required_stages,
        "required_stage_ids": required_stage_ids,
        "optional_stage_ids": optional_stage_ids,
        "stage_order": stage_order,
        "stage_groups": groups,
        "stage_edges": edges,
        "ordered_facts": ordered_facts,
        "unmatched_facts": unmatched_facts,
        "invalid_conflations": rule_set.get("invalid_conflations", []),
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines: list[str] = []
    lines.append("# Runtime Fact Sequencing")
    lines.append("")
    lines.append(f"- Runtime facts: `{args.runtime_facts}`")
    lines.append(f"- Stage rules: `{args.stage_rules}`")
    lines.append(f"- Rule set: `{rule_set_id}`")
    lines.append(f"- Facts total: `{len(facts)}`")
    lines.append(f"- Staged facts total: `{len(staged_facts)}`")
    lines.append(f"- Unmatched facts total: `{len(unmatched_facts)}`")
    lines.append(f"- Ordered facts total: `{len(ordered_facts)}`")
    lines.append(f"- Stages total: `{len(stage_order)}`")
    lines.append(f"- Missing stages: `{missing_stages}`")
    lines.append(f"- Missing required stages: `{missing_required_stages}`")
    lines.append("")
    lines.append("## Stage Sequence")
    lines.append("")

    for idx, group in enumerate(groups):
        if group["stage"] not in stage_order:
            continue

        status = "present" if group["present"] else "missing"
        lines.append(f"### {idx + 1}. `{group['stage']}` — {status}")
        lines.append("")

        if group["reason"]:
            lines.append(group["reason"])
            lines.append("")

        for fact in group["facts"]:
            lines.append(
                f"- `{fact.get('id')}` "
                f"kind=`{fact.get('kind')}` "
                f"category=`{fact.get('category')}` "
                f"name=`{fact.get('name')}` "
                f"realm=`{fact_realm(fact)}` "
                f"file=`{fact_file(fact)}` "
                f"line=`{fact_line(fact)}`"
            )

        lines.append("")

    lines.append("## Stage Edges")
    lines.append("")

    for edge in edges:
        lines.append(
            f"- `{edge['from_stage']}` → `{edge['to_stage']}` "
            f"type=`{edge['type']}` support=`{edge['support']}`"
        )

    lines.append("")
    lines.append("## Unmatched Facts")
    lines.append("")

    for fact in unmatched_facts:
        lines.append(
            f"- `{fact.get('id')}` "
            f"kind=`{fact.get('kind')}` "
            f"category=`{fact.get('category')}` "
            f"name=`{fact.get('name')}` "
            f"realm=`{fact_realm(fact)}` "
            f"file=`{fact_file(fact)}` "
            f"line=`{fact_line(fact)}`"
        )

    lines.append("")
    lines.append("## Invalid Conflations")
    lines.append("")

    for conflation in rule_set.get("invalid_conflations", []):
        if not isinstance(conflation, dict):
            continue

        lines.append(
            f"- `{conflation.get('left')}` must not be conflated with "
            f"`{conflation.get('right')}` — {conflation.get('reason', '')}"
        )

    args.out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Facts total: {len(facts)}")
    print(f"Staged facts total: {len(staged_facts)}")
    print(f"Unmatched facts total: {len(unmatched_facts)}")
    print(f"Ordered facts total: {len(ordered_facts)}")
    print(f"Missing stages: {missing_stages}")
    print(f"Missing required stages: {missing_required_stages}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")


if __name__ == "__main__":
    main()