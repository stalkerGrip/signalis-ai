from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


EVENT_RE = re.compile(r'hook\.Run\(\s*["\']([^"\']+)["\']')
NETSTREAM_START_RE = re.compile(r'netstream\.Start\(\s*([^,\n\)]+)')
NETSTREAM_HOOK_RE = re.compile(r'netstream\.Hook\(\s*["\']([^"\']+)["\']')
NET_START_RE = re.compile(r'net\.Start\(\s*["\']([^"\']+)["\']')
NET_RECEIVE_RE = re.compile(r'net\.Receive\(\s*["\']([^"\']+)["\']')
SETDATA_RE = re.compile(r':setData\(\s*["\']([^"\']+)["\']')
SYNC_RE = re.compile(r':sync\(')
TIMER_RE = re.compile(r'timer\.(Create|Simple|Remove|Exists)\(')


LIFECYCLE_EVENTS = {
    "PrePlayerLoadedChar",
    "PlayerLoadedChar",
    "CharacterLoaded",
    "PlayerLoadout",
    "PostPlayerLoadout",
    "InventoryInitialized",
    "ItemInitialized",
    "LoadData",
    "SaveData",
    "PostLoadData",
    "CharacterPreSave",
    "CharacterPostSave",
}

UI_NETWORK_NAMES = {
    "inventoryOpen",
    "inventorySetPanelStatus",
    "vendorTradeInterface",
    "inventoryCloseOnAction",
    "removeReceiverFromVendor",
    "storageInventory",
    "storageOpen",
}


@dataclass
class RuntimeOccurrence:
    file: str | None
    line: int | None
    realm: str
    evidence: str


@dataclass
class RuntimeFact:
    fact_key: str
    category: str
    kind: str
    name: str
    confidence: str
    occurrences: list[RuntimeOccurrence] = field(default_factory=list)


def infer_realm(path: str | None) -> str:
    if not path:
        return "unknown"

    normalized = path.replace("\\", "/").lower()
    name = Path(normalized).name

    if name.startswith("sv_"):
        return "server"
    if name.startswith("cl_"):
        return "client"
    if name.startswith("sh_"):
        return "shared"

    return "unknown"


