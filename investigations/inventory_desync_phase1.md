# Qdrant Query Results

Collection: `signalis_semantic`
Query: `inventory desync after character load`
Top K: **20**
Model: `nomic-ai/nomic-embed-text-v1.5`
Device: `cpu`

## Filters

```json
{}
```

## Returned results: 20

## Result 1

- Score: **0.7188**
- Rerank score: `1.32882343`
- Rerank bonus: `0.61`
- Rerank reasons: `['doc_type:runtime_node:+0.00', 'node_type:plugin:+0.12', 'intent_node_type:+0.08', 'plugin_match:inventory:+0.16', 'text_subsystem:character:+0.04', 'text_event:postplayerloadout:+0.08', 'network_text_match:+0.08', 'high_priority_subsystem:+0.05']`
- Source ID: `doc:runtime_node:03a413ab22454d13`
- Doc type: `runtime_node`
- Node type: `plugin`
- Plugin: `inventory`
- Subsystem: `None`
- Realm: `None`
- File: `None`

### Metadata

```json
{
  "source_id": "doc:runtime_node:03a413ab22454d13",
  "doc_type": "runtime_node",
  "content_hash": "af22812656bc4431ed18e41903f87bdc65d6267d9f1f166dc56479b5f9a6b0d9",
  "embedding_dim": 768,
  "text": "Runtime topology node: inventory\nNode ID: plugin:inventory\nNode type: plugin\nFile: n/a\nRealm: unknown\nPlugin/subsystem: inventory\nOutgoing edge counts: {'emits_event': 3, 'listens_to_event': 8, 'owns_file': 8, 'owns_timer_operation': 2, 'registers_listener': 16}\nIncoming edge counts: {}\nSelected properties: {\"graph_layers\": [\"hook\", \"network\", \"timer\"], \"label\": \"inventory\", \"merge_conflicts\": {\"source_graph\": [\"hook\", \"network\", \"timer\"]}, \"plugin\": \"inventory\", \"source_artifact\": \"derived_from_file_path\", \"source_graph\": \"hook\"}\nSelected neighboring relationships:\n- outgoing emits_event -> hook_event CheckBothHandsAmputation\n- outgoing emits_event -> hook_event ItemTransfered\n- outgoing emits_event -> hook_event OnCreateStoragePanel\n- outgoing listens_to_event -> hook_event CharacterPreSave\n- outgoing listens_to_event -> hook_event CreateNewInventoryPanel\n- outgoing listens_to_event -> hook_event CreateTargetNewInventoryPanel\n- outgoing listens_to_event -> hook_event ItemTransfered\n- outgoing listens_to_event -> hook_event OpenVendorTradeInterface\n- outgoing listens_to_event -> hook_event PlayerButtonDown\n- outgoing listens_to_event -> hook_event PlayerLoadout\n- outgoing listens_to_event -> hook_event PostPlayerLoadout\n- outgoing owns_file -> file plugins\\inventory\\cl_hooks.lua",
  "metadata": {
    "degree": 37,
    "file": null,
    "in_degree": 0,
    "label": "inventory",
    "node_type": "plugin",
    "out_degree": 37,
    "plugin": "inventory",
    "realm": null,
    "source_id": "plugin:inventory",
    "subsystem": null
  },
  "node_type": "plugin",
  "plugin": "inventory",
  "subsystem": null,
  "realm": null,
  "file": null,
  "degree": 37
}
```

### Text

```text
Runtime topology node: inventory
Node ID: plugin:inventory
Node type: plugin
File: n/a
Realm: unknown
Plugin/subsystem: inventory
Outgoing edge counts: {'emits_event': 3, 'listens_to_event': 8, 'owns_file': 8, 'owns_timer_operation': 2, 'registers_listener': 16}
Incoming edge counts: {}
Selected properties: {"graph_layers": ["hook", "network", "timer"], "label": "inventory", "merge_conflicts": {"source_graph": ["hook", "network", "timer"]}, "plugin": "inventory", "source_artifact": "derived_from_file_path", "source_graph": "hook"}
Selected neighboring relationships:
- outgoing emits_event -> hook_event CheckBothHandsAmputation
- outgoing emits_event -> hook_event ItemTransfered
- outgoing emits_event -> hook_event OnCreateStoragePanel
- outgoing listens_to_event -> hook_event CharacterPreSave
- outgoing listens_to_event -> hook_event CreateNewInventoryPanel
- outgoing listens_to_event -> hook_event CreateTargetNewInventoryPanel
- outgoing listens_to_event -> hook_event ItemTransfered
- outgoing listens_to_event -> hook_event OpenVendorTradeInterface
- outgoing listens_to_event -> hook_event PlayerButtonDown
- outgoing listens_to_event -> hook_event PlayerLoadout
- outgoing listens_to_event -> hook_event PostPlayerLoadout
- outgoing owns_file -> file plugins\inventory\cl_hooks.lua
```

## Result 2

- Score: **0.7190**
- Rerank score: `1.2190094999999999`
- Rerank bonus: `0.5`
- Rerank reasons: `['doc_type:file_topology:+0.12', 'node_type:file:+0.10', 'intent_node_type:+0.08', 'text_subsystem:character:+0.04', 'text_event:postplayerloadout:+0.08', 'network_text_match:+0.08']`
- Source ID: `doc:file_topology:fde2f5c4b1424773`
- Doc type: `file_topology`
- Node type: `file`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `plugins/inventory/sh_plugin.lua`

### Metadata

```json
{
  "source_id": "doc:file_topology:fde2f5c4b1424773",
  "doc_type": "file_topology",
  "content_hash": "901b47f6740c9d3f03730d82d63ce6334a68a4d58741ea2365705c0fade5838f",
  "embedding_dim": 768,
  "text": "Runtime topology file summary: plugins/inventory/sh_plugin.lua\nThis source file participates in 24 topology relationships.\nRelationship counts: {'contains_emitter': 1, 'contains_listener': 8, 'contains_network_operation': 5, 'file_receives_network_message': 3, 'file_registers_network_message': 1, 'file_sends_network_message': 1, 'runs_in_realm': 3, 'owns_file': 2}\nPlugin/subsystem guess: unknown\nRealm: shared\nSelected relationships:\n- contains_emitter: hook_emitter emit ItemTransfered @ plugins\\inventory\\sh_plugin.lua:482\n- contains_listener: hook_listener listen CharacterPreSave @ plugins\\inventory\\sh_plugin.lua:719\n- contains_listener: hook_listener listen CharacterPreSave @ plugins\\inventory\\sh_plugin.lua:718\n- contains_listener: hook_listener listen OpenVendorTradeInterface @ plugins\\inventory\\sh_plugin.lua:245\n- contains_listener: hook_listener listen PostPlayerLoadout @ plugins\\inventory\\sh_plugin.lua:688\n- contains_listener: hook_listener listen OpenVendorTradeInterface @ plugins\\inventory\\sh_plugin.lua:246\n- contains_listener: hook_listener listen PostPlayerLoadout @ plugins\\inventory\\sh_plugin.lua:689\n- contains_listener: hook_listener listen PlayerLoadout @ plugins\\inventory\\sh_plugin.lua:638\n- contains_listener: hook_listener listen PlayerLoadout @ plugins\\inventory\\sh_plugin.lua:637\n- contains_network_operation: network_operation netstream hook invsRuleSet\n- contains_network_operation: network_operation netstream hook itemSplitAdd\n- contains_network_operation: network_operation netstream hook itemSplitDrop\n- contains_network_operation: network_operation register OpenMyInv\n- contains_network_operation: network_operation netstream send vendorTradeInterface\n- file_receives_network_message: network_message invsRuleSet\n- file_receives_network_message: network_message itemSplitAdd\n- file_receives_network_message: network_message itemSplitDrop\n- file_registers_network_message: network_message OpenMyInv\n- file_sends_network_message: network_message vendorTradeInterface\n- runs_in_realm: realm shared\n- runs_in_realm: realm shared\n- runs_in_realm: realm shared\n- owns_file: plugin inventory\n- owns_file: plugin inventory\nUse this document to retrieve architectural context for this file without loading raw Lua by default.",
  "metadata": {
    "degree": 24,
    "file": "plugins/inventory/sh_plugin.lua",
    "node_type": "file",
    "source_id": "file:plugins/inventory/sh_plugin.lua"
  },
  "node_type": "file",
  "file": "plugins/inventory/sh_plugin.lua",
  "degree": 24
}
```

### Text

```text
Runtime topology file summary: plugins/inventory/sh_plugin.lua
This source file participates in 24 topology relationships.
Relationship counts: {'contains_emitter': 1, 'contains_listener': 8, 'contains_network_operation': 5, 'file_receives_network_message': 3, 'file_registers_network_message': 1, 'file_sends_network_message': 1, 'runs_in_realm': 3, 'owns_file': 2}
Plugin/subsystem guess: unknown
Realm: shared
Selected relationships:
- contains_emitter: hook_emitter emit ItemTransfered @ plugins\inventory\sh_plugin.lua:482
- contains_listener: hook_listener listen CharacterPreSave @ plugins\inventory\sh_plugin.lua:719
- contains_listener: hook_listener listen CharacterPreSave @ plugins\inventory\sh_plugin.lua:718
- contains_listener: hook_listener listen OpenVendorTradeInterface @ plugins\inventory\sh_plugin.lua:245
- contains_listener: hook_listener listen PostPlayerLoadout @ plugins\inventory\sh_plugin.lua:688
- contains_listener: hook_listener listen OpenVendorTradeInterface @ plugins\inventory\sh_plugin.lua:246
- contains_listener: hook_listener listen PostPlayerLoadout @ plugins\inventory\sh_plugin.lua:689
- contains_listener: hook_listener listen PlayerLoadout @ plugins\inventory\sh_plugin.lua:638
- contains_listener: hook_listener listen PlayerLoadout @ plugins\inventory\sh_plugin.lua:637
- contains_network_operation: network_operation netstream hook invsRuleSet
- contains_network_operation: network_operation netstream hook itemSplitAdd
- contains_network_operation: network_operation netstream hook itemSplitDrop
- contains_network_operation: network_operation register OpenMyInv
- contains_network_operation: network_operation netstream send vendorTradeInterface
- file_receives_network_message: network_message invsRuleSet
- file_receives_network_message: network_mes...
```

## Result 3

- Score: **0.7152**
- Rerank score: `1.2151562`
- Rerank bonus: `0.5`
- Rerank reasons: `['doc_type:runtime_node:+0.00', 'node_type:network_message:+0.16', 'intent_node_type:+0.08', 'text_subsystem:storage:+0.04', 'network_intent_match:+0.14', 'network_text_match:+0.08']`
- Source ID: `doc:runtime_node:bcbbda50a0f14bd8`
- Doc type: `runtime_node`
- Node type: `network_message`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `None`

### Metadata

```json
{
  "source_id": "doc:runtime_node:bcbbda50a0f14bd8",
  "doc_type": "runtime_node",
  "content_hash": "9534390dfd1a22049e73dd7ae7cbb4e6e440ddbefc30768638b34add11e2e20f",
  "embedding_dim": 768,
  "text": "Runtime topology node: inventorySetPanelStatus\nNode ID: netmsg:netstream:inventorySetPanelStatus\nNode type: network_message\nFile: n/a\nRealm: unknown\nPlugin/subsystem: unknown\nOutgoing edge counts: {}\nIncoming edge counts: {'file_receives_network_message': 1, 'file_sends_network_message': 10, 'receives_network_message': 1, 'sends_network_message': 10}\nSelected properties: {\"graph_layers\": [\"network\"], \"label\": \"inventorySetPanelStatus\", \"props\": {\"protocol\": \"netstream\", \"resolution\": \"literal\"}, \"source_graph\": \"network\", \"topology_role\": \"runtime_signal\"}\nSelected neighboring relationships:\n- incoming file_receives_network_message -> file plugins\\inventory\\sv_hooks.lua\n- incoming file_sends_network_message -> file plugins\\cassetteplayer\\sh_plugin.lua\n- incoming file_sends_network_message -> file plugins\\gridinv\\plugins\\gridstorage\\sh_plugin.lua\n- incoming file_sends_network_message -> file plugins\\inventory\\cl_hooks.lua\n- incoming file_sends_network_message -> file plugins\\inventory\\cl_hooks.lua\n- incoming file_sends_network_message -> file plugins\\inventory\\cl_hooks.lua\n- incoming file_sends_network_message -> file plugins\\inventory\\cl_hooks.lua\n- incoming file_sends_network_message -> file plugins\\inventory\\cl_hooks.lua\n- incoming file_sends_network_message -> file plugins\\ragdollinteraction\\interaction\\cl_hooks.lua\n- incoming file_sends_network_message -> file plugins\\ragdollinteraction\\interaction\\cl_hooks.lua\n- incoming file_sends_network_message -> file plugins\\tying\\sh_charsearch.lua\n- incoming receives_network_message -> network_operation netstream hook inventorySetPanelStatus",
  "metadata": {
    "degree": 22,
    "file": null,
    "in_degree": 22,
    "label": "inventorySetPanelStatus",
    "node_type": "network_message",
    "out_degree": 0,
    "plugin": null,
    "realm": null,
    "source_id": "netmsg:netstream:inventorySetPanelStatus",
    "subsystem": null
  },
  "node_type": "network_message",
  "plugin": null,
  "subsystem": null,
  "realm": null,
  "file": null,
  "degree": 22
}
```

