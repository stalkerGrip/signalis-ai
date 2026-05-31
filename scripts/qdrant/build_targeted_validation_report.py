#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


PATH_ALIASES = {
    "gamemode/core/libs/item/sv_item.lua": "gamemode/core/meta/item/sv_item.lua",
}

SEMANTIC_PATH_ROLES = {
    "gamemode/core/meta/item/sv_item.lua": "server_item_data",
    "gamemode/core/meta/inventory/sv_base_inventory.lua": "server_inventory",
    "gamemode/core/meta/inventory/cl_base_inventory.lua": "client_inventory",
    "plugins/gridinv/sv_transfer.lua": "gridinv_transfer",
    "plugins/vendor/entities/entities/nut_vendor/init.lua": "server_vendor_entity",
    "plugins/inventory/cl_hooks.lua": "client_inventory_hooks",
    "plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua": "client_grid_panel",
    "plugins/vendor/derma/cl_vendor.lua": "legacy_or_vendor_trade_ui",
    "plugins/vendor/cl_networking.lua": "vendor_client_networking",
    "plugins/storage/cl_networking.lua": "storage_client_networking",
    "plugins/gridinv/plugins/gridstorage/sh_plugin.lua": "grid_storage_ui",
}


@dataclass
class TargetedCheck:
    check_id: str
    hypothesis: str
    confidence: str
    priority: str
    file: str
    semantic_role: str
    validation_questions: list[str]
    required_patterns: list[str]
    expected_runtime_relation: str
    falsifies_if: list[str]


def norm_path(value: str) -> str:
    return value.replace("\\", "/").strip().lstrip("./")


def canonical_path(value: str) -> str:
    path = norm_path(value)
    return PATH_ALIASES.get(path.lower(), path)


def semantic_role(file_path: str) -> str:
    return SEMANTIC_PATH_ROLES.get(canonical_path(file_path).lower(), "unknown")


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


