# Subsystem: needs

## Purpose

Deterministic subsystem summary generated from runtime topology.

## Topology Summary

- Nodes: **255**
- Edges: **7721**

## Node Types

- `network_operation`: 61
- `timer_operation`: 56
- `network_message`: 31
- `hook_emitter`: 25
- `file`: 25
- `hook_listener`: 17
- `timer`: 10
- `hook_event`: 9
- `timer_class`: 7
- `timer_risk`: 4
- `subsystem`: 3
- `realm`: 3
- `event_class`: 1
- `plugin`: 1
- `network_context`: 1
- `network_payload_operation`: 1

## Edge Types

- `runs_in_realm`: 4470
- `classified_as`: 692
- `references_timer`: 474
- `dispatches_to`: 325
- `belongs_to_subsystem`: 314
- `has_timer_risk`: 243
- `schedules_entity_action`: 182
- `schedules_delay`: 132
- `listens_to`: 120
- `schedules_player_action`: 96
- `listens_to_event`: 65
- `contains_network_operation`: 61
- `removes_timer`: 60
- `contains_timer_operation`: 56
- `owns_timer_operation`: 56
- `file_sends_network_message`: 49
- `sends_network_message`: 49
- `emits`: 48
- `network_dispatches_to`: 37
- `owns_file`: 36

## Major Hooks

- `emit CreateUsingInterface @ plugins\needs\entities\entities\nut_cooking_pottea\cl_init.lua:22`: 1
- `emit SaveData @ gamemode\core\sv_data.lua:95`: 1
- `UpdateMaxNeeds`: 1
- `listen PlayerDeath @ plugins\needs\sv_hooks.lua:132`: 1
- `emit CreateUsingInterface @ plugins\needs\entities\entities\nut_cooking_pan\cl_init.lua:21`: 1
- `CharacterPreSave`: 1
- `listen LoadNutFonts @ plugins\needs\cl_hooks.lua:21`: 1
- `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652`: 1
- `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:2`: 1
- `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737`: 1
- `emit CreateUsingInterface @ plugins\needs\entities\entities\nut_cooking_board\cl_init.lua:21`: 1
- `listen UpdateMaxNeeds @ plugins\needs\sv_hooks.lua:125`: 1
- `emit UpdateMaxNeeds @ schema\libs\sv_utils.lua:53`: 1
- `CreateUsingInterface`: 1
- `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641`: 1
- `emit CreateUsingInterface @ plugins\needs\entities\entities\nut_cooking_oven\cl_init.lua:54`: 1
- `HandlePainKillBoost`: 1
- `LoadData`: 1
- `HandleBloodLoss`: 1
- `emit CreateUsingInterface @ plugins\needs\entities\entities\nut_waterfaucet\cl_init.lua:21`: 1

## Major Network Signals

- `netstream send entFreezeState`: 4
- `netstream send item.player`: 3
- `netstream send interfaceTurnOn`: 3
- `netstream send cookingovenFirstBurnerSwitch`: 2
- `netstream hook cookingpotPourOut`: 1
- `netstream send cookingovenStartBake`: 1
- `kettleInterfaceTurnOn`: 1
- `netstream hook entFreezeState`: 1
- `netstream hook kettleTurnOn`: 1
- `netstream hook kettlePartAddServer`: 1
- `netstream hook cookingpotUpdateCompositionClient`: 1
- `kettleTurnOn`: 1
- `cookingpotPourOut`: 1
- `cookingboardCut`: 1
- `netstream send cookingpotPickUp`: 1
- `netstream hook waterfaucetDrinkWater`: 1
- `cookingovenTakeFood`: 1
- `cookingpotTakeOff`: 1
- `netstream send cookingpotGetCompositionServer`: 1
- `waterfaucetDrawWater`: 1

## Lifecycle Propagation

- `emit SaveData @ gamemode\core\sv_data.lua:95`: 1
- `CharacterPreSave`: 1
- `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652`: 1
- `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737`: 1
- `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641`: 1
- `LoadData`: 1
- `listen SaveData @ plugins\needs\sv_hooks.lua:146`: 1
- `listen CharacterPreSave @ plugins\needs\sv_hooks.lua:119`: 1
- `emit CharacterPreSave @ gamemode\core\meta\sh_character.lua:42`: 1
- `listen LoadData @ plugins\needs\sv_hooks.lua:218`: 1
- `SaveData`: 1
- `listen CharacterPreSave @ plugins\needs\sv_hooks.lua:120`: 1
- `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:731`: 1
- `listen SaveData @ plugins\needs\sv_hooks.lua:145`: 1
- `listen LoadData @ plugins\needs\sv_hooks.lua:217`: 1

## Synchronization Hotspots

- `receive nutStorageOpen`: 1
- `send nutStorageOpen`: 1
- `nutStorageOpen`: 1
- `Start nutStorageOpen`: 1
- `write WriteEntity nutStorageOpen`: 1

