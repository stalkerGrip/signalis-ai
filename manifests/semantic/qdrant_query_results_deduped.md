# Qdrant Query Results

Collection: `signalis_semantic`
Query: `vendor stale price labels after purchase`
Expanded query used: `vendor stale price labels after purchase file file_summary hook_emitter hook_event hook_listener inventory plugin plugin_summary vendor`
Top K: **10**
Retrieve K: **50**
Model: `BAAI/bge-small-en-v1.5`
Hash query: `False`

## Returned results: 10

## Deduplicated results: 7

## Result 1

- Score: **0.7658**
- Rerank score: `0.5830390999999999`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:vendor:+0.05', 'doctrine_required:+0.16', 'file_subsystem:vendor:+0.07', 'causal:net.receive:+0.15', 'causal:setdata:+0.18', 'causal:sync:+0.10', 'causal:itemdatachanged:+0.18', 'causal:nutinventoryadd:+0.16', 'causal:invdata:+0.18', 'state_mutation_or_sync:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:24070106b1a7a7f3`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/runtime/runtime_chains/vendor_purchase_item_metadata_sync.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:24070106b1a7a7f3",
  "doc_type": "doctrine",
  "content_hash": "29690ab687503485d9bec41a21b7d42ca3a9357a8b86071e4541b0005506c4c7",
  "embedding_dim": 384,
  "text": "# Vendor Purchase Item Metadata Sync\n\nStatus: source-validated runtime chain.\n\n- Generated at: `2026-05-31T11:53:24+00:00`\n- Source evidence JSON: `E:\\signalis_ai\\investigations\\validation\\vendor_stale_price_label_after_purchase_validation_targeted_validation_patched_runtime_chain_evidence.json`\n- Subsystem: `vendor`\n- Chain ID: `CHAIN-001`\n- Confidence: `validated`\n- Score: `1904`\n- Raw evidence total: `123`\n- Deduped evidence total: `102`\n- Duplicates removed: `21`\n\n## Runtime Chain\n\n1. gridinv transfer identifies vendor → player purchase\n2. transfer crosses old inventory to player inventory boundary\n3. server removes/adds item across inventories\n4. server resolves current inventory recipients\n5. server sends full item state to recipients\n6. server sends nutInventoryAdd membership delta\n7. client receives nutInventoryAdd\n8. client emits InventoryItemAdded\n9. server clears vendor metadata on purchased item\n10. ITEM:setData mutates authoritative item data\n11. server sends invData item-data delta\n12. client receives invData item-data delta\n13. client emits ItemDataChanged\n14. grid inventory panel handles item-data change\n15. grid inventory panel repopulates item icons\n\n## Architecture Meaning\n\nThis chain records source-validated runtime propagation. It should be used as a durable semantic anchor for retrieval-guided architecture reasoning, not as a replacement for raw source validation when changing code.\n\nWhen investigating related bugs, prefer this chain as compact context before opening raw Lua.\n\n## Validated Chain Form\n\n```text\ngridinv transfer identifies vendor → player purchase\n→ transfer crosses old inventory to player inventory boundary\n→ server removes/adds item across inventories\n→ server resolves current inventory recipients\n→ server sends full item state to recipients\n→ server sends nutInventoryAdd membership delta\n→ client receives nutInventoryAdd\n→ client emits InventoryItemAdded\n→ server clears vendor metadata on purchased item\n→ ITEM:setData mutates authoritative item data\n→ server sends invData item-data delta\n→ client receives invData item-data delta\n→ client emits ItemDataChanged\n→ grid inventory panel handles item-data change\n→ grid inventory panel repopulates item icons\n```\n\n## Representative Evidence\n\n### vendor_purchase_detection\n\n- File: `plugins/gridinv/sv_transfer.lua`\n- Lines: `116-128`\n- Pattern: `vendorSellItem`\n- Score: `145`\n\n### inventory_boundary_transfer\n\n- File: `plugins/gridinv/sv_transfer.lua`\n- Lines: `1-11`\n- Pattern: `oldInventory + destination inventory`\n- Score: `134`\n\n### inventory_membership_mutation\n\n- File: `plugins/gridinv/sv_transfer.lua`\n- Lines: `116-128`\n- Pattern: `remove/add item transfer`\n- Score: `113`\n\n### inventory_recipients_resolved\n\n- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`\n- Lines: `193-205`\n- Pattern: `self:getRecipients()`\n- Score: `104`\n\n### item_full_state_sync\n\n- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`\n- Lines: `41-53`\n- Pattern: `item:sync(recipients)`\n- Score: `118`\n\n### inventory_membership_network_send\n\n- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`\n- Lines: `35-47`\n- Pattern: `Inventory:syncItemAdded`\n- Score: `120`\n\n### inventory_membership_receive_add\n\n- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`\n- Lines: `50-62`\n- Pattern: `net.Receive(\"nutInventoryAdd\")`\n- Score: `120`\n\n### inventory_membership_client_event",
  "metadata": {
    "chunk_index": 0,
    "file": "docs/runtime/runtime_chains/vendor_purchase_item_metadata_sync.md",
    "node_type": "doctrine",
    "source_id": "docs/runtime/runtime_chains/vendor_purchase_item_metadata_sync.md"
  },
  "node_type": "doctrine",
  "file": "docs/runtime/runtime_chains/vendor_purchase_item_metadata_sync.md"
}
```

### Text

```text
# Vendor Purchase Item Metadata Sync

