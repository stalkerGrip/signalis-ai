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
        "investigations/architecture/*architecture_intelligence*.json",
        "investigations/architecture/*architecture_intelligence*.md",
    ],
    "promotion_role": "promotion_support",
    "canonical_status": "active",
}


DEFAULT_STAGE_CLASSES: dict[str, list[str]] = {
    "metadata": ["metadata", "itemdata", "item_data", "data_mutation", "setdata"],
    "network": ["network", "netstream", "sync", "send", "receive", "receiver"],
    "client_apply": ["client_apply", "client", "apply"],
    "ui": ["ui", "refresh", "panel", "presentation", "derma", "hud"],
    "inventory": ["inventory", "transfer", "ownership", "membership"],
    "storage": ["storage"],
    "vendor": ["vendor"],
    "persistence": ["save", "load", "persist", "database", "db"],
    "server_authority": ["server", "mutation", "cleanup", "authoritative"],
    "hook_event": ["hook", "event", "listener", "emit"],
    "timer_scheduler": ["timer", "delay", "scheduler", "tick"],
}


DEFAULT_CONTRACT_RULES: list[dict[str, Any]] = [
    {
        "id": "metadata_sync_contract",
        "required_terms": ["metadata", "send", "client_apply"],
        "description": "Metadata mutation should expose a send/apply synchronization path.",
    },
    {
        "id": "client_apply_to_presentation_contract",
        "required_terms": ["client_apply", "ui"],
        "description": "Client-side state application should have an explicit presentation refresh path when UI is affected.",
    },
    {
        "id": "ownership_vs_metadata_boundary",
        "required_terms": ["inventory", "metadata"],
        "description": "Inventory ownership/membership and item metadata should remain distinguishable propagation concerns.",
    },
    {
        "id": "persistence_sync_boundary",
        "required_terms": ["persistence", "network"],
        "description": "Persistence flows that cross the network boundary should be explicit synchronization contracts.",
    },
]


NETWORK_BOUNDARY_TERMS = {"network", "netstream", "send", "receive", "receiver", "client_apply", "sync"}
CLIENT_TERMS = {"client", "client_apply", "ui", "hud", "derma", "panel", "presentation"}
SERVER_TERMS = {"server", "mutation", "authoritative", "cleanup", "purchase_transfer", "save", "load"}


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def resolve_workspace_path(workspace: Path, path: Path) -> Path:
    if path.is_absolute():
        return path
    return workspace / path


def as_strings(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item is not None]
    return [str(value)]


def extract_chain_stages(chain: dict[str, Any]) -> list[str]:
    for key in ["stages", "runtime_chain_steps", "chain_stages", "steps", "ordered_steps"]:
        value = chain.get(key)
        if value:
            return as_strings(value)
    return []


def load_rule_config(path: Path | None) -> tuple[dict[str, list[str]], list[dict[str, Any]]]:
    if path is None:
        return DEFAULT_STAGE_CLASSES, DEFAULT_CONTRACT_RULES

    payload = read_json(path)

    stage_classes = payload.get("stage_classes", DEFAULT_STAGE_CLASSES)
    contract_rules = payload.get("contract_rules", DEFAULT_CONTRACT_RULES)

    if not isinstance(stage_classes, dict):
        raise ValueError("architecture rule config stage_classes must be an object")

    if not isinstance(contract_rules, list):
        raise ValueError("architecture rule config contract_rules must be a list")

    normalized_classes: dict[str, list[str]] = {}
    for key, value in stage_classes.items():
        normalized_classes[str(key)] = [str(item).lower() for item in as_strings(value)]

    return normalized_classes, contract_rules


def classify_stage(stage: str, stage_classes: dict[str, list[str]]) -> list[str]:
    lower = stage.lower()
    classes = [name for name, terms in stage_classes.items() if any(term in lower for term in terms)]
    return classes or ["unknown"]


def infer_transition_type(left: str, right: str) -> str | None:
    left_terms = set(left.lower().replace("_", " ").split())
    right_terms = set(right.lower().replace("_", " ").split())
    combined = left_terms | right_terms
    combined_text = f"{left} {right}".lower()

    if any(term in combined_text for term in NETWORK_BOUNDARY_TERMS):
        if any(term in combined_text for term in CLIENT_TERMS):
            return "network_or_client_sync_boundary"
        return "network_sync_boundary"

    if any(term in combined_text for term in SERVER_TERMS) and any(term in combined_text for term in CLIENT_TERMS):
        return "server_to_client_boundary_candidate"

    return None


