# Subsystem: inventory

## Purpose

Deterministic subsystem summary generated from runtime topology.

## Topology Summary

- Nodes: **443**
- Edges: **7885**

## Node Types

- `hook_event`: 97
- `network_operation`: 83
- `hook_listener`: 62
- `hook_emitter`: 44
- `network_payload_operation`: 39
- `file`: 37
- `network_message`: 34
- `network_context`: 13
- `plugin`: 12
- `timer_operation`: 9
- `realm`: 3
- `event_class`: 3
- `timer`: 2
- `timer_class`: 2
- `subsystem`: 1
- `gamemode`: 1
- `timer_risk`: 1

## Edge Types

- `runs_in_realm`: 4470
- `classified_as`: 577
- `registers_listener`: 331
- `listens_to_event`: 261
- `listens_to`: 198
- `contains_listener`: 192
- `owns_timer_operation`: 191
- `owns_file`: 188
- `has_timer_risk`: 182
- `contains_network_operation`: 177
- `dispatches_to`: 129
- `emits`: 104
- `file_sends_network_message`: 101
- `contains_timer_operation`: 99
- `contains_emitter`: 96
- `emits_event`: 80
- `file_receives_network_message`: 71
- `contains_network_payload_operation`: 67
- `references_timer`: 64
- `sends_network_message`: 47

## Major Hooks

- `listen CreateInventoryPanel @ plugins\gridinv\plugins\gridinvui\sh_plugin.lua:8`: 2
- `listen ItemDraggedOutOfInventory @ plugins\gridinv\sh_plugin.lua:33`: 2
- `listen CreateInventoryPanel @ plugins\_disabled\simpleinv\plugins\listinvui\sh_plugin.lua:8`: 2
- `listen ns1SetupInventorySearch @ plugins\tying\sh_charsearch.lua:4`: 2
- `listen DisplayInventoryNut1_1_beta @ plugins\ragdollinteraction\interaction\cl_hooks.lua:83`: 2
- `listen DisplayInventoryNut1_1 @ plugins\ragdollinteraction\interaction\cl_hooks.lua:152`: 2
- `VendorItemStockUpdated`: 1
- `OnTakeShipmentItem`: 1
- `name`: 1
- `listen TransferInventory @ plugins\ragdollinteraction\interaction\sv_hooks.lua:144`: 1
- `emit CreateNewInventoryPanel @ plugins\ragdollinteraction\interaction\cl_hooks.lua:90`: 1
- `ItemShouldSave`: 1
- `OnRequestItemTransfer`: 1
- `listen SetupBagInventoryAccessRules @ plugins\gridinv\sv_access_rules.lua:54`: 1
- `InventoryItemAdded`: 1
- `PlayerCanPickupWeapon`: 1
- `emit InventoryItemRemoved @ gamemode\core\libs\item\cl_networking.lua:75`: 1
- `exitStorage`: 1
- `ItemDataChanged`: 1
- `emit PlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:263`: 1

## Major Network Signals

- `netstream send inventorySetPanelStatus`: 10
- `netstream send invAct`: 3
- `netstream send hookName`: 2
- `netstream send itemSplitAdd`: 2
- `netstream send inventoryUpdSkin`: 2
- `send nutInventoryDelete`: 2
- `netstream send storageInventory`: 2
- `netstream hook itemSplitDrop`: 2
- `Start nutInventoryDelete`: 2
- `Start nutTransferItem`: 1
- `foodReadyPartAddClient`: 1
- `register nutInventoryRemove`: 1
- `receive OpenMyInv`: 1
- `netstream send inventoryOpen`: 1
- `netstream hook inventoryCloseOnAction`: 1
- `netstream hook mnhrOpenVisor`: 1
- `netstream hook invAct`: 1
- `send nutInventoryData`: 1
- `receive nutInventoryRemove`: 1
- `send nutInventoryAdd`: 1

## Lifecycle Propagation

