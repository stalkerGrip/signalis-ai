# SIGNALIS AI — Targeted Validation Plan

- Source synthesis: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_investigation_synthesis.json`
- Query: `vendor stale price label after purchase`
- Checks total: `15`

## Purpose

Convert investigation hypotheses into exact source-validation checks.

## Summary

```json
{
  "checks_total": 15,
  "by_priority": {
    "high": 4,
    "medium": 7,
    "low": 4
  },
  "by_role": {
    "client_inventory_hooks": 3,
    "client_inventory": 2,
    "legacy_or_vendor_trade_ui": 2,
    "server_vendor_entity": 2,
    "client_grid_panel": 2,
    "server_inventory": 1,
    "server_item_data": 1,
    "grid_storage_ui": 1,
    "storage_client_networking": 1
  },
  "by_file": {
    "plugins/inventory/cl_hooks.lua": 3,
    "gamemode/core/meta/inventory/cl_base_inventory.lua": 2,
    "plugins/vendor/derma/cl_vendor.lua": 2,
    "plugins/vendor/entities/entities/nut_vendor/init.lua": 2,
    "plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua": 2,
    "gamemode/core/meta/inventory/sv_base_inventory.lua": 1,
    "gamemode/core/meta/item/sv_item.lua": 1,
    "plugins/gridinv/plugins/gridstorage/sh_plugin.lua": 1,
    "plugins/storage/cl_networking.lua": 1
  }
}
```

## Checks

### TV-001 — `gamemode/core/meta/inventory/cl_base_inventory.lua`

- Priority: `high`
- Semantic role: `client_inventory`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Confidence: `high`
- Expected runtime relation: client inventory membership/data receiver boundary

Validation questions:

- Validate the exact runtime relation for this semantic role.

Required source patterns:

- `"invData"`
- `InventoryItemDataChanged`
- `hook.Run("InventoryDataChanged"`
- `hook.Run("InventoryItemAdded"`
- `hook.Run("InventoryItemRemoved"`
- `item:setData("vendorSPrice", nil`
- `net.Receive("nutInventoryAdd"`
- `net.Receive("nutInventoryData"`
- `net.Receive("nutInventoryRemove"`
- `self:populateItems()`

Falsifies hypothesis if:

- If nutInventoryData always triggers an item panel redraw for the affected item.
- If vendor panel close always destroys all item panels before stale labels can persist.
- If vendor* metadata is not actually present on the player's purchased item clientside.

### TV-003 — `plugins/inventory/cl_hooks.lua`

- Priority: `high`
- Semantic role: `client_inventory_hooks`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Confidence: `high`
- Expected runtime relation: client inventory/vendor interface construction and close cleanup boundary

Validation questions:

- How is the vendor trade interface built?
- Which panel is player inventory and which is vendor inventory?
- Does close/removal trigger removeReceiverFromVendor?

Required source patterns:

- `"invData"`
- `InventoryItemDataChanged`
- `PLUGIN:CreateNewInventoryPanel`
- `hook.Run("OnCreateStoragePanel"`
- `item:setData("vendorSPrice", nil`
- `netstream.Hook("vendorTradeInterface"`
- `netstream.Start("inventorySetPanelStatus"`
- `netstream.Start("removeReceiverFromVendor"`
- `self:populateItems()`
- `storageInvPanel:SetUpPanel(loadedInv)`
- `vgui.Create("vendor_grid_inventory")`

Falsifies hypothesis if:

- If nutInventoryData always triggers an item panel redraw for the affected item.
- If vendor panel close always destroys all item panels before stale labels can persist.
- If vendor* metadata is not actually present on the player's purchased item clientside.

### TV-002 — `plugins/vendor/derma/cl_vendor.lua`

- Priority: `high`
- Semantic role: `legacy_or_vendor_trade_ui`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Confidence: `high`
- Expected runtime relation: vendor trade UI price hooks and trade/exit messages

Validation questions:

- Validate the exact runtime relation for this semantic role.

Required source patterns:

- `"invData"`
- `InventoryItemDataChanged`
- `function PANEL:onVendorPriceUpdated`
- `hook.Add("VendorItemPriceUpdated"`
- `item:setData("vendorSPrice", nil`
- `net.Start("nutVendorExit")`
- `net.Start("nutVendorTrade")`
- `panel:updatePrice()`
- `self:populateItems()`

Falsifies hypothesis if:

- If nutInventoryData always triggers an item panel redraw for the affected item.
- If vendor panel close always destroys all item panels before stale labels can persist.
- If vendor* metadata is not actually present on the player's purchased item clientside.

### TV-004 — `plugins/vendor/entities/entities/nut_vendor/init.lua`

- Priority: `high`
- Semantic role: `server_vendor_entity`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Confidence: `high`
- Expected runtime relation: server vendor entity creates/clears vendor item presentation metadata

Validation questions:

- Validate the exact runtime relation for this semantic role.

Required source patterns:

- `"invData"`
- `InventoryItemDataChanged`
- `function ENT:RemoveReceiverFromVendor`
- `function ENT:VendorItemSetData`
- `hook.Run("OpenVendorTradeInterface"`
- `item:setData("vendorMQty"`
- `item:setData("vendorQty"`
- `item:setData("vendorSPrice"`
- `item:setData("vendorSPrice", nil`
- `self:populateItems()`
- `v:setData("vendorBPrice", nil`
- `v:setData("vendorMQty", nil`
- `v:setData("vendorQty", nil`
- `v:setData("vendorSPrice", nil`

Falsifies hypothesis if:

- If nutInventoryData always triggers an item panel redraw for the affected item.
- If vendor panel close always destroys all item panels before stale labels can persist.
- If vendor* metadata is not actually present on the player's purchased item clientside.

### TV-007 — `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`

- Priority: `medium`
- Semantic role: `client_grid_panel`
- Hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI
- Confidence: `medium`
- Expected runtime relation: client grid panel refreshes item icons when item data changes

Validation questions:

- Does item data change call populateItems?
- Does panel reconstruction remove stale icon presentation state?
- Does the panel read vendor price data only during icon creation?

Required source patterns:

- `InventoryItemDataChanged`
- `PLUGIN:CreateNewInventoryPanel`
- `function PANEL:InventoryItemDataChanged`
- `function PANEL:InventoryItemRemoved`
- `function PANEL:addItem`
- `item:getData("x")`
- `item:getData("y")`
- `panel:updatePrice()`
- `self:populateItems()`
- `vgui.Create("vendor_grid_inventory")`

Falsifies hypothesis if:

- If updatePrice is called for both vendor_grid_inventory and player inventory item panels.
- If purchased item panel is reconstructed immediately after trade.
- If player inventory panel ignores vendor* metadata entirely.

### TV-011 — `gamemode/core/meta/inventory/cl_base_inventory.lua`

- Priority: `medium`
- Semantic role: `client_inventory`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Confidence: `medium`
- Expected runtime relation: client inventory membership/data receiver boundary

Validation questions:

- Validate the exact runtime relation for this semantic role.

Required source patterns:

- `"invData"`
- `hook.Run("InventoryDataChanged"`
- `hook.Run("InventoryItemAdded"`
- `hook.Run("InventoryItemRemoved"`
- `item:sync(recipients)`
- `local recipients = self:getRecipients()`
- `net.Receive("nutInventoryAdd"`
- `net.Receive("nutInventoryData"`
- `net.Receive("nutInventoryRemove"`
- `netstream.Start`
- `self:getOwner`

Falsifies hypothesis if:

- If cleanup is always sent to the actual current owner of every affected item.
- If purchased item metadata is cleared before ownership transfer.
- If client item data receiver updates all inventory instances globally by item ID.

### TV-006 — `plugins/inventory/cl_hooks.lua`

- Priority: `medium`
- Semantic role: `client_inventory_hooks`
- Hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI
- Confidence: `medium`
- Expected runtime relation: client inventory/vendor interface construction and close cleanup boundary

Validation questions:

- How is the vendor trade interface built?
- Which panel is player inventory and which is vendor inventory?
- Does close/removal trigger removeReceiverFromVendor?

Required source patterns:

- `InventoryItemDataChanged`
- `PLUGIN:CreateNewInventoryPanel`
- `hook.Run("OnCreateStoragePanel"`
- `netstream.Hook("vendorTradeInterface"`
- `netstream.Start("inventorySetPanelStatus"`
- `netstream.Start("removeReceiverFromVendor"`
- `panel:updatePrice()`
- `storageInvPanel:SetUpPanel(loadedInv)`
- `vgui.Create("vendor_grid_inventory")`

Falsifies hypothesis if:

- If updatePrice is called for both vendor_grid_inventory and player inventory item panels.
- If purchased item panel is reconstructed immediately after trade.
- If player inventory panel ignores vendor* metadata entirely.

### TV-005 — `plugins/vendor/derma/cl_vendor.lua`

- Priority: `medium`
- Semantic role: `legacy_or_vendor_trade_ui`
- Hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI
- Confidence: `medium`
- Expected runtime relation: vendor trade UI price hooks and trade/exit messages

Validation questions:

- Validate the exact runtime relation for this semantic role.

Required source patterns:

- `InventoryItemDataChanged`
- `PLUGIN:CreateNewInventoryPanel`
- `function PANEL:onVendorPriceUpdated`
- `hook.Add("VendorItemPriceUpdated"`
- `net.Start("nutVendorExit")`
- `net.Start("nutVendorTrade")`
- `panel:updatePrice()`
- `vgui.Create("vendor_grid_inventory")`

Falsifies hypothesis if:

- If updatePrice is called for both vendor_grid_inventory and player inventory item panels.
- If purchased item panel is reconstructed immediately after trade.
- If player inventory panel ignores vendor* metadata entirely.

### TV-010 — `gamemode/core/meta/inventory/sv_base_inventory.lua`

- Priority: `medium`
- Semantic role: `server_inventory`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Confidence: `medium`
- Expected runtime relation: server inventory ownership and recipient sync boundary

Validation questions:

- When item ownership changes, which recipients receive item sync?
- Does addItem call item:sync before nutInventoryAdd?
- Does transfer update recipients before item data cleanup?

Required source patterns:

- `"invData"`
- `function Inventory:addItem`
- `function Inventory:getRecipients`
- `function Inventory:removeItem`
- `function Inventory:syncItemAdded`
- `item:sync(recipients)`
- `local recipients = self:getRecipients()`
- `net.Send(recipients)`
- `net.Start("nutInventoryAdd")`
- `netstream.Start`
- `self:getOwner`

Falsifies hypothesis if:

- If cleanup is always sent to the actual current owner of every affected item.
- If purchased item metadata is cleared before ownership transfer.
- If client item data receiver updates all inventory instances globally by item ID.

### TV-009 — `gamemode/core/meta/item/sv_item.lua`

- Priority: `medium`
- Semantic role: `server_item_data`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Confidence: `medium`
- Expected runtime relation: server item data mutation persists and conditionally syncs item data through invData

Validation questions:

- Does ITEM:setData persist item metadata?
- Does ITEM:setData immediately emit invData?
- Which receiver path is used when explicit receivers are passed?
- What happens if explicit receiver is stale or wrong?

Required source patterns:

- `"invData"`
- `function ITEM:setData`
- `item:sync(recipients)`
- `local recipients = self:getRecipients()`
- `netstream.Start`
- `nut.db.updateTable`
- `self.data[key] = value`
- `self:getOwner`
- `self:setNetVar`

Falsifies hypothesis if:

- If cleanup is always sent to the actual current owner of every affected item.
- If purchased item metadata is cleared before ownership transfer.
- If client item data receiver updates all inventory instances globally by item ID.

### TV-008 — `plugins/vendor/entities/entities/nut_vendor/init.lua`

- Priority: `medium`
- Semantic role: `server_vendor_entity`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Confidence: `medium`
- Expected runtime relation: server vendor entity creates/clears vendor item presentation metadata

Validation questions:

- Validate the exact runtime relation for this semantic role.

Required source patterns:

- `"invData"`
- `function ENT:RemoveReceiverFromVendor`
- `function ENT:VendorItemSetData`
- `hook.Run("OpenVendorTradeInterface"`
- `item:setData("vendorMQty"`
- `item:setData("vendorQty"`
- `item:setData("vendorSPrice"`
- `item:sync(recipients)`
- `local recipients = self:getRecipients()`
- `netstream.Start`
- `self:getOwner`
- `v:setData("vendorBPrice", nil`
- `v:setData("vendorMQty", nil`
- `v:setData("vendorQty", nil`
- `v:setData("vendorSPrice", nil`

Falsifies hypothesis if:

- If cleanup is always sent to the actual current owner of every affected item.
- If purchased item metadata is cleared before ownership transfer.
- If client item data receiver updates all inventory instances globally by item ID.

### TV-015 — `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`

- Priority: `low`
- Semantic role: `client_grid_panel`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Confidence: `low`
- Expected runtime relation: client grid panel refreshes item icons when item data changes

Validation questions:

- Does item data change call populateItems?
- Does panel reconstruction remove stale icon presentation state?
- Does the panel read vendor price data only during icon creation?

Required source patterns:

- `OnCreateStoragePanel`
- `SetUpPanel`
- `StorageOpen`
- `function PANEL:InventoryItemDataChanged`
- `function PANEL:InventoryItemRemoved`
- `function PANEL:addItem`
- `item:getData("x")`
- `item:getData("y")`
- `self:populateItems()`

Falsifies hypothesis if:

- If storage movement does not reconstruct the affected item panel.
- If storage movement does not trigger item data resync.
- If recovery is caused by vendor exit rather than storage transfer.

### TV-013 — `plugins/inventory/cl_hooks.lua`

- Priority: `low`
- Semantic role: `client_inventory_hooks`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Confidence: `low`
- Expected runtime relation: client inventory/vendor interface construction and close cleanup boundary

Validation questions:

- How is the vendor trade interface built?
- Which panel is player inventory and which is vendor inventory?
- Does close/removal trigger removeReceiverFromVendor?

Required source patterns:

- `OnCreateStoragePanel`
- `PLUGIN:CreateNewInventoryPanel`
- `SetUpPanel`
- `StorageOpen`
- `hook.Run("OnCreateStoragePanel"`
- `netstream.Hook("vendorTradeInterface"`
- `netstream.Start("inventorySetPanelStatus"`
- `netstream.Start("removeReceiverFromVendor"`
- `self:populateItems()`
- `storageInvPanel:SetUpPanel(loadedInv)`
- `vgui.Create("vendor_grid_inventory")`

Falsifies hypothesis if:

- If storage movement does not reconstruct the affected item panel.
- If storage movement does not trigger item data resync.
- If recovery is caused by vendor exit rather than storage transfer.

### TV-014 — `plugins/gridinv/plugins/gridstorage/sh_plugin.lua`

- Priority: `low`
- Semantic role: `grid_storage_ui`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Confidence: `low`
- Expected runtime relation: grid storage UI construction and panel pairing boundary

Validation questions:

- Validate the exact runtime relation for this semantic role.

Required source patterns:

- `OnCreateStoragePanel`
- `SetUpPanel`
- `StorageOpen`
- `hook.Run("StorageOpen"`
- `inventorySetPanelStatus`
- `self:populateItems()`

Falsifies hypothesis if:

- If storage movement does not reconstruct the affected item panel.
- If storage movement does not trigger item data resync.
- If recovery is caused by vendor exit rather than storage transfer.

### TV-012 — `plugins/storage/cl_networking.lua`

- Priority: `low`
- Semantic role: `storage_client_networking`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Confidence: `low`
- Expected runtime relation: storage open/exit network boundary

Validation questions:

- Validate the exact runtime relation for this semantic role.

Required source patterns:

- `OnCreateStoragePanel`
- `SetUpPanel`
- `StorageOpen`
- `hook.Run("StorageOpen"`
- `inventorySetPanelStatus`
- `self:populateItems()`

Falsifies hypothesis if:

- If storage movement does not reconstruct the affected item panel.
- If storage movement does not trigger item data resync.
- If recovery is caused by vendor exit rather than storage transfer.

## Suggested Next Command

```powershell
python -m scripts.qdrant.validate_targeted_sources `
  --workspace E:/signalis_ai `
  --workspace-config workspace.yaml `
  --targeted investigations/validation/vendor_stale_price_label_after_purchase_validation_targeted_validation.json
```
