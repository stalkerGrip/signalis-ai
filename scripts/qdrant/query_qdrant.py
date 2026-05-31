import argparse
import json
from pathlib import Path
from typing import Any, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue
from sentence_transformers import SentenceTransformer

from scripts.qdrant.retrieval_intent import classify_retrieval_intent, build_expanded_query
from scripts.qdrant.rerank_results import rerank_results
from scripts.qdrant.context_pack import build_context_pack

DEFAULT_COLLECTION = "signalis_semantic"


def build_filter(args: argparse.Namespace) -> Optional[Filter]:
    conditions = []

    for field in ["doc_type", "node_type", "plugin", "subsystem", "realm", "file"]:
        value = getattr(args, field, None)
        if value:
            conditions.append(
                FieldCondition(
                    key=field,
                    match=MatchValue(value=value),
                )
            )

    if not conditions:
        return None

    return Filter(must=conditions)


def run_search(
    client: QdrantClient,
    collection_name: str,
    query_vector: list[float],
    query_filter: Optional[Filter],
    limit: int,
):
    if hasattr(client, "search"):
        return client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

    response = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        query_filter=query_filter,
        limit=limit,
        with_payload=True,
        with_vectors=False,
    )

    return getattr(response, "points", response)


def result_to_dict(result: Any) -> dict[str, Any]:
    payload = result.payload or {}
    return {
        "score": result.score,
        "payload": payload,
        "text": payload.get("text", ""),
        "doc_type": payload.get("doc_type"),
        "node_type": payload.get("node_type"),
        "plugin": payload.get("plugin"),
        "subsystem": payload.get("subsystem"),
        "realm": payload.get("realm"),
        "file": payload.get("file"),
        "_raw": result,
    }


