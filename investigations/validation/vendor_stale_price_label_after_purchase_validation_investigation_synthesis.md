# SIGNALIS AI — Investigation Synthesis

- Source: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_runtime_chains.json`
- Query: `vendor stale price label after purchase`
- Runtime chains: `5`
- Hypotheses: `4`

## Current Working Interpretation

The stale vendor price label issue is currently best modeled as a client presentation metadata / refresh-boundary problem, not as proven inventory ownership corruption.

Validated runtime shape:

```text
Vendor trade
→ server item metadata mutation
→ item:setData conditional sync/persistence boundary
→ client vendor Price handler
→ VendorItemPriceUpdated
→ vendor UI updatePrice

Vendor exit
→ RemoveReceiverFromVendor
→ vendor* metadata cleared with item:setData(nil)
→ conditional sync/persistence boundary
```

## Ranked Hypotheses

### 1. Cleanup sync does not reach or refresh the active client UI

- Confidence: `high`
- Related chains: `vendor_exit_metadata_cleanup, inventory_data_delta_sync`

The runtime chains show that vendor metadata is cleared server-side through RemoveReceiverFromVendor using item:setData(nil), while inventory data delta sync is a separate client receiver path. Human context says item:setData is conditional sync plus persistence. Therefore stale labels can occur if cleanup reaches server state but does not refresh the already-open client panels.

Validation targets:

- `gamemode/core/meta/inventory/cl_base_inventory.lua`
- `plugins/vendor/derma/cl_vendor.lua`
- `plugins/inventory/cl_hooks.lua`
- `plugins/vendor/entities/entities/nut_vendor/init.lua`

Falsification checks:

- If nutInventoryData always triggers an item panel redraw for the affected item.
- If vendor panel close always destroys all item panels before stale labels can persist.
- If vendor* metadata is not actually present on the player's purchased item clientside.

### 2. Price update path refreshes vendor UI, but not necessarily player inventory UI

- Confidence: `medium`
- Related chains: `vendor_price_update_ui_refresh, vendor_open_trade_interface`

The price update chain ends in cl_vendor.lua updatePrice. The open flow creates two panels: player inventory through CreateNewInventoryPanel and vendor inventory through vendor_grid_inventory. The validated price refresh path may only refresh vendor UI panels, not the player inventory panel after the item is moved/purchased.

Validation targets:

- `plugins/vendor/derma/cl_vendor.lua`
- `plugins/inventory/cl_hooks.lua`
- `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`

Falsification checks:

- If updatePrice is called for both vendor_grid_inventory and player inventory item panels.
- If purchased item panel is reconstructed immediately after trade.
- If player inventory panel ignores vendor* metadata entirely.

### 3. Receiver ownership mismatch during item:setData cleanup

- Confidence: `medium`
- Related chains: `vendor_exit_metadata_cleanup`

Cleanup uses item:setData with a client/receiver argument. Human context confirms setData sync depends on receivers/current owner. If the purchased item has already moved to another inventory/owner context, the cleanup sync may target the wrong receiver or miss the active panel state.

Validation targets:

- `plugins/vendor/entities/entities/nut_vendor/init.lua`
- `gamemode/core/libs/item/sv_item.lua`
- `gamemode/core/meta/inventory/sv_base_inventory.lua`
- `gamemode/core/meta/inventory/cl_base_inventory.lua`

Falsification checks:

- If cleanup is always sent to the actual current owner of every affected item.
- If purchased item metadata is cleared before ownership transfer.
- If client item data receiver updates all inventory instances globally by item ID.

### 4. Storage movement forces broader panel reconstruction or item data refresh

- Confidence: `low`
- Related chains: `storage_refresh_recovery_path`

Human observation says moving the item through storage can clear the stale label. The chain currently only proves a storage/vendor UI path exists; it does not yet prove the exact refresh boundary. This is useful as a comparison path, not a confirmed cause.

Validation targets:

- `plugins/storage/cl_networking.lua`
- `plugins/inventory/cl_hooks.lua`
- `plugins/gridinv/plugins/gridstorage/sh_plugin.lua`
- `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`

Falsification checks:

- If storage movement does not reconstruct the affected item panel.
- If storage movement does not trigger item data resync.
- If recovery is caused by vendor exit rather than storage transfer.

## Next Source Validation Targets

### `gamemode/core/meta/inventory/cl_base_inventory.lua`

- Priority: `high`
- Reason: Needed for: Cleanup sync does not reach or refresh the active client UI; Receiver ownership mismatch during item:setData cleanup
- Look for:
  - Validate hypothesis: Cleanup sync does not reach or refresh the active client UI
  - Identify exact emitter/listener/network/state mutation relationship.
  - Check whether UI panel refresh happens after item data changes.
  - Validate hypothesis: Receiver ownership mismatch during item:setData cleanup

### `plugins/inventory/cl_hooks.lua`

- Priority: `high`
- Reason: Needed for: Cleanup sync does not reach or refresh the active client UI; Price update path refreshes vendor UI, but not necessarily player inventory UI; Storage movement forces broader panel reconstruction or item data refresh
- Look for:
  - Validate hypothesis: Cleanup sync does not reach or refresh the active client UI
  - Identify exact emitter/listener/network/state mutation relationship.
  - Check whether UI panel refresh happens after item data changes.
  - Validate hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI
  - Validate hypothesis: Storage movement forces broader panel reconstruction or item data refresh

### `plugins/vendor/derma/cl_vendor.lua`

- Priority: `high`
- Reason: Needed for: Cleanup sync does not reach or refresh the active client UI; Price update path refreshes vendor UI, but not necessarily player inventory UI
- Look for:
  - Validate hypothesis: Cleanup sync does not reach or refresh the active client UI
  - Identify exact emitter/listener/network/state mutation relationship.
  - Check whether UI panel refresh happens after item data changes.
  - Validate hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI

### `plugins/vendor/entities/entities/nut_vendor/init.lua`

- Priority: `high`
- Reason: Needed for: Cleanup sync does not reach or refresh the active client UI; Receiver ownership mismatch during item:setData cleanup
- Look for:
  - Validate hypothesis: Cleanup sync does not reach or refresh the active client UI
  - Identify exact emitter/listener/network/state mutation relationship.
  - Check whether UI panel refresh happens after item data changes.
  - Validate hypothesis: Receiver ownership mismatch during item:setData cleanup

### `gamemode/core/libs/item/sv_item.lua`

- Priority: `medium`
- Reason: Needed for: Receiver ownership mismatch during item:setData cleanup
- Look for:
  - Validate hypothesis: Receiver ownership mismatch during item:setData cleanup
  - Identify exact emitter/listener/network/state mutation relationship.
  - Check whether UI panel refresh happens after item data changes.

### `gamemode/core/meta/inventory/sv_base_inventory.lua`

- Priority: `medium`
- Reason: Needed for: Receiver ownership mismatch during item:setData cleanup
- Look for:
  - Validate hypothesis: Receiver ownership mismatch during item:setData cleanup
  - Identify exact emitter/listener/network/state mutation relationship.
  - Check whether UI panel refresh happens after item data changes.

### `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`

- Priority: `medium`
- Reason: Needed for: Price update path refreshes vendor UI, but not necessarily player inventory UI; Storage movement forces broader panel reconstruction or item data refresh
- Look for:
  - Validate hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI
  - Identify exact emitter/listener/network/state mutation relationship.
  - Check whether UI panel refresh happens after item data changes.
  - Validate hypothesis: Storage movement forces broader panel reconstruction or item data refresh

### `plugins/gridinv/plugins/gridstorage/sh_plugin.lua`

- Priority: `medium`
- Reason: Needed for: Storage movement forces broader panel reconstruction or item data refresh
- Look for:
  - Validate hypothesis: Storage movement forces broader panel reconstruction or item data refresh
  - Identify exact emitter/listener/network/state mutation relationship.
  - Check whether UI panel refresh happens after item data changes.

### `plugins/storage/cl_networking.lua`

- Priority: `medium`
- Reason: Needed for: Storage movement forces broader panel reconstruction or item data refresh
- Look for:
  - Validate hypothesis: Storage movement forces broader panel reconstruction or item data refresh
  - Identify exact emitter/listener/network/state mutation relationship.
  - Check whether UI panel refresh happens after item data changes.

## Recommended Next Pipeline Step

Use this synthesis to generate targeted validation reports instead of broad retrieval.

Suggested next command pattern:

```powershell
python -m scripts.qdrant.validate_sources `
  --workspace E:/signalis_ai `
  --report investigations/generated/vendor_stale_price_label_after_purchase.md
```

Then compare validated source against the hypotheses above.
