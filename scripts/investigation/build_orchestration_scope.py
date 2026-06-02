"""Build canonical orchestration_scope artifacts for SIGNALIS AI.

This script is intentionally capability-driven.

It consumes:
- orchestration_request
- optional orchestration_index

It does not contain benchmark-specific routing, subsystem-specific routing tables,
hidden keyword maps, hardcoded subsystem inference, or version-coupled orchestration.

Important architecture rule:

The orchestration_index is not truth.
It is a compact, evidence-backed scope-signal artifact.

This script only converts matched index signals into orchestration_scope entries.
If no index is supplied, or if supplied index signals do not match, scope remains
explicitly unknown.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

PIPELINE_CONTRACT = {
    "script_id": "scripts.investigation.build_orchestration_scope",
    "purpose": (
        "Build a capability-driven orchestration_scope artifact from an "
        "orchestration_request artifact and an optional contract-valid "
        "orchestration_index artifact."
    ),
    "pipeline_stage": "orchestration",
    "input_families": ["orchestration_request"],
    "optional_input_families": ["orchestration_index"],
    "required_input_capabilities": ["request_text", "normalized_request_text"],
    "optional_input_capabilities": ["scope_entries"],
    "output_families": ["orchestration_scope"],
    "required_output_capabilities": [
        "subsystem_scope",
        "realm_scope",
        "runtime_surface_scope",
    ],
    "output_schemas": ["orchestration_scope"],
    "artifact_patterns": [
        "investigations/orchestration/*_orchestration_scope.json",
        "investigations/orchestration/*_orchestration_scope.md",
    ],
    "promotion_role": "context_or_debug",
    "canonical_status": "active",
}

SCRIPT_ID = "scripts.investigation.build_orchestration_scope"
SCHEMA = "orchestration_scope"
SCHEMA_VERSION = "1"
ARTIFACT_FAMILY = "orchestration_scope"
PIPELINE_STAGE = "orchestration"
PROMOTION_ROLE = "context_or_debug"
CANONICAL_STATUS = "intermediate"

REQUEST_FAMILY = "orchestration_request"
INDEX_FAMILY = "orchestration_index"

REQUIRED_REQUEST_CAPABILITIES = ["request_text", "normalized_request_text"]
REQUIRED_INDEX_CAPABILITIES = ["scope_entries"]
REQUIRED_OUTPUT_CAPABILITIES = [
    "subsystem_scope",
    "realm_scope",
    "runtime_surface_scope",
]

SCOPE_TYPES = ("subsystem", "realm", "runtime_surface")
SCOPE_OUTPUT_FIELDS = {
    "subsystem": "subsystem_scope",
    "realm": "realm_scope",
    "runtime_surface": "runtime_surface_scope",
}
SCOPE_SUMMARY_FIELDS = {
    "subsystem": "subsystems",
    "realm": "realms",
    "runtime_surface": "runtime_surfaces",
}

ALLOWED_CONFIDENCE = {"low", "medium", "high"}
TOKEN_RE = re.compile(r"[A-Za-z0-9_:/.-]+")


class ContractError(ValueError):
    """Raised when an input artifact does not satisfy its family contract."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


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
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def require_family(data: dict[str, Any], expected_family: str, path: Path) -> None:
    family = data.get("artifact_family")
    if family != expected_family:
        raise ContractError(
            f"Expected artifact_family {expected_family!r} in {path}, got {family!r}"
        )


def require_capabilities(
    data: dict[str, Any],
    required_capabilities: Iterable[str],
    path: Path,
    artifact_name: str,
) -> None:
    capabilities = set(data.get("required_capabilities") or [])
    missing = [cap for cap in required_capabilities if cap not in capabilities]
    if missing:
        raise ContractError(
            f"{artifact_name} lacks required capabilities {missing}: {path}"
        )


def require_fields(
    data: dict[str, Any],
    required_fields: Iterable[str],
    path: Path,
    artifact_name: str,
) -> None:
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        raise ContractError(f"{artifact_name} lacks required fields {missing}: {path}")


def validate_orchestration_request(data: dict[str, Any], path: Path) -> None:
    require_family(data, REQUEST_FAMILY, path)
    require_capabilities(data, REQUIRED_REQUEST_CAPABILITIES, path, REQUEST_FAMILY)
    require_fields(data, REQUIRED_REQUEST_CAPABILITIES, path, REQUEST_FAMILY)


