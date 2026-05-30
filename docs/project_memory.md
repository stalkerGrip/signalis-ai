# SIGNALIS AI — Project Memory

## Current Phase

Retrieval-Guided Architecture Intelligence

Current Sprint:
Investigation Pipeline V1

The extraction and normalization bootstrap is complete. The current goal is to use deterministic semantic artifacts, Qdrant retrieval, and external architect reasoning to answer architecture questions about the SIGNALIS NutScript framework.

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

Current canonical topology:

```text
~5066 nodes
~19459 edges
~1696 bridge edges
```

## Source of Truth Order

Architecture reasoning must follow this order:

```text
runtime topology / normalized manifests
→ doctrine docs
→ subsystem docs
→ Qdrant retrieval results
→ targeted raw Lua
→ human validation
→ updated semantic artifacts
```

LLMs do not define truth. LLMs reason over deterministic artifacts.

## Active Architecture Focus

Current investigation and design focus:

- inventory synchronization
- lifecycle ordering
- cross-realm initialization
- network/UI desynchronization
- vendor/inventory presentation metadata
- subsystem coupling
- runtime propagation tracing
- timer/scheduler classification
- profiling-oriented topology analysis

## Important Human Context

Human-validated inventory sync rule:

Item-level data sync and inventory-level data sync are separate.

Item-level data:
ITEM:setData / item:sync
→ netstream "invData"
→ client item.data[key] mutation
→ hook.Run("ItemDataChanged", item, key, oldValue, value)

Inventory-level data:
nutInventoryData
→ inventory instance data mutation
→ hook.Run("InventoryDataChanged", instance, key, oldValue, value)

Do not conflate ItemDataChanged with InventoryDataChanged.

The vendor system was reworked.

Vendor purchase transfer flow is now validated as:
plugins/gridinv/sv_transfer.lua
→ vendor inventory remove
→ player inventory add
→ item:sync
→ nutInventoryAdd
→ invData
→ ItemDataChanged
→ grid inventory panel refresh path

Some files under:

```text
plugins/vendor/*
```

may be legacy and must not automatically be considered authoritative.

Observed vendor bug:

```text
vendor prices sometimes remain visible after buying items
```

Current human interpretation:

```text
likely stale client-side item data or UI presentation state
not proven inventory ownership corruption
```

Recovery observations:

```text
relog usually fixes it
moving item through storage can refresh/clear the incorrect display state
```

Important rule:

```text
vendor price labels are presentation/UI metadata
not authoritative item ownership state
```

## Inventory Understanding

Current working model:

```text
NutScript GridInv
+
SIGNALIS Inventory Extension
```

Ownership chain:

```text
Character
→ inv var
→ Inventory
→ Items
→ Database
```

Known references:

```text
GM:CreateDefaultInventory(character)
nut.char.registerVar("inv", ...)
char:getInv()
```

Equipment slots are believed to move items between inventories rather than duplicate them.

Confidence:

```text
Medium
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

## Open Questions

- Which vendor files are authoritative after the rework?
- Which vendor UI fields persist as stale item presentation metadata?
- Which inventory sync path owns clearing vendor price labels?
- Does storage movement trigger a broader item UI refresh than vendor purchase?
- Which lifecycle event should become the canonical inventory/UI resync boundary?
- Which artifacts should be promoted from investigation reports into doctrine or subsystem docs?

## Update Rule

When human-confirmed information resolves ambiguity, update one of:

- `docs/project_memory.md`
- `docs/human_subsystems/*.md`
- `docs/subsystems/*.md`
- `docs/ai_subsystems/*.md`
- `investigations/*.md`
- project instructions, only for reusable global rules
