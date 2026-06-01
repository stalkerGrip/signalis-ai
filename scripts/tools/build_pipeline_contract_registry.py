from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


CONTRACT_SCHEMA = "pipeline_artifact_contract.v1"

SCRIPT_DIRS = [
    Path("scripts/investigation"),
    Path("scripts/qdrant"),
    Path("scripts/extraction"),
    Path("scripts/normalization"),
]

ARTIFACT_DIRS = [
    Path("investigations/validation"),
    Path("docs/runtime/runtime_chains"),
    Path("manifests/normalized"),
    Path("manifests/semantic"),
]

ALLOWED_STATUSES = [
    "canonical",
    "active",
    "intermediate",
    "debug",
    "legacy",
    "superseded",
    "failed",
    "unknown",
]

ALLOWED_PROMOTION_ROLES = [
    "promotion_core",
    "promotion_support",
    "context_or_debug",
    "not_promotion_relevant",
]


# Future explicit flag format inside scripts:
#
# PIPELINE_CONTRACT = {
#   "script_id": "...",
#   "purpose": "...",
#   "pipeline_stage": "...",
#   "input_schemas": [...],
#   "output_schemas": [...],
#   "artifact_patterns": [...],
#   "promotion_role": "...",
#   "canonical_status": "active"
# }
#
# Future explicit flag format inside JSON artifacts:
#
# {
#   "schema": "...",
#   "producer_script": "scripts.investigation.example",
#   "pipeline_stage": "...",
#   "benchmark": "...",
#   "promotion_role": "...",
#   "canonical_status": "...",
#   "inputs": [...]
# }


@dataclass
class ScriptContract:
    script_id: str
    path: str
    module: str
    purpose: str
    pipeline_stage: str
    input_schemas: list[str]
    output_schemas: list[str]
    artifact_patterns: list[str]
    promotion_role: str
    canonical_status: str
    source: str


@dataclass
class ArtifactContract:
    artifact_id: str
    path: str
    schema: str | None
    producer_script: str | None
    pipeline_stage: str
    benchmark: str
    promotion_role: str
    canonical_status: str
    inputs: list[str]
    source: str


def read_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def module_from_path(path: Path) -> str:
    return ".".join(path.with_suffix("").parts)


def slug(value: str) -> str:
    value = value.replace("\\", "/")
    value = re.sub(r"[^a-zA-Z0-9_.:/-]+", "_", value)
    return value.strip("_")


def extract_pipeline_contract_from_script(path: Path) -> dict[str, Any] | None:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except SyntaxError:
        return None

    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue

        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "PIPELINE_CONTRACT":
                try:
                    value = ast.literal_eval(node.value)
                    if isinstance(value, dict):
                        return value
                except Exception:
                    return None

    return None


def infer_stage_from_name(name: str) -> str:
    n = name.lower()

    rules = [
        ("target", "targeted_validation_request"),
        ("source_validation", "source_validation"),
        ("ranked_evidence", "ranked_evidence"),
        ("runtime_steps", "runtime_steps"),
        ("ordered_steps", "ordered_steps"),
        ("ordered_runtime_facts", "ordered_runtime_facts"),
        ("runtime_facts", "runtime_facts"),
        ("runtime_fact_graph", "runtime_fact_graph"),
        ("runtime_fact_topology", "runtime_fact_topology"),
        ("runtime_chain_candidate", "runtime_chain_candidate"),
        ("runtime_chain_regression", "runtime_chain_regression"),
        ("runtime_chain_promoter", "promotion"),
        ("promote_", "promotion"),
        ("promoted", "promotion_output"),
        ("not_promoted", "promotion_output"),
        ("probe", "probe"),
        ("diagnos", "diagnosis"),
        ("extract_", "extraction"),
        ("normalize_", "normalization"),
        ("build_", "builder"),
        ("query_qdrant", "retrieval"),
        ("embed_", "embedding"),
        ("ingest_", "ingestion"),
    ]

    for needle, stage in rules:
        if needle in n:
            return stage

    return "unknown"


def infer_benchmark_from_name(name: str) -> str:
    n = name.lower()

    if n.startswith("vendor_purchase_itemdata"):
        return "vendor_purchase_itemdata"
    if n.startswith("vendor_stale_price_label"):
        return "vendor_stale_price_label_after_purchase"
    if n.startswith("vendor_purchase_price_label"):
        return "vendor_purchase_price_label_cleanup"
    if n.startswith("characterload_inventory") or "playerloadedchar" in n:
        return "characterload_inventory"
    if n.startswith("runtime_chain_regression") or n.startswith("runtime_fact_topology_regression"):
        return "global_regression"
    if n.startswith("probe_") or n.startswith("debug_"):
        return "topology_debug"
    if "runtime_propagation_topology" in n:
        return "runtime_topology"
    if "runtime_topology" in n:
        return "runtime_topology"
    if "network" in n:
        return "networking"
    if "hook" in n:
        return "hooks"
    if "timer" in n:
        return "timers"

    return "unknown"


