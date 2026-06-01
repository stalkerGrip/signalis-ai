from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


PIPELINE_CONTRACT = {
    "script_id": "scripts.investigation.build_architecture_intelligence_v1",
    "purpose": (
        "Build deterministic architecture intelligence from promoted runtime "
        "chain context packs."
    ),
    "pipeline_stage": "architecture_intelligence",
    "input_schemas": [
        "runtime_chain_context_pack.v1",
        "pipeline_artifact_contract.v1",
    ],
    "output_schemas": [
        "architecture_intelligence.v1",
    ],
    "artifact_patterns": [
        "investigations/architecture/architecture_intelligence_v1.json",
        "investigations/architecture/architecture_intelligence_v1.md",
    ],
    "promotion_role": "promotion_support",
    "canonical_status": "active",
}


STAGE_CLASSES = {
    "metadata": [
        "metadata",
        "itemdata",
        "item_data",
        "data_mutation",
    ],
    "network": [
        "network",
        "sync",
        "send",
        "receive",
        "client_apply",
    ],
    "ui": [
        "ui",
        "refresh",
        "panel",
        "presentation",
    ],
    "inventory_membership": [
        "inventory_membership",
        "inventory",
        "transfer",
        "ownership",
    ],
    "server_authority": [
        "server",
        "mutation",
        "purchase_transfer",
        "cleanup",
    ],
}


CONTRACT_RULES = [
    {
        "id": "item_metadata_sync_contract",
        "required_terms": ["item_metadata_mutation", "item_metadata_network_send", "item_metadata_client_apply"],
        "description": "Item metadata mutation must have an explicit network send and client apply stage.",
    },
    {
        "id": "ui_refresh_contract",
        "required_terms": ["item_metadata_client_apply", "ui_itemdata_refresh_hook"],
        "description": "Client item data application should propagate into a UI refresh hook.",
    },
    {
        "id": "inventory_membership_vs_metadata_boundary",
        "required_terms": ["inventory_membership_client_apply", "item_metadata_client_apply"],
        "description": "Inventory membership sync and item metadata sync appear as separate propagation stages.",
    },
]


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing JSON file: {path}")

    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def classify_stage(stage: str) -> list[str]:
    lower = stage.lower()
    classes: list[str] = []

    for class_name, terms in STAGE_CLASSES.items():
        if any(term in lower for term in terms):
            classes.append(class_name)

    if not classes:
        classes.append("unknown")

    return classes


def infer_realm_transition(stages: list[str]) -> list[dict[str, Any]]:
    transitions: list[dict[str, Any]] = []

    for left, right in zip(stages, stages[1:]):
        left_lower = left.lower()
        right_lower = right.lower()

        if "network" in left_lower or "client_apply" in right_lower:
            transitions.append(
                {
                    "from_stage": left,
                    "to_stage": right,
                    "transition_type": "server_to_client_sync_boundary",
                    "confidence": "medium",
                }
            )

    return transitions


def infer_sync_contracts(chain: dict[str, Any]) -> list[dict[str, Any]]:
    stages = [str(stage) for stage in chain.get("stages", [])]
    stage_text = " ".join(stages).lower()

    contracts: list[dict[str, Any]] = []

    for rule in CONTRACT_RULES:
        matched = [term for term in rule["required_terms"] if term.lower() in stage_text]

        contracts.append(
            {
                "contract_id": rule["id"],
                "description": rule["description"],
                "matched_terms": matched,
                "required_terms": rule["required_terms"],
                "coverage": round(len(matched) / len(rule["required_terms"]), 4),
                "status": "observed" if len(matched) == len(rule["required_terms"]) else "partial",
            }
        )

    return contracts


def infer_coupling(chain: dict[str, Any]) -> list[dict[str, Any]]:
    stages = [str(stage) for stage in chain.get("stages", [])]
    stage_text = " ".join(stages).lower()

    findings: list[dict[str, Any]] = []

    if "inventory_membership" in stage_text and "item_metadata" in stage_text:
        findings.append(
            {
                "coupling_id": "inventory_membership_and_item_metadata",
                "description": (
                    "The chain couples inventory membership propagation with item metadata "
                    "propagation while keeping them as distinct stages."
                ),
                "risk": "ui_desync_if_one_path_refreshes_without_the_other",
                "confidence": chain.get("confidence") or "unknown",
            }
        )

    if "ui" in stage_text and "client_apply" in stage_text:
        findings.append(
            {
                "coupling_id": "client_data_apply_to_ui_refresh",
                "description": "Client-side data application is coupled to UI refresh propagation.",
                "risk": "stale_presentation_if_ui_refresh_hook_does_not_fire",
                "confidence": chain.get("confidence") or "unknown",
            }
        )

    if "network" in stage_text:
        findings.append(
            {
                "coupling_id": "network_sync_boundary",
                "description": "The chain crosses a network synchronization boundary.",
                "risk": "receiver_scope_or_payload_loss_can_create_client_desync",
                "confidence": chain.get("confidence") or "unknown",
            }
        )

    return findings


