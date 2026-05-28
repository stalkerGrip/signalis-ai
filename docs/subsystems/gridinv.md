# Subsystem: gridinv

## Purpose

Deterministic subsystem summary generated from runtime topology.

## Topology Summary

- Nodes: **162**
- Edges: **5357**

## Node Types

- `hook_listener`: 53
- `hook_event`: 31
- `hook_emitter`: 20
- `network_payload_operation`: 16
- `network_operation`: 13
- `file`: 11
- `network_message`: 6
- `network_context`: 4
- `realm`: 3
- `plugin`: 1
- `timer_class`: 1
- `timer_operation`: 1
- `timer`: 1
- `subsystem`: 1

## Edge Types

- `runs_in_realm`: 4470
- `classified_as`: 142
- `references_timer`: 132
- `schedules_delay`: 132
- `listens_to`: 65
- `dispatches_to`: 58
- `contains_listener`: 53
- `registers_listener`: 53
- `listens_to_event`: 35
- `emits`: 28
- `contains_emitter`: 20
- `emits_event`: 20
- `owns_file`: 17
- `contains_network_payload_operation`: 16
- `file_sends_network_message`: 16
- `network_dispatches_to`: 16
- `sends_network_message`: 16
- `contains_network_operation`: 13
- `writes_network_payload`: 12
- `belongs_to_subsystem`: 9

## Major Hooks

- `listen CanItemBeTransfered @ plugins\ragdollinteraction\interaction\sv_hooks.lua:92`: 2
- `listen CreateInventoryPanel @ plugins\gridinv\plugins\gridinvui\sh_plugin.lua:8`: 2
- `listen NutScriptTablesLoaded @ plugins\gridinv\plugins\1_1compat\sh_plugin.lua:8`: 2
- `listen ItemDraggedOutOfInventory @ plugins\gridinv\sh_plugin.lua:33`: 2
- `listen StorageOpen @ plugins\gridinv\plugins\gridstorage\sh_plugin.lua:153`: 2
- `listen ItemCombine @ plugins\gridinv\sh_plugin.lua:18`: 2
- `emit NutScriptTablesLoaded @ gamemode\core\libs\sv_database.lua:519`: 1
- `listen addInventoryData @ plugins\gridinv\plugins\1_1compat\sv_migrations.lua:24`: 1
- `emit CanItemBeTransfered @ plugins\gridinv\sv_transfer.lua:18`: 1
- `listen HandleItemTransferRequest @ plugins\gridinv\sv_transfer.lua:4`: 1
- `listen deleteCharID @ plugins\gridinv\plugins\1_1compat\sv_migrations.lua:66`: 1
- `print`: 1
- `listen getMigrationFilter @ plugins\gridinv\plugins\1_1compat\sv_migrations.lua:14`: 1
- `emit StorageOpen @ plugins\storage\cl_networking.lua:8`: 1
- `emit SetupBagInventoryAccessRules @ plugins\gridinv\items\base\sh_bags.lua:60`: 1
- `HandleItemTransferRequest`: 1
- `listen getMigrationFilter @ plugins\gridinv\plugins\1_1compat\sv_migrations.lua:13`: 1
- `NutScriptTablesLoaded`: 1
- `listen CheckPassword @ plugins\gridinv\plugins\1_1compat\sh_plugin.lua:27`: 1
- `emit HandleItemTransferRequest @ plugins\gridinv\sv_transfer.lua:236`: 1

## Major Network Signals

- `Start nutTransferItem`: 2
- `send nutTransferItem`: 2
- `nutTransferItem`: 1
- `receive nutTransferItem`: 1
- `invMv`: 1
- `Receive nutTransferItem`: 1
- `nutInventoryDelete`: 1
- `netstream hook storageLockTrashcan`: 1
- `netstream send itemSplitTake`: 1
- `netstream send storageLockTrashcan`: 1
- `itemSplitTake`: 1
- `inventorySetPanelStatus`: 1
- `netstream send inventorySetPanelStatus`: 1
- `send nutInventoryDelete`: 1
- `Start nutInventoryDelete`: 1
- `receive nutInventoryDelete`: 1
- `netstream hook inventorySetPanelStatus`: 1
- `netstream hook itemSplitTake`: 1
- `storageLockTrashcan`: 1
- `register nutTransferItem`: 1

## Lifecycle Propagation

- none detected

## Synchronization Hotspots

- `write WriteUInt nutTransferItem`: 6
- `read ReadUInt nutTransferItem`: 3
- `Start nutTransferItem`: 2
- `send nutTransferItem`: 2
- `write WriteType nutTransferItem`: 2
- `write WriteBool nutTransferItem`: 2
- `nutTransferItem`: 1
- `receive nutTransferItem`: 1
- `Receive nutTransferItem`: 1
- `nutInventoryDelete`: 1
- `read ReadType nutTransferItem`: 1
- `write WriteType nutInventoryDelete`: 1
- `inventorySetPanelStatus`: 1
- `netstream send inventorySetPanelStatus`: 1
- `send nutInventoryDelete`: 1
- `Start nutInventoryDelete`: 1
- `read ReadBool nutTransferItem`: 1
- `receive nutInventoryDelete`: 1
- `netstream hook inventorySetPanelStatus`: 1
- `register nutTransferItem`: 1

