# Subsystem: storage

## Purpose

Deterministic subsystem summary generated from runtime topology.

## Topology Summary

- Nodes: **240**
- Edges: **6960**

## Node Types

- `network_operation`: 49
- `hook_emitter`: 38
- `hook_listener`: 36
- `file`: 23
- `hook_event`: 22
- `network_message`: 15
- `network_context`: 14
- `network_payload_operation`: 12
- `plugin`: 11
- `timer_operation`: 9
- `event_class`: 3
- `realm`: 3
- `timer_class`: 2
- `timer`: 2
- `subsystem`: 1

## Edge Types

- `runs_in_realm`: 4470
- `classified_as`: 421
- `dispatches_to`: 300
- `registers_listener`: 216
- `references_timer`: 171
- `listens_to_event`: 143
- `schedules_delay`: 132
- `owns_file`: 127
- `listens_to`: 121
- `owns_timer_operation`: 112
- `contains_network_operation`: 91
- `emits_event`: 80
- `contains_timer_operation`: 73
- `file_sends_network_message`: 70
- `emits`: 69
- `contains_listener`: 61
- `sends_network_message`: 57
- `contains_emitter`: 40
- `network_dispatches_to`: 40
- `schedules_player_action`: 38

## Major Hooks

- `listen PlayerSpawnedProp @ plugins\storage\sv_storage.lua:3`: 2
- `listen StorageOpen @ plugins\_disabled\simpleinv\plugins\liststorage\sh_plugin.lua:16`: 2
- `listen transferItem @ plugins\storage\sh_plugin.lua:23`: 2
- `listen StorageOpen @ plugins\gridinv\plugins\gridstorage\sh_plugin.lua:153`: 2
- `listen StorageUnlockPrompt @ plugins\storage\cl_password.lua:1`: 2
- `emit StorageEntityRemoved @ plugins\mining\entities\entities\nut_ore_smelter\init.lua:474`: 1
- `PlayerSpawnedProp`: 1
- `emit SaveData @ gamemode\core\sv_data.lua:95`: 1
- `listen StorageItemRemoved @ plugins\storage\sv_storage.lua:77`: 1
- `saveStorage`: 1
- `listen exitStorage @ plugins\storage\cl_networking.lua:10`: 1
- `emit StorageOpen @ plugins\storage\cl_networking.lua:8`: 1
- `emit StorageEntityRemoved @ plugins\vendor\entities\entities\nut_vendor\init.lua:278`: 1
- `StorageRestored`: 1
- `emit saveStorage @ plugins\storage\entities\entities\nut_storage\init.lua:190`: 1
- `listen CanPlayerSpawnStorage @ plugins\storage\sv_storage.lua:45`: 1
- `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652`: 1
- `emit StorageItemRemoved @ plugins\cassetteplayer\entities\entities\nut_cassetteplayer.lua:158`: 1
- `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:2`: 1
- `transferItem`: 1

## Major Network Signals

- `netstream send entFreezeState`: 8
- `Start nutStorageOpen`: 5
- `send nutStorageOpen`: 5
- `netstream send storageCleanTrash`: 2
- `Start nutStorageUnlock`: 2
- `Receive nutStorageUnlock`: 2
- `receive nutStorageUnlock`: 2
- `netstream send storageTakeOffLock`: 2
- `send nutStorageUnlock`: 2
- `netstream send storageInventory`: 2
- `netstream hook storageOpen`: 1
- `Start nutStorageExit`: 1
- `netstream hook entFreezeState`: 1
- `netstream send storageOpen`: 1
- `Receive nutStorageTransfer`: 1
- `nutStorageUnlock`: 1
- `netstream send storageNewDesc`: 1
- `receive nutStorageOpen`: 1
- `netstream hook storageTakeOffLock`: 1
- `storageNewDesc`: 1

## Lifecycle Propagation

- `emit SaveData @ gamemode\core\sv_data.lua:95`: 1
- `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652`: 1
- `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737`: 1
- `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641`: 1
- `LoadData`: 1
- `listen SaveData @ plugins\storage\sv_storage.lua:82`: 1
- `SaveData`: 1
- `listen SaveData @ plugins\storage\sv_storage.lua:81`: 1
- `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:731`: 1
- `listen LoadData @ plugins\storage\sv_storage.lua:86`: 1
- `listen LoadData @ plugins\storage\sv_storage.lua:85`: 1

## Synchronization Hotspots