def analyze_chain(chain: dict[str, Any]) -> dict[str, Any]:
    stages = [str(stage) for stage in chain.get("stages", [])]

    classified_stages = [
        {
            "stage": stage,
            "classes": classify_stage(stage),
        }
        for stage in stages
    ]

    class_counts = Counter(
        class_name
        for item in classified_stages
        for class_name in item["classes"]
    )

    return {
        "source_id": chain.get("source_id"),
        "title": chain.get("title"),
        "chain_id": chain.get("chain_id"),
        "confidence": chain.get("confidence"),
        "promotion_status": chain.get("promotion_status"),
        "source_path": chain.get("source_path"),
        "stage_count": len(stages),
        "stages": stages,
        "classified_stages": classified_stages,
        "stage_class_counts": dict(sorted(class_counts.items())),
        "realm_transitions": infer_realm_transition(stages),
        "sync_contracts": infer_sync_contracts(chain),
        "coupling_findings": infer_coupling(chain),
    }


def summarize_global_findings(chain_analyses: list[dict[str, Any]]) -> dict[str, Any]:
    total_stage_classes: Counter[str] = Counter()
    coupling_counter: Counter[str] = Counter()
    contract_counter: Counter[str] = Counter()

    chains_by_confidence: dict[str, int] = defaultdict(int)
    chains_by_promotion_status: dict[str, int] = defaultdict(int)

    for analysis in chain_analyses:
        total_stage_classes.update(analysis.get("stage_class_counts", {}))

        confidence = str(analysis.get("confidence") or "unknown")
        promotion_status = str(analysis.get("promotion_status") or "unknown")

        chains_by_confidence[confidence] += 1
        chains_by_promotion_status[promotion_status] += 1

        for finding in analysis.get("coupling_findings", []):
            coupling_counter[str(finding.get("coupling_id"))] += 1

        for contract in analysis.get("sync_contracts", []):
            if contract.get("status") == "observed":
                contract_counter[str(contract.get("contract_id"))] += 1

    return {
        "chains_total": len(chain_analyses),
        "chains_by_confidence": dict(sorted(chains_by_confidence.items())),
        "chains_by_promotion_status": dict(sorted(chains_by_promotion_status.items())),
        "stage_class_totals": dict(sorted(total_stage_classes.items())),
        "observed_coupling_patterns": dict(sorted(coupling_counter.items())),
        "observed_sync_contracts": dict(sorted(contract_counter.items())),
    }


def build_intelligence(context_pack: dict[str, Any], input_path: Path) -> dict[str, Any]:
    if context_pack.get("schema") != "runtime_chain_context_pack.v1":
        raise ValueError(
            f"Expected runtime_chain_context_pack.v1, got {context_pack.get('schema')!r}"
        )

    chains = context_pack.get("ranked_chains", [])
    if not isinstance(chains, list):
        raise ValueError("runtime_chain_context_pack ranked_chains must be a list")

    analyses = [
        analyze_chain(chain)
        for chain in chains
        if isinstance(chain, dict)
    ]

    return {
        "schema": "architecture_intelligence.v1",
        "producer_script": PIPELINE_CONTRACT["script_id"],
        "pipeline_stage": "architecture_intelligence",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "input_artifact": str(input_path),
        "source_query": context_pack.get("query"),
        "source_context_pack_producer": context_pack.get("producer_script"),
        "summary": summarize_global_findings(analyses),
        "chain_analyses": analyses,
        "architecture_findings": build_architecture_findings(analyses),
        "next_questions": build_next_questions(analyses),
    }


