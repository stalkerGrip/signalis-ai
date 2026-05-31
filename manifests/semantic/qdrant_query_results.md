# Qdrant Query Results

Collection: `signalis_semantic`
Query: `vendor purchase item metadata sync`
Expanded query used: `vendor purchase item metadata sync client UI file file_summary hook_emitter hook_event hook_listener invAct inventory inventoryOpen netstream.Hook netstream.Start network_context network_message network_operation network_payload_operation plugin plugin_summary realm crossing server authoritative vendor`
Top K: **10**
Retrieve K: **50**
Model: `nomic-ai/nomic-embed-text-v1.5`
Hash query: `False`

## Returned results: 10

## Result 1

- Score: **-0.0225**
- Rerank score: `0.31`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:inventory:+0.05', 'network_text_match:+0.10', 'doctrine_required:+0.16', 'file_subsystem:inventory:+0.07', 'causal:itemdatachanged:+0.18', 'causal:nutinventoryadd:+0.16', 'causal:nutinventoryremove:+0.14', 'causal_network_flow:+0.14', 'state_mutation_or_sync:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:85a7da1efbcd3b66`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/subsystems/inventory.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:85a7da1efbcd3b66",
  "doc_type": "doctrine",
  "content_hash": "1c9d2a0945769b3df5df6c52b5cb331b5f800bcaa9c105940490a2028d80b088",
  "embedding_dim": 384,
  "text": "# Subsystem: inventory\n\n## Purpose\n\nDeterministic subsystem summary generated from runtime topology.\n\n## Topology Summary\n\n- Nodes: **443**\n- Edges: **7885**\n\n## Node Types\n\n- `hook_event`: 97\n- `network_operation`: 83\n- `hook_listener`: 62\n- `hook_emitter`: 44\n- `network_payload_operation`: 39\n- `file`: 37\n- `network_message`: 34\n- `network_context`: 13\n- `plugin`: 12\n- `timer_operation`: 9\n- `realm`: 3\n- `event_class`: 3\n- `timer`: 2\n- `timer_class`: 2\n- `subsystem`: 1\n- `gamemode`: 1\n- `timer_risk`: 1\n\n## Edge Types\n\n- `runs_in_realm`: 4470\n- `classified_as`: 577\n- `registers_listener`: 331\n- `listens_to_event`: 261\n- `listens_to`: 198\n- `contains_listener`: 192\n- `owns_timer_operation`: 191\n- `owns_file`: 188\n- `has_timer_risk`: 182\n- `contains_network_operation`: 177\n- `dispatches_to`: 129\n- `emits`: 104\n- `file_sends_network_message`: 101\n- `contains_timer_operation`: 99\n- `contains_emitter`: 96\n- `emits_event`: 80\n- `file_receives_network_message`: 71\n- `contains_network_payload_operation`: 67\n- `references_timer`: 64\n- `sends_network_message`: 47\n\n## Major Hooks\n\n- `listen CreateInventoryPanel @ plugins\\gridinv\\plugins\\gridinvui\\sh_plugin.lua:8`: 2\n- `listen ItemDraggedOutOfInventory @ plugins\\gridinv\\sh_plugin.lua:33`: 2\n- `listen CreateInventoryPanel @ plugins\\_disabled\\simpleinv\\plugins\\listinvui\\sh_plugin.lua:8`: 2\n- `listen ns1SetupInventorySearch @ plugins\\tying\\sh_charsearch.lua:4`: 2\n- `listen DisplayInventoryNut1_1_beta @ plugins\\ragdollinteraction\\interaction\\cl_hooks.lua:83`: 2\n- `listen DisplayInventoryNut1_1 @ plugins\\ragdollinteraction\\interaction\\cl_hooks.lua:152`: 2\n- `VendorItemStockUpdated`: 1\n- `OnTakeShipmentItem`: 1\n- `name`: 1\n- `listen TransferInventory @ plugins\\ragdollinteraction\\interaction\\sv_hooks.lua:144`: 1\n- `emit CreateNewInventoryPanel @ plugins\\ragdollinteraction\\interaction\\cl_hooks.lua:90`: 1\n- `ItemShouldSave`: 1\n- `OnRequestItemTransfer`: 1\n- `listen SetupBagInventoryAccessRules @ plugins\\gridinv\\sv_access_rules.lua:54`: 1\n- `InventoryItemAdded`: 1\n- `PlayerCanPickupWeapon`: 1\n- `emit InventoryItemRemoved @ gamemode\\core\\libs\\item\\cl_networking.lua:75`: 1\n- `exitStorage`: 1\n- `ItemDataChanged`: 1\n- `emit PlayerLoadout @ gamemode\\core\\hooks\\sv_hooks.lua:263`: 1\n\n## Major Network Signals\n\n- `netstream send inventorySetPanelStatus`: 10\n- `netstream send invAct`: 3\n- `netstream send hookName`: 2\n- `netstream send itemSplitAdd`: 2\n- `netstream send inventoryUpdSkin`: 2\n- `send nutInventoryDelete`: 2\n- `netstream send storageInventory`: 2\n- `netstream hook itemSplitDrop`: 2\n- `Start nutInventoryDelete`: 2\n- `Start nutTransferItem`: 1\n- `foodReadyPartAddClient`: 1\n- `register nutInventoryRemove`: 1\n- `receive OpenMyInv`: 1\n- `netstream send inventoryOpen`: 1\n- `netstream hook inventoryCloseOnAction`: 1\n- `netstream hook mnhrOpenVisor`: 1\n- `netstream hook invAct`: 1\n- `send nutInventoryData`: 1\n- `receive nutInventoryRemove`: 1\n- `send nutInventoryAdd`: 1\n\n## Lifecycle Propagation",
  "metadata": {
    "chunk_index": 0,
    "file": "docs/subsystems/inventory.md",
    "node_type": "doctrine",
    "source_id": "docs/subsystems/inventory.md"
  },
  "node_type": "doctrine",
  "file": "docs/subsystems/inventory.md"
}
```

