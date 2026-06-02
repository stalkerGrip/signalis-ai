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
- request_type
- expected_output

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