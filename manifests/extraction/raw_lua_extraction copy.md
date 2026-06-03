# Raw Lua Extraction

- Artifact family: `raw_lua_extraction`
- Artifact ID: `raw_lua_extraction:96fe38321c5c6176`
- Producer: `scripts.extraction.extract_lua_runtime_signals`
- Generated at: `2026-06-03T09:52:45Z`
- Workspace: `E:/signalis_ai`
- Source manifest: `E:/signalis_ai/manifests/extraction/source_file_manifest.json`
- Source manifest artifact ID: `source_file_manifest:ea53d958bc6f5cee`

## Required Capabilities

- `source_manifest_reference`
- `file_digest_verification`
- `lua_assignments`
- `lua_table_fields`
- `lua_literal_values`
- `lua_function_definitions`
- `lua_function_assignments`
- `lua_anonymous_functions`
- `lua_call_expressions`
- `lua_method_call_expressions`
- `lua_call_arguments`
- `lua_function_body_spans`
- `line_evidence`

## Summary

- `files_total`: `1`
- `files_extracted`: `1`
- `files_failed`: `0`
- `digest_mismatch_files`: `0`
- `evidence_total`: `285`
- `evidence_kind_counts`:
  - `lua_assignment`: `38`
  - `lua_call_argument`: `112`
  - `lua_call_expression`: `11`
  - `lua_function_assignment`: `1`
  - `lua_function_definition`: `2`
  - `lua_literal_value`: `58`
  - `lua_method_call_expression`: `51`
  - `lua_table_field`: `12`
- `realm_hint_counts`:
  - `shared`: `1`

## Largest Files by Extracted Evidence

| Evidence | Realm | Digest | File |
|---:|---|---|---|
| `285` | `shared` | `match` | `sh_container.lua` |
