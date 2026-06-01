# SIGNALIS AI — Project Memory

## Current Phase

Retrieval-Guided Architecture Intelligence

Current Sprint:
Investigation Pipeline V1

Current Focus:

Runtime Chain Builder V5 validation against
Runtime Propagation Topology V3.

## Current Bottleneck

Runtime Chain Builder V5 validation against
runtime_propagation_topology.json

Validated:

- Runtime Propagation Topology V1 PASS
- Runtime Propagation Topology V2 PASS
- Runtime Propagation Topology V3 PASS

Validated propagation probes:

- netstream:invData
  → ItemDataChanged

- PlayerLoadedChar
  → PlayerLoadout

- PlayerLoadout
  → PostPlayerLoadout

Generated propagation support:

- generated_hook_listener_emits_hook_event: 583
- generated_network_receiver_emits_hook_event: 433

Important finding:

Existing runtime_fact_topology_v3 artifacts were generated against:

manifests/normalized/runtime_topology.json

rather than:

manifests/normalized/runtime_propagation_topology.json

Therefore existing Runtime Chain Builder V5 results do not yet validate Runtime Propagation Topology V3.

Current experiment:

runtime_fact_topology_mapper
→ runtime_propagation_topology.json

runtime_chain_builder_v5
→ runtime_propagation_topology.json

Benchmark chains:

1. vendor_purchase_item_data_propagation_topology_chain

2. characterload_inventory_initialization_lifecycle_chain

Goal:

Determine whether Runtime Propagation Topology V3 resolves the V5 support bottleneck or whether runtime_chain_builder_v5 becomes the next bottleneck.

---

## Completed Bottlenecks

1. Runtime Topology Relationship Discovery
PASS

2. Runtime Propagation Topology V1
PASS

3. Runtime Propagation Topology V2
PASS

4. Runtime Propagation Topology V3
PASS

Validated propagation chains:

- invData → ItemDataChanged

- PlayerLoadedChar → PlayerLoadout

- PlayerLoadout → PostPlayerLoadout

---

## Completed Infrastructure

- raw Lua extraction manifests
- semantic normalization
- hook/event graph
- network graph
- timer graph
- unified runtime topology
- semantic documents
- embeddings/Qdrant ingestion
- deterministic reranking
- context pack generation
- subsystem document generation

Investigation Pipeline V1:

- Runtime Facts V2
- Runtime Fact Graph V2
- Runtime Fact Topology Mapper V3
- Runtime Fact Topology Regression
- Runtime Chain Builder V5
- Runtime Topology Node Probe

Validated promoted chains:

1. vendor_purchase_item_data_propagation_topology_chain
2. characterload_inventory_initialization_lifecycle_chain

---

## Doctrine Sources

- human_context.md
- runtime_doctrine.md
- runtime_propagation_doctrine.md
- runtime_chain_promotion.md

---

## Runtime Propagation Topology Milestone

Runtime Topology Node Probe established that:

runtime_topology.json is primarily a relationship graph.

Examples:

- hook events contain emits/listens_to relationships
- network messages contain sender/receiver relationships
- classification edges exist
- ownership edges exist

However many runtime propagation paths are not directly traversable.

Observed examples:

- netmsg:netstream:invData
  - incoming relationships present
  - outgoing propagation edges absent

- hook:ItemDataChanged
  - listeners exist
  - hook_event -> listener propagation edges absent

- hook:PlayerLoadedChar
  - listeners exist
  - propagation fanout edges absent

Conclusion:

Runtime chain reconstruction requires a dedicated propagation topology artifact.

Planned artifact:

manifests/normalized/runtime_propagation_topology.json

Planned builder:

scripts/investigation/runtime_propagation_topology_builder.py

Purpose:

Transform relationship-oriented topology into traversal-oriented topology suitable for:

- runtime chain reconstruction
- topology-supported validation
- chain confidence scoring
- architecture intelligence

---

## Investigation Pipeline Lessons

Runtime Propagation Topology validation requires:

1. propagation probe PASS

2. runtime_fact_topology_mapper generated against:

   manifests/normalized/runtime_propagation_topology.json

3. runtime_chain_builder_v5 generated against:

   manifests/normalized/runtime_propagation_topology.json

Artifacts generated against runtime_topology.json are not evidence for Runtime Propagation Topology effectiveness.

Before declaring a Runtime Chain Builder bottleneck:

- verify propagation probes
- verify runtime fact mappings
- verify topology artifact source

Preferred outputs:

- hook chains
- network chains
- realm crossings
- inventory ownership chains
- storage ownership chains
- persistence flows

Goal:

runtime reconstruction

not fragment collection

---

## Source Validation Environment:

Current canonical topology artifacts:

Relationship topology:
manifests/normalized/runtime_topology.json

Propagation topology:
manifests/normalized/runtime_propagation_topology.json

Runtime chain reconstruction should prefer:

runtime_propagation_topology.json

Relationship analysis may use:

runtime_topology.json

---


## Project State Preservation Rule

Project State Preservation Rule

At the end of every significant investigation milestone:

1. Update project_memory.md.

2. Update doctrine documents when reusable pipeline rules are discovered.

3. Update subsystem documents when subsystem understanding changes.

4. Do not create duplicate investigation summaries when equivalent generated artifacts already exist.

Record:

- current bottleneck
- completed bottlenecks
- current experiment
- next experiment
- validated conclusions
- invalidated hypotheses

project_memory.md is the canonical cross-chat state artifact.

Future investigation chats should consult project_memory.md before planning new work.

---

## Canonical Environment

Python:
3.11

Embedding model:
BAAI/bge-small-en-v1.5

Qdrant dimension:
384

Source roots:
config/workspace.yaml

Rule:

Workspace root != source root.

Investigation scripts must load source roots from config/workspace.yaml.

---