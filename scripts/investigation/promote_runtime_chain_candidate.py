from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_doc(candidate: dict, out: Path) -> None:
    lines = []

    lines.append(f"# Runtime Chain: {candidate['chain_name']}")
    lines.append("")
    lines.append(f"Confidence: `{candidate['confidence']}`")
    lines.append("")
    lines.append("## Question")
    lines.append("")
    lines.append(candidate.get("question", ""))
    lines.append("")
    lines.append("## Chain")
    lines.append("")

    for idx, step in enumerate(candidate.get("steps", []), start=1):
        lines.append(f"### {idx}. {step['step']}")
        lines.append("")
        lines.append(f"- Status: `{step.get('status')}`")
        lines.append(f"- Source: `{step.get('source')}`")
        lines.append(f"- Line: `{step.get('line')}`")
        lines.append(f"- Evidence source: `{step.get('evidence_source_type')}`")
        lines.append(f"- Matched terms: `{', '.join(step.get('matched_terms', []))}`")
        lines.append("")
        if step.get("evidence_summary"):
            lines.append("```text")
            lines.append(str(step["evidence_summary"]).strip())
            lines.append("```")
            lines.append("")

    lines.append("## Confidence Reasons")
    lines.append("")
    for reason in candidate.get("confidence_reasons", []):
        lines.append(f"- `{reason}`")
    lines.append("")

    lines.append("## Promotion Notes")
    lines.append("")
    lines.append("- Promoted from deterministic runtime chain candidate.")
    lines.append("- This document is a semantic runtime-chain artifact, not a raw source patch.")
    lines.append("- Raw Lua bugfixing is intentionally deferred until investigation pipeline reliability is proven.")
    lines.append("")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    candidate = load_json(args.candidate)

    if candidate.get("confidence") != "high":
        raise SystemExit(f"Refusing promotion; confidence is {candidate.get('confidence')}")

    if candidate.get("missing_steps"):
        raise SystemExit(f"Refusing promotion; missing steps: {candidate['missing_steps']}")

    write_doc(candidate, args.out)
    print(f"Wrote promoted runtime chain: {args.out}")


if __name__ == "__main__":
    main()