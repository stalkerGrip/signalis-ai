# Investigation Synthesis V2

Question: `Why do vendor price labels sometimes remain visible after buying items?`

## Summary

Evidence was deduplicated with overlapping source-window clustering, ranked for causal-chain relevance, and organized into a runtime-chain candidate. This artifact is intended for targeted validation and possible runtime-chain promotion.

## Input Counts

- `raw_evidence`: `375`
- `deduped_raw_evidence`: `166`
- `ranked_clustered_evidence`: `87`
- `runtime_chain_candidate_steps`: `5`

## Findings

- Inventory membership sync and item metadata sync appear in the same causal chain but remain separate synchronization systems.
- Client UI refresh depends on item/inventory data change callbacks reaching the grid inventory panel.

## Runtime Chain Candidate

### 1. inventory_membership_sync

- Score: `6.45`
- Source: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Line: `41`
- Reasons: `runtime_chain_term:syncItemAdded, runtime_chain_term:nutInventoryAdd, runtime_chain_term:item:sync, network_propagation, inventory_membership_sync_file`

```text
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
gamemode/core/meta/inventory/sv_base_inventory.lua
```

### 2. item_metadata_sync

- Score: `6.55`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Line: `293`
- Reasons: `runtime_chain_term:setData, runtime_chain_term:vendorSPrice, runtime_chain_term:vendorBPrice, runtime_chain_term:vendorQty, runtime_chain_term:vendorMQty, vendor_entity_context_file`

```text
293: 
294: 	local clientItems = client:getChar():getInv():getItems()
295: 	for k, v in pairs(clientItems) do
296: 		v:setData("vendorBPrice", nil, client)
297: 		v:setData("vendorQty", nil, client)
298: 		v:setData("vendorSPrice", nil, client)
299: 		v:setData("vendorMQty", nil, client)
300: 	end
301: end
302: 
303: function ENT:ApplyVendorPos(pos1, pos2, pos3, ang1, ang2, ang3)
304: 	self:SetFirstPos(Vector(pos1))
305: 	self:SetSecPos(Vector(pos2))
plugins/vendor/entities/entities/nut_vendor/init.lua
```

### 3. realm_or_network_transition

- Score: `2.4`
- Source: `gamemode/core/meta/item/sv_item.lua`
- Line: `168`
- Reasons: `runtime_chain_term:invData, network_propagation`

```text
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
gamemode/core/meta/item/sv_item.lua
```

### 4. client_ui_refresh

- Score: `5.15`
- Source: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Line: `270`
- Reasons: `runtime_chain_term:ItemDataChanged, runtime_chain_term:InventoryItemDataChanged, runtime_chain_term:populateItems, grid_inventory_ui_refresh_file`

```text
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
plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua
```

### 5. vendor_context

- Score: `1.55`
- Source: `plugins/vendor/cl_networking.lua`
- Line: `15`
- Reasons: `network_propagation, hook_propagation`

```text
26: 		if (price < 0) then price = nil end
   27: 		if (stock < 0) then stock = nil end
   28: 		if (maxStock <= 0) then maxStock = nil end
   29: 		if (mode < 0) then mode = nil end
   30: 
   31: 		vendor.items[itemType] = {
   32: 			[VENDOR_PRICE] = price,
   33: 			[VENDOR_STOCK] = stock,
   34: 			[VENDOR_MAXSTOCK] = maxStock,
   35: 			[VENDOR_MODE] = mode
   36: 		}
   37: 	end
   38: 
   39: 	hook.Run("VendorSynchronized", vendor)
   40: end)
   41: 
   42: net.Receive("nutVendorOpen", function()
plugins/vendor/cl_networking.lua
```

## Top Ranked Evidence

### Evidence 1

- Score: `6.55`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Line: `293`
- Cluster: `plugins/vendor/entities/entities/nut_vendor/init.lua:ent:applyvendorpos:11`
- Reasons: `runtime_chain_term:setData, runtime_chain_term:vendorSPrice, runtime_chain_term:vendorBPrice, runtime_chain_term:vendorQty, runtime_chain_term:vendorMQty, vendor_entity_context_file`

