# Network operation normalization QA

Schema: `normalized_network_operations.v1`

## Inputs
- `netstream_starts`: **466**
- `netstream_hooks`: **263**
- `net_starts`: **86**
- `net_receives`: **74**
- `util_add_network_strings`: **66**
- `net_reads`: **150**
- `net_writes`: **151**
- `net_messages_deep`: **160**

## Totals
- Normalized operations: **955**
- Sends: **552**
- Receives: **337**
- Registrations: **66**
- Symbol/QA issues: **603**
- Corrected recipient-as-message captures: **99**
- Dynamic/symbolic messages kept: **499**
- Suspicious message IDs remaining: **5**

## Protocols
- `netstream`: 729
- `gmod_net`: 226

## Operations
- `send`: 552
- `receive`: 337
- `register`: 66

## Realms
- `client`: 287
- `server`: 280
- `shared`: 267
- `unknown`: 121

## Message quality
- `dynamic`: 499
- `literal`: 451
- `suspicious`: 5

## Message resolution
- `dynamic`: 504
- `literal`: 394
- `symbol_constant`: 57

## Netstream argument layouts
- `inferred_server_netstream_start`: 183
- `client_netstream_start`: 171
- `server_netstream_start`: 82
- `inferred_client_netstream_start`: 30

## Protocol/subsystem guesses
- `misc`: 510
- `inventory_item_storage`: 175
- `ui_hud`: 155
- `vendor`: 48
- `character`: 23
- `health_status`: 17
- `admin_config`: 16
- `crafting`: 11

## Issue kinds
- `netstream_hook_message_issue`: 263
- `corrected_recipient_misread_as_message`: 99
- `net_start_message_issue`: 86
- `net_receive_message_issue`: 74
- `util_add_network_string_message_issue`: 66
- `netstream_message_issue`: 15

## Top sent messages
- `hudRemoveStatusIcon`: 26
- `hudAddStatusIcon`: 25
- `interfaceTurnOn`: 19
- `endO2Hud`: 10
- `inventorySetPanelStatus`: 10
- `nvisionOff`: 9
- `startO2Hud`: 8
- `nvisionOn`: 8
- `entFreezeState`: 8
- `hudHandleStatusIconCount`: 6
- `entity`: 5
- `diseasesSelectWeapon`: 5
- `actBar`: 5
- `searchExit`: 5
- `lootExit`: 5
- `nutCharFetchNames`: 5
- `nutStorageOpen`: 5
- `VManip_SimplePlay`: 5
- `rezonatorAdd`: 4
- `hookName`: 4
- `elPanelTryFix`: 4
- `rgn`: 4
- `invAct`: 4
- `charSet`: 4
- `gasMaskOff`: 3
- `invExit`: 3
- `radioAdjust`: 3
- `workbenchInvOpen`: 3
- `attachAttachment`: 3
- `voicePlay`: 3
- `seqSet`: 3
- `charDel`: 3
- `sendVendorInfo`: 3
- `obj`: 2
- `cDisp`: 2
- `hideAdd`: 2
- `setBioSwep`: 2
- `compSyncWorkShift`: 2
- `diseasesStatusInterfaceOpen`: 2
- `diseasesStatusInterfaceSync`: 2

