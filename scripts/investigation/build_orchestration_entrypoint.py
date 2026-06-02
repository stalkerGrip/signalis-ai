from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_ID = "scripts.investigation.build_orchestration_entrypoint"
ARTIFACT_FAMILY = "orchestration_request"
SCHEMA = "orchestration_request"
SCHEMA_VERSION = "1"


PIPELINE_CONTRACT = {
    "script_id": SCRIPT_ID,
    "purpose": "Build a normalization-only orchestration_request artifact from request text.",
    "pipeline_stage": "orchestration",
    "input_families": [],
    "output_families": ["orchestration_request"],
    "required_capabilities": [
        "request_text",
        "normalized_request_text",
    ],
    "artifact_patterns": [
        "investigations/orchestration/*_orchestration_request.json",
    ],
    "promotion_role": "context_or_debug",
    "canonical_status": "active",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def slugify(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in value).strip("_")

    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")

    return cleaned[:80] or ARTIFACT_FAMILY


def stable_artifact_id(identity_payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        identity_payload,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")

    digest = hashlib.sha256(encoded).hexdigest()[:16]
    return f"{ARTIFACT_FAMILY}:{digest}"


def split_optional_values(values: list[str]) -> list[str]:
    result: list[str] = []

    for value in values:
        for part in value.split(";"):
            normalized = normalize_text(part)
            if normalized:
                result.append(normalized)

    return result


def build_orchestration_request(
    *,
    request_text: str,
    input_kind: str,
    user_constraints: list[str],
    source_preferences: list[str],
    input_artifacts: list[str],
    parent_artifact_id: str | None,
    regenerates: str | None,
) -> dict[str, Any]:
    request_text = request_text.strip()
    normalized_request_text = normalize_text(request_text)
    input_kind = normalize_text(input_kind) or "human_request"

    identity_payload = {
        "artifact_family": ARTIFACT_FAMILY,
        "request_text": request_text,
    }

    artifact = {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "artifact_family": ARTIFACT_FAMILY,
        "artifact_id": stable_artifact_id(identity_payload),
        "producer_script": SCRIPT_ID,
        "pipeline_stage": "orchestration",
        "canonical_status": "intermediate",
        "promotion_role": "context_or_debug",
        "generated_at": utc_now(),
        "required_capabilities": [
            "request_text",
            "normalized_request_text",
        ],
        "request_text": request_text,
        "normalized_request_text": normalized_request_text,
        "user_constraints": user_constraints,
        "source_preferences": source_preferences,
        "lineage": {
            "input_kind": input_kind,
            "input_artifacts": input_artifacts,
            "parent_artifact_id": parent_artifact_id,
            "regenerates": regenerates,
            "regeneration_inputs": [
                "request_text",
                "producer_script",
                "schema",
            ],
        },
    }

    validate_artifact(artifact)
    return artifact


def validate_artifact(artifact: dict[str, Any]) -> None:
    required_metadata = [
        "schema",
        "schema_version",
        "artifact_family",
        "artifact_id",
        "producer_script",
        "pipeline_stage",
        "canonical_status",
        "promotion_role",
        "generated_at",
        "required_capabilities",
        "lineage",
    ]

    for field in required_metadata:
        if field not in artifact:
            raise ValueError(f"Missing required metadata field: {field}")

    if artifact["schema"] != SCHEMA:
        raise ValueError(f"Invalid schema: {artifact['schema']}")

    if artifact["artifact_family"] != ARTIFACT_FAMILY:
        raise ValueError(f"Invalid artifact_family: {artifact['artifact_family']}")

    if artifact["producer_script"] != SCRIPT_ID:
        raise ValueError(f"Invalid producer_script: {artifact['producer_script']}")

    for capability in artifact["required_capabilities"]:
        if capability not in artifact:
            raise ValueError(f"Missing required capability: {capability}")

        value = artifact[capability]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Required capability must be a non-empty string: {capability}")

    if not isinstance(artifact["lineage"], dict):
        raise ValueError("lineage must be an object")


def resolve_output_path(workspace: Path, request_text: str, explicit_out: str | None) -> Path:
    if explicit_out:
        path = Path(explicit_out)
        return path if path.is_absolute() else workspace / path

    slug = slugify(request_text)
    return workspace / "investigations" / "orchestration" / f"{slug}_orchestration_request.json"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a normalization-only orchestration_request artifact."
    )

    parser.add_argument("--workspace", required=True)
    parser.add_argument("--request", required=True)
    parser.add_argument("--input-kind", default="human_request")

    parser.add_argument("--user-constraint", action="append", default=[])
    parser.add_argument("--source-preference", action="append", default=[])
    parser.add_argument("--input-artifact", action="append", default=[])

    parser.add_argument("--parent-artifact-id", default=None)
    parser.add_argument("--regenerates", default=None)
    parser.add_argument("--out", default=None)

    args = parser.parse_args()

    workspace = Path(args.workspace)
    request_text = args.request.strip()

    if not request_text:
        raise ValueError("--request must not be empty")

    artifact = build_orchestration_request(
        request_text=request_text,
        input_kind=args.input_kind,
        user_constraints=split_optional_values(args.user_constraint),
        source_preferences=split_optional_values(args.source_preference),
        input_artifacts=split_optional_values(args.input_artifact),
        parent_artifact_id=args.parent_artifact_id,
        regenerates=args.regenerates,
    )

    out_path = resolve_output_path(workspace, request_text, args.out)
    write_json(out_path, artifact)

    print(f"Wrote orchestration_request: {out_path}")


if __name__ == "__main__":
    main()