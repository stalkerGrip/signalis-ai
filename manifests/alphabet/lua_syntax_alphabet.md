# Lua Syntax Alphabet

Machine-readable source of truth: `lua_syntax_alphabet.json`.
This Markdown is a generated human review surface and must stay consistent with the JSON artifact.

## Identity

- Schema: `lua_syntax_alphabet`
- Schema version: `1`
- Artifact family: `lua_syntax_alphabet`
- Artifact ID: `lua_syntax_alphabet:32871dfef5c211c0`
- Content digest: `32871dfef5c211c0e5e0b7ac6b296cf82a58c4f8601cbc88fcbed5a4caf70d49`
- Generated at: `2026-06-03T13:23:56Z`
- Pipeline stage: `extraction`
- Producer script: `manual.source_governed_extraction_alphabet`
- Promotion role: `syntax_extraction_rule_input`
- Canonical status: `intermediate`

## Purpose

Declare generic Lua syntax extraction entities, parser operations, regex, value classification, and syntax-only mechanics consumed by raw Lua extraction and future normalization.

## Boundary

### Allowed extraction outputs

- file identity and digest
- source location
- realm hint from filename/manifest
- assignment
- table field
- literal value
- function definition
- function assignment
- anonymous function
- call expression
- method call expression
- call argument
- function body span

### Forbidden extraction outputs

- network sender classification
- network receiver classification
- hook listener classification
- hook emission classification
- scheduler classification
- item action classification
- inventory/vendor/armor/characterload classification
- NutScript-specific behavior decisions
- priority or importance decisions

## Syntax Entities

### 1. `lua_table_field`

- `enabled`: `True`
- `parser_operation`: `table_field`
- `regex`: `table_field`
- `requires_table_context`: `True`
- `requires_same_function_depth_as_table`: `True`
- `function_literal_ownership`: `table_field_only`
- `suppresses`:

```json
[
  "lua_assignment",
  "lua_function_assignment"
]
```

### 2. `lua_assignment`

- `enabled`: `True`
- `parser_operation`: `local_assignment`
- `regex`: `local_assignment`
- `sets_is_local`: `True`
- `opens_table_context_when_value_kind`: `table_literal`

### 3. `lua_assignment`

- `enabled`: `True`
- `parser_operation`: `assignment`
- `regex`: `assignment`
- `sets_is_local`: `False`
- `opens_table_context_when_value_kind`: `table_literal`

### 4. `lua_function_definition`

- `enabled`: `True`
- `parser_operation`: `function_definition`
- `regex`: `function_statement`
- `declaration_line`: `True`

### 5. `lua_function_assignment`

- `enabled`: `True`
- `parser_operation`: `assigned_function`
- `regex`: `assigned_function`
- `declaration_line`: `True`
- `function_literal_assignment_ownership`: `assignment_with_function_body_span`

### 6. `lua_function_assignment`

- `enabled`: `True`
- `parser_operation`: `local_assigned_function`
- `regex`: `local_assigned_function`
- `declaration_line`: `True`
- `function_literal_assignment_ownership`: `assignment_with_function_body_span`

### 7. `lua_anonymous_function`

- `enabled`: `True`
- `parser_operation`: `anonymous_function`
- `regex`: `function_literal_inline`
- `primary_use`: `call_argument_callback_attachment_or_unowned_inline_function_literal`

### 8. `lua_call_expression`

- `enabled`: `True`
- `parser_operation`: `call_expression`
- `regex`: `call`
- `method_kind_id`: `lua_method_call_expression`
- `argument_entity_id`: `lua_call_argument`

### 9. `lua_call_expression`

- `enabled`: `True`
- `parser_operation`: `call_after_call_result`
- `regex`: `call_after_call_result`
- `method_kind_id`: `lua_method_call_expression`
- `argument_entity_id`: `lua_call_argument`
- `parent_call_reference`: `True`
- `target_strategy`: `append_parent_call_target_with_call_suffix_and_selected_member`
- `target_root`: `<call_result>`
- `target_prefix`: `)`
- `purpose`: `Capture call expressions whose callable is selected from the result of a previous call, for syntax such as object:method():next(arg).`

### 10. `lua_call_expression`

- `enabled`: `True`
- `parser_operation`: `parenthesized_expression_method_call`
- `regex`: `parenthesized_expression_method_call`
- `method_kind_id`: `lua_method_call_expression`
- `argument_entity_id`: `lua_call_argument`
- `target_strategy`: `balanced_parenthesized_receiver_plus_selected_member`
- `purpose`: `Capture method calls whose callable is selected from a balanced parenthesized expression receiver, for syntax such as (a() - b()):method().`

