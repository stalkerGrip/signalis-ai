from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


PIPELINE_CONTRACT = {
    "script_id": "scripts.investigation.update_promoted_runtime_chain_registry",
    "pipeline_stage": "promotion",
    "input_schemas": [
        "runtime_chain_promotion_decision.v4",
    ],
    "output_schemas": [
        "promoted_runtime_chain_registry.v1",
    ],
    "canonical_status": "active",
}


PROMOTED_STATUSES = {
    "promoted_confirmed_chain",
    "promoted_topology_supported_chain",
}


def read_candidate_steps(candidate_path: Path) -> tuple[str | None, list[str]]:
    if not candidate_path.exists():
        return None, []

    payload = read_json(candidate_path)

    title = payload.get("title")

    steps = []

    for stage in payload.get("stages", []):
        name = stage.get("stage")
        if name:
            steps.append(name)

    return title, steps


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


def discover_decisions(validation_dir: Path) -> list[Path]:
    return sorted(
        validation_dir.glob("*_promotion_decision_v2.json")
    )


def build_registry_entry(
    decision_file: Path,
    decision_payload: dict[str, Any],
) -> dict[str, Any]:

    decision = decision_payload.get("decision", {})

    decision_name = decision.get("decision")

    if decision_name not in PROMOTED_STATUSES:
        return {}

    outputs = decision_payload.get("outputs", {})
    inputs = decision_payload.get("inputs", [])

    benchmark = decision_payload.get(
        "benchmark",
        decision_file.stem,
    )

    candidate_path = None

    if len(inputs) > 0:
        candidate_path = Path(inputs[0])

    title = None
    steps = []

    if candidate_path:
        title, steps = read_candidate_steps(candidate_path)

    return {
        "chain_id": benchmark,

        "title": title,

        "promotion_status": decision_name,

        "confidence": decision.get("confidence"),
        "score": decision.get("score"),

        "runtime_chain_steps": steps,
        "stages_total": len(steps),

        "generated_at": decision_payload.get("generated_at"),

        "decision_artifact": str(decision_file),

        "candidate_artifact":
            inputs[0] if len(inputs) > 0 else None,

        "promotion_validation_artifact":
            inputs[1] if len(inputs) > 1 else None,

        "promoted_artifact":
            outputs.get("promoted_md"),
    }


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

    chains = []

    for decision_file in discover_decisions(validation_dir):
        payload = read_json(decision_file)

        if payload.get("schema") != "runtime_chain_promotion_decision.v4":
            continue

        entry = build_registry_entry(
            decision_file,
            payload,
        )

        if entry:
            chains.append(entry)

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