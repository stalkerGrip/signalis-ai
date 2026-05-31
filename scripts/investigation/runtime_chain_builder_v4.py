from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

def is_structural_step(step: Dict[str, Any]) -> bool:
    node_type = str(step.get("node_type") or "").lower()
    sid = str(step.get("id") or "").lower()

    return (
        node_type in {"file", "plugin", "subsystem", "realm", "timer_class", "event_class"}
        or sid.startswith("file:")
        or sid.startswith("plugin:")
        or sid.startswith("subsystem:")
        or sid.startswith("realm:")
    )


def semantic_needles_for_step(step: Dict[str, Any]) -> List[str]:
    text = blob(step)

    known = [
        "ItemDataChanged",
        "InventoryItemDataChanged",
        "InventoryDataChanged",
        "nutInventoryAdd",
        "nutInventoryRemove",
        "nutInventoryData",
        "nutInventoryInit",
        "invData",
        "setData",
        "syncItemAdded",
        "populateItems",
        "vendorSPrice",
        "vendorQty",
        "vendorMQty",
        "vendorBPrice",
        "nutTransferItem",
        "HandleItemTransferRequest",
    ]

    found = [x for x in known if x.lower() in text.lower()]
    return found[:5]

def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_md(path: Path, report: Dict[str, Any]) -> None:
    lines: List[str] = []
    chain = report.get("runtime_chain", {})

    lines.append(f"# Runtime Chain Builder V4: {report.get('title')}")
    lines.append("")
    lines.append(f"- Schema: `{report['schema']}`")
    lines.append(f"- Chain schema: `{chain.get('schema')}`")
    lines.append(f"- Confidence: **{chain.get('confidence')}**")
    lines.append(f"- Score: **{chain.get('score')}**")
    lines.append(f"- Path mode: `{chain.get('path_mode')}`")
    lines.append("")

    lines.append("## Missing categories")
    missing = chain.get("missing_categories") or []
    if missing:
        for item in missing:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Runtime steps")
    for i, step in enumerate(chain.get("steps", []), start=1):
        lines.append(f"### {i}. {step.get('label') or step.get('id')}")
        lines.append("")
        lines.append(f"- Node type: `{step.get('node_type')}`")
        lines.append(f"- Realm: `{step.get('realm')}`")
        lines.append(f"- ID: `{step.get('id')}`")
        if step.get("file"):
            lines.append(f"- File: `{step.get('file')}`")
        if step.get("validated_evidence"):
            lines.append("- Validated evidence: yes")
        lines.append("")

    lines.append("## Causal edges")
    lines.append("")

    lines.append("## Targeted validation request")
    targets = report.get("targeted_validation_request", {}).get("targets", [])
    if targets:
        for target in targets:
            lines.append(f"- `{target.get('file')}` :: `{target.get('needle')}`")
            lines.append(f"  - reason: {target.get('reason')}")
    else:
        lines.append("- none")
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def blob(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def flatten_records(data: Any) -> List[Dict[str, Any]]:
    records: List[Dict[str, Any]] = []

    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            if any(k in obj for k in ("source_file", "file", "path", "text", "fragment", "source_text", "line", "line_start")):
                records.append(obj)
            for v in obj.values():
                if isinstance(v, (dict, list)):
                    walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(data)
    return records


def evidence_key(record: Dict[str, Any]) -> str:
    return " ".join(
        str(record.get(k) or "")
        for k in ("source_file", "file", "path", "text", "fragment", "source_text", "label", "summary")
    ).lower().replace("\\", "/")


def load_evidence(path: Optional[Path]) -> List[Dict[str, Any]]:
    if not path or not path.exists():
        return []
    return flatten_records(load_json(path))


def attach_validated_evidence(chain: Dict[str, Any], evidence: List[Dict[str, Any]]) -> Dict[str, Any]:
    evidence_blobs = [(evidence_key(e), e) for e in evidence]

    for step in chain.get("steps", []):
        step_blob = blob(step).lower().replace("\\", "/")
        matches = []

        for e_blob, record in evidence_blobs:
            if not e_blob:
                continue

            matched = False

            for token in extract_tokens(step_blob):
                if len(token) >= 5 and token in e_blob:
                    matched = True
                    break

            if matched:
                matches.append(record)

        if matches:
            step["validated_evidence"] = True
            step["validated_evidence_count"] = len(matches)
            step["validated_evidence_refs"] = [
                {
                    "source_file": m.get("source_file") or m.get("file") or m.get("path"),
                    "line_start": m.get("line_start") or m.get("line"),
                    "line_end": m.get("line_end") or m.get("line"),
                    "label": m.get("label") or m.get("summary") or m.get("symbol"),
                }
                for m in matches[:5]
            ]
        else:
            step["validated_evidence"] = False
            step["validated_evidence_count"] = 0
            step["validated_evidence_refs"] = []

    validated_steps = sum(1 for s in chain.get("steps", []) if s.get("validated_evidence"))
    total_steps = len(chain.get("steps", []))

    chain["validated_step_count"] = validated_steps
    chain["total_step_count"] = total_steps
    chain["validation_coverage"] = round(validated_steps / total_steps, 4) if total_steps else 0.0

    if chain.get("path_mode") == "directed" and chain["validation_coverage"] >= 0.5 and not chain.get("missing_categories"):
        chain["confidence"] = "high"
    elif chain["validation_coverage"] >= 0.3 and not chain.get("missing_categories"):
        chain["confidence"] = "medium"

    return chain


def extract_tokens(text: str) -> List[str]:
    return sorted(set(re.findall(r"[a-zA-Z0-9_./:-]+", text.lower())))


def file_from_step(step: Dict[str, Any]) -> Optional[str]:
    raw = step.get("raw") or {}
    for value in (
        step.get("file"),
        step.get("path"),
        step.get("source_file"),
        raw.get("file"),
        raw.get("path"),
        raw.get("source_file"),
    ):
        if value:
            return str(value).replace("\\", "/")

    sid = str(step.get("id") or "")
    if sid.startswith("file:"):
        return sid.removeprefix("file:").replace("\\", "/")

    return None


def needle_from_step(step: Dict[str, Any]) -> str:
    label = str(step.get("label") or step.get("id") or "")
    sid = str(step.get("id") or "")

    for token in (
        "ItemDataChanged",
        "InventoryItemDataChanged",
        "InventoryDataChanged",
        "nutInventoryAdd",
        "nutInventoryData",
        "invData",
        "setData",
        "populateItems",
        "vendorSPrice",
        "nutTransferItem",
    ):
        if token.lower() in (label + " " + sid).lower():
            return token

    clean = re.sub(r"^(file:|hook:|netmsg:|netop:|listener:|emitter:)", "", sid)
    clean = clean.split(":")[0]
    clean = clean.split("@")[0]
    clean = clean.strip()

    return clean[:120] if clean else label[:120]


def build_targeted_validation(chain: Dict[str, Any]) -> Dict[str, Any]:
    targets: List[Dict[str, Any]] = []

    for step in chain.get("steps", []):
        if step.get("validated_evidence"):
            continue

        if is_structural_step(step):
            continue

        file_path = file_from_step(step)
        if not file_path:
            continue

        needles = semantic_needles_for_step(step)
        if not needles:
            continue

        targets.append({
            "path": file_path,
            "file": file_path,
            "needle": needles[0],
            "needles": needles,
            "reason": "Validate unconfirmed semantic runtime-chain step.",
            "step_id": step.get("id"),
        })

    deduped = []
    seen = set()

    for target in targets:
        key = (target.get("path"), tuple(target.get("needles", [])))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(target)

    return {
        "schema": "targeted_validation_request.v2",
        "targets": deduped[:40],
    }


def select_best_chain(pathfinder: Dict[str, Any]) -> Dict[str, Any]:
    best = pathfinder.get("best_chain")
    if best:
        return best

    paths = pathfinder.get("paths") or []
    if not paths:
        return {
            "schema": "runtime_chain.v2",
            "confidence": "low",
            "score": 0.0,
            "steps": [],
            "causal_edges": [],
            "missing_categories": ["runtime path"],
        }

    paths = sorted(paths, key=lambda p: p.get("score", 0), reverse=True)
    p = paths[0]

    return {
        "schema": "runtime_chain.v2",
        "title": pathfinder.get("title"),
        "confidence": p.get("confidence"),
        "score": p.get("score"),
        "path_mode": p.get("mode"),
        "path_length": p.get("length"),
        "missing_categories": p.get("missing_categories", []),
        "score_reasons": p.get("score_reasons", []),
        "steps": [
            {
                "id": n.get("id"),
                "node_type": n.get("type") or n.get("node_type") or "unknown",
                "label": n.get("label") or n.get("name") or n.get("id"),
                "realm": n.get("realm") or "unknown",
                "file": n.get("file") or n.get("path") or n.get("source_file"),
                "degree": n.get("degree"),
                "raw": n,
            }
            for n in p.get("nodes", [])
        ],
        "causal_edges": p.get("edges", []),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Runtime Chain Builder V4: merge topology pathfinder with validated evidence.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--pathfinder", required=True, type=Path)
    parser.add_argument("--validated-evidence", type=Path, default=None)
    parser.add_argument("--runtime-facts", type=Path, default=None)
    parser.add_argument("--targeted-validation", type=Path, default=None)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument("--out-targeted-validation", required=True, type=Path)

    args = parser.parse_args()

    pathfinder = load_json(args.pathfinder)

    evidence: List[Dict[str, Any]] = []
    evidence.extend(load_evidence(args.validated_evidence))
    evidence.extend(load_evidence(args.runtime_facts))
    evidence.extend(load_evidence(args.targeted_validation))

    chain = select_best_chain(pathfinder)
    chain["title"] = args.title
    chain = attach_validated_evidence(chain, evidence)

    targeted_request = build_targeted_validation(chain)
    write_json(args.out_targeted_validation, targeted_request)

    report = {
        "schema": "runtime_chain_builder_v4_report.v1",
        "title": args.title,
        "source_pathfinder": str(args.pathfinder),
        "evidence_records_loaded": len(evidence),
        "runtime_chain": chain,
        "targeted_validation_request": targeted_request,
    }

    write_json(args.out_json, report)
    write_md(args.out_md, report)

    print(f"Wrote V4 report JSON: {args.out_json}")
    print(f"Wrote V4 report MD:   {args.out_md}")
    print(f"Wrote targeted validation request: {args.out_targeted_validation}")
    print(f"Confidence: {chain.get('confidence')}")
    print(f"Score: {chain.get('score')}")
    print(f"Validation coverage: {chain.get('validation_coverage')}")
    print(f"Missing categories: {', '.join(chain.get('missing_categories', [])) or 'none'}")
    print(f"Validation targets: {len(targeted_request.get('targets', []))}")


if __name__ == "__main__":
    main()