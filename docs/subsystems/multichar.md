# Subsystem: multichar

## Purpose

Deterministic subsystem summary generated from runtime topology.

## Topology Summary

- Nodes: **204**
- Edges: **5541**

## Node Types

- `hook_listener`: 69
- `hook_event`: 24
- `hook_emitter`: 23
- `network_payload_operation`: 20
- `network_operation`: 17
- `network_context`: 12
- `timer_operation`: 11
- `file`: 11
- `network_message`: 5
- `timer`: 3
- `timer_class`: 3
- `realm`: 3
- `subsystem`: 1
- `plugin`: 1
- `timer_risk`: 1

## Edge Types

- `runs_in_realm`: 4470
- `classified_as`: 192
- `references_timer`: 139
- `schedules_delay`: 132
- `dispatches_to`: 85
- `listens_to`: 81
- `contains_listener`: 69
- `registers_listener`: 69
- `listens_to_event`: 47
- `emits`: 27
- `contains_emitter`: 23
- `contains_network_payload_operation`: 20
- `owns_file`: 18
- `contains_network_operation`: 17
- `belongs_to_subsystem`: 16
- `emits_event`: 15
- `contains_network_context`: 12
- `context_references_network_message`: 12
- `contains_timer_operation`: 11
- `owns_timer_operation`: 11

## Major Hooks

- `listen PlayerLoadedChar @ plugins\spawnsaver.lua:18`: 2
- `listen ConfigureCharacterCreationSteps @ plugins\traits\sh_creation.lua:403`: 2
- `listen createCharacter @ plugins\multichar\sh_plugin.lua:55`: 2
- `listen syncCharList @ plugins\multichar\sh_plugin.lua:8`: 2
- `listen PlayerNutDataLoaded @ plugins\multichar\sv_hooks.lua:1`: 2
- `listen chooseCharacter @ plugins\multichar\sh_plugin.lua:34`: 2
- `listen PlayerLoadedChar @ plugins\ammosave.lua:63`: 2
- `listen deleteCharacter @ plugins\multichar\sh_plugin.lua:98`: 2
- `NutScriptLoaded`: 1
- `AdjustCreationData`: 1
- `listen OnCharCreated @ schema\hooks\sv_hooks.lua:88`: 1
- `ShouldMenuButtonShow`: 1
- `listen OnCharCreated @ plugins\logging.lua:155`: 1
- `listen LoadFonts @ plugins\multichar\plugins\charselect\sh_plugin.lua:46`: 1
- `listen PlayerLoadedChar @ plugins\multichar\sv_hooks.lua:48`: 1
- `ConfigureCharacterCreationSteps`: 1
- `emit NutScriptLoaded @ gamemode\core\hooks\cl_hooks.lua:365`: 1
- `nutCharDeleted`: 1
- `listen CharacterLoaded @ schema\hooks\cl_hooks.lua:121`: 1
- `PlayerLoadedChar`: 1

## Major Network Signals

- `receive nutCharChoose`: 2
- `Receive nutCharCreate`: 2
- `receive nutCharCreate`: 2
- `Receive nutCharChoose`: 2
- `send nutCharChoose`: 2
- `Start nutCharCreate`: 2
- `Start nutCharChoose`: 2
- `send nutCharCreate`: 2
- `send nutCharDelete`: 1
- `Start nutCharDelete`: 1
- `Receive nutCharList`: 1
- `register nutCharDelete`: 1
- `receive nutCharList`: 1
- `register nutCharList`: 1
- `register nutCharChoose`: 1
- `register nutCharCreate`: 1
- `nutCharList`: 1
- `nutCharChoose`: 1
- `send nutCharList`: 1
- `Receive nutCharDelete`: 1

## Lifecycle Propagation