### Text

```text
# Subsystem: inventory

## Purpose

Deterministic subsystem summary generated from runtime topology.

## Topology Summary

- Nodes: **443**
- Edges: **7885**

## Node Types

- `hook_event`: 97
- `network_operation`: 83
- `hook_listener`: 62
- `hook_emitter`: 44
- `network_payload_operation`: 39
- `file`: 37
- `network_message`: 34
- `network_context`: 13
- `plugin`: 12
- `timer_operation`: 9
- `realm`: 3
- `event_class`: 3
- `timer`: 2
- `timer_class`: 2
- `subsystem`: 1
- `gamemode`: 1
- `timer_risk`: 1

## Edge Types

- `runs_in_realm`: 4470
- `classified_as`: 577
- `registers_listener`: 331
- `listens_to_event`: 261
- `listens_to`: 198
- `contains_listener`: 192
- `owns_timer_operation`: 191
- `owns_file`: 188
- `has_timer_risk`: 182
- `contains_network_operation`: 177
- `dispatches_to`: 129
- `emits`: 104
- `file_sends_network_message`: 101
- `contains_timer_operation`: 99
- `contains_emitter`: 96
- `emits_event`: 80
- `file_receives_network_message`: 71
- `contains_network_payload_operation`: 67
- `references_timer`: 64
- `sends_network_message`: 47

## Major Hooks

- `listen CreateInventoryPanel @ plugins\gridinv\plugins\gridinvui\sh_plugin.lua:8`: 2
- `listen ItemDraggedOutOfInventory @ plugins\gridinv\sh_plugin.lua:33`: 2
- `listen CreateInventoryPanel @ plugins\_disabled\simpleinv\plugins\listinvui\sh_plugin.lua:8`: 2
- `listen ns1SetupInventorySearch @ plugins\tying\sh_charsearch.lua:4`: 2
- `listen DisplayInventoryNut1_1_beta @ plugins\ragdollinteraction\interaction\cl_hooks.lua:83`: 2
- `listen DisplayInventoryNut1_1 @ plugins\ragdollinteraction\interaction\cl_hooks.lua:152`: 2
- `VendorItemStockUpdated`: 1
- `OnTakeShipmentItem`: 1
- `name`: 1
- `listen TransferInventory @ plugins\ragdollinteraction\interaction\sv_hooks.lua:144`: 1
- `emit CreateNewInventor...
```

## Result 2

- Score: **-0.0212**
- Rerank score: `0.1935`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:inventory:+0.05', 'network_text_match:+0.10', 'doctrine_required:+0.16', 'causal:sync:+0.10', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:5516a60760c5a26c`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `subsystem_docs/pipeline_state.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:5516a60760c5a26c",
  "doc_type": "doctrine",
  "content_hash": "e912116becdedf46e69a4abf5d112c4c523a949926a822a06bbddeb90d59464f",
  "embedding_dim": 384,
  "text": "nerated retrieval-ready semantic documents:\n\n```text\nmanifests/semantic/qdrant_documents.jsonl\nmanifests/semantic/qdrant_documents_summary.md\n```\n\nDocument types:\n\n```text\nruntime_node\nplugin_topology\nfile_topology\ndoctrine\n```\n\n---\n\n## Current Canonical Source of Truth\n\nPrimary reasoning artifacts:\n\n```text\nruntime_topology_nodes.json\nruntime_topology_edges.json\nruntime_topology_summary.md\nqdrant_documents.jsonl\nruntime_doctrine.md\nevent_taxonomy.md\nnetworking_model.md\npersistence_model.md\n```\n\nRaw Lua remains important, but as a secondary exact-check layer.\n\n---\n\n## Known Current Architecture Conclusions\n\nThe framework is:\n\n```text\nsimulation-oriented\nevent-driven\nmostly server-authoritative\ncross-realm UI/sync heavy\ntimer/scheduler driven\n```\n\nMajor topology hotspots include:\n\n```text\nhealthproblems\ninventory\nvendor\nstorage\nneeds\nbiorezonance\nlightitems\nmining\nragdollinteraction\nnextbots\n```\n\nCurrent risk themes:\n\n```text\nUI desync\nPVP/PVE FPS drops\ndynamic light cost\nentity simulation cost\nnextbot cost\nnetwork sync correctness\nmemory leaks\n```\n\n---\n\n## Next Pipeline Tasks\n\nImmediate next technical tasks:\n\n```text\nembed_qdrant_documents.py\ningest_qdrant.py\nquery_qdrant.py\n```\n\nFuture diagnostics:\n\n```text\ntopology hotspot analysis\ncross-realm propagation analysis\ninventory desync analysis\nnetwork protocol cleanup\nscheduler optimization\nentity simulation lifecycle modeling\n```\n\n---\n\n## Model Roles\n\nLocal Qwen2.5-Coder 14B Q4_K_M:\n\n```text\nautocomplete\nsmall refactors\nmanifest helpers\ndeterministic transformations\n```\n\nChatGPT / Gemini:\n\n```text\narchitecture synthesis\ncross-system reasoning\nscheduler redesign\nnetworking redesign\noptimization strategy\nUI/system design\n```\n\nLLMs are mandatory external reasoning engines, but not source of truth.",
  "metadata": {
    "chunk_index": 1,
    "file": "subsystem_docs/pipeline_state.md",
    "node_type": "doctrine",
    "source_id": "subsystem_docs/pipeline_state.md"
  },
  "node_type": "doctrine",
  "file": "subsystem_docs/pipeline_state.md"
}
```

