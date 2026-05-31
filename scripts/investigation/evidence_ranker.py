from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Any


TEXT_KEYS = (
    "text",
    "content",
    "fragment",
    "snippet",
    "body",
    "source_text",
    "matched_text",
    "evidence",
    "summary",
)


RUNTIME_CHAIN_TERMS = {
    "plugins/gridinv/sv_transfer.lua": 3.0,
    "plugins\\gridinv\\sv_transfer.lua": 3.0,
    "vendorSellItem": 2.5,
    "oldInventory.vendor": 2.2,
    "setData": 1.4,
    "vendorSPrice": 1.5,
    "vendorBPrice": 1.1,
    "vendorQty": 1.1,
    "vendorMQty": 1.1,
    "syncItemAdded": 1.6,
    "nutInventoryAdd": 1.4,
    "item:sync": 1.3,
    "invData": 1.5,
    "ItemDataChanged": 1.5,
    "InventoryItemDataChanged": 1.2,
    "populateItems": 1.2,
}


NETWORK_TERMS = (
    "netstream",
    "net.receive",
    "net.start",
    "net.send",
    "nutinventoryadd",
    "invdata",
)


LOW_VALUE_TERMS = (
    "project_structure",
    "readme",
    "directory tree",
    "summary only",
    "generated:",
)


LEGACY_OR_SECONDARY_VENDOR_TERMS = (
    "RemoveReceiverFromVendor",
    "VendorItemSetData",
)


@dataclass
class RankedEvidence:
    score: float
    reasons: list[str]
    item: dict[str, Any]


def get_text(item: dict[str, Any]) -> str:
    parts: list[str] = []

    for key in TEXT_KEYS:
        value = item.get(key)
        if isinstance(value, str):
            parts.append(value)

    for key in ("source", "file", "path"):
        value = item.get(key)
        if isinstance(value, str):
            parts.append(value)

    return "\n".join(parts)


def normalized_path(item: dict[str, Any]) -> str:
    raw = str(item.get("path") or item.get("file") or item.get("source") or "")
    return raw.replace("\\", "/").lower()


def extract_line(item: dict[str, Any]) -> int | None:
    for key in ("line", "line_start", "start_line"):
        value = item.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            return int(value)

    text = get_text(item)
    match = re.search(r"^\s*(\d+)\s*:", text, flags=re.MULTILINE)
    if match:
        return int(match.group(1))

    return None


def line_bucket(item: dict[str, Any], width: int = 25) -> int:
    line = extract_line(item)
    if line is None:
        return -1
    return line // width


def normalized_text_fingerprint(text: str) -> str:
    compact = re.sub(r"\s+", " ", text.lower()).strip()
    compact = re.sub(r"^\d+\s*:\s*", "", compact)
    compact = compact[:500]
    return hashlib.sha1(compact.encode("utf-8", errors="ignore")).hexdigest()[:16]


def evidence_cluster_key(item: dict[str, Any]) -> str:
    path = normalized_path(item)
    text = get_text(item)
    bucket = line_bucket(item)

    function = "unknown"
    function_match = re.search(r"function\s+([A-Za-z0-9_:.]+)", text)
    if function_match:
        function = function_match.group(1).lower()

    return f"{path}:{function}:{bucket}"


def dedupe_ranked_evidence(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Keeps the best fragment per path/function/line-window cluster.

    This specifically collapses repeated overlapping source windows such as:
    same file + same function + nearby lines.
    """
    best_by_cluster: dict[str, dict[str, Any]] = {}

    for item in items:
        key = evidence_cluster_key(item)
        current = best_by_cluster.get(key)

        if current is None:
            best_by_cluster[key] = item
            continue

        if float(item.get("evidence_rank_score", 0)) > float(current.get("evidence_rank_score", 0)):
            best_by_cluster[key] = item

    return sorted(
        best_by_cluster.values(),
        key=lambda entry: float(entry.get("evidence_rank_score", 0)),
        reverse=True,
    )


def rank_evidence(item: dict[str, Any], question: str = "") -> RankedEvidence:
    text = get_text(item)
    lowered = text.lower()
    path = normalized_path(item)

    score = 0.0
    reasons: list[str] = []

    for term, weight in RUNTIME_CHAIN_TERMS.items():
        if term.lower() in lowered or term.lower() in path:
            score += weight
            reasons.append(f"runtime_chain_term:{term}")

    if "server" in lowered and "client" in lowered:
        score += 0.8
        reasons.append("realm_transition")

    if any(term in lowered for term in NETWORK_TERMS):
        score += 0.9
        reasons.append("network_propagation")

    if "hook.run" in lowered or "hook:" in lowered:
        score += 0.5
        reasons.append("hook_propagation")

    if "plugins/gridinv/sv_transfer.lua" in path:
        score += 2.5
        reasons.append("authoritative_purchase_transfer_file")

    if "gamemode/core/meta/inventory/sv_base_inventory.lua" in path:
        score += 1.2
        reasons.append("inventory_membership_sync_file")

    if "gamemode/core/libs/item" in path:
        score += 1.5
        reasons.append("item_metadata_sync_file")

    if "plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua" in path:
        score += 1.2
        reasons.append("grid_inventory_ui_refresh_file")

    if "plugins/vendor/entities/entities/nut_vendor/init.lua" in path:
        score += 0.2
        reasons.append("vendor_entity_context_file")

    for term in LEGACY_OR_SECONDARY_VENDOR_TERMS:
        if term.lower() in lowered:
            score -= 1.2
            reasons.append(f"secondary_vendor_flow_penalty:{term}")

    for term in LOW_VALUE_TERMS:
        if term in lowered:
            score -= 2.0
            reasons.append(f"low_value:{term}")

    if question:
        for token in question.lower().split():
            clean = re.sub(r"[^a-z0-9_]", "", token)
            if len(clean) >= 5 and clean in lowered:
                score += 0.05

    return RankedEvidence(score=round(score, 3), reasons=reasons, item=item)


def rank_evidence_list(items: list[dict[str, Any]], question: str = "") -> list[dict[str, Any]]:
    ranked = [rank_evidence(item, question) for item in items]

    output: list[dict[str, Any]] = []
    for entry in ranked:
        enriched = dict(entry.item)
        enriched["evidence_rank_score"] = entry.score
        enriched["evidence_rank_reasons"] = entry.reasons
        enriched["evidence_cluster_key"] = evidence_cluster_key(entry.item)
        enriched["evidence_text_fingerprint"] = normalized_text_fingerprint(get_text(entry.item))
        output.append(enriched)

    output.sort(key=lambda entry: float(entry.get("evidence_rank_score", 0)), reverse=True)
    return dedupe_ranked_evidence(output)