- `listen PlayerLoadedChar @ plugins\spawnsaver.lua:18`: 2
- `PrePlayerLoadedChar`: 2
- `listen PrePlayerLoadedChar @ gamemode\core\hooks\sv_hooks.lua:180`: 2
- `listen PrePlayerLoadedChar @ plugins\rechargeableequipment\sh_plugin.lua:163`: 2
- `listen PrePlayerLoadedChar @ plugins\mnhr\sh_plugin.lua:243`: 2
- `listen PrePlayerLoadedChar @ plugins\armor\sh_plugin.lua:264`: 2
- `listen PrePlayerLoadedChar @ plugins\healthproblems\sv_hooks.lua:585`: 2
- `listen PrePlayerLoadedChar @ plugins\mnhr\sh_plugin.lua:244`: 2
- `listen PrePlayerLoadedChar @ plugins\healthproblems\sv_hooks.lua:584`: 2
- `listen PrePlayerLoadedChar @ plugins\armor\sh_plugin.lua:263`: 2
- `listen PlayerLoadedChar @ plugins\ammosave.lua:63`: 2
- `emit PrePlayerLoadedChar @ plugins\multichar\sv_networking.lua:35`: 2
- `listen PrePlayerLoadedChar @ plugins\rechargeableequipment\sh_plugin.lua:162`: 2
- `listen PrePlayerLoadedChar @ plugins\biorezonance\sh_plugin.lua:542`: 2
- `listen PrePlayerLoadedChar @ plugins\biorezonance\sh_plugin.lua:541`: 2
- `listen PlayerLoadedChar @ plugins\multichar\sv_hooks.lua:48`: 1
- `listen CharacterLoaded @ schema\hooks\cl_hooks.lua:121`: 1
- `PlayerLoadedChar`: 1
- `listen PlayerLoadedChar @ plugins\multichar\sv_hooks.lua:49`: 1
- `listen PlayerLoadedChar @ plugins\area\sh_plugin.lua:95`: 1

## Synchronization Hotspots

- none detected

## Important Timers

- `high_frequency_infinite_timer`: 2
- `timer_remove@plugins\multichar\plugins\charselect\derma\cl_bg_music.lua:62`: 1
- `nutMusicFader`: 1
- `timer_simple@plugins\multichar\sv_hooks.lua:35`: 1
- `one_shot_delay`: 1
- `timer_create@plugins\multichar\plugins\charselect\derma\cl_bg_music.lua:46`: 1
- `timer_simple@plugins\multichar\sv_networking.lua:120`: 1
- `timer_remove@plugins\multichar\plugins\charselect\derma\cl_bg_music.lua:16`: 1
- `timer_simple@plugins\multichar\plugins\charselect\derma\cl_confirmation.lua:82`: 1
- `timer_simple`: 1
- `timer_remove@plugins\multichar\plugins\charselect\derma\cl_bg_music.lua:59`: 1
- `timer_simple@plugins\multichar\plugins\charselect\derma\cl_selection.lua:72`: 1
- `timer_lifecycle_operation`: 1
- `timer_create@plugins\multichar\plugins\charselect\derma\cl_creation.lua:118`: 1
- `timer_remove@plugins\multichar\plugins\charselect\derma\cl_creation.lua:96`: 1
- `timer_remove@plugins\multichar\plugins\charselect\derma\cl_bg_music.lua:10`: 1
- `nutFailedToCreate`: 1

## Realms

- `shared`: 55
- `server`: 30
- `client`: 30

## Major Files

- `plugins\multichar\sh_plugin.lua`: 13
- `plugins\multichar\sv_hooks.lua`: 12
- `plugins\multichar\plugins\charselect\sh_plugin.lua`: 9
- `plugins\multichar\sv_networking.lua`: 9
- `plugins\multichar\plugins\charselect\derma\cl_bg_music.lua`: 6
- `plugins\multichar\plugins\charselect\derma\cl_creation.lua`: 6
- `gamemode\core\hooks\sv_hooks.lua`: 5
- `plugins\logging.lua`: 4
- `gamemode\core\hooks\cl_hooks.lua`: 4
- `plugins\traits\sh_plugin.lua`: 4
- `plugins\multichar\cl_networking.lua`: 3
- `plugins\multichar\plugins\charselect\derma\cl_selection.lua`: 3
- `plugins\spawnsaver.lua`: 2
- `plugins\traits\sh_creation.lua`: 2
- `plugins\area\sh_plugin.lua`: 2
- `plugins\multichar\plugins\charselect\derma\cl_character.lua`: 2
- `plugins\attributes\sh_plugin.lua`: 2
- `plugins\loyal_system\sh_plugin.lua`: 2
- `gamemode\core\hooks\sh_hooks.lua`: 2
- `plugins\multichar\plugins\charselect\derma\steps\cl_biography.lua`: 2