### Text

```text
nerated retrieval-ready semantic documents:

```text
manifests/semantic/qdrant_documents.jsonl
manifests/semantic/qdrant_documents_summary.md
```

Document types:

```text
runtime_node
plugin_topology
file_topology
doctrine
```

---

## Current Canonical Source of Truth

Primary reasoning artifacts:

```text
runtime_topology_nodes.json
runtime_topology_edges.json
runtime_topology_summary.md
qdrant_documents.jsonl
runtime_doctrine.md
event_taxonomy.md
networking_model.md
persistence_model.md
```

Raw Lua remains important, but as a secondary exact-check layer.

---

## Known Current Architecture Conclusions

The framework is:

```text
simulation-oriented
event-driven
mostly server-authoritative
cross-realm UI/sync heavy
timer/scheduler driven
```

Major topology hotspots include:

```text
healthproblems
inventory
vendor
storage
needs
biorezonance
lightitems
mining
ragdollinteraction
nextbots
```

Current risk themes:

```text
UI desync
PVP/PVE FPS drops
dynamic light cost
entity simulation cost
nextbot cost
network sync correctness
memory leaks
```

---

## Next Pipeline Tasks

Immediate next technical tasks:

```text
embed_qdrant_documents.py
ingest_qdrant.py
query_qdrant.py
```

Future diagnostics:

```text
topology hotspot analysis
cross-realm propagation analysis
inventory desync analysis
network protocol cleanup
scheduler optimization
entity simulation lifecycle modeling
```

---

## Model Roles

Local Qwen2.5-Coder 14B Q4_K_M:

```text
autocomplete
small refactors
manifest helpers
deterministic transformations
```

ChatGPT / Gemini:

```text
architecture synthesis
cross-system reasoning
scheduler redesign
networking redesign
optimization strategy
UI/system design
```

LLMs are mandatory external reasoning engines, but not source of truth.
```

## Result 3

- Score: **-0.0240**
- Rerank score: `0.16499999999999998`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:inventory:+0.05', 'doctrine_required:+0.16', 'file_subsystem:inventory:+0.07']`
- Source ID: `doc:doctrine:d4d21d55f7342475`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/ai_subsystems/inventory.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:d4d21d55f7342475",
  "doc_type": "doctrine",
  "content_hash": "70d4307fa12b8c1c641f085ca4f02035efd51d267a95ca265de45e9a5ef9128a",
  "embedding_dim": 384,
  "text": "t Architecture Assessment\n\nInventory is not merely a storage system.\n\nInventory is a gameplay infrastructure subsystem.\n\nIt acts as the central coordination point for:\n\n```text\nItem Ownership\nEquipment\nVendor Interaction\nStorage Interaction\nLoot Interaction\nCharacter Equipment State\nInventory UI\n```\n\nBecause of this, inventory should be treated as a Tier-1 subsystem during future architecture investigations.",
  "metadata": {
    "chunk_index": 2,
    "file": "docs/ai_subsystems/inventory.md",
    "node_type": "doctrine",
    "source_id": "docs/ai_subsystems/inventory.md"
  },
  "node_type": "doctrine",
  "file": "docs/ai_subsystems/inventory.md"
}
```

### Text

```text
t Architecture Assessment

Inventory is not merely a storage system.

Inventory is a gameplay infrastructure subsystem.

It acts as the central coordination point for:

```text
Item Ownership
Equipment
Vendor Interaction
Storage Interaction
Loot Interaction
Character Equipment State
Inventory UI
```

