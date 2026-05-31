# SIGNALIS AI — Runtime Chain Evidence

- Source validation: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_targeted_validation_patched_source_validation.json`
- Evidence total: `120`

## Summary

```json
{
  "evidence_total": 120,
  "chain_confidence": "validated",
  "chain_steps_present": 15,
  "chain_steps_missing": 0,
  "by_class": {
    "gridinv_item_ui_refresh": 4,
    "gridinv_panel_repopulate": 6,
    "inventory_boundary_transfer": 16,
    "inventory_level_data_not_item_data": 2,
    "inventory_membership_client_event": 5,
    "inventory_membership_mutation": 8,
    "inventory_membership_network_send": 10,
    "inventory_membership_receive_add": 1,
    "inventory_recipients_resolved": 6,
    "item_full_state_sync": 4,
    "item_metadata_client_event": 7,
    "item_metadata_mutation": 4,
    "item_metadata_network_receive": 13,
    "item_metadata_network_sync_send": 11,
    "item_metadata_persistence": 5,
    "vendor_metadata_cleanup": 10,
    "vendor_purchase_detection": 8
  },
  "by_file": {
    "plugins/gridinv/sv_transfer.lua": 40,
    "gamemode/core/meta/inventory/sv_base_inventory.lua": 22,
    "gamemode/core/meta/item/sv_item.lua": 20,
    "gamemode/core/libs/item/cl_networking.lua": 20,
    "plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua": 13,
    "gamemode/core/meta/inventory/cl_base_inventory.lua": 5
  }
}
```

## Confidence Meaning

- `validated`: every required causal boundary for CHAIN-001 is present in source-validation evidence.
- `complete`: the high-level chain is present, but one or more supporting boundary classes are missing.
- `strong_partial` / `partial`: useful propagation evidence exists, but the chain is not fully source-validated.

## CHAIN-001 — Vendor purchase transfer to item metadata cleanup

- Confidence: `validated`

Steps:

- gridinv transfer identifies vendor → player purchase
- transfer crosses old inventory to player inventory boundary
- server removes/adds item across inventories
- server resolves current inventory recipients
- server sends full item state to recipients
- server sends nutInventoryAdd membership delta
- client receives nutInventoryAdd
- client emits InventoryItemAdded
- server clears vendor metadata on purchased item
- ITEM:setData mutates authoritative item data
- server sends invData item-data delta
- client receives invData item-data delta
- client emits ItemDataChanged
- grid inventory panel handles item-data change
- grid inventory panel repopulates item icons

Missing steps:

- none

Evidence:

### E-0065 — `vendor_purchase_detection`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `116-128`
- Pattern: `vendorSellItem`

```lua
116: 
117: 	local tryCombineWith
118: 	local originalAddRes
119: 	local targetCharId = inventory:getData("char")
120: 
121: 	if ((x == 0 && y == 0 && inventory:findFreePosition(item) == nil) ||
122: 		(vendorSellItem && inventory:findFreePosition(item) == nil))
123: 	then
124: 		return true
125: 	end
126: 
127: 	return oldInventory:removeItem(itemID, true)
128: 		:next(function()
vendorSellItem
```

### E-0100 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `1-11`
- Pattern: `oldInventory + destination inventory`

```lua
1: util.AddNetworkString("nutTransferItem")
2: 
3: local TRANSFER = "transfer"
4: 
5: function PLUGIN:HandleItemTransferRequest(client, itemID, x, y, invID, laltPressed)
6: 	-- Get the item that should be moved, its inventory, and the destination.
7: 	local inventory = nut.inventory.instances[invID]
8: 	local item = nut.item.instances[itemID]
9: 	if (not item) then return end
10: 	local oldInventory = nut.inventory.instances[item.invID]
11: 	if (not oldInventory or not oldInventory.items[itemID]) then
HandleItemTransferRequest
```

### E-0067 — `inventory_membership_mutation`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `116-128`
- Pattern: `remove/add item transfer`

```lua
116: 
117: 	local tryCombineWith
118: 	local originalAddRes
119: 	local targetCharId = inventory:getData("char")
120: 
121: 	if ((x == 0 && y == 0 && inventory:findFreePosition(item) == nil) ||
122: 		(vendorSellItem && inventory:findFreePosition(item) == nil))
123: 	then
124: 		return true
125: 	end
126: 
127: 	return oldInventory:removeItem(itemID, true)
128: 		:next(function()
vendorSellItem
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

### E-0072 — `vendor_metadata_cleanup`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `207-219`
- Pattern: `item:setData("vendorSPrice", nil`

```lua
207: 
208: 				if (inventory && inventory.trashcan)
209: 				then
210: 					inventory.storage:SetBodyGroups("011000000")
211: 				end
212: 
213: 				if (vendorSellItem)
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
vendorSellItem
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

### E-0110 — `item_metadata_network_receive`

- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `12-24`
- Pattern: `netstream.Hook("invData")`

```lua
12: 
13: netstream.Hook("invData", function(id, key, value)
14: 	local item = nut.item.instances[id]
15: 
16: 	if (item) then
17: 		item.data = item.data or {}
18: 		local oldValue = item.data[key]
19: 		item.data[key] = value
20: 		hook.Run("ItemDataChanged", item, key, oldValue, value)
21: 	end
22: end)
23: 
24: netstream.Hook("invQuantity", function(id, quantity)
item.data[key]
```

### E-0112 — `item_metadata_client_event`

- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `12-24`
- Pattern: `hook.Run("ItemDataChanged")`

```lua
12: 
13: netstream.Hook("invData", function(id, key, value)
14: 	local item = nut.item.instances[id]
15: 
16: 	if (item) then
17: 		item.data = item.data or {}
18: 		local oldValue = item.data[key]
19: 		item.data[key] = value
20: 		hook.Run("ItemDataChanged", item, key, oldValue, value)
21: 	end
22: end)
23: 
24: netstream.Hook("invQuantity", function(id, quantity)
item.data[key]
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

### E-0068 — `vendor_purchase_detection`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `161-173`
- Pattern: `vendorSellItem`

```lua
161: 		:next(function(res)
162: 			if ((!res || !res.error) && !tryCombineWith)
163: 			then
164: 				return
165: 			end
166: 
167: 			if (vendorSellItem && res && res.error)
168: 			then
169: 				return inventory:add(item)
170: 			end
171: 
172: 			if (tryCombineWith)
173: 			then
vendorSellItem
```

### E-0082 — `vendor_purchase_detection`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `163-175`
- Pattern: `vendorSellItem`

```lua
163: 			then
164: 				return
165: 			end
166: 
167: 			if (vendorSellItem && res && res.error)
168: 			then
169: 				return inventory:add(item)
170: 			end
171: 
172: 			if (tryCombineWith)
173: 			then
174: 				inventory:removeItem(itemID, true)
175: 			end
inventory:add
```

### E-0070 — `vendor_purchase_detection`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `207-219`
- Pattern: `vendorSellItem`

```lua
207: 
208: 				if (inventory && inventory.trashcan)
209: 				then
210: 					inventory.storage:SetBodyGroups("011000000")
211: 				end
212: 
213: 				if (vendorSellItem)
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
vendorSellItem
```

### E-0090 — `vendor_purchase_detection`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `212-224`
- Pattern: `vendorSellItem`

```lua
212: 
213: 				if (vendorSellItem)
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
item:setData("vendorQty", nil
```

### E-0086 — `vendor_purchase_detection`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `213-225`
- Pattern: `vendorSellItem`

```lua
213: 				if (vendorSellItem)
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
225: 				end
item:setData("vendorSPrice", nil
```

### E-0061 — `vendor_purchase_detection`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `72-84`
- Pattern: `vendorSellItem`

```lua
72: 			client:notify("У торговца недостаточно денег")
73: 		end
74: 
75: 		return true
76: 	end
77: 
78: 	local vendorSellItem = false
79: 	if (oldInventory && IsValid(oldInventory.vendor) && inventory == client:getChar():getInv())
80: 	then
81: 		local char = client:getChar()
82: 		price = tonumber(oldInventory.vendor:GetItemPrice(item.uniqueID, true, client)) * qty
83: 		if (char:hasMoney(price))
84: 		then
vendorSellItem
```

### E-0063 — `vendor_purchase_detection`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `79-91`
- Pattern: `vendorSellItem`

```lua
79: 	if (oldInventory && IsValid(oldInventory.vendor) && inventory == client:getChar():getInv())
80: 	then
81: 		local char = client:getChar()
82: 		price = tonumber(oldInventory.vendor:GetItemPrice(item.uniqueID, true, client)) * qty
83: 		if (char:hasMoney(price))
84: 		then
85: 			vendorSellItem = true
86: 		else
87: 			client:notify("У вас не хватает рацион-марок")
88: 			return true
89: 		end
90: 	end
91: 
vendorSellItem
```

### E-0076 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `10-22`
- Pattern: `oldInventory + destination inventory`

```lua
10: 	local oldInventory = nut.inventory.instances[item.invID]
11: 	if (not oldInventory or not oldInventory.items[itemID]) then
12: 		return
13: 	end
14: 	
15: 	local vendor = inventory && IsValid(inventory.vendor) || nil
16: 	vendor = oldInventory && IsValid(oldInventory.vendor) || vendor
17: 	-- Make sure the item is permitted to move between the two inventories.
18: 	local status, reason = hook.Run("CanItemBeTransfered", item, oldInventory, inventory, client)
19: 
20: 	if (status == false) then client:notify(reason or "You can't do that right now.") return end
21: 	local context = {
22: 		client = client,
oldInventory
```

### E-0066 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `116-128`
- Pattern: `oldInventory + destination inventory`

```lua
116: 
117: 	local tryCombineWith
118: 	local originalAddRes
119: 	local targetCharId = inventory:getData("char")
120: 
121: 	if ((x == 0 && y == 0 && inventory:findFreePosition(item) == nil) ||
122: 		(vendorSellItem && inventory:findFreePosition(item) == nil))
123: 	then
124: 		return true
125: 	end
126: 
127: 	return oldInventory:removeItem(itemID, true)
128: 		:next(function()
vendorSellItem
```

### E-0077 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `12-24`
- Pattern: `oldInventory + destination inventory`

```lua
12: 		return
13: 	end
14: 	
15: 	local vendor = inventory && IsValid(inventory.vendor) || nil
16: 	vendor = oldInventory && IsValid(oldInventory.vendor) || vendor
17: 	-- Make sure the item is permitted to move between the two inventories.
18: 	local status, reason = hook.Run("CanItemBeTransfered", item, oldInventory, inventory, client)
19: 
20: 	if (status == false) then client:notify(reason or "You can't do that right now.") return end
21: 	local context = {
22: 		client = client,
23: 		item = item,
24: 		from = oldInventory,
oldInventory
```

### E-0080 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `145-157`
- Pattern: `oldInventory + destination inventory`

```lua
145: 
146: 			local res = nil
147: 			if (x == 0 && y == 0)
148: 			then
149: 				res = inventory:add(item)
150: 			else
151: 				res = inventory:add(item, x, y)
152: 			end
153: 
154: 			if (res && !res.error && item.transfered)
155: 			then
156: 				item:transfered(client, oldInventory, inventory)
157: 			end
inventory:add
```

### E-0078 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `18-30`
- Pattern: `oldInventory + destination inventory`

```lua
18: 	local status, reason = hook.Run("CanItemBeTransfered", item, oldInventory, inventory, client)
19: 
20: 	if (status == false) then client:notify(reason or "You can't do that right now.") return end
21: 	local context = {
22: 		client = client,
23: 		item = item,
24: 		from = oldInventory,
25: 		to = inventory,
26: 		vendor = vendor
27: 	}
28: 
29: 	local canTransfer, reason = oldInventory:canAccess(TRANSFER, context)
30: 	if (not canTransfer) then
oldInventory
```

### E-0084 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `182-194`
- Pattern: `oldInventory + destination inventory`

```lua
182: 				if (conflictingItem) then
183: 					tryCombineWith = conflictingItem
184: 				end
185: 			end
186: 
187: 			originalAddRes = res
188: 			return oldInventory:add(item, oldX, oldY)
189: 		end)
190: 		:next(function(res)
191: 			if (res and res.error) then return res end
192: 			if (tryCombineWith && IsValid(client) && (targetCharId == client:getChar():getID() || !targetCharId))
193: 			then
194: 				if (hook.Run("ItemCombine", client, item, tryCombineWith))
inventory:add
```

### E-0071 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `207-219`
- Pattern: `oldInventory + destination inventory`

```lua
207: 
208: 				if (inventory && inventory.trashcan)
209: 				then
210: 					inventory.storage:SetBodyGroups("011000000")
211: 				end
212: 
213: 				if (vendorSellItem)
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
vendorSellItem
```

### E-0091 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `212-224`
- Pattern: `oldInventory + destination inventory`

```lua
212: 
213: 				if (vendorSellItem)
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
item:setData("vendorQty", nil
```

### E-0087 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `213-225`
- Pattern: `oldInventory + destination inventory`

```lua
213: 				if (vendorSellItem)
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
225: 				end
item:setData("vendorSPrice", nil
```

### E-0094 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `214-226`
- Pattern: `oldInventory + destination inventory`

```lua
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
225: 				end
226: 			end
item:setData("vendorMQty", nil
```

### E-0097 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `217-229`
- Pattern: `oldInventory + destination inventory`

```lua
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
225: 				end
226: 			end
227: 			return originalAddRes
228: 		end)
229: 		:catch(fail)
item:setData("vendorBPrice"
```

### E-0074 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `4-16`
- Pattern: `oldInventory + destination inventory`

```lua
4: 
5: function PLUGIN:HandleItemTransferRequest(client, itemID, x, y, invID, laltPressed)
6: 	-- Get the item that should be moved, its inventory, and the destination.
7: 	local inventory = nut.inventory.instances[invID]
8: 	local item = nut.item.instances[itemID]
9: 	if (not item) then return end
10: 	local oldInventory = nut.inventory.instances[item.invID]
11: 	if (not oldInventory or not oldInventory.items[itemID]) then
12: 		return
13: 	end
14: 	
15: 	local vendor = inventory && IsValid(inventory.vendor) || nil
16: 	vendor = oldInventory && IsValid(oldInventory.vendor) || vendor
oldInventory
```

### E-0075 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `5-17`
- Pattern: `oldInventory + destination inventory`

```lua
5: function PLUGIN:HandleItemTransferRequest(client, itemID, x, y, invID, laltPressed)
6: 	-- Get the item that should be moved, its inventory, and the destination.
7: 	local inventory = nut.inventory.instances[invID]
8: 	local item = nut.item.instances[itemID]
9: 	if (not item) then return end
10: 	local oldInventory = nut.inventory.instances[item.invID]
11: 	if (not oldInventory or not oldInventory.items[itemID]) then
12: 		return
13: 	end
14: 	
15: 	local vendor = inventory && IsValid(inventory.vendor) || nil
16: 	vendor = oldInventory && IsValid(oldInventory.vendor) || vendor
17: 	-- Make sure the item is permitted to move between the two inventories.
oldInventory
```

### E-0062 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `72-84`
- Pattern: `oldInventory + destination inventory`

```lua
72: 			client:notify("У торговца недостаточно денег")
73: 		end
74: 
75: 		return true
76: 	end
77: 
78: 	local vendorSellItem = false
79: 	if (oldInventory && IsValid(oldInventory.vendor) && inventory == client:getChar():getInv())
80: 	then
81: 		local char = client:getChar()
82: 		price = tonumber(oldInventory.vendor:GetItemPrice(item.uniqueID, true, client)) * qty
83: 		if (char:hasMoney(price))
84: 		then
vendorSellItem
```

### E-0064 — `inventory_boundary_transfer`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `79-91`
- Pattern: `oldInventory + destination inventory`

```lua
79: 	if (oldInventory && IsValid(oldInventory.vendor) && inventory == client:getChar():getInv())
80: 	then
81: 		local char = client:getChar()
82: 		price = tonumber(oldInventory.vendor:GetItemPrice(item.uniqueID, true, client)) * qty
83: 		if (char:hasMoney(price))
84: 		then
85: 			vendorSellItem = true
86: 		else
87: 			client:notify("У вас не хватает рацион-марок")
88: 			return true
89: 		end
90: 	end
91: 
vendorSellItem
```

### E-0079 — `inventory_membership_mutation`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `143-155`
- Pattern: `remove/add item transfer`

```lua
143: 				
144: 			end
145: 
146: 			local res = nil
147: 			if (x == 0 && y == 0)
148: 			then
149: 				res = inventory:add(item)
150: 			else
151: 				res = inventory:add(item, x, y)
152: 			end
153: 
154: 			if (res && !res.error && item.transfered)
155: 			then
inventory:add
```

### E-0081 — `inventory_membership_mutation`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `145-157`
- Pattern: `remove/add item transfer`

```lua
145: 
146: 			local res = nil
147: 			if (x == 0 && y == 0)
148: 			then
149: 				res = inventory:add(item)
150: 			else
151: 				res = inventory:add(item, x, y)
152: 			end
153: 
154: 			if (res && !res.error && item.transfered)
155: 			then
156: 				item:transfered(client, oldInventory, inventory)
157: 			end
inventory:add
```

### E-0069 — `inventory_membership_mutation`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `161-173`
- Pattern: `remove/add item transfer`

```lua
161: 		:next(function(res)
162: 			if ((!res || !res.error) && !tryCombineWith)
163: 			then
164: 				return
165: 			end
166: 
167: 			if (vendorSellItem && res && res.error)
168: 			then
169: 				return inventory:add(item)
170: 			end
171: 
172: 			if (tryCombineWith)
173: 			then
vendorSellItem
```

### E-0083 — `inventory_membership_mutation`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `163-175`
- Pattern: `remove/add item transfer`

```lua
163: 			then
164: 				return
165: 			end
166: 
167: 			if (vendorSellItem && res && res.error)
168: 			then
169: 				return inventory:add(item)
170: 			end
171: 
172: 			if (tryCombineWith)
173: 			then
174: 				inventory:removeItem(itemID, true)
175: 			end
inventory:add
```

### E-0085 — `inventory_membership_mutation`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `182-194`
- Pattern: `remove/add item transfer`

```lua
182: 				if (conflictingItem) then
183: 					tryCombineWith = conflictingItem
184: 				end
185: 			end
186: 
187: 			originalAddRes = res
188: 			return oldInventory:add(item, oldX, oldY)
189: 		end)
190: 		:next(function(res)
191: 			if (res and res.error) then return res end
192: 			if (tryCombineWith && IsValid(client) && (targetCharId == client:getChar():getID() || !targetCharId))
193: 			then
194: 				if (hook.Run("ItemCombine", client, item, tryCombineWith))
inventory:add
```

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

### E-0092 — `vendor_metadata_cleanup`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `212-224`
- Pattern: `item:setData("vendorSPrice", nil`

```lua
212: 
213: 				if (vendorSellItem)
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
item:setData("vendorQty", nil
```

### E-0088 — `vendor_metadata_cleanup`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `213-225`
- Pattern: `item:setData("vendorSPrice", nil`

```lua
213: 				if (vendorSellItem)
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
225: 				end
item:setData("vendorSPrice", nil
```

### E-0095 — `vendor_metadata_cleanup`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `214-226`
- Pattern: `item:setData("vendorSPrice", nil`

```lua
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
225: 				end
226: 			end
item:setData("vendorMQty", nil
```

### E-0098 — `vendor_metadata_cleanup`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `217-229`
- Pattern: `item:setData("vendorSPrice", nil`

```lua
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
225: 				end
226: 			end
227: 			return originalAddRes
228: 		end)
229: 		:catch(fail)
item:setData("vendorBPrice"
```

### E-0073 — `vendor_metadata_cleanup`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `207-219`
- Pattern: `vendor metadata setData cleanup/update`

```lua
207: 
208: 				if (inventory && inventory.trashcan)
209: 				then
210: 					inventory.storage:SetBodyGroups("011000000")
211: 				end
212: 
213: 				if (vendorSellItem)
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
vendorSellItem
```

### E-0093 — `vendor_metadata_cleanup`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `212-224`
- Pattern: `vendor metadata setData cleanup/update`

```lua
212: 
213: 				if (vendorSellItem)
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
item:setData("vendorQty", nil
```

### E-0089 — `vendor_metadata_cleanup`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `213-225`
- Pattern: `vendor metadata setData cleanup/update`

```lua
213: 				if (vendorSellItem)
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
225: 				end
item:setData("vendorSPrice", nil
```

### E-0096 — `vendor_metadata_cleanup`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `214-226`
- Pattern: `vendor metadata setData cleanup/update`

```lua
214: 				then
215: 					client:getChar():takeMoney(price)
216: 					oldInventory.vendor:HandleMoney(price, client)
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
225: 				end
226: 			end
item:setData("vendorMQty", nil
```

### E-0099 — `vendor_metadata_cleanup`

- File: `plugins/gridinv/sv_transfer.lua`
- Role: `gridinv_transfer`
- Lines: `217-229`
- Pattern: `vendor metadata setData cleanup/update`

```lua
217: 					oldInventory.vendor:HandleStock(item.uniqueID, true, qty, item.isStackable, client)
218: 					item:setData("vendorQty", nil, client)
219: 					item:setData("vendorSPrice", nil, client)
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
225: 				end
226: 			end
227: 			return originalAddRes
228: 		end)
229: 		:catch(fail)
item:setData("vendorBPrice"
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

### E-0116 — `item_metadata_network_receive`

- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `12-24`
- Pattern: `netstream.Hook("invData")`

```lua
12: 
13: netstream.Hook("invData", function(id, key, value)
14: 	local item = nut.item.instances[id]
15: 
16: 	if (item) then
17: 		item.data = item.data or {}
18: 		local oldValue = item.data[key]
19: 		item.data[key] = value
20: 		hook.Run("ItemDataChanged", item, key, oldValue, value)
21: 	end
22: end)
23: 
24: netstream.Hook("invQuantity", function(id, quantity)
oldValue
```

### E-0113 — `item_metadata_network_receive`

- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `13-25`
- Pattern: `netstream.Hook("invData")`

```lua
13: netstream.Hook("invData", function(id, key, value)
14: 	local item = nut.item.instances[id]
15: 
16: 	if (item) then
17: 		item.data = item.data or {}
18: 		local oldValue = item.data[key]
19: 		item.data[key] = value
20: 		hook.Run("ItemDataChanged", item, key, oldValue, value)
21: 	end
22: end)
23: 
24: netstream.Hook("invQuantity", function(id, quantity)
25: 	local item = nut.item.instances[id]
item.data[key]
```

### E-0101 — `item_metadata_network_receive`

- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `7-19`
- Pattern: `netstream.Hook("invData")`

```lua
7: 	end
8: 
9: 	item.invID = invID or 0
10: 	hook.Run("ItemInitialized", item)
11: end)
12: 
13: netstream.Hook("invData", function(id, key, value)
14: 	local item = nut.item.instances[id]
15: 
16: 	if (item) then
17: 		item.data = item.data or {}
18: 		local oldValue = item.data[key]
19: 		item.data[key] = value
netstream.Hook("invData"
```

### E-0105 — `item_metadata_network_receive`

- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `8-20`
- Pattern: `netstream.Hook("invData")`

```lua
8: 
9: 	item.invID = invID or 0
10: 	hook.Run("ItemInitialized", item)
11: end)
12: 
13: netstream.Hook("invData", function(id, key, value)
14: 	local item = nut.item.instances[id]
15: 
16: 	if (item) then
17: 		item.data = item.data or {}
18: 		local oldValue = item.data[key]
19: 		item.data[key] = value
20: 		hook.Run("ItemDataChanged", item, key, oldValue, value)
nut.item.instances
```

### E-0111 — `item_metadata_network_receive`

- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `12-24`
- Pattern: `client item.data[key] mutation`

```lua
12: 
13: netstream.Hook("invData", function(id, key, value)
14: 	local item = nut.item.instances[id]
15: 
16: 	if (item) then
17: 		item.data = item.data or {}
18: 		local oldValue = item.data[key]
19: 		item.data[key] = value
20: 		hook.Run("ItemDataChanged", item, key, oldValue, value)
21: 	end
22: end)
23: 
24: netstream.Hook("invQuantity", function(id, quantity)
item.data[key]
```

### E-0117 — `item_metadata_network_receive`

- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `12-24`
- Pattern: `client item.data[key] mutation`

```lua
12: 
13: netstream.Hook("invData", function(id, key, value)
14: 	local item = nut.item.instances[id]
15: 
16: 	if (item) then
17: 		item.data = item.data or {}
18: 		local oldValue = item.data[key]
19: 		item.data[key] = value
20: 		hook.Run("ItemDataChanged", item, key, oldValue, value)
21: 	end
22: end)
23: 
24: netstream.Hook("invQuantity", function(id, quantity)
oldValue
```

### E-0114 — `item_metadata_network_receive`

- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `13-25`
- Pattern: `client item.data[key] mutation`

```lua
13: netstream.Hook("invData", function(id, key, value)
14: 	local item = nut.item.instances[id]
15: 
16: 	if (item) then
17: 		item.data = item.data or {}
18: 		local oldValue = item.data[key]
19: 		item.data[key] = value
20: 		hook.Run("ItemDataChanged", item, key, oldValue, value)
21: 	end
22: end)
23: 
24: netstream.Hook("invQuantity", function(id, quantity)
25: 	local item = nut.item.instances[id]
item.data[key]
```

### E-0103 — `item_metadata_network_receive`

- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `14-26`
- Pattern: `client item.data[key] mutation`

```lua
14: 	local item = nut.item.instances[id]
15: 
16: 	if (item) then
17: 		item.data = item.data or {}
18: 		local oldValue = item.data[key]
19: 		item.data[key] = value
20: 		hook.Run("ItemDataChanged", item, key, oldValue, value)
21: 	end
22: end)
23: 
24: netstream.Hook("invQuantity", function(id, quantity)
25: 	local item = nut.item.instances[id]
26: 
hook.Run("ItemDataChanged"
```
