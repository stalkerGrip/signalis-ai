# SIGNALIS AI — Project Memory

## Current Phase

Retrieval-Guided Architecture Intelligence

Current Sprint:
Investigation Pipeline V1

## Current Bottleneck

Runtime Propagation Topology V2 is partially successful.

Validated:

- hook_event → listener fanout exists
- network_message → receiver fanout exists
- listener → owner file/plugin exits exist
- PlayerLoadedChar listener dead ends reduced significantly

Current missing propagation:

callback body
→ emitted hook

Known human-validated examples:

netstream:invData
→ receiver callback
→ ItemDataChanged

and

PlayerLoadedChar
→ GM:PlayerLoadedChar
→ PlayerLoadout

PlayerLoadout
→ GM:PlayerLoadout
→ PostPlayerLoadout

Conclusion:

Runtime Chain Builder V5 is not currently the primary bottleneck.

Current bottleneck is missing callback-body propagation in runtime_propagation_topology.json.

Likely next artifact:

Runtime Propagation Topology Builder V3

Goal:

Support deterministic propagation:

network_operation
→ emitted hook_event

hook_listener
→ emitted hook_event

when supported by extracted source evidence.

---

## Completed Infrastructure

- raw Lua extraction manifests
- semantic normalization
- hook/event graph
- network graph
- timer graph
- unified runtime topology
- semantic documents
- embeddings/Qdrant ingestion
- deterministic reranking
- context pack generation
- subsystem document generation

Investigation Pipeline V1:

- Runtime Facts V2
- Runtime Fact Graph V2
- Runtime Fact Topology Mapper V3
- Runtime Fact Topology Regression
- Runtime Chain Builder V5
- Runtime Topology Node Probe

Validated promoted chains:

1. vendor_purchase_item_data_propagation_topology_chain
2. characterload_inventory_initialization_lifecycle_chain

---

## Runtime Propagation Topology Milestone

Runtime Topology Node Probe established that:

runtime_topology.json is primarily a relationship graph.

Examples:

- hook events contain emits/listens_to relationships
- network messages contain sender/receiver relationships
- classification edges exist
- ownership edges exist

However many runtime propagation paths are not directly traversable.

Observed examples:

- netmsg:netstream:invData
  - incoming relationships present
  - outgoing propagation edges absent

- hook:ItemDataChanged
  - listeners exist
  - hook_event -> listener propagation edges absent

- hook:PlayerLoadedChar
  - listeners exist
  - propagation fanout edges absent

Conclusion:

Runtime chain reconstruction requires a dedicated propagation topology artifact.

Planned artifact:

manifests/normalized/runtime_propagation_topology.json

Planned builder:

scripts/investigation/runtime_propagation_topology_builder.py

Purpose:

Transform relationship-oriented topology into traversal-oriented topology suitable for:

- runtime chain reconstruction
- topology-supported validation
- chain confidence scoring
- architecture intelligence

---

## Investigation Note

runtime_chain_builder_v5 performs generic BFS traversal using the topology supplied through:

--runtime-topology

Current unsupported links are caused by missing callback-body propagation edges in runtime_propagation_topology.json.

Current evidence does not indicate a known BFS or CLI defect in runtime_chain_builder_v5.

Do not modify Runtime Chain Builder V5 unless regression or validation proves a builder defect.

## Canonical Environment

Python:
3.11

Embedding model:
BAAI/bge-small-en-v1.5

Qdrant dimension:
384

Source roots:
config/workspace.yaml

Rule:

Workspace root != source root.

Investigation scripts must load source roots from config/workspace.yaml.