Because of this, inventory should be treated as a Tier-1 subsystem during future architecture investigations.
```

## Result 4

- Score: **-0.0305**
- Rerank score: `0.14200000000000002`
- Rerank reasons: `['doc_type:file_topology:+0.12', 'node_type:file:+0.10', 'intent_node_type:+0.08', 'network_text_match:+0.10', 'causal:sync:+0.10', 'causal_network_flow:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:file_topology:10c4dffa36c7630c`
- Doc type: `file_topology`
- Subsystem: `None`
- File: `plugins/gadgets/cl_hooks.lua`

### Metadata

```json
{
  "source_id": "doc:file_topology:10c4dffa36c7630c",
  "doc_type": "file_topology",
  "content_hash": "7c7cb7106b78385a6addb03ab9d38f9e1d04ca6e6afc69f10c69c973db79dfa2",
  "embedding_dim": 384,
  "text": "Runtime topology file summary: plugins/gadgets/cl_hooks.lua\nThis source file participates in 26 topology relationships.\nRelationship counts: {'contains_emitter': 1, 'contains_listener': 2, 'contains_network_operation': 9, 'file_receives_network_message': 9, 'runs_in_realm': 3, 'owns_file': 2}\nPlugin/subsystem guess: unknown\nRealm: client\nSelected relationships:\n- contains_emitter: hook_emitter emit CreateUsingInterface @ plugins\\gadgets\\cl_hooks.lua:88\n- contains_listener: hook_listener listen CreateUsingInterface @ plugins\\gadgets\\cl_hooks.lua:3\n- contains_listener: hook_listener listen CreateUsingInterface @ plugins\\gadgets\\cl_hooks.lua:2\n- contains_network_operation: network_operation netstream hook compSendUserCardAccess\n- contains_network_operation: network_operation netstream hook compSyncWorkShift\n- contains_network_operation: network_operation netstream hook doorInterfaceTurnOn\n- contains_network_operation: network_operation netstream hook interfaceTurnOn\n- contains_network_operation: network_operation netstream hook setUpLocksInfo\n- contains_network_operation: network_operation netstream hook setUpLocksView\n- contains_network_operation: network_operation netstream hook setUpPointsUpdate\n- contains_network_operation: network_operation netstream hook setUpReplicastatus\n- contains_network_operation: network_operation netstream hook setUpUserCard\n- file_receives_network_message: network_message compSendUserCardAccess\n- file_receives_network_message: network_message compSyncWorkShift\n- file_receives_network_message: network_message doorInterfaceTurnOn\n- file_receives_network_message: network_message interfaceTurnOn\n- file_receives_network_message: network_message setUpLocksInfo\n- file_receives_network_message: network_message setUpLocksView\n- file_receives_network_message: network_message setUpPointsUpdate\n- file_receives_network_message: network_message setUpReplicastatus\n- file_receives_network_message: network_message setUpUserCard\n- runs_in_realm: realm client\n- runs_in_realm: realm client\n- runs_in_realm: realm client\n- owns_file: plugin gadgets\n- owns_file: plugin gadgets\nUse this document to retrieve architectural context for this file without loading raw Lua by default.",
  "metadata": {
    "degree": 26,
    "file": "plugins/gadgets/cl_hooks.lua",
    "node_type": "file",
    "source_id": "file:plugins/gadgets/cl_hooks.lua"
  },
  "node_type": "file",
  "file": "plugins/gadgets/cl_hooks.lua",
  "degree": 26
}
```

### Text

```text
Runtime topology file summary: plugins/gadgets/cl_hooks.lua
This source file participates in 26 topology relationships.
Relationship counts: {'contains_emitter': 1, 'contains_listener': 2, 'contains_network_operation': 9, 'file_receives_network_message': 9, 'runs_in_realm': 3, 'owns_file': 2}
Plugin/subsystem guess: unknown
Realm: client
Selected relationships:
- contains_emitter: hook_emitter emit CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:88
- contains_listener: hook_listener listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:3
- contains_listener: hook_listener listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:2
- contains_network_operation: network_operation netstream hook compSendUserCardAccess
- contains_network_operation: network_operation netstream hook compSyncWorkShift
- contains_network_operation: network_operation netstream hook doorInterfaceTurnOn
- contains_network_operation: network_operation netstream hook interfaceTurnOn
- contains_network_operation: network_operation netstream hook setUpLocksInfo
- contains_network_operation: network_operation netstream hook setUpLocksView
- contains_network_operation: network_operation netstream hook setUpPointsUpdate
- contains_network_operation: network_operation netstream hook setUpReplicastatus
- contains_network_operation: network_operation netstream hook setUpUserCard
- file_receives_network_message: network_message compSendUserCardAccess
- file_receives_network_message: network_message compSyncWorkShift
- file_receives_network_message: network_message doorInterfaceTurnOn
- file_receives_network_message: network_message interfaceTurnOn
- file_receives_network_message: network_message setUpLocksInfo
- file_receives_network_message: network_message setUpLocksView
- file_receives_network_m...
```

## Result 5

- Score: **-0.0334**
- Rerank score: `0.135`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'doctrine_required:+0.16']`
- Source ID: `doc:doctrine:d5ecf75c78e81b11`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/source_index.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:d5ecf75c78e81b11",
  "doc_type": "doctrine",
  "content_hash": "7d34f8830e1229a4e4ed096eefc198c606caa4771ed79df88f156eda778d3061",
  "embedding_dim": 384,
  "text": "lans\n\nPromote durable findings from investigations into doctrine, subsystem docs, or human context.\n\n## Scripts\n\nImportant script groups:\n\n```text\nscripts/extraction/\nscripts/normalization/\nscripts/graphs/\nscripts/qdrant/\nscripts/semantic/\nscripts/profiling/\nscripts/diagnostics/\n```\n\nQdrant scripts:\n\n```text\nscripts/qdrant/build_qdrant_documents.py\nscripts/qdrant/embed_qdrant_documents.py\nscripts/qdrant/ingest_qdrant.py\nscripts/qdrant/query_qdrant.py\nscripts/qdrant/rerank_results.py\nscripts/qdrant/context_pack.py\nscripts/qdrant/path_reconstruction.py\nscripts/qdrant/path_reconstruction_v2.py\nscripts/qdrant/retrieval_intent.py\n```\n\n## Raw Lua Source\n\nRaw Lua is not the default reasoning layer.\n\nUse raw Lua only when:\n\n- topology is ambiguous\n- exact runtime behavior must be validated\n- source authority is disputed\n- legacy vs active implementation must be confirmed\n- a bug path requires implementation-level proof\n\nRaw Lua should be requested selectively, not dumped wholesale.",
  "metadata": {
    "chunk_index": 1,
    "file": "docs/source_index.md",
    "node_type": "doctrine",
    "source_id": "docs/source_index.md"
  },
  "node_type": "doctrine",
  "file": "docs/source_index.md"
}
```

