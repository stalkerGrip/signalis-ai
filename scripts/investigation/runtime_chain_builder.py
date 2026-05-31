from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict, deque
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from scripts.investigation.runtime_chain_scorer import score_chain


RUNTIME_TERMS = [
    "hook.Run",
    "netstream",
    "net.Receive",
    "net.Start",
    "util.AddNetworkString",
    "setData",
    "sync",
    "ItemDataChanged",
    "InventoryDataChanged",
    "populateItems",
    "timer.",
    "vgui",
]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_md(path: Path, chain: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: List[str] = []
    lines.append(f"# Runtime Chain Candidate: {chain['title']}")
    lines.append("")
    lines.append(f"- Schema: `{chain['schema']}`")
    lines.append(f"- Confidence: **{chain['confidence']}**")
    lines.append(f"- Score: **{chain['score']}**")
    lines.append(f"- Steps: **{len(chain.get('steps', []))}**")
    lines.append("")

    lines.append("## Missing causal steps")
    missing = chain.get("missing_steps") or []
    if missing:
        for item in missing:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Score reasons")
    for reason in chain.get("score_reasons", []):
        lines.append(f"- {reason}")
    lines.append("")

    lines.append("## Runtime chain")
    for i, step in enumerate(chain.get("steps", []), start=1):
        label = step.get("label") or step.get("summary") or step.get("text") or "runtime step"
        lines.append(f"### {i}. {label}")
        lines.append("")
        lines.append(f"- Type: `{step.get('step_type', 'unknown')}`")
        lines.append(f"- Realm: `{step.get('realm', 'unknown')}`")
        if step.get("source_file"):
            lines.append(f"- Source: `{step['source_file']}`")
        if step.get("line_start") is not None:
            line_end = step.get("line_end", step.get("line_start"))
            lines.append(f"- Lines: `{step['line_start']}-{line_end}`")
        if step.get("evidence_id"):
            lines.append(f"- Evidence ID: `{step['evidence_id']}`")
        if step.get("score") is not None:
            lines.append(f"- Step score: `{step['score']}`")
        text = step.get("text") or step.get("fragment") or step.get("source_text")
        if text:
            safe = str(text).strip()
            if len(safe) > 1200:
                safe = safe[:1200] + "\n..."
            lines.append("")
            lines.append("```text")
            lines.append(safe)
            lines.append("```")
        lines.append("")

    lines.append("## Targeted validation request")
    req = chain.get("targeted_validation_request") or {}
    if req.get("targets"):
        for target in req["targets"]:
            lines.append(f"- `{target.get('file', 'unknown')}` :: {target.get('needle', '')}")
    else:
        lines.append("- none")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def load_workspace_config(workspace: Path, workspace_config: Optional[Path]) -> Dict[str, Any]:
    config_path = workspace_config or workspace / "config" / "workspace.yaml"
    if not config_path.exists():
        return {
            "workspace": str(workspace),
            "workspace_config": str(config_path),
            "source_roots": [],
            "warning": "workspace.yaml not found; source roots unavailable",
        }

    try:
        import yaml  # type: ignore
    except Exception as exc:
        raise RuntimeError(
            "PyYAML is required to read config/workspace.yaml. Install with: pip install pyyaml"
        ) from exc

    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}

    roots: List[str] = []
    for key in ("source_roots", "sourceRoots", "raw_source_roots", "rawSourceRoots"):
        value = data.get(key)
        if isinstance(value, list):
            roots.extend(str(v) for v in value)
        elif isinstance(value, str):
            roots.append(value)

    if isinstance(data.get("sources"), list):
        for src in data["sources"]:
            if isinstance(src, dict):
                for key in ("root", "path", "source_root"):
                    if src.get(key):
                        roots.append(str(src[key]))

    resolved_roots = []
    for root in roots:
        p = Path(root)
        if not p.is_absolute():
            p = (config_path.parent / p).resolve()
        resolved_roots.append(str(p))

    return {
        "workspace": str(workspace),
        "workspace_config": str(config_path),
        "source_roots": sorted(set(resolved_roots)),
    }


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def infer_realm(file_path: str, text: str = "") -> str:
    name = Path(file_path.replace("\\", "/")).name.lower()
    if name.startswith("sv_"):
        return "server"
    if name.startswith("cl_"):
        return "client"
    if name.startswith("sh_"):
        return "shared"
    if "if SERVER" in text or "SERVER then" in text:
        return "server"
    if "if CLIENT" in text or "CLIENT then" in text:
        return "client"
    return "unknown"


def flatten_records(data: Any) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []

    def walk(obj: Any, parent_key: str = "") -> None:
        if isinstance(obj, dict):
            if any(k in obj for k in ("fragment", "source_text", "text", "file", "source_file", "path", "line", "line_start")):
                records.append(obj)
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    walk(value, key)
        elif isinstance(obj, list):
            for item in obj:
                walk(item, parent_key)

    walk(data)
    return records


