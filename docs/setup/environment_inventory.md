Use Python 3.11 for SIGNALIS AI pipeline.
Python 3.12 caused SentenceTransformer/BGE loading hangs.
Use BAAI/bge-small-en-v1.5 for embeddings.
Qdrant collection dimension is 384.
Run query/embedding commands from .venv.

# Workspace Configuration

Canonical workspace configuration:

config/workspace.yaml

Purpose:

Resolve authoritative source roots.

Investigation scripts must use workspace.yaml instead of hardcoded filesystem paths.

Rule:

Workspace root != Source root

Source roots are loaded from workspace.yaml.

## Investigation Pipeline Dependencies

Runtime chain reconstruction:

- networkx
- pydantic
- jsonschema

Validation:

- pytest

Evidence / topology querying:

- duckdb

Profiling:

- pyinstrument

Workspace configuration:

- PyYAML

# Tooling Inventory

## Retrieval

- Qdrant
- sentence-transformers
- BAAI/bge-small-en-v1.5

## Investigation

- networkx
- pydantic
- jsonschema
- pytest
- duckdb
- pyinstrument
- ripgrep

## System

Ryzen 5 7500f
RX 9060 XT 16Gb
32 Gb DDR5 RAM