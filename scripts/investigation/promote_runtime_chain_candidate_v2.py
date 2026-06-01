from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


PIPELINE_CONTRACT = {
    "script_id": "scripts.investigation.promote_runtime_chain_candidate_v2",
    "purpose": (
        "Govern runtime chain promotion from candidate and promotion validation "
        "into deterministic decision, supersession, and canonical promoted output."
    ),
    "pipeline_stage": "promotion",
    "input_schemas": [
        "runtime_chain_candidate.v5",
        "runtime_chain_candidate.v6",
        "runtime_chain_candidate.v7",
        "runtime_chain_promotion_validation.v1",
        "pipeline_artifact_contract.v1",
    ],
    "output_schemas": [
        "runtime_chain_promotion_decision.v4",
        "promoted_runtime_chain.md",
    ],
    "artifact_patterns": [
        "investigations/validation/*_promotion_decision*.json",
        "investigations/validation/*_promotion_decision*.md",
        "docs/runtime/runtime_chains/*_promoted_confirmed_chain.md",
        "docs/runtime/runtime_chains/*_promoted_topology_supported_chain.md",
        "docs/runtime/runtime_chains/*_not_promoted.md",
    ],
    "promotion_role": "promotion_core",
    "canonical_status": "active",
}


BAD_STATUSES = {"debug", "failed", "legacy", "superseded"}
CONFIDENCE_RANK = {
    "none": 0,
    None: 0,
    "low": 1,
    "medium": 2,
    "high": 3,
}


CANDIDATE_SCHEMAS = {
    "runtime_chain_candidate.v5",
    "runtime_chain_candidate.v6",
    "runtime_chain_candidate.v7",
}


PROMOTION_VALIDATION_SCHEMAS = {
    "runtime_chain_promotion_validation.v1",
}


PROMOTION_DECISION_SCHEMA = "runtime_chain_promotion_decision.v4"


PROMOTED_DECISIONS = {
    "promoted_confirmed_chain",
    "promoted_topology_supported_chain",
    "promoted_source_validated_chain",
}


@dataclass
class PromotionDecision:
    decision: str
    reason: str
    confidence: str
    score: float
    validation_passed: bool
    deterministic_regeneration: bool
    supported_links_count: int
    unsupported_links_count: int
    missing_stages: list[str]
    caveats: list[str]


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def resolve_workspace_path(workspace: Path, value: Path | str | None) -> Path | None:
    if value is None:
        return None

    path = Path(value)

    if path.is_absolute():
        return path

    return workspace / path


def safe_slug(value: str) -> str:
    out = []
    for ch in value.strip().lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in {" ", "-", "_", ".", "/", "\\"}:
            out.append("_")
    slug = "".join(out).strip("_")
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug or "runtime_chain"


def first_present(data: dict[str, Any], keys: list[str], default: Any = None) -> Any:
    for key in keys:
        if key in data and data[key] not in (None, ""):
            return data[key]
    return default


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def extract_schema(data: dict[str, Any]) -> str | None:
    return first_present(data, ["schema", "artifact_schema", "type"])


def extract_status(data: dict[str, Any]) -> str:
    return str(first_present(data, ["canonical_status", "status"], "intermediate"))


def extract_benchmark(data: dict[str, Any], fallback: str | None = None) -> str:
    return str(first_present(data, ["benchmark", "chain_id", "id"], fallback or "unknown"))


def extract_title(candidate: dict[str, Any], fallback: str) -> str:
    return str(first_present(candidate, ["title", "name", "chain_title"], fallback))


def extract_steps(candidate: dict[str, Any]) -> list[str]:
    raw = first_present(
        candidate,
        [
            "ordered_steps",
            "steps",
            "chain",
            "recovered_chain",
            "stages",
        ],
        [],
    )

    steps: list[str] = []

    if isinstance(raw, str):
        for part in raw.replace("→", "\n").splitlines():
            part = part.strip(" -\t")
            if part:
                steps.append(part)
        return steps

    for item in as_list(raw):
        if isinstance(item, str):
            steps.append(item)

        elif isinstance(item, dict):
            label = first_present(
                item,
                [
                    "stage",
                    "step",
                    "id",
                    "name",
                    "title",
                    "label",
                ],
                None,
            )

            if label:
                steps.append(str(label))

    return steps


def extract_links_count(data: dict[str, Any], keys: list[str]) -> int:
    for key in keys:
        value = data.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, list):
            return len(value)
    return 0


