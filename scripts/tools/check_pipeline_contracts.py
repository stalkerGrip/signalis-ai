from __future__ import annotations

import argparse
import ast
import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_CONTRACT = Path("docs/runtime/pipeline_artifact_contract.json")
DEFAULT_OUT_JSON = Path("investigations/validation/pipeline_contract_check_v1.json")
DEFAULT_OUT_MD = Path("investigations/validation/pipeline_contract_check_v1.md")

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

SUPPORTED_ARTIFACT_SUFFIXES = {".json", ".jsonl", ".md", ".txt"}

DEFAULT_CONTRACT_DATA: dict[str, Any] = {
    "schema": "pipeline_artifact_contract.v1",
    "purpose": "Permanent registry for SIGNALIS AI scripts and generated artifacts.",
    "rules": [
        "Every pipeline-stable script must be registered.",
        "Every canonical or promotable artifact must be traceable to a producer script.",
        "Promotion validation must not mix generic, debug, legacy, failed, or superseded artifacts unless explicitly allowed.",
        "runtime_propagation_topology.json is required for propagation-chain promotion evidence.",
        "Permanent infrastructure must discover artifacts by schema/metadata, not filename version.",
    ],
    "allowed_statuses": [
        "canonical",
        "active",
        "intermediate",
        "debug",
        "legacy",
        "superseded",
        "failed",
        "unknown",
    ],
    "allowed_promotion_roles": [
        "promotion_core",
        "promotion_support",
        "context_or_debug",
        "not_promotion_relevant",
    ],
    "scripts": [],
    "artifacts": [],
}


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: str | None = None


@dataclass
class ScriptInfo:
    path: str
    module: str
    has_argparse: bool
    has_pipeline_contract: bool
    declared_outputs: list[str]


@dataclass
class ArtifactInfo:
    path: str
    schema: str | None
    producer_script: str | None
    artifact_id: str | None
    benchmark: str | None
    stage: str | None
    canonical_status: str
    promotion_role: str
    inputs: list[str]
    source: str


def load_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def normalize_rel_path(path: Path | str) -> str:
    return str(path).replace("\\", "/")


def resolve_workspace_path(workspace: Path, path: Path) -> Path:
    if path.is_absolute():
        return path
    return workspace / path


def module_from_path(path: Path) -> str:
    return ".".join(path.with_suffix("").parts)


def discover_script_dirs(workspace: Path, configured: list[Path]) -> list[Path]:
    return [resolve_workspace_path(workspace, item) for item in configured]


def discover_artifact_dirs(workspace: Path, configured: list[Path]) -> list[Path]:
    return [resolve_workspace_path(workspace, item) for item in configured]


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
                except Exception:
                    return None

                if isinstance(value, dict):
                    return value

    return None


def discover_scripts(workspace: Path, script_dirs: list[Path]) -> list[ScriptInfo]:
    scripts: list[ScriptInfo] = []

    for root in discover_script_dirs(workspace, script_dirs):
        if not root.exists():
            continue

        for path in sorted(root.rglob("*.py")):
            if path.name == "__init__.py":
                continue

            rel = path.relative_to(workspace)
            text = path.read_text(encoding="utf-8", errors="ignore")
            explicit = extract_pipeline_contract_from_script(path)

            declared_outputs = sorted(
                set(
                    token
                    for token in [
                        "out",
                        "out_json",
                        "out_md",
                        "out_dir",
                        "output",
                        "write_json",
                        "write_md",
                        "write_text",
                    ]
                    if token in text
                )
            )

            scripts.append(
                ScriptInfo(
                    path=normalize_rel_path(rel),
                    module=module_from_path(rel),
                    has_argparse="argparse.ArgumentParser" in text,
                    has_pipeline_contract=explicit is not None,
                    declared_outputs=declared_outputs,
                )
            )

    return scripts


def read_first_jsonl_object(path: Path) -> dict[str, Any] | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                value = json.loads(line)
                return value if isinstance(value, dict) else None
    except Exception:
        return None

    return None


def read_fenced_json_metadata(path: Path) -> dict[str, Any] | None:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None

    for match in re.finditer(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL):
        try:
            value = json.loads(match.group(1))
        except Exception:
            continue

        if isinstance(value, dict) and (
            "schema" in value
            or "producer_script" in value
            or "pipeline_stage" in value
            or "canonical_status" in value
        ):
            return value

    return None


