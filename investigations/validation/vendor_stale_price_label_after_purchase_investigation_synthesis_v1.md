# Investigation Synthesis V1

Question: `Why do vendor price labels sometimes remain visible after buying items?`

## Summary

Evidence was deduplicated, ranked, and organized into a runtime-chain candidate. This synthesis is not final truth; it is an investigation artifact intended to guide targeted source validation and promotion.

## Runtime Chain Candidate

### inventory_membership_sync

- Score: `3.3`
- Source: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Line: `41`
- Reasons: `runtime_chain_term:nutInventoryAdd, runtime_chain_term:syncItemAdded, causal_term:sync, network_propagation`

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
```

### item_metadata_sync

- Score: `4.2`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Line: `290`
- Reasons: `runtime_chain_term:setData, causal_term:vendorSPrice, causal_term:vendorBPrice, causal_term:vendorQty, causal_term:vendorMQty, causal_term:client`

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
```

### realm_transition

- Score: `4.2`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Line: `290`
- Reasons: `runtime_chain_term:setData, causal_term:vendorSPrice, causal_term:vendorBPrice, causal_term:vendorQty, causal_term:vendorMQty, causal_term:client`

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
  303: function ENT:ApplyVendorPos(pos1, pos2, pos3, ang1, ang2, ang3)
  304: 	self:SetFirstPos(Vector(pos1))
  305: 	self:SetSecPos(Vector(pos2))
  306: 	self:SetThdPos(Vector(pos3))
```

### client_ui_refresh

- Score: `3.0`
- Source: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Line: `270`
- Reasons: `runtime_chain_term:ItemDataChanged, runtime_chain_term:InventoryItemDataChanged, runtime_chain_term:populateItems`

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
```

### vendor_context

- Score: `4.2`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Line: `290`
- Reasons: `runtime_chain_term:setData, causal_term:vendorSPrice, causal_term:vendorBPrice, causal_term:vendorQty, causal_term:vendorMQty, causal_term:client`

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
```

## Top Ranked Evidence

### Evidence 1

- Score: `4.2`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Reasons: `runtime_chain_term:setData, causal_term:vendorSPrice, causal_term:vendorBPrice, causal_term:vendorQty, causal_term:vendorMQty, causal_term:client`

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
```

### Evidence 2

- Score: `4.2`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Reasons: `runtime_chain_term:setData, causal_term:vendorSPrice, causal_term:vendorBPrice, causal_term:vendorQty, causal_term:vendorMQty, causal_term:client`

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
```

### Evidence 3

- Score: `4.2`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Reasons: `runtime_chain_term:setData, causal_term:vendorSPrice, causal_term:vendorBPrice, causal_term:vendorQty, causal_term:vendorMQty, causal_term:client`

```text
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
303: function ENT:ApplyVendorPos(pos1, pos2, pos3, ang1, ang2, ang3)
```

### Evidence 4

- Score: `4.2`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Reasons: `runtime_chain_term:setData, causal_term:vendorSPrice, causal_term:vendorBPrice, causal_term:vendorQty, causal_term:vendorMQty, causal_term:client`

```text
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
303: function ENT:ApplyVendorPos(pos1, pos2, pos3, ang1, ang2, ang3)
304: 	self:SetFirstPos(Vector(pos1))
```

### Evidence 5

- Score: `4.2`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Reasons: `runtime_chain_term:setData, causal_term:vendorSPrice, causal_term:vendorBPrice, causal_term:vendorQty, causal_term:vendorMQty, causal_term:client`

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
  303: function ENT:ApplyVendorPos(pos1, pos2, pos3, ang1, ang2, ang3)
  304: 	self:SetFirstPos(Vector(pos1))
  305: 	self:SetSecPos(Vector(pos2))
  306: 	self:SetThdPos(Vector(pos3))
```

### Evidence 6

