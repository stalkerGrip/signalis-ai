#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable


PATH_ALIASES = {
    "gamemode/core/libs/item/sv_item.lua": "gamemode/core/meta/item/sv_item.lua",
}

SEMANTIC_PATH_ROLES = {
    "plugins/gridinv/sv_transfer.lua": "gridinv_transfer",
    "gamemode/core/meta/inventory/sv_base_inventory.lua": "server_inventory",
    "gamemode/core/meta/inventory/cl_base_inventory.lua": "client_inventory",
    "gamemode/core/meta/item/sv_item.lua": "server_item_data",
    "gamemode/core/libs/item/cl_networking.lua": "client_item_networking",
    "plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua": "client_grid_panel",
    "plugins/inventory/cl_hooks.lua": "client_inventory_hooks",
    "plugins/vendor/cl_networking.lua": "vendor_client_networking",
    "plugins/vendor/derma/cl_vendor.lua": "legacy_or_vendor_trade_ui",
    "plugins/vendor/entities/entities/nut_vendor/init.lua": "server_vendor_entity",
}

CHAIN_ORDER = [
    "vendor_purchase_detection",
    "inventory_boundary_transfer",
    "inventory_membership_mutation",
    "inventory_recipients_resolved",
    "item_full_state_sync",
    "inventory_membership_network_send",
    "inventory_membership_receive_add",
    "inventory_membership_client_event",
    "vendor_metadata_cleanup",
    "item_metadata_mutation",
    "item_metadata_network_sync_send",
    "item_metadata_network_receive",
    "item_metadata_client_event",
    "gridinv_item_ui_refresh",
    "gridinv_panel_repopulate",
]

CLASS_LABELS = {
    "vendor_purchase_detection": "gridinv transfer identifies vendor → player purchase",
    "inventory_boundary_transfer": "transfer crosses old inventory to player inventory boundary",
    "inventory_membership_mutation": "server removes/adds item across inventories",
    "inventory_recipients_resolved": "server resolves current inventory recipients",
    "item_full_state_sync": "server sends full item state to recipients",
    "inventory_membership_network_send": "server sends nutInventoryAdd membership delta",
    "inventory_membership_receive_add": "client receives nutInventoryAdd",
    "inventory_membership_client_event": "client emits InventoryItemAdded",
    "vendor_metadata_cleanup": "server clears vendor metadata on purchased item",
    "item_metadata_mutation": "ITEM:setData mutates authoritative item data",
    "item_metadata_network_sync_send": "server sends invData item-data delta",
    "item_metadata_network_receive": "client receives invData item-data delta",
    "item_metadata_client_event": "client emits ItemDataChanged",
    "gridinv_item_ui_refresh": "grid inventory panel handles item-data change",
    "gridinv_panel_repopulate": "grid inventory panel repopulates item icons",
}

HIGH_VALUE_FILES = {
    "plugins/gridinv/sv_transfer.lua",
    "gamemode/core/meta/inventory/sv_base_inventory.lua",
    "gamemode/core/meta/inventory/cl_base_inventory.lua",
    "gamemode/core/meta/item/sv_item.lua",
    "gamemode/core/libs/item/cl_networking.lua",
    "plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua",
}


@dataclass
class Evidence:
    evidence_id: str
    evidence_class: str
    label: str
    file: str
    role: str
    lines: str
    pattern: str
    score: int
    text: str
    source_index: int


@dataclass
class Chain:
    chain_id: str
    title: str
    confidence: str
    steps: list[str] = field(default_factory=list)
    missing_steps: list[str] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)


def norm_path(value: str) -> str:
    return value.replace("\\", "/").strip().lstrip("./")


def canonical_path(value: str) -> str:
    path = norm_path(value)
    return PATH_ALIASES.get(path.lower(), path)


def semantic_role(file_path: str) -> str:
    return SEMANTIC_PATH_ROLES.get(canonical_path(file_path).lower(), "unknown")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def first_string(d: dict[str, Any], keys: Iterable[str]) -> str:
    for key in keys:
        value = d.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def line_string(d: dict[str, Any]) -> str:
    direct = first_string(d, ["lines", "line_range", "source_lines", "location"])
    if direct:
        return direct

    start = d.get("line_start", d.get("start_line", d.get("line")))
    end = d.get("line_end", d.get("end_line"))
    if isinstance(start, int) and isinstance(end, int):
        return f"{start}-{end}"
    if isinstance(start, int):
        return str(start)
    return "unknown"