## Important Timers

- `high_frequency_infinite_timer`: 2
- `entity_timer_or_action_call@plugins\needs\entities\entities\nut_cooking_base.lua:540`: 2
- `entity_timer_or_action_call@plugins\needs\entities\entities\nut_cooking_base.lua:393`: 2
- `entity_timer_or_action_call@plugins\needs\entities\entities\nut_cooking_kettle\init.lua:109`: 2
- `player_action_timer@plugins\needs\entities\entities\nut_cooking_board\init.lua:113`: 1
- `RemoveTimer`: 1
- `timer_create@plugins\needs\sv_hooks.lua:9`: 1
- `entity_timer_or_action_call@plugins\needs\entities\entities\nut_cooking_oven\init.lua:162`: 1
- `setCancelAction`: 1
- `next_tick_delay`: 1
- `timer_remove@plugins\needs\derma\cl_cookingboard_interface.lua:112`: 1
- `entity_timer_create@plugins\needs\entities\entities\nut_cooking_base.lua:39`: 1
- `player_cancelable_action_timer@plugins\needs\entities\entities\nut_waterfaucet\init.lua:127`: 1
- `entity_timer_or_action_call@plugins\needs\entities\entities\nut_cooking_oven\init.lua:34`: 1
- `entity_timer_remove@plugins\needs\entities\entities\nut_cooking_base.lua:540`: 1
- `entity_timer_exists@plugins\needs\sv_hooks.lua:165`: 1
- `entity_timer_create@plugins\needs\entities\entities\nut_cooking_kettle\init.lua:113`: 1
- `entity_timer_or_action_call@plugins\needs\entities\entities\nut_cooking_base.lua:47`: 1
- `entity_timer_or_action_call@plugins\needs\entities\entities\nut_cooking_base.lua:39`: 1
- `next_tick_or_subframe_delay`: 1

## Realms

- `server`: 50
- `shared`: 33
- `client`: 31

## Major Files

- `plugins\needs\entities\entities\nut_cooking_base.lua`: 22
- `plugins\needs\sv_hooks.lua`: 14
- `plugins\needs\entities\entities\nut_cooking_oven\init.lua`: 12
- `plugins\needs\entities\entities\nut_cooking_kettle\init.lua`: 11
- `plugins\needs\derma\cl_cookingboard_interface.lua`: 7
- `gamemode\core\hooks\sv_hooks.lua`: 4
- `plugins\healthproblems\sv_hooks.lua`: 4
- `plugins\needs\entities\entities\nut_waterfaucet\init.lua`: 3
- `plugins\needs\cl_hooks.lua`: 3
- `plugins\needs\items\base\sh_food.lua`: 3
- `gamemode\config\sh_config.lua`: 3
- `plugins\needs\entities\entities\nut_cooking_board\init.lua`: 2
- `plugins\needs\entities\entities\nut_cooking_pottea\cl_init.lua`: 2
- `plugins\needs\entities\entities\nut_cooking_pan\cl_init.lua`: 2
- `plugins\gadgets\cl_hooks.lua`: 2
- `plugins\needs\entities\entities\nut_cooking_board\cl_init.lua`: 2
- `schema\libs\sv_utils.lua`: 2
- `plugins\needs\entities\entities\nut_cooking_kettle\cl_init.lua`: 2
- `plugins\needs\entities\entities\nut_cooking_oven\cl_init.lua`: 2
- `plugins\needs\items\sh_water_filter.lua`: 2

## Connected Plugins / Subsystems

- `healthproblems`: 9
- `gadgets`: 6
- `farming`: 4
- `admintools`: 3
- `area`: 3
- `biorezonance`: 3
- `crafting`: 3
- `lightitems`: 3
- `mining`: 3
- `mnhr`: 3
- `radio`: 3
- `storage`: 3
- `vendor`: 3
- `ragdollinteraction`: 2
- `cassetteplayer`: 2
- `lootablecontainers`: 2
- `saveitems.lua`: 2
- `inventory`: 1
- `playerinjuries`: 1
- `snowy_components`: 1

## Runtime Propagation Hubs