def iter_evidence_nodes(obj: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            keys = set(value.keys())
            if {
                "file",
                "path",
                "line",
                "line_number",
                "snippet",
                "text",
                "matched_text",
                "content",
                "source",
            } & keys:
                found.append(value)

            for child in value.values():
                walk(child)

        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(obj)
    return found


def get_text(node: dict[str, Any]) -> str:
    for key in ("snippet", "matched_text", "text", "content", "source", "line_text"):
        val = node.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return ""


def get_file(node: dict[str, Any]) -> str | None:
    for key in ("file", "path", "source_file", "relative_path"):
        val = node.get(key)
        if isinstance(val, str) and val.strip():
            return val.replace("\\", "/")
    return None


def get_line(node: dict[str, Any]) -> int | None:
    for key in ("line", "line_number", "start_line"):
        val = node.get(key)
        if isinstance(val, int):
            return val
        if isinstance(val, str) and val.isdigit():
            return int(val)
    return None


def clean_netstream_arg(raw: str) -> str:
    raw = raw.strip()

    # Handles snippets like:
    # 113:     "inventoryOpen"
    if '"' in raw or "'" in raw:
        match = re.search(r'["\']([^"\']+)["\']', raw)
        if match:
            return match.group(1)

    return raw.strip()


def classify_category(category: str, name: str) -> str:
    if category == "event" and name in LIFECYCLE_EVENTS:
        return "lifecycle"

    if category == "network" and name in UI_NETWORK_NAMES:
        return "ui"

    return category


def add_fact(
    facts: dict[str, RuntimeFact],
    category: str,
    kind: str,
    name: str,
    confidence: str,
    occurrence: RuntimeOccurrence,
) -> None:
    category = classify_category(category, name)
    fact_key = f"{category}:{kind}:{name}"

    if fact_key not in facts:
        facts[fact_key] = RuntimeFact(
            fact_key=fact_key,
            category=category,
            kind=kind,
            name=name,
            confidence=confidence,
            occurrences=[],
        )

    # Deduplicate identical occurrence/evidence pairs.
    existing = {
        (o.file, o.line, o.realm, o.evidence)
        for o in facts[fact_key].occurrences
    }

    candidate = (
        occurrence.file,
        occurrence.line,
        occurrence.realm,
        occurrence.evidence,
    )

    if candidate not in existing:
        facts[fact_key].occurrences.append(occurrence)


def extract_facts_from_node(
    node: dict[str, Any],
    facts: dict[str, RuntimeFact],
) -> None:
    text = get_text(node)
    if not text:
        return

    file = get_file(node)
    line = get_line(node)
    realm = infer_realm(file)

    occurrence = RuntimeOccurrence(
        file=file,
        line=line,
        realm=realm,
        evidence=text,
    )

    for match in EVENT_RE.finditer(text):
        add_fact(facts, "event", "hook_emit", match.group(1), "high", occurrence)

    for match in NET_RECEIVE_RE.finditer(text):
        add_fact(facts, "network", "net_receive", match.group(1), "high", occurrence)

    for match in NET_START_RE.finditer(text):
        add_fact(facts, "network", "net_send", match.group(1), "high", occurrence)

    for match in NETSTREAM_HOOK_RE.finditer(text):
        add_fact(facts, "network", "netstream_receive", match.group(1), "high", occurrence)

    for match in NETSTREAM_START_RE.finditer(text):
        name = clean_netstream_arg(match.group(1))
        add_fact(facts, "network", "netstream_send", name, "medium", occurrence)

    for match in SETDATA_RE.finditer(text):
        add_fact(facts, "state_mutation", "item_set_data", match.group(1), "high", occurrence)

    if SYNC_RE.search(text):
        add_fact(facts, "sync", "sync_call", "sync", "medium", occurrence)

    for match in TIMER_RE.finditer(text):
        add_fact(facts, "timer", f"timer_{match.group(1).lower()}", match.group(1), "medium", occurrence)


def write_md(path: Path, facts: list[RuntimeFact]) -> None:
    lines = [
        "# Runtime Facts",
        "",
        f"- Unique facts: `{len(facts)}`",
        "",
    ]

    by_category: dict[str, list[RuntimeFact]] = {}
    for fact in facts:
        by_category.setdefault(fact.category, []).append(fact)

    for category in sorted(by_category):
        lines += [
            f"## Category: `{category}`",
            "",
        ]

        for fact in sorted(by_category[category], key=lambda f: f.fact_key):
            lines += [
                f"### {fact.fact_key}",
                "",
                f"- Kind: `{fact.kind}`",
                f"- Name: `{fact.name}`",
                f"- Confidence: `{fact.confidence}`",
                f"- Occurrences: `{len(fact.occurrences)}`",
                "",
            ]

            for occurrence in fact.occurrences[:5]:
                lines += [
                    f"- File: `{occurrence.file}`",
                    f"  Line: `{occurrence.line}`",
                    f"  Realm: `{occurrence.realm}`",
                    "",
                    "```text",
                    occurrence.evidence,
                    "```",
                    "",
                ]

            if len(fact.occurrences) > 5:
                lines.append(f"_Additional occurrences omitted: {len(fact.occurrences) - 5}_")
                lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build deduplicated normalized runtime facts from targeted source validation output."
    )
    parser.add_argument("--source-validation", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)

    args = parser.parse_args()

    data = json.loads(args.source_validation.read_text(encoding="utf-8"))
    nodes = iter_evidence_nodes(data)

    facts_by_key: dict[str, RuntimeFact] = {}
    for node in nodes:
        extract_facts_from_node(node, facts_by_key)

    facts = sorted(facts_by_key.values(), key=lambda f: f.fact_key)

    payload = {
        "schema": "runtime_facts.v2",
        "source_validation": str(args.source_validation),
        "evidence_nodes": len(nodes),
        "unique_facts_count": len(facts),
        "facts": [
            {
                **asdict(fact),
                "occurrences": [asdict(o) for o in fact.occurrences],
            }
            for fact in facts
        ],
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    write_md(args.out_md, facts)

    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")
    print(f"Evidence nodes: {len(nodes)}")
    print(f"Unique facts:   {len(facts)}")


if __name__ == "__main__":
    main()