from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


PIPELINE_CONTRACT = {
    "script_id": "scripts.tools.cleanup_pipeline_artifacts",
    "purpose": "Plan and optionally delete non-canonical/debug/failed/intermediate pipeline artifacts to reduce contract registry noise.",
    "pipeline_stage": "tooling",
    "input_schemas": ["pipeline_artifact_contract.v1"],
    "output_schemas": ["pipeline_cleanup_plan.v1"],
    "artifact_patterns": [
        "investigations/validation/pipeline_cleanup_plan_v1.json",
        "investigations/validation/pipeline_cleanup_plan_v1.md",
    ],
    "promotion_role": "context_or_debug",
    "canonical_status": "active",
}


KEEP_STATUSES = {"canonical"}
DELETE_STATUSES = {"debug", "failed"}

KEEP_KEYWORDS = {
    "vendor_purchase_itemdata_v6",
    "vendor_purchase_itemdata_runtime_chain_candidate_v6",
    "vendor_purchase_itemdata_promotion_validation",
    "vendor_purchase_itemdata_full_chain",
    "vendor_purchase_itemdata_ordered_runtime_facts",
    "vendor_purchase_itemdata_runtime_facts_v2",
    "vendor_purchase_itemdata_runtime_fact",
    "pipeline_contract_check",
    "pipeline_artifact_contract",
    "runtime_propagation_topology",
    "qdrant_documents",
    "qdrant_embeddings",
    "qdrant_embedding_summary",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def should_keep(path: str, status: str, role: str) -> tuple[bool, str]:
    lowered = path.lower()

    if status in KEEP_STATUSES:
        return True, "canonical artifact"

    if any(keyword in lowered for keyword in KEEP_KEYWORDS):
        return True, "protected keyword"

    if role == "promotion_core" and status not in DELETE_STATUSES:
        return True, "promotion-core artifact not explicitly debug/failed"

    if path.startswith("docs/runtime/runtime_chains/") and "promoted_confirmed_chain" in lowered:
        return True, "confirmed promoted runtime chain"

    return False, ""


def cleanup_reason(path: str, status: str, stage: str, role: str) -> str | None:
    lowered = path.lower()

    keep, _ = should_keep(path, status, role)
    if keep:
        return None

    if status in DELETE_STATUSES:
        return f"status={status}"

    if "not_promoted" in lowered:
        return "not_promoted artifact"

    if "generic_runtime_facts" in lowered:
        return "generic runtime facts artifact"

    if "debug" in lowered or "diagnosis" in lowered:
        return "debug/diagnosis artifact"

    if stage in {"probe", "diagnosis"}:
        return f"transient stage={stage}"

    return None


def render_md(plan: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Pipeline Cleanup Plan V1")
    lines.append("")
    lines.append(f"- Generated at: `{plan['generated_at']}`")
    lines.append(f"- Workspace: `{plan['workspace']}`")
    lines.append(f"- Apply mode: `{plan['apply']}`")
    lines.append(f"- Archive mode: `{plan['archive']}`")
    lines.append(f"- Candidates: `{len(plan['candidates'])}`")
    lines.append(f"- Deleted: `{len(plan['deleted'])}`")
    lines.append("")
    lines.append("## Candidates")
    lines.append("")
    lines.append("| Path | Reason | Status | Stage | Role |")
    lines.append("|---|---|---|---|---|")
    for item in plan["candidates"]:
        lines.append(
            f"| `{item['path']}` | {item['reason']} | `{item['canonical_status']}` | `{item['pipeline_stage']}` | `{item['promotion_role']}` |"
        )
    lines.append("")
    lines.append("## Protected")
    lines.append("")
    lines.append("| Path | Reason |")
    lines.append("|---|---|")
    for item in plan["protected"]:
        lines.append(f"| `{item['path']}` | {item['reason']} |")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", type=Path, required=True)
    ap.add_argument(
        "--contract",
        type=Path,
        default=Path("docs/runtime/pipeline_artifact_contract.json"),
    )
    ap.add_argument(
        "--out-json",
        type=Path,
        default=Path("investigations/validation/pipeline_cleanup_plan_v1.json"),
    )
    ap.add_argument(
        "--out-md",
        type=Path,
        default=Path("investigations/validation/pipeline_cleanup_plan_v1.md"),
    )
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--archive", action="store_true")
    ap.add_argument(
        "--archive-dir",
        type=Path,
        default=Path("_archive/pipeline_cleanup"),
    )
    args = ap.parse_args()

    workspace = args.workspace.resolve()
    contract_path = workspace / args.contract

    contract = load_json(contract_path)

    candidates: list[dict[str, Any]] = []
    protected: list[dict[str, Any]] = []
    deleted: list[str] = []
    missing: list[str] = []

    for artifact in contract.get("artifacts", []):
        path = artifact.get("path")
        if not isinstance(path, str):
            continue

        status = str(artifact.get("canonical_status") or "unknown")
        stage = str(artifact.get("pipeline_stage") or "unknown")
        role = str(artifact.get("promotion_role") or "context_or_debug")

        keep, keep_reason = should_keep(path, status, role)
        if keep:
            protected.append({"path": path, "reason": keep_reason})
            continue

        reason = cleanup_reason(path, status, stage, role)
        if not reason:
            continue

        full_path = workspace / path
        item = {
            "path": path,
            "reason": reason,
            "canonical_status": status,
            "pipeline_stage": stage,
            "promotion_role": role,
            "exists": full_path.exists(),
        }
        candidates.append(item)

        if not full_path.exists():
            missing.append(path)
            continue

        if args.apply:
            if args.archive:
                target = workspace / args.archive_dir / path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(full_path), str(target))
            else:
                full_path.unlink()

            deleted.append(path)

    plan = {
        "schema": "pipeline_cleanup_plan.v1",
        "producer_script": "scripts.tools.cleanup_pipeline_artifacts",
        "pipeline_stage": "tooling",
        "promotion_role": "context_or_debug",
        "canonical_status": "intermediate",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "workspace": str(workspace),
        "contract": str(args.contract).replace("\\", "/"),
        "apply": args.apply,
        "archive": args.archive,
        "archive_dir": str(args.archive_dir).replace("\\", "/"),
        "candidates": candidates,
        "protected": protected,
        "deleted": deleted,
        "missing": missing,
    }

    out_json = workspace / args.out_json
    out_md = workspace / args.out_md

    write_json(out_json, plan)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_md(plan), encoding="utf-8")

    print(f"Wrote JSON: {out_json.relative_to(workspace)}")
    print(f"Wrote MD:   {out_md.relative_to(workspace)}")
    print(f"Candidates: {len(candidates)}")
    print(f"Deleted:    {len(deleted)}")
    print(f"Protected:  {len(protected)}")
    print(f"Apply:      {args.apply}")


if __name__ == "__main__":
    main()