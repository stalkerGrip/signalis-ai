# Subsystem: nextbots

## Purpose

Deterministic subsystem summary generated from runtime topology.

## Topology Summary

- Nodes: **5**
- Edges: **18**

## Node Types

- `hook_event`: 2
- `hook_listener`: 2
- `hook_owner`: 1

## Edge Types

- `listens_to`: 4
- `listens_to_event`: 4
- `runs_in_realm`: 4
- `classified_as`: 2
- `contains_listener`: 2
- `registers_listener`: 2

## Major Hooks

- `PhysgunDrop`: 1
- `OnPhysgunPickup`: 1
- `listen OnPhysgunPickup @ entities\entities\sb_advanced_nextbot_base\motion.lua:1396`: 1
- `listen PhysgunDrop @ entities\entities\sb_advanced_nextbot_base\motion.lua:1403`: 1

## Major Network Signals

- none detected

## Lifecycle Propagation

- none detected

## Synchronization Hotspots

- none detected

## Important Timers

- none detected

## Realms

- `shared`: 2

## Major Files

- `entities\entities\sb_advanced_nextbot_base\motion.lua`: 2

## Connected Plugins / Subsystems

- none detected

## Runtime Propagation Hubs

- degree `5` | `hook_listener` | `listen PhysgunDrop @ entities\entities\sb_advanced_nextbot_base\motion.lua:1403` | `listener:listener_a85399e4dcc0`
- degree `5` | `hook_listener` | `listen OnPhysgunPickup @ entities\entities\sb_advanced_nextbot_base\motion.lua:1396` | `listener:listener_c4e821cd52af`
- degree `5` | `hook_event` | `PhysgunDrop` | `hook:PhysgunDrop`
- degree `5` | `hook_event` | `OnPhysgunPickup` | `hook:OnPhysgunPickup`

## Topology Hubs

- degree `5` | `hook_listener` | `listen PhysgunDrop @ entities\entities\sb_advanced_nextbot_base\motion.lua:1403` | `listener:listener_a85399e4dcc0`
- degree `5` | `hook_listener` | `listen OnPhysgunPickup @ entities\entities\sb_advanced_nextbot_base\motion.lua:1396` | `listener:listener_c4e821cd52af`
- degree `5` | `hook_event` | `PhysgunDrop` | `hook:PhysgunDrop`
- degree `5` | `hook_event` | `OnPhysgunPickup` | `hook:OnPhysgunPickup`
- degree `4` | `hook_owner` | `SBAdvancedNextBots` | `hook_owner:SBAdvancedNextBots`

## Runtime Risks

- Review high-degree hubs for hidden coupling.
- Review network signals for synchronization ownership.
- Review timers for scheduler or debounce behavior.
- Review realm crossings for client/server authority issues.

## Notes

This document is generated from topology only. Use raw Lua only for exact validation.