### Text

```text
Runtime topology node: inventorySetPanelStatus
Node ID: netmsg:netstream:inventorySetPanelStatus
Node type: network_message
File: n/a
Realm: unknown
Plugin/subsystem: unknown
Outgoing edge counts: {}
Incoming edge counts: {'file_receives_network_message': 1, 'file_sends_network_message': 10, 'receives_network_message': 1, 'sends_network_message': 10}
Selected properties: {"graph_layers": ["network"], "label": "inventorySetPanelStatus", "props": {"protocol": "netstream", "resolution": "literal"}, "source_graph": "network", "topology_role": "runtime_signal"}
Selected neighboring relationships:
- incoming file_receives_network_message -> file plugins\inventory\sv_hooks.lua
- incoming file_sends_network_message -> file plugins\cassetteplayer\sh_plugin.lua
- incoming file_sends_network_message -> file plugins\gridinv\plugins\gridstorage\sh_plugin.lua
- incoming file_sends_network_message -> file plugins\inventory\cl_hooks.lua
- incoming file_sends_network_message -> file plugins\inventory\cl_hooks.lua
- incoming file_sends_network_message -> file plugins\inventory\cl_hooks.lua
- incoming file_sends_network_message -> file plugins\inventory\cl_hooks.lua
- incoming file_sends_network_message -> file plugins\inventory\cl_hooks.lua
- incoming file_sends_network_message -> file plugins\ragdollinteraction\interaction\cl_hooks.lua
- incoming file_sends_network_message -> file plugins\ragdollinteraction\interaction\cl_hooks.lua
- incoming file_sends_network_message -> file plugins\tying\sh_charsearch.lua
- incoming receives_network_message -> network_operation netstream hook inventorySetPanelStatus
```

## Result 4

- Score: **0.7113**
- Rerank score: `1.21127975`
- Rerank bonus: `0.5`
- Rerank reasons: `['doc_type:file_topology:+0.12', 'node_type:file:+0.10', 'intent_node_type:+0.08', 'text_subsystem:character:+0.04', 'text_event:characterloaded:+0.08', 'network_text_match:+0.08']`
- Source ID: `doc:file_topology:69116e07b09dbc5c`
- Doc type: `file_topology`
- Node type: `file`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `gamemode/core/meta/sh_character.lua`

### Metadata

```json
{
  "source_id": "doc:file_topology:69116e07b09dbc5c",
  "doc_type": "file_topology",
  "content_hash": "08cb09b01cdefa7968287839f05148811c8b56326939e1a3ab73eb1b5101e23d",
  "embedding_dim": 768,
  "text": "Runtime topology file summary: gamemode/core/meta/sh_character.lua\nThis source file participates in 22 topology relationships.\nRelationship counts: {'contains_emitter': 6, 'contains_network_operation': 6, 'file_sends_network_message': 6, 'runs_in_realm': 3, 'owns_file': 1}\nPlugin/subsystem guess: unknown\nRealm: shared\nSelected relationships:\n- contains_emitter: hook_emitter emit OnCharVarChanged @ gamemode\\core\\meta\\sh_character.lua:255\n- contains_emitter: hook_emitter emit CharacterPreSave @ gamemode\\core\\meta\\sh_character.lua:42\n- contains_emitter: hook_emitter emit CharacterLoaded @ gamemode\\core\\meta\\sh_character.lua:129\n- contains_emitter: hook_emitter emit OnCharVarChanged @ gamemode\\core\\meta\\sh_character.lua:246\n- contains_emitter: hook_emitter emit OnCharPermakilled @ gamemode\\core\\meta\\sh_character.lua:169\n- contains_emitter: hook_emitter emit CharacterPostSave @ gamemode\\core\\meta\\sh_character.lua:51\n- contains_network_operation: network_operation netstream send charKick\n- contains_network_operation: network_operation netstream send nil\n- contains_network_operation: network_operation netstream send nil\n- contains_network_operation: network_operation netstream send receiver\n- contains_network_operation: network_operation netstream send self.player\n- contains_network_operation: network_operation netstream send self.player\n- file_sends_network_message: network_message charKick\n- file_sends_network_message: network_message nil\n- file_sends_network_message: network_message nil\n- file_sends_network_message: network_message receiver\n- file_sends_network_message: network_message self.player\n- file_sends_network_message: network_message self.player\n- runs_in_realm: realm shared\n- runs_in_realm: realm shared\n- runs_in_realm: realm shared\n- owns_file: plugin gamemode\nUse this document to retrieve architectural context for this file without loading raw Lua by default.",
  "metadata": {
    "degree": 22,
    "file": "gamemode/core/meta/sh_character.lua",
    "node_type": "file",
    "source_id": "file:gamemode/core/meta/sh_character.lua"
  },
  "node_type": "file",
  "file": "gamemode/core/meta/sh_character.lua",
  "degree": 22
}
```

### Text

```text
Runtime topology file summary: gamemode/core/meta/sh_character.lua
This source file participates in 22 topology relationships.
Relationship counts: {'contains_emitter': 6, 'contains_network_operation': 6, 'file_sends_network_message': 6, 'runs_in_realm': 3, 'owns_file': 1}
Plugin/subsystem guess: unknown
Realm: shared
Selected relationships:
- contains_emitter: hook_emitter emit OnCharVarChanged @ gamemode\core\meta\sh_character.lua:255
- contains_emitter: hook_emitter emit CharacterPreSave @ gamemode\core\meta\sh_character.lua:42
- contains_emitter: hook_emitter emit CharacterLoaded @ gamemode\core\meta\sh_character.lua:129
- contains_emitter: hook_emitter emit OnCharVarChanged @ gamemode\core\meta\sh_character.lua:246
- contains_emitter: hook_emitter emit OnCharPermakilled @ gamemode\core\meta\sh_character.lua:169
- contains_emitter: hook_emitter emit CharacterPostSave @ gamemode\core\meta\sh_character.lua:51
- contains_network_operation: network_operation netstream send charKick
- contains_network_operation: network_operation netstream send nil
- contains_network_operation: network_operation netstream send nil
- contains_network_operation: network_operation netstream send receiver
- contains_network_operation: network_operation netstream send self.player
- contains_network_operation: network_operation netstream send self.player
- file_sends_network_message: network_message charKick
- file_sends_network_message: network_message nil
- file_sends_network_message: network_message nil
- file_sends_network_message: network_message receiver
- file_sends_network_message: network_message self.player
- file_sends_network_message: network_message self.player
- runs_in_realm: realm shared
- runs_in_realm: realm shared
- runs_in_realm: realm shared
- owns_file: plugin gamemode
Us...
```

## Result 5

- Score: **0.7060**
- Rerank score: `1.1859637`
- Rerank bonus: `0.48000000000000004`
- Rerank reasons: `['doc_type:runtime_node:+0.00', 'node_type:network_operation:+0.14', 'intent_node_type:+0.08', 'text_subsystem:inventory:+0.04', 'network_intent_match:+0.14', 'network_text_match:+0.08']`
- Source ID: `doc:runtime_node:2f1298bea2e45950`
- Doc type: `runtime_node`
- Node type: `network_operation`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `None`

### Metadata

```json
{
  "source_id": "doc:runtime_node:2f1298bea2e45950",
  "doc_type": "runtime_node",
  "content_hash": "023b11528d3cce99ff82d0154afa4b8ebe0b2001d1fd83da8923eea97e116daf",
  "embedding_dim": 768,
  "text": "Runtime topology node: netstream hook inventorySetPanelStatus\nNode ID: netop:hook:netstream:inventorySetPanelStatus:plugins/inventory/sv_hooks.lua:118:83\nNode type: network_operation\nFile: n/a\nRealm: unknown\nPlugin/subsystem: unknown\nOutgoing edge counts: {'receives_network_message': 1}\nIncoming edge counts: {'contains_network_operation': 1, 'network_dispatches_to': 10}\nSelected properties: {\"graph_layers\": [\"network\"], \"label\": \"netstream hook inventorySetPanelStatus\", \"props\": {\"file\": \"plugins\\\\inventory\\\\sv_hooks.lua\", \"line\": 118, \"message\": \"inventorySetPanelStatus\", \"operation\": \"receive\", \"protocol\": \"netstream\", \"realm\": \"server\"}, \"source_graph\": \"network\"}\nSelected neighboring relationships:\n- outgoing receives_network_message -> network_message inventorySetPanelStatus\n- incoming contains_network_operation -> file plugins\\inventory\\sv_hooks.lua\n- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus\n- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus\n- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus\n- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus\n- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus\n- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus\n- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus\n- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus\n- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus\n- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus",
  "metadata": {
    "degree": 12,
    "file": null,
    "in_degree": 11,
    "label": "netstream hook inventorySetPanelStatus",
    "node_type": "network_operation",
    "out_degree": 1,
    "plugin": null,
    "realm": null,
    "source_id": "netop:hook:netstream:inventorySetPanelStatus:plugins/inventory/sv_hooks.lua:118:83",
    "subsystem": null
  },
  "node_type": "network_operation",
  "plugin": null,
  "subsystem": null,
  "realm": null,
  "file": null,
  "degree": 12
}
```

### Text

```text
Runtime topology node: netstream hook inventorySetPanelStatus
Node ID: netop:hook:netstream:inventorySetPanelStatus:plugins/inventory/sv_hooks.lua:118:83
Node type: network_operation
File: n/a
Realm: unknown
Plugin/subsystem: unknown
Outgoing edge counts: {'receives_network_message': 1}
Incoming edge counts: {'contains_network_operation': 1, 'network_dispatches_to': 10}
Selected properties: {"graph_layers": ["network"], "label": "netstream hook inventorySetPanelStatus", "props": {"file": "plugins\\inventory\\sv_hooks.lua", "line": 118, "message": "inventorySetPanelStatus", "operation": "receive", "protocol": "netstream", "realm": "server"}, "source_graph": "network"}
Selected neighboring relationships:
- outgoing receives_network_message -> network_message inventorySetPanelStatus
- incoming contains_network_operation -> file plugins\inventory\sv_hooks.lua
- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus
- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus
- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus
- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus
- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus
- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus
- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus
- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus
- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus
- incoming network_dispatches_to -> network_operation netstream send inventorySetPanelStatus
```

## Result 6

- Score: **0.7036**
- Rerank score: `1.123609`
- Rerank bonus: `0.42000000000000004`
- Rerank reasons: `['doc_type:runtime_node:+0.00', 'node_type:hook_event:+0.14', 'intent_node_type:+0.08', 'text_subsystem:multichar:+0.04', 'text_event:playerloadedchar:+0.08', 'network_text_match:+0.08']`
- Source ID: `doc:runtime_node:b8c15d9d8aabef66`
- Doc type: `runtime_node`
- Node type: `hook_event`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `None`

### Metadata

```json
{
  "source_id": "doc:runtime_node:b8c15d9d8aabef66",
  "doc_type": "runtime_node",
  "content_hash": "2397cf1cb9209ec73aec5c6134fc0021a63d8894b401038c562433897042676f",
  "embedding_dim": 768,
  "text": "Runtime topology node: PlayerLoadedChar\nNode ID: hook:PlayerLoadedChar\nNode type: hook_event\nFile: n/a\nRealm: unknown\nPlugin/subsystem: unknown\nOutgoing edge counts: {'classified_as': 1}\nIncoming edge counts: {'emits': 1, 'emits_event': 1, 'listens_to': 13, 'listens_to_event': 7}\nSelected properties: {\"emitter_count\": 1, \"event\": \"PlayerLoadedChar\", \"event_class\": \"framework_lifecycle\", \"graph_layers\": [\"hook\"], \"has_emitters\": true, \"has_listeners\": true, \"label\": \"PlayerLoadedChar\", \"listener_count\": 13, \"realms_emitted\": [\"server\"], \"realms_listened\": [\"server\", \"shared\"], \"return_policy\": \"maybe_returns\", \"source\": \"hook_event_graph\", \"source_artifact\": \"hook_event_listeners\", \"source_graph\": \"hook\", \"topology_role\": \"runtime_signal\"}\nSelected neighboring relationships:\n- outgoing classified_as -> event_class framework_lifecycle\n- incoming emits -> hook_emitter emit PlayerLoadedChar @ plugins\\multichar\\sv_networking.lua:37\n- incoming emits_event -> plugin multichar\n- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\\multichar\\sv_hooks.lua:49\n- incoming listens_to -> hook_listener listen PlayerLoadedChar @ gamemode\\core\\hooks\\sv_hooks.lua:186\n- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\\loyal_system\\sh_plugin.lua:53\n- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\\traits\\sh_plugin.lua:486\n- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\\area\\sh_plugin.lua:94\n- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\\spawnsaver.lua:18\n- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\\ammosave.lua:63\n- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\\spawnsaver.lua:18\n- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\\ammosave.lua:63\n- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\\traits\\sh_plugin.lua:485",
  "metadata": {
    "degree": 23,
    "file": null,
    "in_degree": 22,
    "label": "PlayerLoadedChar",
    "node_type": "hook_event",
    "out_degree": 1,
    "plugin": null,
    "realm": null,
    "source_id": "hook:PlayerLoadedChar",
    "subsystem": null
  },
  "node_type": "hook_event",
  "plugin": null,
  "subsystem": null,
  "realm": null,
  "file": null,
  "degree": 23
}
```

