# SIGNALIS AI — Orchestration Artifact Families

## Purpose

This document defines the stable orchestration artifact families used by the SIGNALIS AI orchestration pipeline.

Artifact families define pipeline concepts.

Schemas define structure.

Versions are compatibility metadata only.

Pipeline routing, orchestration, discovery, and consumption must use:

- artifact_family
- required_capabilities
- canonical_status
- lineage metadata

not schema version suffixes.

---

## Core Orchestration Flow

Primary flow:

human/local-LLM request
→ orchestration_request
→ retrieval_seed
→ retrieval_result_set
→ evidence_set
→ orchestration_scope
→ doctrine_context_selection
→ retrieval_scope
→ source_validation_request
→ source_validation_result
→ orchestration_context_pack
→ guidance_report

Optional second-pass retrieval:

retrieval_scope
→ retrieval_result_set
→ evidence_set

Optional runtime propagation flow:

runtime_chain_reconstruction_request
→ runtime_chain_candidate
→ promotion_validation
→ promotion_decision

Important correction:

orchestration_scope is evidence-backed.

It must not be generated from hidden request keyword maps, subsystem routing tables, benchmark routing, or manually maintained per-request rules.

If no retrieved/deduplicated evidence supports scope, scope must remain unknown.

Add this section after orchestration_request:

retrieval_seed

Purpose:

Defines safe first-pass retrieval seeds from an orchestration_request.

Required capabilities:

request_text
normalized_request_text
retrieval_seed_queries

Retrieval seed is not scope.

Retrieval seed must not infer:

subsystem
realm
runtime surface
doctrine files
validation targets
implementation files
runtime chain identity

Allowed query seeds:

original request text
normalized request text
explicit user-provided source preferences
explicit user-provided constraints

Do not use hidden keyword maps or subsystem routing tables.

Update orchestration_scope section:

orchestration_scope

Purpose:

Defines evidence-backed scope of work.

Required capabilities:

subsystem_scope
realm_scope
runtime_surface_scope

Rules:

produced after retrieval_result_set and evidence_set in the primary flow
scope is derived from evidence metadata and lineage
scope is not validated truth
scope may contain unknown
if evidence does not expose a scope dimension, output unknown
do not infer scope from request keywords
do not use hidden subsystem routing tables
do not use benchmark-specific routing

---

## orchestration_request

Purpose:

Represents the original user request after normalization.

Required capabilities:

- request_text
- normalized_request_text

Examples:

- bug investigation
- feature change
- architecture question
- performance investigation

---

## orchestration_scope

Purpose:

Defines the inferred scope of work.

Required capabilities:

- subsystem_scope
- realm_scope
- runtime_surface_scope

Examples:

- inventory
- vendor
- storage
- persistence
- networking
- timer

---

## doctrine_context_selection

Purpose:

Defines which doctrine documents should be included.

Required capabilities:

- doctrine_files
- selection_reasoning

Examples:

- inventory.md
- vendor.md
- runtime_doctrine.md
- networking_model.md

---

## retrieval_scope

Purpose:

Defines retrieval planning.

Required capabilities:

- retrieval_queries
- retrieval_targets
- retrieval_reasoning

Retrieval scope is planning.

Retrieval scope is not evidence.

---

## retrieval_result_set

Purpose:

Stores retrieved evidence candidates.

Required capabilities:

- retrieved_documents
- retrieval_metadata

Retrieved evidence is not validated evidence.

---

## evidence_set

Purpose:

Stores deduplicated evidence candidates.

Required capabilities:

- evidence_items
- evidence_sources
- evidence_rank

Evidence is still not validated truth.

---

## source_validation_request

Purpose:

Defines deterministic validation targets.

Required capabilities:

- validation_targets
- validation_reasoning

---

## source_validation_result

Purpose:

Stores validated evidence.

Required capabilities:

- validated_evidence
- authoritative_sources
- validation_status

Validated evidence becomes pipeline truth.

---

## orchestration_context_pack

Purpose:

Primary orchestration product.

Required capabilities:

- request_summary
- doctrine_context
- validated_evidence
- uncertainty_summary
- recommended_next_action

Most requests should terminate here.

---

## guidance_report

Purpose:

Human or LLM consumable guidance.

Required capabilities:

- findings
- risks
- recommendations

---

## runtime_chain_reconstruction_request

Optional.

Used only when propagation reasoning is required.

Required capabilities:

- source_anchor
- target_anchor
- propagation_reasoning

---

## Runtime Chain Rule

Runtime chain generation is optional.

Use runtime chains for:

- desync
- lifecycle ordering
- item ownership transfer
- metadata propagation
- persistence flow
- hook propagation
- network replication

