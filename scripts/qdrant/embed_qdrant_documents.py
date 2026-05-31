#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable


DEFAULT_MODEL = "nomic-ai/nomic-embed-text-v1.5"
FALLBACK_MODEL = "BAAI/bge-small-en-v1.5"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


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
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
            if isinstance(item, dict):
                rows.append(item)

    return rows


def write_jsonl_atomic(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(path.name + ".tmp")

    count = 0
    with tmp_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1

    tmp_path.replace(path)
    return count


def get_doc_text(doc: dict[str, Any]) -> str:
    for key in ("text", "content", "body"):
        value = doc.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    title = str(doc.get("title") or "")
    metadata = doc.get("metadata") or {}
    return f"{title}\n\n{json.dumps(metadata, ensure_ascii=False)}".strip()


def format_for_model(text: str, model_name: str) -> str:
    if "nomic" in model_name.lower() and not text.startswith("search_document:"):
        return f"search_document: {text}"
    return text


def load_model(model_name: str, device: str, trust_remote_code: bool):
    from sentence_transformers import SentenceTransformer

    kwargs: dict[str, Any] = {"device": device}
    if trust_remote_code:
        kwargs["trust_remote_code"] = True

    return SentenceTransformer(model_name, **kwargs)


def embed_with_model(
    docs: list[dict[str, Any]],
    model_name: str,
    device: str,
    batch_size: int,
    trust_remote_code: bool,
) -> list[dict[str, Any]]:
    model = load_model(model_name, device=device, trust_remote_code=trust_remote_code)

    texts = [get_doc_text(doc) for doc in docs]
    encoded_texts = [format_for_model(text, model_name) for text in texts]

    vectors = model.encode(
        encoded_texts,
        batch_size=batch_size,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    rows: list[dict[str, Any]] = []
    for doc, text, vector in zip(docs, texts, vectors):
        vec = vector.tolist() if hasattr(vector, "tolist") else list(vector)
        rows.append(
            {
                "id": doc.get("id"),
                "doc_type": doc.get("doc_type") or doc.get("type") or "unknown",
                "title": doc.get("title"),
                "metadata": doc.get("metadata", {}),
                "content_hash": sha256_text(text),
                "embedding_dim": len(vec),
                "embedding": vec,
                "text": text,
            }
        )

    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Embed SIGNALIS Qdrant documents. Writes qdrant_embeddings.jsonl by default."
    )
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--fallback-model", default=FALLBACK_MODEL)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--trust-remote-code", action="store_true")
    parser.add_argument("--no-fallback", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Embed but do not write output files.")
    # Backward compatibility: accepted but no longer needed.
    parser.add_argument("--write", action="store_true", help="Deprecated; writing is now default.")
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    input_path = workspace / "manifests" / "semantic" / "qdrant_documents.jsonl"
    output_path = workspace / "manifests" / "semantic" / "qdrant_embeddings.jsonl"
    summary_path = workspace / "manifests" / "semantic" / "qdrant_embedding_summary.md"

    print(f"[INFO] Workspace: {workspace}")
    print(f"[INFO] Input documents: {input_path}")
    print(f"[INFO] Output embeddings: {output_path}")

    docs = load_jsonl(input_path)
    if not docs:
        raise ValueError(f"No documents found in {input_path}")

    used_model = args.model
    fallback_used = False
    primary_error = "none"

    try:
        rows = embed_with_model(
            docs=docs,
            model_name=args.model,
            device=args.device,
            batch_size=args.batch_size,
            trust_remote_code=args.trust_remote_code,
        )
    except Exception as exc:
        primary_error = repr(exc)

        if args.no_fallback:
            raise

        print(f"[WARN] Primary model failed: {args.model}")
        print(f"[WARN] Error: {exc}")
        print(f"[INFO] Trying fallback model: {args.fallback_model}")

        used_model = args.fallback_model
        fallback_used = True
        rows = embed_with_model(
            docs=docs,
            model_name=args.fallback_model,
            device=args.device,
            batch_size=args.batch_size,
            trust_remote_code=False,
        )

    written = 0
    if not args.dry_run:
        written = write_jsonl_atomic(output_path, rows)

    summary = f"""# Qdrant Embedding Summary

Model requested: `{args.model}`
Model used: `{used_model}`
Device: `{args.device}`
Batch size: `{args.batch_size}`
Trust remote code requested: `{args.trust_remote_code}`
Fallback used: `{fallback_used}`
Dry run: `{args.dry_run}`

## Results

- Input documents: **{len(docs)}**
- Embeddings produced: **{len(rows)}**
- Embeddings written: **{written}**
- Embedding dimension: **{rows[0]["embedding_dim"] if rows else "n/a"}**

## Outputs

```text
{output_path}
```

## Primary model error

```text
{primary_error}
```
"""

    if not args.dry_run:
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(summary, encoding="utf-8")

    print(summary)

    if not args.dry_run:
        if not output_path.exists():
            raise FileNotFoundError(f"Expected output file was not created: {output_path}")
        if output_path.stat().st_size <= 0:
            raise RuntimeError(f"Output file exists but is empty: {output_path}")
        print(f"[OK] Created embeddings file: {output_path}")
        print(f"[OK] Size: {output_path.stat().st_size} bytes")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
