from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections import defaultdict


EXPECTED_VENDOR_STAGES = {
    "vendor_inventory_remove": [
        "remove", "oldInventory", "vendor inventory", "vendorSellItem"
    ],
    "player_inventory_add": [
        "add", "player inventory", "character inventory", "inventory:add"
    ],
    "item_sync": [
        "sync", "item:sync", "nutInventoryAdd"
    ],
    "vendor_metadata_cleanup": [
        "vendorQty", "vendorSPrice", "vendorMQty", "vendorBPrice"
    ],
    "item_metadata_mutation": [
        "setData", "ITEM:setData", "item:setData"
    ],
    "item_metadata_network_send": [
        "invData", "netstream.Start"
    ],
    "item_metadata_client_apply": [
        "invData", "ItemDataChanged"
    ],
    "ui_refresh": [
        "populateItems", "grid", "refresh", "inventory panel"
    ],
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def flatten_fact_text(fact: dict) -> str:
    parts = []

    def walk(value):
        if isinstance(value, dict):
            for v in value.values():
                walk(v)
        elif isinstance(value, list):
            for v in value:
                walk(v)
        elif value is not None:
            parts.append(str(value))

    walk(fact)
    return " ".join(parts)


def get_facts(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("facts", "runtime_facts", "nodes"):
            if key in data and isinstance(data[key], list):
                return data[key]
    raise ValueError("Could not find facts list in JSON")


def main():
    parser = argparse.ArgumentParser(
        description="Diagnose missing vendor runtime facts/stages."
    )
    parser.add_argument("--facts", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    args = parser.parse_args()

    data = load_json(args.facts)
    facts = get_facts(data)

    stage_hits = defaultdict(list)
    fact_rows = []

    for i, fact in enumerate(facts):
        text = flatten_fact_text(fact)
        text_lower = text.lower()

        name = (
            fact.get("name")
            or fact.get("label")
            or fact.get("id")
            or fact.get("key")
            or f"fact_{i}"
        )

        category = fact.get("category")
        kind = fact.get("kind")
        realms = fact.get("realms")

        matched_stages = []

        for stage, needles in EXPECTED_VENDOR_STAGES.items():
            hits = [
                needle
                for needle in needles
                if needle.lower() in text_lower
            ]

            if hits:
                matched_stages.append(stage)
                stage_hits[stage].append({
                    "fact_index": i,
                    "fact_name": name,
                    "hits": hits,
                })

        fact_rows.append({
            "index": i,
            "name": name,
            "category": category,
            "kind": kind,
            "realms": realms,
            "matched_stages": matched_stages,
        })

    missing_stages = [
        stage for stage in EXPECTED_VENDOR_STAGES
        if stage not in stage_hits
    ]

    present_stages = [
        stage for stage in EXPECTED_VENDOR_STAGES
        if stage in stage_hits
    ]

    if len(facts) <= 5 and missing_stages:
        likely_failure = "runtime_fact_generation_too_narrow"
    elif missing_stages and "item_metadata_client_apply" in present_stages:
        likely_failure = "runtime_fact_generation_or_filtering_missing_server_side_stages"
    elif not missing_stages:
        likely_failure = "stage_selection_or_ordering"
    else:
        likely_failure = "unknown_requires_source_fact_trace"

    result = {
        "facts_total": len(facts),
        "present_stages": present_stages,
        "missing_stages": missing_stages,
        "likely_failure": likely_failure,
        "stage_hits": dict(stage_hits),
        "facts": fact_rows,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = []
    lines.append("# Runtime Fact Generation Diagnosis")
    lines.append("")
    lines.append(f"- Facts total: `{len(facts)}`")
    lines.append(f"- Present stages: `{len(present_stages)}`")
    lines.append(f"- Missing stages: `{len(missing_stages)}`")
    lines.append(f"- Likely failure: `{likely_failure}`")
    lines.append("")
    lines.append("## Present Stages")
    lines.append("")
    for stage in present_stages:
        lines.append(f"### `{stage}`")
        for hit in stage_hits[stage]:
            lines.append(
                f"- Fact `{hit['fact_index']}` / `{hit['fact_name']}` "
                f"matched `{', '.join(hit['hits'])}`"
            )
        lines.append("")
    lines.append("## Missing Stages")
    lines.append("")
    for stage in missing_stages:
        lines.append(f"- `{stage}`")
    lines.append("")
    lines.append("## Fact Inventory")
    lines.append("")
    for row in fact_rows:
        lines.append(
            f"- `{row['index']}` `{row['name']}` "
            f"category=`{row['category']}` kind=`{row['kind']}` "
            f"realms=`{row['realms']}` stages=`{row['matched_stages']}`"
        )

    args.out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Facts total: {len(facts)}")
    print(f"Present stages: {len(present_stages)}")
    print(f"Missing stages: {len(missing_stages)}")
    print(f"Likely failure: {likely_failure}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")


if __name__ == "__main__":
    main()