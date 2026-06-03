# SIGNALIS AI — Task Realisation 2.3.1

## Current task

Create `scripts/extraction/compact_raw_lua_extraction.py`.

Input:

```text
manifests/extraction/raw_lua_extraction.json
```

Outputs:

```text
manifests/extraction/raw_lua_extraction_compact.json
manifests/extraction/raw_lua_extraction_index.md
```

This file owns only implementation guidance unique to task `2.3.1`. General architecture, extraction boundary, environment rules, CLI contract doctrine, and artifact registry rules remain owned by the project source files.

## Task-specific decision

Use a separate post-processing script. Do not change `extract_lua_runtime_signals.py` for compaction.

Reason: extraction already happened. The compactor must reshape the existing artifact without reading raw Lua or creating new syntax evidence.

## Problem being solved

The full raw extraction artifact is too large for practical downstream use because each evidence item repeats file metadata and source line text.

The compact artifact should keep the same syntax evidence, but move repeated data into shared indexes.

## Required preservation

The compact output must preserve:

- every evidence item
- original `evidence_id`
- evidence `kind`
- source `file_id` and `line`
- parent/child links such as `parent_call_evidence_id`
- body/span fields
- context paths
- file summaries
- full-artifact lineage
- evidence kind counts

Evidence count and kind counts must match the parent `raw_lua_extraction.json`.

## Compaction shape

Move repeated file metadata into a top-level `files` table keyed by `file_id`.

Move repeated source text into a top-level `line_index` keyed as:

```text
<file_id>:<line>
```

Each compact evidence item should replace nested `evidence` with:

```json
{
  "evidence_id": "raw_lua_evidence:...",
  "kind": "lua_assignment",
  "file_id": "lua_file:...",
  "line": 42,
  "line_key": "lua_file:...:42"
}
```

Then preserve all remaining syntax fields from the original evidence item.

## Markdown index

`raw_lua_extraction_index.md` is a review surface, not a dump.

It should include only:

- compact artifact id
- parent raw extraction artifact id
- source manifest reference
- Lua syntax alphabet reference
- files total
- evidence total
- digest mismatch count
- evidence kind counts table
- top files by evidence count
- output paths

Do not list individual evidence rows.

## Validation checklist

Before task can pass:

- CLI help works.
- Compact JSON is generated.
- Markdown index is generated.
- Compact evidence count equals full evidence count.
- Compact kind counts equal full kind counts.
- Parent evidence references resolve inside compact evidence ids.
- Build pipeline contract registry accepts the script and artifact metadata.
- No runtime or project meaning is added.

## Known non-goals

- No AST parsing.
- No normalization.
- No raw Lua reading.
- No filtering evidence by perceived importance.
- No benchmark-specific handling.
