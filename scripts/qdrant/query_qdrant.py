#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue

try:
    from scripts.qdrant.retrieval_intent import classify_retrieval_intent, build_expanded_query
except Exception:
    classify_retrieval_intent = None
    build_expanded_query = None

try:
    from scripts.qdrant.rerank_results import rerank_results
except Exception:
    rerank_results = None

DEFAULT_COLLECTION = "signalis_semantic"
DEFAULT_MODEL = "nomic-ai/nomic-embed-text-v1.5"
HASH_MODEL_NAME = "signalis-hash-embedding-v1"


def tokenize(text: str) -> list[str]:
    chars = []
    for ch in text.lower():
        if ch.isalnum() or ch in "_:/.-":
            chars.append(ch)
        else:
            chars.append(" ")
    return [tok for tok in "".join(chars).split() if tok]


def hash_embedding(text: str, dim: int = 384) -> list[float]:
    vec = [0.0] * dim
    tokens = tokenize(text)
    features = tokens[:]
    features.extend(f"{a} {b}" for a, b in zip(tokens, tokens[1:]))

    for feature in features:
        digest = hashlib.blake2b(feature.encode("utf-8", errors="ignore"), digest_size=8).digest()
        raw = int.from_bytes(digest, "little", signed=False)
        idx = raw % dim
        sign = 1.0 if ((raw >> 63) & 1) == 0 else -1.0
        vec[idx] += sign

    norm = math.sqrt(sum(x * x for x in vec))
    if norm <= 0:
        vec[0] = 1.0
        return vec

    return [x / norm for x in vec]


def detect_embedding_dim(workspace: Path) -> int:
    path = workspace / "manifests" / "semantic" / "qdrant_embeddings.jsonl"
    if not path.exists():
        return 384

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            dim = row.get("embedding_dim")
            if isinstance(dim, int) and dim > 0:
                return dim
            emb = row.get("embedding")
            if isinstance(emb, list) and emb:
                return len(emb)

    return 384


def build_filter(args: argparse.Namespace) -> Optional[Filter]:
    conditions = []
    for field in ["doc_type", "node_type", "plugin", "subsystem", "realm", "file"]:
        value = getattr(args, field, None)
        if value:
            conditions.append(FieldCondition(key=field, match=MatchValue(value=value)))

    if not conditions:
        return None
    return Filter(must=conditions)


def encode_query(query: str, args: argparse.Namespace, workspace: Path) -> list[float]:
    if args.hash:
        return hash_embedding(query, dim=detect_embedding_dim(workspace))

    try:
        from sentence_transformers import SentenceTransformer

        kwargs: dict[str, Any] = {"device": args.device}
        if args.trust_remote_code or "nomic" in args.model.lower():
            kwargs["trust_remote_code"] = True

        model = SentenceTransformer(args.model, **kwargs)
        query_text = query
        if "nomic" in args.model.lower() and not query_text.startswith("search_query:"):
            query_text = "search_query: " + query_text
        return model.encode(query_text, normalize_embeddings=True).tolist()
    except Exception as exc:
        print(f"[WARN] Query model failed: {exc!r}")
        print("[INFO] Falling back to deterministic hash query vector.")
        return hash_embedding(query, dim=detect_embedding_dim(workspace))


def run_search(client: QdrantClient, collection: str, vector: list[float], query_filter: Optional[Filter], limit: int):
    if hasattr(client, "search"):
        return client.search(
            collection_name=collection,
            query_vector=vector,
            query_filter=query_filter,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

    response = client.query_points(
        collection_name=collection,
        query=vector,
        query_filter=query_filter,
        limit=limit,
        with_payload=True,
        with_vectors=False,
    )
    return getattr(response, "points", response)


def result_to_dict(result: Any) -> dict[str, Any]:
    payload = result.payload or {}
    return {
        "score": float(result.score),
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
    if isinstance(result, dict):
        score = result.get("score", 0.0)
        payload = result.get("payload", {})
        rerank_score = result.get("rerank_score")
        rerank_reasons = result.get("rerank_reasons", [])
    else:
        score = result.score
        payload = result.payload or {}
        rerank_score = None
        rerank_reasons = []

    text = payload.get("text", "")
    if len(text) > text_chars:
        text = text[:text_chars].rstrip() + "..."

    return "\n".join([
        f"## Result {index}",
        "",
        f"- Score: **{score:.4f}**",
        f"- Rerank score: `{rerank_score}`",
        f"- Rerank reasons: `{rerank_reasons}`",
        f"- Source ID: `{payload.get('source_id')}`",
        f"- Doc type: `{payload.get('doc_type')}`",
        f"- Subsystem: `{payload.get('subsystem')}`",
        f"- File: `{payload.get('file')}`",
        "",
        "### Metadata",
        "",
        "```json",
        json.dumps(payload, indent=2, ensure_ascii=False),
        "```",
        "",
        "### Text",
        "",
        "```text",
        text,
        "```",
        "",
    ])


def main() -> None:
    parser = argparse.ArgumentParser(description="Query SIGNALIS semantic Qdrant collection.")
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--hash", action="store_true", help="Force deterministic hash query vector.")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=6333)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--retrieve-k", type=int, default=None)
    parser.add_argument("--text-chars", type=int, default=1800)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--rerank", action="store_true")
    parser.add_argument("--expanded-query", action="store_true")
    parser.add_argument("--doc-type")
    parser.add_argument("--node-type")
    parser.add_argument("--plugin")
    parser.add_argument("--subsystem")
    parser.add_argument("--realm")
    parser.add_argument("--file")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    report_path = workspace / "manifests" / "semantic" / "qdrant_query_results.md"

    query_text = args.query
    if (args.expanded_query or args.rerank) and classify_retrieval_intent and build_expanded_query:
        intent = classify_retrieval_intent(args.query)
        query_text = build_expanded_query(intent)
    else:
        intent = None

    vector = encode_query(query_text, args, workspace)
    client = QdrantClient(host=args.host, port=args.port)

    retrieve_k = args.retrieve_k or args.top_k
    if args.rerank:
        retrieve_k = max(retrieve_k, args.top_k)

    raw_results = list(run_search(client, args.collection, vector, build_filter(args), retrieve_k))
    results: list[Any] = raw_results

    if args.rerank and rerank_results and intent is not None:
        results = rerank_results(
            [result_to_dict(result) for result in raw_results],
            intent,
            query=args.query,
            use_bge=False,
        )

    results = results[:args.top_k]

    lines = [
        "# Qdrant Query Results",
        "",
        f"Collection: `{args.collection}`",
        f"Query: `{args.query}`",
        f"Expanded query used: `{query_text}`",
        f"Top K: **{args.top_k}**",
        f"Retrieve K: **{retrieve_k}**",
        f"Model: `{args.model}`",
        f"Hash query: `{args.hash}`",
        "",
        f"## Returned results: {len(results)}",
        "",
    ]

    for index, result in enumerate(results, 1):
        lines.append(format_result(index, result, args.text_chars))

    report = "\n".join(lines)

    if args.write:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
        print(f"Wrote report to: {report_path}")

    print(report)


if __name__ == "__main__":
    main()
