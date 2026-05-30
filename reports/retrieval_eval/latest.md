# SIGNALIS AI — Retrieval Evaluation Report

- Generated: `2026-05-29T01:39:41`
- Queries: **25**
- Passed: **19/25**
- Average score: **0.738**
- Pass threshold: **0.60**

## Summary

| ID | Priority | Intent | Score | Result |
|---|---:|---|---:|---|
| `inv_desync_after_character_load` | critical | `lifecycle_sync_investigation` | 0.742 | **PASS** |
| `vendor_price_stale_after_purchase` | critical | `ui_metadata_sync_investigation` | 0.606 | **PASS** |
| `storage_refresh_clears_vendor_metadata` | high | `cross_subsystem_ui_refresh` | 0.591 | **FAIL** |
| `player_loadout_inventory_sync_boundary` | high | `lifecycle_boundary_analysis` | 0.455 | **FAIL** |
| `inventory_panel_status_sync` | high | `network_contract_analysis` | 0.963 | **PASS** |
| `nut_inventory_init_payload` | high | `network_payload_analysis` | 1.000 | **PASS** |
| `gridinv_transfer_contract` | high | `transfer_contract_analysis` | 0.970 | **PASS** |
| `storage_open_sync_contract` | high | `storage_sync_analysis` | 0.879 | **PASS** |
| `save_load_inventory_storage_vendor` | high | `persistence_lifecycle_analysis` | 0.944 | **PASS** |
| `vendor_legacy_authority_check` | high | `legacy_authority_validation` | 1.000 | **PASS** |
| `ui_desync_client_inventory_panels` | high | `ui_desync_analysis` | 0.614 | **PASS** |
| `character_lifecycle_cross_realm` | high | `lifecycle_cross_realm_analysis` | 0.697 | **PASS** |
| `pvp_fps_timer_hotspots` | medium | `performance_topology_analysis` | 0.822 | **PASS** |
| `dynamic_light_performance` | medium | `performance_subsystem_analysis` | 0.952 | **PASS** |
| `health_status_scheduler` | medium | `scheduler_subsystem_analysis` | 1.000 | **PASS** |
| `ragdoll_inventory_interaction` | medium | `cross_subsystem_coupling` | 0.537 | **FAIL** |
| `mining_smelter_storage_persistence` | medium | `entity_persistence_analysis` | 0.944 | **PASS** |
| `network_receiver_without_sender` | medium | `network_qa` | 0.700 | **PASS** |
| `raw_net_addnetworkstring_check` | medium | `network_qa` | 0.000 | **FAIL** |
| `timer_risk_persistence_network_inventory` | medium | `timer_risk_analysis` | 0.222 | **FAIL** |
| `plugin_coupling_inventory_vendor_storage` | high | `topology_coupling_analysis` | 0.875 | **PASS** |
| `player_loaded_char_side_effects` | medium | `lifecycle_fanout_analysis` | 0.739 | **PASS** |
| `inventory_database_ownership` | high | `ownership_model_analysis` | 0.597 | **FAIL** |
| `inventory_item_data_changed_sync` | high | `item_metadata_sync_analysis` | 0.812 | **PASS** |
| `context_pack_inventory_vendor_bug` | critical | `context_pack_generation` | 0.800 | **PASS** |

## Details

### inv_desync_after_character_load

Query: `inventory desync after character load`

Overall: **0.742** — PASS

#### subsystems

- Score: `1.000`
- Matched: `inventory, gridinv, multichar`

#### plugins

- Score: `1.000`
- Matched: `inventory, gridinv, multichar`

#### hooks

- Score: `0.750`
- Matched: `CharacterLoaded, PlayerLoadout, PostPlayerLoadout`
- Missing: `PlayerLoadedChar`

#### network_messages

- Score: `0.000`
- Missing: `inventoryOpen, inventorySetPanelStatus, nutInventoryInit`

#### files

- Score: `0.667`
- Matched: `plugins/inventory/sh_plugin.lua, plugins/inventory/cl_hooks.lua`
- Missing: `plugins/multichar/sv_networking.lua`

