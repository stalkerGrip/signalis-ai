from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


BRANCH_RULES = {
    "membership": {
        "label": "Inventory membership propagation",
        "steps": [
            "inventory_membership_sync_send",
            "inventory_membership_client_apply",
            "grid_inventory_membership_refresh",
        ],
    },
    "metadata": {
        "label": "Item metadata propagation",
        "steps": [
            "vendor_metadata_cleanup",
            "item_metadata_mutation",
            "item_metadata_network_send",
            "item_metadata_client_apply",
            "grid_inventory_item_refresh",
        ],
    },
    "exit_cleanup": {
        "label": "Vendor exit cleanup",
        "steps": [
            "vendor_exit_metadata_cleanup",
        ],
        "secondary": True,
    },
}


@dataclass
class BranchStep:
    step_id: str
    order: int
    category: str
    score: float
    evidence_count: int
    files: list[str]
    representative_pattern: str


@dataclass
class RuntimeBranch:
    branch_id: str
    label: str
    secondary: bool
    steps: list[BranchStep]
    score: float
    evidence_count: int
    missing_steps: list[str]


@dataclass
class BranchChain:
    root: str
    branches: list[RuntimeBranch]
    join: str
    confidence: str
    score: float
    missing_required_steps: list[str]
    notes: list[str]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def step_map(ordered_steps: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(s.get("step_id")): s for s in ordered_steps}


def branch_step(s: dict[str, Any]) -> BranchStep:
    return BranchStep(
        step_id=str(s.get("step_id") or ""),
        order=int(s.get("order") or 0),
        category=str(s.get("category") or ""),
        score=float(s.get("score") or 0),
        evidence_count=int(s.get("evidence_count") or 0),
        files=list(s.get("files") or []),
        representative_pattern=str(s.get("representative_pattern") or ""),
    )


def build_branch(branch_id: str, rule: dict[str, Any], steps_by_id: dict[str, dict[str, Any]]) -> RuntimeBranch:
    found: list[BranchStep] = []
    missing: list[str] = []

    for sid in rule["steps"]:
        raw = steps_by_id.get(sid)
        if raw:
            found.append(branch_step(raw))
        else:
            missing.append(sid)

    found.sort(key=lambda s: s.order)

    return RuntimeBranch(
        branch_id=branch_id,
        label=str(rule["label"]),
        secondary=bool(rule.get("secondary", False)),
        steps=found,
        score=sum(s.score for s in found),
        evidence_count=sum(s.evidence_count for s in found),
        missing_steps=missing,
    )


def infer_confidence(branches: list[RuntimeBranch]) -> tuple[str, float, list[str]]:
    notes: list[str] = []

    required = [b for b in branches if not b.secondary]
    secondary = [b for b in branches if b.secondary]

    required_missing = []
    for b in required:
        required_missing.extend([f"{b.branch_id}:{s}" for s in b.missing_steps])

    total_required_steps = sum(len(BRANCH_RULES[b.branch_id]["steps"]) for b in required)
    present_required_steps = sum(len(b.steps) for b in required)

    coverage = present_required_steps / total_required_steps if total_required_steps else 0.0

    if coverage >= 0.95 and not required_missing:
        confidence = "high"
        notes.append("all required branch steps present")
    elif coverage >= 0.70:
        confidence = "medium"
        notes.append("required branch coverage sufficient but not complete")
    else:
        confidence = "low"
        notes.append("required branch coverage incomplete")

    if secondary:
        notes.append("secondary branches do not block primary chain confidence")

    return confidence, round(coverage, 4), notes


def build_chain(ordered_steps: list[dict[str, Any]], root: str, join: str) -> BranchChain:
    steps_by_id = step_map(ordered_steps)
    branches = [
        build_branch(branch_id, rule, steps_by_id)
        for branch_id, rule in BRANCH_RULES.items()
    ]

    confidence, coverage, notes = infer_confidence(branches)

    missing_required = []
    for b in branches:
        if not b.secondary:
            missing_required.extend([f"{b.branch_id}:{s}" for s in b.missing_steps])

    return BranchChain(
        root=root,
        branches=branches,
        join=join,
        confidence=confidence,
        score=coverage,
        missing_required_steps=missing_required,
        notes=notes,
    )


def write_md(chain: BranchChain, out: Path) -> None:
    lines = [
        "# Branch-Aware Runtime Chain",
        "",
        f"- Root: `{chain.root}`",
        f"- Join: `{chain.join}`",
        f"- Confidence: `{chain.confidence}`",
        f"- Score: `{chain.score}`",
        f"- Missing required steps: `{chain.missing_required_steps or 'none'}`",
        "",
        "## Branch Topology",
        "",
        "```text",
        chain.root,
    ]

    for branch in chain.branches:
        branch_prefix = "└─" if branch == chain.branches[-1] else "├─"
        suffix = " (secondary)" if branch.secondary else ""
        lines.append(f"{branch_prefix} {branch.branch_id}: {branch.label}{suffix}")
        for idx, step in enumerate(branch.steps):
            step_prefix = "   └─" if idx == len(branch.steps) - 1 else "   ├─"
            lines.append(f"{step_prefix} {step.step_id}")
        if branch.missing_steps:
            for missing in branch.missing_steps:
                lines.append(f"   ! missing: {missing}")

    lines.extend(
        [
            chain.join,
            "```",
            "",
        ]
    )

    for branch in chain.branches:
        lines.extend(
            [
                f"## Branch: {branch.branch_id}",
                "",
                f"- Label: `{branch.label}`",
                f"- Secondary: `{branch.secondary}`",
                f"- Score: `{branch.score}`",
                f"- Evidence count: `{branch.evidence_count}`",
                f"- Missing steps: `{branch.missing_steps or 'none'}`",
                "",
            ]
        )

        for step in branch.steps:
            lines.extend(
                [
                    f"### {step.step_id}",
                    "",
                    f"- Order: `{step.order}`",
                    f"- Category: `{step.category}`",
                    f"- Score: `{step.score}`",
                    f"- Evidence count: `{step.evidence_count}`",
                    f"- Files: `{', '.join(step.files)}`",
                    f"- Representative pattern: `{step.representative_pattern}`",
                    "",
                ]
            )

    lines.extend(["## Notes", ""])
    lines.extend([f"- {n}" for n in chain.notes])

    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build branch-aware runtime chain from ordered runtime steps.")
    ap.add_argument("--ordered-steps", required=True, type=Path)
    ap.add_argument("--out-json", required=True, type=Path)
    ap.add_argument("--out-md", required=True, type=Path)
    ap.add_argument("--root", default="vendor purchase transfer")
    ap.add_argument("--join", default="client grid inventory UI refresh")
    args = ap.parse_args()

    data = load_json(args.ordered_steps)
    ordered_steps = data.get("ordered_steps", [])
    if not isinstance(ordered_steps, list):
        raise SystemExit("ordered_steps must be a list")

    chain = build_chain(ordered_steps, args.root, args.join)

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(
        json.dumps(
            {
                "schema": "runtime_branch_chain.v1",
                "source": args.ordered_steps.as_posix(),
                **asdict(chain),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    write_md(chain, args.out_md)

    print(f"Branch chain confidence: {chain.confidence}")
    print(f"Branch chain score: {chain.score}")
    print(f"Missing required steps: {chain.missing_required_steps or 'none'}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")


if __name__ == "__main__":
    main()