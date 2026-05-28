# Subsystem: healthproblems

## Purpose

Deterministic subsystem summary generated from runtime topology.

## Topology Summary

- Nodes: **394**
- Edges: **6874**

## Node Types

- `hook_emitter`: 120
- `network_operation`: 83
- `file`: 62
- `hook_listener`: 54
- `hook_event`: 29
- `timer_operation`: 19
- `network_message`: 14
- `timer`: 5
- `realm`: 3
- `timer_class`: 2
- `plugin`: 1
- `subsystem`: 1
- `timer_risk`: 1

## Edge Types

- `runs_in_realm`: 4470
- `classified_as`: 395
- `references_timer`: 299
- `dispatches_to`: 273
- `schedules_entity_action`: 206
- `has_timer_risk`: 182
- `listens_to`: 124
- `contains_emitter`: 120
- `emits`: 120
- `contains_network_operation`: 83
- `file_sends_network_message`: 73
- `sends_network_message`: 73
- `owns_file`: 72
- `listens_to_event`: 70
- `removes_timer`: 57
- `contains_listener`: 54
- `registers_listener`: 54
- `schedules_player_action`: 36
- `emits_event`: 22
- `belongs_to_subsystem`: 19

## Major Hooks

- `emit HandleInfection @ plugins\healthproblems\sh_plugin.lua:155`: 1
- `listen SetInfectionAction @ plugins\healthproblems\sv_hooks.lua:1121`: 1
- `emit CheckBothHandsAmputation @ gamemode\core\hooks\sv_hooks.lua:955`: 1
- `emit HandleBluntInjure @ plugins\armor\sh_plugin.lua:145`: 1
- `emit HandleDiseaseOnCall @ plugins\healthproblems\diseases\wound.lua:32`: 1
- `emit HandleDiseaseOnEnd @ plugins\healthproblems\diseases\amputation.lua:68`: 1
- `listen BiorezHealDiseaseHandle @ plugins\healthproblems\sv_hooks.lua:1159`: 1
- `listen SetInfectionAction @ plugins\healthproblems\sv_hooks.lua:1120`: 1
- `emit HandlePain @ plugins\healthproblems\diseases\healedacidburn.lua:12`: 1
- `listen HandleDiseaseOnEnd @ plugins\healthproblems\sv_hooks.lua:911`: 1
- `listen PrePlayerLoadedChar @ plugins\healthproblems\sv_hooks.lua:585`: 1
- `emit BiorezHealHandle @ plugins\biorezonance\entities\weapons\nut_biorezonance_swep.lua:246`: 1
- `listen HandlePain @ plugins\healthproblems\sv_hooks.lua:775`: 1
- `listen PlayerUse @ plugins\healthproblems\sv_hooks.lua:225`: 1
- `emit HandleBloodLoss @ plugins\healthproblems\diseases\restoreblood.lua:13`: 1
- `emit HandleInfection @ plugins\healthproblems\items\peals\sh_med_surgical_kit.lua:72`: 1
- `emit HandleDiseaseOnEnd @ plugins\healthproblems\diseases\pain.lua:85`: 1
- `listen CheckHandsAmputation @ plugins\healthproblems\sv_hooks.lua:971`: 1
- `listen CheckBothHandsAmputation @ plugins\healthproblems\sv_hooks.lua:975`: 1
- `emit CharacterPreSave @ gamemode\core\meta\sh_character.lua:42`: 1

## Major Network Signals

- `netstream send nut.diseases.stringConsts.hudRemoveStatusIcon`: 26
- `netstream send nut.diseases.stringConsts.hudAddStatusIcon`: 25
- `netstream send nut.diseases.stringConsts.hudHandleStatusIconCount`: 6
- `netstream send diseasesSelectWeapon`: 5
- `netstream send diseasesStatusInterfaceOpen`: 2
- `netstream send ents.GetByIndex`: 2
- `diseasesSelectWeapon`: 1
- `hudRemoveAllStatusIcons`: 1
- `nut.diseases.stringConsts.hudHandleStatusIconCount`: 1
- `nut.diseases.stringConsts.hudAddStatusIcon`: 1
- `netstream hook hudRemoveAllStatusIcons`: 1
- `netstream send diseasesStatusInterfaceTargetGetData`: 1
- `netstream hook diseasesAddBlindness`: 1
- `diseasesStatusInterfaceTargetGetData`: 1
- `netstream send diseasesRemoveBlindness`: 1
- `diseasesHandleSwepSelect`: 1
- `netstream hook diseasesStatusInterfaceClose`: 1
- `nut.diseases.stringConsts.hudRemoveStatusIcon`: 1
- `diseasesAddBlindness`: 1
- `netstream send diseasesHandleSwepSelect`: 1

