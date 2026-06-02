from __future__ import annotations

import argparse
import ast
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

CONTRACT_SCHEMA = "pipeline_artifact_contract"
SCRIPT_HELP_SCHEMA = "script_cli_contracts"

PIPELINE_CONTRACT = {
    "script_id": "scripts.tools.build_pipeline_contract_registry",
    "purpose": "Build a deterministic registry of explicit SIGNALIS AI pipeline script contracts, CLI contracts, and artifact metadata by scanning the workspace without hardcoded script or artifact subdirectories.",
    "pipeline_stage": "governance",
    "input_families": [],
    "required_input_capabilities": ["workspace_root", "workspace_scan"],
    "output_families": ["pipeline_artifact_contract", "script_cli_contracts"],
    "required_output_capabilities": [
        "script_contracts",
        "script_cli_help",
        "artifact_metadata",
        "artifact_lineage",
        "contract_findings",
    ],
    "output_schemas": ["pipeline_artifact_contract", "script_cli_contracts"],
    "artifact_patterns": [
        "docs/runtime/pipeline_artifact_contract.json",
        "docs/runtime/pipeline_artifact_contract.md",
        "docs/runtime/script_contracts.json",
        "docs/runtime/script_contracts.md",
    ],
    "promotion_role": "context_or_debug",
    "canonical_status": "active",
}

SKIP_DIR_PARTS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".idea",
    ".vscode",
    "node_modules",
    "temp",
    "tmp",
    "logs",
    "_archive",
}

REQUIRED_SCRIPT_FIELDS = [
    "script_id",
    "purpose",
    "pipeline_stage",
    "input_families",
    "required_input_capabilities",
    "output_families",
    "required_output_capabilities",
    "output_schemas",
    "artifact_patterns",
    "promotion_role",
    "canonical_status",
]

ALLOWED_PROMOTION_ROLES = [
    "promotion_core",
    "promotion_support",
    "context_or_debug",
    "not_promotion_relevant",
]

ALLOWED_CANONICAL_STATUSES = [
    "active",
    "canonical",
    "intermediate",
    "debug",
    "legacy",
    "superseded",
    "failed",
    "unknown",
]

ARTIFACT_METADATA_KEYS = [
    "artifact_id",
    "artifact_family",
    "producer_script",
    "pipeline_stage",
    "input_families",
    "output_family",
    "output_families",
    "capabilities",
    "required_capabilities",
    "promotion_role",
    "canonical_status",
    "inputs",
    "source_files",
    "content_digest",
    "lineage",
]


@dataclass
class ScriptContractEntry:
    script_id: str
    declared_script_id: str | None
    path: str
    module: str
    purpose: str
    pipeline_stage: str
    input_families: list[str]
    required_input_capabilities: list[str]
    output_families: list[str]
    required_output_capabilities: list[str]
    output_schemas: list[str]
    artifact_patterns: list[str]
    promotion_role: str
    canonical_status: str
    contract_status: str
    source: str
    findings: list[str]


@dataclass
class ScriptCliEntry:
    path: str
    module: str
    help_ok: bool
    return_code: int | None
    help: str


@dataclass
class ArtifactEntry:
    artifact_id: str
    path: str
    schema: str | None
    artifact_family: str | None
    producer_script: str | None
    pipeline_stage: str | None
    input_families: list[str]
    output_families: list[str]
    capabilities: list[str]
    promotion_role: str | None
    canonical_status: str | None
    inputs: list[str]
    source_files: list[str]
    content_digest: str | None
    source: str
    findings: list[str]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_rel(path: Path) -> str:
    return path.as_posix()


def resolve_path(workspace: Path, path: Path) -> Path:
    return path if path.is_absolute() else workspace / path


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIR_PARTS for part in path.parts)


def as_str_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value if str(item).strip()]
    return [str(value)] if str(value).strip() else []


def sorted_unique(values: Iterable[Any]) -> list[str]:
    return sorted({str(value).replace("\\", "/") for value in values if str(value).strip()})


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def module_from_relative_path(path: Path) -> str:
    return ".".join(path.with_suffix("").parts)