def tokenize(text: str) -> set[str]:
    return {match.group(0).lower() for match in TOKEN_RE.finditer(text or "")}


def normalize_aliases(value: Any, *, entry_id: str) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        candidates = [value]
    elif isinstance(value, list):
        candidates = [str(item) for item in value]
    else:
        raise ContractError(f"orchestration_index entry {entry_id!r} aliases must be a list or string")

    aliases = sorted({normalize_text(item) for item in candidates if normalize_text(item)})
    return aliases


def validate_index_entry(item: dict[str, Any], index: int, path: Path) -> dict[str, Any]:
    entry_id = str(item.get("entry_id") or item.get("scope_entry_id") or "").strip()
    if not entry_id:
        entry_id = f"entry:{index}"

    scope_type = str(item.get("scope_type") or "").strip()
    scope_id = str(item.get("scope_id") or "").strip()

    if scope_type not in SCOPE_TYPES:
        raise ContractError(
            f"Invalid scope_type in orchestration_index {path} entry {entry_id!r}: {scope_type!r}"
        )
    if not scope_id:
        raise ContractError(
            f"Missing scope_id in orchestration_index {path} entry {entry_id!r}"
        )

    aliases = normalize_aliases(item.get("aliases"), entry_id=entry_id)
    if scope_id not in aliases:
        aliases.append(scope_id)
        aliases = sorted(set(aliases))

    # These fields prevent the index from becoming a hidden keyword map.
    # A scope signal must point back to generated/source evidence.
    source_artifact = item.get("source_artifact")
    source_family = item.get("source_family")
    evidence_kind = item.get("evidence_kind")
    if not source_artifact:
        raise ContractError(
            f"orchestration_index entry {entry_id!r} lacks source_artifact"
        )
    if not source_family:
        raise ContractError(
            f"orchestration_index entry {entry_id!r} lacks source_family"
        )
    if not evidence_kind:
        raise ContractError(
            f"orchestration_index entry {entry_id!r} lacks evidence_kind"
        )

    confidence = str(item.get("confidence") or "medium").strip().lower()
    if confidence not in ALLOWED_CONFIDENCE:
        raise ContractError(
            f"orchestration_index entry {entry_id!r} has invalid confidence {confidence!r}"
        )

    lineage = item.get("lineage")
    if not isinstance(lineage, dict) or not lineage:
        raise ContractError(
            f"orchestration_index entry {entry_id!r} lacks non-empty lineage object"
        )

    return {
        "entry_id": entry_id,
        "scope_type": scope_type,
        "scope_id": scope_id,
        "display_name": item.get("display_name") or scope_id,
        "aliases": aliases,
        "source_artifact": source_artifact,
        "source_family": source_family,
        "evidence_kind": evidence_kind,
        "confidence": confidence,
        "lineage": lineage,
        "capabilities": item.get("capabilities") or [],
    }


def validate_orchestration_index(data: dict[str, Any], path: Path) -> None:
    require_family(data, INDEX_FAMILY, path)
    require_capabilities(data, REQUIRED_INDEX_CAPABILITIES, path, INDEX_FAMILY)

    if not data.get("artifact_id"):
        raise ContractError(f"orchestration_index lacks artifact_id: {path}")
    if "lineage" not in data or not isinstance(data["lineage"], dict):
        raise ContractError(f"orchestration_index lacks lineage object: {path}")

    if "scope_entries" not in data:
        raise ContractError(
            f"orchestration_index must contain canonical field scope_entries: {path}"
        )
    if not isinstance(data["scope_entries"], list):
        raise ContractError(f"orchestration_index scope_entries must be a list: {path}")


