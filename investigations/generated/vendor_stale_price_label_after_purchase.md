# SIGNALIS AI — Investigation Report

- Generated: `2026-05-30T19:15:22`
- Query: `vendor stale price label after purchase`
- Intent: `RetrievalIntent(query='vendor stale price label after purchase', domains=set(), subsystems={'inventory', 'vendor'}, events=set(), node_types={'hook_event', 'file', 'plugin_summary', 'hook_listener', 'plugin', 'file_summary', 'hook_emitter'}, wants_timers=False, wants_network=False, wants_doctrine=True, expanded_terms=['file', 'file_summary', 'hook_emitter', 'hook_event', 'hook_listener', 'inventory', 'plugin', 'plugin_summary', 'vendor'])`
- Top K: `12`
- Collection: `signalis_semantic`
- Retrieval result file: `manifests\semantic\qdrant_query_results.md`
- Raw capture: `investigations/generated/vendor_stale_price_label_after_purchase.raw.txt`

## Question

vendor stale price label after purchase

## Retrieval Intent

- Classified intent: `RetrievalIntent(query='vendor stale price label after purchase', domains=set(), subsystems={'inventory', 'vendor'}, events=set(), node_types={'hook_event', 'file', 'plugin_summary', 'hook_listener', 'plugin', 'file_summary', 'hook_emitter'}, wants_timers=False, wants_network=False, wants_doctrine=True, expanded_terms=['file', 'file_summary', 'hook_emitter', 'hook_event', 'hook_listener', 'inventory', 'plugin', 'plugin_summary', 'vendor'])`
- Expanded query: `vendor stale price label after purchase`

## Validation Targets

Targets are selected from retrieved files/hooks/network messages and ranked by query relevance. They are validation candidates, not confirmed causes.

### Priority Files

- `plugins/vendor/derma/cl_vendor.lua`
- `plugins/vendor/cl_networking.lua`
- `plugins/inventory/cl_hooks.lua`
- `gamemode/core/meta/inventory/cl_base_inventory.lua`
- `plugins/vendor/entities/entities/nut_vendor/init.lua`
- `plugins/vendor/entities/entities/nut_vendor/shared.lua`

### Priority Hooks

- `VendorItemPriceUpdated`
- `VendorItemStockUpdated`
- `VendorMoneyUpdated`
- `CanPlayerAccessVendor`
- `CanPlayerTradeWithVendor`
- `CreateNewInventoryPanel`
- `CreateInventoryPanel`

### Priority Network Messages

- `nutVendorTrade`
- `nutVendorExit`
- `nutInventoryData`

## Extracted Signals

These are text-level retrieval signals, not validated truth.

### plugins

- `vendor`
- `inventory`
- `gamemode`
- `gridinv`

### hooks

- `CanItemBeTransfered`
- `CanPlayerAccessVendor`
- `CanPlayerTradeWithVendor`
- `StorageEntityRemoved`
- `StorageRestored`
- `VendorItemPriceUpdated`
- `VendorMoneyUpdated`
- `VendorItemStockUpdated`
- `InventoryItemRemoved`
- `InventoryItemAdded`
- `ItemTransfered`
- `CreateNewInventoryPanel`
- `PlayerLoadout`
- `PostPlayerLoadout`
- `CreateInventoryPanel`

### network_messages

- `nutVendorExit`
- `nutVendorTrade`
- `nutInventoryAdd`
- `nutInventoryData`
- `nutInventoryDelete`
- `nutInventoryInit`
- `nutInventoryRemove`

### files

- `plugins/vendor/derma/cl_vendor.lua`
- `gamemode/core/meta/inventory/cl_base_inventory.lua`
- `plugins/inventory/cl_hooks.lua`
- `plugins/vendor/entities/entities/nut_vendor/init.lua`
- `plugins/vendor/cl_networking.lua`
- `plugins/vendor/entities/entities/nut_vendor/shared.lua`
- `gamemode/core/libs/sh_inventory.lua`
- `plugins/gridinv/plugins/gridinvui/sh_plugin.lua`
- `plugins/_disabled/simpleinv/plugins/listinvui/sh_plugin.lua`

## Retrieval Findings

### Retrieved Headings