def record_to_step(record: Dict[str, Any], source_kind: str, index: int) -> Dict[str, Any]:
    file_path = (
        record.get("source_file")
        or record.get("file")
        or record.get("path")
        or record.get("relative_path")
        or ""
    )

    text = (
        record.get("fragment")
        or record.get("source_text")
        or record.get("text")
        or record.get("summary")
        or record.get("content")
        or ""
    )

    label = (
        record.get("label")
        or record.get("title")
        or record.get("symbol")
        or record.get("function")
        or first_runtime_label(str(text))
        or Path(str(file_path)).name
        or f"{source_kind} step {index}"
    )

    line_start = record.get("line_start", record.get("line"))
    line_end = record.get("line_end", line_start)

    step = {
        "id": f"{source_kind}:{index}",
        "evidence_id": record.get("id") or record.get("evidence_id") or f"{source_kind}:{index}",
        "step_type": source_kind,
        "label": normalize_text(label),
        "source_file": str(file_path).replace("\\", "/") if file_path else None,
        "line_start": line_start,
        "line_end": line_end,
        "realm": record.get("realm") or infer_realm(str(file_path), str(text)),
        "text": str(text).strip(),
        "validated": bool(record.get("validated") or record.get("found") or record.get("is_validated")),
        "targeted_validation": source_kind == "targeted_validation",
        "rank_score": record.get("rank_score") or record.get("score"),
        "raw": record,
    }

    return step


def first_runtime_label(text: str) -> Optional[str]:
    for term in RUNTIME_TERMS:
        if term in text:
            return term
    hook = re.search(r"hook\.Run\s*\(\s*[\"']([^\"']+)[\"']", text)
    if hook:
        return f"hook.Run({hook.group(1)})"
    netstream = re.search(r"netstream\.(Start|Hook)\s*\(([^)]{1,80})", text)
    if netstream:
        return f"netstream.{netstream.group(1)}({netstream.group(2).strip()})"
    net = re.search(r"net\.(Start|Receive)\s*\(\s*[\"']([^\"']+)[\"']", text)
    if net:
        return f"net.{net.group(1)}({net.group(2)})"
    set_data = re.search(r":setData\s*\(\s*[\"']([^\"']+)[\"']", text)
    if set_data:
        return f"setData({set_data.group(1)})"
    return None


def tokenize_query(query: str) -> List[str]:
    return [
        t.lower()
        for t in re.findall(r"[A-Za-z0-9_:.]+", query)
        if len(t) >= 3
    ]


def relevance(step: Dict[str, Any], query_tokens: List[str]) -> float:
    blob = " ".join(
        str(step.get(k) or "")
        for k in ("label", "source_file", "text", "realm", "step_type")
    ).lower()

    score = 0.0
    for token in query_tokens:
        if token in blob:
            score += 1.0

    for term in RUNTIME_TERMS:
        if term.lower() in blob:
            score += 0.5

    if step.get("validated"):
        score += 1.0
    if step.get("targeted_validation"):
        score += 1.25

    return score


