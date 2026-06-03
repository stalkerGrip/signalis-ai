# SIGNALIS AI — Pipeline Artifact Contract Preview

This Markdown is a compact review surface generated from `pipeline_artifact_contract.json`.
The JSON remains the complete machine-readable registry.

## Summary

- Schema: `pipeline_artifact_contract`
- Generated at: `2026-06-03T11:07:46Z`
- Script scan roots: `1`
- Artifact scan roots: `1`
- Scripts scanned: `3`
- Valid script contracts: `2`
- Invalid script contracts: `1`
- Unregistered scripts: `0`
- Artifacts scanned: `6`
- Artifacts with metadata: `4`
- Artifacts without metadata: `2`
- Errors: `4`
- Warnings: `0`

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
| `extraction` | 2 |
| `governance` | 1 |

## Script Contract Status Counts

| Status | Count |
|---|---:|
| `invalid` | 1 |
| `valid` | 2 |

## Registered Scripts

| Script | Stage | Inputs | Outputs | Capabilities | Status |
|---|---|---|---|---|---|
| `scripts.extraction.discover_lua_sources`<br>`scripts/extraction/discover_lua_sources.py` | `extraction` | — | `source_file_manifest` | `file_digests`, `file_realm_hints`, `source_files`, `source_roots` | `active` |
| `scripts.tools.build_pipeline_contract_registry`<br>`scripts/tools/build_pipeline_contract_registry.py` | `governance` | — | `pipeline_artifact_contract`, `script_cli_contracts` | `artifact_lineage`, `artifact_metadata`, `contract_findings`, `script_cli_help`, `script_contracts` | `active` |

## Invalid Script Contracts

| Path | Actual module | Declared script_id | Findings |
|---|---|---|---|
| `scripts/extraction/extract_lua_runtime_signals.py` | `scripts.extraction.extract_lua_runtime_signals` | `scripts.extraction.extract_lua_runtime_signals` | `invalid_promotion_role` |

## Unregistered Scripts

No unregistered scripts.

## Artifact Metadata Source Counts

| Source | Count |
|---|---:|
| `artifact_without_contract_metadata` | 2 |
| `explicit_or_embedded_metadata` | 4 |

## Artifacts With Contract Metadata

| Artifact | Producer | Stage | Family | Capabilities | Status |
|---|---|---|---|---|---|
| `lua_syntax_alphabet:5acdd4b5350419c0`<br>`manifests/alphabet/lua_syntax_alphabet.json` | `manual.source_governed_extraction_alphabet` | `extraction` | `lua_syntax_alphabet` | — | `intermediate` |
| `raw_lua_extraction:96fe38321c5c6176`<br>`manifests/extraction/raw_lua_extraction copy.json` | `scripts.extraction.extract_lua_runtime_signals` | `extraction` | `raw_lua_extraction` | `file_digest_verification`, `line_evidence`, `lua_anonymous_functions`, `lua_assignments` +9 | `intermediate` |
| `raw_lua_extraction:3ad1efa8fcac76d1`<br>`manifests/extraction/raw_lua_extraction.json` | `scripts.extraction.extract_lua_runtime_signals` | `extraction` | `raw_lua_extraction` | `file_digest_verification`, `line_evidence`, `lua_syntax_alphabet_reference`, `source_manifest_reference` | `intermediate` |
| `source_file_manifest:ea53d958bc6f5cee`<br>`manifests/extraction/source_file_manifest.json` | `scripts.extraction.discover_lua_sources` | `extraction` | `source_file_manifest` | `file_digests`, `file_realm_hints`, `source_files`, `source_roots` | `intermediate` |

## Artifacts Missing Metadata

Shown only because `--include-missing-artifacts` was used.

| Path | Schema | Inputs detected |
|---|---|---|
| `docs/runtime/pipeline_artifact_contract.json` | `pipeline_artifact_contract` | `.lua`, `3dpanel.lua`, `3dtext.lua`, `E:/signalis_ai/config/workspace.yaml`, `E:/steam/steamapps/common/GarrysMod/garrysmod/gamemodes/nutscript/entities/effects/nut_smallsmoke.lua` +3300 |
| `docs/runtime/script_contracts.json` | `script_cli_contracts` | `scripts/extraction/discover_lua_sources.py`, `scripts/tools/build_pipeline_contract_registry.py`, `scripts/tools/generate_project_structure.py` |

## Findings

| Severity | Path | Message |
|---|---|---|
| `error` | `manifests/alphabet/lua_syntax_alphabet.json` | `invalid_promotion_role` |
| `error` | `manifests/extraction/raw_lua_extraction copy.json` | `invalid_promotion_role` |
| `error` | `manifests/extraction/raw_lua_extraction.json` | `invalid_promotion_role` |
| `error` | `scripts/extraction/extract_lua_runtime_signals.py` | `invalid_promotion_role` |
