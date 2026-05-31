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

Required consumers:

- source validation
- targeted validation
- runtime chain reconstruction
- evidence extraction
- source discovery
- promotion validation

Rule:

Workspace root != Source root

Source roots are loaded from workspace.yaml.