def dedupe_steps(steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    output: List[Dict[str, Any]] = []

    for step in steps:
        key = (
            step.get("source_file"),
            step.get("line_start"),
            step.get("line_end"),
            normalize_text(step.get("label")),
        )
        if key in seen:
            continue
        seen.add(key)
        output.append(step)

    return output


def sort_steps(steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    def sort_key(step: Dict[str, Any]) -> Tuple[int, str, int, str]:
        realm_order = {"server": 0, "shared": 1, "client": 2, "unknown": 3}
        source = step.get("source_file") or ""
        line = step.get("line_start")
        try:
            line_int = int(line)
        except Exception:
            line_int = 999999
        return (realm_order.get(str(step.get("realm")).lower(), 3), source, line_int, step.get("label") or "")

    return sorted(steps, key=sort_key)


def build_targeted_validation_request(chain: Dict[str, Any]) -> Dict[str, Any]:
    targets: List[Dict[str, Any]] = []

    for step in chain.get("steps", []):
        file_path = step.get("source_file")
        if not file_path:
            continue

        needles: List[str] = []
        text = step.get("text") or ""
        label = step.get("label") or ""

        for term in RUNTIME_TERMS:
            if term in text or term in label:
                needles.append(term)

        for match in re.findall(r"[A-Za-z_][A-Za-z0-9_]*\s*[:.]?\s*[A-Za-z_][A-Za-z0-9_]*", label):
            if len(match.strip()) >= 4:
                needles.append(match.strip())

        if not needles and label:
            needles.append(label)

        for needle in sorted(set(needles))[:4]:
            targets.append(
                {
                    "file": file_path,
                    "needle": needle,
                    "reason": f"Confirm runtime chain step: {label}",
                }
            )

    return {
        "schema": "targeted_validation_request.v1",
        "targets": targets[:32],
    }


def load_steps_from_optional(path: Optional[Path], kind: str) -> List[Dict[str, Any]]:
    if not path:
        return []

    if not path.exists():
        return []

    suffix = path.suffix.lower()

    if suffix == ".json":
        data = load_json(path)
        return [record_to_step(record, kind, idx) for idx, record in enumerate(flatten_records(data), start=1)]

    if suffix in {".md", ".txt"}:
        text = path.read_text(encoding="utf-8", errors="replace")
        chunks = []
        for idx, block in enumerate(re.split(r"\n(?=#+\s|\d+\.\s|\-\s)", text), start=1):
            block = block.strip()
            if not block:
                continue
            if any(term in block for term in RUNTIME_TERMS) or kind == "promoted_chain_step":
                chunks.append(
                    {
                        "id": f"{kind}:{idx}",
                        "text": block,
                        "source_file": str(path).replace("\\", "/"),
                        "line_start": None,
                        "line_end": None,
                        "validated": kind == "promoted_chain_step",
                    }
                )

        return [record_to_step(record, kind, idx) for idx, record in enumerate(chunks, start=1)]

    raise ValueError(f"Unsupported input file type for {kind}: {path}")


def load_topology_steps(path: Optional[Path]) -> List[Dict[str, Any]]:
    if not path:
        return []
    data = load_json(path)
    records = flatten_records(data)
    steps = []
    for idx, record in enumerate(records, start=1):
        step = record_to_step(record, "topology_node", idx)
        steps.append(step)
    return steps


def build_runtime_chain(
    *,
    title: str,
    query: str,
    workspace_info: Dict[str, Any],
    validated_evidence: Optional[Path],
    runtime_facts: Optional[Path],
    runtime_topology: Optional[Path],
    targeted_validation: Optional[Path],
    promoted_chain: Optional[Path],
    max_steps: int,
) -> Dict[str, Any]:
    query_tokens = tokenize_query(query)

    all_steps: List[Dict[str, Any]] = []
    all_steps.extend(load_steps_from_optional(validated_evidence, "source_evidence"))
    all_steps.extend(load_steps_from_optional(runtime_facts, "runtime_fact"))
    all_steps.extend(load_topology_steps(runtime_topology))
    all_steps.extend(load_steps_from_optional(targeted_validation, "targeted_validation"))
    all_steps.extend(load_steps_from_optional(promoted_chain, "promoted_chain_step"))

    if not all_steps:
        chain = {
            "schema": "runtime_chain.v1",
            "title": title,
            "query": query,
            "workspace": workspace_info,
            "steps": [],
        }
        scored = score_chain(chain)
        chain.update(
            {
                "score": scored.score,
                "confidence": scored.confidence,
                "score_reasons": scored.reasons,
                "missing_steps": scored.missing_steps,
                "targeted_validation_request": {"schema": "targeted_validation_request.v1", "targets": []},
            }
        )
        return chain

    ranked = sorted(
        all_steps,
        key=lambda s: relevance(s, query_tokens),
        reverse=True,
    )

    ranked = [s for s in ranked if relevance(s, query_tokens) > 0 or s.get("validated") or s.get("targeted_validation")]
    ranked = dedupe_steps(ranked)
    selected = sort_steps(ranked[:max_steps])

    for step in selected:
        step["score"] = relevance(step, query_tokens)

    chain = {
        "schema": "runtime_chain.v1",
        "title": title,
        "query": query,
        "workspace": workspace_info,
        "steps": selected,
    }

    scored = score_chain(chain)
    chain.update(
        {
            "score": scored.score,
            "confidence": scored.confidence,
            "score_reasons": scored.reasons,
            "missing_steps": scored.missing_steps,
        }
    )
    chain["targeted_validation_request"] = build_targeted_validation_request(chain)
    return chain


def main() -> None:
    parser = argparse.ArgumentParser(description="Build general runtime chain candidate from validated investigation artifacts.")
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--workspace-config", type=Path, default=None)
    parser.add_argument("--title", required=True)
    parser.add_argument("--query", required=True)
    parser.add_argument("--validated-evidence", type=Path, default=None)
    parser.add_argument("--runtime-facts", type=Path, default=None)
    parser.add_argument("--runtime-topology", type=Path, default=None)
    parser.add_argument("--targeted-validation", type=Path, default=None)
    parser.add_argument("--promoted-chain", type=Path, default=None)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--max-steps", type=int, default=24)

    args = parser.parse_args()

    workspace = args.workspace.resolve()
    workspace_info = load_workspace_config(workspace, args.workspace_config)

    chain = build_runtime_chain(
        title=args.title,
        query=args.query,
        workspace_info=workspace_info,
        validated_evidence=args.validated_evidence,
        runtime_facts=args.runtime_facts,
        runtime_topology=args.runtime_topology,
        targeted_validation=args.targeted_validation,
        promoted_chain=args.promoted_chain,
        max_steps=args.max_steps,
    )

    write_json(args.out_json, chain)
    write_md(args.out_md, chain)

    print(f"Wrote runtime chain JSON: {args.out_json}")
    print(f"Wrote runtime chain MD:   {args.out_md}")
    print(f"Confidence: {chain['confidence']}")
    print(f"Score: {chain['score']}")
    print("Missing steps:")
    if chain.get("missing_steps"):
        for item in chain["missing_steps"]:
            print(f"  - {item}")
    else:
        print("  none")


if __name__ == "__main__":
    main()