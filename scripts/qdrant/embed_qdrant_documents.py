#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
import os
import random
from pathlib import Path
from typing import Any, Iterable


PIPELINE_CONTRACT = {
    "script_id": "scripts.qdrant.embed_qdrant_documents",
    "purpose": (
        "Generate BGE embeddings for semantic documents and runtime chain "
        "corpus artifacts."
    ),
    "pipeline_stage": "embedding",
    "input_schemas": [
        "qdrant_documents.v1",
        "runtime_chain_corpus.v1"
    ],
    "output_schemas": [
        "qdrant_embeddings.v1",
        "qdrant_embedding_summary.v1"
    ],
    "artifact_patterns": [
        "manifests/semantic/*embeddings*.jsonl",
        "manifests/semantic/*embedding_summary*.md"
    ],
    "promotion_role": "promotion_support",
    "canonical_status": "active"
}


DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"
FALLBACK_MODEL = "BAAI/bge-small-en-v1.5"
HASH_MODEL_NAME = "signalis-hash-embedding-v1"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing input documents file: {path}")

    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
            if isinstance(value, dict):
                rows.append(value)
    return rows


def load_optional_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return load_jsonl(path)


def resolve_workspace_path(workspace: Path, value: Path) -> Path:
    if value.is_absolute():
        return value
    return workspace / value


def default_required_inputs(workspace: Path) -> list[Path]:
    semantic_dir = workspace / "manifests" / "semantic"
    return [semantic_dir / "qdrant_documents.jsonl"]


def default_optional_inputs(workspace: Path) -> list[Path]:
    semantic_dir = workspace / "manifests" / "semantic"
    return [semantic_dir / "runtime_chain_corpus.jsonl"]


