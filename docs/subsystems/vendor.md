# Subsystem: vendor

## Purpose

Deterministic subsystem summary generated from runtime topology.

## Topology Summary

- Nodes: **343**
- Edges: **7764**

## Node Types

- `network_payload_operation`: 78
- `network_operation`: 58
- `hook_listener`: 44
- `hook_emitter`: 33
- `network_message`: 30
- `hook_event`: 27
- `file`: 19
- `network_context`: 17
- `timer_operation`: 11
- `event_class`: 7
- `timer`: 5
- `plugin`: 4
- `realm`: 3
- `timer_class`: 3
- `subsystem`: 2
- `timer_risk`: 2

## Edge Types

- `runs_in_realm`: 4470
- `classified_as`: 804
- `references_timer`: 372
- `dispatches_to`: 324
- `has_timer_risk`: 215
- `schedules_entity_action`: 182
- `belongs_to_subsystem`: 150
- `schedules_delay`: 132
- `listens_to`: 131
- `contains_network_operation`: 86
- `listens_to_event`: 83
- `contains_network_payload_operation`: 78
- `emits`: 72
- `registers_listener`: 70
- `contains_listener`: 66
- `file_sends_network_message`: 57
- `removes_timer`: 57
- `emits_event`: 50
- `reads_network_payload`: 49
- `sends_network_message`: 47

## Major Hooks

- `listen CanPlayerTradeWithVendor @ plugins\vendor\sv_hooks.lua:18`: 2
- `listen VendorOpened @ plugins\vendor\cl_hooks.lua:1`: 2
- `listen PlayerAccessVendor @ plugins\vendor\sv_hooks.lua:171`: 2
- `listen CanPlayerAccessVendor @ plugins\vendor\sv_hooks.lua:2`: 2
- `listen CanItemBeTransfered @ plugins\ragdollinteraction\interaction\sv_hooks.lua:92`: 2
- `VendorItemStockUpdated`: 1
- `listen VendorItemModeUpdated @ plugins\vendor\derma\cl_vendor.lua:211`: 1
- `emit OnCharVarChanged @ gamemode\core\libs\character\cl_networking.lua:13`: 1
- `listen VendorItemMaxStockUpdated @ plugins\vendor\derma\cl_vendoreditor.lua:324`: 1
- `emit CanPlayerTradeWithVendor @ plugins\vendor\sv_hooks.lua:78`: 1
- `listen VendorMoneyUpdated @ plugins\vendor\derma\cl_vendor.lua:200`: 1
- `listen VendorItemMaxStockUpdated @ plugins\vendor\derma\cl_vendor.lua:208`: 1
- `LoadData`: 1
- `VendorMoneyUpdated`: 1
- `listen LoadData @ plugins\vendor\sv_data.lua:29`: 1
- `CanItemBeTransfered`: 1
- `emit OpenVendorTradeInterface @ plugins\vendor\entities\entities\nut_vendor\init.lua:57`: 1
- `listen VendorItemStockUpdated @ plugins\vendor\derma\cl_vendor.lua:207`: 1
- `emit VendorMoneyUpdated @ plugins\vendor\cl_networking.lua:59`: 1
- `VendorExited`: 1

## Major Network Signals

- `receive nutVendorEdit`: 2
- `netstream send activator`: 2
- `receive nutVendorExit`: 2
- `Receive nutVendorExit`: 2
- `send nutVendorExit`: 2
- `netstream send sendVendorInfo`: 2
- `Receive nutVendorEdit`: 2
- `Start nutVendorExit`: 2
- `Start nutVendorTrade`: 2
- `send nutVendorTrade`: 2
- `nutVendorStock`: 1
- `nutVendorFaction`: 1
- `send nutVendorEdit`: 1
- `nutVendor`: 1
- `Start nutVendorAllowClass`: 1
- `v`: 1
- `nutVendorTrade`: 1
- `netstream hook updateVendorFaction`: 1
- `Start nutVendorAllowFaction`: 1
- `send nutVendorAllowClass`: 1

## Lifecycle Propagation

- `LoadData`: 1
- `listen LoadData @ plugins\vendor\sv_data.lua:29`: 1
- `SaveData`: 1
- `emit SaveData @ gamemode\core\sv_data.lua:95`: 1
- `listen SaveData @ plugins\vendor\sv_data.lua:2`: 1
- `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:731`: 1
- `listen LoadData @ plugins\vendor\sv_data.lua:30`: 1
- `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737`: 1
- `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641`: 1
- `listen SaveData @ plugins\vendor\sv_data.lua:3`: 1
- `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652`: 1

