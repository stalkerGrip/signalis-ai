# Architecture Intelligence V1

- Schema: `architecture_intelligence.v1`
- Producer: `scripts.investigation.build_architecture_intelligence_v1`
- Source query: `vendor purchase itemdata architecture inventory metadata sync UI refresh`
- Input: `E:\signalis_ai\investigations\retrieval\runtime_chain_context_pack.json`
- Chains analyzed: `1`

## Summary

Chains by confidence:

- `high`: `1`

Chains by promotion status:

- `promoted_confirmed_chain`: `1`

Stage class totals:

- `inventory_membership`: `2`
- `metadata`: `6`
- `network`: `3`
- `server_authority`: `3`
- `ui`: `1`

## Architecture Findings

### vendor_purchase_itemdata_runtime_chain_candidate_v6:inventory_membership_and_item_metadata

- Type: `coupling`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md`
- Risk: `ui_desync_if_one_path_refreshes_without_the_other`

The chain couples inventory membership propagation with item metadata propagation while keeping them as distinct stages.

### vendor_purchase_itemdata_runtime_chain_candidate_v6:client_data_apply_to_ui_refresh

- Type: `coupling`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md`
- Risk: `stale_presentation_if_ui_refresh_hook_does_not_fire`

Client-side data application is coupled to UI refresh propagation.

### vendor_purchase_itemdata_runtime_chain_candidate_v6:network_sync_boundary

- Type: `coupling`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md`
- Risk: `receiver_scope_or_payload_loss_can_create_client_desync`

The chain crosses a network synchronization boundary.

### vendor_purchase_itemdata_runtime_chain_candidate_v6:item_metadata_sync_contract

- Type: `sync_contract`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md`
- Coverage: `1.0`

Item metadata mutation must have an explicit network send and client apply stage.

### vendor_purchase_itemdata_runtime_chain_candidate_v6:ui_refresh_contract

- Type: `sync_contract`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md`
- Coverage: `1.0`

Client item data application should propagate into a UI refresh hook.

### vendor_purchase_itemdata_runtime_chain_candidate_v6:inventory_membership_vs_metadata_boundary

- Type: `sync_contract`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md`
- Coverage: `1.0`

Inventory membership sync and item metadata sync appear as separate propagation stages.

## Chain Analyses

### vendor purchase itemdata propagation chain

- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
- Confidence: `high`
- Promotion status: `promoted_confirmed_chain`
- Stage count: `8`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md`

Stages:

- `vendor_open_metadata_assignment` — metadata
- `vendor_purchase_transfer` — inventory_membership, server_authority
- `vendor_metadata_cleanup` — metadata, server_authority
- `item_metadata_mutation` — metadata, server_authority
- `item_metadata_network_send` — metadata, network
- `inventory_membership_client_apply` — network, inventory_membership
- `item_metadata_client_apply` — metadata, network
- `ui_itemdata_refresh_hook` — metadata, ui

Realm / sync transitions:

- `item_metadata_network_send` → `inventory_membership_client_apply` = `server_to_client_sync_boundary`
- `inventory_membership_client_apply` → `item_metadata_client_apply` = `server_to_client_sync_boundary`

## Next Questions

- Which UI refresh hooks are canonical synchronization boundaries versus presentation-only refreshes?
- Which network messages should become explicit synchronization contracts?
- Where should inventory membership sync and item metadata sync be documented as separate contracts?
