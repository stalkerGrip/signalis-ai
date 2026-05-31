from __future__ import annotations

import argparse
import re
from pathlib import Path


RESULT_RE = re.compile(
    r"## Result (?P<rank>\d+)\n(?P<body>.*?)(?=\n## Result \d+|\Z)",
    re.DOTALL,
)

FIELD_RE = {
    "score": re.compile(r"- Score: \*\*(.*?)\*\*"),
    "rerank": re.compile(r"- Rerank score: `(.*?)`"),
    "source_id": re.compile(r"- Source ID: `(.*?)`"),
    "doc_type": re.compile(r"- Doc type: `(.*?)`"),
    "file": re.compile(r"- File: `(.*?)`"),
}


def field(body: str, name: str, default: str = "") -> str:
    match = FIELD_RE[name].search(body)
    return match.group(1).strip() if match else default


def to_float(value: str) -> float:
    if not value or value == "None":
        return -1.0

    try:
        return float(value)
    except ValueError:
        return -1.0


def parse_results(markdown: str) -> list[dict]:
    rows = []

    for match in RESULT_RE.finditer(markdown):
        body = match.group("body")

        file_path = field(body, "file")
        source_id = field(body, "source_id")

        rows.append(
            {
                "rank": int(match.group("rank")),
                "body": body.strip(),
                "score": field(body, "score"),
                "rerank": field(body, "rerank"),
                "source_id": source_id,
                "doc_type": field(body, "doc_type"),
                "file": file_path,
                "dedupe_key": file_path or source_id,
            }
        )

    return rows


def dedupe(rows: list[dict]) -> list[dict]:
    best_by_key: dict[str, dict] = {}

    for row in rows:
        key = row["dedupe_key"]

        if key not in best_by_key:
            best_by_key[key] = row
            continue

        current = best_by_key[key]

        row_rank_score = (
            to_float(row["rerank"]),
            to_float(row["score"]),
            -row["rank"],
        )
        current_rank_score = (
            to_float(current["rerank"]),
            to_float(current["score"]),
            -current["rank"],
        )

        if row_rank_score > current_rank_score:
            best_by_key[key] = row

    return sorted(
        best_by_key.values(),
        key=lambda row: (
            to_float(row["rerank"]),
            to_float(row["score"]),
            -row["rank"],
        ),
        reverse=True,
    )


def rewrite_markdown(original: str, rows: list[dict]) -> str:
    header = original.split("## Result 1", 1)[0].rstrip()

    out = [
        header,
        "",
        f"## Deduplicated results: {len(rows)}",
        "",
    ]

    for index, row in enumerate(rows, start=1):
        out.append(f"## Result {index}")
        out.append("")
        out.append(row["body"])
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def write_summary(out_path: Path, original_count: int, deduped_rows: list[dict]) -> None:
    summary_path = out_path.with_suffix(".summary.md")

    lines = [
        "# Deduplicated Qdrant Results Summary",
        "",
        f"- Original results: **{original_count}**",
        f"- Deduplicated results: **{len(deduped_rows)}**",
        f"- Duplicates removed: **{original_count - len(deduped_rows)}**",
        "",
        "## Kept Results",
        "",
    ]

    for idx, row in enumerate(deduped_rows, start=1):
        lines.append(
            f"{idx}. `{row['file']}` "
            f"| rerank `{row['rerank']}` "
            f"| score `{row['score']}` "
            f"| original rank `{row['rank']}`"
        )

    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] Wrote summary: {summary_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument(
        "--query-results",
        type=Path,
        default=None,
        help="Defaults to manifests/semantic/qdrant_query_results.md",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Defaults to manifests/semantic/qdrant_query_results_deduped.md",
    )

    args = parser.parse_args()

    workspace = args.workspace
    query_results = args.query_results or workspace / "manifests/semantic/qdrant_query_results.md"
    out_path = args.out or workspace / "manifests/semantic/qdrant_query_results_deduped.md"

    if not query_results.exists():
        raise FileNotFoundError(f"Query results not found: {query_results}")

    markdown = query_results.read_text(encoding="utf-8", errors="replace")
    rows = parse_results(markdown)

    if not rows:
        raise RuntimeError(f"No Qdrant results found in: {query_results}")

    deduped_rows = dedupe(rows)
    deduped_markdown = rewrite_markdown(markdown, deduped_rows)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(deduped_markdown, encoding="utf-8")

    print(f"[OK] Original results: {len(rows)}")
    print(f"[OK] Deduplicated results: {len(deduped_rows)}")
    print(f"[OK] Duplicates removed: {len(rows) - len(deduped_rows)}")
    print(f"[OK] Wrote deduped results: {out_path}")

    write_summary(out_path, len(rows), deduped_rows)


if __name__ == "__main__":
    main()