### Text

```text
Runtime topology node: PlayerLoadedChar
Node ID: hook:PlayerLoadedChar
Node type: hook_event
File: n/a
Realm: unknown
Plugin/subsystem: unknown
Outgoing edge counts: {'classified_as': 1}
Incoming edge counts: {'emits': 1, 'emits_event': 1, 'listens_to': 13, 'listens_to_event': 7}
Selected properties: {"emitter_count": 1, "event": "PlayerLoadedChar", "event_class": "framework_lifecycle", "graph_layers": ["hook"], "has_emitters": true, "has_listeners": true, "label": "PlayerLoadedChar", "listener_count": 13, "realms_emitted": ["server"], "realms_listened": ["server", "shared"], "return_policy": "maybe_returns", "source": "hook_event_graph", "source_artifact": "hook_event_listeners", "source_graph": "hook", "topology_role": "runtime_signal"}
Selected neighboring relationships:
- outgoing classified_as -> event_class framework_lifecycle
- incoming emits -> hook_emitter emit PlayerLoadedChar @ plugins\multichar\sv_networking.lua:37
- incoming emits_event -> plugin multichar
- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\multichar\sv_hooks.lua:49
- incoming listens_to -> hook_listener listen PlayerLoadedChar @ gamemode\core\hooks\sv_hooks.lua:186
- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\loyal_system\sh_plugin.lua:53
- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\traits\sh_plugin.lua:486
- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\area\sh_plugin.lua:94
- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\spawnsaver.lua:18
- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\ammosave.lua:63
- incoming listens_to -> hook_listener listen PlayerLoadedChar @ plugins\spawnsaver.lua:18
- incoming listens_to -> hook_listener listen Pl...
```

## Result 7

- Score: **0.7002**
- Rerank score: `1.1202069`
- Rerank bonus: `0.42`
- Rerank reasons: `['doc_type:file_topology:+0.12', 'node_type:file:+0.10', 'intent_node_type:+0.08', 'text_subsystem:inventory:+0.04', 'network_text_match:+0.08']`
- Source ID: `doc:file_topology:112aeba4e7693464`
- Doc type: `file_topology`
- Node type: `file`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`

### Metadata

```json
{
  "source_id": "doc:file_topology:112aeba4e7693464",
  "doc_type": "file_topology",
  "content_hash": "2fb60013ebbbd9fbc788a4644b8f252befb8d280f92ad472b9e52906226a907a",
  "embedding_dim": 768,
  "text": "Runtime topology file summary: gamemode/core/meta/inventory/sv_base_inventory.lua\nThis source file participates in 43 topology relationships.\nRelationship counts: {'contains_network_context': 5, 'contains_network_operation': 10, 'contains_network_payload_operation': 16, 'file_registers_network_message': 5, 'file_sends_network_message': 5, 'runs_in_realm': 1, 'owns_file': 1}\nPlugin/subsystem guess: unknown\nRealm: unknown\nSelected relationships:\n- contains_network_context: network_context Start nutInventoryAdd\n- contains_network_context: network_context Start nutInventoryData\n- contains_network_context: network_context Start nutInventoryDelete\n- contains_network_context: network_context Start nutInventoryInit\n- contains_network_context: network_context Start nutInventoryRemove\n- contains_network_operation: network_operation register nutInventoryAdd\n- contains_network_operation: network_operation register nutInventoryData\n- contains_network_operation: network_operation register nutInventoryDelete\n- contains_network_operation: network_operation register nutInventoryInit\n- contains_network_operation: network_operation register nutInventoryRemove\n- contains_network_operation: network_operation send nutInventoryAdd\n- contains_network_operation: network_operation send nutInventoryData\n- contains_network_operation: network_operation send nutInventoryDelete\n- contains_network_operation: network_operation send nutInventoryInit\n- contains_network_operation: network_operation send nutInventoryRemove\n- contains_network_payload_operation: network_payload_operation write WriteUInt nutInventoryAdd\n- contains_network_payload_operation: network_payload_operation write WriteType nutInventoryAdd\n- contains_network_payload_operation: network_payload_operation write WriteType nutInventoryData\n- contains_network_payload_operation: network_payload_operation write WriteString nutInventoryData\n- contains_network_payload_operation: network_payload_operation write WriteType nutInventoryData\n- contains_network_payload_operation: network_payload_operation write WriteType nutInventoryDelete\n- contains_network_payload_operation: network_payload_operation write WriteType nutInventoryInit\n- contains_network_payload_operation: network_payload_operation write WriteString nutInventoryInit\n- contains_network_payload_operation: network_payload_operation write WriteTable nutInventoryInit\n- contains_network_payload_operation: network_payload_operation write WriteUInt nutInventoryInit\n- contains_network_payload_operation: network_payload_operation write WriteUInt nutInventoryInit\n- contains_network_payload_operation: network_payload_operation write WriteString nutInventoryInit\n- contains_network_payload_operation: network_payload_operation write WriteTable nutInventoryInit\n- contains_network_payload_operation: network_payload_operation write WriteUInt nutInventoryInit\n- contains_network_payload_operation: network_payload_operation write WriteUInt nutInventoryRemove\n- contains_network_payload_operation: network_payload_operation write WriteType nutInventoryRemove\n- file_registers_network_message: network_message nutInventoryAdd\n- file_registers_network_message: network_message nutInventoryData\n- file_registers_network_message: network_message nutInventoryDelete\n- file_registers_network_message: network_message nutInventoryInit\nUse this document to retrieve architectural context for this file without loading raw Lua by default.",
  "metadata": {
    "degree": 43,
    "file": "gamemode/core/meta/inventory/sv_base_inventory.lua",
    "node_type": "file",
    "source_id": "file:gamemode/core/meta/inventory/sv_base_inventory.lua"
  },
  "node_type": "file",
  "file": "gamemode/core/meta/inventory/sv_base_inventory.lua",
  "degree": 43
}
```

### Text

```text
Runtime topology file summary: gamemode/core/meta/inventory/sv_base_inventory.lua
This source file participates in 43 topology relationships.
Relationship counts: {'contains_network_context': 5, 'contains_network_operation': 10, 'contains_network_payload_operation': 16, 'file_registers_network_message': 5, 'file_sends_network_message': 5, 'runs_in_realm': 1, 'owns_file': 1}
Plugin/subsystem guess: unknown
Realm: unknown
Selected relationships:
- contains_network_context: network_context Start nutInventoryAdd
- contains_network_context: network_context Start nutInventoryData
- contains_network_context: network_context Start nutInventoryDelete
- contains_network_context: network_context Start nutInventoryInit
- contains_network_context: network_context Start nutInventoryRemove
- contains_network_operation: network_operation register nutInventoryAdd
- contains_network_operation: network_operation register nutInventoryData
- contains_network_operation: network_operation register nutInventoryDelete
- contains_network_operation: network_operation register nutInventoryInit
- contains_network_operation: network_operation register nutInventoryRemove
- contains_network_operation: network_operation send nutInventoryAdd
- contains_network_operation: network_operation send nutInventoryData
- contains_network_operation: network_operation send nutInventoryDelete
- contains_network_operation: network_operation send nutInventoryInit
- contains_network_operation: network_operation send nutInventoryRemove
- contains_network_payload_operation: network_payload_operation write WriteUInt nutInventoryAdd
- contains_network_payload_operation: network_payload_operation write WriteType nutInventoryAdd
- contains_network_payload_operation: network_payload_operation write WriteType nutInventoryData...
```

## Result 8

- Score: **0.7002**
- Rerank score: `1.1201978`
- Rerank bonus: `0.42`
- Rerank reasons: `['doc_type:file_topology:+0.12', 'node_type:file:+0.10', 'intent_node_type:+0.08', 'text_subsystem:inventory:+0.04', 'network_text_match:+0.08']`
- Source ID: `doc:file_topology:051e1366e8be6265`
- Doc type: `file_topology`
- Node type: `file`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`

### Metadata

```json
{
  "source_id": "doc:file_topology:051e1366e8be6265",
  "doc_type": "file_topology",
  "content_hash": "a1b23cfa06ee26a68583b47b3058b5d8d06284be38196ad80dc2721768b34fc5",
  "embedding_dim": 768,
  "text": "Runtime topology file summary: gamemode/core/meta/inventory/cl_base_inventory.lua\nThis source file participates in 41 topology relationships.\nRelationship counts: {'contains_emitter': 6, 'contains_network_context': 5, 'contains_network_operation': 5, 'contains_network_payload_operation': 16, 'file_receives_network_message': 5, 'runs_in_realm': 3, 'owns_file': 1}\nPlugin/subsystem guess: unknown\nRealm: client\nSelected relationships:\n- contains_emitter: hook_emitter emit ItemInitialized @ gamemode\\core\\meta\\inventory\\cl_base_inventory.lua:41\n- contains_emitter: hook_emitter emit InventoryDeleted @ gamemode\\core\\meta\\inventory\\cl_base_inventory.lua:83\n- contains_emitter: hook_emitter emit InventoryItemRemoved @ gamemode\\core\\meta\\inventory\\cl_base_inventory.lua:75\n- contains_emitter: hook_emitter emit InventoryDataChanged @ gamemode\\core\\meta\\inventory\\cl_base_inventory.lua:17\n- contains_emitter: hook_emitter emit InventoryItemAdded @ gamemode\\core\\meta\\inventory\\cl_base_inventory.lua:63\n- contains_emitter: hook_emitter emit InventoryInitialized @ gamemode\\core\\meta\\inventory\\cl_base_inventory.lua:45\n- contains_network_context: network_context Receive nutInventoryAdd\n- contains_network_context: network_context Receive nutInventoryData\n- contains_network_context: network_context Receive nutInventoryDelete\n- contains_network_context: network_context Receive nutInventoryInit\n- contains_network_context: network_context Receive nutInventoryRemove\n- contains_network_operation: network_operation receive nutInventoryAdd\n- contains_network_operation: network_operation receive nutInventoryData\n- contains_network_operation: network_operation receive nutInventoryDelete\n- contains_network_operation: network_operation receive nutInventoryInit\n- contains_network_operation: network_operation receive nutInventoryRemove\n- contains_network_payload_operation: network_payload_operation read ReadUInt nutInventoryAdd\n- contains_network_payload_operation: network_payload_operation read ReadType nutInventoryAdd\n- contains_network_payload_operation: network_payload_operation read ReadType nutInventoryData\n- contains_network_payload_operation: network_payload_operation read ReadString nutInventoryData\n- contains_network_payload_operation: network_payload_operation read ReadType nutInventoryData\n- contains_network_payload_operation: network_payload_operation read ReadType nutInventoryDelete\n- contains_network_payload_operation: network_payload_operation read ReadType nutInventoryInit\n- contains_network_payload_operation: network_payload_operation read ReadString nutInventoryInit\n- contains_network_payload_operation: network_payload_operation read ReadTable nutInventoryInit\n- contains_network_payload_operation: network_payload_operation read ReadUInt nutInventoryInit\n- contains_network_payload_operation: network_payload_operation read ReadUInt nutInventoryInit\n- contains_network_payload_operation: network_payload_operation read ReadString nutInventoryInit\n- contains_network_payload_operation: network_payload_operation read ReadTable nutInventoryInit\n- contains_network_payload_operation: network_payload_operation read ReadUInt nutInventoryInit\n- contains_network_payload_operation: network_payload_operation read ReadUInt nutInventoryRemove\n- contains_network_payload_operation: network_payload_operation read ReadType nutInventoryRemove\n- file_receives_network_message: network_message nutInventoryAdd\n- file_receives_network_message: network_message nutInventoryData\n- file_receives_network_message: network_message nutInventoryDelete\nUse this document to retrieve architectural context for this file without loading raw Lua by default.",
  "metadata": {
    "degree": 41,
    "file": "gamemode/core/meta/inventory/cl_base_inventory.lua",
    "node_type": "file",
    "source_id": "file:gamemode/core/meta/inventory/cl_base_inventory.lua"
  },
  "node_type": "file",
  "file": "gamemode/core/meta/inventory/cl_base_inventory.lua",
  "degree": 41
}
```

