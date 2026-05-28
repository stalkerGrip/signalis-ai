# SIGNALIS AI

SIGNALIS AI is a deterministic semantic infrastructure project for a complex Garry's Mod NutScript framework.

It is not an autonomous AI swarm and not blind raw-code ingestion.

The architecture pipeline is:

```text
raw Lua source
→ extraction manifests
→ semantic normalization
→ runtime graphs
→ unified runtime topology
→ semantic documents
→ embeddings/Qdrant
→ retrieval-guided architecture reasoning
```

## Current Phase

```text
Retrieval-Guided Architecture Intelligence
```

Completed:

- raw source extraction
- normalization
- hook graph
- network graph
- timer graph
- runtime topology
- semantic documents
- Qdrant ingestion
- retrieval
- reranking
- context packs
- subsystem document generation

Current topology:

```text
~5066 nodes
~19459 edges
```

## Core Doctrine

Truth comes from:

```text
normalized manifests
runtime topology
doctrine docs
subsystem docs
exact source code when needed
human validation
```

LLMs reason over truth.

LLMs do not define truth.

## Runtime Context

Target runtime:

- Garry's Mod GLua
- NutScript-derived framework
- single-threaded runtime
- event-driven architecture
- hook-heavy execution model
- timer-driven scheduler behavior
- server/client/shared realms
- networking-heavy gameplay/UI synchronization

Important propagation systems:

```text
hook.Run / hook.Add
PLUGIN:* methods
SCHEMA:* methods
netstream2
raw net.Start/net.Receive
timer.Create/timer.Simple
Think hooks
```

## Repository Layout

```text
docs/
  ai_subsystems/
  human_subsystems/
  subsystems/
investigations/
manifests/
runtime_schemas/
scripts/
subsystem_docs/
```

Important docs:

```text
docs/project_memory.md
docs/source_index.md
docs/artifact_policy.md
docs/chatgpt_project_sources.md
subsystem_docs/runtime_doctrine.md
subsystem_docs/event_taxonomy.md
subsystem_docs/networking_model.md
subsystem_docs/persistence_model.md
subsystem_docs/realm_model.md
subsystem_docs/qdrant_plan.md
```

## Priority Systems

Current high-priority systems:

```text
inventory
storage
vendor
healthproblems
needs
biorezonance
lightitems
mining
ragdollinteraction
nextbots
```

Current runtime concerns:

- inventory/UI desync
- vendor stale UI metadata
- PVP/PVE FPS drops
- entity simulation cost
- dynamic light cost
- nextbot overhead
- network synchronization
- memory leaks

## Reasoning Rule

Preferred validation order:

```text
runtime topology
→ doctrine
→ subsystem docs
→ retrieval
→ targeted raw Lua
→ human validation
→ updated semantic artifacts
```

Do not infer exact runtime behavior from raw naming alone.

Do not treat Qdrant as truth.

Do not treat legacy files as authoritative without validation.

## Current Active Investigation

```text
inventory desync after character load
```

Current chain:

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

## Retrieval Evaluation

Evaluate retrieval quality against benchmark expectations:

```powershell
python scripts/qdrant/evaluate_retrieval.py `
  --workspace E:/signalis_ai `
  --out reports/retrieval_eval