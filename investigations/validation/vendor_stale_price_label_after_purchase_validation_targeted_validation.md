# SIGNALIS AI — Targeted Validation Plan

- Source synthesis: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_investigation_synthesis.json`
- Query: `vendor stale price label after purchase`
- Checks total: `15`

## Purpose

This report converts investigation hypotheses into exact source-validation checks.

Goal:

```text
hypotheses
→ target files
→ exact questions
→ required source patterns
→ validation/falsification
```

## Primary Failure Boundary

```text
item:setData cleanup / sync boundary
→ client inventory data delta
→ active item panel refresh
```

## Checks

### TV-001 — `gamemode/core/meta/inventory/cl_base_inventory.lua`

- Priority: `high`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Confidence: `high`
- Expected runtime relation: client inventory data delta receiver mutates local inventory/item data

Validation questions:

- What does nutInventoryData mutate on the client?
- Does nutInventoryData emit ItemDataChanged or another refresh event?
- Does item data update trigger existing item panel refresh?

Required source patterns:

- `ItemDataChanged`
- `RemoveReceiverFromVendor`
- `data`
- `invData`
- `net.Receive`
- `netstream.Hook`
- `nil`
- `nutInventoryData`
- `setData`
- `vendorSPrice`

Falsifies hypothesis if:

- If nutInventoryData always triggers an item panel redraw for the affected item.
- If vendor panel close always destroys all item panels before stale labels can persist.
- If vendor* metadata is not actually present on the player's purchased item clientside.

### TV-003 — `plugins/inventory/cl_hooks.lua`

- Priority: `high`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Confidence: `high`
- Expected runtime relation: client inventory/vendor interface constructs player inventory and vendor_grid_inventory panels

Validation questions:

- How exactly is vendorTradeInterface constructed?
- Which panel is the player inventory panel?
- Which panel is vendor_grid_inventory?
- Do either panels subscribe to item data changes?
- Does panel removal trigger removeReceiverFromVendor?

Required source patterns:

- `CreateNewInventoryPanel`
- `OnCreateStoragePanel`
- `OnRemove`
- `RemoveReceiverFromVendor`
- `SetUpPanel`
- `invData`
- `nil`
- `removeReceiverFromVendor`
- `vendorSPrice`
- `vendorTradeInterface`
- `vendor_grid_inventory`

Falsifies hypothesis if:

- If nutInventoryData always triggers an item panel redraw for the affected item.
- If vendor panel close always destroys all item panels before stale labels can persist.
- If vendor* metadata is not actually present on the player's purchased item clientside.

### TV-002 — `plugins/vendor/derma/cl_vendor.lua`

- Priority: `high`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Confidence: `high`
- Expected runtime relation: client vendor UI sends trade/exit and refreshes visible vendor price labels

Validation questions:

- Does vendor UI refresh only vendor-side item panels or also player inventory panels?
- Does closing/removing the vendor panel send the cleanup message reliably?
- Does updatePrice read vendor* metadata from item data?

Required source patterns:

- `OnRemove`
- `RemoveReceiverFromVendor`
- `VendorItemPriceUpdated`
- `hook.Add`
- `invData`
- `nil`
- `nutVendorExit`
- `nutVendorTrade`
- `onVendorPriceUpdated`
- `updatePrice`
- `vendorSPrice`

Falsifies hypothesis if:

- If nutInventoryData always triggers an item panel redraw for the affected item.
- If vendor panel close always destroys all item panels before stale labels can persist.
- If vendor* metadata is not actually present on the player's purchased item clientside.

### TV-004 — `plugins/vendor/entities/entities/nut_vendor/init.lua`

- Priority: `high`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Confidence: `high`
- Expected runtime relation: server vendor entity mutates/clears vendor item presentation metadata

Validation questions:

- Where is vendor presentation metadata created?
- Where is vendor presentation metadata cleared?
- Does cleanup happen before or after item ownership/inventory transfer?
- Which receiver/client is passed into item:setData during cleanup?

Required source patterns:

- `OpenVendorTradeInterface`
- `RemoveReceiverFromVendor`
- `VendorItemSetData`
- `invData`
- `netstream.Start`
- `nil`
- `setData`
- `vendorBPrice`
- `vendorMQty`
- `vendorQty`
- `vendorSPrice`

Falsifies hypothesis if:

- If nutInventoryData always triggers an item panel redraw for the affected item.
- If vendor panel close always destroys all item panels before stale labels can persist.
- If vendor* metadata is not actually present on the player's purchased item clientside.

### TV-009 — `gamemode/core/libs/item/sv_item.lua`

- Priority: `medium`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Confidence: `medium`
- Expected runtime relation: server item data mutation persists and conditionally syncs item data

Validation questions:

- What receivers does ITEM:setData use by default?
- Does setData send invData immediately?
- Does noSave/noCheckEntity affect persistence or network sync?

Required source patterns:

- `ITEM:setData`
- `client`
- `getOwner`
- `invData`
- `netstream.Start`
- `nut.db.updateTable`
- `owner`
- `receiver`
- `receivers`
- `setData`
- `setNetVar`

Falsifies hypothesis if:

- If cleanup is always sent to the actual current owner of every affected item.
- If purchased item metadata is cleared before ownership transfer.
- If client item data receiver updates all inventory instances globally by item ID.

### TV-011 — `gamemode/core/meta/inventory/cl_base_inventory.lua`

- Priority: `medium`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Confidence: `medium`
- Expected runtime relation: client inventory data delta receiver mutates local inventory/item data

Validation questions:

- What does nutInventoryData mutate on the client?
- Does nutInventoryData emit ItemDataChanged or another refresh event?
- Does item data update trigger existing item panel refresh?

Required source patterns:

- `ItemDataChanged`
- `client`
- `data`
- `getOwner`
- `net.Receive`
- `netstream.Hook`
- `nutInventoryData`
- `owner`
- `receiver`
- `receivers`
- `setData`

Falsifies hypothesis if:

- If cleanup is always sent to the actual current owner of every affected item.
- If purchased item metadata is cleared before ownership transfer.
- If client item data receiver updates all inventory instances globally by item ID.

### TV-010 — `gamemode/core/meta/inventory/sv_base_inventory.lua`

- Priority: `medium`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Confidence: `medium`
- Expected runtime relation: server inventory ownership/transfer/sync boundary

Validation questions:

- How does server inventory transfer change item ownership?
- Are receivers updated before or after item data cleanup?
- Does inventory sync resend full item data after transfers?

Required source patterns:

- `addItem`
- `client`
- `getOwner`
- `getReceivers`
- `invData`
- `netstream.Start`
- `owner`
- `receiver`
- `receivers`
- `removeItem`
- `setData`
- `sync`

Falsifies hypothesis if:

- If cleanup is always sent to the actual current owner of every affected item.
- If purchased item metadata is cleared before ownership transfer.
- If client item data receiver updates all inventory instances globally by item ID.

### TV-007 — `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`

- Priority: `medium`
- Hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI
- Confidence: `medium`
- Expected runtime relation: client grid inventory panel renders or refreshes item presentation metadata

Validation questions:

- Does grid inventory panel redraw when item data changes?
- Does it cache vendor price labels?
- Does it read vendorSPrice/vendorBPrice during paint or only on construction?

Required source patterns:

- `CreateNewInventoryPanel`
- `ItemDataChanged`
- `Paint`
- `SetUpPanel`
- `getData`
- `refresh`
- `update`
- `updatePrice`
- `vendorBPrice`
- `vendorSPrice`
- `vendor_grid_inventory`

Falsifies hypothesis if:

- If updatePrice is called for both vendor_grid_inventory and player inventory item panels.
- If purchased item panel is reconstructed immediately after trade.
- If player inventory panel ignores vendor* metadata entirely.

### TV-006 — `plugins/inventory/cl_hooks.lua`

- Priority: `medium`
- Hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI
- Confidence: `medium`
- Expected runtime relation: client inventory/vendor interface constructs player inventory and vendor_grid_inventory panels

Validation questions:

- How exactly is vendorTradeInterface constructed?
- Which panel is the player inventory panel?
- Which panel is vendor_grid_inventory?
- Do either panels subscribe to item data changes?
- Does panel removal trigger removeReceiverFromVendor?

Required source patterns:

- `CreateNewInventoryPanel`
- `OnCreateStoragePanel`
- `OnRemove`
- `SetUpPanel`
- `getData`
- `removeReceiverFromVendor`
- `updatePrice`
- `vendorTradeInterface`
- `vendor_grid_inventory`

Falsifies hypothesis if:

- If updatePrice is called for both vendor_grid_inventory and player inventory item panels.
- If purchased item panel is reconstructed immediately after trade.
- If player inventory panel ignores vendor* metadata entirely.

### TV-005 — `plugins/vendor/derma/cl_vendor.lua`

- Priority: `medium`
- Hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI
- Confidence: `medium`
- Expected runtime relation: client vendor UI sends trade/exit and refreshes visible vendor price labels

Validation questions:

- Does vendor UI refresh only vendor-side item panels or also player inventory panels?
- Does closing/removing the vendor panel send the cleanup message reliably?
- Does updatePrice read vendor* metadata from item data?

Required source patterns:

- `CreateNewInventoryPanel`
- `OnRemove`
- `VendorItemPriceUpdated`
- `getData`
- `hook.Add`
- `nutVendorExit`
- `nutVendorTrade`
- `onVendorPriceUpdated`
- `updatePrice`
- `vendor_grid_inventory`

Falsifies hypothesis if:

- If updatePrice is called for both vendor_grid_inventory and player inventory item panels.
- If purchased item panel is reconstructed immediately after trade.
- If player inventory panel ignores vendor* metadata entirely.

### TV-008 — `plugins/vendor/entities/entities/nut_vendor/init.lua`

- Priority: `medium`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Confidence: `medium`
- Expected runtime relation: server vendor entity mutates/clears vendor item presentation metadata

Validation questions:

- Where is vendor presentation metadata created?
- Where is vendor presentation metadata cleared?
- Does cleanup happen before or after item ownership/inventory transfer?
- Which receiver/client is passed into item:setData during cleanup?

Required source patterns:

- `OpenVendorTradeInterface`
- `RemoveReceiverFromVendor`
- `VendorItemSetData`
- `client`
- `getOwner`
- `netstream.Start`
- `owner`
- `receiver`
- `receivers`
- `setData`
- `vendorBPrice`
- `vendorMQty`
- `vendorQty`
- `vendorSPrice`

Falsifies hypothesis if:

- If cleanup is always sent to the actual current owner of every affected item.
- If purchased item metadata is cleared before ownership transfer.
- If client item data receiver updates all inventory instances globally by item ID.

### TV-015 — `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`

- Priority: `low`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Confidence: `low`
- Expected runtime relation: client grid inventory panel renders or refreshes item presentation metadata

Validation questions:

- Does grid inventory panel redraw when item data changes?
- Does it cache vendor price labels?
- Does it read vendorSPrice/vendorBPrice during paint or only on construction?

Required source patterns:

- `ItemDataChanged`
- `Paint`
- `SetUpPanel`
- `getData`
- `refresh`
- `update`
- `vendorBPrice`
- `vendorSPrice`

Falsifies hypothesis if:

- If storage movement does not reconstruct the affected item panel.
- If storage movement does not trigger item data resync.
- If recovery is caused by vendor exit rather than storage transfer.

### TV-014 — `plugins/gridinv/plugins/gridstorage/sh_plugin.lua`

- Priority: `low`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Confidence: `low`
- Expected runtime relation: storage movement may reconstruct panels or force broader item sync

Validation questions:

- Does storage movement reconstruct item panels?
- Does storage movement force full inventory data resync?
- What refresh boundary explains observed stale-label recovery?

Required source patterns:

- `ItemDataChanged`
- `OnCreateStoragePanel`
- `SetUpPanel`
- `StorageOpen`
- `refresh`
- `storageInventory`

Falsifies hypothesis if:

- If storage movement does not reconstruct the affected item panel.
- If storage movement does not trigger item data resync.
- If recovery is caused by vendor exit rather than storage transfer.

### TV-013 — `plugins/inventory/cl_hooks.lua`

- Priority: `low`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Confidence: `low`
- Expected runtime relation: client inventory/vendor interface constructs player inventory and vendor_grid_inventory panels

Validation questions:

- How exactly is vendorTradeInterface constructed?
- Which panel is the player inventory panel?
- Which panel is vendor_grid_inventory?
- Do either panels subscribe to item data changes?
- Does panel removal trigger removeReceiverFromVendor?

Required source patterns:

- `CreateNewInventoryPanel`
- `OnCreateStoragePanel`
- `OnRemove`
- `SetUpPanel`
- `removeReceiverFromVendor`
- `vendorTradeInterface`
- `vendor_grid_inventory`

Falsifies hypothesis if:

- If storage movement does not reconstruct the affected item panel.
- If storage movement does not trigger item data resync.
- If recovery is caused by vendor exit rather than storage transfer.

### TV-012 — `plugins/storage/cl_networking.lua`

- Priority: `low`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Confidence: `low`
- Expected runtime relation: storage movement may reconstruct panels or force broader item sync

Validation questions:

- Does storage movement reconstruct item panels?
- Does storage movement force full inventory data resync?
- What refresh boundary explains observed stale-label recovery?

Required source patterns:

- `ItemDataChanged`
- `OnCreateStoragePanel`
- `SetUpPanel`
- `StorageOpen`
- `refresh`
- `storageInventory`

Falsifies hypothesis if:

- If storage movement does not reconstruct the affected item panel.
- If storage movement does not trigger item data resync.
- If recovery is caused by vendor exit rather than storage transfer.

## Suggested Next Command

```powershell
python -m scripts.qdrant.validate_sources `
  --workspace E:/signalis_ai `
  --report investigations/validation/vendor_stale_price_label_after_purchase_validation_targeted_validation.md
```