def read_artifact_metadata(path: Path) -> tuple[dict[str, Any] | None, str]:
    suffix = path.suffix.lower()

    if suffix == ".json":
        data = load_json(path)
        return (data, "json") if isinstance(data, dict) else (None, "none")

    if suffix == ".jsonl":
        data = read_first_jsonl_object(path)
        return (data, "jsonl_first_object") if isinstance(data, dict) else (None, "none")

    if suffix in {".md", ".txt"}:
        data = read_fenced_json_metadata(path)
        return (data, "fenced_json_metadata") if isinstance(data, dict) else (None, "none")

    return None, "none"


def infer_stage_from_name(name: str) -> str | None:
    n = name.lower()

    pairs = [
        ("architecture_intelligence", "architecture_intelligence"),
        ("runtime_chain_context_pack", "retrieval"),
        ("runtime_chain_corpus", "retrieval"),
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
        ("promotion_validation", "promotion"),
        ("promotion_decision", "promotion"),
        ("promoted_runtime_chains", "promotion"),
        ("promoted", "promotion_output"),
        ("not_promoted", "promotion_output"),
        ("probe", "probe"),
        ("diagnosis", "diagnosis"),
        ("qdrant_embedding", "embedding"),
        ("qdrant_query", "retrieval"),
        ("qdrant_documents", "retrieval"),
    ]

    for needle, stage in pairs:
        if needle in n:
            return stage

    return None


def infer_benchmark_from_name(name: str) -> str | None:
    n = name.lower()

    if n.startswith("vendor_purchase_itemdata"):
        return "vendor_purchase_itemdata"
    if n.startswith("vendor_stale_price"):
        return "vendor_stale_price_label_after_purchase"
    if n.startswith("characterload_inventory") or "playerloadedchar" in n:
        return "characterload_inventory"
    if n.startswith("runtime_chain_regression"):
        return "global_regression"
    if n.startswith("probe_") or n.startswith("debug_"):
        return "topology_debug"

    return None


def infer_status_from_path(path: str, metadata: dict[str, Any] | None) -> str:
    if metadata and isinstance(metadata.get("canonical_status"), str):
        return metadata["canonical_status"]

    lowered = path.lower()
    if "/_superseded/" in lowered or "\\_superseded\\" in lowered or "_superseded_" in lowered:
        return "superseded"
    if "not_promoted" in lowered:
        return "failed"
    if "debug" in lowered or "probe" in lowered or "diagnosis" in lowered:
        return "debug"

    return "unknown"


def infer_role_from_path(path: str, metadata: dict[str, Any] | None) -> str:
    if metadata and isinstance(metadata.get("promotion_role"), str):
        return metadata["promotion_role"]

    lowered = path.lower()
    if "docs/runtime/runtime_chains" in lowered and "promoted" in lowered:
        return "promotion_core"
    if "promotion" in lowered or "runtime_chain_candidate" in lowered:
        return "promotion_core"

    return "context_or_debug"


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


def discover_artifacts(workspace: Path, artifact_dirs: list[Path]) -> list[ArtifactInfo]:
    artifacts: list[ArtifactInfo] = []

    for root in discover_artifact_dirs(workspace, artifact_dirs):
        if not root.exists():
            continue

        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in SUPPORTED_ARTIFACT_SUFFIXES:
                continue

            rel = normalize_rel_path(path.relative_to(workspace))
            metadata, metadata_source = read_artifact_metadata(path)

            schema = metadata.get("schema") if isinstance(metadata, dict) and isinstance(metadata.get("schema"), str) else None
            producer = metadata.get("producer_script") if isinstance(metadata, dict) and isinstance(metadata.get("producer_script"), str) else None
            artifact_id = metadata.get("artifact_id") if isinstance(metadata, dict) and isinstance(metadata.get("artifact_id"), str) else None
            benchmark = metadata.get("benchmark") if isinstance(metadata, dict) and isinstance(metadata.get("benchmark"), str) else None
            stage = metadata.get("pipeline_stage") if isinstance(metadata, dict) and isinstance(metadata.get("pipeline_stage"), str) else None

            artifacts.append(
                ArtifactInfo(
                    path=rel,
                    schema=schema,
                    producer_script=producer,
                    artifact_id=artifact_id,
                    benchmark=benchmark or infer_benchmark_from_name(path.name),
                    stage=stage or infer_stage_from_name(path.name),
                    canonical_status=infer_status_from_path(rel, metadata),
                    promotion_role=infer_role_from_path(rel, metadata),
                    inputs=extract_inputs(metadata) if metadata is not None else [],
                    source=metadata_source,
                )
            )

    return artifacts