### 11. `lua_literal_value`

- `enabled`: `True`
- `parser_operation`: `quoted_string_literal`
- `regex`: `string_literal`

### 12. `lua_literal_value`

- `enabled`: `True`
- `parser_operation`: `long_bracket_string_literal`
- `regex`: `long_string_literal`

## Parser Operation Order

1. `table_field`
2. `local_assignment`
3. `assignment`
4. `function_definition`
5. `assigned_function`
6. `local_assigned_function`
7. `anonymous_function`
8. `call_expression`
9. `call_after_call_result`
10. `parenthesized_expression_method_call`
11. `quoted_string_literal`
12. `long_bracket_string_literal`

## Regex

### `assigned_function`

```regex
^\s*([A-Za-z_][A-Za-z0-9_]*(?:(?:\.|:)[A-Za-z_][A-Za-z0-9_]*)*(?:\[[^\]]+\])?)\s*=\s*function\s*\(([^)]*)\)
```

### `assignment`

```regex
^\s*(?P<lhs>[^=~<>]+?)\s*=\s*(?P<rhs>.+?)\s*$
```

### `block_token`

```regex
\b(function|then|do|repeat|end|until)\b
```

### `call`

```regex
(?<![\w.:'\"])(?P<target>[A-Za-z_][A-Za-z0-9_]*(?:(?:\[[^\]\n]+\])|(?:\.|:)[A-Za-z_][A-Za-z0-9_]*)*)\s*(?P<call_open>\()
```

### `call_after_call_result`

```regex
\)(?P<postfix>(?:\s*\[[^\]\n]+\])*)\s*(?P<sep>[:.])(?P<leaf>[A-Za-z_][A-Za-z0-9_]*)\s*(?P<call_open>\()
```

### `function_literal_inline`

```regex
function\s*\(([^)]*)\)
```

### `function_statement`

```regex
^\s*(?:(local)\s+)?function\s+([A-Za-z_][A-Za-z0-9_]*(?:(?:\.|:)[A-Za-z_][A-Za-z0-9_]*)*)\s*\(([^)]*)\)
```

### `identifier`

```regex
[A-Za-z_][A-Za-z0-9_]*
```

### `local_assigned_function`

```regex
^\s*local\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*function\s*\(([^)]*)\)
```

### `local_assignment`

```regex
^\s*local\s+(?P<lhs>[A-Za-z_][A-Za-z0-9_]*(?:\s*,\s*[A-Za-z_][A-Za-z0-9_]*)*)\s*=\s*(?P<rhs>.+?)\s*$
```

### `long_string_literal`

```regex
\[(=*)\[(.*?)\]\1\]
```

### `parenthesized_expression_method_call`

```regex
\)\s*(?P<sep>[:.])(?P<leaf>[A-Za-z_][A-Za-z0-9_]*)\s*(?P<call_open>\()
```

### `qualified_symbol`

```regex
[A-Za-z_][A-Za-z0-9_]*(?:(?:\.|:)[A-Za-z_][A-Za-z0-9_]*)*
```

### `string_literal`

```regex
(?P<quote>['\"])(?P<value>(?:\\.|(?!\1).)*)(?P=quote)
```

### `table_constructor_field_explicit`

```regex
^\s*(?P<key>[A-Za-z_][A-Za-z0-9_]*|\[[^\]]+\])\s*=\s*(?P<value>.+?)\s*$
```

### `table_constructor_field_positional`

```regex
^\s*(?P<value>.+?)\s*$
```

### `table_field`

```regex
^\s*(?P<key>[A-Za-z_][A-Za-z0-9_]*|\[[^\]]+\])\s*=\s*(?P<value>.+?)(?:,)?\s*$
```

## Regex Flags

- `long_string_literal`: `DOTALL`

## Value Classification Rules

| Order | Match | Input | Value kind |
|---:|---|---|---|
| 1 | `empty` | `—` | `empty` |
| 2 | `startswith` | `{` | `table_literal` |
| 3 | `regex_search` | `table_constructor_open_at_line_end` | `table_literal` |
| 4 | `startswith` | `function` | `function_literal` |
| 5 | `token_list` | `boolean` | `boolean_literal` |
| 6 | `token_list` | `nil` | `nil_literal` |
| 7 | `regex_fullmatch` | `number_regex` | `number_literal` |
| 8 | `compiled_regex_fullmatch` | `string_literal` | `string_literal` |
| 9 | `compiled_regex_fullmatch` | `long_string_literal` | `string_literal` |
| 10 | `regex_fullmatch` | `qualified_symbol` | `symbol_reference` |
| 11 | `fallback` | `—` | `expression` |

