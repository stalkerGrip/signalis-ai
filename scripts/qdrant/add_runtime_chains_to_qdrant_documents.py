#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def stable_id(path: Path, workspace: Path) -> str:
    rel = path.resolve().relative_to(workspace.resolve()).as_posix()
    safe = rel.replace("/", ":").replace("\\", ":")
    return f"runtime_chain:{safe}"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )


def make_doc(path: Path, workspace: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    rel = path.resolve().relative_to(workspace.resolve()).as_posix()
    title = path.stem.replace("_", " ").title()

    # Use broad field names so downstream embedders that expect either text/content/body
    # have something usable.
    return {
        "id": stable_id(path, workspace),
        "type": "runtime_chain",
        "subsystem": rel.split("/")[2] if rel.startswith("docs/runtime/") else "runtime",
        "title": title,
        "path": rel,
        "source_path": rel,
        "content": text,
        "text": text,
        "metadata": {
            "artifact_type": "runtime_chain",
            "source": "promoted_runtime_chain",
            "path": rel,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument(
        "--chain-dir",
        type=Path,
        default=None,
        help="Defaults to <workspace>/docs/runtime/runtime_chains",
    )
    parser.add_argument(
        "--documents",
        type=Path,
        default=None,
        help="Defaults to <workspace>/manifests/semantic/qdrant_documents.jsonl",
    )
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    chain_dir = args.chain_dir.resolve() if args.chain_dir else workspace / "docs" / "runtime" / "runtime_chains"
    documents = args.documents.resolve() if args.documents else workspace / "manifests" / "semantic" / "qdrant_documents.jsonl"

    if not chain_dir.exists():
        print(f"[FAIL] Runtime chain directory does not exist: {chain_dir}")
        return 2

    rows = read_jsonl(documents)
    by_id = {str(row.get("id")): row for row in rows if row.get("id")}

    added = 0
    updated = 0

    for md in sorted(chain_dir.glob("*.md")):
        doc = make_doc(md, workspace)
        doc_id = doc["id"]

        if doc_id in by_id:
            by_id[doc_id] = doc
            updated += 1
        else:
            by_id[doc_id] = doc
            added += 1

    # Preserve non-id rows too, then append id-indexed rows deterministically.
    no_id_rows = [row for row in rows if not row.get("id")]
    final_rows = no_id_rows + [by_id[k] for k in sorted(by_id)]

    write_jsonl(documents, final_rows)

    print(f"Wrote: {documents}")
    print(f"Runtime chain dir: {chain_dir}")
    print(f"Added: {added}")
    print(f"Updated: {updated}")
    print(f"Total documents now: {len(final_rows)}")
    print("")
    print("Next:")
    print("  python -m scripts.qdrant.embed_qdrant_documents --workspace E:/signalis_ai")
    print("  python -m scripts.qdrant.ingest_qdrant --workspace E:/signalis_ai")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
