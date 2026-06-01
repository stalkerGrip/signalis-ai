# SIGNALIS AI — Script Contracts

Generated from:

```text
python -m <module> --help
```

Purpose:

- prevent guessed CLI usage
- preserve script interfaces across chats
- document inputs/outputs for orchestration
- expose older script usability issues

Rule:

Before wrapping or chaining a script, check this file or run the script with `--help`.

- Scripts checked: `88`

## scripts/diagnostics

### `scripts.diagnostics.test_embeddings`

- Path: `scripts/diagnostics/test_embeddings.py`
- Help status: `NO_HELP_OR_ERROR`

```text
TIMEOUT while running --help
```

## scripts/extraction

### `scripts.extraction.extract_character_inventory`

- Path: `scripts/extraction/extract_character_inventory.py`
- Help status: `OK`

```text
Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis
Lua files found: 969

Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript
Lua files found: 218
Saved 1982 entries -> manifests\character_inventory\character_calls.json
Saved 547 entries -> manifests\character_inventory\inventory_calls.json
Saved 102 entries -> manifests\character_inventory\character_inventory_chains.json
Saved 12 entries -> manifests\character_inventory\inventory_item_queries.json
```

### `scripts.extraction.extract_commands`

- Path: `scripts/extraction/extract_commands.py`
- Help status: `OK`

```text
Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis
Lua files found: 969

Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript
Lua files found: 218
Saved 149 entries -> manifests\commands\commands.json
Saved 149 entries -> manifests\commands\command_callbacks.json
Saved 149 entries -> manifests\commands\command_effects.json
Saved 773 entries -> manifests\commands\command_calls.json
```

### `scripts.extraction.extract_derma`

- Path: `scripts/extraction/extract_derma.py`
- Help status: `OK`

```text
Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis
Lua files found: 969

Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript
Lua files found: 218
Saved 124 entries -> manifests\derma\vgui_creates.json
Saved 488 entries -> manifests\derma\panel_methods.json
Saved 94 entries -> manifests\derma\panel_registers.json
Saved 5 entries -> manifests\derma\derma_menus.json
Saved 201 entries -> manifests\derma\button_callbacks.json
Saved 57 entries -> manifests\derma\ui_hot_callbacks.json
Saved 264 entries -> manifests\derma\netstream_ui_hooks.json
```

### `scripts.extraction.extract_entities`

- Path: `scripts/extraction/extract_entities.py`
- Help status: `OK`

```text
Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis
Lua files found: 969

Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript
Lua files found: 218
Saved 220 entries -> manifests\entities\entity_classes.json
Saved 1030 entries -> manifests\entities\entity_properties.json
Saved 212 entries -> manifests\entities\entity_lifecycle_methods.json
Saved 740 entries -> manifests\entities\entity_gameplay_methods.json
Saved 869 entries -> manifests\entities\entity_engine_calls.json
Saved 49 entries -> manifests\entities\entity_network_calls.json
Saved 82 entries -> manifests\entities\entity_timer_calls.json
Saved 4025 entries -> manifests\entities\entity_gameplay_calls.json
```

### `scripts.extraction.extract_globals`

- Path: `scripts/extraction/extract_globals.py`
- Help status: `OK`

```text
Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis
Lua files found: 969

Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript
Lua files found: 218
Saved 250 entries -> manifests\globals\nut_method_calls.json
Saved 728 entries -> manifests\globals\nut_function_calls.json
Saved 74 entries -> manifests\globals\nut_writes.json
Saved 2051 entries -> manifests\globals\nut_important_refs.json
```

### `scripts.extraction.extract_hooks`

- Path: `scripts/extraction/extract_hooks.py`
- Help status: `OK`