- `listen PostPlayerLoadout @ plugins\inventory\sh_plugin.lua:689`: 2
- `PostPlayerLoadout`: 2
- `listen PostPlayerLoadout @ plugins\inventory\sh_plugin.lua:688`: 2
- `emit PostPlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:367`: 2
- `emit PlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:263`: 1
- `emit PlayerLoadout @ gamemode\core\hooks\sv_hooks.lua:219`: 1
- `emit CharacterPreSave @ gamemode\core\meta\sh_character.lua:42`: 1
- `PlayerLoadout`: 1
- `listen PlayerLoadout @ plugins\inventory\sh_plugin.lua:637`: 1
- `CharacterPreSave`: 1
- `listen CharacterPreSave @ plugins\inventory\sh_plugin.lua:718`: 1
- `listen PlayerLoadout @ plugins\inventory\sh_plugin.lua:638`: 1
- `listen CharacterPreSave @ plugins\inventory\sh_plugin.lua:719`: 1

## Synchronization Hotspots

- `netstream send inventorySetPanelStatus`: 10
- `read ReadUInt nutInventoryInit`: 3
- `write WriteUInt nutInventoryInit`: 3
- `write WriteUInt nutTransferItem`: 3
- `netstream send invAct`: 3
- `write WriteTable nutInventoryInit`: 2
- `read ReadTable nutInventoryInit`: 2
- `send nutInventoryDelete`: 2
- `write WriteString nutInventoryInit`: 2
- `write WriteType nutInventoryDelete`: 2
- `read ReadString nutInventoryInit`: 2
- `netstream send storageInventory`: 2
- `Start nutInventoryDelete`: 2
- `Start nutTransferItem`: 1
- `write WriteUInt nutInventoryRemove`: 1
- `register nutInventoryRemove`: 1
- `netstream send inventoryOpen`: 1
- `write WriteType nutInventoryAdd`: 1
- `read ReadType nutInventoryDelete`: 1
- `netstream hook invAct`: 1

## Important Timers

- `player_action_timer@plugins\inventory\sv_hooks.lua:16`: 1
- `player_cancelable_action_timer@plugins\storage\entities\entities\nut_storage\init.lua:315`: 1
- `timer_simple@plugins\storage\sv_storage.lua:149`: 1
- `SetSimpleTimer`: 1
- `player_cancelable_action_timer@plugins\storage\entities\entities\nut_storage\init.lua:256`: 1
- `player_action_timer`: 1
- `setAction`: 1
- `player_action_timer@plugins\storage\entities\entities\nut_storage\init.lua:70`: 1
- `player_cancelable_action_timer@plugins\crafting\entities\entities\nut_storage_kit\init.lua:30`: 1
- `entity_timer_simple@plugins\inventory\sv_hooks.lua:123`: 1
- `timer_simple@plugins\gridinv\plugins\1_1compat\sh_plugin.lua:31`: 1
- `entity_validity_guard_expected`: 1
- `entity_simulation_timer`: 1
- `player_cancelable_action_timer@plugins\storage\entities\entities\nut_storage\init.lua:147`: 1

## Realms

- `server`: 65
- `shared`: 54
- `client`: 32

## Major Files

- `plugins\tying\sh_charsearch.lua`: 13
- `plugins\inventory\sh_plugin.lua`: 10
- `gamemode\core\hooks\sv_hooks.lua`: 9
- `plugins\inventory\sv_hooks.lua`: 8
- `plugins\gridinv\plugins\1_1compat\sv_migrations.lua`: 7
- `gamemode\core\meta\inventory\cl_base_inventory.lua`: 7
- `plugins\ragdollinteraction\interaction\sv_hooks.lua`: 6
- `plugins\ragdollinteraction\interaction\cl_hooks.lua`: 6
- `plugins\storage\entities\entities\nut_storage\init.lua`: 6
- `plugins\inventory\cl_hooks.lua`: 6
- `plugins\gridinv\sh_plugin.lua`: 5
- `gamemode\core\meta\inventory\cl_panel_extensions.lua`: 3
- `plugins\gridinv\plugins\gridinvui\sh_plugin.lua`: 3
- `plugins\_disabled\simpleinv\plugins\listinvui\sh_plugin.lua`: 3
- `plugins\gridinv\sv_access_rules.lua`: 3
- `plugins\gridinv\items\base\sh_bags.lua`: 3
- `gamemode\core\libs\item\cl_networking.lua`: 3
- `gamemode\core\libs\character\sv_character.lua`: 3
- `plugins\ragdollinteraction\interaction\sv_access_rules.lua`: 3
- `plugins\_disabled\simpleinv\sh_plugin.lua`: 3

