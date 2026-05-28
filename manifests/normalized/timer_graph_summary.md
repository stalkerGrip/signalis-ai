# Timer graph summary
Schema: `timer_graph.v1`
## Inputs
- `timer_creates`: **44**
- `timer_simples`: **132**
- `timer_operations`: **65**
- `entity_timer_calls`: **183**
- `player_action_timers`: **102**
- `legacy_entity_timer_calls`: **82**

## Totals
- Nodes: **940**
- Edges: **4854**
- Timer Operations: **607**
- Timers: **94**
- Files: **163**
- Plugins: **45**

## Node types
- `timer_operation`: **607**
- `file`: **163**
- `timer`: **94**
- `plugin`: **45**
- `subsystem`: **13**
- `timer_class`: **10**
- `timer_risk`: **5**
- `realm`: **3**

## Edge types
- `runs_in_realm`: **770**
- `belongs_to_subsystem`: **607**
- `classified_as`: **607**
- `contains_timer_operation`: **607**
- `owns_timer_operation`: **607**
- `references_timer`: **607**
- `has_timer_risk`: **291**
- `schedules_entity_action`: **207**
- `owns_file`: **163**
- `schedules_delay`: **132**
- `removes_timer`: **110**
- `schedules_player_action`: **102**
- `creates_timer`: **44**

## Timer classes
- `entity_simulation_timer`: **264**
- `one_shot_delay`: **111**
- `player_action_timer`: **102**
- `timer_lifecycle_operation`: **53**
- `next_tick_delay`: **30**
- `infinite_loop_timer`: **24**
- `unknown_timer`: **12**
- `finite_repeating_scheduler`: **4**
- `high_frequency_infinite_timer`: **4**
- `repeating_scheduler`: **3**

## Subsystems
- `misc`: **264**
- `entity_production`: **141**
- `ai_entity`: **54**
- `food_spoilage`: **45**
- `player_action`: **26**
- `health_status`: **19**
- `character`: **16**
- `crafting`: **12**
- `inventory_item_storage`: **9**
- `vendor`: **9**
- `ui_hud`: **5**
- `loot_spawn`: **4**
- `persistence`: **3**

## Risk flags
- `entity_validity_guard_expected`: **182**
- `dynamic_timer_name`: **48**
- `next_tick_or_subframe_delay`: **33**
- `infinite_timer`: **24**
- `high_frequency_infinite_timer`: **4**

## Top timer names / expressions
- `timer_simple`: 132
- `TimerExists`: 92
- `RemoveTimer`: 84
- `SetCustomTimer`: 63
- `setCancelAction`: 62
- `setAction`: 34
- `SetSimpleTimer`: 24
- `uniqueID`: 13
- `timerName`: 11
- `hacktimer`: 6
- `nutMusicFader`: 5
- `nutMovAct" .. self:UniqueID(`: 5
- `doStaredAction`: 5
- `shadowtime`: 4
- `seedUniqueID`: 4
- `EntityBiorezonanseTimer_" .. self:EntIndex(`: 4
- `cutMinigame`: 3
- `nutAreaController`: 3
- `timerId`: 2
- `ply:getChar():getID().."wanted`: 2
- `decreaseBtn`: 2
- `nutWaitUntilPlayerValid`: 2
- `uniqueID2`: 2
- `nutFailedToCreate`: 2
- `nutUnRagdoll" .. entity.nutPlayer:SteamID(`: 2
- `timerID`: 2
- `BlinkingScreamer`: 1
- `regen_energy`: 1
- `gens_break`: 1
- `spawn_containers`: 1

