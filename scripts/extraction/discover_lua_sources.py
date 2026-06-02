from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("Missing dependency: PyYAML. Install with: pip install PyYAML") from exc


PIPELINE_CONTRACT = {
    "script_id": "scripts.extraction.discover_lua_sources",
    "purpose": "Discover canonical Lua source files from config/workspace.yaml and produce a deterministic source_file_manifest artifact.",
    "pipeline_stage": "extraction",
    "input_families": [],
    "required_input_capabilities": ["workspace_config", "source_roots"],
    "output_families": ["source_file_manifest"],
    "required_output_capabilities": [
        "source_roots",
        "source_files",
        "file_realm_hints",
        "file_digests",
    ],
    "output_schemas": ["source_file_manifest"],
    "artifact_patterns": [
        "manifests/extraction/source_file_manifest.json",
        "manifests/extraction/source_file_manifest.md",
    ],
    "promotion_role": "context_or_debug",
    "canonical_status": "active",
}


SCRIPT_ID = "scripts.extraction.discover_lua_sources"
SCHEMA = "source_file_manifest"
SCHEMA_VERSION = "1"
ARTIFACT_FAMILY = "source_file_manifest"
REQUIRED_CAPABILITIES = [
    "source_roots",
    "source_files",
    "file_realm_hints",
    "file_digests",
]


def stable_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_path(path: Path) -> str:
    return path.as_posix()


def infer_realm_from_filename(path: Path) -> str:
    name = path.name.lower()

    if name.startswith("cl_"):
        return "client"
    if name.startswith("sv_"):
        return "server"
    if name.startswith("sh_"):
        return "shared"

    return "shared"


def load_workspace_config(workspace: Path) -> dict[str, Any]:
    config_path = workspace / "config" / "workspace.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Missing workspace config: {config_path}")

    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}

    if not isinstance(data, dict):
        raise ValueError(f"workspace.yaml must contain a mapping: {config_path}")

    return data


def extract_source_roots(config: dict[str, Any], workspace: Path) -> list[Path]:
    raw_roots = None

    if isinstance(config.get("source_roots"), list):
        raw_roots = config.get("source_roots")
    elif isinstance(config.get("workspace"), dict) and isinstance(config["workspace"].get("source_roots"), list):
        raw_roots = config["workspace"].get("source_roots")
    elif isinstance(config.get("sources"), dict) and isinstance(config["sources"].get("source_roots"), list):
        raw_roots = config["sources"].get("source_roots")

    if not raw_roots:
        raise ValueError(
            "No source_roots found in config/workspace.yaml. "
            "Expected one of: source_roots, workspace.source_roots, sources.source_roots"
        )

    roots: list[Path] = []

    for raw in raw_roots:
        if not isinstance(raw, str):
            raise ValueError(f"source_roots entries must be strings, got: {raw!r}")

        root = Path(raw)

        if not root.is_absolute():
            root = workspace / root

        root = root.resolve()

        if not root.exists():
            raise FileNotFoundError(f"Configured source root does not exist: {root}")

        if not root.is_dir():
            raise NotADirectoryError(f"Configured source root is not a directory: {root}")

        roots.append(root)

    deduped: list[Path] = []
    seen: set[str] = set()

    for root in roots:
        key = str(root).lower()
        if key not in seen:
            seen.add(key)
            deduped.append(root)

    return deduped


def discover_lua_files(source_roots: list[Path]) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []

    for root_index, root in enumerate(source_roots):
        for path in sorted(root.rglob("*.lua"), key=lambda p: p.as_posix().lower()):
            if not path.is_file():
                continue

            rel_path = path.relative_to(root)
            stat = path.stat()
            digest = file_sha256(path)

            files.append(
                {
                    "file_id": "lua_file:" + stable_hash(
                        {
                            "source_root_index": root_index,
                            "relative_path": normalize_path(rel_path),
                            "sha256": digest,
                        }
                    )[:16],
                    "source_root_index": root_index,
                    "source_root": normalize_path(root),
                    "relative_path": normalize_path(rel_path),
                    "absolute_path": normalize_path(path.resolve()),
                    "filename": path.name,
                    "extension": ".lua",
                    "realm_hint": infer_realm_from_filename(path),
                    "size_bytes": stat.st_size,
                    "sha256": digest,
                }
            )

    return files


