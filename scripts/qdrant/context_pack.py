from __future__ import annotations

from collections import defaultdict
from typing import Any


def _payload(result: Any) -> dict[str, Any]:
    if isinstance(result, dict):
        return result.get("payload", {}) or {}
    return result.payload or {}


def _score(result: Any) -> float:
    if isinstance(result, dict):
        return float(result.get("rerank_score", result.get("score", 0.0)))
    return float(result.score)


def _text(result: Any) -> str:
    payload = _payload(result)
    return payload.get("text", "")


def build_context_pack(results: list[Any], query: str) -> str:
    groups: dict[str, list[Any]] = defaultdict(list)

    for result in results:
        payload = _payload(result)
        node_type = payload.get("node_type")
        doc_type = payload.get("doc_type")
        text = _text(result).lower()

        if node_type in {"hook_event", "hook_emitter", "hook_listener"}:
            groups["Lifecycle / Hook Signals"].append(result)
        elif node_type in {"network_message", "network_operation", "network_context", "network_payload_operation"}:
            groups["Network / Sync Signals"].append(result)
        elif node_type in {"timer", "timer_operation", "timer_class", "timer_risk"}:
            groups["Timer / Scheduler Signals"].append(result)
        elif doc_type in {"plugin_topology"} or node_type in {"plugin", "plugin_summary"}:
            groups["Subsystem / Plugin Hubs"].append(result)
        elif doc_type in {"file_topology"} or node_type == "file":
            groups["High-Value Files"].append(result)
        elif doc_type == "doctrine":
            groups["Doctrine Context"].append(result)
        elif "inventory" in text or "storage" in text or "vendor" in text:
            groups["Inventory / Storage Related"].append(result)
        else:
            groups["Other Relevant Results"].append(result)

    lines: list[str] = [
        "# Investigation Context Pack",
        "",
        f"Query: `{query}`",
        "",
        "## Context Groups",
        "",
    ]

    for group_name, items in groups.items():
        lines.append(f"## {group_name}")
        lines.append("")

        for idx, result in enumerate(items[:8], start=1):
            payload = _payload(result)
            text = _text(result)
            score = _score(result)

            source_id = payload.get("source_id")
            doc_type = payload.get("doc_type")
            node_type = payload.get("node_type")
            plugin = payload.get("plugin")
            subsystem = payload.get("subsystem")
            realm = payload.get("realm")
            file = payload.get("file")

            first_line = text.splitlines()[0] if text else ""

            lines.extend([
                f"### {idx}. {first_line}",
                "",
                f"- Score: `{score:.4f}`",
                f"- Source ID: `{source_id}`",
                f"- Doc type: `{doc_type}`",
                f"- Node type: `{node_type}`",
                f"- Plugin: `{plugin}`",
                f"- Subsystem: `{subsystem}`",
                f"- Realm: `{realm}`",
                f"- File: `{file}`",
                "",
            ])

        lines.append("")

    lines.extend([
        "## Initial Propagation Hypothesis",
        "",
        "```text",
        "CharacterLoaded",
        "→ PlayerLoadedChar / PlayerLoadout",
        "→ inventory initialization / sync",
        "→ inventoryOpen",
        "→ inventorySetPanelStatus",
        "→ client inventory UI state",
        "```",
        "",
        "## Investigation Notes",
        "",
        "- Validate lifecycle ordering before assuming desync cause.",
        "- Treat network messages as synchronization contracts.",
        "- Treat timers/debounce state as runtime propagation, not noise.",
        "- Use raw Lua only when exact behavior needs confirmation.",
        "",
    ])

    return "\n".join(lines)