# Task Realisation Plan Generation Rules

## Purpose

Use this file when generating or rewriting `task_realisation_plan.md` for a new CURRENT task.

`task_realisation_plan.md` is a compact task-local implementation guide. It must contain only information unique to the current task and accepted investigation results.

## Core rule

Do not duplicate project truth already owned by source files or system/project instructions.

The plan may reference authoritative files by name, but it must not copy their rules, doctrines, contracts, architecture, or environment details unless a task-specific exception is necessary.

## What to include

Include only:

- CURRENT task id and task name.
- NEXT task id and task name, if needed for boundary clarity.
- Accepted task-specific decisions.
- Specific implementation direction for the current task.
- Expected user input for the task, such as files, artifact paths, command output, audit text, or raw samples.
- Known task-local risks or validation checks.
- Exit criteria unique to the task.
- Open questions that block the current task.

## What not to include

Do not include:

- Full source authority lists already required by system/project instructions.
- General architecture doctrine.
- General extraction boundary text.
- Environment/tooling inventory.
- Full CLI contract doctrine.
- Full pipeline artifact registry doctrine.
- Runtime behavior facts unless the current task directly depends on them.
- Benchmark names as infrastructure rules.
- Repeated instructions from previous task realisation files.

## Expected user input section

When useful, include an `Expected input from user` section.

Allowed examples:

```text
- Updated script file.
- Updated alphabet file.
- Generated artifact JSON.
- Raw Lua files used for validation.
- Error output from command execution.
- Audit notes from previous chat.
```

This section should say what input helps the next step. It must not demand files already guaranteed by system/project source directives.

## Source reference style

Use short references only:

```text
See architecture.md for extraction boundary.
See pipeline_artifact_contract.md for artifact metadata rules.
See script_contracts.md for CLI truth after implementation.
```

Do not paste the referenced content.

## Size target

Keep the file small.

Recommended size:

```text
300-900 words
```

If the file grows beyond that, remove duplicated doctrine and keep only task-specific decisions.

## Rewrite rule

When CURRENT task changes, rewrite this file instead of appending historical sections.

Historical investigation results should be kept only if they directly affect the new CURRENT task.
