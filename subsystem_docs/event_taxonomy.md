# SIGNALIS AI — Event Taxonomy

## Core Rule

In this project:

```text
hook.Run(X)
```

is modeled as:

```text
event emission
```

not as a direct method call.

Listeners include:

```text
PLUGIN:X
SCHEMA:X
GM:X
hook.Add(X, ...)
```

---

## NutScript Plugin Listener Registration

NutScript plugin loading registers every function on `PLUGIN` / `SCHEMA` as a hook listener.

Equivalent model:

```lua
for k, v in pairs(PLUGIN) do
    if type(v) == "function" then
        hook.Add(k, PLUGIN, v)
    end
end
```

Therefore:

```text
function PLUGIN:SaveData()
```

means:

```text
listener for event SaveData
```

and:

```text
function SCHEMA:PlayerLoadedChar(...)
```

means:

```text
schema listener for event PlayerLoadedChar
```

---

## Hook Dispatch Semantics

Facepunch/GMod behavior:

```text
hook.Run(eventName, ...)
```

calls hooks associated with `eventName` until one returns non-nil, then returns that value. If no hook returns data, it may call `GAMEMODE:eventName`.

Therefore each event has possible return semantics.

---

## Event Return Policy

Some hooks are likely gates/queries:

```text
Can*
Should*
Get*
Is*
Check*
```

Examples:

```text
CanPlayerUseDoor
ShouldRadioBeep
GetDefaultInventoryType
IsPlayerRecognized
CheckBothHandsAmputation
```

These should be classified as:

```text
query_or_gate
likely_returns
```

Other hooks may be void propagation events:

```text
SaveData
LoadData
PostLoadData
StorageRestored
OnCharVarChanged
```

These should be classified as:

```text
broadcast/runtime event
maybe_returns
```

---

## Event Classes

Recommended taxonomy:

```text
plugin_callback
global_runtime_event
framework_lifecycle
domain_event
entity_signal
entity_inventory_domain
ui_extension_point
network_or_sync
query_or_gate
engine_bridge
ad_hoc_lowercase_event
player_lifecycle_or_action
```

---

## Important Event Types

### Framework Lifecycle

Examples:

```text
InitializedSchema
InitializedPlugins
InitializedItems
LoadData
PostLoadData
SaveData
PersistenceSave
PersistenceLoad
DatabaseConnected
```

Meaning:

```text
framework startup/shutdown/data lifecycle
```

---

### Query / Gate

Examples:

```text
CanPlayerUseDoor
CanPlayerInteractItem
ShouldCreateLoadingScreen
GetDefaultInventoryType
GetSalaryAmount
IsPlayerRecognized
```

Meaning:

```text
control-flow influencing event
```

These often short-circuit behavior.

---

### UI Extension Point

Examples:

```text
LoadFonts
LoadNutFonts
SetupQuickMenu
CreateNewInventoryPanel
DrawItemDescription
HUDPaint
HUDPaintBackground
```

Meaning:

```text
client/UI extension or drawing event
```

---

### Entity / Inventory Domain

Examples:

```text
StorageRestored
StorageEntityRemoved
InventoryItemRemoved
ItemTransfered
CanItemBeTransfered
OnCreateStoragePanel
```

Meaning:

```text
inventory/storage/entity state propagation
```

---

### Player Lifecycle / Action

Examples:

```text
PlayerInitialSpawn
PlayerLoadedChar
PlayerLoadout
PostPlayerLoadout
PlayerDeath
PlayerUse
KeyPress
```

Meaning:

```text
player lifecycle or interaction event
```

---

### Ad-hoc Lowercase Events

Examples:

```text
screamer2
useIhnolitOre
ihnolitOreTimer
saveStorage
```

Important rule:

```text
lowercase/weird naming does not make it invalid
```

These are still hooks/events in this codebase.

They should be classified by usage context, not naming style alone.

---

## Realm Handling

Realm inference:

```text
cl_*.lua → client
sv_*.lua → server
sh_*.lua → shared
unknown prefix → shared unless context says otherwise
```

Shared files may contain:

```lua
if SERVER then
...
end

if CLIENT then
...
end
```

Future extractors should preserve conditional realm context where possible.

---

## Graph Model

Event graph concepts:

```text
file emits hook_event
hook_event dispatches_to listener
plugin/schema/gamemode owns listener
listener runs_in_realm realm
```

Stable IDs should distinguish concepts:

```text
hook:SaveData
listener:plugin:healthproblems:SaveData
file:plugins/healthproblems/sv_hooks.lua
plugin:healthproblems
realm:server
```

---

## Important Design Rule

Do not keep adding fragile normalizer heuristics forever.

Correct loop:

```text
normalization finds ambiguity
→ improve extractor schema
→ regenerate manifests
→ rerun normalization
```
