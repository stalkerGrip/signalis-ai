from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


PIPELINE_CONTRACT = {
    "script_id": "scripts.investigation.retrieve_promoted_runtime_chains",
    "purpose": "Retrieve promoted runtime chains from Qdrant and build a ranked architecture context pack for investigation consumption.",
    "pipeline_stage": "retrieval",
    "input_schemas": [
        "qdrant_collection.v1",
        "runtime_chain_corpus.v1",
        "pipeline_artifact_contract.v1",
    ],
    "output_schemas": [
        "runtime_chain_context_pack.v1",
    ],
    "artifact_patterns": [
        "investigations/retrieval/runtime_chain_context_pack*.json",
        "investigations/retrieval/runtime_chain_context_pack*.md",
    ],
    "promotion_role": "promotion_support",
    "canonical_status": "active",
}


DEFAULT_COLLECTION = "signalis_semantic"
DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
DEFAULT_REQUIRED_DOC_TYPE = "promoted_runtime_chain"
DEFAULT_REQUIRED_SCHEMA = "runtime_chain_corpus.v1"
DEFAULT_ALLOWED_PROMOTION_STATUSES = {
    "promoted_confirmed_chain",
    "promoted_topology_supported_chain",
    "promoted_source_validated_chain",
}


def load_workspace(workspace: Path) -> dict[str, Any]:
    path = workspace / "config" / "workspace.yaml"

    if not path.exists():
        raise FileNotFoundError(f"Missing workspace config: {path}")

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def read_contract(workspace: Path) -> dict[str, Any]:
    path = workspace / "docs" / "runtime" / "pipeline_artifact_contract.json"

    if not path.exists():
        raise FileNotFoundError(f"Missing pipeline artifact contract: {path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def payload_get(payload: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        value = payload.get(key)
        if value is not None:
            return value
    return default


def as_string_list(value: Any) -> list[str]:
    if value is None:
        return []

    if isinstance(value, str):
        if "→" in value:
            return [part.strip() for part in value.split("→") if part.strip()]
        return [value]

    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            if isinstance(item, str):
                result.append(item)
            elif isinstance(item, dict):
                label = payload_get(
                    item,
                    "stage",
                    "step",
                    "name",
                    "id",
                    "title",
                    "label",
                    default=None,
                )
                if label:
                    result.append(str(label))
        return result

    return [str(value)]


def normalize_result(point: Any, rank: int, include_raw_payload: bool) -> dict[str, Any]:
    payload = point.payload or {}

    normalized = {
        "rank": rank,
        "qdrant_id": str(point.id),
        "score": getattr(point, "score", None),
        "schema": payload_get(payload, "schema", default=""),
        "source_id": payload_get(payload, "source_id", "id", default=""),
        "doc_type": payload_get(payload, "doc_type", "type", default=""),
        "title": payload_get(payload, "title", "name", default=""),
        "chain_id": payload_get(payload, "chain_id", "runtime_chain_id", default=""),
        "confidence": payload_get(payload, "confidence", default=""),
        "promotion_status": payload_get(payload, "promotion_status", "status", default=""),
        "source_path": payload_get(
            payload,
            "promoted_artifact",
            "source_path",
            "path",
            default="",
        ),
        "candidate_artifact": payload_get(payload, "candidate_artifact", default=""),
        "decision_artifact": payload_get(payload, "decision_artifact", default=""),
        "promotion_validation_artifact": payload_get(payload, "promotion_validation_artifact", default=""),
        "text": payload_get(payload, "content", "text", "body", default=""),
        "stages": as_string_list(
            payload_get(
                payload,
                "runtime_chain_steps",
                "stages",
                "chain_stages",
                "runtime_chain_text",
                default=[],
            )
        ),
        "rerank_reasons": payload_get(payload, "rerank_reasons", default=[]),
    }

    if include_raw_payload:
        normalized["raw_payload"] = payload

    return normalized


def parse_csv_set(value: str | None) -> set[str]:
    if value is None:
        return set()

    return {part.strip() for part in value.split(",") if part.strip()}


def matches_context_filter(
    result: dict[str, Any],
    *,
    required_schema: str | None,
    required_doc_type: str | None,
    allowed_promotion_statuses: set[str],
) -> bool:
    if required_schema and result.get("schema") != required_schema:
        return False

    if required_doc_type and result.get("doc_type") != required_doc_type:
        return False

    if allowed_promotion_statuses:
        status = str(result.get("promotion_status", ""))
        if status not in allowed_promotion_statuses:
            return False

    return True


def architecture_relevance(result: dict[str, Any], query_terms: set[str]) -> list[str]:
    reasons: list[str] = []

    text = " ".join(
        [
            str(result.get("source_id", "")),
            str(result.get("title", "")),
            str(result.get("text", "")),
            " ".join(map(str, result.get("stages", []))),
        ]
    ).lower()

    hits = sorted(term for term in query_terms if term and term in text)

    if hits:
        reasons.append("query_term_match:" + ",".join(hits[:10]))

    if result.get("confidence"):
        reasons.append(f"confidence:{result['confidence']}")

    if result.get("promotion_status"):
        reasons.append(f"promotion_status:{result['promotion_status']}")

    if result.get("stages"):
        reasons.append(f"stage_count:{len(result['stages'])}")

    return reasons


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def write_md(path: Path, pack: dict[str, Any]) -> None:
    lines: list[str] = []

    lines.append("# Runtime Chain Context Pack")
    lines.append("")
    lines.append(f"- Schema: `{pack['schema']}`")
    lines.append(f"- Producer: `{pack['producer_script']}`")
    lines.append(f"- Query: `{pack['query']}`")
    lines.append(f"- Collection: `{pack['collection']}`")
    lines.append(f"- Accepted chains: `{len(pack['ranked_chains'])}`")
    lines.append(f"- Rejected results: `{len(pack['rejected_results'])}`")
    lines.append("")

    lines.append("## Ranked Runtime Chains")
    lines.append("")

    if not pack["ranked_chains"]:
        lines.append("No runtime chains matched the context filter.")
        lines.append("")
    else:
        for item in pack["ranked_chains"]:
            lines.append(f"### {item['rank']}. {item.get('title') or item.get('source_id')}")
            lines.append("")
            lines.append(f"- Source ID: `{item.get('source_id', '')}`")
            lines.append(f"- Schema: `{item.get('schema', '')}`")
            lines.append(f"- Doc type: `{item.get('doc_type', '')}`")
            lines.append(f"- Chain ID: `{item.get('chain_id', '')}`")
            lines.append(f"- Confidence: `{item.get('confidence', '')}`")
            lines.append(f"- Promotion status: `{item.get('promotion_status', '')}`")
            lines.append(f"- Score: `{item.get('score', '')}`")
            lines.append(f"- Source path: `{item.get('source_path', '')}`")
            lines.append("")

            relevance = item.get("architecture_relevance", [])
            if relevance:
                lines.append("Architecture relevance:")
                lines.append("")
                for reason in relevance:
                    lines.append(f"- `{reason}`")
                lines.append("")

            stages = item.get("stages", [])
            if stages:
                lines.append("Stages:")
                lines.append("")
                for stage in stages:
                    lines.append(f"- `{stage}`")
                lines.append("")

            text = str(item.get("text", "")).strip()
            if text:
                preview = text[:2000]
                lines.append("Context preview:")
                lines.append("")
                lines.append(preview)
                lines.append("")

    lines.append("## Rejected Results")
    lines.append("")

    if not pack["rejected_results"]:
        lines.append("None.")
        lines.append("")
    else:
        for item in pack["rejected_results"]:
            reason = item.get("reject_reason", "filter_mismatch")
            lines.append(
                f"- `{item.get('source_id', '')}` | schema=`{item.get('schema', '')}` | "
                f"doc_type=`{item.get('doc_type', '')}` | status=`{item.get('promotion_status', '')}` | "
                f"score=`{item.get('score', '')}` | reason=`{reason}`"
            )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retrieve runtime chain context from Qdrant and build an architecture context pack."
    )

    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--query", required=True)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--qdrant-url", default="http://localhost:6333")
    parser.add_argument("--retrieve-k", type=int, default=50)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument(
        "--required-doc-type",
        default=DEFAULT_REQUIRED_DOC_TYPE,
        help="Accepted doc_type. Use an empty string to disable doc_type filtering.",
    )
    parser.add_argument(
        "--required-schema",
        default=DEFAULT_REQUIRED_SCHEMA,
        help="Accepted payload schema. Use an empty string to disable schema filtering.",
    )
    parser.add_argument(
        "--allowed-promotion-statuses",
        default=",".join(sorted(DEFAULT_ALLOWED_PROMOTION_STATUSES)),
        help="Comma-separated accepted promotion statuses. Use an empty string to disable status filtering.",
    )
    parser.add_argument(
        "--include-raw-payload",
        action="store_true",
        help="Include raw Qdrant payloads in the JSON context pack.",
    )
    parser.add_argument(
        "--debug-first-payload",
        action="store_true",
        help="Print the first accepted raw payload for diagnostics.",
    )
    parser.add_argument(
        "--out-json",
        type=Path,
        default=Path("investigations/retrieval/runtime_chain_context_pack.json"),
    )
    parser.add_argument(
        "--out-md",
        type=Path,
        default=Path("investigations/retrieval/runtime_chain_context_pack.md"),
    )

    return parser.parse_args()