- # Qdrant Query Results
- ## Filters
- ## Returned results: 10
- ## Result 1
- ### Metadata
- ### Text
- ## Result 2
- ### Metadata
- ### Text
- ## Result 3
- ### Metadata
- ### Text
- ## Result 4
- ### Metadata
- ### Text
- ## Result 5
- ### Metadata
- ### Text
- ## Result 6
- ### Metadata
- ### Text
- ## Result 7
- ### Metadata
- ### Text
- ## Result 8
- ### Metadata
- ### Text
- ## Result 9
- ### Metadata
- ### Text
- ## Result 10
- ### Metadata
- ### Text

### Retrieval Preview

```text
# Qdrant Query Results

Collection: `signalis_semantic`
Query: `build context pack for vendor stale price label inventory UI bug`
Top K: **10**
Model: `nomic-ai/nomic-embed-text-v1.5`
Device: `cpu`

## Filters

```json
{}
```

## Returned results: 10

## Result 1

- Score: **0.5893**
- Rerank score: `None`
- Rerank bonus: `None`
- Rerank reasons: `[]`
- Source ID: `doc:runtime_node:0157ea5724a0dfe0`
- Doc type: `runtime_node`
- Node type: `plugin`
- Plugin: `vendor`
- Subsystem: `None`
- Realm: `None`
- File: `None`

### Metadata

```json
{
  "source_id": "doc:runtime_node:0157ea5724a0dfe0",
  "doc_type": "runtime_node",
  "content_hash": "f3dca0aa8f22472f15354f5cdc603c22914f736db195215bfce0efd2f09e1d45",
  "embedding_dim": 768,
  "text": "Runtime topology node: vendor\nNode ID: plugin:vendor\nNode type: plugin\nFile: n/a\nRealm: unknown\nPlugin/subsystem: vendor\nOutgoing edge counts: {'emits_event': 22, 'listens_to_event': 18, 'owns_file': 23, 'owns_timer_operation': 11, 'registers_listener': 33}\nIncoming edge counts: {}\nSelected properties: {\"graph_layers\": [\"hook\", \"network\", \"timer\"], \"label\": \"vendor\", \"merge_conflicts\": {\"source_graph\": [\"hook\", \"network\", \"timer\"]}, \"plugin\": \"vendor\", \"source_artifact\": \"derived_from_file_path\", \"source_graph\": \"hook\"}\nSelected neighboring relationships:\n- outgoing emits_event -> hook_event CanItemBeTransfered\n- outgoing emits_event -> hook_event CanPlayerAccessVendor\n- outgoing emits_event -> hook_event CanPlayerTradeWithVendor\n- outgoing emits_event -> hook_event CreateUsingInterface\n- outgoing emits_event -> hook_event OnCharTradeVendor\n- outgoing emits_event -> hook_event OnOpenVendorMenu\n- outgoing emits_event -> hook_event OpenVendorTradeInterface\n- outgoing emits_event -> hook_event StorageEntityRemoved\n- outgoing emits_event -> hook_event StorageInventorySet\n- outgoing emits_event -> hook_event StorageRestored\n- outgoing emits_event -> hook_event VendorClassUpdated\n- outgoing emits_event -> hook_event VendorEdited",
  "metadata": {
    "degree": 107,
    "file": null,
    "in_degree": 0,
    "label": "vendor",
    "node_type": "plugin",
    "out_degree": 107,
    "plugin": "vendor",
    "realm": null,
    "source_id": "plugin:vendor",
    "subsystem": null
  },
  "node_type": "plugin",
  "plugin": "vendor",
  "subsystem": null,
  "realm": null,
  "file": null,
  "degree": 107
}
```

### Text

```text
Runtime topology node: vendor
Node ID: plugin:vendor
Node type: plugin
File: n/a
Realm: unknown
Plugin/subsystem: vendor
Outgoing edge counts: {'emits_event': 22, 'listens_to_event': 18, 'owns_file': 23, 'owns_timer_operation': 11, 'registers_listener': 33}
Incoming edge counts: {}
Selected properties: {"graph_layers": ["hook", "network", "timer"], "label": "vendor", "merge_conflicts": {"source_graph": ["hook", "network", "timer"]}, "plugin": "vendor", "source_artifact": "derived_from_file_path", "source_graph": "hook"}
Selected neighboring relationships:
- outgoing emits_event -> hook_event CanItemBeTransfered
- outgoing emits_event -> hook_event CanPlayerAccessVendor
- outgoing emits_event -> hook_event CanPlayerTradeWithVendor
- outgoing emits_event -> hook_event CreateUsingInterface
- outgoing emits_event -> hook_event OnCharTradeVendor
- outgoing emits_event -> hook_event OnOpenVendorMenu
- outgoing emits_event -> hook_event OpenVendorTradeInterface
- outgoing emits_event -> hook_event StorageEntityRemoved
- outgoing emits_event -> hook_event StorageInventorySet
- outgoing emits_event -> hook_event StorageRestored
- outgoing emits_event -> hook_event VendorClassUpdated
- outgoing emits_event -> hook_event VendorEdited
```

## Result 2

- Score: **0.5874**
- Rerank score: `None`
- Rerank bonus: `None`
- Rerank reasons: `[]`
- Source ID: `doc:file_topology:fd221c850144f0ee`
- Doc type: `file_topology`
- Node type: `file`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `plugins/vendor/derma/cl_vendor.lua`

### Metadata

```json
{
  "source_id": "doc:file_topology:fd221c850144f0ee",
  "doc_type": "file_topology",
  "content_hash": "9198a8c42ea2dbda2cfc33d7829b202fb5c2cae2b4a0c2ec0a1ef48e63b3f323",
  "embedding_dim": 768,
  "text": "Runtime topology file summary: plugins/vendor/derma/cl_vendor.lua\nThis source file participates in 25 topology relationships.\nRelationship counts: {'contains_listener': 7, 'contains_network_context': 3, 'contains_network_operation': 3, 'contains_network_payload_operation': 4, 'file_sends_network_message': 3, 'runs_in_realm': 3, 'owns_file': 2}\nPlugin/subsystem guess: unknown\nRealm: client\nSelected relationships:\n- contains_listener: hook_listener listen OnCharVarChanged @ plugins\\vendor\\derma\\cl_vendor.lua:201\n- contains_listener: hook_listener listen VendorItemModeUpdated @ plugins\\vendor\\derma\\cl_vendor.lua:211\n- contains_listener: hook_listener listen VendorEdited @ plugins\\vendor\\derma\\cl_vendor.lua:214\n- contains_listener: hook_listener listen VendorItemMaxStockUpdated @ plugins\\vendor\\derma\\cl_vendor.lua:208\n- contains_listener: hook_listener listen VendorItemPriceUpdated @ plugins\\vendor\\derma\\cl_vendor.lua:204\n- contains_listener: hook_listener listen VendorMoneyUpdated @ plugins\\vendor\\derma\\cl_vendor.lua:200\n- contains_listener: hook_listener listen VendorItemStockUpdated @ plugins\\vendor\\derma\\cl_vendor.lua:207\n- contains_network_context: network_context Start nutVendorExit\n- contains_network_context: network_context Start nutVendorTrade\n- contains_network_context: network_context Start nutVendorTrade\n- contains_network_operation: network_operation send nutVendorExit\n- contains_network_operation: network_operation send nutVendorTrade\n- contains_network_operation: network_operation send nutVendorTrade\n- contains_network_payload_operation: network_payload_operation write WriteString nutVendorTrade\n- contains_network_payload_operation: network_payload_operation write WriteBool nutVendorTrade\n- contains_network_payload_operation: network_payload_operation write WriteString nutVendorTrade\n- contains_network_payload_operation: network_payload_operation write WriteBool nutVendorTrade\n- file_sends_network_message: network_message nutVendorExit\n- file_sends_network_message: network_message nutVendorTrade\n- file_sends_network_message: network_message nutVendorTrade\n- runs_in_realm: realm client\n- runs_in_realm: realm client\n- runs_in_realm: realm client\n- owns_file: plugin vendor\n- owns_file: plugin vendor\nUse this document to retrieve architectural context for this file without loading raw Lua by default.",
  "metadata": {
    "degree": 25,
    "file": "plugins/vendor/derma/cl_vendor.lua",
    "node_type": "file",
    "source_id": "file:plugins/vendor/derma/cl_vendor.lua"
  },
  "node_type": "file",
  "file": "plugins/vendor/derma/cl_vendor.lua",
  "degree": 25
}
```

## Human / Project Context

### human_context

#### Snippet 1

```text
## Item Data Semantics

