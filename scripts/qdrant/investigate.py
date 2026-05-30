#!/usr/bin/env python3
"""
SIGNALIS AI — Investigation Pipeline V1.1

Location:
    scripts/qdrant/investigate.py

Purpose:
    Turn an architecture question into a repeatable investigation report.

Pipeline:
    query
    -> retrieval intent classification
    -> query_qdrant.py execution
    -> raw retrieval capture
    -> lightweight evidence extraction
    -> validation target generation
    -> local human/project context scan
    -> markdown investigation report

This script does not define truth.
It assembles evidence and produces source-validation targets.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

DEFAULT_COLLECTION = "signalis_semantic"


@dataclass
class InvestigationConfig:
    workspace: Path
    query: str
    top_k: int
    collection: str
    out_dir: Path
    extra_query_args: list[str]
    include_human_context: bool = True
    include_project_memory: bool = True
    include_topology_summary: bool = True


@dataclass
class RetrievalRun:
    stdout: str
    result_file: Path | None
    result_text: str


@dataclass
class ValidationTargets:
    priority_files: list[str]
    priority_hooks: list[str]
    priority_network_messages: list[str]
    reason: str


def ensure_workspace_imports(workspace: Path) -> None:
    root = str(workspace.resolve())
    if root not in sys.path:
        sys.path.insert(0, root)


def safe_import_intent(workspace: Path):
    ensure_workspace_imports(workspace)
    try:
        from scripts.qdrant.retrieval_intent import classify_retrieval_intent, build_expanded_query  # type: ignore
        return classify_retrieval_intent, build_expanded_query
    except Exception:
        return None, None


def slugify(value: str, max_len: int = 80) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return (value or "investigation")[:max_len].strip("_")


def read_text_if_exists(path: Path) -> str:
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8", errors="replace")
    return ""


def first_lines(text: str, limit: int = 120) -> str:
    return "\n".join(text.splitlines()[:limit])


def extract_markdown_headings(text: str, limit: int = 40) -> list[str]:
    out: list[str] = []
    for line in text.splitlines():
        if line.startswith("#"):
            out.append(line.strip())
            if len(out) >= limit:
                break
    return out


def clean_path(path: str) -> str:
    path = path.replace("\\", "/")
    path = re.sub(r"/+", "/", path)
    return path.strip()


def unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        value = value.strip()
        marker = value.lower()
        if value and marker not in seen:
            seen.add(marker)
            out.append(value)
    return out


def extract_candidate_terms(text: str) -> dict[str, list[str]]:
    norm = text.replace("\\", "/")

    patterns = {
        "plugins": r"\b(?:inventory|gridinv|storage|vendor|multichar|healthproblems|needs|biorezonance|lightitems|mining|ragdollinteraction|nextbots|tying|crafting|gadgets|hud|armor|gamemode|schema)\b",
        "hooks": r"\b(?:CharacterLoaded|PrePlayerLoadedChar|PlayerLoadedChar|PlayerLoadout|PostPlayerLoadout|SaveData|LoadData|PostLoadData|StorageOpen|StorageRestored|StorageEntityRemoved|ItemTransfered|InventoryItemAdded|InventoryItemRemoved|ItemDataChanged|VendorOpened|VendorItemPriceUpdated|VendorItemStockUpdated|VendorMoneyUpdated|CanPlayerTradeWithVendor|CanPlayerAccessVendor|CanItemBeTransfered|HandleItemTransferRequest|CreateNewInventoryPanel|CreateInventoryPanel|DrawItemDescription|Think|HUDPaint)\b",
        "network_messages": r"\b(?:inventoryOpen|inventorySetPanelStatus|storageInventory|nutInventoryInit|nutInventoryAdd|nutInventoryRemove|nutInventoryDelete|nutInventoryData|nutTransferItem|nutStorageOpen|nutStorageUnlock|nutVendorOpen|nutVendorTrade|nutVendorExit|nutVendorEdit|nutCharChoose|nutCharCreate|nutCharList|nutCharDelete)\b",
        "files": r"\b(?:plugins|gamemode|schema)/[a-z0-9_./-]+\.lua\b",
    }

    result: dict[str, list[str]] = {}

    for key, pattern in patterns.items():
        found = re.findall(pattern, norm, flags=re.IGNORECASE)
        if key == "files":
            found = [clean_path(x) for x in found]
        result[key] = unique_preserve_order(found)[:80]

    return result


def search_snippets(text: str, query: str, window: int = 3, limit: int = 5) -> list[str]:
    terms = [t for t in re.split(r"[^a-zA-Z0-9_]+", query.lower()) if len(t) >= 4]
    if not terms:
        return []

    lines = text.splitlines()
    snippets: list[str] = []

    for idx, line in enumerate(lines):
        lower = line.lower()
        if any(t in lower for t in terms):
            start = max(0, idx - window)
            end = min(len(lines), idx + window + 1)
            snippet = "\n".join(lines[start:end]).strip()
            if snippet and snippet not in snippets:
                snippets.append(snippet)
            if len(snippets) >= limit:
                break

    return snippets


def find_latest_query_result(workspace: Path) -> Path | None:
    candidates = [
        workspace / "manifests" / "semantic" / "qdrant_query_results.md",
        workspace / "qdrant_query_results.md",
        workspace / "reports" / "qdrant_query_results.md",
    ]

    existing = [p for p in candidates if p.exists() and p.is_file()]
    if existing:
        return max(existing, key=lambda p: p.stat().st_mtime)

    matches = list(workspace.rglob("qdrant_query_results.md"))
    if matches:
        return max(matches, key=lambda p: p.stat().st_mtime)

    return None


def run_query_qdrant(config: InvestigationConfig) -> RetrievalRun:
    workspace = config.workspace.resolve()

    cmd = [
        sys.executable,
        "-m",
        "scripts.qdrant.query_qdrant",
        "--workspace",
        str(workspace),
        "--query",
        config.query,
        "--top-k",
        str(config.top_k),
        "--collection",
        config.collection,
        "--write",
        *config.extra_query_args,
    ]

    proc = subprocess.run(
        cmd,
        cwd=str(workspace),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    stdout = proc.stdout
    result_file = find_latest_query_result(workspace)
    result_text = read_text_if_exists(result_file) if result_file else ""

    if not result_text.strip():
        result_text = stdout

    return RetrievalRun(stdout=stdout, result_file=result_file, result_text=result_text)


def load_project_context(config: InvestigationConfig) -> dict[str, str]:
    ws = config.workspace
    context: dict[str, str] = {}

    if config.include_human_context:
        context["human_context"] = (
            read_text_if_exists(ws / "docs" / "human_context.md")
            or read_text_if_exists(ws / "docs" / "human_subsystems" / "human_context.md")
            or read_text_if_exists(ws / "human_context.md")
        )

    if config.include_project_memory:
        context["project_memory"] = (
            read_text_if_exists(ws / "docs" / "project_memory.md")
            or read_text_if_exists(ws / "project_memory.md")
        )

    if config.include_topology_summary:
        context["runtime_topology_summary"] = (
            read_text_if_exists(ws / "manifests" / "normalized" / "runtime_topology_summary.md")
            or read_text_if_exists(ws / "runtime_topology_summary.md")
        )

    return {k: v for k, v in context.items() if v.strip()}


def classify_and_expand(workspace: Path, query: str) -> tuple[str, str]:
    classify_retrieval_intent, build_expanded_query = safe_import_intent(workspace)

    intent_name = "unknown"
    expanded_query = query

    if classify_retrieval_intent:
        try:
            intent = classify_retrieval_intent(query)
            intent_name = str(getattr(intent, "name", intent))
        except Exception as exc:
            intent_name = f"classification_failed:{exc}"

    if build_expanded_query:
        try:
            expanded_query = str(build_expanded_query(query))
        except TypeError:
            try:
                expanded_query = str(build_expanded_query(query, intent_name))
            except Exception:
                expanded_query = query
        except Exception:
            expanded_query = query

    return intent_name, expanded_query


def score_file_for_query(path: str, query: str) -> int:
    q = query.lower()
    p = path.lower()
    score = 0

    if "vendor" in q and "/vendor/" in p:
        score += 5
    if "inventory" in q and "/inventory/" in p:
        score += 5
    if "storage" in q and "/storage/" in p:
        score += 5
    if "grid" in q and "/gridinv/" in p:
        score += 4
    if "char" in q and "/multichar/" in p:
        score += 4

    if "/derma/" in p or p.startswith("plugins/vendor/derma/"):
        score += 3
    if "cl_" in Path(p).name:
        score += 2
    if "sv_" in Path(p).name:
        score += 2
    if "networking" in p:
        score += 2
    if "hooks" in p:
        score += 2

    if "vendor" in q and "price" in q:
        if p == "plugins/vendor/derma/cl_vendor.lua":
            score += 10
        if p == "plugins/vendor/cl_networking.lua":
            score += 7
        if p == "plugins/inventory/cl_hooks.lua":
            score += 6
        if p == "gamemode/core/meta/inventory/cl_base_inventory.lua":
            score += 5

    return score


def score_hook_for_query(hook: str, query: str) -> int:
    q = query.lower()
    h = hook.lower()
    score = 0

    if "vendor" in q and "vendor" in h:
        score += 5
    if "inventory" in q and ("inventory" in h or "item" in h):
        score += 4
    if "storage" in q and "storage" in h:
        score += 4
    if "price" in q and "price" in h:
        score += 10
    if "stock" in h:
        score += 3
    if "money" in h:
        score += 2
    if "datachanged" in h:
        score += 6
    if "createnewinventorypanel" in h or "createinventorypanel" in h:
        score += 4

    return score


def score_network_for_query(msg: str, query: str) -> int:
    q = query.lower()
    m = msg.lower()
    score = 0

    if "vendor" in q and "vendor" in m:
        score += 5
    if "inventory" in q and "inventory" in m:
        score += 5
    if "storage" in q and "storage" in m:
        score += 4
    if "trade" in m:
        score += 3
    if "data" in m:
        score += 2
    if "setpanelstatus" in m:
        score += 4

    return score


def top_scored(values: list[str], scorer, query: str, limit: int) -> list[str]:
    scored = [(scorer(v, query), idx, v) for idx, v in enumerate(values)]
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [v for score, _, v in scored if score > 0][:limit] or values[:limit]


def build_validation_targets(terms: dict[str, list[str]], query: str) -> ValidationTargets:
    files = terms.get("files", [])
    hooks = terms.get("hooks", [])
    network_messages = terms.get("network_messages", [])

    return ValidationTargets(
        priority_files=top_scored(files, score_file_for_query, query, 8),
        priority_hooks=top_scored(hooks, score_hook_for_query, query, 10),
        priority_network_messages=top_scored(network_messages, score_network_for_query, query, 8),
        reason=(
            "Targets are selected from retrieved files/hooks/network messages and ranked "
            "by query relevance. They are validation candidates, not confirmed causes."
        ),
    )


def build_report(
    config: InvestigationConfig,
    retrieval: RetrievalRun,
    intent: str,
    expanded_query: str,
    context: dict[str, str],
) -> tuple[str, ValidationTargets]:
    now = datetime.now().isoformat(timespec="seconds")
    slug = slugify(config.query)
    terms = extract_candidate_terms(retrieval.result_text)
    targets = build_validation_targets(terms, config.query)
    headings = extract_markdown_headings(retrieval.result_text)
    preview = first_lines(retrieval.result_text)

    lines: list[str] = []
    lines.append("# SIGNALIS AI — Investigation Report")
    lines.append("")
    lines.append(f"- Generated: `{now}`")
    lines.append(f"- Query: `{config.query}`")
    lines.append(f"- Intent: `{intent}`")
    lines.append(f"- Top K: `{config.top_k}`")
    lines.append(f"- Collection: `{config.collection}`")
    if retrieval.result_file:
        try:
            rel = retrieval.result_file.relative_to(config.workspace)
            lines.append(f"- Retrieval result file: `{rel}`")
        except ValueError:
            lines.append(f"- Retrieval result file: `{retrieval.result_file}`")
    lines.append(f"- Raw capture: `investigations/generated/{slug}.raw.txt`")
    lines.append("")

    lines.append("## Question")
    lines.append("")
    lines.append(config.query)
    lines.append("")

    lines.append("## Retrieval Intent")
    lines.append("")
    lines.append(f"- Classified intent: `{intent}`")
    lines.append(f"- Expanded query: `{expanded_query}`")
    lines.append("")

    lines.append("## Validation Targets")
    lines.append("")
    lines.append(targets.reason)
    lines.append("")

    lines.append("### Priority Files")
    lines.append("")
    if targets.priority_files:
        for file in targets.priority_files:
            lines.append(f"- `{file}`")
    else:
        lines.append("- none detected")
    lines.append("")

    lines.append("### Priority Hooks")
    lines.append("")
    if targets.priority_hooks:
        for hook in targets.priority_hooks:
            lines.append(f"- `{hook}`")
    else:
        lines.append("- none detected")
    lines.append("")

    lines.append("### Priority Network Messages")
    lines.append("")
    if targets.priority_network_messages:
        for msg in targets.priority_network_messages:
            lines.append(f"- `{msg}`")
    else:
        lines.append("- none detected")
    lines.append("")

    lines.append("## Extracted Signals")
    lines.append("")
    lines.append("These are text-level retrieval signals, not validated truth.")
    lines.append("")
    for key in ["plugins", "hooks", "network_messages", "files"]:
        lines.append(f"### {key}")
        lines.append("")
        values = terms.get(key, [])
        if values:
            for value in values:
                lines.append(f"- `{value}`")
        else:
            lines.append("- none detected")
        lines.append("")

    lines.append("## Retrieval Findings")
    lines.append("")
    if headings:
        lines.append("### Retrieved Headings")
        lines.append("")
        for heading in headings:
            lines.append(f"- {heading}")
        lines.append("")

    lines.append("### Retrieval Preview")
    lines.append("")
    lines.append("```text")
    lines.append(preview[:12000])
    lines.append("```")
    lines.append("")

    lines.append("## Human / Project Context")
    lines.append("")
    if context:
        for name, text in context.items():
            lines.append(f"### {name}")
            lines.append("")
            snippets = search_snippets(text, config.query)
            if snippets:
                for idx, snippet in enumerate(snippets, 1):
                    lines.append(f"#### Snippet {idx}")
                    lines.append("")
                    lines.append("```text")
                    lines.append(snippet[:3000])
                    lines.append("```")
                    lines.append("")
            else:
                lines.append("- no query-matching snippets found")
                lines.append("")
    else:
        lines.append("- no local context files found")
        lines.append("")

    lines.append("## Preliminary Interpretation")
    lines.append("")
    lines.append("- Retrieval evidence has been collected.")
    lines.append("- Validation targets identify the smallest likely source fragments to inspect next.")
    lines.append("- Exact runtime behavior is not proven by this report.")
    lines.append("- Source validation is required before promotion.")
    lines.append("")

    lines.append("## Recommended Validation")
    lines.append("")
    lines.append("Validate in this order:")
    lines.append("")
    lines.append("1. Priority files listed above.")
    lines.append("2. Priority hook listeners/emitters listed above.")
    lines.append("3. Priority network send/receive sites listed above.")
    lines.append("4. Human context for legacy vs authoritative implementation.")
    lines.append("")
    lines.append("For each validation step, capture:")
    lines.append("")
    lines.append("- exact file path")
    lines.append("- exact function/hook/network handler")
    lines.append("- realm")
    lines.append("- whether it mutates authoritative state or only presentation/UI metadata")
    lines.append("")

    lines.append("## Open Questions")
    lines.append("")
    lines.append("- Which retrieved files are authoritative and which are legacy?")
    lines.append("- Which hook/network path actually executes at runtime?")
    lines.append("- Is the issue state corruption, stale client metadata, or UI presentation desync?")
    lines.append("- What exact Lua fragment should be validated next?")
    lines.append("")

    lines.append("## Confidence")
    lines.append("")
    lines.append("`Medium-Low` until exact source validation is performed.")
    lines.append("")

    lines.append("## Promotion Candidates")
    lines.append("")
    lines.append("Only promote after validation:")
    lines.append("")
    lines.append("- `docs/project_memory.md` for durable project state.")
    lines.append("- `docs/human_subsystems/*.md` for human-confirmed facts.")
    lines.append("- `docs/subsystems/*.md` for topology/source-grounded subsystem facts.")
    lines.append("- `docs/ai_subsystems/*.md` for validated architecture synthesis.")
    lines.append("")

    return "\n".join(lines), targets


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate SIGNALIS investigation report.")
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--top-k", type=int, default=12)
    parser.add_argument("--collection", type=str, default=DEFAULT_COLLECTION)
    parser.add_argument("--out-dir", type=Path, default=Path("investigations/generated"))
    parser.add_argument("--extra-query-arg", action="append", default=[])
    parser.add_argument("--no-human-context", action="store_true")
    parser.add_argument("--no-project-memory", action="store_true")
    parser.add_argument("--no-topology-summary", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    workspace = args.workspace.resolve()
    out_dir = args.out_dir if args.out_dir.is_absolute() else workspace / args.out_dir

    config = InvestigationConfig(
        workspace=workspace,
        query=args.query,
        top_k=args.top_k,
        collection=args.collection,
        out_dir=out_dir,
        extra_query_args=args.extra_query_arg,
        include_human_context=not args.no_human_context,
        include_project_memory=not args.no_project_memory,
        include_topology_summary=not args.no_topology_summary,
    )

    intent, expanded_query = classify_and_expand(workspace, args.query)
    retrieval = run_query_qdrant(config)
    context = load_project_context(config)
    report, targets = build_report(config, retrieval, intent, expanded_query, context)

    slug = slugify(args.query)
    out_dir.mkdir(parents=True, exist_ok=True)

    report_path = out_dir / f"{slug}.md"
    raw_path = out_dir / f"{slug}.raw.txt"
    meta_path = out_dir / f"{slug}.json"

    report_path.write_text(report, encoding="utf-8")
    raw_path.write_text(retrieval.result_text, encoding="utf-8", errors="replace")
    meta_path.write_text(
        json.dumps(
            {
                "generated_at": datetime.now().isoformat(timespec="seconds"),
                "query": args.query,
                "intent": intent,
                "expanded_query": expanded_query,
                "top_k": args.top_k,
                "collection": args.collection,
                "report": str(report_path),
                "raw": str(raw_path),
                "retrieval_result_file": str(retrieval.result_file) if retrieval.result_file else None,
                "validation_targets": {
                    "priority_files": targets.priority_files,
                    "priority_hooks": targets.priority_hooks,
                    "priority_network_messages": targets.priority_network_messages,
                },
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"Wrote report: {report_path}")
    print(f"Wrote raw:    {raw_path}")
    print(f"Wrote meta:   {meta_path}")

    if targets.priority_files:
        print("\nPriority files:")
        for file in targets.priority_files[:5]:
            print(f"  - {file}")

    if targets.priority_hooks:
        print("\nPriority hooks:")
        for hook in targets.priority_hooks[:5]:
            print(f"  - {hook}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
