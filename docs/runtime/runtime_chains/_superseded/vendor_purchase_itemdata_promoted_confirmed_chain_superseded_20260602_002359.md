# Vendor purchase item metadata propagation

- Slug: `vendor_purchase_itemdata`
- Promotion decision: `promoted_confirmed_chain`
- Reason: promotion validation passed and candidate has medium/high confidence with no missing stages
- Confidence: `high`
- Score: `1.0`
- Validation passed: `True`
- Deterministic regeneration: `True`
- Supported links: `0`
- Unsupported links: `0`
- Topology artifact: `manifests/normalized/runtime_propagation_topology.json`
- Source validation artifact: `unknown`
- Runtime facts artifact: `unknown`
- Candidate artifact: `investigations\validation\vendor_purchase_itemdata_runtime_chain_candidate_v7.json`
- Promotion validation artifact: `investigations\validation\vendor_purchase_itemdata_promotion_validation_v7.json`

## Runtime Chain

1. `vendor_open_metadata_assignment`
2. `vendor_purchase_transfer`
3. `vendor_metadata_cleanup`
4. `item_metadata_mutation`
5. `item_metadata_network_send`
6. `inventory_membership_client_apply`
7. `item_metadata_client_apply`
8. `ui_itemdata_refresh_hook`

## Missing Stages

- none

## Caveats

- none

## Superseded Outputs

- `E:\signalis_ai\docs\runtime\runtime_chains\vendor_purchase_itemdata_propagation_chain_promoted_confirmed_chain.md` → `E:\signalis_ai\docs\runtime\runtime_chains\_superseded\vendor_purchase_itemdata_propagation_chain_promoted_confirmed_chain_superseded_20260602_000644.md`
- `E:\signalis_ai\docs\runtime\runtime_chains\vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain.md` → `E:\signalis_ai\docs\runtime\runtime_chains\_superseded\vendor_purchase_itemdata_runtime_chain_candidate_v6_promoted_confirmed_chain_superseded_20260602_000644.md`

## Contract Metadata

```json
{
  "schema": "promoted_runtime_chain.md",
  "producer_script": "scripts.investigation.promote_runtime_chain_candidate_v2",
  "pipeline_stage": "promotion",
  "promotion_role": "promotion_core",
  "canonical_status": "canonical",
  "inputs": [
    "investigations\\validation\\vendor_purchase_itemdata_runtime_chain_candidate_v7.json",
    "investigations\\validation\\vendor_purchase_itemdata_promotion_validation_v7.json"
  ]
}
```
