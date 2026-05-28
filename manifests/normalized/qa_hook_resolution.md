# Hook normalization QA

## Summary

- Total hook runs: **495**
- Resolved hook runs: **289**
- Unresolved hook runs: **206**
- Resolution rate: **58.38%**
- Plugin hook edges: **289**
- Edge count matches resolved: **True**

## Unresolved classification

- `missing_plugin_method_or_external_hook`: **91**
- `probably_project_domain_hook`: **43**
- `probably_schema_hook`: **34**
- `probably_nutscript_builtin`: **25**
- `probably_schema_or_project_core_hook`: **12**
- `probably_gmod_builtin`: **1**

## Top unresolved hooks

- `screamer2`: 9
- `StorageRestored`: 5
- `StorageEntityRemoved`: 5
- `OnCharVarChanged`: 5
- `GetDefaultCharName`: 4
- `OnNPCKilled`: 3
- `PersistenceSave`: 3
- `IsPlayerRecognized`: 3
- `ItemInitialized`: 3
- `CanPlayerBustLock`: 2
- `CanPlayerEditData`: 2
- `CanPlayerEditObjectives`: 2
- `PlayerCanKnock`: 2
- `GetStartAttribPoints`: 2
- `OnCreateStoragePanel`: 2
- `ShouldRadioBeep`: 2
- `CanOutfitChangeModel`: 2
- `OnCharAttribUpdated`: 2
- `useIhnolitOre`: 2
- `ihnolitOreTimer`: 2
- `PlayerCanUseLock`: 2
- `StorageCanTransferItem`: 2
- `CreateSalaryTimer`: 2
- `OnPickupObject`: 2
- `InitializedConfig`: 2
- `VManipPickupHook`: 2
- `PostLoadData`: 2
- `PlayerMessageSend`: 2
- `OnPlayerJoinClass`: 2
- `CanPlayerUseCommand`: 2
- `CreateDefaultInventory`: 2
- `InventoryItemRemoved`: 2
- `GetMaxPlayerCharacter`: 2
- `CanPlayerViewData`: 1
- `CanPlayerViewObjectives`: 1
- `PlayerGetStunThreshold`: 1
- `terminator_blocktarget`: 1
- `terminator_engagedenemywasbad`: 1
- `OnTerminatorKilledRagdoll`: 1
- `TerminatorUse`: 1

## Ambiguous resolved hooks

- none

## Known target checks

- `HandleDiseaseOnCall`: OK
- `EnduranceCheck`: OK
