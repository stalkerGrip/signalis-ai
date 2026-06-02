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

Only NEW scripts and MAJOR REWRITES
must contain PIPELINE_CONTRACT.

Old scripts are grandfathered.

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

## Legacy Script Rule

The contract system is forward-looking.

Existing scripts created before the contract system was introduced are considered legacy scripts.

Legacy scripts do not need to be retrofitted with PIPELINE_CONTRACT metadata.

The registry builder may infer metadata for legacy scripts.

Mandatory PIPELINE_CONTRACT metadata applies only to:

- newly created scripts
- major script rewrites
- replacement scripts
- pipeline infrastructure scripts

This prevents large-scale retrofitting work from becoming a bottleneck.

Pipeline progress takes priority over historical contract coverage.

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

## Stable Artifact Family Rule

Pipeline architecture must be built around stable artifact families and capability contracts.

Artifact family names define pipeline concepts.

Schema names describe artifact structure.

Schema versions must not define routing, orchestration, discovery, or script compatibility.

Do not create version-driven pipeline architecture.

Bad:

- runtime_chain_candidate.v5
- runtime_chain_candidate.v6
- runtime_chain_candidate.v7
- retrieval_plan.v1
- retrieval_plan.v2
- retrieval_plan.v3
- orchestration_context_pack.v2

when these names are used as script dependencies or pipeline concepts.

Correct:

artifact_family:
runtime_chain_candidate

schema:
runtime_chain_candidate

required_capabilities:
- ordered_runtime_facts_input
- propagation_chain_candidate
- validation_backed

Pipeline design must reason about:

artifact_family
+
required_capabilities
+
lineage
+
canonical_status

not version suffixes.

## Canonical Orchestration Artifact Families

Preferred orchestration families:

- orchestration_request
- orchestration_scope
- doctrine_context_selection
- retrieval_scope
- retrieval_result_set
- evidence_set
- source_validation_request
- source_validation_result
- orchestration_context_pack
- guidance_report

Optional families:

- runtime_chain_reconstruction_request
- runtime_chain_candidate
- promotion_validation
- promotion_decision

Runtime chains are not mandatory outputs.

Many requests should terminate at:

orchestration_context_pack
→ guidance_report

without chain reconstruction.

## Version-Coupling Prohibition

Scripts must not depend on exact schema version suffixes.

Bad:

input_schemas:
- runtime_chain_candidate.v7

output_schemas:
- runtime_chain_candidate.v7

Good:

input_families:
- runtime_chain_candidate

required_capabilities:
- propagation_chain_candidate
- validation_backed

Schema versions are compatibility metadata only.

Pipeline orchestration, routing, discovery, and consumption must use:

- artifact_family
- required_capabilities
- canonical_status
- lineage metadata

Version numbers must never define pipeline behavior.

Breaking schema changes must be handled through:

- compatibility adapters
- explicit migration
- producer regeneration

not parallel versioned pipeline paths.

## Artifact Creation Rule

Do not create a new artifact family when:

- adding metadata
- adding validation
- changing ranking logic
- changing orchestration logic
- changing retrieval strategy
- changing schema layout

Prefer capability-compatible schema evolution or explicit migration over new artifact families.

Do not create multiple families for the same conceptual artifact.

Bad:

- retrieval_context_pack
- investigation_context_pack
- architecture_context_pack
- orchestration_context_pack

when they represent the same orchestration context product.

Correct:

artifact_family:
orchestration_context_pack

capabilities:
- retrieval_evidence
- doctrine_context
- validation_summary
- guidance_ready

## Regeneration Rule

Long-term artifacts should be reproducible from upstream evidence.

Do not create artifact families that exist only to preserve intermediate reasoning.

Prefer:

evidence
→ validation
→ regeneration

over permanent chains of derived artifacts.

Generated artifacts are disposable if they can be reproduced from authoritative upstream evidence.

The pipeline should regenerate truth from evidence whenever possible.

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