def infer_promotion_role(stage: str, path: str) -> str:
    p = path.lower()

    if stage in {
        "source_validation",
        "runtime_facts",
        "ordered_runtime_facts",
        "runtime_fact_graph",
        "runtime_fact_topology",
        "runtime_chain_candidate",
        "promotion_output",
    }:
        return "promotion_core"

    if stage in {
        "targeted_validation_request",
        "runtime_steps",
        "ordered_steps",
        "runtime_chain_regression",
        "pathfinder",
    }:
        return "promotion_support"

    if "docs/runtime/runtime_chains" in p:
        return "promotion_core"

    return "context_or_debug"


def infer_status(path: str, stage: str) -> str:
    p = path.lower()

    if "not_promoted" in p:
        return "failed"
    if "debug" in p or "probe" in p or "diagnosis" in p:
        return "debug"
    if "generic" in p or "legacy" in p:
        return "intermediate"
    if "regenerated" in p and "confidence_none" in p:
        return "failed"
    if "docs/runtime/runtime_chains" in p and "promoted" in p:
        return "canonical"
    if stage in {"runtime_topology", "runtime_propagation_topology"}:
        return "canonical"

    return "intermediate"


def extract_schemas_from_script_text(text: str) -> tuple[list[str], list[str]]:
    schemas = sorted(set(re.findall(r"[a-zA-Z0-9_.-]+\.v\d+", text)))
    output_schemas = [s for s in schemas if any(key in s for key in ["runtime", "targeted", "pipeline", "chain"])]
    return schemas, output_schemas


def extract_artifact_patterns_from_script_text(text: str) -> list[str]:
    patterns: set[str] = set()

    for match in re.findall(r"['\"]([^'\"]+\.(?:json|md|jsonl))['\"]", text):
        if any(prefix in match for prefix in ["investigations/", "manifests/", "docs/"]):
            patterns.add(match.replace("\\", "/"))

    return sorted(patterns)


def discover_scripts(workspace: Path) -> list[ScriptContract]:
    results: list[ScriptContract] = []

    for script_dir in SCRIPT_DIRS:
        root = workspace / script_dir
        if not root.exists():
            continue

        for path in sorted(root.rglob("*.py")):
            if path.name == "__init__.py":
                continue

            rel = path.relative_to(workspace)
            rel_str = str(rel).replace("\\", "/")
            module = module_from_path(rel)
            text = path.read_text(encoding="utf-8", errors="ignore")

            explicit = extract_pipeline_contract_from_script(path)

            if explicit:
                results.append(
                    ScriptContract(
                        script_id=str(explicit.get("script_id") or module),
                        path=rel_str,
                        module=str(explicit.get("module") or module),
                        purpose=str(explicit.get("purpose") or ""),
                        pipeline_stage=str(explicit.get("pipeline_stage") or infer_stage_from_name(path.name)),
                        input_schemas=list(explicit.get("input_schemas") or []),
                        output_schemas=list(explicit.get("output_schemas") or []),
                        artifact_patterns=list(explicit.get("artifact_patterns") or []),
                        promotion_role=str(explicit.get("promotion_role") or "context_or_debug"),
                        canonical_status=str(explicit.get("canonical_status") or "active"),
                        source="explicit_script_flag",
                    )
                )
                continue

            input_schemas, output_schemas = extract_schemas_from_script_text(text)

            results.append(
                ScriptContract(
                    script_id=module,
                    path=rel_str,
                    module=module,
                    purpose=f"Inferred registry entry for {module}.",
                    pipeline_stage=infer_stage_from_name(path.name),
                    input_schemas=input_schemas,
                    output_schemas=output_schemas,
                    artifact_patterns=extract_artifact_patterns_from_script_text(text),
                    promotion_role=infer_promotion_role(infer_stage_from_name(path.name), rel_str),
                    canonical_status="active",
                    source="inferred_from_script",
                )
            )

    return results


