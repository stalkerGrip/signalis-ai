# Runtime Path Reconstruction V2

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

- Path score: `1.950`

1. `vendorTradeInterface` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
3. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 2

- Path score: `1.950`

1. `vendorTradeInterface` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
3. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 3

- Path score: `1.950`

1. `vendorTradeInterface` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
3. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 4

- Path score: `1.950`

1. `vendorTradeInterface` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
3. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 5

- Path score: `1.950`

1. `vendorTradeInterface` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
3. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 6

- Path score: `2.050`

1. `vendorTradeInterface` (network_message)
2. via `reverse:file_receives_network_message` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
3. via `file_sends_network_message` → `inventorySetPanelStatus` (network_message)

### Path 7

- Path score: `2.550`

1. `vendorTradeInterface` (network_message)
2. via `reverse:receives_network_message` → `netstream hook vendorTradeInterface` (network_operation)
3. via `reverse:contains_network_operation` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
4. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 8

- Path score: `2.550`

1. `vendorTradeInterface` (network_message)
2. via `reverse:receives_network_message` → `netstream hook vendorTradeInterface` (network_operation)
3. via `reverse:contains_network_operation` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
4. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 9

- Path score: `2.550`

1. `vendorTradeInterface` (network_message)
2. via `reverse:receives_network_message` → `netstream hook vendorTradeInterface` (network_operation)
3. via `reverse:contains_network_operation` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
4. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 10

- Path score: `2.550`

1. `vendorTradeInterface` (network_message)
2. via `reverse:receives_network_message` → `netstream hook vendorTradeInterface` (network_operation)
3. via `reverse:contains_network_operation` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
4. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 11

- Path score: `2.550`

1. `vendorTradeInterface` (network_message)
2. via `reverse:receives_network_message` → `netstream hook vendorTradeInterface` (network_operation)
3. via `reverse:contains_network_operation` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
4. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 12

- Path score: `2.650`

1. `vendorTradeInterface` (network_message)
2. via `reverse:receives_network_message` → `netstream hook vendorTradeInterface` (network_operation)
3. via `reverse:contains_network_operation` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
4. via `file_sends_network_message` → `inventorySetPanelStatus` (network_message)

### Path 13

- Path score: `2.700`

1. `vendorTradeInterface` (network_message)
2. via `reverse:sends_network_message` → `netstream send vendorTradeInterface` (network_operation)
3. via `network_dispatches_to` → `netstream hook vendorTradeInterface` (network_operation)
4. via `reverse:contains_network_operation` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
5. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 14

- Path score: `2.700`

1. `vendorTradeInterface` (network_message)
2. via `reverse:sends_network_message` → `netstream send vendorTradeInterface` (network_operation)
3. via `network_dispatches_to` → `netstream hook vendorTradeInterface` (network_operation)
4. via `reverse:contains_network_operation` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
5. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 15

- Path score: `2.700`

1. `vendorTradeInterface` (network_message)
2. via `reverse:sends_network_message` → `netstream send vendorTradeInterface` (network_operation)
3. via `network_dispatches_to` → `netstream hook vendorTradeInterface` (network_operation)
4. via `reverse:contains_network_operation` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
5. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 16

- Path score: `2.700`

1. `vendorTradeInterface` (network_message)
2. via `reverse:sends_network_message` → `netstream send vendorTradeInterface` (network_operation)
3. via `network_dispatches_to` → `netstream hook vendorTradeInterface` (network_operation)
4. via `reverse:contains_network_operation` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
5. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 17

- Path score: `2.700`

1. `vendorTradeInterface` (network_message)
2. via `reverse:sends_network_message` → `netstream send vendorTradeInterface` (network_operation)
3. via `network_dispatches_to` → `netstream hook vendorTradeInterface` (network_operation)
4. via `reverse:contains_network_operation` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
5. via `contains_network_operation` → `netstream send inventorySetPanelStatus` (network_operation)

### Path 18

- Path score: `2.800`

1. `vendorTradeInterface` (network_message)
2. via `reverse:sends_network_message` → `netstream send vendorTradeInterface` (network_operation)
3. via `network_dispatches_to` → `netstream hook vendorTradeInterface` (network_operation)
4. via `reverse:contains_network_operation` → `plugins\inventory\cl_hooks.lua` (file) — file=plugins\inventory\cl_hooks.lua, realm=client
5. via `file_sends_network_message` → `inventorySetPanelStatus` (network_message)

### Path 19

- Path score: `3.800`

1. `listen CharacterLoaded @ schema\hooks\cl_hooks.lua:121` (hook_listener) — file=schema\hooks\cl_hooks.lua, realm=client
2. via `reverse:contains_listener` → `schema\hooks\cl_hooks.lua` (file) — file=schema\hooks\cl_hooks.lua, realm=client
3. via `file_receives_network_message` → `voicePlay` (network_message)

### Path 20

- Path score: `3.850`

1. `emit CharacterLoaded @ plugins\multichar\sh_plugin.lua:41` (hook_emitter) — file=plugins\multichar\sh_plugin.lua, realm=shared
2. via `dispatches_to` → `listen CharacterLoaded @ schema\hooks\cl_hooks.lua:121` (hook_listener) — file=schema\hooks\cl_hooks.lua, realm=client
3. via `reverse:contains_listener` → `schema\hooks\cl_hooks.lua` (file) — file=schema\hooks\cl_hooks.lua, realm=client
4. via `file_receives_network_message` → `voicePlay` (network_message)

## Notes

- V2 uses weighted topology traversal.
- Lower path score means stronger candidate.
- This is still topology-only, not chronological proof.
- Use raw Lua only after a meaningful candidate path is found.