## Value Detection

### `number_regex`

```regex
[-+]?\d+(?:\.\d+)?
```

### `table_constructor_open_at_line_end`

```regex
\{\s*$
```

## Literal Tokens

### `boolean`

```json
[
  "true",
  "false"
]
```

### `nil`

```json
[
  "nil"
]
```

## Control Call Words

`if`, `for`, `while`, `repeat`, `until`, `return`, `function`, `local`, `elseif`

## Block Tokens

### `close`

```json
[
  "end",
  "until"
]
```

### `open`

```json
[
  "function",
  "then",
  "do",
  "repeat"
]
```

### `repeat_close`

```json
[
  "until"
]
```

## Mechanics

- `anonymous_function_arguments_attach_to_parent_call_argument`: `True`
- `anonymous_function_duplicate_suppression_scope`: `call_argument_function_literal_ranges`
- `anonymous_function_entity_for_call_argument_callbacks_only_when_attached`: `True`
- `anonymous_function_evidence_scope`: `call_argument_callbacks_or_unowned_inline_literals`
- `anonymous_function_suppress_when_owned_by_call_argument`: `True`
- `assignment_lhs_grammar`: `qualified_symbol_or_indexed_qualified_symbol`
- `assignment_operator_kind`: `single_equals_not_comparison`
- `assignment_owned_table_fields_preserve_real_source_locations`: `True`
- `assignment_owned_table_literals_are_table_extraction_roots`: `True`
### `body_span_value_kinds`

```json
[
  "table_literal",
  "function_literal"
]
```

- `call_after_call_result_enabled`: `True`
- `call_after_call_result_parent_reference`: `True`
- `call_after_call_result_root_label`: `<call_result>`
- `call_after_call_result_target_example`: `client:getChar():getInv():add`
- `call_after_call_result_target_prefix`: `)`
- `call_after_call_result_target_strategy`: `append_parent_call_target_with_call_suffix_and_selected_member`
- `call_argument_splitting_honors_block_depth_rules`: `True`
- `call_argument_table_literal_condition`: `argument_trimmed_startswith_open_brace`
- `call_arguments_emit_parent_call_evidence_id`: `True`
### `call_receiver_forms`

```json
[
  "qualified_symbol_receiver",
  "indexed_receiver",
  "call_result_receiver",
  "call_result_indexed_receiver",
  "parenthesized_expression_receiver"
]
```

- `call_receiver_forms_owner`: `lua_syntax_alphabet`
- `call_result_index_chain_enabled`: `True`
- `call_target_index_postfix_preserved`: `True`
- `context_kind_table`: `table`
- `definition_form_function_statement`: `function_statement`
- `direct_assignment_table_literal_condition`: `rhs_trimmed_startswith_open_brace`
- `direct_assignment_table_literal_does_not_include_call_with_table_argument`: `True`
- `elseif_then_does_not_open_new_block_depth`: `True`
- `fallback_evidence_ids_allowed`: `False`
- `function_assignment_entity_suppressed_when_assignment_rhs_is_function_literal`: `True`
- `function_body_value_kind`: `function_literal`
- `function_definition_lines_are_not_call_expression_lines`: `True`
- `function_literal_assignment_emits_function_assignment`: `False`
- `function_literals_inside_table_constructors_are_table_fields`: `True`
- `glua_c_style_block_comments_masked_before_extraction`: `True`
- `identifier_key_expression_kind`: `identifier`
- `implicit_array_index_start`: `1`
- `indexed_assignment_lhs_enabled`: `True`
- `indexed_receiver_method_call_enabled`: `True`
### `inline_assignment_left_boundary_tokens`

```json
[
  "then",
  "do"
]
```

### `inline_assignment_right_boundary_tokens`

```json
[
  "end",
  "elseif",
  "else"
]
```

- `inline_nested_table_fields_enabled`: `True`
- `inline_table_constructor_fields_enabled`: `True`
- `inline_table_field_context_strategy`: `nested_context_path`
- `key_syntax_computed`: `computed_key`
- `key_syntax_identifier`: `identifier_key`
- `key_syntax_implicit_array_index`: `implicit_array_index`
- `literal_values_may_be_emitted_separately`: `True`
- `local_assignment_has_is_local_and_clean_lhs`: `True`
- `local_multi_assignment_enabled`: `True`
- `multi_assignment_emit_each_lhs`: `True`
- `multi_assignment_group_identity`: `occurrence_unique_deterministic`
### `multi_assignment_group_identity_inputs`

