#!/usr/bin/env python3
"""
Normalize symbolic hook.Run(...) names into concrete plugin hook names.

Target example:
  hook.Run(nut.diseases.stringConsts.handleDiseaseOnCall)
    -> HandleDiseaseOnCall
    -> PLUGIN:HandleDiseaseOnCall

Inputs, relative to --workspace:
  manifests/plugins/hook_runs.json
  manifests/plugins/plugin_methods.json

Optional but recommended:
  --source-root E:/steam/steamapps/common/GarrysMod/garrysmod/gamemodes/signalis
This lets the normalizer read real GLua assignments like:
  nut.diseases.stringConsts.handleDiseaseOnCall = "HandleDiseaseOnCall"

Outputs:
  manifests/normalized/resolved_hook_runs.json
  manifests/normalized/unresolved_hook_runs.json
  manifests/normalized/plugin_hook_edges.json
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable


HOOK_RUNS_REL = Path("manifests/plugins/hook_runs.json")
PLUGIN_METHODS_REL = Path("manifests/plugins/plugin_methods.json")
OUT_REL = Path("manifests/normalized")

# Matches: nut.foo.bar.baz = "SomeHookName" / 'SomeHookName'
NUT_STRING_ASSIGN_RE = re.compile(
    r"(?P<symbol>nut(?:\s*\.\s*[A-Za-z_][A-Za-z0-9_]*)+)\s*=\s*(?P<quote>[\"'])(?P<value>[^\"']+)(?P=quote)",
    re.MULTILINE,
)

# Matches table fields inside nut.foo = { key = "Value", ["key"] = "Value" }
TABLE_ASSIGN_START_RE = re.compile(
    r"(?P<table>nut(?:\s*\.\s*[A-Za-z_][A-Za-z0-9_]*)+)\s*=\s*\{",
    re.MULTILINE,
)
TABLE_FIELD_STRING_RE = re.compile(
    r"(?:\[\s*[\"'](?P<bracket_key>[A-Za-z_][A-Za-z0-9_]*)[\"']\s*\]|(?P<bare_key>[A-Za-z_][A-Za-z0-9_]*))\s*=\s*(?P<quote>[\"'])(?P<value>[^\"']+)(?P=quote)"
)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def normalize_symbol_text(symbol: str) -> str:
    return re.sub(r"\s+", "", symbol.replace(":", "."))


def lua_file_iter(root: Path) -> Iterable[Path]:
    if not root or not root.exists():
        return []
    return root.rglob("*.lua")


def strip_lua_comments(text: str) -> str:
    # Good enough for manifest normalization. Avoids most false string-constant assignments in comments.
    text = re.sub(r"--\[\[.*?\]\]", "", text, flags=re.DOTALL)
    text = re.sub(r"--.*?$", "", text, flags=re.MULTILINE)
    return text


def find_matching_brace(text: str, open_idx: int) -> int | None:
    depth = 0
    quote: str | None = None
    escape = False
    for i in range(open_idx, len(text)):
        ch = text[i]
        if quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                quote = None
            continue
        if ch in ('"', "'"):
            quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
    return None


def extract_string_constants_from_source(source_roots: list[Path]) -> dict[str, list[dict[str, Any]]]:
    constants: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for root in source_roots:
        for path in lua_file_iter(root):
            try:
                raw = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            text = strip_lua_comments(raw)
            rel_file = str(path.relative_to(root)).replace("/", "\\")

            for m in NUT_STRING_ASSIGN_RE.finditer(text):
                symbol = normalize_symbol_text(m.group("symbol"))
                constants[symbol].append({
                    "symbol": symbol,
                    "value": m.group("value"),
                    "source": "direct_assignment",
                    "file": rel_file,
                    "line": text.count("\n", 0, m.start()) + 1,
                })

            for m in TABLE_ASSIGN_START_RE.finditer(text):
                open_idx = text.find("{", m.end() - 1)
                close_idx = find_matching_brace(text, open_idx)
                if close_idx is None:
                    continue
                table_symbol = normalize_symbol_text(m.group("table"))
                body = text[open_idx + 1:close_idx]
                for fm in TABLE_FIELD_STRING_RE.finditer(body):
                    key = fm.group("bracket_key") or fm.group("bare_key")
                    symbol = f"{table_symbol}.{key}"
                    constants[symbol].append({
                        "symbol": symbol,
                        "value": fm.group("value"),
                        "source": "table_field_assignment",
                        "file": rel_file,
                        "line": text.count("\n", 0, open_idx + 1 + fm.start()) + 1,
                    })

    return dict(constants)


def upper_first(s: str) -> str:
    return s[:1].upper() + s[1:] if s else s


def symbol_leaf_candidate(symbol: str) -> str:
    # Fallback for conventions like handleDiseaseOnCall -> HandleDiseaseOnCall.
    return upper_first(symbol.split(".")[-1])


def method_index(plugin_methods: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    idx: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for m in plugin_methods:
        name = m.get("method_name")
        if name:
            idx[name].append(m)
    return dict(idx)


def choose_method(methods: list[dict[str, Any]], run: dict[str, Any]) -> tuple[dict[str, Any] | None, str]:
    if not methods:
        return None, "no_plugin_method"
    if len(methods) == 1:
        return methods[0], "unique_method"

    run_file = (run.get("file") or "").replace("/", "\\").lower()
    run_plugin = plugin_folder(run_file)

    same_plugin = [m for m in methods if plugin_folder((m.get("file") or "").replace("/", "\\").lower()) == run_plugin]
    if len(same_plugin) == 1:
        return same_plugin[0], "same_plugin_folder"
    if len(same_plugin) > 1:
        return same_plugin[0], "ambiguous_same_plugin_folder"

    # Prefer same realm when available.
    run_realm = run.get("realm")
    same_realm = [m for m in methods if m.get("realm") == run_realm]
    if len(same_realm) == 1:
        return same_realm[0], "same_realm"
    if len(same_realm) > 1:
        return same_realm[0], "ambiguous_same_realm"

    return methods[0], "ambiguous_global_method_name"


def plugin_folder(file_path: str) -> str | None:
    parts = re.split(r"[\\/]", file_path)
    if "plugins" not in parts:
        return None
    i = parts.index("plugins")
    if i + 1 < len(parts):
        return parts[i + 1]
    return None


def confidence_for(resolution_source: str, method_reason: str, value_count: int, method_count: int) -> str:
    if resolution_source in {"direct_assignment", "table_field_assignment"} and value_count == 1 and method_reason in {"unique_method", "same_plugin_folder", "same_realm"}:
        return "high"
    if resolution_source == "leaf_pascal_fallback" and method_count == 1:
        return "medium"
    if "ambiguous" in method_reason or value_count > 1 or method_count > 1:
        return "low"
    return "medium"


def normalize(workspace: Path, source_roots: list[Path]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    hook_runs = load_json(workspace / HOOK_RUNS_REL, [])
    plugin_methods = load_json(workspace / PLUGIN_METHODS_REL, [])

    constants = extract_string_constants_from_source(source_roots)
    methods_by_name = method_index(plugin_methods)

    resolved: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    for run in hook_runs:
        run2 = dict(run)
        original_hook = run.get("hook_name")
        symbol = run.get("symbol")

        candidates: list[dict[str, Any]] = []
        if original_hook:
            candidates.append({"hook_name": original_hook, "source": "literal", "evidence": None})
        elif symbol:
            norm_symbol = normalize_symbol_text(symbol)
            const_hits = constants.get(norm_symbol, [])
            for c in const_hits:
                candidates.append({"hook_name": c["value"], "source": c["source"], "evidence": c})
            if not candidates:
                candidates.append({"hook_name": symbol_leaf_candidate(norm_symbol), "source": "leaf_pascal_fallback", "evidence": {"symbol": norm_symbol}})

        matched = False
        reasons: list[str] = []
        for cand in candidates:
            hook_name = cand["hook_name"]
            method_matches = methods_by_name.get(hook_name, [])
            chosen, reason = choose_method(method_matches, run)
            reasons.append(f"{cand['source']}:{hook_name}:{reason}")
            if not chosen:
                continue

            matched = True
            value_count = len(constants.get(normalize_symbol_text(symbol), [])) if symbol else 1
            conf = confidence_for(cand["source"], reason, value_count, len(method_matches))
            resolved_item = dict(run2)
            resolved_item.update({
                "normalized_hook_name": hook_name,
                "resolved_symbol_value": hook_name if symbol else None,
                "resolution": "resolved_symbol" if symbol else "literal",
                "resolution_source": cand["source"],
                "resolution_confidence": conf,
                "resolution_reason": reason,
                "symbol_evidence": cand.get("evidence"),
                "target_plugin_method": {
                    "method_name": chosen.get("method_name"),
                    "args": chosen.get("args"),
                    "file": chosen.get("file"),
                    "line": chosen.get("line"),
                    "realm": chosen.get("realm"),
                    "framework_layer": chosen.get("framework_layer"),
                    "plugin_context": chosen.get("plugin_context"),
                },
            })
            resolved.append(resolved_item)
            edges.append({
                "type": "plugin_hook_edge",
                "edge_kind": "hook_run_to_plugin_method",
                "hook_name": hook_name,
                "symbol": symbol,
                "source_file": run.get("file"),
                "source_line": run.get("line"),
                "source_realm": run.get("realm"),
                "target_method": chosen.get("method_name"),
                "target_file": chosen.get("file"),
                "target_line": chosen.get("line"),
                "target_realm": chosen.get("realm"),
                "confidence": conf,
                "resolution_source": cand["source"],
                "resolution_reason": reason,
            })
            break

        if not matched:
            item = dict(run2)
            item.update({
                "resolution": "unresolved_symbol" if symbol else "unresolved_literal",
                "normalization_reasons": reasons,
            })
            unresolved.append(item)

    return resolved, unresolved, edges


def main() -> int:
    ap = argparse.ArgumentParser(description="Normalize symbolic hook.Run names to plugin hook methods.")
    ap.add_argument("--workspace", default=".", help="Workspace root containing manifests/. Example: E:/signalis_ai")
    ap.add_argument("--source-root", action="append", default=[], help="Lua source root. Can be passed multiple times.")
    ap.add_argument("--write", action="store_true", help="Write normalized JSON outputs. Without this, only prints a summary.")
    args = ap.parse_args()

    workspace = Path(args.workspace).resolve()
    source_roots = [Path(p).resolve() for p in args.source_root]

    resolved, unresolved, edges = normalize(workspace, source_roots)

    print(f"resolved_hook_runs: {len(resolved)}")
    print(f"unresolved_hook_runs: {len(unresolved)}")
    print(f"plugin_hook_edges: {len(edges)}")

    by_source: dict[str, int] = defaultdict(int)
    by_conf: dict[str, int] = defaultdict(int)
    for r in resolved:
        by_source[r.get("resolution_source", "unknown")] += 1
        by_conf[r.get("resolution_confidence", "unknown")] += 1
    print("resolution_source_counts:", dict(sorted(by_source.items())))
    print("confidence_counts:", dict(sorted(by_conf.items())))

    if args.write:
        out = workspace / OUT_REL
        write_json(out / "resolved_hook_runs.json", resolved)
        write_json(out / "unresolved_hook_runs.json", unresolved)
        write_json(out / "plugin_hook_edges.json", edges)
        print(f"wrote: {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
