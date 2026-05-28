# Inventory — Human Knowledge

## Overview

Inventory is a two-layer system:

### NutScript Base Layer

Location:

* nutscript/plugins/gridinv
* nutscript/gamemode/core/meta/sh_base_inventory.lua
* nutscript/gamemode/core/libs/sh_inventory.lua
* nutscript/gamemode/core/libs/sv_inventory.lua

Responsible for:

* item storage
* coordinates
* inventory dimensions
* transfer operations
* item combine
* inventory rules

Known functions:

* GridInv:add(...)
* GridInv:canItemFitInInventory(...)
* GridInv:setSize(...)
* net.Start("nutTransferItem")

Human confidence: Medium

---

### SIGNALIS Inventory Layer

Location:

* signalis/plugins/inventory

Extends GridInv.

Responsible for:

* equipment slots
* slot restrictions
* slot initialization
* stack split synchronization
* inventory UI extensions
* vendor interaction support

Human confidence: High

---

## Ownership Model

Current understanding:

Character
→ inv var
→ Inventory
→ Items
→ Database

Main references:

* GM:CreateDefaultInventory(character)
* nut.char.registerVar("inv", ...)
* char:getInv()

Inventory links to character.

Items link to inventory.

Everything is ultimately persisted in DB.

Human confidence: Medium

---

## Equipment Slots

Current slots:

* primary item
* melee
* secondary weapon
* primary weapon
* armor
* suit
* face
* headgear
* eyes

Lifecycle:

PlayerLoadout
→ create slot inventories

PostPlayerLoadout
→ initialize slot items

CharacterPreSave
→ save slot state

Human confidence: High

---

## UI Layer

Base GridInv provides:

* grid panels
* item rendering
* drag/drop

SIGNALIS extends:

* slot rendering
* character model preview
* bodygroups
* skin updates
* quick transfer
* stack splitting
* target inventory view
* vendor inventory view

Item presentation uses:

* getName()
* getDesc()
* paintOver()

Important:

UI state is not necessarily authoritative inventory state.

Human confidence: High

---

## Synchronization

Current understanding:

Rules are applied before inventory UI opens.

Item data is synchronized through:

* getData()
* setData()
* net
* netstream

Known gap:

I do not fully understand the complete synchronization flow.

Human confidence: Low

---

## Dependencies

Inventory depends on:

* GridInv
* Vendor
* Storage
* Needs

Inventory interacts with:

* Tying
* RagdollInteraction

Human confidence: High

---

## Known Bugs

### Vendor Price Overlay

Symptoms:

Vendor prices remain visible in inventory/storage.

Recovery:

* relog
* storage transfer

Current understanding:

Likely stale UI metadata.

Confidence: Medium

---

## Known Unknowns

I do not fully understand:

* complete NutScript inventory internals
* full synchronization path
* full UI ownership chain
* some framework-level behavior

These areas require source validation.

---

## Cursed Areas

Not inventory itself.

Main uncertainty comes from:

* NutScript internals
* Facepunch/GMod engine behavior

I understand SIGNALIS plugins significantly better than framework internals.

---

## Performance Notes

Inventory itself is not currently my primary performance concern.

Primary concerns:

1. PVP/PVE FPS drops
2. Dynamic lighting

Previous attempts to solve dynamic lighting through AI-generated visible-area illumination logic were unsuccessful.

This became one of the motivations for building SIGNALIS AI.

---

## Open Questions

* Full inventory synchronization path
* Exact authoritative ownership chain
* Exact character load lifecycle ordering
* UI initialization lifecycle