```json
[
  "file_id",
  "line",
  "raw_evidence_text",
  "normalized_lhs_list",
  "normalized_rhs_list",
  "is_local"
]
```

- `multi_assignment_missing_rhs_value`: `nil`
- `multi_assignment_single_call_rhs_may_return_multiple`: `True`
- `multi_assignment_single_call_rhs_metadata`: `rhs_returns_maybe_multiple`
- `multi_assignment_single_call_rhs_strategy`: `share_rhs_for_all_lhs`
- `multi_assignment_split_strategy`: `top_level_commas_only`
### `multiline_assignment_rhs_balance_tokens`

```json
[
  "parentheses",
  "brackets",
  "braces",
  "function_end_blocks"
]
```

- `multiline_assignment_rhs_enabled`: `True`
- `multiline_assignment_rhs_incomplete_policy`: `emit_rhs_span_complete_false`
- `multiline_assignment_table_fields_use_source_line_traversal`: `True`
- `nested_table_context_uses_child_field_start_line`: `True`
- `owned_function_literals_emit_anonymous_function_evidence`: `False`
- `parenthesized_expression_method_call_enabled`: `True`
- `parenthesized_expression_receiver_target_strategy`: `balanced_parenthesized_receiver_plus_selected_member`
### `parser_operation_order`

```json
[
  "table_field",
  "local_assignment",
  "assignment",
  "function_definition",
  "assigned_function",
  "local_assigned_function",
  "anonymous_function",
  "call_expression",
  "call_after_call_result",
  "parenthesized_expression_method_call",
  "quoted_string_literal",
  "long_bracket_string_literal"
]
```

### `positional_table_field_excluded_standalone_tokens`

```json
[
  "end",
  "else",
  "elseif",
  "until"
]
```

- `positional_table_fields_enabled`: `True`
- `preserve_table_context_labels`: `True`
- `preview_text_is_not_source_location_evidence`: `True`
- `preview_text_table_fields_forbidden_unless_marked_synthetic`: `True`
- `same_line_table_constructor_fields_may_emit_inline_source_evidence`: `True`
- `script_role_for_call_receiver_forms`: `mechanical_balanced_parsing_only`
- `split_line_then_after_elseif_does_not_open_new_block_depth`: `True`
- `table_body_value_kind`: `table_literal`
- `table_constructor_fields_are_not_assignments`: `True`
- `table_constructor_fields_split_strategy`: `top_level_commas_respecting_strings_comments_brackets_parentheses_blocks`
- `table_field_context_must_match_current_function_depth`: `True`
### `table_field_deduplicate_key`

```json
[
  "file_id",
  "line",
  "table_depth",
  "context_path",
  "key_text",
  "value_preview"
]
```

- `table_field_function_literal_emits_function_assignment`: `False`

## Minimal Required Changes for Extractor

