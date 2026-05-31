# Runtime Propagation Topology Summary

Schema: `runtime_propagation_topology.v1`

## Totals

- Nodes: **5066**
- Edges: **9407**
- Copied propagation edges: **4202**
- Generated propagation edges: **5205**

## Edge Types

- `listener_exits_to_owner`: **1991**
- `hook_event_dispatches_to_listener`: **1595**
- `dispatches_to`: **1041**
- `network_operation_exits_to_owner`: **955**
- `network_message_dispatches_to_receiver`: **664**
- `references_timer`: **607**
- `sends_network_message`: **552**
- `emits`: **495**
- `network_dispatches_to`: **423**
- `file_sends_network_message`: **422**
- `schedules_entity_action`: **207**
- `emits_event`: **177**
- `schedules_delay`: **132**
- `schedules_player_action`: **102**
- `creates_timer`: **44**

## Node Types

- `hook_listener`: **999**
- `network_operation`: **955**
- `timer_operation`: **607**
- `hook_emitter`: **495**
- `hook_event`: **464**
- `file`: **454**
- `network_message`: **358**
- `network_payload_operation`: **301**
- `network_context`: **160**
- `plugin`: **95**
- `timer`: **94**
- `hook_owner`: **42**
- `subsystem`: **13**
- `timer_class`: **10**
- `event_class`: **9**
- `timer_risk`: **5**
- `realm`: **3**
- `gamemode`: **1**
- `schema`: **1**

## Purpose

This artifact transforms the relationship-oriented runtime topology into a traversal-oriented propagation topology.

Primary generated propagation rules:

- `listener -> hook_event` relationships become `hook_event -> listener` fanout edges.
- `receiver -> network_message` relationships become `network_message -> receiver` dispatch edges.
- Existing deterministic propagation edges are preserved.