## Important Timers

- `one_shot_delay`: 1
- `timer_simple@plugins\gridinv\plugins\1_1compat\sh_plugin.lua:31`: 1
- `timer_simple`: 1

## Realms

- `server`: 47
- `shared`: 33
- `client`: 7

## Major Files

- `plugins\gridinv\plugins\1_1compat\sv_migrations.lua`: 26
- `plugins\gridinv\sv_transfer.lua`: 8
- `plugins\gridinv\plugins\gridinvui\sh_plugin.lua`: 7
- `plugins\gridinv\sh_plugin.lua`: 7
- `plugins\gridinv\plugins\gridstorage\sh_plugin.lua`: 5
- `plugins\gridinv\plugins\1_1compat\sh_plugin.lua`: 5
- `plugins\gridinv\items\base\sh_bags.lua`: 4
- `plugins\gridinv\sv_access_rules.lua`: 4
- `plugins\gridinv\plugins\gridinvui\derma\cl_grid_inventory_panel.lua`: 3
- `gamemode\core\hooks\sv_hooks.lua`: 3
- `plugins\ragdollinteraction\interaction\sv_hooks.lua`: 2
- `plugins\gridinv\sh_grid_inv.lua`: 2
- `plugins\inventory\cl_hooks.lua`: 2
- `plugins\inventory\sv_hooks.lua`: 2
- `gamemode\core\libs\sv_database.lua`: 1
- `plugins\storage\cl_networking.lua`: 1
- `gamemode\core\hooks\sh_hooks.lua`: 1
- `gamemode\core\libs\sh_inventory.lua`: 1

## Connected Plugins / Subsystems

- `inventory`: 8
- `ragdollinteraction`: 5
- `storage`: 2
- `cassetteplayer`: 1
- `tying`: 1
- `vendor`: 1

## Runtime Propagation Hubs