## Vendor / Inventory Notes

The vendor system has been reworked. Some files under plugins/vendor are legacy and should not be assumed authoritative without validation.
```

#### Snippet 2

```text
## Vendor / Inventory Notes

The vendor system has been reworked. Some files under plugins/vendor are legacy and should not be assumed authoritative without validation.

Observed bug:
After buying items from a vendor, vendor price labels sometimes remain visible on items inside the player inventory.
```

#### Snippet 3

```text
The vendor system has been reworked. Some files under plugins/vendor are legacy and should not be assumed authoritative without validation.

Observed bug:
After buying items from a vendor, vendor price labels sometimes remain visible on items inside the player inventory.

Observed recovery:
Relog usually fixes the issue.
```

#### Snippet 4

```text
Moving the item through storage can also refresh/clear the incorrect display state.

Human interpretation:
This likely involves client-side item data or UI presentation state becoming stale, not necessarily server inventory ownership corruption.

Important rule:
Vendor price labels are presentation/UI metadata and should not be treated as authoritative item ownership state.
```

#### Snippet 5

```text
This likely involves client-side item data or UI presentation state becoming stale, not necessarily server inventory ownership corruption.

Important rule:
Vendor price labels are presentation/UI metadata and should not be treated as authoritative item ownership state.

## Storage / Inventory Notes
```

### project_memory

#### Snippet 1

```text
- lifecycle ordering
- cross-realm initialization
- network/UI desynchronization
- vendor/inventory presentation metadata
- subsystem coupling
- runtime propagation tracing
- timer/scheduler classification
```

#### Snippet 2

```text
## Important Human Context

