"""Build a generic orchestration_index artifact for SIGNALIS AI.

The orchestration_index is a compact, evidence-backed scope-signal index.
It is not truth and it is not routing.

This script intentionally does not infer subsystems, realms, or runtime surfaces
from request text. It only collects explicit scope signals already present in
upstream evidence artifacts.

Accepted upstream signal fields:
- scope_entries
- scope_signals
- orchestration_scope_signals

Each signal must carry:
- scope_type: subsystem | realm | runtime_surface
- scope_id
- source_artifact
- source_family
- evidence_kind
- confidence: low | medium | high
- lineage

Optional signal fields:
- display_name
- aliases / match_terms
- capabilities
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCRIPT_ID = "scripts.investigation.build_orchestration_index"
SCHEMA = "orchestration_index"
SCHEMA_VERSION = "1"
ARTIFACT_FAMILY = "orchestration_index"
PIPELINE_STAGE = "orchestration"
PROMOTION_ROLE = "context_or_debug"
CANONICAL_STATUS = "intermediate"

REQUIRED_OUTPUT_CAPABILITIES = ["scope_entries"]
SCOPE_SIGNAL_FIELDS = ("scope_entries", "scope_signals", "orchestration_scope_signals")
SCOPE_TYPES = {"subsystem", "realm", "runtime_surface"}
ALLOWED_CONFIDENCE = {"low", "medium", "high"}

PIPELINE_CONTRACT = {
    "script_id": SCRIPT_ID,
    "purpose": (
        "Build a generic, evidence-backed orchestration_index artifact from "
        "upstream artifacts that explicitly expose orchestration scope signals."
    ),
    "pipeline_stage": PIPELINE_STAGE,
    "input_families": [],
    "required_input_capabilities": [],
    "output_families": [ARTIFACT_FAMILY],
    "required_output_capabilities": REQUIRED_OUTPUT_CAPABILITIES,
    "output_schemas": [SCHEMA],
    "artifact_patterns": [
        "investigations/orchestration/*_orchestration_index.json",
        "investigations/orchestration/*_orchestration_index.md",
    ],
    "promotion_role": "context_or_debug",
    "canonical_status": "active",
}


class ContractError(ValueError):
    """Raised when an evidence artifact or scope signal violates contract."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stable_hash(value: Any, length: int = 16) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()[:length]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ContractError(f"Expected JSON object in {path}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def split_optional_values(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        for part in str(value).split(";"):
            normalized = normalize_text(part)
            if normalized:
                result.append(normalized)
    return result


def discover_json_files(paths: Iterable[Path]) -> list[Path]:
    discovered: list[Path] = []
    for path in paths:
        if path.is_dir():
            discovered.extend(sorted(child for child in path.rglob("*.json") if child.is_file()))
        elif path.is_file():
            discovered.append(path)
        else:
            raise FileNotFoundError(path)
    return sorted(dict.fromkeys(discovered))


def normalize_terms(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        candidates = [value]
    elif isinstance(value, list):
        candidates = [str(item) for item in value]
    else:
        raise ContractError("aliases/match_terms must be a string or list")
    return sorted({normalize_text(item) for item in candidates if normalize_text(item)})


def first_signal_list(data: dict[str, Any]) -> tuple[str | None, list[Any]]:
    for field in SCOPE_SIGNAL_FIELDS:
        value = data.get(field)
        if value is None:
            continue
        if not isinstance(value, list):
            raise ContractError(f"{field} must be a list")
        return field, value
    return None, []


def source_descriptor(source_path: Path, source_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": str(source_path),
        "artifact_id": source_data.get("artifact_id"),
        "artifact_family": source_data.get("artifact_family"),
        "schema": source_data.get("schema"),
        "digest": stable_hash(source_data, 24),
    }


def normalize_signal(
    *,
    raw_signal: dict[str, Any],
    index: int,
    source_path: Path,
    source_data: dict[str, Any],
    signal_field: str,
) -> dict[str, Any]:
    scope_type = normalize_text(raw_signal.get("scope_type"))
    scope_id = normalize_text(raw_signal.get("scope_id"))

    if scope_type not in SCOPE_TYPES:
        raise ContractError(
            f"Invalid scope_type {scope_type!r} in {source_path} signal #{index}"
        )
    if not scope_id:
        raise ContractError(f"Missing scope_id in {source_path} signal #{index}")

    source_artifact = raw_signal.get("source_artifact") or source_data.get("artifact_id") or str(source_path)
    source_family = raw_signal.get("source_family") or source_data.get("artifact_family")
    evidence_kind = raw_signal.get("evidence_kind")
    confidence = normalize_text(raw_signal.get("confidence") or "low").lower()
    lineage = raw_signal.get("lineage")

    if not source_artifact:
        raise ContractError(f"Signal {scope_type}:{scope_id} lacks source_artifact")
    if not source_family:
        raise ContractError(f"Signal {scope_type}:{scope_id} lacks source_family")
    if not evidence_kind:
        raise ContractError(f"Signal {scope_type}:{scope_id} lacks evidence_kind")
    if confidence not in ALLOWED_CONFIDENCE:
        raise ContractError(
            f"Signal {scope_type}:{scope_id} has invalid confidence {confidence!r}"
        )
    if not isinstance(lineage, dict) or not lineage:
        raise ContractError(f"Signal {scope_type}:{scope_id} lacks non-empty lineage object")

    aliases = normalize_terms(raw_signal.get("aliases"))
    match_terms = normalize_terms(raw_signal.get("match_terms"))
    combined_terms = sorted(set(aliases + match_terms + [scope_id]))

    entry_payload = {
        "scope_type": scope_type,
        "scope_id": scope_id,
        "source_artifact": source_artifact,
        "source_family": source_family,
        "evidence_kind": evidence_kind,
        "lineage": lineage,
    }

    return {
        "entry_id": raw_signal.get("entry_id") or f"scope_signal:{stable_hash(entry_payload, 20)}",
        "scope_type": scope_type,
        "scope_id": scope_id,
        "display_name": raw_signal.get("display_name") or scope_id,
        "aliases": combined_terms,
        "source_artifact": source_artifact,
        "source_family": source_family,
        "evidence_kind": evidence_kind,
        "confidence": confidence,
        "lineage": {
            **lineage,
            "orchestration_index_signal_source": {
                "artifact_path": str(source_path),
                "artifact_id": source_data.get("artifact_id"),
                "artifact_family": source_data.get("artifact_family"),
                "signal_field": signal_field,
                "signal_index": index,
            },
        },
        "capabilities": raw_signal.get("capabilities") or [],
    }


def collect_scope_entries(paths: list[Path]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    entries: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []

    for path in paths:
        data = load_json(path)
        descriptor = source_descriptor(path, data)
        signal_field, signals = first_signal_list(data)
        descriptor["signal_field"] = signal_field
        descriptor["signals_total"] = len(signals)
        descriptor["signals_accepted"] = 0

        if not signal_field:
            sources.append(descriptor)
            continue

        for index, raw_signal in enumerate(signals):
            if not isinstance(raw_signal, dict):
                raise ContractError(f"Scope signal #{index} in {path} must be an object")
            entries.append(
                normalize_signal(
                    raw_signal=raw_signal,
                    index=index,
                    source_path=path,
                    source_data=data,
                    signal_field=signal_field,
                )
            )
            descriptor["signals_accepted"] += 1

        sources.append(descriptor)

    entries.sort(
        key=lambda item: (
            item["scope_type"],
            item["scope_id"],
            item["source_family"],
            item["source_artifact"],
            item["entry_id"],
        )
    )
    return entries, sources


def build_index(*, evidence_paths: list[Path], entries: list[dict[str, Any]], sources: list[dict[str, Any]]) -> dict[str, Any]:
    identity_payload = {
        "artifact_family": ARTIFACT_FAMILY,
        "producer_script": SCRIPT_ID,
        "source_digests": [source["digest"] for source in sources],
        "scope_entries": entries,
    }

    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "artifact_family": ARTIFACT_FAMILY,
        "artifact_id": f"{ARTIFACT_FAMILY}:{stable_hash(identity_payload, 20)}",
        "producer_script": SCRIPT_ID,
        "pipeline_stage": PIPELINE_STAGE,
        "canonical_status": CANONICAL_STATUS,
        "promotion_role": PROMOTION_ROLE,
        "generated_at": utc_now(),
        "required_capabilities": REQUIRED_OUTPUT_CAPABILITIES,
        "scope_entries": entries,
        "index_summary": {
            "evidence_artifacts_total": len(evidence_paths),
            "scope_entries_total": len(entries),
            "scope_types": sorted({entry["scope_type"] for entry in entries}),
        },
        "source_artifacts": sources,
        "lineage": {
            "input_kind": "explicit_scope_signal_artifacts",
            "input_artifacts": [str(path) for path in evidence_paths],
            "parent_artifact_id": None,
            "regenerates": None,
            "regeneration_inputs": {
                "input_artifact_digests": [source["digest"] for source in sources],
                "producer_script": SCRIPT_ID,
                "schema": SCHEMA,
            },
        },
        "contract_guards": {
            "no_benchmark_routing": True,
            "no_subsystem_routing_tables": True,
            "no_hidden_keyword_maps": True,
            "no_hardcoded_runtime_ontology": True,
            "no_version_coupled_orchestration": True,
            "entries_must_reference_source_evidence": True,
            "index_is_scope_signal_not_truth": True,
        },
    }


def render_md(index_artifact: dict[str, Any]) -> str:
    lines = [
        "# Orchestration Index",
        "",
        f"- schema: `{index_artifact['schema']}`",
        f"- artifact_family: `{index_artifact['artifact_family']}`",
        f"- artifact_id: `{index_artifact['artifact_id']}`",
        f"- producer_script: `{index_artifact['producer_script']}`",
        f"- generated_at: `{index_artifact['generated_at']}`",
        "",
        "## Summary",
        "",
        f"- evidence_artifacts_total: `{index_artifact['index_summary']['evidence_artifacts_total']}`",
        f"- scope_entries_total: `{index_artifact['index_summary']['scope_entries_total']}`",
        f"- scope_types: `{', '.join(index_artifact['index_summary']['scope_types'])}`",
        "",
        "## Scope Entries",
        "",
    ]

    if not index_artifact["scope_entries"]:
        lines.append("No explicit scope signals were found.")
        lines.append("")
    else:
        for entry in index_artifact["scope_entries"]:
            aliases = ", ".join(entry.get("aliases") or []) or "none"
            lines.extend(
                [
                    f"- `{entry['scope_type']}:{entry['scope_id']}` — confidence: `{entry['confidence']}`",
                    f"  - entry_id: `{entry['entry_id']}`",
                    f"  - evidence_kind: `{entry['evidence_kind']}`",
                    f"  - source_family: `{entry['source_family']}`",
                    f"  - source_artifact: `{entry['source_artifact']}`",
                    f"  - aliases: {aliases}",
                ]
            )
        lines.append("")

    lines.extend([
        "## Contract Guards",
        "",
    ])
    for key, value in index_artifact["contract_guards"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build orchestration_index from explicit upstream scope-signal artifacts. "
            "No request-text routing or hidden keyword maps are used."
        )
    )
    parser.add_argument("--workspace", type=Path, default=Path("."))
    parser.add_argument(
        "--evidence-artifact",
        action="append",
        default=[],
        help="JSON artifact or directory containing JSON artifacts with explicit scope signals.",
    )
    parser.add_argument("--out-json", type=Path, default=None)
    parser.add_argument("--out-md", type=Path, default=None)
    return parser.parse_args()


def resolve_path(workspace: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else workspace / path


def main() -> None:
    args = parse_args()
    workspace: Path = args.workspace
    evidence_roots = [resolve_path(workspace, item) for item in split_optional_values(args.evidence_artifact)]
    evidence_paths = discover_json_files(evidence_roots) if evidence_roots else []

    entries, sources = collect_scope_entries(evidence_paths)
    index_artifact = build_index(evidence_paths=evidence_paths, entries=entries, sources=sources)

    out_json = args.out_json or workspace / "investigations" / "orchestration" / "orchestration_index.json"
    out_md = args.out_md or workspace / "investigations" / "orchestration" / "orchestration_index.md"
    out_json = resolve_path(workspace, out_json)
    out_md = resolve_path(workspace, out_md)

    write_json(out_json, index_artifact)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_md(index_artifact), encoding="utf-8")

    print(f"Scope entries: {len(entries)}")
    print(f"Wrote JSON: {out_json}")
    print(f"Wrote MD:   {out_md}")
    print(f"Artifact:   {index_artifact['artifact_id']}")


if __name__ == "__main__":
    main()
