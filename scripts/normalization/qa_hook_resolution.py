#!/usr/bin/env python3
"""
QA for Normalization Phase V1 hook symbol resolution.

Reads:
  manifests/normalized/resolved_hook_runs.json
  manifests/normalized/unresolved_hook_runs.json
  manifests/normalized/plugin_hook_edges.json

Writes:
  manifests/normalized/qa_hook_resolution.json
  manifests/normalized/qa_hook_resolution.md

Purpose:
  Tell whether unresolved hook runs are extractor problems, normalizer problems,
  or expected non-plugin/core/NutScript/GMod hook names.

Usage:
  python scripts/normalization/qa_hook_resolution.py --workspace E:/signalis_ai --write

Optional:
  python scripts/normalization/qa_hook_resolution.py --workspace E:/signalis_ai --source-root E:/steam/.../gamemodes/signalis --nutscript-root E:/steam/.../gamemodes/nutscript --write
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


# Conservative seed sets. These are NOT final truth; they only help triage.
# Anything classified here still remains unresolved from plugin-method linking.
GMOD_BUILTIN_HOOKS = {
    "Think", "Tick", "Initialize", "ShutDown",
    "PlayerInitialSpawn", "PlayerSpawn", "PlayerDeath", "PlayerDisconnected",
    "PlayerUse", "PlayerSay", "PlayerButtonDown", "PlayerButtonUp",
    "KeyPress", "KeyRelease", "CanPlayerSuicide",
    "EntityTakeDamage", "EntityRemoved", "OnEntityCreated",
    "SetupMove", "Move", "FinishMove", "CreateMove",
    "StartCommand", "PlayerTick",
    "HUDPaint", "HUDShouldDraw", "PreDrawHUD", "PostDrawHUD",
    "RenderScreenspaceEffects", "PreDrawOpaqueRenderables", "PostDrawOpaqueRenderables",
    "CalcView", "ShouldDrawLocalPlayer",
    "PreDrawViewModel", "PostDrawViewModel",
    "OnPlayerChat", "ChatText",
    "InitPostEntity", "PostCleanupMap",
    "PlayerCanHearPlayersVoice", "PlayerCanSeePlayersChat",
    "PhysgunPickup", "CanTool", "PlayerSpawnProp", "PlayerSpawnedProp",
    "PlayerSpawnSENT", "PlayerSpawnedSENT",
    "PlayerSpawnNPC", "PlayerSpawnedNPC",
    "PlayerSpawnSWEP", "PlayerGiveSWEP",
    "CanProperty", "ContextMenuOpen", "ContextMenuClose",
    "PopulateToolMenu", "AddToolMenuCategories",
}

NUTSCRIPT_LIKELY_HOOKS = {
    "CanPlayerAccessDoor", "CanPlayerUseDoor", "PlayerUseDoor",
    "CanPlayerUseCharacter", "CanPlayerCreateCharacter", "CanPlayerDeleteCharacter",
    "OnCharCreated", "OnCharLoaded", "OnCharDeleted", "OnCharVarChanged",
    "CharacterLoaded", "CharacterPreSave", "CharacterPostSave",
    "GetDefaultCharName", "GetStartAttribPoints", "GetPlayerDeathSound",
    "CanPlayerViewInventory", "CanTransferItem", "CanItemBeTransfered",
    "CanPlayerDropItem", "CanPlayerTakeItem", "OnItemTransferred",
    "CanPlayerInteractItem", "CanItemInteraction", "OnItemSpawned",
    "CanPlayerUseVendor", "CanPlayerTradeWithVendor",
    "CanPlayerJoinClass", "CanPlayerJoinFaction", "OnPlayerJoinClass",
    "CanPlayerUseBusiness", "CanPlayerUseFlags",
    "PlayerLoadedChar", "PlayerLoadout", "PlayerMessageSend",
    "AdjustCreationPayload", "LoadData", "SaveData",
    "PostLoadData", "PostSaveData",
}

# Project-specific likely schema/core/domain events seen in Signalis-style NutScript.
# These are useful triage buckets, not final canonical registries.
PROJECT_CORE_LIKELY = {
    "StorageRestored", "StorageEntityRemoved", "StorageItemRemoved",
    "StorageItemAdded", "OnStorageOpened", "OnStorageClosed",
    "ContainerPasswordChanged",
    "CanPlayerBustLock", "OnLockBusted",
    "OnPlayerAreaChanged", "OnAreaCreated", "OnAreaRemoved",
    "OnRecipeLearned", "CanPlayerCraft",
}

SCHEMA_HINT_PREFIXES = (
    "CanPlayer", "Player", "OnPlayer", "OnChar", "Character",
    "GetDefault", "GetStart", "Adjust", "Load", "Save", "PostLoad", "PostSave",
)

DOMAIN_HINT_WORDS = (
    "Disease", "Infection", "Radiation", "Storage", "Lock", "Door", "Area",
    "Craft", "Recipe", "Vendor", "Inventory", "Item", "Container", "Terminal",
    "Business", "Faction", "Class", "Attribute", "Stamina", "Endurance",
)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def relpath(p: Path, root: Optional[Path]) -> str:
    if root:
        try:
            return str(p.resolve().relative_to(root.resolve())).replace("/", "\\")
        except Exception:
            pass
    return str(p).replace("/", "\\")


def canonical_hook_name(row: Dict[str, Any]) -> str:
    return (
        row.get("normalized_hook_name")
        or row.get("hook_name")
        or row.get("resolved_symbol_value")
        or row.get("symbol")
        or ""
    )


def source_id(row: Dict[str, Any]) -> str:
    return f"{row.get('file', '?')}:{row.get('line', '?')}"


def target_id(row: Dict[str, Any]) -> str:
    t = row.get("target_plugin_method") or {}
    return f"{t.get('file', '?')}:{t.get('line', '?')}:{t.get('method_name', '?')}"


def scan_lua_plugin_methods(roots: Iterable[Path]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Optional independent source scan for PLUGIN:HookName/function PLUGIN.HookName.
    This catches extractor gaps in plugin_methods manifests.
    """
    methods: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    patterns = [
        re.compile(r"\bfunction\s+PLUGIN\s*:\s*([A-Za-z_][A-Za-z0-9_]*)\s*\("),
        re.compile(r"\bfunction\s+PLUGIN\s*\.\s*([A-Za-z_][A-Za-z0-9_]*)\s*\("),
        re.compile(r"\bPLUGIN\s*[\.:]\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*function\s*\("),
    ]

    for root in roots:
        if not root or not root.exists():
            continue
        for path in root.rglob("*.lua"):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                for pat in patterns:
                    m = pat.search(line)
                    if m:
                        name = m.group(1)
                        methods[name].append({
                            "method_name": name,
                            "file": relpath(path, root),
                            "line": lineno,
                            "scan_source": str(root),
                            "raw_line": line.strip()[:240],
                        })
    return methods