def validate_registry(registry: dict[str, Any]) -> None:
    if registry.get("schema") != "pipeline_artifact_contract.v1":
        raise ValueError("Registry schema must be pipeline_artifact_contract.v1")

    scripts = registry.get("scripts", [])
    known = {
        item.get("script_id")
        for item in scripts
        if isinstance(item, dict)
    }

    required = {
        "scripts.investigation.validate_runtime_chain_promotion",
    }

    missing = sorted(required - known)
    if missing:
        raise ValueError(
            "Contract registry missing required promotion scripts: "
            + ", ".join(missing)
        )


def validate_input_artifact(path: Path, data: dict[str, Any], allowed_schemas: set[str]) -> None:
    schema = extract_schema(data)
    status = extract_status(data)

    if schema not in allowed_schemas:
        # Compatibility:
        # some generated promotion validation artifacts incorrectly preserve
        # candidate schema but contain validation/compare/regeneration payload.
        looks_like_promotion_validation = (
            "runtime_chain_promotion_validation.v1" in allowed_schemas
            and (
                "promotion_validation" in data
                or "validation" in data
                or "regeneration" in data
                or "deterministic_regeneration" in data
                or "comparison" in data
                or "matches" in data
                or "matched_steps" in data
                or "missing_steps" in data
                or "errors" in data
                or "summary" in data
            )
        )

        if not looks_like_promotion_validation:
            raise ValueError(
                f"{path} has schema {schema!r}; expected one of {sorted(allowed_schemas)}"
            )

    if status in BAD_STATUSES:
        raise ValueError(f"{path} has blocked status {status!r}")


def extract_validation_result(validation: dict[str, Any]) -> tuple[bool, bool, list[str]]:
    comparison = validation.get("comparison", {})

    passed = bool(
        first_present(
            validation,
            [
                "promotion_validation",
                "promotion_validation_passed",
                "passed",
                "valid",
            ],
            False,
        )
    )

    comparison_passed = bool(
        first_present(
            comparison,
            ["passed"],
            True,
        )
    )

    deterministic = bool(
        first_present(
            validation,
            [
                "rebuild_success",
                "deterministic_regeneration",
                "deterministic_regeneration_passed",
                "regeneration_passed",
            ],
            False,
        )
    )

    errors = []

    for key in ["errors", "failures", "validation_errors"]:
        errors.extend(str(x) for x in as_list(validation.get(key)))

    return (
        passed and comparison_passed,
        deterministic,
        errors,
    )


def decide(candidate: dict[str, Any], validation: dict[str, Any]) -> PromotionDecision:
    confidence = str(first_present(candidate, ["confidence"], "none")).lower()

    try:
        score = float(first_present(candidate, ["score", "runtime_chain_score"], 0.0))
    except (TypeError, ValueError):
        score = 0.0

    missing_stages = [
        str(x)
        for x in as_list(
            first_present(
                candidate,
                ["missing_required_stages", "missing_stages", "missing_required_steps"],
                [],
            )
        )
    ]

    supported = extract_links_count(
        candidate,
        ["supported_links", "topology_supported_links", "supported"],
    )
    unsupported = extract_links_count(
        candidate,
        ["unsupported_links", "topology_unsupported_links", "unsupported"],
    )

    validation_passed, deterministic, validation_errors = extract_validation_result(validation)

    caveats: list[str] = []
    caveats.extend(validation_errors)

    if missing_stages:
        caveats.append("Missing stages: " + ", ".join(missing_stages))

    if not validation_passed:
        return PromotionDecision(
            decision="not_promoted",
            reason="promotion validation did not pass",
            confidence=confidence,
            score=score,
            validation_passed=False,
            deterministic_regeneration=deterministic,
            supported_links_count=supported,
            unsupported_links_count=unsupported,
            missing_stages=missing_stages,
            caveats=caveats,
        )

    if not deterministic:
        return PromotionDecision(
            decision="not_promoted",
            reason="deterministic regeneration did not pass",
            confidence=confidence,
            score=score,
            validation_passed=True,
            deterministic_regeneration=False,
            supported_links_count=supported,
            unsupported_links_count=unsupported,
            missing_stages=missing_stages,
            caveats=caveats,
        )

    if CONFIDENCE_RANK.get(confidence, 0) >= 2 and not missing_stages:
        return PromotionDecision(
            decision="promoted_confirmed_chain",
            reason="promotion validation passed and candidate has medium/high confidence with no missing stages",
            confidence=confidence,
            score=score,
            validation_passed=True,
            deterministic_regeneration=True,
            supported_links_count=supported,
            unsupported_links_count=unsupported,
            missing_stages=missing_stages,
            caveats=caveats,
        )

    if CONFIDENCE_RANK.get(confidence, 0) >= 1 and supported > 0:
        return PromotionDecision(
            decision="promoted_topology_supported_chain",
            reason="promotion validation passed and candidate has topology-supported links",
            confidence=confidence,
            score=score,
            validation_passed=True,
            deterministic_regeneration=True,
            supported_links_count=supported,
            unsupported_links_count=unsupported,
            missing_stages=missing_stages,
            caveats=caveats,
        )

    return PromotionDecision(
        decision="not_promoted",
        reason="candidate did not satisfy confidence/topology support gate",
        confidence=confidence,
        score=score,
        validation_passed=True,
        deterministic_regeneration=True,
        supported_links_count=supported,
        unsupported_links_count=unsupported,
        missing_stages=missing_stages,
        caveats=caveats,
    )


