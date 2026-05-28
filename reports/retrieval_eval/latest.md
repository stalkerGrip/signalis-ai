# SIGNALIS AI — Retrieval Evaluation Report

- Generated: `2026-05-29T01:23:35`
- Queries: **25**
- Passed: **0/25**
- Average score: **0.000**
- Pass threshold: **0.60**

## Summary

| ID | Priority | Intent | Score | Result |
|---|---:|---|---:|---|
| `inv_desync_after_character_load` | critical | `lifecycle_sync_investigation` | 0.000 | **FAIL** |
| `vendor_price_stale_after_purchase` | critical | `ui_metadata_sync_investigation` | 0.000 | **FAIL** |
| `storage_refresh_clears_vendor_metadata` | high | `cross_subsystem_ui_refresh` | 0.000 | **FAIL** |
| `player_loadout_inventory_sync_boundary` | high | `lifecycle_boundary_analysis` | 0.000 | **FAIL** |
| `inventory_panel_status_sync` | high | `network_contract_analysis` | 0.000 | **FAIL** |
| `nut_inventory_init_payload` | high | `network_payload_analysis` | 0.000 | **FAIL** |
| `gridinv_transfer_contract` | high | `transfer_contract_analysis` | 0.000 | **FAIL** |
| `storage_open_sync_contract` | high | `storage_sync_analysis` | 0.000 | **FAIL** |
| `save_load_inventory_storage_vendor` | high | `persistence_lifecycle_analysis` | 0.000 | **FAIL** |
| `vendor_legacy_authority_check` | high | `legacy_authority_validation` | 0.000 | **FAIL** |
| `ui_desync_client_inventory_panels` | high | `ui_desync_analysis` | 0.000 | **FAIL** |
| `character_lifecycle_cross_realm` | high | `lifecycle_cross_realm_analysis` | 0.000 | **FAIL** |
| `pvp_fps_timer_hotspots` | medium | `performance_topology_analysis` | 0.000 | **FAIL** |
| `dynamic_light_performance` | medium | `performance_subsystem_analysis` | 0.000 | **FAIL** |
| `health_status_scheduler` | medium | `scheduler_subsystem_analysis` | 0.000 | **FAIL** |
| `ragdoll_inventory_interaction` | medium | `cross_subsystem_coupling` | 0.000 | **FAIL** |
| `mining_smelter_storage_persistence` | medium | `entity_persistence_analysis` | 0.000 | **FAIL** |
| `network_receiver_without_sender` | medium | `network_qa` | 0.000 | **FAIL** |
| `raw_net_addnetworkstring_check` | medium | `network_qa` | 0.000 | **FAIL** |
| `timer_risk_persistence_network_inventory` | medium | `timer_risk_analysis` | 0.000 | **FAIL** |
| `plugin_coupling_inventory_vendor_storage` | high | `topology_coupling_analysis` | 0.000 | **FAIL** |
| `player_loaded_char_side_effects` | medium | `lifecycle_fanout_analysis` | 0.000 | **FAIL** |
| `inventory_database_ownership` | high | `ownership_model_analysis` | 0.000 | **FAIL** |
| `inventory_item_data_changed_sync` | high | `item_metadata_sync_analysis` | 0.000 | **FAIL** |
| `context_pack_inventory_vendor_bug` | critical | `context_pack_generation` | 0.000 | **FAIL** |

## Details

### inv_desync_after_character_load

Query: `inventory desync after character load`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `inventory, gridinv, multichar`

#### plugins

- Score: `0.000`
- Missing: `inventory, gridinv, multichar`

#### hooks

- Score: `0.000`
- Missing: `CharacterLoaded, PlayerLoadedChar, PlayerLoadout, PostPlayerLoadout`

#### network_messages

- Score: `0.000`
- Missing: `inventoryOpen, inventorySetPanelStatus, nutInventoryInit`

#### files

- Score: `0.000`
- Missing: `plugins/inventory/sh_plugin.lua, plugins/inventory/cl_hooks.lua, plugins/multichar/sv_networking.lua`

### vendor_price_stale_after_purchase

Query: `vendor price labels remain visible after buying item`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `vendor, inventory, gridinv`

#### plugins

- Score: `0.000`
- Missing: `vendor, inventory, gridinv`

#### hooks

