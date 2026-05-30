#!/usr/bin/env python3
"""
SIGNALIS AI — Investigation Synthesis V1

Input:
  *_runtime_chains.json

Output:
  *_investigation_synthesis.md
  *_investigation_synthesis.json

Purpose:
  Convert runtime chains into:
  - likely failure points
  - confidence-ranked hypotheses
  - missing validation questions
  - next source-validation targets
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class Hypothesis:
    title: str
    confidence: str
    chain_ids: list[str]
    reasoning: str
    validation_targets: list[str]
    falsification: list[str]


@dataclass
class ValidationTarget:
    priority: str
    file: str
    reason: str
    look_for: list[str]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def chain_by_id(chains: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(c.get("chain_id")): c for c in chains}


def has_chain(chains: dict[str, dict[str, Any]], chain_id: str) -> bool:
    return chain_id in chains


def collect_sources(chains: list[dict[str, Any]]) -> list[str]:
    sources: set[str] = set()

    for chain in chains:
        for step in chain.get("steps", []):
            file_path = str(step.get("file", ""))
            if file_path and file_path != "human_context.md":
                sources.add(file_path)

    return sorted(sources)


def build_hypotheses(chains: list[dict[str, Any]]) -> list[Hypothesis]:
    by_id = chain_by_id(chains)
    hypotheses: list[Hypothesis] = []

    if has_chain(by_id, "vendor_exit_metadata_cleanup") and has_chain(by_id, "inventory_data_delta_sync"):
        hypotheses.append(
            Hypothesis(
                title="Cleanup sync does not reach or refresh the active client UI",
                confidence="high",
                chain_ids=[
                    "vendor_exit_metadata_cleanup",
                    "inventory_data_delta_sync",
                ],
                reasoning=(
                    "The runtime chains show that vendor metadata is cleared server-side through "
                    "RemoveReceiverFromVendor using item:setData(nil), while inventory data delta sync "
                    "is a separate client receiver path. Human context says item:setData is conditional "
                    "sync plus persistence. Therefore stale labels can occur if cleanup reaches server state "
                    "but does not refresh the already-open client panels."
                ),
                validation_targets=[
                    "gamemode/core/meta/inventory/cl_base_inventory.lua",
                    "plugins/vendor/derma/cl_vendor.lua",
                    "plugins/inventory/cl_hooks.lua",
                    "plugins/vendor/entities/entities/nut_vendor/init.lua",
                ],
                falsification=[
                    "If nutInventoryData always triggers an item panel redraw for the affected item.",
                    "If vendor panel close always destroys all item panels before stale labels can persist.",
                    "If vendor* metadata is not actually present on the player's purchased item clientside.",
                ],
            )
        )

    if has_chain(by_id, "vendor_price_update_ui_refresh"):
        hypotheses.append(
            Hypothesis(
                title="Price update path refreshes vendor UI, but not necessarily player inventory UI",
                confidence="medium",
                chain_ids=[
                    "vendor_price_update_ui_refresh",
                    "vendor_open_trade_interface",
                ],
                reasoning=(
                    "The price update chain ends in cl_vendor.lua updatePrice. The open flow creates "
                    "two panels: player inventory through CreateNewInventoryPanel and vendor inventory through "
                    "vendor_grid_inventory. The validated price refresh path may only refresh vendor UI panels, "
                    "not the player inventory panel after the item is moved/purchased."
                ),
                validation_targets=[
                    "plugins/vendor/derma/cl_vendor.lua",
                    "plugins/inventory/cl_hooks.lua",
                    "plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua",
                ],
                falsification=[
                    "If updatePrice is called for both vendor_grid_inventory and player inventory item panels.",
                    "If purchased item panel is reconstructed immediately after trade.",
                    "If player inventory panel ignores vendor* metadata entirely.",
                ],
            )
        )

    if has_chain(by_id, "vendor_exit_metadata_cleanup"):
        hypotheses.append(
            Hypothesis(
                title="Receiver ownership mismatch during item:setData cleanup",
                confidence="medium",
                chain_ids=[
                    "vendor_exit_metadata_cleanup",
                ],
                reasoning=(
                    "Cleanup uses item:setData with a client/receiver argument. Human context confirms "
                    "setData sync depends on receivers/current owner. If the purchased item has already moved "
                    "to another inventory/owner context, the cleanup sync may target the wrong receiver or miss "
                    "the active panel state."
                ),
                validation_targets=[
                    "plugins/vendor/entities/entities/nut_vendor/init.lua",
                    "gamemode/core/libs/item/sv_item.lua",
                    "gamemode/core/meta/inventory/sv_base_inventory.lua",
                    "gamemode/core/meta/inventory/cl_base_inventory.lua",
                ],
                falsification=[
                    "If cleanup is always sent to the actual current owner of every affected item.",
                    "If purchased item metadata is cleared before ownership transfer.",
                    "If client item data receiver updates all inventory instances globally by item ID.",
                ],
            )
        )

    if has_chain(by_id, "storage_refresh_recovery_path"):
        hypotheses.append(
            Hypothesis(
                title="Storage movement forces broader panel reconstruction or item data refresh",
                confidence="low",
                chain_ids=[
                    "storage_refresh_recovery_path",
                ],
                reasoning=(
                    "Human observation says moving the item through storage can clear the stale label. "
                    "The chain currently only proves a storage/vendor UI path exists; it does not yet prove "
                    "the exact refresh boundary. This is useful as a comparison path, not a confirmed cause."
                ),
                validation_targets=[
                    "plugins/storage/cl_networking.lua",
                    "plugins/inventory/cl_hooks.lua",
                    "plugins/gridinv/plugins/gridstorage/sh_plugin.lua",
                    "plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua",
                ],
                falsification=[
                    "If storage movement does not reconstruct the affected item panel.",
                    "If storage movement does not trigger item data resync.",
                    "If recovery is caused by vendor exit rather than storage transfer.",
                ],
            )
        )

    return hypotheses


def build_validation_targets(hypotheses: list[Hypothesis]) -> list[ValidationTarget]:
    merged: dict[str, ValidationTarget] = {}

    for hyp in hypotheses:
        for file_path in hyp.validation_targets:
            priority = "high" if hyp.confidence == "high" else "medium"
            old = merged.get(file_path)

            look_for = [
                f"Validate hypothesis: {hyp.title}",
                "Identify exact emitter/listener/network/state mutation relationship.",
                "Check whether UI panel refresh happens after item data changes.",
            ]

            if old is None:
                merged[file_path] = ValidationTarget(
                    priority=priority,
                    file=file_path,
                    reason=f"Needed for: {hyp.title}",
                    look_for=look_for,
                )
            else:
                if old.priority != "high" and priority == "high":
                    old.priority = "high"
                old.reason += f"; {hyp.title}"
                old.look_for.extend(x for x in look_for if x not in old.look_for)

    return sorted(
        merged.values(),
        key=lambda t: (0 if t.priority == "high" else 1, t.file),
    )


def format_md(source: Path, payload: dict[str, Any], hypotheses: list[Hypothesis], targets: list[ValidationTarget]) -> str:
    chains = payload.get("chains", [])
    query = payload.get("query", "")

    lines: list[str] = []
    lines.append("# SIGNALIS AI — Investigation Synthesis")
    lines.append("")
    lines.append(f"- Source: `{source}`")
    lines.append(f"- Query: `{query}`")
    lines.append(f"- Runtime chains: `{len(chains)}`")
    lines.append(f"- Hypotheses: `{len(hypotheses)}`")
    lines.append("")

    lines.append("## Current Working Interpretation")
    lines.append("")
    lines.append(
        "The stale vendor price label issue is currently best modeled as a "
        "client presentation metadata / refresh-boundary problem, not as proven "
        "inventory ownership corruption."
    )
    lines.append("")
    lines.append("Validated runtime shape:")
    lines.append("")
    lines.append("```text")
    lines.append("Vendor trade")
    lines.append("→ server item metadata mutation")
    lines.append("→ item:setData conditional sync/persistence boundary")
    lines.append("→ client vendor Price handler")
    lines.append("→ VendorItemPriceUpdated")
    lines.append("→ vendor UI updatePrice")
    lines.append("")
    lines.append("Vendor exit")
    lines.append("→ RemoveReceiverFromVendor")
    lines.append("→ vendor* metadata cleared with item:setData(nil)")
    lines.append("→ conditional sync/persistence boundary")
    lines.append("```")
    lines.append("")

    lines.append("## Ranked Hypotheses")
    lines.append("")

    for idx, hyp in enumerate(hypotheses, start=1):
        lines.append(f"### {idx}. {hyp.title}")
        lines.append("")
        lines.append(f"- Confidence: `{hyp.confidence}`")
        lines.append(f"- Related chains: `{', '.join(hyp.chain_ids)}`")
        lines.append("")
        lines.append(hyp.reasoning)
        lines.append("")
        lines.append("Validation targets:")
        lines.append("")
        for target in hyp.validation_targets:
            lines.append(f"- `{target}`")
        lines.append("")
        lines.append("Falsification checks:")
        lines.append("")
        for item in hyp.falsification:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("## Next Source Validation Targets")
    lines.append("")

    for target in targets:
        lines.append(f"### `{target.file}`")
        lines.append("")
        lines.append(f"- Priority: `{target.priority}`")
        lines.append(f"- Reason: {target.reason}")
        lines.append("- Look for:")
        for item in target.look_for:
            lines.append(f"  - {item}")
        lines.append("")

    lines.append("## Recommended Next Pipeline Step")
    lines.append("")
    lines.append("Use this synthesis to generate targeted validation reports instead of broad retrieval.")
    lines.append("")
    lines.append("Suggested next command pattern:")
    lines.append("")
    lines.append("```powershell")
    lines.append("python -m scripts.qdrant.validate_sources `")
    lines.append("  --workspace E:/signalis_ai `")
    lines.append("  --report investigations/generated/vendor_stale_price_label_after_purchase.md")
    lines.append("```")
    lines.append("")
    lines.append("Then compare validated source against the hypotheses above.")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chains", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source = args.chains.resolve()
    payload = read_json(source)
    chains = list(payload.get("chains", []))

    hypotheses = build_hypotheses(chains)
    targets = build_validation_targets(hypotheses)

    out_dir = args.out_dir.resolve() if args.out_dir else source.parent

    stem = source.stem
    for suffix in [
        "_investigation_synthesis",
        "_runtime_chains",
        "_runtime_facts",
        "_evidence_graph",
        "_deduped",
        "_scored",
    ]:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]

    stem = f"{stem}_investigation_synthesis"

    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"

    output = {
        "source": str(source),
        "query": payload.get("query"),
        "summary": {
            "chains": len(chains),
            "hypotheses": len(hypotheses),
            "validation_targets": len(targets),
        },
        "hypotheses": [asdict(h) for h in hypotheses],
        "validation_targets": [asdict(t) for t in targets],
    }

    write_json(json_path, output)
    write_text(md_path, format_md(source, payload, hypotheses, targets))

    print(f"Wrote investigation synthesis json: {json_path}")
    print(f"Wrote investigation synthesis report: {md_path}")
    print("")
    print("Summary:")
    print(f"  chains: {len(chains)}")
    print(f"  hypotheses: {len(hypotheses)}")
    print(f"  validation_targets: {len(targets)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())