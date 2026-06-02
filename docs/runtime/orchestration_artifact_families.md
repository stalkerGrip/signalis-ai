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

human/local-LLM request
→ orchestration_request
→ orchestration_scope
→ doctrine_context_selection
→ retrieval_scope
→ retrieval_result_set
→ evidence_set
→ source_validation_request
→ source_validation_result
→ orchestration_context_pack
→ guidance_report

Optional:

→ runtime_chain_reconstruction_request
→ runtime_chain_candidate
→ promotion_validation
→ promotion_decision

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