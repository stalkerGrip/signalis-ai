from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue


DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
DEFAULT_COLLECTION = "signalis_semantic"
DEFAULT_DIM = 384


def stable_hash_vector(text: str, dim: int = DEFAULT_DIM) -> list[float]:
    vector = [0.0] * dim
    tokens = re.findall(r"[a-zA-Z0-9_:/\\.]+", text.lower())

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:4], "little") % dim
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[idx] += sign

    norm = math.sqrt(sum(v * v for v in vector))
    if norm > 0:
        vector = [v / norm for v in vector]

    return vector


def encode_query(query: str, model_name: str, hash_only: bool, dim: int) -> list[float]:
    if hash_only:
        return stable_hash_vector(query, dim=dim)

    try:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(model_name, device="cpu")
        vector = model.encode([query], normalize_embeddings=True)[0]
        return [float(v) for v in vector]
    except Exception as exc:
        print(f"[WARN] Query model failed: {exc!r}")
        print("[INFO] Falling back to deterministic hash query vector.")
        return stable_hash_vector(query, dim=dim)


def load_expansion_terms(workspace: Path) -> list[str]:
    terms = [
        "hook_event",
        "hook_listener",
        "hook_emitter",
        "network_message",
        "network_operation",
        "network_context",
        "network_payload_operation",
        "plugin",
        "plugin_summary",
        "file",
        "file_summary",
    ]

    extra = workspace / "manifests" / "semantic" / "query_expansion_terms.json"
    if extra.exists():
        try:
            data = json.loads(extra.read_text(encoding="utf-8"))
            if isinstance(data, list):
                terms.extend(str(x) for x in data)
        except Exception:
            pass

    return sorted(set(terms))


def expand_query(query: str, workspace: Path, enabled: bool) -> str:
    if not enabled:
        return query

    q = query.lower()
    terms = load_expansion_terms(workspace)

    boosts: list[str] = []

    if "inventory" in q or "item" in q:
        boosts.extend(
            [
                "inventory",
                "invData",
                "ItemDataChanged",
                "InventoryDataChanged",
                "nutInventoryAdd",
                "nutInventoryRemove",
                "inventoryOpen",
                "inventorySetPanelStatus",
                "sync",
                "setData",
            ]
        )

    if "vendor" in q or "price" in q:
        boosts.extend(
            [
                "vendor",
                "vendorSPrice",
                "vendorBPrice",
                "vendorSellItem",
                "vendor purchase",
                "price label",
                "stale metadata",
            ]
        )

    if "character" in q or "load" in q or "desync" in q:
        boosts.extend(
            [
                "CharacterLoaded",
                "PlayerLoadedChar",
                "PlayerLoadout",
                "PostPlayerLoadout",
                "CharacterPreSave",
                "client UI",
                "server authoritative",
                "realm crossing",
            ]
        )

    if "storage" in q:
        boosts.extend(
            [
                "storage",
                "StorageOpen",
                "storageInventory",
                "nutStorageOpen",
                "StorageItemRemoved",
            ]
        )

    expanded = query + " " + " ".join(sorted(set(boosts + terms)))
    return expanded.strip()


def build_filter(args: argparse.Namespace) -> Filter | None:
    conditions: list[FieldCondition] = []

    if args.doc_type:
        conditions.append(FieldCondition(key="doc_type", match=MatchValue(value=args.doc_type)))

    if args.file:
        conditions.append(FieldCondition(key="file", match=MatchValue(value=args.file)))

    if not conditions:
        return None

    return Filter(must=conditions)


def validate_vector_dimension(client: QdrantClient, collection: str, vector: list[float]) -> None:
    try:
        info = client.get_collection(collection)
        vectors = info.config.params.vectors

        expected_dim: int | None = None

        if hasattr(vectors, "size"):
            expected_dim = vectors.size
        elif isinstance(vectors, dict):
            first = next(iter(vectors.values()))
            expected_dim = getattr(first, "size", None)

        if expected_dim is not None and expected_dim != len(vector):
            raise RuntimeError(
                f"Vector dimension mismatch before Qdrant query: "
                f"collection expects {expected_dim}, query produced {len(vector)}. "
                f"Collection/model mismatch. Current canonical model is {DEFAULT_MODEL} ({DEFAULT_DIM} dim)."
            )
    except RuntimeError:
        raise
    except Exception as exc:
        print(f"[WARN] Could not validate collection vector dimension: {exc!r}")


def run_search(
    client: QdrantClient,
    collection: str,
    vector: list[float],
    qdrant_filter: Filter | None,
    limit: int,
):
    response = client.query_points(
        collection_name=collection,
        query=vector,
        query_filter=qdrant_filter,
        limit=limit,
        with_payload=True,
    )

    return response.points


def causal_terms(text: str) -> list[str]:
    t = text.lower()
    terms = []

    candidates = [
        "hook.run",
        "net.receive",
        "netstream",
        "setdata",
        "sync",
        "receiver",
        "receivers",
        "itemdatachanged",
        "inventorydatachanged",
        "nutinventoryadd",
        "nutinventoryremove",
        "invdata",
        "removeitem",
        "inventory:add",
        "setuppanel",
        "populateitems",
    ]

    for term in candidates:
        if term in t:
            terms.append(term)

    return terms


