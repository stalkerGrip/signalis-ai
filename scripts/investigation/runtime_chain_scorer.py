from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ChainScore:
    score: float
    confidence: str
    reasons: List[str]
    missing_steps: List[str]


def _blob(step: Dict[str, Any]) -> str:
    return "\n".join(str(step.get(k) or "") for k in (
        "label", "summary", "text", "fragment", "source_text",
        "source_file", "file", "path", "realm", "step_type",
    ))


def _has_server(step: Dict[str, Any]) -> bool:
    b = _blob(step).lower().replace("\\", "/")
    return (
        step.get("realm") == "server"
        or "/sv_" in b
        or b.endswith("sv_hooks.lua")
        or "plugins/gridinv/sv_transfer.lua" in b
        or "server" in b
    )


def _has_client(step: Dict[str, Any]) -> bool:
    b = _blob(step).lower().replace("\\", "/")
    return (
        step.get("realm") == "client"
        or "/cl_" in b
        or "cl_networking.lua" in b
        or "cl_vendor.lua" in b
        or "client" in b
    )


def _has_network(step: Dict[str, Any]) -> bool:
    b = _blob(step)
    bl = b.lower()

    return any(x.lower() in bl for x in (
        "netstream",
        "net.receive",
        "net.start",
        "invdata",
        "nutinventoryadd",
        "nutinventorydata",
        "nutinventoryinit",
        "item metadata sync",
        "item-level data sync",
        "sync boundary",
        "synchronization boundary",
        "item:sync",
        "item.sync",
        ":sync(",
        "setdata",
        "itemdatachanged",
        "inventoryitemdatachanged",
    ))


def _has_hook(step: Dict[str, Any]) -> bool:
    b = _blob(step)
    return any(x in b for x in (
        "hook.Run",
        "ItemDataChanged",
        "InventoryDataChanged",
        "InventoryItemDataChanged",
        "VendorItem",
    ))


def score_step(step: Dict[str, Any]) -> float:
    b = _blob(step)
    score = 0.10

    if step.get("validated"):
        score += 0.25
    if step.get("targeted_validation"):
        score += 0.25
    if step.get("source_file"):
        score += 0.10
    if step.get("line_start"):
        score += 0.05
    if _has_server(step):
        score += 0.10
    if _has_client(step):
        score += 0.10
    if _has_network(step):
        score += 0.15
    if _has_hook(step):
        score += 0.10

    for term in ("setData", "vendorSPrice", "invData", "ItemDataChanged", "populateItems"):
        if term in b:
            score += 0.08

    return min(round(score, 4), 1.0)


def score_chain(chain: Dict[str, Any]) -> ChainScore:
    steps = chain.get("steps") or []
    if not steps:
        return ChainScore(0.0, "low", ["No steps reconstructed."], ["runtime steps"])

    step_scores = [score_step(s) for s in steps]
    base = sum(step_scores) / len(step_scores)

    has_server = any(_has_server(s) for s in steps)
    has_client = any(_has_client(s) for s in steps)
    has_network = any(_has_network(s) for s in steps)
    has_hook = any(_has_hook(s) for s in steps)
    has_validation = any(s.get("validated") or s.get("targeted_validation") for s in steps)

    missing: List[str] = []
    reasons: List[str] = []

    if has_server:
        reasons.append("Server-side ownership/mutation evidence is present.")
    else:
        missing.append("server-side ownership or mutation step")

    if has_client:
        reasons.append("Client-side receiver/UI evidence is present.")
    else:
        missing.append("client-side presentation/receiver step")

    if has_network:
        reasons.append("Network/item sync boundary evidence is present.")
    else:
        missing.append("network or sync boundary")

    if has_hook:
        reasons.append("Hook/event/UI refresh propagation evidence is present.")
    else:
        missing.append("hook/event propagation boundary")

    if has_validation:
        reasons.append("Validated evidence is present.")
    else:
        missing.append("targeted source validation confirmation")

    completeness = (5 - len(missing)) / 5
    final = round(min(base * 0.65 + completeness * 0.35, 1.0), 4)

    if missing:
        final = min(final, 0.74)

    if not missing and final >= 0.70:
        confidence = "high"
    elif final >= 0.50:
        confidence = "medium"
    else:
        confidence = "low"

    return ChainScore(final, confidence, reasons, missing)