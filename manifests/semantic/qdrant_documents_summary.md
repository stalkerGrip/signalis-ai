# Qdrant document generation summary

Schema: `qdrant_documents.v1`

## Inputs
- Runtime topology nodes: **5066**
- Runtime topology edges: **19459**

## Documents
- Total documents: **1079**

## Document types
- `runtime_node`: **900**
- `plugin_topology`: **95**
- `file_topology`: **80**
- `doctrine`: **4**

## Top node types
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

## Top edge types
- `runs_in_realm`: **4470**
- `classified_as`: **1071**
- `dispatches_to`: **1041**
- `contains_listener`: **999**
- `listens_to`: **999**
- `registers_listener`: **992**
- `contains_network_operation`: **955**
- `belongs_to_subsystem`: **607**
- `contains_timer_operation`: **607**
- `owns_timer_operation`: **607**
- `references_timer`: **607**
- `owns_file`: **600**
- `listens_to_event`: **596**
- `file_sends_network_message`: **552**
- `sends_network_message`: **552**
- `contains_emitter`: **495**
- `emits`: **495**
- `network_dispatches_to`: **423**
- `file_receives_network_message`: **337**
- `receives_network_message`: **337**
- `contains_network_payload_operation`: **301**
- `has_timer_risk`: **291**
- `schedules_entity_action`: **207**
- `emits_event`: **177**
- `contains_network_context`: **160**

## Notes
- This step prepares semantic text documents only; it does not call an embedding model or Qdrant.
- Raw Lua should remain a secondary retrieval layer; these documents are the primary architecture-reasoning layer.
- Use metadata fields such as `doc_type`, `node_type`, `plugin`, `subsystem`, `file`, and `degree` for filtered retrieval.
