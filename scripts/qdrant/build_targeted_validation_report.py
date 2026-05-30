#!/usr/bin/env python3
"""
SIGNALIS AI — Targeted Validation Report Builder V1

Input:
  *_investigation_synthesis.json

Output:
  *_targeted_validation.json
  *_targeted_validation.md

Usage:
  python -m scripts.qdrant.build_targeted_validation_report `
    --synthesis investigations/validation/vendor_stale_price_label_after_purchase_validation_investigation_synthesis.json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class TargetedCheck:
    check_id: str
    hypothesis: str
    confidence: str
    priority: str
    file: str
    validation_questions: list[str]
    required_patterns: list[str]
    expected_runtime_relation: str
    falsifies_if: list[str]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def priority_from_confidence(confidence: str) -> str:
    if confidence == "high":
        return "high"
    if confidence == "medium":
        return "medium"
    return "low"


def patterns_for_file(file_path: str, hypothesis_title: str) -> list[str]:
    path = file_path.replace("\\", "/").lower()
    title = hypothesis_title.lower()

    patterns: set[str] = set()

    if "vendor/entities/entities/nut_vendor/init.lua" in path:
        patterns.update([
            "VendorItemSetData",
            "RemoveReceiverFromVendor",
            "setData",
            "vendorSPrice",
            "vendorBPrice",
            "vendorQty",
            "vendorMQty",
            "OpenVendorTradeInterface",
            "netstream.Start",
        ])

    if "vendor/derma/cl_vendor.lua" in path:
        patterns.update([
            "nutVendorTrade",
            "nutVendorExit",
            "VendorItemPriceUpdated",
            "onVendorPriceUpdated",
            "updatePrice",
            "hook.Add",
            "OnRemove",
        ])

    if "vendor/cl_networking.lua" in path:
        patterns.update([
            "addNetHandler",
            "Price",
            "Stock",
            "Money",
            "Mode",
            "hook.Run",
            "VendorItemPriceUpdated",
            "VendorItemStockUpdated",
        ])

    if "inventory/cl_hooks.lua" in path:
        patterns.update([
            "vendorTradeInterface",
            "CreateNewInventoryPanel",
            "vendor_grid_inventory",
            "SetUpPanel",
            "OnCreateStoragePanel",
            "removeReceiverFromVendor",
            "OnRemove",
        ])

    if "cl_base_inventory.lua" in path:
        patterns.update([
            "nutInventoryData",
            "net.Receive",
            "netstream.Hook",
            "setData",
            "data",
            "ItemDataChanged",
        ])

    if "sv_item.lua" in path:
        patterns.update([
            "ITEM:setData",
            "netstream.Start",
            "invData",
            "getOwner",
            "nut.db.updateTable",
            "setNetVar",
        ])

    if "sv_base_inventory.lua" in path:
        patterns.update([
            "addItem",
            "removeItem",
            "sync",
            "getReceivers",
            "netstream.Start",
            "invData",
        ])

    if "cl_grid_inventory_panel.lua" in path:
        patterns.update([
            "SetUpPanel",
            "update",
            "refresh",
            "ItemDataChanged",
            "Paint",
            "getData",
            "vendorSPrice",
            "vendorBPrice",
        ])

    if "gridstorage/sh_plugin.lua" in path or "storage/cl_networking.lua" in path:
        patterns.update([
            "StorageOpen",
            "storageInventory",
            "OnCreateStoragePanel",
            "SetUpPanel",
            "refresh",
            "ItemDataChanged",
        ])

    if "cleanup sync" in title:
        patterns.update(["nil", "RemoveReceiverFromVendor", "vendorSPrice", "invData"])

    if "player inventory ui" in title:
        patterns.update(["CreateNewInventoryPanel", "vendor_grid_inventory", "updatePrice", "getData"])

    if "receiver ownership" in title:
        patterns.update(["client", "receiver", "receivers", "owner", "getOwner", "setData"])

    return sorted(patterns)


def questions_for_file(file_path: str, hypothesis_title: str) -> list[str]:
    path = file_path.replace("\\", "/").lower()
    title = hypothesis_title.lower()

    questions: list[str] = []

    if "vendor/entities/entities/nut_vendor/init.lua" in path:
        questions.extend([
            "Where is vendor presentation metadata created?",
            "Where is vendor presentation metadata cleared?",
            "Does cleanup happen before or after item ownership/inventory transfer?",
            "Which receiver/client is passed into item:setData during cleanup?",
        ])

    if "vendor/derma/cl_vendor.lua" in path:
        questions.extend([
            "Does vendor UI refresh only vendor-side item panels or also player inventory panels?",
            "Does closing/removing the vendor panel send the cleanup message reliably?",
            "Does updatePrice read vendor* metadata from item data?",
        ])

    if "vendor/cl_networking.lua" in path:
        questions.extend([
            "Which network handler emits VendorItemPriceUpdated?",
            "Does the Price handler update item data, UI state, or only emit hooks?",
            "Is there a handler for metadata cleanup or only price/stock updates?",
        ])

    if "inventory/cl_hooks.lua" in path:
        questions.extend([
            "How exactly is vendorTradeInterface constructed?",
            "Which panel is the player inventory panel?",
            "Which panel is vendor_grid_inventory?",
            "Do either panels subscribe to item data changes?",
            "Does panel removal trigger removeReceiverFromVendor?",
        ])

    if "cl_base_inventory.lua" in path:
        questions.extend([
            "What does nutInventoryData mutate on the client?",
            "Does nutInventoryData emit ItemDataChanged or another refresh event?",
            "Does item data update trigger existing item panel refresh?",
        ])

    if "sv_item.lua" in path:
        questions.extend([
            "What receivers does ITEM:setData use by default?",
            "Does setData send invData immediately?",
            "Does noSave/noCheckEntity affect persistence or network sync?",
        ])

    if "sv_base_inventory.lua" in path:
        questions.extend([
            "How does server inventory transfer change item ownership?",
            "Are receivers updated before or after item data cleanup?",
            "Does inventory sync resend full item data after transfers?",
        ])

    if "cl_grid_inventory_panel.lua" in path:
        questions.extend([
            "Does grid inventory panel redraw when item data changes?",
            "Does it cache vendor price labels?",
            "Does it read vendorSPrice/vendorBPrice during paint or only on construction?",
        ])

    if "storage" in path:
        questions.extend([
            "Does storage movement reconstruct item panels?",
            "Does storage movement force full inventory data resync?",
            "What refresh boundary explains observed stale-label recovery?",
        ])

    if not questions:
        questions.append("Identify exact runtime relation relevant to this hypothesis.")

    return questions


def expected_relation(file_path: str, hypothesis_title: str) -> str:
    path = file_path.replace("\\", "/").lower()

    if "vendor/entities/entities/nut_vendor/init.lua" in path:
        return "server vendor entity mutates/clears vendor item presentation metadata"
    if "vendor/derma/cl_vendor.lua" in path:
        return "client vendor UI sends trade/exit and refreshes visible vendor price labels"
    if "vendor/cl_networking.lua" in path:
        return "client vendor network handler emits vendor update hooks"
    if "inventory/cl_hooks.lua" in path:
        return "client inventory/vendor interface constructs player inventory and vendor_grid_inventory panels"
    if "cl_base_inventory.lua" in path:
        return "client inventory data delta receiver mutates local inventory/item data"
    if "sv_item.lua" in path:
        return "server item data mutation persists and conditionally syncs item data"
    if "sv_base_inventory.lua" in path:
        return "server inventory ownership/transfer/sync boundary"
    if "cl_grid_inventory_panel.lua" in path:
        return "client grid inventory panel renders or refreshes item presentation metadata"
    if "storage" in path:
        return "storage movement may reconstruct panels or force broader item sync"

    return "runtime relation requires source validation"


def build_checks(payload: dict[str, Any]) -> list[TargetedCheck]:
    checks: list[TargetedCheck] = []
    counter = 1

    for hyp in payload.get("hypotheses", []):
        title = str(hyp.get("title", "Untitled hypothesis"))
        confidence = str(hyp.get("confidence", "unknown"))
        priority = priority_from_confidence(confidence)
        falsification = list(hyp.get("falsification", []))

        for file_path in hyp.get("validation_targets", []):
            checks.append(
                TargetedCheck(
                    check_id=f"TV-{counter:03d}",
                    hypothesis=title,
                    confidence=confidence,
                    priority=priority,
                    file=str(file_path),
                    validation_questions=questions_for_file(str(file_path), title),
                    required_patterns=patterns_for_file(str(file_path), title),
                    expected_runtime_relation=expected_relation(str(file_path), title),
                    falsifies_if=falsification,
                )
            )
            counter += 1

    checks.sort(key=lambda c: (0 if c.priority == "high" else 1 if c.priority == "medium" else 2, c.file))
    return checks


def summarize(checks: list[TargetedCheck]) -> dict[str, Any]:
    by_priority: dict[str, int] = {}
    by_file: dict[str, int] = {}

    for check in checks:
        by_priority[check.priority] = by_priority.get(check.priority, 0) + 1
        by_file[check.file] = by_file.get(check.file, 0) + 1

    return {
        "checks_total": len(checks),
        "by_priority": by_priority,
        "by_file": dict(sorted(by_file.items(), key=lambda x: x[1], reverse=True)),
    }


def format_md(source: Path, payload: dict[str, Any], checks: list[TargetedCheck]) -> str:
    summary = summarize(checks)

    lines: list[str] = []
    lines.append("# SIGNALIS AI — Targeted Validation Plan")
    lines.append("")
    lines.append(f"- Source synthesis: `{source}`")
    lines.append(f"- Query: `{payload.get('query', '')}`")
    lines.append(f"- Checks total: `{summary['checks_total']}`")
    lines.append("")
    lines.append("## Purpose")
    lines.append("")
    lines.append("This report converts investigation hypotheses into exact source-validation checks.")
    lines.append("")
    lines.append("Goal:")
    lines.append("")
    lines.append("```text")
    lines.append("hypotheses")
    lines.append("→ target files")
    lines.append("→ exact questions")
    lines.append("→ required source patterns")
    lines.append("→ validation/falsification")
    lines.append("```")
    lines.append("")

    lines.append("## Primary Failure Boundary")
    lines.append("")
    lines.append("```text")
    lines.append("item:setData cleanup / sync boundary")
    lines.append("→ client inventory data delta")
    lines.append("→ active item panel refresh")
    lines.append("```")
    lines.append("")

    lines.append("## Checks")
    lines.append("")

    for check in checks:
        lines.append(f"### {check.check_id} — `{check.file}`")
        lines.append("")
        lines.append(f"- Priority: `{check.priority}`")
        lines.append(f"- Hypothesis: {check.hypothesis}")
        lines.append(f"- Confidence: `{check.confidence}`")
        lines.append(f"- Expected runtime relation: {check.expected_runtime_relation}")
        lines.append("")
        lines.append("Validation questions:")
        lines.append("")
        for q in check.validation_questions:
            lines.append(f"- {q}")
        lines.append("")
        lines.append("Required source patterns:")
        lines.append("")
        for p in check.required_patterns:
            lines.append(f"- `{p}`")
        lines.append("")
        lines.append("Falsifies hypothesis if:")
        lines.append("")
        for f in check.falsifies_if:
            lines.append(f"- {f}")
        lines.append("")

    lines.append("## Suggested Next Command")
    lines.append("")
    lines.append("```powershell")
    lines.append("python -m scripts.qdrant.validate_sources `")
    lines.append("  --workspace E:/signalis_ai `")
    lines.append("  --report investigations/validation/vendor_stale_price_label_after_purchase_validation_targeted_validation.md")
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--synthesis", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source = args.synthesis.resolve()
    payload = read_json(source)
    checks = build_checks(payload)

    out_dir = args.out_dir.resolve() if args.out_dir else source.parent

    stem = source.stem
    for suffix in [
        "_targeted_validation",
        "_investigation_synthesis",
        "_runtime_chains",
        "_runtime_facts",
        "_evidence_graph",
        "_deduped",
        "_scored",
    ]:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]

    stem = f"{stem}_targeted_validation"

    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"

    output = {
        "source": str(source),
        "query": payload.get("query"),
        "summary": summarize(checks),
        "checks": [asdict(c) for c in checks],
    }

    write_json(json_path, output)
    write_text(md_path, format_md(source, payload, checks))

    print(f"Wrote targeted validation json: {json_path}")
    print(f"Wrote targeted validation report: {md_path}")
    print("")
    print("Summary:")
    print(f"  checks_total: {len(checks)}")
    for priority, count in summarize(checks)["by_priority"].items():
        print(f"  {priority}: {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())