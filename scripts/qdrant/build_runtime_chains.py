#!/usr/bin/env python3
"""
SIGNALIS AI — Runtime Chain Builder V1

Purpose:
  Convert runtime facts into topology-aware runtime chains.

Input:
  investigations/validation/*_runtime_facts.json

Output:
  *_runtime_chains.json
  *_runtime_chains.md

Usage:
  python -m scripts.qdrant.build_runtime_chains `
    --facts investigations/validation/vendor_stale_price_label_after_purchase_validation_runtime_facts.json
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


FACT_PRIORITY = {
    "network_send_start": 90,
    "network_receive": 88,
    "vendor_network_handler": 86,
    "hook_emit": 82,
    "hook_listener": 80,
    "item_data_mutation": 78,
    "entity_netvar_mutation": 74,
    "ui_refresh_call": 70,
    "ui_text_update": 55,
    "function_context": 30,
}


@dataclass
class ChainStep:
    order: int
    kind: str
    target: str
    file: str
    realm: str
    lines: str
    confidence: str
    reason: str
    fact_index: int | None


@dataclass
class RuntimeChain:
    chain_id: str
    title: str
    confidence: str
    reason: str
    steps: list[ChainStep]
    warnings: list[str]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def norm(value: str) -> str:
    return value.replace("\\", "/").lower()


def fact_label(fact: dict[str, Any]) -> str:
    return f"{fact.get('fact_type')}:{fact.get('target')}"


def detail(fact: dict[str, Any], key: str, default: Any = None) -> Any:
    details = fact.get("details", {})
    if isinstance(details, dict):
        return details.get(key, default)
    return default


def lines_of(fact: dict[str, Any]) -> str:
    return f"{fact.get('line_start', 0)}-{fact.get('line_end', 0)}"


def step_from_fact(
    order: int,
    fact: dict[str, Any],
    fact_index: int,
    reason: str,
    kind_override: str | None = None,
) -> ChainStep:
    return ChainStep(
        order=order,
        kind=kind_override or str(fact.get("fact_type", "")),
        target=str(fact.get("target", "")),
        file=str(fact.get("file", "")),
        realm=str(fact.get("realm", "")),
        lines=lines_of(fact),
        confidence=str(fact.get("confidence", "")),
        reason=reason,
        fact_index=fact_index,
    )


def manual_step(order: int, kind: str, target: str, reason: str, confidence: str = "human_validated") -> ChainStep:
    return ChainStep(
        order=order,
        kind=kind,
        target=target,
        file="human_context.md",
        realm="runtime",
        lines="-",
        confidence=confidence,
        reason=reason,
        fact_index=None,
    )


def find_facts(
    facts: list[dict[str, Any]],
    *,
    fact_type: str | None = None,
    target: str | None = None,
    file_contains: str | None = None,
    detail_key: str | None = None,
    detail_value_contains: str | None = None,
) -> list[tuple[int, dict[str, Any]]]:
    results: list[tuple[int, dict[str, Any]]] = []

    for idx, fact in enumerate(facts):
        if fact_type is not None and fact.get("fact_type") != fact_type:
            continue
        if target is not None and fact.get("target") != target:
            continue
        if file_contains is not None and file_contains.lower() not in norm(str(fact.get("file", ""))):
            continue
        if detail_key is not None:
            value = detail(fact, detail_key)
            if value is None:
                continue
            if detail_value_contains is not None and detail_value_contains.lower() not in str(value).lower():
                continue

        results.append((idx, fact))

    results.sort(
        key=lambda item: (
            int(item[1].get("evidence_score", 0)),
            FACT_PRIORITY.get(str(item[1].get("fact_type", "")), 0),
        ),
        reverse=True,
    )
    return results


def first_fact(
    facts: list[dict[str, Any]],
    **kwargs: Any,
) -> tuple[int, dict[str, Any]] | None:
    found = find_facts(facts, **kwargs)
    return found[0] if found else None


def all_targets(facts: list[dict[str, Any]], fact_type: str) -> set[str]:
    return {str(f.get("target", "")) for f in facts if f.get("fact_type") == fact_type}


def has_fact(facts: list[dict[str, Any]], fact_type: str, target: str) -> bool:
    return any(f.get("fact_type") == fact_type and f.get("target") == target for f in facts)


def build_vendor_open_chain(facts: list[dict[str, Any]]) -> RuntimeChain | None:
    steps: list[ChainStep] = []
    warnings: list[str] = []
    order = 1

    # Human-validated root from human_context.md.
    steps.append(
        manual_step(
            order,
            "player_interaction",
            "Player interacts with vendor",
            "human-validated vendor open flow",
        )
    )
    order += 1

    steps.append(
        manual_step(
            order,
            "server_event_or_call",
            "OpenVendorTradeInterface",
            "server calls/emits OpenVendorTradeInterface before client vendor UI opens",
        )
    )
    order += 1

    vendor_trade_receive = first_fact(
        facts,
        fact_type="network_receive",
        target="vendorTradeInterface",
    )
    if vendor_trade_receive:
        idx, fact = vendor_trade_receive
        steps.append(step_from_fact(order, fact, idx, "client receives vendorTradeInterface"))
        order += 1
    else:
        warnings.append("Missing network_receive:vendorTradeInterface fact.")

    create_panel = first_fact(
        facts,
        fact_type="hook_listener",
        target="CreateNewInventoryPanel",
    )
    if create_panel:
        idx, fact = create_panel
        steps.append(
            step_from_fact(
                order,
                fact,
                idx,
                "vendorTradeInterface creates inventory panels; this is UI construction, not root cause",
                kind_override="ui_panel_construction",
            )
        )
        order += 1
    else:
        warnings.append("Missing CreateNewInventoryPanel fact.")

    steps.append(
        manual_step(
            order,
            "ui_result",
            "Player inventory panel + vendor_grid_inventory panel",
            "human-validated result: player inventory uses CreateNewInventoryPanel; vendor inventory uses vgui.Create('vendor_grid_inventory') and SetUpPanel(loadedInv)",
        )
    )

    return RuntimeChain(
        chain_id="vendor_open_trade_interface",
        title="Vendor Open / Trade Interface Construction",
        confidence="high",
        reason="human-validated flow plus runtime facts",
        steps=steps,
        warnings=warnings,
    )


def build_vendor_price_update_chain(facts: list[dict[str, Any]]) -> RuntimeChain | None:
    steps: list[ChainStep] = []
    warnings: list[str] = []
    order = 1

    trade_send = first_fact(facts, fact_type="network_send_start", target="nutVendorTrade")
    if trade_send:
        idx, fact = trade_send
        steps.append(step_from_fact(order, fact, idx, "client initiates buy/sell request"))
        order += 1
    else:
        warnings.append("Missing client network_send_start:nutVendorTrade.")

    steps.append(
        manual_step(
            order,
            "server_authority",
            "Server validates vendor trade",
            "server is authoritative for gameplay/inventory mutation",
            confidence="doctrine",
        )
    )
    order += 1

    for key in ["vendorQty", "vendorSPrice", "vendorMQty"]:
        mutation = first_fact(
            facts,
            fact_type="item_data_mutation",
            target=key,
            file_contains="nut_vendor/init.lua",
        )
        if mutation:
            idx, fact = mutation
            steps.append(
                step_from_fact(
                    order,
                    fact,
                    idx,
                    "server mutates vendor presentation metadata via item:setData",
                )
            )
            order += 1
        else:
            warnings.append(f"Missing item_data_mutation:{key}.")

    steps.append(
        manual_step(
            order,
            "sync_boundary",
            "item:setData conditional sync / persistence boundary",
            "human-validated: setData persists item data and may immediately sync to receiver/current owner or later to future owner/opened inventory",
        )
    )
    order += 1

    price_handler = first_fact(facts, fact_type="vendor_network_handler", target="Price")
    if price_handler:
        idx, fact = price_handler
        steps.append(step_from_fact(order, fact, idx, "client vendor Price handler receives presentation update"))
        order += 1
    else:
        warnings.append("Missing vendor_network_handler:Price.")

    price_hook_emit = first_fact(facts, fact_type="hook_emit", target="VendorItemPriceUpdated")
    if price_hook_emit:
        idx, fact = price_hook_emit
        steps.append(step_from_fact(order, fact, idx, "Price handler emits VendorItemPriceUpdated"))
        order += 1
    else:
        warnings.append("Missing hook_emit:VendorItemPriceUpdated.")

    price_hook_listener = first_fact(facts, fact_type="hook_listener", target="VendorItemPriceUpdated")
    if price_hook_listener:
        idx, fact = price_hook_listener
        listener_fn = detail(fact, "listener_function", "")
        steps.append(
            step_from_fact(
                order,
                fact,
                idx,
                f"vendor UI listens through {listener_fn or 'registered listener'}",
            )
        )
        order += 1
    else:
        warnings.append("Missing hook_listener:VendorItemPriceUpdated.")

    update_price = first_fact(facts, fact_type="ui_refresh_call", target="updatePrice")
    if update_price:
        idx, fact = update_price
        steps.append(step_from_fact(order, fact, idx, "vendor UI refreshes visible price label"))
    else:
        warnings.append("Missing ui_refresh_call:updatePrice.")

    return RuntimeChain(
        chain_id="vendor_price_update_ui_refresh",
        title="Vendor Price Update / UI Refresh",
        confidence="medium",
        reason="runtime facts show item metadata mutation, vendor network handler, hook dispatch, and UI refresh",
        steps=steps,
        warnings=warnings,
    )


def build_vendor_exit_cleanup_chain(facts: list[dict[str, Any]]) -> RuntimeChain | None:
    steps: list[ChainStep] = []
    warnings: list[str] = []
    order = 1

    exit_send = first_fact(
        facts,
        fact_type="network_send_start",
        target="nutVendorExit",
        file_contains="cl_vendor.lua",
    )
    if exit_send:
        idx, fact = exit_send
        steps.append(step_from_fact(order, fact, idx, "client closes/removes vendor panel and sends exit"))
        order += 1
    else:
        warnings.append("Missing client network_send_start:nutVendorExit.")

    steps.append(
        manual_step(
            order,
            "server_cleanup_call",
            "ENT:RemoveReceiverFromVendor(client)",
            "server removes client from vendor receivers and clears vendor metadata",
            confidence="source_inferred",
        )
    )
    order += 1

    for key in ["vendorBPrice", "vendorQty", "vendorSPrice", "vendorMQty"]:
        mutation = first_fact(
            facts,
            fact_type="item_data_mutation",
            target=key,
            file_contains="nut_vendor/init.lua",
            detail_key="mutator_function",
            detail_value_contains="RemoveReceiverFromVendor",
        )

        if mutation:
            idx, fact = mutation
            steps.append(
                step_from_fact(
                    order,
                    fact,
                    idx,
                    "server clears vendor presentation metadata with nil setData",
                )
            )
            order += 1
        else:
            warnings.append(f"Missing cleanup item_data_mutation:{key} in RemoveReceiverFromVendor.")

    steps.append(
        manual_step(
            order,
            "sync_boundary",
            "item:setData nil sync / persistence boundary",
            "human-validated: cleanup may sync immediately to receiver/current owner or persist for future sync",
        )
    )

    return RuntimeChain(
        chain_id="vendor_exit_metadata_cleanup",
        title="Vendor Exit / Metadata Cleanup",
        confidence="high",
        reason="runtime facts show RemoveReceiverFromVendor clearing vendor* item data keys",
        steps=steps,
        warnings=warnings,
    )


def build_inventory_data_sync_chain(facts: list[dict[str, Any]]) -> RuntimeChain | None:
    steps: list[ChainStep] = []
    warnings: list[str] = []
    order = 1

    inv_data = first_fact(facts, fact_type="network_receive", target="nutInventoryData")
    if inv_data:
        idx, fact = inv_data
        steps.append(step_from_fact(order, fact, idx, "client receives inventory data delta"))
        order += 1
    else:
        warnings.append("Missing network_receive:nutInventoryData.")

    steps.append(
        manual_step(
            order,
            "client_inventory_state_update",
            "Inventory instance data key/value update",
            "nutInventoryData updates client inventory instance data",
            confidence="source_inferred",
        )
    )
    order += 1

    steps.append(
        manual_step(
            order,
            "ui_risk",
            "Existing inventory/vendor item panels may need refresh",
            "stale labels may remain if UI does not observe ItemDataChanged or equivalent refresh boundary",
            confidence="hypothesis",
        )
    )

    return RuntimeChain(
        chain_id="inventory_data_delta_sync",
        title="Inventory Data Delta Sync / UI Refresh Risk",
        confidence="medium",
        reason="runtime facts show nutInventoryData receiver; UI refresh linkage still requires validation",
        steps=steps,
        warnings=warnings,
    )


def build_storage_refresh_recovery_chain(facts: list[dict[str, Any]]) -> RuntimeChain | None:
    steps: list[ChainStep] = []
    warnings: list[str] = []
    order = 1

    storage_interface = first_fact(facts, fact_type="network_receive", target="vendorTradeInterface")
    if storage_interface:
        idx, fact = storage_interface
        steps.append(step_from_fact(order, fact, idx, "vendor/storage inventory UI construction path exists"))
        order += 1

    storage_panel = first_fact(facts, fact_type="hook_emit", target="OnCreateStoragePanel")
    if storage_panel:
        idx, fact = storage_panel
        steps.append(step_from_fact(order, fact, idx, "storage panel creation emits UI/storage hook"))
        order += 1
    else:
        warnings.append("Missing hook_emit:OnCreateStoragePanel.")

    remove_receiver = first_fact(facts, fact_type="network_send_start", target="removeReceiverFromVendor")
    if remove_receiver:
        idx, fact = remove_receiver
        steps.append(step_from_fact(order, fact, idx, "storage/vendor panel close sends removeReceiverFromVendor"))
        order += 1
    else:
        warnings.append("Missing network_send_start:removeReceiverFromVendor.")

    steps.append(
        manual_step(
            order,
            "observed_recovery",
            "Moving item through storage can refresh/clear stale vendor label",
            "human-observed recovery path; exact source-level refresh boundary still needs validation",
            confidence="human_observed",
        )
    )

    return RuntimeChain(
        chain_id="storage_refresh_recovery_path",
        title="Storage Movement / Vendor Label Recovery Path",
        confidence="medium",
        reason="human observation plus runtime facts around storage/vendor panel creation and receiver removal",
        steps=steps,
        warnings=warnings,
    )


def build_chains(facts: list[dict[str, Any]]) -> list[RuntimeChain]:
    candidates = [
        build_vendor_open_chain(facts),
        build_vendor_price_update_chain(facts),
        build_vendor_exit_cleanup_chain(facts),
        build_inventory_data_sync_chain(facts),
        build_storage_refresh_recovery_chain(facts),
    ]

    return [chain for chain in candidates if chain is not None]


def summarize(chains: list[RuntimeChain], facts: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "facts_total": len(facts),
        "chains_total": len(chains),
        "chains": [
            {
                "chain_id": chain.chain_id,
                "title": chain.title,
                "steps": len(chain.steps),
                "warnings": len(chain.warnings),
                "confidence": chain.confidence,
            }
            for chain in chains
        ],
    }


def format_step(step: ChainStep) -> str:
    file_part = f"`{step.file}:{step.lines}`" if step.file != "human_context.md" else "`human_context.md`"
    return (
        f"{step.order}. `{step.kind}` / `{step.target}`\n"
        f"   - Realm: `{step.realm}`\n"
        f"   - Source: {file_part}\n"
        f"   - Confidence: `{step.confidence}`\n"
        f"   - Reason: {step.reason}"
    )


def format_md(source: Path, query: str, chains: list[RuntimeChain], facts: list[dict[str, Any]]) -> str:
    summary = summarize(chains, facts)

    lines: list[str] = []
    lines.append("# SIGNALIS AI — Runtime Chains")
    lines.append("")
    lines.append(f"- Source: `{source}`")
    lines.append(f"- Query: `{query}`")
    lines.append(f"- Facts total: `{summary['facts_total']}`")
    lines.append(f"- Chains total: `{summary['chains_total']}`")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("This report is built from runtime facts, not raw semantic similarity.")
    lines.append("")
    lines.append("Human-validated rules included:")
    lines.append("")
    lines.append("- `item:setData` is persistent item metadata mutation plus conditional sync boundary.")
    lines.append("- Vendor open flow is `OpenVendorTradeInterface → vendorTradeInterface → CreateNewInventoryPanel → vendor_grid_inventory and CreateNewInventoryPanel`.")
    lines.append("- Vendor price labels are UI/presentation metadata, not authoritative item ownership.")
    lines.append("")

    for chain in chains:
        lines.append(f"## {chain.title}")
        lines.append("")
        lines.append(f"- Chain ID: `{chain.chain_id}`")
        lines.append(f"- Confidence: `{chain.confidence}`")
        lines.append(f"- Reason: {chain.reason}")
        lines.append("")

        if chain.warnings:
            lines.append("### Warnings")
            lines.append("")
            for warning in chain.warnings:
                lines.append(f"- {warning}")
            lines.append("")

        lines.append("### Steps")
        lines.append("")
        for step in chain.steps:
            lines.append(format_step(step))
            lines.append("")

    lines.append("## Pipeline Notes")
    lines.append("")
    lines.append("Use this report as input for investigation synthesis.")
    lines.append("")
    lines.append("Do not treat warnings as bugs. They are missing validation links or uncertain runtime edges.")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--facts", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source = args.facts.resolve()
    payload = read_json(source)
    facts = list(payload.get("facts", []))

    chains = build_chains(facts)

    out_dir = args.out_dir.resolve() if args.out_dir else source.parent

    stem = source.stem
    for suffix in ["_runtime_chains", "_runtime_facts", "_evidence_graph", "_deduped", "_scored"]:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]

    stem = f"{stem}_runtime_chains"

    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"

    output = {
        "source": str(source),
        "query": payload.get("query"),
        "summary": summarize(chains, facts),
        "chains": [asdict(chain) for chain in chains],
    }

    write_json(json_path, output)
    write_text(md_path, format_md(source, str(payload.get("query", "")), chains, facts))

    print(f"Wrote runtime chains json: {json_path}")
    print(f"Wrote runtime chains report: {md_path}")
    print("")
    print("Summary:")
    print(f"  facts_total: {len(facts)}")
    print(f"  chains_total: {len(chains)}")
    for chain in chains:
        print(f"  {chain.chain_id}: steps={len(chain.steps)} warnings={len(chain.warnings)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())