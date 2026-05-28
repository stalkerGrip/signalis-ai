# SIGNALIS AI — Artifact Policy

This document defines where each artifact belongs: GitHub, ChatGPT Project Sources, Qdrant, or local-only storage.

## Principle

Each layer has a different job.

```text
GitHub = durable canonical workspace
ChatGPT Project Sources = compact reasoning anchors
Qdrant = semantic retrieval memory
Local workspace = heavy/generated/private operational data
```

No single layer defines truth alone.

Truth remains:

```text
normalized manifests
runtime topology
doctrine docs
subsystem docs
exact source code when needed
human validation
```

## GitHub

GitHub should contain durable project artifacts.

Store in GitHub:

- doctrine docs
- project memory
- source index
- artifact policy
- ChatGPT source list
- subsystem docs
- human subsystem notes
- AI subsystem synthesis
- investigation reports worth preserving
- scripts
- runtime schemas
- manifest summaries
- topology summaries
- Qdrant document summaries

Avoid storing in GitHub by default:

- huge embedding files
- local cache files
- transient logs
- temporary context packs
- generated query dumps
- private raw game source unless intentionally public
- secrets, tokens, server config, database dumps

Recommended Git handling:

```text
commit durable semantic artifacts
ignore generated caches
promote only useful investigation outputs
```

## ChatGPT Project Sources

ChatGPT Project Sources should stay compact and high-signal.

Use for:

- stable doctrine
- current project memory
- source index
- topology summary
- priority subsystem docs
- human context

Do not add by default:

- full runtime topology JSON
- embedding files
- raw Lua source
- large manifests
- old query dumps
- every investigation report
- low-signal generated artifacts

The goal is to give ChatGPT stable orientation, not overload it with raw data.

## Qdrant

Qdrant stores semantic retrieval memory.

Store in Qdrant:

- runtime topology node summaries
- runtime topology edge summaries
- plugin topology summaries
- file topology summaries
- doctrine documents
- event taxonomy
- networking model
- persistence model
- realm model
- subsystem docs
- selected investigation summaries
- profiling summaries when available

Optional secondary collection:

```text
signalis_code
```

Use only for exact source validation if raw Lua is intentionally indexed.

Qdrant does not define truth. It retrieves relevant context.

## Local Workspace

Keep heavy or transient operational data local:

- embeddings
- cache directories
- temporary logs
- profiling raw captures
- generated intermediate manifests
- local Qdrant database storage
- raw private source if not meant for GitHub

Promote only stable summaries into GitHub.

## Artifact Promotion Rule

Promote an artifact when it is:

- reusable
- human-readable
- stable enough to guide future reasoning
- grounded in topology/source/human validation
- useful for future retrieval or project onboarding

Do not promote an artifact when it is:

- temporary
- noisy
- too large
- duplicative
- source-private
- generated only for one immediate query

## Investigation Promotion Flow

```text
runtime symptom
→ Qdrant/context pack
→ investigation report
→ source validation
→ human validation
→ durable finding
→ update subsystem docs / doctrine / project memory
```

## Naming Convention

Recommended durable docs:

```text
docs/project_memory.md
docs/source_index.md
docs/artifact_policy.md
docs/chatgpt_project_sources.md
docs/human_subsystems/<subsystem>.md
docs/ai_subsystems/<subsystem>.md
docs/subsystems/<subsystem>.md
investigations/<topic>.md
```
