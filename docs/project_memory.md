# SIGNALIS AI — Project Memory

## Current Phase

Retrieval-Guided Architecture Intelligence

## Current Sprint

Investigation Pipeline V1 — promoted chain retrieval and architecture synthesis.

## Current Focus

Promoted runtime chains are retrievable architecture knowledge.

The downstream promoted-chain flow works as an artifact-family chain:

runtime_chain_candidate
→ promotion_validation
→ promotion_decision
→ promoted_runtime_chain_registry
→ runtime_chain_corpus
→ qdrant_embeddings
→ qdrant_collection
→ runtime_chain_context_pack
→ architecture_intelligence

Current issue:

The downstream flow still contains historical schema-version suffixes in existing scripts and generated contracts.

Do not treat those suffixes as architectural concepts.

They are compatibility metadata only.

## Current Bottleneck

### Orchestration Entry Point

The pipeline has many working components, but it does not yet have a stable orchestrator that turns a human/local-LLM request into the correct generated artifacts.

Target flow:

natural-language request
→ structured orchestration request
→ retrieval scope
→ doctrine context selection
→ Qdrant retrieval
→ source validation
→ context pack
→ optional runtime chain reconstruction
→ implementation or investigation guidance

Orchestration governance decision:

The orchestration layer must use stable artifact families and capability contracts.

Do not introduce retrieval_plan.vN as a long-term concept.

Use retrieval_scope as the stable family.

Do not introduce runtime_chain_candidate.v8 or any successor-version architecture.

Runtime chain reconstruction remains optional and downstream.

Primary orchestration product:

orchestration_context_pack
→ guidance_report

Runtime chain generation should happen only when the request requires propagation reasoning.

Next implementation order:

1. Define orchestration_request artifact family and required capabilities.
2. Define orchestration_scope artifact family and required capabilities.
3. Define doctrine_context_selection artifact family and required capabilities.
4. Define retrieval_scope artifact family and required capabilities.
5. Define orchestration_context_pack artifact family and required capabilities.
6. Only then create orchestration scripts.

Schema evolution rule:

Schema consumers must check artifact_family and required capabilities, not hardcoded version suffixes.

Breaking schema changes must be handled through compatibility adapters or explicit migration, not by creating parallel versioned pipeline paths.

Do not start from code before these artifact families and compatibility rules are defined.

Important correction:

Do not require human-maintained definitions for every tiny runtime chain.

Human-maintained files should describe doctrine, source authority, subsystem meaning, and orchestration rules.

Concrete runtime chains should be generated from evidence when needed.

Runtime chain reconstruction is optional, not mandatory for every request.

Do not patch generated artifacts.

Do not keep optimizing vendor/characterload as the product.

Vendor and Characterload are regression examples only.

---

## Orchestration Architecture Decision

The orchestration layer is built around four cooperating layers:

```text
Local LLM
= operator
= request interpretation
= query drafting
= artifact rendering
= code generation from validated context

RAG
= evidence access
= doctrine retrieval
= subsystem retrieval
= topology retrieval
= validation artifact retrieval

Pipeline Scripts
= truth machinery
= extraction
= normalization
= topology generation
= retrieval execution
= source validation
= artifact generation

Architect AI
= architecture reviewer
= doctrine compliance
= cross-system reasoning
= risk analysis
= guidance synthesis
```

Core rule:

```text
Local LLM proposes.

RAG retrieves.

Pipeline validates.

Architect AI reviews.

Artifacts preserve.

Guidance reports explain.
```

LLMs do not define truth.

Validated source and deterministic artifacts remain authoritative.

Primary orchestration flow:

```text
natural-language request
→ orchestration_request
→ orchestration_index retrieval
→ orchestration_scope
→ doctrine_context_selection
→ retrieval_scope
→ retrieval_result_set
→ evidence_set
→ source_validation_request
→ source_validation_result
→ orchestration_context_pack
→ guidance_report
→ optional implementation patch
```

Runtime chains remain optional specialist artifacts.

Use runtime chain reconstruction only when propagation reasoning is required.

Generic orchestration requirements:

```text
No benchmark-specific routing.

No vendor-specific routing.

No armor-specific routing.

No hidden keyword maps inside Python.

No version-driven orchestration paths.
```

Scope and doctrine selection should be derived from:

```text
orchestration_index
runtime topology
semantic documents
subsystem documents
promoted runtime chains
source validation artifacts
human authority notes
```

Human-maintained sources define:

```text
meaning
authority
constraints
doctrine
```

Human-maintained sources should not define:

```text
per-request routing
per-feature routing
hardcoded subsystem mappings
```

---

## Project File Budget Rule

ChatGPT Project files are a constrained resource.

Permanent files should only exist when they define:

- doctrine
- governance
- source authority
- subsystem meaning
- artifact family contracts

Do not create a new project file when information belongs in an existing doctrine file.

Preferred order:

1. Update existing doctrine.
2. Update existing contract.
3. Update existing subsystem document.
4. Create a new permanent file only when a genuinely new concept appears.

Generated artifacts are not project files and do not count toward this rule.

The orchestration architecture should minimize permanent file growth.

