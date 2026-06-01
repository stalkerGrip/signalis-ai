# SIGNALIS AI — Pipeline Artifact Doctrine

## Purpose

This document defines permanent rules for:

* script ownership
* artifact ownership
* pipeline contract tracking
* cross-chat context recovery

This file is human-maintained and must never be generated.

Generated files are outputs, not doctrine.

---

## Generated File Rule

The following files are generated artifacts:

```text
docs/runtime/script_contracts.md
docs/runtime/script_contracts.json

docs/runtime/pipeline_artifact_contract.md
docs/runtime/pipeline_artifact_contract.json

investigations/validation/pipeline_contract_check_v1.md
investigations/validation/pipeline_contract_check_v1.json
```

Generated files must not be manually edited to install doctrine.

If generated output is incorrect:

```text
Fix the generating script.
OR
Fix explicit contract metadata.
THEN
Regenerate.
```

Do not patch generated outputs by hand.

---

## Script Folder Ownership

Canonical script ownership:

```text
scripts/tools
    = pipeline infrastructure
    = registry generation
    = contract validation
    = repository-wide tooling

scripts/investigation
    = investigation workflow
    = validation
    = runtime facts
    = runtime chains
    = promotion experiments
    = investigation diagnostics

scripts/qdrant
    = retrieval infrastructure
    = embeddings
    = ingestion
    = reranking
    = context packs
    = retrieval validation

scripts/extraction
    = raw Lua extraction
    = manifest generation

scripts/normalization
    = normalization
    = graph construction
    = topology construction
```

A script belongs in `scripts/tools` when it manages pipeline infrastructure rather than performing an investigation step.

Examples:

```text
scripts/tools/build_pipeline_contract_registry.py
scripts/tools/check_pipeline_contracts.py
```

---

## Pipeline Contract Rule

Every pipeline-stable script must be contract-addressable.

Scripts should declare:

```python
PIPELINE_CONTRACT = {
    "script_id": "scripts.investigation.example",
    "purpose": "What this script does.",
    "pipeline_stage": "runtime_facts",
    "input_schemas": [
        "targeted_validation_result.v2"
    ],
    "output_schemas": [
        "runtime_facts.v2"
    ],
    "artifact_patterns": [
        "investigations/validation/*_runtime_facts_v2.json"
    ],
    "promotion_role": "promotion_core",
    "canonical_status": "active"
}
```

Registry generation must prefer explicit contract flags over inference.

---

## Artifact Metadata Rule

Generated JSON artifacts should contain:

```json
{
  "schema": "runtime_facts.v2",
  "producer_script": "scripts.investigation.example",
  "pipeline_stage": "runtime_facts",
  "benchmark": "vendor_purchase_itemdata",
  "promotion_role": "promotion_core",
  "canonical_status": "intermediate",
  "inputs": [
    "investigations/validation/source_validation.json"
  ]
}
```

Artifact metadata is authoritative for:

```text
producer
pipeline stage
benchmark
promotion role
canonical status
artifact lineage
```

Registry generation must prefer explicit artifact metadata over filename inference.

---

## Contract Validation Rule

Before promotion work:

```powershell
python -m scripts.tools.build_pipeline_contract_registry --workspace E:\signalis_ai

python -m scripts.tools.check_pipeline_contracts --workspace E:\signalis_ai
```

Contract validation must pass before promotion decisions are accepted.

---

## Promotion Compatibility Rule

Promotion decisions must not rely on artifacts marked:

```text
debug
failed
legacy
superseded
```

Generic artifacts:

```text
generic_runtime_facts
generic_runtime_fact_graph
generic_runtime_fact_topology
```

must not be used as full-chain promotion evidence unless explicitly marked compatible.

---

## Cross-Chat Recovery Rule

Before planning work, future chats must recover context in the following order:

```text
1. project_memory.md

2. pipeline_artifact_doctrine.md

3. script_contracts.md

4. pipeline_artifact_contract.md

5. runtime_chain_promotion.md

6. runtime_propagation_doctrine.md

7. relevant subsystem doctrine
```

Do not reconstruct script or artifact lineage from memory when contract artifacts already exist.

Generated contract artifacts are the authoritative machine-readable source.

---

## Current Contract Infrastructure

Current contract tooling:

```text
scripts/tools/build_pipeline_contract_registry.py

scripts/tools/check_pipeline_contracts.py
```

These scripts are pipeline infrastructure.

They are not investigation workflow scripts.

---

## Contract First Principle

When uncertainty exists about:

```text
what a script does
what an artifact does
which artifact is canonical
which artifact supersedes another
which artifact is promotion-valid
```

consult:

```text
pipeline_artifact_contract.json
```

before inspecting investigation outputs.

The contract registry is the canonical machine-readable source for script and artifact ownership.

Investigation outputs are evidence.

The registry defines how evidence is organized.
