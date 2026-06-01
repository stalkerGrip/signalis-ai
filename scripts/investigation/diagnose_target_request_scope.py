from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections import defaultdict


EXPECTED_VENDOR_STAGES = {
    "vendor_inventory_remove": [
        "vendor",
        "remove",
        "oldInventory",
    ],
    "player_inventory_add": [
        "inventory:add",
        ":add(",
        "character inventory",
    ],
    "item_sync": [
        "item:sync",
        ":sync(",
        "nutInventoryAdd",
    ],
    "vendor_metadata_cleanup": [
        "vendorSPrice",
        "vendorQty",
        "vendorMQty",
        "vendorBPrice",
    ],
    "item_metadata_mutation": [
        "setData",
        "ITEM:setData",
        "item:setData",
    ],
    "item_metadata_client_apply": [
        "invData",
        "ItemDataChanged",
    ],
    "ui_refresh": [
        "populateItems",
        "grid_inventory",
        "vendor_grid_inventory",
        "refresh",
    ],
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten(value) -> str:
    parts: list[str] = []

    def walk(v):
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


def get_checks(data: dict) -> list[dict]:
    checks = data.get("checks")
    if isinstance(checks, list):
        return checks

    for key in ("targets", "validation_targets", "required_checks"):
        value = data.get(key)
        if isinstance(value, list):
            return value

    raise ValueError("Could not find checks/targets list in target request JSON")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Diagnose whether a targeted validation request covers the vendor itemdata runtime chain."
    )
    parser.add_argument("--target-request", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    data = load_json(args.target_request)
    checks = get_checks(data)

    files: dict[str, int] = defaultdict(int)
    stage_hits: dict[str, list[dict]] = defaultdict(list)

    for idx, check in enumerate(checks):
        text = flatten(check)
        text_lower = text.lower()

        file_name = (
            check.get("file")
            or check.get("path")
            or check.get("source_file")
            or "unknown"
        )
        files[str(file_name)] += 1

        check_id = check.get("check_id") or check.get("id") or f"check_{idx}"

        for stage, needles in EXPECTED_VENDOR_STAGES.items():
            hits = [n for n in needles if n.lower() in text_lower]
            if hits:
                stage_hits[stage].append(
                    {
                        "check_index": idx,
                        "check_id": check_id,
                        "file": file_name,
                        "hits": hits,
                    }
                )

    present_stages = [stage for stage in EXPECTED_VENDOR_STAGES if stage in stage_hits]
    missing_stages = [stage for stage in EXPECTED_VENDOR_STAGES if stage not in stage_hits]

    if present_stages == ["item_metadata_client_apply"]:
        verdict = "client_apply_only"
    elif len(missing_stages) == 0:
        verdict = "full_vendor_chain"
    elif "item_metadata_client_apply" in present_stages and missing_stages:
        verdict = "partial_vendor_chain"
    else:
        verdict = "wrong_or_unrelated_scope"

    result = {
        "target_request": str(args.target_request),
        "checks_total": len(checks),
        "files_total": len(files),
        "files": dict(files),
        "present_stages": present_stages,
        "missing_stages": missing_stages,
        "scope_verdict": verdict,
        "stage_hits": dict(stage_hits),
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(
        json.dumps(result, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines: list[str] = [
        "# Target Request Scope Diagnosis",
        "",
        f"- Target request: `{args.target_request}`",
        f"- Checks total: `{len(checks)}`",
        f"- Files total: `{len(files)}`",
        f"- Present stages: `{len(present_stages)}`",
        f"- Missing stages: `{len(missing_stages)}`",
        f"- Scope verdict: `{verdict}`",
        "",
        "## Files",
        "",
    ]

    for file_name, count in sorted(files.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{file_name}`: `{count}`")

    lines.extend(["", "## Present Stages", ""])

    for stage in present_stages:
        lines.append(f"### `{stage}`")
        for hit in stage_hits[stage]:
            lines.append(
                f"- Check `{hit['check_index']}` / `{hit['check_id']}` "
                f"file=`{hit['file']}` hits=`{hit['hits']}`"
            )
        lines.append("")

    lines.extend(["## Missing Stages", ""])

    for stage in missing_stages:
        lines.append(f"- `{stage}`")

    args.out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Scope verdict: {verdict}")
    print(f"Checks total: {len(checks)}")
    print(f"Files total: {len(files)}")
    print(f"Present stages: {len(present_stages)}")
    print(f"Missing stages: {len(missing_stages)}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")


if __name__ == "__main__":
    main()