```text
=== SOURCE ROOTS ===
{'workspace_name': 'signalis_ai', 'source_roots': ['E:\\steam\\steamapps\\common\\GarrysMod\\garrysmod\\gamemodes\\signalis', 'E:\\steam\\steamapps\\common\\GarrysMod\\garrysmod\\gamemodes\\nutscript'], 'exclude': ['sandbox', 'terrortown', 'warhammer', '.git', 'node_modules'], 'priority': ['signalis', 'nutscript']}

Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis
Lua files found: 969
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\effects\nut_flesh.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_flesh_bee.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_simple_enemy.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_vendingm.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_corrupt_base.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_corrupt_base.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_empire_base.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_empire_base.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_soldier_base.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_soldier_base.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_soldier_follower.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_empire_hostile.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_klbr_hostile.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_mnhr_boss_hostile.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_replica_crazy.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_replica_friendly.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_replica_hostile.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_bucket\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_bucket\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_bucket\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_cockroach\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_cockroach\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_cockroach\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_flesh\cl_init.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_flesh\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_flesh\init.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_flesh\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_flesh\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_manhole_teleport\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_manhole_teleport\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_manhole_teleport\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_utilizator\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_utilizator\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\nut_utilizator\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\behaviour.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\cl_playercontrol.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\cl_playercontrol.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\drive.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\drive.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\enemy.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\healing.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\looting.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\motion.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\motion.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\nodegraph_path.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\nodegraph_path.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\playercontrol.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\playercontrol.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\tasks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\weapons.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_base\weapons.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\behaviouroverrides.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\compatibilityhacks.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\compatibilityhacks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\enemyoverrides.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\enemyoverrides.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\motionoverrides.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\motionoverrides.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\overcharging.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\pathoverrides.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\prettydamage.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\prettydamage.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\shared.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\spokenlines.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\spokenlines.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\taskoverride.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\weapholstering.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\weaponhacks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\weapons.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\entities\sb_advanced_nextbot_terminator_hunter\weapons.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\arc9_bu5.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\arc9_ein12.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\arc9_eu_k480.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\arc9_eu_k508.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\arc9_srp_base.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\arc9_type11.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\arc9_type1ps.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\arc9_type3.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\arc9_type53.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\arc9_type75.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\arc9_type84.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\arc9_type89.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\arc9_type89h.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\arc9_type89mp.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\nut_stunstick.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\entities\weapons\nut_suitcase.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\gamemode\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\gamemode\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\adminspawnmenu.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\diffchat.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\playerconnected.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\restrictQmenu.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\shootlock.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\sh_ambients.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\worlditemspawner.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\admintools\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\admintools\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\admintools\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\admintools\derma\cl_eventpoint_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\admintools\derma\cl_itempanel.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\admintools\derma\cl_menu.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\admintools\entities\entities\nut_eventpoint\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\admintools\entities\entities\nut_eventpoint\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\admintools\entities\entities\nut_eventpoint\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\admintools\items\sh_fixed_customitem.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\admintools\items\base\sh_customitem.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\armor_repair_kit\sh_mrebel_armor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\armor_repair_kit\sh_rebel_armor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\armor_repair_kit\sh_rkita_big.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\armor_repair_kit\sh_rkita_small.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\armor_repair_kit\sh_rkita_small_simple.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\base\sh_armor_repair_kit.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\base\sh_outfit.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_hat_pilotka.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_helmet_arar_mask.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_helmet_tier1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_helmet_tier2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_helmet_tier3.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_mask_geirmask.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_mask_habrmask.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_mask_lstrmask.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_mask_starmask.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_arar_armor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_eulr_armor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_fklr_armor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_geir_armor_med.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_geir_armor_sheavy.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_geshtalt_armor_heavy.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_geshtalt_armor_med.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_geshtalt_medium_armor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_habr_armor_heavy.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_habr_armor_med.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_kahr_armor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_klbr_armor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_kncr_armor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_lstr_armor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_lstr_armor_heavy.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_lstr_armor_med.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_medic.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_star_armor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_star_armor_heavy.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_star_armor_med.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\armor\items\outfit\sh_outfit_stcr_armor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\attributes\sh_commands.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\attributes\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\attributes\derma\cl_attribute.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\attributes\derma\cl_attributes_step.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\attributes\libs\sh_attribs.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\attributes\libs\sh_attribs.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\attributes\plugins\strength\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\attributes\plugins\strength\attributes\sh_body.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\attributes\plugins\strength\attributes\sh_end.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\attributes\plugins\strength\attributes\sh_stm.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\attributes\plugins\strength\attributes\sh_str.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\cl_hooks.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\sh_plugin.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\sv_hooks.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\derma\cl_oxystantion_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_bioresonanse_fleshradioactive\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_bioresonanse_fleshradioactive\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_bioresonanse_fleshradioactive\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_bioresonanse_gas\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_bioresonanse_gas\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_bioresonanse_gas\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_bioresonanse_ihnolite\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_bioresonanse_ihnolite\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_bioresonanse_ihnolite\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_bioresonanse_teleport\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_bioresonanse_teleport\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_bioresonanse_teleport\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_oxygen_stantion\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_oxygen_stantion\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\entities\nut_oxygen_stantion\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\entities\weapons\nut_biorezonance_swep.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\items\sh_high_gasmask_filters.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\items\sh_medium_gasmask_filters.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\items\sh_oxy_tank.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\items\sh_poor_gasmask_filters.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\items\sh_thermite.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\items\outfit\sh_mask_gasmask.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\items\outfit\sh_outfit_flesh_armor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\biorezonance\items\outfit\sh_outfit_l1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\base\sh_books.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\base\sh_bucklets.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\books\sh_antiterror.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\books\sh_battle_medicine.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\books\sh_book_engineering_knowledge_manual.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\books\sh_civil_codex.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\books\sh_civil_instructions.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\books\sh_dnevnik_eulr.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\books\sh_heath_problems_handbook.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\books\sh_hot_revolutions.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\books\sh_main_medicine.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\books\sh_replicas.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\books\sh_yellow_king.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\bucklets\sh_allreplics.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\bucklets\sh_allreplics_secret.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\bucklets\sh_buck_adlersdiary.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\bucklets\sh_buck_arar_doors.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\bucklets\sh_buck_arar_electrics.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\bucklets\sh_buck_arar_gens.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\bucklets\sh_buck_eres.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\bucklets\sh_buck_nation_computer.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\bucklets\sh_buck_nation_lock.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\books\items\bucklets\sh_cutie_storch.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\entities\entities\nut_cassetteplayer.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\base\sh_cassette.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_bru_achtung.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_bru_dust.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_elly1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_elly2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_empire_ellen3.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_eusan_arbeit.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_eusan_erheben.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_eusan_hugel.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_eusan_jungs.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_eusan_panzer.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_eusan_partisan.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_eusan_pioner.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_eusan_serenadegut.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_eusan_soldat.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_eusan_spring.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_eusan_stand.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_eusan_wenndiesonja.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_example.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_gruppa.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_hangedman.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_lake.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_nezhnost.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_rashpil.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_rashpil_2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_serenade.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_sos_dira.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_sos_menya.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_sos_petlya.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_sos_pos.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_sos_voyna.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_svetit.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\cassetteplayer\items\cassette\sh_world.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\sh_config.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\sh_massitems.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_ammo_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_armor_disassemble_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_armor_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_armor_repair_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_engineering_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_explosives_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_food_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_gen_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_medicine_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_other_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_storage_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_tech_disassemble_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_tech_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_weapons_disassemble_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_weapons_parts_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_weapons_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\craftrecipes\sh_workbench_recipes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\derma\cl_crafting.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\derma\cl_pressing_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\derma\cl_workbench_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_craft_ammunition.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_craft_furnance.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_craft_medic.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_craft_medic2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_craft_tech.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_plita.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\sky_craft_armor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\sky_craft_basic.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\sky_craft_weapons.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_crafting_base\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_crafting_base\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_crafting_base\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_craft_pressing\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_craft_pressing\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_craft_pressing\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_storage_kit\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_storage_kit\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_storage_kit\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_workbench_kit\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_workbench_kit\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\entities\entities\nut_workbench_kit\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\ammo_comsumables\sh_ammo_ar_casings.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\ammo_comsumables\sh_ammo_ar_powder.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\ammo_comsumables\sh_ammo_pistol_casings.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\ammo_comsumables\sh_ammo_pistol_powder.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\ammo_comsumables\sh_ammo_primers_pack.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\ammo_comsumables\sh_ammo_revolver_casings.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\ammo_comsumables\sh_ammo_r_casings.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\ammo_comsumables\sh_ammo_r_powder.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\ammo_comsumables\sh_ammo_shootgun_casings.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\base\sh_ammo_comsumables.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\base\sh_component.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\base\sh_engineering_consumables.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\base\sh_explosives_consumables.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\base\sh_generator_comsumables.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\base\sh_junk.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\base\sh_medical_consumables.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\base\sh_storage_consumables.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\base\sh_weapon_consumables.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\base\sh_workbench_consumables.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\component\sh_comp_aluminum.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\component\sh_comp_eng_thermite.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\component\sh_comp_pad_cloth.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\component\sh_comp_plastic.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\component\sh_comp_plexiglass.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\component\sh_comp_rubber.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\component\sh_comp_scrap_cloth.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\component\sh_comp_scrap_metal.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\component\sh_comp_tech1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\component\sh_comp_titan.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\component\sh_comp_wire1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\engineering_consumables\sh_comp_duct_tape.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\engineering_consumables\sh_eng_coal.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\engineering_consumables\sh_eng_gasmask_filter_hull.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\engineering_consumables\sh_eng_high_mech_part.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\engineering_consumables\sh_eng_medium_mech_part.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\engineering_consumables\sh_eng_metal_work_kit.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\engineering_consumables\sh_eng_nails_pack.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\engineering_consumables\sh_eng_screws_pack.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\engineering_consumables\sh_eng_simple_mech_part.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\engineering_consumables\sh_eng_springs_pack.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\engineering_consumables\sh_eng_textolite_2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\engineering_consumables\sh_eng_textolite_3.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\engineering_consumables\sh_eng_washers_pack.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\explosives_consumables\sh_expl_anthracene.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\explosives_consumables\sh_expl_fuse.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\explosives_consumables\sh_expl_tnt.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\explosives_consumables\sh_expl_type24_casing.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\explosives_consumables\sh_expl_type24_handle.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_car_battery.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_comp_mech1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_comp_mech2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_datachik1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_datachik2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_datachik3.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_doll.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_doll_cat.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_doll_croc.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_doll_croc2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_gas_can.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_junk_aluminumcan.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_junk_bag_for_junk.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_junk_bag_of_junk.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_junk_bodybag.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_junk_empty_waterbottle.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_junk_sigarette_butt.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_metalcanl.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_newspaper.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_scrap_wood.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\junk\sh_shoe.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_absorbent_catal.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_activated_carbon.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_coagulant.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_complete_army_stim.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_complete_autoinjector.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_complete_med_foam.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_complete_med_foam_plus.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_complete_stim.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_foam_agent.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_foam_agent_reagent.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_medical_reagents.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_regen_comp_gsc.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_stim_autoinjector.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_stim_boost_gsc.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_stim_injector.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_stim_rep.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\medical_consumables\sh_med_titan_pins.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\storage_consumables\sh_strg_ammo_can.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\storage_consumables\sh_strg_fridge.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\storage_consumables\sh_strg_fridge_big.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\storage_consumables\sh_strg_green_closet.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\storage_consumables\sh_strg_green_filecabinet.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\storage_consumables\sh_strg_green_filecabinet_group.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\storage_consumables\sh_strg_wood_crate.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_ar_gas_block.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_ar_rifled_barrel.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_ar_trigger_group.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_parts.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_pistol_gas_block.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_pistol_rifled_barrel.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_pistol_tool_kit.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_pistol_trigger_group.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_revolving_drum.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_r_gas_block.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_r_rifled_barrel.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_r_trigger_group.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_shootgun_barrel.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_shootgun_pump.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_shootgun_trigger_group.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_smg_gas_block.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_smg_rifled_barrel.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_smg_trigger_group.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\weapon_consumables\sh_wpn_type3_rifled_barrel.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\workbench_consumables\sh_wb_basic.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\crafting\items\workbench_consumables\sh_wb_medic.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\derma\cl_farmingpot_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\entities\entities\farming_pot\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\entities\entities\farming_pot\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\entities\entities\farming_pot\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\sh_flower1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\sh_water.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\base\sh_pot.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\base\sh_seeds.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\base\sh_soil.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\pot\sh_basic_pot.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\seeds\sh_paporotnik.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\seeds\sh_sprout_apple.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\seeds\sh_sprout_banana.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\seeds\sh_sprout_cabbage.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\seeds\sh_sprout_carrot.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\seeds\sh_sprout_cucumber.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\seeds\sh_sprout_garlic.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\seeds\sh_sprout_melon.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\seeds\sh_sprout_onion.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\seeds\sh_sprout_orange.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\seeds\sh_sprout_potato.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\seeds\sh_sprout_tomato.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\farming\items\soil\sh_dirt.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\derma\cl_computer_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\derma\cl_door_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\derma\cl_nationlock_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\entities\entities\nut_cmblock.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\entities\entities\nut_culock.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\entities\entities\nut_cardupdater\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\entities\entities\nut_cardupdater\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\entities\entities\nut_cardupdater\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\entities\entities\nut_computer\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\entities\entities\nut_computer\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\entities\entities\nut_computer\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\entities\entities\nut_nationlock\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\entities\entities\nut_nationlock\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\entities\entities\nut_nationlock\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\items\sh_cid.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\items\sh_civil_card.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\items\sh_civil_lock.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\items\sh_nation_cid.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\items\sh_nation_lock.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\items\sh_protect_card.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\items\sh_protect_lock.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\gadgets\items\sh_storage_lock.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\entities\entities\customhackbase.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\entities\entities\hack_secdb.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\entities\entities\hack_server.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\entities\entities\hack_server_corp.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\entities\entities\hack_storystorageserver.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\entities\entities\hack_test.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\entities\entities\hack_tut.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\items\sh_hack_remote.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\items\base\sh_hackprogram.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\items\base\sh_hacktool.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\items\hackprogram\sh_hackprog_rangeext.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\items\hackprogram\sh_hackprog_suspend.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\items\hacktool\sh_hktl_adv.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\items\hacktool\sh_hktl_basic.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hacking\items\hacktool\sh_hktl_int.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\cl_hooks.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\sh_lang.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\sh_meta.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\sv_hooks.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\derma\cl_status_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\acidburn.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\activatedcarbon.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\alcoholaddiction.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\alcoholkd.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\alcoholoverdose.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\aminocaproicacid.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\amputation.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\anemia.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\antibiotics.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\autoinjectorkd.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\bleeding.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\blindness.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\bonefracture.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\cigaretteaddiction.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\cigarettekd.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\cough.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\diclofenak.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\dpainkilladdiction.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\dpainkillkd.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\dpainkillkddetox.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\dpainkilloverdose.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\foodpoisoning.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\galoperedol.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\glucosesolution.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\healedacidburn.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\healedbonefracture.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\healedheatburn.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\healedwound.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\heartstop.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\heatburn.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\infection.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\madness.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\pain.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\painkill.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\painkillkd.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\restoreblood.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\staminaregen.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\starvation.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\stoppingbleeding.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\treatedamputation.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\treatedbonefracture.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\treatedwound.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\unconscious.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\diseases\wound.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\sh_med_healthcheck.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\base\sh_peals.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_adminpills.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_bandage.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_bloodbag.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_defib.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_eyespills.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_galoperidol.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_health_kit.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_health_vial.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_alkali.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_ammonia.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_anesthetize_syringe.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_antibiotics.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_army_stimulator.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_autoinjector.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_bloodbag_250ml.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_complete_activated_carbon.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_epinifrin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_gestalt_first_aid_kit.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_glucose_solution.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_nalacson.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_painkillers.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_pantenol.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_pantenol_bandage.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_patch.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_promedol.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_replica_bloodbag_250ml.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_replica_bloodbag_500ml.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_simple_bandage.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_splint.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_stimulator.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_med_surgical_kit.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\items\peals\sh_paracetamol.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\healthproblems\languages\sh_russian.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hud\sh_plugin.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\hud\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\inventory\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\inventory\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\inventory\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\inventory\derma\cl_extended_grid_inventory.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\inventory\derma\cl_vendor_grid_inventory.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\inventory\items\sh_ration_mark.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\cl_hooks.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\sh_breakinfos.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\sh_breaknames.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\sh_breaks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\sh_checktimes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\sh_plugin.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\sv_hooks.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\derma\cl_electricpanel_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\derma\cl_gen_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\derma\cl_lamp_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\entities\entities\nut_chemlight_glow\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\entities\entities\nut_chemlight_glow\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\entities\entities\nut_chemlight_glow\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\entities\entities\nut_diode_light\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\entities\entities\nut_diode_light\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\entities\entities\nut_diode_light\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\entities\entities\nut_electric_generator\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\entities\entities\nut_electric_generator\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\entities\entities\nut_electric_generator\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\entities\entities\nut_electric_panel\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\entities\entities\nut_electric_panel\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\entities\entities\nut_electric_panel\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\base\sh_electrical_appliances.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\base\sh_glowstick.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\electrical_appliances\sh_diode_light.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\electrical_appliances\sh_electric_panel.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\engineering_consumables\sh_eng_diode_lamp.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\engineering_consumables\sh_eng_relay.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\engineering_consumables\sh_eng_wiring.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_areometer.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_bearing.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_cardan_joint.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_center_gear_set.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_cleaning_kit.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_coolant_canister.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_cooling_fan.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_drive_belt.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_drive_roller.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_el_spare_parts.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_fan_unit.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_fitting.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_ignition_coil_set.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_machine_oil_canister.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_multimeter.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_pto_cross_member.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_ring_gear.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_safe_disconnection_device.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_satellite_gear_set.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_sealing_rings.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_settings_device.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_spare_parts.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_spark_plug.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\generator_comsumables\sh_gen_terminal_set.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\glowstick\sh_glowstick_blue.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\glowstick\sh_glowstick_green.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lightitems\items\glowstick\sh_glowstick_red.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_ammoloot_container.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_buildloot_container.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_engloot_container.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_foodloot_container.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_medammoloot_container.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_medbuildloot_container.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_medconloot_container.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_medengloot_container.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_medmedconloot_container.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_pooralcoloot_container.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_uncomammoloot_container.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_uncomweploot_container.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_weploot_container.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_loot_container_base\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_loot_container_base\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_loot_container_base\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_loot_junk\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_loot_junk\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\lootablecontainers\entities\entities\nut_loot_junk\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\loyal_system\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\loyal_system\entities\entities\nut_loyal_terminal\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\loyal_system\entities\entities\nut_loyal_terminal\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\loyal_system\entities\entities\nut_loyal_terminal\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\derma\cl_oresmelter_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\entities\entities\nut_aluminium_orevein.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\entities\entities\nut_ferum_orevein.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\entities\entities\nut_ihnolit_orevein.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\entities\entities\nut_titan_orevein.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\entities\entities\nut_melting_pot\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\entities\entities\nut_melting_pot\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\entities\entities\nut_melting_pot\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\entities\entities\nut_orevein_base\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\entities\entities\nut_orevein_base\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\entities\entities\nut_orevein_base\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\entities\entities\nut_ore_smelter\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\entities\entities\nut_ore_smelter\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\entities\entities\nut_ore_smelter\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\items\base\sh_ore.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\items\ore\sh_aluminium_ore.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\items\ore\sh_ferum_ore.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\items\ore\sh_ihnolit_ore.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mining\items\ore\sh_titan_ore.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mnhr\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mnhr\derma\cl_mnhrstation_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mnhr\entities\entities\nut_mnhr_powerarmor\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mnhr\entities\entities\nut_mnhr_powerarmor\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mnhr\entities\entities\nut_mnhr_powerarmor\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mnhr\entities\entities\nut_mnhr_service\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mnhr\entities\entities\nut_mnhr_service\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\mnhr\entities\entities\nut_mnhr_service\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\sh_panrecepies.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\sh_platerecepies.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\sh_potrecepies.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\sh_pottearecepies.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\sv_hooks.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\derma\cl_cookingboard_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\derma\cl_cookingoven_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\derma\cl_cooking_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\derma\cl_kettle_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\derma\cl_waterfaucet_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_base.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_board\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_board\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_board\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_kettle\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_kettle\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_kettle\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_oven\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_oven\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_oven\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_pan\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_pan\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_pan\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_plate\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_plate\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_plate\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_pot\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_pot\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_pot\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_pottea\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_pottea\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_cooking_pottea\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_waterfaucet\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_waterfaucet\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\entities\entities\nut_waterfaucet\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\sh_chlorine_tablets.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\sh_knife_kitchen.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\sh_metalcan.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\sh_water_filter.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\base\sh_container.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\base\sh_dish_entitied.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\base\sh_food.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\container\sh_bowl.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\container\sh_glass_drink.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\dish_entitied\sh_cooking_pan.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\dish_entitied\sh_cooking_plate.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\dish_entitied\sh_cooking_pot.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\dish_entitied\sh_cooking_pottea.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_apple_compote.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_beer.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_bh_sodacan.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_coffee.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_energy.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_juice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_milkcarton.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_multifruit_compote.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_vinetta.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_waterbottle.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_watercan.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_whiskey.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_whiskey_glass.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_wine_red.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_wine_red_glass.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_wine_white.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drink_wine_white_glass.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_drugs_cigarette.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_dry_coffee.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_dry_flour.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_dry_takeout.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_dry_tea.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_bagchips.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_barchoc.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_bruh.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_cake.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_cake_slice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_canpasta.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_canpilaf.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_canpotato.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_cansoup.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_cockroach.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_crackers.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_apple_red.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_apple_red_slice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_banana.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_banana_slice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_cabbage.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_cabbage_slice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_carrot.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_carrot_slice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_cucumber.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_cucumber_slice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_garlic.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_garlic_slice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_melon.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_melon_slice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_onion.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_onion_slice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_orange.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_orange_slice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_potato.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_potato_slice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_tomato.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_harvest_tomato_slice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_meat.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_mre.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_mre_evsan.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_pizza.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_pizza_slice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_plod.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_rice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_simple_pie.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_supplement.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_takeout.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_food_vegsoup.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_med_antiseptic.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_prepack_cake.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_prepack_dumplings.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_prepack_pancakes_dough.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_prepack_pie.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_prepack_pizza.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_prepack_potato_pancakes_dough.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\needs\items\food\sh_vegtableoil.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newvendorsystem\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newvendorsystem\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newvendorsystem\derma\cl_vendor_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\entities\effects\nut_smokenade.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\entities\entities\nut_type39\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\entities\weapons\nut_mop.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\entities\weapons\nut_pickaxe.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\entities\weapons\tfa_locher.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\entities\weapons\tfa_nade_base.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\entities\weapons\tfa_type39.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\entities\weapons\tfa_type57.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\base\sh_arc9_attachments.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_357.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_ar2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_crowbar.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_mop.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_photo.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_pickaxe.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_pistol.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_rpg.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_shotgun.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_smg.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_k480.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_locher.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_stunstick.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type2000.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type3.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type36m.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type39.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type39pbz.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type3mg.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type41.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type44.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type53.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type57.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type63.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type89.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type89l.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type89mp.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\newweapons\items\weapons\sh_wpn_type98k.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\npc\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\npc\sv_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\playeranimator\sh_plugin.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\playeranimator\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\radio\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\radio\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\radio\derma\cl_radiostation_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\radio\entities\entities\nut_radio_station\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\radio\entities\entities\nut_radio_station\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\radio\entities\entities\nut_radio_station\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\radio\items\sh_mcradio.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\radio\items\sh_radio.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\radio\items\sh_sradio.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\ragdollinteraction\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\ragdollinteraction\corpses\sh_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\ragdollinteraction\corpses\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\ragdollinteraction\derma\cl_corpse_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\ragdollinteraction\interaction\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\ragdollinteraction\interaction\sv_access_rules.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\ragdollinteraction\interaction\sv_hooks.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\ragdollinteraction\interaction\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\ragdollinteraction\interaction\sv_networking.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\ragdollinteraction\languages\sh_english.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\ragdollinteraction\languages\sh_french.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\ragdollinteraction\languages\sh_russian.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\rechargeableequipment\sh_plugin.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\rechargeableequipment\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\rechargeableequipment\items\engineering_consumables\sh_eng_battery.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\rechargeableequipment\items\outfit\sh_flashlight.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\rechargeableequipment\items\outfit\sh_mnhrflashlight.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\rechargeableequipment\items\outfit\sh_nightvision.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\rechargeableequipment\items\outfit\sh_nv_type14.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\rechargeableequipment\items\outfit\sh_nv_type6.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\rechargeableequipment\nvsdata\sh_nvgs.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\snowy_components\cl_derma.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\snowy_components\cl_fonts.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\snowy_components\sh_meta.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\snowy_components\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\snowy_components\sv_meta.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\snowy_components\derma\cl_objects.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\storageinterface\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\storageinterface\derma\cl_storage_interface.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\sh_config.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\sh_creation.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\sh_creation.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\sh_languages.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\sh_languages.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\sh_plugin.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\sh_skillbooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\sh_skilltree.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\derma\cl_traitcreation.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\base\sh_skillbook.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_ammo_craft_1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_craft1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_craft2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_craftarmor1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_craftarmor2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_crafttech1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_craftwep1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_craftwep2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_expl_craft_1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_hack1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_hack2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_hack3.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_heal_med.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_heal_med2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_heal_med3.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_med1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_med2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_med3.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_reanimate_med_1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_repair1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_repair2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_repaira1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_repaira2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_repairw1.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_tech_tech_wep_empire.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\traits\items\skillbook\sh_sb_tech_wep_newnation.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\tying\sh_animstuff.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\tying\sh_animstuff.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\tying\sh_charsearch.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\tying\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\tying\items\sh_tie.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\writing\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\writing\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\writing\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\writing\derma\cl_paper.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\writing\items\base\sh_writing.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\writing\items\writing\sh_note.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\writing\items\writing\sh_paper.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\sh_commands.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\sh_commands.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\sh_config.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\sh_schema.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\sh_voices.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\derma\cl_combine.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\derma\cl_data.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\derma\cl_objective.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_administrator.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_ara.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_cadet.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_centcom.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_corrupt.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_eule.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_geir.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_geshtalts.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_gscpersonnel.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_gscprotector.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_habr.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_imperial.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_ivent.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_kncr.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_kolibri.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_lstr.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_meir.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_mstr.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_mynath.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_notfal.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_refugee.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_star.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_storch.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\factions\sh_swan.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\hooks\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\hooks\sh_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\hooks\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\sh_bleach.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\sh_drugs_cigarettes.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\sh_fklr_plate.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\sh_matches.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\sh_pager.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\sh_ration.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\sh_screw_tool.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\sh_shovel_tool.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\sh_spraycan.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\sh_wrench_tool.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\ammo\sh_357ammo.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\ammo\sh_ammo_buckshot_pyro.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\ammo\sh_ammo_energy_cell.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\ammo\sh_ammo_high_caliber.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\ammo\sh_ammo_rifle.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\ammo\sh_ar2ammo.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\ammo\sh_pistolammo.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\ammo\sh_rocketammo.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\ammo\sh_shotgunammo.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\ammo\sh_smg1ammo.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\bags\sh_large.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\bags\sh_small.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\items\bags\sh_suitcase.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\languages\sh_russian.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\libs\sh_timer.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\libs\sh_voice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\libs\sv_itemspawnextender.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\schema\libs\sv_utils.lua

Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript
Lua files found: 218
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\entities\effects\nut_smallsmoke.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\entities\entities\nut_item.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\entities\entities\nut_money.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\entities\weapons\nut_hands.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\entities\weapons\nut_poshelper.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\entities\weapons\nut_poshelper.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\config\sh_config.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\sh_commands.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\sh_config.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\sh_config.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\sh_util.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\sv_data.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\derma\cl_contextmenu.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\derma\cl_dev_icon.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\derma\cl_horizontal_scroll.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\derma\cl_horizontal_scroll_bar.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\derma\cl_inventory.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\derma\cl_modelpanel.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\derma\cl_quick.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\derma\cl_spawnicon.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\derma\cl_tooltip.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\derma\cl_tooltip.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\derma\cl_uisounds.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\hooks\cl_hooks.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\hooks\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\hooks\sh_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\hooks\sv_hooks.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\hooks\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\cl_markup.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\cl_menu.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\cl_networking.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\cl_playerinteract.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\cl_playerinteract.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_anims.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_character.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_character.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_chatbox.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_chatbox.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_class.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_command.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_currency.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_date.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_date.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_faction.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_flag.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_inventory.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_item.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_language.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_log.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_player.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_plugin.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sv_database.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sv_database.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sv_inventory.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sv_networking.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sv_networking.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\sv_player.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\character\cl_networking.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\character\sv_character.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\item\cl_networking.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\item\sh_item_functions.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\item\sv_item.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\item\sv_networking.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\thirdparty\cl_ikon.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\thirdparty\cl_ikon.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\thirdparty\cl_surfaceGetURL.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\thirdparty\sh_deferred.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\thirdparty\sh_ease.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\thirdparty\sh_netstream2.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\thirdparty\sh_pon.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\libs\thirdparty\sh_utf8.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\meta\sh_base_inventory.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\meta\sh_character.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\meta\sh_item.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\meta\sh_player.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\meta\inventory\cl_base_inventory.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\meta\inventory\cl_panel_extensions.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\meta\inventory\cl_panel_extensions.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\meta\inventory\sv_base_inventory.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\meta\item\sh_item_debug.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\meta\item\sv_item.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\util\cl_blur.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\util\cl_door.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\util\cl_draw.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\util\cl_notice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\util\cl_stringreq.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\util\sh_chair.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\util\sh_sound.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\util\sh_string.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\util\sh_time.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\util\sv_action.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\util\sv_door.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\util\sv_notice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\util\sv_ragdoll.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\util\sv_stringreq.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\items\base\sh_ammo.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\items\base\sh_pacoutfit.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\items\base\sh_weapons.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\items\base\sh_weapons.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\languages\sh_russian.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\3dpanel.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\3dtext.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\ammosave.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\blur3d2d.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\chatsizediff.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\deathscreen.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\holsteredweps.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\logging.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\mapscene.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\newvoice.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\newvoice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\nscredits.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\nscredits.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\observer.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\permakill.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\persistence.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\pluginconfig.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\pluginconfig.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\propprotect.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\recognition.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\saveitems.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\serverguardsupport.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\spawns.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\spawnsaver.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\thirdperson.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\typing.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vignette.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\wepselect.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\act\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\act\sh_setup.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\area\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\area\derma\cl_areamanager.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\area\entities\weapons\nut_areahelper.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\area\entities\weapons\nut_areahelper.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\area\languages\sh_english.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\bars\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\bars\libs\cl_bar.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\chatbox\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\chatbox\derma\cl_chatbox.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\chatbox\derma\cl_markup.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\f1menu\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\f1menu\derma\cl_helps.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\f1menu\derma\cl_helps.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\f1menu\derma\cl_information.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\f1menu\derma\cl_information.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\f1menu\derma\cl_menu.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\f1menu\derma\cl_menubutton.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sh_grid_inv.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_access_rules.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\items\base\sh_bags.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\plugins\1_1compat\sh_plugin.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\plugins\1_1compat\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\plugins\1_1compat\sv_migrations.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\plugins\1_1compat\sv_migrations.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\plugins\1_1compat\libs\sh_item.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\plugins\gridinvui\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\plugins\gridinvui\derma\cl_grid_inventory.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\plugins\gridinvui\derma\cl_grid_inventory_item.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\plugins\gridinvui\derma\cl_grid_inventory_panel.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\plugins\gridstorage\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\cl_networking.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\sv_networking.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\plugins\charselect\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\plugins\charselect\derma\cl_bg_music.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\plugins\charselect\derma\cl_button.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\plugins\charselect\derma\cl_character.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\plugins\charselect\derma\cl_character_slot.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\plugins\charselect\derma\cl_confirmation.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\plugins\charselect\derma\cl_creation.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\plugins\charselect\derma\cl_selection.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\plugins\charselect\derma\cl_selection.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\plugins\charselect\derma\cl_step.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\plugins\charselect\derma\cl_tab_button.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\plugins\charselect\derma\steps\cl_biography.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\plugins\charselect\derma\steps\cl_faction.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\multichar\plugins\charselect\derma\steps\cl_model.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\notices\cl_notice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\notices\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\notices\derma\cl_notice.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\nsintro\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\nsintro\derma\cl_intro.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\nstheme\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\nstheme\derma\cl_skin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\pac\cl_parts.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\pac\cl_ragdolls.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\pac\sh_pacoutfit.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\pac\sh_permissions.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\pac\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\pac\sv_parts.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\playerinjuries\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\playerinjuries\sv_drowning.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\playerinjuries\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\raiseweapons\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\raiseweapons\sh_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\raiseweapons\sh_player_extensions.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\raiseweapons\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\raiseweapons\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\scoreboard\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\scoreboard\derma\cl_scoreboard.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\storage\cl_networking.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\storage\cl_password.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\storage\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\storage\sv_access_rules.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\storage\sv_networking.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\storage\sv_storage.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\storage\entities\entities\nut_storage\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\storage\entities\entities\nut_storage\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\storage\entities\entities\nut_storage\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\cl_editor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\cl_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\cl_networking.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\sh_enums.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\sv_data.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\sv_editor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\sv_hooks.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\sv_logging.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\sv_networking.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\derma\cl_vendor.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\derma\cl_vendor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\derma\cl_vendoreditor.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\derma\cl_vendoreditor.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\derma\cl_vendorfaction.lua
HOOKS FOUND in E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\derma\cl_vendorfaction.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\derma\cl_vendor_item.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\derma\cl_vendor_trader.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\entities\entities\nut_vendor\cl_init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\entities\entities\nut_vendor\init.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\entities\entities\nut_vendor\shared.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\_disabled\simpleinv\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\_disabled\simpleinv\sh_simple_inv.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\_disabled\simpleinv\items\base\sh_bags.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\_disabled\simpleinv\plugins\listinvui\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\_disabled\simpleinv\plugins\listinvui\derma\cl_list_inventory.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\_disabled\simpleinv\plugins\listinvui\derma\cl_list_inventory_panel.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\_disabled\simpleinv\plugins\liststorage\sh_plugin.lua
Reading: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\_disabled\simpleinv\plugins\liststorage\derma\cl_list_storage.lua

=== RESULTS ===
Saved 40 hooks -> manifests\hooks\cl_hooks.json
Saved 16 hooks -> manifests\hooks\sv_hooks.json
Saved 32 hooks -> manifests\hooks\sh_hooks.json
Saved 28 hooks -> manifests\hooks\unknown_hooks.json
Saved 74 entries -> manifests\networking\net_receives.json
Saved 86 entries -> manifests\networking\net_starts.json
Saved 264 entries -> manifests\networking\netstream_hooks.json
Saved 466 entries -> manifests\networking\netstream_starts.json
Saved 383 entries -> manifests\custom_hooks\plugin_methods.json
Saved 496 entries -> manifests\custom_hooks\hook_runs.json
```