Do not force every request into a runtime chain.

---

## Architecture Rule

The orchestration pipeline exists to produce:

orchestration_context_pack
→ guidance_report

Runtime chains are downstream specialist artifacts.

They are not the default orchestration output.

# SIGNALIS AI — Orchestration Request Contract

## Purpose

Defines the stable artifact family:

orchestration_request

This artifact represents a normalized human or local-LLM request.

The orchestration_request artifact is the entry point for the orchestration pipeline.

It is normalization only.

It does not select subsystem scope, doctrine context, retrieval scope, validation targets, or runtime chains.

---

## Artifact Family

artifact_family:

orchestration_request

schema:

orchestration_request

schema_version:

compatibility metadata only

Schema version must not control routing, discovery, orchestration, or script compatibility.

---

## Required Capabilities

Every orchestration_request must contain:

- request_text
- normalized_request_text

An artifact lacking either required capability is not a valid orchestration_request.

---

## Required Metadata

Every orchestration_request must contain:

- schema
- schema_version
- artifact_family
- artifact_id
- producer_script
- pipeline_stage
- canonical_status
- promotion_role
- generated_at
- required_capabilities

Required fixed values:

artifact_family:
orchestration_request

schema:
orchestration_request

pipeline_stage:
orchestration

promotion_role:
context_or_debug

canonical_status:
intermediate

---

## Artifact ID Rule

artifact_id must be deterministic.

Recommended format:

orchestration_request:<stable_request_hash>

The stable request hash should be derived from:

- artifact_family
- request_text

Do not derive artifact identity from:

- filename
- output path
- schema version
- benchmark name
- subsystem guess
- request classification
- expected downstream output

---

## request_text

Purpose:

Preserve the original request.

Rules:

- preserve user intent
- preserve important terminology
- do not inject assumptions
- do not rewrite into subsystem-specific language

---

## normalized_request_text

Purpose:

Provide a lightly normalized version for downstream consumption.

Rules:

- fix whitespace
- preserve meaning
- preserve domain terms
- do not add inferred subsystem scope
- do not add inferred root cause

---

## Optional Capabilities

Optional capabilities may exist without changing the artifact family.

Allowed optional fields:

- user_constraints
- urgency
- source_preferences
- subsystem_hints
- uncertainty

Optional capabilities must never become mandatory through schema evolution.

---

## Lineage Requirements

Every orchestration_request must include lineage metadata:

lineage.input_kind:
human_request or local_llm_request

lineage.input_artifacts:
empty unless generated from another artifact

lineage.parent_artifact_id:
null unless regenerated from another orchestration artifact

lineage.regenerates:
null unless this artifact intentionally replaces an earlier request artifact

lineage.regeneration_inputs:
the minimum inputs needed to deterministically regenerate the artifact

Required regeneration inputs:

- request_text
- producer_script
- schema
- schema_version

---

## Regeneration Rule

orchestration_request must be reproducible from:

- original request text
- producer script
- schema contract
- deterministic classification rules

Generated orchestration_request artifacts must not be manually patched.

If output is wrong:

- fix request classification logic
- fix metadata generation
- fix doctrine
- regenerate

---

## Request Interpretation Rule

orchestration_request must not:

- select subsystems
- select doctrine
- perform retrieval
- perform validation
- build runtime chains
- decide implementation files
- decide source validation targets

Those responsibilities belong to downstream artifact families.

---

## Stability Rule

The orchestration_request artifact family is stable.

Future schema changes must preserve:

- request_text
- request_type
- expected_output

Compatibility adapters should be preferred over creating new orchestration request families.

Schema versions are compatibility metadata only.

---

## Output Rule

The output of orchestration_request should be sufficient for:

orchestration_scope

generation.

Nothing more.

# Orchestration Scope Contract

## Purpose

Defines the stable artifact family:

orchestration_scope

This artifact represents the inferred scope of work for a normalized orchestration_request.

The orchestration_scope artifact is a planning/control artifact.

It does not select doctrine files, generate retrieval queries, perform source validation, produce runtime chains, or provide implementation guidance.

---

## Artifact Family

artifact_family:

orchestration_scope

schema:

orchestration_scope

schema_version:

compatibility metadata only

Schema version must not control routing, discovery, orchestration, or script compatibility.

---

## Required Capabilities

Every orchestration_scope must contain:

- subsystem_scope
- realm_scope
- runtime_surface_scope

An artifact lacking any required capability is not a valid orchestration_scope.

---

## Required Metadata

Every orchestration_scope must contain:

