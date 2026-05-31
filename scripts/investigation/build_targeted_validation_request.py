from __future__ import annotations

import argparse
import json
from pathlib import Path


TARGETS_BY_MISSING_STEP = {
    "purchase_transfer": [
        {
            "path": "plugins/gridinv/sv_transfer.lua",
            "needles": [
                "vendorSellItem",
                "oldInventory.vendor",
                "item:setData(\"vendorQty\", nil, client)",
                "item:setData(\"vendorSPrice\", nil, client)",
                "item:setData(\"vendorMQty\", nil, client)",
                "item:setData(\"vendorBPrice\"",
                "inventory:add",
                "oldInventory:remove",
                "syncItemAdded",
            ],
            "reason": "Validate authoritative vendor purchase transfer and metadata cleanup path.",
        }
    ]
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    candidate = json.loads(args.candidate.read_text(encoding="utf-8"))
    missing_steps = candidate.get("missing_steps", [])

    targets = []
    for step in missing_steps:
        targets.extend(TARGETS_BY_MISSING_STEP.get(step, []))

    request = {
        "schema": "targeted_validation_request.v1",
        "source_candidate": str(args.candidate),
        "question": candidate.get("question", ""),
        "chain_name": candidate.get("chain_name", ""),
        "missing_steps": missing_steps,
        "targets": targets,
        "promotion_blocked": bool(missing_steps),
        "notes": [
            "Validate missing causal-chain steps only.",
            "Do not revalidate already-present downstream sync evidence unless target validation fails.",
            "If purchase_transfer is found, rerun synthesis and runtime_chain_candidate.",
        ],
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(request, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Wrote targeted validation request: {args.out}")
    print(f"Targets: {len(targets)}")


if __name__ == "__main__":
    main()