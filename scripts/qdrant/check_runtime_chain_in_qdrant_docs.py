#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows

    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            print(f"[WARN] Bad JSONL at {path}:{line_no}: {exc}")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument(
        "--needle",
        default="vendor_purchase_item_metadata_sync",
        help="Text/path/title fragment to search in generated Qdrant documents.",
    )
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    docs_path = workspace / "manifests" / "semantic" / "qdrant_documents.jsonl"
    chain_doc = workspace / "docs" / "runtime" / "runtime_chains" / "vendor_purchase_item_metadata_sync.md"

    print(f"Workspace: {workspace}")
    print(f"Qdrant docs: {docs_path}")
    print(f"Runtime chain doc: {chain_doc}")
    print("")

    if chain_doc.exists():
        print("[OK] Runtime chain markdown exists.")
        text = chain_doc.read_text(encoding="utf-8", errors="replace")
        print(f"     Size: {len(text)} chars")
        print(f"     Contains invData: {'invData' in text}")
        print(f"     Contains ItemDataChanged: {'ItemDataChanged' in text}")
    else:
        print("[FAIL] Runtime chain markdown does not exist at expected path.")
        return 2

    rows = read_jsonl(docs_path)
    if not rows:
        print("[FAIL] qdrant_documents.jsonl missing or empty.")
        print("Run: python -m scripts.qdrant.build_qdrant_documents --workspace E:/signalis_ai")
        return 3

    print(f"[OK] Loaded qdrant documents: {len(rows)}")

    needle = args.needle.lower()
    matches: list[dict[str, Any]] = []
    for row in rows:
        blob = json.dumps(row, ensure_ascii=False).lower()
        if needle in blob or "vendor purchase item metadata sync" in blob:
            matches.append(row)

    if not matches:
        print("")
        print("[FAIL] Promoted runtime chain is NOT present in qdrant_documents.jsonl.")
        print("")
        print("Likely cause:")
        print("  build_qdrant_documents.py does not include docs/runtime/runtime_chains/*.md")
        print("")
        print("Next action:")
        print("  Apply/merge the runtime-chain corpus patch, rebuild documents, embed, then ingest.")
        return 4

    print("")
    print(f"[OK] Found {len(matches)} qdrant document(s) matching promoted chain.")
    for i, row in enumerate(matches[:5], 1):
        title = row.get("title") or row.get("name") or row.get("id") or "<no title>"
        path = row.get("path") or row.get("source_path") or row.get("file") or "<no path>"
        doc_id = row.get("id") or row.get("doc_id") or "<no id>"
        print(f"  {i}. id={doc_id}")
        print(f"     title={title}")
        print(f"     path={path}")

    print("")
    print("If query still returns nothing after this is present:")
    print("  1. Re-run embed_qdrant_documents.")
    print("  2. Re-run ingest_qdrant.")
    print("  3. If ingest appends to old collection incorrectly, recreate/clear the collection before ingest.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
