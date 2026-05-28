# Runtime Path Reconstruction

From: `CharacterLoaded`
To: `inventorySetPanelStatus`

## Resolved Start Nodes

- `CharacterLoaded` (hook_event)
- `listen CharacterLoaded @ gamemode\core\hooks\sv_hooks.lua:221` (hook_listener) — file=gamemode\core\hooks\sv_hooks.lua, realm=server
- `listen CharacterLoaded @ plugins\logging.lua:144` (hook_listener) — file=plugins\logging.lua, realm=shared
- `listen CharacterLoaded @ schema\hooks\cl_hooks.lua:121` (hook_listener) — file=schema\hooks\cl_hooks.lua, realm=client
- `listen CharacterLoaded @ plugins\logging.lua:145` (hook_listener) — file=plugins\logging.lua, realm=shared
- `emit CharacterLoaded @ plugins\multichar\sh_plugin.lua:41` (hook_emitter) — file=plugins\multichar\sh_plugin.lua, realm=shared
- `emit CharacterLoaded @ gamemode\core\meta\sh_character.lua:129` (hook_emitter) — file=gamemode\core\meta\sh_character.lua, realm=shared
- `workbenchInvOpen` (network_message)
- `workbenchInvClose` (network_message)
- `waterfaucetWash` (network_message)

## Resolved Target Nodes

- `inventorySetPanelStatus` (network_message)
- `netstream send inventorySetPanelStatus` (network_operation)
- `netstream send inventorySetPanelStatus` (network_operation)
- `netstream send inventorySetPanelStatus` (network_operation)
- `netstream send inventorySetPanelStatus` (network_operation)
- `netstream send inventorySetPanelStatus` (network_operation)
- `netstream send inventorySetPanelStatus` (network_operation)
- `netstream send inventorySetPanelStatus` (network_operation)
- `netstream send inventorySetPanelStatus` (network_operation)
- `netstream send inventorySetPanelStatus` (network_operation)

## Candidate Paths

### Path 1

1. `listen CharacterLoaded @ gamemode\core\hooks\sv_hooks.lua:221` (hook_listener) — file=gamemode\core\hooks\sv_hooks.lua, realm=server
2. via `reverse:contains_listener` → `gamemode\core\hooks\sv_hooks.lua` (file) — file=gamemode\core\hooks\sv_hooks.lua, realm=server
3. via `file_receives_network_message` → `vManipDoorAnimation` (network_message)

### Path 2

1. `listen CharacterLoaded @ gamemode\core\hooks\sv_hooks.lua:221` (hook_listener) — file=gamemode\core\hooks\sv_hooks.lua, realm=server
2. via `reverse:contains_listener` → `gamemode\core\hooks\sv_hooks.lua` (file) — file=gamemode\core\hooks\sv_hooks.lua, realm=server
3. via `file_sends_network_message` → `vManipShowHands` (network_message)

### Path 3

1. `listen CharacterLoaded @ schema\hooks\cl_hooks.lua:121` (hook_listener) — file=schema\hooks\cl_hooks.lua, realm=client
2. via `reverse:contains_listener` → `schema\hooks\cl_hooks.lua` (file) — file=schema\hooks\cl_hooks.lua, realm=client
3. via `file_receives_network_message` → `voicePlay` (network_message)

### Path 4

1. `waterfaucetWash` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\needs\sv_hooks.lua` (file) — file=plugins\needs\sv_hooks.lua, realm=server
3. via `file_receives_network_message` → `waterfaucetDrawWater` (network_message)

### Path 5

1. `waterfaucetWash` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\needs\sv_hooks.lua` (file) — file=plugins\needs\sv_hooks.lua, realm=server
3. via `file_receives_network_message` → `waterfaucetDrinkWater` (network_message)

### Path 6

1. `waterfaucetWash` (network_message)
2. via `reverse:file_sends_network_message` → `plugins\needs\derma\cl_waterfaucet_interface.lua` (file)
3. via `file_sends_network_message` → `waterfaucetDrawWater` (network_message)

### Path 7

1. `waterfaucetWash` (network_message)
2. via `reverse:file_sends_network_message` → `plugins\needs\derma\cl_waterfaucet_interface.lua` (file)
3. via `file_sends_network_message` → `waterfaucetDrinkWater` (network_message)

### Path 8

1. `waterfaucetDrinkWater` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\needs\sv_hooks.lua` (file) — file=plugins\needs\sv_hooks.lua, realm=server
3. via `file_receives_network_message` → `waterfaucetDrawWater` (network_message)

### Path 9

1. `waterfaucetDrinkWater` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\needs\sv_hooks.lua` (file) — file=plugins\needs\sv_hooks.lua, realm=server
3. via `file_receives_network_message` → `waterfaucetWash` (network_message)

### Path 10

1. `waterfaucetDrinkWater` (network_message)
2. via `reverse:file_sends_network_message` → `plugins\needs\derma\cl_waterfaucet_interface.lua` (file)
3. via `file_sends_network_message` → `waterfaucetDrawWater` (network_message)

### Path 11

1. `waterfaucetDrinkWater` (network_message)
2. via `reverse:file_sends_network_message` → `plugins\needs\derma\cl_waterfaucet_interface.lua` (file)
3. via `file_sends_network_message` → `waterfaucetWash` (network_message)

### Path 12

1. `waterfaucetDrawWater` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\needs\sv_hooks.lua` (file) — file=plugins\needs\sv_hooks.lua, realm=server
3. via `file_receives_network_message` → `waterfaucetDrinkWater` (network_message)

### Path 13

1. `waterfaucetDrawWater` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\needs\sv_hooks.lua` (file) — file=plugins\needs\sv_hooks.lua, realm=server
3. via `file_receives_network_message` → `waterfaucetWash` (network_message)

### Path 14

1. `waterfaucetDrawWater` (network_message)
2. via `reverse:file_sends_network_message` → `plugins\needs\derma\cl_waterfaucet_interface.lua` (file)
3. via `file_sends_network_message` → `waterfaucetDrinkWater` (network_message)

### Path 15

1. `waterfaucetDrawWater` (network_message)
2. via `reverse:file_sends_network_message` → `plugins\needs\derma\cl_waterfaucet_interface.lua` (file)
3. via `file_sends_network_message` → `waterfaucetWash` (network_message)

### Path 16

1. `vendorTradeInterface` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
3. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 17

1. `vendorTradeInterface` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
3. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 18

1. `vendorTradeInterface` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
3. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 19

1. `vendorTradeInterface` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
3. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 20

1. `vendorTradeInterface` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
3. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

## Notes

- This is topology-only path reconstruction.
- Paths are candidate runtime relationships, not guaranteed chronological execution order.
- Use raw Lua only to validate exact ordering and control flow.