def extract_inputs(data: Any) -> list[str]:
    refs: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, str):
            normalized = value.replace("\\", "/")
            if (
                normalized.endswith(".json")
                or normalized.endswith(".md")
                or normalized.endswith(".jsonl")
                or normalized.startswith("investigations/")
                or normalized.startswith("docs/")
                or normalized.startswith("manifests/")
            ):
                refs.add(normalized)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, dict):
            for item in value.values():
                walk(item)

    walk(data)
    return sorted(refs)


def artifact_explicit_metadata(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        return {}

    metadata = {}

    for key in [
        "artifact_id",
        "producer_script",
        "pipeline_stage",
        "benchmark",
        "promotion_role",
        "canonical_status",
        "inputs",
    ]:
        if key in data:
            metadata[key] = data[key]

    if isinstance(data.get("pipeline_contract"), dict):
        metadata.update(data["pipeline_contract"])

    return metadata


def discover_artifacts(workspace: Path) -> list[ArtifactContract]:
    results: list[ArtifactContract] = []

    for artifact_dir in ARTIFACT_DIRS:
        root = workspace / artifact_dir
        if not root.exists():
            continue

        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".txt", ".jsonl"}:
                continue

            rel_str = str(path.relative_to(workspace)).replace("\\", "/")
            data = read_json(path) if path.suffix.lower() == ".json" else None
            explicit = artifact_explicit_metadata(data)

            schema = None
            if isinstance(data, dict) and isinstance(data.get("schema"), str):
                schema = data["schema"]

            stage = str(explicit.get("pipeline_stage") or infer_stage_from_name(path.name))
            benchmark = str(explicit.get("benchmark") or infer_benchmark_from_name(path.name))
            role = str(explicit.get("promotion_role") or infer_promotion_role(stage, rel_str))
            status = str(explicit.get("canonical_status") or infer_status(rel_str, stage))

            inputs = explicit.get("inputs")
            if not isinstance(inputs, list):
                inputs = extract_inputs(data)

            artifact_id = str(explicit.get("artifact_id") or slug(rel_str))
            producer = explicit.get("producer_script")
            if not isinstance(producer, str):
                producer = None

            source = "explicit_artifact_flag" if explicit else "inferred_from_artifact"

            results.append(
                ArtifactContract(
                    artifact_id=artifact_id,
                    path=rel_str,
                    schema=schema,
                    producer_script=producer,
                    pipeline_stage=stage,
                    benchmark=benchmark,
                    promotion_role=role,
                    canonical_status=status,
                    inputs=sorted(str(x).replace("\\", "/") for x in inputs),
                    source=source,
                )
            )

    return results


def merge_existing_curations(
    generated: dict[str, Any],
    existing: dict[str, Any] | None,
) -> dict[str, Any]:
    if not isinstance(existing, dict):
        return generated

    existing_scripts = {
        entry.get("path"): entry
        for entry in existing.get("scripts", [])
        if isinstance(entry, dict) and isinstance(entry.get("path"), str)
    }

    existing_artifacts = {
        entry.get("path"): entry
        for entry in existing.get("artifacts", [])
        if isinstance(entry, dict) and isinstance(entry.get("path"), str)
    }

    for entry in generated["scripts"]:
        old = existing_scripts.get(entry["path"])
        if not old:
            continue

        for key in [
            "purpose",
            "pipeline_stage",
            "input_schemas",
            "output_schemas",
            "artifact_patterns",
            "promotion_role",
            "canonical_status",
        ]:
            if key in old and old[key] not in (None, "", [], {}):
                entry[key] = old[key]

        entry["source"] = "merged_existing_curation"

    for entry in generated["artifacts"]:
        old = existing_artifacts.get(entry["path"])
        if not old:
            continue

        for key in [
            "producer_script",
            "pipeline_stage",
            "benchmark",
            "promotion_role",
            "canonical_status",
            "inputs",
        ]:
            if key in old and old[key] not in (None, "", [], {}):
                entry[key] = old[key]

        entry["source"] = "merged_existing_curation"

    return generated