Status: source-validated runtime chain.

- Generated at: `2026-05-31T11:53:24+00:00`
- Source evidence JSON: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_targeted_validation_patched_runtime_chain_evidence.json`
- Subsystem: `vendor`
- Chain ID: `CHAIN-001`
- Confidence: `validated`
- Score: `1904`
- Raw evidence total: `123`
- Deduped evidence total: `102`
- Duplicates removed: `21`

## Runtime Chain

1. gridinv transfer identifies vendor → player purchase
2. transfer crosses old inventory to player inventory boundary
3. server removes/adds item across inventories
4. server resolves current inventory recipients
5. server sends full item state to recipients
6. server sends nutInventoryAdd membership delta
7. client receives nutInventoryAdd
8. client emits InventoryItemAdded
9. server clears vendor metadata on purchased item
10. ITEM:setData mutates authoritative item data
11. server sends invData item-data delta
12. client receives invData item-data delta
13. client emits ItemDataChanged
14. grid inventory panel handles item-data change
15. grid inventory panel repopulates item icons

## Architecture Meaning

This chain records source-validated runtime propagation. It should be used as a durable semantic anchor for retrieval-guided architecture reasoning, not as a replacement for raw source validation when changing code.

When investigating related bugs, prefer this chain as compact context before opening raw Lua.

## Validated Chain Form

```text
gridinv transfer identifies vendor → player purchase
→ transfer crosses old inventory to player inventory boundary
→ server removes/adds item across inventories
→ server resolves current inventory recipients
→ server sends full item state to r...
```

## Result 2

- Score: **0.7521**
- Rerank score: `0.57821932`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:vendor:+0.05', 'doctrine_required:+0.16', 'file_subsystem:vendor:+0.07', 'causal:hook.run:+0.18', 'causal:net.receive:+0.15', 'causal:setdata:+0.18', 'causal:sync:+0.10', 'causal:itemdatachanged:+0.18', 'causal:inventorydatachanged:+0.16', 'causal:nutinventoryadd:+0.16', 'causal:invdata:+0.18', 'causal:removeitem:+0.12', 'causal:inventory:add:+0.14', 'state_mutation_or_sync:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:dad865c1ed66ff02`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/runtime/runtime_chains/vendor_purchase_chain.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:dad865c1ed66ff02",
  "doc_type": "doctrine",
  "content_hash": "c8d4c0ca59d7e9c0166c504b3324defcabb98591ce54571083b90670d4ddc031",
  "embedding_dim": 384,
  "text": "# Vendor Purchase Runtime Chain\n\nStatus: source-validated runtime chain.\n\n- Source evidence JSON: `E:\\signalis_ai\\investigations\\validation\\vendor_stale_price_label_after_purchase_validation_targeted_validation_patched_runtime_chain_evidence.json`\n- Chain ID: `CHAIN-001`\n- Confidence: `validated`\n- Score: `1904`\n- Steps present: `15`\n\n## Runtime Chain\n\n1. gridinv transfer identifies vendor → player purchase\n2. transfer crosses old inventory to player inventory boundary\n3. server removes/adds item across inventories\n4. server resolves current inventory recipients\n5. server sends full item state to recipients\n6. server sends nutInventoryAdd membership delta\n7. client receives nutInventoryAdd\n8. client emits InventoryItemAdded\n9. server clears vendor metadata on purchased item\n10. ITEM:setData mutates authoritative item data\n11. server sends invData item-data delta\n12. client receives invData item-data delta\n13. client emits ItemDataChanged\n14. grid inventory panel handles item-data change\n15. grid inventory panel repopulates item icons\n\n## Architecture Meaning\n\nVendor purchase propagation crosses two separate runtime systems:\n\n1. Inventory membership propagation: transfer, add/remove, item full sync, and `nutInventoryAdd` membership delta.\n2. Item metadata propagation: `ITEM:setData`, `invData`, `ItemDataChanged`, and grid panel refresh.\n\nDo not conflate item metadata sync with inventory-level data sync. `InventoryDataChanged` / `nutInventoryData` is a different channel from `ItemDataChanged` / `invData`.\n\n## Validated Chain Form\n\n```text\nvendorSellItem\n→ oldInventory:removeItem\n→ inventory:add\n→ Inventory:syncItemAdded\n→ item:sync(recipients)\n→ nutInventoryAdd\n→ InventoryItemAdded\n→ item:setData(\"vendorSPrice\", nil)\n→ ITEM:setData\n→ invData\n→ ItemDataChanged\n→ InventoryItemDataChanged\n→ populateItems()\n```\n\n## Representative Evidence\n\n### vendor_purchase_detection\n\n- File: `plugins/gridinv/sv_transfer.lua`\n- Lines: `116-128`\n- Pattern: `vendorSellItem`\n- Score: `145`\n\n### inventory_boundary_transfer\n\n- File: `plugins/gridinv/sv_transfer.lua`\n- Lines: `1-11`\n- Pattern: `oldInventory + destination inventory`\n- Score: `134`\n\n### inventory_membership_mutation\n\n- File: `plugins/gridinv/sv_transfer.lua`\n- Lines: `116-128`\n- Pattern: `remove/add item transfer`\n- Score: `113`\n\n### inventory_recipients_resolved\n\n- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`\n- Lines: `193-205`\n- Pattern: `self:getRecipients()`\n- Score: `104`\n\n### item_full_state_sync\n\n- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`\n- Lines: `41-53`\n- Pattern: `item:sync(recipients)`\n- Score: `118`\n\n### inventory_membership_network_send\n\n- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`\n- Lines: `35-47`\n- Pattern: `Inventory:syncItemAdded`\n- Score: `120`\n\n### inventory_membership_receive_add\n\n- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`\n- Lines: `50-62`\n- Pattern: `net.Receive(\"nutInventoryAdd\")`\n- Score: `120`\n\n### inventory_membership_client_event\n\n- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`\n- Lines: `57-69`\n- Pattern: `hook.Run(\"InventoryItemAdded\")`\n- Score: `115`\n\n### vendor_metadata_cleanup\n\n- File: `plugins/gridinv/sv_transfer.lua`\n- Lines: `207-219`\n- Pattern: `item:setData(\"vendorSPrice\", nil`\n- Score: `150`\n\n### item_metadata_mutation\n\n- File: `gamemode/core/meta/item/sv_item.lua`\n- Lines: `154-166`\n- Pattern: `function ITEM:setData`\n- Score: `130`\n\n### item_metadata_network_sync_send",
  "metadata": {
    "chunk_index": 0,
    "file": "docs/runtime/runtime_chains/vendor_purchase_chain.md",
    "node_type": "doctrine",
    "source_id": "docs/runtime/runtime_chains/vendor_purchase_chain.md"
  },
  "node_type": "doctrine",
  "file": "docs/runtime/runtime_chains/vendor_purchase_chain.md"
}
```

### Text

```text
# Vendor Purchase Runtime Chain

