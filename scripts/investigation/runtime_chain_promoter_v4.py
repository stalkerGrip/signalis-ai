from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONFIRMED = "promoted_confirmed_chain"
TOPOLOGY_SUPPORTED = "promoted_topology_supported_chain"
REJECTED = "not_promoted"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_") or "runtime_chain"


def walk_values(obj: Any, wanted: set[str]) -> list[Any]:
    found: list[Any] = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in wanted:
                found.append(v)
            found.extend(walk_values(v, wanted))
    elif isinstance(obj, list):
        for item in obj:
            found.extend(walk_values(item, wanted))
    return found


def first_value(data: dict[str, Any], names: set[str], default: Any = None) -> Any:
    values = walk_values(data, names)
    return values[0] if values else default


def best_float(data: dict[str, Any], names: set[str], default: float = 0.0) -> float:
    vals = []
    for v in walk_values(data, names):
        try:
            vals.append(float(v))
        except Exception:
            pass
    return max(vals) if vals else default


def normalize_missing(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        v = value.strip().lower()
        return [] if v in {"", "none", "missing none", "none detected", "[]"} else [value]
    if isinstance(value, list):
        out = []
        for item in value:
            if str(item).strip().lower() not in {"", "none"}:
                out.append(str(item))
        return out
    return [str(value)]


def extract_gate(data: dict[str, Any]) -> dict[str, Any]:
    confidence = str(first_value(data, {"confidence"}, "unknown")).lower()

    score = best_float(data, {
        "score",
        "promotion_score",
        "chain_score",
        "path_score",
    })

    coverage = best_float(data, {
        "validation_coverage",
        "coverage",
        "source_validation_coverage",
    })

    missing_raw = first_value(data, {
        "missing_categories",
        "missing_semantic_categories",
        "missing_required_categories",
    }, [])

    missing = normalize_missing(missing_raw)

    validation_targets = first_value(data, {"validation_targets", "targeted_validation_targets"}, None)

    return {
        "confidence": confidence,
        "score": score,
        "validation_coverage": coverage,
        "missing_categories": missing,
        "validation_targets": validation_targets,
    }


def decide(gate: dict[str, Any]) -> tuple[str, list[str]]:
    confidence = gate["confidence"]
    score = gate["score"]
    coverage = gate["validation_coverage"]
    missing = gate["missing_categories"]

    if confidence == "high" and coverage >= 1.0 and not missing:
        return CONFIRMED, ["high confidence", "full validation coverage", "missing categories none"]

    if confidence == "medium" and score >= 0.90 and coverage >= 0.60 and not missing:
        return TOPOLOGY_SUPPORTED, [
            "medium confidence",
            "score >= 0.90",
            "validation coverage >= 0.60",
            "missing categories none",
            "promoted as topology-supported, not fully confirmed",
        ]

    return REJECTED, [
        f"confidence={confidence}",
        f"score={score}",
        f"validation_coverage={coverage}",
        f"missing_categories={missing or 'none'}",
    ]


def extract_title(data: dict[str, Any], source: Path) -> str:
    return str(first_value(data, {"title", "chain_title", "name"}, source.stem))


def render_chain(data: dict[str, Any]) -> str:
    chain = first_value(data, {"chain", "nodes", "runtime_chain", "path"}, [])
    if isinstance(chain, dict):
        chain = chain.get("nodes") or chain.get("steps") or chain.get("path") or []
    if not isinstance(chain, list) or not chain:
        return "_No chain node list found._"

    lines = []
    for i, node in enumerate(chain, 1):
        if isinstance(node, dict):
            label = node.get("label") or node.get("name") or node.get("id") or str(node)
            kind = node.get("type") or node.get("node_type")
            realm = node.get("realm")
            meta = ", ".join(x for x in [kind, realm] if x)
            lines.append(f"{i}. `{label}`" + (f" — {meta}" if meta else ""))
        else:
            lines.append(f"{i}. `{node}`")
    return "\n".join(lines)


def render_md(data: dict[str, Any], gate: dict[str, Any], promotion_type: str, reasons: list[str], source: Path) -> str:
    title = extract_title(data, source)
    generated = datetime.now(timezone.utc).isoformat()

    return f"""# Runtime Chain Promotion: {title}

## Promotion Result

- Promotion type: `{promotion_type}`
- Promoted: `{promotion_type != REJECTED}`
- Source artifact: `{source.as_posix()}`
- Generated: `{generated}`

## Gate Values

- Confidence: `{gate["confidence"]}`
- Score: `{gate["score"]}`
- Validation coverage: `{gate["validation_coverage"]}`
- Missing categories: `{gate["missing_categories"] or "none"}`
- Validation targets: `{gate["validation_targets"]}`

## Gate Reasons

{chr(10).join(f"- {r}" for r in reasons)}

## Runtime Chain

{render_chain(data)}

## Promotion Boundary

`promoted_confirmed_chain` means directed/source-confirmed.

`promoted_topology_supported_chain` means topology path complete and validation coverage sufficient, but not fully directed/source-confirmed.

Do not collapse these promotion classes.
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chain", required=True, type=Path)
    ap.add_argument("--out-dir", default=Path("docs/runtime/runtime_chains"), type=Path)
    ap.add_argument("--out-json", type=Path)
    ap.add_argument("--fail-on-rejected", action="store_true")
    args = ap.parse_args()

    data = load_json(args.chain)
    gate = extract_gate(data)
    promotion_type, reasons = decide(gate)

    title = extract_title(data, args.chain)
    slug = slugify(title)

    args.out_dir.mkdir(parents=True, exist_ok=True)

    out_md = args.out_dir / f"{slug}_{promotion_type}.md"
    out_json = args.out_json or args.out_dir / f"{slug}_{promotion_type}.json"

    out_md.write_text(render_md(data, gate, promotion_type, reasons, args.chain), encoding="utf-8")

    result = {
        "source": args.chain.as_posix(),
        "title": title,
        "promotion_type": promotion_type,
        "promoted": promotion_type != REJECTED,
        "gate": gate,
        "reasons": reasons,
        "output_md": out_md.as_posix(),
    }
    out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Promotion type: {promotion_type}")
    print(f"Promoted: {promotion_type != REJECTED}")
    print(f"Gate: {json.dumps(gate, ensure_ascii=False)}")
    print(f"Wrote MD:   {out_md}")
    print(f"Wrote JSON: {out_json}")

    if promotion_type == REJECTED and args.fail_on_rejected:
        raise SystemExit(2)


if __name__ == "__main__":
    main()