### `scripts.extraction.extract_items`

- Path: `scripts/extraction/extract_items.py`
- Help status: `OK`

```text
Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis
Lua files found: 969

Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript
Lua files found: 218
Saved 511 entries -> manifests\items\item_classes.json
Saved 4103 entries -> manifests\items\item_properties.json
Saved 218 entries -> manifests\items\item_methods.json
Saved 316 entries -> manifests\items\item_calls.json
Saved 71 entries -> manifests\items\item_actions.json
Saved 136 entries -> manifests\items\item_action_callbacks.json
Saved 34 entries -> manifests\items\item_hooks.json
Saved 446 entries -> manifests\items\item_data_access.json
```

### `scripts.extraction.extract_network_payloads`

- Path: `scripts/extraction/extract_network_payloads.py`
- Help status: `OK`

```text
Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis
Lua files found: 969

Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript
Lua files found: 218
Saved 66 entries -> manifests\networking\util_add_network_strings.json
Saved 151 entries -> manifests\networking\net_writes.json
Saved 150 entries -> manifests\networking\net_reads.json
Saved 160 entries -> manifests\networking\net_messages_deep.json
```

### `scripts.extraction.extract_persistence`

- Path: `scripts/extraction/extract_persistence.py`
- Help status: `OK`

```text
Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis
Lua files found: 969

Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript
Lua files found: 218
Saved 1346 entries -> manifests\persistence\data_access.json
Saved 166 entries -> manifests\persistence\netvars.json
Saved 115 entries -> manifests\persistence\db_calls.json
Saved 8 entries -> manifests\persistence\sql_calls.json
```

