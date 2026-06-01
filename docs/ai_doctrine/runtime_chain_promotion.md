# SIGNALIS AI — Runtime Chain Promotion Doctrine

## Purpose

Runtime chain promotion defines when a reconstructed runtime chain is reliable enough to become a reusable semantic artifact.

Promotion does not mean the chain is perfect.

Promotion means the chain is sufficiently supported by deterministic artifacts, source validation, topology evidence, and human context to be used by future retrieval, validation, and architecture reasoning.

---

## Core Rule

LLMs do not promote chains by opinion.

A runtime chain may only be promoted when supported by deterministic evidence.

Promotion consumes:

```text
runtime facts
→ runtime fact graph
→ runtime fact topology mapping
→ runtime chain candidate
→ topology support
→ source validation
→ human validation when required
```

---

## Promotion Inputs

A promotable chain should have:

```text
runtime_facts.v2
runtime_fact_graph.v2
runtime_fact_topology_mapper output
runtime_chain_builder output
source validation output
human validation notes when applicable
```

Runtime chain reconstruction should prefer:

```text
manifests/normalized/runtime_propagation_topology.json
```

Relationship-only analysis may use:

```text
manifests/normalized/runtime_topology.json
```

Artifacts generated against `runtime_topology.json` are not valid evidence for propagation-chain support.

---

## Promotion Criteria

A chain may be promoted when it satisfies most or all of:

```text
1. Facts are normalized and deduplicated.
2. Runtime facts map to topology nodes.
3. Critical links are topology-supported.
4. Required runtime stages are present.
5. Source validation confirms key operations.
6. Realm transitions are explicit or explainable.
7. Network boundaries are identified when present.
8. Ownership/state mutation boundaries are identified when present.
9. Human validation does not contradict the chain.
10. The chain explains the target runtime behavior better than competing hypotheses.
```

---

## Required Evidence Types

Preferred evidence order:

```text
1. SIGNALIS source code
2. SIGNALIS runtime topology
3. SIGNALIS doctrine/docs
4. Human validation
5. External NutScript
6. Facepunch Wiki
```

External NutScript is comparison only.

It must not override validated SIGNALIS behavior.

---

## Confidence Levels

### High Confidence

Use when:

```text
- all critical stages are present
- topology supports key propagation links
- source validation confirms core operations
- realm/network/state transitions are coherent
- no major unresolved contradiction exists
```

High-confidence chains may be used as architecture knowledge.

---

### Medium Confidence

Use when:

```text
- main runtime path is coherent
- most stages are supported
- at least some topology or source validation exists
- missing evidence does not invalidate the chain
- unresolved gaps are known and documented
```

Medium-confidence chains may be promoted as useful architecture artifacts, but should retain caveats.

---

### Low Confidence

Use when:

```text
- chain is mostly inferred
- topology support is weak or absent
- source validation is incomplete
- major runtime stages are missing
- competing explanations remain plausible
```

Low-confidence chains should not be promoted except as explicit investigation candidates.

---

### None

Use when:

```text
- facts do not map
- links are unsupported
- chain is fragment-based rather than propagation-based
- source validation contradicts the chain
- the chain depends on guessed runtime behavior
```

Do not promote.

---

## Rejection Conditions

Reject promotion when:

```text
1. Chain depends on raw retrieval fragments without source validation.
2. Runtime facts are not normalized.
3. Fact topology mappings are missing for critical stages.
4. Critical propagation links are unsupported and unexplained.
5. Chain uses relationship topology as if it were propagation topology.
6. Chain conflates item data sync with inventory membership sync.
7. Chain treats UI metadata as authoritative ownership state.
8. Chain contradicts human_context.md.
9. Chain assumes client authority without evidence.
10. Chain requires gameplay Lua bugfixing to become valid.
```

---

## Runtime Propagation Requirement

Runtime chains should reconstruct propagation, not containment.

Preferred outputs:

```text
hook chains
network chains
realm crossings
inventory ownership chains
storage ownership chains
persistence flows
```

Goal:

```text
runtime reconstruction
not fragment collection
```

Relationship evidence such as:

```text
file owns listener
plugin owns file
hook has listener
network message has receiver
```

is useful, but not sufficient by itself.

---

## Topology Support Rule

For propagation-chain promotion, topology support must be checked against:

```text
runtime_propagation_topology.json
```

Required validation sequence:

```text
runtime_propagation_topology_probe
→ runtime_fact_topology_mapper using runtime_propagation_topology.json
→ runtime_chain_builder_v5 using runtime_propagation_topology.json
```

If an artifact was generated against:

```text
runtime_topology.json
```

then it is not evidence for propagation topology effectiveness.

---

## Source Validation Rule

Promotion should not rely on raw Lua inspection unless needed.

Validation order:

```text
runtime topology
→ doctrine
→ subsystem docs
→ retrieval
→ targeted raw Lua
→ human validation
→ updated semantic artifacts
```

Raw Lua is used for exact validation, not first-pass reasoning.

---

## Human Validation Rule

Ask the project owner only for:

```text
intended behavior
subsystem history
legacy vs authoritative implementation
runtime observations
reproduction steps
targeted Lua
```

Human-confirmed behavior overrides AI assumptions.

Human validation should be recorded in:

```text
human_context.md
```

---

## Vendor / Inventory Promotion Rule

For vendor and inventory chains:

Do not conflate:

```text
InventoryDataChanged
```

with:

```text
ItemDataChanged
```

Do not conflate:

```text
inventory membership sync
```

with:

```text
item metadata sync
```

Vendor price labels are presentation metadata.

They are not authoritative ownership state.

A valid vendor purchase item-data chain must distinguish:

```text
inventory ownership transfer
item metadata mutation
item metadata sync
client item data application
UI refresh / presentation update
```

---

## Promotion Output

A promoted chain should record:

```text
title
confidence
score
supported links
unsupported links
missing stages
topology artifact used
source validation artifact used
runtime facts artifact used
promotion reason
known caveats
```

Promoted chains should be reusable by:

```text
Qdrant retrieval
future investigations
architecture intelligence
regression validation
```

---

## Current Known Promoted Benchmark Chains

Current benchmark chains:

```text
vendor_purchase_item_data_propagation_topology_chain
characterload_inventory_initialization_lifecycle_chain
```

These chains are currently used to validate whether Runtime Chain Builder V5 correctly consumes Runtime Propagation Topology V3.

---

## Current Active Validation Rule

Before declaring Runtime Chain Builder V5 fixed or broken:

```text
1. Rebuild runtime_fact_topology_mapper against runtime_propagation_topology.json.
2. Rebuild runtime_chain_builder_v5 against runtime_propagation_topology.json.
3. Compare supported links against previous baseline.
4. If supported links remain zero while probes pass, inspect runtime_chain_builder_v5 pathfinding logic.
```

Previous baseline:

```text
Supported: 0
```

Expected improvement:

```text
Supported links > 0
```

for at least:

```text
netstream:invData → ItemDataChanged
PlayerLoadedChar → PlayerLoadout
PlayerLoadout → PostPlayerLoadout
```

---

## Doctrine Maintenance

Update this document when:

```text
promotion gates change
confidence scoring changes
runtime_chain_builder changes
runtime_chain_promoter changes
new rejection conditions are discovered
human validation changes promotion policy
```

Do not duplicate generated investigation artifacts here.

This document defines promotion rules, not individual investigation reports.
