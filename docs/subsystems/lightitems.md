# Subsystem: lightitems

## Purpose

Deterministic subsystem summary generated from runtime topology.

## Topology Summary

- Nodes: **227**
- Edges: **6323**

## Node Types

- `timer_operation`: 79
- `network_operation`: 64
- `network_message`: 26
- `file`: 15
- `hook_listener`: 12
- `hook_emitter`: 8
- `hook_event`: 8
- `network_payload_operation`: 4
- `realm`: 3
- `timer_class`: 2
- `timer`: 2
- `network_context`: 2
- `plugin`: 1
- `subsystem`: 1

## Edge Types

- `runs_in_realm`: 4470
- `belongs_to_subsystem`: 264
- `dispatches_to`: 247
- `references_timer`: 203
- `classified_as`: 193
- `schedules_delay`: 132
- `listens_to`: 123
- `contains_timer_operation`: 79
- `owns_timer_operation`: 79
- `listens_to_event`: 69
- `contains_network_operation`: 64
- `file_sends_network_message`: 51
- `sends_network_message`: 51
- `schedules_entity_action`: 46
- `has_timer_risk`: 33
- `emits`: 31
- `network_dispatches_to`: 29
- `file_receives_network_message`: 23
- `owns_file`: 23
- `receives_network_message`: 23

## Major Hooks

- `emit CreateUsingInterface @ plugins\lightitems\entities\entities\nut_diode_light\cl_init.lua:121`: 1
- `emit SaveData @ gamemode\core\sv_data.lua:95`: 1
- `InitPostEntity`: 1
- `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652`: 1
- `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:2`: 1
- `listen RenderScene @ plugins\lightitems\cl_hooks.lua:217`: 1
- `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737`: 1
- `listen LoadData @ plugins\lightitems\sh_plugin.lua:270`: 1
- `CreateUsingInterface`: 1
- `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641`: 1
- `LoadData`: 1
- `listen Think @ plugins\lightitems\cl_hooks.lua:187`: 1
- `listen SaveData @ plugins\lightitems\sh_plugin.lua:36`: 1
- `listen LoadData @ plugins\lightitems\sh_plugin.lua:269`: 1
- `listen SaveData @ plugins\lightitems\sh_plugin.lua:37`: 1
- `RenderScene`: 1
- `SaveData`: 1
- `emit CreateUsingInterface @ plugins\lightitems\entities\entities\nut_electric_generator\cl_init.lua:21`: 1
- `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:3`: 1
- `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:731`: 1

## Major Network Signals

- `netstream send activator`: 5
- `netstream send elPanelTryFix`: 4
- `netstream send targets`: 3
- `register IsFix`: 2
- `netstream send genQuickCheck`: 2
- `netstream send lightItemSwitchPower`: 2
- `netstream send lightItemGensView`: 2
- `netstream send lightItemGensViewShow`: 2
- `netstream send lightItemTakeOff`: 2
- `netstream send genFill`: 2
- `netstream send genCheck`: 2
- `register RandomNumber`: 2
- `netstream hook RequestTopologyBake`: 1
- `netstream send elPanelAttachToGen`: 1
- `genFill`: 1
- `Topology_BatchEnd`: 1
- `targets`: 1
- `netstream hook lightItemSwitchPower`: 1
- `netstream send elPanelRelaySetUp`: 1
- `netstream hook elPanelAttachToGen`: 1

## Lifecycle Propagation

- `emit SaveData @ gamemode\core\sv_data.lua:95`: 1
- `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652`: 1
- `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737`: 1
- `listen LoadData @ plugins\lightitems\sh_plugin.lua:270`: 1
- `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641`: 1
- `LoadData`: 1
- `listen SaveData @ plugins\lightitems\sh_plugin.lua:36`: 1
- `listen LoadData @ plugins\lightitems\sh_plugin.lua:269`: 1
- `listen SaveData @ plugins\lightitems\sh_plugin.lua:37`: 1
- `SaveData`: 1
- `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:731`: 1

## Synchronization Hotspots

- none detected

## Important Timers

