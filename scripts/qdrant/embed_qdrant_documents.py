import argparse
import hashlib
import json
from pathlib import Path

from sentence_transformers import SentenceTransformer


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--model", default="nomic-ai/nomic-embed-text-v1.5")
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    workspace = Path(args.workspace)

    input_path = workspace / "manifests" / "semantic" / "qdrant_documents.jsonl"
    output_path = workspace / "manifests" / "semantic" / "qdrant_embeddings.jsonl"
    summary_path = workspace / "manifests" / "semantic" / "qdrant_embedding_summary.md"

    docs = list(load_jsonl(input_path))

    model = SentenceTransformer(args.model, device=args.device)

    existing_hashes = set()

    if output_path.exists():
        for item in load_jsonl(output_path):
            existing_hashes.add(item.get("content_hash"))

    embedded = 0
    skipped = 0

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("a", encoding="utf-8") as out_f:
        for doc in docs:
            text = doc.get("text", "")
            content_hash = sha256_text(text)

            if content_hash in existing_hashes:
                skipped += 1
                continue

            vector = model.encode(text, normalize_embeddings=True).tolist()

            result = {
                "id": doc.get("id"),
                "doc_type": doc.get("doc_type"),
                "metadata": doc.get("metadata", {}),
                "content_hash": content_hash,
                "embedding_dim": len(vector),
                "embedding": vector,
                "text": text,
            }

            out_f.write(json.dumps(result, ensure_ascii=False) + "\n")
            embedded += 1

    summary = f"""# Qdrant Embedding Summary

Model: `{args.model}`
Device: `{args.device}`

## Results

- Input documents: **{len(docs)}**
- Embedded this run: **{embedded}**
- Skipped by hash cache: **{skipped}**

## Outputs

```text
{output_path}
```
"""

    summary_path.write_text(summary, encoding="utf-8")

    print(summary)


if __name__ == "__main__":
    main()
