SIGNALIS AI Architecture Decision

SIGNALIS AI is a deterministic evidence pipeline plus AI orchestra.

The local LLM is not the authority and should not guess project behavior.
The local LLM acts as a cheap orchestration/execution worker.

Truth comes from:
1. SIGNALIS source code
2. SIGNALIS runtime topology
3. SIGNALIS doctrine/docs
4. Human validation
5. External NutScript
6. Facepunch Wiki

The AI orchestra is:

User command
→ local LLM
→ Qdrant / local RAG / external RAG
→ evidence-backed request for Thinking LLM or ChatGPT
→ Thinking LLM plan / decision
→ local LLM receives context pack + plan
→ bounded code implementation or guidance
→ validation
→ accepted result or retry

The pipeline must produce narrow evidence packs so the local LLM does not need to understand the whole messy GLua/NutScript project globally.

The local LLM should implement only from:
- orchestration_request
- retrieval_result_set
- evidence_set
- orchestration_scope
- doctrine_context_selection
- source_validation_result
- orchestration_context_pack
- guidance_report / Thinking LLM plan

The deterministic pipeline is:

source_file_manifest
→ raw_lua_extraction
→ normalized_runtime_facts
→ runtime_topology
→ runtime_propagation_topology
→ semantic_document_corpus / qdrant_documents
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

## Extraction Boundary

Extraction means syntax evidence capture.

Extraction scripts must capture what source files explicitly contain, without deciding what it means.

Allowed extraction outputs:

- file identity and digest
- source location
- realm hint from filename only
- assignment
- table field
- literal value
- function definition
- function assignment
- anonymous function
- call expression
- method call expression
- call arguments
- function body span

Extraction scripts must not classify project/runtime meaning.

Forbidden in extraction:

- network sender / receiver classification
- hook listener / hook emission classification
- scheduler classification
- item action classification
- inventory, vendor, armor, characterload, or benchmark-specific classification
- NutScript or SIGNALIS-specific behavior decisions
- priority or importance decisions

Normalization owns interpretation.

Examples:

`ITEM.desc = "text"` is extracted as assignment with string literal.

`ITEM.onCombineTo = function(item, target)` is extracted as assignment with function literal and body span.

`ITEM.functions.use = { onRun = function(item) ... }` is extracted as assignment with table literal and table fields.

`netstream.Hook("invData", function(id, key, value) ... end)` is extracted as a call expression with an anonymous function argument.

`hook.Run("ItemDataChanged", item, key, oldValue, value)` is extracted as a call expression.

Only normalization may later classify these as item metadata, item action, network receiver, hook emission, scheduler registration, or runtime propagation.

Optional runtime chains are used only when propagation reasoning is needed.

Regression benchmarks such as vendor, characterload, and armor are only tests of the generic pipeline.
They must never be hardcoded into infrastructure.