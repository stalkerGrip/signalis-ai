# SIGNALIS AI — Source Index

This file maps durable project artifacts by authority and intended use.

## Canonical Doctrine

These files define reusable semantic rules and architecture interpretation.

```text
docs/project_memory.md
subsystem_docs/runtime_doctrine.md
subsystem_docs/event_taxonomy.md
subsystem_docs/networking_model.md
subsystem_docs/persistence_model.md
subsystem_docs/realm_model.md
subsystem_docs/subsystem_priorities.md
subsystem_docs/qdrant_plan.md
```

Use for:

- project bootstrap
- ChatGPT Project Sources
- Qdrant doctrine documents
- architecture reasoning constraints

## Runtime Topology

Canonical generated topology artifacts:

```text
manifests/normalized/runtime_topology.json
manifests/normalized/runtime_topology_nodes.json
manifests/normalized/runtime_topology_edges.json
manifests/normalized/runtime_topology_summary.md
```

Use summary files for ChatGPT/Gemini.

Use full JSON files for scripts and Qdrant document generation.

Do not paste full topology JSON into chat by default.

## Semantic Retrieval Corpus

Qdrant input and output artifacts:

```text
manifests/semantic/qdrant_documents.jsonl
manifests/semantic/qdrant_documents_summary.md
manifests/semantic/qdrant_embeddings.jsonl
manifests/semantic/qdrant_embedding_summary.md
manifests/semantic/qdrant_ingest_summary.md
```

Use for:

- Qdrant ingestion
- retrieval evaluation
- context pack generation

Do not treat embeddings as source of truth.

## Subsystem Documents

Machine-generated subsystem summaries:

```text
docs/subsystems/inventory.md
docs/subsystems/gridinv.md
docs/subsystems/storage.md
docs/subsystems/vendor.md
docs/subsystems/multichar.md
docs/subsystems/healthproblems.md
docs/subsystems/needs.md
docs/subsystems/biorezonance.md
docs/subsystems/lightitems.md
docs/subsystems/mining.md
docs/subsystems/nextbots.md
docs/subsystems/ragdollinteraction.md
```

Use for:

- subsystem-level retrieval anchors
- architecture reasoning
- investigation scoping
- ChatGPT Project Sources for priority systems

These are topology-derived and may need exact Lua validation for behavior claims.

## Human Subsystem Notes

Human-authored or human-confirmed subsystem facts:

```text
docs/human_subsystems/
```

Use for:

- intended behavior
- legacy-vs-authoritative notes
- confirmed bugs
- reproduction observations
- system ownership notes

Human-confirmed facts outrank AI synthesis.

## AI Synthesis Documents

AI-generated architecture synthesis:

```text
docs/ai_subsystems/
```

Use for:

- architecture interpretation
- refactor proposals
- subsystem contracts
- investigation summaries

These are not authoritative unless grounded in topology, doctrine, source code, or human validation.

## Investigations

Case-specific reports:

```text
investigations/
```

Known active investigation files:

```text
investigations/inventory_desync_context_pack.md
investigations/inventory_desync_phase1.md
investigations/paths_characterloaded_to_inventory_panel_status.md
investigations/paths_v2_characterloaded_to_inventory_panel_status.md
```

Use for:

- bug-focused reasoning
- context packs
- path reconstruction
- validation plans

Promote durable findings from investigations into doctrine, subsystem docs, or human context.

## Scripts

Important script groups:

```text
scripts/extraction/
scripts/normalization/
scripts/graphs/
scripts/qdrant/
scripts/semantic/
scripts/profiling/
scripts/diagnostics/
```

Qdrant scripts:

```text
scripts/qdrant/build_qdrant_documents.py
scripts/qdrant/embed_qdrant_documents.py
scripts/qdrant/ingest_qdrant.py
scripts/qdrant/query_qdrant.py
scripts/qdrant/rerank_results.py
scripts/qdrant/context_pack.py
scripts/qdrant/path_reconstruction.py
scripts/qdrant/path_reconstruction_v2.py
scripts/qdrant/retrieval_intent.py
```

## Raw Lua Source

Raw Lua is not the default reasoning layer.

Use raw Lua only when:

- topology is ambiguous
- exact runtime behavior must be validated
- source authority is disputed
- legacy vs active implementation must be confirmed
- a bug path requires implementation-level proof

Raw Lua should be requested selectively, not dumped wholesale.