Status: source-validated runtime chain.

- Source evidence JSON: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_targeted_validation_patched_runtime_chain_evidence.json`
- Chain ID: `CHAIN-001`
- Confidence: `validated`
- Score: `1904`
- Steps present: `15`

## Runtime Chain

1. gridinv transfer identifies vendor → player purchase
2. transfer crosses old inventory to player inventory boundary
3. server removes/adds item across inventories
4. server resolves current inventory recipients
5. server sends full item state to recipients
6. server sends nutInventoryAdd membership delta
7. client receives nutInventoryAdd
8. client emits InventoryItemAdded
9. server clears vendor metadata on purchased item
10. ITEM:setData mutates authoritative item data
11. server sends invData item-data delta
12. client receives invData item-data delta
13. client emits ItemDataChanged
14. grid inventory panel handles item-data change
15. grid inventory panel repopulates item icons

## Architecture Meaning

Vendor purchase propagation crosses two separate runtime systems:

1. Inventory membership propagation: transfer, add/remove, item full sync, and `nutInventoryAdd` membership delta.
2. Item metadata propagation: `ITEM:setData`, `invData`, `ItemDataChanged`, and grid panel refresh.

Do not conflate item metadata sync with inventory-level data sync. `InventoryDataChanged` / `nutInventoryData` is a different channel from `ItemDataChanged` / `invData`.

## Validated Chain Form

```text
vendorSellItem
→ oldInventory:removeItem
→ inventory:add
→ Inventory:syncItemAdded
→ item:sync(recipients)
→ nutInventoryAdd
→ InventoryItemAdded
→ item:setData("vendorSPrice", nil)
→ ITEM:setData
→ invData
→ ItemDataChanged
→ InventoryI...
```

## Result 3

- Score: **0.7425**
- Rerank score: `0.554364675`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:vendor:+0.05', 'doctrine_required:+0.16', 'causal:setdata:+0.18', 'causal:sync:+0.10', 'causal:itemdatachanged:+0.18', 'causal:nutinventoryadd:+0.16', 'causal:invdata:+0.18', 'state_mutation_or_sync:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:47ad906557a8aae4`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/project_memory.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:47ad906557a8aae4",
  "doc_type": "doctrine",
  "content_hash": "b7c45c454648d49e38434ef1ba20cd64f6bddb1a061483982c018dd2cfb78e6b",
  "embedding_dim": 384,
  "text": "than duplicate them.\n\nConfidence:\n\n```text\nMedium\n```\n\n## Current Runtime Chain Under Investigation\n\n```text\nCharacterLoaded\n→ PlayerLoadedChar\n→ PlayerLoadout\n→ PostPlayerLoadout\n→ inventory initialization / sync\n→ inventoryOpen\n→ inventorySetPanelStatus\n→ client inventory UI\n```\n\n## Open Questions\n\n- Which vendor files are authoritative after the rework?\n- Which vendor UI fields persist as stale item presentation metadata?\n- Which inventory sync path owns clearing vendor price labels?\n- Does storage movement trigger a broader item UI refresh than vendor purchase?\n- Which lifecycle event should become the canonical inventory/UI resync boundary?\n- Which artifacts should be promoted from investigation reports into doctrine or subsystem docs?\n\n## Update Rule\n\nWhen human-confirmed information resolves ambiguity, update one of:\n\n- `docs/project_memory.md`\n- `docs/human_subsystems/*.md`\n- `docs/subsystems/*.md`\n- `docs/ai_subsystems/*.md`\n- `investigations/*.md`\n- project instructions, only for reusable global rules\n\n## Local Development Environment\n\nUser workstation:\n\n```text\nOS: Windows 10\nCPU: Ryzen 5 7500F\nRAM: 32 GB DDR4\nGPU: AMD RX 9060 XT 16 GB\nPython torch: 2.12.0+cpu\nCUDA available: false\n```\n\nCUDA is unavailable because GPU is AMD.\nDefault ML pipeline should assume CPU inference.\nBGE reranker should use use_fp16=False by default.\nDo not prioritize ROCm until ranking quality is proven useful.\n\n## Investigation Pipeline Lessons\n\nValidated pipeline lesson:\n\nInventory membership sync and item metadata sync are separate runtime systems, but both may participate in the same causal chain.\n\nFor vendor purchase:\n\n```text\ngridinv sv_transfer\n→ inventory membership transfer\n→ Inventory:syncItemAdded\n→ item:sync(recipients)\n→ nutInventoryAdd\n→ purchase metadata cleanup\n→ item:setData(\"vendorSPrice\", nil, client)\n→ ITEM:setData\n→ invData\n→ ItemDataChanged\n→ grid panel InventoryItemDataChanged\n→ populateItems\n```",
  "metadata": {
    "chunk_index": 1,
    "file": "docs/project_memory.md",
    "node_type": "doctrine",
    "source_id": "docs/project_memory.md"
  },
  "node_type": "doctrine",
  "file": "docs/project_memory.md"
}
```

### Text

```text
than duplicate them.

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
→ item:...
```

## Result 4

- Score: **0.6962**
- Rerank score: `0.541172009`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:vendor:+0.05', 'doctrine_required:+0.16', 'causal:hook.run:+0.18', 'causal:setdata:+0.18', 'causal:sync:+0.10', 'causal:receiver:+0.10', 'causal:receivers:+0.10', 'causal:itemdatachanged:+0.18', 'causal:inventorydatachanged:+0.16', 'causal:invdata:+0.18', 'causal:setuppanel:+0.10', 'state_mutation_or_sync:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:7ba6861373241eea`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/human_context.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:7ba6861373241eea",
  "doc_type": "doctrine",
  "content_hash": "4d0d6d447f8c23e8cb9acd29a9c1eeb87bee51c9ac23ee4a050b32dd661ca748",
  "embedding_dim": 384,
  "text": "# SIGNALIS AI — Human Context\n\n## Project Reality Notes\n\n## Current Architecture Intent\n\n## Known Legacy / Reworked Systems\n\n## Known Bugs and Runtime Symptoms\n\n## Human-Confirmed Correct Behavior\n\n## Human-Confirmed Incorrect Behavior\n\n## Subsystem Ownership Notes\n\n## UI / Sync Rules\n\n## Item Data Semantics\n\nHuman-validated:\n\nITEM:setData(key, value, receivers, noSave, noCheckEntity) mutates server-side item data, optionally syncs the changed key/value to receivers or the current owner through netstream \"invData\", updates world entity netvars when an item entity exists, and persists item data to the database unless noSave is set.\n\nTherefore item:setData is both persistent item metadata mutation and a conditional synchronization boundary.\n\nIt should not be treated as a simple local state write.\n\nIf receivers are missing or incorrect, current clients may not receive the update immediately. Future owners or clients opening/syncing the inventory may still receive the persisted data later.\n\nItem-level data sync is distinct from inventory-level data sync.\n\nClient item data updates are received through netstream \"invData\" in item client networking, mutate item.data[key], and emit:\n\nhook.Run(\"ItemDataChanged\", item, key, oldValue, value)\n\nInventory-level data updates use nutInventoryData and emit InventoryDataChanged.\n\nDo not conflate ItemDataChanged with InventoryDataChanged.\n\n## Vendor / Inventory Notes\n\nHuman-validated vendor purchase transfer flow:\n\nWhen buying from a vendor, grid inventory transfer runs through plugins/gridinv/sv_transfer.lua.\n\nFor vendor → player purchase:\noldInventory is the vendor inventory.\ninventory is the player character inventory.\nvendorSellItem becomes true when oldInventory.vendor is valid and the destination inventory is the player character inventory.\n\nThe transfer flow removes the item from the vendor inventory, adds it to the player inventory, then after successful transfer clears vendor sell metadata on the item:\n\nitem:setData(\"vendorQty\", nil, client)\nitem:setData(\"vendorSPrice\", nil, client)\nitem:setData(\"vendorMQty\", nil, client)\n\nIf the vendor still has a buy price for that item type, the transferred item may receive:\n\nitem:setData(\"vendorBPrice\", buyPrice, client)\n\nTherefore vendor purchase cleanup is not only RemoveReceiverFromVendor. Purchase transfer itself performs item-level vendor metadata mutation after inventory transfer.\n\nHuman-validated vendor open flow:\n\nPlayer interacts with vendor\n→ server calls/emits OpenVendorTradeInterface\n→ client receives vendorTradeInterface\n→ vendorTradeInterface creates the player/local inventory panel through PLUGIN:CreateNewInventoryPanel(...), but the vendor inventory panel is created separately with vgui.Create(\"vendor_grid_inventory\") and then bound to the loaded vendor inventory using storageInvPanel:SetUpPanel(loadedInv).\n→ resulting UI shows vendor inventory and player inventory side by side.\n\nCreateNewInventoryPanel in this flow is not an independent root cause. It is part of vendorTradeInterface UI construction.\n\nThe vendor system has been reworked. Some files under plugins/vendor are legacy and should not be assumed authoritative without validation.\n\nObserved bug:\nAfter buying items from a vendor, vendor price labels sometimes remain visible on items inside the player inventory.\n\nObserved recovery:\nRelog usually fixes the issue.\nMoving the item through storage can also refresh/clear the incorrect display state.",
  "metadata": {
    "chunk_index": 0,
    "file": "docs/human_context.md",
    "node_type": "doctrine",
    "source_id": "docs/human_context.md"
  },
  "node_type": "doctrine",
  "file": "docs/human_context.md"
}
```

### Text

```text
# SIGNALIS AI — Human Context