- `write WriteEntity nutStorageOpen`: 5
- `Start nutStorageOpen`: 5
- `send nutStorageOpen`: 5
- `netstream send storageInventory`: 2
- `receive nutStorageOpen`: 1
- `register nutStorageOpen`: 1
- `inventorySetPanelStatus`: 1
- `netstream send inventorySetPanelStatus`: 1
- `netstream hook storageInventory`: 1
- `Receive nutStorageOpen`: 1
- `netstream hook inventorySetPanelStatus`: 1
- `storageInventory`: 1
- `nutStorageOpen`: 1
- `read ReadEntity nutStorageOpen`: 1

## Important Timers

- `player_action_timer@plugins\inventory\sv_hooks.lua:16`: 1
- `entity_timer_simple@plugins\inventory\sv_hooks.lua:123`: 1
- `one_shot_delay`: 1
- `timer_simple@plugins\gridinv\plugins\1_1compat\sh_plugin.lua:31`: 1
- `player_cancelable_action_timer@plugins\storage\entities\entities\nut_storage\init.lua:315`: 1
- `timer_simple`: 1
- `player_cancelable_action_timer@plugins\storage\entities\entities\nut_storage\init.lua:256`: 1
- `setAction`: 1
- `player_action_timer`: 1
- `player_cancelable_action_timer@plugins\storage\entities\entities\nut_storage\init.lua:147`: 1
- `player_action_timer@plugins\storage\entities\entities\nut_storage\init.lua:70`: 1
- `player_cancelable_action_timer@plugins\crafting\entities\entities\nut_storage_kit\init.lua:30`: 1
- `timer_simple@plugins\storage\sv_storage.lua:149`: 1

## Realms

- `server`: 70
- `shared`: 19
- `client`: 17

## Major Files

- `plugins\storage\sv_storage.lua`: 19
- `plugins\storage\entities\entities\nut_storage\init.lua`: 10
- `plugins\storage\sv_access_rules.lua`: 5
- `plugins\gridinv\plugins\gridstorage\sh_plugin.lua`: 5
- `plugins\storage\cl_networking.lua`: 5
- `plugins\mining\entities\entities\nut_ore_smelter\init.lua`: 4
- `gamemode\core\hooks\sv_hooks.lua`: 4
- `plugins\inventory\sv_hooks.lua`: 4
- `plugins\lootablecontainers\entities\entities\nut_loot_container_base\init.lua`: 4
- `plugins\inventory\cl_hooks.lua`: 4
- `plugins\crafting\entities\entities\nut_crafting_base\init.lua`: 4
- `plugins\cassetteplayer\entities\entities\nut_cassetteplayer.lua`: 3
- `plugins\_disabled\simpleinv\plugins\liststorage\sh_plugin.lua`: 3
- `plugins\crafting\entities\entities\nut_storage_kit\init.lua`: 3
- `plugins\vendor\entities\entities\nut_vendor\shared.lua`: 3
- `plugins\storage\sh_plugin.lua`: 3
- `plugins\storage\sv_networking.lua`: 3
- `plugins\storage\cl_password.lua`: 3
- `plugins\gridinv\plugins\1_1compat\sv_migrations.lua`: 3
- `plugins\vendor\entities\entities\nut_vendor\init.lua`: 2

## Connected Plugins / Subsystems

- `ragdollinteraction`: 133
- `vendor`: 107
- `gridinv`: 99
- `mining`: 75
- `crafting`: 58
- `inventory`: 37
- `lootablecontainers`: 21
- `cassetteplayer`: 15
- `gadgets`: 6
- `needs`: 5
- `admintools`: 3
- `biorezonance`: 3
- `farming`: 3
- `lightitems`: 3
- `mnhr`: 3
- `radio`: 3
- `tying`: 2
- `saveitems.lua`: 2
- `area`: 1
- `propprotect.lua`: 1

## Runtime Propagation Hubs