```text
293: 
294: 	local clientItems = client:getChar():getInv():getItems()
295: 	for k, v in pairs(clientItems) do
296: 		v:setData("vendorBPrice", nil, client)
297: 		v:setData("vendorQty", nil, client)
298: 		v:setData("vendorSPrice", nil, client)
299: 		v:setData("vendorMQty", nil, client)
300: 	end
301: end
302: 
303: function ENT:ApplyVendorPos(pos1, pos2, pos3, ang1, ang2, ang3)
304: 	self:SetFirstPos(Vector(pos1))
305: 	self:SetSecPos(Vector(pos2))
plugins/vendor/entities/entities/nut_vendor/init.lua
```

### Evidence 2

- Score: `6.45`
- Source: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Line: `41`
- Cluster: `gamemode/core/meta/inventory/sv_base_inventory.lua:inventory:syncitemadded:1`
- Reasons: `runtime_chain_term:syncItemAdded, runtime_chain_term:nutInventoryAdd, runtime_chain_term:item:sync, network_propagation, inventory_membership_sync_file`

```text
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
gamemode/core/meta/inventory/sv_base_inventory.lua
```

### Evidence 3

- Score: `5.35`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Line: `290`
- Cluster: `plugins/vendor/entities/entities/nut_vendor/init.lua:ent:removereceiverfromvendor:11`
- Reasons: `runtime_chain_term:setData, runtime_chain_term:vendorSPrice, runtime_chain_term:vendorBPrice, runtime_chain_term:vendorQty, runtime_chain_term:vendorMQty, vendor_entity_context_file, secondary_vendor_flow_penalty:RemoveReceiverFromVendor`

```text
290: function ENT:RemoveReceiverFromVendor(client)
291: 	table.RemoveByValue(self.receivers, client)
292: 	client.nutVendor = nil
293: 
294: 	local clientItems = client:getChar():getInv():getItems()
295: 	for k, v in pairs(clientItems) do
296: 		v:setData("vendorBPrice", nil, client)
297: 		v:setData("vendorQty", nil, client)
298: 		v:setData("vendorSPrice", nil, client)
299: 		v:setData("vendorMQty", nil, client)
300: 	end
301: end
302: 
plugins/vendor/entities/entities/nut_vendor/init.lua
```

### Evidence 4

- Score: `5.15`
- Source: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Line: `270`
- Cluster: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua:panel:inventoryitemremoved:10`
- Reasons: `runtime_chain_term:ItemDataChanged, runtime_chain_term:InventoryItemDataChanged, runtime_chain_term:populateItems, grid_inventory_ui_refresh_file`

```text
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
plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua
```

### Evidence 5

- Score: `5.15`
- Source: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Line: `265`
- Cluster: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua:panel:inventoryitemadded:10`
- Reasons: `runtime_chain_term:ItemDataChanged, runtime_chain_term:InventoryItemDataChanged, runtime_chain_term:populateItems, grid_inventory_ui_refresh_file`

```text
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
plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua
```

### Evidence 6

- Score: `5.0`
- Source: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Line: `1`
- Cluster: `gamemode/core/meta/inventory/sv_base_inventory.lua:unknown:0`
- Reasons: `runtime_chain_term:nutInventoryAdd, runtime_chain_term:invData, network_propagation, inventory_membership_sync_file`

```text
1: local Inventory = nut.Inventory
2: 
3: -- Constants for inventory actions.
4: INV_REPLICATE = "repl" -- Replicate data about the inventory to a player.
5: 
6: local INV_TABLE_NAME = "inventories"
7: local INV_DATA_TABLE_NAME = "invdata"
8: 
9: util.AddNetworkString("nutInventoryInit")
10: util.AddNetworkString("nutInventoryData")
11: util.AddNetworkString("nutInventoryDelete")
12: util.AddNetworkString("nutInventoryAdd")
13: util.AddNetworkString("nutInventoryRemove")
gamemode/core/meta/inventory/sv_base_inventory.lua
```

