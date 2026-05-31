#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

REQUIRED_TARGETS = {
    "plugins/gridinv/sv_transfer.lua": {
        "semantic_role": "gridinv_transfer",
        "required_patterns": [
            "vendorSellItem",
            "oldInventory",
            "inventory:add",
            "item:setData(\"vendorSPrice\", nil",
            "item:setData(\"vendorQty\", nil",
            "item:setData(\"vendorMQty\", nil",
            "item:setData(\"vendorBPrice\"",
            "CanItemBeTransfered",
            "HandleItemTransferRequest",
        ],
        "validation_questions": [
            "Does gridinv transfer identify vendor to player purchase through vendorSellItem?",
            "Does the transfer cross oldInventory to player inventory boundary?",
            "Does the transfer add the item to player inventory before vendor metadata cleanup?",
            "Does the purchase cleanup clear vendorSPrice/vendorQty/vendorMQty on the purchased item?",
        ],
        "expected_runtime_relation": "vendor purchase transfer boundary and purchased-item vendor metadata cleanup",
    },
    "gamemode/core/libs/item/cl_networking.lua": {
        "semantic_role": "client_item_networking",
        "required_patterns": [
            "netstream.Hook(\"invData\"",
            "hook.Run(\"ItemDataChanged\"",
            "nut.item.instances",
            "item.data[key]",
            "oldValue",
        ],
        "validation_questions": [
            "Does client item networking receive invData?",
            "Does invData mutate client item.data[key]?",
            "Does invData emit ItemDataChanged after mutation?",
        ],
        "expected_runtime_relation": "client item metadata delta receive path and ItemDataChanged emission",
    },
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def norm_path(value: str) -> str:
    return value.replace("\\", "/").strip().lstrip("./")


def ensure_list(obj: dict[str, Any], key: str) -> list[Any]:
    value = obj.get(key)
    if isinstance(value, list):
        return value
    obj[key] = []
    return obj[key]


def merge_unique(dst: list[Any], src: list[Any]) -> None:
    seen = {str(x) for x in dst}
    for item in src:
        if str(item) not in seen:
            dst.append(item)
            seen.add(str(item))


def patch_targeted_plan(payload: dict[str, Any]) -> dict[str, Any]:
    out = deepcopy(payload)
    checks = ensure_list(out, "checks")

    existing_by_file: dict[str, dict[str, Any]] = {}
    for check in checks:
        if isinstance(check, dict) and check.get("file"):
            existing_by_file[norm_path(str(check["file"])).lower()] = check

    next_index = len(checks) + 1

    for file_path, spec in REQUIRED_TARGETS.items():
        key = file_path.lower()
        existing = existing_by_file.get(key)

        if existing is not None:
            existing["semantic_role"] = spec["semantic_role"]
            merge_unique(ensure_list(existing, "required_patterns"), spec["required_patterns"])
            merge_unique(ensure_list(existing, "validation_questions"), spec["validation_questions"])
            existing["expected_runtime_relation"] = spec["expected_runtime_relation"]
            existing.setdefault("priority", "high")
            existing.setdefault("confidence", "high")
            existing.setdefault("hypothesis", "Vendor purchase transfer clears purchased-item vendor metadata and syncs item data to client UI")
            continue

        checks.append({
            "check_id": f"TV-PATCH-{next_index:03d}",
            "hypothesis": "Vendor purchase transfer clears purchased-item vendor metadata and syncs item data to client UI",
            "confidence": "high",
            "priority": "high",
            "file": file_path,
            "semantic_role": spec["semantic_role"],
            "validation_questions": spec["validation_questions"],
            "required_patterns": spec["required_patterns"],
            "expected_runtime_relation": spec["expected_runtime_relation"],
            "falsifies_if": [
                "Required patterns are absent from the validated source file.",
                "The file is legacy or not used in the current vendor purchase runtime path.",
            ],
        })
        next_index += 1

    # Rebuild lightweight summary if this is a targeted validation plan.
    by_file: dict[str, int] = {}
    by_role: dict[str, int] = {}
    by_priority: dict[str, int] = {}
    for check in checks:
        if not isinstance(check, dict):
            continue
        by_file[str(check.get("file", "unknown"))] = by_file.get(str(check.get("file", "unknown")), 0) + 1
        by_role[str(check.get("semantic_role", "unknown"))] = by_role.get(str(check.get("semantic_role", "unknown")), 0) + 1
        by_priority[str(check.get("priority", "unknown"))] = by_priority.get(str(check.get("priority", "unknown")), 0) + 1

    out["summary"] = {
        "checks_total": len(checks),
        "by_priority": dict(sorted(by_priority.items(), key=lambda kv: kv[0])),
        "by_role": dict(sorted(by_role.items(), key=lambda kv: kv[1], reverse=True)),
        "by_file": dict(sorted(by_file.items(), key=lambda kv: kv[1], reverse=True)),
    }
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Patch vendor purchase targeted validation plan with missing source checks.")
    parser.add_argument("--input", required=True, type=Path, help="Existing *_targeted_validation.json file")
    parser.add_argument("--output", type=Path, default=None, help="Patched output json. Defaults to *_patched.json")
    args = parser.parse_args()

    source = args.input.resolve()
    if not source.exists():
        raise FileNotFoundError(source)

    output = args.output.resolve() if args.output else source.with_name(source.stem + "_patched.json")

    payload = read_json(source)
    patched = patch_targeted_plan(payload)
    write_json(output, patched)

    print(f"Wrote patched targeted validation plan: {output}")
    print("Required files now included:")
    for path in REQUIRED_TARGETS:
        print(f"  - {path}")
    print("")
    print("Next commands:")
    print("  python -m scripts.qdrant.validate_targeted_sources `")
    print("    --workspace-config config/workspace.yaml `")
    print(f"    --targeted {output}")
    print("")
    print("Then rerun:")
    print("  python -m scripts.qdrant.build_runtime_chain_evidence `")
    print("    --source-validation investigations/validation/vendor_stale_price_label_after_purchase_validation_source_validation.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