### Text

```text
lans

Promote durable findings from investigations into doctrine, subsystem docs, or human context.

## Scripts

Important script groups:

```text
scripts/extraction/
scripts/normalization/
scripts/graphs/
scripts/qdrant/
scripts/semantic/
scripts/profiling/
scripts/diagnostics/
```

Qdrant scripts:

```text
scripts/qdrant/build_qdrant_documents.py
scripts/qdrant/embed_qdrant_documents.py
scripts/qdrant/ingest_qdrant.py
scripts/qdrant/query_qdrant.py
scripts/qdrant/rerank_results.py
scripts/qdrant/context_pack.py
scripts/qdrant/path_reconstruction.py
scripts/qdrant/path_reconstruction_v2.py
scripts/qdrant/retrieval_intent.py
```

## Raw Lua Source

Raw Lua is not the default reasoning layer.

Use raw Lua only when:

- topology is ambiguous
- exact runtime behavior must be validated
- source authority is disputed
- legacy vs active implementation must be confirmed
- a bug path requires implementation-level proof

Raw Lua should be requested selectively, not dumped wholesale.
```

## Result 6

- Score: **-0.0339**
- Rerank score: `0.135`
- Rerank reasons: `['doc_type:plugin_topology:+0.14', 'node_type:plugin_summary:+0.16', 'intent_node_type:+0.08', 'network_text_match:+0.10', 'high_priority_subsystem:+0.06']`
- Source ID: `doc:plugin_topology:e97ed7312a8a8b47`
- Doc type: `plugin_topology`
- Subsystem: `None`
- File: `None`

### Metadata

```json
{
  "source_id": "doc:plugin_topology:e97ed7312a8a8b47",
  "doc_type": "plugin_topology",
  "content_hash": "8cb1ccd4d5d6c7fae2947b3cdc4becfd8a516c889cae4777a46615d6dae46b87",
  "embedding_dim": 384,
  "text": "Plugin/subsystem topology summary: healthproblems\nMember node counts by type: {'plugin': 1}\nRelationship counts: {'owns_file': 72, 'registers_listener': 54, 'listens_to_event': 28, 'owns_timer_operation': 19, 'emits_event': 10}\nHot members:\n- plugin healthproblems degree=183\nArchitectural use: retrieve this when analyzing coupling, responsibilities, runtime load, networking, timers, hooks, or refactoring boundaries for healthproblems.",
  "metadata": {
    "node_count": 1,
    "node_type": "plugin_summary",
    "plugin": "healthproblems",
    "source_id": "plugin:healthproblems"
  },
  "node_type": "plugin_summary",
  "plugin": "healthproblems"
}
```

### Text

```text
Plugin/subsystem topology summary: healthproblems
Member node counts by type: {'plugin': 1}
Relationship counts: {'owns_file': 72, 'registers_listener': 54, 'listens_to_event': 28, 'owns_timer_operation': 19, 'emits_event': 10}
Hot members:
- plugin healthproblems degree=183
Architectural use: retrieve this when analyzing coupling, responsibilities, runtime load, networking, timers, hooks, or refactoring boundaries for healthproblems.
```

## Result 7

