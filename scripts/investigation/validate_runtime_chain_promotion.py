from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


PIPELINE_CONTRACT = {
    "script_id": "scripts.investigation.validate_runtime_chain_promotion",
    "purpose": "Validate deterministic regeneration of a runtime chain promotion candidate.",
    "pipeline_stage": "promotion",
    "input_schemas": [
        "runtime_chain_candidate.v6",
        "ordered_runtime_facts.v1",
    ],
    "output_schemas": [
        "runtime_chain_promotion_validation.v1",
    ],
    "artifact_patterns": [
        "investigations/validation/*_promotion_validation.json",
        "investigations/validation/*_promotion_validation.md",
    ],
    "promotion_role": "promotion_core",
    "canonical_status": "active",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def stage_names(candidate: dict[str, Any]) -> list[str]:
    stages = candidate.get("stages", [])
    names: list[str] = []

    for stage in stages:
        if isinstance(stage, dict):
            name = stage.get("name") or stage.get("stage")
            if name:
                names.append(str(name))

    return names


def link_pairs(candidate: dict[str, Any]) -> list[tuple[str, str]]:
    links = candidate.get("links", [])
    pairs: list[tuple[str, str]] = []

    for link in links:
        if not isinstance(link, dict):
            continue

        source = link.get("source") or link.get("from")
        target = link.get("target") or link.get("to")

        if source and target:
            pairs.append((str(source), str(target)))

    return pairs


def normalize_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": candidate.get("schema"),
        "confidence": candidate.get("confidence"),
        "score": candidate.get("score"),
        "supporting_facts_total": candidate.get("supporting_facts_total")
        or candidate.get("supporting_facts")
        or candidate.get("facts_total"),
        "stages_total": candidate.get("stages_total"),
        "present_stages_total": candidate.get("present_stages_total"),
        "missing_required_stages": candidate.get("missing_required_stages", []),
        "stage_names": stage_names(candidate),
        "links": link_pairs(candidate),
    }


def run_v6_builder(
    ordered_facts: Path,
    out_json: Path,
    out_md: Path,
) -> None:
    cmd = [
        sys.executable,
        "-m",
        "scripts.investigation.build_runtime_chain_candidate_v6",
        "--ordered-facts",
        str(ordered_facts),
        "--out-json",
        str(out_json),
        "--out-md",
        str(out_md),
    ]

    result = subprocess.run(
        cmd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "V6 rebuild failed.\n\n"
            f"Command:\n{' '.join(cmd)}\n\n"
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}"
        )


def compare(original: dict[str, Any], regenerated: dict[str, Any]) -> dict[str, Any]:
    original_norm = normalize_candidate(original)
    regenerated_norm = normalize_candidate(regenerated)

    checks = {
        "schema_match": original_norm["schema"] == regenerated_norm["schema"],
        "confidence_match": original_norm["confidence"] == regenerated_norm["confidence"],
        "score_match": original_norm["score"] == regenerated_norm["score"],
        "missing_required_stages_match": original_norm["missing_required_stages"]
        == regenerated_norm["missing_required_stages"],
        "stage_order_match": original_norm["stage_names"] == regenerated_norm["stage_names"],
        "links_match": original_norm["links"] == regenerated_norm["links"],
    }

    return {
        "checks": checks,
        "passed": all(checks.values()),
        "original": original_norm,
        "regenerated": regenerated_norm,
    }


def write_md(path: Path, report: dict[str, Any]) -> None:
    lines: list[str] = []

    lines.append("# Runtime Chain Promotion Validation")
    lines.append("")
    lines.append(f"- Schema: `{report['schema']}`")
    lines.append(f"- Candidate: `{report['candidate']}`")
    lines.append(f"- Ordered facts: `{report['ordered_facts']}`")
    lines.append(f"- Rebuild success: `{report['rebuild_success']}`")
    lines.append(f"- Promotion validation: `{report['promotion_validation']}`")
    lines.append(f"- Recommendation: `{report['promotion_recommendation']}`")
    lines.append("")

    lines.append("## Checks")
    lines.append("")
    for key, value in report["comparison"]["checks"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")

    lines.append("## Original Candidate")
    lines.append("")
    original = report["comparison"]["original"]
    lines.append(f"- Confidence: `{original.get('confidence')}`")
    lines.append(f"- Score: `{original.get('score')}`")
    lines.append(f"- Missing required stages: `{original.get('missing_required_stages')}`")
    lines.append("")
    lines.append("### Stages")
    lines.append("")
    for stage in original.get("stage_names", []):
        lines.append(f"- `{stage}`")
    lines.append("")

    lines.append("## Regenerated Candidate")
    lines.append("")
    regenerated = report["comparison"]["regenerated"]
    lines.append(f"- Confidence: `{regenerated.get('confidence')}`")
    lines.append(f"- Score: `{regenerated.get('score')}`")
    lines.append(f"- Missing required stages: `{regenerated.get('missing_required_stages')}`")
    lines.append("")
    lines.append("### Stages")
    lines.append("")
    for stage in regenerated.get("stage_names", []):
        lines.append(f"- `{stage}`")
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate deterministic regeneration of a runtime chain promotion candidate."
    )

    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--ordered-facts", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    parser.add_argument(
        "--keep-regenerated-json",
        type=Path,
        default=None,
        help="Optional path to keep regenerated candidate JSON.",
    )
    parser.add_argument(
        "--keep-regenerated-md",
        type=Path,
        default=None,
        help="Optional path to keep regenerated candidate MD.",
    )

    args = parser.parse_args()

    candidate_path: Path = args.candidate
    ordered_facts_path: Path = args.ordered_facts

    if not candidate_path.exists():
        raise FileNotFoundError(f"Candidate not found: {candidate_path}")

    if not ordered_facts_path.exists():
        raise FileNotFoundError(f"Ordered facts not found: {ordered_facts_path}")

    original = load_json(candidate_path)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        regen_json = args.keep_regenerated_json or tmp_path / "regenerated_candidate.json"
        regen_md = args.keep_regenerated_md or tmp_path / "regenerated_candidate.md"

        run_v6_builder(
            ordered_facts=ordered_facts_path,
            out_json=regen_json,
            out_md=regen_md,
        )

        regenerated = load_json(regen_json)

    comparison = compare(original, regenerated)

    report = {
        "schema": "runtime_chain_promotion_validation.v1",
        "producer_script": "scripts.investigation.validate_runtime_chain_promotion",
        "pipeline_stage": "promotion",
        "promotion_role": "promotion_core",
        "canonical_status": "intermediate",
        "candidate": str(candidate_path),
        "ordered_facts": str(ordered_facts_path),
        "rebuild_success": True,
        "promotion_validation": comparison["passed"],
        "promotion_recommendation": "approve" if comparison["passed"] else "reject",
        "comparison": comparison,
        "inputs": [
            str(candidate_path),
            str(ordered_facts_path),
        ],
    }

    write_json(args.out_json, report)
    write_md(args.out_md, report)

    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")
    print(f"Promotion validation: {report['promotion_validation']}")
    print(f"Recommendation: {report['promotion_recommendation']}")


if __name__ == "__main__":
    main()