"""Build canonical orchestration_scope artifacts for SIGNALIS AI.

This script is intentionally capability-driven.
It does not contain benchmark-specific routing, subsystem-specific routing tables,
hidden keyword maps, or version-coupled orchestration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

PIPELINE_CONTRACT = {
    "script_id": "scripts.investigation.build_orchestration_scope",
    "purpose": "Build a capability-driven orchestration_scope artifact from an orchestration_request artifact and optional external orchestration index signals.",
    "pipeline_stage": "orchestration",
    "input_families": ["orchestration_request"],
    "required_input_capabilities": ["request_text", "normalized_request_text"],
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
REQUIRED_INPUT_CAPABILITIES = ["request_text", "normalized_request_text"]
REQUIRED_OUTPUT_CAPABILITIES = [
    "subsystem_scope",
    "realm_scope",
    "runtime_surface_scope",
]
SCOPE_TYPES = ("subsystem", "realm", "runtime_surface")

TOKEN_RE = re.compile(r"[A-Za-z0-9_:/.-]+")


class ContractError(ValueError):
    """Raised when an input artifact does not satisfy the family contract."""


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


def validate_orchestration_request(data: dict[str, Any], path: Path) -> None:
    family = data.get("artifact_family")
    if family != "orchestration_request":
        raise ContractError(
            f"Expected artifact_family 'orchestration_request' in {path}, got {family!r}"
        )

    capabilities = set(data.get("required_capabilities") or [])
    missing_caps = [cap for cap in REQUIRED_INPUT_CAPABILITIES if cap not in capabilities]
    missing_fields = [cap for cap in REQUIRED_INPUT_CAPABILITIES if not data.get(cap)]

    if missing_caps:
        raise ContractError(
            f"Input artifact lacks required capabilities {missing_caps}: {path}"
        )
    if missing_fields:
        raise ContractError(
            f"Input artifact lacks required fields {missing_fields}: {path}"
        )


def tokenize(text: str) -> set[str]:
    return {m.group(0).lower() for m in TOKEN_RE.finditer(text or "")}


def normalize_aliases(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    return []


def load_index(path: Path | None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if path is None:
        return [], {
            "index_present": False,
            "index_path": None,
            "index_digest": None,
            "index_schema": None,
        }

    data = load_json(path)
    raw_entries = data.get("entries", data.get("scopes", []))
    if not isinstance(raw_entries, list):
        raise ContractError("orchestration index must contain a list under entries or scopes")

    entries: list[dict[str, Any]] = []
    for index, item in enumerate(raw_entries):
        if not isinstance(item, dict):
            continue
        scope_type = str(item.get("scope_type") or item.get("type") or "").strip()
        scope_id = str(item.get("scope_id") or item.get("id") or item.get("name") or "").strip()
        if scope_type not in SCOPE_TYPES or not scope_id:
            continue
        aliases = normalize_aliases(item.get("aliases"))
        if scope_id not in aliases:
            aliases.append(scope_id)
        entries.append(
            {
                "scope_type": scope_type,
                "scope_id": scope_id,
                "display_name": item.get("display_name") or scope_id,
                "aliases": aliases,
                "source_artifact": item.get("source_artifact"),
                "source_family": item.get("source_family"),
                "capabilities": item.get("capabilities") or [],
            }
        )

    return entries, {
        "index_present": True,
        "index_path": str(path),
        "index_digest": stable_hash(data, 24),
        "index_schema": data.get("schema"),
    }


def match_entries(
    request_text: str,
    entries: Iterable[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    tokens = tokenize(request_text)
    lowered_text = request_text.lower()
    grouped: dict[str, list[dict[str, Any]]] = {key: [] for key in SCOPE_TYPES}

    for entry in entries:
        matched_aliases: list[str] = []
        for alias in entry.get("aliases", []):
            alias_norm = normalize_text(str(alias)).lower()
            if not alias_norm:
                continue
            if " " in alias_norm or "/" in alias_norm or ":" in alias_norm:
                if alias_norm in lowered_text:
                    matched_aliases.append(alias_norm)
            elif alias_norm in tokens:
                matched_aliases.append(alias_norm)

        if not matched_aliases:
            continue

        grouped[entry["scope_type"]].append(
            {
                "scope_id": entry["scope_id"],
                "display_name": entry.get("display_name") or entry["scope_id"],
                "confidence": "medium",
                "evidence_source": "orchestration_index_alias_match",
                "matched_aliases": sorted(set(matched_aliases)),
                "source_artifact": entry.get("source_artifact"),
                "source_family": entry.get("source_family"),
                "reason": "Request text matched aliases supplied by an external orchestration index entry.",
            }
        )

    for values in grouped.values():
        values.sort(key=lambda item: (item["scope_id"], item.get("display_name") or ""))

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
        "reason": reason,
    }


def build_scope(
    request: dict[str, Any],
    request_path: Path,
    index_entries: list[dict[str, Any]],
    index_metadata: dict[str, Any],
) -> dict[str, Any]:
    request_text = str(request.get("request_text") or "")
    normalized_request_text = normalize_text(str(request.get("normalized_request_text") or request_text))
    request_artifact_id = request.get("artifact_id")

    grouped = match_entries(normalized_request_text, index_entries)

    if not index_metadata.get("index_present"):
        no_index_reason = (
            "No orchestration_index was provided. Scope remains explicit unknown rather "
            "than using hidden keyword maps."
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
                        f"No {scope_type} evidence matched the external orchestration_index.",
                    )
                )

    identity_payload = {
        "artifact_family": ARTIFACT_FAMILY,
        "producer_script": SCRIPT_ID,
        "input_artifact_id": request_artifact_id,
        "normalized_request_text": normalized_request_text,
        "index_digest": index_metadata.get("index_digest"),
        "scope": grouped,
    }
    artifact_id = f"{ARTIFACT_FAMILY}:{stable_hash(identity_payload, 20)}"

    scope_summary = {
        "subsystems": [item["scope_id"] for item in grouped["subsystem"]],
        "realms": [item["scope_id"] for item in grouped["realm"]],
        "runtime_surfaces": [item["scope_id"] for item in grouped["runtime_surface"]],
    }

    confidence_notes: list[str] = []
    for scope_type in SCOPE_TYPES:
        if any(item["scope_id"] == "unknown" for item in grouped[scope_type]):
            confidence_notes.append(f"{scope_type} scope contains unknown due to missing matched evidence")

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
            "parent_artifact_id": request_artifact_id,
            "regenerates": None,
            "regeneration_inputs": {
                "orchestration_request_artifact_id": request_artifact_id,
                "orchestration_request_digest": stable_hash(request, 24),
                "orchestration_index_digest": index_metadata.get("index_digest"),
                "producer_script": SCRIPT_ID,
                "schema": SCHEMA,
                "schema_version": SCHEMA_VERSION,
            },
        },
        "contract_guards": {
            "no_benchmark_routing": True,
            "no_subsystem_routing_tables": True,
            "no_hidden_keyword_maps": True,
            "no_version_coupled_orchestration": True,
            "consumes_by_artifact_family": True,
            "consumes_by_required_capabilities": True,
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
                    f"  - matched_aliases: {aliases}",
                    f"  - reason: {item['reason']}",
                ]
            )
        lines.append("")
        return lines

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
            f"- no_version_coupled_orchestration: `{scope['contract_guards']['no_version_coupled_orchestration']}`",
            "",
            "## Lineage",
            "",
            f"- parent_artifact_id: `{scope['lineage']['parent_artifact_id']}`",
            f"- input_artifacts: `{', '.join(scope['lineage']['input_artifacts'])}`",
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
        description="Build canonical orchestration_scope from orchestration_request without hidden routing maps."
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
            "Optional external orchestration index JSON. Entries must provide "
            "scope_type, scope_id/id/name, and aliases. The script does not contain hidden scope maps."
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