def load_index(path: Path | None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if path is None:
        return [], {
            "index_present": False,
            "index_path": None,
            "index_artifact_id": None,
            "index_digest": None,
            "index_schema": None,
            "index_schema_version": None,
            "index_required_capabilities": [],
            "index_entries_total": 0,
            "index_entries_accepted": 0,
        }

    data = load_json(path)
    validate_orchestration_index(data, path)

    entries = [
        validate_index_entry(item, index, path)
        for index, item in enumerate(data["scope_entries"])
        if isinstance(item, dict)
    ]

    return entries, {
        "index_present": True,
        "index_path": str(path),
        "index_artifact_id": data.get("artifact_id"),
        "index_digest": stable_hash(data, 24),
        "index_schema": data.get("schema"),
        "index_schema_version": data.get("schema_version"),
        "index_required_capabilities": data.get("required_capabilities") or [],
        "index_entries_total": len(data["scope_entries"]),
        "index_entries_accepted": len(entries),
    }


def alias_matches_request(alias: str, request_tokens: set[str], request_text_lower: str) -> bool:
    alias_norm = normalize_text(alias).lower()
    if not alias_norm:
        return False

    # Multi-token aliases are phrase evidence.
    if any(separator in alias_norm for separator in (" ", "/", ":")):
        return alias_norm in request_text_lower

    # Single-token aliases must match token boundaries.
    return alias_norm in request_tokens


def match_entries(
    request_text: str,
    entries: Iterable[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    tokens = tokenize(request_text)
    lowered_text = request_text.lower()
    grouped: dict[str, list[dict[str, Any]]] = {key: [] for key in SCOPE_TYPES}

    for entry in entries:
        matched_aliases = [
            alias
            for alias in entry.get("aliases", [])
            if alias_matches_request(alias, tokens, lowered_text)
        ]

        if not matched_aliases:
            continue

        grouped[entry["scope_type"]].append(
            {
                "scope_id": entry["scope_id"],
                "display_name": entry.get("display_name") or entry["scope_id"],
                "confidence": entry.get("confidence", "medium"),
                "evidence_source": "orchestration_index_scope_signal",
                "matched_aliases": sorted(set(matched_aliases)),
                "source_artifact": entry.get("source_artifact"),
                "source_family": entry.get("source_family"),
                "evidence_kind": entry.get("evidence_kind"),
                "index_entry_id": entry.get("entry_id"),
                "index_entry_lineage": entry.get("lineage"),
                "reason": (
                    "Request text matched aliases supplied by a contract-valid "
                    "orchestration_index entry. This is a scope signal, not validated truth."
                ),
            }
        )

    for values in grouped.values():
        values.sort(
            key=lambda item: (
                item["scope_id"],
                item.get("confidence") or "",
                item.get("display_name") or "",
            )
        )

    return grouped


def unknown_scope(scope_type: str, reason: str) -> dict[str, Any]:
    return {
        "scope_id": "unknown",
        "display_name": "unknown",
        "confidence": "low",
        "evidence_source": "insufficient_external_scope_evidence",
        "matched_aliases": [],
        "source_artifact": None,
        "source_family": None,
        "evidence_kind": None,
        "index_entry_id": None,
        "reason": reason,
    }


def build_scope(
    request: dict[str, Any],
    request_path: Path,
    index_entries: list[dict[str, Any]],
    index_metadata: dict[str, Any],
) -> dict[str, Any]:
    request_text = str(request.get("request_text") or "")
    normalized_request_text = normalize_text(
        str(request.get("normalized_request_text") or request_text)
    )
    request_artifact_id = request.get("artifact_id")

    grouped = match_entries(normalized_request_text, index_entries)

    if not index_metadata.get("index_present"):
        no_index_reason = (
            "No orchestration_index was provided. Scope remains explicit unknown "
            "rather than using hidden keyword maps or hardcoded routing."
        )
        grouped = {
            "subsystem": [unknown_scope("subsystem", no_index_reason)],
            "realm": [unknown_scope("realm", no_index_reason)],
            "runtime_surface": [unknown_scope("runtime_surface", no_index_reason)],
        }
    else:
        for scope_type in SCOPE_TYPES:
            if not grouped[scope_type]:
                grouped[scope_type].append(
                    unknown_scope(
                        scope_type,
                        (
                            f"No {scope_type} evidence matched the provided "
                            "contract-valid orchestration_index."
                        ),
                    )
                )

    identity_payload = {
        "artifact_family": ARTIFACT_FAMILY,
        "producer_script": SCRIPT_ID,
        "input_artifact_id": request_artifact_id,
        "normalized_request_text": normalized_request_text,
        "index_artifact_id": index_metadata.get("index_artifact_id"),
        "index_digest": index_metadata.get("index_digest"),
        "scope": grouped,
    }
    artifact_id = f"{ARTIFACT_FAMILY}:{stable_hash(identity_payload, 20)}"

    scope_summary = {
        SCOPE_SUMMARY_FIELDS[scope_type]: [
            item["scope_id"] for item in grouped[scope_type]
        ]
        for scope_type in SCOPE_TYPES
    }

    confidence_notes: list[str] = []
    for scope_type in SCOPE_TYPES:
        if any(item["scope_id"] == "unknown" for item in grouped[scope_type]):
            confidence_notes.append(
                f"{scope_type} scope contains unknown due to missing matched evidence"
            )

    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "artifact_family": ARTIFACT_FAMILY,
        "artifact_id": artifact_id,
        "producer_script": SCRIPT_ID,
        "pipeline_stage": PIPELINE_STAGE,
        "canonical_status": CANONICAL_STATUS,
        "promotion_role": PROMOTION_ROLE,
        "generated_at": utc_now(),
        "required_capabilities": REQUIRED_OUTPUT_CAPABILITIES,
        "input_artifacts": [str(request_path)],
        "upstream_artifact_ids": [request_artifact_id] if request_artifact_id else [],
        "scope_summary": scope_summary,
        "subsystem_scope": grouped["subsystem"],
        "realm_scope": grouped["realm"],
        "runtime_surface_scope": grouped["runtime_surface"],
        "confidence_notes": confidence_notes,
        "index_metadata": index_metadata,
        "lineage": {
            "input_kind": "orchestration_request",
            "input_artifacts": [str(request_path)],
            "optional_input_artifacts": (
                [index_metadata["index_path"]]
                if index_metadata.get("index_present") and index_metadata.get("index_path")
                else []
            ),
            "parent_artifact_id": request_artifact_id,
            "upstream_artifact_ids": [
                artifact_id_value
                for artifact_id_value in [
                    request_artifact_id,
                    index_metadata.get("index_artifact_id"),
                ]
                if artifact_id_value
            ],
            "regenerates": None,
            "regeneration_inputs": {
                "orchestration_request_artifact_id": request_artifact_id,
                "orchestration_request_digest": stable_hash(request, 24),
                "orchestration_index_artifact_id": index_metadata.get("index_artifact_id"),
                "orchestration_index_digest": index_metadata.get("index_digest"),
                "producer_script": SCRIPT_ID,
                "schema": SCHEMA,
            },
        },
        "contract_guards": {
            "no_benchmark_routing": True,
            "no_subsystem_routing_tables": True,
            "no_hidden_keyword_maps": True,
            "no_hardcoded_subsystem_inference": True,
            "no_version_coupled_orchestration": True,
            "consumes_by_artifact_family": True,
            "consumes_by_required_capabilities": True,
            "orchestration_index_required_when_scope_is_not_unknown": True,
            "orchestration_index_is_scope_signal_not_truth": True,
        },
    }


def render_md(scope: dict[str, Any]) -> str:
    def section(title: str, items: list[dict[str, Any]]) -> list[str]:
        lines = [f"## {title}", ""]
        for item in items:
            aliases = ", ".join(item.get("matched_aliases") or []) or "none"
            lines.extend(
                [
                    f"- `{item['scope_id']}` — confidence: `{item['confidence']}`",
                    f"  - evidence_source: `{item['evidence_source']}`",
                    f"  - evidence_kind: `{item.get('evidence_kind')}`",
                    f"  - source_family: `{item.get('source_family')}`",
                    f"  - source_artifact: `{item.get('source_artifact')}`",
                    f"  - index_entry_id: `{item.get('index_entry_id')}`",
                    f"  - matched_aliases: {aliases}",
                    f"  - reason: {item['reason']}",
                ]
            )
        lines.append("")
        return lines

    index_metadata = scope["index_metadata"]
    lines = [
        "# Orchestration Scope",
        "",
        f"- schema: `{scope['schema']}`",
        f"- artifact_family: `{scope['artifact_family']}`",
        f"- artifact_id: `{scope['artifact_id']}`",
        f"- producer_script: `{scope['producer_script']}`",
        f"- generated_at: `{scope['generated_at']}`",
        "",
        "## Scope Summary",
        "",
        f"- subsystems: `{', '.join(scope['scope_summary']['subsystems'])}`",
        f"- realms: `{', '.join(scope['scope_summary']['realms'])}`",
        f"- runtime_surfaces: `{', '.join(scope['scope_summary']['runtime_surfaces'])}`",
        "",
        "## Orchestration Index",
        "",
        f"- index_present: `{index_metadata['index_present']}`",
        f"- index_artifact_id: `{index_metadata.get('index_artifact_id')}`",
        f"- index_digest: `{index_metadata.get('index_digest')}`",
        f"- index_entries_accepted: `{index_metadata.get('index_entries_accepted')}`",
        "",
    ]
    lines.extend(section("Subsystem Scope", scope["subsystem_scope"]))
    lines.extend(section("Realm Scope", scope["realm_scope"]))
    lines.extend(section("Runtime Surface Scope", scope["runtime_surface_scope"]))
    lines.extend(
        [
            "## Contract Guards",
            "",
            f"- no_benchmark_routing: `{scope['contract_guards']['no_benchmark_routing']}`",
            f"- no_subsystem_routing_tables: `{scope['contract_guards']['no_subsystem_routing_tables']}`",
            f"- no_hidden_keyword_maps: `{scope['contract_guards']['no_hidden_keyword_maps']}`",
            f"- no_hardcoded_subsystem_inference: `{scope['contract_guards']['no_hardcoded_subsystem_inference']}`",
            f"- no_version_coupled_orchestration: `{scope['contract_guards']['no_version_coupled_orchestration']}`",
            f"- orchestration_index_required_when_scope_is_not_unknown: `{scope['contract_guards']['orchestration_index_required_when_scope_is_not_unknown']}`",
            f"- orchestration_index_is_scope_signal_not_truth: `{scope['contract_guards']['orchestration_index_is_scope_signal_not_truth']}`",
            "",
            "## Lineage",
            "",
            f"- parent_artifact_id: `{scope['lineage']['parent_artifact_id']}`",
            f"- input_artifacts: `{', '.join(scope['lineage']['input_artifacts'])}`",
            f"- optional_input_artifacts: `{', '.join(scope['lineage']['optional_input_artifacts'])}`",
            f"- orchestration_index_artifact_id: `{scope['lineage']['regeneration_inputs']['orchestration_index_artifact_id']}`",
            f"- orchestration_index_digest: `{scope['lineage']['regeneration_inputs']['orchestration_index_digest']}`",
            "",
        ]
    )
    return "\n".join(lines)


def default_output_paths(request_path: Path, out_dir: Path | None) -> tuple[Path, Path]:
    directory = out_dir or Path("investigations/orchestration")
    stem = request_path.stem
    if stem.endswith("_orchestration_request"):
        stem = stem[: -len("_orchestration_request")]
    json_path = directory / f"{stem}_orchestration_scope.json"
    md_path = directory / f"{stem}_orchestration_scope.md"
    return json_path, md_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build canonical orchestration_scope from orchestration_request. "
            "Optional scope evidence must come from a contract-valid orchestration_index."
        )
    )
    parser.add_argument(
        "--orchestration-request",
        required=True,
        type=Path,
        help="Path to an orchestration_request JSON artifact.",
    )
    parser.add_argument(
        "--orchestration-index",
        type=Path,
        default=None,
        help=(
            "Optional contract-valid orchestration_index JSON artifact. "
            "Must use artifact_family=orchestration_index and required_capabilities "
            "including scope_entries."
        ),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory. Defaults to investigations/orchestration.",
    )
    parser.add_argument("--out-json", type=Path, default=None, help="Explicit JSON output path.")
    parser.add_argument("--out-md", type=Path, default=None, help="Explicit Markdown output path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    request_path: Path = args.orchestration_request
    request = load_json(request_path)
    validate_orchestration_request(request, request_path)

    index_entries, index_metadata = load_index(args.orchestration_index)
    scope = build_scope(request, request_path, index_entries, index_metadata)

    default_json, default_md = default_output_paths(request_path, args.out_dir)
    out_json = args.out_json or default_json
    out_md = args.out_md or default_md

    write_json(out_json, scope)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(render_md(scope), encoding="utf-8")

    print(f"Wrote JSON: {out_json}")
    print(f"Wrote MD:   {out_md}")
    print(f"Artifact:   {scope['artifact_id']}")


if __name__ == "__main__":
    main()