def load_documents_from_inputs(
    required_inputs: list[Path],
    optional_inputs: list[Path],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    docs: list[dict[str, Any]] = []
    load_report: list[dict[str, Any]] = []

    for input_path in required_inputs:
        rows = load_jsonl(input_path)
        docs.extend(rows)
        load_report.append({
            "path": str(input_path),
            "required": True,
            "exists": True,
            "rows": len(rows),
        })

    for input_path in optional_inputs:
        exists = input_path.exists()
        rows = load_optional_jsonl(input_path)
        docs.extend(rows)
        load_report.append({
            "path": str(input_path),
            "required": False,
            "exists": exists,
            "rows": len(rows),
        })

    return docs, load_report


def count_field(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for row in rows:
        value = row.get(key)
        if value is None and key == "doc_type":
            value = row.get("type")
        counts[str(value or "unknown")] += 1
    return dict(sorted(counts.items()))


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    count = 0
    with tmp.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    tmp.replace(path)
    return count


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def get_doc_text(doc: dict[str, Any]) -> str:
    for key in ("text", "content", "body"):
        value = doc.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    title = str(doc.get("title") or "")
    metadata = doc.get("metadata") or {}
    return f"{title}\n\n{json.dumps(metadata, ensure_ascii=False)}".strip()


def build_embedding_row(
    doc: dict[str, Any],
    *,
    text: str,
    vec: list[float],
    embedding_model: str,
) -> dict[str, Any]:
    row = dict(doc)

    row["id"] = doc.get("id")
    row["doc_type"] = doc.get("doc_type") or doc.get("type") or "unknown"
    row["title"] = doc.get("title")
    row["metadata"] = doc.get("metadata", {})
    row["content_hash"] = sha256_text(text)
    row["embedding_dim"] = len(vec)
    row["embedding_model"] = embedding_model
    row["embedding"] = vec
    row["text"] = text

    return row


def nomic_prefix(text: str, model_name: str) -> str:
    if "nomic" in model_name.lower() and not text.startswith("search_document:"):
        return "search_document: " + text
    return text


def tokenize(text: str) -> list[str]:
    # Lightweight tokenizer good enough for deterministic fallback retrieval.
    chars = []
    for ch in text.lower():
        if ch.isalnum() or ch in "_:/.-":
            chars.append(ch)
        else:
            chars.append(" ")
    return [tok for tok in "".join(chars).split() if tok]


def hash_embedding(text: str, dim: int = 384) -> list[float]:
    # Signed hashing trick with L2 normalization.
    vec = [0.0] * dim
    tokens = tokenize(text)

    # Include word unigrams and adjacent bigrams.
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


def load_sentence_model(model_name: str, device: str, trust_remote_code: bool):
    from sentence_transformers import SentenceTransformer

    kwargs: dict[str, Any] = {"device": device}
    if trust_remote_code or "nomic" in model_name.lower():
        kwargs["trust_remote_code"] = True
    return SentenceTransformer(model_name, **kwargs)


def rows_from_hash(docs: list[dict[str, Any]], dim: int, limit: int | None) -> list[dict[str, Any]]:
    selected = docs[:limit] if limit else docs
    rows: list[dict[str, Any]] = []

    for i, doc in enumerate(selected, 1):
        text = get_doc_text(doc)
        vec = hash_embedding(text, dim=dim)
        rows.append(
            build_embedding_row(
                doc,
                text=text,
                vec=vec,
                embedding_model=HASH_MODEL_NAME,
            )
        )
        if i % 100 == 0:
            print(f"[INFO] Hash embedded {i}/{len(selected)}")

    return rows


def rows_from_sentence_model(
    docs: list[dict[str, Any]],
    model_name: str,
    device: str,
    batch_size: int,
    trust_remote_code: bool,
    limit: int | None,
) -> list[dict[str, Any]]:
    selected = docs[:limit] if limit else docs
    model = load_sentence_model(model_name, device=device, trust_remote_code=trust_remote_code)

    rows: list[dict[str, Any]] = []
    for start in range(0, len(selected), batch_size):
        batch = selected[start:start + batch_size]
        texts = [get_doc_text(doc) for doc in batch]
        inputs = [nomic_prefix(text, model_name) for text in texts]

        print(f"[INFO] Encoding batch {start + 1}-{start + len(batch)} / {len(selected)}")
        vectors = model.encode(
            inputs,
            batch_size=batch_size,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        for doc, text, vector in zip(batch, texts, vectors):
            vec = vector.tolist() if hasattr(vector, "tolist") else list(vector)
            rows.append(
                build_embedding_row(
                    doc,
                    text=text,
                    vec=vec,
                    embedding_model=model_name,
                )
            )

    return rows


def write_summary(
    path: Path,
    *,
    input_report: list[dict[str, Any]],
    output_path: Path,
    model_requested: str,
    model_used: str,
    fallback_reason: str,
    docs_loaded: int,
    rows_written: int,
    dim: int,
    doc_type_counts: dict[str, int],
    schema_counts: dict[str, int],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    input_block = "\n".join(
        f"{item['path']} | required={item['required']} | exists={item['exists']} | rows={item['rows']}"
        for item in input_report
    )

    doc_type_block = "\n".join(
        f"- `{key}`: **{value}**" for key, value in doc_type_counts.items()
    ) or "- none"

    schema_block = "\n".join(
        f"- `{key}`: **{value}**" for key, value in schema_counts.items()
    ) or "- none"

    lines = [
        "# Qdrant Embedding Summary",
        "",
        f"Model requested: `{model_requested}`",
        f"Model used: `{model_used}`",
        "",
        "## Files",
        "",
        "Inputs:",
        "",
        "```text",
        input_block,
        "```",
        "",
        "Output:",
        "",
        "```text",
        str(output_path),
        "```",
        "",
        "## Results",
        "",
        f"- Documents loaded: **{docs_loaded}**",
        f"- Embeddings written: **{rows_written}**",
        f"- Embedding dimension: **{dim}**",
        f"- Output exists: **{output_path.exists()}**",
        f"- Output size: **{output_path.stat().st_size if output_path.exists() else 0} bytes**",
        "",
        "## Document Types",
        "",
        doc_type_block,
        "",
        "## Schemas",
        "",
        schema_block,
        "",
        "## Fallback reason",
        "",
        "```text",
        fallback_reason or "none",
        "```",
        "",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Embed SIGNALIS Qdrant documents with deterministic no-model fallback."
    )
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument(
        "--input-jsonl",
        action="append",
        type=Path,
        default=None,
        help=(
            "Required input JSONL. May be repeated. "
            "Default: <workspace>/manifests/semantic/qdrant_documents.jsonl"
        ),
    )
    parser.add_argument(
        "--optional-input-jsonl",
        action="append",
        type=Path,
        default=None,
        help=(
            "Optional input JSONL. May be repeated. "
            "Default: <workspace>/manifests/semantic/runtime_chain_corpus.jsonl"
        ),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Default: <workspace>/manifests/semantic/qdrant_embeddings.jsonl",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=None,
        help="Default: <workspace>/manifests/semantic/qdrant_embedding_summary.md",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--fallback-model", default=FALLBACK_MODEL)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--hash-only", action="store_true", help="Skip sentence-transformers and use deterministic fallback.")
    parser.add_argument("--hash-dim", type=int, default=384)
    # Compatibility. Writing is always enabled.
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    workspace = args.workspace.resolve()

    semantic_dir = workspace / "manifests" / "semantic"

    required_inputs = [
        resolve_workspace_path(workspace, path)
        for path in (args.input_jsonl or default_required_inputs(workspace))
    ]
    optional_inputs = [
        resolve_workspace_path(workspace, path)
        for path in (args.optional_input_jsonl or default_optional_inputs(workspace))
    ]

    output_path = resolve_workspace_path(
        workspace,
        args.out or semantic_dir / "qdrant_embeddings.jsonl",
    )
    summary_path = resolve_workspace_path(
        workspace,
        args.summary or semantic_dir / "qdrant_embedding_summary.md",
    )

    print(f"[INFO] Workspace: {workspace}")
    for input_path in required_inputs:
        print(f"[INFO] Required input: {input_path}")
    for input_path in optional_inputs:
        print(f"[INFO] Optional input: {input_path}")
    print(f"[INFO] Output embeddings: {output_path}")

    docs, input_report = load_documents_from_inputs(
        required_inputs=required_inputs,
        optional_inputs=optional_inputs,
    )

    for item in input_report:
        print(
            "[INFO] Loaded "
            f"{item['rows']} rows from {item['path']} "
            f"required={item['required']} exists={item['exists']}"
        )

    if not docs:
        raise RuntimeError("No documents loaded from configured input JSONL files.")

    model_used = args.model
    fallback_reason = ""

    if args.hash_only:
        fallback_reason = "--hash-only requested"
        model_used = HASH_MODEL_NAME
        rows = rows_from_hash(docs, dim=args.hash_dim, limit=args.limit)
    else:
        try:
            rows = rows_from_sentence_model(
                docs,
                model_name=args.model,
                device=args.device,
                batch_size=args.batch_size,
                trust_remote_code=args.trust_remote_code,
                limit=args.limit,
            )
        except Exception as primary_exc:
            fallback_reason = f"Primary model failed: {primary_exc!r}"
            print(f"[WARN] {fallback_reason}")
            try:
                model_used = args.fallback_model
                rows = rows_from_sentence_model(
                    docs,
                    model_name=args.fallback_model,
                    device=args.device,
                    batch_size=args.batch_size,
                    trust_remote_code=False,
                    limit=args.limit,
                )
            except Exception as fallback_exc:
                fallback_reason += f"\nFallback model failed: {fallback_exc!r}\nUsing deterministic hash embeddings."
                print(f"[WARN] Fallback model failed: {fallback_exc!r}")
                print("[INFO] Using deterministic hash embeddings.")
                model_used = HASH_MODEL_NAME
                rows = rows_from_hash(docs, dim=args.hash_dim, limit=args.limit)

    if not rows:
        raise RuntimeError("Embedding produced 0 rows.")

    written = write_jsonl(output_path, rows)
    dim = int(rows[0].get("embedding_dim") or 0)

    write_summary(
        summary_path,
        input_report=input_report,
        output_path=output_path,
        model_requested=args.model,
        model_used=model_used,
        fallback_reason=fallback_reason,
        docs_loaded=len(docs),
        rows_written=written,
        dim=dim,
        doc_type_counts=count_field(rows, "doc_type"),
        schema_counts=count_field(rows, "schema"),
    )

    print(f"[OK] Wrote embeddings: {output_path}")
    print(f"[OK] Rows: {written}")
    print(f"[OK] Dimension: {dim}")
    print(f"[OK] Summary: {summary_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