## Project Reality Notes

## Current Architecture Intent

## Known Legacy / Reworked Systems

## Known Bugs and Runtime Symptoms

## Human-Confirmed Correct Behavior

## Human-Confirmed Incorrect Behavior

## Subsystem Ownership Notes

## UI / Sync Rules

## Item Data Semantics

Human-validated:

ITEM:setData(key, value, receivers, noSave, noCheckEntity) mutates server-side item data, optionally syncs the changed key/value to receivers or the current owner through netstream "invData", updates world entity netvars when an item entity exists, and persists item data to the database unless noSave is set.

Therefore item:setData is both persistent item metadata mutation and a conditional synchronization boundary.

It should not be treated as a simple local state write.

If receivers are missing or incorrect, current clients may not receive the update immediately. Future owners or clients opening/syncing the inventory may still receive the persisted data later.

Item-level data sync is distinct from inventory-level data sync.

Client item data updates are received through netstream "invData" in item client networking, mutate item.data[key], and emit:

hook.Run("ItemDataChanged", item, key, oldValue, value)

Inventory-level data updates use nutInventoryData and emit InventoryDataChanged.

Do not conflate ItemDataChanged with InventoryDataChanged.

## Vendor / Inventory Notes

Human-validated vendor purchase transfer flow:

When buying from a vendor, grid inventory transfer runs through plugins/gridinv/sv_transfer.lua.