### Text

```text
Runtime topology file summary: gamemode/core/meta/inventory/cl_base_inventory.lua
This source file participates in 41 topology relationships.
Relationship counts: {'contains_emitter': 6, 'contains_network_context': 5, 'contains_network_operation': 5, 'contains_network_payload_operation': 16, 'file_receives_network_message': 5, 'runs_in_realm': 3, 'owns_file': 1}
Plugin/subsystem guess: unknown
Realm: client
Selected relationships:
- contains_emitter: hook_emitter emit ItemInitialized @ gamemode\core\meta\inventory\cl_base_inventory.lua:41
- contains_emitter: hook_emitter emit InventoryDeleted @ gamemode\core\meta\inventory\cl_base_inventory.lua:83
- contains_emitter: hook_emitter emit InventoryItemRemoved @ gamemode\core\meta\inventory\cl_base_inventory.lua:75
- contains_emitter: hook_emitter emit InventoryDataChanged @ gamemode\core\meta\inventory\cl_base_inventory.lua:17
- contains_emitter: hook_emitter emit InventoryItemAdded @ gamemode\core\meta\inventory\cl_base_inventory.lua:63
- contains_emitter: hook_emitter emit InventoryInitialized @ gamemode\core\meta\inventory\cl_base_inventory.lua:45
- contains_network_context: network_context Receive nutInventoryAdd
- contains_network_context: network_context Receive nutInventoryData
- contains_network_context: network_context Receive nutInventoryDelete
- contains_network_context: network_context Receive nutInventoryInit
- contains_network_context: network_context Receive nutInventoryRemove
- contains_network_operation: network_operation receive nutInventoryAdd
- contains_network_operation: network_operation receive nutInventoryData
- contains_network_operation: network_operation receive nutInventoryDelete
- contains_network_operation: network_operation receive nutInventoryInit
- contains_network_operation: network_operati...
```

## Result 9

- Score: **0.6983**
- Rerank score: `1.11828093`
- Rerank bonus: `0.42`
- Rerank reasons: `['doc_type:file_topology:+0.12', 'node_type:file:+0.10', 'intent_node_type:+0.08', 'text_subsystem:storage:+0.04', 'network_text_match:+0.08']`
- Source ID: `doc:file_topology:219854073d8d8476`
- Doc type: `file_topology`
- Node type: `file`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `plugins/inventory/cl_hooks.lua`

### Metadata

```json
{
  "source_id": "doc:file_topology:219854073d8d8476",
  "doc_type": "file_topology",
  "content_hash": "5abb27667cc4e769dc99bb14a66a80ee141f3d92f71801299b20c3bce665ebf7",
  "embedding_dim": 768,
  "text": "Runtime topology file summary: plugins/inventory/cl_hooks.lua\nThis source file participates in 63 topology relationships.\nRelationship counts: {'contains_emitter': 1, 'contains_listener': 4, 'contains_network_context': 1, 'contains_network_operation': 26, 'file_receives_network_message': 15, 'file_sends_network_message': 11, 'runs_in_realm': 3, 'owns_file': 2}\nPlugin/subsystem guess: unknown\nRealm: client\nSelected relationships:\n- contains_emitter: hook_emitter emit OnCreateStoragePanel @ plugins\\inventory\\cl_hooks.lua:166\n- contains_listener: hook_listener listen CreateNewInventoryPanel @ plugins\\inventory\\cl_hooks.lua:91\n- contains_listener: hook_listener listen CreateTargetNewInventoryPanel @ plugins\\inventory\\cl_hooks.lua:94\n- contains_listener: hook_listener listen CreateNewInventoryPanel @ plugins\\inventory\\cl_hooks.lua:90\n- contains_listener: hook_listener listen CreateTargetNewInventoryPanel @ plugins\\inventory\\cl_hooks.lua:95\n- contains_network_context: network_context Receive OpenMyInv\n- contains_network_operation: network_operation netstream hook foodPartAddClient\n- contains_network_operation: network_operation netstream hook foodPartUseClient\n- contains_network_operation: network_operation netstream hook foodReadyPartAddClient\n- contains_network_operation: network_operation netstream hook inventoryCloseOnAction\n- contains_network_operation: network_operation netstream hook inventoryOpen\n- contains_network_operation: network_operation netstream hook inventoryTargetUpdBg\n- contains_network_operation: network_operation netstream hook inventoryTargetUpdSkin\n- contains_network_operation: network_operation netstream hook inventoryUpdBg\n- contains_network_operation: network_operation netstream hook inventoryUpdSkin\n- contains_network_operation: network_operation netstream hook itemSplitDrop\n- contains_network_operation: network_operation netstream hook itemSplitTake\n- contains_network_operation: network_operation netstream hook kettlePartAddClient\n- contains_network_operation: network_operation netstream hook setUpTargetMoney\n- contains_network_operation: network_operation netstream hook vendorTradeInterface\n- contains_network_operation: network_operation receive OpenMyInv\n- contains_network_operation: network_operation netstream send hookName\n- contains_network_operation: network_operation netstream send hookName\n- contains_network_operation: network_operation netstream send inventorySetPanelStatus\n- contains_network_operation: network_operation netstream send inventorySetPanelStatus\n- contains_network_operation: network_operation netstream send inventorySetPanelStatus\n- contains_network_operation: network_operation netstream send inventorySetPanelStatus\n- contains_network_operation: network_operation netstream send inventorySetPanelStatus\n- contains_network_operation: network_operation netstream send invsRuleSet\n- contains_network_operation: network_operation netstream send itemSplitAdd\n- contains_network_operation: network_operation netstream send itemSplitAdd\n- contains_network_operation: network_operation netstream send removeReceiverFromVendor\n- file_receives_network_message: network_message OpenMyInv\n- file_receives_network_message: network_message foodPartAddClient\n- file_receives_network_message: network_message foodPartUseClient\nUse this document to retrieve architectural context for this file without loading raw Lua by default.",
  "metadata": {
    "degree": 63,
    "file": "plugins/inventory/cl_hooks.lua",
    "node_type": "file",
    "source_id": "file:plugins/inventory/cl_hooks.lua"
  },
  "node_type": "file",
  "file": "plugins/inventory/cl_hooks.lua",
  "degree": 63
}
```

### Text

```text
Runtime topology file summary: plugins/inventory/cl_hooks.lua
This source file participates in 63 topology relationships.
Relationship counts: {'contains_emitter': 1, 'contains_listener': 4, 'contains_network_context': 1, 'contains_network_operation': 26, 'file_receives_network_message': 15, 'file_sends_network_message': 11, 'runs_in_realm': 3, 'owns_file': 2}
Plugin/subsystem guess: unknown
Realm: client
Selected relationships:
- contains_emitter: hook_emitter emit OnCreateStoragePanel @ plugins\inventory\cl_hooks.lua:166
- contains_listener: hook_listener listen CreateNewInventoryPanel @ plugins\inventory\cl_hooks.lua:91
- contains_listener: hook_listener listen CreateTargetNewInventoryPanel @ plugins\inventory\cl_hooks.lua:94
- contains_listener: hook_listener listen CreateNewInventoryPanel @ plugins\inventory\cl_hooks.lua:90
- contains_listener: hook_listener listen CreateTargetNewInventoryPanel @ plugins\inventory\cl_hooks.lua:95
- contains_network_context: network_context Receive OpenMyInv
- contains_network_operation: network_operation netstream hook foodPartAddClient
- contains_network_operation: network_operation netstream hook foodPartUseClient
- contains_network_operation: network_operation netstream hook foodReadyPartAddClient
- contains_network_operation: network_operation netstream hook inventoryCloseOnAction
- contains_network_operation: network_operation netstream hook inventoryOpen
- contains_network_operation: network_operation netstream hook inventoryTargetUpdBg
- contains_network_operation: network_operation netstream hook inventoryTargetUpdSkin
- contains_network_operation: network_operation netstream hook inventoryUpdBg
- contains_network_operation: network_operation netstream hook inventoryUpdSkin
- contains_network_operation: network_operation ne...
```

## Result 10

- Score: **0.6960**
- Rerank score: `1.1159627`
- Rerank bonus: `0.42`
- Rerank reasons: `['doc_type:file_topology:+0.12', 'node_type:file:+0.10', 'intent_node_type:+0.08', 'text_subsystem:character:+0.04', 'network_text_match:+0.08']`
- Source ID: `doc:file_topology:fdad3792c51ac710`
- Doc type: `file_topology`
- Node type: `file`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `gamemode/core/libs/sh_character.lua`

### Metadata

```json
{
  "source_id": "doc:file_topology:fdad3792c51ac710",
  "doc_type": "file_topology",
  "content_hash": "98db3a142c7e6c4a0be2c956e16ba7f4caaa9de39e319ad265874de0ed18a7d1",
  "embedding_dim": 768,
  "text": "Runtime topology file summary: gamemode/core/libs/sh_character.lua\nThis source file participates in 35 topology relationships.\nRelationship counts: {'contains_emitter': 5, 'contains_listener': 2, 'contains_network_operation': 12, 'file_receives_network_message': 3, 'file_sends_network_message': 9, 'runs_in_realm': 3, 'owns_file': 1}\nPlugin/subsystem guess: unknown\nRealm: shared\nSelected relationships:\n- contains_emitter: hook_emitter emit GetDefaultCharName @ gamemode\\core\\libs\\sh_character.lua:97\n- contains_emitter: hook_emitter emit OnCharVarChanged @ gamemode\\core\\libs\\sh_character.lua:189\n- contains_emitter: hook_emitter emit GetDefaultCharName @ gamemode\\core\\libs\\sh_character.lua:137\n- contains_emitter: hook_emitter emit GetDefaultCharName @ gamemode\\core\\libs\\sh_character.lua:129\n- contains_emitter: hook_emitter emit OnCharVarChanged @ gamemode\\core\\libs\\sh_character.lua:306\n- contains_listener: hook_listener listen OnCharCreated @ gamemode\\core\\libs\\sh_character.lua:40\n- contains_listener: hook_listener listen nutCharDeleted @ gamemode\\core\\libs\\sh_character.lua:33\n- contains_network_operation: network_operation netstream hook nutCharFetchNames\n- contains_network_operation: network_operation netstream hook nutCharFetchNames\n- contains_network_operation: network_operation netstream hook nutCharFetchNames\n- contains_network_operation: network_operation netstream send nil\n- contains_network_operation: network_operation netstream send nil\n- contains_network_operation: network_operation netstream send nutCharFetchNames\n- contains_network_operation: network_operation netstream send nutCharFetchNames\n- contains_network_operation: network_operation netstream send nutCharFetchNames\n- contains_network_operation: network_operation netstream send nutCharFetchNames\n- contains_network_operation: network_operation netstream send nutCharFetchNames\n- contains_network_operation: network_operation netstream send receiver\n- contains_network_operation: network_operation netstream send receiver\n- file_receives_network_message: network_message nutCharFetchNames\n- file_receives_network_message: network_message nutCharFetchNames\n- file_receives_network_message: network_message nutCharFetchNames\n- file_sends_network_message: network_message nil\n- file_sends_network_message: network_message nil\n- file_sends_network_message: network_message nutCharFetchNames\n- file_sends_network_message: network_message nutCharFetchNames\n- file_sends_network_message: network_message nutCharFetchNames\n- file_sends_network_message: network_message nutCharFetchNames\n- file_sends_network_message: network_message nutCharFetchNames\n- file_sends_network_message: network_message receiver\n- file_sends_network_message: network_message receiver\n- runs_in_realm: realm shared\n- runs_in_realm: realm shared\n- runs_in_realm: realm shared\n- owns_file: plugin gamemode\nUse this document to retrieve architectural context for this file without loading raw Lua by default.",
  "metadata": {
    "degree": 35,
    "file": "gamemode/core/libs/sh_character.lua",
    "node_type": "file",
    "source_id": "file:gamemode/core/libs/sh_character.lua"
  },
  "node_type": "file",
  "file": "gamemode/core/libs/sh_character.lua",
  "degree": 35
}
```

### Text