- degree `99` | `plugin` | `gridinv` | `plugin:gridinv`
- degree `28` | `file` | `plugins\gridinv\plugins\1_1compat\sv_migrations.lua` | `file:plugins/gridinv/plugins/1_1compat/sv_migrations.lua`
- degree `26` | `network_message` | `nutTransferItem` | `netmsg:gmod_net:nutTransferItem`
- degree `24` | `file` | `plugins\gridinv\sv_transfer.lua` | `file:plugins/gridinv/sv_transfer.lua`
- degree `22` | `network_message` | `inventorySetPanelStatus` | `netmsg:netstream:inventorySetPanelStatus`
- degree `15` | `file` | `plugins\gridinv\plugins\gridinvui\derma\cl_grid_inventory_panel.lua` | `file:plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- degree `14` | `network_message` | `nutInventoryDelete` | `netmsg:gmod_net:nutInventoryDelete`
- degree `14` | `file` | `plugins\gridinv\sh_grid_inv.lua` | `file:plugins/gridinv/sh_grid_inv.lua`
- degree `13` | `file` | `plugins\gridinv\plugins\gridstorage\sh_plugin.lua` | `file:plugins/gridinv/plugins/gridstorage/sh_plugin.lua`
- degree `12` | `network_operation` | `netstream hook inventorySetPanelStatus` | `netop:hook:netstream:inventorySetPanelStatus:plugins/inventory/sv_hooks.lua:118:83`
- degree `12` | `hook_event` | `ItemTransfered` | `hook:ItemTransfered`
- degree `12` | `hook_event` | `CreateNewInventoryPanel` | `hook:CreateNewInventoryPanel`
- degree `12` | `file` | `plugins\gridinv\items\base\sh_bags.lua` | `file:plugins/gridinv/items/base/sh_bags.lua`
- degree `11` | `hook_event` | `CanItemBeTransfered` | `hook:CanItemBeTransfered`
- degree `9` | `hook_listener` | `listen ItemTransfered @ plugins\inventory\sv_hooks.lua:42` | `listener:listener_96ca97d3bed6`
- degree `9` | `hook_listener` | `listen ItemTransfered @ plugins\inventory\sv_hooks.lua:41` | `listener:listener_626806081e9d`
- degree `9` | `hook_listener` | `listen CreateNewInventoryPanel @ plugins\inventory\cl_hooks.lua:91` | `listener:listener_06896af87f09`
- degree `9` | `hook_listener` | `listen CreateNewInventoryPanel @ plugins\inventory\cl_hooks.lua:90` | `listener:listener_c4422fbb3c8d`
- degree `9` | `hook_event` | `StorageOpen` | `hook:StorageOpen`
- degree `9` | `hook_event` | `NutScriptTablesLoaded` | `hook:NutScriptTablesLoaded`
- degree `9` | `hook_event` | `GetDefaultInventoryType` | `hook:GetDefaultInventoryType`
- degree `9` | `file` | `plugins\gridinv\sh_plugin.lua` | `file:plugins/gridinv/sh_plugin.lua`
- degree `9` | `file` | `plugins\gridinv\plugins\gridinvui\sh_plugin.lua` | `file:plugins/gridinv/plugins/gridinvui/sh_plugin.lua`
- degree `8` | `hook_listener` | `listen CanItemBeTransfered @ plugins\ragdollinteraction\interaction\sv_hooks.lua:92` | `listener:listener_b77030683842`
- degree `8` | `hook_listener` | `listen CanItemBeTransfered @ plugins\ragdollinteraction\interaction\sv_hooks.lua:92` | `listener:listener_98b336bb6d8f`

## Topology Hubs

- degree `99` | `plugin` | `gridinv` | `plugin:gridinv`
- degree `28` | `file` | `plugins\gridinv\plugins\1_1compat\sv_migrations.lua` | `file:plugins/gridinv/plugins/1_1compat/sv_migrations.lua`
- degree `26` | `network_message` | `nutTransferItem` | `netmsg:gmod_net:nutTransferItem`
- degree `24` | `file` | `plugins\gridinv\sv_transfer.lua` | `file:plugins/gridinv/sv_transfer.lua`
- degree `22` | `network_message` | `inventorySetPanelStatus` | `netmsg:netstream:inventorySetPanelStatus`
- degree `15` | `file` | `plugins\gridinv\plugins\gridinvui\derma\cl_grid_inventory_panel.lua` | `file:plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- degree `14` | `network_message` | `nutInventoryDelete` | `netmsg:gmod_net:nutInventoryDelete`
- degree `14` | `file` | `plugins\gridinv\sh_grid_inv.lua` | `file:plugins/gridinv/sh_grid_inv.lua`
- degree `13` | `file` | `plugins\gridinv\plugins\gridstorage\sh_plugin.lua` | `file:plugins/gridinv/plugins/gridstorage/sh_plugin.lua`
- degree `12` | `network_operation` | `netstream hook inventorySetPanelStatus` | `netop:hook:netstream:inventorySetPanelStatus:plugins/inventory/sv_hooks.lua:118:83`
- degree `12` | `hook_event` | `ItemTransfered` | `hook:ItemTransfered`
- degree `12` | `hook_event` | `CreateNewInventoryPanel` | `hook:CreateNewInventoryPanel`
- degree `12` | `file` | `plugins\gridinv\items\base\sh_bags.lua` | `file:plugins/gridinv/items/base/sh_bags.lua`
- degree `11` | `hook_event` | `CanItemBeTransfered` | `hook:CanItemBeTransfered`
- degree `9` | `hook_listener` | `listen ItemTransfered @ plugins\inventory\sv_hooks.lua:42` | `listener:listener_96ca97d3bed6`
- degree `9` | `hook_listener` | `listen ItemTransfered @ plugins\inventory\sv_hooks.lua:41` | `listener:listener_626806081e9d`
- degree `9` | `hook_listener` | `listen CreateNewInventoryPanel @ plugins\inventory\cl_hooks.lua:91` | `listener:listener_06896af87f09`
- degree `9` | `hook_listener` | `listen CreateNewInventoryPanel @ plugins\inventory\cl_hooks.lua:90` | `listener:listener_c4422fbb3c8d`
- degree `9` | `hook_event` | `StorageOpen` | `hook:StorageOpen`
- degree `9` | `hook_event` | `NutScriptTablesLoaded` | `hook:NutScriptTablesLoaded`
- degree `9` | `hook_event` | `GetDefaultInventoryType` | `hook:GetDefaultInventoryType`
- degree `9` | `file` | `plugins\gridinv\sh_plugin.lua` | `file:plugins/gridinv/sh_plugin.lua`
- degree `9` | `file` | `plugins\gridinv\plugins\gridinvui\sh_plugin.lua` | `file:plugins/gridinv/plugins/gridinvui/sh_plugin.lua`
- degree `8` | `hook_listener` | `listen CanItemBeTransfered @ plugins\ragdollinteraction\interaction\sv_hooks.lua:92` | `listener:listener_b77030683842`
- degree `8` | `hook_listener` | `listen CanItemBeTransfered @ plugins\ragdollinteraction\interaction\sv_hooks.lua:92` | `listener:listener_98b336bb6d8f`

## Runtime Risks

- Review high-degree hubs for hidden coupling.
- Review network signals for synchronization ownership.
- Review timers for scheduler or debounce behavior.
- Review realm crossings for client/server authority issues.

## Notes

This document is generated from topology only. Use raw Lua only for exact validation.
