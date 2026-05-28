# Signalis Runtime Doctrine

Project: **Signalis AI Orchestration Pipeline**  
Phase: **Normalization / Runtime Topology V1**

## Purpose

This doctrine describes the intended semantic model for the Signalis Garry's Mod / NutScript framework. It is used to guide normalization, runtime graph classification, Qdrant embedding, and future architecture reasoning.

The project goal is not to let AI infer architecture from raw code blindly. The goal is to build deterministic semantic infrastructure:

```text
raw extraction → semantic normalization → runtime graphs → embeddings/Qdrant → architecture reasoning
```

## Core Architectural Direction

The desired architecture is:

```text
simulation-oriented
server-authoritative
event-driven
modular by subsystem
explicit about realm responsibility
stable in sync behavior
less ad-hoc in networking
less hidden in timers / Think hooks
```

Current code is considered messy but recoverable. The objective is to turn the existing framework into something more modular, reliable, and understandable without rewriting blindly.

## Runtime Model

Signalis behaves less like a simple request/response roleplay schema and more like a simulation runtime.

Important runtime systems include:

- smelters and ore processing
- generators and infrastructure entities
- farming systems
- food spoilage and cooking systems
- disease / health status processing
- HUD and status UI updates
- nextbot / AI systems
- players as active runtime entities

Runtime behavior is mixed:

- some systems run continuously,
- some run on timers,
- some run through hooks,
- some run through entity logic,
- some are delayed or event-driven,
- some are UI-driven from client interaction.

## Entity Simulation Doctrine

Active simulation entities include at least:

```text
smelters
generators
farming entities
nextbots
players
food/cooking entities
infrastructure machines
```

Simulation mode is currently mixed:

```text
continuous simulation
on-demand simulation
power/state-dependent simulation
timer-driven simulation
Think-driven simulation
network/UI-driven interaction
```

Future architecture should make this more explicit.

Recommended semantic classifications:

```text
entity_simulation
production_cycle
spoilage_cycle
spawn_cycle
ai_tick
player_status_tick
infrastructure_tick
ui_visual_update
```

Entity state is also mixed:

```text
server authoritative
partially replicated
partially client visualized
sometimes UI-derived
```

Long-term direction should prefer:

```text
server-authoritative simulation
explicit replication boundaries
client-only visual presentation
```

## Hook/Event Bus Doctrine

`hook.Run(...)` should be modeled as event dispatch, not as a direct plugin callback.

Listeners include:

```text
PLUGIN:SomeHook(...)
SCHEMA:SomeHook(...)
GM:SomeHook(...)
hook.Add("SomeHook", id, fn)
```

NutScript automatically registers plugin/schema methods as hook listeners during plugin loading:

```lua
for k, v in pairs(PLUGIN) do
    if (type(v) == "function") then
        hook.Add(k, PLUGIN, v)
    end
end
```

Therefore:

```text
PLUGIN:X → listener for hook event X
SCHEMA:X → listener for hook event X
GM:X     → gamemode fallback / listener behavior
```

Hook names may be lowercase or oddly named. They are still valid runtime events.

Return behavior is event-specific:

```text
Can*/Should*/Get*/Is*/Check* → likely returns and may gate control flow
other hooks                 → may return or may be void
```

## Networking Doctrine

Preferred current abstraction:

```text
netstream2 / netstream.Start
```

Raw `net.Start` is mostly legacy or base NutScript/framework infrastructure.

Network architecture is mixed:

```text
RPC
request/response
state replication
UI opening/sync
entity interaction
ad-hoc messages
```

Current pain points include:

```text
large payloads
UI desync
inconsistent protocol naming
possible duplicated broadcasts
unclear sync ownership
```

Desired direction:

```text
more reliable sync infrastructure
less ad-hoc netstream usage
clearer protocol naming
better batching/delta sync where needed
less UI desync
less FPS/network pressure
```

### Netstream Argument Doctrine

Realm-specific `netstream.Start` layouts:

```text
server realm:
  netstream.Start(recipient, message, payload...)

client realm:
  netstream.Start(message, payload...)
```

Therefore, symbols like:

```text
self
client
receiver
receivers
targets
activator
ply
v
```

are often recipients, not message IDs, especially in server realm.

### Raw GMod Net Doctrine

Raw GMod `net.Start` uses:

```text
net.Start(messageName, unreliable?)
```

Raw net messages should be registered server-side with:

```text
util.AddNetworkString(messageName)
```

Raw net messages also have a practical message size limit, so large payloads should be treated as a risk area.

## Timer / Scheduler Doctrine

Timers are a major hidden runtime scheduler layer.

Timer usage is mixed:

```text
scheduler
polling loop
delayed callback
debounce
async simulation
gameplay tick
visual interpolation
```

Timer names are often not semantically meaningful by themselves. They may just reflect local variable names.

Dynamic timer names are common and often intentional:

```lua
"timer_" .. ent:EntIndex()
"timer_" .. ply:SteamID()
```

Dynamic timer names should not automatically be treated as bad. They often mean:

```text
dynamic_per_entity_timer
dynamic_per_player_timer
runtime_scoped_timer
```

### High-Frequency Timer Doctrine

High-frequency or infinite timers are context-sensitive.

They are acceptable when used for:

```text
animation loops
smooth visual interpolation
client-only UI animation
short-lived minigames
stamina/sprint gameplay tick
local visual effects
```

They are suspicious when used for:

```text
persistence
loot spawning
inventory mutation
network sync
large entity scans
world scans
unbounded production loops
```

Timer risk classification should therefore be semantic, not based only on delay.

Recommended timer intent classes:

```text
animation_loop
visual_interpolation
gameplay_tick
stamina_tick
entity_simulation
production_cycle
spoilage_cycle
spawn_cycle
persistence_cycle
ui_delay
network_sync_delay
unknown
```

## Persistence Doctrine

Persistence is mixed and currently includes:

```text
txt file persistence
database persistence
one-time save
on-demand save
shutdown save
periodic autosave in some areas
```

Persistence is mostly shutdown-oriented, with some on-demand/runtime save behavior.

Known major bottlenecks are not confirmed yet.

`SaveData`, `LoadData`, `PersistenceSave`, and related hooks should be treated as high-importance lifecycle hubs.

Future architecture should clarify:

```text
what saves when
what is authoritative
what can be async
what must be atomic
what can be rebuilt from runtime state
```

## Inventory Doctrine

Inventory is both server-side authoritative and client-visible through Derma/grid inventory.

Current behavior:

```text
items saved in DB
server stores authoritative information
client views/manipulates through UI
grid inventory / Derma represents state visually
```

Known pain point:

```text
UI desync
```

Inventory sync may be mixed between full refresh and partial/delta updates. This needs further inspection.

Inventory is a high-priority subsystem because it connects:

```text
items
storage
entities
networking
UI
persistence
commands
player actions
```

## Realm Doctrine

Realm responsibility is currently mixed but mostly server-side.

Long-term direction:

```text
server owns authoritative simulation and persistence
client owns presentation and UI
shared code should express contracts, not hide authority
networking should explicitly cross realm boundaries
```

Client prediction is not currently well understood or intentionally used. Future architecture should avoid relying on prediction until the model is clear.

Plugin realm roles vary:

```text
UI-only
simulation-only
infrastructure
mixed client/server
legacy/base framework
```

## Performance Doctrine

Current high-priority risk areas:

```text
PVP/PVE performance
dynamic lights
infrastructure entities
nextbots
correct architecture implementation
memory leaks
UI desync
FPS drops with entities
```

Likely performance sources to investigate:

```text
Think hooks
high-frequency timers
entity simulation loops
nextbot processing
dynamic lighting
network sync spam
large payloads
UI refresh loops
memory leaks from timers/entities/panels
```

High-frequency logic should be classified by intent before optimization.

## Runtime Graph Doctrine

Runtime topology should be built from normalized semantic facts, not raw code dumps.

Stable graph IDs should distinguish semantic node types:

```text
hook:SaveData
net:invAct
timer:nutSaveData
plugin:healthproblems
file:plugins/healthproblems/sv_hooks.lua
entity:nut_ore_smelter
command:chargetup
```

File-level edges are useful and should be preserved:

```text
file emits hook
file listens to hook
file sends network message
file receives network message
file creates timer
plugin owns file
```

These allow detection of:

```text
hot files
god files
cross-plugin coupling
runtime propagation chains
isolated protocols
legacy/dead paths
scheduler hotspots
```

## Current Normalized Graph Layers

The current pipeline has produced or is producing:

```text
hook event bus graph
network graph
timer graph
runtime graph V1
```

The next major artifact should be a unified runtime topology graph merging:

```text
hooks
networking
timers
commands
inventory
entities
persistence
UI
```

Initial merge should focus on:

```text
hook graph
network graph
timer graph
```

because those are the runtime propagation backbone.

## Future Architectural Goals

The long-term architecture should become:

```text
modular
simulation-oriented
event-driven
server-authoritative
clear about realm ownership
clear about network protocols
clear about timer/scheduler ownership
less prone to UI desync
less prone to FPS drops
less prone to memory leaks
```

The system should support architecture reasoning over semantic manifests, not raw code.

