# SIGNALIS AI — Orchestration Doctrine

## Purpose

This document defines how SIGNALIS AI turns a human/local-LLM request into deterministic retrieval, validation, and context artifacts.

The goal is not to manually define every possible runtime chain.

The goal is request-driven orchestration:

human/local-LLM request
→ interpreted scope
→ doctrine context
→ retrieval plan
→ validation plan
→ context pack
→ optional runtime chain reconstruction
→ implementation or investigation guidance

## Core Rule

The orchestrator does not define truth.

The orchestrator decides what evidence to gather and how to package it.

Truth rules live in:

- human_context.md
- pipeline_artifact_doctrine.md
- runtime_doctrine.md
- runtime_propagation_doctrine.md
- subsystem doctrine/docs

The orchestrator must consume those rules, not duplicate or override them.

## Intelligence Layer Rule

The orchestrator is not a monolithic AI agent.

It coordinates four layers:

```text
Local LLM

RAG

Pipeline Scripts

Architect AI
```

Responsibilities:

```text
Local LLM
- normalize requests
- generate retrieval candidates
- draft orchestration artifacts
- generate reports and code from validated context

RAG
- retrieve doctrine
- retrieve subsystem documents
- retrieve topology summaries
- retrieve promoted runtime chains
- retrieve validation artifacts

Pipeline Scripts
- generate deterministic artifacts
- execute retrieval
- perform source validation
- preserve lineage
- enforce artifact-family contracts

Architect AI
- review doctrine compliance
- review architecture decisions
- perform cross-system reasoning
- evaluate risks
- review generated patches
- synthesize guidance reports
```

Truth hierarchy:

```text
Source Code
>
Validated Artifacts
>
Retrieved Evidence
>
Architect Reasoning
>
Local LLM Interpretation
```

RAG results are evidence candidates.

Architect AI reasoning is guidance.

Neither becomes truth until supported by validated evidence.

## Main Input

The main input is a natural-language request.

Examples:

- update HUD stamina warning
- why vendor price label stays after purchase
- add storage behavior for locked containers
- optimize generator simulation
- find why inventory desyncs after character load

## Main Output

The main output is a context pack for an LLM or developer.

A valid context pack should include:

- original request
- interpreted request intent
- likely subsystems
- likely realms
- likely runtime surfaces
- selected doctrine context
- retrieval queries
- retrieved evidence summary
- source validation targets
- source validation results when available
- risks and unknowns
- recommended next action

## Orchestration Pipeline

Primary flow:

Request
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

Rationale:

First-pass scope cannot be reliable without evidence unless a deterministic scope index already exists.

Therefore the primary orchestration path performs broad retrieval first, deduplicates/ranks evidence, then derives orchestration_scope from evidence metadata.

orchestration_scope is a planning artifact, not validated truth.

If evidence is missing or lacks scope metadata, scope must remain explicit unknown.

The orchestrator must not infer scope from request text keywords, benchmark names, subsystem routing tables, or hidden Python maps.

Add:

Retrieval Seed Rule

retrieval_seed is the only artifact allowed to be generated directly from orchestration_request before evidence exists.

It may preserve:

original request text
normalized request text
explicit user constraints
explicit source preferences

It must not infer:

subsystem
realm
runtime surface
doctrine context
validation targets
implementation files
runtime chain identity

Add:

Evidence-Backed Scope Rule

orchestration_scope must be generated from evidence_set, not from request keywords.

Valid scope sources:

retrieved document metadata
artifact_family
required_capabilities
canonical_status
lineage
explicit subsystem/realm/runtime_surface metadata emitted by generated artifacts
validated evidence when available

Invalid scope sources:

hidden Python keyword maps
manually maintained per-request routing tables
benchmark-specific routing
schema version suffixes
raw request text substring checks

## Request Interpretation

The orchestrator should classify the request by task type.

Recommended task types:

- feature_change
- bug_investigation
- refactor
- performance_investigation
- architecture_question
- sync_desync_investigation
- ui_change
- persistence_question
- networking_question
- timer_scheduler_question

The orchestrator should extract:

- user_request
- task_type
- target_subsystems
- likely_realms
- likely_runtime_surfaces
- evidence_needed
- expected_output

## Subsystem Scope

Subsystem scope should be generated from evidence.

Inputs may include:

- request words
- subsystem docs
- runtime topology
- human_context.md
- retrieval results
- source validation results

The user should not need to define every chain family manually.

Subsystem scope is generated, not hand-maintained per tiny task.

## Realm Scope

Realm scope should be explicit whenever possible.

The orchestrator should identify whether the request likely involves:

- server authority
- client UI
- shared definitions
- networking boundary
- persistence boundary
- timer/scheduler behavior

Realm uncertainty must remain explicit.

Do not silently assume client authority.

## Runtime Surface Scope

The orchestrator should identify likely runtime surfaces.

Common surfaces:

- hook/event
- network message
- timer/scheduler
- UI/HUD/Derma
- entity simulation
- inventory ownership
- item metadata
- persistence
- command/config
- database-backed state

Runtime surfaces guide retrieval and validation.

They are not proof by themselves.

## Doctrine Context Selection

The orchestrator must include relevant doctrine automatically.

For UI/HUD work, consider:

- realm_model.md
- networking_model.md if server data sync is involved
- runtime_doctrine.md UI/timer/network guidance
- relevant subsystem docs
- human_context.md notes about UI authority

For inventory/vendor work, consider:

- human_context.md item data semantics
- runtime_chain_promotion.md vendor/inventory rules
- inventory subsystem docs
- vendor subsystem docs
- gridinv subsystem docs
- networking_model.md

For persistence work, consider:

- persistence_model.md
- runtime_doctrine.md
- relevant subsystem docs
- human_context.md source authority rules

For timer/performance work, consider:

- runtime_doctrine.md timer doctrine
- realm_model.md timer implication
- subsystem_priorities.md
- relevant subsystem docs

For event/hook work, consider:

- event_taxonomy.md
- runtime_propagation_doctrine.md
- relevant subsystem docs

## Retrieval Planning

The orchestrator should generate multiple retrieval queries from one request.

Queries should cover:

- original user wording
- subsystem terms
- runtime events
- network messages
- UI hooks
- source file candidates
- human-context concepts
- doctrine concepts

Retrieval should prefer broad recall first, then narrow validation.

Retrieval results are evidence candidates, not truth.

## Evidence Validation Rule

Before giving implementation guidance, the orchestrator should validate key claims against deterministic artifacts or source snippets.

Validation should answer:

- which file proves this
- which realm owns it
- which event/network/timer/UI surface is involved
- whether the file appears authoritative or legacy
- whether human_context.md contradicts it
- whether more targeted source validation is needed

## Context Pack Rule

The context pack is the primary product of orchestration.

It should be concise enough for an LLM to use, but grounded enough to prevent guessing.

A context pack should separate:

- request interpretation
- selected doctrine
- retrieved evidence
- validated evidence
- uncertain evidence
- recommended next action

Do not mix speculation with validated facts.

## Runtime Chain Rule

Runtime chain reconstruction is optional.

Use runtime chains when the request needs propagation reasoning, such as:

- desync
- lifecycle ordering
- item ownership transfer
- item metadata sync
- persistence flow
- network state replication
- hook fanout
- timer-driven state propagation

Do not force every request into a runtime chain.

Simple UI or feature tasks may only need source validation and doctrine context.

## Runtime Chain Identity Rule

Do not require humans to manually define logical_chain_id for every request.

When runtime chains are produced, chain identity should be generated deterministically from validated runtime anchors.

Do not infer chain identity from:

- filename
- artifact path
- benchmark name
- version suffix
- promoted markdown name
- stage rule id alone

Stable generated identity should be based on:

- dominant subsystem
- source event or source operation
- target event or target operation
- realm transition
- validated propagation path
- validated runtime surface

## Stable Orchestration Artifact Families

Orchestration must be built around stable artifact families.

The goal is to avoid artifact-version architecture.

Bad:

retrieval_plan.v1
→ retrieval_plan.v2
→ retrieval_plan.v3

runtime_chain_candidate.v4
→ runtime_chain_candidate.v5
→ runtime_chain_candidate.v6
→ runtime_chain_candidate.v7

where each version becomes a new conceptual pipeline stage.

Versions describe schema compatibility.

Versions do not define pipeline concepts.

Stable orchestration families:

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

Runtime chain reconstruction is optional.

Requests that do not require propagation reasoning should not be forced into runtime-chain generation.

Examples:

UI changes
feature additions
simple refactors
configuration changes

may stop at:

orchestration_context_pack
→ guidance_report

without runtime-chain reconstruction.

## Artifact Identity Rule

Artifact identity must not depend on:

- filename
- benchmark name
- script version
- artifact version suffix

Identity should be derived from:

artifact_family
+
request scope
+
 deterministic evidence lineage

Artifact versions represent schema compatibility only.

They do not create new orchestration concepts.

## Orchestration Output Rule

The primary output of orchestration is:

orchestration_context_pack

not:

runtime_chain_candidate

A runtime chain is a supporting artifact when propagation reconstruction is required.

The context pack is the product consumed by:

- developers
- local LLMs
- architecture intelligence
- future orchestration stages

The orchestrator exists to gather and organize evidence.

It does not exist to generate runtime chains for every request.

## Human Context Role

human_context.md is the semantic correction layer for messy raw Lua.

It records:

- legacy vs authoritative systems
- human-confirmed behavior
- known bugs
- UI and sync rules
- subsystem ownership notes
- source authority rules

The orchestrator must treat human_context.md as high-priority context.

The orchestrator should not duplicate human_context.md rules here.

## Generated Artifact Role

Generated artifacts are evidence or control artifacts.

They should not become doctrine unless reviewed and promoted.

Possible orchestration-generated artifacts:

- orchestration request
- retrieval scope
- doctrine context selection
- retrieval results
- source validation request
- source validation result
- context pack
- runtime facts
- runtime chain candidate
- architecture or implementation guidance

Generated orchestration artifacts must not be manually patched.

Fix producers, metadata, or doctrine, then regenerate.

## Failure Rule

If the orchestrator cannot determine scope confidently, it should produce a narrow question or a validation request.

It should not guess architecture.

Allowed questions to the human:

- intended behavior
- subsystem history
- legacy vs authoritative implementation
- reproduction steps
- exact runtime observation
- exact Lua file when deterministic discovery fails

## Current Priority

Build the orchestration entry point first.

Do not create more benchmark-specific pipeline code.

Do not create runtime_chain_candidate.v8.

Do not manually define tiny chain definitions.

Do not patch generated artifacts.

Vendor and characterload chains are regression examples, not the product.

First useful target:

natural-language request
→ structured orchestration request
→ retrieval/context plan
