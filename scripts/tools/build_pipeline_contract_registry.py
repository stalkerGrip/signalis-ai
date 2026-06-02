from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


CONTRACT_SCHEMA = "pipeline_artifact_contract.v1"

DEFAULT_SCRIPT_DIRS = [
    Path("scripts/tools"),
    Path("scripts/investigation"),
    Path("scripts/qdrant"),
    Path("scripts/extraction"),
    Path("scripts/normalization"),
]

DEFAULT_ARTIFACT_DIRS = [
    Path("investigations/validation"),
    Path("investigations/retrieval"),
    Path("investigations/architecture"),
    Path("docs/runtime/runtime_chains"),
    Path("manifests/runtime"),
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

PROMOTION_CORE_STAGES = {
    "source_validation",
    "runtime_facts",
    "ordered_runtime_facts",
    "runtime_fact_graph",
    "runtime_fact_topology",
    "runtime_chain_candidate",
    "promotion",
    "promotion_output",
}

PROMOTION_SUPPORT_STAGES = {
    "targeted_validation_request",
    "runtime_steps",
    "ordered_steps",
    "runtime_chain_regression",
    "pathfinder",
    "retrieval",
    "embedding",
    "ingestion",
    "architecture_intelligence",
}

STAGE_RULES = [
    ("architecture_intelligence", "architecture_intelligence"),
    ("runtime_chain_context_pack", "retrieval"),
    ("runtime_chain_corpus", "retrieval"),
    ("promoted_runtime_chain_registry", "promotion"),
    ("promotion_decision", "promotion"),
    ("promotion_validation", "promotion"),
    ("targeted_validation", "targeted_validation_request"),
    ("source_validation", "source_validation"),
    ("ranked_evidence", "ranked_evidence"),
    ("runtime_steps", "runtime_steps"),
    ("ordered_steps", "ordered_steps"),
    ("ordered_runtime_facts", "ordered_runtime_facts"),
    ("runtime_fact_topology", "runtime_fact_topology"),
    ("runtime_fact_graph", "runtime_fact_graph"),
    ("runtime_facts", "runtime_facts"),
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
    ("query_qdrant", "retrieval"),
    ("retrieve_", "retrieval"),
    ("embed_", "embedding"),
    ("ingest_", "ingestion"),
    ("build_", "builder"),
]


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


def read_jsonl_first_object(path: Path) -> dict[str, Any] | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                data = json.loads(line)
                return data if isinstance(data, dict) else None
    except Exception:
        return None

    return None


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def normalize_rel(path: Path) -> str:
    return str(path).replace("\\", "/")


def resolve_workspace_path(workspace: Path, path: Path) -> Path:
    return path if path.is_absolute() else workspace / path


def module_from_path(path: Path) -> str:
    return ".".join(path.with_suffix("").parts)


def slug(value: str) -> str:
    value = value.replace("\\", "/")
    value = re.sub(r"[^a-zA-Z0-9_.:/-]+", "_", value)
    return value.strip("_")


def as_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def sorted_unique(values: Iterable[str]) -> list[str]:
    return sorted({str(value).replace("\\", "/") for value in values if str(value).strip()})


def safe_eval_contract_node(node: ast.AST, constants: dict[str, Any]) -> Any:
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.Name):
        if node.id in constants:
            return constants[node.id]
        raise ValueError(f"Unknown constant reference: {node.id}")

    if isinstance(node, ast.List):
        return [safe_eval_contract_node(item, constants) for item in node.elts]

    if isinstance(node, ast.Tuple):
        return [safe_eval_contract_node(item, constants) for item in node.elts]

    if isinstance(node, ast.Dict):
        result: dict[str, Any] = {}

        for key_node, value_node in zip(node.keys, node.values):
            if key_node is None:
                raise ValueError("Dict unpacking is not supported in PIPELINE_CONTRACT")

            key = safe_eval_contract_node(key_node, constants)
            value = safe_eval_contract_node(value_node, constants)
            result[str(key)] = value

        return result

    raise ValueError(f"Unsupported PIPELINE_CONTRACT expression: {type(node).__name__}")


def extract_pipeline_contract_from_script(path: Path) -> dict[str, Any] | None:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
    except SyntaxError:
        return None

    constants: dict[str, Any] = {}

    for node in tree.body:
        target_name = None
        value_node = None

        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                target_name = target.id
                value_node = node.value

        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target_name = node.target.id
            value_node = node.value

        if not target_name or value_node is None:
            continue

        if target_name == "PIPELINE_CONTRACT":
            try:
                value = safe_eval_contract_node(value_node, constants)
                return value if isinstance(value, dict) else None
            except Exception:
                return None

        try:
            value = ast.literal_eval(value_node)
            if isinstance(value, (str, int, float, bool, list, tuple, dict)) or value is None:
                constants[target_name] = value
        except Exception:
            continue

    return None