## Doctrine Hierarchy Rule

When planning or modifying pipeline work, doctrine files must be applied in this order:

1. `human_context.md`
2. `project_memory.md`
3. `pipeline_artifact_doctrine.md`
4. `pipeline_artifact_contract.json`
5. `script_contracts.md`
6. `runtime_chain_promotion.md`
7. `runtime_propagation_doctrine.md`
8. subsystem doctrine files

`human_context.md` is first for authority rules and human-validated behavior, but SIGNALIS source code still wins for exact implementation behavior.

`project_memory.md` controls current phase, current bottleneck, completed bottlenecks, and active direction.

`pipeline_artifact_doctrine.md` controls permanent pipeline governance, script ownership, artifact ownership, architecture-first implementation, and cross-chat recovery.

`pipeline_artifact_contract.json` controls machine-readable script/artifact ownership and promotion compatibility.

`script_contracts.md` controls actual CLI usage and prevents invented script names or arguments.

Runtime and subsystem doctrine explain semantics, but they must not override source authority, current bottleneck, or artifact governance.

If these sources conflict:

* human-validated behavior wins over generated artifacts
* doctrine wins over generated summaries
* contract registry wins over memory for script/artifact ownership
* script contracts win over guessed CLI usage
* current bottleneck wins over tempting side quests

Before proposing code, commands, or artifact promotion, check the highest applicable authority in this hierarchy.

Do not reconstruct script names, artifact paths, or pipeline state from memory when contract or script-contract artifacts exist.

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

## Code Generation Markup Safety Rule

Problem:

ChatGPT responses frequently corrupt code when multiple markup layers are nested:

* Markdown code block containing Markdown code block
* Python triple-quoted string containing Markdown fences
* Markdown examples containing triple backticks
* JSON examples inside Markdown inside Python

These corruptions are difficult to detect and cause copy-paste failures.

### Rule 1

Never demonstrate Markdown fences inside another Markdown fence.

Bad:

[Markdown block]
`python
    text = '''
    `text
value
`     '''
    `
[/Markdown block]

### Rule 2

When generating Python that writes Markdown:

Do not use large triple-quoted templates.

Avoid:

Python:
summary = f"""..."""

Prefer:

Python:
lines = []
lines.append(...)
path.write_text("\n".join(lines))

### Rule 3

When discussing code that itself contains code fences:

Use indentation examples or pseudocode.

Do not emit nested triple-backtick examples.

### Rule 4

For copy-paste script delivery:

Prefer:

* exact replacement blocks
* complete functions
* complete files

Avoid:

* partial multiline fragments
* snippets that start/end inside a string literal

### Rule 5

If a response contains:

* Python
* Markdown generation
* JSON generation

then perform a "markup safety check":

Verify:

* all quotes balanced
* all parentheses balanced
* all braces balanced
* all Markdown fences balanced
* no nested Markdown fences

### Rule 6

Canonical SIGNALIS pipeline scripts should use:

Python:
lines: list[str]

for Markdown generation.

This is the preferred architecture pattern.

Reason:

Deterministic generation is more important than concise generation.

Copy-paste reliability is a pipeline requirement.

## Promoted runtime chains are first-class retrieval artifacts.

A promoted runtime chain must flow through:

promotion decision
→ promoted runtime chain registry
→ runtime chain corpus
→ qdrant embeddings
→ qdrant ingestion
→ retrieval validation

Promotion is not complete until the promoted chain is retrievable by chain_id and promotion_status.

## Incremental Pipeline Execution Rule

For multi-stage pipeline work:

Do not generate future commands based on assumed intermediate outputs.

Execute one stage at a time.

Workflow:

1. Provide exactly one command or one inspection step.
2. Wait for actual output.
3. Re-evaluate using the output.
4. Provide the next step.

Prefer evidence-driven progression over predicted pipeline paths.

This is mandatory when:

- promotion workflows
- contract workflows
- retrieval workflows
- validation workflows
- artifact generation workflows