## Lifecycle Propagation

- `listen PrePlayerLoadedChar @ plugins\healthproblems\sv_hooks.lua:585`: 2
- `PostPlayerLoadout`: 2
- `emit PrePlayerLoadedChar @ plugins\multichar\sv_networking.lua:35`: 2
- `emit PostPlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:367`: 2
- `PrePlayerLoadedChar`: 2
- `listen PostPlayerLoadout @ plugins\healthproblems\sv_hooks.lua:293`: 2
- `listen PrePlayerLoadedChar @ plugins\healthproblems\sv_hooks.lua:584`: 2
- `listen PostPlayerLoadout @ plugins\healthproblems\sv_hooks.lua:294`: 2
- `emit CharacterPreSave @ gamemode\core\meta\sh_character.lua:42`: 1
- `listen CharacterPreSave @ plugins\healthproblems\sv_hooks.lua:575`: 1
- `CharacterPreSave`: 1
- `listen CharacterPreSave @ plugins\healthproblems\sv_hooks.lua:576`: 1

## Synchronization Hotspots

- none detected

## Important Timers

- `entity_timer_exists@plugins\healthproblems\sv_hooks.lua:586`: 1
- `TimerExists`: 1
- `entity_timer_simple@plugins\healthproblems\items\peals\sh_med_autoinjector.lua:56`: 1
- `entity_timer_simple@plugins\healthproblems\items\peals\sh_med_army_stimulator.lua:58`: 1
- `entity_timer_exists@plugins\healthproblems\sv_hooks.lua:679`: 1
- `player_action_timer@plugins\healthproblems\items\base\sh_peals.lua:243`: 1
- `entity_timer_simple@plugins\healthproblems\items\peals\sh_med_gestalt_first_aid_kit.lua:27`: 1
- `entity_timer_simple@plugins\healthproblems\items\peals\sh_bandage.lua:15`: 1
- `RemoveTimer`: 1
- `SetSimpleTimer`: 1
- `entity_timer_remove@plugins\healthproblems\sv_hooks.lua:588`: 1
- `player_action_timer`: 1
- `SetCustomTimer`: 1
- `entity_timer_simple@plugins\healthproblems\sv_hooks.lua:255`: 1
- `entity_timer_create@plugins\healthproblems\sv_hooks.lua:681`: 1
- `entity_timer_simple@plugins\healthproblems\items\peals\sh_med_stimulator.lua:56`: 1
- `entity_timer_simple@plugins\healthproblems\items\peals\sh_med_alkali.lua:14`: 1
- `entity_timer_remove@plugins\healthproblems\sv_hooks.lua:688`: 1
- `entity_timer_simple@plugins\healthproblems\items\peals\sh_health_vial.lua:21`: 1
- `entity_timer_simple@plugins\healthproblems\items\peals\sh_med_pantenol.lua:13`: 1

## Realms

- `shared`: 152
- `server`: 73
- `client`: 3

## Major Files

- `plugins\healthproblems\sv_hooks.lua`: 61
- `plugins\healthproblems\diseases\amputation.lua`: 7
- `plugins\healthproblems\diseases\acidburn.lua`: 6
- `plugins\healthproblems\diseases\heatburn.lua`: 6
- `plugins\healthproblems\diseases\wound.lua`: 6
- `gamemode\items\base\sh_weapons.lua`: 6
- `plugins\healthproblems\diseases\treatedamputation.lua`: 6
- `plugins\armor\sh_plugin.lua`: 5
- `plugins\healthproblems\diseases\healedacidburn.lua`: 5
- `plugins\healthproblems\diseases\healedbonefracture.lua`: 5
- `plugins\healthproblems\diseases\bonefracture.lua`: 5
- `plugins\healthproblems\diseases\healedheatburn.lua`: 5
- `plugins\healthproblems\diseases\stoppingbleeding.lua`: 5
- `plugins\healthproblems\diseases\treatedwound.lua`: 5
- `plugins\healthproblems\diseases\bleeding.lua`: 5
- `plugins\healthproblems\diseases\healedwound.lua`: 5
- `plugins\healthproblems\diseases\treatedbonefracture.lua`: 5
- `gamemode\core\hooks\sv_hooks.lua`: 4
- `plugins\healthproblems\items\base\sh_peals.lua`: 4
- `plugins\healthproblems\diseases\pain.lua`: 4