def is_promoted_status(decision_name: str) -> bool:
    return decision_name in PROMOTED_DECISIONS


def supersede_existing(promoted_dir: Path, slug: str, dry_run: bool) -> list[dict[str, str]]:
    superseded: list[dict[str, str]] = []
    if not promoted_dir.exists():
        return superseded

    archive = promoted_dir / "_superseded"
    patterns = [
        f"{slug}_promoted_confirmed_chain.md",
        f"{slug}_promoted_topology_supported_chain.md",
        f"{slug}_not_promoted.md",
        f"{slug}*.md",
    ]

    seen: set[Path] = set()
    for pattern in patterns:
        for path in promoted_dir.glob(pattern):
            if path in seen or path.parent.name == "_superseded":
                continue
            seen.add(path)

            target = archive / f"{path.stem}_superseded_{datetime.now().strftime('%Y%m%d_%H%M%S')}{path.suffix}"
            superseded.append({"from": str(path), "to": str(target)})

            if not dry_run:
                archive.mkdir(parents=True, exist_ok=True)
                shutil.move(str(path), str(target))

    return superseded


def render_markdown(
    *,
    title: str,
    slug: str,
    candidate_path: Path,
    validation_path: Path,
    decision: PromotionDecision,
    candidate: dict[str, Any],
    validation: dict[str, Any],
    superseded: list[dict[str, str]],
) -> str:
    steps = extract_steps(candidate)
    topology = first_present(
        candidate,
        ["topology", "topology_artifact", "runtime_topology", "runtime_propagation_topology"],
        "manifests/normalized/runtime_propagation_topology.json",
    )

    source_validation = first_present(
        candidate,
        ["source_validation", "source_validation_artifact"],
        first_present(validation, ["source_validation", "source_validation_artifact"], "unknown"),
    )

    runtime_facts = first_present(
        candidate,
        ["runtime_facts", "runtime_facts_artifact"],
        first_present(validation, ["runtime_facts", "runtime_facts_artifact"], "unknown"),
    )

    lines = [
        f"# {title}",
        "",
        f"- Slug: `{slug}`",
        f"- Promotion decision: `{decision.decision}`",
        f"- Reason: {decision.reason}",
        f"- Confidence: `{decision.confidence}`",
        f"- Score: `{decision.score}`",
        f"- Validation passed: `{decision.validation_passed}`",
        f"- Deterministic regeneration: `{decision.deterministic_regeneration}`",
        f"- Supported links: `{decision.supported_links_count}`",
        f"- Unsupported links: `{decision.unsupported_links_count}`",
        f"- Topology artifact: `{topology}`",
        f"- Source validation artifact: `{source_validation}`",
        f"- Runtime facts artifact: `{runtime_facts}`",
        f"- Candidate artifact: `{candidate_path}`",
        f"- Promotion validation artifact: `{validation_path}`",
        "",
        "## Runtime Chain",
        "",
    ]

    if steps:
        lines.extend(f"{i}. `{step}`" for i, step in enumerate(steps, 1))
    else:
        lines.append("- No ordered steps found in candidate artifact.")

    lines.extend(["", "## Missing Stages", ""])
    if decision.missing_stages:
        lines.extend(f"- `{stage}`" for stage in decision.missing_stages)
    else:
        lines.append("- none")

    lines.extend(["", "## Caveats", ""])
    if decision.caveats:
        lines.extend(f"- {caveat}" for caveat in decision.caveats)
    else:
        lines.append("- none")

    lines.extend(["", "## Superseded Outputs", ""])
    if superseded:
        lines.extend(f"- `{item['from']}` → `{item['to']}`" for item in superseded)
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Contract Metadata",
            "",
            "```json",
            json.dumps(
                {
                    "schema": "promoted_runtime_chain.md",
                    "producer_script": PIPELINE_CONTRACT["script_id"],
                    "pipeline_stage": "promotion",
                    "promotion_role": "promotion_core",
                    "canonical_status": (
                        "canonical" if is_promoted_status(decision.decision) else "intermediate"
                    ),
                    "inputs": [str(candidate_path), str(validation_path)],
                },
                indent=2,
                ensure_ascii=False,
            ),
            "```",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Promote runtime chain candidate with contract validation, promotion validation, supersession, and canonical output."
    )
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--promotion-validation", required=True, type=Path)
    parser.add_argument(
        "--registry",
        type=Path,
        default=None,
        help="Default: <workspace>/docs/runtime/pipeline_artifact_contract.json",
    )
    parser.add_argument("--name", default=None, help="Output slug. Default: benchmark/title derived.")
    parser.add_argument(
        "--promoted-dir",
        type=Path,
        default=None,
        help="Default: <workspace>/docs/runtime/runtime_chains",
    )
    parser.add_argument("--out-json", type=Path, default=None)
    parser.add_argument("--out-md", type=Path, default=None)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and write decision files, but do not move superseded promoted docs.",
    )
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    registry_path = resolve_workspace_path(
        workspace,
        args.registry or "docs/runtime/pipeline_artifact_contract.json",
    )
    promoted_dir = resolve_workspace_path(
        workspace,
        args.promoted_dir or "docs/runtime/runtime_chains",
    )

    if registry_path is None:
        raise ValueError("Registry path could not be resolved")

    if promoted_dir is None:
        raise ValueError("Promoted output directory could not be resolved")

    candidate_path = resolve_workspace_path(workspace, args.candidate)
    validation_path = resolve_workspace_path(workspace, args.promotion_validation)

    if candidate_path is None:
        raise ValueError("--candidate is required")

    if validation_path is None:
        raise ValueError("--promotion-validation is required")

    registry = read_json(registry_path)
    candidate = read_json(candidate_path)
    validation = read_json(validation_path)

    validate_registry(registry)
    validate_input_artifact(
        candidate_path,
        candidate,
        CANDIDATE_SCHEMAS,
    )
    validate_input_artifact(
        validation_path,
        validation,
        PROMOTION_VALIDATION_SCHEMAS,
    )

    benchmark = extract_benchmark(candidate, fallback=candidate_path.stem)
    title = extract_title(candidate, fallback=benchmark)
    slug = safe_slug(args.name or benchmark)

    decision = decide(candidate, validation)

    superseded = []
    if is_promoted_status(decision.decision):
        superseded = supersede_existing(promoted_dir, slug, args.dry_run)

    out_json = resolve_workspace_path(
        workspace,
        args.out_json or f"investigations/validation/{slug}_promotion_decision.json",
    )
    out_md = resolve_workspace_path(
        workspace,
        args.out_md or f"investigations/validation/{slug}_promotion_decision.md",
    )

    if out_json is None or out_md is None:
        raise ValueError("Decision output paths could not be resolved")

    promoted_md = promoted_dir / f"{slug}_{decision.decision}.md"

    decision_payload = {
        "schema": PROMOTION_DECISION_SCHEMA,
        "producer_script": PIPELINE_CONTRACT["script_id"],
        "pipeline_stage": "promotion",
        "benchmark": benchmark,
        "promotion_role": "promotion_core",
        "canonical_status": (
            "canonical"
            if is_promoted_status(decision.decision) and not args.dry_run
            else "intermediate"
        ),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "decision": decision.__dict__,
        "inputs": [str(candidate_path), str(validation_path), str(registry_path)],
        "outputs": {
            "decision_json": str(out_json),
            "decision_md": str(out_md),
            "promoted_md": str(promoted_md),
        },
        "superseded": superseded,
        "dry_run": args.dry_run,
    }

    markdown = render_markdown(
        title=title,
        slug=slug,
        candidate_path=candidate_path,
        validation_path=validation_path,
        decision=decision,
        candidate=candidate,
        validation=validation,
        superseded=superseded,
    )

    write_json(out_json, decision_payload)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(markdown, encoding="utf-8")

    if is_promoted_status(decision.decision):
        promoted_dir.mkdir(parents=True, exist_ok=True)
        promoted_md.write_text(markdown, encoding="utf-8")

    print(f"Decision: {decision.decision}")
    print(f"Wrote JSON: {out_json}")
    print(f"Wrote MD:   {out_md}")
    if is_promoted_status(decision.decision):
        print(f"Wrote promoted chain: {promoted_md}")


if __name__ == "__main__":
    main()