def text_from_dict(d: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in [
        "text", "snippet", "code", "source", "content", "matched_text", "context",
        "function", "pattern", "match", "name", "message", "hook", "event",
    ]:
        value = d.get(key)
        if isinstance(value, str) and value.strip():
            parts.append(value)
    return "\n".join(dict.fromkeys(parts))


def flatten_fragments(payload: Any) -> list[dict[str, Any]]:
    """Extract source-validation hits from many possible JSON shapes.

    This intentionally accepts loose input because earlier pipeline stages have
    changed names several times: fragments, hits, matches, evidence, files, etc.
    """
    out: list[dict[str, Any]] = []

    def walk(node: Any, inherited: dict[str, Any] | None = None) -> None:
        inherited = inherited or {}
        if isinstance(node, dict):
            current = dict(inherited)

            file_value = first_string(node, ["file", "path", "file_path", "source_file", "target_file"])
            if file_value:
                current["file"] = file_value

            role_value = first_string(node, ["semantic_role", "role"])
            if role_value:
                current["semantic_role"] = role_value

            has_source_signal = bool(current.get("file")) and bool(
                text_from_dict(node)
                or any(k in node for k in ["line", "line_start", "start_line", "lines", "pattern", "match"])
            )
            if has_source_signal:
                merged = dict(node)
                merged.setdefault("file", current.get("file", ""))
                if "semantic_role" not in merged and current.get("semantic_role"):
                    merged["semantic_role"] = current["semantic_role"]
                out.append(merged)

            for value in node.values():
                if isinstance(value, (dict, list)):
                    walk(value, current)
        elif isinstance(node, list):
            for item in node:
                walk(item, inherited)

    walk(payload)

    # Deduplicate by file/lines/text prefix.
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for frag in out:
        file_path = canonical_path(first_string(frag, ["file", "path", "file_path", "source_file", "target_file"]))
        text = normalize_text(text_from_dict(frag))
        key = (file_path.lower(), line_string(frag), text[:500])
        if file_path and text and key not in seen:
            seen.add(key)
            frag["file"] = file_path
            deduped.append(frag)
    return deduped


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def contains_all(text: str, *needles: str) -> bool:
    lower = text.lower()
    return all(n.lower() in lower for n in needles)


def contains_any(text: str, needles: Iterable[str]) -> bool:
    lower = text.lower()
    return any(n.lower() in lower for n in needles)


def classify_fragment(file_path: str, text: str) -> list[tuple[str, str, int]]:
    """Return evidence classes as (class, matched_pattern, score)."""
    f = canonical_path(file_path).lower()
    t = text
    n = normalize_text(text).lower()
    classes: list[tuple[str, str, int]] = []

    def add(cls: str, pattern: str, score: int = 10) -> None:
        classes.append((cls, pattern, score))

    if f.endswith("plugins/gridinv/sv_transfer.lua"):
        if contains_any(n, ["vendorsellitem"]):
            add("vendor_purchase_detection", "vendorSellItem", 30)
        if contains_all(n, "oldinventory") and contains_any(n, ["inventory", "character", "getinv"]):
            add("inventory_boundary_transfer", "oldInventory + destination inventory", 24)
        if contains_any(n, ["oldinventory:remove", "removeitem", "inventory:add", ":additem", "itemtransfered"]):
            add("inventory_membership_mutation", "remove/add item transfer", 18)
        if contains_any(n, ["item:setdata(\"vendorsprice\", nil", "item:setdata('vendorsprice', nil"]):
            add("vendor_metadata_cleanup", "item:setData(\"vendorSPrice\", nil", 35)
        if contains_any(n, ["item:setdata(\"vendorqty\", nil", "item:setdata(\"vendormqty\", nil", "item:setdata(\"vendorbprice\""]):
            add("vendor_metadata_cleanup", "vendor metadata setData cleanup/update", 22)

    if f.endswith("gamemode/core/meta/inventory/sv_base_inventory.lua"):
        if contains_any(n, ["function inventory:syncitemadded", "syncitemadded"]):
            add("inventory_membership_network_send", "Inventory:syncItemAdded", 30)
        if contains_any(n, ["local recipients = self:getrecipients", "self:getrecipients()", "getrecipients"]):
            add("inventory_recipients_resolved", "self:getRecipients()", 24)
        if contains_any(n, ["item:sync(recipients", "item:sync("]):
            add("item_full_state_sync", "item:sync(recipients)", 28)
        if contains_any(n, ["net.start(\"nutinventoryadd\"", "net.start('nutinventoryadd'"]):
            add("inventory_membership_network_send", "net.Start(\"nutInventoryAdd\")", 28)
        if contains_any(n, ["net.send(recipients", "net.send(receiver", "net.send(client"]):
            add("inventory_membership_network_send", "net.Send(recipients)", 18)
        if contains_any(n, ["function inventory:add", "function inventory:additem", ":additem", ":add("]):
            add("inventory_membership_mutation", "Inventory add item", 14)

    if f.endswith("gamemode/core/meta/inventory/cl_base_inventory.lua"):
        if contains_any(n, ["net.receive(\"nutinventoryadd\"", "net.receive('nutinventoryadd'"]):
            add("inventory_membership_receive_add", "net.Receive(\"nutInventoryAdd\")", 30)
        if contains_any(n, ["hook.run(\"inventoryitemadded\"", "hook.run('inventoryitemadded'"]):
            add("inventory_membership_client_event", "hook.Run(\"InventoryItemAdded\")", 30)
        if contains_any(n, ["net.receive(\"nutinventorydata\"", "inventorydatachanged"]):
            add("inventory_level_data_not_item_data", "nutInventoryData / InventoryDataChanged", 5)

    if f.endswith("gamemode/core/meta/item/sv_item.lua"):
        if contains_any(n, ["function item:setdata", "function item:setdata", "item:setdata"]):
            add("item_metadata_mutation", "function ITEM:setData", 30)
        if contains_any(n, ["self.data[key]", "self.data[ key ]", "data[key] = value"]):
            add("item_metadata_mutation", "self.data[key] = value", 24)
        if contains_any(n, ["invdata"]):
            add("item_metadata_network_sync_send", "invData", 30)
        if contains_any(n, ["netstream.start"]):
            add("item_metadata_network_sync_send", "netstream.Start(..., \"invData\", ...)", 24)
        if contains_any(n, ["nut.db.updatetable", "save", "nosave"]):
            add("item_metadata_persistence", "database/noSave behavior", 10)

    if f.endswith("gamemode/core/libs/item/cl_networking.lua"):
        if contains_any(n, ["netstream.hook(\"invdata\"", "netstream.hook('invdata'"]):
            add("item_metadata_network_receive", "netstream.Hook(\"invData\")", 35)
        if contains_any(n, ["item.data[key]", "item.data[ key ]"]):
            add("item_metadata_network_receive", "client item.data[key] mutation", 25)
        if contains_any(n, ["hook.run(\"itemdatachanged\"", "hook.run('itemdatachanged'"]):
            add("item_metadata_client_event", "hook.Run(\"ItemDataChanged\")", 35)

    if f.endswith("plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua"):
        if contains_any(n, ["inventoryitemdatachanged"]):
            add("gridinv_item_ui_refresh", "PANEL:InventoryItemDataChanged", 35)
        if contains_any(n, ["populateitems"]):
            add("gridinv_panel_repopulate", "self:populateItems()", 35)
        if contains_any(n, ["inventoryitemadded"]):
            add("inventory_membership_client_event", "PANEL:InventoryItemAdded", 12)

    return classes


def build_evidence(fragments: list[dict[str, Any]]) -> list[Evidence]:
    evidence: list[Evidence] = []
    counter = 1

    for idx, frag in enumerate(fragments):
        file_path = canonical_path(first_string(frag, ["file", "path", "file_path", "source_file", "target_file"]))
        if not file_path:
            continue
        text = text_from_dict(frag)
        if not text:
            continue
        role = first_string(frag, ["semantic_role", "role"]) or semantic_role(file_path)
        lines = line_string(frag)

        for cls, pattern, score in classify_fragment(file_path, text):
            # Keep the negative guard evidence in JSON, but don't let it consume CHAIN-001 steps.
            evidence.append(Evidence(
                evidence_id=f"E-{counter:04d}",
                evidence_class=cls,
                label=CLASS_LABELS.get(cls, cls),
                file=file_path,
                role=role,
                lines=lines,
                pattern=pattern,
                score=score + (5 if file_path in HIGH_VALUE_FILES else 0),
                text=text.strip(),
                source_index=idx,
            ))
            counter += 1

    evidence.sort(key=lambda e: (CHAIN_ORDER.index(e.evidence_class) if e.evidence_class in CHAIN_ORDER else 999, -e.score, e.file, e.lines))
    return evidence


def best_by_class(evidence: list[Evidence]) -> dict[str, Evidence]:
    best: dict[str, Evidence] = {}
    for ev in evidence:
        if ev.evidence_class not in CHAIN_ORDER:
            continue
        existing = best.get(ev.evidence_class)
        if existing is None or ev.score > existing.score:
            best[ev.evidence_class] = ev
    return best


def confidence_for(present: set[str]) -> str:
    # Promotion rule for CHAIN-001.
    #
    # The chain is considered validated only when the source-validation input
    # contains evidence for all causal boundaries, not merely generic inventory
    # or item-data behavior. This prevents generic NutScript evidence from
    # being mistaken for proof of the vendor purchase path.
    validated_required = {
        "vendor_purchase_detection",
        "inventory_boundary_transfer",
        "inventory_membership_mutation",
        "inventory_recipients_resolved",
        "item_full_state_sync",
        "inventory_membership_network_send",
        "inventory_membership_receive_add",
        "inventory_membership_client_event",
        "vendor_metadata_cleanup",
        "item_metadata_mutation",
        "item_metadata_network_sync_send",
        "item_metadata_network_receive",
        "item_metadata_client_event",
        "gridinv_item_ui_refresh",
        "gridinv_panel_repopulate",
    }

    strong_required = {
        "vendor_purchase_detection",
        "inventory_boundary_transfer",
        "inventory_membership_network_send",
        "inventory_membership_receive_add",
        "vendor_metadata_cleanup",
        "item_metadata_mutation",
        "item_metadata_network_sync_send",
        "item_metadata_network_receive",
        "item_metadata_client_event",
        "gridinv_item_ui_refresh",
        "gridinv_panel_repopulate",
    }

    if validated_required <= present:
        return "validated"

    count = len(strong_required & present)
    if count == len(strong_required):
        return "complete"
    if count >= 8 and "vendor_metadata_cleanup" in present and "item_metadata_client_event" in present:
        return "strong_partial"
    if count >= 5:
        return "partial"
    return "weak_partial"


def build_chain(evidence: list[Evidence]) -> Chain:
    best = best_by_class(evidence)
    present = set(best)
    steps = [CLASS_LABELS[c] for c in CHAIN_ORDER if c in present]
    missing = [CLASS_LABELS[c] for c in CHAIN_ORDER if c not in present]
    chain_evidence = [best[c] for c in CHAIN_ORDER if c in best]
    return Chain(
        chain_id="CHAIN-001",
        title="Vendor purchase transfer to item metadata cleanup",
        confidence=confidence_for(present),
        steps=steps,
        missing_steps=missing,
        evidence=chain_evidence,
    )


def summarize(evidence: list[Evidence], chain: Chain) -> dict[str, Any]:
    by_class: dict[str, int] = {}
    by_file: dict[str, int] = {}
    for ev in evidence:
        by_class[ev.evidence_class] = by_class.get(ev.evidence_class, 0) + 1
        by_file[ev.file] = by_file.get(ev.file, 0) + 1
    return {
        "evidence_total": len(evidence),
        "chain_confidence": chain.confidence,
        "chain_steps_present": len(chain.steps),
        "chain_steps_missing": len(chain.missing_steps),
        "by_class": dict(sorted(by_class.items(), key=lambda x: x[0])),
        "by_file": dict(sorted(by_file.items(), key=lambda x: x[1], reverse=True)),
    }


def lua_block(text: str, max_chars: int = 2200) -> str:
    trimmed = text.strip()
    if len(trimmed) > max_chars:
        trimmed = trimmed[:max_chars].rstrip() + "\n-- [trimmed]"
    return "```lua\n" + trimmed + "\n```"


def format_md(source: Path, chain: Chain, evidence: list[Evidence]) -> str:
    summary = summarize(evidence, chain)
    lines: list[str] = [
        "# SIGNALIS AI — Runtime Chain Evidence",
        "",
        f"- Source validation: `{source}`",
        f"- Evidence total: `{summary['evidence_total']}`",
        "",
        "## Summary",
        "",
        "```json",
        json.dumps(summary, indent=2, ensure_ascii=False),
        "```",
        "",
        "## Confidence Meaning",
        "",
        "- `validated`: every required causal boundary for CHAIN-001 is present in source-validation evidence.",
        "- `complete`: the high-level chain is present, but one or more supporting boundary classes are missing.",
        "- `strong_partial` / `partial`: useful propagation evidence exists, but the chain is not fully source-validated.",
        "",
        f"## {chain.chain_id} — {chain.title}",
        "",
        f"- Confidence: `{chain.confidence}`",
        "",
        "Steps:",
        "",
    ]
    lines += [f"- {step}" for step in chain.steps] or ["- none"]
    lines += ["", "Missing steps:", ""]
    lines += [f"- {step}" for step in chain.missing_steps] or ["- none"]
    lines += ["", "Evidence:", ""]

    for ev in chain.evidence:
        lines += [
            f"### {ev.evidence_id} — `{ev.evidence_class}`",
            "",
            f"- File: `{ev.file}`",
            f"- Role: `{ev.role}`",
            f"- Lines: `{ev.lines}`",
            f"- Pattern: `{ev.pattern}`",
            "",
            lua_block(ev.text),
            "",
        ]

    extra = [ev for ev in evidence if ev.evidence_id not in {x.evidence_id for x in chain.evidence}]
    if extra:
        lines += ["## Additional Classified Evidence", ""]
        for ev in extra[:80]:
            lines += [
                f"### {ev.evidence_id} — `{ev.evidence_class}`",
                "",
                f"- File: `{ev.file}`",
                f"- Role: `{ev.role}`",
                f"- Lines: `{ev.lines}`",
                f"- Pattern: `{ev.pattern}`",
                "",
                lua_block(ev.text, max_chars=1200),
                "",
            ]

    return "\n".join(lines)


def output_stem(source: Path) -> str:
    stem = source.stem
    for suffix in [
        "_runtime_chain_evidence",
        "_source_validation",
        "_targeted_validation",
        "_investigation_synthesis",
        "_runtime_chains",
        "_runtime_facts",
        "_evidence_graph",
        "_deduped",
        "_scored",
        "_validation",
    ]:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
    return f"{stem}_runtime_chain_evidence"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build runtime chain evidence from targeted source-validation JSON.")
    parser.add_argument("--synthesis", "--source-validation", dest="source_validation", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source = args.source_validation.resolve()
    payload = read_json(source)
    fragments = flatten_fragments(payload)
    evidence = build_evidence(fragments)
    chain = build_chain(evidence)

    out_dir = args.out_dir.resolve() if args.out_dir else source.parent
    stem = output_stem(source)
    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"

    output = {
        "source": str(source),
        "summary": summarize(evidence, chain),
        "chains": [
            {
                "chain_id": chain.chain_id,
                "title": chain.title,
                "confidence": chain.confidence,
                "steps": chain.steps,
                "missing_steps": chain.missing_steps,
                "evidence": [asdict(ev) for ev in chain.evidence],
            }
        ],
        "evidence": [asdict(ev) for ev in evidence],
    }

    write_json(json_path, output)
    write_text(md_path, format_md(source, chain, evidence))

    print(f"Wrote runtime chain evidence json: {json_path}")
    print(f"Wrote runtime chain evidence report: {md_path}")
    print("")
    print("Summary:")
    print(f"  evidence_total: {len(evidence)}")
    print(f"  {chain.chain_id}: {chain.confidence}")
    print(f"  steps_present: {len(chain.steps)}")
    print(f"  steps_missing: {len(chain.missing_steps)}")
    if chain.missing_steps:
        print("  missing:")
        for step in chain.missing_steps:
            print(f"    - {step}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
