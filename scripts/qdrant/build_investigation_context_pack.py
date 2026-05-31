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

TEXT_RE = re.compile(r"### Text\n\n```text\n(?P<text>.*?)(?:\n```|\Z)", re.DOTALL)


def field(body: str, name: str, default: str = "") -> str:
    match = FIELD_RE[name].search(body)
    return match.group(1).strip() if match else default


def extract_text(body: str, limit: int) -> str:
    match = TEXT_RE.search(body)
    if not match:
        return ""
    text = match.group("text").strip()
    if len(text) > limit:
        return text[:limit].rstrip() + "\n...[truncated]"
    return text


def classify(file_path: str, doc_type: str) -> str:
    p = file_path.replace("\\", "/").lower()

    if "runtime_chains/" in p:
        return "runtime_chains"
    if "human_context" in p or "human_subsystems" in p:
        return "human_context"
    if "subsystems/" in p or "ai_subsystems/" in p or "subsystem_docs/" in p:
        return "subsystem_docs"
    if doc_type == "file_topology":
        return "file_topology"
    if "doctrine" in doc_type or "doctrine" in p or "project_memory" in p:
        return "doctrine"

    return "other"


def parse_results(markdown: str, text_limit: int) -> list[dict]:
    rows = []

    for match in RESULT_RE.finditer(markdown):
        body = match.group("body")

        row = {
            "rank": int(match.group("rank")),
            "score": field(body, "score"),
            "rerank": field(body, "rerank"),
            "source_id": field(body, "source_id"),
            "doc_type": field(body, "doc_type"),
            "file": field(body, "file"),
            "text": extract_text(body, text_limit),
        }

        row["bucket"] = classify(row["file"], row["doc_type"])
        rows.append(row)

    return rows


def emit_section(title: str, rows: list[dict]) -> str:
    if not rows:
        return f"## {title}\n\nNone.\n"

    out = [f"## {title}\n"]

    for row in rows:
        out.append(
            f"### Result {row['rank']} — `{row['file']}`\n\n"
            f"- Source ID: `{row['source_id']}`\n"
            f"- Doc type: `{row['doc_type']}`\n"
            f"- Score: `{row['score']}`\n"
            f"- Rerank score: `{row['rerank']}`\n\n"
            f"```text\n{row['text']}\n```\n"
        )

    return "\n".join(out)


def build_pack(rows: list[dict], query: str) -> str:
    buckets = {
        "runtime_chains": [],
        "human_context": [],
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
            f"Query: `{query}`",
            "Purpose: compact retrieval pack for investigation synthesis. Use this before opening raw Lua.",
            emit_section("Runtime Chains", buckets["runtime_chains"]),
            emit_section("Human Context", buckets["human_context"]),
            emit_section("Subsystem Docs", buckets["subsystem_docs"]),
            emit_section("Doctrine / Project Memory", buckets["doctrine"]),
            emit_section("File Topology", buckets["file_topology"]),
            emit_section("Other Retrieved Evidence", buckets["other"]),
        ]
    )


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
        help="Defaults to investigations/context_pack.md",
    )
    parser.add_argument("--query", required=True)
    parser.add_argument("--text-limit", type=int, default=2500)

    args = parser.parse_args()

    workspace = args.workspace
    query_results = args.query_results or workspace / "manifests/semantic/qdrant_query_results.md"
    out_path = args.out or workspace / "investigations/context_pack.md"

    if not query_results.exists():
        raise FileNotFoundError(f"Query results not found: {query_results}")

    markdown = query_results.read_text(encoding="utf-8", errors="replace")
    rows = parse_results(markdown, args.text_limit)

    if not rows:
        raise RuntimeError(f"No Qdrant results found in: {query_results}")

    pack = build_pack(rows, args.query)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(pack, encoding="utf-8")

    print(f"[OK] Wrote context pack: {out_path}")
    print(f"[OK] Results included: {len(rows)}")


if __name__ == "__main__":
    main()