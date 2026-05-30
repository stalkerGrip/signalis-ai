#!/usr/bin/env python3
"""
SIGNALIS AI — Runtime Fact Extraction V1

Purpose:
  Convert deduplicated validation evidence into explicit runtime facts.

Input:
  investigations/validation/*_validation_deduped.json

Output:
  *_runtime_facts.json
  *_runtime_facts.md

Usage:
  python -m scripts.qdrant.extract_runtime_facts `
    --deduped investigations/validation/vendor_stale_price_label_after_purchase_validation_deduped.json
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class RuntimeFact:
    fact_type: str
    target: str
    file: str
    realm: str
    line_start: int
    line_end: int
    confidence: str
    evidence_score: int
    evidence_classification: str
    details: dict[str, Any]
    snippet: str


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def strip_line_numbers(snippet: str) -> str:
    lines: list[str] = []
    for raw in snippet.splitlines():
        line = re.sub(r"^\s*\d+\s*:\s*", "", raw)
        lines.append(line)
    return "\n".join(lines)


def clean(value: str) -> str:
    return value.strip().strip('"').strip("'")


def infer_file_realm(file_path: str, fallback: str) -> str:
    path = file_path.replace("\\", "/").lower()
    name = path.split("/")[-1]

    if name.startswith("sv_") or "/server/" in path:
        return "server"
    if name.startswith("cl_") or "/client/" in path or "/derma/" in path:
        return "client"
    if name.startswith("sh_"):
        return "shared"
    if "/entities/entities/" in path and path.endswith("/init.lua"):
        return "server"

    return fallback or "unknown"


def enclosing_function(snippet: str, line_start: int) -> str | None:
    best_name: str | None = None
    best_line = -1

    patterns = [
        r"function\s+([A-Za-z_][\w\.]*:[A-Za-z_][\w]*)\s*\(",
        r"function\s+([A-Za-z_][\w\.]*)\s*\(",
        r"([A-Za-z_][\w\.]*:[A-Za-z_][\w]*)\s*=\s*function\s*\(",
    ]

    for raw in snippet.splitlines():
        match = re.match(r"^\s*(\d+)\s*:\s*(.*)$", raw)
        if match:
            source_line = int(match.group(1))
            code = match.group(2)
        else:
            source_line = 0
            code = raw

        if source_line > line_start:
            continue

        for pattern in patterns:
            fn = re.search(pattern, code)
            if fn and source_line >= best_line:
                best_name = clean(fn.group(1))
                best_line = source_line

    return best_name


def add_fact(
    facts: list[RuntimeFact],
    evidence: dict[str, Any],
    fact_type: str,
    target: str,
    confidence: str,
    details: dict[str, Any],
) -> None:
    file_path = str(evidence.get("file", ""))
    realm = infer_file_realm(file_path, str(evidence.get("realm", "")))

    facts.append(
        RuntimeFact(
            fact_type=fact_type,
            target=target,
            file=file_path,
            realm=realm,
            line_start=int(evidence.get("line_start", 0)),
            line_end=int(evidence.get("line_end", 0)),
            confidence=confidence,
            evidence_score=int(evidence.get("score", 0)),
            evidence_classification=str(evidence.get("classification", "")),
            details=details,
            snippet=str(evidence.get("snippet", "")),
        )
    )


def extract_from_evidence(evidence: dict[str, Any]) -> list[RuntimeFact]:
    facts: list[RuntimeFact] = []

    snippet_raw = str(evidence.get("snippet", ""))
    snippet = strip_line_numbers(snippet_raw)
    file_path = str(evidence.get("file", ""))
    line_start = int(evidence.get("line_start", 0))
    fn = enclosing_function(snippet_raw, line_start)

    # hook.Run(...)
    for hook in re.findall(r'hook\.Run\s*\(\s*["\']([^"\']+)["\']', snippet):
        add_fact(
            facts,
            evidence,
            "hook_emit",
            clean(hook),
            "high",
            {
                "emitter_function": fn,
                "runtime_meaning": "event emission",
            },
        )

    # hook.Add(...)
    for hook, listener, listener_fn in re.findall(
        r'hook\.Add\s*\(\s*["\']([^"\']+)["\']\s*,\s*([^,\n]+)\s*,\s*([^)]+)\)',
        snippet,
    ):
        add_fact(
            facts,
            evidence,
            "hook_listener",
            clean(hook),
            "high",
            {
                "listener_owner": clean(listener),
                "listener_function": clean(listener_fn),
                "enclosing_function": fn,
            },
        )

    # Simpler hook.Add fallback.
    for hook in re.findall(r'hook\.Add\s*\(\s*["\']([^"\']+)["\']', snippet):
        if not any(f.fact_type == "hook_listener" and f.target == clean(hook) for f in facts):
            add_fact(
                facts,
                evidence,
                "hook_listener",
                clean(hook),
                "high",
                {
                    "enclosing_function": fn,
                },
            )

    # PLUGIN:/SCHEMA:/GM: methods as implicit listeners.
    for owner, hook_name in re.findall(r"function\s+(PLUGIN|SCHEMA|GM)\s*:\s*([A-Za-z_][\w]*)\s*\(", snippet):
        add_fact(
            facts,
            evidence,
            "hook_listener",
            clean(hook_name),
            "medium",
            {
                "listener_owner": owner,
                "listener_function": f"{owner}:{hook_name}",
                "registration_model": "NutScript implicit plugin/schema hook listener",
            },
        )

    # Raw net receive/send.
    for msg in re.findall(r'net\.Receive\s*\(\s*["\']([^"\']+)["\']', snippet):
        add_fact(
            facts,
            evidence,
            "network_receive",
            clean(msg),
            "high",
            {
                "network_api": "gmod_net",
                "receiver_function": fn,
            },
        )

    for msg in re.findall(r'net\.Start\s*\(\s*["\']([^"\']+)["\']', snippet):
        add_fact(
            facts,
            evidence,
            "network_send_start",
            clean(msg),
            "high",
            {
                "network_api": "gmod_net",
                "sender_function": fn,
            },
        )

    # netstream receive/send.
    for msg in re.findall(r'netstream\.Hook\s*\(\s*["\']([^"\']+)["\']', snippet):
        add_fact(
            facts,
            evidence,
            "network_receive",
            clean(msg),
            "high",
            {
                "network_api": "netstream",
                "receiver_function": fn,
            },
        )

    # Server netstream: netstream.Start(client, "message", ...)
    for _recipient, msg in re.findall(
        r'netstream\.Start\s*\(\s*([^,\n]+)\s*,\s*["\']([^"\']+)["\']',
        snippet,
    ):
        add_fact(
            facts,
            evidence,
            "network_send_start",
            clean(msg),
            "medium",
            {
                "network_api": "netstream",
                "recipient_expr": clean(_recipient),
                "sender_function": fn,
            },
        )

    # Client netstream: netstream.Start("message", ...)
    for msg in re.findall(r'netstream\.Start\s*\(\s*["\']([^"\']+)["\']', snippet):
        add_fact(
            facts,
            evidence,
            "network_send_start",
            clean(msg),
            "medium",
            {
                "network_api": "netstream",
                "sender_function": fn,
            },
        )

    # Vendor-specific network handler abstraction.
    for msg in re.findall(r'addNetHandler\s*\(\s*["\']([^"\']+)["\']', snippet):
        add_fact(
            facts,
            evidence,
            "vendor_network_handler",
            clean(msg),
            "high",
            {
                "handler_function": fn,
                "semantic_note": "vendor client-side submessage handler",
            },
        )

    # item:setData(...)
    for key in re.findall(r':setData\s*\(\s*["\']([^"\']+)["\']', snippet):
        add_fact(
            facts,
            evidence,
            "item_data_mutation",
            clean(key),
            "high",
            {
                "mutator_function": fn,
                "runtime_meaning": [
                    "server item metadata mutation",
                    "database persistence unless noSave",
                    "conditional immediate client sync",
                    "future owner/open inventory sync source",
                ],
                "human_validated": True,
            },
        )

    for key in re.findall(r':getData\s*\(\s*["\']([^"\']+)["\']', snippet):
        add_fact(
            facts,
            evidence,
            "item_data_read",
            clean(key),
            "high",
            {
                "reader_function": fn,
            },
        )

    # Entity netvar sync.
    for key in re.findall(r':setNetVar\s*\(\s*["\']([^"\']+)["\']', snippet):
        add_fact(
            facts,
            evidence,
            "entity_netvar_mutation",
            clean(key),
            "high",
            {
                "mutator_function": fn,
                "runtime_meaning": "entity networked variable update",
            },
        )

    # UI refresh calls.
    for call in re.findall(r'[:\.](updatePrice)\s*\(', snippet):
        add_fact(
            facts,
            evidence,
            "ui_refresh_call",
            clean(call),
            "high",
            {
                "caller_function": fn,
                "ui_context": "vendor/inventory presentation",
            },
        )

    for call in re.findall(r'[:\.](SetText)\s*\(', snippet):
        add_fact(
            facts,
            evidence,
            "ui_text_update",
            clean(call),
            "medium",
            {
                "caller_function": fn,
            },
        )

    # Function context fact if no stronger fact was found.
    if not facts and fn:
        add_fact(
            facts,
            evidence,
            "function_context",
            fn,
            "low",
            {
                "note": "no explicit runtime operation extracted; kept as context only",
            },
        )

    # Add source classification context.
    if facts:
        for fact in facts:
            fact.details["source_semantic_target"] = evidence.get("semantic_target")
            fact.details["source_bucket"] = evidence.get("bucket")
            fact.details["source_duplicate_count"] = evidence.get("duplicate_count")

    return facts


def dedupe_facts(facts: list[RuntimeFact]) -> list[RuntimeFact]:
    best: dict[tuple[str, str, str, int], RuntimeFact] = {}

    for fact in facts:
        key = (
            fact.fact_type,
            fact.target,
            fact.file.replace("\\", "/").lower(),
            fact.line_start,
        )

        old = best.get(key)
        if old is None or fact.evidence_score > old.evidence_score:
            best[key] = fact

    return sorted(
        best.values(),
        key=lambda f: (f.evidence_score, f.fact_type, f.target),
        reverse=True,
    )


def summarize(facts: list[RuntimeFact]) -> dict[str, Any]:
    by_type: dict[str, int] = {}
    by_realm: dict[str, int] = {}
    by_file: dict[str, int] = {}

    for fact in facts:
        by_type[fact.fact_type] = by_type.get(fact.fact_type, 0) + 1
        by_realm[fact.realm] = by_realm.get(fact.realm, 0) + 1
        by_file[fact.file] = by_file.get(fact.file, 0) + 1

    return {
        "facts_total": len(facts),
        "by_type": dict(sorted(by_type.items(), key=lambda x: x[1], reverse=True)),
        "by_realm": dict(sorted(by_realm.items(), key=lambda x: x[1], reverse=True)),
        "by_file": dict(sorted(by_file.items(), key=lambda x: x[1], reverse=True)),
    }


def format_md(source: Path, query: str, facts: list[RuntimeFact]) -> str:
    summary = summarize(facts)

    lines: list[str] = []
    lines.append("# SIGNALIS AI — Runtime Facts")
    lines.append("")
    lines.append(f"- Source: `{source}`")
    lines.append(f"- Query: `{query}`")
    lines.append(f"- Facts total: `{summary['facts_total']}`")
    lines.append("")

    lines.append("## Fact Type Counts")
    lines.append("")
    for fact_type, count in summary["by_type"].items():
        lines.append(f"- `{fact_type}`: `{count}`")
    lines.append("")

    lines.append("## Facts")
    lines.append("")

    for idx, fact in enumerate(facts, start=1):
        lines.append(f"### {idx}. `{fact.fact_type}` / `{fact.target}`")
        lines.append("")
        lines.append(f"- File: `{fact.file}`")
        lines.append(f"- Lines: `{fact.line_start}-{fact.line_end}`")
        lines.append(f"- Realm: `{fact.realm}`")
        lines.append(f"- Confidence: `{fact.confidence}`")
        lines.append(f"- Evidence score: `{fact.evidence_score}`")
        lines.append(f"- Evidence classification: `{fact.evidence_classification}`")
        lines.append(f"- Details: `{json.dumps(fact.details, ensure_ascii=False)}`")
        lines.append("")
        lines.append("```lua")
        lines.append(fact.snippet)
        lines.append("```")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deduped", required=True, type=Path)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source = args.deduped.resolve()
    payload = read_json(source)

    all_facts: list[RuntimeFact] = []
    for evidence in payload.get("evidence", []):
        all_facts.extend(extract_from_evidence(evidence))

    facts = dedupe_facts(all_facts)

    out_dir = args.out_dir.resolve() if args.out_dir else source.parent

    stem = source.stem
    for suffix in ["_runtime_facts", "_evidence_graph", "_deduped", "_scored"]:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]

    stem = f"{stem}_runtime_facts"

    json_path = out_dir / f"{stem}.json"
    md_path = out_dir / f"{stem}.md"

    output = {
        "source": str(source),
        "query": payload.get("query"),
        "summary": summarize(facts),
        "facts": [asdict(fact) for fact in facts],
    }

    write_json(json_path, output)
    write_text(md_path, format_md(source, str(payload.get("query", "")), facts))

    print(f"Wrote runtime facts json: {json_path}")
    print(f"Wrote runtime facts report: {md_path}")
    print("")
    print("Summary:")
    print(f"  facts_total: {len(facts)}")
    for fact_type, count in summarize(facts)["by_type"].items():
        print(f"  {fact_type}: {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())