```text
Runtime topology file summary: gamemode/core/libs/sh_character.lua
This source file participates in 35 topology relationships.
Relationship counts: {'contains_emitter': 5, 'contains_listener': 2, 'contains_network_operation': 12, 'file_receives_network_message': 3, 'file_sends_network_message': 9, 'runs_in_realm': 3, 'owns_file': 1}
Plugin/subsystem guess: unknown
Realm: shared
Selected relationships:
- contains_emitter: hook_emitter emit GetDefaultCharName @ gamemode\core\libs\sh_character.lua:97
- contains_emitter: hook_emitter emit OnCharVarChanged @ gamemode\core\libs\sh_character.lua:189
- contains_emitter: hook_emitter emit GetDefaultCharName @ gamemode\core\libs\sh_character.lua:137
- contains_emitter: hook_emitter emit GetDefaultCharName @ gamemode\core\libs\sh_character.lua:129
- contains_emitter: hook_emitter emit OnCharVarChanged @ gamemode\core\libs\sh_character.lua:306
- contains_listener: hook_listener listen OnCharCreated @ gamemode\core\libs\sh_character.lua:40
- contains_listener: hook_listener listen nutCharDeleted @ gamemode\core\libs\sh_character.lua:33
- contains_network_operation: network_operation netstream hook nutCharFetchNames
- contains_network_operation: network_operation netstream hook nutCharFetchNames
- contains_network_operation: network_operation netstream hook nutCharFetchNames
- contains_network_operation: network_operation netstream send nil
- contains_network_operation: network_operation netstream send nil
- contains_network_operation: network_operation netstream send nutCharFetchNames
- contains_network_operation: network_operation netstream send nutCharFetchNames
- contains_network_operation: network_operation netstream send nutCharFetchNames
- contains_network_operation: network_operation netstream send nutCharFetchNames
- contain...
```

## Result 11

- Score: **0.7008**
- Rerank score: `1.0808368000000002`
- Rerank bonus: `0.38`
- Rerank reasons: `['doc_type:file_topology:+0.12', 'node_type:file:+0.10', 'intent_node_type:+0.08', 'network_text_match:+0.08']`
- Source ID: `doc:file_topology:f2d977049341a7b2`
- Doc type: `file_topology`
- Node type: `file`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `plugins/newvendorsystem/sh_plugin.lua`

### Metadata

```json
{
  "source_id": "doc:file_topology:f2d977049341a7b2",
  "doc_type": "file_topology",
  "content_hash": "8bce27053f20dbd5f000b7a92787c4676e7e818d43d905c5e8b6d293587a452e",
  "embedding_dim": 768,
  "text": "Runtime topology file summary: plugins/newvendorsystem/sh_plugin.lua\nThis source file participates in 22 topology relationships.\nRelationship counts: {'contains_network_operation': 10, 'file_receives_network_message': 10, 'runs_in_realm': 1, 'owns_file': 1}\nPlugin/subsystem guess: unknown\nRealm: unknown\nSelected relationships:\n- contains_network_operation: network_operation netstream hook applyVendorAppearance\n- contains_network_operation: network_operation netstream hook applyVendorPos\n- contains_network_operation: network_operation netstream hook changeVendorPos\n- contains_network_operation: network_operation netstream hook itemVendorBuySet\n- contains_network_operation: network_operation netstream hook itemVendorRemove\n- contains_network_operation: network_operation netstream hook itemVendorTradeSet\n- contains_network_operation: network_operation netstream hook makeVendorMovable\n- contains_network_operation: network_operation netstream hook removeReceiverFromVendor\n- contains_network_operation: network_operation netstream hook updateVendorFaction\n- contains_network_operation: network_operation netstream hook vendorTrade\n- file_receives_network_message: network_message applyVendorAppearance\n- file_receives_network_message: network_message applyVendorPos\n- file_receives_network_message: network_message changeVendorPos\n- file_receives_network_message: network_message itemVendorBuySet\n- file_receives_network_message: network_message itemVendorRemove\n- file_receives_network_message: network_message itemVendorTradeSet\n- file_receives_network_message: network_message makeVendorMovable\n- file_receives_network_message: network_message removeReceiverFromVendor\n- file_receives_network_message: network_message updateVendorFaction\n- file_receives_network_message: network_message vendorTrade\n- runs_in_realm: realm shared\n- owns_file: plugin newvendorsystem\nUse this document to retrieve architectural context for this file without loading raw Lua by default.",
  "metadata": {
    "degree": 22,
    "file": "plugins/newvendorsystem/sh_plugin.lua",
    "node_type": "file",
    "source_id": "file:plugins/newvendorsystem/sh_plugin.lua"
  },
  "node_type": "file",
  "file": "plugins/newvendorsystem/sh_plugin.lua",
  "degree": 22
}
```

### Text

```text
Runtime topology file summary: plugins/newvendorsystem/sh_plugin.lua
This source file participates in 22 topology relationships.
Relationship counts: {'contains_network_operation': 10, 'file_receives_network_message': 10, 'runs_in_realm': 1, 'owns_file': 1}
Plugin/subsystem guess: unknown
Realm: unknown
Selected relationships:
- contains_network_operation: network_operation netstream hook applyVendorAppearance
- contains_network_operation: network_operation netstream hook applyVendorPos
- contains_network_operation: network_operation netstream hook changeVendorPos
- contains_network_operation: network_operation netstream hook itemVendorBuySet
- contains_network_operation: network_operation netstream hook itemVendorRemove
- contains_network_operation: network_operation netstream hook itemVendorTradeSet
- contains_network_operation: network_operation netstream hook makeVendorMovable
- contains_network_operation: network_operation netstream hook removeReceiverFromVendor
- contains_network_operation: network_operation netstream hook updateVendorFaction
- contains_network_operation: network_operation netstream hook vendorTrade
- file_receives_network_message: network_message applyVendorAppearance
- file_receives_network_message: network_message applyVendorPos
- file_receives_network_message: network_message changeVendorPos
- file_receives_network_message: network_message itemVendorBuySet
- file_receives_network_message: network_message itemVendorRemove
- file_receives_network_message: network_message itemVendorTradeSet
- file_receives_network_message: network_message makeVendorMovable
- file_receives_network_message: network_message removeReceiverFromVendor
- file_receives_network_message: network_message updateVendorFaction
- file_receives_network_message: network_message v...
```

## Result 12

- Score: **0.7041**
- Rerank score: `1.0641068`
- Rerank bonus: `0.36`
- Rerank reasons: `['doc_type:runtime_node:+0.00', 'node_type:hook_emitter:+0.12', 'intent_node_type:+0.08', 'text_subsystem:multichar:+0.04', 'text_event:characterloaded:+0.08', 'realm_awareness:shared:+0.04']`
- Source ID: `doc:runtime_node:c11c5d16372dfa47`
- Doc type: `runtime_node`
- Node type: `hook_emitter`
- Plugin: `None`
- Subsystem: `None`
- Realm: `shared`
- File: `plugins/multichar/sh_plugin.lua`

### Metadata

```json
{
  "source_id": "doc:runtime_node:c11c5d16372dfa47",
  "doc_type": "runtime_node",
  "content_hash": "b7533a3659784b47997e16b040bdf412a809ce64975e99a8e97914e27ced54a1",
  "embedding_dim": 768,
  "text": "Runtime topology node: emit CharacterLoaded @ plugins\\multichar\\sh_plugin.lua:41\nNode ID: emitter:emitter_74d4d83cf2fd\nNode type: hook_emitter\nFile: plugins/multichar/sh_plugin.lua\nRealm: shared\nPlugin/subsystem: unknown\nOutgoing edge counts: {'dispatches_to': 4, 'emits': 1, 'runs_in_realm': 2}\nIncoming edge counts: {'contains_emitter': 1}\nSelected properties: {\"call_type\": \"Run\", \"event\": \"CharacterLoaded\", \"file\": \"plugins\\\\multichar\\\\sh_plugin.lua\", \"graph_layers\": [\"hook\"], \"label\": \"emit CharacterLoaded @ plugins\\\\multichar\\\\sh_plugin.lua:41\", \"line\": 41, \"normalization_status\": \"resolved\", \"realm\": \"shared\", \"resolution_confidence\": \"medium\", \"resolution_source\": \"literal\", \"return_policy\": \"maybe_returns\", \"source_artifact\": \"hook_event_emitters\", \"source_graph\": \"hook\"}\nSelected neighboring relationships:\n- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ plugins\\logging.lua:145\n- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ schema\\hooks\\cl_hooks.lua:121\n- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ plugins\\logging.lua:144\n- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ gamemode\\core\\hooks\\sv_hooks.lua:221\n- outgoing emits -> hook_event CharacterLoaded\n- outgoing runs_in_realm -> realm shared\n- outgoing runs_in_realm -> realm shared\n- incoming contains_emitter -> file plugins\\multichar\\sh_plugin.lua",
  "metadata": {
    "degree": 8,
    "file": "plugins/multichar/sh_plugin.lua",
    "in_degree": 1,
    "label": "emit CharacterLoaded @ plugins\\multichar\\sh_plugin.lua:41",
    "node_type": "hook_emitter",
    "out_degree": 7,
    "plugin": null,
    "realm": "shared",
    "source_id": "emitter:emitter_74d4d83cf2fd",
    "subsystem": null
  },
  "node_type": "hook_emitter",
  "plugin": null,
  "subsystem": null,
  "realm": "shared",
  "file": "plugins/multichar/sh_plugin.lua",
  "degree": 8
}
```

### Text

```text
Runtime topology node: emit CharacterLoaded @ plugins\multichar\sh_plugin.lua:41
Node ID: emitter:emitter_74d4d83cf2fd
Node type: hook_emitter
File: plugins/multichar/sh_plugin.lua
Realm: shared
Plugin/subsystem: unknown
Outgoing edge counts: {'dispatches_to': 4, 'emits': 1, 'runs_in_realm': 2}
Incoming edge counts: {'contains_emitter': 1}
Selected properties: {"call_type": "Run", "event": "CharacterLoaded", "file": "plugins\\multichar\\sh_plugin.lua", "graph_layers": ["hook"], "label": "emit CharacterLoaded @ plugins\\multichar\\sh_plugin.lua:41", "line": 41, "normalization_status": "resolved", "realm": "shared", "resolution_confidence": "medium", "resolution_source": "literal", "return_policy": "maybe_returns", "source_artifact": "hook_event_emitters", "source_graph": "hook"}
Selected neighboring relationships:
- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ plugins\logging.lua:145
- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ schema\hooks\cl_hooks.lua:121
- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ plugins\logging.lua:144
- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ gamemode\core\hooks\sv_hooks.lua:221
- outgoing emits -> hook_event CharacterLoaded
- outgoing runs_in_realm -> realm shared
- outgoing runs_in_realm -> realm shared
- incoming contains_emitter -> file plugins\multichar\sh_plugin.lua
```

## Result 13

- Score: **0.7016**
- Rerank score: `1.0616143999999998`
- Rerank bonus: `0.36`
- Rerank reasons: `['doc_type:runtime_node:+0.00', 'node_type:hook_emitter:+0.12', 'intent_node_type:+0.08', 'text_subsystem:character:+0.04', 'text_event:characterpresave:+0.08', 'realm_awareness:shared:+0.04']`
- Source ID: `doc:runtime_node:d58fb1246ff2ba47`
- Doc type: `runtime_node`
- Node type: `hook_emitter`
- Plugin: `None`
- Subsystem: `None`
- Realm: `shared`
- File: `gamemode/core/meta/sh_character.lua`

### Metadata

```json
{
  "source_id": "doc:runtime_node:d58fb1246ff2ba47",
  "doc_type": "runtime_node",
  "content_hash": "9d7cb78578e526176a20915aa3d94de7f3522c0cf0a75320afcd6249cca8244d",
  "embedding_dim": 768,
  "text": "Runtime topology node: emit CharacterPreSave @ gamemode\\core\\meta\\sh_character.lua:42\nNode ID: emitter:emitter_6566c7251cfe\nNode type: hook_emitter\nFile: gamemode/core/meta/sh_character.lua\nRealm: shared\nPlugin/subsystem: unknown\nOutgoing edge counts: {'dispatches_to': 11, 'emits': 1, 'runs_in_realm': 2}\nIncoming edge counts: {'contains_emitter': 1}\nSelected properties: {\"call_type\": \"Run\", \"event\": \"CharacterPreSave\", \"file\": \"gamemode\\\\core\\\\meta\\\\sh_character.lua\", \"graph_layers\": [\"hook\"], \"label\": \"emit CharacterPreSave @ gamemode\\\\core\\\\meta\\\\sh_character.lua:42\", \"line\": 42, \"normalization_status\": \"resolved\", \"realm\": \"shared\", \"resolution_confidence\": \"low\", \"resolution_source\": \"literal\", \"return_policy\": \"maybe_returns\", \"source_artifact\": \"hook_event_emitters\", \"source_graph\": \"hook\"}\nSelected neighboring relationships:\n- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\\ammosave.lua:42\n- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\\inventory\\sh_plugin.lua:719\n- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\\spawnsaver.lua:6\n- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\\inventory\\sh_plugin.lua:718\n- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\\healthproblems\\sv_hooks.lua:575\n- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\\spawnsaver.lua:6\n- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\\needs\\sv_hooks.lua:119\n- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ gamemode\\core\\hooks\\sv_hooks.lua:740\n- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\\needs\\sv_hooks.lua:120\n- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\\healthproblems\\sv_hooks.lua:576\n- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\\ammosave.lua:42\n- outgoing emits -> hook_event CharacterPreSave\n- incoming contains_emitter -> file gamemode\\core\\meta\\sh_character.lua",
  "metadata": {
    "degree": 15,
    "file": "gamemode/core/meta/sh_character.lua",
    "in_degree": 1,
    "label": "emit CharacterPreSave @ gamemode\\core\\meta\\sh_character.lua:42",
    "node_type": "hook_emitter",
    "out_degree": 14,
    "plugin": null,
    "realm": "shared",
    "source_id": "emitter:emitter_6566c7251cfe",
    "subsystem": null
  },
  "node_type": "hook_emitter",
  "plugin": null,
  "subsystem": null,
  "realm": "shared",
  "file": "gamemode/core/meta/sh_character.lua",
  "degree": 15
}
```

