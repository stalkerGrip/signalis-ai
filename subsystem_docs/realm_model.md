# SIGNALIS AI — Realm Model

## Purpose

This document defines how server/client/shared execution should be interpreted in the SIGNALIS AI semantic pipeline.

The goal is to make runtime topology and future architecture reasoning realm-aware.

---

## Current Reality

The codebase is mixed-realm.

Most authoritative gameplay logic is intended to be server-side, but many systems include:

```text
shared files
client UI
server simulation
client rendering
cross-realm networking
```

---

## File-Based Realm Defaults

The normalizer should infer realm from filename prefix:

```text
cl_*.lua → client
sv_*.lua → server
sh_*.lua → shared
```

If no prefix exists:

```text
unknown prefix → shared by default
```

unless stronger evidence exists.

Examples of stronger evidence:

```lua
if SERVER then
    ...
end

if CLIENT then
    ...
end
```

Future extractors should preserve branch-level realm context where possible.

---

## Realm Responsibilities

### Server

Server should own:

```text
authoritative gameplay state
entity simulation
inventory mutation
character state
persistence
damage/status calculations
production chains
loot spawning
security-sensitive validation
```

---

### Client

Client should own:

```text
UI rendering
HUD
Derma panels
3D2D presentation
visual interpolation
input capture
local effects
```

Client should not be trusted as authoritative for gameplay state.

---

### Shared

Shared code should define:

```text
schemas
metadata
item definitions
protocol constants
utility functions
state descriptions
```

Shared files may still execute realm-specific logic in `SERVER` / `CLIENT` blocks.

---

## Networking Implication

Networking exists to cross the realm boundary.

Important netstream rule:

```text
SERVER:
netstream.Start(recipient, message, payload...)

CLIENT:
netstream.Start(message, payload...)
```

This means the same function has different argument semantics depending on realm.

Realm inference is mandatory for correct network normalization.

---

## Event Bus Implication

Hook events can exist in server, client, or shared contexts.

A hook name alone is not enough to determine runtime behavior.

Example:

```text
LoadData
HUDPaint
PlayerLoadedChar
StorageRestored
```

must be understood with:

```text
emitter realm
listener realm
file realm
plugin ownership
```

---

## Timer Implication

Timers may be:

```text
server simulation timers
client visual timers
shared utility timers
entity-local timers
player-local timers
```

High-frequency timers are acceptable when used for:

```text
animation
visual interpolation
stamina/sprint handling
short-lived UI/gameplay loops
```

High-frequency timers become suspicious when used for:

```text
persistence
network sync
large entity scans
inventory mutation
loot spawning
```

---

## Desired Future Direction

The architecture should move toward:

```text
server-authoritative simulation
explicit client presentation layer
clear protocol contracts
minimal implicit shared-side behavior
realm-aware subsystem boundaries
```

---

## Future QA Questions

Realm diagnostics should answer:

```text
Which systems mutate state clientside?
Which client UI depends on server sync?
Which shared files contain server-only logic?
Which shared files contain client-only logic?
Which network protocols cross which realm boundary?
Which timers run clientside vs serverside?
```

---

## Core Rule

Every runtime graph node should eventually be realm-aware.

If realm is uncertain, keep uncertainty explicit:

```text
realm = unknown
confidence = low
```

Do not silently assume correctness.
