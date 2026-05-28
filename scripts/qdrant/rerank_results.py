from __future__ import annotations

from typing import Any

from scripts.qdrant.retrieval_intent import RetrievalIntent


NODE_TYPE_WEIGHTS = {
    "doctrine": 0.18,
    "plugin_summary": 0.16,
    "file_summary": 0.14,
    "plugin": 0.12,
    "file": 0.10,
    "hook_event": 0.14,
    "hook_emitter": 0.12,
    "hook_listener": 0.12,
    "network_message": 0.16,
    "network_operation": 0.14,
    "network_payload_operation": 0.10,
    "network_context": 0.10,
    "timer_operation": -0.10,
    "timer": -0.08,
}

DOC_TYPE_WEIGHTS = {
    "doctrine": 0.20,
    "plugin_topology": 0.14,
    "file_topology": 0.12,
    "runtime_node": 0.00,
}

HIGH_PRIORITY_SUBSYSTEMS = {
    "inventory",
    "storage",
    "gridinv",
    "vendor",
    "multichar",
    "healthproblems",
    "needs",
    "lightitems",
    "nextbots",
}


def _lower_set(values: set[str]) -> set[str]:
    return {v.lower() for v in values if v}


def rerank_results(
    results: list[dict[str, Any]],
    intent: RetrievalIntent,
    *,
    timer_noise_penalty: float = 0.18,
) -> list[dict[str, Any]]:
    intent_subsystems = _lower_set(intent.subsystems)
    intent_events = _lower_set(intent.events)
    intent_node_types = _lower_set(intent.node_types)
    intent_terms = _lower_set(set(intent.expanded_terms))

    reranked: list[dict[str, Any]] = []

    for result in results:
        payload = result.get("payload", {}) or result.get("metadata", {}) or {}
        text = (payload.get("text") or result.get("text") or "").lower()

        doc_type = str(payload.get("doc_type") or result.get("doc_type") or "").lower()
        node_type = str(payload.get("node_type") or result.get("node_type") or "").lower()
        plugin = str(payload.get("plugin") or result.get("plugin") or "").lower()
        subsystem = str(payload.get("subsystem") or result.get("subsystem") or "").lower()
        event = str(payload.get("event") or "").lower()
        realm = str(payload.get("realm") or result.get("realm") or "").lower()
        file_path = str(payload.get("file") or result.get("file") or "").lower()

        dense_score = float(result.get("score", 0.0))
        bonus = 0.0
        reasons: list[str] = []

        if doc_type in DOC_TYPE_WEIGHTS:
            value = DOC_TYPE_WEIGHTS[doc_type]
            bonus += value
            reasons.append(f"doc_type:{doc_type}:{value:+.2f}")

        if node_type in NODE_TYPE_WEIGHTS:
            value = NODE_TYPE_WEIGHTS[node_type]
            bonus += value
            reasons.append(f"node_type:{node_type}:{value:+.2f}")

        if node_type in intent_node_types:
            bonus += 0.08
            reasons.append("intent_node_type:+0.08")

        if plugin in intent_subsystems:
            bonus += 0.16
            reasons.append(f"plugin_match:{plugin}:+0.16")

        if subsystem in intent_subsystems:
            bonus += 0.16
            reasons.append(f"subsystem_match:{subsystem}:+0.16")

        for subsystem_name in intent_subsystems:
            if subsystem_name and subsystem_name in text:
                bonus += 0.04
                reasons.append(f"text_subsystem:{subsystem_name}:+0.04")
                break

        for event_name in intent_events:
            if event_name and event_name in text:
                bonus += 0.08
                reasons.append(f"text_event:{event_name}:+0.08")
                break

        if event and event in intent_events:
            bonus += 0.12
            reasons.append(f"event_match:{event}:+0.12")

        if intent.wants_network and node_type.startswith("network"):
            bonus += 0.14
            reasons.append("network_intent_match:+0.14")

        if intent.wants_network and any(
            term in text
            for term in ("netstream", "network", "sync", "desync", "realm crossing")
        ):
            bonus += 0.08
            reasons.append("network_text_match:+0.08")

        if intent.wants_doctrine and doc_type == "doctrine":
            bonus += 0.16
            reasons.append("doctrine_required:+0.16")

        if realm in {"client", "server", "shared"} and (
            "realm" in intent.domains or "realm crossing" in intent_terms
        ):
            bonus += 0.04
            reasons.append(f"realm_awareness:{realm}:+0.04")

        if plugin in HIGH_PRIORITY_SUBSYSTEMS or subsystem in HIGH_PRIORITY_SUBSYSTEMS:
            bonus += 0.05
            reasons.append("high_priority_subsystem:+0.05")

        if not intent.wants_timers and node_type in {"timer", "timer_operation", "timer_class", "timer_risk"}:
            bonus -= timer_noise_penalty
            reasons.append(f"timer_noise:-{timer_noise_penalty:.2f}")

        if not any(s in text or s == plugin or s == subsystem for s in intent_subsystems):
            if node_type in {"timer", "timer_operation"}:
                bonus -= 0.12
                reasons.append("unrelated_timer:-0.12")

        final_score = dense_score + bonus

        enriched = dict(result)
        enriched["rerank_score"] = final_score
        enriched["rerank_bonus"] = bonus
        enriched["rerank_reasons"] = reasons
        reranked.append(enriched)

    reranked.sort(key=lambda item: item["rerank_score"], reverse=True)
    return reranked