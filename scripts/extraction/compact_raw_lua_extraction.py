from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

PIPELINE_CONTRACT = {
    "script_id": "scripts.extraction.compact_raw_lua_extraction",
    "purpose": "Compact full raw Lua syntax evidence into a deduplicated pipeline-friendly extraction artifact and Markdown index without changing syntax facts.",
    "pipeline_stage": "extraction",
    "input_families": ["raw_lua_extraction"],
    "required_input_capabilities": [
        "source_manifest_reference",
        "lua_syntax_alphabet_reference",
        "file_digest_verification",
        "line_evidence",
    ],
    "output_families": ["raw_lua_extraction_compact"],
    "required_output_capabilities": [
        "source_manifest_reference",
        "lua_syntax_alphabet_reference",
        "raw_lua_extraction_reference",
        "file_digest_verification",
        "deduplicated_line_evidence",
        "evidence_relationship_preservation",
    ],
    "output_schemas": ["raw_lua_extraction_compact"],
    "artifact_patterns": [
        "manifests/extraction/raw_lua_extraction_compact.json",
        "manifests/extraction/raw_lua_extraction_index.md",
    ],
    "promotion_role": "intermediate_evidence",
    "canonical_status": "active",
}

SCRIPT_ID = "scripts.extraction.compact_raw_lua_extraction"
SCHEMA = "raw_lua_extraction_compact"
SCHEMA_VERSION = "1"
ARTIFACT_FAMILY = "raw_lua_extraction_compact"


def stable_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def normalize_path(path: Path | str) -> str:
    return Path(path).as_posix() if isinstance(path, Path) else str(path).replace("\\", "/")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return data