def safe_eval_node(node: ast.AST, constants: dict[str, Any]) -> Any:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        if node.id in constants:
            return constants[node.id]
        raise ValueError(f"Unknown constant reference: {node.id}")
    if isinstance(node, ast.List):
        return [safe_eval_node(item, constants) for item in node.elts]
    if isinstance(node, ast.Tuple):
        return [safe_eval_node(item, constants) for item in node.elts]
    if isinstance(node, ast.Set):
        return [safe_eval_node(item, constants) for item in node.elts]
    if isinstance(node, ast.Dict):
        result: dict[str, Any] = {}
        for key_node, value_node in zip(node.keys, node.values):
            if key_node is None:
                raise ValueError("Dict unpacking is not supported in PIPELINE_CONTRACT")
            result[str(safe_eval_node(key_node, constants))] = safe_eval_node(value_node, constants)
        return result
    raise ValueError(f"Unsupported PIPELINE_CONTRACT expression: {type(node).__name__}")


def extract_pipeline_contract(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        tree = ast.parse(read_text(path))
    except SyntaxError as exc:
        return None, f"syntax_error:{exc}"

    constants: dict[str, Any] = {}
    for node in tree.body:
        target_name: str | None = None
        value_node: ast.AST | None = None
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            target_name = node.targets[0].id
            value_node = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target_name = node.target.id
            value_node = node.value

        if not target_name or value_node is None:
            continue

        if target_name == "PIPELINE_CONTRACT":
            try:
                value = safe_eval_node(value_node, constants)
            except Exception as exc:
                return None, f"invalid_pipeline_contract:{exc}"
            if not isinstance(value, dict):
                return None, "invalid_pipeline_contract:not_dictionary"
            return value, None

        try:
            literal = ast.literal_eval(value_node)
        except Exception:
            continue
        if isinstance(literal, (str, int, float, bool, list, tuple, dict, set)) or literal is None:
            constants[target_name] = literal

    return None, None


def validate_script_contract(contract: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    for field in REQUIRED_SCRIPT_FIELDS:
        if field not in contract:
            findings.append(f"missing_field:{field}")

    if contract.get("promotion_role") not in ALLOWED_PROMOTION_ROLES:
        findings.append("invalid_promotion_role")
    if contract.get("canonical_status") not in ALLOWED_CANONICAL_STATUSES:
        findings.append("invalid_canonical_status")

    for list_field in [
        "input_families",
        "required_input_capabilities",
        "output_families",
        "required_output_capabilities",
        "output_schemas",
        "artifact_patterns",
    ]:
        if list_field in contract and not isinstance(contract[list_field], list):
            findings.append(f"field_not_list:{list_field}")
    return findings


def script_entry_from_contract(rel: Path, contract: dict[str, Any], parse_error: str | None) -> ScriptContractEntry:
    module = module_from_relative_path(rel)
    declared_script_id = str(contract.get("script_id") or "").strip() or None
    declared_module = str(contract.get("module") or "").strip() or None
    findings = validate_script_contract(contract)
    if parse_error:
        findings.append(parse_error)
    if declared_script_id and declared_script_id != module:
        findings.append(f"script_id_module_mismatch:declared={declared_script_id}:actual={module}")
    if declared_module and declared_module != module:
        findings.append(f"module_path_mismatch:declared={declared_module}:actual={module}")

    return ScriptContractEntry(
        script_id=module,
        declared_script_id=declared_script_id,
        path=normalize_rel(rel),
        module=module,
        purpose=str(contract.get("purpose") or ""),
        pipeline_stage=str(contract.get("pipeline_stage") or "unknown"),
        input_families=sorted_unique(as_str_list(contract.get("input_families"))),
        required_input_capabilities=sorted_unique(as_str_list(contract.get("required_input_capabilities"))),
        output_families=sorted_unique(as_str_list(contract.get("output_families"))),
        required_output_capabilities=sorted_unique(as_str_list(contract.get("required_output_capabilities"))),
        output_schemas=sorted_unique(as_str_list(contract.get("output_schemas"))),
        artifact_patterns=sorted_unique(as_str_list(contract.get("artifact_patterns"))),
        promotion_role=str(contract.get("promotion_role") or "unknown"),
        canonical_status=str(contract.get("canonical_status") or "unknown"),
        contract_status="valid" if not findings else "invalid",
        source="explicit_pipeline_contract",
        findings=findings,
    )


def unregistered_script_entry(rel: Path, parse_error: str | None) -> ScriptContractEntry:
    module = module_from_relative_path(rel)
    findings = ["missing_pipeline_contract"]
    if parse_error:
        findings.append(parse_error)
    return ScriptContractEntry(
        script_id=module,
        declared_script_id=None,
        path=normalize_rel(rel),
        module=module,
        purpose="",
        pipeline_stage="unknown",
        input_families=[],
        required_input_capabilities=[],
        output_families=[],
        required_output_capabilities=[],
        output_schemas=[],
        artifact_patterns=[],
        promotion_role="unknown",
        canonical_status="unknown",
        contract_status="unregistered",
        source="script_without_pipeline_contract",
        findings=findings,
    )


def discover_python_scripts(workspace: Path, scan_roots: list[Path]) -> list[Path]:
    paths: set[Path] = set()
    for root_arg in scan_roots:
        root = resolve_path(workspace, root_arg).resolve()
        if not root.exists():
            continue
        if root.is_file() and root.suffix == ".py" and root.name != "__init__.py" and not should_skip(root.relative_to(workspace)):
            paths.add(root)
            continue
        if root.is_dir():
            for path in root.rglob("*.py"):
                try:
                    rel = path.relative_to(workspace)
                except ValueError:
                    continue
                if path.name != "__init__.py" and not should_skip(rel):
                    paths.add(path.resolve())
    return sorted(paths, key=lambda p: normalize_rel(p.relative_to(workspace)))


def discover_script_contracts(workspace: Path, scan_roots: list[Path]) -> list[ScriptContractEntry]:
    entries: list[ScriptContractEntry] = []
    for path in discover_python_scripts(workspace, scan_roots):
        rel = path.relative_to(workspace)
        contract, parse_error = extract_pipeline_contract(path)
        if contract is None:
            entries.append(unregistered_script_entry(rel, parse_error))
        else:
            entries.append(script_entry_from_contract(rel, contract, parse_error))
    return entries


def run_help(module: str, workspace: Path, timeout_seconds: int) -> tuple[bool, int | None, str]:
    try:
        result = subprocess.run(
            [sys.executable, "-m", module, "--help"],
            cwd=workspace,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        return False, None, "TIMEOUT while running --help"
    except Exception as exc:
        return False, None, f"ERROR while running --help:{exc}"
    output = ((result.stdout or "") + (result.stderr or "")).strip()
    return result.returncode == 0, result.returncode, output


def discover_cli_contracts(workspace: Path, scan_roots: list[Path], timeout_seconds: int) -> list[ScriptCliEntry]:
    entries: list[ScriptCliEntry] = []
    for path in discover_python_scripts(workspace, scan_roots):
        rel = path.relative_to(workspace)
        module = module_from_relative_path(rel)
        ok, return_code, help_text = run_help(module, workspace, timeout_seconds)
        entries.append(ScriptCliEntry(normalize_rel(rel), module, ok, return_code, help_text))
    return entries


def read_jsonl_first_object(path: Path) -> Any | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    return json.loads(line)
    except Exception:
        return None
    return None


def read_markdown_metadata(path: Path) -> dict[str, Any]:
    text = read_text(path)
    marker = "```json"
    start = text.find(marker)
    if start == -1:
        return {}
    start += len(marker)
    end = text.find("```", start)
    if end == -1:
        return {}
    try:
        data = json.loads(text[start:end].strip())
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def load_artifact_data(path: Path) -> Any | None:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return read_json(path)
    if suffix == ".jsonl":
        return read_jsonl_first_object(path)
    if suffix == ".md":
        return read_markdown_metadata(path)
    return None


def extract_artifact_metadata(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        return {}
    metadata: dict[str, Any] = {}
    for key in ARTIFACT_METADATA_KEYS:
        if key in data:
            metadata[key] = data[key]
    nested = data.get("pipeline_contract")
    if isinstance(nested, dict):
        for key in ARTIFACT_METADATA_KEYS:
            if key in nested:
                metadata[key] = nested[key]
    return metadata


def extract_input_refs(data: Any) -> list[str]:
    refs: set[str] = set()
    def walk(value: Any) -> None:
        if isinstance(value, str):
            normalized = value.replace("\\", "/")
            if normalized.endswith((".json", ".jsonl", ".md", ".lua", ".py", ".yaml", ".yml")):
                refs.add(normalized)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, dict):
            for item in value.values():
                walk(item)
    walk(data)
    return sorted(refs)


def artifact_id_from_path(rel: Path) -> str:
    return normalize_rel(rel.with_suffix(""))


def discover_artifact_files(workspace: Path, scan_roots: list[Path]) -> list[Path]:
    paths: set[Path] = set()
    for root_arg in scan_roots:
        root = resolve_path(workspace, root_arg).resolve()
        if not root.exists():
            continue
        candidates = [root] if root.is_file() else root.rglob("*")
        for path in candidates:
            if not path.is_file() or path.suffix.lower() not in {".json", ".jsonl", ".md"}:
                continue
            try:
                rel = path.relative_to(workspace)
            except ValueError:
                continue
            if not should_skip(rel):
                paths.add(path.resolve())
    return sorted(paths, key=lambda p: normalize_rel(p.relative_to(workspace)))


def discover_artifacts(workspace: Path, scan_roots: list[Path], include_missing_metadata: bool) -> list[ArtifactEntry]:
    entries: list[ArtifactEntry] = []
    for path in discover_artifact_files(workspace, scan_roots):
        rel = path.relative_to(workspace)
        data = load_artifact_data(path)
        metadata = extract_artifact_metadata(data)
        schema = data.get("schema") if isinstance(data, dict) and isinstance(data.get("schema"), str) else None

        if not metadata and not schema and not include_missing_metadata:
            continue

        findings: list[str] = []
        if not metadata and schema is None:
            findings.append("missing_artifact_metadata")

        producer = metadata.get("producer_script")
        if producer is not None and not isinstance(producer, str):
            findings.append("invalid_producer_script")
            producer = None

        status = metadata.get("canonical_status")
        if status is not None and status not in ALLOWED_CANONICAL_STATUSES:
            findings.append("invalid_canonical_status")

        role = metadata.get("promotion_role")
        if role is not None and role not in ALLOWED_PROMOTION_ROLES:
            findings.append("invalid_promotion_role")

        output_families = as_str_list(metadata.get("output_families"))
        if not output_families:
            output_families = as_str_list(metadata.get("output_family") or metadata.get("artifact_family"))

        capabilities = as_str_list(metadata.get("capabilities"))
        if not capabilities:
            capabilities = as_str_list(metadata.get("required_capabilities"))

        entries.append(
            ArtifactEntry(
                artifact_id=str(metadata.get("artifact_id") or artifact_id_from_path(rel)),
                path=normalize_rel(rel),
                schema=schema,
                artifact_family=str(metadata.get("artifact_family")) if metadata.get("artifact_family") else None,
                producer_script=producer,
                pipeline_stage=str(metadata.get("pipeline_stage")) if metadata.get("pipeline_stage") else None,
                input_families=sorted_unique(as_str_list(metadata.get("input_families"))),
                output_families=sorted_unique(output_families),
                capabilities=sorted_unique(capabilities),
                promotion_role=str(role) if role else None,
                canonical_status=str(status) if status else None,
                inputs=sorted_unique(as_str_list(metadata.get("inputs")) or extract_input_refs(data)),
                source_files=sorted_unique(as_str_list(metadata.get("source_files"))),
                content_digest=str(metadata.get("content_digest")) if metadata.get("content_digest") else None,
                source="explicit_or_embedded_metadata" if metadata else "artifact_without_contract_metadata",
                findings=findings,
            )
        )
    return entries


def count_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        value = str(item.get(key) if item.get(key) is not None else "unknown")
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def fmt_list(values: list[Any] | None, limit: int = 5) -> str:
    items = [str(value) for value in (values or []) if str(value).strip()]
    if not items:
        return "—"
    visible = items[:limit]
    suffix = f" +{len(items) - limit}" if len(items) > limit else ""
    return ", ".join(f"`{item}`" for item in visible) + suffix


def fmt_value(value: Any) -> str:
    return "—" if value is None or value == "" else f"`{value}`"


def short_text(value: str, limit: int = 160) -> str:
    value = " ".join(str(value or "").split())
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


def sort_entries(entries: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    return sorted(entries, key=lambda item: (str(item.get(key) or ""), str(item.get("path") or "")))


def render_registry_md(registry: dict[str, Any]) -> str:
    scripts = registry["scripts"]
    artifacts = registry["artifacts"]
    findings = registry["findings"]
    valid_scripts = [entry for entry in scripts if entry.get("contract_status") == "valid"]
    unregistered_scripts = [entry for entry in scripts if entry.get("contract_status") == "unregistered"]
    invalid_scripts = [entry for entry in scripts if entry.get("contract_status") == "invalid"]
    artifact_with_metadata = [entry for entry in artifacts if entry.get("source") == "explicit_or_embedded_metadata"]
    artifact_without_metadata = [entry for entry in artifacts if entry.get("source") == "artifact_without_contract_metadata"]
    errors = [finding for finding in findings if finding.get("severity") == "error"]
    warnings = [finding for finding in findings if finding.get("severity") == "warning"]

    lines = [
        "# SIGNALIS AI — Pipeline Artifact Contract Preview",
        "",
        "This Markdown is a compact review surface generated from `pipeline_artifact_contract.json`.",
        "The JSON remains the complete machine-readable registry.",
        "",
        "## Summary",
        "",
        f"- Schema: `{registry['schema']}`",
        f"- Generated at: `{registry['generated_at']}`",
        f"- Script scan roots: `{len(registry.get('script_scan_roots', []))}`",
        f"- Artifact scan roots: `{len(registry.get('artifact_scan_roots', []))}`",
        f"- Scripts scanned: `{len(scripts)}`",
        f"- Valid script contracts: `{len(valid_scripts)}`",
        f"- Invalid script contracts: `{len(invalid_scripts)}`",
        f"- Unregistered scripts: `{len(unregistered_scripts)}`",
        f"- Artifacts scanned: `{len(artifacts)}`",
        f"- Artifacts with metadata: `{len(artifact_with_metadata)}`",
        f"- Artifacts without metadata: `{len(artifact_without_metadata)}`",
        f"- Errors: `{len(errors)}`",
        f"- Warnings: `{len(warnings)}`",
        "",
        "## Rules",
        "",
    ]
    for rule in registry["rules"]:
        lines.append(f"- {rule}")

    lines.extend(["", "## Scan Roots", "", "### Script scan roots", ""])
    for root in registry.get("script_scan_roots", []):
        lines.append(f"- `{root}`")
    lines.extend(["", "### Artifact scan roots", ""])
    for root in registry.get("artifact_scan_roots", []):
        lines.append(f"- `{root}`")

    lines.extend(["", "## Script Stage Counts", "", "| Stage | Count |", "|---|---:|"])
    for stage, count in count_by(scripts, "pipeline_stage").items():
        lines.append(f"| `{stage}` | {count} |")

    lines.extend(["", "## Script Contract Status Counts", "", "| Status | Count |", "|---|---:|"])
    for status, count in count_by(scripts, "contract_status").items():
        lines.append(f"| `{status}` | {count} |")

    lines.extend(["", "## Registered Scripts", ""])
    if not valid_scripts:
        lines.append("No valid registered scripts found.")
    else:
        lines.extend(["| Script | Stage | Inputs | Outputs | Capabilities | Status |", "|---|---|---|---|---|---|"])
        for entry in sort_entries(valid_scripts, "pipeline_stage"):
            lines.append(
                "| "
                f"`{entry['script_id']}`<br>`{entry['path']}` | "
                f"`{entry.get('pipeline_stage') or 'unknown'}` | "
                f"{fmt_list(entry.get('input_families'))} | "
                f"{fmt_list(entry.get('output_families'))} | "
                f"{fmt_list(entry.get('required_output_capabilities'))} | "
                f"`{entry.get('canonical_status') or 'unknown'}` |"
            )

    lines.extend(["", "## Invalid Script Contracts", ""])
    if not invalid_scripts:
        lines.append("No invalid script contracts.")
    else:
        lines.extend(["| Path | Actual module | Declared script_id | Findings |", "|---|---|---|---|"])
        for entry in sort_entries(invalid_scripts, "path"):
            lines.append(f"| `{entry['path']}` | `{entry.get('module')}` | {fmt_value(entry.get('declared_script_id'))} | {fmt_list(entry.get('findings'), 8)} |")

    lines.extend(["", "## Unregistered Scripts", ""])
    if not unregistered_scripts:
        lines.append("No unregistered scripts.")
    else:
        lines.append("These are findings only. No pipeline truth is inferred from them.")
        lines.extend(["", "| Path | Module | Findings |", "|---|---|---|"])
        for entry in sort_entries(unregistered_scripts, "path"):
            lines.append(f"| `{entry['path']}` | `{entry['module']}` | {fmt_list(entry.get('findings'), 4)} |")

    lines.extend(["", "## Artifact Metadata Source Counts", "", "| Source | Count |", "|---|---:|"])
    for source, count in count_by(artifacts, "source").items():
        lines.append(f"| `{source}` | {count} |")

    lines.extend(["", "## Artifacts With Contract Metadata", ""])
    if not artifact_with_metadata:
        lines.append("No artifacts with explicit/embedded contract metadata found.")
    else:
        lines.extend(["| Artifact | Producer | Stage | Family | Capabilities | Status |", "|---|---|---|---|---|---|"])
        for entry in sort_entries(artifact_with_metadata, "path"):
            family = entry.get("artifact_family") or fmt_list(entry.get("output_families"), 3)
            lines.append(
                "| "
                f"`{entry['artifact_id']}`<br>`{entry['path']}` | "
                f"{fmt_value(entry.get('producer_script'))} | "
                f"{fmt_value(entry.get('pipeline_stage'))} | "
                f"{fmt_value(family) if isinstance(family, str) and not family.startswith('`') else family} | "
                f"{fmt_list(entry.get('capabilities'), 4)} | "
                f"{fmt_value(entry.get('canonical_status'))} |"
            )

    if artifact_without_metadata:
        lines.extend(["", "## Artifacts Missing Metadata", ""])
        lines.append("Shown only because `--include-missing-artifacts` was used.")
        lines.extend(["", "| Path | Schema | Inputs detected |", "|---|---|---|"])
        for entry in sort_entries(artifact_without_metadata, "path"):
            lines.append(f"| `{entry['path']}` | {fmt_value(entry.get('schema'))} | {fmt_list(entry.get('inputs'), 5)} |")

    lines.extend(["", "## Findings", ""])
    if not findings:
        lines.append("No findings.")
    else:
        lines.extend(["| Severity | Path | Message |", "|---|---|---|"])
        for finding in sorted(findings, key=lambda item: (item.get("severity") != "error", item.get("path", ""), item.get("message", ""))):
            lines.append(f"| `{finding['severity']}` | `{finding['path']}` | `{short_text(finding['message'])}` |")

    return "\n".join(lines)


def render_cli_md(cli_contracts: dict[str, Any]) -> str:
    entries = cli_contracts["contracts"]
    lines = [
        "# SIGNALIS AI — Script CLI Contracts",
        "",
        "Generated from:",
        "",
        "```text",
        "python -m <module> --help",
        "```",
        "",
        "Purpose:",
        "",
        "- prevent guessed CLI usage",
        "- preserve script interfaces across chats",
        "- expose scripts without usable command-line help",
        "",
        f"- Scripts checked: `{len(entries)}`",
        "",
    ]
    by_group: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        parts = entry["path"].split("/")
        group = parts[1] if len(parts) > 1 else "root"
        by_group.setdefault(group, []).append(entry)
    for group, group_entries in sorted(by_group.items()):
        lines.extend([f"## {group}", ""])
        for entry in group_entries:
            status = "OK" if entry["help_ok"] else "NO_HELP_OR_ERROR"
            lines.extend([
                f"### `{entry['module']}`",
                "",
                f"- Path: `{entry['path']}`",
                f"- Help status: `{status}`",
                "",
                "```text",
                entry["help"] or "(no help output)",
                "```",
                "",
            ])
    return "\n".join(lines)


def build_findings(scripts: list[ScriptContractEntry], artifacts: list[ArtifactEntry]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for script in scripts:
        severity = "error" if script.contract_status == "invalid" else "warning"
        for message in script.findings:
            findings.append({"severity": severity, "path": script.path, "message": message})
    for artifact in artifacts:
        for message in artifact.findings:
            severity = "warning" if message == "missing_artifact_metadata" else "error"
            findings.append({"severity": severity, "path": artifact.path, "message": message})
    return findings


def normalize_scan_roots(workspace: Path, values: list[str] | None) -> list[Path]:
    if not values:
        return [workspace]
    return [Path(value) for value in values]


def rel_roots(workspace: Path, roots: list[Path]) -> list[str]:
    result: list[str] = []
    for root in roots:
        resolved = resolve_path(workspace, root).resolve()
        try:
            result.append(normalize_rel(resolved.relative_to(workspace)))
        except ValueError:
            result.append(normalize_rel(resolved))
    return sorted_unique(result)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build generic SIGNALIS AI pipeline artifact + script CLI contract registries.")
    parser.add_argument("--workspace", type=Path, required=True, help="Workspace root, e.g. E:/signalis_ai")
    parser.add_argument("--out-json", type=Path, default=Path("docs/runtime/pipeline_artifact_contract.json"))
    parser.add_argument("--out-md", type=Path, default=Path("docs/runtime/pipeline_artifact_contract.md"))
    parser.add_argument("--cli-out-json", type=Path, default=Path("docs/runtime/script_contracts.json"))
    parser.add_argument("--cli-out-md", type=Path, default=Path("docs/runtime/script_contracts.md"))
    parser.add_argument("--script-root", action="append", default=None, help="Optional scan root for Python scripts. Repeatable. Defaults to the workspace root.")
    parser.add_argument("--artifact-root", action="append", default=None, help="Optional scan root for artifacts. Repeatable. Defaults to the workspace root.")
    parser.add_argument("--include-missing-artifacts", action="store_true", help="Also include JSON/JSONL/MD files without explicit artifact metadata.")
    parser.add_argument("--skip-cli-help", action="store_true", help="Do not run python -m <module> --help.")
    parser.add_argument("--help-timeout", type=int, default=10)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    if not workspace.exists() or not workspace.is_dir():
        raise NotADirectoryError(f"Workspace is not a directory: {workspace}")

    script_roots = normalize_scan_roots(workspace, args.script_root)
    artifact_roots = normalize_scan_roots(workspace, args.artifact_root)

    scripts = discover_script_contracts(workspace, script_roots)
    artifacts = discover_artifacts(workspace, artifact_roots, args.include_missing_artifacts)
    findings = build_findings(scripts, artifacts)

    generated_at = utc_now()
    registry = {
        "schema": CONTRACT_SCHEMA,
        "generated_at": generated_at,
        "purpose": "Deterministic registry for explicit SIGNALIS AI pipeline script contracts and artifact metadata.",
        "rules": [
            "The registry scans the workspace by default; it does not depend on hardcoded script or artifact subdirectories.",
            "Script pipeline truth comes only from explicit PIPELINE_CONTRACT dictionaries.",
            "The filesystem/module path is evidence; a declared script_id that does not match the actual module is a finding.",
            "The registry does not infer pipeline stage, schema, or benchmark identity from filename versions.",
            "Artifacts become pipeline truth only through explicit or embedded artifact metadata.",
            "Files without artifact metadata are omitted by default and may be surfaced with --include-missing-artifacts for cleanup.",
            "CLI contracts are captured separately from semantic pipeline contracts.",
        ],
        "allowed_promotion_roles": ALLOWED_PROMOTION_ROLES,
        "allowed_canonical_statuses": ALLOWED_CANONICAL_STATUSES,
        "script_scan_roots": rel_roots(workspace, script_roots),
        "artifact_scan_roots": rel_roots(workspace, artifact_roots),
        "scripts": [asdict(entry) for entry in scripts],
        "artifacts": [asdict(entry) for entry in artifacts],
        "findings": findings,
    }

    cli_registry = {"schema": SCRIPT_HELP_SCHEMA, "generated_at": generated_at, "contracts": []}
    if not args.skip_cli_help:
        cli_registry["contracts"] = [asdict(entry) for entry in discover_cli_contracts(workspace, script_roots, args.help_timeout)]

    out_json = resolve_path(workspace, args.out_json)
    out_md = resolve_path(workspace, args.out_md)
    cli_out_json = resolve_path(workspace, args.cli_out_json)
    cli_out_md = resolve_path(workspace, args.cli_out_md)

    write_json(out_json, registry)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_registry_md(registry) + "\n", encoding="utf-8")
    write_json(cli_out_json, cli_registry)
    cli_out_md.parent.mkdir(parents=True, exist_ok=True)
    cli_out_md.write_text(render_cli_md(cli_registry) + "\n", encoding="utf-8")

    errors = [finding for finding in findings if finding["severity"] == "error"]
    print(f"Wrote JSON: {out_json.relative_to(workspace)}")
    print(f"Wrote MD:   {out_md.relative_to(workspace)}")
    print(f"Wrote CLI JSON: {cli_out_json.relative_to(workspace)}")
    print(f"Wrote CLI MD:   {cli_out_md.relative_to(workspace)}")
    print(f"Scripts:    {len(scripts)}")
    print(f"Artifacts:  {len(artifacts)}")
    print(f"Findings:   {len(findings)}")
    print(f"Errors:     {len(errors)}")
    return 1 if args.fail_on_error and errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
