from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


STEP_PATTERNS = [
    ("vendor_purchase_detection", ["vendorsellitem", "oldinventory.vendor"]),
    ("vendor_metadata_cleanup", ["vendorsprice", "nil", "setdata"]),
    ("vendor_exit_metadata_cleanup", ["removereceiverfromvendor", "vendorsprice", "vendorbprice"]),
    ("inventory_membership_sync_send", ["syncitemadded", "nutinventoryadd", "item:sync", "getrecipients"]),
    ("inventory_membership_client_apply", ["nutinventoryadd", "inventoryitemadded", "net.receive"]),
    ("item_metadata_mutation", ["function item:setdata", "self.data[key]", "setdata"]),
    ("item_metadata_network_send", ["invdata", "netstream.start", "self:getowner"]),
    ("item_metadata_client_apply", ["netstream.hook", "invdata", "itemdatachanged"]),
    ("grid_inventory_item_refresh", ["inventoryitemdatachanged", "populateitems"]),
    ("grid_inventory_membership_refresh", ["inventoryitemadded", "inventoryitemremoved", "populateitems"]),
    ("vendor_item_metadata_assignment", ["vendoritemsetdata", "vendorqty", "vendorsprice", "vendormqty"]),
]

GENERIC_STEP_SUFFIXES = ("_related",)
SETUP_ONLY_STEPS = {"vendor_item_metadata_assignment"}


@dataclass
class RuntimeStep:
    rank: int
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
    reasons: list[str]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def clean_text(text: Any) -> str:
    return str(text or "").strip()


def norm(text: Any) -> str:
    return clean_text(text).lower().replace("\\", "/")


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def safe_line(v: Any) -> int | None:
    try:
        value = int(v)
        return value if value > 0 else None
    except Exception:
        return None


def evidence_blob(ev: dict[str, Any]) -> str:
    return compact(" ".join([
        norm(ev.get("file")),
        norm(ev.get("path")),
        norm(ev.get("source")),
        norm(ev.get("source_file")),
        norm(ev.get("pattern")),
        norm(ev.get("matched_terms")),
        norm(ev.get("text")),
        norm(ev.get("snippet")),
        norm(ev.get("fragment")),
        norm(ev.get("evidence")),
        norm(ev.get("content")),
        norm(ev.get("category")),
    ]))


