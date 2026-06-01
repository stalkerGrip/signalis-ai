# vendor purchase itemdata propagation chain

- Slug: `vendor_purchase_itemdata_runtime_chain_candidate_v6`
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
- Candidate artifact: `investigations\validation\vendor_purchase_itemdata_runtime_chain_candidate_v6.json`
- Promotion validation artifact: `investigations\validation\vendor_purchase_itemdata_v6_promotion_validation.json`

## Runtime Chain

- No ordered steps found in candidate artifact.

## Missing Stages

- none

## Caveats

- none

## Superseded Outputs

- none

## Contract Metadata

```json
{
  "schema": "promoted_runtime_chain.md",
  "producer_script": "scripts.investigation.promote_runtime_chain_candidate_v2",
  "pipeline_stage": "promotion",
  "promotion_role": "promotion_core",
  "canonical_status": "canonical",
  "inputs": [
    "investigations\\validation\\vendor_purchase_itemdata_runtime_chain_candidate_v6.json",
    "investigations\\validation\\vendor_purchase_itemdata_v6_promotion_validation.json"
  ]
}
```
