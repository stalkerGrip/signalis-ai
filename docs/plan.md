## Master plan

### Tasks
1. Source discovery PASS
   → discover_lua_sources.py implemented
   → source_file_manifest:
        source_file_manifest.json
        source_file_manifest.md

1.2 Audit of current scripts PASS
   build_pipeline_contract_registry implemented
   → source_file_manifest:
        pipeline_artifact_contract.json
        pipeline_artifact_contract.md
        script_contracts.json
        script_contracts.md

1.3 Make a solid plan BLOCKED
1.3.1 Update system promt PASS
   Promt updated implemented
   → source_file_manifest:
      None
1.3.2 Update project sources CURRENT
1.3.3 Define a solid pipeline on base of plan and Current Architecture Intent in human_context.md NEXT

2. Raw extraction
   → extract_lua_runtime_signals.py
   → raw_lua_extraction

3. Normalization
   → normalize_runtime_facts.py
   → normalized_runtime_facts

4. Relationship topology
   → build_runtime_topology.py
   → runtime_topology

5. Propagation topology
   → build_runtime_propagation_topology.py
   → runtime_propagation_topology

6. Semantic corpus
   → build_semantic_documents.py
   → semantic_document_corpus / qdrant_documents

7. Retrieval infrastructure
   → embed_qdrant_documents.py
   → ingest_qdrant.py
   → query_qdrant.py

8. Orchestration entry
   → review/fix build_orchestration_entrypoint.py
   → orchestration_request

9. First-pass retrieval
   → build_retrieval_seed.py
   → retrieval_seed
   → build_retrieval_result_set.py
   → retrieval_result_set

10. Evidence
   → build_evidence_set.py
   → evidence_set

11. Evidence-backed scope
   → rebuild build_orchestration_scope.py
   → orchestration_scope from evidence_set

12. Doctrine context
   → build_doctrine_context_selection.py
   → doctrine_context_selection

13. Retrieval scope
   → build_retrieval_scope.py
   → retrieval_scope

14. Source validation
   → build_source_validation_request.py
   → source_validation_request
   → run_source_validation_request.py
   → source_validation_result

15. Context pack
   → build_orchestration_context_pack.py
   → orchestration_context_pack

16. Guidance
   → build_guidance_report.py
   → guidance_report

17. Optional runtime chains
   → only when propagation reasoning is needed
   → runtime_chain_reconstruction_request
   → runtime_chain_candidate
   → promotion_validation
   → promotion_decision

18. Regression benchmarks
   → vendor
   → characterload
   → armor
   Used only to test generic pipeline.
   Never hardcode into infrastructure.

## Rules

Task status should be tracked.
Task results should be filled in.
The master should be divided into tasks and subtasks.

## Plan terminology

CURRENT = task actively being executed now.
NEXT = task that starts only after CURRENT is completed.
BLOCKED = cannot start until prerequisites are completed.
PASS = completed.