def extract_markdown_contract_metadata(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {}

    # Prefer fenced JSON blocks that explicitly describe generated artifact metadata.
    for match in re.finditer(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL):
        data = read_json_from_text(match.group(1))
        if isinstance(data, dict) and (
            "schema" in data
            or "producer_script" in data
            or "pipeline_stage" in data
            or "canonical_status" in data
        ):
            return data

    return {}


def read_json_from_text(text: str) -> Any | None:
    try:
        return json.loads(text)
    except Exception:
        return None


def infer_stage_from_name(name: str) -> str:
    n = name.lower()

    for needle, stage in STAGE_RULES:
        if needle in n:
            return stage

    return "unknown"


def infer_benchmark_from_name(name: str) -> str:
    n = name.lower()

    # This is fallback only. Explicit artifact metadata wins.
    fallback_rules = [
        ("vendor_purchase_itemdata", "vendor_purchase_itemdata"),
        ("vendor_stale_price_label", "vendor_stale_price_label_after_purchase"),
        ("vendor_purchase_price_label", "vendor_purchase_price_label_cleanup"),
        ("characterload_inventory", "characterload_inventory"),
        ("playerloadedchar", "characterload_inventory"),
        ("runtime_chain_regression", "global_regression"),
        ("runtime_fact_topology_regression", "global_regression"),
        ("runtime_propagation_topology", "runtime_topology"),
        ("runtime_topology", "runtime_topology"),
        ("network", "networking"),
        ("hook", "hooks"),
        ("timer", "timers"),
    ]

    for needle, benchmark in fallback_rules:
        if needle in n:
            return benchmark

    if n.startswith("probe_") or n.startswith("debug_"):
        return "topology_debug"

    return "unknown"


def infer_promotion_role(stage: str, path: str) -> str:
    p = path.lower().replace("\\", "/")

    if stage in PROMOTION_CORE_STAGES:
        return "promotion_core"

    if stage in PROMOTION_SUPPORT_STAGES:
        return "promotion_support"

    if "docs/runtime/runtime_chains" in p:
        return "promotion_core"

    return "context_or_debug"


def infer_status(path: str, stage: str) -> str:
    p = path.lower().replace("\\", "/")

    if "/_superseded/" in p or "_superseded_" in p:
        return "superseded"
    if "not_promoted" in p:
        return "failed"
    if "debug" in p or "probe" in p or "diagnosis" in p:
        return "debug"
    if "legacy" in p:
        return "legacy"
    if "generic" in p:
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
    output_schemas = [
        schema
        for schema in schemas
        if any(key in schema for key in ["runtime", "targeted", "pipeline", "chain", "architecture"])
    ]
    return schemas, output_schemas


def extract_artifact_patterns_from_script_text(text: str) -> list[str]:
    patterns: set[str] = set()

    for match in re.findall(r"['\"]([^'\"]+\.(?:json|md|jsonl))['\"]", text):
        normalized = match.replace("\\", "/")
        if any(prefix in normalized for prefix in ["investigations/", "manifests/", "docs/"]):
            patterns.add(normalized)

    return sorted(patterns)


def discover_scripts(workspace: Path, script_dirs: list[Path]) -> list[ScriptContract]:
    results: list[ScriptContract] = []

    for script_dir in script_dirs:
        root = resolve_workspace_path(workspace, script_dir)
        if not root.exists():
            continue

        for path in sorted(root.rglob("*.py")):
            if path.name == "__init__.py":
                continue

            rel = path.relative_to(workspace)
            rel_str = normalize_rel(rel)
            module = module_from_path(rel)
            text = path.read_text(encoding="utf-8", errors="ignore")

            explicit = extract_pipeline_contract_from_script(path)
            if explicit:
                print(f"[CONTRACT] {path}")

            if explicit:
                results.append(
                    ScriptContract(
                        script_id=str(explicit.get("script_id") or module),
                        path=rel_str,
                        module=str(explicit.get("module") or module),
                        purpose=str(explicit.get("purpose") or ""),
                        pipeline_stage=str(explicit.get("pipeline_stage") or infer_stage_from_name(path.name)),
                        input_schemas=as_str_list(explicit.get("input_schemas")),
                        output_schemas=as_str_list(explicit.get("output_schemas")),
                        artifact_patterns=sorted_unique(as_str_list(explicit.get("artifact_patterns"))),
                        promotion_role=str(explicit.get("promotion_role") or "context_or_debug"),
                        canonical_status=str(explicit.get("canonical_status") or "active"),
                        source="explicit_script_flag",
                    )
                )
                continue

            input_schemas, output_schemas = extract_schemas_from_script_text(text)
            stage = infer_stage_from_name(path.name)

            results.append(
                ScriptContract(
                    script_id=module,
                    path=rel_str,
                    module=module,
                    purpose=f"Inferred registry entry for {module}.",
                    pipeline_stage=stage,
                    input_schemas=input_schemas,
                    output_schemas=output_schemas,
                    artifact_patterns=extract_artifact_patterns_from_script_text(text),
                    promotion_role=infer_promotion_role(stage, rel_str),
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


def load_artifact_data(path: Path) -> Any | None:
    suffix = path.suffix.lower()

    if suffix == ".json":
        return read_json(path)
    if suffix == ".jsonl":
        return read_jsonl_first_object(path)
    if suffix == ".md":
        return extract_markdown_contract_metadata(path)

    return None


def discover_artifacts(workspace: Path, artifact_dirs: list[Path]) -> list[ArtifactContract]:
    results: list[ArtifactContract] = []

    for artifact_dir in artifact_dirs:
        root = resolve_workspace_path(workspace, artifact_dir)
        if not root.exists():
            continue

        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".txt", ".jsonl"}:
                continue

            rel_str = normalize_rel(path.relative_to(workspace))
            data = load_artifact_data(path)
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
                    inputs=sorted_unique(str(x) for x in inputs),
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
        if not old or entry.get("source") == "explicit_script_flag":
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
        if not old or entry.get("source") == "explicit_artifact_flag":
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


def count_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(key) or "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def render_md(contract: dict[str, Any]) -> str:
    scripts = contract["scripts"]
    artifacts = contract["artifacts"]

    scripts_by_stage = count_by(scripts, "pipeline_stage")
    artifacts_by_stage = count_by(artifacts, "pipeline_stage")
    artifacts_by_status = count_by(artifacts, "canonical_status")
    artifacts_by_source = count_by(artifacts, "source")

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

    for stage, count in scripts_by_stage.items():
        lines.append(f"| `{stage}` | {count} |")

    lines.extend(["", "## Artifact Stages", "", "| Stage | Count |", "|---|---:|"])
    for stage, count in artifacts_by_stage.items():
        lines.append(f"| `{stage}` | {count} |")

    lines.extend(["", "## Artifact Statuses", "", "| Status | Count |", "|---|---:|"])
    for status, count in artifacts_by_status.items():
        lines.append(f"| `{status}` | {count} |")

    lines.extend(["", "## Artifact Metadata Sources", "", "| Source | Count |", "|---|---:|"])
    for source, count in artifacts_by_source.items():
        lines.append(f"| `{source}` | {count} |")

    lines.extend(
        [
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
        ]
    )

    return "\n".join(lines)


def parse_path_list(values: list[str] | None, defaults: list[Path]) -> list[Path]:
    if not values:
        return defaults
    return [Path(value) for value in values]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build fire-and-forget SIGNALIS pipeline script/artifact contract registry."
    )
    parser.add_argument("--workspace", type=Path, default=Path("."))
    parser.add_argument("--existing-contract", type=Path, default=Path("docs/runtime/pipeline_artifact_contract.json"))
    parser.add_argument("--out-json", type=Path, default=Path("docs/runtime/pipeline_artifact_contract.json"))
    parser.add_argument("--out-md", type=Path, default=Path("docs/runtime/pipeline_artifact_contract.md"))
    parser.add_argument(
        "--script-dir",
        action="append",
        default=None,
        help="Script directory to scan, relative to workspace unless absolute. Can be repeated. Defaults to canonical script roots.",
    )
    parser.add_argument(
        "--artifact-dir",
        action="append",
        default=None,
        help="Artifact directory to scan, relative to workspace unless absolute. Can be repeated. Defaults to canonical artifact roots.",
    )
    parser.add_argument(
        "--no-merge-existing",
        action="store_true",
        help="Do not preserve manual curations from existing contract.",
    )
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    script_dirs = parse_path_list(args.script_dir, DEFAULT_SCRIPT_DIRS)
    artifact_dirs = parse_path_list(args.artifact_dir, DEFAULT_ARTIFACT_DIRS)

    scripts = discover_scripts(workspace, script_dirs)
    artifacts = discover_artifacts(workspace, artifact_dirs)

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
            "Stable infrastructure scripts must discover artifacts by schema and metadata before filename version.",
        ],
        "allowed_statuses": ALLOWED_STATUSES,
        "allowed_promotion_roles": ALLOWED_PROMOTION_ROLES,
        "script_dirs": [normalize_rel(path) for path in script_dirs],
        "artifact_dirs": [normalize_rel(path) for path in artifact_dirs],
        "scripts": [asdict(s) for s in scripts],
        "artifacts": [asdict(a) for a in artifacts],
    }

    existing_path = resolve_workspace_path(workspace, args.existing_contract)
    if not args.no_merge_existing and existing_path.exists():
        contract = merge_existing_curations(contract, read_json(existing_path))

    out_json = resolve_workspace_path(workspace, args.out_json)
    out_md = resolve_workspace_path(workspace, args.out_md)

    write_json(out_json, contract)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_md(contract), encoding="utf-8")

    print(f"Wrote JSON: {out_json.relative_to(workspace)}")
    print(f"Wrote MD:   {out_md.relative_to(workspace)}")
    print(f"Scripts:    {len(contract['scripts'])}")
    print(f"Artifacts:  {len(contract['artifacts'])}")


if __name__ == "__main__":
    main()
