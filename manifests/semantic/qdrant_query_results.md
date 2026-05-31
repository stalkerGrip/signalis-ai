# Qdrant Query Results

Collection: `signalis_semantic`
Query: `inventory desync after character load`
Expanded query used: `inventory desync after character load CharacterLoaded CharacterPreSave PlayerLoadedChar PlayerLoadout PostPlayerLoadout character client UI file file_summary gridinv hook_emitter hook_event hook_listener invAct inventory inventoryOpen multichar netstream.Hook netstream.Start network_context network_message network_operation network_payload_operation plugin plugin_summary realm crossing server authoritative storage`
Top K: **10**
Retrieve K: **50**
Model: `BAAI/bge-small-en-v1.5`
Hash query: `False`

## Returned results: 10

## Result 1

- Score: **-0.0172**
- Rerank score: `0.335`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:storage:+0.05', 'text_event:playerloadout:+0.10', 'network_text_match:+0.10', 'doctrine_required:+0.16', 'file_subsystem:inventory:+0.07', 'causal:itemdatachanged:+0.18', 'causal:nutinventoryadd:+0.16', 'causal:nutinventoryremove:+0.14', 'causal_network_flow:+0.14', 'state_mutation_or_sync:+0.14', 'realm_signal:+0.04']`
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

- Score: **-0.0277**
- Rerank score: `0.30500000000000005`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:storage:+0.05', 'text_event:playerloadout:+0.10', 'network_text_match:+0.10', 'doctrine_required:+0.16', 'file_subsystem:inventory:+0.07', 'causal:setdata:+0.18', 'causal:sync:+0.10', 'causal_network_flow:+0.14', 'state_mutation_or_sync:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:3a4b169ea7c423ab`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/ai_subsystems/inventory.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:3a4b169ea7c423ab",
  "doc_type": "doctrine",
  "content_hash": "48250c64ba1ae1f2f36df192959eaa4dd313b9740f2575a3704c9e727ce97c1a",
  "embedding_dim": 384,
  "text": "# Inventory — AI Synthesis\n\n## Purpose\n\nInventory is one of the core architectural subsystems of SIGNALIS.\n\nIts primary purpose is not simply storing items.\n\nInventory acts as the central ownership, transfer, equipment, and interaction layer used by multiple gameplay systems.\n\nCurrent understanding:\n\n```text\nCharacter\n→ Inventory\n→ Item\n```\n\nand\n\n```text\nInventory\n→ Equipment Slots\n→ Vendor\n→ Storage\n→ Tying\n→ Ragdoll Loot\n→ Needs\n```\n\nInventory is therefore a dependency hub rather than an isolated feature.\n\nConfidence: High\n\n---\n\n## Architectural Layers\n\n### Layer 1 — NutScript Base Inventory\n\nProvided by:\n\n```text\nnutscript/plugins/gridinv\nnutscript/gamemode/core/libs/sh_inventory.lua\nnutscript/gamemode/core/libs/sv_inventory.lua\nnutscript/gamemode/core/meta/sh_base_inventory.lua\n```\n\nResponsibilities:\n\n* inventory creation\n* inventory dimensions\n* item placement\n* transfer operations\n* inventory rules\n* item combine\n\nThis layer provides the actual inventory implementation.\n\nConfidence: Medium\n\n---\n\n### Layer 2 — SIGNALIS Inventory Extension\n\nProvided by:\n\n```text\nsignalis/plugins/inventory\n```\n\nResponsibilities:\n\n* equipment slots\n* slot restrictions\n* slot lifecycle\n* stack split synchronization\n* inventory UI extensions\n* vendor integration\n* character equipment management\n\nThis layer extends GridInv rather than replacing it.\n\nConfidence: High\n\n---\n\n### Layer 3 — Inventory UI Layer\n\nResponsibilities:\n\n* grid rendering\n* slot rendering\n* item interaction\n* item tooltips\n* equipment visualization\n* vendor visualization\n* storage visualization\n\nImportant rendering functions:\n\n```lua\ngetName()\ngetDesc()\npaintOver()\n```\n\nInventory UI state is not necessarily authoritative inventory state.\n\nConfidence: High\n\n---\n\n## Ownership Model\n\nCurrent synthesized model:\n\n```text\nCharacter\n→ stores inv variable\n\nInventory\n→ references character\n\nItem\n→ references inventory\n\nPersistence\n→ database-backed\n```\n\nImportant references:\n\n```lua\nGM:CreateDefaultInventory(character)\nnut.char.registerVar(\"inv\", ...)\nchar:getInv()\n```\n\nInventory ownership appears to originate from the character.\n\nItems appear to be moved between inventories rather than duplicated.\n\nConfidence: Medium\n\nNeeds validation:\nExact persistence ownership chain.\n\n---\n\n## Lifecycle Model\n\nCurrent understanding:\n\n```text\nCharacter Creation\n→ CreateDefaultInventory\n\nCharacter Load\n→ CharacterLoaded\n\nPlayer Initialization\n→ PlayerLoadedChar\n\nEquipment Initialization\n→ PlayerLoadout\n\nSlot Population\n→ PostPlayerLoadout\n\nPersistence\n→ CharacterPreSave\n```\n\nHuman understanding indicates all of these occur before normal player interaction begins.\n\nThis suggests inventory synchronization problems are more likely related to delayed client initialization than early player interaction.\n\nConfidence: Medium\n\nNeeds validation:\nExact hook ordering.\n\n---\n\n## Equipment Model\n\nEquipment slots appear to be implemented as additional inventory instances.\n\nKnown slots:\n\n* Primary Item\n* Melee\n* Secondary Weapon\n* Primary Weapon\n* Armor\n* Suit\n* Face\n* Headgear\n* Eyes\n\nCurrent understanding:\n\n```text\nMain Inventory\n↔ Equipment Slot Inventory\n```\n\nItems are moved between inventories.\n\nConfidence: Medium\n\n---\n\n## Synchronization Model\n\nCurrent understanding:\n\nSynchronization is performed through:\n\n```text\nInventory Rules\ngetData()\nsetData()\nnet\nnetstream\n```\n\nInventory behavior is tightly coupled with UI behavior.\n\nCurrent knowledge gap:\n\nFull synchronization path is not yet reconstructed.\n\nConfidence: Low",
  "metadata": {
    "chunk_index": 0,
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
# Inventory — AI Synthesis

## Purpose

Inventory is one of the core architectural subsystems of SIGNALIS.

Its primary purpose is not simply storing items.

Inventory acts as the central ownership, transfer, equipment, and interaction layer used by multiple gameplay systems.

Current understanding:

```text
Character
→ Inventory
→ Item
```

and

```text
Inventory
→ Equipment Slots
→ Vendor
→ Storage
→ Tying
→ Ragdoll Loot
→ Needs
```

Inventory is therefore a dependency hub rather than an isolated feature.

Confidence: High

---

## Architectural Layers

### Layer 1 — NutScript Base Inventory

Provided by:

```text
nutscript/plugins/gridinv
nutscript/gamemode/core/libs/sh_inventory.lua
nutscript/gamemode/core/libs/sv_inventory.lua
nutscript/gamemode/core/meta/sh_base_inventory.lua
```

Responsibilities:

* inventory creation
* inventory dimensions
* item placement
* transfer operations
* inventory rules
* item combine

This layer provides the actual inventory implementation.

Confidence: Medium

---

### Layer 2 — SIGNALIS Inventory Extension

Provided by:

```text
signalis/plugins/inventory
```

Responsibilities:

* equipment slots
* slot restrictions
* slot lifecycle
* stack split synchronization
* inventory UI extensions
* vendor integration
* character equipment management

This layer extends GridInv rather than replacing it.

Confidence: High

---

### Layer 3 — Inventory UI Layer

Responsibilities:

* grid rendering
* slot rendering
* item interaction
* item tooltips
* equipment visualization
* vendor visualization
* storage visualization

Important rendering functions:

```lua
getName()
getDesc()
paintOver()
```

Inventory UI state is not necessarily authoritative inventory state.

Confidence: High

---

## Ownership Model

Current synthesized model:

```text
Ch...
```

## Result 3

- Score: **-0.0395**
- Rerank score: `0.257`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:character:+0.05', 'text_event:playerloadedchar:+0.10', 'network_text_match:+0.10', 'doctrine_required:+0.16', 'file_subsystem:multichar:+0.07', 'causal:sync:+0.10', 'causal_network_flow:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:7d9b2c7ce13ae06b`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/subsystems/multichar.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:7d9b2c7ce13ae06b",
  "doc_type": "doctrine",
  "content_hash": "5ab5aeeff3566fe0061098eaba2ffee84625809b66d1182b40bf0b86832160c1",
  "embedding_dim": 384,
  "text": "# Subsystem: multichar\n\n## Purpose\n\nDeterministic subsystem summary generated from runtime topology.\n\n## Topology Summary\n\n- Nodes: **204**\n- Edges: **5541**\n\n## Node Types\n\n- `hook_listener`: 69\n- `hook_event`: 24\n- `hook_emitter`: 23\n- `network_payload_operation`: 20\n- `network_operation`: 17\n- `network_context`: 12\n- `timer_operation`: 11\n- `file`: 11\n- `network_message`: 5\n- `timer`: 3\n- `timer_class`: 3\n- `realm`: 3\n- `subsystem`: 1\n- `plugin`: 1\n- `timer_risk`: 1\n\n## Edge Types\n\n- `runs_in_realm`: 4470\n- `classified_as`: 192\n- `references_timer`: 139\n- `schedules_delay`: 132\n- `dispatches_to`: 85\n- `listens_to`: 81\n- `contains_listener`: 69\n- `registers_listener`: 69\n- `listens_to_event`: 47\n- `emits`: 27\n- `contains_emitter`: 23\n- `contains_network_payload_operation`: 20\n- `owns_file`: 18\n- `contains_network_operation`: 17\n- `belongs_to_subsystem`: 16\n- `emits_event`: 15\n- `contains_network_context`: 12\n- `context_references_network_message`: 12\n- `contains_timer_operation`: 11\n- `owns_timer_operation`: 11\n\n## Major Hooks\n\n- `listen PlayerLoadedChar @ plugins\\spawnsaver.lua:18`: 2\n- `listen ConfigureCharacterCreationSteps @ plugins\\traits\\sh_creation.lua:403`: 2\n- `listen createCharacter @ plugins\\multichar\\sh_plugin.lua:55`: 2\n- `listen syncCharList @ plugins\\multichar\\sh_plugin.lua:8`: 2\n- `listen PlayerNutDataLoaded @ plugins\\multichar\\sv_hooks.lua:1`: 2\n- `listen chooseCharacter @ plugins\\multichar\\sh_plugin.lua:34`: 2\n- `listen PlayerLoadedChar @ plugins\\ammosave.lua:63`: 2\n- `listen deleteCharacter @ plugins\\multichar\\sh_plugin.lua:98`: 2\n- `NutScriptLoaded`: 1\n- `AdjustCreationData`: 1\n- `listen OnCharCreated @ schema\\hooks\\sv_hooks.lua:88`: 1\n- `ShouldMenuButtonShow`: 1\n- `listen OnCharCreated @ plugins\\logging.lua:155`: 1\n- `listen LoadFonts @ plugins\\multichar\\plugins\\charselect\\sh_plugin.lua:46`: 1\n- `listen PlayerLoadedChar @ plugins\\multichar\\sv_hooks.lua:48`: 1\n- `ConfigureCharacterCreationSteps`: 1\n- `emit NutScriptLoaded @ gamemode\\core\\hooks\\cl_hooks.lua:365`: 1\n- `nutCharDeleted`: 1\n- `listen CharacterLoaded @ schema\\hooks\\cl_hooks.lua:121`: 1\n- `PlayerLoadedChar`: 1\n\n## Major Network Signals\n\n- `receive nutCharChoose`: 2\n- `Receive nutCharCreate`: 2\n- `receive nutCharCreate`: 2\n- `Receive nutCharChoose`: 2\n- `send nutCharChoose`: 2\n- `Start nutCharCreate`: 2\n- `Start nutCharChoose`: 2\n- `send nutCharCreate`: 2\n- `send nutCharDelete`: 1\n- `Start nutCharDelete`: 1\n- `Receive nutCharList`: 1\n- `register nutCharDelete`: 1\n- `receive nutCharList`: 1\n- `register nutCharList`: 1\n- `register nutCharChoose`: 1\n- `register nutCharCreate`: 1\n- `nutCharList`: 1\n- `nutCharChoose`: 1\n- `send nutCharList`: 1\n- `Receive nutCharDelete`: 1\n\n## Lifecycle Propagation",
  "metadata": {
    "chunk_index": 0,
    "file": "docs/subsystems/multichar.md",
    "node_type": "doctrine",
    "source_id": "docs/subsystems/multichar.md"
  },
  "node_type": "doctrine",
  "file": "docs/subsystems/multichar.md"
}
```

### Text

```text
# Subsystem: multichar

## Purpose

Deterministic subsystem summary generated from runtime topology.

## Topology Summary

- Nodes: **204**
- Edges: **5541**

## Node Types

- `hook_listener`: 69
- `hook_event`: 24
- `hook_emitter`: 23
- `network_payload_operation`: 20
- `network_operation`: 17
- `network_context`: 12
- `timer_operation`: 11
- `file`: 11
- `network_message`: 5
- `timer`: 3
- `timer_class`: 3
- `realm`: 3
- `subsystem`: 1
- `plugin`: 1
- `timer_risk`: 1

## Edge Types

- `runs_in_realm`: 4470
- `classified_as`: 192
- `references_timer`: 139
- `schedules_delay`: 132
- `dispatches_to`: 85
- `listens_to`: 81
- `contains_listener`: 69
- `registers_listener`: 69
- `listens_to_event`: 47
- `emits`: 27
- `contains_emitter`: 23
- `contains_network_payload_operation`: 20
- `owns_file`: 18
- `contains_network_operation`: 17
- `belongs_to_subsystem`: 16
- `emits_event`: 15
- `contains_network_context`: 12
- `context_references_network_message`: 12
- `contains_timer_operation`: 11
- `owns_timer_operation`: 11

## Major Hooks

- `listen PlayerLoadedChar @ plugins\spawnsaver.lua:18`: 2
- `listen ConfigureCharacterCreationSteps @ plugins\traits\sh_creation.lua:403`: 2
- `listen createCharacter @ plugins\multichar\sh_plugin.lua:55`: 2
- `listen syncCharList @ plugins\multichar\sh_plugin.lua:8`: 2
- `listen PlayerNutDataLoaded @ plugins\multichar\sv_hooks.lua:1`: 2
- `listen chooseCharacter @ plugins\multichar\sh_plugin.lua:34`: 2
- `listen PlayerLoadedChar @ plugins\ammosave.lua:63`: 2
- `listen deleteCharacter @ plugins\multichar\sh_plugin.lua:98`: 2
- `NutScriptLoaded`: 1
- `AdjustCreationData`: 1
- `listen OnCharCreated @ schema\hooks\sv_hooks.lua:88`: 1
- `ShouldMenuButtonShow`: 1
- `listen OnCharCreated @ plugins\logging.lua:155`: 1
- `listen LoadFonts @ plugins\mu...
```

## Result 4

- Score: **-0.0449**
- Rerank score: `0.23950000000000002`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:storage:+0.05', 'text_event:characterpresave:+0.10', 'network_text_match:+0.10', 'doctrine_required:+0.16', 'causal:sync:+0.10', 'causal_network_flow:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:7194ee3324987855`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/subsystems/needs.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:7194ee3324987855",
  "doc_type": "doctrine",
  "content_hash": "5c2b2395d4e8a7cc0e9c68e53f24732e20982b76d90038efb543f1995231d7f2",
  "embedding_dim": 384,
  "text": "TurnOn`: 1\n- `cookingpotPourOut`: 1\n- `cookingboardCut`: 1\n- `netstream send cookingpotPickUp`: 1\n- `netstream hook waterfaucetDrinkWater`: 1\n- `cookingovenTakeFood`: 1\n- `cookingpotTakeOff`: 1\n- `netstream send cookingpotGetCompositionServer`: 1\n- `waterfaucetDrawWater`: 1\n\n## Lifecycle Propagation\n\n- `emit SaveData @ gamemode\\core\\sv_data.lua:95`: 1\n- `CharacterPreSave`: 1\n- `emit SaveData @ gamemode\\core\\hooks\\sv_hooks.lua:652`: 1\n- `emit LoadData @ gamemode\\core\\hooks\\sv_hooks.lua:737`: 1\n- `emit LoadData @ gamemode\\core\\hooks\\sv_hooks.lua:641`: 1\n- `LoadData`: 1\n- `listen SaveData @ plugins\\needs\\sv_hooks.lua:146`: 1\n- `listen CharacterPreSave @ plugins\\needs\\sv_hooks.lua:119`: 1\n- `emit CharacterPreSave @ gamemode\\core\\meta\\sh_character.lua:42`: 1\n- `listen LoadData @ plugins\\needs\\sv_hooks.lua:218`: 1\n- `SaveData`: 1\n- `listen CharacterPreSave @ plugins\\needs\\sv_hooks.lua:120`: 1\n- `emit SaveData @ gamemode\\core\\hooks\\sv_hooks.lua:731`: 1\n- `listen SaveData @ plugins\\needs\\sv_hooks.lua:145`: 1\n- `listen LoadData @ plugins\\needs\\sv_hooks.lua:217`: 1\n\n## Synchronization Hotspots\n\n- `receive nutStorageOpen`: 1\n- `send nutStorageOpen`: 1\n- `nutStorageOpen`: 1\n- `Start nutStorageOpen`: 1\n- `write WriteEntity nutStorageOpen`: 1\n\n## Important Timers\n\n- `high_frequency_infinite_timer`: 2\n- `entity_timer_or_action_call@plugins\\needs\\entities\\entities\\nut_cooking_base.lua:540`: 2\n- `entity_timer_or_action_call@plugins\\needs\\entities\\entities\\nut_cooking_base.lua:393`: 2\n- `entity_timer_or_action_call@plugins\\needs\\entities\\entities\\nut_cooking_kettle\\init.lua:109`: 2\n- `player_action_timer@plugins\\needs\\entities\\entities\\nut_cooking_board\\init.lua:113`: 1\n- `RemoveTimer`: 1\n- `timer_create@plugins\\needs\\sv_hooks.lua:9`: 1\n- `entity_timer_or_action_call@plugins\\needs\\entities\\entities\\nut_cooking_oven\\init.lua:162`: 1\n- `setCancelAction`: 1\n- `next_tick_delay`: 1\n- `timer_remove@plugins\\needs\\derma\\cl_cookingboard_interface.lua:112`: 1\n- `entity_timer_create@plugins\\needs\\entities\\entities\\nut_cooking_base.lua:39`: 1\n- `player_cancelable_action_timer@plugins\\needs\\entities\\entities\\nut_waterfaucet\\init.lua:127`: 1\n- `entity_timer_or_action_call@plugins\\needs\\entities\\entities\\nut_cooking_oven\\init.lua:34`: 1\n- `entity_timer_remove@plugins\\needs\\entities\\entities\\nut_cooking_base.lua:540`: 1\n- `entity_timer_exists@plugins\\needs\\sv_hooks.lua:165`: 1\n- `entity_timer_create@plugins\\needs\\entities\\entities\\nut_cooking_kettle\\init.lua:113`: 1\n- `entity_timer_or_action_call@plugins\\needs\\entities\\entities\\nut_cooking_base.lua:47`: 1\n- `entity_timer_or_action_call@plugins\\needs\\entities\\entities\\nut_cooking_base.lua:39`: 1\n- `next_tick_or_subframe_delay`: 1\n\n## Realms\n\n- `server`: 50\n- `shared`: 33\n- `client`: 31\n\n## Major Files",
  "metadata": {
    "chunk_index": 1,
    "file": "docs/subsystems/needs.md",
    "node_type": "doctrine",
    "source_id": "docs/subsystems/needs.md"
  },
  "node_type": "doctrine",
  "file": "docs/subsystems/needs.md"
}
```

### Text

```text
TurnOn`: 1
- `cookingpotPourOut`: 1
- `cookingboardCut`: 1
- `netstream send cookingpotPickUp`: 1
- `netstream hook waterfaucetDrinkWater`: 1
- `cookingovenTakeFood`: 1
- `cookingpotTakeOff`: 1
- `netstream send cookingpotGetCompositionServer`: 1
- `waterfaucetDrawWater`: 1

## Lifecycle Propagation

- `emit SaveData @ gamemode\core\sv_data.lua:95`: 1
- `CharacterPreSave`: 1
- `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652`: 1
- `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737`: 1
- `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641`: 1
- `LoadData`: 1
- `listen SaveData @ plugins\needs\sv_hooks.lua:146`: 1
- `listen CharacterPreSave @ plugins\needs\sv_hooks.lua:119`: 1
- `emit CharacterPreSave @ gamemode\core\meta\sh_character.lua:42`: 1
- `listen LoadData @ plugins\needs\sv_hooks.lua:218`: 1
- `SaveData`: 1
- `listen CharacterPreSave @ plugins\needs\sv_hooks.lua:120`: 1
- `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:731`: 1
- `listen SaveData @ plugins\needs\sv_hooks.lua:145`: 1
- `listen LoadData @ plugins\needs\sv_hooks.lua:217`: 1

## Synchronization Hotspots

- `receive nutStorageOpen`: 1
- `send nutStorageOpen`: 1
- `nutStorageOpen`: 1
- `Start nutStorageOpen`: 1
- `write WriteEntity nutStorageOpen`: 1

## Important Timers

- `high_frequency_infinite_timer`: 2
- `entity_timer_or_action_call@plugins\needs\entities\entities\nut_cooking_base.lua:540`: 2
- `entity_timer_or_action_call@plugins\needs\entities\entities\nut_cooking_base.lua:393`: 2
- `entity_timer_or_action_call@plugins\needs\entities\entities\nut_cooking_kettle\init.lua:109`: 2
- `player_action_timer@plugins\needs\entities\entities\nut_cooking_board\init.lua:113`: 1
- `RemoveTimer`: 1
- `timer_create@plugins\needs\sv_hooks.lua:9`: 1
- `entity_timer_or_action_call@plugins\needs\entiti...
```

## Result 5

- Score: **-0.0390**
- Rerank score: `0.232`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:storage:+0.05', 'network_text_match:+0.10', 'doctrine_required:+0.16', 'file_subsystem:gridinv:+0.07', 'causal:sync:+0.10', 'causal_network_flow:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:75274fbbe44913ae`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/subsystems/gridinv.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:75274fbbe44913ae",
  "doc_type": "doctrine",
  "content_hash": "5edd85feab6559014e2a6313847ee5912afd0755cd48420e51aa94e584a80012",
  "embedding_dim": 384,
  "text": "# Subsystem: gridinv\n\n## Purpose\n\nDeterministic subsystem summary generated from runtime topology.\n\n## Topology Summary\n\n- Nodes: **162**\n- Edges: **5357**\n\n## Node Types\n\n- `hook_listener`: 53\n- `hook_event`: 31\n- `hook_emitter`: 20\n- `network_payload_operation`: 16\n- `network_operation`: 13\n- `file`: 11\n- `network_message`: 6\n- `network_context`: 4\n- `realm`: 3\n- `plugin`: 1\n- `timer_class`: 1\n- `timer_operation`: 1\n- `timer`: 1\n- `subsystem`: 1\n\n## Edge Types\n\n- `runs_in_realm`: 4470\n- `classified_as`: 142\n- `references_timer`: 132\n- `schedules_delay`: 132\n- `listens_to`: 65\n- `dispatches_to`: 58\n- `contains_listener`: 53\n- `registers_listener`: 53\n- `listens_to_event`: 35\n- `emits`: 28\n- `contains_emitter`: 20\n- `emits_event`: 20\n- `owns_file`: 17\n- `contains_network_payload_operation`: 16\n- `file_sends_network_message`: 16\n- `network_dispatches_to`: 16\n- `sends_network_message`: 16\n- `contains_network_operation`: 13\n- `writes_network_payload`: 12\n- `belongs_to_subsystem`: 9\n\n## Major Hooks\n\n- `listen CanItemBeTransfered @ plugins\\ragdollinteraction\\interaction\\sv_hooks.lua:92`: 2\n- `listen CreateInventoryPanel @ plugins\\gridinv\\plugins\\gridinvui\\sh_plugin.lua:8`: 2\n- `listen NutScriptTablesLoaded @ plugins\\gridinv\\plugins\\1_1compat\\sh_plugin.lua:8`: 2\n- `listen ItemDraggedOutOfInventory @ plugins\\gridinv\\sh_plugin.lua:33`: 2\n- `listen StorageOpen @ plugins\\gridinv\\plugins\\gridstorage\\sh_plugin.lua:153`: 2\n- `listen ItemCombine @ plugins\\gridinv\\sh_plugin.lua:18`: 2\n- `emit NutScriptTablesLoaded @ gamemode\\core\\libs\\sv_database.lua:519`: 1\n- `listen addInventoryData @ plugins\\gridinv\\plugins\\1_1compat\\sv_migrations.lua:24`: 1\n- `emit CanItemBeTransfered @ plugins\\gridinv\\sv_transfer.lua:18`: 1\n- `listen HandleItemTransferRequest @ plugins\\gridinv\\sv_transfer.lua:4`: 1\n- `listen deleteCharID @ plugins\\gridinv\\plugins\\1_1compat\\sv_migrations.lua:66`: 1\n- `print`: 1\n- `listen getMigrationFilter @ plugins\\gridinv\\plugins\\1_1compat\\sv_migrations.lua:14`: 1\n- `emit StorageOpen @ plugins\\storage\\cl_networking.lua:8`: 1\n- `emit SetupBagInventoryAccessRules @ plugins\\gridinv\\items\\base\\sh_bags.lua:60`: 1\n- `HandleItemTransferRequest`: 1\n- `listen getMigrationFilter @ plugins\\gridinv\\plugins\\1_1compat\\sv_migrations.lua:13`: 1\n- `NutScriptTablesLoaded`: 1\n- `listen CheckPassword @ plugins\\gridinv\\plugins\\1_1compat\\sh_plugin.lua:27`: 1\n- `emit HandleItemTransferRequest @ plugins\\gridinv\\sv_transfer.lua:236`: 1\n\n## Major Network Signals\n\n- `Start nutTransferItem`: 2\n- `send nutTransferItem`: 2\n- `nutTransferItem`: 1\n- `receive nutTransferItem`: 1\n- `invMv`: 1\n- `Receive nutTransferItem`: 1\n- `nutInventoryDelete`: 1\n- `netstream hook storageLockTrashcan`: 1\n- `netstream send itemSplitTake`: 1\n- `netstream send storageLockTrashcan`: 1\n- `itemSplitTake`: 1\n- `inventorySetPanelStatus`: 1\n- `netstream send inventorySetPanelStatus`: 1\n- `send nutInventoryDelete`: 1\n- `Start nutInventoryDelete`: 1\n- `receive nutInventoryDelete`: 1\n- `netstream hook inventorySetPanelStatus`: 1\n- `netstream hook itemSplitTake`: 1\n- `storageLockTrashcan`: 1\n- `register nutTransferItem`: 1\n\n## Lifecycle Propagation\n\n- none detected\n\n## Synchronization Hotspots",
  "metadata": {
    "chunk_index": 0,
    "file": "docs/subsystems/gridinv.md",
    "node_type": "doctrine",
    "source_id": "docs/subsystems/gridinv.md"
  },
  "node_type": "doctrine",
  "file": "docs/subsystems/gridinv.md"
}
```

### Text

```text
# Subsystem: gridinv