### vendor_price_stale_after_purchase

Query: `vendor price labels remain visible after buying item`

Overall: **0.606** — PASS

#### subsystems

- Score: `0.667`
- Matched: `vendor, inventory`
- Missing: `gridinv`

#### plugins

- Score: `0.667`
- Matched: `vendor, inventory`
- Missing: `gridinv`

#### hooks

- Score: `0.750`
- Matched: `VendorItemStockUpdated, VendorMoneyUpdated, CanPlayerTradeWithVendor`
- Missing: `VendorOpened`

#### network_messages

- Score: `0.333`
- Matched: `nutVendorTrade`
- Missing: `nutVendorOpen, inventorySetPanelStatus`

#### files

- Score: `0.500`
- Matched: `plugins/vendor/cl_networking.lua, plugins/vendor/derma/cl_vendor.lua`
- Missing: `plugins/vendor/sv_hooks.lua, plugins/inventory/cl_hooks.lua`

### storage_refresh_clears_vendor_metadata

Query: `moving item through storage clears stale vendor price label`

Overall: **0.591** — FAIL

#### subsystems

- Score: `1.000`
- Matched: `storage, inventory, vendor, gridinv`

#### plugins

- Score: `1.000`
- Matched: `storage, inventory, vendor, gridinv`

#### hooks

- Score: `0.000`
- Missing: `StorageOpen, ItemTransfered, InventoryItemAdded, InventoryItemRemoved`

#### network_messages

- Score: `0.250`
- Matched: `storageInventory`
- Missing: `nutStorageOpen, nutTransferItem, inventorySetPanelStatus`

#### files

- Score: `0.000`
- Missing: `plugins/storage/cl_networking.lua, plugins/storage/sv_networking.lua, plugins/gridinv/sv_transfer.lua, plugins/inventory/cl_hooks.lua`

### player_loadout_inventory_sync_boundary

Query: `which lifecycle event should synchronize inventory UI after player loadout`

Overall: **0.455** — FAIL

#### subsystems

- Score: `0.500`
- Matched: `inventory`
- Missing: `multichar`

#### plugins

- Score: `0.500`
- Matched: `inventory`
- Missing: `multichar`

#### hooks

- Score: `0.667`
- Matched: `PlayerLoadout, PostPlayerLoadout`
- Missing: `PlayerLoadedChar`

#### network_messages

- Score: `0.000`
- Missing: `inventoryOpen, inventorySetPanelStatus, nutInventoryInit`

#### files

- Score: `0.667`
- Matched: `gamemode/core/hooks/sv_hooks.lua, plugins/inventory/sh_plugin.lua`
- Missing: `plugins/multichar/sv_networking.lua`

### inventory_panel_status_sync

Query: `inventorySetPanelStatus synchronization ownership`

Overall: **0.963** — PASS

#### subsystems

- Score: `1.000`
- Matched: `inventory, gridinv, storage`

#### plugins

- Score: `1.000`
- Matched: `inventory, gridinv, storage`

#### network_messages

- Score: `1.000`
- Matched: `inventorySetPanelStatus`

#### files