def scan_hook_registries(roots: Iterable[Path]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Optional loose scan for hook.Add("Name", ...), hook.Run("Name", ...), hook.Call("Name", ...).
    This helps identify hook names common in framework/source even when no plugin method exists.
    """
    found: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    pat = re.compile(r"\bhook\s*\.\s*(?:Add|Run|Call)\s*\(\s*['\"]([^'\"]+)['\"]")
    for root in roots:
        if not root or not root.exists():
            continue
        for path in root.rglob("*.lua"):
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                m = pat.search(line)
                if m:
                    found[m.group(1)].append({
                        "file": relpath(path, root),
                        "line": lineno,
                        "call": m.group(0),
                    })
    return found


def classify_unresolved(
    row: Dict[str, Any],
    scanned_methods: Dict[str, List[Dict[str, Any]]],
    scanned_hook_refs: Dict[str, List[Dict[str, Any]]],
) -> Tuple[str, List[str], float]:
    name = canonical_hook_name(row)
    reasons: List[str] = []

    if not name:
        return "possibly_extractor_gap", ["missing_hook_name"], 0.95

    if row.get("symbol") and not row.get("resolved_symbol_value") and row.get("resolution") != "unresolved_literal":
        reasons.append("symbol_present_without_resolved_value")
        return "possibly_extractor_gap", reasons, 0.90

    if name in scanned_methods:
        reasons.append("source_scan_found_PLUGIN_method_but_normalizer_did_not_link")
        return "possibly_normalizer_gap", reasons, 0.95

    if name in GMOD_BUILTIN_HOOKS:
        reasons.append("known_gmod_builtin_hook_seed")
        return "probably_gmod_builtin", reasons, 0.90

    if name in NUTSCRIPT_LIKELY_HOOKS:
        reasons.append("known_or_likely_nutscript_hook_seed")
        return "probably_nutscript_builtin", reasons, 0.85

    if name in PROJECT_CORE_LIKELY:
        reasons.append("known_project_core_domain_event_seed")
        return "probably_schema_or_project_core_hook", reasons, 0.80

    if name in scanned_hook_refs and len(scanned_hook_refs[name]) >= 2:
        reasons.append(f"seen_{len(scanned_hook_refs[name])}_times_in_source_hook_refs")
        return "probably_core_or_event_bus_hook", reasons, 0.75

    if name.startswith(SCHEMA_HINT_PREFIXES):
        reasons.append("matches_schema_style_hook_prefix")
        return "probably_schema_hook", reasons, 0.65

    if any(word in name for word in DOMAIN_HINT_WORDS):
        reasons.append("contains_domain_word")
        return "probably_project_domain_hook", reasons, 0.60

    if row.get("resolution") == "unresolved_literal":
        reasons.append("literal_hook_has_no_matching_PLUGIN_method")
        return "missing_plugin_method_or_external_hook", reasons, 0.55

    reasons.append("unclassified_unresolved")
    return "unknown_unresolved", reasons, 0.40


def pct(n: int, d: int) -> float:
    return round((n / d * 100.0), 2) if d else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", default=".", help="Project workspace, e.g. E:/signalis_ai")
    ap.add_argument("--normalized-dir", default=None, help="Override normalized manifest dir")
    ap.add_argument("--source-root", default=None, help="Optional Signalis source root for independent QA scan")
    ap.add_argument("--nutscript-root", default=None, help="Optional NutScript source root for independent QA scan")
    ap.add_argument("--write", action="store_true", help="Write qa JSON and markdown reports")
    ap.add_argument("--top", type=int, default=40, help="How many top unresolved names to include")
    args = ap.parse_args()

    workspace = Path(args.workspace)
    normalized_dir = Path(args.normalized_dir) if args.normalized_dir else workspace / "manifests" / "normalized"

    resolved = load_json(normalized_dir / "resolved_hook_runs.json", [])
    unresolved = load_json(normalized_dir / "unresolved_hook_runs.json", [])
    edges = load_json(normalized_dir / "plugin_hook_edges.json", [])

    scan_roots: List[Path] = []
    if args.source_root:
        scan_roots.append(Path(args.source_root))
    if args.nutscript_root:
        scan_roots.append(Path(args.nutscript_root))

    scanned_methods = scan_lua_plugin_methods(scan_roots)
    scanned_hook_refs = scan_hook_registries(scan_roots)

    total = len(resolved) + len(unresolved)

    resolved_by_source = Counter(r.get("resolution_source") or r.get("resolution") or "unknown" for r in resolved)
    resolved_by_conf = Counter(r.get("resolution_confidence") or r.get("confidence") or "unknown" for r in resolved)
    unresolved_by_name = Counter(canonical_hook_name(r) or "<missing>" for r in unresolved)
    unresolved_by_file = Counter(r.get("file") or "<missing>" for r in unresolved)

    classifications = []
    class_counter = Counter()
    for r in unresolved:
        cls, reasons, confidence = classify_unresolved(r, scanned_methods, scanned_hook_refs)
        class_counter[cls] += 1
        classifications.append({
            "hook_name": canonical_hook_name(r),
            "symbol": r.get("symbol"),
            "file": r.get("file"),
            "line": r.get("line"),
            "realm": r.get("realm"),
            "framework_layer": r.get("framework_layer"),
            "plugin_context": r.get("plugin_context"),
            "classification": cls,
            "classification_confidence": confidence,
            "classification_reasons": reasons,
            "normalization_reasons": r.get("normalization_reasons", []),
            "source_scan_plugin_methods": scanned_methods.get(canonical_hook_name(r), [])[:5],
            "source_scan_hook_refs": scanned_hook_refs.get(canonical_hook_name(r), [])[:8],
        })

    # Duplicate/ambiguous target analysis from resolved rows and edges.
    hook_to_targets: Dict[str, set] = defaultdict(set)
    hook_to_sources: Dict[str, set] = defaultdict(set)
    for r in resolved:
        name = canonical_hook_name(r)
        hook_to_targets[name].add(target_id(r))
        hook_to_sources[name].add(source_id(r))

    ambiguous_resolved = []
    for name, targets in sorted(hook_to_targets.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        if len(targets) > 1:
            ambiguous_resolved.append({
                "hook_name": name,
                "target_count": len(targets),
                "targets": sorted(targets),
                "source_count": len(hook_to_sources.get(name, [])),
                "sources_sample": sorted(hook_to_sources.get(name, []))[:10],
            })

    known_targets = {
        "HandleDiseaseOnCall": False,
        "EnduranceCheck": False,
    }
    for r in resolved:
        name = canonical_hook_name(r)
        if name in known_targets:
            known_targets[name] = True

    top_unresolved = [
        {"hook_name": name, "count": count}
        for name, count in unresolved_by_name.most_common(args.top)
    ]

    report = {
        "inputs": {
            "normalized_dir": str(normalized_dir),
            "source_roots_scanned": [str(p) for p in scan_roots],
            "resolved_file_exists": (normalized_dir / "resolved_hook_runs.json").exists(),
            "unresolved_file_exists": (normalized_dir / "unresolved_hook_runs.json").exists(),
            "edges_file_exists": (normalized_dir / "plugin_hook_edges.json").exists(),
        },
        "summary": {
            "total_hook_runs": total,
            "resolved_hook_runs": len(resolved),
            "unresolved_hook_runs": len(unresolved),
            "plugin_hook_edges": len(edges),
            "resolution_rate_pct": pct(len(resolved), total),
            "unresolved_rate_pct": pct(len(unresolved), total),
            "edge_count_matches_resolved": len(edges) == len(resolved),
        },
        "resolved_by_source": dict(resolved_by_source),
        "resolved_by_confidence": dict(resolved_by_conf),
        "unresolved_classifications": dict(class_counter),
        "top_unresolved_hooks": top_unresolved,
        "top_unresolved_files": [
            {"file": f, "count": c} for f, c in unresolved_by_file.most_common(25)
        ],
        "ambiguous_resolved_hooks": ambiguous_resolved,
        "known_target_checks": known_targets,
        "unresolved_details": classifications,
    }

    md_lines = []
    s = report["summary"]
    md_lines.append("# Hook normalization QA\n")
    md_lines.append("## Summary\n")
    md_lines.append(f"- Total hook runs: **{s['total_hook_runs']}**")
    md_lines.append(f"- Resolved hook runs: **{s['resolved_hook_runs']}**")
    md_lines.append(f"- Unresolved hook runs: **{s['unresolved_hook_runs']}**")
    md_lines.append(f"- Resolution rate: **{s['resolution_rate_pct']}%**")
    md_lines.append(f"- Plugin hook edges: **{s['plugin_hook_edges']}**")
    md_lines.append(f"- Edge count matches resolved: **{s['edge_count_matches_resolved']}**\n")

    md_lines.append("## Unresolved classification\n")
    for k, v in class_counter.most_common():
        md_lines.append(f"- `{k}`: **{v}**")
    md_lines.append("")

    md_lines.append("## Top unresolved hooks\n")
    for item in top_unresolved[:args.top]:
        md_lines.append(f"- `{item['hook_name']}`: {item['count']}")
    md_lines.append("")

    md_lines.append("## Ambiguous resolved hooks\n")
    if ambiguous_resolved:
        for item in ambiguous_resolved[:25]:
            md_lines.append(f"- `{item['hook_name']}` → {item['target_count']} targets")
    else:
        md_lines.append("- none")
    md_lines.append("")

    md_lines.append("## Known target checks\n")
    for k, v in known_targets.items():
        md_lines.append(f"- `{k}`: {'OK' if v else 'MISSING'}")
    md_lines.append("")

    md = "\n".join(md_lines)

    print(md)
    print("JSON unresolved classifications:")
    for k, v in class_counter.most_common():
        print(f"  {k}: {v}")

    if args.write:
        write_json(normalized_dir / "qa_hook_resolution.json", report)
        (normalized_dir / "qa_hook_resolution.md").write_text(md, encoding="utf-8")
        print(f"\nWrote: {normalized_dir / 'qa_hook_resolution.json'}")
        print(f"Wrote: {normalized_dir / 'qa_hook_resolution.md'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
