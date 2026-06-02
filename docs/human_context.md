# SIGNALIS AI — Human Context

## Project Reality Notes

ChatGPT is actively going off track, strict control is required, about a week of work was ultimately lost due to the fact that the chat was too focused on specific moments instead of conceptual work

## Current Architecture Intent

Important:

This section describes human intent, goals, desired capabilities, and architectural direction.
It is not the authoritative architecture definition.
The accepted architecture derived from this intent is owned by architecture.md.
If architecture.md differs from this section, architecture.md represents the current accepted architecture while this section remains historical human intent.

AI Orchestra: Local LLM + qdrant + RAG API + Thinking AI API + ChatGPT
The idea is to use PC power to maximize savings on Thinking AI API tokens during refactoring, creating new features, and code analysis using a local LLM, which will provide maximum context for the current project from qdrant and external sources via a low-cost RAG. This also applies to using a ChatGPT Plus subscription, which maximizes cost savings and accelerates coding and the adoption of architectural decisions or changes.
I would like to achieve from the local LLM the ability to update the code, using all the instruments and models available in the orchestra as a brain

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

## Character Load / Loadout Lifecycle

Human-validated runtime behavior:

Source:
nutscript/plugins/multichar/sv_networking.lua

Inside:

net.Receive("nutCharChoose", function(_, client) ...)

Runtime order:

PrePlayerLoadedChar
character:setup()
PlayerLoadedChar

Important:

PrePlayerLoadedChar does NOT directly emit PlayerLoadedChar.

Both hooks are emitted from the same nutCharChoose flow.

Source:
nutscript/gamemode/core/hooks/sv_hooks.lua

Runtime propagation:

PlayerLoadedChar
→ GM:PlayerLoadedChar
→ hook.Run("PlayerLoadout", client)

PlayerLoadout
→ GM:PlayerLoadout
→ hook.Run("PostPlayerLoadout", client)

Therefore:

PrePlayerLoadedChar → PlayerLoadedChar

is sibling emission from the same network flow.

But:

PlayerLoadedChar
→ PlayerLoadout
→ PostPlayerLoadout

is valid runtime propagation.

## invData Client Receiver Behavior

Human-validated runtime behavior:

Source:
gamemode/core/libs/item/cl_networking.lua

Receiver:

netstream.Hook("invData", function(id, key, value)

Behavior:

1. locate item instance
2. mutate item.data
3. emit ItemDataChanged

Equivalent runtime flow:

netstream:invData
→ receiver callback
→ item.data mutation
→ ItemDataChanged

Important:

ItemDataChanged is emitted directly inside the invData receiver callback.

Therefore:

netstream:invData
→ ItemDataChanged

is valid runtime propagation.

If topology cannot reconstruct this chain, the missing artifact is callback-body propagation, not invalid runtime evidence.

## Listener Body Semantics

Human-validated behavior:

Hook listeners are mixed.

Some listeners perform direct state mutation.

Some listeners call helper functions.

Some listeners perform both.

Examples:

- loyalty point initialization
- violation point initialization
- trait switching
- trait migration
- character migration logic

Therefore listeners must not be treated as passive labels.

Future propagation topology should support:

hook_event
→ listener
→ body-local operations
→ emitted hooks
→ state mutation

File/plugin ownership exits are useful but incomplete.