def flatten(obj: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    def walk(x: Any) -> None:
        if isinstance(x, dict):
            b = evidence_blob(x)
            if b:
                out.append(x)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(obj)
    return out


def normalize_raw_ev(ev: dict[str, Any], source: Path) -> dict[str, Any]:
    text = (
        ev.get("text")
        or ev.get("snippet")
        or ev.get("fragment")
        or ev.get("evidence")
        or ev.get("content")
        or ""
    )
    file = ev.get("file") or ev.get("path") or ev.get("source_file") or ev.get("source") or ""
    pattern = ev.get("pattern") or ev.get("matched_terms") or ev.get("needle") or ""

    return {
        "rank": 9999,
        "score": 250,
        "category": "item_metadata_client_apply",
        "file": str(file),
        "line": ev.get("line") or ev.get("line_start") or ev.get("start_line"),
        "pattern": str(pattern),
        "text": str(text),
        "source": source.as_posix(),
        "reasons": ["recovered_from_validation_input"],
    }


def is_client_apply_ev(ev: dict[str, Any]) -> bool:
    b = evidence_blob(ev)
    return (
        "gamemode/core/libs/item/cl_networking.lua" in b
        or ("netstream.hook" in b and "invdata" in b)
        or ("itemdatachanged" in b and "invdata" in b)
        or ("hook.run" in b and "itemdatachanged" in b)
    )


def is_cleanup_blob(b: str) -> bool:
    return (
        "setdata" in b
        and "vendorsprice" in b
        and (" nil" in b or ",nil" in b or ", nil" in b or "vendorsprice\", nil" in b)
    )


def is_assignment_blob(b: str) -> bool:
    return (
        "vendoritemsetdata" in b
        or ("vendorsprice" in b and "setdata" in b and not is_cleanup_blob(b) and "price" in b)
    )


def classify_step(ev: dict[str, Any]) -> str:
    b = evidence_blob(ev)

    if is_client_apply_ev(ev):
        return "item_metadata_client_apply"

    if is_cleanup_blob(b):
        if "removereceiverfromvendor" in b:
            return "vendor_exit_metadata_cleanup"
        return "vendor_metadata_cleanup"

    if is_assignment_blob(b):
        return "vendor_item_metadata_assignment"

    for step_id, terms in STEP_PATTERNS:
        if step_id in {"vendor_metadata_cleanup", "vendor_item_metadata_assignment"}:
            continue
        hits = sum(1 for t in terms if t in b)
        if hits >= min(2, len(terms)):
            return step_id

    category = str(ev.get("category") or "unknown")
    if category == "inventory_membership":
        return "inventory_membership_related"
    if category == "item_metadata":
        return "item_metadata_related"
    if category == "network_send":
        return "network_send_related"
    if category == "network_receive":
        return "network_receive_related"
    if category == "ui_refresh":
        return "ui_refresh_related"

    return "incidental_related"


def should_drop_evidence(ev: dict[str, Any], drop_empty_text: bool, min_evidence_score: float) -> bool:
    score = float(ev.get("score") or 0)
    if score < min_evidence_score:
        return True
    if drop_empty_text and not clean_text(ev.get("text")) and safe_line(ev.get("line")) is None:
        return True
    return False


def choose_representative(evidence: list[dict[str, Any]]) -> dict[str, Any]:
    non_empty = [ev for ev in evidence if clean_text(ev.get("text"))]
    return sorted(non_empty or evidence, key=lambda x: float(x.get("score") or 0), reverse=True)[0]


def build_steps(
    ranked: list[dict[str, Any]],
    recovery_inputs: list[Path],
    min_score: float,
    min_evidence_score: float,
    max_evidence_per_step: int,
    drop_generic_related: bool,
    drop_empty_text: bool,
    drop_setup_only: bool,
) -> list[RuntimeStep]:
    groups: dict[str, list[dict[str, Any]]] = {}

    for ev in ranked:
        if should_drop_evidence(ev, drop_empty_text, min_evidence_score):
            continue

        step_id = classify_step(ev)

        if drop_setup_only and step_id in SETUP_ONLY_STEPS:
            continue
        if drop_generic_related and step_id.endswith(GENERIC_STEP_SUFFIXES):
            continue

        groups.setdefault(step_id, []).append(ev)

    if "item_metadata_client_apply" not in groups:
        recovered: list[dict[str, Any]] = []

        for path in recovery_inputs:
            data = load_json(path)
            for ev in flatten(data):
                if is_client_apply_ev(ev):
                    normalized = normalize_raw_ev(ev, path)
                    if clean_text(normalized.get("text")):
                        recovered.append(normalized)

        if recovered:
            groups["item_metadata_client_apply"] = recovered[:max_evidence_per_step]

    steps: list[RuntimeStep] = []

    for step_id, evidence in groups.items():
        evidence = sorted(evidence, key=lambda x: float(x.get("score") or 0), reverse=True)
        kept = evidence[:max_evidence_per_step]

        scores = [float(x.get("score") or 0) for x in kept]
        files = sorted({str(x.get("file") or "") for x in kept if x.get("file")})
        lines = [safe_line(x.get("line")) for x in kept]
        lines = [x for x in lines if x is not None]

        rep = choose_representative(kept)
        categories = [str(x.get("category") or "") for x in kept if x.get("category")]
        category = max(set(categories), key=categories.count) if categories else "unknown"

        final_score = max(scores) + (len(evidence) * 5)

        if step_id == "vendor_metadata_cleanup":
            final_score += 75
        elif step_id == "vendor_exit_metadata_cleanup":
            final_score += 15
        elif step_id == "item_metadata_client_apply":
            final_score += 75
        elif step_id in SETUP_ONLY_STEPS:
            final_score -= 100

        if final_score < min_score:
            continue

        reasons = [
            f"collapsed_from_evidence={len(evidence)}",
            f"kept_representative_evidence={len(kept)}",
            f"category={category}",
        ]

        if step_id == "item_metadata_client_apply":
            reasons.append("client_invdata_apply_recovered=true")

        steps.append(RuntimeStep(
            rank=0,
            step_id=step_id,
            category=category,
            score=final_score,
            evidence_count=len(evidence),
            files=files,
            line_min=min(lines) if lines else None,
            line_max=max(lines) if lines else None,
            representative_pattern=str(rep.get("pattern") or ""),
            representative_text=str(rep.get("text") or "")[:2000],
            evidence_ranks=[int(x.get("rank") or 0) for x in kept],
            reasons=reasons,
        ))

    steps.sort(key=lambda x: x.score, reverse=True)

    for i, step in enumerate(steps, 1):
        step.rank = i

    return steps


def write_md(steps: list[RuntimeStep], out: Path) -> None:
    lines = ["# Runtime Chain Steps", "", f"Total runtime steps: **{len(steps)}**", ""]
    for step in steps:
        lines.extend([
            f"## {step.rank}. {step.step_id} — score {step.score:.2f}",
            "",
            f"- Category: `{step.category}`",
            f"- Evidence count: `{step.evidence_count}`",
            f"- Files: `{', '.join(step.files)}`",
            f"- Line range: `{step.line_min}-{step.line_max}`",
            f"- Evidence ranks: `{step.evidence_ranks}`",
            f"- Representative pattern: `{step.representative_pattern}`",
            f"- Reasons: `{', '.join(step.reasons)}`",
            "",
            "```text",
            step.representative_text.strip(),
            "```",
            "",
        ])
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ranked-evidence", required=True, type=Path)
    ap.add_argument("--recovery-input", nargs="*", type=Path, default=[])
    ap.add_argument("--out-json", required=True, type=Path)
    ap.add_argument("--out-md", required=True, type=Path)
    ap.add_argument("--min-score", type=float, default=120.0)
    ap.add_argument("--min-evidence-score", type=float, default=120.0)
    ap.add_argument("--max-evidence-per-step", type=int, default=5)
    ap.add_argument("--drop-generic-related", action="store_true")
    ap.add_argument("--drop-empty-text", action="store_true")
    ap.add_argument("--drop-setup-only", action="store_true")
    args = ap.parse_args()

    data = load_json(args.ranked_evidence)
    ranked = data.get("ranked_evidence", [])
    if not isinstance(ranked, list):
        raise SystemExit("ranked_evidence must be a list")

    steps = build_steps(
        ranked=ranked,
        recovery_inputs=args.recovery_input,
        min_score=args.min_score,
        min_evidence_score=args.min_evidence_score,
        max_evidence_per_step=args.max_evidence_per_step,
        drop_generic_related=args.drop_generic_related,
        drop_empty_text=args.drop_empty_text,
        drop_setup_only=args.drop_setup_only,
    )

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(json.dumps({
        "schema": "runtime_chain_steps.v4",
        "source": args.ranked_evidence.as_posix(),
        "recovery_inputs": [p.as_posix() for p in args.recovery_input],
        "total_steps": len(steps),
        "steps": [asdict(x) for x in steps],
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    write_md(steps, args.out_md)

    print(f"Runtime steps: {len(steps)}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")


if __name__ == "__main__":
    main()