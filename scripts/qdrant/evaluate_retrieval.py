#!/usr/bin/env python3
"""
SIGNALIS AI — Retrieval Evaluation V1

Purpose:
    Evaluate Qdrant/retrieval quality against config/retrieval_queries.yaml.

Recommended location:
    scripts/qdrant/evaluate_retrieval.py

Two usage modes:

1) Existing results mode:
    python scripts/qdrant/evaluate_retrieval.py \
        --queries config/retrieval_queries.yaml \
        --results path/to/results.json \
        --out reports/retrieval_eval

2) Command mode:
    python scripts/qdrant/evaluate_retrieval.py \
        --queries config/retrieval_queries.yaml \
        --workspace E:/signalis_ai \
        --query-script scripts/qdrant/query_qdrant.py \
        --out reports/retrieval_eval

Command mode expects query_qdrant.py to support:
    --workspace <path>
    --query <text>
    --top-k <n>
    --write

The evaluator is intentionally text-based. It does not treat retrieval output as truth.
It checks whether expected subsystems/plugins/hooks/network messages/files appear in top-K text.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: PyYAML\n"
        "Install with:\n"
        "  pip install pyyaml\n"
    ) from exc


CATEGORY_KEYS = {
    "subsystems": ("subsystem_weight", 3),
    "plugins": ("plugin_weight", 3),
    "hooks": ("hook_weight", 2),
    "network_messages": ("network_weight", 2),
    "files": ("file_weight", 1),
}


@dataclass
class CategoryScore:
    expected: list[str]
    matched: list[str]
    missing: list[str]
    score: float


@dataclass
class QueryScore:
    id: str
    query: str
    intent: str
    priority: str
    top_k: int
    categories: dict[str, CategoryScore]
    overall: float
    passed: bool


def normalize_text(value: str) -> str:
    """Normalize for tolerant substring matching."""
    value = value.replace("\\", "/")
    value = value.lower()
    value = re.sub(r"[^a-z0-9_./:-]+", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def candidate_patterns(term: str) -> list[str]:
    """
    Build tolerant match candidates.

    Examples:
      inventorySetPanelStatus should match:
        inventorysetpanelstatus
        inventory set panel status
        netmsg:netstream:inventorySetPanelStatus

      plugins/vendor/cl_networking.lua should match slash/backslash variants.
    """
    raw = term.strip()
    normalized = normalize_text(raw)

    # camelCase / PascalCase split.
    spaced = re.sub(r"(?<!^)(?=[A-Z])", " ", raw)
    spaced = normalize_text(spaced)

    # Path basename is useful when results omit full path.
    basename = normalize_text(Path(raw.replace("\\", "/")).name)

    candidates = {normalized, spaced, basename}

    # Hook/network IDs can appear with prefixes.
    compact = re.sub(r"[^a-z0-9]+", "", normalized)
    if compact:
        candidates.add(compact)

    return [c for c in candidates if c]


def text_contains_term(text_norm: str, text_compact: str, term: str) -> bool:
    for pattern in candidate_patterns(term):
        if not pattern:
            continue

        compact_pattern = re.sub(r"[^a-z0-9]+", "", pattern)

        if "/" in pattern or "." in pattern:
            if pattern in text_norm:
                return True
            if Path(pattern).name and Path(pattern).name in text_norm:
                return True
        elif pattern in text_norm:
            return True

        if compact_pattern and compact_pattern in text_compact:
            return True

    return False


def flatten_result_text(value: Any) -> str:
    """
    Convert unknown retrieval output structures into searchable text.

    Supports:
      - list[str]
      - list[dict]
      - dict with results/items/documents/matches
      - arbitrary nested JSON
      - markdown/text files
    """
    parts: list[str] = []

    def walk(obj: Any) -> None:
        if obj is None:
            return
        if isinstance(obj, str):
            parts.append(obj)
        elif isinstance(obj, (int, float, bool)):
            parts.append(str(obj))
        elif isinstance(obj, dict):
            # Prefer common text-bearing fields first.
            for key in (
                "title",
                "id",
                "doc_id",
                "source",
                "path",
                "file",
                "plugin",
                "subsystem",
                "text",
                "content",
                "summary",
                "page_content",
                "payload",
            ):
                if key in obj:
                    walk(obj[key])
            for key, val in obj.items():
                if key not in {
                    "title",
                    "id",
                    "doc_id",
                    "source",
                    "path",
                    "file",
                    "plugin",
                    "subsystem",
                    "text",
                    "content",
                    "summary",
                    "page_content",
                    "payload",
                }:
                    walk(val)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)
        else:
            parts.append(str(obj))

    walk(value)
    return "\n".join(parts)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    if "queries" not in data or not isinstance(data["queries"], list):
        raise ValueError(f"YAML must contain queries: list: {path}")
    return data


def load_results(path: Path) -> Any:
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return text


def index_results_by_query(results: Any) -> dict[str, Any]:
    """
    Best-effort index for externally produced result files.

    Accepted shapes:
      { "<query_id>": ... }
      { "results": [{ "id": "...", "results": [...] }, ...] }
      [{ "id": "...", "results": [...] }, ...]
    """
    if isinstance(results, dict):
        if "results" in results and isinstance(results["results"], list):
            return index_results_by_query(results["results"])
        return results

    if isinstance(results, list):
        out: dict[str, Any] = {}
        for item in results:
            if isinstance(item, dict):
                qid = item.get("id") or item.get("query_id") or item.get("name")
                if qid:
                    out[str(qid)] = item
        return out

    return {"__all__": results}


def run_query_command(
    query_script: Path,
    workspace: Path,
    query: str,
    top_k: int,
    extra_args: list[str],
) -> str:
    cmd = [
        sys.executable,
        str(query_script),
        "--workspace",
        str(workspace),
        "--query",
        query,
        "--top-k",
        str(top_k),
        "--write",
        *extra_args,
    ]

    proc = subprocess.run(
        cmd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    return proc.stdout


def score_category(expected: Iterable[str], corpus_text: str) -> CategoryScore:
    expected_list = [str(x) for x in expected if str(x).strip()]
    text_norm = normalize_text(corpus_text)
    text_compact = re.sub(r"[^a-z0-9]+", "", text_norm)

    matched: list[str] = []
    missing: list[str] = []

    for item in expected_list:
        if text_contains_term(text_norm, text_compact, item):
            matched.append(item)
        else:
            missing.append(item)

    score = 1.0 if not expected_list else len(matched) / len(expected_list)

    return CategoryScore(
        expected=expected_list,
        matched=matched,
        missing=missing,
        score=score,
    )


def score_query(
    query_cfg: dict[str, Any],
    corpus_text: str,
    weights: dict[str, int],
    top_k: int,
    pass_threshold: float,
) -> QueryScore:
    expect = query_cfg.get("expect") or {}
    categories: dict[str, CategoryScore] = {}

    weighted_sum = 0.0
    weight_total = 0

    for category, (weight_key, default_weight) in CATEGORY_KEYS.items():
        expected_values = expect.get(category, [])
        if not expected_values:
            continue

        category_score = score_category(expected_values, corpus_text)
        categories[category] = category_score

        weight = int(weights.get(weight_key, default_weight))
        weighted_sum += category_score.score * weight
        weight_total += weight

    overall = 1.0 if weight_total == 0 else weighted_sum / weight_total

    return QueryScore(
        id=str(query_cfg.get("id", "unknown")),
        query=str(query_cfg.get("query", "")),
        intent=str(query_cfg.get("intent", "")),
        priority=str(query_cfg.get("priority", "")),
        top_k=top_k,
        categories=categories,
        overall=overall,
        passed=overall >= pass_threshold,
    )


def score_to_dict(score: QueryScore) -> dict[str, Any]:
    data = asdict(score)
    # dataclasses nested dict is okay, but keep category ordering stable.
    data["categories"] = {
        key: asdict(value) for key, value in score.categories.items()
    }
    return data


def format_markdown(scores: list[QueryScore], metadata: dict[str, Any]) -> str:
    passed = sum(1 for s in scores if s.passed)
    total = len(scores)
    avg = sum(s.overall for s in scores) / total if total else 0.0

    lines: list[str] = []
    lines.append("# SIGNALIS AI — Retrieval Evaluation Report")
    lines.append("")
    lines.append(f"- Generated: `{metadata['generated_at']}`")
    lines.append(f"- Queries: **{total}**")
    lines.append(f"- Passed: **{passed}/{total}**")
    lines.append(f"- Average score: **{avg:.3f}**")
    lines.append(f"- Pass threshold: **{metadata['pass_threshold']:.2f}**")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append("| ID | Priority | Intent | Score | Result |")
    lines.append("|---|---:|---|---:|---|")
    for s in scores:
        result = "PASS" if s.passed else "FAIL"
        lines.append(f"| `{s.id}` | {s.priority} | `{s.intent}` | {s.overall:.3f} | **{result}** |")

    lines.append("")
    lines.append("## Details")
    lines.append("")

    for s in scores:
        lines.append(f"### {s.id}")
        lines.append("")
        lines.append(f"Query: `{s.query}`")
        lines.append("")
        lines.append(f"Overall: **{s.overall:.3f}** — {'PASS' if s.passed else 'FAIL'}")
        lines.append("")
        for category, category_score in s.categories.items():
            lines.append(f"#### {category}")
            lines.append("")
            lines.append(f"- Score: `{category_score.score:.3f}`")
            if category_score.matched:
                lines.append(f"- Matched: `{', '.join(category_score.matched)}`")
            if category_score.missing:
                lines.append(f"- Missing: `{', '.join(category_score.missing)}`")
            lines.append("")
    return "\n".join(lines)


def print_console_summary(scores: list[QueryScore]) -> None:
    passed = sum(1 for s in scores if s.passed)
    total = len(scores)
    avg = sum(s.overall for s in scores) / total if total else 0.0

    print("=" * 72)
    print("SIGNALIS AI — Retrieval Evaluation")
    print(f"Queries: {total} | Passed: {passed}/{total} | Average: {avg:.3f}")
    print("=" * 72)

    for s in scores:
        print(f"{s.id}: {s.overall:.3f} {'PASS' if s.passed else 'FAIL'}")
        for category, category_score in s.categories.items():
            missing = f" | missing: {', '.join(category_score.missing)}" if category_score.missing else ""
            print(f"  {category}: {category_score.score:.3f}{missing}")
        print("-" * 72)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate SIGNALIS retrieval quality.")

    parser.add_argument(
        "--queries",
        type=Path,
        default=Path("config/retrieval_queries.yaml"),
        help="Path to retrieval_queries.yaml.",
    )
    parser.add_argument(
        "--results",
        type=Path,
        default=None,
        help="Optional JSON/MD/TXT results file to evaluate instead of running query command.",
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Workspace path for command mode.",
    )
    parser.add_argument(
        "--query-script",
        type=Path,
        default=Path("scripts/qdrant/query_qdrant.py"),
        help="Path to query_qdrant.py for command mode.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("reports/retrieval_eval"),
        help="Output directory for latest.json/latest.md.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Override top_k from YAML defaults.",
    )
    parser.add_argument(
        "--pass-threshold",
        type=float,
        default=0.60,
        help="Overall score needed for PASS.",
    )
    parser.add_argument(
        "--only",
        nargs="*",
        default=None,
        help="Optional query IDs to run/evaluate.",
    )
    parser.add_argument(
        "--extra-query-arg",
        action="append",
        default=[],
        help="Extra argument passed to query_qdrant.py. Can be repeated.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    cfg = load_yaml(args.queries)
    defaults = cfg.get("defaults") or {}
    weights = defaults.get("scoring") or {}

    top_k = args.top_k or int(defaults.get("top_k", 10))
    query_cfgs = cfg["queries"]

    if args.only:
        wanted = set(args.only)
        query_cfgs = [q for q in query_cfgs if str(q.get("id")) in wanted]

    if not query_cfgs:
        raise SystemExit("No queries selected.")

    result_index: dict[str, Any] = {}
    all_results_text = ""

    if args.results:
        loaded = load_results(args.results)
        result_index = index_results_by_query(loaded)
        all_results_text = flatten_result_text(loaded)
    elif not args.workspace:
        raise SystemExit(
            "Provide either --results <file> or --workspace <path> for command mode."
        )

    scores: list[QueryScore] = []
    raw_outputs: dict[str, str] = {}

    for query_cfg in query_cfgs:
        qid = str(query_cfg.get("id"))
        query = str(query_cfg.get("query", ""))

        if args.results:
            result_obj = result_index.get(qid, result_index.get("__all__", all_results_text))
            corpus_text = flatten_result_text(result_obj)
        else:
            output = run_query_command(
                query_script=args.query_script,
                workspace=args.workspace,
                query=query,
                top_k=top_k,
                extra_args=args.extra_query_arg,
            )
            raw_outputs[qid] = output
            corpus_text = output

        scores.append(
            score_query(
                query_cfg=query_cfg,
                corpus_text=corpus_text,
                weights=weights,
                top_k=top_k,
                pass_threshold=args.pass_threshold,
            )
        )

    generated_at = datetime.now().isoformat(timespec="seconds")
    metadata = {
        "generated_at": generated_at,
        "queries_file": str(args.queries),
        "results_file": str(args.results) if args.results else None,
        "workspace": str(args.workspace) if args.workspace else None,
        "top_k": top_k,
        "pass_threshold": args.pass_threshold,
    }

    output = {
        "metadata": metadata,
        "summary": {
            "total": len(scores),
            "passed": sum(1 for s in scores if s.passed),
            "average_score": sum(s.overall for s in scores) / len(scores) if scores else 0.0,
        },
        "scores": [score_to_dict(s) for s in scores],
    }

    args.out.mkdir(parents=True, exist_ok=True)

    json_path = args.out / "latest.json"
    md_path = args.out / "latest.md"

    json_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(format_markdown(scores, metadata), encoding="utf-8")

    if raw_outputs:
        raw_dir = args.out / "raw"
        raw_dir.mkdir(exist_ok=True)
        for qid, text in raw_outputs.items():
            (raw_dir / f"{qid}.txt").write_text(text, encoding="utf-8", errors="replace")

    print_console_summary(scores)
    print(f"\nWrote: {json_path}")
    print(f"Wrote: {md_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
