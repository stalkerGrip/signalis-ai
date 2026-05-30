# SIGNALIS AI — Project Bootstrap

## Project Name

```text
SIGNALIS AI
```

## Purpose

Build deterministic semantic infrastructure for a complex Garry’s Mod NutScript framework.

The project is not an autonomous AI swarm.

The project is a semantic orchestration pipeline:

```text
raw Lua source
→ extraction
→ normalization
→ runtime topology
→ semantic documents
→ embeddings/Qdrant
→ architect reasoning
```

---

## Source of Truth

Primary truth sources:

```text
normalized manifests
runtime topology
semantic documents
doctrine docs
source code for exact checks
```

LLMs reason over truth; they do not define it.

---

## Current State

Completed:

```text
extraction manifests
hook normalization
hook event bus
runtime graph
network graph
network normalization
timer graph
unified runtime topology
runtime doctrine
qdrant document generation
```

Current canonical topology:

```text
~5066 nodes
~19459 edges
~1696 bridge edges
```

---

## Recommended ChatGPT Project Chats

### 1. Pipeline Core

Purpose:

```text
extraction
normalization
graph construction
semantic infrastructure
```

---

### 2. Qdrant / Retrieval

Purpose:

```text
embedding generation
Qdrant ingestion
retrieval quality
query orchestration
context packaging
```

---

### 3. Runtime Architecture

Purpose:

```text
scheduler redesign
network redesign
inventory sync
simulation architecture
subsystem decomposition
```

---

### 4. UI / System Design

Purpose:

```text
HUD
Derma
3D2D panels
inventory UX
entity interaction interfaces
simulation visualization
```

---

### 5. Profiling / Performance

Purpose:

```text
FPS drops
PVP/PVE
nextbots
dynamic lights
memory leaks
timer storms
Think hooks
```

---

## Recommended Project File Set

Current preferred Project source set:

Core doctrine:

- project_bootstrap.md
- runtime_doctrine.md
- event_taxonomy.md
- networking_model.md
- persistence_model.md
- realm_model.md
- subsystem_priorities.md
- qdrant_plan.md
- runtime_topology_summary.md
- project_structure.md

Priority subsystem docs:

- docs/subsystems/inventory.md
- docs/subsystems/storage.md
- docs/subsystems/vendor.md
- docs/subsystems/gridinv.md
- docs/subsystems/multichar.md

Avoid adding by default:

- raw Lua
- large manifests
- qdrant_query_results.md
- embedding summaries
- transient investigation reports

Raw source should only be used for exact runtime validation.

---

## External Reasoning Engines

### ChatGPT

Best for:

```text
architecture abstraction
ontology design
runtime reasoning
pipeline strategy
cross-system synthesis
```

### Gemini

Best for:

```text
large-context correlation
bulk subsystem review
alternative architecture reasoning
```

### Local Qwen2.5-Coder

Best for:

```text
autocomplete
small refactors
manifest work
deterministic code transformations
```

---

## Current Active Phase

The project has completed semantic infrastructure bootstrap.

Completed phases:

- extraction manifests
- hook normalization
- hook event bus reconstruction
- network graph
- timer graph
- unified runtime topology
- semantic documents
- embeddings
- Qdrant ingestion
- initial retrieval validation
- deterministic reranking
- context pack export
- subsystem document generation

Current phase:

Retrieval-Guided Architecture Intelligence

Current focus:

- topology-aware retrieval
- runtime propagation tracing
- subsystem semantic documents
- investigation context packs
- inventory synchronization analysis
- lifecycle ordering analysis
- cross-realm network/UI synchronization
- timer/scheduler noise reduction

Current pipeline:

query
→ intent classification
→ query expansion
→ Qdrant retrieval
→ deterministic reranking
→ context pack generation
→ topology path reconstruction
→ exact source validation when required

---

## Investigation Evidence Doctrine

Investigation should not operate directly on retrieval results.

Required investigation pipeline:

```text
Retrieval
→ Source Validation
→ Evidence Deduplication
→ Evidence Ranking
→ Investigation
→ Architecture Intelligence
```

Source validation establishes truth.

Deduplication establishes unique evidence.

Ranking establishes likely causal importance.

Investigation consumes ranked evidence only.

Large quantities of overlapping source fragments are validation noise, not additional evidence.

A fragment count increase does not imply investigation quality increase.

Priority:

```text
unique causal evidence
>
fragment count
>
keyword frequency
```

Preferred investigation outputs:

```text
hook propagation chains
network propagation chains
realm transitions
inventory ownership chains
storage ownership chains
persistence flows
```

The objective of investigation is runtime reconstruction, not fragment collection.

## Long-Term Vision

The final system should support questions like:

```text
Why does inventory desync after character load?
Which timers can affect PVP FPS?
What systems emit network messages during storage interaction?
Which plugins depend on SaveData?
What should be refactored first for simulation performance?
```

using:

```text
Qdrant retrieval
runtime topology
semantic doctrine
external architect reasoning
```

---

## Core Principle

```text
Deterministic infrastructure first.
LLM architecture reasoning second.
```