def patterns_for_role(role: str, hypothesis_title: str) -> list[str]:
    title = hypothesis_title.lower()
    patterns: set[str] = set()

    if role == "server_item_data":
        patterns.update([
            "function ITEM:setData",
            "self.data[key] = value",
            "netstream.Start",
            "\"invData\"",
            "nut.db.updateTable",
            "self:getOwner",
            "self:setNetVar",
        ])

    elif role == "server_inventory":
        patterns.update([
            "function Inventory:addItem",
            "function Inventory:removeItem",
            "function Inventory:syncItemAdded",
            "local recipients = self:getRecipients()",
            "item:sync(recipients)",
            "net.Start(\"nutInventoryAdd\")",
            "net.Send(recipients)",
            "function Inventory:getRecipients",
        ])

    elif role == "client_inventory":
        patterns.update([
            "net.Receive(\"nutInventoryData\"",
            "hook.Run(\"InventoryDataChanged\"",
            "net.Receive(\"nutInventoryAdd\"",
            "hook.Run(\"InventoryItemAdded\"",
            "net.Receive(\"nutInventoryRemove\"",
            "hook.Run(\"InventoryItemRemoved\"",
        ])

    elif role == "gridinv_transfer":
        patterns.update([
            "HandleItemTransferRequest",
            "CanItemBeTransfered",
            "oldInventory",
            "inventory:add",
            "vendorSellItem",
            "item:setData(\"vendorQty\", nil",
            "item:setData(\"vendorSPrice\", nil",
            "item:setData(\"vendorMQty\", nil",
            "item:setData(\"vendorBPrice\"",
        ])

    elif role == "server_vendor_entity":
        patterns.update([
            "function ENT:VendorItemSetData",
            "item:setData(\"vendorQty\"",
            "item:setData(\"vendorSPrice\"",
            "item:setData(\"vendorMQty\"",
            "function ENT:RemoveReceiverFromVendor",
            "v:setData(\"vendorBPrice\", nil",
            "v:setData(\"vendorQty\", nil",
            "v:setData(\"vendorSPrice\", nil",
            "v:setData(\"vendorMQty\", nil",
            "hook.Run(\"OpenVendorTradeInterface\"",
        ])

    elif role == "client_inventory_hooks":
        patterns.update([
            "netstream.Hook(\"vendorTradeInterface\"",
            "PLUGIN:CreateNewInventoryPanel",
            "vgui.Create(\"vendor_grid_inventory\")",
            "storageInvPanel:SetUpPanel(loadedInv)",
            "netstream.Start(\"removeReceiverFromVendor\"",
            "netstream.Start(\"inventorySetPanelStatus\"",
            "hook.Run(\"OnCreateStoragePanel\"",
        ])

    elif role == "client_grid_panel":
        patterns.update([
            "function PANEL:InventoryItemDataChanged",
            "self:populateItems()",
            "function PANEL:InventoryItemRemoved",
            "function PANEL:addItem",
            "item:getData(\"x\")",
            "item:getData(\"y\")",
        ])

    elif role == "legacy_or_vendor_trade_ui":
        patterns.update([
            "net.Start(\"nutVendorTrade\")",
            "net.Start(\"nutVendorExit\")",
            "hook.Add(\"VendorItemPriceUpdated\"",
            "function PANEL:onVendorPriceUpdated",
            "panel:updatePrice()",
        ])

    elif role == "vendor_client_networking":
        patterns.update([
            "VendorItemPriceUpdated",
            "VendorItemStockUpdated",
            "VendorMoneyUpdated",
            "hook.Run",
            "netstream.Hook",
        ])

    elif role in {"storage_client_networking", "grid_storage_ui"}:
        patterns.update([
            "StorageOpen",
            "hook.Run(\"StorageOpen\"",
            "OnCreateStoragePanel",
            "SetUpPanel",
            "inventorySetPanelStatus",
        ])

    if "cleanup sync" in title:
        patterns.update([
            "item:setData(\"vendorSPrice\", nil",
            "\"invData\"",
            "InventoryItemDataChanged",
            "self:populateItems()",
        ])

    if "player inventory ui" in title:
        patterns.update([
            "PLUGIN:CreateNewInventoryPanel",
            "vgui.Create(\"vendor_grid_inventory\")",
            "InventoryItemDataChanged",
            "panel:updatePrice()",
        ])

    if "receiver ownership" in title:
        patterns.update([
            "self:getOwner",
            "local recipients = self:getRecipients()",
            "item:sync(recipients)",
            "netstream.Start",
            "\"invData\"",
        ])

    if "storage movement" in title:
        patterns.update([
            "StorageOpen",
            "OnCreateStoragePanel",
            "SetUpPanel",
            "self:populateItems()",
        ])

    return sorted(patterns)


def questions_for_role(role: str) -> list[str]:
    if role == "server_item_data":
        return [
            "Does ITEM:setData persist item metadata?",
            "Does ITEM:setData immediately emit invData?",
            "Which receiver path is used when explicit receivers are passed?",
            "What happens if explicit receiver is stale or wrong?",
        ]
    if role == "server_inventory":
        return [
            "When item ownership changes, which recipients receive item sync?",
            "Does addItem call item:sync before nutInventoryAdd?",
            "Does transfer update recipients before item data cleanup?",
        ]
    if role == "gridinv_transfer":
        return [
            "Does vendor purchase cleanup happen after transfer?",
            "Are vendorSPrice/vendorQty/vendorMQty cleared on the transferred item?",
            "Which client is passed into item:setData cleanup?",
        ]
    if role == "client_grid_panel":
        return [
            "Does item data change call populateItems?",
            "Does panel reconstruction remove stale icon presentation state?",
            "Does the panel read vendor price data only during icon creation?",
        ]
    if role == "client_inventory_hooks":
        return [
            "How is the vendor trade interface built?",
            "Which panel is player inventory and which is vendor inventory?",
            "Does close/removal trigger removeReceiverFromVendor?",
        ]
    return ["Validate the exact runtime relation for this semantic role."]


