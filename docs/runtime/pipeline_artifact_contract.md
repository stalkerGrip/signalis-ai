# Pipeline Artifact Contract Registry

- Schema: `pipeline_artifact_contract.v1`
- Generated at: `2026-06-01T18:53:39`
- Scripts: `90`
- Artifacts: `276`

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
| `promotion` | 5 |
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
| `diagnosis` | 2 |
| `ingestion` | 3 |
| `ordered_runtime_facts` | 2 |
| `ordered_steps` | 14 |
| `probe` | 16 |
| `promotion_output` | 6 |
| `ranked_evidence` | 6 |
| `runtime_chain_candidate` | 22 |
| `runtime_chain_regression` | 2 |
| `runtime_fact_graph` | 10 |
| `runtime_fact_topology` | 22 |
| `runtime_facts` | 14 |
| `runtime_steps` | 16 |
| `source_validation` | 8 |
| `targeted_validation_request` | 35 |
| `unknown` | 98 |

## Artifact Statuses

| Status | Count |
|---|---:|
| `canonical` | 4 |
| `debug` | 28 |
| `failed` | 2 |
| `intermediate` | 242 |

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