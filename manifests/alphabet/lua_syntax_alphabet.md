# Lua Syntax Alphabet — Option B Candidate

- Artifact family: `lua_syntax_alphabet`
- Artifact ID: `lua_syntax_alphabet:5acdd4b5350419c0`
- Pipeline stage: `extraction`
- Role: syntax extraction rule input

## Responsibility Split

The alphabet declares extractable syntax entities, parser operation wiring, regex names, value classification rules, and syntax-only mechanics.

The extractor executes parser operations and emits only entities declared by `syntax_entities`.

## Syntax Entities

| Entity ID | Parser operation | Regex | Notes |
|---|---|---|---|
| `lua_table_field` | `table_field` | `table_field` |  |
| `lua_assignment` | `local_assignment` | `local_assignment` |  |
| `lua_assignment` | `assignment` | `assignment` |  |
| `lua_function_definition` | `function_definition` | `function_statement` | declaration line |
| `lua_function_assignment` | `assigned_function` | `assigned_function` | declaration line |
| `lua_function_assignment` | `local_assigned_function` | `local_assigned_function` | declaration line |
| `lua_anonymous_function` | `anonymous_function` | `function_literal_inline` |  |
| `lua_call_expression` | `call_expression` | `call` |  |
| `lua_literal_value` | `quoted_string_literal` | `string_literal` |  |
| `lua_literal_value` | `long_bracket_string_literal` | `long_string_literal` |  |

## Minimal Required Changes

- Replace script-owned evidence-kind/vocabulary constants with syntax_entities declared by lua_syntax_alphabet.
- Dispatch extraction by syntax_entities[*].parser_operation instead of a fixed script-owned evidence vocabulary list.
- Use alphabet value_classification_rules for all value_kind decisions.
- Use alphabet mechanics for table context labels, body-span value kinds, declaration-line call suppression, and callback argument ownership.
- Keep Lua parsing utilities in the script, but do not let the script define which evidence kinds exist or which syntax entities are emitted.
- Keep extraction syntax-only; defer all runtime/project meaning to normalization.