def render_md(contract: dict[str, Any]) -> str:
    scripts = contract["scripts"]
    artifacts = contract["artifacts"]

    scripts_by_stage: dict[str, int] = {}
    artifacts_by_stage: dict[str, int] = {}
    artifacts_by_status: dict[str, int] = {}

    for s in scripts:
        scripts_by_stage[s["pipeline_stage"]] = scripts_by_stage.get(s["pipeline_stage"], 0) + 1

    for a in artifacts:
        artifacts_by_stage[a["pipeline_stage"]] = artifacts_by_stage.get(a["pipeline_stage"], 0) + 1
        artifacts_by_status[a["canonical_status"]] = artifacts_by_status.get(a["canonical_status"], 0) + 1

    lines = [
        "# Pipeline Artifact Contract Registry",
        "",
        f"- Schema: `{contract['schema']}`",
        f"- Generated at: `{contract['generated_at']}`",
        f"- Scripts: `{len(scripts)}`",
        f"- Artifacts: `{len(artifacts)}`",
        "",
        "## Script Stages",
        "",
        "| Stage | Count |",
        "|---|---:|",
    ]

    for stage, count in sorted(scripts_by_stage.items()):
        lines.append(f"| `{stage}` | {count} |")

    lines.extend([
        "",
        "## Artifact Stages",
        "",
        "| Stage | Count |",
        "|---|---:|",
    ])

    for stage, count in sorted(artifacts_by_stage.items()):
        lines.append(f"| `{stage}` | {count} |")

    lines.extend([
        "",
        "## Artifact Statuses",
        "",
        "| Status | Count |",
        "|---|---:|",
    ])

    for status, count in sorted(artifacts_by_status.items()):
        lines.append(f"| `{status}` | {count} |")

    lines.extend([
        "",
        "## Contract Flag Format",
        "",
        "Scripts may define:",
        "",
        "```python",
        "PIPELINE_CONTRACT = {",
        '    "script_id": "scripts.investigation.example",',
        '    "purpose": "What this script does.",',
        '    "pipeline_stage": "runtime_facts",',
        '    "input_schemas": ["targeted_validation_result.v2"],',
        '    "output_schemas": ["runtime_facts.v2"],',
        '    "artifact_patterns": ["investigations/validation/*_runtime_facts_v2.json"],',
        '    "promotion_role": "promotion_core",',
        '    "canonical_status": "active",',
        "}",
        "```",
        "",
        "Generated JSON artifacts may define:",
        "",
        "```json",
        "{",
        '  "schema": "runtime_facts.v2",',
        '  "producer_script": "scripts.investigation.example",',
        '  "pipeline_stage": "runtime_facts",',
        '  "benchmark": "vendor_purchase_itemdata",',
        '  "promotion_role": "promotion_core",',
        '  "canonical_status": "intermediate",',
        '  "inputs": ["investigations/validation/source_validation.json"]',
        "}",
        "```",
    ])

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build fire-and-forget SIGNALIS pipeline script/artifact contract registry."
    )
    parser.add_argument("--workspace", type=Path, default=Path("."))
    parser.add_argument(
        "--existing-contract",
        type=Path,
        default=Path("docs/runtime/pipeline_artifact_contract.json"),
    )
    parser.add_argument(
        "--out-json",
        type=Path,
        default=Path("docs/runtime/pipeline_artifact_contract.json"),
    )
    parser.add_argument(
        "--out-md",
        type=Path,
        default=Path("docs/runtime/pipeline_artifact_contract.md"),
    )
    parser.add_argument(
        "--no-merge-existing",
        action="store_true",
        help="Do not preserve manual curations from existing contract.",
    )
    args = parser.parse_args()

    workspace = args.workspace.resolve()

    scripts = discover_scripts(workspace)
    artifacts = discover_artifacts(workspace)

    contract = {
        "schema": CONTRACT_SCHEMA,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "purpose": "Permanent fire-and-forget registry for SIGNALIS AI scripts and generated artifacts.",
        "rules": [
            "Every pipeline-stable script must be registered.",
            "Every canonical or promotable artifact must be traceable to a producer script.",
            "Promotion validation must not mix generic, debug, legacy, failed, or superseded artifacts unless explicitly allowed.",
            "runtime_propagation_topology.json is required for propagation-chain promotion evidence.",
            "Explicit PIPELINE_CONTRACT flags in scripts override inference.",
            "Explicit artifact metadata fields override inference.",
        ],
        "allowed_statuses": ALLOWED_STATUSES,
        "allowed_promotion_roles": ALLOWED_PROMOTION_ROLES,
        "scripts": [asdict(s) for s in scripts],
        "artifacts": [asdict(a) for a in artifacts],
    }

    existing_path = workspace / args.existing_contract
    if not args.no_merge_existing and existing_path.exists():
        contract = merge_existing_curations(contract, read_json(existing_path))

    out_json = workspace / args.out_json
    out_md = workspace / args.out_md

    write_json(out_json, contract)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_md(contract), encoding="utf-8")

    print(f"Wrote JSON: {out_json.relative_to(workspace)}")
    print(f"Wrote MD:   {out_md.relative_to(workspace)}")
    print(f"Scripts:    {len(contract['scripts'])}")
    print(f"Artifacts:  {len(contract['artifacts'])}")


if __name__ == "__main__":
    main()