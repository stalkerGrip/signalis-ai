# SIGNALIS AI — Qdrant Plan

## Purpose

Qdrant will provide semantic retrieval over the SIGNALIS AI runtime topology and doctrine.

It should NOT replace deterministic extraction or normalization.

It should provide:

```text
architecture memory
semantic search
subsystem retrieval
topology-aware context assembly
```

for ChatGPT, Gemini, and local tools.

---

## Embedding Model

Preferred embedding model:

```text
nomic-ai/nomic-embed-text-v1.5
```

Reason:

```text
good for technical text
good for code-adjacent semantics
good for architecture summaries
local-friendly
```

---

## Primary Collection Content

Primary retrieval layer should store semantic artifacts, not raw Lua first.

Store:

```text
runtime topology nodes
runtime topology edge summaries
plugin topology summaries
file topology summaries
doctrine documents
event taxonomy
networking model
persistence model
realm model
subsystem summaries
```

Raw Lua should be a secondary retrieval layer for exact implementation checks.

---

## Current Semantic Corpus

Already generated:

```text
manifests/semantic/qdrant_documents.jsonl
manifests/semantic/qdrant_documents_summary.md
```

Current document types:

```text
runtime_node
plugin_topology
file_topology
doctrine
```

---

## Recommended Qdrant Collections

### `signalis_semantic`

Primary architecture retrieval.

Contains:

```text
runtime nodes
plugin summaries
file summaries
doctrine
ontology
subsystem docs
```

---

### `signalis_code`

Optional secondary collection.

Contains:

```text
raw Lua chunks
function-level snippets
exact implementation references
```

Use only when semantic retrieval says exact code is needed.

---

### `signalis_diagnostics`

Optional future collection.

Contains:

```text
QA reports
profiling results
runtime measurements
hotspot summaries
```

---

## Metadata Fields

Each embedded document should include metadata such as:

```json
{
  "doc_type": "runtime_node",
  "node_type": "hook_event",
  "plugin": "inventory",
  "subsystem": "inventory_item_storage",
  "realm": "server",
  "file": "plugins/inventory/cl_hooks.lua",
  "degree": 42
}
```

Recommended metadata fields:

```text
doc_type
node_type
edge_type
plugin
subsystem
realm
file
event
message
timer
degree
risk_flags
source_artifact
```

---

## Retrieval Strategy

Queries should retrieve:

```text
semantic topology docs
then related doctrine
then exact raw code only if needed
```

Example query:

```text
Why does inventory desync after character load?
```

Expected retrieval:

```text
inventory topology
character load events
inventory network messages
relevant timers
runtime doctrine
networking model
```

---

## Pipeline Scripts

Next scripts:

```text
scripts/qdrant/embed_qdrant_documents.py
scripts/qdrant/ingest_qdrant.py
scripts/qdrant/query_qdrant.py
```

Optional later:

```text
scripts/qdrant/rebuild_embeddings.py
scripts/qdrant/evaluate_retrieval.py
scripts/qdrant/export_context_pack.py
```

---

## Correct Order

Do not start with Qdrant installation first.

Correct order:

```text
1. generate semantic documents
2. generate embeddings/cache
3. install/run Qdrant
4. ingest vectors
5. test retrieval quality
6. integrate with architect reasoning
```

---

## Future Orchestration Model

Long-term flow:

```text
user asks architecture question
→ query Qdrant
→ retrieve topology + doctrine
→ assemble semantic context package
→ send to ChatGPT/Gemini
→ receive reasoning
→ store summary back into semantic memory
```

---

## Core Principle

Qdrant stores semantic memory.

It does not define truth.

Truth remains:

```text
normalized manifests
runtime topology
doctrine docs
source code when needed
```