- Replace script-owned evidence-kind/vocabulary constants with syntax_entities declared by lua_syntax_alphabet.
- Dispatch extraction by syntax_entities[*].parser_operation instead of a fixed script-owned evidence vocabulary list.
- Use alphabet value_classification_rules for all value_kind decisions.
- Use alphabet mechanics for table context labels, body-span value kinds, declaration-line call suppression, and callback argument ownership.
- Keep Lua parsing utilities in the script, but do not let the script define which evidence kinds exist or which syntax entities are emitted.
- Keep extraction syntax-only; defer all runtime/project meaning to normalization.
- Use lua_syntax_alphabet regex.call_after_call_result and parser_operation=call_after_call_result for chained calls after call results.
- Do not emit lua_function_assignment for table field function literals when mechanics.table_field_function_literal_emits_function_assignment is false.
- Do not emit duplicate lua_function_assignment for assignment RHS function literals when mechanics.function_literal_assignment_emits_function_assignment is false.
- Do not emit standalone lua_anonymous_function for owned function literals when mechanics.owned_function_literals_emit_anonymous_function_evidence is false.
- For parser_operation=call_after_call_result, build the emitted symbol target by appending the selected member to the parent call target, e.g. client:getChar():getInv():add.
- When mechanics.call_after_call_result_parent_reference is true, emit parent call evidence references for chained-call evidence.
- When mechanics.owned_function_literals_emit_anonymous_function_evidence is false, suppress lua_anonymous_function for function literals already owned by lua_assignment or lua_table_field.
- Use lua_syntax_alphabet regex.function_literal_inline for anonymous function parameter capture; do not hardcode function literal regex in the script.
- When mechanics.anonymous_function_suppress_when_owned_by_call_argument is true, suppress standalone lua_anonymous_function evidence for spans already emitted as call-argument callbacks.
- Use mechanics.parser_operation_order for parser operation precedence instead of script-owned operation ordering.
- When mechanics.fallback_evidence_ids_allowed is false, the script must not invent fallback evidence ids such as lua_call_argument when the alphabet entity does not declare them.
- Classify assignment RHS that syntactically opens a table constructor at line end as table_literal using alphabet value_classification_rules, so assigned table context labels are preserved without project-specific rules.
- Use alphabet regex.call named call_open group so argument extraction starts from the declared callable open parenthesis, not from the first parenthesis inside an indexed or complex receiver.
- Use alphabet regex.call_after_call_result postfix group to preserve call-result indexing chains before selected method members.
- Use parser_operation=parenthesized_expression_method_call for method calls selected from balanced parenthesized expressions such as (expr):method().
- Declare call receiver forms in mechanics.call_receiver_forms; the script may mechanically parse only forms listed there.
- Treat indexed receivers, call-result receivers, call-result indexed receivers, and parenthesized expression receivers as alphabet-owned syntax forms, not script-owned special cases.
- When mechanics.call_argument_splitting_honors_block_depth_rules is true, split multiline call arguments only at top-level commas after applying alphabet block-depth rules, including elseif/then exceptions.
- When mechanics.inline_table_constructor_fields_enabled is true, parse same-line table constructors and emit lua_table_field evidence for explicit nested fields under nested_context_path.
- When mechanics.positional_table_fields_enabled is true, emit implicit numeric lua_table_field keys for positional table constructor elements starting at mechanics.implicit_array_index_start.
- When mechanics.local_multi_assignment_enabled is true, split local assignment LHS/RHS by top-level commas and emit one lua_assignment per LHS when multi_assignment_emit_each_lhs is true.
- Classify assigned table context as table_literal only when mechanics.direct_assignment_table_literal_condition is satisfied; call-with-table-argument expressions remain expression assignments.
- When mechanics.multiline_assignment_rhs_enabled is true, capture balanced multiline RHS spans and mark incomplete spans explicitly if balance is not found.
- For assignment-owned multiline table literals, do not emit table fields from collected RHS preview text; emit child fields only from real source-line traversal.
- When emitting nested table fields, preserve the real child table field start line in context_path and value_body_span.
- Deduplicate lua_table_field evidence by file_id, line, table_depth, context_path, key_text, and value_preview.
- When a multi-assignment has multiple LHS entries and exactly one RHS that is a syntactic call expression, do not invent nil for later LHS entries; share the call RHS and mark rhs_returns_maybe_multiple when declared.
- multi_assignment_group must be deterministic per raw assignment occurrence: same emitted assignments from one raw occurrence share a group, repeated identical assignment text on different lines must have different groups using source occurrence identity.
### `positional_table_field_exclusions`

```json
{
  "applies_to": "lua_table_field",
  "excluded_standalone_tokens": [
    "end",
    "else",
    "elseif",
    "until"
  ],
  "name": "positional_table_field_exclusions",
  "reason": "These tokens close or continue syntax blocks and are not table values unless explicitly quoted or embedded inside an expression.",
  "rule": "Lua block delimiters and control-flow keywords are not positional table fields."
}
```

### `glua_c_style_block_comments`

```json
{
  "applies_before_extraction": true,
  "forbidden_outputs_inside_mask": [
    "lua_assignment",
    "lua_table_field",
    "lua_literal_value",
    "lua_function_definition",
    "lua_anonymous_function",
    "lua_call_expression",
    "lua_method_call_expression",
    "lua_call_argument"
  ],
  "masking": true,
  "name": "glua_c_style_block_comments",
  "syntax_forms": [
    "/* ... */"
  ]
}
```

### `indexed_assignment_lhs`

```json
{
  "forbidden": [
    "project_specific_lhs_names",
    "field_name_allowlists",
    "method_name_allowlists"
  ],
  "kind": "lua_assignment",
  "name": "indexed_assignment_lhs",
  "rhs_capture": true,
  "syntax_forms": [
    "symbol[index] = rhs",
    "symbol.field[index] = rhs",
    "symbol[index].field = rhs",
    "symbol.field[index].field[index] = rhs"
  ],
  "table_literal_rhs_supported": true
}
```
