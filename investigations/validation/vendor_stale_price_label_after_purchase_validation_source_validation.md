# SIGNALIS AI — Targeted Source Validation

- Targeted plan: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_targeted_validation.json`
- Query: `vendor stale price label after purchase`
- Pattern results: `282`
- Found: `216`
- Missing: `66`

## Interpretation

This report validates targeted hypothesis checks against exact source files.

Use found patterns as source anchors. Missing patterns are not automatically bugs; they may mean the targeted plan expected the wrong file or naming.

## File Summary

- `gamemode/core/meta/inventory/cl_base_inventory.lua`: found `24`, missing `14`
- `plugins/inventory/cl_hooks.lua`: found `53`, missing `4`
- `plugins/vendor/derma/cl_vendor.lua`: found `37`, missing `6`
- `plugins/vendor/entities/entities/nut_vendor/init.lua`: found `68`, missing `3`
- `gamemode/core/libs/item/sv_item.lua`: found `0`, missing `11`
- `gamemode/core/meta/inventory/sv_base_inventory.lua`: found `18`, missing `6`
- `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`: found `12`, missing `13`
- `plugins/gridinv/plugins/gridstorage/sh_plugin.lua`: found `2`, missing `4`
- `plugins/storage/cl_networking.lua`: found `2`, missing `5`

## TV-001 — `gamemode/core/meta/inventory/cl_base_inventory.lua`

- Priority: `high`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Expected runtime relation: client inventory data delta receiver mutates local inventory/item data
- Found: `13`
- Missing: `6`

### Missing Patterns

- `ItemDataChanged`
- `RemoveReceiverFromVendor`
- `invData`
- `netstream.Hook`
- `setData`
- `vendorSPrice`

### Found Evidence

#### 1. `data` lines `1-9`

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

#### 2. `data` lines `3-15`

```lua
3: net.Receive("nutInventoryData", function()
4: 	local id = net.ReadType()
5: 	local key = net.ReadString()
6: 	local value = net.ReadType()
7: 	local instance = nut.inventory.instances[id]
8: 	if (not instance) then
9: 		ErrorNoHalt("Got data "..key.." for non-existent instance "..id)
10: 		return
11: 	end
12: 
13: 	local oldValue = instance.data[key]
14: 	instance.data[key] = value
15: 	instance:onDataChanged(key, oldValue, value)
```

#### 3. `data` lines `7-19`

```lua
7: 	local instance = nut.inventory.instances[id]
8: 	if (not instance) then
9: 		ErrorNoHalt("Got data "..key.." for non-existent instance "..id)
10: 		return
11: 	end
12: 
13: 	local oldValue = instance.data[key]
14: 	instance.data[key] = value
15: 	instance:onDataChanged(key, oldValue, value)
16: 
17: 	hook.Run("InventoryDataChanged", instance, key, oldValue, value)
18: end)
19: 
```

#### 4. `data` lines `8-20`

```lua
8: 	if (not instance) then
9: 		ErrorNoHalt("Got data "..key.." for non-existent instance "..id)
10: 		return
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
```

#### 5. `data` lines `9-21`

```lua
9: 		ErrorNoHalt("Got data "..key.." for non-existent instance "..id)
10: 		return
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
```

#### 6. `net.Receive` lines `1-9`

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

#### 7. `net.Receive` lines `14-26`

```lua
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
24: 	local instance = nut.inventory.new(typeID)
25: 	instance.id = id
26: 	instance.data = data
```

#### 8. `net.Receive` lines `50-62`

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

#### 9. `net.Receive` lines `61-73`

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

#### 10. `net.Receive` lines `73-85`

```lua
73: 		inventory.items[itemID] = nil
74: 		item.invID = 0
75: 		hook.Run("InventoryItemRemoved", inventory, item)
76: 	end
77: end)
78: 
79: net.Receive("nutInventoryDelete", function()
80: 	local invID = net.ReadType()
81: 	local instance = nut.inventory.instances[invID]
82: 	if (instance) then
83: 		hook.Run("InventoryDeleted", instance)
84: 	end
85: 	if (invID) then
```

#### 11. `nil` lines `67-79`

```lua
67: net.Receive("nutInventoryRemove", function()
68: 	local itemID = net.ReadUInt(32)
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
```

#### 12. `nil` lines `80-92`

```lua
80: 	local invID = net.ReadType()
81: 	local instance = nut.inventory.instances[invID]
82: 	if (instance) then
83: 		hook.Run("InventoryDeleted", instance)
84: 	end
85: 	if (invID) then
86: 		nut.inventory.instances[invID] = nil
87: 	end
88: end)
89: 
90: function Inventory:show(parent)
91: 	return nut.inventory.show(self, parent)
92: end
```

#### 13. `nutInventoryData` lines `1-9`

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

## TV-003 — `plugins/inventory/cl_hooks.lua`

- Priority: `high`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Expected runtime relation: client inventory/vendor interface constructs player inventory and vendor_grid_inventory panels
- Found: `21`
- Missing: `2`

### Missing Patterns

- `invData`
- `vendorSPrice`

### Found Evidence

#### 1. `CreateNewInventoryPanel` lines `85-97`

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

#### 2. `CreateNewInventoryPanel` lines `101-113`

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

#### 3. `CreateNewInventoryPanel` lines `114-126`

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

#### 4. `CreateNewInventoryPanel` lines `125-137`

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

#### 5. `OnCreateStoragePanel` lines `160-172`

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

#### 6. `OnRemove` lines `143-155`

```lua
143: 	localParent:Center()
144: 	storageInvPanel:Center()
145: 	localParent.x = localParent.x + extraWidth
146: 	storageInvPanel:MoveLeftOf(localParent, PADDING)
147: 
148: 	local firstToRemove = true
149: 	localParent.oldOnRemove = localParent.OnRemove
150: 	storageInvPanel.oldOnRemove = storageInvPanel.OnRemove
151: 
152: 	local function exitStorageOnRemove(panel)
153: 		if (firstToRemove) then
154: 			firstToRemove = false
155: 			nutStorageBase:exitStorage()
```

#### 7. `OnRemove` lines `144-156`

```lua
144: 	storageInvPanel:Center()
145: 	localParent.x = localParent.x + extraWidth
146: 	storageInvPanel:MoveLeftOf(localParent, PADDING)
147: 
148: 	local firstToRemove = true
149: 	localParent.oldOnRemove = localParent.OnRemove
150: 	storageInvPanel.oldOnRemove = storageInvPanel.OnRemove
151: 
152: 	local function exitStorageOnRemove(panel)
153: 		if (firstToRemove) then
154: 			firstToRemove = false
155: 			nutStorageBase:exitStorage()
156: 			local otherPanel =
```

#### 8. `OnRemove` lines `146-158`

```lua
146: 	storageInvPanel:MoveLeftOf(localParent, PADDING)
147: 
148: 	local firstToRemove = true
149: 	localParent.oldOnRemove = localParent.OnRemove
150: 	storageInvPanel.oldOnRemove = storageInvPanel.OnRemove
151: 
152: 	local function exitStorageOnRemove(panel)
153: 		if (firstToRemove) then
154: 			firstToRemove = false
155: 			nutStorageBase:exitStorage()
156: 			local otherPanel =
157: 				panel == localParent and storageInvPanel or localParent
158: 			if (IsValid(otherPanel)) then otherPanel:Remove() end
```

#### 9. `OnRemove` lines `165-177`

```lua
165: 
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
168: 	localInvPanel.MainInvPanel.pair = storageInvPanel.mainInvPanel
169: 	storageInvPanel.mainInvPanel.pair = localInvPanel.MainInvPanel
170: 
171: 	localParent.OnRemove = exitStorageOnRemove
172: 	storageInvPanel.OnRemove = exitStorageOnRemove
173: end)
174: 
175: local function createTextEntry(frame, placeHolder, x, y, w, h)
176: 	local text = frame:Add("DTextEntry")
177: 	text:SetFont("nutWriteFont")
```

#### 10. `OnRemove` lines `166-178`

```lua
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
168: 	localInvPanel.MainInvPanel.pair = storageInvPanel.mainInvPanel
169: 	storageInvPanel.mainInvPanel.pair = localInvPanel.MainInvPanel
170: 
171: 	localParent.OnRemove = exitStorageOnRemove
172: 	storageInvPanel.OnRemove = exitStorageOnRemove
173: end)
174: 
175: local function createTextEntry(frame, placeHolder, x, y, w, h)
176: 	local text = frame:Add("DTextEntry")
177: 	text:SetFont("nutWriteFont")
178: 	text:SetPos(x, y)
```

#### 11. `RemoveReceiverFromVendor` lines `155-167`

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

#### 12. `SetUpPanel` lines `73-85`

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

#### 13. `SetUpPanel` lines `129-141`

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

#### 14. `nil` lines `99-111`

```lua
99: net.Receive(
100: 	"OpenMyInv",
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
```

#### 15. `nil` lines `101-113`

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

#### 16. `nil` lines `114-126`

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

#### 17. `nil` lines `125-137`

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

#### 18. `removeReceiverFromVendor` lines `155-167`

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

#### 19. `vendorTradeInterface` lines `117-129`

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

#### 20. `vendorTradeInterface` lines `130-142`

```lua
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
142: 	local extraWidth = (storageInvPanel:GetWide() + PADDING) / 2
```

#### 21. `vendor_grid_inventory` lines `127-139`

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

## TV-002 — `plugins/vendor/derma/cl_vendor.lua`

- Priority: `high`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Expected runtime relation: client vendor UI sends trade/exit and refreshes visible vendor price labels
- Found: `19`
- Missing: `3`

### Missing Patterns

- `RemoveReceiverFromVendor`
- `invData`
- `vendorSPrice`

### Found Evidence

#### 1. `OnRemove` lines `227-239`

```lua
227: 	nut.util.drawBlur(self, 10)
228: 
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
```

#### 2. `VendorItemPriceUpdated` lines `198-210`

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

#### 3. `hook.Add` lines `194-206`

```lua
194: 		self.me:setMoney(newValue)
195: 	end
196: end
197: 
198: function PANEL:listenForChanges()
199: 	-- Money changes.
200: 	hook.Add("VendorMoneyUpdated", self, self.onVendorMoneyUpdated)
201: 	hook.Add("OnCharVarChanged", self, self.onCharVarChanged)
202: 
203: 	-- Price change.
204: 	hook.Add("VendorItemPriceUpdated", self, self.onVendorPriceUpdated)
205: 
206: 	-- Item stock changes.
```

#### 4. `hook.Add` lines `195-207`

```lua
195: 	end
196: end
197: 
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
```

#### 5. `hook.Add` lines `198-210`

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

#### 6. `hook.Add` lines `201-213`

```lua
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
211: 	hook.Add("VendorItemModeUpdated", self, self.onVendorModeUpdated)
212: 
213: 	-- Name change.
```

#### 7. `hook.Add` lines `202-214`

```lua
202: 
203: 	-- Price change.
204: 	hook.Add("VendorItemPriceUpdated", self, self.onVendorPriceUpdated)
205: 
206: 	-- Item stock changes.
207: 	hook.Add("VendorItemStockUpdated", self, self.onItemStockUpdated)
208: 	hook.Add("VendorItemMaxStockUpdated", self, self.onItemStockUpdated)
209: 
210: 	-- Item mode change.
211: 	hook.Add("VendorItemModeUpdated", self, self.onVendorModeUpdated)
212: 
213: 	-- Name change.
214: 	hook.Add("VendorEdited", self, self.onVendorPropEdited)
```

#### 8. `nil` lines `114-126`

```lua
114: 	end
115: 
116: 	if (parent == self.vendor and mode == VENDOR_BUYONLY) then
117: 		return false
118: 	end
119: 
120: 	return mode ~= nil
121: end
122: 
123: function PANEL:updateItem(itemType, parent, quantity)
124: 	assert(isstring(itemType), "itemType must be a string")
125: 
126: 	if (not self.items[parent]) then return end
```

#### 9. `nutVendorExit` lines `229-241`

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

#### 10. `nutVendorTrade` lines `47-59`

```lua
47: 		self.editor:SizeToContents()
48: 		self.editor:SetPaintBackground(false)
49: 		self.leave.x = self.leave.x + 16 + self.leave:GetWide() * 0.5
50: 		self.editor.x = ScrW() * 0.5 - 16 - self.editor:GetWide()
51: 	end
52: 
53: 	self.vendor = self:Add("nutVendorTrader")
54: 	self.vendor:SetWide(math.max(ScrW() * 0.25, 220))
55: 	self.vendor:SetPos(
56: 		ScrW() * 0.5 - self.vendor:GetWide() - PADDING_HALF,
57: 		PADDING + self.leave:GetTall()
58: 	)
59: 	self.vendor:SetTall(ScrH() - self.vendor.y - PADDING)
```

#### 11. `nutVendorTrade` lines `57-69`

```lua
57: 		PADDING + self.leave:GetTall()
58: 	)
59: 	self.vendor:SetTall(ScrH() - self.vendor.y - PADDING)
60: 	self.vendor:setName(nutVendorEnt:getNetVar("name"))
61: 	self.vendor:setMoney(nutVendorEnt:getMoney())
62: 
63: 	self.me = self:Add("nutVendorTrader")
64: 	self.me:SetSize(self.vendor:GetSize())
65: 	self.me:SetPos(ScrW() * 0.5 + PADDING_HALF, self.vendor.y)
66: 	self.me:setName(L"you")
67: 	self.me:setMoney(LocalPlayer():getChar():getMoney())
68: 
69: 	self:listenForChanges()
```

#### 12. `nutVendorTrade` lines `75-87`

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

#### 13. `nutVendorTrade` lines `82-94`

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

#### 14. `onVendorPriceUpdated` lines `167-179`

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

#### 15. `onVendorPriceUpdated` lines `198-210`

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

#### 16. `updatePrice` lines `154-166`

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

#### 17. `updatePrice` lines `158-170`

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

#### 18. `updatePrice` lines `169-181`

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

#### 19. `updatePrice` lines `172-184`

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

## TV-004 — `plugins/vendor/entities/entities/nut_vendor/init.lua`

- Priority: `high`
- Hypothesis: Cleanup sync does not reach or refresh the active client UI
- Expected runtime relation: server vendor entity mutates/clears vendor item presentation metadata
- Found: `29`
- Missing: `1`

### Missing Patterns

- `invData`

### Found Evidence

#### 1. `OpenVendorTradeInterface` lines `51-63`

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

#### 2. `RemoveReceiverFromVendor` lines `284-296`

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

#### 3. `VendorItemSetData` lines `149-161`

```lua
149: function ENT:AddItemAndSetQty(inv, uniqueID, client)
150: 	inv:add(uniqueID, self.items[uniqueID].x, self.items[uniqueID].y, true)
151: 	:next(function(newItem)
152: 		if (newItem && !newItem.error && newItem.isStackable)
153: 		then
154: 			newItem:setQuantity(self.items[uniqueID].qty >= newItem.maxQuantity && newItem.maxQuantity || self.items[uniqueID].qty, client)
155: 			self:VendorItemSetData(newItem, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
156: 		end
157: 
158: 		return newItem
159: 	end)
160: end
161: 
```

#### 4. `VendorItemSetData` lines `171-183`

```lua
171: 				if (isStackable)
172: 				then
173: 					local item = inv:getFirstItemOfType(uniqueID)
174: 					if (item)
175: 					then
176: 						item:setQuantity(self.items[uniqueID].qty >= item.maxQuantity && item.maxQuantity || self.items[uniqueID].qty, client)
177: 						self:VendorItemSetData(item, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
178: 					else
179: 						self:AddItemAndSetQty(inv, uniqueID, client)
180: 					end
181: 				else
182: 					inv:add(uniqueID, self.items[uniqueID].x, self.items[uniqueID].y)
183: 					:next(function(newItem)
```

#### 5. `VendorItemSetData` lines `180-192`

```lua
180: 					end
181: 				else
182: 					inv:add(uniqueID, self.items[uniqueID].x, self.items[uniqueID].y)
183: 					:next(function(newItem)
184: 						if (newItem && !newItem.error)
185: 						then
186: 							self:VendorItemSetData(newItem, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
187: 						end
188: 				
189: 						return newItem
190: 					end)
191: 				end
192: 			end
```

#### 6. `VendorItemSetData` lines `199-211`

```lua
199: 					self:AddItemAndSetQty(inv, uniqueID, client)
200: 				else
201: 					local item = inv:getFirstItemOfType(uniqueID)
202: 					if (item)
203: 					then
204: 						item:setQuantity(self.items[uniqueID].qty >= item.maxQuantity && item.maxQuantity || self.items[uniqueID].qty, client)
205: 						self:VendorItemSetData(item, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
206: 					else
207: 						self:AddItemAndSetQty(inv, uniqueID, client)
208: 					end
209: 				end
210: 			end
211: 		end
```

#### 7. `VendorItemSetData` lines `209-221`

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

#### 8. `netstream.Start` lines `22-34`

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

#### 9. `netstream.Start` lines `25-37`

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

#### 10. `netstream.Start` lines `64-76`

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

#### 11. `netstream.Start` lines `114-126`

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

#### 12. `netstream.Start` lines `131-143`

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

#### 13. `nil` lines `233-245`

```lua
233: 
234: function ENT:RemoveItem(uniqueID, isBuy)
235: 	if (isBuy && self.items[uniqueID])
236: 	then
237: 		if (self.items[uniqueID].price)
238: 		then
239: 			self.items[uniqueID].maxQty = nil
240: 			self.items[uniqueID].buyPrice = nil
241: 		else
242: 			self.items[uniqueID] = nil
243: 		end
244: 	else
245: 		if (self.items[uniqueID].buyPrice)
```

#### 14. `nil` lines `234-246`

```lua
234: function ENT:RemoveItem(uniqueID, isBuy)
235: 	if (isBuy && self.items[uniqueID])
236: 	then
237: 		if (self.items[uniqueID].price)
238: 		then
239: 			self.items[uniqueID].maxQty = nil
240: 			self.items[uniqueID].buyPrice = nil
241: 		else
242: 			self.items[uniqueID] = nil
243: 		end
244: 	else
245: 		if (self.items[uniqueID].buyPrice)
246: 		then
```

#### 15. `nil` lines `236-248`

```lua
236: 	then
237: 		if (self.items[uniqueID].price)
238: 		then
239: 			self.items[uniqueID].maxQty = nil
240: 			self.items[uniqueID].buyPrice = nil
241: 		else
242: 			self.items[uniqueID] = nil
243: 		end
244: 	else
245: 		if (self.items[uniqueID].buyPrice)
246: 		then
247: 			self.items[uniqueID].initQty = nil
248: 			self.items[uniqueID].price = nil
```

#### 16. `nil` lines `241-253`

```lua
241: 		else
242: 			self.items[uniqueID] = nil
243: 		end
244: 	else
245: 		if (self.items[uniqueID].buyPrice)
246: 		then
247: 			self.items[uniqueID].initQty = nil
248: 			self.items[uniqueID].price = nil
249: 			self.items[uniqueID].x = nil
250: 			self.items[uniqueID].y = nil
251: 		else
252: 			self.items[uniqueID] = nil
253: 		end
```

#### 17. `nil` lines `242-254`

```lua
242: 			self.items[uniqueID] = nil
243: 		end
244: 	else
245: 		if (self.items[uniqueID].buyPrice)
246: 		then
247: 			self.items[uniqueID].initQty = nil
248: 			self.items[uniqueID].price = nil
249: 			self.items[uniqueID].x = nil
250: 			self.items[uniqueID].y = nil
251: 		else
252: 			self.items[uniqueID] = nil
253: 		end
254: 
```

#### 18. `setData` lines `149-161`

```lua
149: function ENT:AddItemAndSetQty(inv, uniqueID, client)
150: 	inv:add(uniqueID, self.items[uniqueID].x, self.items[uniqueID].y, true)
151: 	:next(function(newItem)
152: 		if (newItem && !newItem.error && newItem.isStackable)
153: 		then
154: 			newItem:setQuantity(self.items[uniqueID].qty >= newItem.maxQuantity && newItem.maxQuantity || self.items[uniqueID].qty, client)
155: 			self:VendorItemSetData(newItem, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
156: 		end
157: 
158: 		return newItem
159: 	end)
160: end
161: 
```

#### 19. `setData` lines `171-183`

```lua
171: 				if (isStackable)
172: 				then
173: 					local item = inv:getFirstItemOfType(uniqueID)
174: 					if (item)
175: 					then
176: 						item:setQuantity(self.items[uniqueID].qty >= item.maxQuantity && item.maxQuantity || self.items[uniqueID].qty, client)
177: 						self:VendorItemSetData(item, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
178: 					else
179: 						self:AddItemAndSetQty(inv, uniqueID, client)
180: 					end
181: 				else
182: 					inv:add(uniqueID, self.items[uniqueID].x, self.items[uniqueID].y)
183: 					:next(function(newItem)
```

#### 20. `setData` lines `180-192`

```lua
180: 					end
181: 				else
182: 					inv:add(uniqueID, self.items[uniqueID].x, self.items[uniqueID].y)
183: 					:next(function(newItem)
184: 						if (newItem && !newItem.error)
185: 						then
186: 							self:VendorItemSetData(newItem, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
187: 						end
188: 				
189: 						return newItem
190: 					end)
191: 				end
192: 			end
```

#### 21. `setData` lines `199-211`

```lua
199: 					self:AddItemAndSetQty(inv, uniqueID, client)
200: 				else
201: 					local item = inv:getFirstItemOfType(uniqueID)
202: 					if (item)
203: 					then
204: 						item:setQuantity(self.items[uniqueID].qty >= item.maxQuantity && item.maxQuantity || self.items[uniqueID].qty, client)
205: 						self:VendorItemSetData(item, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
206: 					else
207: 						self:AddItemAndSetQty(inv, uniqueID, client)
208: 					end
209: 				end
210: 			end
211: 		end
```

#### 22. `setData` lines `209-221`

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

#### 23. `vendorBPrice` lines `290-302`

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

#### 24. `vendorMQty` lines `212-224`

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

#### 25. `vendorMQty` lines `293-305`

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

#### 26. `vendorQty` lines `210-222`

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

#### 27. `vendorQty` lines `291-303`

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

#### 28. `vendorSPrice` lines `211-223`

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

#### 29. `vendorSPrice` lines `292-304`

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

## TV-009 — `gamemode/core/libs/item/sv_item.lua`

- Priority: `medium`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Expected runtime relation: server item data mutation persists and conditionally syncs item data
- Found: `0`
- Missing: `11`

### Missing Patterns

- `ITEM:setData`
- `client`
- `getOwner`
- `invData`
- `netstream.Start`
- `nut.db.updateTable`
- `owner`
- `receiver`
- `receivers`
- `setData`
- `setNetVar`

## TV-011 — `gamemode/core/meta/inventory/cl_base_inventory.lua`

- Priority: `medium`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Expected runtime relation: client inventory data delta receiver mutates local inventory/item data
- Found: `11`
- Missing: `8`

### Missing Patterns

- `ItemDataChanged`
- `client`
- `getOwner`
- `netstream.Hook`
- `owner`
- `receiver`
- `receivers`
- `setData`

### Found Evidence

#### 1. `data` lines `1-9`

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

#### 2. `data` lines `3-15`

```lua
3: net.Receive("nutInventoryData", function()
4: 	local id = net.ReadType()
5: 	local key = net.ReadString()
6: 	local value = net.ReadType()
7: 	local instance = nut.inventory.instances[id]
8: 	if (not instance) then
9: 		ErrorNoHalt("Got data "..key.." for non-existent instance "..id)
10: 		return
11: 	end
12: 
13: 	local oldValue = instance.data[key]
14: 	instance.data[key] = value
15: 	instance:onDataChanged(key, oldValue, value)
```

#### 3. `data` lines `7-19`

```lua
7: 	local instance = nut.inventory.instances[id]
8: 	if (not instance) then
9: 		ErrorNoHalt("Got data "..key.." for non-existent instance "..id)
10: 		return
11: 	end
12: 
13: 	local oldValue = instance.data[key]
14: 	instance.data[key] = value
15: 	instance:onDataChanged(key, oldValue, value)
16: 
17: 	hook.Run("InventoryDataChanged", instance, key, oldValue, value)
18: end)
19: 
```

#### 4. `data` lines `8-20`

```lua
8: 	if (not instance) then
9: 		ErrorNoHalt("Got data "..key.." for non-existent instance "..id)
10: 		return
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
```

#### 5. `data` lines `9-21`

```lua
9: 		ErrorNoHalt("Got data "..key.." for non-existent instance "..id)
10: 		return
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
```

#### 6. `net.Receive` lines `1-9`

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

#### 7. `net.Receive` lines `14-26`

```lua
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
24: 	local instance = nut.inventory.new(typeID)
25: 	instance.id = id
26: 	instance.data = data
```

#### 8. `net.Receive` lines `50-62`

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

#### 9. `net.Receive` lines `61-73`

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

#### 10. `net.Receive` lines `73-85`

```lua
73: 		inventory.items[itemID] = nil
74: 		item.invID = 0
75: 		hook.Run("InventoryItemRemoved", inventory, item)
76: 	end
77: end)
78: 
79: net.Receive("nutInventoryDelete", function()
80: 	local invID = net.ReadType()
81: 	local instance = nut.inventory.instances[invID]
82: 	if (instance) then
83: 		hook.Run("InventoryDeleted", instance)
84: 	end
85: 	if (invID) then
```

#### 11. `nutInventoryData` lines `1-9`

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

## TV-010 — `gamemode/core/meta/inventory/sv_base_inventory.lua`

- Priority: `medium`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Expected runtime relation: server inventory ownership/transfer/sync boundary
- Found: `18`
- Missing: `6`

### Missing Patterns

- `getOwner`
- `getReceivers`
- `netstream.Start`
- `owner`
- `receiver`
- `receivers`

### Found Evidence

#### 1. `addItem` lines `12-24`

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

#### 2. `addItem` lines `30-42`

```lua
30: 	-- Replicate adding the item to this inventory client-side
31: 	self:syncItemAdded(item)
32: 
33: 	return self
34: end
35: 
36: -- Sample implementation of Inventory:add - delegates to addItem
37: function Inventory:add(item)
38: 	return self:addItem(item)
39: end
40: 
41: function Inventory:syncItemAdded(item)
42: 	assert(istable(item) and item.getID, "cannot sync non-item")
```

#### 3. `addItem` lines `32-44`

```lua
32: 
33: 	return self
34: end
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
```

#### 4. `client` lines `24-36`

```lua
24: 		id = NULL
25: 	end
26: 	nut.db.updateTable({
27: 		_invID = id
28: 	}, nil, "items", "_itemID = "..item:getID())
29: 
30: 	-- Replicate adding the item to this inventory client-side
31: 	self:syncItemAdded(item)
32: 
33: 	return self
34: end
35: 
36: -- Sample implementation of Inventory:add - delegates to addItem
```

#### 5. `client` lines `163-175`

```lua
163: 
164: 	self:syncData(key)
165: 	self:onDataChanged(key, oldValue, value)
166: 	return self
167: end
168: 
169: -- Whether or not a client can interact with this inventory.
170: function Inventory:canAccess(action, context)
171: 	context = context or {}
172: 	local result
173: 	for _, rule in ipairs(self.config.accessRules) do
174: 		result, reason = rule(self, action, context)
175: 		if (result ~= nil) then
```

#### 6. `client` lines `195-207`

```lua
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
206: 	return recipients
207: end
```

#### 7. `client` lines `196-208`

```lua
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
206: 	return recipients
207: end
208: 
```

#### 8. `client` lines `197-209`

```lua
197: 
198: -- Returns a list of players who can interact with this inventory.
199: function Inventory:getRecipients()
200: 	local recipients = {}
201: 	for _, client in ipairs(player.GetAll()) do
202: 		if (self:canAccess(INV_REPLICATE, {client = client})) then
203: 			recipients[#recipients + 1] = client
204: 		end
205: 	end
206: 	return recipients
207: end
208: 
209: -- Called after this inventory has first been created and loaded.
```

#### 9. `invData` lines `1-13`

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

#### 10. `removeItem` lines `99-111`

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

#### 11. `removeItem` lines `128-140`

```lua
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
```

#### 12. `removeItem` lines `130-142`

```lua
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
141: 	local oldValue = self.data[key]
142: 	self.data[key] = value
```

#### 13. `setData` lines `134-146`

```lua
134: -- Sample implementation of Inventory:remove() - delegate to removeItem
135: function Inventory:remove(itemID)
136: 	return self:removeItem(itemID)
137: end
138: 
139: -- Stores arbitrary data that can later be looked up using the given key.
140: function Inventory:setData(key, value)
141: 	local oldValue = self.data[key]
142: 	self.data[key] = value
143: 
144: 	local keyData = self.config.data[key]
145: 	if (key == "char") then
146: 		-- Compatibility with NS1.1 inventory
```

#### 14. `sync` lines `25-37`

```lua
25: 	end
26: 	nut.db.updateTable({
27: 		_invID = id
28: 	}, nil, "items", "_itemID = "..item:getID())
29: 
30: 	-- Replicate adding the item to this inventory client-side
31: 	self:syncItemAdded(item)
32: 
33: 	return self
34: end
35: 
36: -- Sample implementation of Inventory:add - delegates to addItem
37: function Inventory:add(item)
```

#### 15. `sync` lines `35-47`

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

#### 16. `sync` lines `36-48`

```lua
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
```

#### 17. `sync` lines `42-54`

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

#### 18. `sync` lines `158-170`

```lua
158: 				{_invID = self.id, _key = key, _value = {value}},
159: 				INV_DATA_TABLE_NAME
160: 			)
161: 		end
162: 	end
163: 
164: 	self:syncData(key)
165: 	self:onDataChanged(key, oldValue, value)
166: 	return self
167: end
168: 
169: -- Whether or not a client can interact with this inventory.
170: function Inventory:canAccess(action, context)
```

## TV-007 — `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`

- Priority: `medium`
- Hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI
- Expected runtime relation: client grid inventory panel renders or refreshes item presentation metadata
- Found: `6`
- Missing: `8`

### Missing Patterns

- `CreateNewInventoryPanel`
- `SetUpPanel`
- `refresh`
- `update`
- `updatePrice`
- `vendorBPrice`
- `vendorSPrice`
- `vendor_grid_inventory`

### Found Evidence

#### 1. `ItemDataChanged` lines `270-282`

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

#### 2. `Paint` lines `8-20`

```lua
8: local BORDER_FIX_W = 8
9: local BORDER_FIX_H = 14
10: 
11: local SHADOW_COLOR = Color(0, 0, 0, 100)
12: 
13: function PANEL:Init()
14: 	self:SetPaintBackground(false)
15: 
16: 	self.icons = {}
17: 	self:setGridSize(1, 1)
18: 
19: 	self.occupied = {}
20: end
```

#### 3. `Paint` lines `287-299`

```lua
287: 		return
288: 	end
289: 
290: 	nut.item.heldPanel = self
291: end
292: 
293: function PANEL:Paint(w, h)
294: 	surface.SetDrawColor(0, 0, 0, 100)
295: 
296: 	local size = self.size
297: 	for y = 0, self.gridH - 1 do
298: 		for x = 0, self.gridW - 1 do
299: 			surface.DrawRect(
```

#### 4. `getData` lines `27-39`

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

#### 5. `getData` lines `108-120`

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

#### 6. `getData` lines `188-200`

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

## TV-006 — `plugins/inventory/cl_hooks.lua`

- Priority: `medium`
- Hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI
- Expected runtime relation: client inventory/vendor interface constructs player inventory and vendor_grid_inventory panels
- Found: `16`
- Missing: `2`

### Missing Patterns

- `getData`
- `updatePrice`

### Found Evidence

#### 1. `CreateNewInventoryPanel` lines `85-97`

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

#### 2. `CreateNewInventoryPanel` lines `101-113`

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

#### 3. `CreateNewInventoryPanel` lines `114-126`

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

#### 4. `CreateNewInventoryPanel` lines `125-137`

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

#### 5. `OnCreateStoragePanel` lines `160-172`

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

#### 6. `OnRemove` lines `143-155`

```lua
143: 	localParent:Center()
144: 	storageInvPanel:Center()
145: 	localParent.x = localParent.x + extraWidth
146: 	storageInvPanel:MoveLeftOf(localParent, PADDING)
147: 
148: 	local firstToRemove = true
149: 	localParent.oldOnRemove = localParent.OnRemove
150: 	storageInvPanel.oldOnRemove = storageInvPanel.OnRemove
151: 
152: 	local function exitStorageOnRemove(panel)
153: 		if (firstToRemove) then
154: 			firstToRemove = false
155: 			nutStorageBase:exitStorage()
```

#### 7. `OnRemove` lines `144-156`

```lua
144: 	storageInvPanel:Center()
145: 	localParent.x = localParent.x + extraWidth
146: 	storageInvPanel:MoveLeftOf(localParent, PADDING)
147: 
148: 	local firstToRemove = true
149: 	localParent.oldOnRemove = localParent.OnRemove
150: 	storageInvPanel.oldOnRemove = storageInvPanel.OnRemove
151: 
152: 	local function exitStorageOnRemove(panel)
153: 		if (firstToRemove) then
154: 			firstToRemove = false
155: 			nutStorageBase:exitStorage()
156: 			local otherPanel =
```

#### 8. `OnRemove` lines `146-158`

```lua
146: 	storageInvPanel:MoveLeftOf(localParent, PADDING)
147: 
148: 	local firstToRemove = true
149: 	localParent.oldOnRemove = localParent.OnRemove
150: 	storageInvPanel.oldOnRemove = storageInvPanel.OnRemove
151: 
152: 	local function exitStorageOnRemove(panel)
153: 		if (firstToRemove) then
154: 			firstToRemove = false
155: 			nutStorageBase:exitStorage()
156: 			local otherPanel =
157: 				panel == localParent and storageInvPanel or localParent
158: 			if (IsValid(otherPanel)) then otherPanel:Remove() end
```

#### 9. `OnRemove` lines `165-177`

```lua
165: 
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
168: 	localInvPanel.MainInvPanel.pair = storageInvPanel.mainInvPanel
169: 	storageInvPanel.mainInvPanel.pair = localInvPanel.MainInvPanel
170: 
171: 	localParent.OnRemove = exitStorageOnRemove
172: 	storageInvPanel.OnRemove = exitStorageOnRemove
173: end)
174: 
175: local function createTextEntry(frame, placeHolder, x, y, w, h)
176: 	local text = frame:Add("DTextEntry")
177: 	text:SetFont("nutWriteFont")
```

#### 10. `OnRemove` lines `166-178`

```lua
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
168: 	localInvPanel.MainInvPanel.pair = storageInvPanel.mainInvPanel
169: 	storageInvPanel.mainInvPanel.pair = localInvPanel.MainInvPanel
170: 
171: 	localParent.OnRemove = exitStorageOnRemove
172: 	storageInvPanel.OnRemove = exitStorageOnRemove
173: end)
174: 
175: local function createTextEntry(frame, placeHolder, x, y, w, h)
176: 	local text = frame:Add("DTextEntry")
177: 	text:SetFont("nutWriteFont")
178: 	text:SetPos(x, y)
```

#### 11. `SetUpPanel` lines `73-85`

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

#### 12. `SetUpPanel` lines `129-141`

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

#### 13. `removeReceiverFromVendor` lines `155-167`

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

#### 14. `vendorTradeInterface` lines `117-129`

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

#### 15. `vendorTradeInterface` lines `130-142`

```lua
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
142: 	local extraWidth = (storageInvPanel:GetWide() + PADDING) / 2
```

#### 16. `vendor_grid_inventory` lines `127-139`

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

## TV-005 — `plugins/vendor/derma/cl_vendor.lua`

- Priority: `medium`
- Hypothesis: Price update path refreshes vendor UI, but not necessarily player inventory UI
- Expected runtime relation: client vendor UI sends trade/exit and refreshes visible vendor price labels
- Found: `18`
- Missing: `3`

### Missing Patterns

- `CreateNewInventoryPanel`
- `getData`
- `vendor_grid_inventory`

### Found Evidence

#### 1. `OnRemove` lines `227-239`

```lua
227: 	nut.util.drawBlur(self, 10)
228: 
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
```

#### 2. `VendorItemPriceUpdated` lines `198-210`

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

#### 3. `hook.Add` lines `194-206`

```lua
194: 		self.me:setMoney(newValue)
195: 	end
196: end
197: 
198: function PANEL:listenForChanges()
199: 	-- Money changes.
200: 	hook.Add("VendorMoneyUpdated", self, self.onVendorMoneyUpdated)
201: 	hook.Add("OnCharVarChanged", self, self.onCharVarChanged)
202: 
203: 	-- Price change.
204: 	hook.Add("VendorItemPriceUpdated", self, self.onVendorPriceUpdated)
205: 
206: 	-- Item stock changes.
```

#### 4. `hook.Add` lines `195-207`

```lua
195: 	end
196: end
197: 
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
```

#### 5. `hook.Add` lines `198-210`

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

#### 6. `hook.Add` lines `201-213`

```lua
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
211: 	hook.Add("VendorItemModeUpdated", self, self.onVendorModeUpdated)
212: 
213: 	-- Name change.
```

#### 7. `hook.Add` lines `202-214`

```lua
202: 
203: 	-- Price change.
204: 	hook.Add("VendorItemPriceUpdated", self, self.onVendorPriceUpdated)
205: 
206: 	-- Item stock changes.
207: 	hook.Add("VendorItemStockUpdated", self, self.onItemStockUpdated)
208: 	hook.Add("VendorItemMaxStockUpdated", self, self.onItemStockUpdated)
209: 
210: 	-- Item mode change.
211: 	hook.Add("VendorItemModeUpdated", self, self.onVendorModeUpdated)
212: 
213: 	-- Name change.
214: 	hook.Add("VendorEdited", self, self.onVendorPropEdited)
```

#### 8. `nutVendorExit` lines `229-241`

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

#### 9. `nutVendorTrade` lines `47-59`

```lua
47: 		self.editor:SizeToContents()
48: 		self.editor:SetPaintBackground(false)
49: 		self.leave.x = self.leave.x + 16 + self.leave:GetWide() * 0.5
50: 		self.editor.x = ScrW() * 0.5 - 16 - self.editor:GetWide()
51: 	end
52: 
53: 	self.vendor = self:Add("nutVendorTrader")
54: 	self.vendor:SetWide(math.max(ScrW() * 0.25, 220))
55: 	self.vendor:SetPos(
56: 		ScrW() * 0.5 - self.vendor:GetWide() - PADDING_HALF,
57: 		PADDING + self.leave:GetTall()
58: 	)
59: 	self.vendor:SetTall(ScrH() - self.vendor.y - PADDING)
```

#### 10. `nutVendorTrade` lines `57-69`

```lua
57: 		PADDING + self.leave:GetTall()
58: 	)
59: 	self.vendor:SetTall(ScrH() - self.vendor.y - PADDING)
60: 	self.vendor:setName(nutVendorEnt:getNetVar("name"))
61: 	self.vendor:setMoney(nutVendorEnt:getMoney())
62: 
63: 	self.me = self:Add("nutVendorTrader")
64: 	self.me:SetSize(self.vendor:GetSize())
65: 	self.me:SetPos(ScrW() * 0.5 + PADDING_HALF, self.vendor.y)
66: 	self.me:setName(L"you")
67: 	self.me:setMoney(LocalPlayer():getChar():getMoney())
68: 
69: 	self:listenForChanges()
```

#### 11. `nutVendorTrade` lines `75-87`

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

#### 12. `nutVendorTrade` lines `82-94`

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

#### 13. `onVendorPriceUpdated` lines `167-179`

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

#### 14. `onVendorPriceUpdated` lines `198-210`

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

#### 15. `updatePrice` lines `154-166`

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

#### 16. `updatePrice` lines `158-170`

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

#### 17. `updatePrice` lines `169-181`

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

#### 18. `updatePrice` lines `172-184`

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

## TV-008 — `plugins/vendor/entities/entities/nut_vendor/init.lua`

- Priority: `medium`
- Hypothesis: Receiver ownership mismatch during item:setData cleanup
- Expected runtime relation: server vendor entity mutates/clears vendor item presentation metadata
- Found: `39`
- Missing: `2`

### Missing Patterns

- `getOwner`
- `owner`

### Found Evidence

#### 1. `OpenVendorTradeInterface` lines `51-63`

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

#### 2. `RemoveReceiverFromVendor` lines `284-296`

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

#### 3. `VendorItemSetData` lines `149-161`

```lua
149: function ENT:AddItemAndSetQty(inv, uniqueID, client)
150: 	inv:add(uniqueID, self.items[uniqueID].x, self.items[uniqueID].y, true)
151: 	:next(function(newItem)
152: 		if (newItem && !newItem.error && newItem.isStackable)
153: 		then
154: 			newItem:setQuantity(self.items[uniqueID].qty >= newItem.maxQuantity && newItem.maxQuantity || self.items[uniqueID].qty, client)
155: 			self:VendorItemSetData(newItem, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
156: 		end
157: 
158: 		return newItem
159: 	end)
160: end
161: 
```

#### 4. `VendorItemSetData` lines `171-183`

```lua
171: 				if (isStackable)
172: 				then
173: 					local item = inv:getFirstItemOfType(uniqueID)
174: 					if (item)
175: 					then
176: 						item:setQuantity(self.items[uniqueID].qty >= item.maxQuantity && item.maxQuantity || self.items[uniqueID].qty, client)
177: 						self:VendorItemSetData(item, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
178: 					else
179: 						self:AddItemAndSetQty(inv, uniqueID, client)
180: 					end
181: 				else
182: 					inv:add(uniqueID, self.items[uniqueID].x, self.items[uniqueID].y)
183: 					:next(function(newItem)
```

#### 5. `VendorItemSetData` lines `180-192`

```lua
180: 					end
181: 				else
182: 					inv:add(uniqueID, self.items[uniqueID].x, self.items[uniqueID].y)
183: 					:next(function(newItem)
184: 						if (newItem && !newItem.error)
185: 						then
186: 							self:VendorItemSetData(newItem, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
187: 						end
188: 				
189: 						return newItem
190: 					end)
191: 				end
192: 			end
```

#### 6. `VendorItemSetData` lines `199-211`

```lua
199: 					self:AddItemAndSetQty(inv, uniqueID, client)
200: 				else
201: 					local item = inv:getFirstItemOfType(uniqueID)
202: 					if (item)
203: 					then
204: 						item:setQuantity(self.items[uniqueID].qty >= item.maxQuantity && item.maxQuantity || self.items[uniqueID].qty, client)
205: 						self:VendorItemSetData(item, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
206: 					else
207: 						self:AddItemAndSetQty(inv, uniqueID, client)
208: 					end
209: 				end
210: 			end
211: 		end
```

#### 7. `VendorItemSetData` lines `209-221`

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

#### 8. `client` lines `3-15`

```lua
3: 
4: AddCSLuaFile("cl_init.lua")
5: AddCSLuaFile("shared.lua")
6: 
7: local PLUGIN = PLUGIN
8: 
9: function ENT:SpawnFunction(client, trace)
10: 	local angles = (trace.HitPos - client:GetPos()):Angle()
11: 	angles.r = 0
12: 	angles.p = 0
13: 	angles.y = angles.y + 180
14: 
15: 	local entity = ents.Create("nut_vendor")
```

#### 9. `client` lines `4-16`

```lua
4: AddCSLuaFile("cl_init.lua")
5: AddCSLuaFile("shared.lua")
6: 
7: local PLUGIN = PLUGIN
8: 
9: function ENT:SpawnFunction(client, trace)
10: 	local angles = (trace.HitPos - client:GetPos()):Angle()
11: 	angles.r = 0
12: 	angles.p = 0
13: 	angles.y = angles.y + 180
14: 
15: 	local entity = ents.Create("nut_vendor")
16: 	entity:SetPos(trace.HitPos)
```

#### 10. `client` lines `59-71`

```lua
59: 
60: function ENT:SetMoneyAmount(value)
61: 	if (!isnumber(value) || value < 0) then return end
62: 	self:SetMoney(value)
63: end
64: 
65: function ENT:HandleMoney(value, client)
66: 	if (!isnumber(value)) then return end
67: 	self:SetMoney(self:GetMoney() + value)
68: 
69: 	for k, v in pairs(self.receivers) do
70: 		netstream.Start(v, "setUpTargetMoney", self:GetMoney(), "vendorTradeInterface" .. self:EntIndex())
71: 	end
```

#### 11. `client` lines `82-94`

```lua
82: 	self:SetModel(model)
83: 	self:SetSkin(skin)
84: 	self:SetBodyGroups(bodygroups)
85: 	self:SetVendorBodyGroups(bodygroups)
86: end
87: 
88: function ENT:SetItemInStock(uniqueID, qty, price, x, y, client)
89: 	local numberQty = tonumber(qty || 1)
90: 	if (self.items[uniqueID])
91: 	then
92: 		self.items[uniqueID].initQty = numberQty
93: 		self.items[uniqueID].qty = numberQty
94: 		self.items[uniqueID].price = tonumber(price)
```

#### 12. `client` lines `111-123`

```lua
111: 		inv:removeItem(item.id, true)
112: 		:next(function()
113: 			return inv:add(item, x, y)
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
```

#### 13. `netstream.Start` lines `22-34`

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

#### 14. `netstream.Start` lines `25-37`

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

#### 15. `netstream.Start` lines `64-76`

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

#### 16. `netstream.Start` lines `114-126`

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

#### 17. `netstream.Start` lines `131-143`

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

#### 18. `receiver` lines `48-60`

```lua
48: 	if (!self.factions[factionID] && !activator:IsAdmin())
49: 	then
50: 		activator:notify("Торговец не хочет торговать с вами")
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
```

#### 19. `receiver` lines `63-75`

```lua
63: end
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
```

#### 20. `receiver` lines `261-273`

```lua
261: 	end
262: end
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
```

#### 21. `receiver` lines `264-276`

```lua
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
```

#### 22. `receiver` lines `284-296`

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

#### 23. `receivers` lines `48-60`

```lua
48: 	if (!self.factions[factionID] && !activator:IsAdmin())
49: 	then
50: 		activator:notify("Торговец не хочет торговать с вами")
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
```

#### 24. `receivers` lines `63-75`

```lua
63: end
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
```

#### 25. `receivers` lines `261-273`

```lua
261: 	end
262: end
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
```

#### 26. `receivers` lines `264-276`

```lua
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
```

#### 27. `receivers` lines `285-297`

```lua
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

#### 28. `setData` lines `149-161`

```lua
149: function ENT:AddItemAndSetQty(inv, uniqueID, client)
150: 	inv:add(uniqueID, self.items[uniqueID].x, self.items[uniqueID].y, true)
151: 	:next(function(newItem)
152: 		if (newItem && !newItem.error && newItem.isStackable)
153: 		then
154: 			newItem:setQuantity(self.items[uniqueID].qty >= newItem.maxQuantity && newItem.maxQuantity || self.items[uniqueID].qty, client)
155: 			self:VendorItemSetData(newItem, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
156: 		end
157: 
158: 		return newItem
159: 	end)
160: end
161: 
```

#### 29. `setData` lines `171-183`

```lua
171: 				if (isStackable)
172: 				then
173: 					local item = inv:getFirstItemOfType(uniqueID)
174: 					if (item)
175: 					then
176: 						item:setQuantity(self.items[uniqueID].qty >= item.maxQuantity && item.maxQuantity || self.items[uniqueID].qty, client)
177: 						self:VendorItemSetData(item, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
178: 					else
179: 						self:AddItemAndSetQty(inv, uniqueID, client)
180: 					end
181: 				else
182: 					inv:add(uniqueID, self.items[uniqueID].x, self.items[uniqueID].y)
183: 					:next(function(newItem)
```

#### 30. `setData` lines `180-192`

```lua
180: 					end
181: 				else
182: 					inv:add(uniqueID, self.items[uniqueID].x, self.items[uniqueID].y)
183: 					:next(function(newItem)
184: 						if (newItem && !newItem.error)
185: 						then
186: 							self:VendorItemSetData(newItem, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
187: 						end
188: 				
189: 						return newItem
190: 					end)
191: 				end
192: 			end
```

#### 31. `setData` lines `199-211`

```lua
199: 					self:AddItemAndSetQty(inv, uniqueID, client)
200: 				else
201: 					local item = inv:getFirstItemOfType(uniqueID)
202: 					if (item)
203: 					then
204: 						item:setQuantity(self.items[uniqueID].qty >= item.maxQuantity && item.maxQuantity || self.items[uniqueID].qty, client)
205: 						self:VendorItemSetData(item, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
206: 					else
207: 						self:AddItemAndSetQty(inv, uniqueID, client)
208: 					end
209: 				end
210: 			end
211: 		end
```

#### 32. `setData` lines `209-221`

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

#### 33. `vendorBPrice` lines `290-302`

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

#### 34. `vendorMQty` lines `212-224`

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

#### 35. `vendorMQty` lines `293-305`

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

#### 36. `vendorQty` lines `210-222`

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

#### 37. `vendorQty` lines `291-303`

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

#### 38. `vendorSPrice` lines `211-223`

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

#### 39. `vendorSPrice` lines `292-304`

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

## TV-015 — `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`

- Priority: `low`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Expected runtime relation: client grid inventory panel renders or refreshes item presentation metadata
- Found: `6`
- Missing: `5`

### Missing Patterns

- `SetUpPanel`
- `refresh`
- `update`
- `vendorBPrice`
- `vendorSPrice`

### Found Evidence

#### 1. `ItemDataChanged` lines `270-282`

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

#### 2. `Paint` lines `8-20`

```lua
8: local BORDER_FIX_W = 8
9: local BORDER_FIX_H = 14
10: 
11: local SHADOW_COLOR = Color(0, 0, 0, 100)
12: 
13: function PANEL:Init()
14: 	self:SetPaintBackground(false)
15: 
16: 	self.icons = {}
17: 	self:setGridSize(1, 1)
18: 
19: 	self.occupied = {}
20: end
```

#### 3. `Paint` lines `287-299`

```lua
287: 		return
288: 	end
289: 
290: 	nut.item.heldPanel = self
291: end
292: 
293: function PANEL:Paint(w, h)
294: 	surface.SetDrawColor(0, 0, 0, 100)
295: 
296: 	local size = self.size
297: 	for y = 0, self.gridH - 1 do
298: 		for x = 0, self.gridW - 1 do
299: 			surface.DrawRect(
```

#### 4. `getData` lines `27-39`

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

#### 5. `getData` lines `108-120`

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

#### 6. `getData` lines `188-200`

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

## TV-014 — `plugins/gridinv/plugins/gridstorage/sh_plugin.lua`

- Priority: `low`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Expected runtime relation: storage movement may reconstruct panels or force broader item sync
- Found: `2`
- Missing: `4`

### Missing Patterns

- `ItemDataChanged`
- `SetUpPanel`
- `refresh`
- `storageInventory`

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

## TV-013 — `plugins/inventory/cl_hooks.lua`

- Priority: `low`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Expected runtime relation: client inventory/vendor interface constructs player inventory and vendor_grid_inventory panels
- Found: `16`
- Missing: `0`

### Found Evidence

#### 1. `CreateNewInventoryPanel` lines `85-97`

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

#### 2. `CreateNewInventoryPanel` lines `101-113`

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

#### 3. `CreateNewInventoryPanel` lines `114-126`

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

#### 4. `CreateNewInventoryPanel` lines `125-137`

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

#### 5. `OnCreateStoragePanel` lines `160-172`

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

#### 6. `OnRemove` lines `143-155`

```lua
143: 	localParent:Center()
144: 	storageInvPanel:Center()
145: 	localParent.x = localParent.x + extraWidth
146: 	storageInvPanel:MoveLeftOf(localParent, PADDING)
147: 
148: 	local firstToRemove = true
149: 	localParent.oldOnRemove = localParent.OnRemove
150: 	storageInvPanel.oldOnRemove = storageInvPanel.OnRemove
151: 
152: 	local function exitStorageOnRemove(panel)
153: 		if (firstToRemove) then
154: 			firstToRemove = false
155: 			nutStorageBase:exitStorage()
```

#### 7. `OnRemove` lines `144-156`

```lua
144: 	storageInvPanel:Center()
145: 	localParent.x = localParent.x + extraWidth
146: 	storageInvPanel:MoveLeftOf(localParent, PADDING)
147: 
148: 	local firstToRemove = true
149: 	localParent.oldOnRemove = localParent.OnRemove
150: 	storageInvPanel.oldOnRemove = storageInvPanel.OnRemove
151: 
152: 	local function exitStorageOnRemove(panel)
153: 		if (firstToRemove) then
154: 			firstToRemove = false
155: 			nutStorageBase:exitStorage()
156: 			local otherPanel =
```

#### 8. `OnRemove` lines `146-158`

```lua
146: 	storageInvPanel:MoveLeftOf(localParent, PADDING)
147: 
148: 	local firstToRemove = true
149: 	localParent.oldOnRemove = localParent.OnRemove
150: 	storageInvPanel.oldOnRemove = storageInvPanel.OnRemove
151: 
152: 	local function exitStorageOnRemove(panel)
153: 		if (firstToRemove) then
154: 			firstToRemove = false
155: 			nutStorageBase:exitStorage()
156: 			local otherPanel =
157: 				panel == localParent and storageInvPanel or localParent
158: 			if (IsValid(otherPanel)) then otherPanel:Remove() end
```

#### 9. `OnRemove` lines `165-177`

```lua
165: 
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
168: 	localInvPanel.MainInvPanel.pair = storageInvPanel.mainInvPanel
169: 	storageInvPanel.mainInvPanel.pair = localInvPanel.MainInvPanel
170: 
171: 	localParent.OnRemove = exitStorageOnRemove
172: 	storageInvPanel.OnRemove = exitStorageOnRemove
173: end)
174: 
175: local function createTextEntry(frame, placeHolder, x, y, w, h)
176: 	local text = frame:Add("DTextEntry")
177: 	text:SetFont("nutWriteFont")
```

#### 10. `OnRemove` lines `166-178`

```lua
166: 	hook.Run("OnCreateStoragePanel", localInvPanel, storageInvPanel, storage)
167: 
168: 	localInvPanel.MainInvPanel.pair = storageInvPanel.mainInvPanel
169: 	storageInvPanel.mainInvPanel.pair = localInvPanel.MainInvPanel
170: 
171: 	localParent.OnRemove = exitStorageOnRemove
172: 	storageInvPanel.OnRemove = exitStorageOnRemove
173: end)
174: 
175: local function createTextEntry(frame, placeHolder, x, y, w, h)
176: 	local text = frame:Add("DTextEntry")
177: 	text:SetFont("nutWriteFont")
178: 	text:SetPos(x, y)
```

#### 11. `SetUpPanel` lines `73-85`

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

#### 12. `SetUpPanel` lines `129-141`

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

#### 13. `removeReceiverFromVendor` lines `155-167`

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

#### 14. `vendorTradeInterface` lines `117-129`

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

#### 15. `vendorTradeInterface` lines `130-142`

```lua
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
142: 	local extraWidth = (storageInvPanel:GetWide() + PADDING) / 2
```

#### 16. `vendor_grid_inventory` lines `127-139`

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

## TV-012 — `plugins/storage/cl_networking.lua`

- Priority: `low`
- Hypothesis: Storage movement forces broader panel reconstruction or item data refresh
- Expected runtime relation: storage movement may reconstruct panels or force broader item sync
- Found: `2`
- Missing: `5`

### Missing Patterns

- `ItemDataChanged`
- `OnCreateStoragePanel`
- `SetUpPanel`
- `refresh`
- `storageInventory`

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