## Purpose

Deterministic subsystem summary generated from runtime topology.

## Topology Summary

- Nodes: **162**
- Edges: **5357**

## Node Types

- `hook_listener`: 53
- `hook_event`: 31
- `hook_emitter`: 20
- `network_payload_operation`: 16
- `network_operation`: 13
- `file`: 11
- `network_message`: 6
- `network_context`: 4
- `realm`: 3
- `plugin`: 1
- `timer_class`: 1
- `timer_operation`: 1
- `timer`: 1
- `subsystem`: 1

## Edge Types

- `runs_in_realm`: 4470
- `classified_as`: 142
- `references_timer`: 132
- `schedules_delay`: 132
- `listens_to`: 65
- `dispatches_to`: 58
- `contains_listener`: 53
- `registers_listener`: 53
- `listens_to_event`: 35
- `emits`: 28
- `contains_emitter`: 20
- `emits_event`: 20
- `owns_file`: 17
- `contains_network_payload_operation`: 16
- `file_sends_network_message`: 16
- `network_dispatches_to`: 16
- `sends_network_message`: 16
- `contains_network_operation`: 13
- `writes_network_payload`: 12
- `belongs_to_subsystem`: 9

## Major Hooks

- `listen CanItemBeTransfered @ plugins\ragdollinteraction\interaction\sv_hooks.lua:92`: 2
- `listen CreateInventoryPanel @ plugins\gridinv\plugins\gridinvui\sh_plugin.lua:8`: 2
- `listen NutScriptTablesLoaded @ plugins\gridinv\plugins\1_1compat\sh_plugin.lua:8`: 2
- `listen ItemDraggedOutOfInventory @ plugins\gridinv\sh_plugin.lua:33`: 2
- `listen StorageOpen @ plugins\gridinv\plugins\gridstorage\sh_plugin.lua:153`: 2
- `listen ItemCombine @ plugins\gridinv\sh_plugin.lua:18`: 2
- `emit NutScriptTablesLoaded @ gamemode\core\libs\sv_database.lua:519`: 1
- `listen addInventoryData @ plugins\gridinv\plugins\1_1compat\sv_migrations.lua:24`: 1
- `emit CanItemBeTransfered @ plugins\gridinv\sv_transfer.lua:18`: 1
- `listen HandleItemTransferRequest @ plugins\gridinv\sv_transfer.lua:4`:...
```

## Result 6

- Score: **-0.0120**
- Rerank score: `0.2185`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:storage:+0.05', 'text_event:characterloaded:+0.10', 'network_text_match:+0.10', 'doctrine_required:+0.16', 'causal:sync:+0.10', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:a55aa39858a02df4`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/source_index.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:a55aa39858a02df4",
  "doc_type": "doctrine",
  "content_hash": "11e633e1293582f667aa6667efddb0de7dd466b4764de5fc509ac92f80c3bcbf",
  "embedding_dim": 384,
  "text": "# SIGNALIS AI — Source Index\n\nThis file maps durable project artifacts by authority and intended use.\n\n## Canonical Doctrine\n\nThese files define reusable semantic rules and architecture interpretation.\n\n```text\ndocs/project_memory.md\nsubsystem_docs/runtime_doctrine.md\nsubsystem_docs/event_taxonomy.md\nsubsystem_docs/networking_model.md\nsubsystem_docs/persistence_model.md\nsubsystem_docs/realm_model.md\nsubsystem_docs/subsystem_priorities.md\nsubsystem_docs/qdrant_plan.md\n```\n\nUse for:\n\n- project bootstrap\n- ChatGPT Project Sources\n- Qdrant doctrine documents\n- architecture reasoning constraints\n\n## Runtime Topology\n\nCanonical generated topology artifacts:\n\n```text\nmanifests/normalized/runtime_topology.json\nmanifests/normalized/runtime_topology_nodes.json\nmanifests/normalized/runtime_topology_edges.json\nmanifests/normalized/runtime_topology_summary.md\n```\n\nUse summary files for ChatGPT/Gemini.\n\nUse full JSON files for scripts and Qdrant document generation.\n\nDo not paste full topology JSON into chat by default.\n\n## Semantic Retrieval Corpus\n\nQdrant input and output artifacts:\n\n```text\nmanifests/semantic/qdrant_documents.jsonl\nmanifests/semantic/qdrant_documents_summary.md\nmanifests/semantic/qdrant_embeddings.jsonl\nmanifests/semantic/qdrant_embedding_summary.md\nmanifests/semantic/qdrant_ingest_summary.md\n```\n\nUse for:\n\n- Qdrant ingestion\n- retrieval evaluation\n- context pack generation\n\nDo not treat embeddings as source of truth.\n\n## Subsystem Documents\n\nMachine-generated subsystem summaries:\n\n```text\ndocs/subsystems/inventory.md\ndocs/subsystems/gridinv.md\ndocs/subsystems/storage.md\ndocs/subsystems/vendor.md\ndocs/subsystems/multichar.md\ndocs/subsystems/healthproblems.md\ndocs/subsystems/needs.md\ndocs/subsystems/biorezonance.md\ndocs/subsystems/lightitems.md\ndocs/subsystems/mining.md\ndocs/subsystems/nextbots.md\ndocs/subsystems/ragdollinteraction.md\n```\n\nUse for:\n\n- subsystem-level retrieval anchors\n- architecture reasoning\n- investigation scoping\n- ChatGPT Project Sources for priority systems\n\nThese are topology-derived and may need exact Lua validation for behavior claims.\n\n## Human Subsystem Notes\n\nHuman-authored or human-confirmed subsystem facts:\n\n```text\ndocs/human_subsystems/\n```\n\nUse for:\n\n- intended behavior\n- legacy-vs-authoritative notes\n- confirmed bugs\n- reproduction observations\n- system ownership notes\n\nHuman-confirmed facts outrank AI synthesis.\n\n## AI Synthesis Documents\n\nAI-generated architecture synthesis:\n\n```text\ndocs/ai_subsystems/\n```\n\nUse for:\n\n- architecture interpretation\n- refactor proposals\n- subsystem contracts\n- investigation summaries\n\nThese are not authoritative unless grounded in topology, doctrine, source code, or human validation.\n\n## Investigations\n\nCase-specific reports:\n\n```text\ninvestigations/\n```\n\nKnown active investigation files:\n\n```text\ninvestigations/inventory_desync_context_pack.md\ninvestigations/inventory_desync_phase1.md\ninvestigations/paths_characterloaded_to_inventory_panel_status.md\ninvestigations/paths_v2_characterloaded_to_inventory_panel_status.md\n```\n\nUse for:\n\n- bug-focused reasoning\n- context packs\n- path reconstruction\n- validation plans\n\nPromote durable findings from investigations into doctrine, subsystem docs, or human context.\n\n## Scripts\n\nImportant script groups:\n\n```text\nscripts/extraction/\nscripts/normalization/\nscripts/graphs/\nscripts/qdrant/\nscripts/semantic/\nscripts/profiling/\nscripts/diagnostics/\n```\n\nQdrant scripts:",
  "metadata": {
    "chunk_index": 0,
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
# SIGNALIS AI — Source Index

This file maps durable project artifacts by authority and intended use.

## Canonical Doctrine

These files define reusable semantic rules and architecture interpretation.

```text
docs/project_memory.md
subsystem_docs/runtime_doctrine.md
subsystem_docs/event_taxonomy.md
subsystem_docs/networking_model.md
subsystem_docs/persistence_model.md
subsystem_docs/realm_model.md
subsystem_docs/subsystem_priorities.md
subsystem_docs/qdrant_plan.md
```

Use for:

- project bootstrap
- ChatGPT Project Sources
- Qdrant doctrine documents
- architecture reasoning constraints

## Runtime Topology

Canonical generated topology artifacts:

```text
manifests/normalized/runtime_topology.json
manifests/normalized/runtime_topology_nodes.json
manifests/normalized/runtime_topology_edges.json
manifests/normalized/runtime_topology_summary.md
```

Use summary files for ChatGPT/Gemini.

Use full JSON files for scripts and Qdrant document generation.

Do not paste full topology JSON into chat by default.

## Semantic Retrieval Corpus

Qdrant input and output artifacts:

```text
manifests/semantic/qdrant_documents.jsonl
manifests/semantic/qdrant_documents_summary.md
manifests/semantic/qdrant_embeddings.jsonl
manifests/semantic/qdrant_embedding_summary.md
manifests/semantic/qdrant_ingest_summary.md
```

Use for:

- Qdrant ingestion
- retrieval evaluation
- context pack generation

Do not treat embeddings as source of truth.

## Subsystem Documents

Machine-generated subsystem summaries:

```text
docs/subsystems/inventory.md
docs/subsystems/gridinv.md
docs/subsystems/storage.md
docs/subsystems/vendor.md
docs/subsystems/multichar.md
docs/subsystems/healthproblems.md
docs/subsystems/needs.md
docs/subsystems/biorezonance.md
docs/subsystems/lightitems.md
docs/subsystems/mini...
```

## Result 7

- Score: **-0.0348**
- Rerank score: `0.217`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:storage:+0.05', 'network_text_match:+0.10', 'doctrine_required:+0.16', 'file_subsystem:storage:+0.07', 'causal_network_flow:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:53d0af6ef466806c`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/subsystems/storage.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:53d0af6ef466806c",
  "doc_type": "doctrine",
  "content_hash": "63935425dbad39f4a4886befe1b983392eaea51ebb447f71af8db51abc9f4fcc",
  "embedding_dim": 384,
  "text": "# Subsystem: storage\n\n## Purpose\n\nDeterministic subsystem summary generated from runtime topology.\n\n## Topology Summary\n\n- Nodes: **240**\n- Edges: **6960**\n\n## Node Types\n\n- `network_operation`: 49\n- `hook_emitter`: 38\n- `hook_listener`: 36\n- `file`: 23\n- `hook_event`: 22\n- `network_message`: 15\n- `network_context`: 14\n- `network_payload_operation`: 12\n- `plugin`: 11\n- `timer_operation`: 9\n- `event_class`: 3\n- `realm`: 3\n- `timer_class`: 2\n- `timer`: 2\n- `subsystem`: 1\n\n## Edge Types\n\n- `runs_in_realm`: 4470\n- `classified_as`: 421\n- `dispatches_to`: 300\n- `registers_listener`: 216\n- `references_timer`: 171\n- `listens_to_event`: 143\n- `schedules_delay`: 132\n- `owns_file`: 127\n- `listens_to`: 121\n- `owns_timer_operation`: 112\n- `contains_network_operation`: 91\n- `emits_event`: 80\n- `contains_timer_operation`: 73\n- `file_sends_network_message`: 70\n- `emits`: 69\n- `contains_listener`: 61\n- `sends_network_message`: 57\n- `contains_emitter`: 40\n- `network_dispatches_to`: 40\n- `schedules_player_action`: 38\n\n## Major Hooks\n\n- `listen PlayerSpawnedProp @ plugins\\storage\\sv_storage.lua:3`: 2\n- `listen StorageOpen @ plugins\\_disabled\\simpleinv\\plugins\\liststorage\\sh_plugin.lua:16`: 2\n- `listen transferItem @ plugins\\storage\\sh_plugin.lua:23`: 2\n- `listen StorageOpen @ plugins\\gridinv\\plugins\\gridstorage\\sh_plugin.lua:153`: 2\n- `listen StorageUnlockPrompt @ plugins\\storage\\cl_password.lua:1`: 2\n- `emit StorageEntityRemoved @ plugins\\mining\\entities\\entities\\nut_ore_smelter\\init.lua:474`: 1\n- `PlayerSpawnedProp`: 1\n- `emit SaveData @ gamemode\\core\\sv_data.lua:95`: 1\n- `listen StorageItemRemoved @ plugins\\storage\\sv_storage.lua:77`: 1\n- `saveStorage`: 1\n- `listen exitStorage @ plugins\\storage\\cl_networking.lua:10`: 1\n- `emit StorageOpen @ plugins\\storage\\cl_networking.lua:8`: 1\n- `emit StorageEntityRemoved @ plugins\\vendor\\entities\\entities\\nut_vendor\\init.lua:278`: 1\n- `StorageRestored`: 1\n- `emit saveStorage @ plugins\\storage\\entities\\entities\\nut_storage\\init.lua:190`: 1\n- `listen CanPlayerSpawnStorage @ plugins\\storage\\sv_storage.lua:45`: 1\n- `emit SaveData @ gamemode\\core\\hooks\\sv_hooks.lua:652`: 1\n- `emit StorageItemRemoved @ plugins\\cassetteplayer\\entities\\entities\\nut_cassetteplayer.lua:158`: 1\n- `listen CreateUsingInterface @ plugins\\gadgets\\cl_hooks.lua:2`: 1\n- `transferItem`: 1\n\n## Major Network Signals\n\n- `netstream send entFreezeState`: 8\n- `Start nutStorageOpen`: 5\n- `send nutStorageOpen`: 5\n- `netstream send storageCleanTrash`: 2\n- `Start nutStorageUnlock`: 2\n- `Receive nutStorageUnlock`: 2\n- `receive nutStorageUnlock`: 2\n- `netstream send storageTakeOffLock`: 2\n- `send nutStorageUnlock`: 2\n- `netstream send storageInventory`: 2\n- `netstream hook storageOpen`: 1\n- `Start nutStorageExit`: 1\n- `netstream hook entFreezeState`: 1\n- `netstream send storageOpen`: 1\n- `Receive nutStorageTransfer`: 1\n- `nutStorageUnlock`: 1\n- `netstream send storageNewDesc`: 1\n- `receive nutStorageOpen`: 1\n- `netstream hook storageTakeOffLock`: 1\n- `storageNewDesc`: 1\n\n## Lifecycle Propagation",
  "metadata": {
    "chunk_index": 0,
    "file": "docs/subsystems/storage.md",
    "node_type": "doctrine",
    "source_id": "docs/subsystems/storage.md"
  },
  "node_type": "doctrine",
  "file": "docs/subsystems/storage.md"
}
```

### Text

```text
# Subsystem: storage

## Purpose

Deterministic subsystem summary generated from runtime topology.

## Topology Summary

- Nodes: **240**
- Edges: **6960**

## Node Types

- `network_operation`: 49
- `hook_emitter`: 38
- `hook_listener`: 36
- `file`: 23
- `hook_event`: 22
- `network_message`: 15
- `network_context`: 14
- `network_payload_operation`: 12
- `plugin`: 11
- `timer_operation`: 9
- `event_class`: 3
- `realm`: 3
- `timer_class`: 2
- `timer`: 2
- `subsystem`: 1

## Edge Types

- `runs_in_realm`: 4470
- `classified_as`: 421
- `dispatches_to`: 300
- `registers_listener`: 216
- `references_timer`: 171
- `listens_to_event`: 143
- `schedules_delay`: 132
- `owns_file`: 127
- `listens_to`: 121
- `owns_timer_operation`: 112
- `contains_network_operation`: 91
- `emits_event`: 80
- `contains_timer_operation`: 73
- `file_sends_network_message`: 70
- `emits`: 69
- `contains_listener`: 61
- `sends_network_message`: 57
- `contains_emitter`: 40
- `network_dispatches_to`: 40
- `schedules_player_action`: 38

## Major Hooks

- `listen PlayerSpawnedProp @ plugins\storage\sv_storage.lua:3`: 2
- `listen StorageOpen @ plugins\_disabled\simpleinv\plugins\liststorage\sh_plugin.lua:16`: 2
- `listen transferItem @ plugins\storage\sh_plugin.lua:23`: 2
- `listen StorageOpen @ plugins\gridinv\plugins\gridstorage\sh_plugin.lua:153`: 2
- `listen StorageUnlockPrompt @ plugins\storage\cl_password.lua:1`: 2
- `emit StorageEntityRemoved @ plugins\mining\entities\entities\nut_ore_smelter\init.lua:474`: 1
- `PlayerSpawnedProp`: 1
- `emit SaveData @ gamemode\core\sv_data.lua:95`: 1
- `listen StorageItemRemoved @ plugins\storage\sv_storage.lua:77`: 1
- `saveStorage`: 1
- `listen exitStorage @ plugins\storage\cl_networking.lua:10`: 1
- `emit StorageOpen @ plugins\storage\cl_networking.lua:8`: 1
- `emi...
```

## Result 8

- Score: **-0.0067**
- Rerank score: `0.21450000000000002`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:storage:+0.05', 'network_text_match:+0.10', 'doctrine_required:+0.16', 'causal:sync:+0.10', 'causal_network_flow:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:9fecbfcfc9d8d544`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `subsystem_docs/qdrant_plan.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:9fecbfcfc9d8d544",
  "doc_type": "doctrine",
  "content_hash": "c509ed0f67fb3b2bc314b88e591a60219b28cd55e8c3d46c611b7fae0f363d3e",
  "embedding_dim": 384,
  "text": "# SIGNALIS AI — Qdrant Plan\n\n## Purpose\n\nQdrant will provide semantic retrieval over the SIGNALIS AI runtime topology and doctrine.\n\nIt should NOT replace deterministic extraction or normalization.\n\nIt should provide:\n\n```text\narchitecture memory\nsemantic search\nsubsystem retrieval\ntopology-aware context assembly\n```\n\nfor ChatGPT, Gemini, and local tools.\n\n---\n\n## Embedding Model\n\nPreferred embedding model:\n\n```text\nBAAI/bge-small-en-v1.5\n```\n\nReason:\n\n```text\ngood for technical text\ngood for code-adjacent semantics\ngood for architecture summaries\nlocal-friendly\n```\n\n---\n\n## Primary Collection Content\n\nPrimary retrieval layer should store semantic artifacts, not raw Lua first.\n\nStore:\n\n```text\nruntime topology nodes\nruntime topology edge summaries\nplugin topology summaries\nfile topology summaries\ndoctrine documents\nevent taxonomy\nnetworking model\npersistence model\nrealm model\nsubsystem summaries\n```\n\nRaw Lua should be a secondary retrieval layer for exact implementation checks.\n\n---\n\n## Current Semantic Corpus\n\nAlready generated:\n\n```text\nmanifests/semantic/qdrant_documents.jsonl\nmanifests/semantic/qdrant_documents_summary.md\n```\n\nCurrent document types:\n\n```text\nruntime_node\nplugin_topology\nfile_topology\ndoctrine\n```\n\n---\n\n## Recommended Qdrant Collections\n\n### `signalis_semantic`\n\nPrimary architecture retrieval.\n\nContains:\n\n```text\nruntime nodes\nplugin summaries\nfile summaries\ndoctrine\nontology\nsubsystem docs\n```\n\n---\n\n### `signalis_code`\n\nOptional secondary collection.\n\nContains:\n\n```text\nraw Lua chunks\nfunction-level snippets\nexact implementation references\n```\n\nUse only when semantic retrieval says exact code is needed.\n\n---\n\n### `signalis_diagnostics`\n\nOptional future collection.\n\nContains:\n\n```text\nQA reports\nprofiling results\nruntime measurements\nhotspot summaries\n```\n\n---\n\n## Metadata Fields\n\nEach embedded document should include metadata such as:\n\n```json\n{\n  \"doc_type\": \"runtime_node\",\n  \"node_type\": \"hook_event\",\n  \"plugin\": \"inventory\",\n  \"subsystem\": \"inventory_item_storage\",\n  \"realm\": \"server\",\n  \"file\": \"plugins/inventory/cl_hooks.lua\",\n  \"degree\": 42\n}\n```\n\nRecommended metadata fields:\n\n```text\ndoc_type\nnode_type\nedge_type\nplugin\nsubsystem\nrealm\nfile\nevent\nmessage\ntimer\ndegree\nrisk_flags\nsource_artifact\n```\n\n---\n\n## Retrieval Strategy\n\nQueries should retrieve:\n\n```text\nsemantic topology docs\nthen related doctrine\nthen exact raw code only if needed\n```\n\nExample query:\n\n```text\nWhy does inventory desync after character load?\n```\n\nExpected retrieval:\n\n```text\ninventory topology\ncharacter load events\ninventory network messages\nrelevant timers\nruntime doctrine\nnetworking model\n```\n\n---\n\n## Pipeline Scripts\n\nNext scripts:\n\n```text\nscripts/qdrant/embed_qdrant_documents.py\nscripts/qdrant/ingest_qdrant.py\nscripts/qdrant/query_qdrant.py\n```\n\nOptional later:\n\n```text\nscripts/qdrant/rebuild_embeddings.py\nscripts/qdrant/evaluate_retrieval.py\nscripts/qdrant/export_context_pack.py\n```\n\n---\n\n## Correct Order\n\nDo not start with Qdrant installation first.\n\nCorrect order:\n\n```text\n1. generate semantic documents\n2. generate embeddings/cache\n3. install/run Qdrant\n4. ingest vectors\n5. test retrieval quality\n6. integrate with architect reasoning\n```\n\n---\n\n## Future Orchestration Model\n\nLong-term flow:\n\n```text\nuser asks architecture question\n→ query Qdrant\n→ retrieve topology + doctrine\n→ assemble semantic context package\n→ send to ChatGPT/Gemini\n→ receive reasoning\n→ store summary back into semantic memory\n```\n\n---",
  "metadata": {
    "chunk_index": 0,
    "file": "subsystem_docs/qdrant_plan.md",
    "node_type": "doctrine",
    "source_id": "subsystem_docs/qdrant_plan.md"
  },
  "node_type": "doctrine",
  "file": "subsystem_docs/qdrant_plan.md"
}
```

### Text

```text
# SIGNALIS AI — Qdrant Plan

## Purpose

Qdrant will provide semantic retrieval over the SIGNALIS AI runtime topology and doctrine.

It should NOT replace deterministic extraction or normalization.

It should provide:

```text
architecture memory
semantic search
subsystem retrieval
topology-aware context assembly
```

for ChatGPT, Gemini, and local tools.

---

## Embedding Model

Preferred embedding model:

```text
BAAI/bge-small-en-v1.5
```

Reason:

```text
good for technical text
good for code-adjacent semantics
good for architecture summaries
local-friendly
```

---

## Primary Collection Content

Primary retrieval layer should store semantic artifacts, not raw Lua first.

Store:

```text
runtime topology nodes
runtime topology edge summaries
plugin topology summaries
file topology summaries
doctrine documents
event taxonomy
networking model
persistence model
realm model
subsystem summaries
```

Raw Lua should be a secondary retrieval layer for exact implementation checks.

---

## Current Semantic Corpus

Already generated:

```text
manifests/semantic/qdrant_documents.jsonl
manifests/semantic/qdrant_documents_summary.md
```

Current document types:

```text
runtime_node
plugin_topology
file_topology
doctrine
```

---

## Recommended Qdrant Collections

### `signalis_semantic`

Primary architecture retrieval.

Contains:

```text
runtime nodes
plugin summaries
file summaries
doctrine
ontology
subsystem docs
```

---

### `signalis_code`

Optional secondary collection.

Contains:

```text
raw Lua chunks
function-level snippets
exact implementation references
```

Use only when semantic retrieval says exact code is needed.

---

### `signalis_diagnostics`

Optional future collection.

Contains:

```text
QA reports
profiling results
runtime measurements
hotspot...
```

## Result 9

- Score: **-0.0231**
- Rerank score: `0.21450000000000002`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:character:+0.05', 'network_text_match:+0.10', 'doctrine_required:+0.16', 'causal:sync:+0.10', 'causal_network_flow:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:00ea627ae8d9a515`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/subsystems/vendor.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:00ea627ae8d9a515",
  "doc_type": "doctrine",
  "content_hash": "b078eae071cfe32036a48a30508e287c721de71bed30154b5868cb2b84b78feb",
  "embedding_dim": 384,
  "text": "# Subsystem: vendor\n\n## Purpose\n\nDeterministic subsystem summary generated from runtime topology.\n\n## Topology Summary\n\n- Nodes: **343**\n- Edges: **7764**\n\n## Node Types\n\n- `network_payload_operation`: 78\n- `network_operation`: 58\n- `hook_listener`: 44\n- `hook_emitter`: 33\n- `network_message`: 30\n- `hook_event`: 27\n- `file`: 19\n- `network_context`: 17\n- `timer_operation`: 11\n- `event_class`: 7\n- `timer`: 5\n- `plugin`: 4\n- `realm`: 3\n- `timer_class`: 3\n- `subsystem`: 2\n- `timer_risk`: 2\n\n## Edge Types\n\n- `runs_in_realm`: 4470\n- `classified_as`: 804\n- `references_timer`: 372\n- `dispatches_to`: 324\n- `has_timer_risk`: 215\n- `schedules_entity_action`: 182\n- `belongs_to_subsystem`: 150\n- `schedules_delay`: 132\n- `listens_to`: 131\n- `contains_network_operation`: 86\n- `listens_to_event`: 83\n- `contains_network_payload_operation`: 78\n- `emits`: 72\n- `registers_listener`: 70\n- `contains_listener`: 66\n- `file_sends_network_message`: 57\n- `removes_timer`: 57\n- `emits_event`: 50\n- `reads_network_payload`: 49\n- `sends_network_message`: 47\n\n## Major Hooks\n\n- `listen CanPlayerTradeWithVendor @ plugins\\vendor\\sv_hooks.lua:18`: 2\n- `listen VendorOpened @ plugins\\vendor\\cl_hooks.lua:1`: 2\n- `listen PlayerAccessVendor @ plugins\\vendor\\sv_hooks.lua:171`: 2\n- `listen CanPlayerAccessVendor @ plugins\\vendor\\sv_hooks.lua:2`: 2\n- `listen CanItemBeTransfered @ plugins\\ragdollinteraction\\interaction\\sv_hooks.lua:92`: 2\n- `VendorItemStockUpdated`: 1\n- `listen VendorItemModeUpdated @ plugins\\vendor\\derma\\cl_vendor.lua:211`: 1\n- `emit OnCharVarChanged @ gamemode\\core\\libs\\character\\cl_networking.lua:13`: 1\n- `listen VendorItemMaxStockUpdated @ plugins\\vendor\\derma\\cl_vendoreditor.lua:324`: 1\n- `emit CanPlayerTradeWithVendor @ plugins\\vendor\\sv_hooks.lua:78`: 1\n- `listen VendorMoneyUpdated @ plugins\\vendor\\derma\\cl_vendor.lua:200`: 1\n- `listen VendorItemMaxStockUpdated @ plugins\\vendor\\derma\\cl_vendor.lua:208`: 1\n- `LoadData`: 1\n- `VendorMoneyUpdated`: 1\n- `listen LoadData @ plugins\\vendor\\sv_data.lua:29`: 1\n- `CanItemBeTransfered`: 1\n- `emit OpenVendorTradeInterface @ plugins\\vendor\\entities\\entities\\nut_vendor\\init.lua:57`: 1\n- `listen VendorItemStockUpdated @ plugins\\vendor\\derma\\cl_vendor.lua:207`: 1\n- `emit VendorMoneyUpdated @ plugins\\vendor\\cl_networking.lua:59`: 1\n- `VendorExited`: 1\n\n## Major Network Signals\n\n- `receive nutVendorEdit`: 2\n- `netstream send activator`: 2\n- `receive nutVendorExit`: 2\n- `Receive nutVendorExit`: 2\n- `send nutVendorExit`: 2\n- `netstream send sendVendorInfo`: 2\n- `Receive nutVendorEdit`: 2\n- `Start nutVendorExit`: 2\n- `Start nutVendorTrade`: 2\n- `send nutVendorTrade`: 2\n- `nutVendorStock`: 1\n- `nutVendorFaction`: 1\n- `send nutVendorEdit`: 1\n- `nutVendor`: 1\n- `Start nutVendorAllowClass`: 1\n- `v`: 1\n- `nutVendorTrade`: 1\n- `netstream hook updateVendorFaction`: 1\n- `Start nutVendorAllowFaction`: 1\n- `send nutVendorAllowClass`: 1\n\n## Lifecycle Propagation\n\n- `LoadData`: 1\n- `listen LoadData @ plugins\\vendor\\sv_data.lua:29`: 1\n- `SaveData`: 1\n- `emit SaveData @ gamemode\\core\\sv_data.lua:95`: 1\n- `listen SaveData @ plugins\\vendor\\sv_data.lua:2`: 1\n- `emit SaveData @ gamemode\\core\\hooks\\sv_hooks.lua:731`: 1\n- `listen LoadData @ plugins\\vendor\\sv_data.lua:30`: 1\n- `emit LoadData @ gamemode\\core\\hooks\\sv_hooks.lua:737`: 1\n- `emit LoadData @ gamemode\\core\\hooks\\sv_hooks.lua:641`: 1\n- `listen SaveData @ plugins\\vendor\\sv_data.lua:3`: 1\n- `emit SaveData @ gamemode\\core\\hooks\\sv_hooks.lua:652`: 1\n\n## Synchronization Hotspots",
  "metadata": {
    "chunk_index": 0,
    "file": "docs/subsystems/vendor.md",
    "node_type": "doctrine",
    "source_id": "docs/subsystems/vendor.md"
  },
  "node_type": "doctrine",
  "file": "docs/subsystems/vendor.md"
}
```

### Text

```text
# Subsystem: vendor

## Purpose

Deterministic subsystem summary generated from runtime topology.

## Topology Summary

- Nodes: **343**
- Edges: **7764**

## Node Types

- `network_payload_operation`: 78
- `network_operation`: 58
- `hook_listener`: 44
- `hook_emitter`: 33
- `network_message`: 30
- `hook_event`: 27
- `file`: 19
- `network_context`: 17
- `timer_operation`: 11
- `event_class`: 7
- `timer`: 5
- `plugin`: 4
- `realm`: 3
- `timer_class`: 3
- `subsystem`: 2
- `timer_risk`: 2

## Edge Types

- `runs_in_realm`: 4470
- `classified_as`: 804
- `references_timer`: 372
- `dispatches_to`: 324
- `has_timer_risk`: 215
- `schedules_entity_action`: 182
- `belongs_to_subsystem`: 150
- `schedules_delay`: 132
- `listens_to`: 131
- `contains_network_operation`: 86
- `listens_to_event`: 83
- `contains_network_payload_operation`: 78
- `emits`: 72
- `registers_listener`: 70
- `contains_listener`: 66
- `file_sends_network_message`: 57
- `removes_timer`: 57
- `emits_event`: 50
- `reads_network_payload`: 49
- `sends_network_message`: 47

## Major Hooks

- `listen CanPlayerTradeWithVendor @ plugins\vendor\sv_hooks.lua:18`: 2
- `listen VendorOpened @ plugins\vendor\cl_hooks.lua:1`: 2
- `listen PlayerAccessVendor @ plugins\vendor\sv_hooks.lua:171`: 2
- `listen CanPlayerAccessVendor @ plugins\vendor\sv_hooks.lua:2`: 2
- `listen CanItemBeTransfered @ plugins\ragdollinteraction\interaction\sv_hooks.lua:92`: 2
- `VendorItemStockUpdated`: 1
- `listen VendorItemModeUpdated @ plugins\vendor\derma\cl_vendor.lua:211`: 1
- `emit OnCharVarChanged @ gamemode\core\libs\character\cl_networking.lua:13`: 1
- `listen VendorItemMaxStockUpdated @ plugins\vendor\derma\cl_vendoreditor.lua:324`: 1
- `emit CanPlayerTradeWithVendor @ plugins\vendor\sv_hooks.lua:78`: 1
- `listen VendorMoneyUpdated @ plugins\...
```

## Result 10

- Score: **-0.0443**
- Rerank score: `0.21250000000000002`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:character:+0.05', 'text_event:characterloaded:+0.10', 'network_text_match:+0.10', 'doctrine_required:+0.16', 'causal:sync:+0.10']`
- Source ID: `doc:doctrine:41b2487acd40a617`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/project_structure.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:41b2487acd40a617",
  "doc_type": "doctrine",
  "content_hash": "d7a7ba63d75445ae5f7dbe6421126824c7643d4b179ca5d06a8d1f6722f6435e",
  "embedding_dim": 384,
  "text": "# SIGNALIS AI — Project Structure\n\nGenerated: `2026-05-31T13:44:58`\n\n## Workspace\n\n```text\nE:/signalis_ai\n```\n\n## Directory Tree\n\n```text\nconfig/\ndecisions/\ndocs/\n  ai_subsystems/\n  human_subsystems/\n  runtime/\n    runtime_chains/\n  subsystems/\nembeddings/\ngraphs/\ninvestigations/\n  generated/\n  templates/\n  validation/\nlogs/\nmanifests/\n  character_inventory/\n  commands/\n  custom_hooks/\n  derma/\n  entities/\n  globals/\n  hooks/\n  items/\n  networking/\n  normalized/\n  persistence/\n  plugins/\n  registries/\n  semantic/\n  timers/\nprompts/\nreports/\n  retrieval_eval/\n    raw/\nruntime_schemas/\nscripts/\n  diagnostics/\n  doctrine/\n  embeddings/\n  extraction/\n  graphs/\n  manifests/\n  normalization/\n  profiling/\n  qdrant/\n  runtime/\n  semantic/\n  tools/\n  utils/\nsubsystem_docs/\ntemp/\n```\n\n## Known Important Paths\n\n### Runtime Topology Files\n\n- `manifests/normalized/runtime_topology.json` (11579.3 KB)\n- `manifests/normalized/runtime_topology_edges.json` (8330.6 KB)\n- `manifests/normalized/runtime_topology_nodes.json` (2566.3 KB)\n\n### Qdrant Files\n\n- `manifests/semantic/qdrant_documents.jsonl` (2185.2 KB)\n- `manifests/semantic/qdrant_documents_summary.md` (2.0 KB)\n- `manifests/semantic/qdrant_embedding_summary.md` (0.3 KB)\n- `manifests/semantic/qdrant_embeddings.jsonl` (20126.6 KB)\n- `manifests/semantic/qdrant_ingest_summary.md` (0.5 KB)\n- `manifests/semantic/qdrant_query_results.md` (46.9 KB)\n- `scripts/qdrant/`\n- `scripts/qdrant/build_qdrant_documents.py` (16.3 KB)\n- `scripts/qdrant/embed_qdrant_documents.py` (2.5 KB)\n- `scripts/qdrant/ingest_qdrant.py` (7.1 KB)\n- `scripts/qdrant/query_qdrant.py` (8.9 KB)\n- `subsystem_docs/qdrant_plan.md` (3.6 KB)\n\n### Investigation Files\n\n- `investigations/generated/`\n- `investigations/generated/vendor_stale_price_label_after_purchase.json` (1.7 KB)\n- `investigations/generated/vendor_stale_price_label_after_purchase.md` (15.5 KB)\n- `investigations/generated/vendor_stale_price_label_after_purchase.raw.txt` (46.9 KB)\n- `investigations/inventory_desync_context_pack.md` (105.7 KB)\n- `investigations/inventory_desync_phase1.md` (99.7 KB)\n- `investigations/paths_characterloaded_to_inventory_panel_status.md` (7.6 KB)\n- `investigations/paths_v2_characterloaded_to_inventory_panel_status.md` (10.3 KB)\n- `investigations/templates/`\n- `investigations/templates/investigation.md` (0.0 KB)\n- `investigations/validation/`\n- `investigations/validation/vendor_stale_price_label_after_purchase_runtime_chain_evidence.json` (60.7 KB)\n- `investigations/validation/vendor_stale_price_label_after_purchase_runtime_chain_evidence.md` (39.5 KB)\n- `investigations/validation/vendor_stale_price_label_after_purchase_validation.json` (164.2 KB)\n- `investigations/validation/vendor_stale_price_label_after_purchase_validation.md` (102.3 KB)\n- `investigations/validation/vendor_stale_price_label_after_purchase_validation_deduped.json` (266.7 KB)\n- `investigations/validation/vendor_stale_price_label_after_purchase_validation_deduped.md` (40.7 KB)\n- `investigations/validation/vendor_stale_price_label_after_purchase_validation_evidence_graph.json` (64.4 KB)\n- `investigations/validation/vendor_stale_price_label_after_purchase_validation_evidence_graph.md` (41.3 KB)\n- `investigations/validation/vendor_stale_price_label_after_purchase_validation_investigation_synthesis.json` (9.9 KB)\n- `investigations/validation/vendor_stale_price_label_after_purchase_validation_investigation_synthesis.md` (9.6 KB)\n- `investigations/validation/vendor_stale_price_label_after_purc",
  "metadata": {
    "chunk_index": 0,
    "file": "docs/project_structure.md",
    "node_type": "doctrine",
    "source_id": "docs/project_structure.md"
  },
  "node_type": "doctrine",
  "file": "docs/project_structure.md"
}
```

### Text

```text
# SIGNALIS AI — Project Structure