def contract_script_map(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}

    for entry in contract.get("scripts", []):
        if not isinstance(entry, dict):
            continue

        path = entry.get("path")
        module = entry.get("module")

        if isinstance(path, str):
            result[path.replace("\\", "/")] = entry

        if isinstance(module, str):
            result[module] = entry

    return result


def contract_artifact_map(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}

    for entry in contract.get("artifacts", []):
        if isinstance(entry, dict) and isinstance(entry.get("path"), str):
            result[entry["path"].replace("\\", "/")] = entry

    return result


def is_registered_script(script: ScriptInfo, registry: dict[str, dict[str, Any]]) -> bool:
    return script.path in registry or script.module in registry


def is_artifact_contract_relevant(artifact: ArtifactInfo) -> bool:
    if artifact.path.endswith(".json"):
        return True

    if artifact.schema or artifact.producer_script or artifact.canonical_status == "canonical":
        return True

    return artifact.promotion_role == "promotion_core"


def validate(
    contract: dict[str, Any],
    scripts: list[ScriptInfo],
    artifacts: list[ArtifactInfo],
) -> list[Finding]:
    findings: list[Finding] = []

    if contract.get("schema") != "pipeline_artifact_contract.v1":
        findings.append(
            Finding(
                "ERROR",
                "BAD_CONTRACT_SCHEMA",
                "Contract must declare schema pipeline_artifact_contract.v1.",
                None,
            )
        )

    script_registry = contract_script_map(contract)
    artifact_registry = contract_artifact_map(contract)

    allowed_statuses = set(contract.get("allowed_statuses", []))
    allowed_roles = set(contract.get("allowed_promotion_roles", []))
    known_script_ids = {
        str(entry.get("script_id"))
        for entry in contract.get("scripts", [])
        if isinstance(entry, dict) and entry.get("script_id")
    }

    for script in scripts:
        if not is_registered_script(script, script_registry):
            findings.append(
                Finding(
                    "WARN",
                    "SCRIPT_UNREGISTERED",
                    "Script exists but is not registered in pipeline_artifact_contract.json.",
                    script.path,
                )
            )

        if script.has_argparse and not script.has_pipeline_contract:
            findings.append(
                Finding(
                    "INFO",
                    "SCRIPT_HAS_CLI_WITHOUT_EXPLICIT_CONTRACT",
                    "CLI script has no explicit PIPELINE_CONTRACT. This is allowed for legacy scripts but should be fixed for new infrastructure.",
                    script.path,
                )
            )

    discovered_script_paths = {script.path for script in scripts}

    for entry in contract.get("scripts", []):
        if not isinstance(entry, dict):
            continue

        path = entry.get("path")
        if isinstance(path, str) and path.replace("\\", "/") not in discovered_script_paths:
            findings.append(
                Finding(
                    "ERROR",
                    "REGISTERED_SCRIPT_MISSING",
                    "Registered script path does not exist.",
                    path,
                )
            )

    artifact_by_path = {artifact.path: artifact for artifact in artifacts}

    for artifact in artifacts:
        if (
            is_artifact_contract_relevant(artifact)
            and artifact.path not in artifact_registry
        ):
            findings.append(
                Finding(
                    "WARN",
                    "ARTIFACT_UNREGISTERED",
                    "Artifact exists but is not registered.",
                    artifact.path,
                )
            )

        if artifact.canonical_status not in allowed_statuses:
            findings.append(
                Finding(
                    "ERROR",
                    "BAD_ARTIFACT_STATUS",
                    f"Artifact has invalid canonical_status `{artifact.canonical_status}`.",
                    artifact.path,
                )
            )

        if artifact.promotion_role not in allowed_roles:
            findings.append(
                Finding(
                    "ERROR",
                    "BAD_PROMOTION_ROLE",
                    f"Artifact has invalid promotion_role `{artifact.promotion_role}`.",
                    artifact.path,
                )
            )

        if (
            artifact.promotion_role == "promotion_core"
            and artifact.canonical_status in {"debug", "failed", "legacy", "superseded"}
        ):
            findings.append(
                Finding(
                    "ERROR",
                    "INVALID_PROMOTION_CORE_STATUS",
                    "Promotion-core artifact cannot be debug/failed/legacy/superseded.",
                    artifact.path,
                )
            )

        if artifact.canonical_status == "canonical":
            if artifact.path.endswith(".json") and not artifact.schema:
                findings.append(
                    Finding(
                        "ERROR",
                        "CANONICAL_ARTIFACT_MISSING_SCHEMA",
                        "Canonical JSON artifact must declare schema.",
                        artifact.path,
                    )
                )

            if not artifact.producer_script:
                findings.append(
                    Finding(
                        "WARN",
                        "CANONICAL_ARTIFACT_MISSING_PRODUCER",
                        "Canonical artifact should declare producer_script.",
                        artifact.path,
                    )
                )

            if artifact.producer_script and artifact.producer_script not in known_script_ids:
                findings.append(
                    Finding(
                        "ERROR",
                        "CANONICAL_ARTIFACT_UNKNOWN_PRODUCER",
                        "Canonical artifact producer_script is not registered.",
                        artifact.path,
                    )
                )

    for path, entry in artifact_registry.items():
        if path not in artifact_by_path:
            findings.append(
                Finding(
                    "ERROR",
                    "REGISTERED_ARTIFACT_MISSING",
                    "Registered artifact path does not exist.",
                    path,
                )
            )
            continue

        status = entry.get("canonical_status")
        if isinstance(status, str) and status not in allowed_statuses:
            findings.append(
                Finding(
                    "ERROR",
                    "REGISTERED_BAD_STATUS",
                    f"Registered artifact has invalid status `{status}`.",
                    path,
                )
            )

    canonical_by_artifact_id: dict[str, list[str]] = defaultdict(list)
    for artifact in artifacts:
        if artifact.canonical_status != "canonical":
            continue

        if artifact.artifact_id:
            canonical_by_artifact_id[artifact.artifact_id].append(artifact.path)

    for artifact_id, paths in canonical_by_artifact_id.items():
        if len(paths) > 1:
            findings.append(
                Finding(
                    "ERROR",
                    "MULTIPLE_CANONICAL_ARTIFACT_IDS",
                    f"Multiple canonical artifacts use artifact_id `{artifact_id}`.",
                    ", ".join(paths),
                )
            )

    promotion_outputs = [
        artifact
        for artifact in artifacts
        if (
            artifact.stage in {"promotion", "promotion_output"}
            or "promoted" in artifact.path.lower()
        )
    ]

    for artifact in promotion_outputs:
        lowered_inputs = " ".join(artifact.inputs).lower()

        if "generic" in lowered_inputs and artifact.canonical_status == "canonical":
            findings.append(
                Finding(
                    "ERROR",
                    "CANONICAL_PROMOTION_DEPENDS_ON_GENERIC",
                    "Canonical promotion artifact references generic evidence.",
                    artifact.path,
                )
            )

        if (
            "runtime_topology.json" in lowered_inputs
            and "runtime_propagation_topology.json" not in lowered_inputs
            and artifact.canonical_status == "canonical"
        ):
            findings.append(
                Finding(
                    "ERROR",
                    "CANONICAL_PROMOTION_USES_RELATIONSHIP_TOPOLOGY",
                    "Propagation-chain promotion must use runtime_propagation_topology.json.",
                    artifact.path,
                )
            )

    return findings


