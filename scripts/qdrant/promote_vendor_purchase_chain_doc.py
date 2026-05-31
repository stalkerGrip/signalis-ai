#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_chain(payload: dict[str, Any]) -> dict[str, Any]:
    chains = payload.get("chains") or []
    if not chains:
        raise SystemExit("No chains found in runtime chain evidence JSON.")
    return chains[0]


def format_chain_doc(source_json: Path, payload: dict[str, Any], chain: dict[str, Any]) -> str:
    summary = payload.get("summary", {})
    steps = chain.get("steps", [])
    evidence = chain.get("evidence", [])

    lines = [
        "# Vendor Purchase Runtime Chain",
        "",
        "Status: source-validated runtime chain.",
        "",
        f"- Source evidence JSON: `{source_json}`",
        f"- Chain ID: `{chain.get('chain_id', 'CHAIN-001')}`",
        f"- Confidence: `{chain.get('confidence', 'unknown')}`",
        f"- Score: `{chain.get('score', summary.get('chain_score', 'unknown'))}`",
        f"- Steps present: `{len(steps)}`",
        "",
        "## Runtime Chain",
        "",
    ]
    lines.extend(f"{idx}. {step}" for idx, step in enumerate(steps, start=1))
    lines += [
        "",
        "## Architecture Meaning",
        "",
        "Vendor purchase propagation crosses two separate runtime systems:",
        "",
        "1. Inventory membership propagation: transfer, add/remove, item full sync, and `nutInventoryAdd` membership delta.",
        "2. Item metadata propagation: `ITEM:setData`, `invData`, `ItemDataChanged`, and grid panel refresh.",
        "",
        "Do not conflate item metadata sync with inventory-level data sync. `InventoryDataChanged` / `nutInventoryData` is a different channel from `ItemDataChanged` / `invData`.",
        "",
        "## Validated Chain Form",
        "",
        "```text",
        "vendorSellItem",
        "→ oldInventory:removeItem",
        "→ inventory:add",
        "→ Inventory:syncItemAdded",
        "→ item:sync(recipients)",
        "→ nutInventoryAdd",
        "→ InventoryItemAdded",
        "→ item:setData(\"vendorSPrice\", nil)",
        "→ ITEM:setData",
        "→ invData",
        "→ ItemDataChanged",
        "→ InventoryItemDataChanged",
        "→ populateItems()",
        "```",
        "",
        "## Representative Evidence",
        "",
    ]

    for ev in evidence:
        lines += [
            f"### {ev.get('evidence_class', 'evidence')}",
            "",
            f"- File: `{ev.get('file', '')}`",
            f"- Lines: `{ev.get('lines', '')}`",
            f"- Pattern: `{ev.get('pattern', '')}`",
            f"- Score: `{ev.get('score', '')}`",
            "",
        ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote validated vendor purchase runtime chain to durable markdown doc.")
    parser.add_argument("--chain-evidence", required=True, type=Path, help="Runtime chain evidence JSON produced by build_runtime_chain_evidence.py")
    parser.add_argument("--out", type=Path, default=Path("docs/runtime/runtime_chains/vendor_purchase_chain.md"))
    args = parser.parse_args()

    source = args.chain_evidence.resolve()
    payload = read_json(source)
    chain = load_chain(payload)
    if chain.get("confidence") != "validated":
        raise SystemExit(f"Refusing to promote non-validated chain: confidence={chain.get('confidence')!r}")

    write_text(args.out, format_chain_doc(source, payload, chain))
    print(f"Wrote promoted runtime chain doc: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