### `scripts.extraction.extract_plugins`

- Path: `scripts/extraction/extract_plugins.py`
- Help status: `OK`

```text
Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis
Lua files found: 969

Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript
Lua files found: 218
Saved 332 entries -> manifests\plugins\plugin_properties.json
Saved 383 entries -> manifests\plugins\plugin_methods.json
Saved 496 entries -> manifests\plugins\hook_runs.json
Saved 47 entries -> manifests\plugins\plugin_refs.json
```

### `scripts.extraction.extract_registries`

- Path: `scripts/extraction/extract_registries.py`
- Help status: `OK`

```text
Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis
Lua files found: 969

Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript
Lua files found: 218
Saved 13 entries -> manifests\registries\nut_table_assignments.json
Saved 0 entries -> manifests\registries\nut_string_constants.json
Saved 3092 entries -> manifests\registries\nut_registry_refs.json
```

### `scripts.extraction.extract_timers`

- Path: `scripts/extraction/extract_timers.py`
- Help status: `OK`

```text
Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis
Lua files found: 969

Scanning root: E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript
Lua files found: 218
Saved 42 entries -> manifests\timers\timer_creates.json
Saved 131 entries -> manifests\timers\timer_simples.json
Saved 64 entries -> manifests\timers\timer_operations.json
Saved 183 entries -> manifests\timers\entity_timer_calls.json
Saved 102 entries -> manifests\timers\player_action_timers.json
```

## scripts/investigation

### `scripts.investigation.build_characterload_runtime_chain_candidate`

- Path: `scripts/investigation/build_characterload_runtime_chain_candidate.py`
- Help status: `OK`

```text
usage: build_characterload_runtime_chain_candidate.py [-h]
                                                      [--runtime-facts RUNTIME_FACTS]
                                                      [--out-json OUT_JSON]
                                                      [--out-md OUT_MD]

Build CharacterLoaded inventory lifecycle runtime-chain candidate from
normalized runtime facts.

options:
  -h, --help            show this help message and exit
  --runtime-facts RUNTIME_FACTS
  --out-json OUT_JSON
  --out-md OUT_MD
```

### `scripts.investigation.build_characterload_runtime_facts`

- Path: `scripts/investigation/build_characterload_runtime_facts.py`
- Help status: `OK`

```text
usage: build_characterload_runtime_facts.py [-h]
                                            [--source-validation SOURCE_VALIDATION]
                                            [--out-json OUT_JSON]
                                            [--out-md OUT_MD]

Build normalized runtime facts for CharacterLoaded inventory lifecycle
validation.

options:
  -h, --help            show this help message and exit
  --source-validation SOURCE_VALIDATION
  --out-json OUT_JSON
  --out-md OUT_MD
```

### `scripts.investigation.build_investigation_synthesis`

- Path: `scripts/investigation/build_investigation_synthesis.py`
- Help status: `OK`

