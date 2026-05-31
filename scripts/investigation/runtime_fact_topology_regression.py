from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_EXPECTATIONS = {
    "vendor_purchase_itemdata_runtime_fact_topology_v3.json": {
        "facts_count": 5,
        "mapped_count": 5,
        "expected_unmapped_count": 0,
        "unmapped_count": 0,
        "required_bindings": {
            "ItemInitialized": ["hook:ItemInitialized"],
            "ItemDataChanged": ["hook:ItemDataChanged"],
            "invData": ["netmsg:netstream:invData"],
            "invQuantity": ["netmsg:netstream:invQuantity"],
            "item": ["netmsg:netstream:item"],
        },
        "forbidden_matches": {
            "item": [
                "netmsg:gmod_net:ItemFound",
                "netmsg:gmod_net:ItemUpdated",
                "netmsg:gmod_net:RemoveItem",
                "netmsg:gmod_net:adminSpawnItem",
            ],
        },
    },
    "characterload_inventory_runtime_fact_topology_v3.json": {
        "facts_count": 18,
        "mapped_count": 17,
        "expected_unmapped_count": 1,
        "unmapped_count": 0,
        "required_bindings": {
            "InventoryInitialized": ["hook:InventoryInitialized"],
            "ItemInitialized": ["hook:ItemInitialized"],
            "PlayerLoadedChar": ["hook:PlayerLoadedChar"],
            "PlayerLoadout": ["hook:PlayerLoadout"],
            "PostPlayerLoadout": ["hook:PostPlayerLoadout"],
            "PrePlayerLoadedChar": ["hook:PrePlayerLoadedChar"],
            "InventoryDataChanged": ["hook:InventoryDataChanged"],
            "nutInventoryInit": ["netmsg:gmod_net:nutInventoryInit"],
            "inventorySetPanelStatus": ["netmsg:netstream:inventorySetPanelStatus"],
            "vendorTradeInterface": ["netmsg:netstream:vendorTradeInterface"],
        },
        "expected_unmapped": {
            "sync": "expected_unmapped",
        },
    },
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def bindings_by_name(payload: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}

    for binding in payload.get("bindings", []):
        name = str(binding.get("fact_name", ""))
        result.setdefault(name, []).append(binding)

    return result


def match_ids(binding: dict[str, Any]) -> set[str]:
    return {
        str(match.get("topology_node_id", ""))
        for match in binding.get("matches", [])
    }


def check_file(path: Path) -> list[str]:
    errors: list[str] = []

    payload = load_json(path)
    filename = path.name

    expected = DEFAULT_EXPECTATIONS.get(filename)
    if not expected:
        errors.append(f"No default expectations registered for {filename}")
        return errors

    if payload.get("schema") != "runtime_fact_topology.v3":
        errors.append(
            f"{filename}: expected schema runtime_fact_topology.v3, got {payload.get('schema')!r}"
        )

    for key in (
        "facts_count",
        "mapped_count",
        "expected_unmapped_count",
        "unmapped_count",
    ):
        actual = payload.get(key)
        wanted = expected.get(key)
        if actual != wanted:
            errors.append(f"{filename}: {key} expected {wanted}, got {actual}")

    by_name = bindings_by_name(payload)

    for fact_name, required_ids in expected.get("required_bindings", {}).items():
        bindings = by_name.get(fact_name, [])
        if not bindings:
            errors.append(f"{filename}: missing binding for fact {fact_name!r}")
            continue

        found_ids = set()
        for binding in bindings:
            found_ids |= match_ids(binding)

        for required_id in required_ids:
            if required_id not in found_ids:
                errors.append(
                    f"{filename}: fact {fact_name!r} missing required topology match {required_id!r}"
                )

    for fact_name, forbidden_ids in expected.get("forbidden_matches", {}).items():
        bindings = by_name.get(fact_name, [])

        found_ids = set()
        for binding in bindings:
            found_ids |= match_ids(binding)

        for forbidden_id in forbidden_ids:
            if forbidden_id in found_ids:
                errors.append(
                    f"{filename}: fact {fact_name!r} contains forbidden topology match {forbidden_id!r}"
                )

    for fact_name, expected_status in expected.get("expected_unmapped", {}).items():
        bindings = by_name.get(fact_name, [])
        if not bindings:
            errors.append(f"{filename}: missing expected-unmapped fact {fact_name!r}")
            continue

        for binding in bindings:
            actual_status = binding.get("mapping_status")
            if actual_status != expected_status:
                errors.append(
                    f"{filename}: fact {fact_name!r} expected status {expected_status!r}, got {actual_status!r}"
                )

    return errors


def write_report(path: Path, checked: int, errors: list[str]) -> None:
    lines = [
        "# Runtime Fact Topology Regression",
        "",
        f"- Checked: `{checked}`",
        f"- Passed: `{checked - (1 if errors else 0)}`",
        f"- Failed: `{1 if errors else 0}`",
        "",
    ]

    if errors:
        lines += ["## Errors", ""]
        for error in errors:
            lines.append(f"- {error}")
    else:
        lines.append("All runtime fact topology regression checks passed.")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Regression checks for runtime fact topology mapping artifacts."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        type=Path,
        help="runtime_fact_topology.v3 JSON files to check.",
    )
    parser.add_argument("--out-md", required=True, type=Path)

    args = parser.parse_args()

    all_errors: list[str] = []

    for path in args.files:
        all_errors.extend(check_file(path))

    write_report(args.out_md, checked=len(args.files), errors=all_errors)

    print(f"Checked: {len(args.files)}")
    print(f"Passed:  {0 if all_errors else len(args.files)}")
    print(f"Failed:  {1 if all_errors else 0}")
    print(f"Wrote:   {args.out_md}")

    if all_errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()