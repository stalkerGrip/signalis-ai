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
vendorSellItem becomes true when oldInventory.vendor is valid and the destination inventory is the player character inventory.

The transfer flow removes the item from the vendor inventory, adds it to the player inventory, then after successful transfer clears vendor sell metadata on the item:

item:setData("vendorQty", nil, client)
item:setData("vendorSPrice", nil, client)
item:setData("vendorMQty", nil, client)

If the vendor still has a buy price for that item type, the transferred item may receive:

item:setData("vendorBPrice", buyPrice, client)

Therefore vendor purchase cleanup is not only RemoveReceiverFromVendor. Purchase transfer itself performs item-level vendor metadata mutation after inventory transfer.

Human-validated vendor open flow:

Player interacts with vendor
→ server calls/emits OpenVendorTradeInterface
→ client receives vendorTradeInterface
→ vendorTradeInterface creates the player/local inventory panel through PLUGIN:CreateNewInventoryPanel(...), but the vendor inventory panel is created separately with vgui.Create("vendor_grid_inventory") and then bound to the loaded vendor inventory using storageInvPanel:SetUpPanel(loadedInv).
→ resulting UI shows vendor inventory and player inventory side by side.

CreateNewInventoryPanel in this flow is not an independent root cause. It is part of vendorTradeInterface UI construction.

The vendor system has been reworked. Some files under plugins/vendor are legacy and should not be assumed authoritative without validation.

Observed bug:
After buying items from a vendor, vendor price labels sometimes remain visible on items inside the player inventory.

Observed recovery:
Relog usually fixes the issue.
Moving the item through storage can also refresh/clear the incorrect display state.

Human interpretation:
This likely involves client-side item data or UI presentation state becoming stale, not necessarily server inventory ownership corruption.

Important rule:
Vendor price labels are presentation/UI metadata and should not be treated as authoritative item ownership state.

## Storage / Inventory Notes

## Performance Observations

## Refactor Intent

## Open Questions

## Human Validation Rule

When topology, doctrine, subsystem docs, and retrieval do not provide enough evidence to determine runtime behavior:

DO NOT GUESS.

Ask the project owner for:

- intended behavior
- subsystem history
- legacy vs authoritative implementation
- runtime observations
- reproduction steps
- exact Lua files involved

Human-confirmed information has higher priority than AI inference.

The preferred validation order is:

runtime topology
→ doctrine
→ subsystem docs
→ retrieval
→ targeted raw Lua
→ human validation
→ updated semantic artifacts

The goal is architecture understanding, not architecture speculation.

## Source Authority Rules

The NutScript framework included inside the SIGNALIS repository is not treated as external authority.

Local NutScript code is part of SIGNALIS source and may contain modifications, fixes, behavioral changes, and architectural divergence.

Authority order:

1. SIGNALIS source code
2. SIGNALIS runtime topology
3. SIGNALIS doctrine/docs
4. Human validation
5. External NutScript
6. Facepunch Wiki

External NutScript should be used only for comparison or historical reference and must not override validated behavior from local SIGNALIS source.