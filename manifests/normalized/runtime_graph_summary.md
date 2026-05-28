# Runtime graph summary

Schema: `runtime_graph.v1`

## Totals
- Nodes: **2376**
- Edges: **8263**
- Hook events: **464**
- Files: **292**
- Plugins: **70**
- Runtime dispatch edges: **1041**

## Node types
- `hook_listener`: **999**
- `hook_emitter`: **495**
- `hook_event`: **464**
- `file`: **292**
- `plugin`: **70**
- `hook_owner`: **42**
- `event_class`: **9**
- `realm`: **3**
- `gamemode`: **1**
- `schema`: **1**

## Edge types
- `runs_in_realm`: **1786**
- `dispatches_to`: **1041**
- `contains_listener`: **999**
- `listens_to`: **999**
- `registers_listener`: **992**
- `listens_to_event`: **596**
- `contains_emitter`: **495**
- `emits`: **495**
- `classified_as`: **464**
- `owns_file`: **219**
- `emits_event`: **177**

## Top emitted events
- `HandleDiseaseOnEnd`: 38
- `CreateUsingInterface`: 26
- `HandleDiseaseOnCall`: 20
- `CheckBothHandsAmputation`: 12
- `HandlePain`: 12
- `GetDisplayedName`: 11
- `screamer2`: 9
- `LoadNutFonts`: 7
- `HandleInfection`: 6
- `StorageRestored`: 5
- `OnCharVarChanged`: 5
- `StorageInventorySet`: 5
- `HandleBloodLoss`: 5
- `StorageEntityRemoved`: 5
- `EnduranceDecrease`: 4
- `GetDefaultCharName`: 4
- `saveStorage`: 4
- `EnduranceCheck`: 4
- `CreateNewInventoryPanel`: 4
- `ItemTransfered`: 4
- `OnNPCKilled`: 3
- `HandlePainKillBoost`: 3
- `SaveData`: 3
- `ItemInitialized`: 3
- `OnCharRecognized`: 3
- `HandleBulletInjure`: 3
- `PersistenceSave`: 3
- `CanItemBeTransfered`: 3
- `ShouldAllowScoreboardOverride`: 3
- `IsPlayerRecognized`: 3

## Top listened events
- `LoadData`: 45
- `SaveData`: 35
- `HUDPaint`: 22
- `PostPlayerLoadout`: 16
- `PlayerDeath`: 14
- `PlayerLoadedChar`: 13
- `SetupQuickMenu`: 13
- `PlayerInitialSpawn`: 13
- `Think`: 13
- `PlayerLoadout`: 11
- `CharacterPreSave`: 11
- `PrePlayerLoadedChar`: 11
- `LoadFonts`: 10
- `PlayerBindPress`: 10
- `KeyPress`: 10
- `EntityTakeDamage`: 8
- `OnCharCreated`: 8
- `PlayerButtonDown`: 7
- `PostDrawTranslucentRenderables`: 7
- `CanPlayerInteractItem`: 7
- `LoadNutFonts`: 7
- `ShouldDrawEntityInfo`: 7
- `CalcView`: 7
- `InitPostEntity`: 7
- `PlayerHurt`: 6
- `HUDPaintBackground`: 6
- `PlayerSpawn`: 6
- `InitializedPlugins`: 6
- `OnEntityCreated`: 6
- `PhysgunPickup`: 5

## Top runtime dispatch events
- `SaveData`: 105 dispatch edge(s)
- `LoadData`: 90 dispatch edge(s)
- `HandleDiseaseOnEnd`: 76 dispatch edge(s)
- `CreateUsingInterface`: 52 dispatch edge(s)
- `LoadNutFonts`: 49 dispatch edge(s)
- `HandleDiseaseOnCall`: 40 dispatch edge(s)
- `CheckBothHandsAmputation`: 24 dispatch edge(s)
- `HandlePain`: 24 dispatch edge(s)
- `GetDisplayedName`: 22 dispatch edge(s)
- `PlayerLoadout`: 22 dispatch edge(s)
- `OnCharVarChanged`: 20 dispatch edge(s)
- `PostPlayerLoadout`: 16 dispatch edge(s)
- `SetupQuickMenu`: 13 dispatch edge(s)
- `PlayerLoadedChar`: 13 dispatch edge(s)
- `HandleInfection`: 12 dispatch edge(s)
- `CharacterPreSave`: 11 dispatch edge(s)
- `PrePlayerLoadedChar`: 11 dispatch edge(s)
- `StorageInventorySet`: 10 dispatch edge(s)
- `LoadFonts`: 10 dispatch edge(s)
- `HandleBloodLoss`: 10 dispatch edge(s)
- `screamer2`: 9 dispatch edge(s)
- `CanItemBeTransfered`: 9 dispatch edge(s)
- `EnduranceDecrease`: 8 dispatch edge(s)
- `saveStorage`: 8 dispatch edge(s)
- `EnduranceCheck`: 8 dispatch edge(s)
- `GetDefaultInventoryType`: 8 dispatch edge(s)
- `CreateNewInventoryPanel`: 8 dispatch edge(s)
- `CharacterLoaded`: 8 dispatch edge(s)
- `ItemTransfered`: 8 dispatch edge(s)
- `OnCharCreated`: 8 dispatch edge(s)

## Hot files by emitter/listener declarations
- `gamemode\core\hooks\sv_hooks.lua`: 82
- `plugins\healthproblems\sv_hooks.lua`: 54
- `gamemode\core\hooks\cl_hooks.lua`: 31
- `plugins\hud\sh_plugin.lua`: 28
- `plugins\ragdollinteraction\interaction\sv_hooks.lua`: 26
- `plugins\recognition.lua`: 25
- `plugins\gridinv\plugins\1_1compat\sv_migrations.lua`: 25
- `plugins\attributes\plugins\strength\sh_plugin.lua`: 22
- `plugins\area\sh_plugin.lua`: 21
- `schema\hooks\sv_hooks.lua`: 20
- `plugins\tying\sh_charsearch.lua`: 18
- `plugins\storage\sv_storage.lua`: 17
- `gamemode\core\hooks\sh_hooks.lua`: 16
- `plugins\propprotect.lua`: 16
- `plugins\ragdollinteraction\corpses\sv_hooks.lua`: 15
- `entities\weapons\nut_hands.lua`: 14
- `gamemode\core\libs\sh_plugin.lua`: 14
- `plugins\armor\sh_plugin.lua`: 14
- `plugins\biorezonance\sh_plugin.lua`: 14
- `plugins\act\sh_plugin.lua`: 14
- `plugins\logging.lua`: 14
- `plugins\chatbox\sh_plugin.lua`: 13
- `plugins\multichar\sh_plugin.lua`: 12
- `plugins\observer.lua`: 12
- `plugins\pluginconfig.lua`: 12