def infer_realm_transitions(stages: list[str]) -> list[dict[str, Any]]:
    transitions: list[dict[str, Any]] = []
    for left, right in zip(stages, stages[1:]):
        transition_type = infer_transition_type(left, right)
        if transition_type:
            transitions.append({
                "from_stage": left,
                "to_stage": right,
                "transition_type": transition_type,
                "confidence": "medium",
            })
    return transitions


def infer_sync_contracts(stages: list[str], contract_rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    stage_text = " ".join(stages).lower()
    contracts: list[dict[str, Any]] = []

    for rule in contract_rules:
        required_terms = [str(term).lower() for term in rule.get("required_terms", [])]
        if not required_terms:
            continue

        matched = [term for term in required_terms if term in stage_text]
        coverage = round(len(matched) / len(required_terms), 4)

        contracts.append({
            "contract_id": str(rule.get("id", "unnamed_contract")),
            "description": str(rule.get("description", "")),
            "matched_terms": matched,
            "required_terms": required_terms,
            "coverage": coverage,
            "status": "observed" if coverage == 1.0 else "partial" if matched else "absent",
        })

    return contracts


def infer_coupling_findings(chain: dict[str, Any], class_counts: Counter[str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    confidence = chain.get("confidence") or "unknown"

    def add(coupling_id: str, description: str, risk: str) -> None:
        findings.append({
            "coupling_id": coupling_id,
            "description": description,
            "risk": risk,
            "confidence": confidence,
        })

    if class_counts.get("inventory") and class_counts.get("metadata"):
        add(
            "inventory_and_metadata_propagation",
            "The chain contains both inventory propagation and metadata propagation concerns.",
            "desync_risk_if_one_path_refreshes_without_the_other",
        )

    if class_counts.get("client_apply") and class_counts.get("ui"):
        add(
            "client_apply_to_ui_refresh",
            "Client-side state application appears coupled to UI/presentation refresh.",
            "stale_presentation_if_refresh_hook_or_panel_update_is_missing",
        )

    if class_counts.get("network"):
        add(
            "network_sync_boundary",
            "The chain crosses at least one synchronization/network boundary.",
            "receiver_scope_payload_or_ordering_errors_can_create_client_desync",
        )

    if class_counts.get("persistence") and class_counts.get("network"):
        add(
            "persistence_to_network_sync",
            "The chain combines persistence lifecycle and network synchronization concerns.",
            "load_save_ordering_or_late_replication_can_surface_as_stale_client_state",
        )

    if class_counts.get("timer_scheduler") and (class_counts.get("network") or class_counts.get("persistence")):
        add(
            "scheduler_to_state_sync",
            "Timer/scheduler propagation appears near state synchronization or persistence.",
            "scheduled_side_effects_need_observability_and_runtime_order_validation",
        )

    return findings


def analyze_chain(
    chain: dict[str, Any],
    stage_classes: dict[str, list[str]],
    contract_rules: list[dict[str, Any]],
) -> dict[str, Any]:
    stages = extract_chain_stages(chain)

    classified_stages = [
        {"stage": stage, "classes": classify_stage(stage, stage_classes)}
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
        "realm_transitions": infer_realm_transitions(stages),
        "sync_contracts": infer_sync_contracts(stages, contract_rules),
        "coupling_findings": infer_coupling_findings(chain, class_counts),
    }


def summarize_global_findings(chain_analyses: list[dict[str, Any]]) -> dict[str, Any]:
    total_stage_classes: Counter[str] = Counter()
    coupling_counter: Counter[str] = Counter()
    contract_counter: Counter[str] = Counter()
    chains_by_confidence: dict[str, int] = defaultdict(int)
    chains_by_promotion_status: dict[str, int] = defaultdict(int)

    for analysis in chain_analyses:
        total_stage_classes.update(analysis.get("stage_class_counts", {}))
        chains_by_confidence[str(analysis.get("confidence") or "unknown")] += 1
        chains_by_promotion_status[str(analysis.get("promotion_status") or "unknown")] += 1

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


def build_architecture_findings(analyses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    for analysis in analyses:
        chain_id = analysis.get("chain_id") or analysis.get("source_id") or "unknown_chain"

        for coupling in analysis.get("coupling_findings", []):
            findings.append({
                "finding_id": f"{chain_id}:{coupling.get('coupling_id')}",
                "chain_id": chain_id,
                "type": "coupling",
                "description": coupling.get("description"),
                "risk": coupling.get("risk"),
                "confidence": coupling.get("confidence"),
                "source_path": analysis.get("source_path"),
            })

        for contract in analysis.get("sync_contracts", []):
            if contract.get("status") == "observed":
                findings.append({
                    "finding_id": f"{chain_id}:{contract.get('contract_id')}",
                    "chain_id": chain_id,
                    "type": "sync_contract",
                    "description": contract.get("description"),
                    "coverage": contract.get("coverage"),
                    "confidence": analysis.get("confidence"),
                    "source_path": analysis.get("source_path"),
                })

    return findings


def build_next_questions(analyses: list[dict[str, Any]]) -> list[str]:
    class_totals = Counter()
    for analysis in analyses:
        class_totals.update(analysis.get("stage_class_counts", {}))

    questions: list[str] = []

    if class_totals.get("ui"):
        questions.append("Which UI refresh stages are synchronization boundaries versus presentation-only refreshes?")
    if class_totals.get("network"):
        questions.append("Which network propagation stages should become explicit synchronization contracts?")
    if class_totals.get("inventory") and class_totals.get("metadata"):
        questions.append("Where should inventory membership and metadata synchronization be documented as separate contracts?")
    if class_totals.get("persistence"):
        questions.append("Which persistence stages need load/save ordering validation against runtime propagation topology?")
    if class_totals.get("timer_scheduler"):
        questions.append("Which scheduler/timer stages require runtime observability before architecture decisions?")

    return questions or ["Which additional promoted chains are needed before broader architecture synthesis is useful?"]


def build_intelligence(
    context_pack: dict[str, Any],
    input_path: Path,
    rule_config_path: Path | None,
) -> dict[str, Any]:
    if context_pack.get("schema") != "runtime_chain_context_pack.v1":
        raise ValueError(f"Expected runtime_chain_context_pack.v1, got {context_pack.get('schema')!r}")

    chains = context_pack.get("ranked_chains", [])
    if not isinstance(chains, list):
        raise ValueError("runtime_chain_context_pack ranked_chains must be a list")

    stage_classes, contract_rules = load_rule_config(rule_config_path)

    analyses = [
        analyze_chain(chain, stage_classes, contract_rules)
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
        "rule_config_artifact": str(rule_config_path) if rule_config_path else None,
        "analysis_rules": {
            "stage_classes": stage_classes,
            "contract_rules": contract_rules,
        },
        "summary": summarize_global_findings(analyses),
        "chain_analyses": analyses,
        "architecture_findings": build_architecture_findings(analyses),
        "next_questions": build_next_questions(analyses),
    }


def write_md(path: Path, intelligence: dict[str, Any]) -> None:
    lines: list[str] = []
    summary = intelligence["summary"]

    lines.append("# Architecture Intelligence V1")
    lines.append("")
    lines.append(f"- Schema: `{intelligence['schema']}`")
    lines.append(f"- Producer: `{intelligence['producer_script']}`")
    lines.append(f"- Source query: `{intelligence.get('source_query')}`")
    lines.append(f"- Input: `{intelligence.get('input_artifact')}`")
    lines.append(f"- Rule config: `{intelligence.get('rule_config_artifact')}`")
    lines.append(f"- Chains analyzed: `{summary.get('chains_total')}`")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    for title, values in [
        ("Chains by confidence", summary.get("chains_by_confidence", {})),
        ("Chains by promotion status", summary.get("chains_by_promotion_status", {})),
        ("Stage class totals", summary.get("stage_class_totals", {})),
        ("Observed coupling patterns", summary.get("observed_coupling_patterns", {})),
        ("Observed sync contracts", summary.get("observed_sync_contracts", {})),
    ]:
        lines.append(f"{title}:")
        lines.append("")
        if values:
            for key, value in values.items():
                lines.append(f"- `{key}`: `{value}`")
        else:
            lines.append("- none")
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
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument(
        "--context-pack",
        type=Path,
        default=Path("investigations/retrieval/runtime_chain_context_pack.json"),
    )
    parser.add_argument(
        "--rule-config",
        type=Path,
        default=None,
        help="Optional JSON file with stage_classes and contract_rules.",
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


def main() -> None:
    args = parse_args()
    workspace = args.workspace.resolve()

    context_pack_path = resolve_workspace_path(workspace, args.context_pack)
    out_json = resolve_workspace_path(workspace, args.out_json)
    out_md = resolve_workspace_path(workspace, args.out_md)
    rule_config = resolve_workspace_path(workspace, args.rule_config) if args.rule_config else None

    context_pack = read_json(context_pack_path)
    intelligence = build_intelligence(context_pack, context_pack_path, rule_config)

    write_json(out_json, intelligence)
    write_md(out_md, intelligence)

    print(f"Wrote JSON: {out_json}")
    print(f"Wrote MD:   {out_md}")
    print(f"Chains analyzed: {intelligence['summary']['chains_total']}")
    print(f"Findings: {len(intelligence['architecture_findings'])}")


if __name__ == "__main__":
    main()