## Synchronization Hotspots

- `nutVendorOpen`: 1
- `Start nutVendorOpen`: 1
- `receive nutVendorOpen`: 1
- `register nutVendorOpen`: 1
- `read ReadEntity nutVendorOpen`: 1
- `write WriteEntity nutVendorOpen`: 1
- `send nutVendorOpen`: 1
- `Receive nutVendorOpen`: 1

## Important Timers

- `TimerExists`: 1
- `timer_simple@plugins\vendor\entities\entities\nut_vendor\shared.lua:106`: 1
- `entity_timer_remove@plugins\vendor\entities\entities\nut_vendor\init.lua:351`: 1
- `RemoveTimer`: 1
- `next_tick_delay`: 1
- `nutVendorScale`: 1
- `timer_simple@plugins\vendor\entities\entities\nut_vendor\shared.lua:39`: 1
- `timer_simple`: 1
- `SetCustomTimer`: 1
- `entity_timer_or_action_call@plugins\vendor\entities\entities\nut_vendor\init.lua:349`: 1
- `entity_timer_exists@plugins\vendor\entities\entities\nut_vendor\init.lua:349`: 1
- `next_tick_or_subframe_delay`: 1
- `timer_simple@plugins\vendor\derma\cl_vendoreditor.lua:254`: 1
- `entity_timer_or_action_call@plugins\vendor\entities\entities\nut_vendor\init.lua:351`: 1
- `entity_timer_create@plugins\vendor\entities\entities\nut_vendor\init.lua:341`: 1
- `one_shot_delay`: 1
- `timer_simple@plugins\vendor\cl_networking.lua:134`: 1
- `timer_create@plugins\vendor\derma\cl_vendoreditor.lua:102`: 1
- `entity_validity_guard_expected`: 1
- `entity_simulation_timer`: 1

## Realms

- `client`: 49
- `server`: 39
- `shared`: 17

## Major Files

- `plugins\vendor\cl_networking.lua`: 13
- `plugins\vendor\sv_hooks.lua`: 12
- `plugins\vendor\derma\cl_vendoreditor.lua`: 9
- `plugins\vendor\entities\entities\nut_vendor\init.lua`: 9
- `plugins\vendor\derma\cl_vendor.lua`: 8
- `plugins\vendor\cl_hooks.lua`: 8
- `plugins\vendor\sv_data.lua`: 5
- `plugins\vendor\entities\entities\nut_vendor\shared.lua`: 5
- `gamemode\core\hooks\sv_hooks.lua`: 4
- `plugins\vendor\derma\cl_vendorfaction.lua`: 3
- `plugins\logging.lua`: 3
- `plugins\vendor\sv_networking.lua`: 3
- `plugins\inventory\sh_plugin.lua`: 3
- `plugins\vendor\entities\entities\nut_vendor\cl_init.lua`: 2
- `gamemode\core\meta\sh_character.lua`: 2
- `plugins\storage\sv_access_rules.lua`: 2
- `gamemode\core\libs\sh_character.lua`: 2
- `plugins\ragdollinteraction\interaction\sv_hooks.lua`: 2
- `plugins\gadgets\cl_hooks.lua`: 2
- `gamemode\core\libs\character\cl_networking.lua`: 1

## Connected Plugins / Subsystems

- `inventory`: 37
- `storage`: 9
- `crafting`: 6
- `gadgets`: 6
- `mining`: 6
- `lootablecontainers`: 5
- `ragdollinteraction`: 4
- `admintools`: 3
- `biorezonance`: 3
- `farming`: 3
- `lightitems`: 3
- `mnhr`: 3
- `needs`: 3
- `radio`: 3
- `area`: 2
- `cassetteplayer`: 2
- `saveitems.lua`: 2
- `gridinv`: 1
- `f1menu`: 1
- `multichar`: 1

## Runtime Propagation Hubs