## Connected Plugins / Subsystems

- `ragdollinteraction`: 133
- `vendor`: 107
- `gridinv`: 99
- `mining`: 75
- `tying`: 69
- `storage`: 67
- `crafting`: 58
- `lootablecontainers`: 21
- `cassetteplayer`: 15
- `healthproblems`: 6
- `armor`: 5
- `gadgets`: 4
- `propprotect.lua`: 4
- `pac`: 3
- `wepselect.lua`: 2
- `saveitems.lua`: 1
- `snowy_components`: 1
- `admintools`: 1
- `attributes`: 1
- `biorezonance`: 1

## Runtime Propagation Hubs

- degree `133` | `plugin` | `ragdollinteraction` | `plugin:ragdollinteraction`
- degree `126` | `file` | `gamemode\core\hooks\sv_hooks.lua` | `file:gamemode/core/hooks/sv_hooks.lua`
- degree `113` | `plugin` | `gamemode` | `plugin:gamemode`
- degree `107` | `plugin` | `vendor` | `plugin:vendor`
- degree `99` | `plugin` | `gridinv` | `plugin:gridinv`
- degree `81` | `file` | `plugins\ragdollinteraction\interaction\sv_hooks.lua` | `file:plugins/ragdollinteraction/interaction/sv_hooks.lua`
- degree `75` | `plugin` | `mining` | `plugin:mining`
- degree `69` | `plugin` | `tying` | `plugin:tying`
- degree `67` | `plugin` | `storage` | `plugin:storage`
- degree `65` | `file` | `plugins\mining\entities\entities\nut_ore_smelter\init.lua` | `file:plugins/mining/entities/entities/nut_ore_smelter/init.lua`
- degree `63` | `file` | `plugins\inventory\cl_hooks.lua` | `file:plugins/inventory/cl_hooks.lua`
- degree `58` | `plugin` | `crafting` | `plugin:crafting`
- degree `45` | `file` | `plugins\tying\sh_charsearch.lua` | `file:plugins/tying/sh_charsearch.lua`
- degree `45` | `file` | `plugins\ragdollinteraction\interaction\cl_hooks.lua` | `file:plugins/ragdollinteraction/interaction/cl_hooks.lua`
- degree `43` | `file` | `gamemode\core\meta\inventory\sv_base_inventory.lua` | `file:gamemode/core/meta/inventory/sv_base_inventory.lua`
- degree `41` | `file` | `gamemode\core\meta\inventory\cl_base_inventory.lua` | `file:gamemode/core/meta/inventory/cl_base_inventory.lua`
- degree `37` | `plugin` | `inventory` | `plugin:inventory`
- degree `37` | `file` | `plugins\cassetteplayer\sh_plugin.lua` | `file:plugins/cassetteplayer/sh_plugin.lua`
- degree `34` | `file` | `gamemode\core\libs\item\cl_networking.lua` | `file:gamemode/core/libs/item/cl_networking.lua`
- degree `28` | `file` | `plugins\gridinv\plugins\1_1compat\sv_migrations.lua` | `file:plugins/gridinv/plugins/1_1compat/sv_migrations.lua`
- degree `26` | `network_message` | `nutTransferItem` | `netmsg:gmod_net:nutTransferItem`
- degree `26` | `hook_event` | `PostPlayerLoadout` | `hook:PostPlayerLoadout`
- degree `26` | `file` | `plugins\storageinterface\derma\cl_storage_interface.lua` | `file:plugins/storageinterface/derma/cl_storage_interface.lua`
- degree `25` | `file` | `plugins\storage\entities\entities\nut_storage\init.lua` | `file:plugins/storage/entities/entities/nut_storage/init.lua`
- degree `24` | `network_message` | `nutInventoryInit` | `netmsg:gmod_net:nutInventoryInit`

