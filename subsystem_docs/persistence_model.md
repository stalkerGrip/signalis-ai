# SIGNALIS AI — Persistence Model

## Current Persistence Reality

Persistence is mixed.

Current persistence modes include:

```text
shutdown-only saves
periodic autosave
on-demand saves
TXT file saves
database-backed item/character saves
entity/world state saves
```

The system is not one clean persistence model yet.

---

## Known Persistence Targets

Persistence may include:

```text
characters
items
inventories
entities
storage containers
world state
plugin data
configuration
production/entity state
food spoilage state
disease/status data
```

Not all categories are equally normalized or centralized.

---

## Current Storage Backends

Known storage styles:

```text
database tables
TXT files
NutScript data helpers
plugin-specific persistence
entity-specific save/load
```

Important:

```text
items are saved in database
inventory state is server-authoritative
client views inventory through Derma/grid inventory UI
```

---

## Important Events

Persistence-related hook/event names include:

```text
SaveData
LoadData
PostLoadData
PersistenceSave
PersistenceLoad
CharacterPreSave
CharacterPostSave
OnSavedItemLoaded
ShouldDeleteSavedItems
StorageRestored
StorageEntityRemoved
```

These should be treated as persistence/runtime lifecycle events.

---

## Persistence Topology Signals

Known topology findings:

```text
SaveData has high listener fanout
LoadData has high listener fanout
core hooks participate heavily in persistence orchestration
storage/entity/inventory systems connect strongly to persistence
```

This means persistence is a major coupling hub.

---

## Risk Model

Persistence risk is currently not known to be a real bottleneck, but topology suggests it is architecturally important.

Potential risk categories:

```text
shutdown save ordering
large fanout during SaveData
plugin-specific save/load assumptions
entity restoration ordering
inventory restoration ordering
stale UI after load
partial save failure
```

No confirmed freeze bottleneck yet.

---

## Desired Direction

Persistence should become:

```text
explicit
subsystem-owned
lifecycle-aware
dependency-ordered
observable
less ad-hoc
```

Potential future architecture:

```text
central persistence service
subsystem save contracts
explicit load order
dirty-state tracking
batched saves
clear server authority
```

---

## Graph Model

Persistence-related graph nodes should include:

```text
hook:SaveData
hook:LoadData
hook:PersistenceSave
hook:PersistenceLoad
plugin:<name>
file:<path>
subsystem:persistence
entity:<class>
inventory:<id/type>
```

Useful edge concepts:

```text
emits persistence event
listens to persistence event
loads entity state
saves entity state
restores inventory
mutates persisted data
syncs loaded state to client
```

---

## Future QA Questions

Future persistence diagnostics should answer:

```text
Which plugins listen to SaveData?
Which files emit SaveData?
Which systems save on shutdown only?
Which systems save periodically?
Which systems restore entities/inventories?
Which persistence events trigger network sync?
Which persistence flows can affect UI desync?
```

---

## Important Design Principle

Do not optimize persistence before measuring.

Current goal:

```text
map persistence topology first
then identify save/load ordering and fanout risk
then decide refactor boundaries
```
