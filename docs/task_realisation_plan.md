# SIGNALIS AI — Task Realisation 2.3.3

## Current task

```text
2.3.3 Validate extract_ast_lua_runtime_signals.py output against raw LUA and extract_lua_runtime_signals.py
```

Includes:

```text
2.3.3.1 Polish extraction via extract_ast_lua_runtime_signals.py and lua_ast_syntax_alphabet.json
```

This file owns only AST validation and polishing guidance.

---

## Current validated AST status

Validated PASS from current AST sample audit:

* parser loads and produces AST evidence;
* assignment LHS extraction works;
* local declarations emit `is_local = true`;
* function parameter extraction works;
* function body spans are emitted;
* method-call extraction works;
* nested call extraction works;
* literal extraction works for string, number, boolean, and nil;
* unary negative values are preserved;
* local multi-assignment extraction works;
* local declaration assignment ownership is preserved in audited samples.

These are extraction findings only and must not be interpreted as runtime meaning.

---

## Current hardcode doctrine status

Validated PASS:

* no SIGNALIS-specific extraction logic found;
* no NutScript-specific extraction logic found;
* no benchmark-specific extraction logic found;
* no hook-name allowlists found;
* no method-name allowlists found;
* no field-name allowlists found.

Remaining doctrine audit:

* reduce script-owned evidence-kind decisions where practical;
* continue moving extraction ownership toward lua_ast_syntax_alphabet.json;
* keep alphabet and script synchronized.

---

## Validation inputs

Use:

```text
raw Lua source files
raw_lua_extraction_compact.json
ast_lua_extraction.json
lua_ast_syntax_alphabet.json
```

Use full raw_lua_extraction.json only when compact output is insufficient.

---

## Main comparison question

Does AST extraction preserve existing validated regex evidence while improving structurally fragile syntax cases?

Comparison is evidence-based, not byte-identical.

Compare:

* evidence kind;
* source file and range;
* symbol;
* lhs;
* literal value;
* parameters;
* body spans;
* ownership and parent relationships.

---

## Priority validation targets

Current priority:

1. Validate duplicate suppression at scale.
2. Validate callback ownership.
3. Validate multiple callback arguments in one call.
4. Validate nested table field extraction.
5. Validate multiline table constructors.
6. Validate call-with-table-argument handling.
7. Validate indexed receivers.
8. Validate call-result chains.
9. Validate parenthesized receiver calls.
10. Validate parent-child ownership.
11. Validate source-range precision.
12. Validate future call-argument evidence emission.

---

## Comparison outputs

Expected outputs:

```text
manifests/extraction/ast_lua_extraction_comparison.json
manifests/extraction/ast_lua_extraction_comparison.md
```

Markdown should summarize mismatch classes and representative examples.

---

## Mismatch classification

Use:

```text
ast_missing_regex_confirmed_evidence
ast_added_valid_evidence
ast_added_suspicious_evidence
regex_missing_ast_confirmed_evidence
source_ambiguous_requires_manual_audit
parser_failure
preprocessing_mapping_failure
ast_known_prototype_defect
```

Do not convert ambiguous differences into facts.

---

## Polish loop

Polish order:

1. Parser/source mapping failures.
2. Duplicate suppression failures.
3. Callback ownership.
4. Multiple callback argument ownership.
5. AST alphabet mapping gaps.
6. Parent-child ownership.
7. Span precision.
8. GLua preprocessing safety.
9. Re-run comparison.

Do not patch for:

* benchmark names;
* file names;
* hook names;
* item names;
* NutScript-specific symbols;
* method-name allowlists.

---

## Expected input from user

Useful inputs:

* updated extract_ast_lua_runtime_signals.py;
* updated lua_ast_syntax_alphabet.json;
* ast_lua_extraction.json;
* comparison artifacts;
* raw Lua examples for mismatch review.

---

## Exit criteria

Task can PASS when:

* AST output exists for the target source set;
* parser failures are explicit;
* comparison artifacts exist;
* regex PASS families are preserved or justified;
* callback ownership is validated;
* duplicate suppression is validated;
* parent-child ownership is validated;
* source-range mapping is acceptable;
* previously fixed defects remain fixed:

  * lhs extraction;
  * local detection;
  * parameter extraction;
  * unary negative values;
  * local multi-assignment extraction;
* no extraction-boundary violation is introduced.
