# SIGNALIS AI — Subsystem Priorities

## Purpose

This document defines the current subsystem priority map for future architecture, profiling, UI, and retrieval work.

---

## Highest Priority Systems

Current high-priority systems:

```text
healthproblems
inventory
vendor
storage
needs
biorezonance
lightitems
mining
ragdollinteraction
nextbots
```

These systems dominate runtime topology, synchronization, or performance risk.

---

## Main Performance Concerns

Known or suspected concerns:

```text
PVP/PVE FPS drops
dynamic light cost
infrastructure entity cost
nextbot cost
UI desync
memory leaks
entity simulation overhead
network synchronization issues
```

---

## Simulation-Oriented Systems

Systems that behave like active simulation layers:

```text
healthproblems
needs
biorezonance
lightitems
mining
farming
food spoilage
smelters
generators
nextbots
players themselves
```

These require scheduler and realm-aware design.

---

## UI / Sync Sensitive Systems

Systems likely tied to UI desync or cross-realm complexity:

```text
inventory
vendor
storage
health HUD
disease UI
crafting panels
3D2D entity displays
character selection
admin/config tools
```

These should eventually receive explicit sync contracts.

---

## Entity Simulation Hotspots

Important entity simulation candidates:

```text
ore smelter
electric generator
cooking entities
oxygen station
crafting machines
farming entities
nextbots
dynamic light entities
```

Future work should classify each as:

```text
continuous simulation
nearby-player simulation
powered-only simulation
on-demand/lazy simulation
```

---

## Networking Hotspots

Likely networking-heavy systems:

```text
inventory
vendor
multichar
hud
healthproblems
gadgets
admin tools
pluginconfig
```

Known issues:

```text
large payloads
UI desync
inconsistent protocol naming
mixed legacy raw net and netstream2
```

---

## Timer / Scheduler Hotspots

Timer-heavy areas:

```text
entity production
food spoilage
health/status systems
AI/nextbots
player action timers
UI delay/interpolation
loot spawning
persistence/autosave
```

High-frequency timers are context-sensitive and should not be treated as defects without semantic classification.

---

## Architecture Goals

Future target architecture:

```text
modular
event-driven
simulation-oriented
server-authoritative
realm-explicit
sync-contract driven
observable
profilable
```

---

## Near-Term Investigation Targets

Recommended near-term diagnostics:

```text
inventory desync analysis
network protocol cleanup
timer/scheduler fanout
entity simulation lifecycle
PVP/PVE FPS profiling
dynamic light impact
nextbot topology
memory leak candidates
```

---

## Future Subsystem Docs

Recommended files:

```text
subsystem_docs/subsystems/inventory.md
subsystem_docs/subsystems/healthproblems.md
subsystem_docs/subsystems/biorezonance.md
subsystem_docs/subsystems/storage.md
subsystem_docs/subsystems/vendor.md
subsystem_docs/subsystems/needs.md
subsystem_docs/subsystems/mining.md
subsystem_docs/subsystems/lightitems.md
subsystem_docs/subsystems/nextbots.md
```

---

## Core Rule

Subsystem priority should be driven by:

```text
runtime topology
QA reports
profiling evidence
human semantic context
```

not by intuition alone.
