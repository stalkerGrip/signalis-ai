# SIGNALIS AI — Pipeline Artifact Contract Preview

This Markdown is a compact review surface generated from `pipeline_artifact_contract.json`.
The JSON remains the complete machine-readable registry.

## Summary

- Schema: `pipeline_artifact_contract`
- Generated at: `2026-06-03T21:15:44Z`
- Script scan roots: `1`
- Artifact scan roots: `1`
- Scripts scanned: `4`
- Valid script contracts: `4`
- Invalid script contracts: `0`
- Unregistered scripts: `0`
- Artifacts scanned: `7`
- Artifacts with metadata: `5`
- Artifacts without metadata: `2`
- Errors: `0`
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
| `extraction` | 3 |
| `governance` | 1 |

## Script Contract Status Counts

| Status | Count |
|---|---:|
| `valid` | 4 |

## Registered Scripts

| Script | Stage | Inputs | Outputs | Capabilities | Status |
|---|---|---|---|---|---|
| `scripts.extraction.compact_raw_lua_extraction`<br>`scripts/extraction/compact_raw_lua_extraction.py` | `extraction` | `raw_lua_extraction` | `raw_lua_extraction_compact` | `deduplicated_line_evidence`, `evidence_relationship_preservation`, `file_digest_verification`, `lua_syntax_alphabet_reference`, `raw_lua_extraction_reference` +1 | `active` |
| `scripts.extraction.discover_lua_sources`<br>`scripts/extraction/discover_lua_sources.py` | `extraction` | — | `source_file_manifest` | `file_digests`, `file_realm_hints`, `source_files`, `source_roots` | `active` |
| `scripts.extraction.extract_lua_runtime_signals`<br>`scripts/extraction/extract_lua_runtime_signals.py` | `extraction` | `lua_syntax_alphabet`, `source_file_manifest` | `raw_lua_extraction` | `file_digest_verification`, `line_evidence`, `lua_syntax_alphabet_reference`, `source_manifest_reference` | `active` |
| `scripts.tools.build_pipeline_contract_registry`<br>`scripts/tools/build_pipeline_contract_registry.py` | `governance` | — | `pipeline_artifact_contract`, `script_cli_contracts` | `artifact_lineage`, `artifact_metadata`, `contract_findings`, `script_cli_help`, `script_contracts` | `active` |

## Invalid Script Contracts

No invalid script contracts.

## Unregistered Scripts

No unregistered scripts.

## Artifact Metadata Source Counts

| Source | Count |
|---|---:|
| `artifact_without_contract_metadata` | 2 |
| `explicit_or_embedded_metadata` | 5 |

## Artifacts With Contract Metadata

| Artifact | Producer | Stage | Family | Capabilities | Status |
|---|---|---|---|---|---|
| `lua_syntax_alphabet:32871dfef5c211c0`<br>`manifests/alphabet/lua_syntax_alphabet.json` | `manual.source_governed_extraction_alphabet` | `extraction` | `lua_syntax_alphabet` | — | `intermediate` |
| `raw_lua_extraction:7cc09f210e5fbd50`<br>`manifests/extraction/raw_lua_extraction.json` | `scripts.extraction.extract_lua_runtime_signals` | `extraction` | `raw_lua_extraction` | `file_digest_verification`, `line_evidence`, `lua_syntax_alphabet_reference`, `source_manifest_reference` | `intermediate` |
| `raw_lua_extraction_compact:022c5534a7b11bce`<br>`manifests/extraction/raw_lua_extraction_compact.json` | `scripts.extraction.compact_raw_lua_extraction` | `extraction` | `raw_lua_extraction_compact` | `deduplicated_line_evidence`, `evidence_relationship_preservation`, `file_digest_verification`, `lua_syntax_alphabet_reference` +2 | `intermediate` |
| `raw_lua_extraction:7cc09f210e5fbd50`<br>`manifests/extraction/raw_lua_extraction_sample.json` | `scripts.extraction.extract_lua_runtime_signals` | `extraction` | `raw_lua_extraction` | `file_digest_verification`, `line_evidence`, `lua_syntax_alphabet_reference`, `source_manifest_reference` | `intermediate` |
| `source_file_manifest:a423e63f13adbb3d`<br>`manifests/extraction/source_file_manifest.json` | `scripts.extraction.discover_lua_sources` | `extraction` | `source_file_manifest` | `file_digests`, `file_realm_hints`, `source_files`, `source_roots` | `intermediate` |

## Artifacts Missing Metadata

Shown only because `--include-missing-artifacts` was used.

| Path | Schema | Inputs detected |
|---|---|---|
| `docs/runtime/pipeline_artifact_contract.json` | `pipeline_artifact_contract` | `../../../sh_enums.lua`, `.lua`, `/*.lua`, `/base/*.lua`, `/cl_editor.lua` +3363 |
| `docs/runtime/script_contracts.json` | `script_cli_contracts` | `scripts/extraction/discover_lua_sources.py`, `scripts/extraction/extract_lua_runtime_signals.py`, `scripts/tools/build_pipeline_contract_registry.py` |

## Findings

No findings.
