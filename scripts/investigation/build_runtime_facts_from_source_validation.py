from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


STAGE_RULES = [
    {
        "stage": "vendor_open_metadata_assignment",
        "needles": ["vendorSPrice", "vendorBPrice", "v:setData"],
        "kind": "item_metadata_assignment",
        "realm": "server",
    },
    {
        "stage": "vendor_purchase_transfer",
        "needles": ["vendorSellItem", "oldInventory.vendor", "inventory:add"],
        "kind": "inventory_transfer",
        "realm": "server",
    },
    {
        "stage": "vendor_metadata_cleanup",
        "needles": ["vendorQty", "vendorSPrice", "vendorMQty", "vendorBPrice"],
        "kind": "item_metadata_cleanup",
        "realm": "server",
    },
    {
        "stage": "item_metadata_mutation",
        "needles": ["function ITEM:setData", "item:setData", "setData"],
        "kind": "state_mutation",
        "realm": "server",
    },
    {
        "stage": "item_metadata_network_send",
        "needles": ["netstream.Start", "invData"],
        "kind": "network_send",
        "realm": "server",
    },
    {
        "stage": "inventory_membership_client_apply",
        "needles": ["nutInventoryAdd", "inventory.items", "InventoryItemAdded"],
        "kind": "client_membership_apply",
        "realm": "client",
    },
    {
        "stage": "item_metadata_client_apply",
        "needles": ["netstream.Hook", "invData", "item.data[key]", "ItemDataChanged"],
        "kind": "client_metadata_apply",
        "realm": "client",
    },
    {
        "stage": "ui_itemdata_refresh_hook",
        "needles": ["InventoryItemDataChanged", "ItemDataChanged"],
        "kind": "ui_refresh_hook",
        "realm": "client",
    },
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_results(data: Any):
    results = data.get("results", []) if isinstance(data, dict) else []
    if isinstance(results, list):
        for result in results:
            if isinstance(result, dict):
                yield result


def get_file(result: dict) -> str:
    return str(
        result.get("file")
        or result.get("path")
        or result.get("source_file")
        or "unknown"
    )


def get_needles(result: dict) -> list[dict]:
    for key in ("needles", "checks", "matches"):
        value = result.get(key)
        if isinstance(value, list):
            return [v for v in value if isinstance(v, dict)]
    return []


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


def classify_fact(text: str) -> list[dict]:
    lowered = text.lower()
    hits = []

    for rule in STAGE_RULES:
        matched = [
            needle for needle in rule["needles"]
            if needle.lower() in lowered
        ]
        if matched:
            hits.append({
                "stage": rule["stage"],
                "kind": rule["kind"],
                "realm": rule["realm"],
                "matched_needles": matched,
            })

    return hits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-validation", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    data = load_json(args.source_validation)

    facts: list[dict] = []
    fact_id = 0

    for result in iter_results(data):
        file_path = get_file(result)

        for needle in get_needles(result):
            found = bool(needle.get("found") or needle.get("Found"))
            if not found:
                continue

            text = flatten(needle)
            classifications = classify_fact(text)

            for cls in classifications:
                fact = {
                    "id": f"runtime_fact:{fact_id}",
                    "source_file": file_path,
                    "stage": cls["stage"],
                    "kind": cls["kind"],
                    "realm": cls["realm"],
                    "matched_needles": cls["matched_needles"],
                    "line": needle.get("line") or needle.get("Line"),
                    "evidence": text,
                }
                facts.append(fact)
                fact_id += 1

    # Deduplicate by stage + file + line.
    seen = set()
    deduped = []
    for fact in facts:
        key = (fact["stage"], fact["source_file"], fact.get("line"))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(fact)

    stages = sorted({fact["stage"] for fact in deduped})

    output = {
        "schema": "runtime_facts.v2",
        "source_validation": str(args.source_validation),
        "facts_total": len(deduped),
        "stages_total": len(stages),
        "stages": stages,
        "facts": deduped,
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "# Runtime Facts From Source Validation",
        "",
        f"- Source validation: `{args.source_validation}`",
        f"- Facts total: `{len(deduped)}`",
        f"- Stages total: `{len(stages)}`",
        "",
        "## Stages",
        "",
    ]

    for stage in stages:
        lines.append(f"- `{stage}`")

    lines += ["", "## Facts", ""]

    for fact in deduped:
        lines.append(
            f"- `{fact['id']}` stage=`{fact['stage']}` "
            f"kind=`{fact['kind']}` realm=`{fact['realm']}` "
            f"file=`{fact['source_file']}` line=`{fact.get('line')}`"
        )

    args.out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Facts total: {len(deduped)}")
    print(f"Stages total: {len(stages)}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")


if __name__ == "__main__":
    main()