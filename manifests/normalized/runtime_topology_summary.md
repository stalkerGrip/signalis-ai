# Runtime topology summary

Schema: `runtime_topology.v1`

## Inputs
- Hook/event runtime graph: **loaded** nodes=2376 edges=8263
- Network graph: **loaded** nodes=2043 edges=7042
- Timer graph: **loaded** nodes=940 edges=4854

## Totals
- Nodes: **5066**
- Edges: **19459**
- Bridge edges added: **1696**
- Hook Events: **464**
- Network Messages: **358**
- Timers: **94**
- Files: **454**
- Plugins: **95**

## Graph layers by node participation
- `hook`: **2376**
- `network`: **2043**
- `timer`: **940**

## Node types
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

## Edge types
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
- `context_references_network_message`: **160**
- `writes_network_payload`: **151**
- `reads_network_payload`: **150**
- `schedules_delay`: **132**
- `removes_timer`: **110**
- `schedules_player_action`: **102**
- `file_registers_network_message`: **66**
- `registers_network_message`: **66**
- `creates_timer`: **44**

## Top connected files
- `gamemode/core/hooks/sv_hooks.lua`: 126
- `plugins/healthproblems/sv_hooks.lua`: 96
- `plugins/ragdollinteraction/interaction/sv_hooks.lua`: 81
- `plugins/biorezonance/sh_plugin.lua`: 78
- `plugins/hacking/sh_plugin.lua`: 73
- `plugins/mnhr/sh_plugin.lua`: 66
- `plugins/mining/entities/entities/nut_ore_smelter/init.lua`: 65
- `plugins/inventory/cl_hooks.lua`: 63
- `plugins/gadgets/sv_hooks.lua`: 62
- `plugins/needs/sv_hooks.lua`: 61
- `plugins/vendor/cl_networking.lua`: 60
- `plugins/pluginconfig.lua`: 59
- `gamemode/core/hooks/cl_hooks.lua`: 54
- `plugins/recognition.lua`: 54
- `plugins/lightitems/entities/entities/nut_electric_generator/init.lua`: 54
- `plugins/area/sh_plugin.lua`: 53
- `plugins/admintools/sv_hooks.lua`: 48
- `plugins/multichar/sv_networking.lua`: 47
- `plugins/lightitems/sv_hooks.lua`: 47
- `plugins/multichar/sh_plugin.lua`: 45
- `plugins/ragdollinteraction/interaction/cl_hooks.lua`: 45
- `plugins/tying/sh_charsearch.lua`: 45
- `plugins/vendor/sv_networking.lua`: 43
- `gamemode/core/meta/inventory/sv_base_inventory.lua`: 43
- `plugins/admintools/sh_plugin.lua`: 42
- `gamemode/core/meta/inventory/cl_base_inventory.lua`: 41
- `plugins/hud/sh_plugin.lua`: 41
- `plugins/lightitems/cl_hooks.lua`: 41
- `plugins/cassetteplayer/sh_plugin.lua`: 37
- `plugins/pac/sv_parts.lua`: 36

## Top connected plugins
- `healthproblems`: 183
- `ragdollinteraction`: 133
- `lightitems`: 120
- `gamemode`: 113
- `needs`: 112
- `vendor`: 107
- `gridinv`: 99
- `biorezonance`: 89
- `entities`: 89
- `multichar`: 87
- `mining`: 75
- `tying`: 69
- `storage`: 67
- `pac`: 61
- `attributes`: 59
- `crafting`: 58
- `gadgets`: 58
- `traits`: 52
- `area`: 44
- `admintools`: 43
- `hud`: 43
- `inventory`: 37
- `mnhr`: 36
- `armor`: 32
- `hacking`: 31
- `recognition.lua`: 29
- `chatbox`: 27
- `newweapons`: 24
- `schema`: 24
- `propprotect.lua`: 23

## High-frequency timer operation candidates
- none detected

## Notes
- This merge is manifest-first and does not scan source code.
- High-frequency timers are not automatically defects; animation, sprint/stamina, and short-lived UI loops may be intentional.
- Use this topology as the first canonical graph for Qdrant ingestion and external architect reasoning.