## Hot files by timer declarations
- `plugins\mining\entities\entities\nut_ore_smelter\init.lua`: 50
- `plugins\lightitems\entities\entities\nut_electric_generator\init.lua`: 40
- `plugins\needs\entities\entities\nut_cooking_base.lua`: 21
- `plugins\hacking\sh_plugin.lua`: 19
- `plugins\ragdollinteraction\interaction\sv_hooks.lua`: 19
- `entities\entities\sb_advanced_nextbot_terminator_hunter\shared.lua`: 16
- `plugins\lightitems\entities\entities\nut_diode_light\init.lua`: 14
- `plugins\tying\sh_plugin.lua`: 14
- `plugins\biorezonance\sh_plugin.lua`: 12
- `plugins\admintools\sh_plugin.lua`: 12
- `plugins\needs\entities\entities\nut_cooking_oven\init.lua`: 11
- `plugins\needs\entities\entities\nut_cooking_kettle\init.lua`: 10
- `entities\entities\sb_advanced_nextbot_terminator_hunter\motionoverrides.lua`: 9
- `schema\libs\sh_timer.lua`: 9
- `plugins\hacking\entities\entities\hack_secdb.lua`: 8
- `gamemode\core\hooks\cl_hooks.lua`: 8
- `plugins\snowy_components\sv_meta.lua`: 8
- `plugins\mnhr\sh_plugin.lua`: 8
- `plugins\lightitems\entities\entities\nut_electric_panel\init.lua`: 8
- `gamemode\core\hooks\sv_hooks.lua`: 7
- `gamemode\core\util\sv_action.lua`: 7
- `gamemode\core\util\sv_ragdoll.lua`: 7
- `gamemode\items\base\sh_weapons.lua`: 7
- `plugins\crafting\entities\entities\nut_craft_pressing\init.lua`: 7
- `plugins\npc\sv_plugin.lua`: 6
- `plugins\healthproblems\sv_hooks.lua`: 6
- `plugins\admintools\entities\entities\nut_eventpoint\init.lua`: 6
- `plugins\biorezonance\entities\entities\nut_oxygen_stantion\init.lua`: 6
- `plugins\vendor\entities\entities\nut_vendor\init.lua`: 6
- `plugins\needs\derma\cl_cookingboard_interface.lua`: 5