Never assume:

- artifact existence
- artifact schema
- script arguments
- script outputs

until verified from actual execution.

## Benchmark Generalization Rule

Vendor and characterload are benchmark datasets.

They are not infrastructure templates.

Do not hardcode benchmark-specific stages into generic pipeline scripts.

Benchmark-specific logic may exist only as:

* configuration
* stage-rule files
* test fixtures
* benchmark fixtures

not as hidden constants inside generic scripts.

Required direction:

```text
source validation
→ runtime fact extraction
→ runtime fact sequencing
→ runtime chain candidate building
```

must accept explicit stage-rule input.

Generic scripts should consume:

```text
stage_rule_set.v1
```

rather than hardcoded stage names.

Allowed benchmark rule files:

```text
docs/runtime/stage_rules/vendor_purchase_itemdata_stage_rules.json
docs/runtime/stage_rules/characterload_inventory_stage_rules.json
```

or equivalent configured paths.

Rule files define:

* benchmark key
* stage order
* stage descriptions
* classification needles
* expected realms
* expected kinds
* required / optional stages
* promotion compatibility

Promotion must record which stage-rule set was used.

A promoted runtime chain is invalid if its stage order came from hidden benchmark-specific script constants.

Vendor and characterload should remain regression benchmarks for the generic pipeline, not special-case infrastructure.

### Infrastructure Direction

Current hardcoded benchmark implementations:

* build_runtime_facts_from_source_validation.py
* runtime_fact_sequencer.py
* build_runtime_chain_candidate_v6.py

These scripts must be migrated to consume:

```text
stage_rule_set.v1
```

through explicit inputs rather than embedded benchmark rules.

Target architecture:

```text
benchmark targets
    ↓
source validation
    ↓
runtime facts
    ↓
stage rules
    ↓
ordered runtime facts
    ↓
runtime chain candidate
    ↓
promotion validation
    ↓
promoted runtime chain
```

Benchmark-specific knowledge belongs in stage-rule artifacts, not in pipeline infrastructure.

## Stage Rule Set Rule

Runtime fact classification and ordering must be data-driven.

Benchmark-specific stage ordering must live in stage-rule artifacts, not inside generic scripts.

Stage-rule artifacts use:

`stage_rule_set.v1`

Stage rules are consumed after runtime facts are generated:

source validation
→ runtime facts
→ stage rules
→ ordered runtime facts
→ runtime chain candidate
→ promotion

Stage rules may classify, require, order, or reject stages.

Stage rules must not invent runtime facts.

Promotion-compatible runtime chain candidates must record which stage_rule_set was used.

## Architecture-First Implementation Rule

Pipeline work must prefer architecturally reusable solutions over benchmark-specific fixes.

Benchmarks such as vendor purchase item data and characterload inventory are regression fixtures.

They are not infrastructure design targets.

When a benchmark exposes a failure, the preferred response is:

1. identify the generic pipeline stage that failed
2. move benchmark-specific knowledge into data artifacts
3. keep scripts generic
4. add only the minimum one-time migration or compatibility code needed
5. validate the benchmark as a regression

Do not over-optimize a single benchmark rule set.

Do not hardcode vendor, characterload, storage, or other subsystem behavior into generic scripts.

Allowed one-time scripts:

* migration helpers
* artifact inspectors
* compatibility converters
* contract repair utilities
* regression setup utilities

One-time scripts must not become promotion-critical unless later generalized and registered.

Preferred long-term pattern:

runtime facts
→ neutral facts

stage rules
→ declarative classification and ordering

sequencer
→ generic rule engine

chain candidate builder
→ generic ordered-fact consumer

promotion
→ deterministic validation and registry update

Architecture goal:

Each fix should improve future investigation orchestration, not only make the current benchmark pass.

## Schema-Driven Discovery Rule

Permanent pipeline scripts must not discover canonical artifacts by filename version when a stable schema exists.

Preferred discovery order:

1. scan candidate JSON artifacts broadly
2. load JSON
3. filter by `schema`
4. filter by `canonical_status`
5. filter by semantic status fields such as promotion decision
6. resolve artifact lineage from explicit metadata and `inputs` / `outputs`

Filename patterns may be used only as a broad search optimization, not as authority.

Versioned filename filters such as `_v6`, `_v7`, or `_promotion_decision_v2` are allowed only in one-time migration or diagnostic scripts.

Stable infrastructure scripts must survive future artifact versions without code edits when the schema contract remains compatible.

## Stable Pipeline Rule

When a pipeline stage is considered operational:

Do not investigate generated artifacts first.

Investigate the producer script first.

Artifact review remains useful for diagnosis, but fixes should be applied to the producer whenever possible.

Preferred order:

Producer Script
→ Contract
→ Registry
→ Generated Artifact

not

Generated Artifact
→ Manual Cleanup

Manual artifact cleanup is allowed only for migration, archival, or corruption recovery.

## Artifact Lineage Metadata Rule

Stable long-term pipeline artifacts should carry explicit lineage metadata.

Preferred fields:

- logical_chain_id
- chain_id
- artifact_version
- candidate_version
- producer_script
- source_schema
- input_artifacts
- supersedes
- superseded_by
- canonical_status
- promotion_role

Producer scripts must prefer explicit lineage metadata over filename inference.

Allowed fallback order:

1. explicit artifact metadata
2. upstream artifact metadata
3. pipeline contract metadata
4. normalized benchmark name
5. filename inference

Filename inference is last-resort compatibility behavior, not primary governance.

Registry and retrieval scripts should dedupe by explicit logical identity when available.

Generated artifacts must not be manually patched to add lineage metadata.
Fix producer scripts and regenerate.

## Orchestration Governance Rule

The active pipeline must be request-driven.

A human/local-LLM request should produce generated artifacts through orchestration, not through manually maintained per-chain definitions.

Manual doctrine files may define:

- source authority
- subsystem meaning
- legacy vs authoritative notes
- orchestration rules
- artifact governance

Manual doctrine files should not define every small runtime chain.

Concrete runtime chains, retrieval scopes, validation requests, and context packs are generated evidence artifacts.

Runtime chain reconstruction is optional and should only run when propagation reasoning is needed.

## Artifact Lineage Identity Rule

Active pipeline code must not infer logical artifact identity from:

- filenames
- artifact paths
- benchmark names embedded in filenames
- candidate version suffixes
- promoted markdown output names

Permanent precedence:

1. explicit artifact metadata
2. contract registry metadata
3. explicit CLI migration override, clearly marked as migration-only
4. fail clearly

Filename/path inference is forbidden for active lineage decisions.

Generated artifacts must not be manually patched to add missing lineage.

If lineage metadata is missing:

1. fix the earliest producer script that should have emitted it
2. regenerate the artifact
3. regenerate downstream artifacts

Required lineage metadata for chain-specific artifacts:

```json
{
  "schema": "...",
  "artifact_id": "...",
  "logical_chain_id": "...",
  "artifact_role": "...",
  "producer_script": "...",
  "pipeline_stage": "...",
  "promotion_role": "...",
  "canonical_status": "...",
  "generated_at": "...",
  "input_artifacts": [],
  "lineage_source": "input_metadata|producer_metadata|cli_migration"
}
```

## Orchestration Artifact Rule

Request-driven orchestration is the active pipeline entry point.

The orchestrator may generate:

- orchestration request
- retrieval scope
- doctrine context selection
- source validation request
- source validation result
- context pack
- optional runtime chain artifacts

These are generated evidence/control artifacts, not doctrine.

Do not manually patch orchestration outputs.

Do not require human-maintained definitions for every concrete runtime chain.

Runtime chains are generated only when propagation reasoning is required.

Artifact family names are stable pipeline concepts.
Schema versions are compatibility contracts.
Do not create new artifact families or script generations only because an implementation changed.