## Connected Plugins / Subsystems

- `armor`: 4
- `inventory`: 4
- `biorezonance`: 3
- `needs`: 3
- `tying`: 3
- `attributes`: 2
- `gadgets`: 2
- `multichar`: 1
- `snowy_components`: 1
- `admintools`: 1
- `area`: 1
- `bars`: 1
- `hud`: 1
- `mnhr`: 1
- `observer.lua`: 1
- `ragdollinteraction`: 1
- `raiseweapons`: 1
- `traits`: 1
- `wepselect.lua`: 1

## Runtime Propagation Hubs

- degree `183` | `plugin` | `healthproblems` | `plugin:healthproblems`
- degree `96` | `file` | `plugins\healthproblems\sv_hooks.lua` | `file:plugins/healthproblems/sv_hooks.lua`
- degree `52` | `network_message` | `nut.diseases.stringConsts.hudRemoveStatusIcon` | `netmsg:netstream:nut.diseases.stringConsts.hudRemoveStatusIcon`
- degree `50` | `network_message` | `nut.diseases.stringConsts.hudAddStatusIcon` | `netmsg:netstream:nut.diseases.stringConsts.hudAddStatusIcon`
- degree `43` | `hook_listener` | `listen HandleDiseaseOnEnd @ plugins\healthproblems\sv_hooks.lua:912` | `listener:listener_c5055290e761`
- degree `43` | `hook_listener` | `listen HandleDiseaseOnEnd @ plugins\healthproblems\sv_hooks.lua:911` | `listener:listener_1f96f84882ae`
- degree `43` | `hook_event` | `HandleDiseaseOnEnd` | `hook:HandleDiseaseOnEnd`
- degree `37` | `hook_event` | `HUDPaint` | `hook:HUDPaint`
- degree `26` | `hook_event` | `PostPlayerLoadout` | `hook:PostPlayerLoadout`
- degree `25` | `hook_listener` | `listen HandleDiseaseOnCall @ plugins\healthproblems\sv_hooks.lua:886` | `listener:listener_1b8f1f3ebad4`
- degree `25` | `hook_listener` | `listen HandleDiseaseOnCall @ plugins\healthproblems\sv_hooks.lua:885` | `listener:listener_abebaabb5667`
- degree `25` | `hook_event` | `HandleDiseaseOnCall` | `hook:HandleDiseaseOnCall`
- degree `20` | `hook_event` | `PrePlayerLoadedChar` | `hook:PrePlayerLoadedChar`
- degree `20` | `hook_event` | `CheckBothHandsAmputation` | `hook:CheckBothHandsAmputation`
- degree `20` | `hook_emitter` | `emit PostPlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:367` | `emitter:emitter_a6c7c42490cf`
- degree `19` | `hook_event` | `CharacterPreSave` | `hook:CharacterPreSave`
- degree `18` | `hook_event` | `KeyPress` | `hook:KeyPress`
- degree `18` | `file` | `plugins\healthproblems\cl_hooks.lua` | `file:plugins/healthproblems/cl_hooks.lua`
- degree `17` | `hook_listener` | `listen HandlePain @ plugins\healthproblems\sv_hooks.lua:776` | `listener:listener_77287ea1c5a2`
- degree `17` | `hook_listener` | `listen HandlePain @ plugins\healthproblems\sv_hooks.lua:775` | `listener:listener_d01483811216`
- degree `17` | `hook_listener` | `listen CheckBothHandsAmputation @ plugins\healthproblems\sv_hooks.lua:976` | `listener:listener_4739ff5edecd`
- degree `17` | `hook_listener` | `listen CheckBothHandsAmputation @ plugins\healthproblems\sv_hooks.lua:975` | `listener:listener_1b43fef49d25`
- degree `17` | `hook_event` | `HandlePain` | `hook:HandlePain`
- degree `15` | `hook_emitter` | `emit PrePlayerLoadedChar @ plugins\multichar\sv_networking.lua:35` | `emitter:emitter_a6ea50326fb4`
- degree `15` | `hook_emitter` | `emit CharacterPreSave @ gamemode\core\meta\sh_character.lua:42` | `emitter:emitter_6566c7251cfe`