For vendor → player purchase:
oldInventory is the vendor inventory.
inventory is the player character inventory.
vendorSellItem becomes true when oldInventory.vendor is valid and the destination inventory is the player character in...
```

## Result 5

- Score: **0.6477**
- Rerank score: `0.524203855`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:inventory:+0.05', 'doctrine_required:+0.16', 'causal:sync:+0.10', 'causal:itemdatachanged:+0.18', 'causal:inventorydatachanged:+0.16', 'causal:nutinventoryadd:+0.16', 'causal:nutinventoryremove:+0.14', 'causal:invdata:+0.18', 'state_mutation_or_sync:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:716ac0b5c759aa56`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `subsystem_docs/runtime_doctrine.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:716ac0b5c759aa56",
  "doc_type": "doctrine",
  "content_hash": "c47ca56f15bbe081c67ddcc591fa87591b677fbfa95a47e21717f4400e104ab0",
  "embedding_dim": 384,
  "text": "some areas\n```\n\nPersistence is mostly shutdown-oriented, with some on-demand/runtime save behavior.\n\nKnown major bottlenecks are not confirmed yet.\n\n`SaveData`, `LoadData`, `PersistenceSave`, and related hooks should be treated as high-importance lifecycle hubs.\n\nFuture architecture should clarify:\n\n```text\nwhat saves when\nwhat is authoritative\nwhat can be async\nwhat must be atomic\nwhat can be rebuilt from runtime state\n```\n\n## Inventory Doctrine\n\nInventory synchronization has multiple separate channels:\n\n- inventory metadata delta: nutInventoryData → InventoryDataChanged\n- full inventory initialization: nutInventoryInit\n- item membership delta: nutInventoryAdd / nutInventoryRemove\n- item data delta: invData → ItemDataChanged\n\nItem UI desync investigations must distinguish inventory.data from item.data.\n\nInventory is both server-side authoritative and client-visible through Derma/grid inventory.\n\nCurrent behavior:\n\n```text\nitems saved in DB\nserver stores authoritative information\nclient views/manipulates through UI\ngrid inventory / Derma represents state visually\n```\n\nKnown pain point:\n\n```text\nUI desync\n```\n\nInventory sync may be mixed between full refresh and partial/delta updates. This needs further inspection.\n\nInventory is a high-priority subsystem because it connects:\n\n```text\nitems\nstorage\nentities\nnetworking\nUI\npersistence\ncommands\nplayer actions\n```\n\n## Realm Doctrine\n\nRealm responsibility is currently mixed but mostly server-side.\n\nLong-term direction:\n\n```text\nserver owns authoritative simulation and persistence\nclient owns presentation and UI\nshared code should express contracts, not hide authority\nnetworking should explicitly cross realm boundaries\n```\n\nClient prediction is not currently well understood or intentionally used. Future architecture should avoid relying on prediction until the model is clear.\n\nPlugin realm roles vary:\n\n```text\nUI-only\nsimulation-only\ninfrastructure\nmixed client/server\nlegacy/base framework\n```\n\n## Performance Doctrine\n\nCurrent high-priority risk areas:\n\n```text\nPVP/PVE performance\ndynamic lights\ninfrastructure entities\nnextbots\ncorrect architecture implementation\nmemory leaks\nUI desync\nFPS drops with entities\n```\n\nLikely performance sources to investigate:\n\n```text\nThink hooks\nhigh-frequency timers\nentity simulation loops\nnextbot processing\ndynamic lighting\nnetwork sync spam\nlarge payloads\nUI refresh loops\nmemory leaks from timers/entities/panels\n```\n\nHigh-frequency logic should be classified by intent before optimization.\n\n## Investigation-Oriented Topology Doctrine\n\nValidation exists to confirm runtime propagation.\n\nInvestigation should prioritize:\n\n```text\nevent propagation\nnetwork propagation\nrealm crossings\nstate ownership transitions\n```\n\nover isolated source fragments.\n\nPreferred investigation artifacts:\n\n```text\nruntime chains\ncausal chains\nsubsystem interaction paths\n```\n\nrather than ranked code snippets alone.\n\nTopology-aware evidence is preferred over semantic similarity alone.\n\n\n## Runtime Graph Doctrine\n\nRuntime topology should be built from normalized semantic facts, not raw code dumps.\n\nStable graph IDs should distinguish semantic node types:\n\n```text\nhook:SaveData\nnet:invAct\ntimer:nutSaveData\nplugin:healthproblems\nfile:plugins/healthproblems/sv_hooks.lua\nentity:nut_ore_smelter\ncommand:chargetup\n```\n\nFile-level edges are useful and should be preserved:",
  "metadata": {
    "chunk_index": 2,
    "file": "subsystem_docs/runtime_doctrine.md",
    "node_type": "doctrine",
    "source_id": "subsystem_docs/runtime_doctrine.md"
  },
  "node_type": "doctrine",
  "file": "subsystem_docs/runtime_doctrine.md"
}
```

### Text

```text
some areas
```

Persistence is mostly shutdown-oriented, with some on-demand/runtime save behavior.

Known major bottlenecks are not confirmed yet.

`SaveData`, `LoadData`, `PersistenceSave`, and related hooks should be treated as high-importance lifecycle hubs.

Future architecture should clarify:

```text
what saves when
what is authoritative
what can be async
what must be atomic
what can be rebuilt from runtime state
```

## Inventory Doctrine

Inventory synchronization has multiple separate channels:

- inventory metadata delta: nutInventoryData → InventoryDataChanged
- full inventory initialization: nutInventoryInit
- item membership delta: nutInventoryAdd / nutInventoryRemove
- item data delta: invData → ItemDataChanged

Item UI desync investigations must distinguish inventory.data from item.data.

Inventory is both server-side authoritative and client-visible through Derma/grid inventory.

Current behavior:

```text
items saved in DB
server stores authoritative information
client views/manipulates through UI
grid inventory / Derma represents state visually
```

Known pain point:

```text
UI desync
```

Inventory sync may be mixed between full refresh and partial/delta updates. This needs further inspection.

Inventory is a high-priority subsystem because it connects:

```text
items
storage
entities
networking
UI
persistence
commands
player actions
```

## Realm Doctrine

Realm responsibility is currently mixed but mostly server-side.

Long-term direction:

```text
server owns authoritative simulation and persistence
client owns presentation and UI
shared code should express contracts, not hide authority
networking should explicitly cross realm boundaries
```

Client prediction is not currently well understood or intentionally used. Future architecture should avoi...
```