## High-risk timer candidates
- `timerName` at `entities\entities\sb_advanced_nextbot_terminator_hunter\motionoverrides.lua:2343` class=`high_frequency_infinite_timer` delay=`0` reps=`0` flags=['dynamic_timer_name', 'high_frequency_infinite_timer', 'next_tick_or_subframe_delay']
- `timerName` at `entities\entities\sb_advanced_nextbot_terminator_hunter\shared.lua:1275` class=`high_frequency_infinite_timer` delay=`0` reps=`0` flags=['dynamic_timer_name', 'high_frequency_infinite_timer', 'next_tick_or_subframe_delay']
- `regen_energy` at `plugins\biorezonance\sv_hooks.lua:5` class=`infinite_loop_timer` delay=`t_regen` reps=`0` flags=['infinite_timer']
- `hacktimer` at `plugins\hacking\sh_plugin.lua:939` class=`infinite_loop_timer` delay=`1` reps=`0` flags=['infinite_timer']
- `shadowtime` at `plugins\hacking\sh_plugin.lua:1271` class=`infinite_loop_timer` delay=`1` reps=`0` flags=['infinite_timer']
- `spawn_containers` at `plugins\lootablecontainers\sv_hooks.lua:184` class=`infinite_loop_timer` delay=`t_loot` reps=`0` flags=['infinite_timer']
- `spawn_oreveins` at `plugins\mining\sv_hooks.lua:6` class=`infinite_loop_timer` delay=`t_oreveins` reps=`0` flags=['infinite_timer']
- `signalis_food_decay_check` at `plugins\needs\sv_hooks.lua:9` class=`infinite_loop_timer` delay=`60` reps=`0` flags=['infinite_timer']
- `signalis_global_needs_timer` at `plugins\needs\sv_hooks.lua:53` class=`infinite_loop_timer` delay=`5` reps=`0` flags=['infinite_timer']
- `spawn_junk` at `plugins\npc\sv_plugin.lua:168` class=`infinite_loop_timer` delay=`t_loot` reps=`0` flags=['infinite_timer']
- `spawn_flesh` at `plugins\npc\sv_plugin.lua:174` class=`infinite_loop_timer` delay=`t_flesh` reps=`0` flags=['infinite_timer']
- `spawn_npc` at `plugins\npc\sv_plugin.lua:180` class=`infinite_loop_timer` delay=`t_npc` reps=`0` flags=['infinite_timer']
- `spawn_rezon` at `plugins\npc\sv_plugin.lua:186` class=`infinite_loop_timer` delay=`7200` reps=`0` flags=['infinite_timer']
- `spawn_cockroach` at `plugins\npc\sv_plugin.lua:192` class=`infinite_loop_timer` delay=`t_cockroach` reps=`0` flags=['infinite_timer']
- `uniqueID` at `plugins\attributes\plugins\strength\sh_plugin.lua:119` class=`infinite_loop_timer` delay=`0.25` reps=`0` flags=['dynamic_timer_name', 'infinite_timer']
- `cutMinigame` at `plugins\needs\derma\cl_cookingboard_interface.lua:97` class=`high_frequency_infinite_timer` delay=`0.045` reps=`0` flags=['high_frequency_infinite_timer', 'next_tick_or_subframe_delay']
- `CombineDisplayClear` at `schema\hooks\cl_hooks.lua:184` class=`infinite_loop_timer` delay=`10` reps=`0` flags=['infinite_timer']
- `VoiceClean` at `plugins\newvoice.lua:106` class=`infinite_loop_timer` delay=`10` reps=`0` flags=['infinite_timer']
- `nutVignetteChecker` at `plugins\vignette.lua:17` class=`infinite_loop_timer` delay=`1` reps=`0` flags=['infinite_timer']
- `nutSaveData` at `gamemode\core\sv_data.lua:94` class=`infinite_loop_timer` delay=`600` reps=`0` flags=['infinite_timer']
- `nutWaitUntilPlayerValid` at `gamemode\core\hooks\cl_hooks.lua:349` class=`infinite_loop_timer` delay=`0.5` reps=`0` flags=['infinite_timer']
- `timerName` at `gamemode\core\libs\sh_log.lua:76` class=`infinite_loop_timer` delay=`30` reps=`0` flags=['dynamic_timer_name', 'infinite_timer']
- `nutResolutionMonitor` at `gamemode\core\util\cl_draw.lua:57` class=`infinite_loop_timer` delay=`1` reps=`0` flags=['infinite_timer']
- `uniqueID2` at `gamemode\core\util\sv_door.lua:122` class=`infinite_loop_timer` delay=`1` reps=`0` flags=['infinite_timer']
- `uniqueID` at `gamemode\core\util\sv_ragdoll.lua:280` class=`infinite_loop_timer` delay=`0.33` reps=`0` flags=['dynamic_timer_name', 'infinite_timer']
- `nutAreaController` at `plugins\area\sh_plugin.lua:58` class=`infinite_loop_timer` delay=`0.33` reps=`0` flags=['infinite_timer']
- `nutLifeGuard` at `plugins\playerinjuries\sv_drowning.lua:1` class=`infinite_loop_timer` delay=`1` reps=`0` flags=['infinite_timer']
- `nutMusicFader` at `plugins\multichar\plugins\charselect\derma\cl_bg_music.lua:46` class=`high_frequency_infinite_timer` delay=`0.1` reps=`0` flags=['high_frequency_infinite_timer']
- `timer_simple` at `entities\weapons\arc9_srp_base.lua:65` class=`next_tick_delay` delay=`0` reps=`None` flags=['next_tick_or_subframe_delay']
- `timer_simple` at `entities\entities\sb_advanced_nextbot_terminator_hunter\enemyoverrides.lua:295` class=`next_tick_delay` delay=`0` reps=`None` flags=['next_tick_or_subframe_delay']
- `timer_simple` at `entities\entities\sb_advanced_nextbot_terminator_hunter\enemyoverrides.lua:307` class=`next_tick_delay` delay=`0` reps=`None` flags=['next_tick_or_subframe_delay']
- `timer_simple` at `entities\entities\sb_advanced_nextbot_terminator_hunter\motionoverrides.lua:2258` class=`next_tick_delay` delay=`0` reps=`None` flags=['next_tick_or_subframe_delay']
- `timer_simple` at `entities\entities\sb_advanced_nextbot_terminator_hunter\prettydamage.lua:322` class=`next_tick_delay` delay=`0` reps=`None` flags=['next_tick_or_subframe_delay']
- `timer_simple` at `entities\entities\sb_advanced_nextbot_terminator_hunter\prettydamage.lua:330` class=`next_tick_delay` delay=`0` reps=`None` flags=['next_tick_or_subframe_delay']
- `timer_simple` at `entities\entities\sb_advanced_nextbot_terminator_hunter\shared.lua:4052` class=`next_tick_delay` delay=`0` reps=`None` flags=['next_tick_or_subframe_delay']
- `timer_simple` at `entities\entities\sb_advanced_nextbot_terminator_hunter\weapons.lua:289` class=`next_tick_delay` delay=`0` reps=`None` flags=['next_tick_or_subframe_delay']
- `timer_simple` at `entities\entities\sb_advanced_nextbot_terminator_hunter\weapons.lua:301` class=`next_tick_delay` delay=`0` reps=`None` flags=['next_tick_or_subframe_delay']
- `timer_simple` at `plugins\needs\items\base\sh_food.lua:255` class=`next_tick_delay` delay=`0` reps=`None` flags=['next_tick_or_subframe_delay']
- `timer_simple` at `plugins\newweapons\entities\weapons\tfa_nade_base.lua:122` class=`next_tick_delay` delay=`0` reps=`None` flags=['next_tick_or_subframe_delay']
- `timer_simple` at `plugins\traits\derma\cl_traitcreation.lua:34` class=`next_tick_delay` delay=`0` reps=`None` flags=['next_tick_or_subframe_delay']