def render_md(
    contract_path: Path,
    scripts: list[ScriptInfo],
    artifacts: list[ArtifactInfo],
    findings: list[Finding],
) -> str:
    by_severity: dict[str, list[Finding]] = defaultdict(list)
    for finding in findings:
        by_severity[finding.severity].append(finding)

    lines: list[str] = []
    lines.append("# Pipeline Contract Check V1")
    lines.append("")
    lines.append(f"- Contract: `{contract_path}`")
    lines.append(f"- Scripts discovered: `{len(scripts)}`")
    lines.append(f"- Artifacts discovered: `{len(artifacts)}`")
    lines.append(f"- Findings: `{len(findings)}`")
    lines.append("")

    lines.append("## Finding Summary")
    lines.append("")
    lines.append("| Severity | Count |")
    lines.append("|---|---:|")
    for severity in ["ERROR", "WARN", "INFO"]:
        lines.append(f"| `{severity}` | {len(by_severity.get(severity, []))} |")
    lines.append("")

    for severity in ["ERROR", "WARN", "INFO"]:
        items = by_severity.get(severity, [])
        if not items:
            continue

        lines.append(f"## {severity}")
        lines.append("")
        lines.append("| Code | Path | Message |")
        lines.append("|---|---|---|")
        for item in items:
            lines.append(
                f"| `{item.code}` | `{item.path or ''}` | {item.message} |"
            )
        lines.append("")

    lines.append("## Doctrine Reminder")
    lines.append("")
    lines.append(
        "This checker enforces permanent script/artifact tracking: "
        "canonical and promotion-relevant artifacts must be schema/metadata-addressable, "
        "and stable scripts should be registered through explicit PIPELINE_CONTRACT metadata."
    )

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check SIGNALIS AI script/artifact contracts against actual repository state."
    )

    parser.add_argument("--workspace", type=Path, default=Path("."))
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--out-json", type=Path, default=DEFAULT_OUT_JSON)
    parser.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
    parser.add_argument(
        "--script-dir",
        action="append",
        type=Path,
        default=None,
        help="Additional or replacement script directory to scan. Repeatable. Defaults to canonical script dirs.",
    )
    parser.add_argument(
        "--artifact-dir",
        action="append",
        type=Path,
        default=None,
        help="Additional or replacement artifact directory to scan. Repeatable. Defaults to canonical artifact dirs.",
    )
    parser.add_argument(
        "--init-contract",
        action="store_true",
        help="Create a starter contract if missing.",
    )
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="Exit non-zero when ERROR findings exist.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    workspace = args.workspace.resolve()

    contract_path = resolve_workspace_path(workspace, args.contract)
    out_json = resolve_workspace_path(workspace, args.out_json)
    out_md = resolve_workspace_path(workspace, args.out_md)

    if args.init_contract and not contract_path.exists():
        write_json(contract_path, DEFAULT_CONTRACT_DATA)
        print(f"Wrote starter contract: {contract_path.relative_to(workspace)}")

    if not contract_path.exists():
        raise SystemExit(
            f"Missing contract: {contract_path}\n"
            f"Run first with --init-contract."
        )

    contract = load_json(contract_path)
    if not isinstance(contract, dict):
        raise SystemExit(f"Invalid contract JSON: {contract_path}")

    script_dirs = args.script_dir or DEFAULT_SCRIPT_DIRS
    artifact_dirs = args.artifact_dir or DEFAULT_ARTIFACT_DIRS

    scripts = discover_scripts(workspace, script_dirs)
    artifacts = discover_artifacts(workspace, artifact_dirs)
    findings = validate(contract, scripts, artifacts)

    result = {
        "schema": "pipeline_contract_check.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "contract": normalize_rel_path(args.contract),
        "script_dirs": [normalize_rel_path(item) for item in script_dirs],
        "artifact_dirs": [normalize_rel_path(item) for item in artifact_dirs],
        "scripts_discovered": [asdict(script) for script in scripts],
        "artifacts_discovered": [asdict(artifact) for artifact in artifacts],
        "findings": [asdict(finding) for finding in findings],
        "summary": {
            "scripts": len(scripts),
            "artifacts": len(artifacts),
            "errors": sum(1 for finding in findings if finding.severity == "ERROR"),
            "warnings": sum(1 for finding in findings if finding.severity == "WARN"),
            "info": sum(1 for finding in findings if finding.severity == "INFO"),
        },
    }

    write_json(out_json, result)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_md(args.contract, scripts, artifacts, findings), encoding="utf-8")

    print(f"Wrote JSON: {out_json.relative_to(workspace)}")
    print(f"Wrote MD:   {out_md.relative_to(workspace)}")
    print(f"Scripts:    {len(scripts)}")
    print(f"Artifacts:  {len(artifacts)}")
    print(f"Errors:     {result['summary']['errors']}")
    print(f"Warnings:   {result['summary']['warnings']}")
    print(f"Info:       {result['summary']['info']}")

    if args.fail_on_error and result["summary"]["errors"] > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
