# SIGNALIS AI — Runtime Chains

- Source: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_runtime_facts.json`
- Query: `vendor stale price label after purchase`
- Facts total: `63`
- Chains total: `5`

## Interpretation

This report is built from runtime facts, not raw semantic similarity.

Human-validated rules included:

- `item:setData` is persistent item metadata mutation plus conditional sync boundary.
- Vendor open flow is `OpenVendorTradeInterface → vendorTradeInterface → CreateNewInventoryPanel → vendor_grid_inventory and CreateNewInventoryPanel`.
- Vendor price labels are UI/presentation metadata, not authoritative item ownership.

## Vendor Open / Trade Interface Construction

- Chain ID: `vendor_open_trade_interface`
- Confidence: `high`
- Reason: human-validated flow plus runtime facts

### Steps

1. `player_interaction` / `Player interacts with vendor`
   - Realm: `runtime`
   - Source: `human_context.md`
   - Confidence: `human_validated`
   - Reason: human-validated vendor open flow

2. `server_event_or_call` / `OpenVendorTradeInterface`
   - Realm: `runtime`
   - Source: `human_context.md`
   - Confidence: `human_validated`
   - Reason: server calls/emits OpenVendorTradeInterface before client vendor UI opens

3. `network_receive` / `vendorTradeInterface`
   - Realm: `client`
   - Source: `plugins/inventory/cl_hooks.lua:101-141`
   - Confidence: `high`
   - Reason: client receives vendorTradeInterface

4. `ui_panel_construction` / `CreateNewInventoryPanel`
   - Realm: `client`
   - Source: `plugins/inventory/cl_hooks.lua:85-101`
   - Confidence: `medium`
   - Reason: vendorTradeInterface creates inventory panels; this is UI construction, not root cause

5. `ui_result` / `Player inventory panel + vendor_grid_inventory panel`
   - Realm: `runtime`
   - Source: `human_context.md`
   - Confidence: `human_validated`
   - Reason: human-validated result: player inventory uses CreateNewInventoryPanel; vendor inventory uses vgui.Create('vendor_grid_inventory') and SetUpPanel(loadedInv)

## Vendor Price Update / UI Refresh

- Chain ID: `vendor_price_update_ui_refresh`
- Confidence: `medium`
- Reason: runtime facts show item metadata mutation, vendor network handler, hook dispatch, and UI refresh

### Steps

1. `network_send_start` / `nutVendorTrade`
   - Realm: `client`
   - Source: `plugins/vendor/derma/cl_vendor.lua:67-98`
   - Confidence: `high`
   - Reason: client initiates buy/sell request

2. `server_authority` / `Server validates vendor trade`
   - Realm: `runtime`
   - Source: `human_context.md`
   - Confidence: `doctrine`
   - Reason: server is authoritative for gameplay/inventory mutation

3. `item_data_mutation` / `vendorQty`
   - Realm: `server`
   - Source: `plugins/vendor/entities/entities/nut_vendor/init.lua:209-228`
   - Confidence: `high`
   - Reason: server mutates vendor presentation metadata via item:setData

4. `item_data_mutation` / `vendorSPrice`
   - Realm: `server`
   - Source: `plugins/vendor/entities/entities/nut_vendor/init.lua:209-228`
   - Confidence: `high`
   - Reason: server mutates vendor presentation metadata via item:setData

5. `item_data_mutation` / `vendorMQty`
   - Realm: `server`
   - Source: `plugins/vendor/entities/entities/nut_vendor/init.lua:209-228`
   - Confidence: `high`
   - Reason: server mutates vendor presentation metadata via item:setData

6. `sync_boundary` / `item:setData conditional sync / persistence boundary`
   - Realm: `runtime`
   - Source: `human_context.md`
   - Confidence: `human_validated`
   - Reason: human-validated: setData persists item data and may immediately sync to receiver/current owner or later to future owner/opened inventory

7. `vendor_network_handler` / `Price`
   - Realm: `client`
   - Source: `plugins/vendor/cl_networking.lua:53-72`
   - Confidence: `high`
   - Reason: client vendor Price handler receives presentation update

8. `hook_emit` / `VendorItemPriceUpdated`
   - Realm: `client`
   - Source: `plugins/vendor/cl_networking.lua:62-80`
   - Confidence: `high`
   - Reason: Price handler emits VendorItemPriceUpdated

9. `hook_listener` / `VendorItemPriceUpdated`
   - Realm: `client`
   - Source: `plugins/vendor/derma/cl_vendor.lua:194-214`
   - Confidence: `high`
   - Reason: vendor UI listens through self.onVendorPriceUpdated

10. `ui_refresh_call` / `updatePrice`
   - Realm: `client`
   - Source: `plugins/vendor/derma/cl_vendor.lua:148-183`
   - Confidence: `high`
   - Reason: vendor UI refreshes visible price label

## Vendor Exit / Metadata Cleanup

- Chain ID: `vendor_exit_metadata_cleanup`
- Confidence: `high`
- Reason: runtime facts show RemoveReceiverFromVendor clearing vendor* item data keys

### Steps

1. `network_send_start` / `nutVendorExit`
   - Realm: `client`
   - Source: `plugins/vendor/derma/cl_vendor.lua:229-245`
   - Confidence: `high`
   - Reason: client closes/removes vendor panel and sends exit

2. `server_cleanup_call` / `ENT:RemoveReceiverFromVendor(client)`
   - Realm: `runtime`
   - Source: `human_context.md`
   - Confidence: `source_inferred`
   - Reason: server removes client from vendor receivers and clears vendor metadata

3. `item_data_mutation` / `vendorBPrice`
   - Realm: `server`
   - Source: `plugins/vendor/entities/entities/nut_vendor/init.lua:290-309`
   - Confidence: `high`
   - Reason: server clears vendor presentation metadata with nil setData

4. `item_data_mutation` / `vendorQty`
   - Realm: `server`
   - Source: `plugins/vendor/entities/entities/nut_vendor/init.lua:290-309`
   - Confidence: `high`
   - Reason: server clears vendor presentation metadata with nil setData

5. `item_data_mutation` / `vendorSPrice`
   - Realm: `server`
   - Source: `plugins/vendor/entities/entities/nut_vendor/init.lua:290-309`
   - Confidence: `high`
   - Reason: server clears vendor presentation metadata with nil setData

6. `item_data_mutation` / `vendorMQty`
   - Realm: `server`
   - Source: `plugins/vendor/entities/entities/nut_vendor/init.lua:290-309`
   - Confidence: `high`
   - Reason: server clears vendor presentation metadata with nil setData

7. `sync_boundary` / `item:setData nil sync / persistence boundary`
   - Realm: `runtime`
   - Source: `human_context.md`
   - Confidence: `human_validated`
   - Reason: human-validated: cleanup may sync immediately to receiver/current owner or persist for future sync

## Inventory Data Delta Sync / UI Refresh Risk

- Chain ID: `inventory_data_delta_sync`
- Confidence: `medium`
- Reason: runtime facts show nutInventoryData receiver; UI refresh linkage still requires validation

### Steps

1. `network_receive` / `nutInventoryData`
   - Realm: `client`
   - Source: `gamemode/core/meta/inventory/cl_base_inventory.lua:1-13`
   - Confidence: `high`
   - Reason: client receives inventory data delta

2. `client_inventory_state_update` / `Inventory instance data key/value update`
   - Realm: `runtime`
   - Source: `human_context.md`
   - Confidence: `source_inferred`
   - Reason: nutInventoryData updates client inventory instance data

3. `ui_risk` / `Existing inventory/vendor item panels may need refresh`
   - Realm: `runtime`
   - Source: `human_context.md`
   - Confidence: `hypothesis`
   - Reason: stale labels may remain if UI does not observe ItemDataChanged or equivalent refresh boundary

## Storage Movement / Vendor Label Recovery Path

- Chain ID: `storage_refresh_recovery_path`
- Confidence: `medium`
- Reason: human observation plus runtime facts around storage/vendor panel creation and receiver removal

### Steps

1. `network_receive` / `vendorTradeInterface`
   - Realm: `client`
   - Source: `plugins/inventory/cl_hooks.lua:101-141`
   - Confidence: `high`
   - Reason: vendor/storage inventory UI construction path exists

2. `hook_emit` / `OnCreateStoragePanel`
   - Realm: `client`
   - Source: `plugins/inventory/cl_hooks.lua:131-171`
   - Confidence: `high`
   - Reason: storage panel creation emits UI/storage hook

3. `network_send_start` / `removeReceiverFromVendor`
   - Realm: `client`
   - Source: `plugins/inventory/cl_hooks.lua:131-171`
   - Confidence: `medium`
   - Reason: storage/vendor panel close sends removeReceiverFromVendor

4. `observed_recovery` / `Moving item through storage can refresh/clear stale vendor label`
   - Realm: `runtime`
   - Source: `human_context.md`
   - Confidence: `human_observed`
   - Reason: human-observed recovery path; exact source-level refresh boundary still needs validation

## Pipeline Notes

Use this report as input for investigation synthesis.

Do not treat warnings as bugs. They are missing validation links or uncertain runtime edges.
