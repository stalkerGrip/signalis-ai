# SIGNALIS AI — Event Taxonomy

This is information for informational purposes only; you cannot build generic scripts based on this knowledge.

NutScript 1.2 derived framework
messy legacy-heavy codebase
do not assume clean architecture
runtime propagation priority
realm transitions

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

## Networking Doctrine

Preferred abstraction:

* netstream2

Legacy:

* net.Start
* net.Receive

Networking represents:

* synchronization
* replication
* realm crossing
* UI updates

Not all networking is RPC.

### netstream2 Semantics

Important project rule:
Dynamic/symbolic messages are allowed in the codebase.

Examples:

```lua
netstream.Start(client, hookName, ...)
netstream.Start(client, callbackHook, ...)
```

However, many previously “dynamic” values were actually recipient variables misread as messages.

#### Server realm

```lua
netstream.Start(recipient, message, payload...)
```

Examples:

```lua
netstream.Start(client, "inventoryOpen", data)
netstream.Start(receivers, "hudAddStatusIcon", status)
```

#### Client realm

```lua
netstream.Start(message, payload...)
```

Example:

```lua
netstream.Start("invAct", index, entity)
```

Reason:

```text
client sends to server implicitly as LocalPlayer()
```

### Raw GMod net Semantics

Raw net model:

```lua
net.Start(messageName, unreliable?)
net.Write*
net.Send(...)
```

Receiver:

```lua
net.Receive(messageName, function(len, ply)
    ...
end)
```

Server-side registration:

```lua
util.AddNetworkString(messageName)
```

Raw GMod net messages should generally have `util.AddNetworkString` on server before use.

## Timer Doctrine

Timers are scheduler/runtime propagation layers.

High-frequency timers are not automatically defects.

Acceptable:

* animation
* interpolation
* UI behavior
* stamina/sprint

Suspicious:

* persistence
* inventory mutation
* heavy networking
* large scans

Classify timer intent before judging.

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

Server owns:

* gameplay state
* inventory mutation
* persistence
* simulation
* authority

Client owns:

* UI rendering
* HUD
* Derma panels
* 3D2D presentation
* visual interpolation
* input capture
* local effects

Shared code should define:

text
* schemas
* metadata
* item definitions
* protocol constants
* utility functions
* state descriptions

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