## Top received messages
- `nutCharFetchNames`: 3
- `cOpen`: 2
- `itemSplitDrop`: 2
- `radioAdjust`: 2
- `searchExit`: 2
- `searchPly`: 2
- `obj`: 2
- `cfgSet`: 2
- `nutPluginDisable`: 2
- `nutPluginList`: 2
- `syncClientTime`: 2
- `nutStringReq`: 2
- `NetStreamDS`: 2
- `nutCharChoose`: 2
- `nutCharCreate`: 2
- `nutStorageUnlock`: 2
- `nutVendorExit`: 2
- `nutVendorEdit`: 2
- `nut_DisplaySpawnPoints`: 1
- `hideAdd`: 1
- `createCustomItem`: 1
- `eventpointSetSpawn`: 1
- `eventpointSetUnbanTime`: 1
- `eventpointSpawnMenuSwitch`: 1
- `eventpointSpawnItem`: 1
- `eventpointSpawn300Mid`: 1
- `eventpointSpawn300Lrg`: 1
- `rezonatorAdd`: 1
- `rezonatorRemove`: 1
- `gasMaskOn`: 1
- `gasMaskOff`: 1
- `startO2Hud`: 1
- `endO2Hud`: 1
- `oxystantionSelfFill`: 1
- `oxystantionTankFill`: 1
- `oxystantionL1Fill`: 1
- `setBioSwep`: 1
- `workbenchInvClose`: 1
- `workbenchInvOpen`: 1
- `pressingSetProgram`: 1

## Raw GMod net messages missing util.AddNetworkString in manifests
- `ChatMessage`
- `ClearAllItems`
- `ItemUpdated`
- `OpenItemManager`
- `RemoveEntity`
- `RemoveItem`
- `RequestEntityData`
- `RequestItemData`
- `SendEntityData`
- `SendItemData`
- `VManip_SimplePlay`
- `mgbase_tpanim`
- `nutVendor`
- `nutVendorFaction`

## Raw GMod net messages registered but not observed as sent/received
- `ContainerEmpty`
- `IsFix`
- `nutCharMenu`
- `nutVendorMaxStock`
- `nutVendorMode`
- `nutVendorMoney`
- `nutVendorPrice`
- `nutVendorStock`

## Messages with senders but no receivers
- `ChatMessage`
- `RemoveEntity`
- `VManip_SimplePlay`
- `bank::SyncVaultAttempts`
- `bank::ValidateVaultPassword`
- `callbackHook`
- `charDel`
- `classUpdate`
- `entity`
- `hookName`
- `invExit`
- `mgbase_tpanim`
- `mnhr`
- `name`
- `nutLogStream`
- `nutVendorAllowClass`
- `nutVendorAllowFaction`
- `self:GetPos()`
- `vendorEdit`

## Messages with receivers but no senders
- `OpenCraft`
- `OpenMyInv`
- `RemoveItem`
- `RequestEntityData`
- `areaManager`
- `cPlayerActive`
- `cPlayerDisable`
- `cPlayerVolumeChanged`
- `cookingpotEat`
- `cookingpotPreserveFood`
- `cookingpotTakePortion`
- `foodPartAddServer`
- `foodPartUseServer`
- `foodReadyPartAddServer`
- `getUserCardAccess`
- `invMv`
- `item`
- `kettlePartAddServer`
- `nutSyncGesture`
- `nutVendor`
- `nutVendorFaction`
- `nutVendorSync`
- `performCprChoose`
- `rezonatorRemove`
- `setUpPointsUpdate`
- `setUpReplicastatus`
- `setUpUserCard`
- `smokeTryChoke`
- `stationFlashLight`
- `stationNvg2`
- `stationNvg3`
- `stationWepPower`

## Remaining suspicious message IDs
- `entity` at `plugins\cassetteplayer\sh_plugin.lua:69` via `netstream.Start` layout=`inferred_server_netstream_start` expr=`entity`
- `entity` at `plugins\cassetteplayer\sh_plugin.lua:77` via `netstream.Start` layout=`inferred_server_netstream_start` expr=`entity`
- `entity` at `plugins\cassetteplayer\sh_plugin.lua:91` via `netstream.Start` layout=`inferred_server_netstream_start` expr=`entity`
- `entity` at `plugins\cassetteplayer\sh_plugin.lua:157` via `netstream.Start` layout=`inferred_server_netstream_start` expr=`entity`
- `entity` at `plugins\cassetteplayer\sh_plugin.lua:165` via `netstream.Start` layout=`inferred_server_netstream_start` expr=`entity`