- `entity_timer_create@plugins\lightitems\items\electrical_appliances\sh_electric_panel.lua:41`: 1
- `entity_timer_remove@plugins\lightitems\entities\entities\nut_electric_generator\init.lua:322`: 1
- `entity_timer_remove@plugins\lightitems\entities\entities\nut_electric_generator\init.lua:798`: 1
- `entity_timer_or_action_call@plugins\lightitems\entities\entities\nut_electric_generator\init.lua:322`: 1
- `entity_timer_or_action_call@plugins\lightitems\entities\entities\nut_electric_generator\init.lua:325`: 1
- `entity_timer_exists@plugins\lightitems\entities\entities\nut_electric_generator\init.lua:313`: 1
- `entity_timer_exists@plugins\lightitems\entities\entities\nut_electric_generator\init.lua:320`: 1
- `timer_simple@plugins\lightitems\sv_hooks.lua:282`: 1
- `entity_timer_create@plugins\lightitems\entities\entities\nut_electric_generator\init.lua:325`: 1
- `entity_timer_or_action_call@plugins\lightitems\entities\entities\nut_diode_light\init.lua:126`: 1
- `entity_timer_remove@plugins\lightitems\entities\entities\nut_diode_light\init.lua:258`: 1
- `entity_timer_or_action_call@plugins\lightitems\entities\entities\nut_diode_light\init.lua:76`: 1
- `entity_timer_create@plugins\lightitems\entities\entities\nut_electric_generator\init.lua:357`: 1
- `entity_timer_create@plugins\lightitems\entities\entities\nut_electric_generator\init.lua:525`: 1
- `entity_timer_remove@plugins\lightitems\entities\entities\nut_diode_light\init.lua:128`: 1
- `timer_simple@plugins\lightitems\sh_plugin.lua:341`: 1
- `player_cancelable_action_timer@plugins\lightitems\entities\entities\nut_electric_panel\init.lua:394`: 1
- `entity_timer_or_action_call@plugins\lightitems\entities\entities\nut_electric_generator\init.lua:280`: 1
- `player_cancelable_action_timer@plugins\lightitems\entities\entities\nut_electric_generator\init.lua:565`: 1
- `entity_timer_exists@plugins\lightitems\items\electrical_appliances\sh_diode_light.lua:109`: 1

## Realms

- `server`: 73
- `client`: 18
- `shared`: 17

## Major Files

- `plugins\lightitems\entities\entities\nut_electric_generator\init.lua`: 41
- `plugins\lightitems\entities\entities\nut_diode_light\init.lua`: 15
- `plugins\lightitems\cl_hooks.lua`: 9
- `plugins\lightitems\entities\entities\nut_electric_panel\init.lua`: 9
- `plugins\lightitems\sh_plugin.lua`: 8
- `plugins\lightitems\items\electrical_appliances\sh_electric_panel.lua`: 5
- `plugins\lightitems\items\electrical_appliances\sh_diode_light.lua`: 5
- `plugins\lightitems\sv_hooks.lua`: 4
- `gamemode\core\hooks\sv_hooks.lua`: 4
- `plugins\lightitems\entities\entities\nut_diode_light\cl_init.lua`: 2
- `plugins\lightitems\entities\entities\nut_electric_panel\cl_init.lua`: 2
- `plugins\gadgets\cl_hooks.lua`: 2
- `plugins\lightitems\entities\entities\nut_chemlight_glow\init.lua`: 2
- `plugins\lightitems\entities\entities\nut_electric_generator\cl_init.lua`: 2
- `gamemode\core\sv_data.lua`: 1

## Connected Plugins / Subsystems

- `gadgets`: 6
- `admintools`: 4
- `biorezonance`: 4
- `crafting`: 3
- `farming`: 3
- `mining`: 3
- `mnhr`: 3
- `needs`: 3
- `radio`: 3
- `storage`: 3
- `vendor`: 3
- `ragdollinteraction`: 2
- `cassetteplayer`: 2
- `lootablecontainers`: 2
- `saveitems.lua`: 2
- `area`: 1
- `chatbox`: 1
- `hud`: 1
- `newvoice.lua`: 1

## Runtime Propagation Hubs

