# SIGNALIS AI — Pipeline Artifact Contract Preview

This Markdown is a compact review surface generated from `pipeline_artifact_contract.json`.
The JSON remains the complete machine-readable registry.

## Summary

- Schema: `pipeline_artifact_contract`
- Generated at: `2026-06-04T13:56:52Z`
- Script scan roots: `1`
- Artifact scan roots: `1`
- Scripts scanned: `5`
- Valid script contracts: `4`
- Invalid script contracts: `1`
- Unregistered scripts: `0`
- Artifacts scanned: `8`
- Artifacts with metadata: `6`
- Artifacts without metadata: `2`
- Errors: `3`
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
| `extraction` | 4 |
| `governance` | 1 |

## Script Contract Status Counts

| Status | Count |
|---|---:|
| `invalid` | 1 |
| `valid` | 4 |

## Registered Scripts

| Script | Stage | Inputs | Outputs | Capabilities | Status |
|---|---|---|---|---|---|
| `scripts.extraction.compact_raw_lua_extraction`<br>`scripts/extraction/compact_raw_lua_extraction.py` | `extraction` | `raw_lua_extraction` | `raw_lua_extraction_compact` | `deduplicated_line_evidence`, `evidence_relationship_preservation`, `file_digest_verification`, `lua_syntax_alphabet_reference`, `raw_lua_extraction_reference` +1 | `active` |
| `scripts.extraction.discover_lua_sources`<br>`scripts/extraction/discover_lua_sources.py` | `extraction` | — | `source_file_manifest` | `file_digests`, `file_realm_hints`, `source_files`, `source_roots` | `active` |
| `scripts.extraction.extract_lua_runtime_signals`<br>`scripts/extraction/extract_lua_runtime_signals.py` | `extraction` | `lua_syntax_alphabet`, `source_file_manifest` | `raw_lua_extraction` | `file_digest_verification`, `line_evidence`, `lua_syntax_alphabet_reference`, `source_manifest_reference` | `active` |
| `scripts.tools.build_pipeline_contract_registry`<br>`scripts/tools/build_pipeline_contract_registry.py` | `governance` | — | `pipeline_artifact_contract`, `script_cli_contracts` | `artifact_lineage`, `artifact_metadata`, `contract_findings`, `script_cli_help`, `script_contracts` | `active` |

## Invalid Script Contracts

| Path | Actual module | Declared script_id | Findings |
|---|---|---|---|
| `scripts/extraction/extract_ast_lua_runtime_signals.py` | `scripts.extraction.extract_ast_lua_runtime_signals` | `scripts.extraction.extract_ast_lua_runtime_signals` | `invalid_canonical_status` |

## Unregistered Scripts

No unregistered scripts.

## Artifact Metadata Source Counts

| Source | Count |
|---|---:|
| `artifact_without_contract_metadata` | 2 |
| `explicit_or_embedded_metadata` | 6 |

## Artifacts With Contract Metadata

| Artifact | Producer | Stage | Family | Capabilities | Status |
|---|---|---|---|---|---|
| `lua_ast_syntax_alphabet:ba6dfc309c582a38`<br>`manifests/alphabet/lua_ast_syntax_alphabet.json` | `manual.source_governed_ast_extraction_alphabet` | `extraction` | `lua_ast_syntax_alphabet` | — | `prototype` |
| `lua_syntax_alphabet:32871dfef5c211c0`<br>`manifests/alphabet/lua_syntax_alphabet.json` | `manual.source_governed_extraction_alphabet` | `extraction` | `lua_syntax_alphabet` | — | `intermediate` |
| `ast_lua_extraction:600c782285d262e1`<br>`manifests/extraction/ast_lua_extraction.json` | `scripts.extraction.extract_ast_lua_runtime_signals` | `extraction` | `ast_lua_extraction` | `file_digest_verification`, `lua_ast_syntax_alphabet_reference`, `parser_status`, `source_manifest_reference` +1 | `prototype` |
| `raw_lua_extraction:7cc09f210e5fbd50`<br>`manifests/extraction/raw_lua_extraction.json` | `scripts.extraction.extract_lua_runtime_signals` | `extraction` | `raw_lua_extraction` | `file_digest_verification`, `line_evidence`, `lua_syntax_alphabet_reference`, `source_manifest_reference` | `intermediate` |
| `raw_lua_extraction_compact:022c5534a7b11bce`<br>`manifests/extraction/raw_lua_extraction_compact.json` | `scripts.extraction.compact_raw_lua_extraction` | `extraction` | `raw_lua_extraction_compact` | `deduplicated_line_evidence`, `evidence_relationship_preservation`, `file_digest_verification`, `lua_syntax_alphabet_reference` +2 | `intermediate` |
| `source_file_manifest:a423e63f13adbb3d`<br>`manifests/extraction/source_file_manifest.json` | `scripts.extraction.discover_lua_sources` | `extraction` | `source_file_manifest` | `file_digests`, `file_realm_hints`, `source_files`, `source_roots` | `intermediate` |

## Artifacts Missing Metadata

Shown only because `--include-missing-artifacts` was used.

| Path | Schema | Inputs detected |
|---|---|---|
| `docs/runtime/pipeline_artifact_contract.json` | `pipeline_artifact_contract` | `../../../sh_enums.lua`, `.lua`, `/*.lua`, `/base/*.lua`, `/cl_editor.lua` +3368 |
| `docs/runtime/script_contracts.json` | `script_cli_contracts` | `scripts/extraction/compact_raw_lua_extraction.py`, `scripts/extraction/discover_lua_sources.py`, `scripts/extraction/extract_lua_runtime_signals.py`, `scripts/tools/build_pipeline_contract_registry.py` |

## Findings

| Severity | Path | Message |
|---|---|---|
| `error` | `manifests/alphabet/lua_ast_syntax_alphabet.json` | `invalid_canonical_status` |
| `error` | `manifests/extraction/ast_lua_extraction.json` | `invalid_canonical_status` |
| `error` | `scripts/extraction/extract_ast_lua_runtime_signals.py` | `invalid_canonical_status` |
