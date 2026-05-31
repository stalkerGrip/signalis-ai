# SIGNALIS AI — Runtime Chain Evidence

- Source validation: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_targeted_validation_patched_source_validation.json`
- Raw evidence total: `123`
- Deduped evidence total: `102`
- Duplicates removed: `21`

## Summary

```json
{
  "raw_evidence_total": 123,
  "deduped_evidence_total": 102,
  "duplicates_removed": 21,
  "chain_confidence": "validated",
  "chain_score": 1904,
  "chain_steps_present": 15,
  "chain_steps_missing": 0,
  "by_class": {
    "gridinv_item_ui_refresh": 5,
    "gridinv_panel_repopulate": 7,
    "inventory_boundary_transfer": 17,
    "inventory_level_data_not_item_data": 2,
    "inventory_membership_client_event": 5,
    "inventory_membership_mutation": 8,
    "inventory_membership_network_send": 5,
    "inventory_membership_receive_add": 1,
    "inventory_recipients_resolved": 6,
    "item_full_state_sync": 4,
    "item_metadata_client_event": 7,
    "item_metadata_mutation": 2,
    "item_metadata_network_receive": 8,
    "item_metadata_network_sync_send": 7,
    "item_metadata_persistence": 5,
    "vendor_metadata_cleanup": 5,
    "vendor_purchase_detection": 8
  },
  "by_file": {
    "plugins/gridinv/sv_transfer.lua": 36,
    "gamemode/core/meta/inventory/sv_base_inventory.lua": 17,
    "plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua": 15,
    "gamemode/core/libs/item/cl_networking.lua": 15,
    "gamemode/core/meta/item/sv_item.lua": 14,
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
- Score: `1904`

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

Ranked Chain Evidence:

### E-0001 — `vendor_purchase_detection`

- Rank: `1`
- Score: `145`
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

### E-0009 — `inventory_boundary_transfer`

- Rank: `9`
- Score: `134`
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

### E-0026 — `inventory_membership_mutation`

- Rank: `26`
- Score: `113`
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

### E-0034 — `inventory_recipients_resolved`

- Rank: `34`
- Score: `104`
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

### E-0040 — `item_full_state_sync`

- Rank: `40`
- Score: `118`
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

### E-0044 — `inventory_membership_network_send`

- Rank: `44`
- Score: `120`
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

### E-0049 — `inventory_membership_receive_add`

- Rank: `49`
- Score: `120`
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

### E-0050 — `inventory_membership_client_event`

- Rank: `50`
- Score: `115`
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

### E-0055 — `vendor_metadata_cleanup`

- Rank: `55`
- Score: `150`
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

### E-0060 — `item_metadata_mutation`

- Rank: `60`
- Score: `130`
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

### E-0062 — `item_metadata_network_sync_send`

- Rank: `62`
- Score: `130`
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

### E-0069 — `item_metadata_network_receive`

- Rank: `69`
- Score: `140`
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

### E-0077 — `item_metadata_client_event`

- Rank: `77`
- Score: `140`
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

### E-0084 — `gridinv_item_ui_refresh`

- Rank: `84`
- Score: `125`
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

### E-0089 — `gridinv_panel_repopulate`

- Rank: `89`
- Score: `120`
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

## Additional Deduped Classified Evidence

### E-0002 — `vendor_purchase_detection`

- Rank: `2`
- Score: `145`
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

### E-0003 — `vendor_purchase_detection`

- Rank: `3`
- Score: `145`
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

### E-0004 — `vendor_purchase_detection`

- Rank: `4`
- Score: `145`
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

### E-0005 — `vendor_purchase_detection`

- Rank: `5`
- Score: `145`
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

### E-0006 — `vendor_purchase_detection`

- Rank: `6`
- Score: `145`
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

### E-0007 — `vendor_purchase_detection`

- Rank: `7`
- Score: `145`
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

### E-0008 — `vendor_purchase_detection`

- Rank: `8`
- Score: `145`
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

### E-0010 — `inventory_boundary_transfer`

- Rank: `10`
- Score: `134`
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

### E-0011 — `inventory_boundary_transfer`

- Rank: `11`
- Score: `134`
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

### E-0012 — `inventory_boundary_transfer`

- Rank: `12`
- Score: `134`
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

### E-0013 — `inventory_boundary_transfer`

- Rank: `13`
- Score: `134`
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
CanItemBeTransfered
```

### E-0014 — `inventory_boundary_transfer`

- Rank: `14`
- Score: `134`
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

### E-0015 — `inventory_boundary_transfer`

- Rank: `15`
- Score: `134`
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

### E-0016 — `inventory_boundary_transfer`

- Rank: `16`
- Score: `134`
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

### E-0017 — `inventory_boundary_transfer`

- Rank: `17`
- Score: `134`
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

### E-0018 — `inventory_boundary_transfer`

- Rank: `18`
- Score: `134`
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

### E-0019 — `inventory_boundary_transfer`

- Rank: `19`
- Score: `134`
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

### E-0020 — `inventory_boundary_transfer`

- Rank: `20`
- Score: `134`
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

### E-0021 — `inventory_boundary_transfer`

- Rank: `21`
- Score: `134`
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

### E-0022 — `inventory_boundary_transfer`

- Rank: `22`
- Score: `134`
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

### E-0023 — `inventory_boundary_transfer`

- Rank: `23`
- Score: `134`
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

### E-0024 — `inventory_boundary_transfer`

- Rank: `24`
- Score: `134`
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

### E-0025 — `inventory_boundary_transfer`

- Rank: `25`
- Score: `134`
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

### E-0027 — `inventory_membership_mutation`

- Rank: `27`
- Score: `113`
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

### E-0028 — `inventory_membership_mutation`

- Rank: `28`
- Score: `113`
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

### E-0029 — `inventory_membership_mutation`

- Rank: `29`
- Score: `113`
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

### E-0030 — `inventory_membership_mutation`

- Rank: `30`
- Score: `113`
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

### E-0031 — `inventory_membership_mutation`

- Rank: `31`
- Score: `113`
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

### E-0032 — `inventory_membership_mutation`

- Rank: `32`
- Score: `109`
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

### E-0033 — `inventory_membership_mutation`

- Rank: `33`
- Score: `109`
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

### E-0035 — `inventory_recipients_resolved`

- Rank: `35`
- Score: `104`
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

### E-0036 — `inventory_recipients_resolved`

- Rank: `36`
- Score: `104`
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

### E-0037 — `inventory_recipients_resolved`

- Rank: `37`
- Score: `104`
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

### E-0038 — `inventory_recipients_resolved`

- Rank: `38`
- Score: `104`
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

### E-0039 — `inventory_recipients_resolved`

- Rank: `39`
- Score: `104`
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

### E-0041 — `item_full_state_sync`

- Rank: `41`
- Score: `118`
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

### E-0042 — `item_full_state_sync`

- Rank: `42`
- Score: `118`
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

### E-0043 — `item_full_state_sync`

- Rank: `43`
- Score: `118`
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

### E-0045 — `inventory_membership_network_send`

- Rank: `45`
- Score: `120`
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

### E-0046 — `inventory_membership_network_send`

- Rank: `46`
- Score: `118`
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

### E-0047 — `inventory_membership_network_send`

- Rank: `47`
- Score: `118`
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

### E-0048 — `inventory_membership_network_send`

- Rank: `48`
- Score: `118`
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

### E-0051 — `inventory_membership_client_event`

- Rank: `51`
- Score: `115`
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

### E-0052 — `inventory_membership_client_event`

- Rank: `52`
- Score: `97`
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

### E-0053 — `inventory_membership_client_event`

- Rank: `53`
- Score: `97`
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

### E-0054 — `inventory_membership_client_event`

- Rank: `54`
- Score: `97`
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

### E-0056 — `vendor_metadata_cleanup`

- Rank: `56`
- Score: `150`
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

### E-0057 — `vendor_metadata_cleanup`

- Rank: `57`
- Score: `150`
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

### E-0058 — `vendor_metadata_cleanup`

- Rank: `58`
- Score: `150`
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

### E-0059 — `vendor_metadata_cleanup`

- Rank: `59`
- Score: `150`
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

### E-0061 — `item_metadata_mutation`

- Rank: `61`
- Score: `130`
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

### E-0063 — `item_metadata_network_sync_send`

- Rank: `63`
- Score: `130`
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

### E-0064 — `item_metadata_network_sync_send`

- Rank: `64`
- Score: `130`
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

### E-0065 — `item_metadata_network_sync_send`

- Rank: `65`
- Score: `130`
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

### E-0066 — `item_metadata_network_sync_send`

- Rank: `66`
- Score: `124`
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

### E-0067 — `item_metadata_network_sync_send`

- Rank: `67`
- Score: `124`
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

### E-0068 — `item_metadata_network_sync_send`

- Rank: `68`
- Score: `124`
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

### E-0070 — `item_metadata_network_receive`

- Rank: `70`
- Score: `140`
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

### E-0071 — `item_metadata_network_receive`

- Rank: `71`
- Score: `140`
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

### E-0072 — `item_metadata_network_receive`

- Rank: `72`
- Score: `140`
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

### E-0073 — `item_metadata_network_receive`

- Rank: `73`
- Score: `140`
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

### E-0074 — `item_metadata_network_receive`

- Rank: `74`
- Score: `130`
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

### E-0075 — `item_metadata_network_receive`

- Rank: `75`
- Score: `130`
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
oldValue
```

### E-0076 — `item_metadata_network_receive`

- Rank: `76`
- Score: `130`
- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `19-31`
- Pattern: `client item.data[key] mutation`

```lua
19: 		item.data[key] = value
20: 		hook.Run("ItemDataChanged", item, key, oldValue, value)
21: 	end
22: end)
23: 
24: netstream.Hook("invQuantity", function(id, quantity)
25: 	local item = nut.item.instances[id]
26: 
27: 	if (item) then
28: 		local oldValue = item:getQuantity()
29: 		item.quantity = quantity
30: 
31: 		hook.Run("ItemQuantityChanged", item, oldValue, quantity)
nut.item.instances
```

### E-0078 — `item_metadata_client_event`

- Rank: `78`
- Score: `140`
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
oldValue
```

### E-0079 — `item_metadata_client_event`

- Rank: `79`
- Score: `140`
- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `13-25`
- Pattern: `hook.Run("ItemDataChanged")`

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

### E-0080 — `item_metadata_client_event`

- Rank: `80`
- Score: `140`
- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `14-26`
- Pattern: `hook.Run("ItemDataChanged")`

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

### E-0081 — `item_metadata_client_event`

- Rank: `81`
- Score: `140`
- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `14-26`
- Pattern: `hook.Run("ItemDataChanged")`

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
oldValue
```

### E-0082 — `item_metadata_client_event`

- Rank: `82`
- Score: `140`
- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `19-31`
- Pattern: `hook.Run("ItemDataChanged")`

```lua
19: 		item.data[key] = value
20: 		hook.Run("ItemDataChanged", item, key, oldValue, value)
21: 	end
22: end)
23: 
24: netstream.Hook("invQuantity", function(id, quantity)
25: 	local item = nut.item.instances[id]
26: 
27: 	if (item) then
28: 		local oldValue = item:getQuantity()
29: 		item.quantity = quantity
30: 
31: 		hook.Run("ItemQuantityChanged", item, oldValue, quantity)
nut.item.instances
```

### E-0083 — `item_metadata_client_event`

- Rank: `83`
- Score: `140`
- File: `gamemode/core/libs/item/cl_networking.lua`
- Role: `client_item_networking`
- Lines: `8-20`
- Pattern: `hook.Run("ItemDataChanged")`

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

### E-0085 — `gridinv_item_ui_refresh`

- Rank: `85`
- Score: `125`
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

### E-0086 — `gridinv_item_ui_refresh`

- Rank: `86`
- Score: `125`
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

### E-0087 — `gridinv_item_ui_refresh`

- Rank: `87`
- Score: `125`
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
function PANEL:InventoryItemDataChanged
```

### E-0088 — `gridinv_item_ui_refresh`

- Rank: `88`
- Score: `125`
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

### E-0090 — `gridinv_panel_repopulate`

- Rank: `90`
- Score: `120`
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

### E-0091 — `gridinv_panel_repopulate`

- Rank: `91`
- Score: `120`
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

### E-0092 — `gridinv_panel_repopulate`

- Rank: `92`
- Score: `120`
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

### E-0093 — `gridinv_panel_repopulate`

- Rank: `93`
- Score: `120`
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
function PANEL:InventoryItemDataChanged
```

### E-0094 — `gridinv_panel_repopulate`

- Rank: `94`
- Score: `120`
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

### E-0095 — `gridinv_panel_repopulate`

- Rank: `95`
- Score: `120`
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