The vendor system was reworked.

Some files under:
```

#### Snippet 3

```text
Some files under:

```text
plugins/vendor/*
```

may be legacy and must not automatically be considered authoritative.
```

#### Snippet 4

```text
may be legacy and must not automatically be considered authoritative.

Observed vendor bug:

```text
vendor prices sometimes remain visible after buying items
```

#### Snippet 5

```text
Observed vendor bug:

```text
vendor prices sometimes remain visible after buying items
```

Current human interpretation:
```

### runtime_topology_summary

#### Snippet 1

```text
- `plugins/inventory/cl_hooks.lua`: 63
- `plugins/gadgets/sv_hooks.lua`: 62
- `plugins/needs/sv_hooks.lua`: 61
- `plugins/vendor/cl_networking.lua`: 60
- `plugins/pluginconfig.lua`: 59
- `gamemode/core/hooks/cl_hooks.lua`: 54
- `plugins/recognition.lua`: 54
```

#### Snippet 2

```text
- `plugins/multichar/sh_plugin.lua`: 45
- `plugins/ragdollinteraction/interaction/cl_hooks.lua`: 45
- `plugins/tying/sh_charsearch.lua`: 45
- `plugins/vendor/sv_networking.lua`: 43
- `gamemode/core/meta/inventory/sv_base_inventory.lua`: 43
- `plugins/admintools/sh_plugin.lua`: 42
- `gamemode/core/meta/inventory/cl_base_inventory.lua`: 41
```

#### Snippet 3

```text
- `lightitems`: 120
- `gamemode`: 113
- `needs`: 112
- `vendor`: 107
- `gridinv`: 99
- `biorezonance`: 89
- `entities`: 89
```

## Preliminary Interpretation

- Retrieval evidence has been collected.
- Validation targets identify the smallest likely source fragments to inspect next.
- Exact runtime behavior is not proven by this report.
- Source validation is required before promotion.

## Recommended Validation

Validate in this order:

1. Priority files listed above.
2. Priority hook listeners/emitters listed above.
3. Priority network send/receive sites listed above.
4. Human context for legacy vs authoritative implementation.

For each validation step, capture:

- exact file path
- exact function/hook/network handler
- realm
- whether it mutates authoritative state or only presentation/UI metadata

## Open Questions

- Which retrieved files are authoritative and which are legacy?
- Which hook/network path actually executes at runtime?
- Is the issue state corruption, stale client metadata, or UI presentation desync?
- What exact Lua fragment should be validated next?

## Confidence

`Medium-Low` until exact source validation is performed.

## Promotion Candidates

Only promote after validation:

- `docs/project_memory.md` for durable project state.
- `docs/human_subsystems/*.md` for human-confirmed facts.
- `docs/subsystems/*.md` for topology/source-grounded subsystem facts.
- `docs/ai_subsystems/*.md` for validated architecture synthesis.
