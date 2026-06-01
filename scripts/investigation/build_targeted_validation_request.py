from __future__ import annotations

import argparse
import json
from pathlib import Path


FULL_CHAIN_TARGETS_BY_CHAIN_KEY = {
    "vendor_itemdata": [
        {
            "path": "plugins/gridinv/sv_transfer.lua",
            "needles": [
                "vendorSellItem",
                "oldInventory.vendor",
                "oldInventory:remove",
                "inventory:add",
                "item:setData(\"vendorQty\", nil, client)",
                "item:setData(\"vendorSPrice\", nil, client)",
                "item:setData(\"vendorMQty\", nil, client)",
                "item:setData(\"vendorBPrice\"",
                "syncItemAdded",
            ],
            "reason": "Validate vendor purchase transfer, ownership move, and vendor metadata cleanup.",
        },
        {
            "path": "gamemode/core/meta/item/sv_item.lua",
            "needles": [
                "function ITEM:setData",
                "netstream.Start",
                "\"invData\"",
                "noSave",
            ],
            "reason": "Validate ITEM:setData server mutation, persistence, and invData sync boundary.",
        },
        {
            "path": "gamemode/core/meta/inventory/cl_base_inventory.lua",
            "needles": [
                "net.Receive",
                "\"nutInventoryAdd\"",
                "nut.item.new",
                "item.invID",
            ],
            "reason": "Validate client inventory membership add path.",
        },
        {
            "path": "gamemode/core/libs/item/cl_networking.lua",
            "needles": [
                "netstream.Hook",
                "\"invData\"",
                "item.data[key]",
                "hook.Run(\"ItemDataChanged\"",
            ],
            "reason": "Validate client item metadata apply path.",
        },
        {
            "path": "plugins/inventory/sh_plugin.lua",
            "needles": [
                "vendorSPrice",
                "vendorBPrice",
                "v:setData(\"vendorSPrice\"",
                "v:setData(\"vendorBPrice\"",
            ],
            "reason": "Validate vendor open metadata assignment for vendor price labels.",
        },
        {
            "path": "plugins/inventory/derma/cl_extended_grid_inventory.lua",
            "needles": [
                "InventoryItemDataChanged",
                "ItemDataChanged",
            ],
            "reason": "Validate grid inventory reacts to item metadata changes.",
        },
    ]
}


TARGETS_BY_MISSING_STEP = {
    "purchase_transfer": FULL_CHAIN_TARGETS_BY_CHAIN_KEY["vendor_itemdata"],
    "vendor_inventory_remove": FULL_CHAIN_TARGETS_BY_CHAIN_KEY["vendor_itemdata"],
    "player_inventory_add": FULL_CHAIN_TARGETS_BY_CHAIN_KEY["vendor_itemdata"],
    "item_sync": FULL_CHAIN_TARGETS_BY_CHAIN_KEY["vendor_itemdata"],
    "vendor_metadata_cleanup": FULL_CHAIN_TARGETS_BY_CHAIN_KEY["vendor_itemdata"],
    "item_metadata_mutation": FULL_CHAIN_TARGETS_BY_CHAIN_KEY["vendor_itemdata"],
    "item_metadata_client_apply": FULL_CHAIN_TARGETS_BY_CHAIN_KEY["vendor_itemdata"],
    "ui_refresh": FULL_CHAIN_TARGETS_BY_CHAIN_KEY["vendor_itemdata"],
}


def infer_chain_key(candidate: dict) -> str | None:
    text = " ".join(
        str(candidate.get(k, ""))
        for k in ("question", "chain_name", "title", "name")
    ).lower()

    if "vendor" in text and ("itemdata" in text or "item data" in text or "metadata" in text):
        return "vendor_itemdata"

    return None


def dedupe_targets(targets: list[dict]) -> list[dict]:
    seen = set()
    result = []

    for target in targets:
        key = target.get("path")
        if key in seen:
            continue
        seen.add(key)
        result.append(target)

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    missing_steps = candidate.get("missing_steps", [])
    chain_key = infer_chain_key(candidate)

    targets = []

    if chain_key:
        targets.extend(FULL_CHAIN_TARGETS_BY_CHAIN_KEY[chain_key])

    for step in missing_steps:
        targets.extend(TARGETS_BY_MISSING_STEP.get(step, []))

    targets = dedupe_targets(targets)

    request = {
        "schema": "targeted_validation_request.v2",
        "source_candidate": str(args.candidate),
        "question": candidate.get("question", ""),
        "chain_name": candidate.get("chain_name", candidate.get("title", "")),
        "chain_key": chain_key,
        "missing_steps": missing_steps,
        "targets": targets,
        "promotion_blocked": bool(missing_steps),
        "notes": [
            "Validate full causal chain for known benchmark chains, not only missing downstream evidence.",
            "Vendor itemdata validation must include ownership transfer, item metadata mutation, metadata sync, client apply, and UI presentation.",
            "Do not conflate inventory membership sync with item metadata sync.",
        ],
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(request, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote targeted validation request: {args.out}")
    print(f"Chain key: {chain_key}")
    print(f"Targets: {len(targets)}")


if __name__ == "__main__":
    main()