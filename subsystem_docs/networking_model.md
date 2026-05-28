# SIGNALIS AI — Networking Model

## Current Networking Reality

The project uses mixed networking:

```text
netstream2 = preferred/current abstraction
raw net.Start/net.Receive = mostly NutScript base / legacy
```

The networking layer is used for:

```text
entity realm communication
UI opening/updating
character/HUD data transfer
inventory/vendor/storage interactions
admin/config tooling
health/status UI
```

Known issues:

```text
large payloads
UI desync
mixed protocol naming
possible missing sync contracts
legacy raw net usage
```

---

## netstream2 Semantics

Important project rule:

### Server realm

```lua
netstream.Start(recipient, message, payload...)
```

Examples:

```lua
netstream.Start(client, "inventoryOpen", data)
netstream.Start(receivers, "hudAddStatusIcon", status)
```

### Client realm

```lua
netstream.Start(message, payload...)
```

Example:

```lua
netstream.Start("invAct", index, entity)
```

Reason:

```text
client sends to server implicitly as LocalPlayer()
```

---

## Raw GMod net Semantics

Raw net model:

```lua
net.Start(messageName, unreliable?)
net.Write*
net.Send(...)
```

Receiver:

```lua
net.Receive(messageName, function(len, ply)
    ...
end)
```

Server-side registration:

```lua
util.AddNetworkString(messageName)
```

Raw GMod net messages should generally have `util.AddNetworkString` on server before use.

---

## Network Graph Concepts

Stable node IDs should distinguish:

```text
netmsg:inventoryOpen
netop:send:<file>:<line>
netop:receive:<file>:<line>
file:plugins/inventory/cl_hooks.lua
plugin:inventory
realm:client
```

Important edge types:

```text
file_sends_network_message
file_receives_network_message
sends_network_message
receives_network_message
network_dispatches_to
registers_network_message
reads_network_payload
writes_network_payload
```

---

## Protocol Naming Reality

Current protocol naming is inconsistent:

```text
inv*
inventory*
char*
character*
hud*
diseases*
vendor*
```

This is expected legacy/mixed-code reality.

Do not assume inconsistent naming means incorrect behavior.

---

## Protocol/Subystem Guesses

Useful protocol classes:

```text
inventory_item_storage
ui_hud
vendor
character
health_status
admin_config
crafting
misc
```

---

## Dynamic Message Names

Dynamic/symbolic messages are allowed in the codebase.

Examples:

```lua
netstream.Start(client, hookName, ...)
netstream.Start(client, callbackHook, ...)
```

However, many previously “dynamic” values were actually recipient variables misread as messages.

Corrected examples:

```text
self
client
receiver
targets
activator
v
```

These are usually recipients, not protocol IDs, when used as first argument server-side.

---

## Normalization Rules

For `netstream.Start`:

```text
if realm == server:
    arg0 = recipient
    arg1 = message
    arg2+ = payload

if realm == client:
    arg0 = message
    arg1+ = payload

if realm == shared/unknown:
    infer using argument shape and suspicious recipient names
```

For `net.Start`:

```text
arg0 = message
```

---

## QA Categories

Network QA should detect:

```text
raw_net_missing_addnetworkstring
sender_without_receiver
receiver_without_sender
dynamic_message_name
suspicious_message_id
recipient_misread_as_message
large_payload_risk
legacy_raw_net_usage
```

---

## Known Architecture Goals

Future direction:

```text
decrease FPS drops
improve sync reliability
reduce UI desync
centralize protocol contracts
reduce ad-hoc netstream calls
batch where appropriate
make state replication explicit
```

---

## Important External Constraint

Raw GMod net has practical payload limitations.

Large payload warnings are weak static signals, not proof of bugs.

True validation requires runtime profiling / payload measurement.

---

## Design Principle

Networking should become:

```text
contract-driven
subsystem-tagged
realm-explicit
less ad-hoc
observable in topology
```
