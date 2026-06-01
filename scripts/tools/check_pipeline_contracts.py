from __future__ import annotations

import argparse
import ast
import json
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_CONTRACT = Path("docs/runtime/pipeline_artifact_contract.json")
DEFAULT_OUT_JSON = Path("investigations/validation/pipeline_contract_check_v1.json")
DEFAULT_OUT_MD = Path("investigations/validation/pipeline_contract_check_v1.md")


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


DEFAULT_CONTRACT_DATA: dict[str, Any] = {
    "schema": "pipeline_artifact_contract.v1",
    "purpose": "Permanent registry for SIGNALIS AI scripts and generated artifacts.",
    "rules": [
        "Every pipeline-stable script must be registered.",
        "Every canonical or promotable artifact must be traceable to a producer script.",
        "Promotion validation must not mix generic, debug, legacy, failed, or superseded artifacts unless explicitly allowed.",
        "runtime_propagation_topology.json is required for propagation-chain promotion evidence.",
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
    declared_outputs: list[str]


@dataclass
class ArtifactInfo:
    path: str
    schema: str | None
    producer_script: str | None
    benchmark: str | None
    stage: str | None
    canonical_status: str
    promotion_role: str
    inputs: list[str]


def load_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def module_from_path(path: Path) -> str:
    return ".".join(path.with_suffix("").parts)


def discover_scripts(workspace: Path) -> list[ScriptInfo]:
    scripts: list[ScriptInfo] = []

    for script_dir in SCRIPT_DIRS:
        root = workspace / script_dir
        if not root.exists():
            continue

        for path in sorted(root.rglob("*.py")):
            if path.name == "__init__.py":
                continue

            text = path.read_text(encoding="utf-8", errors="ignore")
            declared_outputs = sorted(
                set(
                    token
                    for token in [
                        "out",
                        "out_json",
                        "out_md",
                        "out_dir",
                        "output",
                        "write",
                    ]
                    if token in text
                )
            )

            scripts.append(
                ScriptInfo(
                    path=str(path.relative_to(workspace)).replace("\\", "/"),
                    module=module_from_path(path.relative_to(workspace)),
                    has_argparse="argparse.ArgumentParser" in text,
                    declared_outputs=declared_outputs,
                )
            )

    return scripts


def infer_stage_from_name(name: str) -> str | None:
    n = name.lower()

    pairs = [
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
        ("promoted", "promotion_output"),
        ("not_promoted", "promotion_output"),
        ("probe", "probe"),
        ("diagnosis", "diagnosis"),
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


def extract_inputs(data: Any) -> list[str]:
    refs: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, str):
            normalized = value.replace("\\", "/")
            if (
                normalized.endswith(".json")
                or normalized.endswith(".md")
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


def discover_artifacts(workspace: Path) -> list[ArtifactInfo]:
    artifacts: list[ArtifactInfo] = []

    for artifact_dir in ARTIFACT_DIRS:
        root = workspace / artifact_dir
        if not root.exists():
            continue

        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in {
                ".json",
                ".jsonl",
                ".md",
                ".txt",
            }:
                continue

            data = None

            if path.suffix.lower() == ".json":
                data = load_json(path)
            schema = data.get("schema") if isinstance(data, dict) and isinstance(data.get("schema"), str) else None
            producer = data.get("producer_script") if isinstance(data, dict) and isinstance(data.get("producer_script"), str) else None
            benchmark = data.get("benchmark") if isinstance(data, dict) and isinstance(data.get("benchmark"), str) else None
            stage = data.get("pipeline_stage") if isinstance(data, dict) and isinstance(data.get("pipeline_stage"), str) else None
            status = data.get("canonical_status") if isinstance(data, dict) and isinstance(data.get("canonical_status"), str) else "unknown"
            role = data.get("promotion_role") if isinstance(data, dict) and isinstance(data.get("promotion_role"), str) else "context_or_debug"

            artifacts.append(
                ArtifactInfo(
                    path=str(path.relative_to(workspace)).replace("\\", "/"),
                    schema=schema,
                    producer_script=producer,
                    benchmark=benchmark or infer_benchmark_from_name(path.name),
                    stage=stage or infer_stage_from_name(path.name),
                    canonical_status=status,
                    promotion_role=role,
                    inputs=extract_inputs(data) if data is not None else [],
                )
            )

    return artifacts


def contract_script_map(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result = {}
    for entry in contract.get("scripts", []):
        if isinstance(entry, dict):
            path = entry.get("path")
            module = entry.get("module")
            if isinstance(path, str):
                result[path.replace("\\", "/")] = entry
            elif isinstance(module, str):
                result[module] = entry
    return result


def contract_artifact_map(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result = {}
    for entry in contract.get("artifacts", []):
        if isinstance(entry, dict) and isinstance(entry.get("path"), str):
            result[entry["path"].replace("\\", "/")] = entry
    return result


def validate(
    contract: dict[str, Any],
    scripts: list[ScriptInfo],
    artifacts: list[ArtifactInfo],
) -> list[Finding]:
    findings: list[Finding] = []

    script_registry = contract_script_map(contract)
    artifact_registry = contract_artifact_map(contract)

    allowed_statuses = set(contract.get("allowed_statuses", []))
    allowed_roles = set(contract.get("allowed_promotion_roles", []))

    for script in scripts:
        if script.path not in script_registry and script.module not in script_registry:
            findings.append(
                Finding(
                    "WARN",
                    "SCRIPT_UNREGISTERED",
                    "Script exists but is not registered in pipeline_artifact_contract.json.",
                    script.path,
                )
            )

    for key, entry in script_registry.items():
        path = entry.get("path")
        if isinstance(path, str) and not any(s.path == path.replace("\\", "/") for s in scripts):
            findings.append(
                Finding(
                    "ERROR",
                    "REGISTERED_SCRIPT_MISSING",
                    "Registered script path does not exist.",
                    path,
                )
            )

    artifact_by_path = {a.path: a for a in artifacts}

    for artifact in artifacts:
        if artifact.path not in artifact_registry and artifact.path.endswith(".json"):
            findings.append(
                Finding(
                    "WARN",
                    "ARTIFACT_UNREGISTERED",
                    "JSON artifact exists but is not registered.",
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

        if artifact.promotion_role == "promotion_core" and artifact.canonical_status in {"debug", "failed", "legacy", "superseded"}:
            findings.append(
                Finding(
                    "ERROR",
                    "INVALID_PROMOTION_CORE_STATUS",
                    "Promotion-core artifact cannot be debug/failed/legacy/superseded.",
                    artifact.path,
                )
            )

        if artifact.canonical_status == "canonical":
            if not artifact.schema and artifact.path.endswith(".json"):
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

    canonical_groups: dict[tuple[str, str], list[str]] = defaultdict(list)

    for artifact in artifacts:
        if artifact.canonical_status == "canonical" and artifact.benchmark and artifact.stage:
            canonical_groups[(artifact.benchmark, artifact.stage)].append(artifact.path)

    for (benchmark, stage), paths in canonical_groups.items():
        if len(paths) > 1:
            findings.append(
                Finding(
                    "ERROR",
                    "MULTIPLE_CANONICAL_ARTIFACTS",
                    f"Multiple canonical artifacts for benchmark `{benchmark}` stage `{stage}`.",
                    ", ".join(paths),
                )
            )

    promotion_outputs = [
        a for a in artifacts
        if a.stage == "promotion_output" or "promoted" in a.path.lower()
    ]

    for artifact in promotion_outputs:
        lowered_inputs = " ".join(artifact.inputs).lower()
        if "generic" in lowered_inputs:
            findings.append(
                Finding(
                    "ERROR",
                    "PROMOTION_DEPENDS_ON_GENERIC",
                    "Promotion artifact references generic evidence.",
                    artifact.path,
                )
            )

        if "runtime_topology.json" in lowered_inputs and "runtime_propagation_topology.json" not in lowered_inputs:
            findings.append(
                Finding(
                    "ERROR",
                    "PROMOTION_USES_RELATIONSHIP_TOPOLOGY",
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
        "This checker enforces the permanent script/artifact tracking rule: "
        "scripts and promotion-relevant artifacts must be contract-addressable before they are used as canonical evidence."
    )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check SIGNALIS AI script/artifact contracts against actual repository state."
    )
    parser.add_argument("--workspace", type=Path, default=Path("."))
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--out-json", type=Path, default=DEFAULT_OUT_JSON)
    parser.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
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

    args = parser.parse_args()
    workspace = args.workspace.resolve()

    contract_path = workspace / args.contract

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

    scripts = discover_scripts(workspace)
    artifacts = discover_artifacts(workspace)
    findings = validate(contract, scripts, artifacts)

    result = {
        "schema": "pipeline_contract_check.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "contract": str(args.contract).replace("\\", "/"),
        "scripts_discovered": [asdict(s) for s in scripts],
        "artifacts_discovered": [asdict(a) for a in artifacts],
        "findings": [asdict(f) for f in findings],
        "summary": {
            "scripts": len(scripts),
            "artifacts": len(artifacts),
            "errors": sum(1 for f in findings if f.severity == "ERROR"),
            "warnings": sum(1 for f in findings if f.severity == "WARN"),
        },
    }

    out_json = workspace / args.out_json
    out_md = workspace / args.out_md

    write_json(out_json, result)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_md(args.contract, scripts, artifacts, findings), encoding="utf-8")

    print(f"Wrote JSON: {out_json.relative_to(workspace)}")
    print(f"Wrote MD:   {out_md.relative_to(workspace)}")
    print(f"Scripts:    {len(scripts)}")
    print(f"Artifacts:  {len(artifacts)}")
    print(f"Errors:     {result['summary']['errors']}")
    print(f"Warnings:   {result['summary']['warnings']}")

    if args.fail_on_error and result["summary"]["errors"] > 0:
        raise SystemExit(1)


if __name__ == "__main__":
    main()