def rerank_result(point: Any, query: str) -> tuple[float, list[str]]:
    payload = point.payload or {}
    text = str(payload.get("text", ""))
    file_path = str(payload.get("file", ""))
    doc_type = str(payload.get("doc_type", ""))
    node_type = str(payload.get("node_type", ""))

    q = query.lower()
    normalized_file = file_path.replace("\\", "/").lower()

    score = 0.0
    reasons: list[str] = []

    if "docs/project_structure.md" in normalized_file:
        score -= 0.40
        reasons.append("penalty:project_structure:-0.40")

    if doc_type == "doctrine":
        score += 0.20
        reasons.append("doc_type:doctrine:+0.20")

    if doc_type == "file_topology":
        score += 0.12
        reasons.append("doc_type:file_topology:+0.12")

    if node_type:
        score += 0.10
        reasons.append(f"node_type:{node_type}:+0.10")

    for subsystem in ["inventory", "vendor", "storage", "gridinv", "multichar"]:
        if subsystem in q and subsystem in (text.lower() + " " + file_path.lower()):
            score += 0.05
            reasons.append(f"text_subsystem:{subsystem}:+0.05")

    for event in [
        "characterloaded",
        "playerloadedchar",
        "playerloadout",
        "postplayerloadout",
        "itemdatachanged",
        "inventorydatachanged",
    ]:
        if event in q and event in text.lower():
            score += 0.10
            reasons.append(f"text_event:{event}:+0.10")

    if "docs/runtime/runtime_chains/" in normalized_file:
        score += 0.45
        reasons.append("runtime_chain:+0.45")

    if "docs/project_memory" in file_path.replace("\\", "/"):
        score += 0.16
        reasons.append("project_memory:+0.16")

    if "docs/human_context" in file_path.replace("\\", "/"):
        score += 0.16
        reasons.append("human_context:+0.16")

    for term in causal_terms(text):
        score += 0.08
        reasons.append(f"causal:{term}:+0.08")

    if any(x in text.lower() for x in ["server", "client", "realm", "netstream", "net.receive"]):
        score += 0.04
        reasons.append("realm_or_network_signal:+0.04")

    base = float(point.score or 0.0)
    final = base * 0.55 + score * 0.45

    return final, reasons


def write_report(
    out_path: Path,
    *,
    collection: str,
    query: str,
    expanded_query: str,
    top_k: int,
    retrieve_k: int,
    model: str,
    hash_query: bool,
    rows: list[dict[str, Any]],
) -> None:
    lines: list[str] = []

    lines.extend(
        [
            "# Qdrant Query Results",
            "",
            f"Collection: `{collection}`",
            f"Query: `{query}`",
            f"Expanded query used: `{expanded_query}`",
            f"Top K: **{top_k}**",
            f"Retrieve K: **{retrieve_k}**",
            f"Model: `{model}`",
            f"Hash query: `{hash_query}`",
            "",
            f"## Returned results: {len(rows)}",
            "",
        ]
    )

    for i, row in enumerate(rows, start=1):
        payload = row["payload"]

        lines.extend(
            [
                f"## Result {i}",
                "",
                f"- Score: **{row['score']:.4f}**",
                f"- Rerank score: `{row.get('rerank_score')}`",
                f"- Rerank reasons: `{row.get('rerank_reasons', [])}`",
                f"- Source ID: `{payload.get('source_id', '')}`",
                f"- Doc type: `{payload.get('doc_type', '')}`",
                f"- Node type: `{payload.get('node_type', '')}`",
                f"- Plugin: `{payload.get('plugin', '')}`",
                f"- Subsystem: `{payload.get('subsystem', '')}`",
                f"- Realm: `{payload.get('realm', '')}`",
                f"- File: `{payload.get('file', '')}`",
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
                str(payload.get("text", "")),
                "```",
                "",
            ]
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--query", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--retrieve-k", type=int, default=None)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=6333)
    parser.add_argument("--hash", action="store_true", help="Use deterministic hash query vector.")
    parser.add_argument("--dim", type=int, default=DEFAULT_DIM)
    parser.add_argument("--no-expand", action="store_true")
    parser.add_argument("--rerank", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--doc-type", default=None)
    parser.add_argument("--file", default=None)

    args = parser.parse_args()

    retrieve_k = args.retrieve_k or args.top_k
    expanded_query = expand_query(args.query, args.workspace, enabled=not args.no_expand)

    vector = encode_query(
        query=expanded_query,
        model_name=args.model,
        hash_only=args.hash,
        dim=args.dim,
    )

    client = QdrantClient(host=args.host, port=args.port)

    validate_vector_dimension(client, args.collection, vector)

    raw_results = list(
        run_search(
            client=client,
            collection=args.collection,
            vector=vector,
            qdrant_filter=build_filter(args),
            limit=retrieve_k,
        )
    )

    rows: list[dict[str, Any]] = []

    for point in raw_results:
        payload = point.payload or {}
        row = {
            "score": float(point.score or 0.0),
            "payload": payload,
            "rerank_score": None,
            "rerank_reasons": [],
        }

        if args.rerank:
            rerank_score, reasons = rerank_result(point, args.query)
            row["rerank_score"] = rerank_score
            row["rerank_reasons"] = reasons

        rows.append(row)

    if args.rerank:
        rows.sort(key=lambda r: float(r["rerank_score"] or -1.0), reverse=True)
    else:
        rows.sort(key=lambda r: float(r["score"]), reverse=True)

    rows = rows[: args.top_k]

    if args.write:
        out_path = args.out or args.workspace / "manifests" / "semantic" / "qdrant_query_results.md"
        write_report(
            out_path,
            collection=args.collection,
            query=args.query,
            expanded_query=expanded_query,
            top_k=args.top_k,
            retrieve_k=retrieve_k,
            model=args.model,
            hash_query=args.hash,
            rows=rows,
        )
        print(f"Wrote report to: {out_path}")
    else:
        print("# Qdrant Query Results")
        print()
        for i, row in enumerate(rows, start=1):
            payload = row["payload"]
            print(f"{i}. score={row['score']:.4f} rerank={row['rerank_score']} file={payload.get('file')}")


if __name__ == "__main__":
    main()