def format_result(index: int, result: Any, text_chars: int) -> str:
    rerank_score = None
    rerank_bonus = None
    rerank_reasons = []
    rerank_components = {}
    bge_score = None
    bge_error = None

    if isinstance(result, dict):
        rerank_score = result.get("rerank_score")
        rerank_bonus = result.get("rerank_bonus")
        rerank_reasons = result.get("rerank_reasons", [])
        rerank_components = result.get("rerank_components", {})
        bge_score = result.get("bge_score")
        bge_error = result.get("bge_error")
        payload = result.get("payload", {})
        score = result.get("score", 0.0)
    else:
        payload = result.payload or {}
        score = result.score

    text = payload.get("text", "")
    metadata = payload

    if len(text) > text_chars:
        text = text[:text_chars].rstrip() + "..."

    lines = [
        f"## Result {index}",
        "",
        f"- Score: **{score:.4f}**",
        f"- BGE score: `{bge_score}`",
        f"- BGE error: `{bge_error}`",
        f"- Rerank score: `{rerank_score}`",
        f"- Rerank bonus: `{rerank_bonus}`",
        f"- Rerank components: `{rerank_components}`",
        f"- Rerank reasons: `{rerank_reasons}`",
        f"- Source ID: `{payload.get('source_id')}`",
        f"- Doc type: `{payload.get('doc_type')}`",
        f"- Node type: `{payload.get('node_type')}`",
        f"- Plugin: `{payload.get('plugin')}`",
        f"- Subsystem: `{payload.get('subsystem')}`",
        f"- Realm: `{payload.get('realm')}`",
        f"- File: `{payload.get('file')}`",
        "",
        "### Metadata",
        "",
        "```json",
        json.dumps(metadata, indent=2, ensure_ascii=False),
        "```",
        "",
        "### Text",
        "",
        "```text",
        text,
        "```",
        "",
    ]

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Query SIGNALIS semantic Qdrant collection.")
    parser.add_argument("--context-pack", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--model", default="nomic-ai/nomic-embed-text-v1.5")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=6333)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--retrieve-k", type=int, default=None)
    parser.add_argument("--text-chars", type=int, default=1800)
    parser.add_argument("--write", action="store_true")

    parser.add_argument("--rerank", action="store_true")
    parser.add_argument("--expanded-query", action="store_true")

    parser.add_argument("--bge-rerank", action="store_true")
    parser.add_argument("--bge-model", default="BAAI/bge-reranker-v2-m3")
    parser.add_argument("--bge-fp16", action="store_true")
    parser.add_argument("--bge-batch-size", type=int, default=4)

    parser.add_argument("--dense-weight", type=float, default=0.35)
    parser.add_argument("--bge-weight", type=float, default=0.25)
    parser.add_argument("--structural-weight", type=float, default=0.25)
    parser.add_argument("--causal-weight", type=float, default=0.15)

    parser.add_argument("--doc-type")
    parser.add_argument("--node-type")
    parser.add_argument("--plugin")
    parser.add_argument("--subsystem")
    parser.add_argument("--realm")
    parser.add_argument("--file")

    args = parser.parse_args()

    workspace = Path(args.workspace)
    report_path = workspace / "manifests" / "semantic" / "qdrant_query_results.md"

    intent = classify_retrieval_intent(args.query)

    query_text = args.query
    if args.expanded_query or args.rerank or args.bge_rerank:
        query_text = build_expanded_query(intent)

    model = SentenceTransformer(args.model, device=args.device)
    query_vector = model.encode(query_text, normalize_embeddings=True).tolist()

    client = QdrantClient(host=args.host, port=args.port)
    query_filter = build_filter(args)

    retrieve_k = args.retrieve_k or args.top_k
    if args.rerank or args.bge_rerank:
        retrieve_k = max(retrieve_k, args.top_k)

    raw_results = run_search(
        client=client,
        collection_name=args.collection,
        query_vector=query_vector,
        query_filter=query_filter,
        limit=retrieve_k,
    )

    results: list[Any] = list(raw_results)

    if args.rerank or args.bge_rerank:
        result_dicts = [result_to_dict(result) for result in results]

        results = rerank_results(
            result_dicts,
            intent,
            query=args.query,
            use_bge=args.bge_rerank,
            bge_model=args.bge_model,
            bge_fp16=args.bge_fp16,
            bge_batch_size=args.bge_batch_size,
            dense_weight=args.dense_weight,
            bge_weight=args.bge_weight,
            structural_weight=args.structural_weight,
            causal_weight=args.causal_weight,
        )

        results = results[:args.top_k]

    filter_summary = {
        "doc_type": args.doc_type,
        "node_type": args.node_type,
        "plugin": args.plugin,
        "subsystem": args.subsystem,
        "realm": args.realm,
        "file": args.file,
    }
    filter_summary = {k: v for k, v in filter_summary.items() if v}

    lines = [
        "# Qdrant Query Results",
        "",
        f"Collection: `{args.collection}`",
        f"Query: `{args.query}`",
        f"Expanded query used: `{query_text}`",
        f"Top K: **{args.top_k}**",
        f"Retrieve K: **{retrieve_k}**",
        f"Model: `{args.model}`",
        f"Device: `{args.device}`",
        f"Deterministic rerank: `{args.rerank}`",
        f"BGE rerank: `{args.bge_rerank}`",
        f"BGE model: `{args.bge_model}`",
        f"BGE fp16: `{args.bge_fp16}`",
        "",
        "## Filters",
        "",
        "```json",
        json.dumps(filter_summary, indent=2, ensure_ascii=False),
        "```",
        "",
        f"## Returned results: {len(results)}",
        "",
    ]

    for idx, result in enumerate(results, start=1):
        lines.append(format_result(idx, result, args.text_chars))

    report = "\n".join(lines)

    if args.context_pack:
        report += "\n\n"
        report += build_context_pack(results, args.query)

    output_path = None

    if args.output:
        output_path = args.output
        if not output_path.is_absolute():
            output_path = workspace / output_path
    elif args.write:
        output_path = report_path

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(f"\nWrote report to: {output_path}")

    print(report)


if __name__ == "__main__":
    main()