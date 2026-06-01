from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


STAGE_ORDER = [
    "vendor_open_metadata_assignment",
    "vendor_purchase_transfer",
    "vendor_metadata_cleanup",
    "item_metadata_mutation",
    "item_metadata_network_send",
    "inventory_membership_client_apply",
    "item_metadata_client_apply",
    "ui_itemdata_refresh_hook",
]


STAGE_REASON = {
    "vendor_open_metadata_assignment": "Vendor inventory items receive presentation metadata before trade UI/use.",
    "vendor_purchase_transfer": "Vendor purchase transfers ownership/membership from vendor inventory to player inventory.",
    "vendor_metadata_cleanup": "After successful transfer, vendor sell metadata is cleared or adjusted on the item.",
    "item_metadata_mutation": "ITEM:setData mutates authoritative server-side item metadata.",
    "item_metadata_network_send": "ITEM:setData sends item metadata deltas through invData when receivers are available.",
    "inventory_membership_client_apply": "Client receives inventory membership addition through nutInventoryAdd.",
    "item_metadata_client_apply": "Client receives item metadata delta through invData and applies item.data[key].",
    "ui_itemdata_refresh_hook": "Client UI reacts to ItemDataChanged / InventoryItemDataChanged.",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def stage_rank(stage: str) -> int:
    try:
        return STAGE_ORDER.index(stage)
    except ValueError:
        return 999


def line_number(fact: dict[str, Any]) -> int:
    value = fact.get("line")
    try:
        return int(value)
    except (TypeError, ValueError):
        return 999999


def source_file(fact: dict[str, Any]) -> str:
    return str(fact.get("source_file") or fact.get("file") or "")


def fact_sort_key(fact: dict[str, Any]) -> tuple[int, str, int, str]:
    return (
        stage_rank(str(fact.get("stage", ""))),
        source_file(fact),
        line_number(fact),
        str(fact.get("id", "")),
    )


def build_stage_groups(facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups = []

    for stage in STAGE_ORDER:
        stage_facts = [
            fact for fact in facts
            if fact.get("stage") == stage
        ]
        stage_facts = sorted(stage_facts, key=fact_sort_key)

        if not stage_facts:
            groups.append({
                "stage": stage,
                "present": False,
                "reason": STAGE_REASON.get(stage, ""),
                "facts": [],
            })
            continue

        groups.append({
            "stage": stage,
            "present": True,
            "reason": STAGE_REASON.get(stage, ""),
            "facts": stage_facts,
        })

    unknown_facts = [
        fact for fact in facts
        if fact.get("stage") not in STAGE_ORDER
    ]

    if unknown_facts:
        groups.append({
            "stage": "unknown_or_unordered",
            "present": True,
            "reason": "Facts with stages not known to this sequencer.",
            "facts": sorted(unknown_facts, key=fact_sort_key),
        })

    return groups


def build_edges(groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    present_stages = [
        group["stage"]
        for group in groups
        if group["present"] and group["stage"] in STAGE_ORDER
    ]

    edges = []

    for before, after in zip(present_stages, present_stages[1:]):
        edges.append({
            "from_stage": before,
            "to_stage": after,
            "type": "stage_precedence",
            "support": "deterministic_vendor_itemdata_stage_order",
        })

    return edges


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Order runtime facts into deterministic vendor itemdata stage sequence."
    )
    parser.add_argument("--runtime-facts", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    data = load_json(args.runtime_facts)
    facts = data.get("facts", [])

    if not isinstance(facts, list):
        raise ValueError("runtime facts JSON must contain a list field named 'facts'")

    facts = [fact for fact in facts if isinstance(fact, dict)]

    groups = build_stage_groups(facts)
    edges = build_edges(groups)

    missing_stages = [
        group["stage"]
        for group in groups
        if group["stage"] in STAGE_ORDER and not group["present"]
    ]

    ordered_facts = []
    sequence_index = 0

    for group in groups:
        if group["stage"] not in STAGE_ORDER:
            continue

        for fact in group["facts"]:
            new_fact = dict(fact)
            new_fact["sequence_index"] = sequence_index
            new_fact["stage_rank"] = stage_rank(str(fact.get("stage", "")))
            new_fact["stage_reason"] = STAGE_REASON.get(str(fact.get("stage", "")), "")
            ordered_facts.append(new_fact)
            sequence_index += 1

    result = {
        "schema": "ordered_runtime_facts.v1",
        "source_runtime_facts": str(args.runtime_facts),
        "facts_total": len(facts),
        "ordered_facts_total": len(ordered_facts),
        "stages_total": len(STAGE_ORDER),
        "missing_stages": missing_stages,
        "stage_order": STAGE_ORDER,
        "stage_groups": groups,
        "stage_edges": edges,
        "ordered_facts": ordered_facts,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "# Runtime Fact Sequencing",
        "",
        f"- Runtime facts: `{args.runtime_facts}`",
        f"- Facts total: `{len(facts)}`",
        f"- Ordered facts total: `{len(ordered_facts)}`",
        f"- Stages total: `{len(STAGE_ORDER)}`",
        f"- Missing stages: `{missing_stages}`",
        "",
        "## Stage Sequence",
        "",
    ]

    for idx, group in enumerate(groups):
        if group["stage"] not in STAGE_ORDER:
            continue

        status = "present" if group["present"] else "missing"
        lines.append(f"### {idx + 1}. `{group['stage']}` — {status}")
        lines.append("")
        lines.append(group["reason"])
        lines.append("")

        for fact in group["facts"]:
            lines.append(
                f"- `{fact.get('id')}` "
                f"kind=`{fact.get('kind')}` "
                f"realm=`{fact.get('realm')}` "
                f"file=`{fact.get('source_file')}` "
                f"line=`{fact.get('line')}`"
            )

        lines.append("")

    lines.append("## Stage Edges")
    lines.append("")

    for edge in edges:
        lines.append(
            f"- `{edge['from_stage']}` → `{edge['to_stage']}` "
            f"type=`{edge['type']}` support=`{edge['support']}`"
        )

    args.out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Facts total: {len(facts)}")
    print(f"Ordered facts total: {len(ordered_facts)}")
    print(f"Missing stages: {missing_stages}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")


if __name__ == "__main__":
    main()