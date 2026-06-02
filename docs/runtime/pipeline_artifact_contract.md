# SIGNALIS AI — Pipeline Artifact Contract Preview

This Markdown is a compact review surface generated from `pipeline_artifact_contract.json`.
The JSON remains the complete machine-readable registry.

## Summary

- Schema: `pipeline_artifact_contract`
- Generated at: `2026-06-02T21:13:05Z`
- Script scan roots: `1`
- Artifact scan roots: `1`
- Scripts scanned: `3`
- Valid script contracts: `2`
- Invalid script contracts: `0`
- Unregistered scripts: `1`
- Artifacts scanned: `1`
- Artifacts with metadata: `1`
- Artifacts without metadata: `0`
- Errors: `0`
- Warnings: `1`

## Rules

- The registry scans the workspace by default; it does not depend on hardcoded script or artifact subdirectories.
- Script pipeline truth comes only from explicit PIPELINE_CONTRACT dictionaries.
- The filesystem/module path is evidence; a declared script_id that does not match the actual module is a finding.
- The registry does not infer pipeline stage, schema, or benchmark identity from filename versions.
- Artifacts become pipeline truth only through explicit or embedded artifact metadata.
- Files without artifact metadata are omitted by default and may be surfaced with --include-missing-artifacts for cleanup.
- CLI contracts are captured separately from semantic pipeline contracts.

## Scan Roots

### Script scan roots

- `.`

### Artifact scan roots

- `.`

## Script Stage Counts

| Stage | Count |
|---|---:|
| `extraction` | 1 |
| `governance` | 1 |
| `unknown` | 1 |

## Script Contract Status Counts

| Status | Count |
|---|---:|
| `unregistered` | 1 |
| `valid` | 2 |

## Registered Scripts

| Script | Stage | Inputs | Outputs | Capabilities | Status |
|---|---|---|---|---|---|
| `scripts.extraction.discover_lua_sources`<br>`scripts/extraction/discover_lua_sources.py` | `extraction` | — | `source_file_manifest` | `file_digests`, `file_realm_hints`, `source_files`, `source_roots` | `active` |
| `scripts.tools.build_pipeline_contract_registry`<br>`scripts/tools/build_pipeline_contract_registry.py` | `governance` | — | `pipeline_artifact_contract`, `script_cli_contracts` | `artifact_lineage`, `artifact_metadata`, `contract_findings`, `script_cli_help`, `script_contracts` | `active` |

## Invalid Script Contracts

No invalid script contracts.

## Unregistered Scripts

These are findings only. No pipeline truth is inferred from them.

| Path | Module | Findings |
|---|---|---|
| `scripts/tools/generate_project_structure.py` | `scripts.tools.generate_project_structure` | `missing_pipeline_contract` |

## Artifact Metadata Source Counts

| Source | Count |
|---|---:|
| `explicit_or_embedded_metadata` | 1 |

## Artifacts With Contract Metadata

| Artifact | Producer | Stage | Family | Capabilities | Status |
|---|---|---|---|---|---|
| `source_file_manifest:d1b1a82028f98992`<br>`manifests/extraction/source_file_manifest.json` | `scripts.extraction.discover_lua_sources` | `extraction` | `source_file_manifest` | `file_digests`, `file_realm_hints`, `source_files`, `source_roots` | `intermediate` |

## Findings

| Severity | Path | Message |
|---|---|---|
| `warning` | `scripts/tools/generate_project_structure.py` | `missing_pipeline_contract` |
