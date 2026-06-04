## Master plan

Important:
it's a context for a chat, not a directive for immediate execution

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

1.3 Make a solid plan PASS
   1.3.1 Update system prompt PASS
      Prompt updated implemented
      → source_file_manifest:
         None
   1.3.2 Update project sources, include new to system prompt if needed PASS
      human_context updated
      → source_file_manifest:
         architecture.md
      1.3.2.1 Define a solid pipeline on base of plan and Current Architecture Intent in human_context.md PASS
         Architectural decision has been made
         → source_file_manifest:
            None

2. Raw extraction IN PROGRESS
2.1 Make extract infrostructure IN PROGRESS
   2.1.1 Investigation of creation extract_lua_runtime_signals.py based on discover_lua_sources.py input PASS
      test variant extract_lua_runtime_signals.py inplemented
      → source_file_manifest:
         lua_syntax_alphabet.json
         lua_syntax_alphabet.md
   2.1.2 Working on extract_lua_runtime_signals.py IN PROGRESS
      2.1.2.1 Validate extract_lua_runtime_signals.py output against raw PASS
      2.1.2.2 Polish extraction alphabet for extract_lua_runtime_signals.py PASS
         → source_file_manifest:
            raw_lua_extraction.json
            raw_lua_extraction.md
      2.1.2.3 provide fixes for extract_lua_runtime_signals.py and lua_syntax_alphabet build_pipeline_contract_registry generation for PASS
2.2 Next step investigation brainstorm PASS
    → source_file_manifest:
      task_realisation_plan.md
2.3 Investigation of creation extract_ast_lua_runtime_signals.py based on results of extract_lua_runtime_signals.py input IN PROGRESS
   2.3.1 Create compact_raw_lua_extraction.py to consume raw_lua_extraction.json, sript execution should provide raw_lua_extraction_compact.json, raw_lua_extraction_index.md PASS
      compact_raw_lua_extraction.py implemented
      → source_file_manifest:
         raw_lua_extraction_compact.json
         raw_lua_extraction_index.md
   2.3.2 Start work on extract_ast_lua_runtime_signals.py prototype and it alphabet CURRENT
   2.3.3 Validate extract_ast_lua_runtime_signals.py output agaist raw LUA and extract_lua_runtime_signals.py NEXT
      2.3.3.1 Polish extraction via extract_ast_lua_runtime_signals.py and it alphabet

3. Normalization
3.1 Brainstorm, task_realisation_plan creation
3.2 Investigation of creation normalize_runtime_facts.py based on extract_lua_runtime_signals.py input
   3.2.1 Working on normalize_runtime_facts.py
      3.2.1.1 Validate normalize_runtime_facts.py output agaist raw LUA and extract_lua_runtime_signals.py output artifact
      3.2.1.2 Polish extraction alphabet for normalize_runtime_facts.py
3.3 Audit 3 chain pipeline discover_lua_sources -> extract_lua_runtime_signals -> normalize_runtime_facts

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
Few subtasks can be done in one chat if they close context related.

## Plan terminology

CURRENT - task actively being executed now.
INCLUDE - means that task can be implemented with CURRENT if possible
NEXT - task that starts only after CURRENT is completed.
IN PROGRESS - currently in progress
BLOCKED - blocked for some reason
PASS - completed.

Hierarchical schema example by numeration
1 Block - 1-st
1.1 Task - 2-nd
1.1.1 Subtask - 3-rd
1.2 Task - 4-th
1.2.1 Subtask - 5-th
1.2.2 Subtask - 6-th
... etc