def reject_reason(
    result: dict[str, Any],
    *,
    required_schema: str | None,
    required_doc_type: str | None,
    allowed_promotion_statuses: set[str],
) -> str:
    if required_schema and result.get("schema") != required_schema:
        return "schema_mismatch"

    if required_doc_type and result.get("doc_type") != required_doc_type:
        return "doc_type_mismatch"

    if allowed_promotion_statuses and result.get("promotion_status") not in allowed_promotion_statuses:
        return "promotion_status_mismatch"

    return "filter_mismatch"


def main() -> None:
    args = parse_args()

    workspace = args.workspace.resolve()
    load_workspace(workspace)
    contract = read_contract(workspace)

    required_doc_type = args.required_doc_type or None
    required_schema = args.required_schema or None
    allowed_promotion_statuses = parse_csv_set(args.allowed_promotion_statuses)

    model = SentenceTransformer(args.model, device="cpu")
    vector = model.encode([args.query], normalize_embeddings=True)[0].tolist()

    client = QdrantClient(url=args.qdrant_url)

    query_response = client.query_points(
        collection_name=args.collection,
        query=vector,
        limit=args.retrieve_k,
        with_payload=True,
    )

    search_results = query_response.points
    query_terms = {part.lower() for part in args.query.replace("_", " ").split()}

    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []

    for index, point in enumerate(search_results, start=1):
        normalized = normalize_result(
            point,
            index,
            include_raw_payload=args.include_raw_payload,
        )

        if matches_context_filter(
            normalized,
            required_schema=required_schema,
            required_doc_type=required_doc_type,
            allowed_promotion_statuses=allowed_promotion_statuses,
        ):
            if args.debug_first_payload and not accepted:
                print("==== FIRST ACCEPTED PAYLOAD ====")
                print(json.dumps(point.payload or {}, indent=2, ensure_ascii=False))

            normalized["architecture_relevance"] = architecture_relevance(normalized, query_terms)
            accepted.append(normalized)
        else:
            rejected.append(
                {
                    "rank": normalized["rank"],
                    "qdrant_id": normalized["qdrant_id"],
                    "score": normalized["score"],
                    "schema": normalized["schema"],
                    "source_id": normalized["source_id"],
                    "doc_type": normalized["doc_type"],
                    "promotion_status": normalized["promotion_status"],
                    "title": normalized["title"],
                    "reject_reason": reject_reason(
                        normalized,
                        required_schema=required_schema,
                        required_doc_type=required_doc_type,
                        allowed_promotion_statuses=allowed_promotion_statuses,
                    ),
                }
            )

    accepted = accepted[: args.top_k]

    for index, item in enumerate(accepted, start=1):
        item["rank"] = index

    pack = {
        "schema": "runtime_chain_context_pack.v1",
        "producer_script": PIPELINE_CONTRACT["script_id"],
        "pipeline_stage": "retrieval",
        "query": args.query,
        "collection": args.collection,
        "model": args.model,
        "filters": {
            "required_schema": required_schema,
            "required_doc_type": required_doc_type,
            "allowed_promotion_statuses": sorted(allowed_promotion_statuses),
            "retrieve_k": args.retrieve_k,
            "top_k": args.top_k,
        },
        "inputs": [
            "qdrant_collection.v1",
            "runtime_chain_corpus.v1",
            str(workspace / "docs" / "runtime" / "pipeline_artifact_contract.json"),
        ],
        "contract_generated_at": contract.get("generated_at"),
        "ranked_chains": accepted,
        "rejected_results": rejected,
    }

    out_json = args.out_json
    out_md = args.out_md

    if not out_json.is_absolute():
        out_json = workspace / out_json

    if not out_md.is_absolute():
        out_md = workspace / out_md

    write_json(out_json, pack)
    write_md(out_md, pack)

    print(f"Wrote JSON: {out_json}")
    print(f"Wrote MD:   {out_md}")
    print(f"Accepted chains: {len(accepted)}")
    print(f"Rejected results: {len(rejected)}")


if __name__ == "__main__":
    main()
