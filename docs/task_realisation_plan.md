# SIGNALIS AI — Task Realisation 2.3.2

## Next task

Start prototype work on:

```text
scripts/extraction/extract_ast_lua_runtime_signals.py
manifests/alphabet/lua_ast_syntax_alphabet.json
```

This file owns only implementation guidance unique to task `2.3.2`. General extraction boundary and pipeline doctrine remain owned by the project source files.

## Task-specific decision

Use Tree-sitter Lua as the first AST investigation target.

The AST extractor must have its own alphabet/contract file. Do not hardcode emitted syntax families inside the script.

The script executes parser mechanics. The AST alphabet declares what AST node families may produce which extraction evidence kinds.

## Prototype goal

Produce a first `ast_lua_extraction` artifact that can be compared against the compact regex extraction baseline.

The AST extractor is not intended to replace regex extraction immediately. It must first prove parity or improvement against known weak areas.

## Required inputs

Expected inputs:

```text
source_file_manifest.json
lua_ast_syntax_alphabet.json
```

Optional comparison input may be added later, but comparison should preferably stay in validation tooling, not in the AST extractor itself.

## Expected outputs

Prototype output:

```text
manifests/extraction/ast_lua_extraction.json
manifests/extraction/ast_lua_extraction.md
```

## AST alphabet responsibilities

`lua_ast_syntax_alphabet.json` should declare:

- allowed AST node types
- node type to evidence kind mapping
- allowed evidence fields per emitted kind
- GLua preprocessing rules used for parser compatibility
- source range mapping policy
- forbidden interpretation reminders specific to AST extraction

Keep it smaller than `lua_syntax_alphabet.json`. It should not duplicate regex mechanics.

## GLua compatibility strategy

Parse a transformed copy, never overwrite original source.

Initial compatibility transformations to investigate:

```text
!x       -> not x
a != b   -> a ~= b
a && b   -> a and b
a || b   -> a or b
continue -> parser-safe placeholder
```

The output must cite original file lines and original source text/ranges, not transformed text.

## Evidence focus

Prototype should prioritize syntax facts that were fragile in regex extraction:

- function declarations and body spans
- assignment and local assignment
- multi-assignment
- table constructor fields
- nested table constructors
- function literals in table fields
- call expressions
- method calls
- call arguments
- anonymous callback function arguments
- call-result chains where possible

## Validation expectations for prototype

The prototype does not need full parity on first run, but it must report parser failures and unsupported syntax explicitly.

Each file summary should include:

- parse status
- transformation status
- syntax error count if available
- emitted evidence count by kind
- source digest reference

## Known non-goals

- No runtime meaning.
- No hook/network/timer classification.
- No normalization.
- No replacement of regex extraction before validation.
- No project-specific symbol allowlists.
