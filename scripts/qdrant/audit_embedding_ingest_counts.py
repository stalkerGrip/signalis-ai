from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def read_jsonl(path: Path):
    rows = []
    bad = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception as e:
                bad.append((i, str(e)))
    return rows, bad


def get_id(row):
    return row.get("id") or row.get("point_id") or row.get("document_id") or row.get("payload", {}).get("id")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--workspace", required=True, type=Path)
    args = p.parse_args()

    workspace = args.workspace
    docs_path = workspace / "manifests" / "semantic" / "qdrant_documents.jsonl"
    emb_path = workspace / "manifests" / "semantic" / "qdrant_embeddings.jsonl"
    out_md = workspace / "manifests" / "semantic" / "qdrant_embedding_ingest_audit.md"

    docs, docs_bad = read_jsonl(docs_path)
    embs, embs_bad = read_jsonl(emb_path)

    doc_ids = [get_id(r) for r in docs]
    emb_ids = [get_id(r) for r in embs]

    doc_counter = Counter(doc_ids)
    emb_counter = Counter(emb_ids)

    missing_embeddings = sorted(set(doc_ids) - set(emb_ids))
    extra_embeddings = sorted(set(emb_ids) - set(doc_ids))
    duplicate_doc_ids = sorted(k for k, v in doc_counter.items() if v > 1)
    duplicate_emb_ids = sorted(k for k, v in emb_counter.items() if v > 1)

    empty_vectors = []
    bad_dimensions = []

    for row in embs:
        rid = get_id(row)
        vector = row.get("vector") or row.get("embedding")
        if not vector:
            empty_vectors.append(rid)
        elif len(vector) != 384:
            bad_dimensions.append((rid, len(vector)))

    lines = [
        "# Qdrant Embedding/Ingest Count Audit",
        "",
        f"- Documents JSONL rows: **{len(docs)}**",
        f"- Embeddings JSONL rows: **{len(embs)}**",
        f"- Unique document IDs: **{len(set(doc_ids))}**",
        f"- Unique embedding IDs: **{len(set(emb_ids))}**",
        f"- Bad document JSON lines: **{len(docs_bad)}**",
        f"- Bad embedding JSON lines: **{len(embs_bad)}**",
        f"- Duplicate document IDs: **{len(duplicate_doc_ids)}**",
        f"- Duplicate embedding IDs: **{len(duplicate_emb_ids)}**",
        f"- Missing embeddings: **{len(missing_embeddings)}**",
        f"- Extra embeddings: **{len(extra_embeddings)}**",
        f"- Empty vectors: **{len(empty_vectors)}**",
        f"- Bad vector dimensions: **{len(bad_dimensions)}**",
        "",
        "## Duplicate embedding IDs",
    ]

    lines += [f"- `{x}`" for x in duplicate_emb_ids[:50]] or ["- none"]

    lines += ["", "## Duplicate document IDs"]
    lines += [f"- `{x}`" for x in duplicate_doc_ids[:50]] or ["- none"]

    lines += ["", "## Missing embeddings"]
    lines += [f"- `{x}`" for x in missing_embeddings[:50]] or ["- none"]

    lines += ["", "## Extra embeddings"]
    lines += [f"- `{x}`" for x in extra_embeddings[:50]] or ["- none"]

    lines += ["", "## Empty vectors"]
    lines += [f"- `{x}`" for x in empty_vectors[:50]] or ["- none"]

    lines += ["", "## Bad dimensions"]
    lines += [f"- `{rid}` dim={dim}" for rid, dim in bad_dimensions[:50]] or ["- none"]

    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote audit: {out_md}")


if __name__ == "__main__":
    main()