```text
usage: build_investigation_synthesis.py [-h] --question QUESTION
                                        [--source-validation SOURCE_VALIDATION]
                                        [--runtime-facts RUNTIME_FACTS]
                                        [--runtime-chain-evidence RUNTIME_CHAIN_EVIDENCE]
                                        --out-json OUT_JSON --out-md OUT_MD

options:
  -h, --help            show this help message and exit
  --question QUESTION
  --source-validation SOURCE_VALIDATION
  --runtime-facts RUNTIME_FACTS
  --runtime-chain-evidence RUNTIME_CHAIN_EVIDENCE
  --out-json OUT_JSON
  --out-md OUT_MD
```

### `scripts.investigation.build_targeted_validation_request`

- Path: `scripts/investigation/build_targeted_validation_request.py`
- Help status: `OK`

```text
usage: build_targeted_validation_request.py [-h] --candidate CANDIDATE --out
                                            OUT

options:
  -h, --help            show this help message and exit
  --candidate CANDIDATE
  --out OUT
```

### `scripts.investigation.debug_runtime_propagation_v3_bridges`

- Path: `scripts/investigation/debug_runtime_propagation_v3_bridges.py`
- Help status: `OK`

```text
usage: debug_runtime_propagation_v3_bridges.py [-h] --runtime-topology
                                               RUNTIME_TOPOLOGY --out-md
                                               OUT_MD
                                               [--max-forward-lines MAX_FORWARD_LINES]
                                               [--max-backward-lines MAX_BACKWARD_LINES]
                                               [--focus-file FOCUS_FILE]

options:
  -h, --help            show this help message and exit
  --runtime-topology RUNTIME_TOPOLOGY
  --out-md OUT_MD
  --max-forward-lines MAX_FORWARD_LINES
  --max-backward-lines MAX_BACKWARD_LINES
  --focus-file FOCUS_FILE
```

### `scripts.investigation.evidence_ranker`

- Path: `scripts/investigation/evidence_ranker.py`
- Help status: `OK`

```text
(no help output)
```

### `scripts.investigation.promote_characterload_runtime_chain`

- Path: `scripts/investigation/promote_characterload_runtime_chain.py`
- Help status: `OK`

```text
usage: promote_characterload_runtime_chain.py [-h] [--candidate CANDIDATE]
                                              [--out-dir OUT_DIR]

Promote CharacterLoaded runtime chain candidate as topology/source-validation
supported chain.

options:
  -h, --help            show this help message and exit
  --candidate CANDIDATE
  --out-dir OUT_DIR
```

### `scripts.investigation.promote_runtime_chain_candidate`

- Path: `scripts/investigation/promote_runtime_chain_candidate.py`
- Help status: `OK`

```text
usage: promote_runtime_chain_candidate.py [-h] --candidate CANDIDATE --out OUT

options:
  -h, --help            show this help message and exit
  --candidate CANDIDATE
  --out OUT
```

### `scripts.investigation.run_targeted_validation_request`

- Path: `scripts/investigation/run_targeted_validation_request.py`
- Help status: `OK`

```text
usage: run_targeted_validation_request.py [-h] --workspace-config
                                          WORKSPACE_CONFIG --request REQUEST
                                          --out-json OUT_JSON --out-md OUT_MD

options:
  -h, --help            show this help message and exit
  --workspace-config WORKSPACE_CONFIG
  --request REQUEST
  --out-json OUT_JSON
  --out-md OUT_MD
```

### `scripts.investigation.runtime_chain_branch_builder`

- Path: `scripts/investigation/runtime_chain_branch_builder.py`
- Help status: `OK`

```text
usage: runtime_chain_branch_builder.py [-h] --ordered-steps ORDERED_STEPS
                                       --out-json OUT_JSON --out-md OUT_MD
                                       [--root ROOT] [--join JOIN]

Build branch-aware runtime chain from ordered runtime steps.

options:
  -h, --help            show this help message and exit
  --ordered-steps ORDERED_STEPS
  --out-json OUT_JSON
  --out-md OUT_MD
  --root ROOT
  --join JOIN
```

### `scripts.investigation.runtime_chain_builder`

- Path: `scripts/investigation/runtime_chain_builder.py`
- Help status: `OK`

```text
usage: runtime_chain_builder.py [-h] --workspace WORKSPACE
                                [--workspace-config WORKSPACE_CONFIG] --title
                                TITLE --query QUERY
                                [--validated-evidence VALIDATED_EVIDENCE]
                                [--runtime-facts RUNTIME_FACTS]
                                [--runtime-topology RUNTIME_TOPOLOGY]
                                [--targeted-validation TARGETED_VALIDATION]
                                [--promoted-chain PROMOTED_CHAIN] --out-json
                                OUT_JSON --out-md OUT_MD
                                [--max-steps MAX_STEPS]

Build general runtime chain candidate from validated investigation artifacts.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --workspace-config WORKSPACE_CONFIG
  --title TITLE
  --query QUERY
  --validated-evidence VALIDATED_EVIDENCE
  --runtime-facts RUNTIME_FACTS
  --runtime-topology RUNTIME_TOPOLOGY
  --targeted-validation TARGETED_VALIDATION
  --promoted-chain PROMOTED_CHAIN
  --out-json OUT_JSON
  --out-md OUT_MD
  --max-steps MAX_STEPS
```

### `scripts.investigation.runtime_chain_builder_v4`

- Path: `scripts/investigation/runtime_chain_builder_v4.py`
- Help status: `OK`

```text
usage: runtime_chain_builder_v4.py [-h] --title TITLE --pathfinder PATHFINDER
                                   [--validated-evidence VALIDATED_EVIDENCE]
                                   [--runtime-facts RUNTIME_FACTS]
                                   [--targeted-validation TARGETED_VALIDATION]
                                   --out-json OUT_JSON --out-md OUT_MD
                                   --out-targeted-validation
                                   OUT_TARGETED_VALIDATION

Runtime Chain Builder V4: merge topology pathfinder with validated evidence.

options:
  -h, --help            show this help message and exit
  --title TITLE
  --pathfinder PATHFINDER
  --validated-evidence VALIDATED_EVIDENCE
  --runtime-facts RUNTIME_FACTS
  --targeted-validation TARGETED_VALIDATION
  --out-json OUT_JSON
  --out-md OUT_MD
  --out-targeted-validation OUT_TARGETED_VALIDATION
```

### `scripts.investigation.runtime_chain_builder_v5`

- Path: `scripts/investigation/runtime_chain_builder_v5.py`
- Help status: `OK`

```text
usage: runtime_chain_builder_v5.py [-h] --title TITLE --runtime-facts
                                   RUNTIME_FACTS --runtime-fact-topology
                                   RUNTIME_FACT_TOPOLOGY --runtime-topology
                                   RUNTIME_TOPOLOGY
                                   [--stage-facts STAGE_FACTS] --out-json
                                   OUT_JSON --out-md OUT_MD
                                   [--max-depth MAX_DEPTH]

Build generic runtime chain candidate from runtime facts and fact-topology
bindings.

options:
  -h, --help            show this help message and exit
  --title TITLE
  --runtime-facts RUNTIME_FACTS
  --runtime-fact-topology RUNTIME_FACT_TOPOLOGY
  --runtime-topology RUNTIME_TOPOLOGY
  --stage-facts STAGE_FACTS
                        Comma-separated ordered fact names to build chain
                        links from.
  --out-json OUT_JSON
  --out-md OUT_MD
  --max-depth MAX_DEPTH
```

### `scripts.investigation.runtime_chain_candidate`

- Path: `scripts/investigation/runtime_chain_candidate.py`
- Help status: `OK`

```text
usage: runtime_chain_candidate.py [-h] --synthesis SYNTHESIS
                                  [--targeted-validation TARGETED_VALIDATION]
                                  --out-json OUT_JSON --out-md OUT_MD

options:
  -h, --help            show this help message and exit
  --synthesis SYNTHESIS
  --targeted-validation TARGETED_VALIDATION
  --out-json OUT_JSON
  --out-md OUT_MD
```

### `scripts.investigation.runtime_chain_graph`

- Path: `scripts/investigation/runtime_chain_graph.py`
- Help status: `OK`

```text
usage: runtime_chain_graph.py [-h] --workspace WORKSPACE [--nodes NODES]
                              [--edges EDGES] [--out-json OUT_JSON]
                              [--out-md OUT_MD] [--source-query SOURCE_QUERY]
                              [--target-query TARGET_QUERY]
                              [--max-paths MAX_PATHS] [--cutoff CUTOFF]

Runtime Chain Builder V4 graph foundation.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --nodes NODES
  --edges EDGES
  --out-json OUT_JSON
  --out-md OUT_MD
  --source-query SOURCE_QUERY
  --target-query TARGET_QUERY
  --max-paths MAX_PATHS
  --cutoff CUTOFF
```

### `scripts.investigation.runtime_chain_graph_characterload`

- Path: `scripts/investigation/runtime_chain_graph_characterload.py`
- Help status: `OK`

```text
Wrote graph audit JSON: investigations\validation\runtime_chain_graph_characterload_v1.json
Wrote graph audit MD:   investigations\validation\runtime_chain_graph_characterload_v1.md
Nodes: 5066
Edges: 19459
Candidate paths: 0
[RUN] E:\signalis_ai\.venv\Scripts\python.exe -m scripts.investigation.runtime_chain_graph --workspace E:\signalis_ai --source-query CharacterLoaded PlayerLoadedChar PrePlayerLoadedChar --target-query inventoryOpen inventorySetPanelStatus client inventory UI --max-paths 50 --cutoff 12 --out-json investigations\validation\runtime_chain_graph_characterload_v1.json --out-md investigations\validation\runtime_chain_graph_characterload_v1.md

[DONE] CharacterLoaded graph audit written:
JSON: investigations\validation\runtime_chain_graph_characterload_v1.json
MD:   investigations\validation\runtime_chain_graph_characterload_v1.md
```

### `scripts.investigation.runtime_chain_node_search_characterload`

- Path: `scripts/investigation/runtime_chain_node_search_characterload.py`
- Help status: `OK`

```text
Wrote: investigations\validation\runtime_chain_node_search_characterload_v1.md
```

### `scripts.investigation.runtime_chain_pathfinder`

- Path: `scripts/investigation/runtime_chain_pathfinder.py`
- Help status: `OK`

```text
usage: runtime_chain_pathfinder.py [-h] --graph-audit GRAPH_AUDIT --title
                                   TITLE --out-json OUT_JSON --out-md OUT_MD
                                   [--top-k TOP_K]

Score topology candidate paths and export runtime_chain.v2 candidate.

options:
  -h, --help            show this help message and exit
  --graph-audit GRAPH_AUDIT
  --title TITLE
  --out-json OUT_JSON
  --out-md OUT_MD
  --top-k TOP_K
```

### `scripts.investigation.runtime_chain_pipeline`

- Path: `scripts/investigation/runtime_chain_pipeline.py`
- Help status: `OK`

