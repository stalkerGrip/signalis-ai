#!/usr/bin/env python3
"""
SIGNALIS AI — Source Validation Pipeline V1.1

Location:
    scripts/qdrant/validate_sources.py

Purpose:
    Convert an investigation report into a source validation report.

Pipeline:
    investigation report
    -> Priority Files / Hooks / Network Messages
    -> workspace.yaml source_roots
    -> local Lua source scan
    -> exact fragments
    -> validation report

This script does NOT fix gameplay code.
It does NOT define truth by itself.
It extracts source evidence for human / architecture validation.

Usage:

    python -m scripts.qdrant.validate_sources ^
      --workspace E:/signalis_ai ^
      --report investigations/generated/vendor_stale_price_label_after_purchase.md

Expected workspace.yaml:

    source_roots:
      - E:\\steam\\steamapps\\common\\GarrysMod\\garrysmod\\gamemodes\\signalis
      - E:\\steam\\steamapps\\common\\GarrysMod\\garrysmod\\gamemodes\\nutscript

Outputs:

    investigations/validation/<name>_validation.md
    investigations/validation/<name>_validation.json
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable, Any


DEFAULT_OUT_DIR = Path("investigations/validation")
DEFAULT_WORKSPACE_CONFIG = Path("workspace.yaml")


@dataclass
class SourceFragment:
    file: str
    resolved_path: str
    source_root: str
    line_start: int
    line_end: int
    match_type: str
    match_value: str
    realm: str
    classification: str
    snippet: str


@dataclass
class FileValidation:
    file: str
    exists: bool
    resolved_path: str | None
    source_root: str | None
    realm: str
    fragments: list[SourceFragment]
    notes: list[str]


@dataclass
class ValidationReport:
    generated_at: str
    source_report: str
    query: str
    workspace: str
    source_roots: list[str]
    priority_files: list[str]
    priority_hooks: list[str]
    priority_network_messages: list[str]
    files: list[FileValidation]
    missing_files: list[str]
    summary: dict[str, int | str]


# ---------------------------------------------------------------------------
# File / text helpers
# ---------------------------------------------------------------------------

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def normalize_path(value: str) -> str:
    value = value.strip().strip("`").strip()
    value = value.replace("\\", "/")
    value = re.sub(r"/+", "/", value)
    return value


def slug_from_report(path: Path) -> str:
    name = path.stem
    if name.endswith("_validation"):
        name = name[:-11]
    return name


def unique_preserve_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        value = str(value).strip()
        marker = value.lower()
        if value and marker not in seen:
            seen.add(marker)
            out.append(value)
    return out


def simple_yaml_source_roots(text: str) -> list[str]:
    """
    Minimal YAML parser for:

      source_roots:
        - E:\\path
        - "E:\\path with spaces"

    This avoids requiring PyYAML.
    """
    roots: list[str] = []
    in_source_roots = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        if re.match(r"^source_roots\s*:", stripped):
            in_source_roots = True
            continue

        if in_source_roots:
            if re.match(r"^[A-Za-z0-9_ -]+\s*:", stripped) and not stripped.startswith("-"):
                break

            if stripped.startswith("-"):
                value = stripped[1:].strip()
                value = value.strip("'\"")
                if value:
                    roots.append(value)

    return roots


def load_source_roots(workspace: Path, config_path: Path | None, cli_source_roots: list[str]) -> list[Path]:
    roots: list[str] = []

    if cli_source_roots:
        roots.extend(cli_source_roots)

    config_candidates: list[Path] = []

    if config_path:
        config_candidates.append(config_path if config_path.is_absolute() else workspace / config_path)
    else:
        config_candidates.extend([
            workspace / DEFAULT_WORKSPACE_CONFIG,
            workspace / "config" / DEFAULT_WORKSPACE_CONFIG,
            workspace / "config" / "workspace.yaml",
        ])

    for candidate in config_candidates:
        if candidate.exists() and candidate.is_file():
            roots.extend(simple_yaml_source_roots(read_text(candidate)))
            break

    # Fallback: workspace itself.
    if not roots:
        roots.append(str(workspace))

    resolved: list[Path] = []
    for root in unique_preserve_order(roots):
        p = Path(root)
        if not p.is_absolute():
            p = workspace / p
        resolved.append(p.resolve())

    return resolved


def infer_realm_from_path(path: str) -> str:
    name = Path(path.replace("\\", "/")).name.lower()
    if name.startswith("cl_"):
        return "client"
    if name.startswith("sv_"):
        return "server"
    if name.startswith("sh_"):
        return "shared"
    return "unknown"


def detect_realm_from_content(path: str, text: str) -> str:
    file_realm = infer_realm_from_path(path)

    has_server = bool(re.search(r"\bSERVER\b|if\s*\(?\s*SERVER\s*\)?\s*then", text))
    has_client = bool(re.search(r"\bCLIENT\b|if\s*\(?\s*CLIENT\s*\)?\s*then", text))

    if file_realm != "unknown":
        if has_server and has_client:
            return f"{file_realm}+conditional"
        return file_realm

    if has_server and has_client:
        return "shared/conditional"
    if has_server:
        return "server-evidence"
    if has_client:
        return "client-evidence"
    return "unknown"


def line_window(lines: list[str], index: int, before: int, after: int) -> tuple[int, int, str]:
    start = max(0, index - before)
    end = min(len(lines), index + after + 1)

    numbered = []
    for i in range(start, end):
        numbered.append(f"{i + 1:>5}: {lines[i]}")

    return start + 1, end, "\n".join(numbered)


# ---------------------------------------------------------------------------
# Investigation report parsing
# ---------------------------------------------------------------------------

def extract_query(report_text: str) -> str:
    match = re.search(r"^- Query:\s*`([^`]+)`", report_text, flags=re.MULTILINE)
    if match:
        return match.group(1).strip()

    match = re.search(r"^## Question\s+(.+?)(?:\n## |\Z)", report_text, flags=re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1).strip()

    return "unknown"


def extract_markdown_list_section(report_text: str, heading: str) -> list[str]:
    pattern = rf"^###\s+{re.escape(heading)}\s*(.+?)(?=^###\s+|^##\s+|\Z)"
    match = re.search(pattern, report_text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return []

    section = match.group(1)
    values: list[str] = []

    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("-"):
            continue

        raw = line[1:].strip()
        tick = re.search(r"`([^`]+)`", raw)
        if tick:
            raw = tick.group(1)

        raw = raw.strip()
        if raw and raw.lower() != "none detected":
            values.append(normalize_path(raw) if "/" in raw or "\\" in raw else raw)

    return unique_preserve_order(values)


def parse_investigation_report(report_path: Path) -> tuple[str, list[str], list[str], list[str]]:
    text = read_text(report_path)

    query = extract_query(text)
    priority_files = extract_markdown_list_section(text, "Priority Files")
    priority_hooks = extract_markdown_list_section(text, "Priority Hooks")
    priority_network_messages = extract_markdown_list_section(text, "Priority Network Messages")

    # Fallback for older reports without Validation Targets.
    if not priority_files:
        priority_files = extract_markdown_list_section(text, "files")
    if not priority_hooks:
        priority_hooks = extract_markdown_list_section(text, "hooks")
    if not priority_network_messages:
        priority_network_messages = extract_markdown_list_section(text, "network_messages")

    return query, priority_files, priority_hooks, priority_network_messages


# ---------------------------------------------------------------------------
# Source resolving
# ---------------------------------------------------------------------------

def possible_relative_paths(relative_file: str) -> list[str]:
    rel = normalize_path(relative_file)
    candidates = [rel]

    # Some manifests store gamemode/core/... while source root may itself be gamemode folder.
    if rel.startswith("gamemode/"):
        candidates.append(rel[len("gamemode/"):])

    # If source root is the schema/gamemode root, these are already correct.
    # Keep normalized de-duplicated.
    return unique_preserve_order(candidates)


def resolve_source_file(source_roots: list[Path], relative_file: str) -> tuple[Path | None, Path | None]:
    candidates = possible_relative_paths(relative_file)

    for root in source_roots:
        for rel in candidates:
            direct = root / rel
            if direct.exists() and direct.is_file():
                return direct.resolve(), root

    # Fallback: basename search inside source roots.
    basename = Path(relative_file.replace("\\", "/")).name.lower()
    matches: list[tuple[Path, Path]] = []

    for root in source_roots:
        if not root.exists():
            continue
        for path in root.rglob("*.lua"):
            if path.name.lower() == basename:
                normalized = normalize_path(str(path))
                rel_parts = normalize_path(relative_file).lower().split("/")
                # Prefer paths containing the final 2-3 relative components.
                tail2 = "/".join(rel_parts[-2:])
                tail3 = "/".join(rel_parts[-3:])
                score = 0
                if tail3 and tail3 in normalized.lower():
                    score += 3
                if tail2 and tail2 in normalized.lower():
                    score += 2
                if basename in normalized.lower():
                    score += 1
                matches.append((path.resolve(), root))

    if matches:
        matches.sort(key=lambda pair: len(str(pair[0])))
        return matches[0]

    return None, None


# ---------------------------------------------------------------------------
# Source matching
# ---------------------------------------------------------------------------

def classify_match(line: str, match_type: str, value: str) -> str:
    stripped = line.strip()
    lower = stripped.lower()

    if match_type == "hook":
        if "hook.run" in lower:
            return "hook_emitter"
        if "hook.add" in lower:
            return "hook_listener_explicit"
        if re.search(r"function\s+(plugin|schema|gm)\s*:", lower):
            return "hook_listener_plugin_method"
        return "hook_reference"

    if match_type == "network":
        if "netstream.start" in lower or "net.start" in lower:
            return "network_send_or_start"
        if "netstream.hook" in lower or "net.receive" in lower:
            return "network_receiver"
        if "util.addnetworkstring" in lower:
            return "network_registration"
        if "write" in lower:
            return "network_payload_write"
        if "read" in lower:
            return "network_payload_read"
        return "network_reference"

    if match_type == "state":
        if ":setdata" in lower or ".setdata" in lower or "setdata(" in lower:
            return "item_data_mutation"
        if ":getdata" in lower or ".getdata" in lower or "getdata(" in lower:
            return "item_data_read"
        if "setnetvar" in lower or "setlocalvar" in lower:
            return "networked_var_mutation"
        if "getnetvar" in lower or "getlocalvar" in lower:
            return "networked_var_read"
        if "settext" in lower or "label" in lower or "price" in lower:
            return "ui_presentation_logic"
        return "state_or_ui_reference"

    return "reference"


def build_hook_patterns(hook: str) -> list[re.Pattern[str]]:
    escaped = re.escape(hook)
    return [
        re.compile(rf"\bhook\.Run\s*\(\s*['\"]{escaped}['\"]", re.IGNORECASE),
        re.compile(rf"\bhook\.Add\s*\(\s*['\"]{escaped}['\"]", re.IGNORECASE),
        re.compile(rf"\bfunction\s+(?:PLUGIN|SCHEMA|GM)\s*:\s*{escaped}\s*\(", re.IGNORECASE),
        re.compile(rf"\b{escaped}\b", re.IGNORECASE),
    ]


def build_network_patterns(message: str) -> list[re.Pattern[str]]:
    escaped = re.escape(message)
    return [
        re.compile(rf"\bnetstream\.Start\s*\([^)\n]*['\"]{escaped}['\"]", re.IGNORECASE),
        re.compile(rf"\bnetstream\.Hook\s*\(\s*['\"]{escaped}['\"]", re.IGNORECASE),
        re.compile(rf"\bnet\.Start\s*\(\s*['\"]{escaped}['\"]", re.IGNORECASE),
        re.compile(rf"\bnet\.Receive\s*\(\s*['\"]{escaped}['\"]", re.IGNORECASE),
        re.compile(rf"\butil\.AddNetworkString\s*\(\s*['\"]{escaped}['\"]", re.IGNORECASE),
        re.compile(rf"\b{escaped}\b", re.IGNORECASE),
    ]


def build_state_patterns(query: str) -> list[tuple[str, re.Pattern[str]]]:
    q = query.lower()
    patterns: list[tuple[str, re.Pattern[str]]] = []

    generic = [
        r":SetData\s*\(",
        r"\.SetData\s*\(",
        r":GetData\s*\(",
        r"\.GetData\s*\(",
        r"setData\s*\(",
        r"getData\s*\(",
        r"SetText\s*\(",
        r"SetTooltip\s*\(",
        r"\bprice\b",
        r"\bvendor\b",
        r"\blabel\b",
    ]

    if "vendor" in q or "price" in q or "label" in q:
        for raw in generic:
            patterns.append(("state", re.compile(raw, re.IGNORECASE)))

    return patterns


def scan_file(
    workspace: Path,
    source_roots: list[Path],
    relative_file: str,
    hooks: list[str],
    network_messages: list[str],
    query: str,
    context_before: int,
    context_after: int,
) -> FileValidation:
    resolved_path, source_root = resolve_source_file(source_roots, relative_file)

    if not resolved_path or not source_root:
        return FileValidation(
            file=relative_file,
            exists=False,
            resolved_path=None,
            source_root=None,
            realm=infer_realm_from_path(relative_file),
            fragments=[],
            notes=[
                "File not found in workspace or source_roots.",
                "Check workspace.yaml source_roots if this path should exist.",
            ],
        )

    text = read_text(resolved_path)
    realm = detect_realm_from_content(relative_file, text)
    lines = text.splitlines()
    fragments: list[SourceFragment] = []

    hook_patterns = [(hook, build_hook_patterns(hook)) for hook in hooks]
    network_patterns = [(msg, build_network_patterns(msg)) for msg in network_messages]
    state_patterns = build_state_patterns(query)

    for idx, line in enumerate(lines):
        for hook, patterns in hook_patterns:
            if any(pattern.search(line) for pattern in patterns):
                start, end, snippet = line_window(lines, idx, context_before, context_after)
                fragments.append(
                    SourceFragment(
                        file=relative_file,
                        resolved_path=str(resolved_path),
                        source_root=str(source_root),
                        line_start=start,
                        line_end=end,
                        match_type="hook",
                        match_value=hook,
                        realm=realm,
                        classification=classify_match(line, "hook", hook),
                        snippet=snippet,
                    )
                )

        for msg, patterns in network_patterns:
            if any(pattern.search(line) for pattern in patterns):
                start, end, snippet = line_window(lines, idx, context_before, context_after)
                fragments.append(
                    SourceFragment(
                        file=relative_file,
                        resolved_path=str(resolved_path),
                        source_root=str(source_root),
                        line_start=start,
                        line_end=end,
                        match_type="network",
                        match_value=msg,
                        realm=realm,
                        classification=classify_match(line, "network", msg),
                        snippet=snippet,
                    )
                )

        for match_type, pattern in state_patterns:
            if pattern.search(line):
                matched_value = pattern.pattern
                start, end, snippet = line_window(lines, idx, context_before, context_after)
                fragments.append(
                    SourceFragment(
                        file=relative_file,
                        resolved_path=str(resolved_path),
                        source_root=str(source_root),
                        line_start=start,
                        line_end=end,
                        match_type=match_type,
                        match_value=matched_value,
                        realm=realm,
                        classification=classify_match(line, "state", matched_value),
                        snippet=snippet,
                    )
                )

    fragments = dedupe_fragments(fragments)

    notes: list[str] = []
    if not fragments:
        notes.append("No direct hook/network/state fragments found for selected validation targets.")

    if realm.startswith("client"):
        notes.append("Client realm: likely presentation/UI or client request logic unless source shows otherwise.")
    elif realm.startswith("server"):
        notes.append("Server realm: may contain authoritative gameplay/state logic.")
    elif "conditional" in realm:
        notes.append("Conditional realm evidence: validate SERVER/CLIENT branches manually.")

    return FileValidation(
        file=relative_file,
        exists=True,
        resolved_path=str(resolved_path),
        source_root=str(source_root),
        realm=realm,
        fragments=fragments,
        notes=notes,
    )


def dedupe_fragments(fragments: list[SourceFragment]) -> list[SourceFragment]:
    seen: set[tuple[str, int, int, str, str]] = set()
    out: list[SourceFragment] = []

    for frag in fragments:
        key = (
            frag.resolved_path.lower(),
            frag.line_start,
            frag.line_end,
            frag.match_type,
            frag.match_value.lower(),
        )
        if key not in seen:
            seen.add(key)
            out.append(frag)

    return out


# ---------------------------------------------------------------------------
# Markdown report
# ---------------------------------------------------------------------------

def format_markdown(report: ValidationReport) -> str:
    lines: list[str] = []

    lines.append("# SIGNALIS AI — Source Validation Report")
    lines.append("")
    lines.append(f"- Generated: `{report.generated_at}`")
    lines.append(f"- Investigation report: `{report.source_report}`")
    lines.append(f"- Query: `{report.query}`")
    lines.append(f"- Workspace: `{report.workspace}`")
    lines.append("")

    lines.append("## Source Roots")
    lines.append("")
    for root in report.source_roots:
        lines.append(f"- `{root}`")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Priority files: `{len(report.priority_files)}`")
    lines.append(f"- Files found: `{report.summary['files_found']}`")
    lines.append(f"- Missing files: `{len(report.missing_files)}`")
    lines.append(f"- Extracted fragments: `{report.summary['fragments_total']}`")
    lines.append(f"- Hook fragments: `{report.summary['hook_fragments']}`")
    lines.append(f"- Network fragments: `{report.summary['network_fragments']}`")
    lines.append(f"- State/UI fragments: `{report.summary['state_fragments']}`")
    lines.append("")

    lines.append("## Validation Targets")
    lines.append("")
    lines.append("### Priority Files")
    lines.append("")
    for value in report.priority_files:
        lines.append(f"- `{value}`")
    if not report.priority_files:
        lines.append("- none")
    lines.append("")

    lines.append("### Priority Hooks")
    lines.append("")
    for value in report.priority_hooks:
        lines.append(f"- `{value}`")
    if not report.priority_hooks:
        lines.append("- none")
    lines.append("")

    lines.append("### Priority Network Messages")
    lines.append("")
    for value in report.priority_network_messages:
        lines.append(f"- `{value}`")
    if not report.priority_network_messages:
        lines.append("- none")
    lines.append("")

    lines.append("## Missing Files")
    lines.append("")
    if report.missing_files:
        for value in report.missing_files:
            lines.append(f"- `{value}`")
    else:
        lines.append("- none")
    lines.append("")

    lines.append("## Source Evidence")
    lines.append("")

    for file_result in report.files:
        lines.append(f"### `{file_result.file}`")
        lines.append("")
        lines.append(f"- Exists: `{file_result.exists}`")
        if file_result.resolved_path:
            lines.append(f"- Resolved path: `{file_result.resolved_path}`")
        if file_result.source_root:
            lines.append(f"- Source root: `{file_result.source_root}`")
        lines.append(f"- Realm: `{file_result.realm}`")
        for note in file_result.notes:
            lines.append(f"- Note: {note}")
        lines.append("")

        if not file_result.fragments:
            lines.append("_No matching fragments extracted._")
            lines.append("")
            continue

        for idx, frag in enumerate(file_result.fragments, start=1):
            lines.append(f"#### Fragment {idx}: {frag.match_type} / {frag.match_value}")
            lines.append("")
            lines.append(f"- Lines: `{frag.line_start}-{frag.line_end}`")
            lines.append(f"- Realm: `{frag.realm}`")
            lines.append(f"- Classification: `{frag.classification}`")
            lines.append("")
            lines.append("```lua")
            lines.append(frag.snippet)
            lines.append("```")
            lines.append("")

    lines.append("## Validation Interpretation")
    lines.append("")
    lines.append("This report extracts source evidence only.")
    lines.append("")
    lines.append("Do not treat matches as confirmed causes without human/source review.")
    lines.append("")
    lines.append("Use the extracted fragments to answer:")
    lines.append("")
    lines.append("- Which file is authoritative?")
    lines.append("- Which hook/listener/network path actually runs?")
    lines.append("- Is the logic server-authoritative, client presentation-only, or mixed?")
    lines.append("- Does the code mutate persisted state or only UI/item presentation metadata?")
    lines.append("")

    lines.append("## Promotion Rule")
    lines.append("")
    lines.append("Promote findings only after validation:")
    lines.append("")
    lines.append("investigation -> source validation -> human validation -> subsystem docs -> doctrine/project memory")
    lines.append("")

    return "\n".join(lines)


def build_summary(files: list[FileValidation]) -> dict[str, int | str]:
    fragments = [frag for f in files for frag in f.fragments]

    return {
        "files_total": len(files),
        "files_found": sum(1 for f in files if f.exists),
        "fragments_total": len(fragments),
        "hook_fragments": sum(1 for f in fragments if f.match_type == "hook"),
        "network_fragments": sum(1 for f in fragments if f.match_type == "network"),
        "state_fragments": sum(1 for f in fragments if f.match_type == "state"),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate source fragments from a SIGNALIS investigation report.")

    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--workspace-config", type=Path, default=None)
    parser.add_argument("--source-root", action="append", default=[])
    parser.add_argument("--context-before", type=int, default=6)
    parser.add_argument("--context-after", type=int, default=10)
    parser.add_argument("--limit-files", type=int, default=0)

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    workspace = args.workspace.resolve()

    report_path = args.report
    if not report_path.is_absolute():
        report_path = workspace / report_path

    if not report_path.exists():
        raise SystemExit(f"Investigation report not found: {report_path}")

    out_dir = args.out_dir
    if not out_dir.is_absolute():
        out_dir = workspace / out_dir

    source_roots = load_source_roots(
        workspace=workspace,
        config_path=args.workspace_config,
        cli_source_roots=args.source_root,
    )

    query, priority_files, priority_hooks, priority_network_messages = parse_investigation_report(report_path)

    if args.limit_files and args.limit_files > 0:
        priority_files = priority_files[: args.limit_files]

    files: list[FileValidation] = []

    for file_path in priority_files:
        files.append(
            scan_file(
                workspace=workspace,
                source_roots=source_roots,
                relative_file=file_path,
                hooks=priority_hooks,
                network_messages=priority_network_messages,
                query=query,
                context_before=args.context_before,
                context_after=args.context_after,
            )
        )

    missing_files = [f.file for f in files if not f.exists]

    validation = ValidationReport(
        generated_at=datetime.now().isoformat(timespec="seconds"),
        source_report=str(report_path),
        query=query,
        workspace=str(workspace),
        source_roots=[str(p) for p in source_roots],
        priority_files=priority_files,
        priority_hooks=priority_hooks,
        priority_network_messages=priority_network_messages,
        files=files,
        missing_files=missing_files,
        summary=build_summary(files),
    )

    slug = slug_from_report(report_path)
    md_path = out_dir / f"{slug}_validation.md"
    json_path = out_dir / f"{slug}_validation.json"

    write_text(md_path, format_markdown(validation))
    write_text(json_path, json.dumps(asdict(validation), indent=2, ensure_ascii=False))

    print(f"Wrote validation report: {md_path}")
    print(f"Wrote validation json:   {json_path}")
    print("")
    print("Source roots:")
    for root in source_roots:
        exists = "exists" if root.exists() else "MISSING"
        print(f"  - {root} [{exists}]")
    print("")
    print("Summary:")
    for key, value in validation.summary.items():
        print(f"  {key}: {value}")

    if missing_files:
        print("")
        print("Missing files:")
        for value in missing_files:
            print(f"  - {value}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
