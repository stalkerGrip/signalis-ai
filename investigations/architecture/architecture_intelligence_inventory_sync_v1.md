# Architecture Intelligence V1

- Schema: `architecture_intelligence.v1`
- Producer: `scripts.investigation.build_architecture_intelligence_v1`
- Source query: `inventory vendor storage item metadata sync UI desync network propagation`
- Input: `E:\signalis_ai\investigations\retrieval\runtime_chain_context_pack_inventory_sync.json`
- Rule config: `None`
- Chains analyzed: `2`

## Summary

Chains by confidence:

- `high`: `2`

Chains by promotion status:

- `promoted_confirmed_chain`: `2`

Stage class totals:

- `client_apply`: `4`
- `hook_event`: `2`
- `inventory`: `4`
- `metadata`: `12`
- `network`: `2`
- `server_authority`: `4`
- `ui`: `2`
- `vendor`: `6`

Observed coupling patterns:

- `client_apply_to_ui_refresh`: `2`
- `inventory_and_metadata_propagation`: `2`
- `network_sync_boundary`: `2`

Observed sync contracts:

- `client_apply_to_presentation_contract`: `2`
- `metadata_sync_contract`: `2`
- `ownership_vs_metadata_boundary`: `2`

## Architecture Findings

### vendor_purchase_itemdata_runtime_chain_candidate_v7:inventory_and_metadata_propagation

- Type: `coupling`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v7`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_promoted_confirmed_chain.md`
- Risk: `desync_risk_if_one_path_refreshes_without_the_other`

The chain contains both inventory propagation and metadata propagation concerns.

### vendor_purchase_itemdata_runtime_chain_candidate_v7:client_apply_to_ui_refresh

- Type: `coupling`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v7`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_promoted_confirmed_chain.md`
- Risk: `stale_presentation_if_refresh_hook_or_panel_update_is_missing`

Client-side state application appears coupled to UI/presentation refresh.

### vendor_purchase_itemdata_runtime_chain_candidate_v7:network_sync_boundary

- Type: `coupling`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v7`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_promoted_confirmed_chain.md`
- Risk: `receiver_scope_payload_or_ordering_errors_can_create_client_desync`

The chain crosses at least one synchronization/network boundary.

### vendor_purchase_itemdata_runtime_chain_candidate_v7:metadata_sync_contract

- Type: `sync_contract`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v7`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_promoted_confirmed_chain.md`
- Coverage: `1.0`

Metadata mutation should expose a send/apply synchronization path.

### vendor_purchase_itemdata_runtime_chain_candidate_v7:client_apply_to_presentation_contract

- Type: `sync_contract`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v7`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_promoted_confirmed_chain.md`
- Coverage: `1.0`

Client-side state application should have an explicit presentation refresh path when UI is affected.

### vendor_purchase_itemdata_runtime_chain_candidate_v7:ownership_vs_metadata_boundary

- Type: `sync_contract`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v7`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_promoted_confirmed_chain.md`
- Coverage: `1.0`

Inventory ownership/membership and item metadata should remain distinguishable propagation concerns.

### vendor_purchase_itemdata_runtime_chain_candidate_v6:inventory_and_metadata_propagation

- Type: `coupling`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md`
- Risk: `desync_risk_if_one_path_refreshes_without_the_other`

The chain contains both inventory propagation and metadata propagation concerns.

### vendor_purchase_itemdata_runtime_chain_candidate_v6:client_apply_to_ui_refresh

- Type: `coupling`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md`
- Risk: `stale_presentation_if_refresh_hook_or_panel_update_is_missing`

Client-side state application appears coupled to UI/presentation refresh.

### vendor_purchase_itemdata_runtime_chain_candidate_v6:network_sync_boundary

- Type: `coupling`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md`
- Risk: `receiver_scope_payload_or_ordering_errors_can_create_client_desync`

The chain crosses at least one synchronization/network boundary.

### vendor_purchase_itemdata_runtime_chain_candidate_v6:metadata_sync_contract

- Type: `sync_contract`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md`
- Coverage: `1.0`

Metadata mutation should expose a send/apply synchronization path.

### vendor_purchase_itemdata_runtime_chain_candidate_v6:client_apply_to_presentation_contract

- Type: `sync_contract`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md`
- Coverage: `1.0`

Client-side state application should have an explicit presentation refresh path when UI is affected.

### vendor_purchase_itemdata_runtime_chain_candidate_v6:ownership_vs_metadata_boundary

- Type: `sync_contract`
- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
- Confidence: `high`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md`
- Coverage: `1.0`

Inventory ownership/membership and item metadata should remain distinguishable propagation concerns.

## Chain Analyses

### Vendor purchase item metadata propagation

- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v7`
- Confidence: `high`
- Promotion status: `promoted_confirmed_chain`
- Stage count: `8`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_promoted_confirmed_chain.md`

Stages:

- `vendor_open_metadata_assignment` — metadata, vendor
- `vendor_purchase_transfer` — inventory, vendor
- `vendor_metadata_cleanup` — metadata, vendor, server_authority
- `item_metadata_mutation` — metadata, server_authority
- `item_metadata_network_send` — metadata, network
- `inventory_membership_client_apply` — client_apply, inventory
- `item_metadata_client_apply` — metadata, client_apply
- `ui_itemdata_refresh_hook` — metadata, ui, hook_event

Realm / sync transitions:

- `item_metadata_mutation` → `item_metadata_network_send` = `network_sync_boundary`
- `item_metadata_network_send` → `inventory_membership_client_apply` = `network_or_client_sync_boundary`
- `inventory_membership_client_apply` → `item_metadata_client_apply` = `network_or_client_sync_boundary`
- `item_metadata_client_apply` → `ui_itemdata_refresh_hook` = `network_or_client_sync_boundary`

### vendor purchase itemdata propagation chain

- Chain ID: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
- Confidence: `high`
- Promotion status: `promoted_confirmed_chain`
- Stage count: `8`
- Source path: `E:/signalis_ai/docs/runtime/runtime_chains/vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md`

Stages:

- `vendor_open_metadata_assignment` — metadata, vendor
- `vendor_purchase_transfer` — inventory, vendor
- `vendor_metadata_cleanup` — metadata, vendor, server_authority
- `item_metadata_mutation` — metadata, server_authority
- `item_metadata_network_send` — metadata, network
- `inventory_membership_client_apply` — client_apply, inventory
- `item_metadata_client_apply` — metadata, client_apply
- `ui_itemdata_refresh_hook` — metadata, ui, hook_event

Realm / sync transitions:

- `item_metadata_mutation` → `item_metadata_network_send` = `network_sync_boundary`
- `item_metadata_network_send` → `inventory_membership_client_apply` = `network_or_client_sync_boundary`
- `inventory_membership_client_apply` → `item_metadata_client_apply` = `network_or_client_sync_boundary`
- `item_metadata_client_apply` → `ui_itemdata_refresh_hook` = `network_or_client_sync_boundary`

## Next Questions

- Which UI refresh stages are synchronization boundaries versus presentation-only refreshes?
- Which network propagation stages should become explicit synchronization contracts?
- Where should inventory membership and metadata synchronization be documented as separate contracts?