## Connected Plugins / Subsystems

- `traits`: 9
- `area`: 4
- `armor`: 3
- `attributes`: 3
- `biorezonance`: 3
- `healthproblems`: 3
- `mnhr`: 3
- `f1menu`: 1
- `pac`: 1
- `vendor`: 1

## Runtime Propagation Hubs

- degree `87` | `plugin` | `multichar` | `plugin:multichar`
- degree `47` | `file` | `plugins\multichar\sv_networking.lua` | `file:plugins/multichar/sv_networking.lua`
- degree `45` | `file` | `plugins\multichar\sh_plugin.lua` | `file:plugins/multichar/sh_plugin.lua`
- degree `24` | `network_message` | `nutCharCreate` | `netmsg:gmod_net:nutCharCreate`
- degree `23` | `hook_event` | `PlayerLoadedChar` | `hook:PlayerLoadedChar`
- degree `20` | `hook_event` | `PrePlayerLoadedChar` | `hook:PrePlayerLoadedChar`
- degree `18` | `network_message` | `nutCharChoose` | `netmsg:gmod_net:nutCharChoose`
- degree `17` | `hook_event` | `LoadFonts` | `hook:LoadFonts`
- degree `17` | `hook_emitter` | `emit PlayerLoadedChar @ plugins\multichar\sv_networking.lua:37` | `emitter:emitter_750ad8b7d8cd`
- degree `16` | `hook_event` | `OnCharCreated` | `hook:OnCharCreated`
- degree `15` | `hook_emitter` | `emit PrePlayerLoadedChar @ plugins\multichar\sv_networking.lua:35` | `emitter:emitter_a6ea50326fb4`
- degree `15` | `file` | `plugins\multichar\sv_hooks.lua` | `file:plugins/multichar/sv_hooks.lua`
- degree `14` | `hook_emitter` | `emit LoadFonts @ gamemode\core\hooks\cl_hooks.lua:281` | `emitter:emitter_521b95048ed6`
- degree `12` | `network_message` | `nutCharList` | `netmsg:gmod_net:nutCharList`
- degree `12` | `hook_emitter` | `emit OnCharCreated @ plugins\multichar\sv_networking.lua:104` | `emitter:emitter_daa38e73cb71`
- degree `12` | `file` | `plugins\multichar\cl_networking.lua` | `file:plugins/multichar/cl_networking.lua`
- degree `11` | `hook_event` | `CharacterLoaded` | `hook:CharacterLoaded`
- degree `11` | `file` | `plugins\multichar\plugins\charselect\sh_plugin.lua` | `file:plugins/multichar/plugins/charselect/sh_plugin.lua`
- degree `10` | `network_message` | `nutCharDelete` | `netmsg:gmod_net:nutCharDelete`
- degree `9` | `hook_listener` | `listen GetDefaultCharName @ gamemode\core\hooks\sh_hooks.lua:264` | `listener:listener_9b2e5ec02224`
- degree `9` | `hook_event` | `ConfigureCharacterCreationSteps` | `hook:ConfigureCharacterCreationSteps`
- degree `9` | `file` | `plugins\multichar\plugins\charselect\derma\cl_creation.lua` | `file:plugins/multichar/plugins/charselect/derma/cl_creation.lua`
- degree `8` | `timer_operation` | `timer_create@plugins\multichar\plugins\charselect\derma\cl_bg_music.lua:46` | `timer_op:plugins/multichar/plugins/charselect/derma/cl_bg_music.lua:46:timer_create:nutMusicFader:41`
- degree `8` | `hook_event` | `PostPlayerInitialSpawn` | `hook:PostPlayerInitialSpawn`
- degree `8` | `hook_event` | `NutScriptLoaded` | `hook:NutScriptLoaded`