## Result 6

- Score: **0.6652**
- Rerank score: `0.466824774`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:vendor:+0.05', 'doctrine_required:+0.16', 'file_subsystem:inventory:+0.07', 'causal:setdata:+0.18', 'causal:sync:+0.10', 'state_mutation_or_sync:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:31bbd827617dc491`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/ai_subsystems/inventory.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:31bbd827617dc491",
  "doc_type": "doctrine",
  "content_hash": "c821a6db62224a148e057f8ba70601bb1ac3e47694901d420af95832515a0f55",
  "embedding_dim": 384,
  "text": "# Synchronization Model\n\nCurrent understanding:\n\nSynchronization is performed through:\n\n```text\nInventory Rules\ngetData()\nsetData()\nnet\nnetstream\n```\n\nInventory behavior is tightly coupled with UI behavior.\n\nCurrent knowledge gap:\n\nFull synchronization path is not yet reconstructed.\n\nConfidence: Low\n\n---\n\n## Dependency Graph\n\nPrimary consumers:\n\n```text\nVendor\nStorage\nTying\nRagdollInteraction\nNeeds\n```\n\nObserved topology confirms inventory as a major dependency hub.\nConfidence: High\n\n---\n\n## Known Architectural Risks\n\n### UI / State Coupling\n\nInventory state and inventory presentation are closely coupled.\n\nExample:\n\nVendor pricing information may appear as UI metadata rather than authoritative item state.\n\nThis can create visual desynchronization without inventory corruption.\n\nConfidence: High\n\n---\n\n### Synchronization Complexity\n\nInventory uses:\n\n```text\nRules\nSlots\nItem Data\nNet Messages\nNetstream\n```\n\nacross:\n\n```text\nServer\nShared\nClient\n```\n\nThis creates a large synchronization surface area.\n\nConfidence: High\n\n---\n\n## Known Unknowns\n\nNot yet fully understood:\n\n* full inventory synchronization path\n* exact lifecycle ordering\n* NutScript internal inventory ownership model\n* UI initialization ordering\n* slot persistence implementation details\n\nThese areas require targeted source validation.\n\n---\n\n## Human Confidence Overlay\n\nStrong understanding:\n\n* SIGNALIS inventory plugin\n* slot architecture\n* inventory UI behavior\n\nWeak understanding:\n\n* NutScript internals\n* framework lifecycle\n* engine-level inventory behavior\n\nFuture investigations should prioritize source validation when entering these areas.\n\n---\n\n## Current Architecture Assessment\n\nInventory is not merely a storage system.\n\nInventory is a gameplay infrastructure subsystem.\n\nIt acts as the central coordination point for:\n\n```text\nItem Ownership\nEquipment\nVendor Interaction\nStorage Interaction\nLoot Interaction\nCharacter Equipment State\nInventory UI\n```",
  "metadata": {
    "chunk_index": 1,
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
# Synchronization Model

Current understanding:

Synchronization is performed through:

```text
Inventory Rules
getData()
setData()
net
netstream
```

Inventory behavior is tightly coupled with UI behavior.

Current knowledge gap:

Full synchronization path is not yet reconstructed.

Confidence: Low

---

## Dependency Graph

Primary consumers:

```text
Vendor
Storage
Tying
RagdollInteraction
Needs
```

Observed topology confirms inventory as a major dependency hub.
Confidence: High

---

## Known Architectural Risks

### UI / State Coupling

Inventory state and inventory presentation are closely coupled.

Example:

Vendor pricing information may appear as UI metadata rather than authoritative item state.

This can create visual desynchronization without inventory corruption.

Confidence: High

---

### Synchronization Complexity

Inventory uses:

```text
Rules
Slots
Item Data
Net Messages
Netstream
```

across:

```text
Server
Shared
Client
```

This creates a large synchronization surface area.

Confidence: High

---

## Known Unknowns

Not yet fully understood:

* full inventory synchronization path
* exact lifecycle ordering
* NutScript internal inventory ownership model
* UI initialization ordering
* slot persistence implementation details

These areas require targeted source validation.

---

## Human Confidence Overlay

Strong understanding:

* SIGNALIS inventory plugin
* slot architecture
* inventory UI behavior

Weak understanding:

* NutScript internals
* framework lifecycle
* engine-level inventory behavior

Future investigations should prioritize source validation when entering these areas.

---

## Current Architecture Assessment

Inventory is not merely a storage system.

Inventory is a gameplay infrastructure subsystem.

It acts as the central coordinatio...
```