def build_architecture_findings(analyses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    for analysis in analyses:
        chain_id = analysis.get("chain_id")

        for coupling in analysis.get("coupling_findings", []):
            findings.append(
                {
                    "finding_id": f"{chain_id}:{coupling.get('coupling_id')}",
                    "chain_id": chain_id,
                    "type": "coupling",
                    "description": coupling.get("description"),
                    "risk": coupling.get("risk"),
                    "confidence": coupling.get("confidence"),
                    "source_path": analysis.get("source_path"),
                }
            )

        for contract in analysis.get("sync_contracts", []):
            if contract.get("status") == "observed":
                findings.append(
                    {
                        "finding_id": f"{chain_id}:{contract.get('contract_id')}",
                        "chain_id": chain_id,
                        "type": "sync_contract",
                        "description": contract.get("description"),
                        "coverage": contract.get("coverage"),
                        "confidence": analysis.get("confidence"),
                        "source_path": analysis.get("source_path"),
                    }
                )

    return findings


def build_next_questions(analyses: list[dict[str, Any]]) -> list[str]:
    questions: list[str] = []

    has_ui = any(
        "ui" in analysis.get("stage_class_counts", {})
        for analysis in analyses
    )

    has_network = any(
        "network" in analysis.get("stage_class_counts", {})
        for analysis in analyses
    )

    has_inventory_metadata_boundary = any(
        finding.get("coupling_id") == "inventory_membership_and_item_metadata"
        for analysis in analyses
        for finding in analysis.get("coupling_findings", [])
    )

    if has_ui:
        questions.append(
            "Which UI refresh hooks are canonical synchronization boundaries versus presentation-only refreshes?"
        )

    if has_network:
        questions.append(
            "Which network messages should become explicit synchronization contracts?"
        )

    if has_inventory_metadata_boundary:
        questions.append(
            "Where should inventory membership sync and item metadata sync be documented as separate contracts?"
        )

    if not questions:
        questions.append(
            "Which additional promoted chains are needed before broader architecture synthesis is useful?"
        )

    return questions


def write_md(path: Path, intelligence: dict[str, Any]) -> None:
    lines: list[str] = []

    summary = intelligence["summary"]

    lines.append("# Architecture Intelligence V1")
    lines.append("")
    lines.append(f"- Schema: `{intelligence['schema']}`")
    lines.append(f"- Producer: `{intelligence['producer_script']}`")
    lines.append(f"- Source query: `{intelligence.get('source_query')}`")
    lines.append(f"- Input: `{intelligence.get('input_artifact')}`")
    lines.append(f"- Chains analyzed: `{summary.get('chains_total')}`")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append("Chains by confidence:")
    lines.append("")
    for key, value in summary.get("chains_by_confidence", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")

    lines.append("Chains by promotion status:")
    lines.append("")
    for key, value in summary.get("chains_by_promotion_status", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")

    lines.append("Stage class totals:")
    lines.append("")
    for key, value in summary.get("stage_class_totals", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")

    lines.append("## Architecture Findings")
    lines.append("")

    findings = intelligence.get("architecture_findings", [])
    if not findings:
        lines.append("No architecture findings generated.")
        lines.append("")
    else:
        for finding in findings:
            lines.append(f"### {finding.get('finding_id')}")
            lines.append("")
            lines.append(f"- Type: `{finding.get('type')}`")
            lines.append(f"- Chain ID: `{finding.get('chain_id')}`")
            lines.append(f"- Confidence: `{finding.get('confidence')}`")
            lines.append(f"- Source path: `{finding.get('source_path')}`")
            if finding.get("coverage") is not None:
                lines.append(f"- Coverage: `{finding.get('coverage')}`")
            if finding.get("risk"):
                lines.append(f"- Risk: `{finding.get('risk')}`")
            lines.append("")
            lines.append(str(finding.get("description") or ""))
            lines.append("")

    lines.append("## Chain Analyses")
    lines.append("")

    for analysis in intelligence.get("chain_analyses", []):
        lines.append(f"### {analysis.get('title') or analysis.get('chain_id')}")
        lines.append("")
        lines.append(f"- Chain ID: `{analysis.get('chain_id')}`")
        lines.append(f"- Confidence: `{analysis.get('confidence')}`")
        lines.append(f"- Promotion status: `{analysis.get('promotion_status')}`")
        lines.append(f"- Stage count: `{analysis.get('stage_count')}`")
        lines.append(f"- Source path: `{analysis.get('source_path')}`")
        lines.append("")

        lines.append("Stages:")
        lines.append("")
        for item in analysis.get("classified_stages", []):
            classes = ", ".join(item.get("classes", []))
            lines.append(f"- `{item.get('stage')}` — {classes}")
        lines.append("")

        transitions = analysis.get("realm_transitions", [])
        if transitions:
            lines.append("Realm / sync transitions:")
            lines.append("")
            for transition in transitions:
                lines.append(
                    f"- `{transition.get('from_stage')}` → `{transition.get('to_stage')}` "
                    f"= `{transition.get('transition_type')}`"
                )
            lines.append("")

    lines.append("## Next Questions")
    lines.append("")
    for question in intelligence.get("next_questions", []):
        lines.append(f"- {question}")
    lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build deterministic architecture intelligence from runtime chain context packs."
    )

    parser.add_argument(
        "--workspace",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--context-pack",
        type=Path,
        default=Path("investigations/retrieval/runtime_chain_context_pack.json"),
    )

    parser.add_argument(
        "--out-json",
        type=Path,
        default=Path("investigations/architecture/architecture_intelligence_v1.json"),
    )

    parser.add_argument(
        "--out-md",
        type=Path,
        default=Path("investigations/architecture/architecture_intelligence_v1.md"),
    )

    return parser.parse_args()


def resolve_workspace_path(workspace: Path, path: Path) -> Path:
    if path.is_absolute():
        return path
    return workspace / path


def main() -> None:
    args = parse_args()

    workspace = args.workspace.resolve()

    context_pack_path = resolve_workspace_path(workspace, args.context_pack)
    out_json = resolve_workspace_path(workspace, args.out_json)
    out_md = resolve_workspace_path(workspace, args.out_md)

    context_pack = read_json(context_pack_path)
    intelligence = build_intelligence(context_pack, context_pack_path)

    write_json(out_json, intelligence)
    write_md(out_md, intelligence)

    print(f"Wrote JSON: {out_json}")
    print(f"Wrote MD:   {out_md}")
    print(f"Chains analyzed: {intelligence['summary']['chains_total']}")
    print(f"Findings: {len(intelligence['architecture_findings'])}")


if __name__ == "__main__":
    main()