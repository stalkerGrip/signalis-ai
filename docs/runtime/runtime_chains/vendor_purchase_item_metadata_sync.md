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
→ server sends full item state to recipients
→ server sends nutInventoryAdd membership delta
→ client receives nutInventoryAdd
→ client emits InventoryItemAdded
→ server clears vendor metadata on purchased item
→ ITEM:setData mutates authoritative item data
→ server sends invData item-data delta
→ client receives invData item-data delta
→ client emits ItemDataChanged
→ grid inventory panel handles item-data change
→ grid inventory panel repopulates item icons
```

## Representative Evidence

### vendor_purchase_detection

- File: `plugins/gridinv/sv_transfer.lua`
- Lines: `116-128`
- Pattern: `vendorSellItem`
- Score: `145`

### inventory_boundary_transfer

- File: `plugins/gridinv/sv_transfer.lua`
- Lines: `1-11`
- Pattern: `oldInventory + destination inventory`
- Score: `134`

### inventory_membership_mutation

- File: `plugins/gridinv/sv_transfer.lua`
- Lines: `116-128`
- Pattern: `remove/add item transfer`
- Score: `113`

### inventory_recipients_resolved

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Lines: `193-205`
- Pattern: `self:getRecipients()`
- Score: `104`

### item_full_state_sync

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Lines: `41-53`
- Pattern: `item:sync(recipients)`
- Score: `118`

### inventory_membership_network_send

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Lines: `35-47`
- Pattern: `Inventory:syncItemAdded`
- Score: `120`

### inventory_membership_receive_add

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Lines: `50-62`
- Pattern: `net.Receive("nutInventoryAdd")`
- Score: `120`

### inventory_membership_client_event

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Lines: `57-69`
- Pattern: `hook.Run("InventoryItemAdded")`
- Score: `115`

### vendor_metadata_cleanup

- File: `plugins/gridinv/sv_transfer.lua`
- Lines: `207-219`
- Pattern: `item:setData("vendorSPrice", nil`
- Score: `150`

### item_metadata_mutation

- File: `gamemode/core/meta/item/sv_item.lua`
- Lines: `154-166`
- Pattern: `function ITEM:setData`
- Score: `130`

### item_metadata_network_sync_send

- File: `gamemode/core/meta/item/sv_item.lua`
- Lines: `165-177`
- Pattern: `invData`
- Score: `130`

### item_metadata_network_receive

- File: `gamemode/core/libs/item/cl_networking.lua`
- Lines: `12-24`
- Pattern: `netstream.Hook("invData")`
- Score: `140`

### item_metadata_client_event

- File: `gamemode/core/libs/item/cl_networking.lua`
- Lines: `12-24`
- Pattern: `hook.Run("ItemDataChanged")`
- Score: `140`

### gridinv_item_ui_refresh

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Lines: `265-277`
- Pattern: `PANEL:InventoryItemDataChanged`
- Score: `125`

### gridinv_panel_repopulate

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Lines: `261-273`
- Pattern: `self:populateItems()`
- Score: `120`

### item_metadata_persistence

- File: `gamemode/core/meta/item/sv_item.lua`
- Lines: `154-166`
- Pattern: `database/noSave behavior`
- Score: `50`

### inventory_level_data_not_item_data

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Lines: `1-9`
- Pattern: `nutInventoryData / InventoryDataChanged`
- Score: `30`

## Promotion Notes

Promote this document to Qdrant/retrieval corpus only after the chain is source-validated and reviewed.
Do not promote speculative or partial chains as authoritative subsystem knowledge.
