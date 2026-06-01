# Runtime Propagation Doctrine

Purpose:

Runtime topology relationships are not runtime propagation.

Examples:

hook_event
→ listener

is relationship evidence.

Actual runtime propagation may be:

hook_event
→ listener
→ body mutation
→ emitted hook_event
→ listener
→ network message
→ receiver
→ state mutation

## Propagation Types

hook_event
→ listener

listener
→ helper_call

listener
→ state_mutation

listener
→ network_send

listener
→ emitted_hook

network_message
→ receiver

receiver
→ state_mutation

receiver
→ emitted_hook

timer
→ callback

callback
→ state_mutation

callback
→ emitted_hook

callback
→ network_send

## Human-Validated Examples

netstream:invData
→ receiver callback
→ ItemDataChanged

PlayerLoadedChar
→ GM:PlayerLoadedChar
→ PlayerLoadout
→ GM:PlayerLoadout
→ PostPlayerLoadout

## Investigation Goal

Runtime chains should reconstruct propagation.

Not ownership.

Not file containment.

Not relationship counts.

Propagation topology is traversal-oriented.