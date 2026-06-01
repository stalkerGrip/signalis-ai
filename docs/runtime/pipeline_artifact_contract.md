# Pipeline Artifact Contract Registry

- Schema: `pipeline_artifact_contract.v1`
- Generated at: `2026-06-01T23:55:54`
- Scripts: `88`
- Artifacts: `135`

## Script Stages

| Stage | Count |
|---|---:|
| `architecture_intelligence` | 1 |
| `builder` | 10 |
| `diagnosis` | 1 |
| `embedding` | 1 |
| `extraction` | 12 |
| `ingestion` | 3 |
| `normalization` | 2 |
| `ordered_runtime_facts` | 2 |
| `probe` | 2 |
| `promotion` | 4 |
| `retrieval` | 3 |
| `runtime_chain_candidate` | 5 |
| `runtime_chain_regression` | 1 |
| `runtime_fact_graph` | 1 |
| `runtime_fact_topology` | 2 |
| `runtime_facts` | 2 |
| `source_validation` | 1 |
| `targeted_validation_request` | 5 |
| `unknown` | 30 |

## Artifact Stages

| Stage | Count |
|---|---:|
| `diagnosis` | 2 |
| `ingestion` | 3 |
| `ordered_runtime_facts` | 5 |
| `promotion` | 2 |
| `promotion_output` | 5 |
| `runtime_chain_candidate` | 26 |
| `runtime_chain_regression` | 1 |
| `runtime_fact_graph` | 4 |
| `runtime_fact_topology` | 11 |
| `runtime_facts` | 9 |
| `source_validation` | 5 |
| `targeted_validation_request` | 12 |
| `tooling` | 1 |
| `unknown` | 49 |

## Artifact Statuses

| Status | Count |
|---|---:|
| `canonical` | 8 |
| `debug` | 2 |
| `intermediate` | 125 |

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