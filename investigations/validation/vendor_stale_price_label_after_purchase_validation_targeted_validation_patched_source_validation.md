# SIGNALIS AI — Targeted Source Validation

- Targeted plan: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_targeted_validation_patched.json`
- Query: `vendor stale price label after purchase`
- Pattern results: `238`
- Found: `188`
- Missing: `50`
- Requested files: `11`
- Resolved files: `11`
- Duplicate fragments: `66`
- Causal fragments: `132`
- Resolution rate: `1.0`
- Pattern hit rate: `0.79`
- Causal hit rate: `0.702`

## TV-001 — `gamemode/core/meta/inventory/cl_base_inventory.lua`

- Priority: `high`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Expected runtime relation: client inventory membership/data receiver boundary
- Resolution: `direct_root_join`
- Found: `6`
- Missing: `4`

### Missing Patterns

- `"invData"`
- `InventoryItemDataChanged`
- `item:setData("vendorSPrice", nil`
- `self:populateItems()`

### Found Evidence

#### 1. `hook.Run("InventoryDataChanged"` lines `11-23`

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
```

#### 2. `hook.Run("InventoryItemAdded"` lines `57-69`

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
```

#### 3. `hook.Run("InventoryItemRemoved"` lines `69-81`

```lua
69: 	local invID = net.ReadType()
70: 	local item = nut.item.instances[itemID]
71: 	local inventory = nut.inventory.instances[invID]
72: 	if (item and inventory and inventory.items[itemID]) then
73: 		inventory.items[itemID] = nil
74: 		item.invID = 0
75: 		hook.Run("InventoryItemRemoved", inventory, item)
76: 	end
77: end)
78: 
79: net.Receive("nutInventoryDelete", function()
80: 	local invID = net.ReadType()
81: 	local instance = nut.inventory.instances[invID]
```

#### 4. `net.Receive("nutInventoryAdd"` lines `50-62`

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
```

#### 5. `net.Receive("nutInventoryData"` lines `1-9`

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
```

#### 6. `net.Receive("nutInventoryRemove"` lines `61-73`

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
```

## TV-002 — `plugins/vendor/derma/cl_vendor.lua`

- Priority: `high`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Expected runtime relation: vendor trade UI price hooks and trade/exit messages
- Resolution: `direct_root_join`
- Found: `9`
- Missing: `4`

### Missing Patterns

- `"invData"`
- `InventoryItemDataChanged`
- `item:setData("vendorSPrice", nil`
- `self:populateItems()`

### Found Evidence

#### 1. `function PANEL:onVendorPriceUpdated` lines `167-179`

```lua
167: end
168: 
169: function PANEL:onVendorMoneyUpdated(vendor, money)
170: 	self.vendor:setMoney(money)
171: end
172: 
173: function PANEL:onVendorPriceUpdated(vendor, itemType, value)
174: 	local panel = self.items[self.vendor][itemType]
175: 	if (IsValid(panel)) then panel:updatePrice() end
176: 
177: 	panel = self.items[self.me][itemType]
178: 	if (IsValid(panel)) then panel:updatePrice() end
179: end
```

#### 2. `hook.Add("VendorItemPriceUpdated"` lines `198-210`

```lua
198: function PANEL:listenForChanges()
199: 	-- Money changes.
200: 	hook.Add("VendorMoneyUpdated", self, self.onVendorMoneyUpdated)
201: 	hook.Add("OnCharVarChanged", self, self.onCharVarChanged)
202: 
203: 	-- Price change.
204: 	hook.Add("VendorItemPriceUpdated", self, self.onVendorPriceUpdated)
205: 
206: 	-- Item stock changes.
207: 	hook.Add("VendorItemStockUpdated", self, self.onItemStockUpdated)
208: 	hook.Add("VendorItemMaxStockUpdated", self, self.onItemStockUpdated)
209: 
210: 	-- Item mode change.
```

#### 3. `net.Start("nutVendorExit")` lines `229-241`

```lua
229: 	surface.SetDrawColor(0, 0, 0, 100)
230: 	surface.DrawRect(0, 0, w, h)
231: end
232: 
233: function PANEL:OnRemove()
234: 	if (not self.noSendExit) then
235: 		net.Start("nutVendorExit")
236: 		net.SendToServer()
237: 		self.noSendExit = true
238: 	end
239: 
240: 	if (IsValid(nut.gui.vendorEditor)) then
241: 		nut.gui.vendorEditor:Remove()
```

#### 4. `net.Start("nutVendorTrade")` lines `75-87`

```lua
75: 	}
76: 
77: 	self:initializeItems()
78: end
79: 
80: function PANEL:buyItemFromVendor(itemType)
81: 	net.Start("nutVendorTrade")
82: 		net.WriteString(itemType)
83: 		net.WriteBool(false)
84: 	net.SendToServer()
85: end
86: 
87: function PANEL:sellItemToVendor(itemType)
```

#### 5. `net.Start("nutVendorTrade")` lines `82-94`

```lua
82: 		net.WriteString(itemType)
83: 		net.WriteBool(false)
84: 	net.SendToServer()
85: end
86: 
87: function PANEL:sellItemToVendor(itemType)
88: 	net.Start("nutVendorTrade")
89: 		net.WriteString(itemType)
90: 		net.WriteBool(true)
91: 	net.SendToServer()
92: end
93: 
94: function PANEL:initializeItems()
```

#### 6. `panel:updatePrice()` lines `154-166`

```lua
154: function PANEL:onVendorPropEdited(vendor, key)
155: 	if (key == "name") then
156: 		self.vendor:setName(vendor:getName())
157: 	elseif (key == "scale") then
158: 		for _, panel in pairs(self.items[self.vendor]) do
159: 			if (not IsValid(panel)) then continue end
160: 			panel:updatePrice()
161: 		end
162: 		for _, panel in pairs(self.items[self.me]) do
163: 			if (not IsValid(panel)) then continue end
164: 			panel:updatePrice()
165: 		end
166: 	end
```

#### 7. `panel:updatePrice()` lines `158-170`

```lua
158: 		for _, panel in pairs(self.items[self.vendor]) do
159: 			if (not IsValid(panel)) then continue end
160: 			panel:updatePrice()
161: 		end
162: 		for _, panel in pairs(self.items[self.me]) do
163: 			if (not IsValid(panel)) then continue end
164: 			panel:updatePrice()
165: 		end
166: 	end
167: end
168: 
169: function PANEL:onVendorMoneyUpdated(vendor, money)
170: 	self.vendor:setMoney(money)
```

#### 8. `panel:updatePrice()` lines `169-181`

```lua
169: function PANEL:onVendorMoneyUpdated(vendor, money)
170: 	self.vendor:setMoney(money)
171: end
172: 
173: function PANEL:onVendorPriceUpdated(vendor, itemType, value)
174: 	local panel = self.items[self.vendor][itemType]
175: 	if (IsValid(panel)) then panel:updatePrice() end
176: 
177: 	panel = self.items[self.me][itemType]
178: 	if (IsValid(panel)) then panel:updatePrice() end
179: end
180: 
181: function PANEL:onVendorModeUpdated(vendor, itemType, mode)
```

#### 9. `panel:updatePrice()` lines `172-184`

```lua
172: 
173: function PANEL:onVendorPriceUpdated(vendor, itemType, value)
174: 	local panel = self.items[self.vendor][itemType]
175: 	if (IsValid(panel)) then panel:updatePrice() end
176: 
177: 	panel = self.items[self.me][itemType]
178: 	if (IsValid(panel)) then panel:updatePrice() end
179: end
180: 
181: function PANEL:onVendorModeUpdated(vendor, itemType, mode)
182: 	self:updateItem(itemType, self.vendor)
183: 	self:updateItem(itemType, self.me)
184: end
```

## TV-003 — `plugins/inventory/cl_hooks.lua`

- Priority: `high`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Expected runtime relation: client inventory/vendor interface construction and close cleanup boundary
- Resolution: `direct_root_join`
- Found: `14`
- Missing: `4`

### Missing Patterns

- `"invData"`
- `InventoryItemDataChanged`
- `item:setData("vendorSPrice", nil`
- `self:populateItems()`

### Found Evidence

#### 1. `PLUGIN:CreateNewInventoryPanel` lines `85-97`

```lua
85: 
86: 	netstream.Start("inventorySetPanelStatus", true)
87: 
88: 	return panel
89: end
90: 
91: function PLUGIN:CreateNewInventoryPanel(client, parent)
92: 	return showInvPanel(client:getChar():getInv(true), client, parent)
93: end
94: 
95: function PLUGIN:CreateTargetNewInventoryPanel(target, invId, parent)
96: 	return showInvPanel(invId, target, parent)
97: end
```

#### 2. `PLUGIN:CreateNewInventoryPanel` lines `101-113`

```lua
101: 	function()
102: 		if (IsValid(invPanel))
103: 		then
104: 			invPanel:Close()
105: 			invPanel = nil
106: 		else
107: 			invPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
108: 		end
109: 	end)
110: 
111: local currInvPanel
112: netstream.Hook(
113: 	"inventoryOpen", 
```

#### 3. `PLUGIN:CreateNewInventoryPanel` lines `114-126`

```lua
114: 	function()
115: 		if (IsValid(currInvPanel))
116: 		then
117: 			return
118: 		end
119: 
120: 		currInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
121: 	end)
122: 
123: netstream.Hook("vendorTradeInterface", function(vendor, invId)
124: 	local PADDING = 4
125: 	if (!IsValid(vendor)) then return end
126: 
```

#### 4. `PLUGIN:CreateNewInventoryPanel` lines `125-137`

```lua
125: 	if (!IsValid(vendor)) then return end
126: 
127: 	local localInv = LocalPlayer():getChar() && LocalPlayer():getChar():getInv(true)
128: 	local loadedInv = nut.inventory.instances[invId]
129: 	if (!loadedInv) then return end
130: 
131: 	local localInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
132: 	local localParent = localInvPanel:GetParent()
133: 	local storageInvPanel = vgui.Create("vendor_grid_inventory")
134: 	storageInvPanel.vendor = vendor
135: 	storageInvPanel:SetUpPanel(loadedInv)
136: 	nut.gui["vendorTradeInterface" .. vendor:EntIndex()] = storageInvPanel
137: 	storageInvPanel:SetTitle(vendor:GetVendorName())
```

#### 5. `hook.Run("OnCreateStoragePanel"` lines `160-172`

```lua
160: 
161: 		netstream.Start("removeReceiverFromVendor", vendor:EntIndex())
162: 
163: 		netstream.Start("inventorySetPanelStatus", false)
164: 	end
165: 
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
168: 	localInvPanel.MainInvPanel.pair = storageInvPanel.mainInvPanel
169: 	storageInvPanel.mainInvPanel.pair = localInvPanel.MainInvPanel
170: 
171: 	localParent.OnRemove = exitStorageOnRemove
172: 	storageInvPanel.OnRemove = exitStorageOnRemove
```

#### 6. `netstream.Hook("vendorTradeInterface"` lines `117-129`

```lua
117: 			return
118: 		end
119: 
120: 		currInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
121: 	end)
122: 
123: netstream.Hook("vendorTradeInterface", function(vendor, invId)
124: 	local PADDING = 4
125: 	if (!IsValid(vendor)) then return end
126: 
127: 	local localInv = LocalPlayer():getChar() && LocalPlayer():getChar():getInv(true)
128: 	local loadedInv = nut.inventory.instances[invId]
129: 	if (!loadedInv) then return end
```

#### 7. `netstream.Start("inventorySetPanelStatus"` lines `24-36`

```lua
24: 	parentFrame.model.Entity:SetSkin(target:GetSkin())
25: 
26: 	parentFrame.OnKeyCodePressed = function(this, keyCode)
27: 		if (keyCode == KEY_I)
28: 		then
29: 			parentFrame:Close()
30: 			netstream.Start("inventorySetPanelStatus", false)
31: 		end
32: 	end
33: 
34: 	parentFrame.OnClose = function(this)
35: 		netstream.Start("inventorySetPanelStatus", false)
36: 	end
```

#### 8. `netstream.Start("inventorySetPanelStatus"` lines `29-41`

```lua
29: 			parentFrame:Close()
30: 			netstream.Start("inventorySetPanelStatus", false)
31: 		end
32: 	end
33: 
34: 	parentFrame.OnClose = function(this)
35: 		netstream.Start("inventorySetPanelStatus", false)
36: 	end
37: 
38: 	local charScale = {
39: 		["models/krizhpinky/kncr.mdl"] = 0.82,
40: 		["models/voxaid/signalis_star/star_pm.mdl"] = 0.82,
41: 		["models/voxaid/signalis_mynah/mynah_no_armor.mdl"] = 0.82,
```

#### 9. `netstream.Start("inventorySetPanelStatus"` lines `80-92`

```lua
80: 	panel:SetPos(1, 25)
81: 
82: 	netstream.Start("invsRuleSet", target)
83: 
84: 	nut.gui[globalName] = panel
85: 
86: 	netstream.Start("inventorySetPanelStatus", true)
87: 
88: 	return panel
89: end
90: 
91: function PLUGIN:CreateNewInventoryPanel(client, parent)
92: 	return showInvPanel(client:getChar():getInv(true), client, parent)
```

#### 10. `netstream.Start("inventorySetPanelStatus"` lines `157-169`

```lua
157: 				panel == localParent and storageInvPanel or localParent
158: 			if (IsValid(otherPanel)) then otherPanel:Remove() end
159: 		end
160: 
161: 		netstream.Start("removeReceiverFromVendor", vendor:EntIndex())
162: 
163: 		netstream.Start("inventorySetPanelStatus", false)
164: 	end
165: 
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
168: 	localInvPanel.MainInvPanel.pair = storageInvPanel.mainInvPanel
169: 	storageInvPanel.mainInvPanel.pair = localInvPanel.MainInvPanel
```

#### 11. `netstream.Start("inventorySetPanelStatus"` lines `313-321`

```lua
313: netstream.Hook(
314: 	"inventoryCloseOnAction",
315: 	function()
316: 		if (IsValid(invFrame))
317: 		then
318: 			invFrame:Close()
319: 			netstream.Start("inventorySetPanelStatus", false)
320: 		end
321: 	end)
```

#### 12. `netstream.Start("removeReceiverFromVendor"` lines `155-167`

```lua
155: 			nutStorageBase:exitStorage()
156: 			local otherPanel =
157: 				panel == localParent and storageInvPanel or localParent
158: 			if (IsValid(otherPanel)) then otherPanel:Remove() end
159: 		end
160: 
161: 		netstream.Start("removeReceiverFromVendor", vendor:EntIndex())
162: 
163: 		netstream.Start("inventorySetPanelStatus", false)
164: 	end
165: 
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
```

#### 13. `storageInvPanel:SetUpPanel(loadedInv)` lines `129-141`

```lua
129: 	if (!loadedInv) then return end
130: 
131: 	local localInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
132: 	local localParent = localInvPanel:GetParent()
133: 	local storageInvPanel = vgui.Create("vendor_grid_inventory")
134: 	storageInvPanel.vendor = vendor
135: 	storageInvPanel:SetUpPanel(loadedInv)
136: 	nut.gui["vendorTradeInterface" .. vendor:EntIndex()] = storageInvPanel
137: 	storageInvPanel:SetTitle(vendor:GetVendorName())
138: 
139: 	localParent:ShowCloseButton(true)
140: 	storageInvPanel:ShowCloseButton(true)
141: 
```

#### 14. `vgui.Create("vendor_grid_inventory")` lines `127-139`

```lua
127: 	local localInv = LocalPlayer():getChar() && LocalPlayer():getChar():getInv(true)
128: 	local loadedInv = nut.inventory.instances[invId]
129: 	if (!loadedInv) then return end
130: 
131: 	local localInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
132: 	local localParent = localInvPanel:GetParent()
133: 	local storageInvPanel = vgui.Create("vendor_grid_inventory")
134: 	storageInvPanel.vendor = vendor
135: 	storageInvPanel:SetUpPanel(loadedInv)
136: 	nut.gui["vendorTradeInterface" .. vendor:EntIndex()] = storageInvPanel
137: 	storageInvPanel:SetTitle(vendor:GetVendorName())
138: 
139: 	localParent:ShowCloseButton(true)
```

## TV-004 — `plugins/vendor/entities/entities/nut_vendor/init.lua`

- Priority: `high`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Expected runtime relation: server vendor entity creates/clears vendor item presentation metadata
- Resolution: `direct_root_join`
- Found: `10`
- Missing: `4`

### Missing Patterns

- `"invData"`
- `InventoryItemDataChanged`
- `item:setData("vendorSPrice", nil`
- `self:populateItems()`

### Found Evidence

#### 1. `function ENT:RemoveReceiverFromVendor` lines `284-296`

```lua
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

#### 2. `function ENT:VendorItemSetData` lines `209-221`

```lua
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

#### 3. `hook.Run("OpenVendorTradeInterface"` lines `51-63`

```lua
51: 		return false
52: 	end
53: 
54: 	self.receivers[#self.receivers + 1] = activator
55: 	activator.nutVendor = self
56: 
57: 	hook.Run("OpenVendorTradeInterface", activator, self, self.invId)
58: end
59: 
60: function ENT:SetMoneyAmount(value)
61: 	if (!isnumber(value) || value < 0) then return end
62: 	self:SetMoney(value)
63: end
```

#### 4. `item:setData("vendorMQty"` lines `212-224`

```lua
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

#### 5. `item:setData("vendorQty"` lines `210-222`

```lua
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

#### 6. `item:setData("vendorSPrice"` lines `211-223`

```lua
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

#### 7. `v:setData("vendorBPrice", nil` lines `290-302`

```lua
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

#### 8. `v:setData("vendorMQty", nil` lines `293-305`

```lua
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

#### 9. `v:setData("vendorQty", nil` lines `291-303`

```lua
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

#### 10. `v:setData("vendorSPrice", nil` lines `292-304`

```lua
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

## TV-005 — `plugins/vendor/derma/cl_vendor.lua`

- Priority: `medium`
- Hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI
- Expected runtime relation: vendor trade UI price hooks and trade/exit messages
- Resolution: `direct_root_join`
- Found: `9`
- Missing: `3`

### Missing Patterns

- `InventoryItemDataChanged`
- `PLUGIN:CreateNewInventoryPanel`
- `vgui.Create("vendor_grid_inventory")`

### Found Evidence

#### 1. `function PANEL:onVendorPriceUpdated` lines `167-179`

```lua
167: end
168: 
169: function PANEL:onVendorMoneyUpdated(vendor, money)
170: 	self.vendor:setMoney(money)
171: end
172: 
173: function PANEL:onVendorPriceUpdated(vendor, itemType, value)
174: 	local panel = self.items[self.vendor][itemType]
175: 	if (IsValid(panel)) then panel:updatePrice() end
176: 
177: 	panel = self.items[self.me][itemType]
178: 	if (IsValid(panel)) then panel:updatePrice() end
179: end
```

#### 2. `hook.Add("VendorItemPriceUpdated"` lines `198-210`

```lua
198: function PANEL:listenForChanges()
199: 	-- Money changes.
200: 	hook.Add("VendorMoneyUpdated", self, self.onVendorMoneyUpdated)
201: 	hook.Add("OnCharVarChanged", self, self.onCharVarChanged)
202: 
203: 	-- Price change.
204: 	hook.Add("VendorItemPriceUpdated", self, self.onVendorPriceUpdated)
205: 
206: 	-- Item stock changes.
207: 	hook.Add("VendorItemStockUpdated", self, self.onItemStockUpdated)
208: 	hook.Add("VendorItemMaxStockUpdated", self, self.onItemStockUpdated)
209: 
210: 	-- Item mode change.
```

#### 3. `net.Start("nutVendorExit")` lines `229-241`

```lua
229: 	surface.SetDrawColor(0, 0, 0, 100)
230: 	surface.DrawRect(0, 0, w, h)
231: end
232: 
233: function PANEL:OnRemove()
234: 	if (not self.noSendExit) then
235: 		net.Start("nutVendorExit")
236: 		net.SendToServer()
237: 		self.noSendExit = true
238: 	end
239: 
240: 	if (IsValid(nut.gui.vendorEditor)) then
241: 		nut.gui.vendorEditor:Remove()
```

#### 4. `net.Start("nutVendorTrade")` lines `75-87`

```lua
75: 	}
76: 
77: 	self:initializeItems()
78: end
79: 
80: function PANEL:buyItemFromVendor(itemType)
81: 	net.Start("nutVendorTrade")
82: 		net.WriteString(itemType)
83: 		net.WriteBool(false)
84: 	net.SendToServer()
85: end
86: 
87: function PANEL:sellItemToVendor(itemType)
```

#### 5. `net.Start("nutVendorTrade")` lines `82-94`

```lua
82: 		net.WriteString(itemType)
83: 		net.WriteBool(false)
84: 	net.SendToServer()
85: end
86: 
87: function PANEL:sellItemToVendor(itemType)
88: 	net.Start("nutVendorTrade")
89: 		net.WriteString(itemType)
90: 		net.WriteBool(true)
91: 	net.SendToServer()
92: end
93: 
94: function PANEL:initializeItems()
```

#### 6. `panel:updatePrice()` lines `154-166`

```lua
154: function PANEL:onVendorPropEdited(vendor, key)
155: 	if (key == "name") then
156: 		self.vendor:setName(vendor:getName())
157: 	elseif (key == "scale") then
158: 		for _, panel in pairs(self.items[self.vendor]) do
159: 			if (not IsValid(panel)) then continue end
160: 			panel:updatePrice()
161: 		end
162: 		for _, panel in pairs(self.items[self.me]) do
163: 			if (not IsValid(panel)) then continue end
164: 			panel:updatePrice()
165: 		end
166: 	end
```

#### 7. `panel:updatePrice()` lines `158-170`

```lua
158: 		for _, panel in pairs(self.items[self.vendor]) do
159: 			if (not IsValid(panel)) then continue end
160: 			panel:updatePrice()
161: 		end
162: 		for _, panel in pairs(self.items[self.me]) do
163: 			if (not IsValid(panel)) then continue end
164: 			panel:updatePrice()
165: 		end
166: 	end
167: end
168: 
169: function PANEL:onVendorMoneyUpdated(vendor, money)
170: 	self.vendor:setMoney(money)
```

#### 8. `panel:updatePrice()` lines `169-181`

```lua
169: function PANEL:onVendorMoneyUpdated(vendor, money)
170: 	self.vendor:setMoney(money)
171: end
172: 
173: function PANEL:onVendorPriceUpdated(vendor, itemType, value)
174: 	local panel = self.items[self.vendor][itemType]
175: 	if (IsValid(panel)) then panel:updatePrice() end
176: 
177: 	panel = self.items[self.me][itemType]
178: 	if (IsValid(panel)) then panel:updatePrice() end
179: end
180: 
181: function PANEL:onVendorModeUpdated(vendor, itemType, mode)
```

#### 9. `panel:updatePrice()` lines `172-184`

```lua
172: 
173: function PANEL:onVendorPriceUpdated(vendor, itemType, value)
174: 	local panel = self.items[self.vendor][itemType]
175: 	if (IsValid(panel)) then panel:updatePrice() end
176: 
177: 	panel = self.items[self.me][itemType]
178: 	if (IsValid(panel)) then panel:updatePrice() end
179: end
180: 
181: function PANEL:onVendorModeUpdated(vendor, itemType, mode)
182: 	self:updateItem(itemType, self.vendor)
183: 	self:updateItem(itemType, self.me)
184: end
```

## TV-006 — `plugins/inventory/cl_hooks.lua`

- Priority: `medium`
- Hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI
- Expected runtime relation: client inventory/vendor interface construction and close cleanup boundary
- Resolution: `direct_root_join`
- Found: `14`
- Missing: `2`

### Missing Patterns

- `InventoryItemDataChanged`
- `panel:updatePrice()`

### Found Evidence

#### 1. `PLUGIN:CreateNewInventoryPanel` lines `85-97`

```lua
85: 
86: 	netstream.Start("inventorySetPanelStatus", true)
87: 
88: 	return panel
89: end
90: 
91: function PLUGIN:CreateNewInventoryPanel(client, parent)
92: 	return showInvPanel(client:getChar():getInv(true), client, parent)
93: end
94: 
95: function PLUGIN:CreateTargetNewInventoryPanel(target, invId, parent)
96: 	return showInvPanel(invId, target, parent)
97: end
```

#### 2. `PLUGIN:CreateNewInventoryPanel` lines `101-113`

```lua
101: 	function()
102: 		if (IsValid(invPanel))
103: 		then
104: 			invPanel:Close()
105: 			invPanel = nil
106: 		else
107: 			invPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
108: 		end
109: 	end)
110: 
111: local currInvPanel
112: netstream.Hook(
113: 	"inventoryOpen", 
```

#### 3. `PLUGIN:CreateNewInventoryPanel` lines `114-126`

```lua
114: 	function()
115: 		if (IsValid(currInvPanel))
116: 		then
117: 			return
118: 		end
119: 
120: 		currInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
121: 	end)
122: 
123: netstream.Hook("vendorTradeInterface", function(vendor, invId)
124: 	local PADDING = 4
125: 	if (!IsValid(vendor)) then return end
126: 
```

#### 4. `PLUGIN:CreateNewInventoryPanel` lines `125-137`

```lua
125: 	if (!IsValid(vendor)) then return end
126: 
127: 	local localInv = LocalPlayer():getChar() && LocalPlayer():getChar():getInv(true)
128: 	local loadedInv = nut.inventory.instances[invId]
129: 	if (!loadedInv) then return end
130: 
131: 	local localInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
132: 	local localParent = localInvPanel:GetParent()
133: 	local storageInvPanel = vgui.Create("vendor_grid_inventory")
134: 	storageInvPanel.vendor = vendor
135: 	storageInvPanel:SetUpPanel(loadedInv)
136: 	nut.gui["vendorTradeInterface" .. vendor:EntIndex()] = storageInvPanel
137: 	storageInvPanel:SetTitle(vendor:GetVendorName())
```

#### 5. `hook.Run("OnCreateStoragePanel"` lines `160-172`

```lua
160: 
161: 		netstream.Start("removeReceiverFromVendor", vendor:EntIndex())
162: 
163: 		netstream.Start("inventorySetPanelStatus", false)
164: 	end
165: 
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
168: 	localInvPanel.MainInvPanel.pair = storageInvPanel.mainInvPanel
169: 	storageInvPanel.mainInvPanel.pair = localInvPanel.MainInvPanel
170: 
171: 	localParent.OnRemove = exitStorageOnRemove
172: 	storageInvPanel.OnRemove = exitStorageOnRemove
```

#### 6. `netstream.Hook("vendorTradeInterface"` lines `117-129`

```lua
117: 			return
118: 		end
119: 
120: 		currInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
121: 	end)
122: 
123: netstream.Hook("vendorTradeInterface", function(vendor, invId)
124: 	local PADDING = 4
125: 	if (!IsValid(vendor)) then return end
126: 
127: 	local localInv = LocalPlayer():getChar() && LocalPlayer():getChar():getInv(true)
128: 	local loadedInv = nut.inventory.instances[invId]
129: 	if (!loadedInv) then return end
```

#### 7. `netstream.Start("inventorySetPanelStatus"` lines `24-36`

```lua
24: 	parentFrame.model.Entity:SetSkin(target:GetSkin())
25: 
26: 	parentFrame.OnKeyCodePressed = function(this, keyCode)
27: 		if (keyCode == KEY_I)
28: 		then
29: 			parentFrame:Close()
30: 			netstream.Start("inventorySetPanelStatus", false)
31: 		end
32: 	end
33: 
34: 	parentFrame.OnClose = function(this)
35: 		netstream.Start("inventorySetPanelStatus", false)
36: 	end
```

#### 8. `netstream.Start("inventorySetPanelStatus"` lines `29-41`

```lua
29: 			parentFrame:Close()
30: 			netstream.Start("inventorySetPanelStatus", false)
31: 		end
32: 	end
33: 
34: 	parentFrame.OnClose = function(this)
35: 		netstream.Start("inventorySetPanelStatus", false)
36: 	end
37: 
38: 	local charScale = {
39: 		["models/krizhpinky/kncr.mdl"] = 0.82,
40: 		["models/voxaid/signalis_star/star_pm.mdl"] = 0.82,
41: 		["models/voxaid/signalis_mynah/mynah_no_armor.mdl"] = 0.82,
```

#### 9. `netstream.Start("inventorySetPanelStatus"` lines `80-92`

```lua
80: 	panel:SetPos(1, 25)
81: 
82: 	netstream.Start("invsRuleSet", target)
83: 
84: 	nut.gui[globalName] = panel
85: 
86: 	netstream.Start("inventorySetPanelStatus", true)
87: 
88: 	return panel
89: end
90: 
91: function PLUGIN:CreateNewInventoryPanel(client, parent)
92: 	return showInvPanel(client:getChar():getInv(true), client, parent)
```

#### 10. `netstream.Start("inventorySetPanelStatus"` lines `157-169`

```lua
157: 				panel == localParent and storageInvPanel or localParent
158: 			if (IsValid(otherPanel)) then otherPanel:Remove() end
159: 		end
160: 
161: 		netstream.Start("removeReceiverFromVendor", vendor:EntIndex())
162: 
163: 		netstream.Start("inventorySetPanelStatus", false)
164: 	end
165: 
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
168: 	localInvPanel.MainInvPanel.pair = storageInvPanel.mainInvPanel
169: 	storageInvPanel.mainInvPanel.pair = localInvPanel.MainInvPanel
```

#### 11. `netstream.Start("inventorySetPanelStatus"` lines `313-321`

```lua
313: netstream.Hook(
314: 	"inventoryCloseOnAction",
315: 	function()
316: 		if (IsValid(invFrame))
317: 		then
318: 			invFrame:Close()
319: 			netstream.Start("inventorySetPanelStatus", false)
320: 		end
321: 	end)
```

#### 12. `netstream.Start("removeReceiverFromVendor"` lines `155-167`

```lua
155: 			nutStorageBase:exitStorage()
156: 			local otherPanel =
157: 				panel == localParent and storageInvPanel or localParent
158: 			if (IsValid(otherPanel)) then otherPanel:Remove() end
159: 		end
160: 
161: 		netstream.Start("removeReceiverFromVendor", vendor:EntIndex())
162: 
163: 		netstream.Start("inventorySetPanelStatus", false)
164: 	end
165: 
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
```

#### 13. `storageInvPanel:SetUpPanel(loadedInv)` lines `129-141`

```lua
129: 	if (!loadedInv) then return end
130: 
131: 	local localInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
132: 	local localParent = localInvPanel:GetParent()
133: 	local storageInvPanel = vgui.Create("vendor_grid_inventory")
134: 	storageInvPanel.vendor = vendor
135: 	storageInvPanel:SetUpPanel(loadedInv)
136: 	nut.gui["vendorTradeInterface" .. vendor:EntIndex()] = storageInvPanel
137: 	storageInvPanel:SetTitle(vendor:GetVendorName())
138: 
139: 	localParent:ShowCloseButton(true)
140: 	storageInvPanel:ShowCloseButton(true)
141: 
```

#### 14. `vgui.Create("vendor_grid_inventory")` lines `127-139`

```lua
127: 	local localInv = LocalPlayer():getChar() && LocalPlayer():getChar():getInv(true)
128: 	local loadedInv = nut.inventory.instances[invId]
129: 	if (!loadedInv) then return end
130: 
131: 	local localInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
132: 	local localParent = localInvPanel:GetParent()
133: 	local storageInvPanel = vgui.Create("vendor_grid_inventory")
134: 	storageInvPanel.vendor = vendor
135: 	storageInvPanel:SetUpPanel(loadedInv)
136: 	nut.gui["vendorTradeInterface" .. vendor:EntIndex()] = storageInvPanel
137: 	storageInvPanel:SetTitle(vendor:GetVendorName())
138: 
139: 	localParent:ShowCloseButton(true)
```

## TV-007 — `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`

- Priority: `medium`
- Hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI
- Expected runtime relation: client grid panel refreshes item icons when item data changes
- Resolution: `direct_root_join`
- Found: `14`
- Missing: `3`

### Missing Patterns

- `PLUGIN:CreateNewInventoryPanel`
- `panel:updatePrice()`
- `vgui.Create("vendor_grid_inventory")`

### Found Evidence

#### 1. `InventoryItemDataChanged` lines `270-282`

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
```

#### 2. `function PANEL:InventoryItemDataChanged` lines `270-282`

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
```

#### 3. `function PANEL:InventoryItemRemoved` lines `265-277`

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
```

#### 4. `function PANEL:addItem` lines `106-118`

```lua
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
```

#### 5. `item:getData("x")` lines `27-39`

```lua
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
```

#### 6. `item:getData("x")` lines `108-120`

```lua
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
119: 	end
120: 	local size = self.size + PADDING
```

#### 7. `item:getData("x")` lines `188-200`

```lua
188: 	local maxOffsetY = (item.height or 1) - 1
189: 	local maxOffsetX = (item.width or 1) - 1
190: 	local drawTarget = nil 
191: 	for itemID, invItem in pairs(self.inventory.items) do
192: 		if (item:getID() == itemID) then continue end
193: 
194: 		local targetX, targetY = invItem:getData("x") - 1, invItem:getData("y") - 1
195: 		local targetW, targetH = invItem.width - 1, invItem.height - 1
196: 
197: 		if (
198: 			x + (item.width - 1) >= targetX and x <= targetX + targetW and
199: 			y + (item.height - 1) >= targetY and y <= targetY + targetH and 
200: 			(invItem.onCombine or item.onCombineTo)
```

#### 8. `item:getData("y")` lines `27-39`

```lua
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
```

#### 9. `item:getData("y")` lines `108-120`

```lua
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
119: 	end
120: 	local size = self.size + PADDING
```

#### 10. `item:getData("y")` lines `188-200`

```lua
188: 	local maxOffsetY = (item.height or 1) - 1
189: 	local maxOffsetX = (item.width or 1) - 1
190: 	local drawTarget = nil 
191: 	for itemID, invItem in pairs(self.inventory.items) do
192: 		if (item:getID() == itemID) then continue end
193: 
194: 		local targetX, targetY = invItem:getData("x") - 1, invItem:getData("y") - 1
195: 		local targetW, targetH = invItem.width - 1, invItem.height - 1
196: 
197: 		if (
198: 			x + (item.width - 1) >= targetX and x <= targetX + targetW and
199: 			y + (item.height - 1) >= targetY and y <= targetY + targetH and 
200: 			(invItem.onCombine or item.onCombineTo)
```

#### 11. `self:populateItems()` lines `41-53`

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
```

#### 12. `self:populateItems()` lines `261-273`

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
```

#### 13. `self:populateItems()` lines `266-278`

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
```

#### 14. `self:populateItems()` lines `271-283`

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
```

## TV-008 — `plugins/vendor/entities/entities/nut_vendor/init.lua`

- Priority: `medium`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Expected runtime relation: server vendor entity creates/clears vendor item presentation metadata
- Resolution: `direct_root_join`
- Found: `15`
- Missing: `4`

### Missing Patterns

- `"invData"`
- `item:sync(recipients)`
- `local recipients = self:getRecipients()`
- `self:getOwner`

### Found Evidence

#### 1. `function ENT:RemoveReceiverFromVendor` lines `284-296`

```lua
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

#### 2. `function ENT:VendorItemSetData` lines `209-221`

```lua
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

#### 3. `hook.Run("OpenVendorTradeInterface"` lines `51-63`

```lua
51: 		return false
52: 	end
53: 
54: 	self.receivers[#self.receivers + 1] = activator
55: 	activator.nutVendor = self
56: 
57: 	hook.Run("OpenVendorTradeInterface", activator, self, self.invId)
58: end
59: 
60: function ENT:SetMoneyAmount(value)
61: 	if (!isnumber(value) || value < 0) then return end
62: 	self:SetMoney(value)
63: end
```

#### 4. `item:setData("vendorMQty"` lines `212-224`

```lua
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

#### 5. `item:setData("vendorQty"` lines `210-222`

```lua
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

#### 6. `item:setData("vendorSPrice"` lines `211-223`

```lua
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

#### 7. `netstream.Start` lines `22-34`

```lua
22: 	return entity
23: end
24: 
25: function ENT:Use(activator)
26: 	nut.log.add(activator, "vendorAccess", self:GetVendorName())
27: 	local index = self:EntIndex()
28: 	netstream.Start(activator, "sendVendorInfo", index, self.factions, self.items)
29: 	if (activator:IsAdmin())
30: 	then
31: 		netstream.Start(activator, "interfaceTurnOn", index)
32: 	else
33: 		self:OpenVendorTrade(activator)
34: 	end
```

#### 8. `netstream.Start` lines `25-37`

```lua
25: function ENT:Use(activator)
26: 	nut.log.add(activator, "vendorAccess", self:GetVendorName())
27: 	local index = self:EntIndex()
28: 	netstream.Start(activator, "sendVendorInfo", index, self.factions, self.items)
29: 	if (activator:IsAdmin())
30: 	then
31: 		netstream.Start(activator, "interfaceTurnOn", index)
32: 	else
33: 		self:OpenVendorTrade(activator)
34: 	end
35: end
36: 
37: function ENT:OpenVendorTrade(activator)
```

#### 9. `netstream.Start` lines `64-76`

```lua
64: 
65: function ENT:HandleMoney(value, client)
66: 	if (!isnumber(value)) then return end
67: 	self:SetMoney(self:GetMoney() + value)
68: 
69: 	for k, v in pairs(self.receivers) do
70: 		netstream.Start(v, "setUpTargetMoney", self:GetMoney(), "vendorTradeInterface" .. self:EntIndex())
71: 	end
72: end
73: 
74: function ENT:IsCanAfford(value)
75: 	if (!isnumber(value) or value < 0) then return end
76: 	return self:GetMoney() - value >= 0
```

#### 10. `netstream.Start` lines `114-126`

```lua
114: 		end)
115: 	elseif (!item)
116: 	then
117: 		self:AddItemAndSetQty(inv, uniqueID, client)
118: 	end
119: 
120: 	netstream.Start(client, "sendVendorInfo", self:EntIndex(), self.factions, self.items)
121: end
122: 
123: function ENT:SetItemToBuy(uniqueID, qty, price)
124: 	if (self.items[uniqueID])
125: 	then
126: 		self.items[uniqueID].maxQty = tonumber(qty) || 0
```

#### 11. `netstream.Start` lines `131-143`

```lua
131: 			maxQty = tonumber(qty) || 0,
132: 			buyPrice = tonumber(price),
133: 			qty = 0
134: 		}
135: 	end
136: 
137: 	netstream.Start(client, "sendVendorInfo", self:EntIndex(), self.factions, self.items)
138: end
139: 
140: function ENT:GetItemPrice(uniqueID, isSell, client)
141: 	if (self.items[uniqueID])
142: 	then
143: 		return isSell && self.items[uniqueID].price || self.items[uniqueID].buyPrice
```

#### 12. `v:setData("vendorBPrice", nil` lines `290-302`

```lua
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

#### 13. `v:setData("vendorMQty", nil` lines `293-305`

```lua
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

#### 14. `v:setData("vendorQty", nil` lines `291-303`

```lua
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

#### 15. `v:setData("vendorSPrice", nil` lines `292-304`

```lua
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

## TV-009 — `gamemode/core/meta/item/sv_item.lua`

- Priority: `medium`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Expected runtime relation: server item data mutation persists and conditionally syncs item data through invData
- Resolution: `direct_root_join`
- Found: `12`
- Missing: `3`

### Missing Patterns

- `item:sync(recipients)`
- `local recipients = self:getRecipients()`
- `self:setNetVar`

### Found Evidence

#### 1. `"invData"` lines `168-180`

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
```

#### 2. `function ITEM:setData` lines `154-166`

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
```

#### 3. `netstream.Start` lines `166-178`

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
```

#### 4. `netstream.Start` lines `222-234`

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
```

#### 5. `nut.db.updateTable` lines `183-195`

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
```

#### 6. `nut.db.updateTable` lines `198-210`

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
```

#### 7. `nut.db.updateTable` lines `237-249`

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
```

#### 8. `self.data[key] = value` lines `156-168`

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
```

#### 9. `self:getOwner` lines `165-177`

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
```

#### 10. `self:getOwner` lines `167-179`

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
```

#### 11. `self:getOwner` lines `221-233`

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
```

#### 12. `self:getOwner` lines `223-235`

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
```

## TV-010 — `gamemode/core/meta/inventory/sv_base_inventory.lua`

- Priority: `medium`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Expected runtime relation: server inventory ownership and recipient sync boundary
- Resolution: `direct_root_join`
- Found: `9`
- Missing: `2`

### Missing Patterns

- `netstream.Start`
- `self:getOwner`

### Found Evidence

#### 1. `"invData"` lines `1-13`

```lua
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
```

#### 2. `function Inventory:addItem` lines `12-24`

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
```

#### 3. `function Inventory:getRecipients` lines `193-205`

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
```

#### 4. `function Inventory:removeItem` lines `99-111`

```lua
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
```

#### 5. `function Inventory:syncItemAdded` lines `35-47`

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
```

#### 6. `item:sync(recipients)` lines `42-54`

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
```

#### 7. `local recipients = self:getRecipients()` lines `41-53`

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
```

#### 8. `net.Send(recipients)` lines `46-58`

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
```

#### 9. `net.Start("nutInventoryAdd")` lines `43-55`

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
```

## TV-011 — `gamemode/core/meta/inventory/cl_base_inventory.lua`

- Priority: `medium`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Expected runtime relation: client inventory membership/data receiver boundary
- Resolution: `direct_root_join`
- Found: `6`
- Missing: `5`

### Missing Patterns

- `"invData"`
- `item:sync(recipients)`
- `local recipients = self:getRecipients()`
- `netstream.Start`
- `self:getOwner`

### Found Evidence

#### 1. `hook.Run("InventoryDataChanged"` lines `11-23`

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
```

#### 2. `hook.Run("InventoryItemAdded"` lines `57-69`

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
```

#### 3. `hook.Run("InventoryItemRemoved"` lines `69-81`

```lua
69: 	local invID = net.ReadType()
70: 	local item = nut.item.instances[itemID]
71: 	local inventory = nut.inventory.instances[invID]
72: 	if (item and inventory and inventory.items[itemID]) then
73: 		inventory.items[itemID] = nil
74: 		item.invID = 0
75: 		hook.Run("InventoryItemRemoved", inventory, item)
76: 	end
77: end)
78: 
79: net.Receive("nutInventoryDelete", function()
80: 	local invID = net.ReadType()
81: 	local instance = nut.inventory.instances[invID]
```

#### 4. `net.Receive("nutInventoryAdd"` lines `50-62`

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
```

#### 5. `net.Receive("nutInventoryData"` lines `1-9`

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
```

#### 6. `net.Receive("nutInventoryRemove"` lines `61-73`

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
```

## TV-012 — `plugins/storage/cl_networking.lua`

- Priority: `low`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Expected runtime relation: storage open/exit network boundary
- Resolution: `direct_root_join`
- Found: `3`
- Missing: `4`

### Missing Patterns

- `OnCreateStoragePanel`
- `SetUpPanel`
- `inventorySetPanelStatus`
- `self:populateItems()`

### Found Evidence

#### 1. `StorageOpen` lines `1-12`

```lua
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
```

#### 2. `StorageOpen` lines `2-14`

```lua
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
13: 	net.SendToServer()
14: end
```

#### 3. `hook.Run("StorageOpen"` lines `2-14`

```lua
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
13: 	net.SendToServer()
14: end
```

## TV-013 — `plugins/inventory/cl_hooks.lua`

- Priority: `low`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Expected runtime relation: client inventory/vendor interface construction and close cleanup boundary
- Resolution: `direct_root_join`
- Found: `17`
- Missing: `2`

### Missing Patterns

- `StorageOpen`
- `self:populateItems()`

### Found Evidence

#### 1. `OnCreateStoragePanel` lines `160-172`

```lua
160: 
161: 		netstream.Start("removeReceiverFromVendor", vendor:EntIndex())
162: 
163: 		netstream.Start("inventorySetPanelStatus", false)
164: 	end
165: 
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
168: 	localInvPanel.MainInvPanel.pair = storageInvPanel.mainInvPanel
169: 	storageInvPanel.mainInvPanel.pair = localInvPanel.MainInvPanel
170: 
171: 	localParent.OnRemove = exitStorageOnRemove
172: 	storageInvPanel.OnRemove = exitStorageOnRemove
```

#### 2. `PLUGIN:CreateNewInventoryPanel` lines `85-97`

```lua
85: 
86: 	netstream.Start("inventorySetPanelStatus", true)
87: 
88: 	return panel
89: end
90: 
91: function PLUGIN:CreateNewInventoryPanel(client, parent)
92: 	return showInvPanel(client:getChar():getInv(true), client, parent)
93: end
94: 
95: function PLUGIN:CreateTargetNewInventoryPanel(target, invId, parent)
96: 	return showInvPanel(invId, target, parent)
97: end
```

#### 3. `PLUGIN:CreateNewInventoryPanel` lines `101-113`

```lua
101: 	function()
102: 		if (IsValid(invPanel))
103: 		then
104: 			invPanel:Close()
105: 			invPanel = nil
106: 		else
107: 			invPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
108: 		end
109: 	end)
110: 
111: local currInvPanel
112: netstream.Hook(
113: 	"inventoryOpen", 
```

#### 4. `PLUGIN:CreateNewInventoryPanel` lines `114-126`

```lua
114: 	function()
115: 		if (IsValid(currInvPanel))
116: 		then
117: 			return
118: 		end
119: 
120: 		currInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
121: 	end)
122: 
123: netstream.Hook("vendorTradeInterface", function(vendor, invId)
124: 	local PADDING = 4
125: 	if (!IsValid(vendor)) then return end
126: 
```

#### 5. `PLUGIN:CreateNewInventoryPanel` lines `125-137`

```lua
125: 	if (!IsValid(vendor)) then return end
126: 
127: 	local localInv = LocalPlayer():getChar() && LocalPlayer():getChar():getInv(true)
128: 	local loadedInv = nut.inventory.instances[invId]
129: 	if (!loadedInv) then return end
130: 
131: 	local localInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
132: 	local localParent = localInvPanel:GetParent()
133: 	local storageInvPanel = vgui.Create("vendor_grid_inventory")
134: 	storageInvPanel.vendor = vendor
135: 	storageInvPanel:SetUpPanel(loadedInv)
136: 	nut.gui["vendorTradeInterface" .. vendor:EntIndex()] = storageInvPanel
137: 	storageInvPanel:SetTitle(vendor:GetVendorName())
```

#### 6. `SetUpPanel` lines `73-85`

```lua
73: 	if (IsValid(nut.gui[globalName]))
74: 	then
75: 		nut.gui[globalName]:Remove()
76: 	end
77: 
78: 	panel = vgui.Create("extendedNutGridInventory", parentFrame)
79: 	panel:SetUpPanel(invs)
80: 	panel:SetPos(1, 25)
81: 
82: 	netstream.Start("invsRuleSet", target)
83: 
84: 	nut.gui[globalName] = panel
85: 
```

#### 7. `SetUpPanel` lines `129-141`

```lua
129: 	if (!loadedInv) then return end
130: 
131: 	local localInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
132: 	local localParent = localInvPanel:GetParent()
133: 	local storageInvPanel = vgui.Create("vendor_grid_inventory")
134: 	storageInvPanel.vendor = vendor
135: 	storageInvPanel:SetUpPanel(loadedInv)
136: 	nut.gui["vendorTradeInterface" .. vendor:EntIndex()] = storageInvPanel
137: 	storageInvPanel:SetTitle(vendor:GetVendorName())
138: 
139: 	localParent:ShowCloseButton(true)
140: 	storageInvPanel:ShowCloseButton(true)
141: 
```

#### 8. `hook.Run("OnCreateStoragePanel"` lines `160-172`

```lua
160: 
161: 		netstream.Start("removeReceiverFromVendor", vendor:EntIndex())
162: 
163: 		netstream.Start("inventorySetPanelStatus", false)
164: 	end
165: 
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
168: 	localInvPanel.MainInvPanel.pair = storageInvPanel.mainInvPanel
169: 	storageInvPanel.mainInvPanel.pair = localInvPanel.MainInvPanel
170: 
171: 	localParent.OnRemove = exitStorageOnRemove
172: 	storageInvPanel.OnRemove = exitStorageOnRemove
```

#### 9. `netstream.Hook("vendorTradeInterface"` lines `117-129`

```lua
117: 			return
118: 		end
119: 
120: 		currInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
121: 	end)
122: 
123: netstream.Hook("vendorTradeInterface", function(vendor, invId)
124: 	local PADDING = 4
125: 	if (!IsValid(vendor)) then return end
126: 
127: 	local localInv = LocalPlayer():getChar() && LocalPlayer():getChar():getInv(true)
128: 	local loadedInv = nut.inventory.instances[invId]
129: 	if (!loadedInv) then return end
```

#### 10. `netstream.Start("inventorySetPanelStatus"` lines `24-36`

```lua
24: 	parentFrame.model.Entity:SetSkin(target:GetSkin())
25: 
26: 	parentFrame.OnKeyCodePressed = function(this, keyCode)
27: 		if (keyCode == KEY_I)
28: 		then
29: 			parentFrame:Close()
30: 			netstream.Start("inventorySetPanelStatus", false)
31: 		end
32: 	end
33: 
34: 	parentFrame.OnClose = function(this)
35: 		netstream.Start("inventorySetPanelStatus", false)
36: 	end
```

#### 11. `netstream.Start("inventorySetPanelStatus"` lines `29-41`

```lua
29: 			parentFrame:Close()
30: 			netstream.Start("inventorySetPanelStatus", false)
31: 		end
32: 	end
33: 
34: 	parentFrame.OnClose = function(this)
35: 		netstream.Start("inventorySetPanelStatus", false)
36: 	end
37: 
38: 	local charScale = {
39: 		["models/krizhpinky/kncr.mdl"] = 0.82,
40: 		["models/voxaid/signalis_star/star_pm.mdl"] = 0.82,
41: 		["models/voxaid/signalis_mynah/mynah_no_armor.mdl"] = 0.82,
```

#### 12. `netstream.Start("inventorySetPanelStatus"` lines `80-92`

```lua
80: 	panel:SetPos(1, 25)
81: 
82: 	netstream.Start("invsRuleSet", target)
83: 
84: 	nut.gui[globalName] = panel
85: 
86: 	netstream.Start("inventorySetPanelStatus", true)
87: 
88: 	return panel
89: end
90: 
91: function PLUGIN:CreateNewInventoryPanel(client, parent)
92: 	return showInvPanel(client:getChar():getInv(true), client, parent)
```

#### 13. `netstream.Start("inventorySetPanelStatus"` lines `157-169`

```lua
157: 				panel == localParent and storageInvPanel or localParent
158: 			if (IsValid(otherPanel)) then otherPanel:Remove() end
159: 		end
160: 
161: 		netstream.Start("removeReceiverFromVendor", vendor:EntIndex())
162: 
163: 		netstream.Start("inventorySetPanelStatus", false)
164: 	end
165: 
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
168: 	localInvPanel.MainInvPanel.pair = storageInvPanel.mainInvPanel
169: 	storageInvPanel.mainInvPanel.pair = localInvPanel.MainInvPanel
```

#### 14. `netstream.Start("inventorySetPanelStatus"` lines `313-321`

```lua
313: netstream.Hook(
314: 	"inventoryCloseOnAction",
315: 	function()
316: 		if (IsValid(invFrame))
317: 		then
318: 			invFrame:Close()
319: 			netstream.Start("inventorySetPanelStatus", false)
320: 		end
321: 	end)
```

#### 15. `netstream.Start("removeReceiverFromVendor"` lines `155-167`

```lua
155: 			nutStorageBase:exitStorage()
156: 			local otherPanel =
157: 				panel == localParent and storageInvPanel or localParent
158: 			if (IsValid(otherPanel)) then otherPanel:Remove() end
159: 		end
160: 
161: 		netstream.Start("removeReceiverFromVendor", vendor:EntIndex())
162: 
163: 		netstream.Start("inventorySetPanelStatus", false)
164: 	end
165: 
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
```

#### 16. `storageInvPanel:SetUpPanel(loadedInv)` lines `129-141`

```lua
129: 	if (!loadedInv) then return end
130: 
131: 	local localInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
132: 	local localParent = localInvPanel:GetParent()
133: 	local storageInvPanel = vgui.Create("vendor_grid_inventory")
134: 	storageInvPanel.vendor = vendor
135: 	storageInvPanel:SetUpPanel(loadedInv)
136: 	nut.gui["vendorTradeInterface" .. vendor:EntIndex()] = storageInvPanel
137: 	storageInvPanel:SetTitle(vendor:GetVendorName())
138: 
139: 	localParent:ShowCloseButton(true)
140: 	storageInvPanel:ShowCloseButton(true)
141: 
```

#### 17. `vgui.Create("vendor_grid_inventory")` lines `127-139`

```lua
127: 	local localInv = LocalPlayer():getChar() && LocalPlayer():getChar():getInv(true)
128: 	local loadedInv = nut.inventory.instances[invId]
129: 	if (!loadedInv) then return end
130: 
131: 	local localInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
132: 	local localParent = localInvPanel:GetParent()
133: 	local storageInvPanel = vgui.Create("vendor_grid_inventory")
134: 	storageInvPanel.vendor = vendor
135: 	storageInvPanel:SetUpPanel(loadedInv)
136: 	nut.gui["vendorTradeInterface" .. vendor:EntIndex()] = storageInvPanel
137: 	storageInvPanel:SetTitle(vendor:GetVendorName())
138: 
139: 	localParent:ShowCloseButton(true)
```

## TV-014 — `plugins/gridinv/plugins/gridstorage/sh_plugin.lua`

- Priority: `low`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Expected runtime relation: grid storage UI construction and panel pairing boundary
- Resolution: `direct_root_join`
- Found: `3`
- Missing: `3`

### Missing Patterns

- `SetUpPanel`
- `hook.Run("StorageOpen"`
- `self:populateItems()`

### Found Evidence

#### 1. `OnCreateStoragePanel` lines `207-219`

```lua
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
```

#### 2. `StorageOpen` lines `147-159`

```lua
147: 		end)
148: 	end
149: }
150: 
151: 
152: if (CLIENT) then
153: 	function PLUGIN:StorageOpen(storage)
154: 		-- Number of pixels between the local inventory and storage inventory.
155: 		local PADDING = 4
156: 
157: 		if (
158: 			!IsValid(storage) ||
159: 			((storage.getStorageInfo && storage:getStorageInfo().invType != INV_TYPE_ID) &&
```

#### 3. `inventorySetPanelStatus` lines `204-216`

```lua
204: 
205: 			if (storage:GetModel() == "models/trashcan/trashcan.mdl")
206: 			then
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
```

## TV-015 — `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`

- Priority: `low`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Expected runtime relation: client grid panel refreshes item icons when item data changes
- Resolution: `direct_root_join`
- Found: `13`
- Missing: `3`

### Missing Patterns

- `OnCreateStoragePanel`
- `SetUpPanel`
- `StorageOpen`

### Found Evidence

#### 1. `function PANEL:InventoryItemDataChanged` lines `270-282`

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
```

#### 2. `function PANEL:InventoryItemRemoved` lines `265-277`

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
```

#### 3. `function PANEL:addItem` lines `106-118`

```lua
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
```

#### 4. `item:getData("x")` lines `27-39`

```lua
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
```

#### 5. `item:getData("x")` lines `108-120`

```lua
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
119: 	end
120: 	local size = self.size + PADDING
```

#### 6. `item:getData("x")` lines `188-200`

```lua
188: 	local maxOffsetY = (item.height or 1) - 1
189: 	local maxOffsetX = (item.width or 1) - 1
190: 	local drawTarget = nil 
191: 	for itemID, invItem in pairs(self.inventory.items) do
192: 		if (item:getID() == itemID) then continue end
193: 
194: 		local targetX, targetY = invItem:getData("x") - 1, invItem:getData("y") - 1
195: 		local targetW, targetH = invItem.width - 1, invItem.height - 1
196: 
197: 		if (
198: 			x + (item.width - 1) >= targetX and x <= targetX + targetW and
199: 			y + (item.height - 1) >= targetY and y <= targetY + targetH and 
200: 			(invItem.onCombine or item.onCombineTo)
```

#### 7. `item:getData("y")` lines `27-39`

```lua
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
```

#### 8. `item:getData("y")` lines `108-120`

```lua
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
119: 	end
120: 	local size = self.size + PADDING
```

#### 9. `item:getData("y")` lines `188-200`

```lua
188: 	local maxOffsetY = (item.height or 1) - 1
189: 	local maxOffsetX = (item.width or 1) - 1
190: 	local drawTarget = nil 
191: 	for itemID, invItem in pairs(self.inventory.items) do
192: 		if (item:getID() == itemID) then continue end
193: 
194: 		local targetX, targetY = invItem:getData("x") - 1, invItem:getData("y") - 1
195: 		local targetW, targetH = invItem.width - 1, invItem.height - 1
196: 
197: 		if (
198: 			x + (item.width - 1) >= targetX and x <= targetX + targetW and
199: 			y + (item.height - 1) >= targetY and y <= targetY + targetH and 
200: 			(invItem.onCombine or item.onCombineTo)
```

#### 10. `self:populateItems()` lines `41-53`

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
```

#### 11. `self:populateItems()` lines `261-273`

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
```

#### 12. `self:populateItems()` lines `266-278`

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
```

#### 13. `self:populateItems()` lines `271-283`

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
```

## TV-PATCH-016 — `plugins/gridinv/sv_transfer.lua`

- Priority: `high`
- Hypothesis: Vendor purchase transfer clears purchased-item vendor metadata and syncs item data to client UI
- Expected runtime relation: vendor purchase transfer boundary and purchased-item vendor metadata cleanup
- Resolution: `direct_root_join`
- Found: `21`
- Missing: `0`

### Found Evidence

#### 1. `vendorSellItem` lines `72-84`

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
```

#### 2. `vendorSellItem` lines `79-91`

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
```

#### 3. `vendorSellItem` lines `116-128`

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
```

#### 4. `vendorSellItem` lines `161-173`

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
```

#### 5. `vendorSellItem` lines `207-219`

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
```

#### 6. `oldInventory` lines `4-16`

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
```

#### 7. `oldInventory` lines `5-17`

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
```

#### 8. `oldInventory` lines `10-22`

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
```

#### 9. `oldInventory` lines `12-24`

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
```

#### 10. `oldInventory` lines `18-30`

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
```

#### 11. `inventory:add` lines `143-155`

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
```

#### 12. `inventory:add` lines `145-157`

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
```

#### 13. `inventory:add` lines `163-175`

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
```

#### 14. `inventory:add` lines `182-194`

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
```

#### 15. `item:setData("vendorSPrice", nil` lines `213-225`

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
```

#### 16. `item:setData("vendorQty", nil` lines `212-224`

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
```

#### 17. `item:setData("vendorMQty", nil` lines `214-226`

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
```

#### 18. `item:setData("vendorBPrice"` lines `217-229`

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
```

#### 19. `CanItemBeTransfered` lines `12-24`

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
```

#### 20. `HandleItemTransferRequest` lines `1-11`

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
```

#### 21. `HandleItemTransferRequest` lines `233-240`

```lua
233: 	local itemID = net.ReadUInt(32)
234: 	local x = net.ReadUInt(32)
235: 	local y = net.ReadUInt(32)
236: 	local invID = net.ReadType()
237: 	local laltPressed = net.ReadBool()
238: 
239: 	hook.Run("HandleItemTransferRequest", client, itemID, x, y, invID, laltPressed)
240: end)
```

## TV-PATCH-017 — `gamemode/core/libs/item/cl_networking.lua`

- Priority: `high`
- Hypothesis: Vendor purchase transfer clears purchased-item vendor metadata and syncs item data to client UI
- Expected runtime relation: client item metadata delta receive path and ItemDataChanged emission
- Resolution: `direct_root_join`
- Found: `13`
- Missing: `0`

### Found Evidence

#### 1. `netstream.Hook("invData"` lines `7-19`

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
```

#### 2. `hook.Run("ItemDataChanged"` lines `14-26`

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
```

#### 3. `nut.item.instances` lines `8-20`

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
```

#### 4. `nut.item.instances` lines `19-31`

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
```

#### 5. `nut.item.instances` lines `41-53`

```lua
41: 	local quantity = net.ReadUInt(32)
42: 
43: 	item.data = table.Merge(item.data or {}, data)
44: 	item.invID = invID
45: 	item.quantity = quantity
46: 
47: 	nut.item.instances[itemID] = item
48: 	hook.Run("ItemInitialized", item)
49: end)
50: 
51: net.Receive("nutCharacterInvList", function()
52: 	local charID = net.ReadUInt(32)
53: 	local length = net.ReadUInt(32)
```

#### 6. `nut.item.instances` lines `62-74`

```lua
62: 		character.vars.inv = inventories
63: 	end
64: end)
65: 
66: net.Receive("nutItemDelete", function()
67: 	local id = net.ReadUInt(32)
68: 	local instance = nut.item.instances[id]
69: 	if (instance and instance.invID) then
70: 		local inventory = nut.inventory.instances[instance.invID]
71: 		if (not inventory or not inventory.items[id]) then return end
72: 
73: 		inventory.items[id] = nil
74: 		instance.invID = 0
```

#### 7. `nut.item.instances` lines `72-80`

```lua
72: 
73: 		inventory.items[id] = nil
74: 		instance.invID = 0
75: 		hook.Run("InventoryItemRemoved", inventory, instance)
76: 	end
77: 
78: 	nut.item.instances[id] = nil
79: 	hook.Run("ItemDeleted", instance)
80: end)
```

#### 8. `item.data[key]` lines `12-24`

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
```

#### 9. `item.data[key]` lines `13-25`

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
```

#### 10. `oldValue` lines `12-24`

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
```

#### 11. `oldValue` lines `14-26`

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
```

#### 12. `oldValue` lines `22-34`

```lua
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
32: 	end
33: end)
34: 
```

#### 13. `oldValue` lines `25-37`

```lua
25: 	local item = nut.item.instances[id]
26: 
27: 	if (item) then
28: 		local oldValue = item:getQuantity()
29: 		item.quantity = quantity
30: 
31: 		hook.Run("ItemQuantityChanged", item, oldValue, quantity)
32: 	end
33: end)
34: 
35: net.Receive("nutItemInstance", function()
36: 	local itemID = net.ReadUInt(32)
37: 	local itemType = net.ReadString()
```
