# SIGNALIS AI — Project Memory

## Current Phase

Retrieval-Guided Architecture Intelligence

Current Sprint:
Investigation Pipeline V1

Current Focus:

Runtime Chain Builder V5 validation against
Runtime Propagation Topology V3.

---

## Current Investigation Update — Vendor Benchmark

Runtime Propagation Topology V3:
PASS

Characterload benchmark:
PASS

Vendor benchmark:
previous FAIL was traced to targeted validation request scope collapse.

Confirmed failure chain:

vendor_purchase_itemdata_invdata_client_apply_targets.json
contained only:

- gamemode/core/libs/item/cl_networking.lua
- invData
- ItemDataChanged

Therefore source validation, runtime facts, and chain builder only received client-apply evidence.

Root cause was not Runtime Chain Builder V5 and not Runtime Propagation Topology V3.

Resolved bottleneck:

targeted_validation_request_generation

Fix applied:

scripts/investigation/build_targeted_validation_request.py now expands known vendor itemdata benchmark chains into full-chain validation targets.

New full-chain target request validation:

vendor_purchase_itemdata_full_chain_targets_v3.json

Source validation result:

vendor_purchase_itemdata_full_chain_source_validation_v3.md

Result:

- files_total: 6
- files_found: 6
- needles_total: 27
- needles_found: 26
- all_needles_found: False

Validated stages:

- vendor open metadata assignment
- vendorSPrice/vendorBPrice assignment
- vendor purchase transfer
- inventory:add
- vendor metadata cleanup
- ITEM:setData
- netstream.Start("invData")
- invData client apply
- ItemDataChanged
- InventoryItemDataChanged UI hook

Only missing needle:

- syncItemAdded

Interpretation:

syncItemAdded is likely outdated stage naming or wrong expected needle, because inventory:add and nutInventoryAdd were validated directly.

---

## Current Bottleneck

### Runtime Fact Sequencing Validation

Status:

ACTIVE

Vendor benchmark status:

PARTIAL PASS

Current evidence:

Full-chain source validation now recovers:

vendor open metadata assignment
→ vendorSPrice/vendorBPrice assignment
→ vendor purchase transfer
→ inventory:add
→ vendor metadata cleanup
→ ITEM:setData
→ netstream.Start("invData")
→ invData
→ ItemDataChanged
→ InventoryItemDataChanged

Source validation coverage:

- files_total: 6
- files_found: 6
- needles_total: 27
- needles_found: 26

Only missing needle:

- syncItemAdded

Current unknown:

Determine how runtime facts are generated from:

vendor_purchase_itemdata_full_chain_source_validation_v3.json

Goal:

Determine whether runtime fact generation preserves:

vendor purchase transfer
→ metadata mutation
→ metadata synchronization
→ client apply
→ UI refresh

or whether sequencing/stage loss still occurs after source validation.

Important:

Do not guess script names.

script_contracts.md is authoritative.

If a runtime-fact generation script is not listed in script_contracts.md:

1. inspect actual pipeline scripts
2. use --help
3. ask human for authoritative module

before continuing investigation.

Current investigation target:

Identify the actual runtime-fact generation module and continue validation from:

vendor_purchase_itemdata_full_chain_source_validation_v3.json

Pipeline-first doctrine remains active.

Do not investigate gameplay fixes.

---

## Completed Bottlenecks

### Extraction Phase
PASS

Completed:

- Hook extraction stabilization
- Registry/global extraction improvements
- Runtime event extraction
- Network extraction
- Timer extraction

Result:

Deterministic runtime topology generation established.

---

### Embedding / Retrieval Phase
PASS

Completed:

- Migration to Python 3.11
- BAAI/bge-small-en-v1.5 adoption
- Qdrant ingestion pipeline
- Reranking integration
- Retrieval validation
- Context pack generation

Result:

Runtime investigations can retrieve authoritative evidence from semantic artifacts.

---

### Runtime Propagation Topology V3
PASS

Completed:

- Runtime graph construction
- Runtime propagation topology generation
- Topology probe tooling
- Character lifecycle validation

Result:

Runtime propagation topology accepted as authoritative runtime structure source.

---

### Characterload Benchmark
PASS

Validated:

PlayerLoadedChar
→ CharacterLoaded
→ inventory initialization
→ PlayerLoadout
→ PostPlayerLoadout

Result:

Characterload benchmark chain successfully reconstructed and promoted.

---

### Runtime Chain Builder Validation
PASS

Completed:

- Runtime chain graph generation
- Runtime chain pathfinder
- Runtime chain builder V4/V5 validation
- Runtime chain promotion validation

Result:

Runtime chain builder correctly reconstructs chains from supplied evidence.

---

### Vendor Benchmark Investigation
PARTIAL PASS

Resolved bottleneck:

Targeted Validation Request Generation

Root cause:

vendor_purchase_itemdata_invdata_client_apply_targets.json
collapsed investigation scope to:

- cl_networking.lua
- invData
- ItemDataChanged

This caused:

- client-only source validation
- client-only runtime facts
- incomplete runtime chains

Fix:

build_targeted_validation_request.py expanded to support benchmark-aware full-chain target generation.

Validation result:

vendor_purchase_itemdata_full_chain_targets_v3.json

Recovered stages:

- vendor metadata assignment
- vendor purchase transfer
- inventory:add
- vendor metadata cleanup
- ITEM:setData
- invData synchronization
- ItemDataChanged
- InventoryItemDataChanged

Result:

Target selection bottleneck resolved.

---

### Eliminated Bottlenecks

Evidence currently does NOT support failures in:

- Runtime Propagation Topology V3
- Runtime Fact Graph generation
- Runtime Fact Ordering
- Runtime Chain Builder V5
- Source Validation execution

These systems behaved correctly given supplied evidence.

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

Critical lesson:

Do not infer script names from prior chats.
script_contracts.md is authoritative.
If a script is missing from script_contracts.md, do not invent it.
Use:
1. docs/runtime/script_contracts.md
2. python -m <module> --help
3. ask user for actual module if not listed

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