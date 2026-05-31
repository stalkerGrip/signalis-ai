from __future__ import annotations

import math
from typing import Any

from scripts.qdrant.retrieval_intent import RetrievalIntent


NODE_TYPE_WEIGHTS = {
    "doctrine": 0.18,
    "plugin_summary": 0.16,
    "file_summary": 0.14,
    "plugin": 0.12,
    "file": 0.10,
    "hook_event": 0.16,
    "hook_emitter": 0.14,
    "hook_listener": 0.14,
    "network_message": 0.17,
    "network_operation": 0.16,
    "network_payload_operation": 0.12,
    "network_context": 0.12,
    "timer_operation": -0.08,
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

CAUSAL_TERMS = {
    "hook.run": 0.18,
    "netstream.start": 0.18,
    "net.receive": 0.15,
    "net.start": 0.12,
    "setdata": 0.18,
    "sync": 0.10,
    "receiver": 0.10,
    "receivers": 0.10,
    "itemdatachanged": 0.18,
    "inventorydatachanged": 0.16,
    "nutinventoryadd": 0.16,
    "nutinventoryremove": 0.14,
    "invdata": 0.18,
    "setupanel": 0.10,
    "setuppanel": 0.10,
    "removeitem": 0.12,
    "additem": 0.12,
    "inventory:add": 0.14,
}

REALM_TERMS = {
    "client": 0.04,
    "server": 0.04,
    "shared": 0.03,
    "realm": 0.05,
}

BGE_MODEL_CACHE: dict[str, Any] = {}


def _lower_set(values: set[str]) -> set[str]:
    return {v.lower() for v in values if v}


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        result = float(value)
        if math.isnan(result) or math.isinf(result):
            return default
        return result
    except Exception:
        return default


def _normalize_bge_score(score: float) -> float:
    # FlagEmbedding normalized scores are usually already 0..1.
    # Clamp anyway to keep hybrid scoring stable.
    return max(0.0, min(1.0, score))


def _get_bge_reranker(model_name: str, use_fp16: bool) -> Any:
    cache_key = f"{model_name}|fp16={use_fp16}"
    if cache_key in BGE_MODEL_CACHE:
        return BGE_MODEL_CACHE[cache_key]

    from FlagEmbedding import FlagReranker

    reranker = FlagReranker(model_name, use_fp16=use_fp16)
    BGE_MODEL_CACHE[cache_key] = reranker
    return reranker


def apply_bge_scores(
    results: list[dict[str, Any]],
    query: str,
    *,
    model_name: str = "BAAI/bge-reranker-v2-m3",
    use_fp16: bool = False,
    batch_size: int = 8,
) -> list[dict[str, Any]]:
    if not results:
        return results

    reranker = _get_bge_reranker(model_name, use_fp16)

    pairs = []
    for result in results:
        payload = result.get("payload", {}) or {}
        text = payload.get("text") or result.get("text") or ""
        pairs.append([query, text])

    scores: list[float] = []
    for start in range(0, len(pairs), batch_size):
        batch = pairs[start:start + batch_size]
        batch_scores = reranker.compute_score(batch, normalize=True)

        if isinstance(batch_scores, float):
            scores.append(batch_scores)
        else:
            scores.extend([float(x) for x in batch_scores])

    enriched: list[dict[str, Any]] = []
    for result, score in zip(results, scores):
        item = dict(result)
        item["bge_score"] = _normalize_bge_score(score)
        enriched.append(item)

    return enriched


def compute_structural_score(
    result: dict[str, Any],
    intent: RetrievalIntent,
    *,
    timer_noise_penalty: float = 0.18,
) -> tuple[float, list[str]]:
    intent_subsystems = _lower_set(intent.subsystems)
    intent_events = _lower_set(intent.events)
    intent_node_types = _lower_set(intent.node_types)
    intent_terms = _lower_set(set(intent.expanded_terms))

    payload = result.get("payload", {}) or result.get("metadata", {}) or {}
    text = (payload.get("text") or result.get("text") or "").lower()

    doc_type = str(payload.get("doc_type") or result.get("doc_type") or "").lower()
    node_type = str(payload.get("node_type") or result.get("node_type") or "").lower()
    plugin = str(payload.get("plugin") or result.get("plugin") or "").lower()
    subsystem = str(payload.get("subsystem") or result.get("subsystem") or "").lower()
    event = str(payload.get("event") or "").lower()
    realm = str(payload.get("realm") or result.get("realm") or "").lower()
    file_path = str(payload.get("file") or result.get("file") or "").lower()

    score = 0.0
    reasons: list[str] = []

    if doc_type in DOC_TYPE_WEIGHTS:
        value = DOC_TYPE_WEIGHTS[doc_type]
        score += value
        reasons.append(f"doc_type:{doc_type}:{value:+.2f}")

    if node_type in NODE_TYPE_WEIGHTS:
        value = NODE_TYPE_WEIGHTS[node_type]
        score += value
        reasons.append(f"node_type:{node_type}:{value:+.2f}")

    if node_type in intent_node_types:
        score += 0.08
        reasons.append("intent_node_type:+0.08")

    if plugin in intent_subsystems:
        score += 0.18
        reasons.append(f"plugin_match:{plugin}:+0.18")

    if subsystem in intent_subsystems:
        score += 0.18
        reasons.append(f"subsystem_match:{subsystem}:+0.18")

    for subsystem_name in intent_subsystems:
        if subsystem_name and subsystem_name in text:
            score += 0.05
            reasons.append(f"text_subsystem:{subsystem_name}:+0.05")
            break

    for event_name in intent_events:
        if event_name and event_name in text:
            score += 0.10
            reasons.append(f"text_event:{event_name}:+0.10")
            break

    if event and event in intent_events:
        score += 0.14
        reasons.append(f"event_match:{event}:+0.14")

    if intent.wants_network and node_type.startswith("network"):
        score += 0.16
        reasons.append("network_intent_match:+0.16")

    if intent.wants_network and any(
        term in text
        for term in ("netstream", "network", "sync", "desync", "realm crossing", "net.receive", "net.start")
    ):
        score += 0.10
        reasons.append("network_text_match:+0.10")

    if intent.wants_doctrine and doc_type == "doctrine":
        score += 0.16
        reasons.append("doctrine_required:+0.16")

    if realm in {"client", "server", "shared"} and (
        "realm" in intent.domains or "realm crossing" in intent_terms
    ):
        score += 0.06
        reasons.append(f"realm_awareness:{realm}:+0.06")

    if plugin in HIGH_PRIORITY_SUBSYSTEMS or subsystem in HIGH_PRIORITY_SUBSYSTEMS:
        score += 0.06
        reasons.append("high_priority_subsystem:+0.06")

    if file_path:
        for subsystem_name in intent_subsystems:
            if subsystem_name and subsystem_name in file_path:
                score += 0.07
                reasons.append(f"file_subsystem:{subsystem_name}:+0.07")
                break

    if not intent.wants_timers and node_type in {"timer", "timer_operation", "timer_class", "timer_risk"}:
        score -= timer_noise_penalty
        reasons.append(f"timer_noise:-{timer_noise_penalty:.2f}")

    if not any(s in text or s == plugin or s == subsystem for s in intent_subsystems):
        if node_type in {"timer", "timer_operation"}:
            score -= 0.12
            reasons.append("unrelated_timer:-0.12")

    return score, reasons


def compute_causal_score(result: dict[str, Any], intent: RetrievalIntent) -> tuple[float, list[str]]:
    payload = result.get("payload", {}) or result.get("metadata", {}) or {}
    text = (payload.get("text") or result.get("text") or "").lower()
    node_type = str(payload.get("node_type") or result.get("node_type") or "").lower()

    score = 0.0
    reasons: list[str] = []

    for term, weight in CAUSAL_TERMS.items():
        if term in text:
            score += weight
            reasons.append(f"causal:{term}:{weight:+.2f}")

    if intent.wants_network and any(term in text for term in ("netstream", "net.receive", "net.start", "send", "receive")):
        score += 0.14
        reasons.append("causal_network_flow:+0.14")

    if node_type in {"hook_emitter", "hook_listener", "hook_event"}:
        score += 0.08
        reasons.append("hook_chain_candidate:+0.08")

    if node_type in {"network_message", "network_operation", "network_payload_operation", "network_context"}:
        score += 0.08
        reasons.append("network_chain_candidate:+0.08")

    if any(term in text for term in ("setdata", "datachanged", "item.data", "inventory.items", "invdata")):
        score += 0.14
        reasons.append("state_mutation_or_sync:+0.14")

    if any(term in text for term in REALM_TERMS):
        score += 0.04
        reasons.append("realm_signal:+0.04")

    return min(score, 1.0), reasons


def rerank_results(
    results: list[dict[str, Any]],
    intent: RetrievalIntent,
    *,
    query: str | None = None,
    use_bge: bool = False,
    bge_model: str = "BAAI/bge-reranker-v2-m3",
    bge_fp16: bool = False,
    bge_batch_size: int = 8,
    timer_noise_penalty: float = 0.18,
    dense_weight: float = 0.35,
    bge_weight: float = 0.25,
    structural_weight: float = 0.25,
    causal_weight: float = 0.15,
) -> list[dict[str, Any]]:
    working = [dict(r) for r in results]

    if use_bge and query:
        try:
            working = apply_bge_scores(
                working,
                query,
                model_name=bge_model,
                use_fp16=bge_fp16,
                batch_size=bge_batch_size,
            )
        except Exception as exc:
            for item in working:
                item["bge_score"] = None
                item["bge_error"] = repr(exc)

    reranked: list[dict[str, Any]] = []

    for result in working:
        dense_score = _safe_float(result.get("score", 0.0))
        bge_score = result.get("bge_score")
        bge_score_float = _safe_float(bge_score, 0.0)

        structural_score, structural_reasons = compute_structural_score(
            result,
            intent,
            timer_noise_penalty=timer_noise_penalty,
        )
        causal_score, causal_reasons = compute_causal_score(result, intent)

        # Dense scores from Qdrant are often cosine-ish. Keep them bounded.
        dense_component = max(0.0, min(1.0, dense_score))

        final_score = (
            dense_weight * dense_component
            + bge_weight * bge_score_float
            + structural_weight * structural_score
            + causal_weight * causal_score
        )

        enriched = dict(result)
        enriched["rerank_score"] = final_score
        enriched["rerank_components"] = {
            "dense": dense_component,
            "bge": bge_score,
            "structural": structural_score,
            "causal": causal_score,
            "weights": {
                "dense": dense_weight,
                "bge": bge_weight,
                "structural": structural_weight,
                "causal": causal_weight,
            },
        }
        enriched["rerank_bonus"] = structural_score + causal_score
        enriched["rerank_reasons"] = structural_reasons + causal_reasons
        reranked.append(enriched)

    reranked.sort(key=lambda item: item["rerank_score"], reverse=True)
    return reranked