## Topology Hubs

- degree `87` | `plugin` | `multichar` | `plugin:multichar`
- degree `47` | `file` | `plugins\multichar\sv_networking.lua` | `file:plugins/multichar/sv_networking.lua`
- degree `45` | `file` | `plugins\multichar\sh_plugin.lua` | `file:plugins/multichar/sh_plugin.lua`
- degree `24` | `network_message` | `nutCharCreate` | `netmsg:gmod_net:nutCharCreate`
- degree `23` | `hook_event` | `PlayerLoadedChar` | `hook:PlayerLoadedChar`
- degree `20` | `hook_event` | `PrePlayerLoadedChar` | `hook:PrePlayerLoadedChar`
- degree `18` | `network_message` | `nutCharChoose` | `netmsg:gmod_net:nutCharChoose`
- degree `17` | `hook_event` | `LoadFonts` | `hook:LoadFonts`
- degree `17` | `hook_emitter` | `emit PlayerLoadedChar @ plugins\multichar\sv_networking.lua:37` | `emitter:emitter_750ad8b7d8cd`
- degree `16` | `hook_event` | `OnCharCreated` | `hook:OnCharCreated`
- degree `15` | `hook_emitter` | `emit PrePlayerLoadedChar @ plugins\multichar\sv_networking.lua:35` | `emitter:emitter_a6ea50326fb4`
- degree `15` | `file` | `plugins\multichar\sv_hooks.lua` | `file:plugins/multichar/sv_hooks.lua`
- degree `14` | `hook_emitter` | `emit LoadFonts @ gamemode\core\hooks\cl_hooks.lua:281` | `emitter:emitter_521b95048ed6`
- degree `12` | `network_message` | `nutCharList` | `netmsg:gmod_net:nutCharList`
- degree `12` | `hook_emitter` | `emit OnCharCreated @ plugins\multichar\sv_networking.lua:104` | `emitter:emitter_daa38e73cb71`
- degree `12` | `file` | `plugins\multichar\cl_networking.lua` | `file:plugins/multichar/cl_networking.lua`
- degree `11` | `hook_event` | `CharacterLoaded` | `hook:CharacterLoaded`
- degree `11` | `file` | `plugins\multichar\plugins\charselect\sh_plugin.lua` | `file:plugins/multichar/plugins/charselect/sh_plugin.lua`
- degree `10` | `network_message` | `nutCharDelete` | `netmsg:gmod_net:nutCharDelete`
- degree `9` | `hook_listener` | `listen GetDefaultCharName @ gamemode\core\hooks\sh_hooks.lua:264` | `listener:listener_9b2e5ec02224`
- degree `9` | `hook_event` | `ConfigureCharacterCreationSteps` | `hook:ConfigureCharacterCreationSteps`
- degree `9` | `file` | `plugins\multichar\plugins\charselect\derma\cl_creation.lua` | `file:plugins/multichar/plugins/charselect/derma/cl_creation.lua`
- degree `8` | `timer_operation` | `timer_create@plugins\multichar\plugins\charselect\derma\cl_bg_music.lua:46` | `timer_op:plugins/multichar/plugins/charselect/derma/cl_bg_music.lua:46:timer_create:nutMusicFader:41`
- degree `8` | `hook_event` | `PostPlayerInitialSpawn` | `hook:PostPlayerInitialSpawn`
- degree `8` | `hook_event` | `NutScriptLoaded` | `hook:NutScriptLoaded`

## Runtime Risks

- Review high-degree hubs for hidden coupling.
- Review network signals for synchronization ownership.
- Review timers for scheduler or debounce behavior.
- Review realm crossings for client/server authority issues.

## Notes

This document is generated from topology only. Use raw Lua only for exact validation.