- Score: `0.000`
- Missing: `VendorItemStockUpdated, VendorMoneyUpdated, VendorOpened, CanPlayerTradeWithVendor`

#### network_messages

- Score: `0.000`
- Missing: `nutVendorTrade, nutVendorOpen, inventorySetPanelStatus`

#### files

- Score: `0.000`
- Missing: `plugins/vendor/cl_networking.lua, plugins/vendor/derma/cl_vendor.lua, plugins/vendor/sv_hooks.lua, plugins/inventory/cl_hooks.lua`

### storage_refresh_clears_vendor_metadata

Query: `moving item through storage clears stale vendor price label`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `storage, inventory, vendor, gridinv`

#### plugins

- Score: `0.000`
- Missing: `storage, inventory, vendor, gridinv`

#### hooks

- Score: `0.000`
- Missing: `StorageOpen, ItemTransfered, InventoryItemAdded, InventoryItemRemoved`

#### network_messages

- Score: `0.000`
- Missing: `storageInventory, nutStorageOpen, nutTransferItem, inventorySetPanelStatus`

#### files

- Score: `0.000`
- Missing: `plugins/storage/cl_networking.lua, plugins/storage/sv_networking.lua, plugins/gridinv/sv_transfer.lua, plugins/inventory/cl_hooks.lua`

### player_loadout_inventory_sync_boundary

Query: `which lifecycle event should synchronize inventory UI after player loadout`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `inventory, multichar`

#### plugins

- Score: `0.000`
- Missing: `inventory, multichar`

#### hooks

- Score: `0.000`
- Missing: `PlayerLoadedChar, PlayerLoadout, PostPlayerLoadout`

#### network_messages

- Score: `0.000`
- Missing: `inventoryOpen, inventorySetPanelStatus, nutInventoryInit`

#### files

- Score: `0.000`
- Missing: `gamemode/core/hooks/sv_hooks.lua, plugins/inventory/sh_plugin.lua, plugins/multichar/sv_networking.lua`

### inventory_panel_status_sync

Query: `inventorySetPanelStatus synchronization ownership`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `inventory, gridinv, storage`

#### plugins

- Score: `0.000`
- Missing: `inventory, gridinv, storage`

#### network_messages

- Score: `0.000`
- Missing: `inventorySetPanelStatus`

#### files

- Score: `0.000`
- Missing: `plugins/inventory/sv_hooks.lua, plugins/inventory/cl_hooks.lua, plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`

### nut_inventory_init_payload

Query: `nutInventoryInit payload and inventory client initialization`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `inventory`

#### plugins

- Score: `0.000`
- Missing: `inventory`

#### network_messages

- Score: `0.000`
- Missing: `nutInventoryInit, nutInventoryAdd, nutInventoryRemove, nutInventoryDelete`

#### files

- Score: `0.000`
- Missing: `gamemode/core/libs/item/cl_networking.lua, gamemode/core/meta/inventory/cl_base_inventory.lua, gamemode/core/meta/inventory/sv_base_inventory.lua`

### gridinv_transfer_contract

Query: `grid inventory item transfer contract and validation`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `gridinv, inventory`

#### plugins

- Score: `0.000`
- Missing: `gridinv, inventory`

#### hooks

- Score: `0.000`
- Missing: `CanItemBeTransfered, HandleItemTransferRequest, ItemTransfered`

#### network_messages

- Score: `0.000`
- Missing: `nutTransferItem`

#### files

- Score: `0.000`
- Missing: `plugins/gridinv/sv_transfer.lua, plugins/gridinv/sv_access_rules.lua, plugins/inventory/sv_hooks.lua`

### storage_open_sync_contract

Query: `storage open network sync and inventory panel interaction`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `storage, gridinv, inventory`

#### plugins

- Score: `0.000`
- Missing: `storage, gridinv, inventory`

#### hooks

- Score: `0.000`
- Missing: `StorageOpen`

#### network_messages

- Score: `0.000`
- Missing: `nutStorageOpen, storageInventory, inventorySetPanelStatus`

#### files

- Score: `0.000`
- Missing: `plugins/storage/cl_networking.lua, plugins/storage/sv_networking.lua, plugins/gridinv/plugins/gridstorage/sh_plugin.lua`

### save_load_inventory_storage_vendor

