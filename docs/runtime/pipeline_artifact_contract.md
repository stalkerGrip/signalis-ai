# Pipeline Artifact Contract Registry

- Schema: `pipeline_artifact_contract.v1`
- Generated at: `2026-06-01T19:53:45`
- Scripts: `91`
- Artifacts: `295`

## Script Stages

| Stage | Count |
|---|---:|
| `builder` | 10 |
| `diagnosis` | 1 |
| `embedding` | 1 |
| `extraction` | 12 |
| `ingestion` | 3 |
| `normalization` | 2 |
| `probe` | 2 |
| `promotion` | 6 |
| `retrieval` | 1 |
| `runtime_chain_candidate` | 4 |
| `runtime_chain_regression` | 1 |
| `runtime_fact_graph` | 1 |
| `runtime_fact_topology` | 2 |
| `runtime_facts` | 2 |
| `source_validation` | 2 |
| `targeted_validation_request` | 6 |
| `unknown` | 35 |

## Artifact Stages

| Stage | Count |
|---|---:|
| `diagnosis` | 4 |
| `ingestion` | 3 |
| `ordered_runtime_facts` | 4 |
| `ordered_steps` | 14 |
| `probe` | 16 |
| `promotion` | 1 |
| `promotion_output` | 8 |
| `ranked_evidence` | 6 |
| `runtime_chain_candidate` | 24 |
| `runtime_chain_regression` | 2 |
| `runtime_fact_graph` | 12 |
| `runtime_fact_topology` | 24 |
| `runtime_facts` | 16 |
| `runtime_steps` | 16 |
| `source_validation` | 8 |
| `targeted_validation_request` | 35 |
| `unknown` | 102 |

## Artifact Statuses

| Status | Count |
|---|---:|
| `canonical` | 5 |
| `debug` | 30 |
| `failed` | 3 |
| `intermediate` | 257 |

## Contract Flag Format

Scripts may define:

```python
PIPELINE_CONTRACT = {
    "script_id": "scripts.investigation.example",
    "purpose": "What this script does.",
    "pipeline_stage": "runtime_facts",
    "input_schemas": ["targeted_validation_result.v2"],
    "output_schemas": ["runtime_facts.v2"],
    "artifact_patterns": ["investigations/validation/*_runtime_facts_v2.json"],
    "promotion_role": "promotion_core",
    "canonical_status": "active",
}
```

Generated JSON artifacts may define:

```json
{
  "schema": "runtime_facts.v2",
  "producer_script": "scripts.investigation.example",
  "pipeline_stage": "runtime_facts",
  "benchmark": "vendor_purchase_itemdata",
  "promotion_role": "promotion_core",
  "canonical_status": "intermediate",
  "inputs": ["investigations/validation/source_validation.json"]
}
```