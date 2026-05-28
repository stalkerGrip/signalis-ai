# SIGNALIS AI — Pipeline State

## Project

**Signalis AI Orchestration Pipeline**

Purpose:

```text
Build deterministic semantic infrastructure for a complex Garry’s Mod NutScript framework.
```

Core philosophy:

```text
No autonomous AI swarm.
No blind raw context dumps.
LLMs reason over semantic truth.
They do not define truth.
```

---

## Pipeline Shape

```text
raw Lua source
→ extraction manifests
→ semantic normalization
→ runtime graphs
→ unified runtime topology
→ semantic documents
→ embeddings / Qdrant
→ external architecture reasoning
```

---

## Current Workspace

```text
E:/signalis_ai
```

Source roots:

```text
E:/steam/steamapps/common/GarrysMod/garrysmod/gamemodes/signalis
E:/steam/steamapps/common/GarrysMod/garrysmod/gamemodes/nutscript
```

---

## Completed Extraction Manifests

Completed extraction categories:

```text
hooks
networking
timers
items
entities
derma/UI
globals
persistence
commands
registries
character_inventory
```

---

## Completed Normalization / Graph Phases

### Hook Symbol Normalization

Resolved symbolic hook dispatch such as:

```lua
hook.Run(nut.diseases.stringConsts.handleDiseaseOnCall)
```

into:

```text
HandleDiseaseOnCall
→ PLUGIN:HandleDiseaseOnCall
```

Outputs:

```text
manifests/normalized/resolved_hook_runs.json
manifests/normalized/unresolved_hook_runs.json
manifests/normalized/plugin_hook_edges.json
```

---

### Hook Event Bus

Model:

```text
hook.Run(X) = event emission
PLUGIN:X = listener
SCHEMA:X = listener
GM:X = listener
hook.Add(X, ...) = listener
```

Outputs:

```text
manifests/normalized/hook_event_emitters.json
manifests/normalized/hook_event_listeners.json
manifests/normalized/hook_event_graph.json
manifests/normalized/hook_event_bus_qa.md
```

---

### Runtime Graph V1

Merged hook emitters, listeners, files, plugins, realms.

Outputs:

```text
runtime_graph_nodes.json
runtime_graph_edges.json
runtime_graph_summary.md
```

---

### Network Graph

Modeled:

```text
netstream.Start
netstream.Hook
net.Start
net.Receive
util.AddNetworkString
net.Read*
net.Write*
```

Outputs:

```text
network_graph_nodes.json
network_graph_edges.json
network_graph_summary.md
```

---

### Network Operation Normalization

Important rule:

```text
SERVER:
netstream.Start(recipient, message, payload...)

CLIENT:
netstream.Start(message, payload...)
```

This fixed recipient-as-message pollution.

Outputs:

```text
normalized_network_operations.json
network_symbol_issues.json
network_protocol_qa.md
```

---

### Timer Graph

Modeled:

```text
timer.Create
timer.Simple
timer.Remove
timer.Exists
entity timer helpers
player action timers
legacy entity timer calls
```

Outputs:

```text
timer_graph_nodes.json
timer_graph_edges.json
timer_graph_summary.md
```

---

### Unified Runtime Topology

Merged:

```text
hook graph
network graph
timer graph
```

Current topology scale:

```text
Nodes: ~5066
Edges: ~19459
Bridge edges: ~1696
```

Outputs:

```text
runtime_topology_nodes.json
runtime_topology_edges.json
runtime_topology.json
runtime_topology_summary.md
```

---

### Semantic Document Generation

Generated retrieval-ready semantic documents:

```text
manifests/semantic/qdrant_documents.jsonl
manifests/semantic/qdrant_documents_summary.md
```

Document types:

```text
runtime_node
plugin_topology
file_topology
doctrine
```

---

## Current Canonical Source of Truth

Primary reasoning artifacts:

```text
runtime_topology_nodes.json
runtime_topology_edges.json
runtime_topology_summary.md
qdrant_documents.jsonl
runtime_doctrine.md
event_taxonomy.md
networking_model.md
persistence_model.md
```

Raw Lua remains important, but as a secondary exact-check layer.

---

## Known Current Architecture Conclusions

The framework is:

```text
simulation-oriented
event-driven
mostly server-authoritative
cross-realm UI/sync heavy
timer/scheduler driven
```

Major topology hotspots include:

```text
healthproblems
inventory
vendor
storage
needs
biorezonance
lightitems
mining
ragdollinteraction
nextbots
```

Current risk themes:

```text
UI desync
PVP/PVE FPS drops
dynamic light cost
entity simulation cost
nextbot cost
network sync correctness
memory leaks
```

---

## Next Pipeline Tasks

Immediate next technical tasks:

```text
embed_qdrant_documents.py
ingest_qdrant.py
query_qdrant.py
```

Future diagnostics:

```text
topology hotspot analysis
cross-realm propagation analysis
inventory desync analysis
network protocol cleanup
scheduler optimization
entity simulation lifecycle modeling
```

---

## Model Roles

Local Qwen2.5-Coder 14B Q4_K_M:

```text
autocomplete
small refactors
manifest helpers
deterministic transformations
```

ChatGPT / Gemini:

```text
architecture synthesis
cross-system reasoning
scheduler redesign
networking redesign
optimization strategy
UI/system design
```

LLMs are mandatory external reasoning engines, but not source of truth.