Query: `SaveData LoadData inventory storage vendor persistence ordering`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `storage, vendor, inventory`

#### plugins

- Score: `0.000`
- Missing: `storage, vendor, inventory`

#### hooks

- Score: `0.000`
- Missing: `SaveData, LoadData, PostLoadData, StorageRestored`

#### files

- Score: `0.000`
- Missing: `plugins/storage/sv_storage.lua, plugins/vendor/sv_data.lua, gamemode/core/hooks/sv_hooks.lua, gamemode/core/sv_data.lua`

### vendor_legacy_authority_check

Query: `which vendor files are legacy and which are authoritative after vendor rework`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `vendor`

#### plugins

- Score: `0.000`
- Missing: `vendor`

#### hooks

- Score: `0.000`
- Missing: `VendorOpened, PlayerAccessVendor, CanPlayerAccessVendor, CanPlayerTradeWithVendor`

#### files

- Score: `0.000`
- Missing: `plugins/vendor/cl_networking.lua, plugins/vendor/sv_networking.lua, plugins/vendor/sv_hooks.lua, plugins/vendor/derma/cl_vendor.lua, plugins/vendor/entities/entities/nut_vendor/init.lua`

### ui_desync_client_inventory_panels

Query: `client inventory UI desync panel refresh stale item data`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `inventory, gridinv, vendor, storage`

#### plugins

- Score: `0.000`
- Missing: `inventory, gridinv, vendor, storage`

#### hooks

- Score: `0.000`
- Missing: `CreateNewInventoryPanel, CreateInventoryPanel, DrawItemDescription, ItemDataChanged`

#### network_messages

- Score: `0.000`
- Missing: `inventorySetPanelStatus, inventoryOpen, storageInventory`

#### files

- Score: `0.000`
- Missing: `plugins/inventory/cl_hooks.lua, gamemode/core/meta/inventory/cl_panel_extensions.lua, plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua, plugins/vendor/derma/cl_vendor.lua`

### character_lifecycle_cross_realm

Query: `character lifecycle cross realm synchronization CharacterLoaded PlayerLoadedChar`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `multichar, inventory`

#### plugins

- Score: `0.000`
- Missing: `multichar, inventory`

#### hooks

- Score: `0.000`
- Missing: `CharacterLoaded, PrePlayerLoadedChar, PlayerLoadedChar, OnCharCreated`

#### network_messages

- Score: `0.000`
- Missing: `nutCharChoose, nutCharCreate, nutCharList`

#### files

- Score: `0.000`
- Missing: `plugins/multichar/sv_networking.lua, plugins/multichar/cl_networking.lua, plugins/multichar/sh_plugin.lua`

### pvp_fps_timer_hotspots

Query: `PVP FPS drops timer Think hooks entity simulation hotspots`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `healthproblems, needs, lightitems, nextbots, ragdollinteraction`

#### plugins

- Score: `0.000`
- Missing: `healthproblems, needs, lightitems, ragdollinteraction`

#### hooks

- Score: `0.000`
- Missing: `Think, HUDPaint`

#### files

- Score: `0.000`
- Missing: `plugins/healthproblems/sv_hooks.lua, plugins/needs/sv_hooks.lua, plugins/lightitems/sv_hooks.lua, plugins/ragdollinteraction/interaction/sv_hooks.lua`

### dynamic_light_performance

Query: `dynamic light performance impact lightitems generators`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `lightitems`

#### plugins

- Score: `0.000`
- Missing: `lightitems`

#### files

- Score: `0.000`
- Missing: `plugins/lightitems/entities/entities/nut_electric_generator/init.lua, plugins/lightitems/sv_hooks.lua, plugins/lightitems/cl_hooks.lua`

### health_status_scheduler

Query: `health problems disease status timers scheduler player status tick`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `healthproblems, needs`

#### plugins

- Score: `0.000`
- Missing: `healthproblems, needs`

#### files

- Score: `0.000`
- Missing: `plugins/healthproblems/sv_hooks.lua, plugins/needs/sv_hooks.lua`

### ragdoll_inventory_interaction

Query: `ragdoll interaction inventory transfer character search coupling`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `inventory, gridinv, ragdollinteraction`

#### plugins

- Score: `0.000`
- Missing: `inventory, gridinv, ragdollinteraction, tying`