- schema
- schema_version
- artifact_family
- artifact_id
- producer_script
- pipeline_stage
- canonical_status
- promotion_role
- generated_at
- required_capabilities
- input_artifacts
- upstream_artifact_ids
- lineage

Required fixed values:

artifact_family:

orchestration_scope

schema:

orchestration_scope

pipeline_stage:

orchestration

promotion_role:

context_or_debug

canonical_status:

intermediate

---

## Artifact ID Rule

artifact_id must be deterministic.

Recommended format:

orchestration_scope:<stable_scope_hash>

The stable scope hash must be derived from:

- artifact_family
- producer_script
- upstream orchestration_request artifact_id
- normalized_request_text
- external orchestration_index digest when present
- generated scope payload

Do not derive artifact identity from:

- filename
- output path
- schema version
- benchmark name
- subsystem guess alone
- request classification alone
- expected downstream output alone

---

## subsystem_scope

Purpose:

Record candidate subsystems involved in the request.

Rules:

- generated from request artifact plus external evidence/index signals
- may contain `unknown` when evidence is insufficient
- must preserve confidence and reasoning
- must not be treated as validated truth
- must not be produced from hidden subsystem routing tables inside Python

Each subsystem scope item should contain:

- scope_id
- display_name
- confidence
- evidence_source
- matched_aliases
- source_artifact
- source_family
- reason

---

## realm_scope

Purpose:

Record likely execution realms involved in the request.

Allowed scope_id examples:

- server
- client
- shared
- cross_realm
- unknown

Rules:

- realm uncertainty must remain explicit
- do not silently assume client authority
- do not silently assume server authority without evidence
- networking/cross-realm scope is a planning signal, not proof

Each realm scope item should contain:

- scope_id
- display_name
- confidence
- evidence_source
- matched_aliases
- source_artifact
- source_family
- reason

---

## runtime_surface_scope

Purpose:

Record likely runtime surfaces involved in the request.

Allowed scope_id examples:

- hook_event
- network_message
- timer_scheduler
- ui_derma
- hud
- entity_simulation
- inventory_ownership
- item_metadata
- persistence
- command_config
- database_state
- unknown

Rules:

- runtime surfaces guide downstream doctrine and retrieval selection
- runtime surfaces are not source validation targets by themselves
- runtime chain reconstruction is only requested later when propagation reasoning is required

Each runtime surface scope item should contain:

- scope_id
- display_name
- confidence
- evidence_source
- matched_aliases
- source_artifact
- source_family
- reason

---

## Required Capabilities Are Not Routing Tables

The three required scope capabilities define artifact structure only.

They must not become hardcoded routing tables.

Downstream consumers must use:

- artifact_family
- required_capabilities
- canonical_status
- lineage
- scope item confidence
- scope item evidence_source

not schema version suffixes or benchmark names.

---

## Lineage Requirements

Every orchestration_scope must include lineage metadata:

lineage.input_kind:

orchestration_request

lineage.input_artifacts:

at least the upstream orchestration_request JSON artifact path

lineage.parent_artifact_id:

upstream orchestration_request artifact_id

lineage.regenerates:

null unless this artifact intentionally replaces an earlier orchestration_scope

lineage.regeneration_inputs:

the minimum inputs needed to deterministically regenerate the artifact

Required regeneration inputs:

- orchestration_request_artifact_id
- orchestration_request_digest
- orchestration_index_digest when present
- producer_script
- schema
- schema_version

---

## Capability-Based Consumption Rule

A consumer may consume orchestration_scope only when:

- artifact_family == orchestration_scope
- required_capabilities contains subsystem_scope
- required_capabilities contains realm_scope
- required_capabilities contains runtime_surface_scope
- canonical_status is not failed, legacy, superseded, or debug unless explicitly allowed
- lineage.parent_artifact_id points to an orchestration_request artifact

A consumer must not consume orchestration_scope by:

- exact schema version suffix
- filename pattern only
- benchmark name
- subsystem name alone
- request wording alone

---

## Prohibited Behavior

orchestration_scope must not introduce:

- benchmark-specific routing
- subsystem-specific routing tables
- hidden keyword maps
- version-coupled orchestration
- doctrine file selection
- retrieval query generation
- source validation targets
- runtime chain generation
- implementation guidance

---

## Regeneration Rule

orchestration_scope must be reproducible from:

- upstream orchestration_request artifact
- producer script
- schema contract
- optional external orchestration_index artifact

Generated orchestration_scope artifacts must not be manually patched.

If output is wrong:

- fix the producer script
- fix the external orchestration_index producer
- fix the scope contract
- regenerate

---

## Output Rule

The output of orchestration_scope should be sufficient for:

doctrine_context_selection

and later retrieval_scope planning.

Nothing more.