- Score: **-0.0067**
- Rerank score: `0.1325`
- Rerank reasons: `['doc_type:plugin_topology:+0.14', 'node_type:plugin_summary:+0.16', 'intent_node_type:+0.08', 'text_subsystem:vendor:+0.05', 'network_text_match:+0.10']`
- Source ID: `doc:plugin_topology:6734ebe6a22b5468`
- Doc type: `plugin_topology`
- Subsystem: `None`
- File: `None`

### Metadata

```json
{
  "source_id": "doc:plugin_topology:6734ebe6a22b5468",
  "doc_type": "plugin_topology",
  "content_hash": "95bb70af5942e0dde5124eb877c5ae8e82c7efe06cf7556659e3ab1a0401c341",
  "embedding_dim": 384,
  "text": "Plugin/subsystem topology summary: newvendorsystem\nMember node counts by type: {'plugin': 1}\nRelationship counts: {'owns_file': 3}\nHot members:\n- plugin newvendorsystem degree=3\nArchitectural use: retrieve this when analyzing coupling, responsibilities, runtime load, networking, timers, hooks, or refactoring boundaries for newvendorsystem.",
  "metadata": {
    "node_count": 1,
    "node_type": "plugin_summary",
    "plugin": "newvendorsystem",
    "source_id": "plugin:newvendorsystem"
  },
  "node_type": "plugin_summary",
  "plugin": "newvendorsystem"
}
```

### Text

```text
Plugin/subsystem topology summary: newvendorsystem
Member node counts by type: {'plugin': 1}
Relationship counts: {'owns_file': 3}
Hot members:
- plugin newvendorsystem degree=3
Architectural use: retrieve this when analyzing coupling, responsibilities, runtime load, networking, timers, hooks, or refactoring boundaries for newvendorsystem.
```

## Result 8

- Score: **-0.0279**
- Rerank score: `0.127`
- Rerank reasons: `['doc_type:file_topology:+0.12', 'node_type:file:+0.10', 'intent_node_type:+0.08', 'network_text_match:+0.10', 'causal_network_flow:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:file_topology:870fd673d9af2a22`
- Doc type: `file_topology`
- Subsystem: `None`
- File: `schema/hooks/cl_hooks.lua`

### Metadata

```json
{
  "source_id": "doc:file_topology:870fd673d9af2a22",
  "doc_type": "file_topology",
  "content_hash": "b047c6597baf4d9a9e4950776b064e0cf1655702006edff4ff6a154376cab3aa",
  "embedding_dim": 384,
  "text": "Runtime topology file summary: schema/hooks/cl_hooks.lua\nThis source file participates in 21 topology relationships.\nRelationship counts: {'contains_listener': 7, 'contains_network_operation': 4, 'contains_timer_operation': 1, 'file_receives_network_message': 4, 'runs_in_realm': 3, 'owns_file': 2}\nPlugin/subsystem guess: unknown\nRealm: client\nSelected relationships:\n- contains_listener: hook_listener listen CharacterLoaded @ schema\\hooks\\cl_hooks.lua:121\n- contains_listener: hook_listener listen addDisplay @ schema\\hooks\\cl_hooks.lua:104\n- contains_listener: hook_listener listen HUDPaint @ schema\\hooks\\cl_hooks.lua:15\n- contains_listener: hook_listener listen OnChatReceived @ schema\\hooks\\cl_hooks.lua:113\n- contains_listener: hook_listener listen OnContextMenuClose @ schema\\hooks\\cl_hooks.lua:138\n- contains_listener: hook_listener listen RenderScreenspaceEffects @ schema\\hooks\\cl_hooks.lua:155\n- contains_listener: hook_listener listen OnContextMenuOpen @ schema\\hooks\\cl_hooks.lua:132\n- contains_network_operation: network_operation netstream hook cDisp\n- contains_network_operation: network_operation netstream hook obj\n- contains_network_operation: network_operation netstream hook plyData\n- contains_network_operation: network_operation netstream hook voicePlay\n- contains_timer_operation: timer_operation timer_create@schema\\hooks\\cl_hooks.lua:184\n- file_receives_network_message: network_message cDisp\n- file_receives_network_message: network_message obj\n- file_receives_network_message: network_message plyData\n- file_receives_network_message: network_message voicePlay\n- runs_in_realm: realm client\n- runs_in_realm: realm client\n- runs_in_realm: realm client\n- owns_file: plugin schema\n- owns_file: plugin schema\nUse this document to retrieve architectural context for this file without loading raw Lua by default.",
  "metadata": {
    "degree": 21,
    "file": "schema/hooks/cl_hooks.lua",
    "node_type": "file",
    "source_id": "file:schema/hooks/cl_hooks.lua"
  },
  "node_type": "file",
  "file": "schema/hooks/cl_hooks.lua",
  "degree": 21
}
```

### Text