def build_artifact(workspace: Path) -> dict[str, Any]:
    config = load_workspace_config(workspace)
    source_roots = extract_source_roots(config, workspace)
    source_files = discover_lua_files(source_roots)

    source_root_payload = [
        {
            "source_root_index": index,
            "path": normalize_path(root),
        }
        for index, root in enumerate(source_roots)
    ]

    content_digest = stable_hash(
        {
            "source_roots": source_root_payload,
            "source_files": [
                {
                    "source_root_index": item["source_root_index"],
                    "relative_path": item["relative_path"],
                    "sha256": item["sha256"],
                    "realm_hint": item["realm_hint"],
                }
                for item in source_files
            ],
        }
    )

    artifact_id = f"{ARTIFACT_FAMILY}:{content_digest[:16]}"

    return {
        "schema": SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "artifact_family": ARTIFACT_FAMILY,
        "artifact_id": artifact_id,
        "producer_script": SCRIPT_ID,
        "pipeline_stage": "extraction",
        "canonical_status": "intermediate",
        "promotion_role": "context_or_debug",
        "generated_at": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "required_capabilities": REQUIRED_CAPABILITIES,
        "content_digest": content_digest,
        "workspace": normalize_path(workspace),
        "source_roots": source_root_payload,
        "source_files": source_files,
        "summary": {
            "source_roots_total": len(source_root_payload),
            "lua_files_total": len(source_files),
            "realm_hint_counts": count_by(source_files, "realm_hint"),
        },
        "lineage": {
            "input_kind": "workspace_config",
            "input_artifacts": [normalize_path(workspace / "config" / "workspace.yaml")],
            "parent_artifact_id": None,
            "regenerates": None,
            "regeneration_inputs": {
                "workspace_config": normalize_path(workspace / "config" / "workspace.yaml"),
                "producer_script": SCRIPT_ID,
                "schema": SCHEMA,
                "schema_version": SCHEMA_VERSION,
            },
        },
    }


def count_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}

    for item in items:
        value = str(item.get(key, "unknown"))
        counts[value] = counts.get(value, 0) + 1

    return dict(sorted(counts.items()))


def write_json(path: Path, artifact: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, artifact: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []

    lines.append("# Source File Manifest")
    lines.append("")
    lines.append(f"- Artifact family: `{artifact['artifact_family']}`")
    lines.append(f"- Artifact ID: `{artifact['artifact_id']}`")
    lines.append(f"- Producer: `{artifact['producer_script']}`")
    lines.append(f"- Generated at: `{artifact['generated_at']}`")
    lines.append(f"- Workspace: `{artifact['workspace']}`")
    lines.append(f"- Source roots: `{artifact['summary']['source_roots_total']}`")
    lines.append(f"- Lua files: `{artifact['summary']['lua_files_total']}`")
    lines.append("")
    lines.append("## Required Capabilities")
    lines.append("")

    for capability in artifact["required_capabilities"]:
        lines.append(f"- `{capability}`")

    lines.append("")
    lines.append("## Realm Hint Counts")
    lines.append("")

    for realm, count in artifact["summary"]["realm_hint_counts"].items():
        lines.append(f"- `{realm}`: `{count}`")

    lines.append("")
    lines.append("## Source Roots")
    lines.append("")

    for root in artifact["source_roots"]:
        lines.append(f"- `{root['source_root_index']}`: `{root['path']}`")

    lines.append("")
    lines.append("## Lua Files")
    lines.append("")

    for item in artifact["source_files"]:
        lines.append(
            f"- `{item['relative_path']}` | realm_hint=`{item['realm_hint']}` | "
            f"size=`{item['size_bytes']}` | sha256=`{item['sha256']}`"
        )

    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discover Lua source files from config/workspace.yaml and build source_file_manifest artifacts."
    )

    parser.add_argument(
        "--workspace",
        required=True,
        help="Workspace root containing config/workspace.yaml.",
    )

    parser.add_argument(
        "--out-json",
        default=None,
        help="Output JSON path. Defaults to manifests/extraction/source_file_manifest.json.",
    )

    parser.add_argument(
        "--out-md",
        default=None,
        help="Output Markdown path. Defaults to manifests/extraction/source_file_manifest.md.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    workspace = Path(args.workspace).resolve()

    if not workspace.exists():
        raise FileNotFoundError(f"Workspace does not exist: {workspace}")

    if not workspace.is_dir():
        raise NotADirectoryError(f"Workspace is not a directory: {workspace}")

    artifact = build_artifact(workspace)

    out_json = Path(args.out_json) if args.out_json else workspace / "manifests" / "extraction" / "source_file_manifest.json"
    out_md = Path(args.out_md) if args.out_md else workspace / "manifests" / "extraction" / "source_file_manifest.md"

    if not out_json.is_absolute():
        out_json = workspace / out_json

    if not out_md.is_absolute():
        out_md = workspace / out_md

    write_json(out_json, artifact)
    write_md(out_md, artifact)

    print(f"Lua files: {artifact['summary']['lua_files_total']}")
    print(f"Wrote JSON: {out_json}")
    print(f"Wrote MD:   {out_md}")


if __name__ == "__main__":
    main()