### Text

```text
Runtime topology node: emit CharacterPreSave @ gamemode\core\meta\sh_character.lua:42
Node ID: emitter:emitter_6566c7251cfe
Node type: hook_emitter
File: gamemode/core/meta/sh_character.lua
Realm: shared
Plugin/subsystem: unknown
Outgoing edge counts: {'dispatches_to': 11, 'emits': 1, 'runs_in_realm': 2}
Incoming edge counts: {'contains_emitter': 1}
Selected properties: {"call_type": "Run", "event": "CharacterPreSave", "file": "gamemode\\core\\meta\\sh_character.lua", "graph_layers": ["hook"], "label": "emit CharacterPreSave @ gamemode\\core\\meta\\sh_character.lua:42", "line": 42, "normalization_status": "resolved", "realm": "shared", "resolution_confidence": "low", "resolution_source": "literal", "return_policy": "maybe_returns", "source_artifact": "hook_event_emitters", "source_graph": "hook"}
Selected neighboring relationships:
- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\ammosave.lua:42
- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\inventory\sh_plugin.lua:719
- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\spawnsaver.lua:6
- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\inventory\sh_plugin.lua:718
- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\healthproblems\sv_hooks.lua:575
- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\spawnsaver.lua:6
- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\needs\sv_hooks.lua:119
- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ gamemode\core\hooks\sv_hooks.lua:740
- outgoing dispatches_to -> hook_listener listen CharacterPreSave @ plugins\needs\sv_hooks.lua:120
- outgoing dispatches_to -> hook_listener listen CharacterP...
```

## Result 14

- Score: **0.6995**
- Rerank score: `1.059537`
- Rerank bonus: `0.36`
- Rerank reasons: `['doc_type:runtime_node:+0.00', 'node_type:hook_emitter:+0.12', 'intent_node_type:+0.08', 'text_subsystem:character:+0.04', 'text_event:characterloaded:+0.08', 'realm_awareness:shared:+0.04']`
- Source ID: `doc:runtime_node:819310f067a6850d`
- Doc type: `runtime_node`
- Node type: `hook_emitter`
- Plugin: `None`
- Subsystem: `None`
- Realm: `shared`
- File: `gamemode/core/meta/sh_character.lua`

### Metadata

```json
{
  "source_id": "doc:runtime_node:819310f067a6850d",
  "doc_type": "runtime_node",
  "content_hash": "3d2d524e6b4f08252c8b4b3de5c83e98c40c7f354882991a10be362bbe93ee25",
  "embedding_dim": 768,
  "text": "Runtime topology node: emit CharacterLoaded @ gamemode\\core\\meta\\sh_character.lua:129\nNode ID: emitter:emitter_739379a19d2e\nNode type: hook_emitter\nFile: gamemode/core/meta/sh_character.lua\nRealm: shared\nPlugin/subsystem: unknown\nOutgoing edge counts: {'dispatches_to': 4, 'emits': 1, 'runs_in_realm': 2}\nIncoming edge counts: {'contains_emitter': 1}\nSelected properties: {\"call_type\": \"Run\", \"event\": \"CharacterLoaded\", \"file\": \"gamemode\\\\core\\\\meta\\\\sh_character.lua\", \"graph_layers\": [\"hook\"], \"label\": \"emit CharacterLoaded @ gamemode\\\\core\\\\meta\\\\sh_character.lua:129\", \"line\": 129, \"normalization_status\": \"resolved\", \"realm\": \"shared\", \"resolution_confidence\": \"medium\", \"resolution_source\": \"literal\", \"return_policy\": \"maybe_returns\", \"source_artifact\": \"hook_event_emitters\", \"source_graph\": \"hook\"}\nSelected neighboring relationships:\n- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ plugins\\logging.lua:145\n- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ schema\\hooks\\cl_hooks.lua:121\n- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ plugins\\logging.lua:144\n- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ gamemode\\core\\hooks\\sv_hooks.lua:221\n- outgoing emits -> hook_event CharacterLoaded\n- outgoing runs_in_realm -> realm shared\n- outgoing runs_in_realm -> realm shared\n- incoming contains_emitter -> file gamemode\\core\\meta\\sh_character.lua",
  "metadata": {
    "degree": 8,
    "file": "gamemode/core/meta/sh_character.lua",
    "in_degree": 1,
    "label": "emit CharacterLoaded @ gamemode\\core\\meta\\sh_character.lua:129",
    "node_type": "hook_emitter",
    "out_degree": 7,
    "plugin": null,
    "realm": "shared",
    "source_id": "emitter:emitter_739379a19d2e",
    "subsystem": null
  },
  "node_type": "hook_emitter",
  "plugin": null,
  "subsystem": null,
  "realm": "shared",
  "file": "gamemode/core/meta/sh_character.lua",
  "degree": 8
}
```

### Text

```text
Runtime topology node: emit CharacterLoaded @ gamemode\core\meta\sh_character.lua:129
Node ID: emitter:emitter_739379a19d2e
Node type: hook_emitter
File: gamemode/core/meta/sh_character.lua
Realm: shared
Plugin/subsystem: unknown
Outgoing edge counts: {'dispatches_to': 4, 'emits': 1, 'runs_in_realm': 2}
Incoming edge counts: {'contains_emitter': 1}
Selected properties: {"call_type": "Run", "event": "CharacterLoaded", "file": "gamemode\\core\\meta\\sh_character.lua", "graph_layers": ["hook"], "label": "emit CharacterLoaded @ gamemode\\core\\meta\\sh_character.lua:129", "line": 129, "normalization_status": "resolved", "realm": "shared", "resolution_confidence": "medium", "resolution_source": "literal", "return_policy": "maybe_returns", "source_artifact": "hook_event_emitters", "source_graph": "hook"}
Selected neighboring relationships:
- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ plugins\logging.lua:145
- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ schema\hooks\cl_hooks.lua:121
- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ plugins\logging.lua:144
- outgoing dispatches_to -> hook_listener listen CharacterLoaded @ gamemode\core\hooks\sv_hooks.lua:221
- outgoing emits -> hook_event CharacterLoaded
- outgoing runs_in_realm -> realm shared
- outgoing runs_in_realm -> realm shared
- incoming contains_emitter -> file gamemode\core\meta\sh_character.lua
```

## Result 15

- Score: **0.7175**
- Rerank score: `1.05751314`
- Rerank bonus: `0.34`
- Rerank reasons: `['doc_type:runtime_node:+0.00', 'node_type:hook_event:+0.14', 'intent_node_type:+0.08', 'text_subsystem:multichar:+0.04', 'text_event:characterloaded:+0.08']`
- Source ID: `doc:runtime_node:d92f6f532bd21025`
- Doc type: `runtime_node`
- Node type: `hook_event`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `None`

### Metadata

```json
{
  "source_id": "doc:runtime_node:d92f6f532bd21025",
  "doc_type": "runtime_node",
  "content_hash": "f21dd42c874981f9d82a0ff144b2364d97f918462389b1d93230b037cd48ff73",
  "embedding_dim": 768,
  "text": "Runtime topology node: CharacterLoaded\nNode ID: hook:CharacterLoaded\nNode type: hook_event\nFile: n/a\nRealm: unknown\nPlugin/subsystem: unknown\nOutgoing edge counts: {'classified_as': 1}\nIncoming edge counts: {'emits': 2, 'emits_event': 1, 'listens_to': 4, 'listens_to_event': 3}\nSelected properties: {\"emitter_count\": 2, \"event\": \"CharacterLoaded\", \"event_class\": \"framework_lifecycle\", \"graph_layers\": [\"hook\"], \"has_emitters\": true, \"has_listeners\": true, \"label\": \"CharacterLoaded\", \"listener_count\": 4, \"realms_emitted\": [\"shared\"], \"realms_listened\": [\"client\", \"server\", \"shared\"], \"return_policy\": \"maybe_returns\", \"source\": \"hook_event_graph\", \"source_artifact\": \"hook_event_listeners\", \"source_graph\": \"hook\", \"topology_role\": \"runtime_signal\"}\nSelected neighboring relationships:\n- outgoing classified_as -> event_class framework_lifecycle\n- incoming emits -> hook_emitter emit CharacterLoaded @ gamemode\\core\\meta\\sh_character.lua:129\n- incoming emits -> hook_emitter emit CharacterLoaded @ plugins\\multichar\\sh_plugin.lua:41\n- incoming emits_event -> plugin multichar\n- incoming listens_to -> hook_listener listen CharacterLoaded @ plugins\\logging.lua:145\n- incoming listens_to -> hook_listener listen CharacterLoaded @ schema\\hooks\\cl_hooks.lua:121\n- incoming listens_to -> hook_listener listen CharacterLoaded @ plugins\\logging.lua:144\n- incoming listens_to -> hook_listener listen CharacterLoaded @ gamemode\\core\\hooks\\sv_hooks.lua:221\n- incoming listens_to_event -> gamemode GM\n- incoming listens_to_event -> plugin logging.lua\n- incoming listens_to_event -> schema schema",
  "metadata": {
    "degree": 11,
    "file": null,
    "in_degree": 10,
    "label": "CharacterLoaded",
    "node_type": "hook_event",
    "out_degree": 1,
    "plugin": null,
    "realm": null,
    "source_id": "hook:CharacterLoaded",
    "subsystem": null
  },
  "node_type": "hook_event",
  "plugin": null,
  "subsystem": null,
  "realm": null,
  "file": null,
  "degree": 11
}
```

### Text

```text
Runtime topology node: CharacterLoaded
Node ID: hook:CharacterLoaded
Node type: hook_event
File: n/a
Realm: unknown
Plugin/subsystem: unknown
Outgoing edge counts: {'classified_as': 1}
Incoming edge counts: {'emits': 2, 'emits_event': 1, 'listens_to': 4, 'listens_to_event': 3}
Selected properties: {"emitter_count": 2, "event": "CharacterLoaded", "event_class": "framework_lifecycle", "graph_layers": ["hook"], "has_emitters": true, "has_listeners": true, "label": "CharacterLoaded", "listener_count": 4, "realms_emitted": ["shared"], "realms_listened": ["client", "server", "shared"], "return_policy": "maybe_returns", "source": "hook_event_graph", "source_artifact": "hook_event_listeners", "source_graph": "hook", "topology_role": "runtime_signal"}
Selected neighboring relationships:
- outgoing classified_as -> event_class framework_lifecycle
- incoming emits -> hook_emitter emit CharacterLoaded @ gamemode\core\meta\sh_character.lua:129
- incoming emits -> hook_emitter emit CharacterLoaded @ plugins\multichar\sh_plugin.lua:41
- incoming emits_event -> plugin multichar
- incoming listens_to -> hook_listener listen CharacterLoaded @ plugins\logging.lua:145
- incoming listens_to -> hook_listener listen CharacterLoaded @ schema\hooks\cl_hooks.lua:121
- incoming listens_to -> hook_listener listen CharacterLoaded @ plugins\logging.lua:144
- incoming listens_to -> hook_listener listen CharacterLoaded @ gamemode\core\hooks\sv_hooks.lua:221
- incoming listens_to_event -> gamemode GM
- incoming listens_to_event -> plugin logging.lua
- incoming listens_to_event -> schema schema
```

## Result 16

