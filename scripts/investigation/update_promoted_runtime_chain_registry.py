from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any
import re


PIPELINE_CONTRACT = {
    "script_id": "scripts.investigation.update_promoted_runtime_chain_registry",
    "purpose": "Build promoted runtime chain registry from canonical promotion decisions.",
    "pipeline_stage": "promotion",
    "input_schemas": [
        "runtime_chain_promotion_decision.v4",
    ],
    "output_schemas": [
        "promoted_runtime_chain_registry.v1",
    ],
    "artifact_patterns": [
        "manifests/runtime/promoted_runtime_chains.json",
    ],
    "promotion_role": "promotion_support",
    "canonical_status": "active",
}


PROMOTED_STATUSES = {
    "promoted_confirmed_chain",
    "promoted_topology_supported_chain",
    "promoted_source_validated_chain",
}


def logical_chain_id(value: str | None) -> str:
    if not value:
        return "unknown"

    text = str(value).lower().replace("\\", "/")
    text = Path(text).stem

    text = re.sub(
        r"_runtime_chain_candidate_v\d+$",
        "",
        text,
    )

    text = re.sub(
        r"_promotion_decision(?:_v\d+)?$",
        "",
        text,
    )

    text = re.sub(
        r"_promoted_(confirmed_chain|topology_supported_chain|source_validated_chain)$",
        "",
        text,
    )

    return text


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def resolve_workspace_path(workspace: Path, value: Any) -> Path | None:
    if not value:
        return None

    path = Path(str(value))

    if path.is_absolute():
        return path

    return workspace / path


def read_candidate_steps(candidate_path: Path | None) -> tuple[str | None, list[str]]:
    if not candidate_path or not candidate_path.exists():
        return None, []

    payload = read_json(candidate_path)

    title = payload.get("title")

    steps = []

    for stage in payload.get("stages", []):
        name = stage.get("stage")
        if name:
            steps.append(name)

    return title, steps


def discover_decisions(validation_dir: Path) -> list[Path]:
    return sorted(validation_dir.glob("*promotion_decision*.json"))


def decision_timestamp(payload: dict[str, Any]) -> str:
    value = payload.get("generated_at")

    if isinstance(value, str):
        return value

    return ""


def promoted_artifact_key(workspace: Path, payload: dict[str, Any], fallback: str) -> str:
    outputs = payload.get("outputs", {})
    promoted_md = outputs.get("promoted_md")

    if promoted_md:
        path = resolve_workspace_path(workspace, promoted_md)
        if path:
            try:
                return str(path.resolve()).lower()
            except OSError:
                return str(path).lower()

    benchmark = payload.get("benchmark")
    if benchmark:
        return str(benchmark)

    return fallback


def is_promoted_decision(payload: dict[str, Any]) -> bool:
    if payload.get("schema") != "runtime_chain_promotion_decision.v4":
        return False

    if payload.get("canonical_status") != "canonical":
        return False

    decision = payload.get("decision", {})
    if decision.get("decision") not in PROMOTED_STATUSES:
        return False

    outputs = payload.get("outputs", {})
    promoted_md = outputs.get("promoted_md")
    if not promoted_md:
        return False

    return True


def build_registry_entry(
    workspace: Path,
    decision_file: Path,
    decision_payload: dict[str, Any],
) -> dict[str, Any]:

    decision = decision_payload.get("decision", {})
    outputs = decision_payload.get("outputs", {})
    inputs = decision_payload.get("inputs", [])

    benchmark = decision_payload.get(
        "benchmark",
        decision_file.stem,
    )

    candidate_path = None
    if len(inputs) > 0:
        candidate_path = resolve_workspace_path(workspace, inputs[0])

    title, steps = read_candidate_steps(candidate_path)

    return {
        "chain_id": benchmark,
        "logical_chain_id": logical_chain_id(benchmark),
        "title": title,
        "promotion_status": decision.get("decision"),
        "confidence": decision.get("confidence"),
        "score": decision.get("score"),
        "runtime_chain_steps": steps,
        "stages_total": len(steps),
        "generated_at": decision_payload.get("generated_at"),
        "decision_artifact": str(decision_file),
        "candidate_artifact": inputs[0] if len(inputs) > 0 else None,
        "promotion_validation_artifact": inputs[1] if len(inputs) > 1 else None,
        "promoted_artifact": outputs.get("promoted_md"),
    }


def collect_latest_promoted_decisions(
    workspace: Path,
    validation_dir: Path,
) -> list[tuple[Path, dict[str, Any]]]:
    latest_by_logical_chain: dict[str, tuple[Path, dict[str, Any]]] = {}

    for decision_file in discover_decisions(validation_dir):
        payload = read_json(decision_file)

        if not is_promoted_decision(payload):
            continue

        benchmark = payload.get("benchmark") or decision_file.stem
        key = logical_chain_id(benchmark)

        existing = latest_by_logical_chain.get(key)
        if existing is None:
            latest_by_logical_chain[key] = (decision_file, payload)
            continue

        _, existing_payload = existing
        if decision_timestamp(payload) >= decision_timestamp(existing_payload):
            latest_by_logical_chain[key] = (decision_file, payload)

    return sorted(
        latest_by_logical_chain.values(),
        key=lambda item: logical_chain_id(item[1].get("benchmark", item[0].stem)),
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build promoted runtime chain registry."
    )

    parser.add_argument(
        "--workspace",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--validation-dir",
        type=Path,
        default=None,
    )

    parser.add_argument(
        "--out",
        type=Path,
        default=None,
    )

    args = parser.parse_args()

    workspace = args.workspace.resolve()

    validation_dir = (
        args.validation_dir
        or workspace / "investigations" / "validation"
    )

    out_file = (
        args.out
        or workspace
        / "manifests"
        / "runtime"
        / "promoted_runtime_chains.json"
    )

    promoted_decisions = collect_latest_promoted_decisions(
        workspace=workspace,
        validation_dir=validation_dir,
    )

    chains = [
        build_registry_entry(
            workspace=workspace,
            decision_file=decision_file,
            decision_payload=payload,
        )
        for decision_file, payload in promoted_decisions
    ]

    chains.sort(
        key=lambda x: x["chain_id"]
    )

    registry = {
        "schema": "promoted_runtime_chain_registry.v1",
        "producer_script": PIPELINE_CONTRACT["script_id"],
        "pipeline_stage": "promotion",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "chains_total": len(chains),
        "chains": chains,
    }

    write_json(
        out_file,
        registry,
    )

    print(
        f"Promoted chains: {len(chains)}"
    )

    print(
        f"Wrote registry: {out_file}"
    )


if __name__ == "__main__":
    main()
