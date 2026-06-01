from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path


PIPELINE_CONTRACT = {
    "script_id": "scripts.tools.classify_pipeline_artifacts",
    "purpose": "Classify pipeline artifacts into keep/archive/delete groups by benchmark, family, version, promotion relevance, and canonical status.",
    "pipeline_stage": "tooling",
    "input_schemas": ["pipeline_artifact_contract.v1"],
    "output_schemas": ["pipeline_artifact_classification.v1"],
    "artifact_patterns": [
        "investigations/validation/pipeline_artifact_classification_v1.json",
        "investigations/validation/pipeline_artifact_classification_v1.md",
    ],
    "promotion_role": "context_or_debug",
    "canonical_status": "active",
}


KEEP_PATTERNS = [
    "pipeline_contract_check_v1",
    "pipeline_artifact_contract",
    "pipeline_cleanup_plan_v1",
    "pipeline_artifact_classification_v1",

    "vendor_purchase_itemdata_full_chain",
    "vendor_purchase_itemdata_runtime_chain_candidate_v6",
    "vendor_purchase_itemdata_v6_promotion_validation",
    "vendor_purchase_itemdata_v6_promotion_decision",

    "characterload_inventory_runtime_chain_candidate_v5",
    "characterload_inventory_runtime_fact_topology_v3",
    "runtime_propagation_topology",
    "qdrant_documents",
    "qdrant_embeddings",
    "qdrant_embedding_summary",
    "qdrant_ingest_summary",
    "vendor_purchase_chain",
    "vendor_purchase_item_metadata_sync",
    "vendor_purchase_price_label_cleanup",
    ]

DELETE_PATTERNS = [
    "debug",
    "diagnosis",
    "not_promoted",
]

ARCHIVE_PATTERNS = [
    "_v1",
    "_v2",
    "_v3",
    "_v4",
    "_v5",
    "_fix1",
    "_pipeline",
    "generic_runtime_facts",
    "branch_chain",
    "ordered_steps",
    "runtime_steps",
    "ranked_evidence",
    "pathfinder",
    "node_search",
    "graph_audit",
    "stale_price_label_after_purchase",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def version_number(name: str) -> int:
    found = re.findall(r"_v(\d+)", name)
    return max([int(x) for x in found], default=0)


def family_key(name: str) -> str:
    stem = Path(name).stem
    stem = re.sub(r"_v\d+", "", stem)
    stem = stem.replace("_fix1", "")
    return stem


def matches(name: str, patterns: list[str]) -> bool:
    lowered = name.lower()
    return any(p.lower() in lowered for p in patterns)


def classify(path: str, artifact: dict) -> tuple[str, str]:
    name = Path(path).name
    status = str(artifact.get("canonical_status") or "").lower()
    role = str(artifact.get("promotion_role") or "").lower()

    if status == "canonical":
        return "keep", "canonical status"

    if matches(name, KEEP_PATTERNS):
        return "keep", "protected current/canonical lineage"

    if status in {"debug", "failed"}:
        return "delete", f"status={status}"

    if matches(name, DELETE_PATTERNS):
        return "delete", "debug/diagnosis/not_promoted artifact"

    if role == "promotion_core":
        return "review", "promotion_core but not protected"

    if matches(name, ARCHIVE_PATTERNS):
        return "archive", "historical version/intermediate artifact"

    return "review", "unclassified"


def render_md(report: dict) -> str:
    lines = []
    lines.append("# Pipeline Artifact Classification V1")
    lines.append("")
    lines.append(f"- Generated at: `{report['generated_at']}`")
    lines.append(f"- Apply: `{report['apply']}`")
    lines.append(f"- Archive dir: `{report['archive_dir']}`")
    lines.append("")
    for bucket in ["keep", "archive", "delete", "review", "missing"]:
        lines.append(f"- {bucket}: `{len(report[bucket])}`")
    lines.append("")

    for bucket in ["keep", "archive", "delete", "review", "missing"]:
        lines.append(f"## {bucket.upper()}")
        lines.append("")
        lines.append("| Path | Reason |")
        lines.append("|---|---|")
        for item in report[bucket]:
            lines.append(f"| `{item['path']}` | {item['reason']} |")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True, type=Path)
    ap.add_argument(
        "--contract",
        default=Path("docs/runtime/pipeline_artifact_contract.json"),
        type=Path,
    )
    ap.add_argument(
        "--out-json",
        default=Path("investigations/validation/pipeline_artifact_classification_v1.json"),
        type=Path,
    )
    ap.add_argument(
        "--out-md",
        default=Path("investigations/validation/pipeline_artifact_classification_v1.md"),
        type=Path,
    )
    ap.add_argument(
        "--archive-dir",
        default=Path(r"E:\signalis_ai_archive\pipeline_artifacts"),
        type=Path,
    )
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--delete", action="store_true")
    args = ap.parse_args()

    workspace = args.workspace.resolve()
    contract = load_json(workspace / args.contract)

    buckets = {
        "keep": [],
        "archive": [],
        "delete": [],
        "review": [],
        "missing": [],
    }

    artifacts = contract.get("artifacts", [])

    for artifact in artifacts:
        path = artifact.get("path")
        if not isinstance(path, str):
            continue

        full = workspace / path
        if not full.exists():
            buckets["missing"].append({"path": path, "reason": "registered but missing on disk"})
            continue

        bucket, reason = classify(path, artifact)
        buckets[bucket].append({"path": path, "reason": reason})

    # Keep only newest version in each family; archive older same-family artifacts.
    by_family = defaultdict(list)
    for item in list(buckets["review"]):
        by_family[family_key(item["path"])].append(item)

    for family, items in by_family.items():
        if len(items) <= 1:
            continue

        newest = max(items, key=lambda x: version_number(x["path"]))
        for item in items:
            if item is newest:
                continue
            buckets["review"].remove(item)
            item["reason"] = f"older version in family `{family}`"
            buckets["archive"].append(item)

    if args.apply:
        for item in buckets["archive"]:
            src = workspace / item["path"]
            dst = args.archive_dir / item["path"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))

        if args.delete:
            for item in buckets["delete"]:
                src = workspace / item["path"]
                if src.exists():
                    src.unlink()

    report = {
        "schema": "pipeline_artifact_classification.v1",
        "producer_script": "scripts.tools.classify_pipeline_artifacts",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "workspace": str(workspace),
        "contract": str(args.contract).replace("\\", "/"),
        "archive_dir": str(args.archive_dir),
        "apply": args.apply,
        "delete_enabled": args.delete,
        **buckets,
    }

    out_json = workspace / args.out_json
    out_md = workspace / args.out_md
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    out_md.write_text(render_md(report), encoding="utf-8")

    print(f"Wrote JSON: {out_json.relative_to(workspace)}")
    print(f"Wrote MD:   {out_md.relative_to(workspace)}")
    print(f"Keep:       {len(buckets['keep'])}")
    print(f"Archive:    {len(buckets['archive'])}")
    print(f"Delete:     {len(buckets['delete'])}")
    print(f"Review:     {len(buckets['review'])}")
    print(f"Missing:    {len(buckets['missing'])}")
    print(f"Apply:      {args.apply}")


if __name__ == "__main__":
    main()