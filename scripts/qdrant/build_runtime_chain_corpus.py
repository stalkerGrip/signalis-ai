from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


PIPELINE_CONTRACT = {
    "script_id": "scripts.qdrant.build_runtime_chain_corpus",
    "purpose": (
        "Build retrieval-ready runtime chain corpus documents from the "
        "promoted runtime chain registry."
    ),
    "pipeline_stage": "retrieval",
    "input_schemas": [
        "promoted_runtime_chain_registry.v1"
    ],
    "output_schemas": [
        "runtime_chain_corpus.v1"
    ],
    "artifact_patterns": [
        "manifests/semantic/runtime_chain_corpus.jsonl"
    ],
    "promotion_role": "promotion_support",
    "canonical_status": "active"
}


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            f.write("\n")


def normalize_path(path: Any) -> str | None:
    if path is None:
        return None
    return str(path).replace("\\", "/")


def build_content(chain: dict[str, Any]) -> str:
    title = chain.get("title") or chain.get("chain_id")
    steps = chain.get("runtime_chain_steps") or []

    chain_text = " -> ".join(str(step) for step in steps)

    parts = [
        f"Promoted runtime chain: {title}",
        f"Chain ID: {chain.get('chain_id')}",
        f"Promotion status: {chain.get('promotion_status')}",
        f"Confidence: {chain.get('confidence')}",
        f"Score: {chain.get('score')}",
        f"Runtime propagation: {chain_text}",
    ]

    return "\n".join(part for part in parts if part)


def build_doc(
    chain: dict[str, Any],
    registry_path: Path,
    registry: dict[str, Any],
) -> dict[str, Any]:
    chain_id = chain.get("chain_id")
    steps = chain.get("runtime_chain_steps") or []

    KNOWN_FIELDS = {
        "chain_id",
        "title",
        "promotion_status",
        "confidence",
        "score",
        "stages_total",
        "runtime_chain_steps",
        "decision_artifact",
        "candidate_artifact",
        "promotion_validation_artifact",
        "promoted_artifact",
    }

    return {
        "schema": "runtime_chain_corpus.v1",
        "producer_script": PIPELINE_CONTRACT["script_id"],
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_registry_schema": registry.get("schema"),
        "source_registry_generated_at": registry.get("generated_at"),
        "doc_type": "promoted_runtime_chain",
        "id": f"promoted_runtime_chain:{chain_id}",
        "chain_id": chain_id,
        "title": chain.get("title"),

        "promotion_status": chain.get("promotion_status"),
        "confidence": chain.get("confidence"),
        "score": chain.get("score"),

        "stages_total": chain.get("stages_total", len(steps)),
        "runtime_chain_steps": steps,
        "runtime_chain_text": " -> ".join(str(step) for step in steps),

        "registry_artifact": normalize_path(registry_path),
        "decision_artifact": normalize_path(chain.get("decision_artifact")),
        "candidate_artifact": normalize_path(chain.get("candidate_artifact")),
        "promotion_validation_artifact": normalize_path(
            chain.get("promotion_validation_artifact")
        ),
        "promoted_artifact": normalize_path(chain.get("promoted_artifact")),

        "metadata": {
            k: v
            for k, v in chain.items()
            if k not in KNOWN_FIELDS
        },

        "content": build_content(chain),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build runtime chain retrieval corpus from promoted runtime chain registry."
    )

    parser.add_argument(
        "--workspace",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--registry",
        type=Path,
        default=None,
        help="Default: <workspace>/manifests/runtime/promoted_runtime_chains.json",
    )

    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Default: <workspace>/manifests/semantic/runtime_chain_corpus.jsonl",
    )

    args = parser.parse_args()

    workspace = args.workspace.resolve()

    registry_path = (
        args.registry
        or workspace / "manifests" / "runtime" / "promoted_runtime_chains.json"
    )

    out_path = (
        args.out
        or workspace / "manifests" / "semantic" / "runtime_chain_corpus.jsonl"
    )

    registry = read_json(registry_path)

    if registry.get("schema") != "promoted_runtime_chain_registry.v1":
        raise ValueError(
            f"Expected promoted_runtime_chain_registry.v1, got {registry.get('schema')!r}"
        )

    rows: list[dict[str, Any]] = []

    for chain in registry.get("chains", []):
        if not isinstance(chain, dict):
            continue

        ALLOWED_PROMOTION_STATUSES = {
            "promoted_confirmed_chain",
            "promoted_topology_supported_chain",
            "promoted_source_validated_chain",
        }

        if chain.get("promotion_status") not in ALLOWED_PROMOTION_STATUSES:
            continue

        rows.append(
            build_doc(
                chain=chain,
                registry_path=registry_path,
                registry=registry,
            )
        )

    rows.sort(key=lambda row: str(row.get("chain_id", "")))

    write_jsonl(out_path, rows)

    print(f"Runtime chain corpus docs: {len(rows)}")
    print(f"Wrote JSONL: {out_path}")


if __name__ == "__main__":
    main()