Generated: `2026-05-31T13:44:58`

## Workspace

```text
E:/signalis_ai
```

## Directory Tree

```text
config/
decisions/
docs/
  ai_subsystems/
  human_subsystems/
  runtime/
    runtime_chains/
  subsystems/
embeddings/
graphs/
investigations/
  generated/
  templates/
  validation/
logs/
manifests/
  character_inventory/
  commands/
  custom_hooks/
  derma/
  entities/
  globals/
  hooks/
  items/
  networking/
  normalized/
  persistence/
  plugins/
  registries/
  semantic/
  timers/
prompts/
reports/
  retrieval_eval/
    raw/
runtime_schemas/
scripts/
  diagnostics/
  doctrine/
  embeddings/
  extraction/
  graphs/
  manifests/
  normalization/
  profiling/
  qdrant/
  runtime/
  semantic/
  tools/
  utils/
subsystem_docs/
temp/
```

## Known Important Paths

### Runtime Topology Files

- `manifests/normalized/runtime_topology.json` (11579.3 KB)
- `manifests/normalized/runtime_topology_edges.json` (8330.6 KB)
- `manifests/normalized/runtime_topology_nodes.json` (2566.3 KB)

### Qdrant Files

- `manifests/semantic/qdrant_documents.jsonl` (2185.2 KB)
- `manifests/semantic/qdrant_documents_summary.md` (2.0 KB)
- `manifests/semantic/qdrant_embedding_summary.md` (0.3 KB)
- `manifests/semantic/qdrant_embeddings.jsonl` (20126.6 KB)
- `manifests/semantic/qdrant_ingest_summary.md` (0.5 KB)
- `manifests/semantic/qdrant_query_results.md` (46.9 KB)
- `scripts/qdrant/`
- `scripts/qdrant/build_qdrant_documents.py` (16.3 KB)
- `scripts/qdrant/embed_qdrant_documents.py` (2.5 KB)
- `scripts/qdrant/ingest_qdrant.py` (7.1 KB)
- `scripts/qdrant/query_qdrant.py` (8.9 KB)
- `subsystem_docs/qdrant_plan.md` (3.6 KB)

### Investigation Files

- `investigations/generated/`
- `investigations/generated/vendor_stale_price_label_after_purchase.json` (1.7 KB)...
```
