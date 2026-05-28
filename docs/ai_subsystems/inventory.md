# Inventory — AI Synthesis

## Purpose

Inventory is one of the core architectural subsystems of SIGNALIS.

Its primary purpose is not simply storing items.

Inventory acts as the central ownership, transfer, equipment, and interaction layer used by multiple gameplay systems.

Current understanding:

```text
Character
→ Inventory
→ Item
```

and

```text
Inventory
→ Equipment Slots
→ Vendor
→ Storage
→ Tying
→ Ragdoll Loot
→ Needs
```

Inventory is therefore a dependency hub rather than an isolated feature.

Confidence: High

---

## Architectural Layers

### Layer 1 — NutScript Base Inventory

Provided by:

```text
nutscript/plugins/gridinv
nutscript/gamemode/core/libs/sh_inventory.lua
nutscript/gamemode/core/libs/sv_inventory.lua
nutscript/gamemode/core/meta/sh_base_inventory.lua
```

Responsibilities:

* inventory creation
* inventory dimensions
* item placement
* transfer operations
* inventory rules
* item combine

This layer provides the actual inventory implementation.

Confidence: Medium

---

### Layer 2 — SIGNALIS Inventory Extension

Provided by:

```text
signalis/plugins/inventory
```

Responsibilities:

* equipment slots
* slot restrictions
* slot lifecycle
* stack split synchronization
* inventory UI extensions
* vendor integration
* character equipment management

This layer extends GridInv rather than replacing it.

Confidence: High

---

### Layer 3 — Inventory UI Layer

Responsibilities:

* grid rendering
* slot rendering
* item interaction
* item tooltips
* equipment visualization
* vendor visualization
* storage visualization

Important rendering functions:

```lua
getName()
getDesc()
paintOver()
```

Inventory UI state is not necessarily authoritative inventory state.

Confidence: High

---

## Ownership Model

Current synthesized model:

```text
Character
→ stores inv variable

Inventory
→ references character

Item
→ references inventory

Persistence
→ database-backed
```

Important references:

```lua
GM:CreateDefaultInventory(character)
nut.char.registerVar("inv", ...)
char:getInv()
```

Inventory ownership appears to originate from the character.

Items appear to be moved between inventories rather than duplicated.

Confidence: Medium

Needs validation:
Exact persistence ownership chain.

---

## Lifecycle Model

Current understanding:

```text
Character Creation
→ CreateDefaultInventory

Character Load
→ CharacterLoaded

Player Initialization
→ PlayerLoadedChar

Equipment Initialization
→ PlayerLoadout

Slot Population
→ PostPlayerLoadout

Persistence
→ CharacterPreSave
```

Human understanding indicates all of these occur before normal player interaction begins.

This suggests inventory synchronization problems are more likely related to delayed client initialization than early player interaction.

Confidence: Medium

Needs validation:
Exact hook ordering.

---

## Equipment Model

Equipment slots appear to be implemented as additional inventory instances.

Known slots:

* Primary Item
* Melee
* Secondary Weapon
* Primary Weapon
* Armor
* Suit
* Face
* Headgear
* Eyes

Current understanding:

```text
Main Inventory
↔ Equipment Slot Inventory
```

Items are moved between inventories.

Confidence: Medium

---

## Synchronization Model

Current understanding:

Synchronization is performed through:

```text
Inventory Rules
getData()
setData()
net
netstream
```

Inventory behavior is tightly coupled with UI behavior.

Current knowledge gap:

Full synchronization path is not yet reconstructed.

Confidence: Low

---

## Dependency Graph

Primary consumers:

```text
Vendor
Storage
Tying
RagdollInteraction
Needs
```

Observed topology confirms inventory as a major dependency hub.
Confidence: High

---

## Known Architectural Risks

### UI / State Coupling

Inventory state and inventory presentation are closely coupled.

Example:

Vendor pricing information may appear as UI metadata rather than authoritative item state.

This can create visual desynchronization without inventory corruption.

Confidence: High

---

### Synchronization Complexity

Inventory uses:

```text
Rules
Slots
Item Data
Net Messages
Netstream
```

across:

```text
Server
Shared
Client
```

This creates a large synchronization surface area.

Confidence: High

---

## Known Unknowns

Not yet fully understood:

* full inventory synchronization path
* exact lifecycle ordering
* NutScript internal inventory ownership model
* UI initialization ordering
* slot persistence implementation details

These areas require targeted source validation.

---

## Human Confidence Overlay

Strong understanding:

* SIGNALIS inventory plugin
* slot architecture
* inventory UI behavior

Weak understanding:

* NutScript internals
* framework lifecycle
* engine-level inventory behavior

Future investigations should prioritize source validation when entering these areas.

---

## Current Architecture Assessment

Inventory is not merely a storage system.

Inventory is a gameplay infrastructure subsystem.

It acts as the central coordination point for:

```text
Item Ownership
Equipment
Vendor Interaction
Storage Interaction
Loot Interaction
Character Equipment State
Inventory UI
```

Because of this, inventory should be treated as a Tier-1 subsystem during future architecture investigations.