```text
Runtime topology file summary: schema/hooks/cl_hooks.lua
This source file participates in 21 topology relationships.
Relationship counts: {'contains_listener': 7, 'contains_network_operation': 4, 'contains_timer_operation': 1, 'file_receives_network_message': 4, 'runs_in_realm': 3, 'owns_file': 2}
Plugin/subsystem guess: unknown
Realm: client
Selected relationships:
- contains_listener: hook_listener listen CharacterLoaded @ schema\hooks\cl_hooks.lua:121
- contains_listener: hook_listener listen addDisplay @ schema\hooks\cl_hooks.lua:104
- contains_listener: hook_listener listen HUDPaint @ schema\hooks\cl_hooks.lua:15
- contains_listener: hook_listener listen OnChatReceived @ schema\hooks\cl_hooks.lua:113
- contains_listener: hook_listener listen OnContextMenuClose @ schema\hooks\cl_hooks.lua:138
- contains_listener: hook_listener listen RenderScreenspaceEffects @ schema\hooks\cl_hooks.lua:155
- contains_listener: hook_listener listen OnContextMenuOpen @ schema\hooks\cl_hooks.lua:132
- contains_network_operation: network_operation netstream hook cDisp
- contains_network_operation: network_operation netstream hook obj
- contains_network_operation: network_operation netstream hook plyData
- contains_network_operation: network_operation netstream hook voicePlay
- contains_timer_operation: timer_operation timer_create@schema\hooks\cl_hooks.lua:184
- file_receives_network_message: network_message cDisp
- file_receives_network_message: network_message obj
- file_receives_network_message: network_message plyData
- file_receives_network_message: network_message voicePlay
- runs_in_realm: realm client
- runs_in_realm: realm client
- runs_in_realm: realm client
- owns_file: plugin schema
- owns_file: plugin schema
Use this document to retrieve architectural context for this file...
```

## Result 9

- Score: **-0.0288**
- Rerank score: `0.127`
- Rerank reasons: `['doc_type:file_topology:+0.12', 'node_type:file:+0.10', 'intent_node_type:+0.08', 'network_text_match:+0.10', 'causal_network_flow:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:file_topology:e1156a59d633d83d`
- Doc type: `file_topology`
- Subsystem: `None`
- File: `schema/hooks/sv_hooks.lua`

### Metadata

```json
{
  "source_id": "doc:file_topology:e1156a59d633d83d",
  "doc_type": "file_topology",
  "content_hash": "8f67a45d608ac9634a5a0ce87fbe6929618a18bf3b2ac122979f26995209660d",
  "embedding_dim": 384,
  "text": "Runtime topology file summary: schema/hooks/sv_hooks.lua\nThis source file participates in 34 topology relationships.\nRelationship counts: {'contains_emitter': 3, 'contains_listener': 17, 'contains_network_operation': 5, 'file_receives_network_message': 2, 'file_sends_network_message': 3, 'runs_in_realm': 3, 'owns_file': 1}\nPlugin/subsystem guess: unknown\nRealm: server\nSelected relationships:\n- contains_emitter: hook_emitter emit CanPlayerEditData @ schema\\hooks\\sv_hooks.lua:424\n- contains_emitter: hook_emitter emit CanPlayerEditObjectives @ schema\\hooks\\sv_hooks.lua:433\n- contains_emitter: hook_emitter emit PlayerRankChanged @ schema\\hooks\\sv_hooks.lua:224\n- contains_listener: hook_listener listen PlayerHurt @ schema\\hooks\\sv_hooks.lua:284\n- contains_listener: hook_listener listen PlayerSetHandsModel @ schema\\hooks\\sv_hooks.lua:409\n- contains_listener: hook_listener listen PlayerFootstep @ schema\\hooks\\sv_hooks.lua:13\n- contains_listener: hook_listener listen CanPlayerViewData @ schema\\hooks\\sv_hooks.lua:150\n- contains_listener: hook_listener listen PostPlayerLoadout @ schema\\hooks\\sv_hooks.lua:146\n- contains_listener: hook_listener listen PlayerTick @ schema\\hooks\\sv_hooks.lua:322\n- contains_listener: hook_listener listen PlayerMessageSend @ schema\\hooks\\sv_hooks.lua:341\n- contains_listener: hook_listener listen CanPlayerViewObjectives @ schema\\hooks\\sv_hooks.lua:401\n- contains_listener: hook_listener listen GetPlayerPainSound @ schema\\hooks\\sv_hooks.lua:314\n- contains_listener: hook_listener listen CanPlayerEditObjectives @ schema\\hooks\\sv_hooks.lua:405\n- contains_listener: hook_listener listen LoadData @ schema\\hooks\\sv_hooks.lua:140\n- contains_listener: hook_listener listen PlayerRankChanged @ schema\\hooks\\sv_hooks.lua:186\n- contains_listener: hook_listener listen PlayerUseDoor @ schema\\hooks\\sv_hooks.lua:156\n- contains_listener: hook_listener listen PlayerStaminaLost @ schema\\hooks\\sv_hooks.lua:385\n- contains_listener: hook_listener listen GetPlayerDeathSound @ schema\\hooks\\sv_hooks.lua:240\n- contains_listener: hook_listener listen OnCharVarChanged @ schema\\hooks\\sv_hooks.lua:215\n- contains_listener: hook_listener listen OnCharCreated @ schema\\hooks\\sv_hooks.lua:88\n- contains_network_operation: network_operation netstream hook dataCls\n- contains_network_operation: network_operation netstream hook obj\n- contains_network_operation: network_operation netstream send nil\n- contains_network_operation: network_operation netstream send nil\n- contains_network_operation: network_operation netstream send nil\n- file_receives_network_message: network_message dataCls\n- file_receives_network_message: network_message obj\n- file_sends_network_message: network_message nil\n- file_sends_network_message: network_message nil\n- file_sends_network_message: network_message nil\n- runs_in_realm: realm server\n- runs_in_realm: realm server\n- runs_in_realm: realm server\n- owns_file: plugin schema\nUse this document to retrieve architectural context for this file without loading raw Lua by default.",
  "metadata": {
    "degree": 34,
    "file": "schema/hooks/sv_hooks.lua",
    "node_type": "file",
    "source_id": "file:schema/hooks/sv_hooks.lua"
  },
  "node_type": "file",
  "file": "schema/hooks/sv_hooks.lua",
  "degree": 34
}
```

