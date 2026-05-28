from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class RetrievalIntent:
    query: str
    domains: set[str] = field(default_factory=set)
    subsystems: set[str] = field(default_factory=set)
    events: set[str] = field(default_factory=set)
    node_types: set[str] = field(default_factory=set)
    wants_timers: bool = False
    wants_network: bool = False
    wants_doctrine: bool = True
    expanded_terms: list[str] = field(default_factory=list)


SUBSYSTEM_ALIASES = {
    "inventory": {"inventory", "gridinv", "storage"},
    "storage": {"storage", "inventory", "gridinv"},
    "vendor": {"vendor", "inventory"},
    "character": {"character", "multichar"},
    "health": {"healthproblems", "needs", "hud"},
}

EVENT_ALIASES = {
    "character load": {
        "CharacterLoaded",
        "PlayerLoadedChar",
        "PlayerLoadout",
        "PostPlayerLoadout",
        "CharacterPreSave",
    },
    "save": {
        "SaveData",
        "LoadData",
        "PostLoadData",
        "PersistenceSave",
        "PersistenceLoad",
        "CharacterPreSave",
    },
    "inventory ui": {
        "CreateNewInventoryPanel",
        "CreateTargetNewInventoryPanel",
        "OnCreateStoragePanel",
        "ItemTransfered",
    },
}

NETWORK_TERMS = {
    "desync",
    "sync",
    "network",
    "netstream",
    "net",
    "message",
    "protocol",
    "ui update",
}

TIMER_TERMS = {
    "timer",
    "scheduler",
    "delay",
    "tick",
    "loop",
    "think",
    "fps",
    "performance",
    "lag",
}


def classify_retrieval_intent(query: str) -> RetrievalIntent:
    q = query.lower()
    intent = RetrievalIntent(query=query)

    for key, subsystems in SUBSYSTEM_ALIASES.items():
        if key in q:
            intent.subsystems.update(subsystems)

    for key, events in EVENT_ALIASES.items():
        if key in q:
            intent.events.update(events)

    intent.wants_network = any(term in q for term in NETWORK_TERMS)
    intent.wants_timers = any(term in q for term in TIMER_TERMS)

    if intent.wants_network:
        intent.node_types.update({
            "network_message",
            "network_operation",
            "network_payload_operation",
            "network_context",
        })

    if intent.wants_timers:
        intent.node_types.update({
            "timer",
            "timer_operation",
            "timer_class",
            "timer_risk",
        })

    intent.node_types.update({
        "plugin",
        "plugin_summary",
        "file",
        "file_summary",
        "hook_event",
        "hook_emitter",
        "hook_listener",
    })

    if "desync" in q or "sync" in q:
        intent.domains.update({"realm", "networking", "ui_sync"})
        intent.wants_doctrine = True

    expanded = set()
    expanded.update(intent.subsystems)
    expanded.update(intent.events)
    expanded.update(intent.node_types)

    if intent.wants_network:
        expanded.update({
            "netstream.Start",
            "netstream.Hook",
            "inventoryOpen",
            "invAct",
            "client UI",
            "server authoritative",
            "realm crossing",
        })

    intent.expanded_terms = sorted(expanded)
    return intent


def build_expanded_query(intent: RetrievalIntent) -> str:
    parts = [intent.query]
    if intent.expanded_terms:
        parts.append(" ".join(intent.expanded_terms))
    return " ".join(parts)