### Evidence 7

- Score: `4.85`
- Source: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Line: `42`
- Cluster: `gamemode/core/meta/inventory/sv_base_inventory.lua:unknown:1`
- Reasons: `runtime_chain_term:nutInventoryAdd, runtime_chain_term:item:sync, network_propagation, inventory_membership_sync_file`

```text
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
gamemode/core/meta/inventory/sv_base_inventory.lua
```

### Evidence 8

- Score: `4.85`
- Source: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Line: `46`
- Cluster: `gamemode/core/meta/inventory/sv_base_inventory.lua:inventory:initializestorage:1`
- Reasons: `runtime_chain_term:nutInventoryAdd, runtime_chain_term:item:sync, network_propagation, inventory_membership_sync_file`

```text
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
gamemode/core/meta/inventory/sv_base_inventory.lua
```

### Evidence 9

- Score: `4.25`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Line: `209`
- Cluster: `plugins/vendor/entities/entities/nut_vendor/init.lua:ent:vendoritemsetdata:8`
- Reasons: `runtime_chain_term:setData, runtime_chain_term:vendorSPrice, runtime_chain_term:vendorQty, runtime_chain_term:vendorMQty, vendor_entity_context_file, secondary_vendor_flow_penalty:VendorItemSetData`

```text
209: 				end
210: 			end
211: 		end
212: 	end
213: end
214: 
215: function ENT:VendorItemSetData(item, qty, price, maxQty, client)
216: 	item:setData("vendorQty", qty, client)
217: 	item:setData("vendorSPrice", price, client)
218: 	item:setData("vendorMQty", maxQty, client)
219: end
220: 
221: function ENT:CanBuy(uniqueID, qty)
plugins/vendor/entities/entities/nut_vendor/init.lua
```

### Evidence 10

- Score: `4.15`
- Source: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Line: `36`
- Cluster: `gamemode/core/meta/inventory/sv_base_inventory.lua:inventory:add:1`
- Reasons: `runtime_chain_term:syncItemAdded, runtime_chain_term:item:sync, inventory_membership_sync_file`

```text
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
48: 	item:sync(recipients)
gamemode/core/meta/inventory/sv_base_inventory.lua
```

### Evidence 11

- Score: `3.6`
- Source: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Line: `12`
- Cluster: `gamemode/core/meta/inventory/sv_base_inventory.lua:inventory:additem:0`
- Reasons: `runtime_chain_term:nutInventoryAdd, network_propagation, inventory_membership_sync_file`

```text
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
gamemode/core/meta/inventory/sv_base_inventory.lua
```

### Evidence 12

- Score: `2.6`
- Source: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Line: `128`
- Cluster: `gamemode/core/meta/inventory/sv_base_inventory.lua:inventory:remove:5`
- Reasons: `runtime_chain_term:setData, inventory_membership_sync_file`

```text
128: 		d:resolve()
129: 	end
130: 
131: 	return d
132: end
133: 
134: -- Sample implementation of Inventory:remove() - delegate to removeItem
135: function Inventory:remove(itemID)
136: 	return self:removeItem(itemID)
137: end
138: 
139: -- Stores arbitrary data that can later be looked up using the given key.
140: function Inventory:setData(key, value)
gamemode/core/meta/inventory/sv_base_inventory.lua
```

### Evidence 13