---

## Completed Bottlenecks

### Artifact Lineage Audit Result

PASS.

Audit proved that `logical_chain_id` is not currently born anywhere in the active pipeline.

Eliminated as lineage origin:

* `runtime_facts.v2`
* `stage_rule_set.v1`
* `ordered_runtime_facts.v1`
* `runtime_chain_candidate.v7`
* `targeted_validation_request.v2`

Important findings:

* `runtime_facts.v2` is neutral runtime evidence.
* `stage_rule_set.v1` is stage classification logic, not chain identity.
* `ordered_runtime_facts.v1` is the first binding point between neutral facts and a selected stage rule set.
* `runtime_chain_candidate.v7` is downstream and must only propagate identity.
* Current scripts implicitly use `stage_rule_set.rule_set_id` as identity, which is the governance leak.

Superseded decision:

The earlier idea to introduce human-maintained per-chain identity configs under config/runtime_chains/*.json is postponed/superseded.

Reason:

The project goal is request-driven orchestration, not manual chain catalog maintenance.

Humans should maintain doctrine, source authority, subsystem meaning, and orchestration rules.

Concrete runtime chain identity should be generated deterministically from validated evidence when runtime chain reconstruction is needed.

Do not require human-maintained logical_chain_id definitions for every small request or chain.

### Benchmark Generalization Bottleneck
PASS

Implemented:

- stage_rule_set.v1
- generic runtime_fact_sequencer
- generic runtime_chain_candidate.v7

Removed benchmark-specific chain construction from active path.

Validated:

- Characterload benchmark
- Vendor benchmark

---

Promotion Governance Automation: PASS
Promoted Runtime Chain Registry: PASS
Runtime Chain Corpus Builder: PASS
Promoted Runtime Chain Retrieval: PASS

Completed:

runtime_chain_candidate.v6
→ promotion_validation.v1
→ promotion_decision.v4
→ promoted_runtime_chain_registry.v1
→ runtime_chain_corpus.v1
→ qdrant_embeddings
→ qdrant_ingest
→ query_qdrant
→ promoted chain retrieval

### Runtime Chain Promotion Validation
PASS

Validated candidate:

vendor_purchase_itemdata_runtime_chain_candidate_v6

Deterministic regeneration:
PASS

Promotion validation:
PASS

Promotion decision:
promoted_confirmed_chain

Recovered chain:

vendor_open_metadata_assignment
→ vendor_purchase_transfer
→ vendor_metadata_cleanup
→ item_metadata_mutation
→ item_metadata_network_send
→ inventory_membership_client_apply
→ item_metadata_client_apply
→ ui_itemdata_refresh_hook

Result:

Promotion can now be validated from
ordered runtime facts rather than
manual reconstruction.

Vendor V6 supersedes previous vendor promotion.

### Contract Adoption Policy

Contract Registry:
PASS

Contract Checker:
PASS

Adoption strategy:

- Legacy scripts are grandfathered.
- Registry inference is acceptable for legacy scripts.
- PIPELINE_CONTRACT metadata is mandatory only for:
  - new scripts
  - major rewrites
  - replacement scripts
  - pipeline infrastructure

Do not pause pipeline progress to retrofit historical scripts.

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

### Runtime Fact Sequencing Validation
PASS

Completed:
Runtime Propagation Topology V3
Characterload Benchmark

Targeted Validation Request Generation
Source Validation
Runtime Fact Generation
Runtime Fact Sequencing Validation

Runtime Chain Builder V5

Vendor Benchmark
PASS

Recovered chain:

vendor_open_metadata_assignment
→ vendor_purchase_transfer
→ vendor_metadata_cleanup
→ item_metadata_mutation
→ item_metadata_network_send
→ inventory_membership_client_apply
→ item_metadata_client_apply
→ ui_itemdata_refresh_hook

Result:

Pipeline bottleneck found
→ fixed
→ revalidated
→ full chain recovered

---

### Vendor Benchmark Investigation
PASS

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

Vendor benchmark completed.

Recovered chain:

vendor_open_metadata_assignment
→ vendor_purchase_transfer
→ vendor_metadata_cleanup
→ item_metadata_mutation
→ item_metadata_network_send
→ inventory_membership_client_apply
→ item_metadata_client_apply
→ ui_itemdata_refresh_hook

Root cause was not:

- Runtime Propagation Topology V3
- Runtime Fact Generation
- Runtime Fact Ordering
- Runtime Chain Builder V5

Root cause was:

- Targeted Validation Request Generation

Pipeline bottleneck identified
→ fixed
→ revalidated
→ benchmark passed

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
- pipeline_artifact_doctrine.md - permanent source for script ownership, artifact ownership, contract metadata rules, and cross-chat recovery order

Critical lesson:

Do not infer script names from prior chats.
pipeline_artifact_doctrine.md is doctrine.
script_contracts.md is generated CLI reference.
pipeline_artifact_contract.json/md is generated machine registry.
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

The original benchmark failure was not caused by:

runtime topology
runtime facts
runtime sequencing
runtime chain building

It was caused by:

targeted validation request scope collapse

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