## Topology Hubs

- degree `183` | `plugin` | `healthproblems` | `plugin:healthproblems`
- degree `96` | `file` | `plugins\healthproblems\sv_hooks.lua` | `file:plugins/healthproblems/sv_hooks.lua`
- degree `52` | `network_message` | `nut.diseases.stringConsts.hudRemoveStatusIcon` | `netmsg:netstream:nut.diseases.stringConsts.hudRemoveStatusIcon`
- degree `50` | `network_message` | `nut.diseases.stringConsts.hudAddStatusIcon` | `netmsg:netstream:nut.diseases.stringConsts.hudAddStatusIcon`
- degree `43` | `hook_listener` | `listen HandleDiseaseOnEnd @ plugins\healthproblems\sv_hooks.lua:912` | `listener:listener_c5055290e761`
- degree `43` | `hook_listener` | `listen HandleDiseaseOnEnd @ plugins\healthproblems\sv_hooks.lua:911` | `listener:listener_1f96f84882ae`
- degree `43` | `hook_event` | `HandleDiseaseOnEnd` | `hook:HandleDiseaseOnEnd`
- degree `37` | `hook_event` | `HUDPaint` | `hook:HUDPaint`
- degree `26` | `hook_event` | `PostPlayerLoadout` | `hook:PostPlayerLoadout`
- degree `25` | `hook_listener` | `listen HandleDiseaseOnCall @ plugins\healthproblems\sv_hooks.lua:886` | `listener:listener_1b8f1f3ebad4`
- degree `25` | `hook_listener` | `listen HandleDiseaseOnCall @ plugins\healthproblems\sv_hooks.lua:885` | `listener:listener_abebaabb5667`
- degree `25` | `hook_event` | `HandleDiseaseOnCall` | `hook:HandleDiseaseOnCall`
- degree `20` | `hook_event` | `PrePlayerLoadedChar` | `hook:PrePlayerLoadedChar`
- degree `20` | `hook_event` | `CheckBothHandsAmputation` | `hook:CheckBothHandsAmputation`
- degree `20` | `hook_emitter` | `emit PostPlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:367` | `emitter:emitter_a6c7c42490cf`
- degree `19` | `hook_event` | `CharacterPreSave` | `hook:CharacterPreSave`
- degree `18` | `hook_event` | `KeyPress` | `hook:KeyPress`
- degree `18` | `file` | `plugins\healthproblems\cl_hooks.lua` | `file:plugins/healthproblems/cl_hooks.lua`
- degree `17` | `hook_listener` | `listen HandlePain @ plugins\healthproblems\sv_hooks.lua:776` | `listener:listener_77287ea1c5a2`
- degree `17` | `hook_listener` | `listen HandlePain @ plugins\healthproblems\sv_hooks.lua:775` | `listener:listener_d01483811216`
- degree `17` | `hook_listener` | `listen CheckBothHandsAmputation @ plugins\healthproblems\sv_hooks.lua:976` | `listener:listener_4739ff5edecd`
- degree `17` | `hook_listener` | `listen CheckBothHandsAmputation @ plugins\healthproblems\sv_hooks.lua:975` | `listener:listener_1b43fef49d25`
- degree `17` | `hook_event` | `HandlePain` | `hook:HandlePain`
- degree `15` | `hook_emitter` | `emit PrePlayerLoadedChar @ plugins\multichar\sv_networking.lua:35` | `emitter:emitter_a6ea50326fb4`
- degree `15` | `hook_emitter` | `emit CharacterPreSave @ gamemode\core\meta\sh_character.lua:42` | `emitter:emitter_6566c7251cfe`

## Runtime Risks

- Review high-degree hubs for hidden coupling.
- Review network signals for synchronization ownership.
- Review timers for scheduler or debounce behavior.
- Review realm crossings for client/server authority issues.

## Notes

This document is generated from topology only. Use raw Lua only for exact validation.
