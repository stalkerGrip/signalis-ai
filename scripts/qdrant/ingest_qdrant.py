import argparse
import json
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


DEFAULT_COLLECTION = "signalis_semantic"


def load_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc


def stable_point_id(item: Dict[str, Any]) -> str:
    """
    Qdrant point IDs support UUIDs. Use UUIDv5 so re-ingesting the same document
    updates the same point instead of creating duplicates.
    """
    raw = "|".join(
        [
            str(item.get("id", "")),
            str(item.get("content_hash", "")),
            str(item.get("doc_type", "")),
        ]
    )
    return str(uuid.uuid5(uuid.NAMESPACE_URL, raw))


def normalize_payload(item: Dict[str, Any]) -> Dict[str, Any]:
    metadata = item.get("metadata") or {}

    payload = {
        "source_id": item.get("id"),
        "doc_type": item.get("doc_type"),
        "content_hash": item.get("content_hash"),
        "embedding_dim": item.get("embedding_dim"),
        "text": item.get("text", ""),
    }

    # Flatten selected metadata for easy Qdrant filtering.
    if isinstance(metadata, dict):
        payload["metadata"] = metadata

        for key in [
            "node_type",
            "edge_type",
            "plugin",
            "subsystem",
            "realm",
            "file",
            "event",
            "message",
            "timer",
            "degree",
            "risk_flags",
            "source_artifact",
        ]:
            if key in metadata:
                payload[key] = metadata[key]
    else:
        payload["metadata"] = {}

    return payload


def batched(items: List[Dict[str, Any]], batch_size: int) -> Iterable[List[Dict[str, Any]]]:
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]


def infer_vector_size(items: List[Dict[str, Any]]) -> int:
    for item in items:
        vector = item.get("embedding")
        if isinstance(vector, list) and vector:
            return len(vector)

    raise ValueError("Could not infer vector size: no valid embedding vectors found.")


def create_or_recreate_collection(
    client: QdrantClient,
    collection_name: str,
    vector_size: int,
    recreate: bool,
) -> str:
    existing = [c.name for c in client.get_collections().collections]

    if collection_name in existing:
        if recreate:
            client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            )
            return "recreated"

        info = client.get_collection(collection_name)
        current_size = info.config.params.vectors.size

        if current_size != vector_size:
            raise ValueError(
                f"Collection {collection_name!r} already exists with vector size "
                f"{current_size}, but embeddings have size {vector_size}. "
                f"Use --recreate to replace it."
            )

        return "reused"

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )
    return "created"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest SIGNALIS semantic embeddings into Qdrant."
    )
    parser.add_argument("--workspace", required=True, help="Workspace root, e.g. E:/signalis_ai")
    parser.add_argument("--host", default="localhost", help="Qdrant host")
    parser.add_argument("--port", type=int, default=6333, help="Qdrant HTTP port")
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--recreate", action="store_true", help="Drop/recreate collection")
    parser.add_argument("--dry-run", action="store_true", help="Validate only; do not ingest")
    parser.add_argument("--write", action="store_true", help="Write summary markdown")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    input_path = workspace / "manifests" / "semantic" / "qdrant_embeddings.jsonl"
    summary_path = workspace / "manifests" / "semantic" / "qdrant_ingest_summary.md"

    if not input_path.exists():
        raise FileNotFoundError(f"Missing embeddings file: {input_path}")

    items = list(load_jsonl(input_path))
    if not items:
        raise ValueError(f"No embeddings found in: {input_path}")

    vector_size = infer_vector_size(items)

    invalid = []
    for item in items:
        vector = item.get("embedding")
        if not isinstance(vector, list) or len(vector) != vector_size:
            invalid.append(item.get("id"))

    if invalid:
        raise ValueError(
            f"Found {len(invalid)} invalid embeddings. First invalid IDs: {invalid[:10]}"
        )

    client = QdrantClient(host=args.host, port=args.port)

    collection_action = "dry_run_not_created"
    upserted = 0

    if not args.dry_run:
        collection_action = create_or_recreate_collection(
            client=client,
            collection_name=args.collection,
            vector_size=vector_size,
            recreate=args.recreate,
        )

        for batch in batched(items, args.batch_size):
            points = [
                PointStruct(
                    id=stable_point_id(item),
                    vector=item["embedding"],
                    payload=normalize_payload(item),
                )
                for item in batch
            ]

            client.upsert(collection_name=args.collection, points=points)
            upserted += len(points)

    doc_types = {}
    for item in items:
        doc_type = item.get("doc_type") or "unknown"
        doc_types[doc_type] = doc_types.get(doc_type, 0) + 1

    lines = [
        "# Qdrant Ingest Summary",
        "",
        f"Collection: `{args.collection}`",
        f"Host: `{args.host}:{args.port}`",
        f"Input: `{input_path}`",
        "",
        "## Results",
        "",
        f"- Input embeddings: **{len(items)}**",
        f"- Vector size: **{vector_size}**",
        f"- Collection action: **{collection_action}**",
        f"- Upserted points: **{upserted}**",
        f"- Dry run: **{args.dry_run}**",
        "",
        "## Document types",
        "",
    ]

    for doc_type, count in sorted(doc_types.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- `{doc_type}`: **{count}**")

    lines.extend(
        [
            "",
            "## Next",
            "",
            "Use `query_qdrant.py` to test semantic retrieval quality.",
            "",
        ]
    )

    summary = "\n".join(lines)

    if args.write:
        summary_path.write_text(summary, encoding="utf-8")

    print(summary)


if __name__ == "__main__":
    main()
