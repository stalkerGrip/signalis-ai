#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_slug(value: str) -> str:
    return (
        value.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace(":", "")
        .replace("-", "_")
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Promote CharacterLoaded runtime chain candidate as topology/source-validation supported chain."
    )
    parser.add_argument(
        "--candidate",
        type=Path,
        default=Path("investigations/validation/characterload_inventory_runtime_chain_candidate_v1.json"),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("docs/runtime/runtime_chains"),
    )

    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    candidate = load_json(args.candidate)

    title = candidate.get("title", "characterload inventory initialization lifecycle chain")
    confidence = candidate.get("confidence", "unknown")
    score = float(candidate.get("score", 0.0))
    missing = candidate.get("missing_required_stages", [])

    promoted = (
        confidence in {"high", "medium"}
        and score >= 0.90
        and not missing
    )

    promotion_type = (
        "promoted_source_validated_chain"
        if promoted
        else "not_promoted"
    )

    slug = safe_slug(title)
    out_json = args.out_dir / f"{slug}_{promotion_type}.json"
    out_md = args.out_dir / f"{slug}_{promotion_type}.md"

    artifact: dict[str, Any] = {
        "source": str(args.candidate),
        "title": title,
        "promotion_type": promotion_type,
        "promoted": promoted,
        "gate": {
            "confidence": confidence,
            "score": score,
            "missing_required_stages": missing,
        },
        "reasons": [
            f"{confidence} confidence",
            "score >= 0.90" if score >= 0.90 else "score < 0.90",
            "missing required stages none" if not missing else "missing required stages present",
            "promoted from targeted source validation runtime facts",
        ],
        "output_md": str(out_md),
        "chain": candidate,
    }

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(artifact, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Promoted Runtime Chain",
        "",
        f"- Title: `{title}`",
        f"- Promotion type: `{promotion_type}`",
        f"- Promoted: `{promoted}`",
        f"- Confidence: `{confidence}`",
        f"- Score: `{score}`",
        f"- Missing required stages: `{', '.join(missing) if missing else 'none'}`",
        "",
        "## Chain",
        "",
        "```text",
    ]

    for stage in candidate.get("stages", []):
        lines.append(f"{stage.get('order')}. {stage.get('category')} — {stage.get('label')}")

    lines += [
        "```",
        "",
        "## Source Candidate",
        "",
        f"`{args.candidate}`",
        "",
    ]

    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Promoted: {promoted}")
    print(f"Promotion type: {promotion_type}")
    print(f"Wrote JSON: {out_json}")
    print(f"Wrote MD:   {out_md}")

    return 0 if promoted else 1


if __name__ == "__main__":
    raise SystemExit(main())