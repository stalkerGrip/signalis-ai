from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def read_jsonl(path: Path):
    rows = []
    bad = []

    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            raw = line.strip()
            if not raw:
                continue

            try:
                rows.append((line_no, json.loads(raw)))
            except Exception as exc:
                bad.append((line_no, str(exc)))

    return rows, bad


def get_id(row):
    return (
        row.get("id")
        or row.get("point_id")
        or row.get("document_id")
        or row.get("payload", {}).get("id")
    )


def get_vector(row):
    return row.get("vector") or row.get("embedding")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--expected-dim", type=int, default=384)
    args = parser.parse_args()

    workspace = args.workspace
    embeddings_path = workspace / "manifests" / "semantic" / "qdrant_embeddings.jsonl"
    out_md = workspace / "manifests" / "semantic" / "qdrant_ingest_filtering_audit.md"

    rows, bad_json = read_jsonl(embeddings_path)

    ids = []
    valid = []
    skipped = []

    for line_no, row in rows:
        rid = get_id(row)
        vector = get_vector(row)
        payload = row.get("payload")

        reasons = []

        if not rid:
            reasons.append("missing id")

        if not isinstance(vector, list):
            reasons.append("missing or non-list vector")
        elif len(vector) != args.expected_dim:
            reasons.append(f"bad vector dimension: {len(vector)}")

        if payload is not None and not isinstance(payload, dict):
            reasons.append("payload is not object")

        if reasons:
            skipped.append(
                {
                    "line": line_no,
                    "id": rid,
                    "reasons": reasons,
                }
            )
        else:
            valid.append(row)
            ids.append(rid)

    duplicate_ids = sorted(k for k, v in Counter(ids).items() if v > 1)

    lines = [
        "# Qdrant Ingest Filtering Audit",
        "",
        f"- Embedding JSONL rows: **{len(rows)}**",
        f"- Bad JSON lines: **{len(bad_json)}**",
        f"- Rows valid for ingest: **{len(valid)}**",
        f"- Rows skipped before ingest: **{len(skipped)}**",
        f"- Unique valid IDs: **{len(set(ids))}**",
        f"- Duplicate valid IDs: **{len(duplicate_ids)}**",
        "",
        "## Skipped rows",
    ]

    if skipped:
        for item in skipped[:100]:
            lines.append(
                f"- line `{item['line']}` id=`{item['id']}` reasons={', '.join(item['reasons'])}"
            )
    else:
        lines.append("- none")

    lines += ["", "## Bad JSON lines"]
    if bad_json:
        for line_no, err in bad_json[:100]:
            lines.append(f"- line `{line_no}`: {err}")
    else:
        lines.append("- none")

    lines += ["", "## Duplicate valid IDs"]
    if duplicate_ids:
        for rid in duplicate_ids[:100]:
            lines.append(f"- `{rid}`")
    else:
        lines.append("- none")

    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote audit: {out_md}")


if __name__ == "__main__":
    main()