- Score: `2.45`
- Source: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Line: `41`
- Cluster: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua:panel:setinventory:1`
- Reasons: `runtime_chain_term:populateItems, grid_inventory_ui_refresh_file`

```text
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
plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua
```

### Evidence 14

- Score: `2.4`
- Source: `gamemode/core/meta/item/sv_item.lua`
- Line: `168`
- Cluster: `gamemode/core/meta/item/sv_item.lua:unknown:6`
- Reasons: `runtime_chain_term:invData, network_propagation`

```text
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
gamemode/core/meta/item/sv_item.lua
```

### Evidence 15

- Score: `2.35`
- Source: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Line: `50`
- Cluster: `gamemode/core/meta/inventory/cl_base_inventory.lua:unknown:2`
- Reasons: `runtime_chain_term:nutInventoryAdd, network_propagation`

```text
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
gamemode/core/meta/inventory/cl_base_inventory.lua
```

### Evidence 16

- Score: `2.3`
- Source: `gamemode/core/meta/item/sv_item.lua`
- Line: `154`
- Cluster: `gamemode/core/meta/item/sv_item.lua:item:setdata:6`
- Reasons: `runtime_chain_term:setData, network_propagation`

```text
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
gamemode/core/meta/item/sv_item.lua
```

### Evidence 17

- Score: `1.65`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Line: `263`
- Cluster: `plugins/vendor/entities/entities/nut_vendor/init.lua:ent:onremove:10`
- Reasons: `network_propagation, hook_propagation, vendor_entity_context_file`

```text
263: 
  264: function ENT:OnRemove()
  265: 	NUT_VENDORS[self:EntIndex()] = nil
  266: 
  267: 	if (self.receivers)
  268: 	then
  269: 		net.Start("nutVendorExit")
  270: 		net.Send(self.receivers)
  271: 	end
  272: 
  273: 	if (!nut.entityDataLoaded || !PLUGIN.loadedData) then return end
  274: 	if (nut.shuttingDown || self.nutIsSafe) then return end
  275: 
  276: 	local inv = nut.inventory.instances[self.invId]
  277: 	inv:delete()
  278: 	hook.Run("StorageEntityRemoved", self, inv)
  279: end
