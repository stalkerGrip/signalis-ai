# SIGNALIS AI — Runtime Chain Evidence

- Source validation: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_source_validation.json`
- Evidence total: `60`

## Summary

```json
{
  "evidence_total": 60,
  "chain_confidence": "partial",
  "chain_steps_present": 10,
  "chain_steps_missing": 5,
  "by_class": {
    "gridinv_item_ui_refresh": 4,
    "gridinv_panel_repopulate": 6,
    "inventory_level_data_not_item_data": 2,
    "inventory_membership_client_event": 5,
    "inventory_membership_mutation": 2,
    "inventory_membership_network_send": 10,
    "inventory_membership_receive_add": 1,
    "inventory_recipients_resolved": 6,
    "item_full_state_sync": 4,
    "item_metadata_mutation": 4,
    "item_metadata_network_sync_send": 11,
    "item_metadata_persistence": 5
  },
  "by_file": {
    "gamemode/core/meta/inventory/sv_base_inventory.lua": 22,
    "gamemode/core/meta/item/sv_item.lua": 20,
    "plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua": 13,
    "gamemode/core/meta/inventory/cl_base_inventory.lua": 5
  }
}
```

## CHAIN-001 — Vendor purchase transfer to item metadata cleanup

- Confidence: `partial`

Steps:

- server removes/adds item across inventories
- server resolves current inventory recipients
- server sends full item state to recipients
- server sends nutInventoryAdd membership delta
- client receives nutInventoryAdd
- client emits InventoryItemAdded
- ITEM:setData mutates authoritative item data
- server sends invData item-data delta
- grid inventory panel handles item-data change
- grid inventory panel repopulates item icons

Missing steps:

- gridinv transfer identifies vendor → player purchase
- transfer crosses old inventory to player inventory boundary
- server clears vendor metadata on purchased item
- client receives invData item-data delta
- client emits ItemDataChanged

Evidence:

### E-0019 — `inventory_membership_mutation`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `12-24`
- Pattern: `Inventory add item`

```lua
12: util.AddNetworkString("nutInventoryAdd")
13: util.AddNetworkString("nutInventoryRemove")
14: 
15: -- Given an item type string, creates an instance of that item type
16: -- and adds it to this inventory. A promise is returned containing
17: -- the newly created item after it has been added to the inventory.
18: function Inventory:addItem(item)
19: 	self.items[item:getID()] = item
20: 	item.invID = self:getID()
21: 
22: 	local id = self.id
23: 	if (not isnumber(id)) then
24: 		id = NULL
function Inventory:addItem
```

### E-0020 — `inventory_recipients_resolved`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `193-205`
- Pattern: `self:getRecipients()`

```lua
193: function Inventory:removeAccessRule(rule)
194: 	table.RemoveByValue(self.config.accessRules, rule)
195: 	return self
196: end
197: 
198: -- Returns a list of players who can interact with this inventory.
199: function Inventory:getRecipients()
200: 	local recipients = {}
201: 	for _, client in ipairs(player.GetAll()) do
202: 		if (self:canAccess(INV_REPLICATE, {client = client})) then
203: 			recipients[#recipients + 1] = client
204: 		end
205: 	end
function Inventory:getRecipients
```

### E-0030 — `item_full_state_sync`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `41-53`
- Pattern: `item:sync(recipients)`

```lua
41: function Inventory:syncItemAdded(item)
42: 	assert(istable(item) and item.getID, "cannot sync non-item")
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
local recipients = self:getRecipients()
```

### E-0021 — `inventory_membership_network_send`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `35-47`
- Pattern: `Inventory:syncItemAdded`

```lua
35: 
36: -- Sample implementation of Inventory:add - delegates to addItem
37: function Inventory:add(item)
38: 	return self:addItem(item)
39: end
40: 
41: function Inventory:syncItemAdded(item)
42: 	assert(istable(item) and item.getID, "cannot sync non-item")
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
function Inventory:syncItemAdded
```

### E-0003 — `inventory_membership_receive_add`

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Lines: `50-62`
- Pattern: `net.Receive("nutInventoryAdd")`

```lua
50: 				character.vars.inv[index] = instance
51: 			end
52: 		end
53: 	end
54: end)
55: 
56: net.Receive("nutInventoryAdd", function()
57: 	local itemID = net.ReadUInt(32)
58: 	local invID = net.ReadType()
59: 	local item = nut.item.instances[itemID]
60: 	local inventory = nut.inventory.instances[invID]
61: 	if (item and inventory) then
62: 		inventory.items[itemID] = item
net.Receive("nutInventoryAdd"
```

### E-0002 — `inventory_membership_client_event`

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Lines: `57-69`
- Pattern: `hook.Run("InventoryItemAdded")`

```lua
57: 	local itemID = net.ReadUInt(32)
58: 	local invID = net.ReadType()
59: 	local item = nut.item.instances[itemID]
60: 	local inventory = nut.inventory.instances[invID]
61: 	if (item and inventory) then
62: 		inventory.items[itemID] = item
63: 		hook.Run("InventoryItemAdded", inventory, item)
64: 	end
65: end)
66: 
67: net.Receive("nutInventoryRemove", function()
68: 	local itemID = net.ReadUInt(32)
69: 	local invID = net.ReadType()
hook.Run("InventoryItemAdded"
```

### E-0043 — `item_metadata_mutation`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `154-166`
- Pattern: `function ITEM:setData`

```lua
154: 	else
155: 		net.Send(recipient)
156: 	end
157: 	self:onSync(recipient)
158: end
159: 
160: function ITEM:setData(key, value, receivers, noSave, noCheckEntity)
161: 	self.data = self.data or {}
162: 	self.data[key] = value
163: 
164: 	if (not noCheckEntity) then
165: 		local ent = self:getEntity()
166: 		if (IsValid(ent)) then
function ITEM:setData
```

### E-0055 — `item_metadata_network_sync_send`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `165-177`
- Pattern: `invData`

```lua
165: 		local ent = self:getEntity()
166: 		if (IsValid(ent)) then
167: 			ent:setNetVar("data", self.data)
168: 		end
169: 	end
170: 
171: 	if (receivers or self:getOwner()) then
172: 		netstream.Start(
173: 			receivers or self:getOwner(),
174: 			"invData",
175: 			self:getID(),
176: 			key,
177: 			value
self:getOwner
```

### E-0008 — `gridinv_item_ui_refresh`

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Lines: `265-277`
- Pattern: `PANEL:InventoryItemDataChanged`

```lua
265: -- Called when the given item has been added to the inventory.
266: function PANEL:InventoryItemAdded(item)
267: 	self:populateItems()
268: end
269: 
270: -- Called when the given item has been removed from the inventory.
271: function PANEL:InventoryItemRemoved(item)
272: 	self:populateItems()
273: end
274: 
275: -- Called when an item within this inventory has its data changed.
276: function PANEL:InventoryItemDataChanged(item, key, oldValue, newValue)
277: 	self:populateItems()
function PANEL:InventoryItemRemoved
```

### E-0012 — `gridinv_panel_repopulate`

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Lines: `261-273`
- Pattern: `self:populateItems()`

```lua
261: 		centerY - (self:GetTall() * 0.5)
262: 	)
263: end
264: 
265: -- Called when the given item has been added to the inventory.
266: function PANEL:InventoryItemAdded(item)
267: 	self:populateItems()
268: end
269: 
270: -- Called when the given item has been removed from the inventory.
271: function PANEL:InventoryItemRemoved(item)
272: 	self:populateItems()
273: end
self:populateItems()
```

## Additional Classified Evidence

### E-0023 — `inventory_membership_mutation`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `35-47`
- Pattern: `Inventory add item`

```lua
35: 
36: -- Sample implementation of Inventory:add - delegates to addItem
37: function Inventory:add(item)
38: 	return self:addItem(item)
39: end
40: 
41: function Inventory:syncItemAdded(item)
42: 	assert(istable(item) and item.getID, "cannot sync non-item")
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
function Inventory:syncItemAdded
```

### E-0022 — `inventory_recipients_resolved`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `35-47`
- Pattern: `self:getRecipients()`

```lua
35: 
36: -- Sample implementation of Inventory:add - delegates to addItem
37: function Inventory:add(item)
38: 	return self:addItem(item)
39: end
40: 
41: function Inventory:syncItemAdded(item)
42: 	assert(istable(item) and item.getID, "cannot sync non-item")
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
function Inventory:syncItemAdded
```

### E-0029 — `inventory_recipients_resolved`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `41-53`
- Pattern: `self:getRecipients()`

```lua
41: function Inventory:syncItemAdded(item)
42: 	assert(istable(item) and item.getID, "cannot sync non-item")
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
local recipients = self:getRecipients()
```

### E-0024 — `inventory_recipients_resolved`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `42-54`
- Pattern: `self:getRecipients()`

```lua
42: 	assert(istable(item) and item.getID, "cannot sync non-item")
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
54: 
item:sync(recipients)
```

### E-0037 — `inventory_recipients_resolved`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `43-55`
- Pattern: `self:getRecipients()`

```lua
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
54: 
55: -- Called to handle the logic for creating the data storage for this.
net.Start("nutInventoryAdd")
```

### E-0033 — `inventory_recipients_resolved`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `46-58`
- Pattern: `self:getRecipients()`

```lua
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
54: 
55: -- Called to handle the logic for creating the data storage for this.
56: -- Returns a promise that is resolved after the storing is done.
57: function Inventory:initializeStorage(initialData)
58: 	local d = deferred.new()
net.Send(recipients)
```

### E-0025 — `item_full_state_sync`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `42-54`
- Pattern: `item:sync(recipients)`

```lua
42: 	assert(istable(item) and item.getID, "cannot sync non-item")
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
54: 
item:sync(recipients)
```

### E-0038 — `item_full_state_sync`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `43-55`
- Pattern: `item:sync(recipients)`

```lua
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
54: 
55: -- Called to handle the logic for creating the data storage for this.
net.Start("nutInventoryAdd")
```

### E-0034 — `item_full_state_sync`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `46-58`
- Pattern: `item:sync(recipients)`

```lua
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
54: 
55: -- Called to handle the logic for creating the data storage for this.
56: -- Returns a promise that is resolved after the storing is done.
57: function Inventory:initializeStorage(initialData)
58: 	local d = deferred.new()
net.Send(recipients)
```

### E-0028 — `inventory_membership_network_send`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `41-53`
- Pattern: `Inventory:syncItemAdded`

```lua
41: function Inventory:syncItemAdded(item)
42: 	assert(istable(item) and item.getID, "cannot sync non-item")
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
local recipients = self:getRecipients()
```

### E-0031 — `inventory_membership_network_send`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `41-53`
- Pattern: `net.Start("nutInventoryAdd")`

```lua
41: function Inventory:syncItemAdded(item)
42: 	assert(istable(item) and item.getID, "cannot sync non-item")
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
local recipients = self:getRecipients()
```

### E-0026 — `inventory_membership_network_send`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `42-54`
- Pattern: `net.Start("nutInventoryAdd")`

```lua
42: 	assert(istable(item) and item.getID, "cannot sync non-item")
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
54: 
item:sync(recipients)
```

### E-0039 — `inventory_membership_network_send`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `43-55`
- Pattern: `net.Start("nutInventoryAdd")`

```lua
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
54: 
55: -- Called to handle the logic for creating the data storage for this.
net.Start("nutInventoryAdd")
```

### E-0035 — `inventory_membership_network_send`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `46-58`
- Pattern: `net.Start("nutInventoryAdd")`

```lua
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
54: 
55: -- Called to handle the logic for creating the data storage for this.
56: -- Returns a promise that is resolved after the storing is done.
57: function Inventory:initializeStorage(initialData)
58: 	local d = deferred.new()
net.Send(recipients)
```

### E-0032 — `inventory_membership_network_send`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `41-53`
- Pattern: `net.Send(recipients)`

```lua
41: function Inventory:syncItemAdded(item)
42: 	assert(istable(item) and item.getID, "cannot sync non-item")
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
local recipients = self:getRecipients()
```

### E-0027 — `inventory_membership_network_send`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `42-54`
- Pattern: `net.Send(recipients)`

```lua
42: 	assert(istable(item) and item.getID, "cannot sync non-item")
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
54: 
item:sync(recipients)
```

### E-0040 — `inventory_membership_network_send`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `43-55`
- Pattern: `net.Send(recipients)`

```lua
43: 	assert(
44: 		self.items[item:getID()],
45: 		"Item "..item:getID().." does not belong to "..self.id
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
54: 
55: -- Called to handle the logic for creating the data storage for this.
net.Start("nutInventoryAdd")
```

### E-0036 — `inventory_membership_network_send`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `46-58`
- Pattern: `net.Send(recipients)`

```lua
46: 	)
47: 	local recipients = self:getRecipients()
48: 	item:sync(recipients)
49: 	net.Start("nutInventoryAdd")
50: 		net.WriteUInt(item:getID(), 32)
51: 		net.WriteType(self.id)
52: 	net.Send(recipients)
53: end
54: 
55: -- Called to handle the logic for creating the data storage for this.
56: -- Returns a promise that is resolved after the storing is done.
57: function Inventory:initializeStorage(initialData)
58: 	local d = deferred.new()
net.Send(recipients)
```

### E-0005 — `inventory_membership_client_event`

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Lines: `61-73`
- Pattern: `hook.Run("InventoryItemAdded")`

```lua
61: 	if (item and inventory) then
62: 		inventory.items[itemID] = item
63: 		hook.Run("InventoryItemAdded", inventory, item)
64: 	end
65: end)
66: 
67: net.Receive("nutInventoryRemove", function()
68: 	local itemID = net.ReadUInt(32)
69: 	local invID = net.ReadType()
70: 	local item = nut.item.instances[itemID]
71: 	local inventory = nut.inventory.instances[invID]
72: 	if (item and inventory and inventory.items[itemID]) then
73: 		inventory.items[itemID] = nil
net.Receive("nutInventoryRemove"
```

### E-0013 — `inventory_membership_client_event`

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Lines: `261-273`
- Pattern: `PANEL:InventoryItemAdded`

```lua
261: 		centerY - (self:GetTall() * 0.5)
262: 	)
263: end
264: 
265: -- Called when the given item has been added to the inventory.
266: function PANEL:InventoryItemAdded(item)
267: 	self:populateItems()
268: end
269: 
270: -- Called when the given item has been removed from the inventory.
271: function PANEL:InventoryItemRemoved(item)
272: 	self:populateItems()
273: end
self:populateItems()
```

### E-0010 — `inventory_membership_client_event`

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Lines: `265-277`
- Pattern: `PANEL:InventoryItemAdded`

```lua
265: -- Called when the given item has been added to the inventory.
266: function PANEL:InventoryItemAdded(item)
267: 	self:populateItems()
268: end
269: 
270: -- Called when the given item has been removed from the inventory.
271: function PANEL:InventoryItemRemoved(item)
272: 	self:populateItems()
273: end
274: 
275: -- Called when an item within this inventory has its data changed.
276: function PANEL:InventoryItemDataChanged(item, key, oldValue, newValue)
277: 	self:populateItems()
function PANEL:InventoryItemRemoved
```

### E-0016 — `inventory_membership_client_event`

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Lines: `266-278`
- Pattern: `PANEL:InventoryItemAdded`

```lua
266: function PANEL:InventoryItemAdded(item)
267: 	self:populateItems()
268: end
269: 
270: -- Called when the given item has been removed from the inventory.
271: function PANEL:InventoryItemRemoved(item)
272: 	self:populateItems()
273: end
274: 
275: -- Called when an item within this inventory has its data changed.
276: function PANEL:InventoryItemDataChanged(item, key, oldValue, newValue)
277: 	self:populateItems()
278: end
self:populateItems()
```

### E-0052 — `item_metadata_mutation`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `156-168`
- Pattern: `function ITEM:setData`

```lua
156: 	end
157: 	self:onSync(recipient)
158: end
159: 
160: function ITEM:setData(key, value, receivers, noSave, noCheckEntity)
161: 	self.data = self.data or {}
162: 	self.data[key] = value
163: 
164: 	if (not noCheckEntity) then
165: 		local ent = self:getEntity()
166: 		if (IsValid(ent)) then
167: 			ent:setNetVar("data", self.data)
168: 		end
self.data[key] = value
```

### E-0044 — `item_metadata_mutation`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `154-166`
- Pattern: `self.data[key] = value`

```lua
154: 	else
155: 		net.Send(recipient)
156: 	end
157: 	self:onSync(recipient)
158: end
159: 
160: function ITEM:setData(key, value, receivers, noSave, noCheckEntity)
161: 	self.data = self.data or {}
162: 	self.data[key] = value
163: 
164: 	if (not noCheckEntity) then
165: 		local ent = self:getEntity()
166: 		if (IsValid(ent)) then
function ITEM:setData
```

### E-0053 — `item_metadata_mutation`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `156-168`
- Pattern: `self.data[key] = value`

```lua
156: 	end
157: 	self:onSync(recipient)
158: end
159: 
160: function ITEM:setData(key, value, receivers, noSave, noCheckEntity)
161: 	self.data = self.data or {}
162: 	self.data[key] = value
163: 
164: 	if (not noCheckEntity) then
165: 		local ent = self:getEntity()
166: 		if (IsValid(ent)) then
167: 			ent:setNetVar("data", self.data)
168: 		end
self.data[key] = value
```

### E-0046 — `item_metadata_network_sync_send`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `166-178`
- Pattern: `invData`

```lua
166: 		if (IsValid(ent)) then
167: 			ent:setNetVar("data", self.data)
168: 		end
169: 	end
170: 
171: 	if (receivers or self:getOwner()) then
172: 		netstream.Start(
173: 			receivers or self:getOwner(),
174: 			"invData",
175: 			self:getID(),
176: 			key,
177: 			value
178: 		)
netstream.Start
```

### E-0057 — `item_metadata_network_sync_send`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `167-179`
- Pattern: `invData`

```lua
167: 			ent:setNetVar("data", self.data)
168: 		end
169: 	end
170: 
171: 	if (receivers or self:getOwner()) then
172: 		netstream.Start(
173: 			receivers or self:getOwner(),
174: 			"invData",
175: 			self:getID(),
176: 			key,
177: 			value
178: 		)
179: 	end
self:getOwner
```

### E-0041 — `item_metadata_network_sync_send`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `168-180`
- Pattern: `invData`

```lua
168: 		end
169: 	end
170: 
171: 	if (receivers or self:getOwner()) then
172: 		netstream.Start(
173: 			receivers or self:getOwner(),
174: 			"invData",
175: 			self:getID(),
176: 			key,
177: 			value
178: 		)
179: 	end
180: 
"invData"
```

### E-0056 — `item_metadata_network_sync_send`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `165-177`
- Pattern: `netstream.Start(..., "invData", ...)`

```lua
165: 		local ent = self:getEntity()
166: 		if (IsValid(ent)) then
167: 			ent:setNetVar("data", self.data)
168: 		end
169: 	end
170: 
171: 	if (receivers or self:getOwner()) then
172: 		netstream.Start(
173: 			receivers or self:getOwner(),
174: 			"invData",
175: 			self:getID(),
176: 			key,
177: 			value
self:getOwner
```

### E-0047 — `item_metadata_network_sync_send`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `166-178`
- Pattern: `netstream.Start(..., "invData", ...)`

```lua
166: 		if (IsValid(ent)) then
167: 			ent:setNetVar("data", self.data)
168: 		end
169: 	end
170: 
171: 	if (receivers or self:getOwner()) then
172: 		netstream.Start(
173: 			receivers or self:getOwner(),
174: 			"invData",
175: 			self:getID(),
176: 			key,
177: 			value
178: 		)
netstream.Start
```

### E-0058 — `item_metadata_network_sync_send`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `167-179`
- Pattern: `netstream.Start(..., "invData", ...)`

```lua
167: 			ent:setNetVar("data", self.data)
168: 		end
169: 	end
170: 
171: 	if (receivers or self:getOwner()) then
172: 		netstream.Start(
173: 			receivers or self:getOwner(),
174: 			"invData",
175: 			self:getID(),
176: 			key,
177: 			value
178: 		)
179: 	end
self:getOwner
```

### E-0042 — `item_metadata_network_sync_send`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `168-180`
- Pattern: `netstream.Start(..., "invData", ...)`

```lua
168: 		end
169: 	end
170: 
171: 	if (receivers or self:getOwner()) then
172: 		netstream.Start(
173: 			receivers or self:getOwner(),
174: 			"invData",
175: 			self:getID(),
176: 			key,
177: 			value
178: 		)
179: 	end
180: 
"invData"
```

### E-0059 — `item_metadata_network_sync_send`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `221-233`
- Pattern: `netstream.Start(..., "invData", ...)`

```lua
221: 
222: 		if (IsValid(ent)) then
223: 			ent:setNetVar("quantity", self.quantity)
224: 		end
225: 	end
226: 
227: 	if (receivers or self:getOwner()) then
228: 		netstream.Start(
229: 			receivers or self:getOwner(),
230: 			"invQuantity",
231: 			self:getID(),
232: 			self.quantity
233: 		)
self:getOwner
```

### E-0048 — `item_metadata_network_sync_send`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `222-234`
- Pattern: `netstream.Start(..., "invData", ...)`

```lua
222: 		if (IsValid(ent)) then
223: 			ent:setNetVar("quantity", self.quantity)
224: 		end
225: 	end
226: 
227: 	if (receivers or self:getOwner()) then
228: 		netstream.Start(
229: 			receivers or self:getOwner(),
230: 			"invQuantity",
231: 			self:getID(),
232: 			self.quantity
233: 		)
234: 	end
netstream.Start
```

### E-0060 — `item_metadata_network_sync_send`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `223-235`
- Pattern: `netstream.Start(..., "invData", ...)`

```lua
223: 			ent:setNetVar("quantity", self.quantity)
224: 		end
225: 	end
226: 
227: 	if (receivers or self:getOwner()) then
228: 		netstream.Start(
229: 			receivers or self:getOwner(),
230: 			"invQuantity",
231: 			self:getID(),
232: 			self.quantity
233: 		)
234: 	end
235: 
self:getOwner
```

### E-0014 — `gridinv_item_ui_refresh`

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Lines: `266-278`
- Pattern: `PANEL:InventoryItemDataChanged`

```lua
266: function PANEL:InventoryItemAdded(item)
267: 	self:populateItems()
268: end
269: 
270: -- Called when the given item has been removed from the inventory.
271: function PANEL:InventoryItemRemoved(item)
272: 	self:populateItems()
273: end
274: 
275: -- Called when an item within this inventory has its data changed.
276: function PANEL:InventoryItemDataChanged(item, key, oldValue, newValue)
277: 	self:populateItems()
278: end
self:populateItems()
```

### E-0006 — `gridinv_item_ui_refresh`

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Lines: `270-282`
- Pattern: `PANEL:InventoryItemDataChanged`

```lua
270: -- Called when the given item has been removed from the inventory.
271: function PANEL:InventoryItemRemoved(item)
272: 	self:populateItems()
273: end
274: 
275: -- Called when an item within this inventory has its data changed.
276: function PANEL:InventoryItemDataChanged(item, key, oldValue, newValue)
277: 	self:populateItems()
278: end
279: 
280: function PANEL:computeHeldPanel()
281: 	if (not nut.item.held or nut.item.held == self) then return end
282: 	local cursorX, cursorY = self:LocalCursorPos()
InventoryItemDataChanged
```

### E-0017 — `gridinv_item_ui_refresh`

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Lines: `271-283`
- Pattern: `PANEL:InventoryItemDataChanged`

```lua
271: function PANEL:InventoryItemRemoved(item)
272: 	self:populateItems()
273: end
274: 
275: -- Called when an item within this inventory has its data changed.
276: function PANEL:InventoryItemDataChanged(item, key, oldValue, newValue)
277: 	self:populateItems()
278: end
279: 
280: function PANEL:computeHeldPanel()
281: 	if (not nut.item.held or nut.item.held == self) then return end
282: 	local cursorX, cursorY = self:LocalCursorPos()
283: 	if (
self:populateItems()
```

### E-0009 — `gridinv_panel_repopulate`

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Lines: `265-277`
- Pattern: `self:populateItems()`

```lua
265: -- Called when the given item has been added to the inventory.
266: function PANEL:InventoryItemAdded(item)
267: 	self:populateItems()
268: end
269: 
270: -- Called when the given item has been removed from the inventory.
271: function PANEL:InventoryItemRemoved(item)
272: 	self:populateItems()
273: end
274: 
275: -- Called when an item within this inventory has its data changed.
276: function PANEL:InventoryItemDataChanged(item, key, oldValue, newValue)
277: 	self:populateItems()
function PANEL:InventoryItemRemoved
```

### E-0015 — `gridinv_panel_repopulate`

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Lines: `266-278`
- Pattern: `self:populateItems()`

```lua
266: function PANEL:InventoryItemAdded(item)
267: 	self:populateItems()
268: end
269: 
270: -- Called when the given item has been removed from the inventory.
271: function PANEL:InventoryItemRemoved(item)
272: 	self:populateItems()
273: end
274: 
275: -- Called when an item within this inventory has its data changed.
276: function PANEL:InventoryItemDataChanged(item, key, oldValue, newValue)
277: 	self:populateItems()
278: end
self:populateItems()
```

### E-0007 — `gridinv_panel_repopulate`

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Lines: `270-282`
- Pattern: `self:populateItems()`

```lua
270: -- Called when the given item has been removed from the inventory.
271: function PANEL:InventoryItemRemoved(item)
272: 	self:populateItems()
273: end
274: 
275: -- Called when an item within this inventory has its data changed.
276: function PANEL:InventoryItemDataChanged(item, key, oldValue, newValue)
277: 	self:populateItems()
278: end
279: 
280: function PANEL:computeHeldPanel()
281: 	if (not nut.item.held or nut.item.held == self) then return end
282: 	local cursorX, cursorY = self:LocalCursorPos()
InventoryItemDataChanged
```

### E-0018 — `gridinv_panel_repopulate`

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Lines: `271-283`
- Pattern: `self:populateItems()`

```lua
271: function PANEL:InventoryItemRemoved(item)
272: 	self:populateItems()
273: end
274: 
275: -- Called when an item within this inventory has its data changed.
276: function PANEL:InventoryItemDataChanged(item, key, oldValue, newValue)
277: 	self:populateItems()
278: end
279: 
280: function PANEL:computeHeldPanel()
281: 	if (not nut.item.held or nut.item.held == self) then return end
282: 	local cursorX, cursorY = self:LocalCursorPos()
283: 	if (
self:populateItems()
```

### E-0011 — `gridinv_panel_repopulate`

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Lines: `41-53`
- Pattern: `self:populateItems()`

```lua
41: 	end
42: end
43: 
44: function PANEL:setInventory(inventory)
45: 	self:nutListenForInventoryChanges(inventory)
46: 	self.inventory = inventory
47: 	self:populateItems()
48: end
49: 
50: function PANEL:setGridSize(width, height, iconSize)
51: 	self.size = iconSize or NS_ICON_SIZE
52: 	self.gridW = width
53: 	self.gridH = height
self:populateItems()
```

### E-0045 — `item_metadata_persistence`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `154-166`
- Pattern: `database/noSave behavior`

```lua
154: 	else
155: 		net.Send(recipient)
156: 	end
157: 	self:onSync(recipient)
158: end
159: 
160: function ITEM:setData(key, value, receivers, noSave, noCheckEntity)
161: 	self.data = self.data or {}
162: 	self.data[key] = value
163: 
164: 	if (not noCheckEntity) then
165: 		local ent = self:getEntity()
166: 		if (IsValid(ent)) then
function ITEM:setData
```

### E-0054 — `item_metadata_persistence`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `156-168`
- Pattern: `database/noSave behavior`

```lua
156: 	end
157: 	self:onSync(recipient)
158: end
159: 
160: function ITEM:setData(key, value, receivers, noSave, noCheckEntity)
161: 	self.data = self.data or {}
162: 	self.data[key] = value
163: 
164: 	if (not noCheckEntity) then
165: 		local ent = self:getEntity()
166: 		if (IsValid(ent)) then
167: 			ent:setNetVar("data", self.data)
168: 		end
self.data[key] = value
```

### E-0049 — `item_metadata_persistence`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `183-195`
- Pattern: `database/noSave behavior`

```lua
183: 	-- Legacy support for x, y data
184: 	if (key == "x" or key == "y") then
185: 		value = tonumber(value)
186: 		if (MYSQLOO_PREPARED) then
187: 			nut.db.preparedCall("item"..key, nil, value, self:getID())
188: 		else
189: 			nut.db.updateTable({
190: 				["_"..key] = value
191: 			}, nil, "items", "_itemID = "..self:getID())
192: 		end
193: 		return
194: 	end
195: 
nut.db.updateTable
```

### E-0050 — `item_metadata_persistence`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `198-210`
- Pattern: `database/noSave behavior`

```lua
198: 	local x, y = self.data.x, self.data.y
199: 	self.data.x, self.data.y = nil, nil
200: 
201: 	if (MYSQLOO_PREPARED) then
202: 		nut.db.preparedCall("itemData", nil, self.data, self:getID())
203: 	else
204: 		nut.db.updateTable({
205: 			_data = self.data
206: 		}, nil, "items", "_itemID = "..self:getID())
207: 	end
208: 
209: 	self.data.x, self.data.y = x, y
210: end
nut.db.updateTable
```

### E-0051 — `item_metadata_persistence`

- File: `gamemode/core/meta/item/sv_item.lua`
- Role: `server_item_data`
- Lines: `237-249`
- Pattern: `database/noSave behavior`

```lua
237: 
238: 	-- Weird workaround, but essentially xy data should not be saved in the
239: 	-- data column.
240: 	if (MYSQLOO_PREPARED) then
241: 		nut.db.preparedCall("itemq", nil, self.quantity, self:getID())
242: 	else
243: 		nut.db.updateTable({
244: 			_quantity = self.quantity
245: 		}, nil, "items", "_itemID = "..self:getID())
246: 	end
247: end
248: 
249: function ITEM:interact(action, client, entity, data)
nut.db.updateTable
```

### E-0004 — `inventory_level_data_not_item_data`

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Lines: `1-9`
- Pattern: `nutInventoryData / InventoryDataChanged`

```lua
1: local Inventory = nut.Inventory
2: 
3: net.Receive("nutInventoryData", function()
4: 	local id = net.ReadType()
5: 	local key = net.ReadString()
6: 	local value = net.ReadType()
7: 	local instance = nut.inventory.instances[id]
8: 	if (not instance) then
9: 		ErrorNoHalt("Got data "..key.." for non-existent instance "..id)
net.Receive("nutInventoryData"
```

### E-0001 — `inventory_level_data_not_item_data`

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Lines: `11-23`
- Pattern: `nutInventoryData / InventoryDataChanged`

```lua
11: 	end
12: 
13: 	local oldValue = instance.data[key]
14: 	instance.data[key] = value
15: 	instance:onDataChanged(key, oldValue, value)
16: 
17: 	hook.Run("InventoryDataChanged", instance, key, oldValue, value)
18: end)
19: 
20: net.Receive("nutInventoryInit", function()
21: 	local id = net.ReadType()
22: 	local typeID = net.ReadString()
23: 	local data = net.ReadTable()
hook.Run("InventoryDataChanged"
```
