# SIGNALIS AI — ChatGPT Project Sources

This document defines the recommended file set for ChatGPT Project Sources.

## Goal

ChatGPT Project Sources should provide stable orientation for architecture reasoning without turning the project into raw context dumping.

The source set should be:

- compact
- durable
- doctrine-heavy
- topology-aware
- subsystem-focused
- updated when project status changes

## Required Core Sources

Always include:

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
subsystem_docs/subsystem_priorities.md
subsystem_docs/qdrant_plan.md
manifests/normalized/runtime_topology_summary.md
```

## Priority Subsystem Sources

Include current priority subsystem docs:

```text
docs/subsystems/inventory.md
docs/subsystems/gridinv.md
docs/subsystems/storage.md
docs/subsystems/vendor.md
docs/subsystems/multichar.md
```

Add others when actively working on them:

```text
docs/subsystems/healthproblems.md
docs/subsystems/needs.md
docs/subsystems/biorezonance.md
docs/subsystems/lightitems.md
docs/subsystems/mining.md
docs/subsystems/nextbots.md
docs/subsystems/ragdollinteraction.md
```

## Human Context Sources

Include human-authored notes when available:

```text
docs/human_subsystems/
```

Current important human context:

```text
vendor system was reworked
some plugins/vendor files may be legacy
vendor price label bug likely involves stale UI metadata
not proven inventory ownership corruption
```

## Optional Active Investigation Sources

Only include active investigation reports when currently discussing that investigation.

Current candidate files:

```text
investigations/inventory_desync_phase1.md
investigations/paths_characterloaded_to_inventory_panel_status.md
investigations/paths_v2_characterloaded_to_inventory_panel_status.md
```

Avoid uploading every context pack by default.

## Do Not Add By Default

Avoid these in ChatGPT Project Sources:

```text
raw Lua source
full runtime_topology.json
full runtime_topology_nodes.json
full runtime_topology_edges.json
qdrant_embeddings.jsonl
qdrant_query_results.md
large generated context packs
temporary logs
private server/source files
```

Use raw Lua only for targeted validation.

## Update Cadence

Update Project Sources when:

- doctrine changes
- project phase changes
- new subsystem docs become important
- human context resolves ambiguity
- an investigation produces durable findings
- source index or artifact policy changes

Do not update Project Sources for every query result.

## Recommended ChatGPT Project Chats

Recommended separation:

```text
Pipeline Core
Qdrant / Retrieval
Runtime Architecture
UI / System Design
Profiling / Performance
```

## Bootstrap Prompt for New Chats

Use:

```text
We are continuing SIGNALIS AI.

Use Project Sources as doctrine and semantic context.
Reason in this order:

runtime topology
→ doctrine
→ subsystem docs
→ Qdrant/retrieval context
→ targeted raw Lua
→ human validation

Do not guess through missing topology/source gaps.
Current phase: Retrieval-Guided Architecture Intelligence.
Current focus: inventory sync, lifecycle ordering, cross-realm UI/network desync, vendor stale UI metadata, subsystem coupling.
```