plugins/vendor/entities/entities/nut_vendor/init.lua
```

### Evidence 18

- Score: `1.55`
- Source: `plugins/vendor/cl_networking.lua`
- Line: `15`
- Cluster: `plugins/vendor/cl_networking.lua:unknown:0`
- Reasons: `network_propagation, hook_propagation`

```text
26: 		if (price < 0) then price = nil end
   27: 		if (stock < 0) then stock = nil end
   28: 		if (maxStock <= 0) then maxStock = nil end
   29: 		if (mode < 0) then mode = nil end
   30: 
   31: 		vendor.items[itemType] = {
   32: 			[VENDOR_PRICE] = price,
   33: 			[VENDOR_STOCK] = stock,
   34: 			[VENDOR_MAXSTOCK] = maxStock,
   35: 			[VENDOR_MODE] = mode
   36: 		}
   37: 	end
   38: 
   39: 	hook.Run("VendorSynchronized", vendor)
   40: end)
   41: 
   42: net.Receive("nutVendorOpen", function()
plugins/vendor/cl_networking.lua
```

### Evidence 19

- Score: `1.5`
- Source: `plugins/vendor/cl_networking.lua`
- Line: `49`
- Cluster: `plugins/vendor/cl_networking.lua:unknown:1`
- Reasons: `network_propagation, hook_propagation`

```text
49: 
   50: net.Receive("nutVendorExit", function()
   51: 	nutVendorEnt = nil
   52: 	hook.Run("VendorExited")
   53: end)
   54: 
   55: addNetHandler("Money", function(vendor)
   56: 	local money = net.ReadInt(32)
   57: 	if (money < 0) then money = nil end
   58: 	vendor.money = money
   59: 	hook.Run("VendorMoneyUpdated", vendor, money, vendor.money)
   60: end)
   61: 
   62: addNetHandler("Price", function(vendor)
   63: 	local itemType = net.ReadString()
   64: 	local value = net.ReadInt(32)
   65: 	if (value < 0) then value = nil end
plugins/vendor/cl_networking.lua
```

### Evidence 20

- Score: `1.4`
- Source: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Line: `11`
- Cluster: `gamemode/core/meta/inventory/cl_base_inventory.lua:unknown:0`
- Reasons: `network_propagation, hook_propagation`

```text
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
gamemode/core/meta/inventory/cl_base_inventory.lua
```

### Evidence 21

- Score: `1.4`
- Source: `plugins/gridinv/plugins/gridstorage/sh_plugin.lua`
- Line: `207`
- Cluster: `plugins/gridinv/plugins/gridstorage/sh_plugin.lua:unknown:8`
- Reasons: `network_propagation, hook_propagation`

```text
207: 				netstream.Start("storageLockTrashcan", storage:EntIndex())
208: 			end
209: 
210: 			netstream.Start("inventorySetPanelStatus", false)
211: 		end
212: 
213: 		hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
214: 		LocalPlayer().stgInvPanel = localParent
215: 
216: 		localInvPanel.MainInvPanel.pair = storageInvPanel.content
217: 		storageInvPanel.content.pair = localInvPanel.MainInvPanel
218: 
219: 		localParent.OnRemove = exitStorageOnRemove
plugins/gridinv/plugins/gridstorage/sh_plugin.lua
```

### Evidence 22

- Score: `1.4`
- Source: `plugins/storage/cl_networking.lua`
- Line: `1`
- Cluster: `plugins/storage/cl_networking.lua:plugin:exitstorage:0`
- Reasons: `network_propagation, hook_propagation`

```text
1: net.Receive("nutStorageUnlock", function()
2: 	local entity = net.ReadEntity()
3: 	hook.Run("StorageUnlockPrompt", entity)
4: end)
5: 
6: net.Receive("nutStorageOpen", function()
7: 	local entity = net.ReadEntity()
8: 	hook.Run("StorageOpen", entity)
9: end)
10: 
11: function PLUGIN:exitStorage()
12: 	net.Start("nutStorageExit")
plugins/storage/cl_networking.lua
```

### Evidence 23

- Score: `1.3`
- Source: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Line: `99`
- Cluster: `gamemode/core/meta/inventory/sv_base_inventory.lua:inventory:restorefromstorage:3`
- Reasons: `inventory_membership_sync_file`

```text
99: function Inventory:restoreFromStorage(id)
100: end
101: 
102: -- Removes an item corresponding to the given item ID if it is in this
103: -- inventory. If the item belongs to this inventory, it is then deleted.
104: -- A promise is returned which is resolved after removal from this.
105: function Inventory:removeItem(itemID, preserveItem)
106: 	assert(isnumber(itemID), "itemID must be a number for remove")
107: 
108: 	local d = deferred.new()
109: 	local instance = self.items[itemID]
110: 
111: 	if (instance) then
gamemode/core/meta/inventory/sv_base_inventory.lua
```

### Evidence 24

- Score: `1.25`
- Source: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Line: `106`
- Cluster: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua:panel:additem:4`
- Reasons: `grid_inventory_ui_refresh_file`

```text
106: 	for _, item in pairs(self.inventory:getItems(true)) do
107: 		self:addItem(item)
108: 	end
109: 	self:computeOccupied()
110: end
111: 
112: function PANEL:addItem(item)
113: 	local id = item:getID()
114: 	local x, y = item:getData("x"), item:getData("y")
115: 	if (not x or not y) then return end
116: 
117: 	if (IsValid(self.icons[id])) then
118: 		self.icons[id]:Remove()
plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua
```

### Evidence 25

- Score: `1.25`
- Source: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Line: `27`
- Cluster: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua:unknown:1`
- Reasons: `grid_inventory_ui_refresh_file`

```text
27: 		for x = 0, self.gridW do
28: 			self.occupied[y][x] = false
29: 		end
30: 	end
31: 
32: 	for _, item in pairs(self.inventory:getItems(true)) do
33: 		local x, y = item:getData("x"), item:getData("y")
34: 		if (not x) then continue end
35: 
36: 		for offsetX = 0, (item.width or 1) - 1 do
37: 			for offsetY = 0, (item.height or 1) - 1 do
38: 				self.occupied[y + offsetY - 1][x + offsetX - 1] = true
39: 			end
plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua
```