- degree `107` | `plugin` | `vendor` | `plugin:vendor`
- degree `71` | `hook_event` | `LoadData` | `hook:LoadData`
- degree `63` | `file` | `plugins\inventory\cl_hooks.lua` | `file:plugins/inventory/cl_hooks.lua`
- degree `60` | `file` | `plugins\vendor\cl_networking.lua` | `file:plugins/vendor/cl_networking.lua`
- degree `57` | `hook_event` | `SaveData` | `hook:SaveData`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737` | `emitter:emitter_0b3042055654`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641` | `emitter:emitter_5e2c403ba5e0`
- degree `43` | `hook_event` | `CreateUsingInterface` | `hook:CreateUsingInterface`
- degree `43` | `file` | `plugins\vendor\sv_networking.lua` | `file:plugins/vendor/sv_networking.lua`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\sv_data.lua:95` | `emitter:emitter_79872d3f1d81`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:731` | `emitter:emitter_268470f88607`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652` | `emitter:emitter_1375b23e6ac9`
- degree `38` | `network_message` | `activator` | `netmsg:netstream:activator`
- degree `37` | `plugin` | `inventory` | `plugin:inventory`
- degree `35` | `network_message` | `nutVendorEdit` | `netmsg:gmod_net:nutVendorEdit`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:3` | `listener:listener_107469c23641`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:2` | `listener:listener_c14bd3d652fb`
- degree `30` | `file` | `plugins\vendor\sv_hooks.lua` | `file:plugins/vendor/sv_hooks.lua`
- degree `27` | `network_message` | `nutVendorExit` | `netmsg:gmod_net:nutVendorExit`
- degree `27` | `file` | `plugins\vendor\entities\entities\nut_vendor\init.lua` | `file:plugins/vendor/entities/entities/nut_vendor/init.lua`
- degree `27` | `file` | `plugins\vendor\cl_editor.lua` | `file:plugins/vendor/cl_editor.lua`
- degree `25` | `file` | `plugins\vendor\derma\cl_vendor.lua` | `file:plugins/vendor/derma/cl_vendor.lua`
- degree `24` | `network_message` | `unknown` | `netmsg:gmod_net:unknown`
- degree `24` | `file` | `plugins\inventory\sh_plugin.lua` | `file:plugins/inventory/sh_plugin.lua`
- degree `22` | `plugin` | `logging.lua` | `plugin:logging.lua`

## Topology Hubs

- degree `107` | `plugin` | `vendor` | `plugin:vendor`
- degree `71` | `hook_event` | `LoadData` | `hook:LoadData`
- degree `63` | `file` | `plugins\inventory\cl_hooks.lua` | `file:plugins/inventory/cl_hooks.lua`
- degree `60` | `file` | `plugins\vendor\cl_networking.lua` | `file:plugins/vendor/cl_networking.lua`
- degree `57` | `hook_event` | `SaveData` | `hook:SaveData`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737` | `emitter:emitter_0b3042055654`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641` | `emitter:emitter_5e2c403ba5e0`
- degree `43` | `hook_event` | `CreateUsingInterface` | `hook:CreateUsingInterface`
- degree `43` | `file` | `plugins\vendor\sv_networking.lua` | `file:plugins/vendor/sv_networking.lua`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\sv_data.lua:95` | `emitter:emitter_79872d3f1d81`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:731` | `emitter:emitter_268470f88607`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652` | `emitter:emitter_1375b23e6ac9`
- degree `38` | `network_message` | `activator` | `netmsg:netstream:activator`
- degree `37` | `plugin` | `inventory` | `plugin:inventory`
- degree `35` | `network_message` | `nutVendorEdit` | `netmsg:gmod_net:nutVendorEdit`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:3` | `listener:listener_107469c23641`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:2` | `listener:listener_c14bd3d652fb`
- degree `30` | `file` | `plugins\vendor\sv_hooks.lua` | `file:plugins/vendor/sv_hooks.lua`
- degree `27` | `network_message` | `nutVendorExit` | `netmsg:gmod_net:nutVendorExit`
- degree `27` | `file` | `plugins\vendor\entities\entities\nut_vendor\init.lua` | `file:plugins/vendor/entities/entities/nut_vendor/init.lua`
- degree `27` | `file` | `plugins\vendor\cl_editor.lua` | `file:plugins/vendor/cl_editor.lua`
- degree `25` | `file` | `plugins\vendor\derma\cl_vendor.lua` | `file:plugins/vendor/derma/cl_vendor.lua`
- degree `24` | `network_message` | `unknown` | `netmsg:gmod_net:unknown`
- degree `24` | `file` | `plugins\inventory\sh_plugin.lua` | `file:plugins/inventory/sh_plugin.lua`
- degree `22` | `plugin` | `logging.lua` | `plugin:logging.lua`

## Runtime Risks

- Review high-degree hubs for hidden coupling.
- Review network signals for synchronization ownership.
- Review timers for scheduler or debounce behavior.
- Review realm crossings for client/server authority issues.

## Notes

This document is generated from topology only. Use raw Lua only for exact validation.
