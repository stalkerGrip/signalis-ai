from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any


RESULT_RE = re.compile(
    r"## Result (?P<rank>\d+)\n(?P<body>.*?)(?=\n## Result \d+|\Z)",
    re.DOTALL,
)

FIELD_RE = {
    "score": re.compile(r"- Score: \*\*(.*?)\*\*"),
    "rerank": re.compile(r"- Rerank score: `(.*?)`"),
    "source_id": re.compile(r"- Source ID: `(.*?)`"),
    "doc_type": re.compile(r"- Doc type: `(.*?)`"),
    "node_type": re.compile(r"- Node type: `(.*?)`"),
    "plugin": re.compile(r"- Plugin: `(.*?)`"),
    "subsystem": re.compile(r"- Subsystem: `(.*?)`"),
    "realm": re.compile(r"- Realm: `(.*?)`"),
    "file": re.compile(r"- File: `(.*?)`"),
}


def field(body: str, name: str, default: str = "") -> str:
    match = FIELD_RE[name].search(body)
    if not match:
        return default

    value = match.group(1).strip()
    return "" if value == "None" else value


def to_float(value: str) -> float:
    if not value or value == "None":
        return -1.0

    try:
        return float(value)
    except ValueError:
        return -1.0


def extract_text_block(body: str) -> str:
    marker = "### Text"
    marker_index = body.find(marker)

    if marker_index < 0:
        return ""

    tail = body[marker_index + len(marker):].lstrip()

    fence = "```text"
    if tail.startswith(fence):
        tail = tail[len(fence):].lstrip("\r\n")

    # Qdrant result text may itself contain markdown code fences.
    # Remove only the final wrapper fence if present.
    final_fence = tail.rfind("\n```")
    if final_fence >= 0:
        tail = tail[:final_fence]

    return tail.strip()


def classify(file_path: str, doc_type: str) -> str:
    path = file_path.replace("\\", "/").lower()
    doc_type = (doc_type or "").lower()

    if "runtime_chains/" in path:
        return "runtime_chains"

    if "human_context" in path or "human_subsystems/" in path:
        return "human_context"

    if "project_memory" in path:
        return "project_memory"

    if "subsystems/" in path or "ai_subsystems/" in path or "subsystem_docs/" in path:
        return "subsystem_docs"

    if doc_type == "file_topology":
        return "file_topology"

    if "doctrine" in doc_type or "doctrine" in path:
        return "doctrine"

    return "other"