- Score: **0.7073**
- Rerank score: `1.0472511299999998`
- Rerank bonus: `0.33999999999999997`
- Rerank reasons: `['doc_type:runtime_node:+0.00', 'node_type:file:+0.10', 'intent_node_type:+0.08', 'text_subsystem:inventory:+0.04', 'network_text_match:+0.08', 'realm_awareness:server:+0.04']`
- Source ID: `doc:runtime_node:5e2f777d61e66256`
- Doc type: `runtime_node`
- Node type: `file`
- Plugin: `None`
- Subsystem: `None`
- Realm: `server`
- File: `plugins/inventory/sv_hooks.lua`

### Metadata

```json
{
  "source_id": "doc:runtime_node:5e2f777d61e66256",
  "doc_type": "runtime_node",
  "content_hash": "fb8bc9a9709f250ac63bb7414fff3506fc8dd2d02d647c3fa8328a07c3daf83b",
  "embedding_dim": 768,
  "text": "Runtime topology node: plugins\\inventory\\sv_hooks.lua\nNode ID: file:plugins/inventory/sv_hooks.lua\nNode type: file\nFile: plugins/inventory/sv_hooks.lua\nRealm: server\nPlugin/subsystem: unknown\nOutgoing edge counts: {'contains_emitter': 1, 'contains_listener': 4, 'contains_network_operation': 3, 'contains_timer_operation': 2, 'file_receives_network_message': 2, 'file_sends_network_message': 1, 'runs_in_realm': 3}\nIncoming edge counts: {'owns_file': 3}\nSelected properties: {\"framework_layer\": \"domain\", \"graph_layers\": [\"hook\", \"network\", \"timer\"], \"label\": \"plugins\\\\inventory\\\\sv_hooks.lua\", \"merge_conflicts\": {\"source_graph\": [\"hook\", \"network\", \"timer\"]}, \"path\": \"plugins\\\\inventory\\\\sv_hooks.lua\", \"props\": {\"path\": \"plugins\\\\inventory\\\\sv_hooks.lua\"}, \"realm\": \"server\", \"source\": \"emitter_file\", \"source_graph\": \"hook\"}\nSelected neighboring relationships:\n- outgoing contains_emitter -> hook_emitter emit CheckBothHandsAmputation @ plugins\\inventory\\sv_hooks.lua:11\n- outgoing contains_listener -> hook_listener listen ItemTransfered @ plugins\\inventory\\sv_hooks.lua:41\n- outgoing contains_listener -> hook_listener listen PlayerButtonDown @ plugins\\inventory\\sv_hooks.lua:3\n- outgoing contains_listener -> hook_listener listen ItemTransfered @ plugins\\inventory\\sv_hooks.lua:42\n- outgoing contains_listener -> hook_listener listen PlayerButtonDown @ plugins\\inventory\\sv_hooks.lua:2\n- outgoing contains_network_operation -> network_operation netstream hook inventoryPackAmmo\n- outgoing contains_network_operation -> network_operation netstream hook inventorySetPanelStatus\n- outgoing contains_network_operation -> network_operation netstream send inventoryOpen\n- outgoing contains_timer_operation -> timer_operation entity_timer_simple@plugins\\inventory\\sv_hooks.lua:123\n- outgoing contains_timer_operation -> timer_operation player_action_timer@plugins\\inventory\\sv_hooks.lua:16\n- outgoing file_receives_network_message -> network_message inventoryPackAmmo\n- outgoing file_receives_network_message -> network_message inventorySetPanelStatus\n- incoming owns_file -> plugin inventory\n- incoming owns_file -> plugin inventory\n- incoming owns_file -> plugin inventory",
  "metadata": {
    "degree": 19,
    "file": "plugins/inventory/sv_hooks.lua",
    "in_degree": 3,
    "label": "plugins\\inventory\\sv_hooks.lua",
    "node_type": "file",
    "out_degree": 16,
    "plugin": null,
    "realm": "server",
    "source_id": "file:plugins/inventory/sv_hooks.lua",
    "subsystem": null
  },
  "node_type": "file",
  "plugin": null,
  "subsystem": null,
  "realm": "server",
  "file": "plugins/inventory/sv_hooks.lua",
  "degree": 19
}
```

### Text

```text
Runtime topology node: plugins\inventory\sv_hooks.lua
Node ID: file:plugins/inventory/sv_hooks.lua
Node type: file
File: plugins/inventory/sv_hooks.lua
Realm: server
Plugin/subsystem: unknown
Outgoing edge counts: {'contains_emitter': 1, 'contains_listener': 4, 'contains_network_operation': 3, 'contains_timer_operation': 2, 'file_receives_network_message': 2, 'file_sends_network_message': 1, 'runs_in_realm': 3}
Incoming edge counts: {'owns_file': 3}
Selected properties: {"framework_layer": "domain", "graph_layers": ["hook", "network", "timer"], "label": "plugins\\inventory\\sv_hooks.lua", "merge_conflicts": {"source_graph": ["hook", "network", "timer"]}, "path": "plugins\\inventory\\sv_hooks.lua", "props": {"path": "plugins\\inventory\\sv_hooks.lua"}, "realm": "server", "source": "emitter_file", "source_graph": "hook"}
Selected neighboring relationships:
- outgoing contains_emitter -> hook_emitter emit CheckBothHandsAmputation @ plugins\inventory\sv_hooks.lua:11
- outgoing contains_listener -> hook_listener listen ItemTransfered @ plugins\inventory\sv_hooks.lua:41
- outgoing contains_listener -> hook_listener listen PlayerButtonDown @ plugins\inventory\sv_hooks.lua:3
- outgoing contains_listener -> hook_listener listen ItemTransfered @ plugins\inventory\sv_hooks.lua:42
- outgoing contains_listener -> hook_listener listen PlayerButtonDown @ plugins\inventory\sv_hooks.lua:2
- outgoing contains_network_operation -> network_operation netstream hook inventoryPackAmmo
- outgoing contains_network_operation -> network_operation netstream hook inventorySetPanelStatus
- outgoing contains_network_operation -> network_operation netstream send inventoryOpen
- outgoing contains_timer_operation -> timer_operation entity_timer_simple@plugins\inventory\sv_hooks.lua:123
- outgoing contai...
```

## Result 17

- Score: **0.7066**
- Rerank score: `1.046589`
- Rerank bonus: `0.34`
- Rerank reasons: `['doc_type:runtime_node:+0.00', 'node_type:hook_event:+0.14', 'intent_node_type:+0.08', 'text_subsystem:character:+0.04', 'text_event:characterpresave:+0.08']`
- Source ID: `doc:runtime_node:a60fd745ef7de37a`
- Doc type: `runtime_node`
- Node type: `hook_event`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `None`

### Metadata

```json
{
  "source_id": "doc:runtime_node:a60fd745ef7de37a",
  "doc_type": "runtime_node",
  "content_hash": "5fc00f9c7fcda54a5d44070f50a2f5a1b6a73ac1a79c32505c920cf1e278039a",
  "embedding_dim": 768,
  "text": "Runtime topology node: CharacterPreSave\nNode ID: hook:CharacterPreSave\nNode type: hook_event\nFile: n/a\nRealm: unknown\nPlugin/subsystem: unknown\nOutgoing edge counts: {'classified_as': 1}\nIncoming edge counts: {'emits': 1, 'listens_to': 11, 'listens_to_event': 6}\nSelected properties: {\"emitter_count\": 1, \"event\": \"CharacterPreSave\", \"event_class\": \"framework_lifecycle\", \"graph_layers\": [\"hook\"], \"has_emitters\": true, \"has_listeners\": true, \"label\": \"CharacterPreSave\", \"listener_count\": 11, \"realms_emitted\": [\"shared\"], \"realms_listened\": [\"server\", \"shared\"], \"return_policy\": \"maybe_returns\", \"source\": \"hook_event_graph\", \"source_artifact\": \"hook_event_listeners\", \"source_graph\": \"hook\", \"topology_role\": \"runtime_signal\"}\nSelected neighboring relationships:\n- outgoing classified_as -> event_class framework_lifecycle\n- incoming emits -> hook_emitter emit CharacterPreSave @ gamemode\\core\\meta\\sh_character.lua:42\n- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\\ammosave.lua:42\n- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\\inventory\\sh_plugin.lua:719\n- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\\spawnsaver.lua:6\n- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\\inventory\\sh_plugin.lua:718\n- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\\healthproblems\\sv_hooks.lua:575\n- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\\spawnsaver.lua:6\n- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\\needs\\sv_hooks.lua:119\n- incoming listens_to -> hook_listener listen CharacterPreSave @ gamemode\\core\\hooks\\sv_hooks.lua:740\n- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\\needs\\sv_hooks.lua:120\n- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\\healthproblems\\sv_hooks.lua:576\n- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\\ammosave.lua:42",
  "metadata": {
    "degree": 19,
    "file": null,
    "in_degree": 18,
    "label": "CharacterPreSave",
    "node_type": "hook_event",
    "out_degree": 1,
    "plugin": null,
    "realm": null,
    "source_id": "hook:CharacterPreSave",
    "subsystem": null
  },
  "node_type": "hook_event",
  "plugin": null,
  "subsystem": null,
  "realm": null,
  "file": null,
  "degree": 19
}
```

### Text

```text
Runtime topology node: CharacterPreSave
Node ID: hook:CharacterPreSave
Node type: hook_event
File: n/a
Realm: unknown
Plugin/subsystem: unknown
Outgoing edge counts: {'classified_as': 1}
Incoming edge counts: {'emits': 1, 'listens_to': 11, 'listens_to_event': 6}
Selected properties: {"emitter_count": 1, "event": "CharacterPreSave", "event_class": "framework_lifecycle", "graph_layers": ["hook"], "has_emitters": true, "has_listeners": true, "label": "CharacterPreSave", "listener_count": 11, "realms_emitted": ["shared"], "realms_listened": ["server", "shared"], "return_policy": "maybe_returns", "source": "hook_event_graph", "source_artifact": "hook_event_listeners", "source_graph": "hook", "topology_role": "runtime_signal"}
Selected neighboring relationships:
- outgoing classified_as -> event_class framework_lifecycle
- incoming emits -> hook_emitter emit CharacterPreSave @ gamemode\core\meta\sh_character.lua:42
- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\ammosave.lua:42
- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\inventory\sh_plugin.lua:719
- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\spawnsaver.lua:6
- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\inventory\sh_plugin.lua:718
- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\healthproblems\sv_hooks.lua:575
- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\spawnsaver.lua:6
- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\needs\sv_hooks.lua:119
- incoming listens_to -> hook_listener listen CharacterPreSave @ gamemode\core\hooks\sv_hooks.lua:740
- incoming listens_to -> hook_listener listen CharacterPreSave @ plugins\needs\sv_hooks.lua:120
- incom...
```

## Result 18

- Score: **0.7038**
- Rerank score: `1.04377535`
- Rerank bonus: `0.34`
- Rerank reasons: `['doc_type:runtime_node:+0.00', 'node_type:hook_event:+0.14', 'intent_node_type:+0.08', 'text_subsystem:inventory:+0.04', 'text_event:playerloadout:+0.08']`
- Source ID: `doc:runtime_node:b5b67b6f52f8aefa`
- Doc type: `runtime_node`
- Node type: `hook_event`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `None`

### Metadata

```json
{
  "source_id": "doc:runtime_node:b5b67b6f52f8aefa",
  "doc_type": "runtime_node",
  "content_hash": "7667abb06d3b49e674e7a0ce5ae9ab7b59d49f309629a5435a9e078692f214ee",
  "embedding_dim": 768,
  "text": "Runtime topology node: PlayerLoadout\nNode ID: hook:PlayerLoadout\nNode type: hook_event\nFile: n/a\nRealm: unknown\nPlugin/subsystem: unknown\nOutgoing edge counts: {'classified_as': 1}\nIncoming edge counts: {'emits': 2, 'listens_to': 11, 'listens_to_event': 6}\nSelected properties: {\"emitter_count\": 2, \"event\": \"PlayerLoadout\", \"event_class\": \"player_lifecycle_or_action\", \"graph_layers\": [\"hook\"], \"has_emitters\": true, \"has_listeners\": true, \"label\": \"PlayerLoadout\", \"listener_count\": 11, \"realms_emitted\": [\"server\"], \"realms_listened\": [\"server\", \"shared\"], \"return_policy\": \"maybe_returns\", \"source\": \"hook_event_graph\", \"source_artifact\": \"hook_event_listeners\", \"source_graph\": \"hook\", \"topology_role\": \"runtime_signal\"}\nSelected neighboring relationships:\n- outgoing classified_as -> event_class player_lifecycle_or_action\n- incoming emits -> hook_emitter emit PlayerLoadout @ gamemode\\core\\hooks\\sv_hooks.lua:219\n- incoming emits -> hook_emitter emit PlayerLoadout @ gamemode\\core\\hooks\\sv_hooks.lua:263\n- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\\pac\\sv_parts.lua:53\n- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\\mnhr\\sh_plugin.lua:200\n- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\\tying\\sh_plugin.lua:42\n- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\\armor\\sh_plugin.lua:270\n- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\\pac\\sv_parts.lua:52\n- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\\mnhr\\sh_plugin.lua:201\n- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\\tying\\sh_plugin.lua:42\n- incoming listens_to -> hook_listener listen PlayerLoadout @ gamemode\\core\\hooks\\sv_hooks.lua:311\n- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\\inventory\\sh_plugin.lua:638\n- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\\armor\\sh_plugin.lua:269",
  "metadata": {
    "degree": 20,
    "file": null,
    "in_degree": 19,
    "label": "PlayerLoadout",
    "node_type": "hook_event",
    "out_degree": 1,
    "plugin": null,
    "realm": null,
    "source_id": "hook:PlayerLoadout",
    "subsystem": null
  },
  "node_type": "hook_event",
  "plugin": null,
  "subsystem": null,
  "realm": null,
  "file": null,
  "degree": 20
}
```

