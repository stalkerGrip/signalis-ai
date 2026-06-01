# Character load inventory lifecycle propagation

- Slug: `characterload_inventory`
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
- Candidate artifact: `investigations\validation\characterload_inventory_runtime_chain_candidate_v7.json`
- Promotion validation artifact: `investigations\validation\characterload_inventory_promotion_validation_v7.json`

## Runtime Chain

1. `character_choose_network_receive`
2. `pre_player_loaded_char`
3. `player_loaded_char`
4. `inventory_initialization`
5. `player_loadout`
6. `post_player_loadout`

## Missing Stages

- none

## Caveats

- none

## Superseded Outputs

- `E:\signalis_ai\docs\runtime\runtime_chains\characterload_inventory_initialization_lifecycle_chain_promoted_source_validated_chain.md` → `E:\signalis_ai\docs\runtime\runtime_chains\_superseded\characterload_inventory_initialization_lifecycle_chain_promoted_source_validated_chain_superseded_20260602_000641.md`

## Contract Metadata

```json
{
  "schema": "promoted_runtime_chain.md",
  "producer_script": "scripts.investigation.promote_runtime_chain_candidate_v2",
  "pipeline_stage": "promotion",
  "promotion_role": "promotion_core",
  "canonical_status": "canonical",
  "inputs": [
    "investigations\\validation\\characterload_inventory_runtime_chain_candidate_v7.json",
    "investigations\\validation\\characterload_inventory_promotion_validation_v7.json"
  ]
}
```
