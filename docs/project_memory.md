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

## Local Development Environment

User workstation:

```text
OS: Windows 10
CPU: Ryzen 5 7500F
RAM: 32 GB DDR4
GPU: AMD RX 9060 XT 16 GB
Python torch: 2.12.0+cpu
CUDA available: false
```

CUDA is unavailable because GPU is AMD.
Default ML pipeline should assume CPU inference.
BGE reranker should use use_fp16=False by default.
Do not prioritize ROCm until ranking quality is proven useful.

Canonical Python runtime: Python 3.11.
Python 3.12 caused SentenceTransformer/BGE model loading hangs.
Use .venv311 for Qdrant embeddings, ingestion, retrieval, reranking, and investigation pipeline commands.

Canonical embedding model: BAAI/bge-small-en-v1.5
Canonical embedding dimension: 384
Canonical Python runtime: Python 3.11
Nomic 768-dim defaults are deprecated for this pipeline unless the Qdrant collection is rebuilt with Nomic.

## Installed Investigation Tooling

Installed for Runtime Chain Builder V4 work:

```text
networkx
pydantic
jsonschema
pytest
duckdb
pyinstrument
ripgrep
```
networkx — runtime topology path reconstruction
pydantic — runtime chain schema models
jsonschema — artifact validation
pytest — golden regression tests
duckdb — local topology/evidence query cache
pyinstrument — script profiling

## Investigation Pipeline Lessons

Validated pipeline lesson:

Inventory membership sync and item metadata sync are separate runtime systems, but both may participate in the same causal chain.

For vendor purchase:

```text
gridinv sv_transfer
→ inventory membership transfer
→ Inventory:syncItemAdded
→ item:sync(recipients)
→ nutInventoryAdd
→ purchase metadata cleanup
→ item:setData("vendorSPrice", nil, client)
→ ITEM:setData
→ invData
→ ItemDataChanged
→ grid panel InventoryItemDataChanged
→ populateItems
```
## Future Orchestration Layer

SIGNALIS AI is not currently an autonomous agent system.

Future architecture may add two orchestration roles:

- Planner
- Executor

Planner responsibility:

Question / investigation target
→ choose retrieval strategy
→ choose validation targets
→ choose chain reconstruction strategy
→ decide whether more evidence is needed
→ produce investigation plan

Executor responsibility:

Run deterministic pipeline steps only:

- Qdrant retrieval
- context pack generation
- source validation
- evidence deduplication
- evidence ranking
- runtime chain reconstruction
- synthesis generation
- promotion candidate generation

Important constraint:

Planner and Executor must not define truth.

They only orchestrate deterministic tools over:

1. normalized manifests
2. runtime topology
3. doctrine docs
4. subsystem docs
5. validated source evidence
6. human validation

Planner/Executor are pipeline control layers, not autonomous code editors and not architecture authorities.

Current priority remains:

Evidence Ranking
→ Runtime Chain Reconstruction
→ Investigation Synthesis

Planner/Executor should be implemented only after runtime chain reconstruction is reliable.

## Source Validation Environment

Canonical source roots are defined in:

config/workspace.yaml

Source validation tools must use workspace.yaml and must not assume:

E:/signalis_ai

is the raw Lua source root.

The repository root and source root are separate concepts.

Repository root contains:

- scripts
- investigations
- manifests
- docs

Raw source roots are resolved from workspace.yaml.

All future validation, runtime chain reconstruction, targeted validation, and source discovery tools should load source paths from workspace.yaml.

Do not hardcode source roots in investigation scripts.

## Runtime Chain Builder V4 Lesson

Missing causal steps may be caused by
source-validation coverage gaps.

Before modifying branch reconstruction logic:

1. Verify targeted validation coverage.
2. Verify recovery-input ingestion.
3. Verify step classification.

Branch-builder defects should only be investigated
after validation coverage has been confirmed.

Validated example:

vendor purchase item data propagation chain

Recovered step:

item_metadata_client_apply

## Pipeline-First Gameplay Rule

Raw Lua gameplay fixes are deferred until the Investigation Orchestration Pipeline is reliable.

Known gameplay bugs should be used as benchmark targets for:

Retrieval
→ Source Validation
→ Evidence Ranking
→ Runtime Chain Reconstruction
→ Targeted Validation
→ Promotion

Do not patch gameplay logic simply because a likely source cause is found.

Allowed exceptions:

- pipeline tooling fixes
- source validation fixes
- extraction fixes
- normalization fixes
- topology fixes
- retrieval fixes
- evidence ranking fixes
- runtime chain fixes
- investigation orchestration fixes