## Dynamic/symbolic messages
- `hookName` at `plugins\inventory\cl_hooks.lua:246` via `netstream.Start` resolution=`dynamic`
- `hookName` at `plugins\inventory\cl_hooks.lua:254` via `netstream.Start` resolution=`dynamic`
- `mnhr` at `plugins\mnhr\sh_plugin.lua:283` via `netstream.Start` resolution=`dynamic`
- `mnhr` at `plugins\mnhr\sh_plugin.lua:294` via `netstream.Start` resolution=`dynamic`
- `callbackHook` at `plugins\gadgets\entities\entities\nut_computer\init.lua:192` via `netstream.Start` resolution=`dynamic`
- `hookName` at `plugins\mnhr\derma\cl_mnhrstation_interface.lua:60` via `netstream.Start` resolution=`dynamic`
- `hookName` at `plugins\needs\derma\cl_cooking_interface.lua:150` via `netstream.Start` resolution=`dynamic`
- `self:GetPos()` at `gamemode\core\meta\sh_player.lua:43` via `netstream.Start` resolution=`dynamic`
- `name` at `gamemode\core\libs\thirdparty\sh_netstream2.lua:54` via `netstream.Start` resolution=`dynamic`
- `name` at `gamemode\core\libs\thirdparty\sh_netstream2.lua:132` via `netstream.Start` resolution=`dynamic`
- `nut_DisplaySpawnPoints` at `plugins\worlditemspawner.lua:96` via `netstream.Hook` resolution=`dynamic`
- `hideAdd` at `plugins\admintools\cl_hooks.lua:3` via `netstream.Hook` resolution=`dynamic`
- `createCustomItem` at `plugins\admintools\sh_plugin.lua:587` via `netstream.Hook` resolution=`dynamic`
- `eventpointSetSpawn` at `plugins\admintools\sv_hooks.lua:9` via `netstream.Hook` resolution=`dynamic`
- `eventpointSetUnbanTime` at `plugins\admintools\sv_hooks.lua:16` via `netstream.Hook` resolution=`dynamic`
- `eventpointSpawnMenuSwitch` at `plugins\admintools\sv_hooks.lua:23` via `netstream.Hook` resolution=`dynamic`
- `eventpointSpawnItem` at `plugins\admintools\sv_hooks.lua:30` via `netstream.Hook` resolution=`dynamic`
- `eventpointSpawn300Mid` at `plugins\admintools\sv_hooks.lua:37` via `netstream.Hook` resolution=`dynamic`
- `eventpointSpawn300Lrg` at `plugins\admintools\sv_hooks.lua:43` via `netstream.Hook` resolution=`dynamic`
- `rezonatorAdd` at `plugins\biorezonance\cl_hooks.lua:3` via `netstream.Hook` resolution=`dynamic`
- `rezonatorRemove` at `plugins\biorezonance\cl_hooks.lua:9` via `netstream.Hook` resolution=`dynamic`
- `gasMaskOn` at `plugins\biorezonance\sh_plugin.lua:354` via `netstream.Hook` resolution=`dynamic`
- `gasMaskOff` at `plugins\biorezonance\sh_plugin.lua:367` via `netstream.Hook` resolution=`dynamic`
- `startO2Hud` at `plugins\biorezonance\sh_plugin.lua:380` via `netstream.Hook` resolution=`dynamic`
- `endO2Hud` at `plugins\biorezonance\sh_plugin.lua:421` via `netstream.Hook` resolution=`dynamic`
- `oxystantionSelfFill` at `plugins\biorezonance\sv_hooks.lua:152` via `netstream.Hook` resolution=`dynamic`
- `oxystantionTankFill` at `plugins\biorezonance\sv_hooks.lua:159` via `netstream.Hook` resolution=`dynamic`
- `oxystantionL1Fill` at `plugins\biorezonance\sv_hooks.lua:166` via `netstream.Hook` resolution=`dynamic`
- `setBioSwep` at `plugins\biorezonance\sv_hooks.lua:173` via `netstream.Hook` resolution=`dynamic`
- `cOpen` at `plugins\cassetteplayer\sh_plugin.lua:119` via `netstream.Hook` resolution=`dynamic`
- `workbenchInvClose` at `plugins\crafting\cl_hooks.lua:3` via `netstream.Hook` resolution=`dynamic`
- `workbenchInvOpen` at `plugins\crafting\sv_hooks.lua:52` via `netstream.Hook` resolution=`dynamic`
- `pressingSetProgram` at `plugins\crafting\sv_hooks.lua:59` via `netstream.Hook` resolution=`dynamic`
- `fpotHarvest` at `plugins\farming\sh_plugin.lua:10` via `netstream.Hook` resolution=`dynamic`
- `interfaceTurnOn` at `plugins\gadgets\cl_hooks.lua:19` via `netstream.Hook` resolution=`dynamic`
- `setUpUserCard` at `plugins\gadgets\cl_hooks.lua:26` via `netstream.Hook` resolution=`dynamic`
- `setUpReplicastatus` at `plugins\gadgets\cl_hooks.lua:33` via `netstream.Hook` resolution=`dynamic`
- `setUpPointsUpdate` at `plugins\gadgets\cl_hooks.lua:40` via `netstream.Hook` resolution=`dynamic`
- `setUpLocksView` at `plugins\gadgets\cl_hooks.lua:47` via `netstream.Hook` resolution=`dynamic`
- `compSendUserCardAccess` at `plugins\gadgets\cl_hooks.lua:54` via `netstream.Hook` resolution=`dynamic`
- `compSyncWorkShift` at `plugins\gadgets\cl_hooks.lua:66` via `netstream.Hook` resolution=`dynamic`
- `setUpLocksInfo` at `plugins\gadgets\cl_hooks.lua:78` via `netstream.Hook` resolution=`dynamic`
- `doorInterfaceTurnOn` at `plugins\gadgets\cl_hooks.lua:85` via `netstream.Hook` resolution=`dynamic`
- `searchReplica` at `plugins\gadgets\sv_hooks.lua:151` via `netstream.Hook` resolution=`dynamic`
- `logOut` at `plugins\gadgets\sv_hooks.lua:158` via `netstream.Hook` resolution=`dynamic`
- `compAddShiftSv` at `plugins\gadgets\sv_hooks.lua:165` via `netstream.Hook` resolution=`dynamic`
- `remAddShiftSv` at `plugins\gadgets\sv_hooks.lua:175` via `netstream.Hook` resolution=`dynamic`
- `lockResetPassword` at `plugins\gadgets\sv_hooks.lua:188` via `netstream.Hook` resolution=`dynamic`
- `lockCorrectPass` at `plugins\gadgets\sv_hooks.lua:195` via `netstream.Hook` resolution=`dynamic`
- `lockUpdateAccess` at `plugins\gadgets\sv_hooks.lua:202` via `netstream.Hook` resolution=`dynamic`
- `setUpCard` at `plugins\gadgets\sv_hooks.lua:209` via `netstream.Hook` resolution=`dynamic`
- `setUpCardAccess` at `plugins\gadgets\sv_hooks.lua:216` via `netstream.Hook` resolution=`dynamic`
- `getUserCardAccess` at `plugins\gadgets\sv_hooks.lua:223` via `netstream.Hook` resolution=`dynamic`
- `setUpCardBodyGroup` at `plugins\gadgets\sv_hooks.lua:230` via `netstream.Hook` resolution=`dynamic`
- `setCharPoints` at `plugins\gadgets\sv_hooks.lua:237` via `netstream.Hook` resolution=`dynamic`
- `getLocksView` at `plugins\gadgets\sv_hooks.lua:244` via `netstream.Hook` resolution=`dynamic`
- `getLockInfo` at `plugins\gadgets\sv_hooks.lua:251` via `netstream.Hook` resolution=`dynamic`
- `lockNameChange` at `plugins\gadgets\sv_hooks.lua:258` via `netstream.Hook` resolution=`dynamic`
- `switchLockState` at `plugins\gadgets\sv_hooks.lua:265` via `netstream.Hook` resolution=`dynamic`
- `doorLockSwitchState` at `plugins\gadgets\sv_hooks.lua:272` via `netstream.Hook` resolution=`dynamic`
- `doorLockResetPassword` at `plugins\gadgets\sv_hooks.lua:280` via `netstream.Hook` resolution=`dynamic`
- `doorLockUpdateAccess` at `plugins\gadgets\sv_hooks.lua:299` via `netstream.Hook` resolution=`dynamic`
- `diseasesAddBlindness` at `plugins\healthproblems\cl_hooks.lua:11` via `netstream.Hook` resolution=`dynamic`
- `diseasesRemoveBlindness` at `plugins\healthproblems\cl_hooks.lua:19` via `netstream.Hook` resolution=`dynamic`
- `diseasesSelectWeapon` at `plugins\healthproblems\cl_hooks.lua:25` via `netstream.Hook` resolution=`dynamic`
- `diseasesStatusInterfaceOpen` at `plugins\healthproblems\cl_hooks.lua:34` via `netstream.Hook` resolution=`dynamic`
- `diseasesStatusInterfaceSync` at `plugins\healthproblems\cl_hooks.lua:45` via `netstream.Hook` resolution=`dynamic`
- `diseasesHandleSwepSelect` at `plugins\healthproblems\sv_hooks.lua:229` via `netstream.Hook` resolution=`dynamic`
- `diseasesStatusInterfaceClose` at `plugins\healthproblems\sv_hooks.lua:250` via `netstream.Hook` resolution=`dynamic`
- `diseasesUseItem` at `plugins\healthproblems\sv_hooks.lua:268` via `netstream.Hook` resolution=`dynamic`
- `diseasesStatusInterfaceTargetGetData` at `plugins\healthproblems\sv_hooks.lua:288` via `netstream.Hook` resolution=`dynamic`
- `hudAddStatusIcon` at `plugins\hud\sh_plugin.lua:434` via `netstream.Hook` resolution=`dynamic`
- `hudHandleStatusIconCount` at `plugins\hud\sh_plugin.lua:465` via `netstream.Hook` resolution=`dynamic`
- `hudRemoveStatusIcon` at `plugins\hud\sh_plugin.lua:484` via `netstream.Hook` resolution=`dynamic`
- `hudRemoveAllStatusIcons` at `plugins\hud\sh_plugin.lua:507` via `netstream.Hook` resolution=`dynamic`
- `inventoryOpen` at `plugins\inventory\cl_hooks.lua:112` via `netstream.Hook` resolution=`dynamic`
- `vendorTradeInterface` at `plugins\inventory\cl_hooks.lua:123` via `netstream.Hook` resolution=`dynamic`
- `itemSplitTake` at `plugins\inventory\cl_hooks.lua:193` via `netstream.Hook` resolution=`dynamic`
- `setUpTargetMoney` at `plugins\inventory\cl_hooks.lua:222` via `netstream.Hook` resolution=`dynamic`
- `foodPartUseClient` at `plugins\inventory\cl_hooks.lua:259` via `netstream.Hook` resolution=`dynamic`
- ... 419 more

## External doctrine checks
- `net.Start(messageName, unreliable?)`: message name is arg0.
- Raw GMod net messages should be pooled server-side with `util.AddNetworkString(messageName)` before use.
- Raw net messages have an approximate 64 KiB/message limit; high payload arg count is only a weak static risk signal, not proof of oversize payload.
- `netstream.Start` is project/library-level: server layout is recipient first, client layout is message first.
