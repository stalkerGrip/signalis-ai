# Runtime Chain Promotion: vendor purchase item data propagation topology chain

## Promotion Result

- Promotion type: `promoted_topology_supported_chain`
- Promoted: `True`
- Source artifact: `investigations/validation/vendor_purchase_itemdata_runtime_chain_v4_after_validation.json`
- Generated: `2026-05-31T17:44:22.166761+00:00`

## Gate Values

- Confidence: `medium`
- Score: `1.0`
- Validation coverage: `0.6667`
- Missing categories: `none`
- Validation targets: `None`

## Gate Reasons

- medium confidence
- score >= 0.90
- validation coverage >= 0.60
- missing categories none
- promoted as topology-supported, not fully confirmed

## Runtime Chain

1. `plugins\gridinv\sv_transfer.lua` — file, server
2. `nutTransferItem` — network_message, unknown
3. `plugins\gridinv\plugins\gridinvui\derma\cl_grid_inventory_panel.lua` — file, client
4. `client` — realm, client
5. `emit ItemDataChanged @ gamemode\core\libs\item\cl_networking.lua:20` — hook_emitter, client
6. `listen ItemDataChanged @ gamemode\core\meta\inventory\cl_panel_extensions.lua:47` — hook_listener, client

## Promotion Boundary

`promoted_confirmed_chain` means directed/source-confirmed.

`promoted_topology_supported_chain` means topology path complete and validation coverage sufficient, but not fully directed/source-confirmed.

Do not collapse these promotion classes.
