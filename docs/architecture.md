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

Optional runtime chains are used only when propagation reasoning is needed.

Regression benchmarks such as vendor, characterload, and armor are only tests of the generic pipeline.
They must never be hardcoded into infrastructure.