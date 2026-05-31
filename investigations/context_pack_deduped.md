# Investigation Context Pack

Query: `vendor stale price labels after purchase`

Purpose: compact retrieval pack for investigation synthesis. Use this before opening raw Lua.

## Runtime Chains

### Result 1 — `docs/runtime/runtime_chains/vendor_purchase_item_metadata_sync.md`

- Source ID: `doc:doctrine:24070106b1a7a7f3`
- Doc type: `doctrine`
- Score: `0.7658`
- Rerank score: `0.5830390999999999`

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
```

### Result 2 — `docs/runtime/runtime_chains/vendor_purchase_chain.md`

- Source ID: `doc:doctrine:dad865c1ed66ff02`
- Doc type: `doctrine`
- Score: `0.7521`
- Rerank score: `0.57821932`

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
```


## Human Context

### Result 4 — `docs/human_context.md`

- Source ID: `doc:doctrine:7ba6861373241eea`
- Doc type: `doctrine`
- Score: `0.6962`
- Rerank score: `0.541172009`

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


## Subsystem Docs

### Result 5 — `subsystem_docs/runtime_doctrine.md`

- Source ID: `doc:doctrine:716ac0b5c759aa56`
- Doc type: `doctrine`
- Score: `0.6477`
- Rerank score: `0.524203855`

```text
some areas
```

### Result 6 — `docs/ai_subsystems/inventory.md`

- Source ID: `doc:doctrine:31bbd827617dc491`
- Doc type: `doctrine`
- Score: `0.6652`
- Rerank score: `0.466824774`

```text
# Synchronization Model

Current understanding:

Synchronization is performed through:
```

### Result 7 — `docs/subsystems/inventory.md`

- Source ID: `doc:doctrine:b15bac403297b54b`
- Doc type: `doctrine`
- Score: `0.6431`
- Rerank score: `0.45607477999999996`

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


## Doctrine / Project Memory

### Result 3 — `docs/project_memory.md`

- Source ID: `doc:doctrine:47ad906557a8aae4`
- Doc type: `doctrine`
- Score: `0.7425`
- Rerank score: `0.554364675`

```text
than duplicate them.

Confidence:
```


## File Topology

None.


## Other Retrieved Evidence

None.