```text
usage: runtime_chain_pipeline.py [-h] --ranked-evidence RANKED_EVIDENCE --name
                                 NAME [--out-dir OUT_DIR]
                                 [--recovery-input [RECOVERY_INPUT ...]]
                                 [--root ROOT] [--join JOIN]
                                 [--min-score MIN_SCORE]
                                 [--min-evidence-score MIN_EVIDENCE_SCORE]
                                 [--max-evidence-per-step MAX_EVIDENCE_PER_STEP]
                                 [--drop-generic-related] [--drop-empty-text]
                                 [--drop-setup-only]

Run Runtime Chain Builder V4 pipeline: step builder -> step orderer -> branch
builder.

options:
  -h, --help            show this help message and exit
  --ranked-evidence RANKED_EVIDENCE
  --name NAME
  --out-dir OUT_DIR
  --recovery-input [RECOVERY_INPUT ...]
  --root ROOT
  --join JOIN
  --min-score MIN_SCORE
  --min-evidence-score MIN_EVIDENCE_SCORE
  --max-evidence-per-step MAX_EVIDENCE_PER_STEP
  --drop-generic-related
  --drop-empty-text
  --drop-setup-only
```

### `scripts.investigation.runtime_chain_promoter`

- Path: `scripts/investigation/runtime_chain_promoter.py`
- Help status: `OK`

```text
usage: runtime_chain_promoter.py [-h] --chain CHAIN --workspace WORKSPACE
                                 [--out OUT] [--allow-medium]

Promote a high-confidence runtime chain candidate into
docs/runtime/runtime_chains.

options:
  -h, --help            show this help message and exit
  --chain CHAIN
  --workspace WORKSPACE
  --out OUT
  --allow-medium
```

### `scripts.investigation.runtime_chain_promoter_v4`

- Path: `scripts/investigation/runtime_chain_promoter_v4.py`
- Help status: `OK`

```text
usage: runtime_chain_promoter_v4.py [-h] --chain CHAIN [--out-dir OUT_DIR]
                                    [--out-json OUT_JSON] [--fail-on-rejected]

options:
  -h, --help           show this help message and exit
  --chain CHAIN
  --out-dir OUT_DIR
  --out-json OUT_JSON
  --fail-on-rejected
```

### `scripts.investigation.runtime_chain_ranker`

- Path: `scripts/investigation/runtime_chain_ranker.py`
- Help status: `OK`

```text
usage: runtime_chain_ranker.py [-h] --input INPUT [INPUT ...] --scope SCOPE
                               --out-json OUT_JSON --out-md OUT_MD
                               [--top-n TOP_N]
                               [--max-per-cluster MAX_PER_CLUSTER]

Rank validated evidence for runtime-chain reconstruction.

options:
  -h, --help            show this help message and exit
  --input INPUT [INPUT ...]
  --scope SCOPE
  --out-json OUT_JSON
  --out-md OUT_MD
  --top-n TOP_N
  --max-per-cluster MAX_PER_CLUSTER
```

### `scripts.investigation.runtime_chain_regression`

- Path: `scripts/investigation/runtime_chain_regression.py`
- Help status: `OK`

```text
usage: runtime_chain_regression.py [-h] [--chains-dir CHAINS_DIR]
                                   [--out-json OUT_JSON] [--out-md OUT_MD]
                                   [--min-score MIN_SCORE] [--allow-medium]

Regression gate for promoted runtime-chain artifacts.

options:
  -h, --help            show this help message and exit
  --chains-dir CHAINS_DIR
  --out-json OUT_JSON
  --out-md OUT_MD
  --min-score MIN_SCORE
  --allow-medium
```

### `scripts.investigation.runtime_chain_scorer`

- Path: `scripts/investigation/runtime_chain_scorer.py`
- Help status: `OK`

```text
(no help output)
```

### `scripts.investigation.runtime_chain_step_builder`

- Path: `scripts/investigation/runtime_chain_step_builder.py`
- Help status: `OK`

```text
usage: runtime_chain_step_builder.py [-h] --ranked-evidence RANKED_EVIDENCE
                                     [--recovery-input [RECOVERY_INPUT ...]]
                                     --out-json OUT_JSON --out-md OUT_MD
                                     [--min-score MIN_SCORE]
                                     [--min-evidence-score MIN_EVIDENCE_SCORE]
                                     [--max-evidence-per-step MAX_EVIDENCE_PER_STEP]
                                     [--drop-generic-related]
                                     [--drop-empty-text] [--drop-setup-only]

options:
  -h, --help            show this help message and exit
  --ranked-evidence RANKED_EVIDENCE
  --recovery-input [RECOVERY_INPUT ...]
  --out-json OUT_JSON
  --out-md OUT_MD
  --min-score MIN_SCORE
  --min-evidence-score MIN_EVIDENCE_SCORE
  --max-evidence-per-step MAX_EVIDENCE_PER_STEP
  --drop-generic-related
  --drop-empty-text
  --drop-setup-only
```

### `scripts.investigation.runtime_chain_step_orderer`

- Path: `scripts/investigation/runtime_chain_step_orderer.py`
- Help status: `OK`

```text
usage: runtime_chain_step_orderer.py [-h] --steps STEPS --out-json OUT_JSON
                                     --out-md OUT_MD

Order runtime-chain causal steps into propagation sequence.

options:
  -h, --help           show this help message and exit
  --steps STEPS
  --out-json OUT_JSON
  --out-md OUT_MD
```

### `scripts.investigation.runtime_fact_builder`

- Path: `scripts/investigation/runtime_fact_builder.py`
- Help status: `OK`

```text
usage: runtime_fact_builder.py [-h] --source-validation SOURCE_VALIDATION
                               --out-json OUT_JSON --out-md OUT_MD

Build deduplicated normalized runtime facts from targeted source validation
output.

options:
  -h, --help            show this help message and exit
  --source-validation SOURCE_VALIDATION
  --out-json OUT_JSON
  --out-md OUT_MD
```

### `scripts.investigation.runtime_fact_graph`

- Path: `scripts/investigation/runtime_fact_graph.py`
- Help status: `OK`

```text
usage: runtime_fact_graph.py [-h] --runtime-facts RUNTIME_FACTS --out-json
                             OUT_JSON --out-md OUT_MD

Build a node-only runtime fact graph from normalized runtime facts.

options:
  -h, --help            show this help message and exit
  --runtime-facts RUNTIME_FACTS
  --out-json OUT_JSON
  --out-md OUT_MD
```

### `scripts.investigation.runtime_fact_topology_mapper`

- Path: `scripts/investigation/runtime_fact_topology_mapper.py`
- Help status: `OK`

```text
usage: runtime_fact_topology_mapper.py [-h] --runtime-fact-graph
                                       RUNTIME_FACT_GRAPH --runtime-topology
                                       RUNTIME_TOPOLOGY --out-json OUT_JSON
                                       --out-md OUT_MD
                                       [--max-matches MAX_MATCHES]

Map runtime fact graph nodes to runtime topology nodes with stricter quality
scoring.

options:
  -h, --help            show this help message and exit
  --runtime-fact-graph RUNTIME_FACT_GRAPH
  --runtime-topology RUNTIME_TOPOLOGY
  --out-json OUT_JSON
  --out-md OUT_MD
  --max-matches MAX_MATCHES
```

### `scripts.investigation.runtime_fact_topology_regression`

- Path: `scripts/investigation/runtime_fact_topology_regression.py`
- Help status: `OK`

```text
usage: runtime_fact_topology_regression.py [-h] --files FILES [FILES ...]
                                           --out-md OUT_MD

Regression checks for runtime fact topology mapping artifacts.

options:
  -h, --help            show this help message and exit
  --files FILES [FILES ...]
                        runtime_fact_topology.v3 JSON files to check.
  --out-md OUT_MD
```

### `scripts.investigation.runtime_propagation_topology_builder`

- Path: `scripts/investigation/runtime_propagation_topology_builder.py`
- Help status: `OK`

```text
usage: runtime_propagation_topology_builder.py [-h] [--workspace WORKSPACE]
                                               [--runtime-topology RUNTIME_TOPOLOGY]
                                               [--out-json OUT_JSON]
                                               [--out-md OUT_MD]
                                               [--max-callback-forward-lines MAX_CALLBACK_FORWARD_LINES]
                                               [--max-callback-backward-lines MAX_CALLBACK_BACKWARD_LINES]

Build traversal-oriented runtime propagation topology from
runtime_topology.json.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --runtime-topology RUNTIME_TOPOLOGY
  --out-json OUT_JSON
  --out-md OUT_MD
  --max-callback-forward-lines MAX_CALLBACK_FORWARD_LINES
  --max-callback-backward-lines MAX_CALLBACK_BACKWARD_LINES
```

### `scripts.investigation.runtime_propagation_topology_probe`

- Path: `scripts/investigation/runtime_propagation_topology_probe.py`
- Help status: `OK`

```text
usage: runtime_propagation_topology_probe.py [-h] --runtime-topology
                                             RUNTIME_TOPOLOGY --source SOURCE
                                             [--target TARGET]
                                             [--max-depth MAX_DEPTH] --out-md
                                             OUT_MD

options:
  -h, --help            show this help message and exit
  --runtime-topology RUNTIME_TOPOLOGY
  --source SOURCE
  --target TARGET
  --max-depth MAX_DEPTH
  --out-md OUT_MD
```

### `scripts.investigation.runtime_topology_node_probe`

- Path: `scripts/investigation/runtime_topology_node_probe.py`
- Help status: `OK`

```text
usage: runtime_topology_node_probe.py [-h] --runtime-topology RUNTIME_TOPOLOGY
                                      --node-id NODE_ID --out-md OUT_MD
                                      [--max-edges MAX_EDGES]

Inspect incoming/outgoing edges around a runtime topology node.

options:
  -h, --help            show this help message and exit
  --runtime-topology RUNTIME_TOPOLOGY
  --node-id NODE_ID
  --out-md OUT_MD
  --max-edges MAX_EDGES
```

## scripts/normalization

### `scripts.normalization.build_hook_event_bus`

- Path: `scripts/normalization/build_hook_event_bus.py`
- Help status: `OK`

```text
usage: build_hook_event_bus.py [-h] [--workspace WORKSPACE]
                               [--manifests-dir MANIFESTS_DIR]
                               [--normalized-dir NORMALIZED_DIR]
                               [--source-root SOURCE_ROOT]
                               [--nutscript-root NUTSCRIPT_ROOT] [--write]

Build normalized NutScript/GMod hook event-bus graph.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
                        Workspace root, e.g. E:/signalis_ai
  --manifests-dir MANIFESTS_DIR
                        Override manifests dir. Default: <workspace>/manifests
  --normalized-dir NORMALIZED_DIR
                        Override normalized dir. Default: <manifests-
                        dir>/normalized
  --source-root SOURCE_ROOT
                        Optional source root to scan for GM/PLUGIN/SCHEMA
                        methods. Can be repeated.
  --nutscript-root NUTSCRIPT_ROOT
                        Optional NutScript source root to scan.
  --write               Write output files. Without this, prints summary only.
```

### `scripts.normalization.build_network_graph`

- Path: `scripts/normalization/build_network_graph.py`
- Help status: `OK`