def write_json(path: Path, artifact: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def count_by(items: Iterable[dict[str, Any]], key: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for item in items:
        counts[str(item.get(key, "unknown"))] += 1
    return dict(sorted(counts.items()))


def validate_raw_artifact(raw: dict[str, Any], path: Path) -> None:
    if raw.get("schema") != "raw_lua_extraction" or raw.get("artifact_family") != "raw_lua_extraction":
        raise ValueError(f"Input is not raw_lua_extraction: {path}")
    if not isinstance(raw.get("evidence_items"), list):
        raise ValueError("raw_lua_extraction.evidence_items must be a list")
    if not isinstance(raw.get("file_summaries", []), list):
        raise ValueError("raw_lua_extraction.file_summaries must be a list when present")


def line_key(file_id: str, line: int) -> str:
    return f"{file_id}:{line}"


class InternPool:
    def __init__(self, prefix: str) -> None:
        self.prefix = prefix
        self._value_to_ref: dict[str, str] = {}
        self.index: dict[str, Any] = {}
        self._next = 1

    def intern(self, value: Any) -> str:
        key = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        ref = self._value_to_ref.get(key)
        if ref is None:
            ref = f"{self.prefix}_{self._next}"
            self._next += 1
            self._value_to_ref[key] = ref
            self.index[ref] = value
        return ref


def maybe_intern_compact_field(compact: dict[str, Any], key: str, pool: InternPool, ref_key: str | None = None) -> None:
    if key not in compact:
        return
    value = compact.pop(key)
    if value is None:
        compact[ref_key or f"{key}_ref"] = None
        return
    compact[ref_key or f"{key}_ref"] = pool.intern(value)


def compact_item_with_interning(item: dict[str, Any], symbol_pool: InternPool, preview_pool: InternPool, kind_pool: InternPool) -> dict[str, Any]:
    compact = dict(item)

    # Evidence kind is repeated on every item. Keep a ref but preserve counts by resolving kind_ref in validation.
    kind = compact.pop("kind")
    compact["kind_ref"] = kind_pool.intern(kind)

    # Symbol structures are highly repetitive and large. Parent symbols are usually exact repeats.
    maybe_intern_compact_field(compact, "symbol", symbol_pool, "symbol_ref")
    maybe_intern_compact_field(compact, "parent_call_symbol", symbol_pool, "parent_call_symbol_ref")

    # Preview strings are repeated heavily across assignments, arguments, calls, and literals.
    for key in list(compact.keys()):
        if key.endswith("_preview") and isinstance(compact.get(key), str):
            maybe_intern_compact_field(compact, key, preview_pool, f"{key}_ref")

    return compact


def resolve_item_kind(item: dict[str, Any], kind_index: dict[str, Any] | None = None) -> str:
    if "kind" in item:
        return str(item.get("kind", "unknown"))
    if kind_index and item.get("kind_ref") in kind_index:
        return str(kind_index[item.get("kind_ref")])
    return str(item.get("kind_ref", "unknown"))


def count_kinds(items: Iterable[dict[str, Any]], kind_index: dict[str, Any] | None = None) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for item in items:
        counts[resolve_item_kind(item, kind_index)] += 1
    return dict(sorted(counts.items()))


def find_unresolved_intern_references(artifact: dict[str, Any]) -> list[dict[str, Any]]:
    indexes = {
        "kind_ref": artifact.get("kind_index", {}),
        "symbol_ref": artifact.get("symbol_index", {}),
        "parent_call_symbol_ref": artifact.get("symbol_index", {}),
    }
    unresolved: list[dict[str, Any]] = []
    for item in artifact.get("evidence_items", []):
        if not isinstance(item, dict):
            continue
        for key, value in item.items():
            index = indexes.get(key)
            if index is not None and value is not None and value not in index:
                unresolved.append({"evidence_id": item.get("evidence_id"), "field": key, "ref": value})
            if key.endswith("_preview_ref") and value is not None and value not in artifact.get("preview_index", {}):
                unresolved.append({"evidence_id": item.get("evidence_id"), "field": key, "ref": value})
    return unresolved


def collect_files(raw: dict[str, Any]) -> dict[str, dict[str, Any]]:
    files: dict[str, dict[str, Any]] = {}

    for summary in raw.get("file_summaries", []):
        if not isinstance(summary, dict):
            continue
        file_id = summary.get("file_id")
        if not file_id:
            continue
        files[str(file_id)] = {
            "file_id": file_id,
            "source_root_index": summary.get("source_root_index"),
            "relative_path": summary.get("relative_path"),
            "absolute_path": summary.get("absolute_path"),
            "realm_hint": summary.get("realm_hint"),
            "expected_sha256": summary.get("expected_sha256"),
            "actual_sha256": summary.get("actual_sha256"),
            "digest_status": summary.get("digest_status"),
            "encoding": summary.get("encoding"),
            "line_count": summary.get("line_count"),
            "evidence_total": summary.get("evidence_total"),
            "evidence_kind_counts": summary.get("evidence_kind_counts"),
        }

    for item in raw.get("evidence_items", []):
        evidence = item.get("evidence", {}) if isinstance(item, dict) else {}
        if not isinstance(evidence, dict):
            continue
        file_id = evidence.get("file_id")
        if not file_id:
            continue
        files.setdefault(str(file_id), {
            "file_id": file_id,
            "source_root_index": evidence.get("source_root_index"),
            "relative_path": evidence.get("relative_path"),
            "absolute_path": evidence.get("absolute_path"),
            "realm_hint": evidence.get("realm_hint"),
            "expected_sha256": None,
            "actual_sha256": None,
            "digest_status": None,
            "encoding": None,
            "line_count": None,
            "evidence_total": None,
            "evidence_kind_counts": None,
        })

    return dict(sorted(files.items()))


def compact_evidence_items(raw: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    compact_items: list[dict[str, Any]] = []
    line_index: dict[str, dict[str, Any]] = {}
    errors: list[dict[str, Any]] = []
    symbol_pool = InternPool("sym")
    preview_pool = InternPool("prv")
    kind_pool = InternPool("kind")

    for ordinal, item in enumerate(raw.get("evidence_items", [])):
        if not isinstance(item, dict):
            errors.append({"ordinal": ordinal, "error_type": "invalid_evidence_item", "message": "Evidence item is not an object"})
            continue

        evidence = item.get("evidence")
        if not isinstance(evidence, dict):
            errors.append({"ordinal": ordinal, "evidence_id": item.get("evidence_id"), "error_type": "missing_evidence", "message": "Evidence item has no nested evidence object"})
            continue

        file_id = evidence.get("file_id")
        line = evidence.get("line")
        evidence_id = item.get("evidence_id")
        kind = item.get("kind")
        if file_id is None or line is None or evidence_id is None or kind is None:
            errors.append({"ordinal": ordinal, "evidence_id": evidence_id, "error_type": "missing_required_field", "message": "Evidence item must include evidence_id, kind, evidence.file_id, and evidence.line"})
            continue

        try:
            line_int = int(line)
        except (TypeError, ValueError):
            errors.append({"ordinal": ordinal, "evidence_id": evidence_id, "error_type": "invalid_line", "message": f"Line is not an integer: {line!r}"})
            continue

        key = line_key(str(file_id), line_int)
        if key not in line_index:
            line_index[key] = {
                "file_id": file_id,
                "line": line_int,
                "text": evidence.get("text"),
            }

        compact = {
            "evidence_id": evidence_id,
            "kind": kind,
            "file_id": file_id,
            "line": line_int,
            "line_key": key,
        }
        for k, v in item.items():
            if k in {"evidence_id", "kind", "evidence"}:
                continue
            compact[k] = v
        compact_items.append(compact_item_with_interning(compact, symbol_pool, preview_pool, kind_pool))

    indexes = {
        "symbol_index": dict(sorted(symbol_pool.index.items())),
        "preview_index": dict(sorted(preview_pool.index.items())),
        "kind_index": dict(sorted(kind_pool.index.items())),
    }
    return compact_items, dict(sorted(line_index.items())), indexes, errors

def find_unresolved_parent_references(evidence_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    evidence_ids = {str(item.get("evidence_id")) for item in evidence_items if item.get("evidence_id")}
    unresolved: list[dict[str, Any]] = []
    for item in evidence_items:
        source_id = item.get("evidence_id")
        for key, value in item.items():
            if key == "evidence_id":
                continue
            if not key.endswith("evidence_id"):
                continue
            if isinstance(value, str) and value.startswith("raw_lua_evidence:") and value not in evidence_ids:
                unresolved.append({"evidence_id": source_id, "field": key, "target_evidence_id": value})
    return unresolved


def validate_counts(raw: dict[str, Any], compact_items: list[dict[str, Any]], kind_index: dict[str, Any]) -> dict[str, Any]:
    raw_items = raw.get("evidence_items", [])
    raw_kind_counts = count_by(raw_items, "kind")
    compact_kind_counts = count_kinds(compact_items, kind_index)
    raw_summary = raw.get("summary", {}) if isinstance(raw.get("summary"), dict) else {}
    return {
        "raw_evidence_total": len(raw_items),
        "compact_evidence_total": len(compact_items),
        "evidence_total_match": len(raw_items) == len(compact_items),
        "raw_kind_counts": raw_kind_counts,
        "compact_kind_counts": compact_kind_counts,
        "evidence_kind_counts_match": raw_kind_counts == compact_kind_counts,
        "raw_summary_evidence_total_match": raw_summary.get("evidence_total") in (None, len(raw_items)),
        "raw_summary_kind_counts_match": raw_summary.get("evidence_kind_counts") in (None, raw_kind_counts),
        "file_summaries_total": len(raw.get("file_summaries", [])),
    }


def estimate_original_repeated_payload_size(raw: dict[str, Any]) -> dict[str, int]:
    symbol_bytes = 0
    preview_bytes = 0
    kind_bytes = 0
    for item in raw.get("evidence_items", []):
        if not isinstance(item, dict):
            continue
        if "kind" in item:
            kind_bytes += len(json.dumps(item["kind"], ensure_ascii=False))
        for key, value in item.items():
            if key in {"symbol", "parent_call_symbol"}:
                symbol_bytes += len(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
            if key.endswith("_preview") and isinstance(value, str):
                preview_bytes += len(json.dumps(value, ensure_ascii=False))
    return {
        "symbol_payload_bytes_before_interning": symbol_bytes,
        "preview_payload_bytes_before_interning": preview_bytes,
        "kind_payload_bytes_before_interning": kind_bytes,
    }


def estimate_index_payload_size(indexes: dict[str, Any]) -> dict[str, int]:
    return {
        "symbol_index_payload_bytes": len(json.dumps(indexes.get("symbol_index", {}), ensure_ascii=False, sort_keys=True, separators=(",", ":"))),
        "preview_index_payload_bytes": len(json.dumps(indexes.get("preview_index", {}), ensure_ascii=False, sort_keys=True, separators=(",", ":"))),
        "kind_index_payload_bytes": len(json.dumps(indexes.get("kind_index", {}), ensure_ascii=False, sort_keys=True, separators=(",", ":"))),
    }


def build_artifact(workspace: Path, input_json_path: Path) -> dict[str, Any]:
    raw = load_json(input_json_path)
    validate_raw_artifact(raw, input_json_path)

    compact_items, line_index, intern_indexes, compaction_errors = compact_evidence_items(raw)
    files = collect_files(raw)
    unresolved_refs = find_unresolved_parent_references(compact_items)
    validation = validate_counts(raw, compact_items, intern_indexes["kind_index"])
    intern_ref_errors = find_unresolved_intern_references({**intern_indexes, "evidence_items": compact_items})

    evidence_by_file = count_by(compact_items, "file_id")
    top_files = []
    for file_id, count in sorted(evidence_by_file.items(), key=lambda x: (-x[1], x[0]))[:25]:
        f = files.get(file_id, {})
        top_files.append({
            "file_id": file_id,
            "relative_path": f.get("relative_path"),
            "realm_hint": f.get("realm_hint"),
            "evidence_total": count,
            "digest_status": f.get("digest_status"),
        })

    content_digest = stable_hash({
        "raw_lua_extraction_artifact_id": raw.get("artifact_id"),
        "raw_lua_extraction_content_digest": raw.get("content_digest"),
        "files": files,
        "line_index_digest": stable_hash(line_index),
        "evidence_items_digest": stable_hash(compact_items),
        "intern_indexes_digest": stable_hash(intern_indexes),
        "errors": raw.get("errors", []),
        "compaction_errors": compaction_errors,
        "unresolved_parent_evidence_references": unresolved_refs,
    })

    raw_summary = raw.get("summary", {}) if isinstance(raw.get("summary"), dict) else {}
    digest_mismatch_files = raw_summary.get("digest_mismatch_files")
    if digest_mismatch_files is None:
        digest_mismatch_files = sum(1 for f in files.values() if f.get("digest_status") not in (None, "match"))

    intern_size_estimates = estimate_original_repeated_payload_size(raw) | estimate_index_payload_size(intern_indexes)

    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "artifact_family": ARTIFACT_FAMILY,
        "artifact_id": f"{ARTIFACT_FAMILY}:{content_digest[:16]}",
        "producer_script": SCRIPT_ID,
        "pipeline_stage": "extraction",
        "canonical_status": "intermediate",
        "promotion_role": "intermediate_evidence",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "required_capabilities": PIPELINE_CONTRACT["required_output_capabilities"],
        "content_digest": content_digest,
        "workspace": normalize_path(workspace),
        "raw_lua_extraction": {
            "path": normalize_path(input_json_path),
            "artifact_id": raw.get("artifact_id"),
            "content_digest": raw.get("content_digest"),
            "schema": raw.get("schema"),
            "schema_version": raw.get("schema_version"),
        },
        "source_manifest": raw.get("source_manifest"),
        "lua_syntax_alphabet": raw.get("lua_syntax_alphabet"),
        "summary": {
            "files_total": len(files),
            "file_summaries_total": len(raw.get("file_summaries", [])),
            "lines_total": len(line_index),
            "evidence_total": len(compact_items),
            "evidence_kind_counts": count_kinds(compact_items, intern_indexes["kind_index"]),
            "digest_mismatch_files": digest_mismatch_files,
            "unresolved_parent_evidence_references": len(unresolved_refs),
            "unresolved_intern_references": len(intern_ref_errors),
            "compaction_errors": len(compaction_errors),
            "symbol_index_entries": len(intern_indexes["symbol_index"]),
            "preview_index_entries": len(intern_indexes["preview_index"]),
            "kind_index_entries": len(intern_indexes["kind_index"]),
        },
        "validation": validation | {
            "parent_evidence_references_resolve": len(unresolved_refs) == 0,
            "intern_references_resolve": len(intern_ref_errors) == 0,
        },
        "interning": intern_size_estimates,
        "files": files,
        "kind_index": intern_indexes["kind_index"],
        "symbol_index": intern_indexes["symbol_index"],
        "preview_index": intern_indexes["preview_index"],
        "line_index": line_index,
        "file_summaries": raw.get("file_summaries", []),
        "top_files_by_evidence_count": top_files,
        "evidence_items": compact_items,
        "errors": raw.get("errors", []),
        "compaction_errors": compaction_errors,
        "unresolved_parent_evidence_references": unresolved_refs,
        "unresolved_intern_references": intern_ref_errors,
        "lineage": {
            "input_kind": "pipeline_artifact",
            "input_artifacts": [normalize_path(input_json_path)],
            "parent_artifact_id": raw.get("artifact_id"),
            "regenerates": None,
            "regeneration_inputs": {
                "producer_script": SCRIPT_ID,
                "schema": SCHEMA,
                "schema_version": SCHEMA_VERSION,
                "raw_lua_extraction": normalize_path(input_json_path),
                "raw_lua_extraction_artifact_id": raw.get("artifact_id"),
            },
        },
    }


def write_md(path: Path, artifact: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    summary = artifact["summary"]
    lines = [
        "# Raw Lua Extraction Compact Index",
        "",
        f"- Artifact ID: `{artifact['artifact_id']}`",
        f"- Producer: `{artifact['producer_script']}`",
        f"- Raw extraction parent artifact: `{artifact['raw_lua_extraction'].get('artifact_id')}`",
        f"- Raw extraction path: `{artifact['raw_lua_extraction'].get('path')}`",
        f"- Source manifest: `{(artifact.get('source_manifest') or {}).get('path')}`",
        f"- Lua syntax alphabet: `{(artifact.get('lua_syntax_alphabet') or {}).get('path')}`",
        f"- Files total: `{summary['files_total']}`",
        f"- Line index entries: `{summary['lines_total']}`",
        f"- Evidence total: `{summary['evidence_total']}`",
        f"- Digest mismatch files: `{summary['digest_mismatch_files']}`",
        f"- Unresolved parent evidence references: `{summary['unresolved_parent_evidence_references']}`",
        f"- Compaction errors: `{summary['compaction_errors']}`",
        f"- Symbol index entries: `{summary['symbol_index_entries']}`",
        f"- Preview index entries: `{summary['preview_index_entries']}`",
        f"- Kind index entries: `{summary['kind_index_entries']}`",
        "",
        "## Evidence kind counts",
        "",
        "| Kind | Count |",
        "|---|---:|",
    ]
    for kind, count in summary["evidence_kind_counts"].items():
        lines.append(f"| `{kind}` | {count} |")

    lines.extend([
        "",
        "## Top files by evidence count",
        "",
        "| Relative path | Realm | Evidence | Digest |",
        "|---|---|---:|---|",
    ])
    for row in artifact.get("top_files_by_evidence_count", []):
        lines.append(
            f"| `{row.get('relative_path')}` | `{row.get('realm_hint')}` | {row.get('evidence_total')} | `{row.get('digest_status')}` |"
        )

    lines.extend([
        "",
        "## Output contract",
        "",
        "- Full debug artifact: `raw_lua_extraction.json`",
        "- Compact pipeline artifact: `raw_lua_extraction_compact.json`",
        "- Review index: `raw_lua_extraction_index.md`",
        "",
        "## Validation",
        "",
        f"- Evidence total match: `{artifact['validation']['evidence_total_match']}`",
        f"- Evidence kind counts match: `{artifact['validation']['evidence_kind_counts_match']}`",
        f"- Parent evidence references resolve: `{artifact['validation']['parent_evidence_references_resolve']}`",
        f"- Intern references resolve: `{artifact['validation']['intern_references_resolve']}`",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compact raw_lua_extraction into deduplicated line/file indexes without changing syntax evidence."
    )
    parser.add_argument("--workspace", required=True, help="Workspace root containing manifests/extraction/raw_lua_extraction.json.")
    parser.add_argument("--input-json", "--input", dest="input_json", help="Input raw_lua_extraction JSON path. Defaults to manifests/extraction/raw_lua_extraction.json.")
    parser.add_argument("--out-json", help="Output compact JSON path. Defaults to manifests/extraction/raw_lua_extraction_compact.json.")
    parser.add_argument("--out-md", help="Output Markdown index path. Defaults to manifests/extraction/raw_lua_extraction_index.md.")
    parser.add_argument("--fail-on-validation-error", action="store_true", help="Exit with an error when count validation or parent evidence reference validation fails.")
    return parser.parse_args()


def resolve_workspace_path(workspace: Path, maybe_path: str | None, default_relative: Path) -> Path:
    path = Path(maybe_path) if maybe_path else workspace / default_relative
    if not path.is_absolute():
        path = workspace / path
    return path.resolve()


def main() -> None:
    args = parse_args()
    workspace = Path(args.workspace).resolve()
    if not workspace.is_dir():
        raise NotADirectoryError(f"Workspace is not a directory: {workspace}")

    input_json = resolve_workspace_path(workspace, args.input_json, Path("manifests/extraction/raw_lua_extraction.json"))
    out_json = resolve_workspace_path(workspace, args.out_json, Path("manifests/extraction/raw_lua_extraction_compact.json"))
    out_md = resolve_workspace_path(workspace, args.out_md, Path("manifests/extraction/raw_lua_extraction_index.md"))

    artifact = build_artifact(workspace, input_json)
    write_json(out_json, artifact)
    write_md(out_md, artifact)

    validation = artifact["validation"]
    if args.fail_on_validation_error and not (
        validation["evidence_total_match"]
        and validation["evidence_kind_counts_match"]
        and validation["parent_evidence_references_resolve"]
        and validation["intern_references_resolve"]
        and artifact["summary"]["compaction_errors"] == 0
    ):
        raise ValueError("Compact artifact validation failed; inspect validation, compaction_errors, and unresolved_parent_evidence_references.")

    print(f"Compact Lua evidence: {artifact['summary']['evidence_total']}")
    print(f"Files indexed: {artifact['summary']['files_total']}")
    print(f"Line index entries: {artifact['summary']['lines_total']}")
    print(f"Symbol index entries: {artifact['summary']['symbol_index_entries']}")
    print(f"Preview index entries: {artifact['summary']['preview_index_entries']}")
    print(f"Kind index entries: {artifact['summary']['kind_index_entries']}")
    print(f"Unresolved parent evidence references: {artifact['summary']['unresolved_parent_evidence_references']}")
    print(f"Unresolved intern references: {artifact['summary']['unresolved_intern_references']}")
    print(f"Wrote JSON: {out_json}")
    print(f"Wrote MD: {out_md}")


if __name__ == "__main__":
    main()