def expected_relation(role: str) -> str:
    return {
        "server_item_data": "server item data mutation persists and conditionally syncs item data through invData",
        "server_inventory": "server inventory ownership and recipient sync boundary",
        "client_inventory": "client inventory membership/data receiver boundary",
        "gridinv_transfer": "server transfer flow mutates ownership and vendor presentation metadata",
        "server_vendor_entity": "server vendor entity creates/clears vendor item presentation metadata",
        "client_inventory_hooks": "client inventory/vendor interface construction and close cleanup boundary",
        "client_grid_panel": "client grid panel refreshes item icons when item data changes",
        "legacy_or_vendor_trade_ui": "vendor trade UI price hooks and trade/exit messages",
        "vendor_client_networking": "client vendor networking emits vendor update hooks",
        "storage_client_networking": "storage open/exit network boundary",
        "grid_storage_ui": "grid storage UI construction and panel pairing boundary",
    }.get(role, "runtime relation requires source validation")


def build_checks(payload: dict[str, Any]) -> list[TargetedCheck]:
    checks: list[TargetedCheck] = []
    counter = 1

    for hyp in payload.get("hypotheses", []):
        title = str(hyp.get("title", "Untitled hypothesis"))
        confidence = str(hyp.get("confidence", "unknown"))
        priority = priority_from_confidence(confidence)
        falsification = list(hyp.get("falsification", []))

        for raw_file in hyp.get("validation_targets", []):
            file_path = canonical_path(str(raw_file))
            role = semantic_role(file_path)

            checks.append(TargetedCheck(
                check_id=f"TV-{counter:03d}",
                hypothesis=title,
                confidence=confidence,
                priority=priority,
                file=file_path,
                semantic_role=role,
                validation_questions=questions_for_role(role),
                required_patterns=patterns_for_role(role, title),
                expected_runtime_relation=expected_relation(role),
                falsifies_if=falsification,
            ))
            counter += 1

    checks.sort(key=lambda c: (
        0 if c.priority == "high" else 1 if c.priority == "medium" else 2,
        c.semantic_role,
        c.file,
    ))
    return checks


def summarize(checks: list[TargetedCheck]) -> dict[str, Any]:
    by_priority: dict[str, int] = {}
    by_file: dict[str, int] = {}
    by_role: dict[str, int] = {}

    for check in checks:
        by_priority[check.priority] = by_priority.get(check.priority, 0) + 1
        by_file[check.file] = by_file.get(check.file, 0) + 1
        by_role[check.semantic_role] = by_role.get(check.semantic_role, 0) + 1

    return {
        "checks_total": len(checks),
        "by_priority": by_priority,
        "by_role": dict(sorted(by_role.items(), key=lambda x: x[1], reverse=True)),
        "by_file": dict(sorted(by_file.items(), key=lambda x: x[1], reverse=True)),
    }


def format_md(source: Path, payload: dict[str, Any], checks: list[TargetedCheck]) -> str:
    summary = summarize(checks)
    lines = [
        "# SIGNALIS AI — Targeted Validation Plan",
        "",
        f"- Source synthesis: `{source}`",
        f"- Query: `{payload.get('query', '')}`",
        f"- Checks total: `{summary['checks_total']}`",
        "",
        "## Purpose",
        "",
        "Convert investigation hypotheses into exact source-validation checks.",
        "",
        "## Summary",
        "",
        "```json",
        json.dumps(summary, indent=2, ensure_ascii=False),
        "```",
        "",
        "## Checks",
        "",
    ]

    for check in checks:
        lines += [
            f"### {check.check_id} — `{check.file}`",
            "",
            f"- Priority: `{check.priority}`",
            f"- Semantic role: `{check.semantic_role}`",
            f"- Hypothesis: {check.hypothesis}",
            f"- Confidence: `{check.confidence}`",
            f"- Expected runtime relation: {check.expected_runtime_relation}",
            "",
            "Validation questions:",
            "",
        ]
        lines += [f"- {q}" for q in check.validation_questions]
        lines += ["", "Required source patterns:", ""]
        lines += [f"- `{p}`" for p in check.required_patterns]
        lines += ["", "Falsifies hypothesis if:", ""]
        lines += [f"- {f}" for f in check.falsifies_if] or ["- No falsification rule provided."]
        lines.append("")

    lines += [
        "## Suggested Next Command",
        "",
        "```powershell",
        "python -m scripts.qdrant.validate_targeted_sources `",
        "  --workspace E:/signalis_ai `",
        "  --workspace-config workspace.yaml `",
        "  --targeted investigations/validation/vendor_stale_price_label_after_purchase_validation_targeted_validation.json",
        "```",
        "",
    ]

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