```text
usage: build_network_graph.py [-h] --workspace WORKSPACE [--write]

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
                        Workspace root, e.g. E:/signalis_ai
  --write               Write output files
```

### `scripts.normalization.build_runtime_graph`

- Path: `scripts/normalization/build_runtime_graph.py`
- Help status: `OK`

```text
usage: build_runtime_graph.py [-h] [--workspace WORKSPACE]
                              [--normalized-dir NORMALIZED_DIR] [--write]

Build Runtime Graph V1 from normalized hook event-bus manifests.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
                        Workspace root, e.g. E:/signalis_ai
  --normalized-dir NORMALIZED_DIR
                        Override normalized dir. Default:
                        <workspace>/manifests/normalized
  --write               Write output files. Without this, prints summary only.
```

### `scripts.normalization.build_timer_graph`

- Path: `scripts/normalization/build_timer_graph.py`
- Help status: `OK`

```text
usage: build_timer_graph.py [-h] --workspace WORKSPACE [--write]

Build normalized timer/scheduler graph from manifests.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
                        Project workspace root, e.g. E:/signalis_ai
  --write               Write outputs to manifests/normalized
```

### `scripts.normalization.merge_runtime_graphs`

- Path: `scripts/normalization/merge_runtime_graphs.py`
- Help status: `OK`

```text
usage: merge_runtime_graphs.py [-h] --workspace WORKSPACE
                               [--normalized-dir NORMALIZED_DIR] [--write]

Merge normalized hook/network/timer graphs into runtime topology.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
                        Workspace root, e.g. E:/signalis_ai
  --normalized-dir NORMALIZED_DIR
                        Override normalized manifest directory
  --write               Write outputs
```

### `scripts.normalization.normalize_hook_symbols`

- Path: `scripts/normalization/normalize_hook_symbols.py`
- Help status: `OK`

```text
usage: normalize_hook_symbols.py [-h] [--workspace WORKSPACE]
                                 [--source-root SOURCE_ROOT] [--write]

Normalize symbolic hook.Run names to plugin hook methods.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
                        Workspace root containing manifests/. Example:
                        E:/signalis_ai
  --source-root SOURCE_ROOT
                        Lua source root. Can be passed multiple times.
  --write               Write normalized JSON outputs. Without this, only
                        prints a summary.
```

### `scripts.normalization.normalize_network_operations`

- Path: `scripts/normalization/normalize_network_operations.py`
- Help status: `OK`

```text
usage: normalize_network_operations.py [-h] [--workspace WORKSPACE]
                                       [--source-root SOURCE_ROOT]
                                       [--nutscript-root NUTSCRIPT_ROOT]
                                       [--write]

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
                        Project workspace, e.g. E:/signalis_ai
  --source-root SOURCE_ROOT
                        Signalis gamemode source root for source-call recovery
  --nutscript-root NUTSCRIPT_ROOT
                        NutScript gamemode source root for source-call
                        recovery
  --write
```

### `scripts.normalization.qa_hook_resolution`

- Path: `scripts/normalization/qa_hook_resolution.py`
- Help status: `OK`

```text
usage: qa_hook_resolution.py [-h] [--workspace WORKSPACE]
                             [--normalized-dir NORMALIZED_DIR]
                             [--source-root SOURCE_ROOT]
                             [--nutscript-root NUTSCRIPT_ROOT] [--write]
                             [--top TOP]

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
                        Project workspace, e.g. E:/signalis_ai
  --normalized-dir NORMALIZED_DIR
                        Override normalized manifest dir
  --source-root SOURCE_ROOT
                        Optional Signalis source root for independent QA scan
  --nutscript-root NUTSCRIPT_ROOT
                        Optional NutScript source root for independent QA scan
  --write               Write qa JSON and markdown reports
  --top TOP             How many top unresolved names to include
```

## scripts/qdrant

### `scripts.qdrant.add_runtime_chains_to_qdrant_documents`

- Path: `scripts/qdrant/add_runtime_chains_to_qdrant_documents.py`
- Help status: `OK`

```text
usage: add_runtime_chains_to_qdrant_documents.py [-h] --workspace WORKSPACE
                                                 [--chain-dir CHAIN_DIR]
                                                 [--documents DOCUMENTS]

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --chain-dir CHAIN_DIR
                        Defaults to <workspace>/docs/runtime/runtime_chains
  --documents DOCUMENTS
                        Defaults to
                        <workspace>/manifests/semantic/qdrant_documents.jsonl
```

### `scripts.qdrant.audit_embedding_ingest_counts`

- Path: `scripts/qdrant/audit_embedding_ingest_counts.py`
- Help status: `OK`

```text
usage: audit_embedding_ingest_counts.py [-h] --workspace WORKSPACE

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
```

### `scripts.qdrant.audit_ingest_filtering`

- Path: `scripts/qdrant/audit_ingest_filtering.py`
- Help status: `OK`

```text
usage: audit_ingest_filtering.py [-h] --workspace WORKSPACE
                                 [--expected-dim EXPECTED_DIM]

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --expected-dim EXPECTED_DIM
```

### `scripts.qdrant.build_evidence_graph`

- Path: `scripts/qdrant/build_evidence_graph.py`
- Help status: `OK`

```text
usage: build_evidence_graph.py [-h] --deduped DEDUPED [--out-dir OUT_DIR]

options:
  -h, --help         show this help message and exit
  --deduped DEDUPED
  --out-dir OUT_DIR
```

### `scripts.qdrant.build_investigation_context_pack`

- Path: `scripts/qdrant/build_investigation_context_pack.py`
- Help status: `OK`

```text
usage: build_investigation_context_pack.py [-h] --workspace WORKSPACE --query
                                           QUERY
                                           [--query-results QUERY_RESULTS]
                                           [--out OUT] [--no-dedupe]
                                           [--text-limit TEXT_LIMIT]
                                           [--runtime-chain-limit RUNTIME_CHAIN_LIMIT]

Build a deduplicated investigation context pack from Qdrant markdown results.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --query QUERY
  --query-results QUERY_RESULTS
                        Defaults to manifests/semantic/qdrant_query_results.md
  --out OUT             Defaults to investigations/context_pack.md
  --no-dedupe
  --text-limit TEXT_LIMIT
  --runtime-chain-limit RUNTIME_CHAIN_LIMIT
```

### `scripts.qdrant.build_qdrant_documents`

- Path: `scripts/qdrant/build_qdrant_documents.py`
- Help status: `OK`

```text
usage: build_qdrant_documents.py [-h] [--workspace WORKSPACE] [--write]
                                 [--include-node-docs]
                                 [--top-node-docs TOP_NODE_DOCS]

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --write
  --include-node-docs   Include per-node documents for all nodes. Can be
                        large.
  --top-node-docs TOP_NODE_DOCS
                        Include this many high-degree node docs by default.
```

### `scripts.qdrant.build_runtime_chain_evidence`

- Path: `scripts/qdrant/build_runtime_chain_evidence.py`
- Help status: `OK`

```text
usage: build_runtime_chain_evidence.py [-h] --synthesis SOURCE_VALIDATION
                                       [--out-dir OUT_DIR]

Build deduped/ranked runtime chain evidence from targeted source-validation
JSON.

options:
  -h, --help            show this help message and exit
  --synthesis SOURCE_VALIDATION, --source-validation SOURCE_VALIDATION
  --out-dir OUT_DIR
```

### `scripts.qdrant.build_runtime_chains`

- Path: `scripts/qdrant/build_runtime_chains.py`
- Help status: `OK`

```text
usage: build_runtime_chains.py [-h] --facts FACTS [--out-dir OUT_DIR]

options:
  -h, --help         show this help message and exit
  --facts FACTS
  --out-dir OUT_DIR
```

### `scripts.qdrant.build_targeted_validation_report`

- Path: `scripts/qdrant/build_targeted_validation_report.py`
- Help status: `OK`

```text
usage: build_targeted_validation_report.py [-h] --synthesis SYNTHESIS
                                           [--out-dir OUT_DIR]

options:
  -h, --help            show this help message and exit
  --synthesis SYNTHESIS
  --out-dir OUT_DIR
```

### `scripts.qdrant.check_embedding_outputs`

- Path: `scripts/qdrant/check_embedding_outputs.py`
- Help status: `OK`

```text
usage: check_embedding_outputs.py [-h] --workspace WORKSPACE

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
```

### `scripts.qdrant.check_runtime_chain_in_qdrant_docs`

- Path: `scripts/qdrant/check_runtime_chain_in_qdrant_docs.py`
- Help status: `OK`

```text
usage: check_runtime_chain_in_qdrant_docs.py [-h] --workspace WORKSPACE
                                             [--needle NEEDLE]

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --needle NEEDLE       Text/path/title fragment to search in generated Qdrant
                        documents.
```

### `scripts.qdrant.context_pack`

- Path: `scripts/qdrant/context_pack.py`
- Help status: `OK`

```text
(no help output)
```

### `scripts.qdrant.deduplicate_qdrant_results`

- Path: `scripts/qdrant/deduplicate_qdrant_results.py`
- Help status: `OK`

```text
usage: deduplicate_qdrant_results.py [-h] --workspace WORKSPACE
                                     [--query-results QUERY_RESULTS]
                                     [--out OUT]

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --query-results QUERY_RESULTS
                        Defaults to manifests/semantic/qdrant_query_results.md
  --out OUT             Defaults to
                        manifests/semantic/qdrant_query_results_deduped.md
```

### `scripts.qdrant.deduplicate_validation_fragments`

- Path: `scripts/qdrant/deduplicate_validation_fragments.py`
- Help status: `OK`

```text
usage: deduplicate_validation_fragments.py [-h] --validation VALIDATION
                                           [--out-dir OUT_DIR]
                                           [--line-tolerance LINE_TOLERANCE]
                                           [--max-items MAX_ITEMS]

options:
  -h, --help            show this help message and exit
  --validation VALIDATION
  --out-dir OUT_DIR
  --line-tolerance LINE_TOLERANCE
  --max-items MAX_ITEMS
```

### `scripts.qdrant.embed_qdrant_documents`

- Path: `scripts/qdrant/embed_qdrant_documents.py`
- Help status: `OK`

```text
usage: embed_qdrant_documents.py [-h] --workspace WORKSPACE [--model MODEL]
                                 [--fallback-model FALLBACK_MODEL]
                                 [--device DEVICE] [--batch-size BATCH_SIZE]
                                 [--limit LIMIT] [--trust-remote-code]
                                 [--hash-only] [--hash-dim HASH_DIM] [--write]

Embed SIGNALIS Qdrant documents with deterministic no-model fallback.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --model MODEL
  --fallback-model FALLBACK_MODEL
  --device DEVICE
  --batch-size BATCH_SIZE
  --limit LIMIT
  --trust-remote-code
  --hash-only           Skip sentence-transformers and use deterministic
                        fallback.
  --hash-dim HASH_DIM
  --write
```

### `scripts.qdrant.evaluate_retrieval`

- Path: `scripts/qdrant/evaluate_retrieval.py`
- Help status: `OK`