def parse_results(markdown: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    for match in RESULT_RE.finditer(markdown):
        body = match.group("body").strip()
        file_path = field(body, "file")
        source_id = field(body, "source_id")
        doc_type = field(body, "doc_type")

        row: dict[str, Any] = {
            "rank": int(match.group("rank")),
            "body": body,
            "score": field(body, "score"),
            "rerank": field(body, "rerank"),
            "source_id": source_id,
            "doc_type": doc_type,
            "node_type": field(body, "node_type"),
            "plugin": field(body, "plugin"),
            "subsystem": field(body, "subsystem"),
            "realm": field(body, "realm"),
            "file": file_path,
            "text": extract_text_block(body),
            "dedupe_key": file_path or source_id,
        }

        row["bucket"] = classify(row["file"], row["doc_type"])
        rows.append(row)

    return rows


def result_sort_key(row: dict[str, Any]) -> tuple[float, float, int]:
    return (
        to_float(row["rerank"]),
        to_float(row["score"]),
        -int(row["rank"]),
    )


def dedupe_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    best_by_key: dict[str, dict[str, Any]] = {}

    for row in rows:
        key = row["dedupe_key"]

        if key not in best_by_key:
            best_by_key[key] = row
            continue

        if result_sort_key(row) > result_sort_key(best_by_key[key]):
            best_by_key[key] = row

    return sorted(best_by_key.values(), key=result_sort_key, reverse=True)


def trim_text(row: dict[str, Any], default_limit: int, runtime_chain_limit: int) -> str:
    text = row["text"]

    limit = runtime_chain_limit if row["bucket"] == "runtime_chains" else default_limit

    if len(text) <= limit:
        return text

    return text[:limit].rstrip() + "\n...[truncated]"


def emit_row(row: dict[str, Any], default_limit: int, runtime_chain_limit: int) -> str:
    text = trim_text(row, default_limit, runtime_chain_limit)

    return (
        f"### Result {row['rank']} — `{row['file']}`\n\n"
        f"- Source ID: `{row['source_id']}`\n"
        f"- Doc type: `{row['doc_type']}`\n"
        f"- Node type: `{row['node_type']}`\n"
        f"- Plugin: `{row['plugin']}`\n"
        f"- Subsystem: `{row['subsystem']}`\n"
        f"- Realm: `{row['realm']}`\n"
        f"- Score: `{row['score']}`\n"
        f"- Rerank score: `{row['rerank']}`\n\n"
        f"~~~text\n{text}\n~~~\n"
    )


def emit_section(
    title: str,
    rows: list[dict[str, Any]],
    default_limit: int,
    runtime_chain_limit: int,
) -> str:
    if not rows:
        return f"## {title}\n\nNone.\n"

    parts = [f"## {title}\n"]

    for row in rows:
        parts.append(emit_row(row, default_limit, runtime_chain_limit))

    return "\n".join(parts)


def build_pack(
    rows: list[dict[str, Any]],
    query: str,
    original_count: int,
    default_limit: int,
    runtime_chain_limit: int,
) -> str:
    buckets: dict[str, list[dict[str, Any]]] = {
        "runtime_chains": [],
        "human_context": [],
        "project_memory": [],
        "subsystem_docs": [],
        "doctrine": [],
        "file_topology": [],
        "other": [],
    }

    for row in rows:
        buckets[row["bucket"]].append(row)

    return "\n\n".join(
        [
            "# Investigation Context Pack",
            "",
            f"Query: `{query}`",
            "",
            "Purpose: compact retrieval pack for investigation synthesis. Use this before opening raw Lua.",
            "",
            "## Pack Summary",
            "",
            f"- Original retrieved results: **{original_count}**",
            f"- Deduplicated results: **{len(rows)}**",
            f"- Duplicates removed: **{original_count - len(rows)}**",
            "",
            emit_section("Runtime Chains", buckets["runtime_chains"], default_limit, runtime_chain_limit),
            emit_section("Human Context", buckets["human_context"], default_limit, runtime_chain_limit),
            emit_section("Project Memory", buckets["project_memory"], default_limit, runtime_chain_limit),
            emit_section("Subsystem Docs", buckets["subsystem_docs"], default_limit, runtime_chain_limit),
            emit_section("Doctrine", buckets["doctrine"], default_limit, runtime_chain_limit),
            emit_section("File Topology", buckets["file_topology"], default_limit, runtime_chain_limit),
            emit_section("Other Retrieved Evidence", buckets["other"], default_limit, runtime_chain_limit),
        ]
    )


def write_summary(out_path: Path, original_count: int, rows: list[dict[str, Any]]) -> None:
    summary_path = out_path.with_suffix(".summary.md")

    lines = [
        "# Investigation Context Pack Summary",
        "",
        f"- Original retrieved results: **{original_count}**",
        f"- Deduplicated results: **{len(rows)}**",
        f"- Duplicates removed: **{original_count - len(rows)}**",
        "",
        "## Kept Results",
        "",
    ]

    for index, row in enumerate(rows, start=1):
        lines.append(
            f"{index}. `{row['file']}` "
            f"| bucket `{row['bucket']}` "
            f"| rerank `{row['rerank']}` "
            f"| score `{row['score']}` "
            f"| original rank `{row['rank']}`"
        )

    summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] Wrote summary: {summary_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a deduplicated investigation context pack from Qdrant markdown results."
    )

    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--query", required=True)
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
        help="Defaults to investigations/context_pack.md",
    )
    parser.add_argument("--no-dedupe", action="store_true")
    parser.add_argument("--text-limit", type=int, default=2500)
    parser.add_argument("--runtime-chain-limit", type=int, default=7000)

    args = parser.parse_args()

    workspace: Path = args.workspace
    query_results = args.query_results or workspace / "manifests/semantic/qdrant_query_results.md"
    out_path = args.out or workspace / "investigations/context_pack.md"

    if not query_results.exists():
        raise FileNotFoundError(f"Query results not found: {query_results}")

    markdown = query_results.read_text(encoding="utf-8", errors="replace")
    rows = parse_results(markdown)

    if not rows:
        raise RuntimeError(f"No Qdrant results found in: {query_results}")

    original_count = len(rows)

    if not args.no_dedupe:
        rows = dedupe_rows(rows)

    pack = build_pack(
        rows=rows,
        query=args.query,
        original_count=original_count,
        default_limit=args.text_limit,
        runtime_chain_limit=args.runtime_chain_limit,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(pack, encoding="utf-8")

    print(f"[OK] Original results: {original_count}")
    print(f"[OK] Deduplicated results: {len(rows)}")
    print(f"[OK] Duplicates removed: {original_count - len(rows)}")
    print(f"[OK] Wrote context pack: {out_path}")

    write_summary(out_path, original_count, rows)


if __name__ == "__main__":
    main()