#### hooks

- Score: `0.000`
- Missing: `DisplayInventoryNut1_1, DisplayInventoryNut1_1_beta, TransferInventory, CanItemBeTransfered`

#### files

- Score: `0.000`
- Missing: `plugins/ragdollinteraction/interaction/sv_hooks.lua, plugins/ragdollinteraction/interaction/cl_hooks.lua, plugins/tying/sh_charsearch.lua`

### mining_smelter_storage_persistence

Query: `ore smelter storage persistence SaveData StorageEntityRemoved`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `mining, storage`

#### plugins

- Score: `0.000`
- Missing: `mining, storage`

#### hooks

- Score: `0.000`
- Missing: `SaveData, LoadData, StorageEntityRemoved`

#### files

- Score: `0.000`
- Missing: `plugins/mining/entities/entities/nut_ore_smelter/init.lua, plugins/storage/sv_storage.lua`

### network_receiver_without_sender

Query: `network messages with receiver without sender inventory vendor storage`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `inventory, vendor, storage`

#### network_messages

- Score: `0.000`
- Missing: `inventorySetPanelStatus, nutVendorOpen, nutStorageOpen, nutTransferItem`

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

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `inventory, storage, vendor`

#### hooks

- Score: `0.000`
- Missing: `SaveData, LoadData`

#### files

- Score: `0.000`
- Missing: `plugins/inventory/sv_hooks.lua, plugins/storage/sv_storage.lua, plugins/vendor/cl_networking.lua`

### plugin_coupling_inventory_vendor_storage

Query: `hidden coupling between inventory vendor storage gridinv`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `inventory, vendor, storage, gridinv`

#### plugins

- Score: `0.000`
- Missing: `inventory, vendor, storage, gridinv`

#### hooks

- Score: `0.000`
- Missing: `CanItemBeTransfered, ItemTransfered, StorageOpen, VendorOpened`

### player_loaded_char_side_effects

Query: `PlayerLoadedChar side effects across health inventory armor biorezonance`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `multichar, inventory, healthproblems, biorezonance`

#### plugins

- Score: `0.000`
- Missing: `multichar, inventory, healthproblems, biorezonance, armor`

#### hooks

- Score: `0.000`
- Missing: `PrePlayerLoadedChar, PlayerLoadedChar`

#### files

- Score: `0.000`
- Missing: `plugins/multichar/sv_networking.lua, plugins/healthproblems/sv_hooks.lua`

### inventory_database_ownership

Query: `character inventory ownership inv var database items CreateDefaultInventory`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `inventory, gridinv, multichar`

#### hooks

- Score: `0.000`
- Missing: `CharacterPreSave, PlayerLoadedChar, PlayerLoadout`

#### files

- Score: `0.000`
- Missing: `gamemode/core/meta/sh_character.lua, gamemode/core/meta/inventory/sv_base_inventory.lua, gamemode/core/libs/character/sv_character.lua, gamemode/core/hooks/sv_hooks.lua`

### inventory_item_data_changed_sync

Query: `ItemDataChanged item data synchronization stale client item metadata`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `inventory, vendor, gridinv`

#### hooks

- Score: `0.000`
- Missing: `ItemDataChanged, DrawItemDescription, InventoryItemAdded, InventoryItemRemoved`

#### network_messages

- Score: `0.000`
- Missing: `nutInventoryData, nutInventoryAdd, nutInventoryRemove`

#### files

- Score: `0.000`
- Missing: `gamemode/core/libs/item/cl_networking.lua, plugins/inventory/cl_hooks.lua, plugins/vendor/derma/cl_vendor.lua`

### context_pack_inventory_vendor_bug

Query: `build context pack for vendor stale price label inventory UI bug`

Overall: **0.000** — FAIL

#### subsystems

- Score: `0.000`
- Missing: `vendor, inventory, gridinv, storage`

#### plugins

- Score: `0.000`
- Missing: `vendor, inventory, gridinv, storage`

#### hooks

- Score: `0.000`
- Missing: `VendorItemStockUpdated, ItemDataChanged, ItemTransfered, StorageOpen`

#### network_messages

- Score: `0.000`
- Missing: `nutVendorTrade, inventorySetPanelStatus, storageInventory, nutTransferItem`