```text
usage: evaluate_retrieval.py [-h] [--queries QUERIES] [--results RESULTS]
                             [--workspace WORKSPACE]
                             [--query-script QUERY_SCRIPT] [--out OUT]
                             [--top-k TOP_K] [--pass-threshold PASS_THRESHOLD]
                             [--only [ONLY ...]]
                             [--extra-query-arg EXTRA_QUERY_ARG]

Evaluate SIGNALIS retrieval quality.

options:
  -h, --help            show this help message and exit
  --queries QUERIES     Path to retrieval_queries.yaml.
  --results RESULTS     Optional JSON/MD/TXT results file to evaluate instead
                        of running query command.
  --workspace WORKSPACE
                        Workspace path for command mode.
  --query-script QUERY_SCRIPT
                        Path to query_qdrant.py for command mode.
  --out OUT             Output directory for latest.json/latest.md.
  --top-k TOP_K         Override top_k from YAML defaults.
  --pass-threshold PASS_THRESHOLD
                        Overall score needed for PASS.
  --only [ONLY ...]     Optional query IDs to run/evaluate.
  --extra-query-arg EXTRA_QUERY_ARG
                        Extra argument passed to query_qdrant.py. Can be
                        repeated.
```

### `scripts.qdrant.extract_runtime_facts`

- Path: `scripts/qdrant/extract_runtime_facts.py`
- Help status: `OK`

```text
usage: extract_runtime_facts.py [-h] --deduped DEDUPED [--out-dir OUT_DIR]

options:
  -h, --help         show this help message and exit
  --deduped DEDUPED
  --out-dir OUT_DIR
```

### `scripts.qdrant.ingest_qdrant`

- Path: `scripts/qdrant/ingest_qdrant.py`
- Help status: `OK`

```text
usage: ingest_qdrant.py [-h] --workspace WORKSPACE [--host HOST] [--port PORT]
                        [--collection COLLECTION] [--batch-size BATCH_SIZE]
                        [--recreate] [--dry-run] [--write]

Ingest SIGNALIS semantic embeddings into Qdrant.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
                        Workspace root, e.g. E:/signalis_ai
  --host HOST           Qdrant host
  --port PORT           Qdrant HTTP port
  --collection COLLECTION
  --batch-size BATCH_SIZE
  --recreate            Drop/recreate collection
  --dry-run             Validate only; do not ingest
  --write               Write summary markdown
```

### `scripts.qdrant.investigate`

- Path: `scripts/qdrant/investigate.py`
- Help status: `OK`

```text
usage: investigate.py [-h] --workspace WORKSPACE --query QUERY [--top-k TOP_K]
                      [--collection COLLECTION] [--out-dir OUT_DIR]
                      [--extra-query-arg EXTRA_QUERY_ARG] [--no-human-context]
                      [--no-project-memory] [--no-topology-summary]

Generate SIGNALIS investigation report.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --query QUERY
  --top-k TOP_K
  --collection COLLECTION
  --out-dir OUT_DIR
  --extra-query-arg EXTRA_QUERY_ARG
  --no-human-context
  --no-project-memory
  --no-topology-summary
```

### `scripts.qdrant.patch_vendor_purchase_validation_targets`

- Path: `scripts/qdrant/patch_vendor_purchase_validation_targets.py`
- Help status: `OK`

```text
usage: patch_vendor_purchase_validation_targets.py [-h] --input INPUT
                                                   [--output OUTPUT]

Patch vendor purchase targeted validation plan with missing source checks.

options:
  -h, --help       show this help message and exit
  --input INPUT    Existing *_targeted_validation.json file
  --output OUTPUT  Patched output json. Defaults to *_patched.json
```

### `scripts.qdrant.path_reconstruction`

- Path: `scripts/qdrant/path_reconstruction.py`
- Help status: `OK`

```text
usage: path_reconstruction.py [-h] --workspace WORKSPACE [--topology TOPOLOGY]
                              --from FROM_TERM --to TO_TERM
                              [--max-depth MAX_DEPTH] [--max-paths MAX_PATHS]
                              [--output OUTPUT]

Reconstruct candidate runtime topology paths.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --topology TOPOLOGY
  --from FROM_TERM
  --to TO_TERM
  --max-depth MAX_DEPTH
  --max-paths MAX_PATHS
  --output OUTPUT
```

### `scripts.qdrant.path_reconstruction_v2`

- Path: `scripts/qdrant/path_reconstruction_v2.py`
- Help status: `OK`

```text
usage: path_reconstruction_v2.py [-h] --workspace WORKSPACE
                                 [--topology TOPOLOGY] --from FROM_TERM --to
                                 TO_TERM [--terms [TERMS ...]]
                                 [--max-depth MAX_DEPTH]
                                 [--max-paths MAX_PATHS] [--output OUTPUT]

Weighted runtime topology path reconstruction.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --topology TOPOLOGY
  --from FROM_TERM
  --to TO_TERM
  --terms [TERMS ...]
  --max-depth MAX_DEPTH
  --max-paths MAX_PATHS
  --output OUTPUT
```

### `scripts.qdrant.promote_runtime_chain`

- Path: `scripts/qdrant/promote_runtime_chain.py`
- Help status: `OK`

```text
usage: promote_runtime_chain.py [-h] --chain CHAIN --subsystem SUBSYSTEM
                                --name NAME [--out-dir OUT_DIR] [--out OUT]
                                [--title TITLE] [--chain-id CHAIN_ID]

Promote validated runtime chain evidence into durable runtime-chain
documentation.

options:
  -h, --help            show this help message and exit
  --chain CHAIN         Runtime chain evidence JSON
  --subsystem SUBSYSTEM
                        Subsystem name, e.g. vendor
  --name NAME           Output slug/name, e.g.
                        vendor_purchase_item_metadata_sync
  --out-dir OUT_DIR
  --out OUT             Optional exact output markdown path
  --title TITLE         Optional document title
  --chain-id CHAIN_ID   Optional chain id to select from multi-chain evidence
                        JSON
```

### `scripts.qdrant.promote_vendor_purchase_chain_doc`

- Path: `scripts/qdrant/promote_vendor_purchase_chain_doc.py`
- Help status: `OK`

```text
usage: promote_vendor_purchase_chain_doc.py [-h] --chain-evidence
                                            CHAIN_EVIDENCE [--out OUT]

Promote validated vendor purchase runtime chain to durable markdown doc.

options:
  -h, --help            show this help message and exit
  --chain-evidence CHAIN_EVIDENCE
                        Runtime chain evidence JSON produced by
                        build_runtime_chain_evidence.py
  --out OUT
```

### `scripts.qdrant.query_qdrant`

- Path: `scripts/qdrant/query_qdrant.py`
- Help status: `OK`

```text
usage: query_qdrant.py [-h] --workspace WORKSPACE [--collection COLLECTION]
                       --query QUERY [--model MODEL] [--top-k TOP_K]
                       [--retrieve-k RETRIEVE_K] [--host HOST] [--port PORT]
                       [--hash] [--dim DIM] [--no-expand] [--rerank] [--write]
                       [--out OUT] [--doc-type DOC_TYPE] [--file FILE]

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --collection COLLECTION
  --query QUERY
  --model MODEL
  --top-k TOP_K
  --retrieve-k RETRIEVE_K
  --host HOST
  --port PORT
  --hash                Use deterministic hash query vector.
  --dim DIM
  --no-expand
  --rerank
  --write
  --out OUT
  --doc-type DOC_TYPE
  --file FILE
```

### `scripts.qdrant.rerank_results`

- Path: `scripts/qdrant/rerank_results.py`
- Help status: `OK`

```text
(no help output)
```

### `scripts.qdrant.retrieval_intent`

- Path: `scripts/qdrant/retrieval_intent.py`
- Help status: `OK`

```text
(no help output)
```

### `scripts.qdrant.score_validation_report`

- Path: `scripts/qdrant/score_validation_report.py`
- Help status: `OK`

```text
(no help output)
```

### `scripts.qdrant.synthesize_investigation`

- Path: `scripts/qdrant/synthesize_investigation.py`
- Help status: `OK`

```text
usage: synthesize_investigation.py [-h] --chains CHAINS [--out-dir OUT_DIR]

options:
  -h, --help         show this help message and exit
  --chains CHAINS
  --out-dir OUT_DIR
```

### `scripts.qdrant.validate_sources`

- Path: `scripts/qdrant/validate_sources.py`
- Help status: `OK`

```text
usage: validate_sources.py [-h] --validation VALIDATION [--out-dir OUT_DIR]
                           [--max-per-bucket MAX_PER_BUCKET]

options:
  -h, --help            show this help message and exit
  --validation VALIDATION
  --out-dir OUT_DIR
  --max-per-bucket MAX_PER_BUCKET
```

### `scripts.qdrant.validate_targeted_sources`

- Path: `scripts/qdrant/validate_targeted_sources.py`
- Help status: `OK`

```text
usage: validate_targeted_sources.py [-h] [--workspace WORKSPACE]
                                    [--workspace-config WORKSPACE_CONFIG]
                                    --targeted TARGETED [--out-dir OUT_DIR]
                                    [--context CONTEXT]
                                    [--max-hits-per-pattern MAX_HITS_PER_PATTERN]

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --workspace-config WORKSPACE_CONFIG
  --targeted TARGETED
  --out-dir OUT_DIR
  --context CONTEXT
  --max-hits-per-pattern MAX_HITS_PER_PATTERN
```

## scripts/semantic

### `scripts.semantic.generate_subsystem_docs`

- Path: `scripts/semantic/generate_subsystem_docs.py`
- Help status: `OK`

```text
usage: generate_subsystem_docs.py [-h] --workspace WORKSPACE
                                  [--topology TOPOLOGY]
                                  [--output-dir OUTPUT_DIR]
                                  [--subsystems [SUBSYSTEMS ...]]

Generate subsystem semantic docs from runtime topology.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --topology TOPOLOGY
  --output-dir OUTPUT_DIR
  --subsystems [SUBSYSTEMS ...]
```

## scripts/tools

### `scripts.tools.generate_project_structure`

- Path: `scripts/tools/generate_project_structure.py`
- Help status: `OK`

```text
usage: generate_project_structure.py [-h] --workspace WORKSPACE
                                     [--output OUTPUT] [--max-depth MAX_DEPTH]

Generate SIGNALIS AI project structure manifest.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --output OUTPUT
  --max-depth MAX_DEPTH
```

### `scripts.tools.generate_script_contracts`

- Path: `scripts/tools/generate_script_contracts.py`
- Help status: `OK`

```text
usage: generate_script_contracts.py [-h] [--root ROOT]
                                    [--scripts-dir SCRIPTS_DIR]
                                    [--out-md OUT_MD] [--out-json OUT_JSON]

Generate script CLI contract documentation from python -m <module> --help.

options:
  -h, --help            show this help message and exit
  --root ROOT
  --scripts-dir SCRIPTS_DIR
  --out-md OUT_MD
  --out-json OUT_JSON
```