- Score: `3.6`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Reasons: `runtime_chain_term:setData, causal_term:vendorSPrice, causal_term:vendorQty, causal_term:vendorMQty, causal_term:client`

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
```

### Evidence 7

- Score: `3.6`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Reasons: `runtime_chain_term:setData, causal_term:vendorSPrice, causal_term:vendorQty, causal_term:vendorMQty, causal_term:client`

```text
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
222: 	local vendorNeed = true
223: 	if (self.items[uniqueID]
224: 		&& self.items[uniqueID].maxQty
```

### Evidence 8

- Score: `3.6`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Reasons: `runtime_chain_term:setData, causal_term:vendorSPrice, causal_term:vendorQty, causal_term:vendorMQty, causal_term:client`

```text
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
222: 	local vendorNeed = true
```

### Evidence 9

- Score: `3.6`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Reasons: `runtime_chain_term:setData, causal_term:vendorSPrice, causal_term:vendorQty, causal_term:vendorMQty, causal_term:client`

```text
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
222: 	local vendorNeed = true
223: 	if (self.items[uniqueID]
```

### Evidence 10

- Score: `3.6`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Reasons: `runtime_chain_term:setData, causal_term:vendorSPrice, causal_term:vendorQty, causal_term:vendorMQty, causal_term:client`

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
  222: 	local vendorNeed = true
  223: 	if (self.items[uniqueID]
  224: 		&& self.items[uniqueID].maxQty
  225: 		&& self.items[uniqueID].maxQty > 0
```

### Evidence 11

- Score: `3.3`
- Source: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Reasons: `runtime_chain_term:nutInventoryAdd, runtime_chain_term:syncItemAdded, causal_term:sync, network_propagation`

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
```

### Evidence 12

- Score: `3.0`
- Source: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Reasons: `runtime_chain_term:ItemDataChanged, runtime_chain_term:InventoryItemDataChanged, runtime_chain_term:populateItems`

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
```

### Evidence 13

- Score: `3.0`
- Source: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Reasons: `runtime_chain_term:ItemDataChanged, runtime_chain_term:InventoryItemDataChanged, runtime_chain_term:populateItems`

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
```

### Evidence 14

- Score: `3.0`
- Source: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Reasons: `runtime_chain_term:ItemDataChanged, runtime_chain_term:InventoryItemDataChanged, runtime_chain_term:populateItems`

```text
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
```

### Evidence 15

- Score: `3.0`
- Source: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Reasons: `runtime_chain_term:ItemDataChanged, runtime_chain_term:InventoryItemDataChanged, runtime_chain_term:populateItems`

```text
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
```

### Evidence 16

- Score: `3.0`
- Source: `plugins/vendor/cl_networking.lua`
- Reasons: `runtime_chain_term:cl_networking, causal_term:sync, hook_propagation, network_propagation`

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
```

### Evidence 17

- Score: `3.0`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Reasons: `runtime_chain_term:setData, causal_term:vendorBPrice, causal_term:vendorQty, causal_term:client`

```text
285: 	else
286: 		self.factions[factionID] = true
287: 	end
288: end
289: 
290: function ENT:RemoveReceiverFromVendor(client)
291: 	table.RemoveByValue(self.receivers, client)
292: 	client.nutVendor = nil
293: 
294: 	local clientItems = client:getChar():getInv():getItems()
295: 	for k, v in pairs(clientItems) do
296: 		v:setData("vendorBPrice", nil, client)
297: 		v:setData("vendorQty", nil, client)
```

### Evidence 18

- Score: `2.4`
- Source: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Reasons: `runtime_chain_term:setData, causal_term:vendorBPrice, causal_term:client`

```text
284: 		self.factions[factionID] = nil
285: 	else
286: 		self.factions[factionID] = true
287: 	end
288: end
289: 
290: function ENT:RemoveReceiverFromVendor(client)
291: 	table.RemoveByValue(self.receivers, client)
292: 	client.nutVendor = nil
293: 
294: 	local clientItems = client:getChar():getInv():getItems()
295: 	for k, v in pairs(clientItems) do
296: 		v:setData("vendorBPrice", nil, client)
```

### Evidence 19

- Score: `2.4`
- Source: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Reasons: `runtime_chain_term:nutInventoryAdd, causal_term:sync, network_propagation`

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
```

### Evidence 20

- Score: `2.4`
- Source: `plugins/vendor/cl_networking.lua`
- Reasons: `runtime_chain_term:cl_networking, hook_propagation, network_propagation`

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
```
