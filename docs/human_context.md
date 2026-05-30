# SIGNALIS AI — Human Context

## Project Reality Notes

## Current Architecture Intent

## Known Legacy / Reworked Systems

## Known Bugs and Runtime Symptoms

## Human-Confirmed Correct Behavior

## Human-Confirmed Incorrect Behavior

## Subsystem Ownership Notes

## UI / Sync Rules

## Item Data Semantics

Human-validated:

ITEM:setData(key, value, receivers, noSave, noCheckEntity) mutates server-side item data, optionally syncs the changed key/value to receivers or the current owner through netstream "invData", updates world entity netvars when an item entity exists, and persists item data to the database unless noSave is set.

Therefore item:setData is both persistent item metadata mutation and a conditional synchronization boundary.

It should not be treated as a simple local state write.

If receivers are missing or incorrect, current clients may not receive the update immediately. Future owners or clients opening/syncing the inventory may still receive the persisted data later.

## Vendor / Inventory Notes

The vendor system has been reworked. Some files under plugins/vendor are legacy and should not be assumed authoritative without validation.

Observed bug:
After buying items from a vendor, vendor price labels sometimes remain visible on items inside the player inventory.

Observed recovery:
Relog usually fixes the issue.
Moving the item through storage can also refresh/clear the incorrect display state.

Human interpretation:
This likely involves client-side item data or UI presentation state becoming stale, not necessarily server inventory ownership corruption.

Important rule:
Vendor price labels are presentation/UI metadata and should not be treated as authoritative item ownership state.

## Storage / Inventory Notes

## Performance Observations

## Refactor Intent

## Open Questions

## Human Validation Rule

When topology, doctrine, subsystem docs, and retrieval do not provide enough evidence to determine runtime behavior:

DO NOT GUESS.

Ask the project owner for:

- intended behavior
- subsystem history
- legacy vs authoritative implementation
- runtime observations
- reproduction steps
- exact Lua files involved

Human-confirmed information has higher priority than AI inference.

The preferred validation order is:

runtime topology
→ doctrine
→ subsystem docs
→ retrieval
→ targeted raw Lua
→ human validation
→ updated semantic artifacts

The goal is architecture understanding, not architecture speculation.