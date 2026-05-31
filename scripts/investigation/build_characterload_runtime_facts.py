#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CATEGORY_MAP = {
    "multichar_emits_loaded_char": "lifecycle_event",
    "core_loadout_lifecycle": "lifecycle_event",
    "inventory_loadout_slot_lifecycle": "inventory_initialization",
    "inventory_init_network_sync": "inventory_network_sync",
    "inventory_init_client_apply": "inventory_client_apply",
    "inventory_ui_open_client": "inventory_ui_open",
}


REALM_MAP = {
    "plugins/multichar/sv_networking.lua": "server",
    "gamemode/core/hooks/sv_hooks.lua": "server",
    "plugins/inventory/sh_plugin.lua": "shared",
    "gamemode/core/meta/inventory/sv_base_inventory.lua": "server",
    "gamemode/core/meta/inventory/cl_base_inventory.lua": "client",
    "plugins/inventory/cl_hooks.lua": "client",
}


def norm_path(path: str) -> str:
    return path.replace("\\", "/")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_hits(data: dict[str, Any]) -> list[dict[str, Any]]:
    hits = data.get("hits", [])
    return [hit for hit in hits if isinstance(hit, dict)]


def infer_check_id(hit: dict[str, Any]) -> str:
    return str(
        hit.get("check_id")
        or hit.get("target_id")
        or hit.get("id")
        or "unknown_check"
    )


def infer_file(hit: dict[str, Any]) -> str:
    return norm_path(str(
        hit.get("file")
        or hit.get("path")
        or hit.get("source_file")
        or ""
    ))


def infer_pattern(hit: dict[str, Any]) -> str:
    return str(
        hit.get("pattern")
        or hit.get("needle")
        or hit.get("matched_pattern")
        or hit.get("query")
        or ""
    )


def infer_lines(hit: dict[str, Any]) -> str:
    start = hit.get("line_start") or hit.get("start_line") or hit.get("line")
    end = hit.get("line_end") or hit.get("end_line") or start

    if start is None:
        return ""

    return f"{start}-{end}" if end != start else str(start)


def fact_from_hit(index: int, hit: dict[str, Any]) -> dict[str, Any]:
    check_id = infer_check_id(hit)
    file_path = infer_file(hit)
    category = CATEGORY_MAP.get(check_id, "unknown")
    pattern = infer_pattern(hit)
    lines = infer_lines(hit)

    if check_id == "inventory_loadout_slot_lifecycle" and pattern == "char:getInv":
        text = json.dumps(hit, ensure_ascii=False)
        if "CharacterPreSave" in text or "719" in text or "728" in text:
            category = "persistence_save_noise"
    realm = REALM_MAP.get(file_path, "unknown")

    return {
        "fact_id": f"characterload_fact_{index:03d}",
        "check_id": check_id,
        "category": category,
        "realm": realm,
        "file": file_path,
        "pattern": pattern,
        "lines": lines,
        "evidence_type": "targeted_source_validation",
        "confidence": "validated" if hit.get("found", True) else "missing",
    }


def write_md(facts: list[dict[str, Any]], out_md: Path) -> None:
    by_category: dict[str, list[dict[str, Any]]] = {}

    for fact in facts:
        by_category.setdefault(fact["category"], []).append(fact)

    lines = [
        "# CharacterLoaded Inventory Runtime Facts",
        "",
        f"- Facts: `{len(facts)}`",
        "",
        "## Categories",
        "",
    ]

    for category, items in sorted(by_category.items()):
        lines += [
            f"### {category}",
            "",
            f"- Count: `{len(items)}`",
            "",
        ]

        for fact in items:
            lines += [
                f"#### {fact['fact_id']}",
                "",
                f"- Check: `{fact['check_id']}`",
                f"- Realm: `{fact['realm']}`",
                f"- File: `{fact['file']}`",
                f"- Pattern: `{fact['pattern']}`",
                f"- Lines: `{fact['lines'] or 'unknown'}`",
                "",
            ]

    out_md.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build normalized runtime facts for CharacterLoaded inventory lifecycle validation."
    )
    parser.add_argument(
        "--source-validation",
        type=Path,
        default=Path("investigations/validation/characterload_inventory_lifecycle_targets_source_validation.json"),
    )
    parser.add_argument(
        "--out-json",
        type=Path,
        default=Path("investigations/validation/characterload_inventory_runtime_facts.json"),
    )
    parser.add_argument(
        "--out-md",
        type=Path,
        default=Path("investigations/validation/characterload_inventory_runtime_facts.md"),
    )

    args = parser.parse_args()
    args.out_json.parent.mkdir(parents=True, exist_ok=True)

    data = load_json(args.source_validation)
    hits = collect_hits(data)

    facts = [
        fact_from_hit(index + 1, hit)
        for index, hit in enumerate(hits)
    ]

    report = {
        "schema": "characterload_inventory_runtime_facts.v1",
        "source_validation": str(args.source_validation),
        "facts_total": len(facts),
        "categories": sorted(set(f["category"] for f in facts)),
        "facts": facts,
    }

    args.out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    write_md(facts, args.out_md)

    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")
    print(f"Facts: {len(facts)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())