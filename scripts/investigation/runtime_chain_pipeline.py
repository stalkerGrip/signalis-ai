#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print("\n[RUN]", " ".join(cmd))
    result = subprocess.run(cmd, text=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Runtime Chain Builder V4 pipeline: step builder -> step orderer -> branch builder."
    )
    parser.add_argument("--ranked-evidence", required=True, type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--out-dir", type=Path, default=Path("investigations/validation"))
    parser.add_argument("--recovery-input", nargs="*", default=[])
    parser.add_argument("--root", default="vendor purchase transfer")
    parser.add_argument("--join", default="client grid inventory UI refresh")
    parser.add_argument("--min-score", default=None)
    parser.add_argument("--min-evidence-score", default=None)
    parser.add_argument("--max-evidence-per-step", default=None)
    parser.add_argument("--drop-generic-related", action="store_true")
    parser.add_argument("--drop-empty-text", action="store_true")
    parser.add_argument("--drop-setup-only", action="store_true")

    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    runtime_steps_json = args.out_dir / f"{args.name}_runtime_steps_pipeline.json"
    runtime_steps_md = args.out_dir / f"{args.name}_runtime_steps_pipeline.md"

    ordered_steps_json = args.out_dir / f"{args.name}_ordered_steps_pipeline.json"
    ordered_steps_md = args.out_dir / f"{args.name}_ordered_steps_pipeline.md"

    branch_chain_json = args.out_dir / f"{args.name}_branch_chain_pipeline.json"
    branch_chain_md = args.out_dir / f"{args.name}_branch_chain_pipeline.md"

    step_cmd = [
        sys.executable,
        "-m",
        "scripts.investigation.runtime_chain_step_builder",
        "--ranked-evidence",
        str(args.ranked_evidence),
        "--out-json",
        str(runtime_steps_json),
        "--out-md",
        str(runtime_steps_md),
    ]

    if args.recovery_input:
        step_cmd.append("--recovery-input")
        step_cmd.extend(str(Path(p)) for p in args.recovery_input)

    if args.min_score is not None:
        step_cmd.extend(["--min-score", str(args.min_score)])
    if args.min_evidence_score is not None:
        step_cmd.extend(["--min-evidence-score", str(args.min_evidence_score)])
    if args.max_evidence_per_step is not None:
        step_cmd.extend(["--max-evidence-per-step", str(args.max_evidence_per_step)])
    if args.drop_generic_related:
        step_cmd.append("--drop-generic-related")
    if args.drop_empty_text:
        step_cmd.append("--drop-empty-text")
    if args.drop_setup_only:
        step_cmd.append("--drop-setup-only")

    run(step_cmd)

    run([
        sys.executable,
        "-m",
        "scripts.investigation.runtime_chain_step_orderer",
        "--steps",
        str(runtime_steps_json),
        "--out-json",
        str(ordered_steps_json),
        "--out-md",
        str(ordered_steps_md),
    ])

    run([
        sys.executable,
        "-m",
        "scripts.investigation.runtime_chain_branch_builder",
        "--ordered-steps",
        str(ordered_steps_json),
        "--out-json",
        str(branch_chain_json),
        "--out-md",
        str(branch_chain_md),
        "--root",
        args.root,
        "--join",
        args.join,
    ])

    print("\n[DONE] Runtime chain pipeline complete")
    print(f"Runtime steps:  {runtime_steps_json}")
    print(f"Ordered steps:  {ordered_steps_json}")
    print(f"Branch chain:   {branch_chain_json}")
    print(f"Branch report:  {branch_chain_md}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())