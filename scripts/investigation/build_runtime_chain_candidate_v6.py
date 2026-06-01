from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_STAGE_ORDER = [
    "vendor_open_metadata_assignment",
    "vendor_purchase_transfer",
    "vendor_metadata_cleanup",
    "item_metadata_mutation",
    "item_metadata_network_send",
    "inventory_membership_client_apply",
    "item_metadata_client_apply",
    "ui_itemdata_refresh_hook",
]


STAGE_DESCRIPTIONS = {
    "vendor_open_metadata_assignment": "Vendor items receive price-label presentation metadata before/while vendor trade UI is built.",
    "vendor_purchase_transfer": "Vendor purchase moves item ownership/membership from vendor inventory to player inventory.",
    "vendor_metadata_cleanup": "Vendor sell/buy metadata is cleared or adjusted after successful transfer.",
    "item_metadata_mutation": "ITEM:setData mutates authoritative item metadata server-side.",
    "item_metadata_network_send": "Server sends item metadata delta through invData when receivers are available.",
    "inventory_membership_client_apply": "Client applies inventory membership addition through nutInventoryAdd.",
    "item_metadata_client_apply": "Client applies item metadata delta through invData and emits ItemDataChanged.",
    "ui_itemdata_refresh_hook": "Client UI reacts to ItemDataChanged / InventoryItemDataChanged.",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def unique_sorted(values: list[Any]) -> list[str]:
    return sorted({str(v) for v in values if v is not None})


def build_stage(stage_name: str, facts: list[dict[str, Any]]) -> dict[str, Any]:
    stage_facts = [
        fact for fact in facts
        if fact.get("stage") == stage_name
    ]

    return {
        "stage": stage_name,
        "description": STAGE_DESCRIPTIONS.get(stage_name, ""),
        "present": bool(stage_facts),
        "supporting_fact_ids": [
            str(fact.get("id"))
            for fact in stage_facts
            if fact.get("id") is not None
        ],
        "supporting_facts_count": len(stage_facts),
        "realms": unique_sorted([fact.get("realm") for fact in stage_facts]),
        "kinds": unique_sorted([fact.get("kind") for fact in stage_facts]),
        "source_files": unique_sorted([
            fact.get("source_file") or fact.get("file")
            for fact in stage_facts
        ]),
        "lines": unique_sorted([fact.get("line") for fact in stage_facts]),
    }


def build_edges(stages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    present_stages = [
        stage["stage"]
        for stage in stages
        if stage["present"]
    ]

    edges = []

    for from_stage, to_stage in zip(present_stages, present_stages[1:]):
        edges.append({
            "from_stage": from_stage,
            "to_stage": to_stage,
            "type": "runtime_stage_precedence",
            "support": "ordered_runtime_facts_v1",
        })

    return edges


def confidence_and_score(missing_required_stages: list[str]) -> tuple[str, float]:
    total = len(REQUIRED_STAGE_ORDER)
    missing = len(missing_required_stages)

    score = round((total - missing) / total, 4)

    if missing == 0:
        return "high", score
    if missing == 1:
        return "medium", score
    return "low", score


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build runtime chain candidate V6 from ordered runtime facts."
    )
    parser.add_argument("--ordered-facts", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    ordered = load_json(args.ordered_facts)

    facts = ordered.get("ordered_facts")
    if not isinstance(facts, list):
        raise ValueError("ordered facts JSON must contain list field: ordered_facts")

    facts = [fact for fact in facts if isinstance(fact, dict)]

    stages = [
        build_stage(stage_name, facts)
        for stage_name in REQUIRED_STAGE_ORDER
    ]

    missing_required_stages = [
        stage["stage"]
        for stage in stages
        if not stage["present"]
    ]

    confidence, score = confidence_and_score(missing_required_stages)
    edges = build_edges(stages)

    all_source_files = unique_sorted([
        source_file
        for stage in stages
        for source_file in stage["source_files"]
    ])

    all_realms = unique_sorted([
        realm
        for stage in stages
        for realm in stage["realms"]
    ])

    result = {
        "schema": "runtime_chain_candidate.v6",
        "title": "vendor purchase itemdata propagation chain",
        "source_ordered_facts": str(args.ordered_facts),
        "confidence": confidence,
        "score": score,
        "required_stage_order": REQUIRED_STAGE_ORDER,
        "missing_required_stages": missing_required_stages,
        "stages_total": len(stages),
        "present_stages_total": len(stages) - len(missing_required_stages),
        "supporting_facts_total": len(facts),
        "realms": all_realms,
        "source_files": all_source_files,
        "stages": stages,
        "stage_edges": edges,
        "conclusion": (
            "Full vendor itemdata propagation chain recovered."
            if confidence == "high"
            else "Vendor itemdata propagation chain remains incomplete."
        ),
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines: list[str] = [
        "# Vendor Purchase Itemdata Runtime Chain Candidate V6",
        "",
        f"- Source ordered facts: `{args.ordered_facts}`",
        f"- Confidence: `{confidence}`",
        f"- Score: `{score}`",
        f"- Supporting facts total: `{len(facts)}`",
        f"- Stages total: `{len(stages)}`",
        f"- Present stages total: `{len(stages) - len(missing_required_stages)}`",
        f"- Missing required stages: `{missing_required_stages}`",
        "",
        "## Runtime Chain",
        "",
    ]

    for edge in edges:
        lines.append(f"- `{edge['from_stage']}` → `{edge['to_stage']}`")

    lines.extend(["", "## Stages", ""])

    for index, stage in enumerate(stages, start=1):
        status = "present" if stage["present"] else "missing"

        lines.extend([
            f"### {index}. `{stage['stage']}` — {status}",
            "",
            stage["description"],
            "",
            f"- Supporting facts: `{stage['supporting_facts_count']}`",
            f"- Realms: `{stage['realms']}`",
            f"- Kinds: `{stage['kinds']}`",
            f"- Source files: `{stage['source_files']}`",
            f"- Lines: `{stage['lines']}`",
            "",
        ])

    lines.extend([
        "## Conclusion",
        "",
        result["conclusion"],
    ])

    args.out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Confidence: {confidence}")
    print(f"Score: {score}")
    print(f"Supporting facts: {len(facts)}")
    print(f"Missing required stages: {missing_required_stages}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")


if __name__ == "__main__":
    main()