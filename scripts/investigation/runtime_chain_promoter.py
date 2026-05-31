from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return re.sub(r"_+", "_", value).strip("_") or "runtime_chain"


def write_promoted_doc(path: Path, chain: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: List[str] = []
    lines.append(f"# Runtime Chain: {chain.get('title', path.stem)}")
    lines.append("")
    lines.append("## Status")
    lines.append("")
    lines.append("- Artifact type: promoted runtime chain")
    lines.append(f"- Source schema: `{chain.get('schema', 'runtime_chain.v1')}`")
    lines.append(f"- Confidence: **{chain.get('confidence', 'unknown')}**")
    lines.append(f"- Score: **{chain.get('score', 'unknown')}**")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(chain.get("query", "No query recorded."))
    lines.append("")
    lines.append("## Chain")
    lines.append("")

    for i, step in enumerate(chain.get("steps", []), start=1):
        label = step.get("label") or step.get("summary") or "runtime step"
        realm = step.get("realm", "unknown")
        src = step.get("source_file")
        line_start = step.get("line_start")
        line_end = step.get("line_end", line_start)

        line = f"{i}. **{label}**"
        details = []
        if realm:
            details.append(f"realm=`{realm}`")
        if src:
            if line_start:
                details.append(f"`{src}:{line_start}-{line_end}`")
            else:
                details.append(f"`{src}`")
        if details:
            line += " — " + ", ".join(details)
        lines.append(line)

    lines.append("")
    lines.append("## Missing causal steps")
    lines.append("")
    missing = chain.get("missing_steps") or []
    if missing:
        for item in missing:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    lines.append("")
    lines.append("## Promotion notes")
    lines.append("")
    lines.append("- This document is a durable runtime-chain anchor.")
    lines.append("- It does not modify raw Lua.")
    lines.append("- It should be regenerated or superseded if targeted validation contradicts any step.")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Promote a high-confidence runtime chain candidate into docs/runtime/runtime_chains.")
    parser.add_argument("--chain", required=True, type=Path)
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--allow-medium", action="store_true")

    args = parser.parse_args()

    chain = load_json(args.chain)
    confidence = str(chain.get("confidence", "low")).lower()
    missing = chain.get("missing_steps") or []

    if confidence != "high":
        if not (args.allow_medium and confidence == "medium"):
            raise SystemExit(f"Refusing promotion: confidence is {confidence!r}, expected high.")

    if missing:
        raise SystemExit(f"Refusing promotion: missing causal steps remain: {missing}")

    out = args.out
    if out is None:
        name = slugify(chain.get("title") or args.chain.stem)
        out = args.workspace / "docs" / "runtime" / "runtime_chains" / f"{name}.md"

    write_promoted_doc(out, chain)
    print(f"Promoted runtime chain doc: {out}")


if __name__ == "__main__":
    main()