- degree `133` | `plugin` | `ragdollinteraction` | `plugin:ragdollinteraction`
- degree `107` | `plugin` | `vendor` | `plugin:vendor`
- degree `99` | `plugin` | `gridinv` | `plugin:gridinv`
- degree `75` | `plugin` | `mining` | `plugin:mining`
- degree `71` | `hook_event` | `LoadData` | `hook:LoadData`
- degree `67` | `plugin` | `storage` | `plugin:storage`
- degree `65` | `file` | `plugins\mining\entities\entities\nut_ore_smelter\init.lua` | `file:plugins/mining/entities/entities/nut_ore_smelter/init.lua`
- degree `63` | `file` | `plugins\inventory\cl_hooks.lua` | `file:plugins/inventory/cl_hooks.lua`
- degree `58` | `plugin` | `crafting` | `plugin:crafting`
- degree `57` | `hook_event` | `SaveData` | `hook:SaveData`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737` | `emitter:emitter_0b3042055654`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641` | `emitter:emitter_5e2c403ba5e0`
- degree `43` | `hook_event` | `CreateUsingInterface` | `hook:CreateUsingInterface`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\sv_data.lua:95` | `emitter:emitter_79872d3f1d81`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:731` | `emitter:emitter_268470f88607`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652` | `emitter:emitter_1375b23e6ac9`
- degree `38` | `network_message` | `activator` | `netmsg:netstream:activator`
- degree `37` | `plugin` | `inventory` | `plugin:inventory`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:3` | `listener:listener_107469c23641`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:2` | `listener:listener_c14bd3d652fb`
- degree `28` | `file` | `plugins\gridinv\plugins\1_1compat\sv_migrations.lua` | `file:plugins/gridinv/plugins/1_1compat/sv_migrations.lua`
- degree `27` | `file` | `plugins\vendor\entities\entities\nut_vendor\init.lua` | `file:plugins/vendor/entities/entities/nut_vendor/init.lua`
- degree `26` | `network_message` | `nutStorageOpen` | `netmsg:gmod_net:nutStorageOpen`
- degree `26` | `file` | `plugins\storageinterface\derma\cl_storage_interface.lua` | `file:plugins/storageinterface/derma/cl_storage_interface.lua`
- degree `26` | `file` | `plugins\storage\sv_networking.lua` | `file:plugins/storage/sv_networking.lua`

## Topology Hubs

- degree `133` | `plugin` | `ragdollinteraction` | `plugin:ragdollinteraction`
- degree `107` | `plugin` | `vendor` | `plugin:vendor`
- degree `99` | `plugin` | `gridinv` | `plugin:gridinv`
- degree `75` | `plugin` | `mining` | `plugin:mining`
- degree `71` | `hook_event` | `LoadData` | `hook:LoadData`
- degree `67` | `plugin` | `storage` | `plugin:storage`
- degree `65` | `file` | `plugins\mining\entities\entities\nut_ore_smelter\init.lua` | `file:plugins/mining/entities/entities/nut_ore_smelter/init.lua`
- degree `63` | `file` | `plugins\inventory\cl_hooks.lua` | `file:plugins/inventory/cl_hooks.lua`
- degree `58` | `plugin` | `crafting` | `plugin:crafting`
- degree `57` | `hook_event` | `SaveData` | `hook:SaveData`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737` | `emitter:emitter_0b3042055654`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641` | `emitter:emitter_5e2c403ba5e0`
- degree `43` | `hook_event` | `CreateUsingInterface` | `hook:CreateUsingInterface`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\sv_data.lua:95` | `emitter:emitter_79872d3f1d81`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:731` | `emitter:emitter_268470f88607`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652` | `emitter:emitter_1375b23e6ac9`
- degree `38` | `network_message` | `activator` | `netmsg:netstream:activator`
- degree `37` | `plugin` | `inventory` | `plugin:inventory`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:3` | `listener:listener_107469c23641`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:2` | `listener:listener_c14bd3d652fb`
- degree `28` | `file` | `plugins\gridinv\plugins\1_1compat\sv_migrations.lua` | `file:plugins/gridinv/plugins/1_1compat/sv_migrations.lua`
- degree `27` | `file` | `plugins\vendor\entities\entities\nut_vendor\init.lua` | `file:plugins/vendor/entities/entities/nut_vendor/init.lua`
- degree `26` | `network_message` | `nutStorageOpen` | `netmsg:gmod_net:nutStorageOpen`
- degree `26` | `file` | `plugins\storageinterface\derma\cl_storage_interface.lua` | `file:plugins/storageinterface/derma/cl_storage_interface.lua`
- degree `26` | `file` | `plugins\storage\sv_networking.lua` | `file:plugins/storage/sv_networking.lua`

## Runtime Risks

- Review high-degree hubs for hidden coupling.
- Review network signals for synchronization ownership.
- Review timers for scheduler or debounce behavior.
- Review realm crossings for client/server authority issues.

## Notes

This document is generated from topology only. Use raw Lua only for exact validation.