- Score: `0.667`
- Matched: `plugins/inventory/sv_hooks.lua, plugins/inventory/cl_hooks.lua`
- Missing: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`

### nut_inventory_init_payload

Query: `nutInventoryInit payload and inventory client initialization`

Overall: **1.000** — PASS

#### subsystems

- Score: `1.000`
- Matched: `inventory`

#### plugins

- Score: `1.000`
- Matched: `inventory`

#### network_messages

- Score: `1.000`
- Matched: `nutInventoryInit, nutInventoryAdd, nutInventoryRemove, nutInventoryDelete`

#### files

- Score: `1.000`
- Matched: `gamemode/core/libs/item/cl_networking.lua, gamemode/core/meta/inventory/cl_base_inventory.lua, gamemode/core/meta/inventory/sv_base_inventory.lua`

### gridinv_transfer_contract

Query: `grid inventory item transfer contract and validation`

Overall: **0.970** — PASS

#### subsystems

- Score: `1.000`
- Matched: `gridinv, inventory`

#### plugins

- Score: `1.000`
- Matched: `gridinv, inventory`

#### hooks

- Score: `1.000`
- Matched: `CanItemBeTransfered, HandleItemTransferRequest, ItemTransfered`

#### network_messages

- Score: `1.000`
- Matched: `nutTransferItem`

#### files

- Score: `0.667`
- Matched: `plugins/gridinv/sv_transfer.lua, plugins/inventory/sv_hooks.lua`
- Missing: `plugins/gridinv/sv_access_rules.lua`

### storage_open_sync_contract

Query: `storage open network sync and inventory panel interaction`

Overall: **0.879** — PASS

#### subsystems

- Score: `1.000`
- Matched: `storage, gridinv, inventory`

#### plugins

- Score: `1.000`
- Matched: `storage, gridinv, inventory`

#### hooks

- Score: `1.000`
- Matched: `StorageOpen`

#### network_messages

- Score: `0.667`
- Matched: `storageInventory, inventorySetPanelStatus`
- Missing: `nutStorageOpen`

#### files

- Score: `0.333`
- Matched: `plugins/gridinv/plugins/gridstorage/sh_plugin.lua`
- Missing: `plugins/storage/cl_networking.lua, plugins/storage/sv_networking.lua`

### save_load_inventory_storage_vendor

Query: `SaveData LoadData inventory storage vendor persistence ordering`

Overall: **0.944** — PASS

#### subsystems

- Score: `1.000`
- Matched: `storage, vendor, inventory`

#### plugins

- Score: `1.000`
- Matched: `storage, vendor, inventory`

#### hooks

- Score: `0.750`
- Matched: `SaveData, LoadData, StorageRestored`
- Missing: `PostLoadData`

#### files

- Score: `1.000`
- Matched: `plugins/storage/sv_storage.lua, plugins/vendor/sv_data.lua, gamemode/core/hooks/sv_hooks.lua, gamemode/core/sv_data.lua`

### vendor_legacy_authority_check

Query: `which vendor files are legacy and which are authoritative after vendor rework`

Overall: **1.000** — PASS

#### subsystems

- Score: `1.000`
- Matched: `vendor`

#### plugins

- Score: `1.000`
- Matched: `vendor`

#### hooks

- Score: `1.000`
- Matched: `VendorOpened, PlayerAccessVendor, CanPlayerAccessVendor, CanPlayerTradeWithVendor`

#### files

- Score: `1.000`
- Matched: `plugins/vendor/cl_networking.lua, plugins/vendor/sv_networking.lua, plugins/vendor/sv_hooks.lua, plugins/vendor/derma/cl_vendor.lua, plugins/vendor/entities/entities/nut_vendor/init.lua`

### ui_desync_client_inventory_panels

Query: `client inventory UI desync panel refresh stale item data`

Overall: **0.614** — PASS

#### subsystems

- Score: `1.000`
- Matched: `inventory, gridinv, vendor, storage`

#### plugins

- Score: `1.000`
- Matched: `inventory, gridinv, vendor, storage`

#### hooks

- Score: `0.250`
- Matched: `CreateNewInventoryPanel`
- Missing: `CreateInventoryPanel, DrawItemDescription, ItemDataChanged`

#### network_messages

- Score: `0.000`
- Missing: `inventorySetPanelStatus, inventoryOpen, storageInventory`

#### files

- Score: `0.250`
- Matched: `plugins/inventory/cl_hooks.lua`
- Missing: `gamemode/core/meta/inventory/cl_panel_extensions.lua, plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua, plugins/vendor/derma/cl_vendor.lua`

### character_lifecycle_cross_realm

Query: `character lifecycle cross realm synchronization CharacterLoaded PlayerLoadedChar`

Overall: **0.697** — PASS

#### subsystems

- Score: `1.000`
- Matched: `multichar, inventory`

#### plugins

- Score: `1.000`
- Matched: `multichar, inventory`

#### hooks

- Score: `0.500`
- Matched: `CharacterLoaded, PlayerLoadedChar`
- Missing: `PrePlayerLoadedChar, OnCharCreated`

#### network_messages

- Score: `0.000`
- Missing: `nutCharChoose, nutCharCreate, nutCharList`

#### files

- Score: `0.667`
- Matched: `plugins/multichar/sv_networking.lua, plugins/multichar/sh_plugin.lua`
- Missing: `plugins/multichar/cl_networking.lua`

### pvp_fps_timer_hotspots

Query: `PVP FPS drops timer Think hooks entity simulation hotspots`

Overall: **0.822** — PASS

#### subsystems

- Score: `0.800`
- Matched: `healthproblems, needs, lightitems, ragdollinteraction`
- Missing: `nextbots`

#### plugins

- Score: `1.000`
- Matched: `healthproblems, needs, lightitems, ragdollinteraction`

#### hooks

- Score: `0.500`
- Matched: `Think`
- Missing: `HUDPaint`

#### files

- Score: `1.000`
- Matched: `plugins/healthproblems/sv_hooks.lua, plugins/needs/sv_hooks.lua, plugins/lightitems/sv_hooks.lua, plugins/ragdollinteraction/interaction/sv_hooks.lua`

### dynamic_light_performance

Query: `dynamic light performance impact lightitems generators`

Overall: **0.952** — PASS

#### subsystems

- Score: `1.000`
- Matched: `lightitems`

#### plugins

- Score: `1.000`
- Matched: `lightitems`

#### files

- Score: `0.667`
- Matched: `plugins/lightitems/entities/entities/nut_electric_generator/init.lua, plugins/lightitems/cl_hooks.lua`
- Missing: `plugins/lightitems/sv_hooks.lua`

### health_status_scheduler

Query: `health problems disease status timers scheduler player status tick`

Overall: **1.000** — PASS

#### subsystems

- Score: `1.000`
- Matched: `healthproblems, needs`

#### plugins

- Score: `1.000`
- Matched: `healthproblems, needs`

#### files

- Score: `1.000`
- Matched: `plugins/healthproblems/sv_hooks.lua, plugins/needs/sv_hooks.lua`

### ragdoll_inventory_interaction

Query: `ragdoll interaction inventory transfer character search coupling`

Overall: **0.537** — FAIL

#### subsystems

- Score: `0.667`
- Matched: `inventory, ragdollinteraction`
- Missing: `gridinv`

#### plugins

- Score: `0.500`
- Matched: `inventory, ragdollinteraction`
- Missing: `gridinv, tying`

#### hooks

- Score: `0.500`
- Matched: `TransferInventory, CanItemBeTransfered`
- Missing: `DisplayInventoryNut1_1, DisplayInventoryNut1_1_beta`

#### files

- Score: `0.333`
- Matched: `plugins/ragdollinteraction/interaction/sv_hooks.lua`
- Missing: `plugins/ragdollinteraction/interaction/cl_hooks.lua, plugins/tying/sh_charsearch.lua`

### mining_smelter_storage_persistence

Query: `ore smelter storage persistence SaveData StorageEntityRemoved`

Overall: **0.944** — PASS

#### subsystems

- Score: `1.000`
- Matched: `mining, storage`

#### plugins

- Score: `1.000`
- Matched: `mining, storage`

#### hooks

- Score: `1.000`
- Matched: `SaveData, LoadData, StorageEntityRemoved`

#### files

- Score: `0.500`
- Matched: `plugins/mining/entities/entities/nut_ore_smelter/init.lua`
- Missing: `plugins/storage/sv_storage.lua`

### network_receiver_without_sender

Query: `network messages with receiver without sender inventory vendor storage`

Overall: **0.700** — PASS

#### subsystems

- Score: `1.000`
- Matched: `inventory, vendor, storage`

#### network_messages

- Score: `0.250`
- Matched: `inventorySetPanelStatus`
- Missing: `nutVendorOpen, nutStorageOpen, nutTransferItem`

### raw_net_addnetworkstring_check

Query: `raw net messages missing util.AddNetworkString inventory vendor multichar`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `inventory, vendor, multichar`

#### network_messages

- Score: `0.000`
- Missing: `nutInventoryInit, nutVendorOpen, nutCharChoose, nutCharCreate`

### timer_risk_persistence_network_inventory

Query: `suspicious timers persistence networking inventory mutation large entity scans`

Overall: **0.222** — FAIL

#### subsystems

- Score: `0.333`
- Matched: `inventory`
- Missing: `storage, vendor`

#### hooks

- Score: `0.000`
- Missing: `SaveData, LoadData`

#### files

- Score: `0.333`
- Matched: `plugins/inventory/sv_hooks.lua`
- Missing: `plugins/storage/sv_storage.lua, plugins/vendor/cl_networking.lua`

### plugin_coupling_inventory_vendor_storage

Query: `hidden coupling between inventory vendor storage gridinv`

Overall: **0.875** — PASS

#### subsystems

- Score: `1.000`
- Matched: `inventory, vendor, storage, gridinv`

#### plugins

- Score: `1.000`
- Matched: `inventory, vendor, storage, gridinv`

#### hooks

- Score: `0.500`
- Matched: `CanItemBeTransfered, StorageOpen`
- Missing: `ItemTransfered, VendorOpened`

### player_loaded_char_side_effects

Query: `PlayerLoadedChar side effects across health inventory armor biorezonance`

Overall: **0.739** — PASS

#### subsystems

- Score: `0.750`
- Matched: `inventory, healthproblems, biorezonance`
- Missing: `multichar`

#### plugins

- Score: `0.800`
- Matched: `inventory, healthproblems, biorezonance, armor`
- Missing: `multichar`

#### hooks

- Score: `1.000`
- Matched: `PrePlayerLoadedChar, PlayerLoadedChar`

#### files

- Score: `0.000`
- Missing: `plugins/multichar/sv_networking.lua, plugins/healthproblems/sv_hooks.lua`

### inventory_database_ownership

Query: `character inventory ownership inv var database items CreateDefaultInventory`

Overall: **0.597** — FAIL

#### subsystems

- Score: `0.667`
- Matched: `inventory, gridinv`
- Missing: `multichar`

#### hooks

- Score: `0.667`
- Matched: `CharacterPreSave, PlayerLoadout`
- Missing: `PlayerLoadedChar`

#### files

- Score: `0.250`
- Matched: `gamemode/core/hooks/sv_hooks.lua`
- Missing: `gamemode/core/meta/sh_character.lua, gamemode/core/meta/inventory/sv_base_inventory.lua, gamemode/core/libs/character/sv_character.lua`

### inventory_item_data_changed_sync

Query: `ItemDataChanged item data synchronization stale client item metadata`

Overall: **0.812** — PASS

#### subsystems

- Score: `1.000`
- Matched: `inventory, vendor, gridinv`

#### hooks

- Score: `0.750`
- Matched: `ItemDataChanged, InventoryItemAdded, InventoryItemRemoved`
- Missing: `DrawItemDescription`

#### network_messages

- Score: `1.000`
- Matched: `nutInventoryData, nutInventoryAdd, nutInventoryRemove`

#### files

- Score: `0.000`
- Missing: `gamemode/core/libs/item/cl_networking.lua, plugins/inventory/cl_hooks.lua, plugins/vendor/derma/cl_vendor.lua`

### context_pack_inventory_vendor_bug

Query: `build context pack for vendor stale price label inventory UI bug`

Overall: **0.800** — PASS

#### subsystems

- Score: `1.000`
- Matched: `vendor, inventory, gridinv, storage`

#### plugins

- Score: `1.000`
- Matched: `vendor, inventory, gridinv, storage`

#### hooks

- Score: `0.500`
- Matched: `VendorItemStockUpdated, ItemTransfered`
- Missing: `ItemDataChanged, StorageOpen`

#### network_messages

- Score: `0.500`
- Matched: `nutVendorTrade, storageInventory`
- Missing: `inventorySetPanelStatus, nutTransferItem`
