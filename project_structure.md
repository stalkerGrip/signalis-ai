# SIGNALIS AI — Project Structure

Generated: `2026-05-28T23:59:10`

## Workspace

```text
E:/signalis_ai
```

## Directory Tree

```text
config/
decisions/
docs/
  ai_subsystems/
  human_subsystems/
  subsystems/
embeddings/
graphs/
investigations/
logs/
manifests/
  character_inventory/
  commands/
  custom_hooks/
  derma/
  entities/
  globals/
  hooks/
  items/
  networking/
  normalized/
  persistence/
  plugins/
  registries/
  semantic/
  timers/
prompts/
runtime_schemas/
scripts/
  diagnostics/
  doctrine/
  embeddings/
  extraction/
  graphs/
  manifests/
  normalization/
  profiling/
  qdrant/
  runtime/
  semantic/
  tools/
  utils/
subsystem_docs/
temp/
```

## Known Important Paths

### Runtime Topology Files

- `manifests/normalized/runtime_topology.json` (11579.3 KB)
- `manifests/normalized/runtime_topology_edges.json` (8330.6 KB)
- `manifests/normalized/runtime_topology_nodes.json` (2566.3 KB)

### Qdrant Files

- `manifests/semantic/qdrant_documents.jsonl` (2185.2 KB)
- `manifests/semantic/qdrant_documents_summary.md` (2.0 KB)
- `manifests/semantic/qdrant_embedding_summary.md` (0.3 KB)
- `manifests/semantic/qdrant_embeddings.jsonl` (20126.6 KB)
- `manifests/semantic/qdrant_ingest_summary.md` (0.5 KB)
- `manifests/semantic/qdrant_query_results.md` (100.4 KB)
- `scripts/qdrant/`
- `scripts/qdrant/build_qdrant_documents.py` (16.3 KB)
- `scripts/qdrant/embed_qdrant_documents.py` (2.5 KB)
- `scripts/qdrant/ingest_qdrant.py` (7.1 KB)
- `scripts/qdrant/query_qdrant.py` (7.4 KB)
- `subsystem_docs/qdrant_plan.md` (3.6 KB)

### Investigation Files

- `investigations/inventory_desync_context_pack.md` (105.7 KB)
- `investigations/inventory_desync_phase1.md` (99.7 KB)
- `investigations/paths_characterloaded_to_inventory_panel_status.md` (7.6 KB)
- `investigations/paths_v2_characterloaded_to_inventory_panel_status.md` (10.3 KB)

### Subsystem Docs

- `docs/subsystems/gridinv.md` (11.1 KB)
- `docs/subsystems/healthproblems.md` (12.9 KB)
- `docs/subsystems/inventory.md` (12.2 KB)
- `docs/subsystems/lightitems.md` (12.5 KB)
- `docs/subsystems/multichar.md` (11.9 KB)
- `docs/subsystems/needs.md` (12.5 KB)
- `docs/subsystems/nextbots.md` (2.3 KB)
- `docs/subsystems/storage.md` (11.7 KB)
- `docs/subsystems/vendor.md` (11.3 KB)

### Qdrant Scripts

- `scripts/qdrant/build_qdrant_documents.py` (16.3 KB)
- `scripts/qdrant/context_pack.py` (3.9 KB)
- `scripts/qdrant/embed_qdrant_documents.py` (2.5 KB)
- `scripts/qdrant/ingest_qdrant.py` (7.1 KB)
- `scripts/qdrant/path_reconstruction.py` (7.9 KB)
- `scripts/qdrant/path_reconstruction_v2.py` (11.4 KB)
- `scripts/qdrant/query_qdrant.py` (7.4 KB)
- `scripts/qdrant/rerank_results.py` (5.3 KB)
- `scripts/qdrant/retrieval_intent.py` (3.5 KB)

### Semantic Scripts

- `scripts/semantic/generate_subsystem_docs.py` (10.6 KB)

## Important Matched Files

- `manifests/normalized/network_graph_summary.md` (7.3 KB)
- `manifests/normalized/runtime_graph_edges.json` (2625.8 KB)
- `manifests/normalized/runtime_graph_nodes.json` (1116.8 KB)
- `manifests/normalized/runtime_graph_summary.md` (4.6 KB)
- `manifests/normalized/runtime_topology.json` (11579.3 KB)
- `manifests/normalized/runtime_topology_edges.json` (8330.6 KB)
- `manifests/normalized/runtime_topology_nodes.json` (2566.3 KB)
- `manifests/normalized/runtime_topology_summary.md` (4.4 KB)
- `manifests/normalized/timer_graph_summary.md` (16.5 KB)
- `manifests/semantic/qdrant_documents.jsonl` (2185.2 KB)
- `manifests/semantic/qdrant_documents_summary.md` (2.0 KB)
- `manifests/semantic/qdrant_embedding_summary.md` (0.3 KB)
- `manifests/semantic/qdrant_embeddings.jsonl` (20126.6 KB)
- `manifests/semantic/qdrant_ingest_summary.md` (0.5 KB)
- `manifests/semantic/qdrant_query_results.md` (100.4 KB)
- `scripts/qdrant/context_pack.py` (3.9 KB)
- `scripts/qdrant/rerank_results.py` (5.3 KB)
- `scripts/qdrant/retrieval_intent.py` (3.5 KB)
- `scripts/semantic/generate_subsystem_docs.py` (10.6 KB)
- `subsystem_docs/event_taxonomy.md` (4.2 KB)
- `subsystem_docs/networking_model.md` (3.8 KB)
- `subsystem_docs/persistence_model.md` (3.3 KB)
- `subsystem_docs/qdrant_plan.md` (3.6 KB)
- `subsystem_docs/realm_model.md` (3.5 KB)
- `subsystem_docs/runtime_doctrine.md` (9.9 KB)

## Active Investigation

```text
inventory desync after character load
```

## Current Runtime Chain Under Investigation

```text
CharacterLoaded
→ PlayerLoadedChar
→ PlayerLoadout
→ PostPlayerLoadout
→ inventory initialization / sync
→ inventoryOpen
→ inventorySetPanelStatus
→ client inventory UI
```

## Notes

This file is generated on demand. Re-run this script after adding scripts, manifests, subsystem docs, or investigation reports.