## Result 7

- Score: **0.6431**
- Rerank score: `0.45607477999999996`
- Rerank reasons: `['doc_type:doctrine:+0.20', 'node_type:doctrine:+0.18', 'text_subsystem:inventory:+0.05', 'doctrine_required:+0.16', 'file_subsystem:inventory:+0.07', 'causal:sync:+0.10', 'causal:nutinventoryadd:+0.16', 'causal:nutinventoryremove:+0.14', 'realm_signal:+0.04']`
- Source ID: `doc:doctrine:b15bac403297b54b`
- Doc type: `doctrine`
- Subsystem: `None`
- File: `docs/subsystems/inventory.md`

### Metadata

```json
{
  "source_id": "doc:doctrine:b15bac403297b54b",
  "doc_type": "doctrine",
  "content_hash": "4bbf57292d0f7143971bd748b3eb498c7f436df363cb50ae5d9eccf89780209e",
  "embedding_dim": 384,
  "text": "ryRemove`: 1\n- `receive OpenMyInv`: 1\n- `netstream send inventoryOpen`: 1\n- `netstream hook inventoryCloseOnAction`: 1\n- `netstream hook mnhrOpenVisor`: 1\n- `netstream hook invAct`: 1\n- `send nutInventoryData`: 1\n- `receive nutInventoryRemove`: 1\n- `send nutInventoryAdd`: 1\n\n## Lifecycle Propagation\n\n- `listen PostPlayerLoadout @ plugins\\inventory\\sh_plugin.lua:689`: 2\n- `PostPlayerLoadout`: 2\n- `listen PostPlayerLoadout @ plugins\\inventory\\sh_plugin.lua:688`: 2\n- `emit PostPlayerLoadout @ gamemode\\core\\hooks\\sv_hooks.lua:367`: 2\n- `emit PlayerLoadout @ gamemode\\core\\hooks\\sv_hooks.lua:263`: 1\n- `emit PlayerLoadout @ gamemode\\core\\hooks\\sv_hooks.lua:219`: 1\n- `emit CharacterPreSave @ gamemode\\core\\meta\\sh_character.lua:42`: 1\n- `PlayerLoadout`: 1\n- `listen PlayerLoadout @ plugins\\inventory\\sh_plugin.lua:637`: 1\n- `CharacterPreSave`: 1\n- `listen CharacterPreSave @ plugins\\inventory\\sh_plugin.lua:718`: 1\n- `listen PlayerLoadout @ plugins\\inventory\\sh_plugin.lua:638`: 1\n- `listen CharacterPreSave @ plugins\\inventory\\sh_plugin.lua:719`: 1\n\n## Synchronization Hotspots\n\n- `netstream send inventorySetPanelStatus`: 10\n- `read ReadUInt nutInventoryInit`: 3\n- `write WriteUInt nutInventoryInit`: 3\n- `write WriteUInt nutTransferItem`: 3\n- `netstream send invAct`: 3\n- `write WriteTable nutInventoryInit`: 2\n- `read ReadTable nutInventoryInit`: 2\n- `send nutInventoryDelete`: 2\n- `write WriteString nutInventoryInit`: 2\n- `write WriteType nutInventoryDelete`: 2\n- `read ReadString nutInventoryInit`: 2\n- `netstream send storageInventory`: 2\n- `Start nutInventoryDelete`: 2\n- `Start nutTransferItem`: 1\n- `write WriteUInt nutInventoryRemove`: 1\n- `register nutInventoryRemove`: 1\n- `netstream send inventoryOpen`: 1\n- `write WriteType nutInventoryAdd`: 1\n- `read ReadType nutInventoryDelete`: 1\n- `netstream hook invAct`: 1\n\n## Important Timers\n\n- `player_action_timer@plugins\\inventory\\sv_hooks.lua:16`: 1\n- `player_cancelable_action_timer@plugins\\storage\\entities\\entities\\nut_storage\\init.lua:315`: 1\n- `timer_simple@plugins\\storage\\sv_storage.lua:149`: 1\n- `SetSimpleTimer`: 1\n- `player_cancelable_action_timer@plugins\\storage\\entities\\entities\\nut_storage\\init.lua:256`: 1\n- `player_action_timer`: 1\n- `setAction`: 1\n- `player_action_timer@plugins\\storage\\entities\\entities\\nut_storage\\init.lua:70`: 1\n- `player_cancelable_action_timer@plugins\\crafting\\entities\\entities\\nut_storage_kit\\init.lua:30`: 1\n- `entity_timer_simple@plugins\\inventory\\sv_hooks.lua:123`: 1\n- `timer_simple@plugins\\gridinv\\plugins\\1_1compat\\sh_plugin.lua:31`: 1\n- `entity_validity_guard_expected`: 1\n- `entity_simulation_timer`: 1\n- `player_cancelable_action_timer@plugins\\storage\\entities\\entities\\nut_storage\\init.lua:147`: 1\n\n## Realms\n\n- `server`: 65\n- `shared`: 54\n- `client`: 32\n\n## Major Files",
  "metadata": {
    "chunk_index": 1,
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
ryRemove`: 1
- `receive OpenMyInv`: 1
- `netstream send inventoryOpen`: 1
- `netstream hook inventoryCloseOnAction`: 1
- `netstream hook mnhrOpenVisor`: 1
- `netstream hook invAct`: 1
- `send nutInventoryData`: 1
- `receive nutInventoryRemove`: 1
- `send nutInventoryAdd`: 1

## Lifecycle Propagation

- `listen PostPlayerLoadout @ plugins\inventory\sh_plugin.lua:689`: 2
- `PostPlayerLoadout`: 2
- `listen PostPlayerLoadout @ plugins\inventory\sh_plugin.lua:688`: 2
- `emit PostPlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:367`: 2
- `emit PlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:263`: 1
- `emit PlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:219`: 1
- `emit CharacterPreSave @ gamemode\core\meta\sh_character.lua:42`: 1
- `PlayerLoadout`: 1
- `listen PlayerLoadout @ plugins\inventory\sh_plugin.lua:637`: 1
- `CharacterPreSave`: 1
- `listen CharacterPreSave @ plugins\inventory\sh_plugin.lua:718`: 1
- `listen PlayerLoadout @ plugins\inventory\sh_plugin.lua:638`: 1
- `listen CharacterPreSave @ plugins\inventory\sh_plugin.lua:719`: 1

## Synchronization Hotspots

- `netstream send inventorySetPanelStatus`: 10
- `read ReadUInt nutInventoryInit`: 3
- `write WriteUInt nutInventoryInit`: 3
- `write WriteUInt nutTransferItem`: 3
- `netstream send invAct`: 3
- `write WriteTable nutInventoryInit`: 2
- `read ReadTable nutInventoryInit`: 2
- `send nutInventoryDelete`: 2
- `write WriteString nutInventoryInit`: 2
- `write WriteType nutInventoryDelete`: 2
- `read ReadString nutInventoryInit`: 2
- `netstream send storageInventory`: 2
- `Start nutInventoryDelete`: 2
- `Start nutTransferItem`: 1
- `write WriteUInt nutInventoryRemove`: 1
- `register nutInventoryRemove`: 1
- `netstream send inventoryOpen`: 1
- `write WriteType nutInventoryAdd`: 1
- `read ReadType nutInventoryDelete`: 1...
```