## Topology Hubs

- degree `133` | `plugin` | `ragdollinteraction` | `plugin:ragdollinteraction`
- degree `126` | `file` | `gamemode\core\hooks\sv_hooks.lua` | `file:gamemode/core/hooks/sv_hooks.lua`
- degree `113` | `plugin` | `gamemode` | `plugin:gamemode`
- degree `107` | `plugin` | `vendor` | `plugin:vendor`
- degree `99` | `plugin` | `gridinv` | `plugin:gridinv`
- degree `81` | `file` | `plugins\ragdollinteraction\interaction\sv_hooks.lua` | `file:plugins/ragdollinteraction/interaction/sv_hooks.lua`
- degree `75` | `plugin` | `mining` | `plugin:mining`
- degree `69` | `plugin` | `tying` | `plugin:tying`
- degree `67` | `plugin` | `storage` | `plugin:storage`
- degree `65` | `file` | `plugins\mining\entities\entities\nut_ore_smelter\init.lua` | `file:plugins/mining/entities/entities/nut_ore_smelter/init.lua`
- degree `63` | `file` | `plugins\inventory\cl_hooks.lua` | `file:plugins/inventory/cl_hooks.lua`
- degree `58` | `plugin` | `crafting` | `plugin:crafting`
- degree `45` | `file` | `plugins\tying\sh_charsearch.lua` | `file:plugins/tying/sh_charsearch.lua`
- degree `45` | `file` | `plugins\ragdollinteraction\interaction\cl_hooks.lua` | `file:plugins/ragdollinteraction/interaction/cl_hooks.lua`
- degree `43` | `file` | `gamemode\core\meta\inventory\sv_base_inventory.lua` | `file:gamemode/core/meta/inventory/sv_base_inventory.lua`
- degree `41` | `file` | `gamemode\core\meta\inventory\cl_base_inventory.lua` | `file:gamemode/core/meta/inventory/cl_base_inventory.lua`
- degree `37` | `plugin` | `inventory` | `plugin:inventory`
- degree `37` | `file` | `plugins\cassetteplayer\sh_plugin.lua` | `file:plugins/cassetteplayer/sh_plugin.lua`
- degree `34` | `file` | `gamemode\core\libs\item\cl_networking.lua` | `file:gamemode/core/libs/item/cl_networking.lua`
- degree `28` | `file` | `plugins\gridinv\plugins\1_1compat\sv_migrations.lua` | `file:plugins/gridinv/plugins/1_1compat/sv_migrations.lua`
- degree `26` | `network_message` | `nutTransferItem` | `netmsg:gmod_net:nutTransferItem`
- degree `26` | `hook_event` | `PostPlayerLoadout` | `hook:PostPlayerLoadout`
- degree `26` | `file` | `plugins\storageinterface\derma\cl_storage_interface.lua` | `file:plugins/storageinterface/derma/cl_storage_interface.lua`
- degree `25` | `file` | `plugins\storage\entities\entities\nut_storage\init.lua` | `file:plugins/storage/entities/entities/nut_storage/init.lua`
- degree `24` | `network_message` | `nutInventoryInit` | `netmsg:gmod_net:nutInventoryInit`

## Runtime Risks

- Review high-degree hubs for hidden coupling.
- Review network signals for synchronization ownership.
- Review timers for scheduler or debounce behavior.
- Review realm crossings for client/server authority issues.

## Notes

This document is generated from topology only. Use raw Lua only for exact validation.