### Text

```text
Runtime topology node: PlayerLoadout
Node ID: hook:PlayerLoadout
Node type: hook_event
File: n/a
Realm: unknown
Plugin/subsystem: unknown
Outgoing edge counts: {'classified_as': 1}
Incoming edge counts: {'emits': 2, 'listens_to': 11, 'listens_to_event': 6}
Selected properties: {"emitter_count": 2, "event": "PlayerLoadout", "event_class": "player_lifecycle_or_action", "graph_layers": ["hook"], "has_emitters": true, "has_listeners": true, "label": "PlayerLoadout", "listener_count": 11, "realms_emitted": ["server"], "realms_listened": ["server", "shared"], "return_policy": "maybe_returns", "source": "hook_event_graph", "source_artifact": "hook_event_listeners", "source_graph": "hook", "topology_role": "runtime_signal"}
Selected neighboring relationships:
- outgoing classified_as -> event_class player_lifecycle_or_action
- incoming emits -> hook_emitter emit PlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:219
- incoming emits -> hook_emitter emit PlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:263
- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\pac\sv_parts.lua:53
- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\mnhr\sh_plugin.lua:200
- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\tying\sh_plugin.lua:42
- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\armor\sh_plugin.lua:270
- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\pac\sv_parts.lua:52
- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\mnhr\sh_plugin.lua:201
- incoming listens_to -> hook_listener listen PlayerLoadout @ plugins\tying\sh_plugin.lua:42
- incoming listens_to -> hook_listener listen PlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:311
- incoming listens_to -> hook_listener liste...
```

## Result 19

- Score: **0.6983**
- Rerank score: `1.03833076`
- Rerank bonus: `0.34`
- Rerank reasons: `['doc_type:runtime_node:+0.00', 'node_type:hook_event:+0.14', 'intent_node_type:+0.08', 'text_subsystem:inventory:+0.04', 'text_event:postplayerloadout:+0.08']`
- Source ID: `doc:runtime_node:64ba1bba577e6086`
- Doc type: `runtime_node`
- Node type: `hook_event`
- Plugin: `None`
- Subsystem: `None`
- Realm: `None`
- File: `None`

### Metadata

```json
{
  "source_id": "doc:runtime_node:64ba1bba577e6086",
  "doc_type": "runtime_node",
  "content_hash": "a40406a43ee2c4095d4473e8b43b6985e9bcc6fc1a0fe209b3f743dd29a80667",
  "embedding_dim": 768,
  "text": "Runtime topology node: PostPlayerLoadout\nNode ID: hook:PostPlayerLoadout\nNode type: hook_event\nFile: n/a\nRealm: unknown\nPlugin/subsystem: unknown\nOutgoing edge counts: {'classified_as': 1}\nIncoming edge counts: {'emits': 1, 'listens_to': 16, 'listens_to_event': 8}\nSelected properties: {\"emitter_count\": 1, \"event\": \"PostPlayerLoadout\", \"event_class\": \"player_lifecycle_or_action\", \"graph_layers\": [\"hook\"], \"has_emitters\": true, \"has_listeners\": true, \"label\": \"PostPlayerLoadout\", \"listener_count\": 16, \"realms_emitted\": [\"server\"], \"realms_listened\": [\"server\", \"shared\"], \"return_policy\": \"maybe_returns\", \"source\": \"hook_event_graph\", \"source_artifact\": \"hook_event_listeners\", \"source_graph\": \"hook\", \"topology_role\": \"runtime_signal\"}\nSelected neighboring relationships:\n- outgoing classified_as -> event_class player_lifecycle_or_action\n- incoming emits -> hook_emitter emit PostPlayerLoadout @ gamemode\\core\\hooks\\sv_hooks.lua:367\n- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\\attributes\\plugins\\strength\\sh_plugin.lua:112\n- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\\admintools\\sh_plugin.lua:473\n- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\\traits\\sh_plugin.lua:517\n- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\\spawns.lua:8\n- incoming listens_to -> hook_listener listen PostPlayerLoadout @ schema\\hooks\\sv_hooks.lua:146\n- incoming listens_to -> hook_listener listen PostPlayerLoadout @ gamemode\\core\\hooks\\sv_hooks.lua:376\n- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\\attributes\\sh_plugin.lua:56\n- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\\healthproblems\\sv_hooks.lua:294\n- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\\inventory\\sh_plugin.lua:688\n- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\\admintools\\sh_plugin.lua:474\n- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\\attributes\\plugins\\strength\\sh_plugin.lua:111",
  "metadata": {
    "degree": 26,
    "file": null,
    "in_degree": 25,
    "label": "PostPlayerLoadout",
    "node_type": "hook_event",
    "out_degree": 1,
    "plugin": null,
    "realm": null,
    "source_id": "hook:PostPlayerLoadout",
    "subsystem": null
  },
  "node_type": "hook_event",
  "plugin": null,
  "subsystem": null,
  "realm": null,
  "file": null,
  "degree": 26
}
```

### Text

```text
Runtime topology node: PostPlayerLoadout
Node ID: hook:PostPlayerLoadout
Node type: hook_event
File: n/a
Realm: unknown
Plugin/subsystem: unknown
Outgoing edge counts: {'classified_as': 1}
Incoming edge counts: {'emits': 1, 'listens_to': 16, 'listens_to_event': 8}
Selected properties: {"emitter_count": 1, "event": "PostPlayerLoadout", "event_class": "player_lifecycle_or_action", "graph_layers": ["hook"], "has_emitters": true, "has_listeners": true, "label": "PostPlayerLoadout", "listener_count": 16, "realms_emitted": ["server"], "realms_listened": ["server", "shared"], "return_policy": "maybe_returns", "source": "hook_event_graph", "source_artifact": "hook_event_listeners", "source_graph": "hook", "topology_role": "runtime_signal"}
Selected neighboring relationships:
- outgoing classified_as -> event_class player_lifecycle_or_action
- incoming emits -> hook_emitter emit PostPlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:367
- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\attributes\plugins\strength\sh_plugin.lua:112
- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\admintools\sh_plugin.lua:473
- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\traits\sh_plugin.lua:517
- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\spawns.lua:8
- incoming listens_to -> hook_listener listen PostPlayerLoadout @ schema\hooks\sv_hooks.lua:146
- incoming listens_to -> hook_listener listen PostPlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:376
- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\attributes\sh_plugin.lua:56
- incoming listens_to -> hook_listener listen PostPlayerLoadout @ plugins\healthproblems\sv_hooks.lua:294
- incoming listens_to -> hook_listener liste...
```

## Result 20

- Score: **0.6968**
- Rerank score: `1.0368022`
- Rerank bonus: `0.33999999999999997`
- Rerank reasons: `['doc_type:runtime_node:+0.00', 'node_type:file:+0.10', 'intent_node_type:+0.08', 'text_subsystem:inventory:+0.04', 'network_text_match:+0.08', 'realm_awareness:client:+0.04']`
- Source ID: `doc:runtime_node:07ce874eb4df93be`
- Doc type: `runtime_node`
- Node type: `file`
- Plugin: `None`
- Subsystem: `None`
- Realm: `client`
- File: `gamemode/core/derma/cl_inventory.lua`

### Metadata

```json
{
  "source_id": "doc:runtime_node:07ce874eb4df93be",
  "doc_type": "runtime_node",
  "content_hash": "54de533f4e5225f4be10d305b3fc1e4f196e68ff57d7385a0b161b5e480d4aaf",
  "embedding_dim": 768,
  "text": "Runtime topology node: gamemode\\core\\derma\\cl_inventory.lua\nNode ID: file:gamemode/core/derma/cl_inventory.lua\nNode type: file\nFile: gamemode/core/derma/cl_inventory.lua\nRealm: client\nPlugin/subsystem: unknown\nOutgoing edge counts: {'contains_emitter': 2, 'contains_network_operation': 3, 'file_sends_network_message': 3, 'runs_in_realm': 3}\nIncoming edge counts: {'owns_file': 1}\nSelected properties: {\"framework_layer\": \"framework\", \"graph_layers\": [\"hook\", \"network\"], \"label\": \"gamemode\\\\core\\\\derma\\\\cl_inventory.lua\", \"merge_conflicts\": {\"source_graph\": [\"hook\", \"network\"]}, \"path\": \"gamemode\\\\core\\\\derma\\\\cl_inventory.lua\", \"props\": {\"path\": \"gamemode\\\\core\\\\derma\\\\cl_inventory.lua\"}, \"realm\": \"client\", \"source\": \"emitter_file\", \"source_graph\": \"hook\"}\nSelected neighboring relationships:\n- outgoing contains_emitter -> hook_emitter emit ItemPaintOver @ gamemode\\core\\derma\\cl_inventory.lua:130\n- outgoing contains_emitter -> hook_emitter emit OnCreateItemInteractionMenu @ gamemode\\core\\derma\\cl_inventory.lua:153\n- outgoing contains_network_operation -> network_operation netstream send invAct\n- outgoing contains_network_operation -> network_operation netstream send invAct\n- outgoing contains_network_operation -> network_operation netstream send invAct\n- outgoing file_sends_network_message -> network_message invAct\n- outgoing file_sends_network_message -> network_message invAct\n- outgoing file_sends_network_message -> network_message invAct\n- outgoing runs_in_realm -> realm client\n- outgoing runs_in_realm -> realm client\n- outgoing runs_in_realm -> realm client\n- incoming owns_file -> plugin gamemode",
  "metadata": {
    "degree": 12,
    "file": "gamemode/core/derma/cl_inventory.lua",
    "in_degree": 1,
    "label": "gamemode\\core\\derma\\cl_inventory.lua",
    "node_type": "file",
    "out_degree": 11,
    "plugin": null,
    "realm": "client",
    "source_id": "file:gamemode/core/derma/cl_inventory.lua",
    "subsystem": null
  },
  "node_type": "file",
  "plugin": null,
  "subsystem": null,
  "realm": "client",
  "file": "gamemode/core/derma/cl_inventory.lua",
  "degree": 12
}
```

### Text

```text
Runtime topology node: gamemode\core\derma\cl_inventory.lua
Node ID: file:gamemode/core/derma/cl_inventory.lua
Node type: file
File: gamemode/core/derma/cl_inventory.lua
Realm: client
Plugin/subsystem: unknown
Outgoing edge counts: {'contains_emitter': 2, 'contains_network_operation': 3, 'file_sends_network_message': 3, 'runs_in_realm': 3}
Incoming edge counts: {'owns_file': 1}
Selected properties: {"framework_layer": "framework", "graph_layers": ["hook", "network"], "label": "gamemode\\core\\derma\\cl_inventory.lua", "merge_conflicts": {"source_graph": ["hook", "network"]}, "path": "gamemode\\core\\derma\\cl_inventory.lua", "props": {"path": "gamemode\\core\\derma\\cl_inventory.lua"}, "realm": "client", "source": "emitter_file", "source_graph": "hook"}
Selected neighboring relationships:
- outgoing contains_emitter -> hook_emitter emit ItemPaintOver @ gamemode\core\derma\cl_inventory.lua:130
- outgoing contains_emitter -> hook_emitter emit OnCreateItemInteractionMenu @ gamemode\core\derma\cl_inventory.lua:153
- outgoing contains_network_operation -> network_operation netstream send invAct
- outgoing contains_network_operation -> network_operation netstream send invAct
- outgoing contains_network_operation -> network_operation netstream send invAct
- outgoing file_sends_network_message -> network_message invAct
- outgoing file_sends_network_message -> network_message invAct
- outgoing file_sends_network_message -> network_message invAct
- outgoing runs_in_realm -> realm client
- outgoing runs_in_realm -> realm client
- outgoing runs_in_realm -> realm client
- incoming owns_file -> plugin gamemode
```