- degree `112` | `plugin` | `needs` | `plugin:needs`
- degree `71` | `hook_event` | `LoadData` | `hook:LoadData`
- degree `61` | `file` | `plugins\needs\sv_hooks.lua` | `file:plugins/needs/sv_hooks.lua`
- degree `57` | `hook_event` | `SaveData` | `hook:SaveData`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737` | `emitter:emitter_0b3042055654`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641` | `emitter:emitter_5e2c403ba5e0`
- degree `43` | `hook_event` | `CreateUsingInterface` | `hook:CreateUsingInterface`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\sv_data.lua:95` | `emitter:emitter_79872d3f1d81`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:731` | `emitter:emitter_268470f88607`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652` | `emitter:emitter_1375b23e6ac9`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:3` | `listener:listener_107469c23641`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:2` | `listener:listener_c14bd3d652fb`
- degree `31` | `file` | `plugins\needs\entities\entities\nut_cooking_base.lua` | `file:plugins/needs/entities/entities/nut_cooking_base.lua`
- degree `26` | `network_message` | `nutStorageOpen` | `netmsg:gmod_net:nutStorageOpen`
- degree `25` | `hook_event` | `PlayerDeath` | `hook:PlayerDeath`
- degree `20` | `hook_event` | `LoadNutFonts` | `hook:LoadNutFonts`
- degree `19` | `hook_event` | `CharacterPreSave` | `hook:CharacterPreSave`
- degree `18` | `network_message` | `entFreezeState` | `netmsg:netstream:entFreezeState`
- degree `18` | `file` | `plugins\needs\entities\entities\nut_cooking_kettle\init.lua` | `file:plugins/needs/entities/entities/nut_cooking_kettle/init.lua`
- degree `18` | `file` | `plugins\needs\derma\cl_cookingboard_interface.lua` | `file:plugins/needs/derma/cl_cookingboard_interface.lua`
- degree `17` | `file` | `plugins\needs\entities\entities\nut_cooking_oven\init.lua` | `file:plugins/needs/entities/entities/nut_cooking_oven/init.lua`
- degree `16` | `network_message` | `item.player` | `netmsg:netstream:item.player`
- degree `15` | `hook_emitter` | `emit CharacterPreSave @ gamemode\core\meta\sh_character.lua:42` | `emitter:emitter_6566c7251cfe`
- degree `15` | `file` | `plugins\needs\cl_hooks.lua` | `file:plugins/needs/cl_hooks.lua`
- degree `14` | `file` | `plugins\needs\derma\cl_cooking_interface.lua` | `file:plugins/needs/derma/cl_cooking_interface.lua`

## Topology Hubs

- degree `112` | `plugin` | `needs` | `plugin:needs`
- degree `71` | `hook_event` | `LoadData` | `hook:LoadData`
- degree `61` | `file` | `plugins\needs\sv_hooks.lua` | `file:plugins/needs/sv_hooks.lua`
- degree `57` | `hook_event` | `SaveData` | `hook:SaveData`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737` | `emitter:emitter_0b3042055654`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641` | `emitter:emitter_5e2c403ba5e0`
- degree `43` | `hook_event` | `CreateUsingInterface` | `hook:CreateUsingInterface`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\sv_data.lua:95` | `emitter:emitter_79872d3f1d81`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:731` | `emitter:emitter_268470f88607`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652` | `emitter:emitter_1375b23e6ac9`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:3` | `listener:listener_107469c23641`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:2` | `listener:listener_c14bd3d652fb`
- degree `31` | `file` | `plugins\needs\entities\entities\nut_cooking_base.lua` | `file:plugins/needs/entities/entities/nut_cooking_base.lua`
- degree `26` | `network_message` | `nutStorageOpen` | `netmsg:gmod_net:nutStorageOpen`
- degree `25` | `hook_event` | `PlayerDeath` | `hook:PlayerDeath`
- degree `20` | `hook_event` | `LoadNutFonts` | `hook:LoadNutFonts`
- degree `19` | `hook_event` | `CharacterPreSave` | `hook:CharacterPreSave`
- degree `18` | `network_message` | `entFreezeState` | `netmsg:netstream:entFreezeState`
- degree `18` | `file` | `plugins\needs\entities\entities\nut_cooking_kettle\init.lua` | `file:plugins/needs/entities/entities/nut_cooking_kettle/init.lua`
- degree `18` | `file` | `plugins\needs\derma\cl_cookingboard_interface.lua` | `file:plugins/needs/derma/cl_cookingboard_interface.lua`
- degree `17` | `file` | `plugins\needs\entities\entities\nut_cooking_oven\init.lua` | `file:plugins/needs/entities/entities/nut_cooking_oven/init.lua`
- degree `16` | `network_message` | `item.player` | `netmsg:netstream:item.player`
- degree `15` | `hook_emitter` | `emit CharacterPreSave @ gamemode\core\meta\sh_character.lua:42` | `emitter:emitter_6566c7251cfe`
- degree `15` | `file` | `plugins\needs\cl_hooks.lua` | `file:plugins/needs/cl_hooks.lua`
- degree `14` | `file` | `plugins\needs\derma\cl_cooking_interface.lua` | `file:plugins/needs/derma/cl_cooking_interface.lua`

## Runtime Risks

- Review high-degree hubs for hidden coupling.
- Review network signals for synchronization ownership.
- Review timers for scheduler or debounce behavior.
- Review realm crossings for client/server authority issues.

## Notes

This document is generated from topology only. Use raw Lua only for exact validation.
