#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    count = 0
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                json.loads(line)
                count += 1
    return count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    docs = workspace / "manifests" / "semantic" / "qdrant_documents.jsonl"
    embeddings = workspace / "manifests" / "semantic" / "qdrant_embeddings.jsonl"
    summary = workspace / "manifests" / "semantic" / "qdrant_embedding_summary.md"

    for path in [docs, embeddings, summary]:
        print(f"{path}")
        print(f"  exists: {path.exists()}")
        print(f"  size: {path.stat().st_size if path.exists() else 0}")
        if path.suffix == ".jsonl" and path.exists():
            print(f"  jsonl rows: {count_jsonl(path)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