- degree `120` | `plugin` | `lightitems` | `plugin:lightitems`
- degree `71` | `hook_event` | `LoadData` | `hook:LoadData`
- degree `57` | `hook_event` | `SaveData` | `hook:SaveData`
- degree `54` | `file` | `plugins\lightitems\entities\entities\nut_electric_generator\init.lua` | `file:plugins/lightitems/entities/entities/nut_electric_generator/init.lua`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737` | `emitter:emitter_0b3042055654`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641` | `emitter:emitter_5e2c403ba5e0`
- degree `47` | `file` | `plugins\lightitems\sv_hooks.lua` | `file:plugins/lightitems/sv_hooks.lua`
- degree `43` | `hook_event` | `CreateUsingInterface` | `hook:CreateUsingInterface`
- degree `41` | `file` | `plugins\lightitems\cl_hooks.lua` | `file:plugins/lightitems/cl_hooks.lua`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\sv_data.lua:95` | `emitter:emitter_79872d3f1d81`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:731` | `emitter:emitter_268470f88607`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652` | `emitter:emitter_1375b23e6ac9`
- degree `38` | `network_message` | `activator` | `netmsg:netstream:activator`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:3` | `listener:listener_107469c23641`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:2` | `listener:listener_c14bd3d652fb`
- degree `27` | `file` | `plugins\lightitems\entities\entities\nut_electric_panel\init.lua` | `file:plugins/lightitems/entities/entities/nut_electric_panel/init.lua`
- degree `24` | `file` | `plugins\lightitems\derma\cl_gen_interface.lua` | `file:plugins/lightitems/derma/cl_gen_interface.lua`
- degree `23` | `hook_event` | `Think` | `hook:Think`
- degree `22` | `hook_event` | `PlayerInitialSpawn` | `hook:PlayerInitialSpawn`
- degree `20` | `file` | `plugins\lightitems\entities\entities\nut_diode_light\init.lua` | `file:plugins/lightitems/entities/entities/nut_diode_light/init.lua`
- degree `16` | `file` | `plugins\lightitems\derma\cl_electricpanel_interface.lua` | `file:plugins/lightitems/derma/cl_electricpanel_interface.lua`
- degree `14` | `network_message` | `RandomNumber` | `netmsg:gmod_net:RandomNumber`
- degree `13` | `hook_event` | `InitPostEntity` | `hook:InitPostEntity`
- degree `12` | `hook_event` | `PostDrawTranslucentRenderables` | `hook:PostDrawTranslucentRenderables`
- degree `11` | `file` | `plugins\lightitems\sh_plugin.lua` | `file:plugins/lightitems/sh_plugin.lua`

## Topology Hubs

- degree `120` | `plugin` | `lightitems` | `plugin:lightitems`
- degree `71` | `hook_event` | `LoadData` | `hook:LoadData`
- degree `57` | `hook_event` | `SaveData` | `hook:SaveData`
- degree `54` | `file` | `plugins\lightitems\entities\entities\nut_electric_generator\init.lua` | `file:plugins/lightitems/entities/entities/nut_electric_generator/init.lua`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:737` | `emitter:emitter_0b3042055654`
- degree `49` | `hook_emitter` | `emit LoadData @ gamemode\core\hooks\sv_hooks.lua:641` | `emitter:emitter_5e2c403ba5e0`
- degree `47` | `file` | `plugins\lightitems\sv_hooks.lua` | `file:plugins/lightitems/sv_hooks.lua`
- degree `43` | `hook_event` | `CreateUsingInterface` | `hook:CreateUsingInterface`
- degree `41` | `file` | `plugins\lightitems\cl_hooks.lua` | `file:plugins/lightitems/cl_hooks.lua`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\sv_data.lua:95` | `emitter:emitter_79872d3f1d81`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:731` | `emitter:emitter_268470f88607`
- degree `39` | `hook_emitter` | `emit SaveData @ gamemode\core\hooks\sv_hooks.lua:652` | `emitter:emitter_1375b23e6ac9`
- degree `38` | `network_message` | `activator` | `netmsg:netstream:activator`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:3` | `listener:listener_107469c23641`
- degree `31` | `hook_listener` | `listen CreateUsingInterface @ plugins\gadgets\cl_hooks.lua:2` | `listener:listener_c14bd3d652fb`
- degree `27` | `file` | `plugins\lightitems\entities\entities\nut_electric_panel\init.lua` | `file:plugins/lightitems/entities/entities/nut_electric_panel/init.lua`
- degree `24` | `file` | `plugins\lightitems\derma\cl_gen_interface.lua` | `file:plugins/lightitems/derma/cl_gen_interface.lua`
- degree `23` | `hook_event` | `Think` | `hook:Think`
- degree `22` | `hook_event` | `PlayerInitialSpawn` | `hook:PlayerInitialSpawn`
- degree `20` | `file` | `plugins\lightitems\entities\entities\nut_diode_light\init.lua` | `file:plugins/lightitems/entities/entities/nut_diode_light/init.lua`
- degree `16` | `file` | `plugins\lightitems\derma\cl_electricpanel_interface.lua` | `file:plugins/lightitems/derma/cl_electricpanel_interface.lua`
- degree `14` | `network_message` | `RandomNumber` | `netmsg:gmod_net:RandomNumber`
- degree `13` | `hook_event` | `InitPostEntity` | `hook:InitPostEntity`
- degree `12` | `hook_event` | `PostDrawTranslucentRenderables` | `hook:PostDrawTranslucentRenderables`
- degree `11` | `file` | `plugins\lightitems\sh_plugin.lua` | `file:plugins/lightitems/sh_plugin.lua`

## Runtime Risks

- Review high-degree hubs for hidden coupling.
- Review network signals for synchronization ownership.
- Review timers for scheduler or debounce behavior.
- Review realm crossings for client/server authority issues.

## Notes

This document is generated from topology only. Use raw Lua only for exact validation.