## Dynamic timer name examples
- `timerName` at `entities\entities\sb_advanced_nextbot_terminator_hunter\motionoverrides.lua:751` type=`timer_create` class=`one_shot_delay` subsystem=`ai_entity`
- `timerName` at `entities\entities\sb_advanced_nextbot_terminator_hunter\motionoverrides.lua:2343` type=`timer_create` class=`high_frequency_infinite_timer` subsystem=`ai_entity`
- `timerName` at `entities\entities\sb_advanced_nextbot_terminator_hunter\shared.lua:1275` type=`timer_create` class=`high_frequency_infinite_timer` subsystem=`ai_entity`
- `uniqueID` at `plugins\attributes\plugins\strength\sh_plugin.lua:119` type=`timer_create` class=`infinite_loop_timer` subsystem=`misc`
- `ply:getChar():getID().."wanted` at `plugins\hacking\entities\entities\hack_secdb.lua:73` type=`timer_create` class=`one_shot_delay` subsystem=`character`
- `ply:getChar():getID().."wanted` at `plugins\hacking\entities\entities\hack_secdb.lua:155` type=`timer_create` class=`one_shot_delay` subsystem=`character`
- `self:EntIndex() .. "[" .. identifier .. "]` at `schema\libs\sh_timer.lua:15` type=`timer_create` class=`repeating_scheduler` subsystem=`misc`
- `uniqueID` at `gamemode\core\hooks\sv_hooks.lua:231` type=`timer_create` class=`repeating_scheduler` subsystem=`entity_production`
- `timerName` at `gamemode\core\libs\sh_log.lua:76` type=`timer_create` class=`infinite_loop_timer` subsystem=`entity_production`
- `uniqueID` at `gamemode\core\util\sv_action.lua:52` type=`timer_create` class=`repeating_scheduler` subsystem=`entity_production`
- `uniqueID` at `gamemode\core\util\sv_door.lua:130` type=`timer_create` class=`one_shot_delay` subsystem=`entity_production`
- `uniqueID` at `gamemode\core\util\sv_door.lua:135` type=`timer_create` class=`finite_repeating_scheduler` subsystem=`entity_production`
- `uniqueID` at `gamemode\core\util\sv_ragdoll.lua:280` type=`timer_create` class=`infinite_loop_timer` subsystem=`entity_production`
- `nutUnRagdoll" .. corpse.nutPlayer:SteamID(` at `entities\entities\sb_advanced_nextbot_empire_base.lua:505` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`player_action`
- `QTETimer_"..ply:SteamID(` at `entities\entities\nut_flesh\init.lua:69` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`misc`
- `timerName` at `entities\entities\sb_advanced_nextbot_terminator_hunter\motionoverrides.lua:750` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`ai_entity`
- `timerName` at `entities\entities\sb_advanced_nextbot_terminator_hunter\motionoverrides.lua:752` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`ai_entity`
- `timerName` at `entities\entities\sb_advanced_nextbot_terminator_hunter\motionoverrides.lua:2322` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`ai_entity`
- `timerName` at `entities\entities\sb_advanced_nextbot_terminator_hunter\motionoverrides.lua:2336` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`ai_entity`
- `timerName` at `entities\entities\sb_advanced_nextbot_terminator_hunter\shared.lua:1276` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`ai_entity`
- `relockdoor"..v:MapCreationID(` at `plugins\hacking\sh_plugin.lua:574` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`misc`
- `nutMovAct" .. self:UniqueID(` at `plugins\snowy_components\sv_meta.lua:37` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`misc`
- `nutMovAct" .. self:UniqueID(` at `plugins\snowy_components\sv_meta.lua:49` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`misc`
- `nutMovAct" .. self:UniqueID(` at `plugins\snowy_components\sv_meta.lua:57` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`misc`
- `nutMovAct" .. self:UniqueID(` at `plugins\snowy_components\sv_meta.lua:67` type=`timer_exists` class=`unknown_timer` subsystem=`misc`
- `nutMovAct" .. self:UniqueID(` at `plugins\snowy_components\sv_meta.lua:55` type=`timer_reps_left` class=`unknown_timer` subsystem=`misc`
- `glassblur"..id` at `plugins\traits\sh_config.lua:817` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`misc`
- `alcoh"..id` at `plugins\traits\sh_config.lua:897` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`misc`
- `uniqueID` at `plugins\attributes\plugins\strength\sh_plugin.lua:121` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`misc`
- `EntityBiorezonanseTimer_" .. self:EntIndex(` at `plugins\biorezonance\entities\entities\nut_bioresonanse_ihnolite\init.lua:40` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`entity_production`
- `EntityBiorezonanseTimer_" .. self:EntIndex(` at `plugins\biorezonance\entities\entities\nut_bioresonanse_ihnolite\init.lua:38` type=`timer_exists` class=`unknown_timer` subsystem=`entity_production`
- `EntityBiorezonanseTimer_" .. self:EntIndex(` at `plugins\mining\entities\entities\nut_ihnolit_orevein.lua:33` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`entity_production`
- `EntityBiorezonanseTimer_" .. self:EntIndex(` at `plugins\mining\entities\entities\nut_ihnolit_orevein.lua:31` type=`timer_exists` class=`unknown_timer` subsystem=`entity_production`
- `nutUnRagdoll" .. entity.nutPlayer:SteamID(` at `plugins\ragdollinteraction\interaction\sv_hooks.lua:473` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`player_action`
- `nutUnRagdoll" .. entity.nutPlayer:SteamID(` at `plugins\ragdollinteraction\interaction\sv_hooks.lua:516` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`player_action`
- `self:EntIndex(` at `schema\libs\sh_timer.lua:23` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`misc`
- `nutToggleRaise"..client:SteamID(` at `gamemode\core\hooks\sv_hooks.lua:108` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`entity_production`
- `uniqueID` at `gamemode\core\hooks\sv_hooks.lua:235` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`entity_production`
- `timerID` at `gamemode\core\hooks\sv_hooks.lua:878` type=`timer_remove` class=`timer_lifecycle_operation` subsystem=`entity_production`
- `timerID` at `gamemode\core\hooks\sv_hooks.lua:873` type=`timer_exists` class=`unknown_timer` subsystem=`entity_production`