### Text

```text
Runtime topology file summary: schema/hooks/sv_hooks.lua
This source file participates in 34 topology relationships.
Relationship counts: {'contains_emitter': 3, 'contains_listener': 17, 'contains_network_operation': 5, 'file_receives_network_message': 2, 'file_sends_network_message': 3, 'runs_in_realm': 3, 'owns_file': 1}
Plugin/subsystem guess: unknown
Realm: server
Selected relationships:
- contains_emitter: hook_emitter emit CanPlayerEditData @ schema\hooks\sv_hooks.lua:424
- contains_emitter: hook_emitter emit CanPlayerEditObjectives @ schema\hooks\sv_hooks.lua:433
- contains_emitter: hook_emitter emit PlayerRankChanged @ schema\hooks\sv_hooks.lua:224
- contains_listener: hook_listener listen PlayerHurt @ schema\hooks\sv_hooks.lua:284
- contains_listener: hook_listener listen PlayerSetHandsModel @ schema\hooks\sv_hooks.lua:409
- contains_listener: hook_listener listen PlayerFootstep @ schema\hooks\sv_hooks.lua:13
- contains_listener: hook_listener listen CanPlayerViewData @ schema\hooks\sv_hooks.lua:150
- contains_listener: hook_listener listen PostPlayerLoadout @ schema\hooks\sv_hooks.lua:146
- contains_listener: hook_listener listen PlayerTick @ schema\hooks\sv_hooks.lua:322
- contains_listener: hook_listener listen PlayerMessageSend @ schema\hooks\sv_hooks.lua:341
- contains_listener: hook_listener listen CanPlayerViewObjectives @ schema\hooks\sv_hooks.lua:401
- contains_listener: hook_listener listen GetPlayerPainSound @ schema\hooks\sv_hooks.lua:314
- contains_listener: hook_listener listen CanPlayerEditObjectives @ schema\hooks\sv_hooks.lua:405
- contains_listener: hook_listener listen LoadData @ schema\hooks\sv_hooks.lua:140
- contains_listener: hook_listener listen PlayerRankChanged @ schema\hooks\sv_hooks.lua:186
- contains_listener: hook_listener listen P...
```

## Result 10

- Score: **-0.0283**
- Rerank score: `0.12600000000000003`
- Rerank reasons: `['doc_type:plugin_topology:+0.14', 'node_type:plugin_summary:+0.16', 'intent_node_type:+0.08', 'network_text_match:+0.10', 'realm_signal:+0.04']`
- Source ID: `doc:plugin_topology:8ea779cd9ca10b47`
- Doc type: `plugin_topology`
- Subsystem: `None`
- File: `None`

### Metadata

```json
{
  "source_id": "doc:plugin_topology:8ea779cd9ca10b47",
  "doc_type": "plugin_topology",
  "content_hash": "76ae15f1473637c02a657a35fbaf44d65e58e777b509f7125b4d54307ddba405",
  "embedding_dim": 384,
  "text": "Plugin/subsystem topology summary: observer\nMember node counts by type: {'plugin': 1}\nRelationship counts: {'owns_file': 1, 'owns_timer_operation': 1}\nHot members:\n- plugin observer degree=2\nArchitectural use: retrieve this when analyzing coupling, responsibilities, runtime load, networking, timers, hooks, or refactoring boundaries for observer.",
  "metadata": {
    "node_count": 1,
    "node_type": "plugin_summary",
    "plugin": "observer",
    "source_id": "plugin:observer"
  },
  "node_type": "plugin_summary",
  "plugin": "observer"
}
```

### Text

```text
Plugin/subsystem topology summary: observer
Member node counts by type: {'plugin': 1}
Relationship counts: {'owns_file': 1, 'owns_timer_operation': 1}
Hot members:
- plugin observer degree=2
Architectural use: retrieve this when analyzing coupling, responsibilities, runtime load, networking, timers, hooks, or refactoring boundaries for observer.
```
