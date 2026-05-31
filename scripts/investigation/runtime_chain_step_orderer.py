from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ORDER_HINTS = {
    "vendor_purchase_detection": 10,
    "vendor_item_metadata_assignment": 20,
    "inventory_membership_related": 25,
    "inventory_membership_sync_send": 30,
    "inventory_membership_client_apply": 40,
    "grid_inventory_membership_refresh": 50,
    "vendor_metadata_cleanup": 60,
    "item_metadata_mutation": 70,
    "item_metadata_network_send": 80,
    "item_metadata_client_apply": 90,
    "grid_inventory_item_refresh": 100,
}


@dataclass
class OrderedStep:
    order: int
    step_id: str
    category: str
    score: float
    evidence_count: int
    files: list[str]
    line_min: int | None
    line_max: int | None
    representative_pattern: str
    representative_text: str
    evidence_ranks: list[int]
    order_hint: int
    ordering_reasons: list[str]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def infer_order_hint(step: dict[str, Any]) -> tuple[int, list[str]]:
    step_id = str(step.get("step_id") or "")
    category = str(step.get("category") or "")
    text = f"{step_id} {category} {step.get('representative_pattern') or ''} {step.get('representative_text') or ''}".lower()

    if step_id in ORDER_HINTS:
        return ORDER_HINTS[step_id], [f"explicit_step_order:{step_id}={ORDER_HINTS[step_id]}"]

    if "vendorsellitem" in text or "oldinventory.vendor" in text:
        return 10, ["vendor purchase detection comes first"]

    if "syncitemadded" in text or "nutinventoryadd" in text:
        return 30, ["inventory membership send before client apply"]

    if "inventoryitemadded" in text and "hook.run" in text:
        return 40, ["client membership apply after nutInventoryAdd"]

    if "function item:setdata" in text or "self.data[key]" in text:
        return 70, ["server item metadata mutation before invData send"]

    if "invdata" in text and "netstream.start" in text:
        return 80, ["invData send after item metadata mutation"]

    if "itemdatachanged" in text and "netstream.hook" in text:
        return 90, ["client item data apply after invData send"]

    if "populateitems" in text:
        return 100, ["UI refresh after client data/event apply"]

    return 500, ["unknown order placed late"]


def order_steps(steps: list[dict[str, Any]]) -> list[OrderedStep]:
    enriched: list[tuple[int, float, dict[str, Any], list[str]]] = []

    for step in steps:
        hint, reasons = infer_order_hint(step)
        score = float(step.get("score") or 0)
        enriched.append((hint, -score, step, reasons))

    enriched.sort(key=lambda x: (x[0], x[1]))

    ordered: list[OrderedStep] = []
    for i, (hint, _neg_score, step, reasons) in enumerate(enriched, 1):
        ordered.append(
            OrderedStep(
                order=i,
                step_id=str(step.get("step_id") or ""),
                category=str(step.get("category") or ""),
                score=float(step.get("score") or 0),
                evidence_count=int(step.get("evidence_count") or 0),
                files=list(step.get("files") or []),
                line_min=step.get("line_min"),
                line_max=step.get("line_max"),
                representative_pattern=str(step.get("representative_pattern") or ""),
                representative_text=str(step.get("representative_text") or ""),
                evidence_ranks=list(step.get("evidence_ranks") or []),
                order_hint=hint,
                ordering_reasons=reasons,
            )
        )

    return ordered


def write_md(ordered: list[OrderedStep], out: Path) -> None:
    lines = [
        "# Ordered Runtime Chain Steps",
        "",
        f"Total ordered steps: **{len(ordered)}**",
        "",
        "```text",
    ]

    for step in ordered:
        lines.append(f"{step.order}. {step.step_id}")

    lines.extend(["```", ""])

    for step in ordered:
        lines.extend(
            [
                f"## {step.order}. {step.step_id}",
                "",
                f"- Category: `{step.category}`",
                f"- Score: `{step.score}`",
                f"- Evidence count: `{step.evidence_count}`",
                f"- Files: `{', '.join(step.files)}`",
                f"- Line range: `{step.line_min}-{step.line_max}`",
                f"- Order hint: `{step.order_hint}`",
                f"- Ordering reasons: `{', '.join(step.ordering_reasons)}`",
                f"- Representative pattern: `{step.representative_pattern}`",
                "",
                "```text",
                step.representative_text.strip(),
                "```",
                "",
            ]
        )

    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Order runtime-chain causal steps into propagation sequence.")
    ap.add_argument("--steps", required=True, type=Path)
    ap.add_argument("--out-json", required=True, type=Path)
    ap.add_argument("--out-md", required=True, type=Path)
    args = ap.parse_args()

    data = load_json(args.steps)
    steps = data.get("steps", [])
    if not isinstance(steps, list):
        raise SystemExit("steps must be a list")

    ordered = order_steps(steps)

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(
        json.dumps(
            {
                "schema": "runtime_chain_ordered_steps.v1",
                "source": args.steps.as_posix(),
                "total_ordered_steps": len(ordered),
                "ordered_steps": [asdict(x) for x in ordered],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    write_md(ordered, args.out_md)

    print(f"Ordered steps: {len(ordered)}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")


if __name__ == "__main__":
    main()