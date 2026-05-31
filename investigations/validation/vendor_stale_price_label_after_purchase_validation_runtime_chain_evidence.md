# SIGNALIS AI — Runtime Chain Evidence

- Source validation: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_source_validation.json`
- Evidence total: `107`
- Chains total: `5`
- Complete chains: `0`
- Partial chains: `5`
- Unclassified rate: `0.346`

## Summary

```json
{
  "evidence_total": 107,
  "chains_total": 5,
  "by_class": {
    "unclassified": 37,
    "player_inventory_panel_create": 7,
    "vendor_ui_price_listener": 5,
    "inventory_metadata_changed_event": 4,
    "vendor_metadata_creation_entry": 4,
    "inventory_membership_sync_entry": 4,
    "storage_panel_created_event": 3,
    "vendor_ui_price_update_handler": 3,
    "vendor_receiver_cleanup_entry": 3,
    "vendor_exit_metadata_cleanup": 3,
    "inventory_metadata_mutation_entry": 3,
    "inventory_metadata_receive": 2,
    "vendor_trade_interface_receive": 2,
    "vendor_remove_receiver_request": 2,
    "vendor_exit_request": 2,
    "vendor_trade_request": 2,
    "vendor_ui_price_refresh": 2,
    "vendor_open_event_emit": 2,
    "inventory_metadata_network_send": 2,
    "grid_panel_item_position_read": 2,
    "storage_open_receive": 2,
    "inventory_membership_receive_add": 1,
    "inventory_item_added_event": 1,
    "inventory_item_removed_event": 1,
    "inventory_membership_receive_remove": 1,
    "panel_bind_inventory": 1,
    "inventory_membership_add": 1,
    "inventory_membership_remove": 1,
    "inventory_recipient_resolution": 1,
    "grid_panel_item_metadata_listener": 1,
    "grid_panel_item_icon_create": 1,
    "storage_open_ui_handler": 1
  },
  "by_role": {
    "server_vendor_entity": 34,
    "server_inventory": 18,
    "client_inventory_hooks": 17,
    "vendor_trade_ui": 17,
    "client_inventory": 11,
    "client_grid_panel": 6,
    "grid_storage_ui": 2,
    "storage_client_networking": 2
  },
  "by_confidence": {
    "high": 53,
    "low": 37,
    "medium": 17
  },
  "complete_chains": 0,
  "partial_chains": 5,
  "unclassified": 37,
  "unclassified_rate": 0.346
}
```

## Runtime Chains

### CHAIN-001 — Vendor purchase transfer to item metadata cleanup

- Confidence: `partial`

Steps:

- server adds item to player inventory
- server enters inventory membership sync
- server resolves current inventory recipients
- client receives nutInventoryAdd
- client emits InventoryItemAdded

Missing steps:

- gridinv transfer identifies vendor → player purchase
- transfer crosses old inventory to player inventory boundary
- server sends full item state to recipients
- server sends nutInventoryAdd
- server clears vendor metadata on purchased item

Evidence:

#### E-0008 — `inventory_membership_receive_add`

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Lines: `50-62`
- Pattern: `net.Receive`

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

#### E-0009 — `inventory_item_added_event`

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Lines: `61-73`
- Pattern: `net.Receive`

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

#### E-0094 — `inventory_membership_add`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `12-24`
- Pattern: `addItem`

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

#### E-0095 — `inventory_membership_sync_entry`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `30-42`
- Pattern: `addItem`

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

#### E-0096 — `inventory_membership_sync_entry`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `32-44`
- Pattern: `addItem`

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

#### E-0108 — `inventory_membership_sync_entry`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `35-47`
- Pattern: `sync`

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

#### E-0109 — `inventory_membership_sync_entry`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `36-48`
- Pattern: `sync`

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

#### E-0110 — `inventory_recipient_resolution`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `42-54`
- Pattern: `sync`

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

Notes:

- This chain intentionally includes both inventory membership sync and item metadata cleanup.
- Inventory:setData is not ITEM:setData and must not satisfy item metadata mutation.

### CHAIN-002 — ITEM:setData to client item metadata refresh

- Confidence: `partial`

Steps:

- grid panel listens for item metadata change

Missing steps:

- server enters ITEM:setData
- server mutates item.data[key]
- server resolves owner/receiver fallback
- server sends invData item metadata delta
- server persists item metadata when noSave is false
- grid panel repopulates/rebuilds item icons

Evidence:

#### E-0112 — `grid_panel_item_metadata_listener`

- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Lines: `270-282`
- Pattern: `ItemDataChanged`

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

Notes:

- This chain is item metadata only.
- Inventory metadata evidence must not satisfy this chain.

### CHAIN-003 — Inventory metadata sync path

- Confidence: `partial`

Steps:

- server enters Inventory:setData
- server sends inventory metadata delta
- client receives nutInventoryData
- client emits InventoryDataChanged

Missing steps:

- server mutates inventory.data[key]

Evidence:

#### E-0001 — `inventory_metadata_receive`

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Lines: `1-9`
- Pattern: `data`

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

#### E-0002 — `inventory_metadata_receive`

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Lines: `3-15`
- Pattern: `data`

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

#### E-0003 — `inventory_metadata_changed_event`

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Lines: `7-19`
- Pattern: `data`

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

#### E-0004 — `inventory_metadata_changed_event`

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Lines: `8-20`
- Pattern: `data`

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

#### E-0005 — `inventory_metadata_changed_event`

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Lines: `9-21`
- Pattern: `data`

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

#### E-0007 — `inventory_metadata_changed_event`

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Lines: `14-26`
- Pattern: `net.Receive`

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

#### E-0098 — `inventory_metadata_network_send`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `163-175`
- Pattern: `client`

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

#### E-0104 — `inventory_metadata_mutation_entry`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `128-140`
- Pattern: `removeItem`

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

#### E-0105 — `inventory_metadata_mutation_entry`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `130-142`
- Pattern: `removeItem`

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

#### E-0106 — `inventory_metadata_mutation_entry`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `134-146`
- Pattern: `setData`

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

#### E-0111 — `inventory_metadata_network_send`

- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Lines: `158-170`
- Pattern: `sync`

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

Notes:

- This chain is separate from ITEM:setData / invData.
- Do not conflate InventoryDataChanged with ItemDataChanged.

### CHAIN-004 — Vendor UI open/close cleanup path

- Confidence: `partial`

Steps:

- server emits OpenVendorTradeInterface
- client receives vendorTradeInterface
- client creates player inventory panel
- client binds vendor inventory to vendor panel
- client requests removeReceiverFromVendor on close
- server enters RemoveReceiverFromVendor
- server clears vendor metadata from client inventory items

Missing steps:

- client creates vendor_grid_inventory

Evidence:

#### E-0014 — `player_inventory_panel_create`

- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Lines: `85-97`
- Pattern: `CreateNewInventoryPanel`

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

#### E-0015 — `player_inventory_panel_create`

- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Lines: `101-113`
- Pattern: `CreateNewInventoryPanel`

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

#### E-0016 — `vendor_trade_interface_receive`

- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Lines: `114-126`
- Pattern: `CreateNewInventoryPanel`

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

#### E-0017 — `player_inventory_panel_create`

- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Lines: `125-137`
- Pattern: `CreateNewInventoryPanel`

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

#### E-0018 — `vendor_remove_receiver_request`

- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Lines: `160-172`
- Pattern: `OnCreateStoragePanel`

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

#### E-0024 — `vendor_remove_receiver_request`

- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Lines: `155-167`
- Pattern: `RemoveReceiverFromVendor`

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

#### E-0025 — `panel_bind_inventory`

- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Lines: `73-85`
- Pattern: `SetUpPanel`

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

#### E-0026 — `player_inventory_panel_create`

- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Lines: `129-141`
- Pattern: `SetUpPanel`

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

#### E-0027 — `player_inventory_panel_create`

- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Lines: `99-111`
- Pattern: `nil`

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

#### E-0032 — `vendor_trade_interface_receive`

- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Lines: `117-129`
- Pattern: `vendorTradeInterface`

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

#### E-0033 — `player_inventory_panel_create`

- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Lines: `130-142`
- Pattern: `vendorTradeInterface`

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

#### E-0034 — `player_inventory_panel_create`

- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Lines: `127-139`
- Pattern: `vendor_grid_inventory`

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

#### E-0054 — `vendor_open_event_emit`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Lines: `51-63`
- Pattern: `OpenVendorTradeInterface`

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

#### E-0055 — `vendor_receiver_cleanup_entry`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Lines: `284-296`
- Pattern: `RemoveReceiverFromVendor`

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

#### E-0076 — `vendor_receiver_cleanup_entry`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Lines: `290-302`
- Pattern: `vendorBPrice`

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

#### E-0078 — `vendor_exit_metadata_cleanup`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Lines: `293-305`
- Pattern: `vendorMQty`

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

#### E-0080 — `vendor_exit_metadata_cleanup`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Lines: `291-303`
- Pattern: `vendorQty`

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

#### E-0082 — `vendor_exit_metadata_cleanup`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Lines: `292-304`
- Pattern: `vendorSPrice`

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

#### E-0169 — `vendor_open_event_emit`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Lines: `48-60`
- Pattern: `receiver`

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

#### E-0178 — `vendor_receiver_cleanup_entry`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Lines: `285-297`
- Pattern: `receivers`

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

Notes:

- This chain explains cleanup on vendor close.
- Purchase-transfer cleanup and RemoveReceiverFromVendor are separate cleanup paths.

### CHAIN-005 — Storage movement / panel reconstruction recovery path

- Confidence: `partial`

Steps:

- client receives nutStorageOpen
- client handles StorageOpen UI construction
- client emits OnCreateStoragePanel

Missing steps:

- client emits StorageOpen
- client binds inventory to storage/grid panel
- grid panel repopulates item icons

Evidence:

#### E-0022 — `storage_panel_created_event`

- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Lines: `165-177`
- Pattern: `OnRemove`

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

#### E-0023 — `storage_panel_created_event`

- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Lines: `166-178`
- Pattern: `OnRemove`

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

#### E-0197 — `storage_panel_created_event`

- File: `plugins/gridinv/plugins/gridstorage/sh_plugin.lua`
- Role: `grid_storage_ui`
- Lines: `207-219`
- Pattern: `OnCreateStoragePanel`

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

#### E-0198 — `storage_open_ui_handler`

- File: `plugins/gridinv/plugins/gridstorage/sh_plugin.lua`
- Role: `grid_storage_ui`
- Lines: `147-159`
- Pattern: `StorageOpen`

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

#### E-0215 — `storage_open_receive`

- File: `plugins/storage/cl_networking.lua`
- Role: `storage_client_networking`
- Lines: `1-12`
- Pattern: `StorageOpen`

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

#### E-0216 — `storage_open_receive`

- File: `plugins/storage/cl_networking.lua`
- Role: `storage_client_networking`
- Lines: `2-14`
- Pattern: `StorageOpen`

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

Notes:

- This chain explains why storage movement may clear stale presentation state.
- It does not prove server metadata was wrong.

## Classified Evidence Index

### E-0001 — `inventory_metadata_receive`

- Check: `TV-001`
- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Confidence: `high`
- Tags: `['client', 'inventory_metadata', 'network_receive']`
- Lines: `1-9`

### E-0002 — `inventory_metadata_receive`

- Check: `TV-001`
- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Confidence: `high`
- Tags: `['client', 'inventory_metadata', 'network_receive']`
- Lines: `3-15`

### E-0003 — `inventory_metadata_changed_event`

- Check: `TV-001`
- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Confidence: `high`
- Tags: `['client', 'hook_event', 'inventory_metadata']`
- Lines: `7-19`

### E-0004 — `inventory_metadata_changed_event`

- Check: `TV-001`
- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Confidence: `high`
- Tags: `['client', 'hook_event', 'inventory_metadata']`
- Lines: `8-20`

### E-0005 — `inventory_metadata_changed_event`

- Check: `TV-001`
- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Confidence: `high`
- Tags: `['client', 'hook_event', 'inventory_metadata']`
- Lines: `9-21`

### E-0007 — `inventory_metadata_changed_event`

- Check: `TV-001`
- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Confidence: `high`
- Tags: `['client', 'hook_event', 'inventory_metadata']`
- Lines: `14-26`

### E-0008 — `inventory_membership_receive_add`

- Check: `TV-001`
- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Confidence: `high`
- Tags: `['client', 'inventory_membership', 'network_receive']`
- Lines: `50-62`

### E-0009 — `inventory_item_added_event`

- Check: `TV-001`
- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Confidence: `high`
- Tags: `['client', 'hook_event', 'inventory_membership']`
- Lines: `61-73`

### E-0010 — `inventory_item_removed_event`

- Check: `TV-001`
- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Confidence: `high`
- Tags: `['client', 'hook_event', 'inventory_membership']`
- Lines: `73-85`

### E-0011 — `inventory_membership_receive_remove`

- Check: `TV-001`
- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Confidence: `high`
- Tags: `['client', 'inventory_membership', 'network_receive']`
- Lines: `67-79`

### E-0012 — `unclassified`

- Check: `TV-001`
- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Role: `client_inventory`
- Confidence: `low`
- Tags: `['client_inventory']`
- Lines: `80-92`

### E-0014 — `player_inventory_panel_create`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `high`
- Tags: `['client', 'player_inventory_panel', 'ui_construct']`
- Lines: `85-97`

### E-0015 — `player_inventory_panel_create`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `high`
- Tags: `['client', 'player_inventory_panel', 'ui_construct']`
- Lines: `101-113`

### E-0016 — `vendor_trade_interface_receive`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `high`
- Tags: `['client', 'network_receive', 'ui_construct']`
- Lines: `114-126`

### E-0017 — `player_inventory_panel_create`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `high`
- Tags: `['client', 'player_inventory_panel', 'ui_construct']`
- Lines: `125-137`

### E-0018 — `vendor_remove_receiver_request`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `high`
- Tags: `['client_to_server', 'network_send', 'vendor_cleanup']`
- Lines: `160-172`

### E-0019 — `unclassified`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `low`
- Tags: `['client_inventory_hooks']`
- Lines: `143-155`

### E-0020 — `unclassified`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `low`
- Tags: `['client_inventory_hooks']`
- Lines: `144-156`

### E-0021 — `unclassified`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `low`
- Tags: `['client_inventory_hooks']`
- Lines: `146-158`

### E-0022 — `storage_panel_created_event`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `medium`
- Tags: `['client', 'hook_event', 'ui_construct']`
- Lines: `165-177`

### E-0023 — `storage_panel_created_event`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `medium`
- Tags: `['client', 'hook_event', 'ui_construct']`
- Lines: `166-178`

### E-0024 — `vendor_remove_receiver_request`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `high`
- Tags: `['client_to_server', 'network_send', 'vendor_cleanup']`
- Lines: `155-167`

### E-0025 — `panel_bind_inventory`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `medium`
- Tags: `['client', 'inventory_binding', 'ui_construct']`
- Lines: `73-85`

### E-0026 — `player_inventory_panel_create`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `high`
- Tags: `['client', 'player_inventory_panel', 'ui_construct']`
- Lines: `129-141`

### E-0027 — `player_inventory_panel_create`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `high`
- Tags: `['client', 'player_inventory_panel', 'ui_construct']`
- Lines: `99-111`

### E-0032 — `vendor_trade_interface_receive`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `high`
- Tags: `['client', 'network_receive', 'ui_construct']`
- Lines: `117-129`

### E-0033 — `player_inventory_panel_create`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `high`
- Tags: `['client', 'player_inventory_panel', 'ui_construct']`
- Lines: `130-142`

### E-0034 — `player_inventory_panel_create`

- Check: `TV-003`
- File: `plugins/inventory/cl_hooks.lua`
- Role: `client_inventory_hooks`
- Confidence: `high`
- Tags: `['client', 'player_inventory_panel', 'ui_construct']`
- Lines: `127-139`

### E-0035 — `vendor_exit_request`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `high`
- Tags: `['client_to_server', 'network_send', 'vendor_cleanup']`
- Lines: `227-239`

### E-0036 — `vendor_ui_price_listener`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `medium`
- Tags: `['client', 'hook_listener', 'vendor_price']`
- Lines: `198-210`

### E-0037 — `vendor_ui_price_listener`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `medium`
- Tags: `['client', 'hook_listener', 'vendor_price']`
- Lines: `194-206`

### E-0038 — `vendor_ui_price_listener`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `medium`
- Tags: `['client', 'hook_listener', 'vendor_price']`
- Lines: `195-207`

### E-0040 — `vendor_ui_price_listener`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `medium`
- Tags: `['client', 'hook_listener', 'vendor_price']`
- Lines: `201-213`

### E-0041 — `vendor_ui_price_listener`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `medium`
- Tags: `['client', 'hook_listener', 'vendor_price']`
- Lines: `202-214`

### E-0042 — `unclassified`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `low`
- Tags: `['vendor_trade_ui']`
- Lines: `114-126`

### E-0043 — `vendor_exit_request`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `high`
- Tags: `['client_to_server', 'network_send', 'vendor_cleanup']`
- Lines: `229-241`

### E-0044 — `unclassified`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `low`
- Tags: `['vendor_trade_ui']`
- Lines: `47-59`

### E-0045 — `unclassified`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `low`
- Tags: `['vendor_trade_ui']`
- Lines: `57-69`

### E-0046 — `vendor_trade_request`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `high`
- Tags: `['client_to_server', 'network_send', 'vendor_trade']`
- Lines: `75-87`

### E-0047 — `vendor_trade_request`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `high`
- Tags: `['client_to_server', 'network_send', 'vendor_trade']`
- Lines: `82-94`

### E-0048 — `vendor_ui_price_update_handler`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `medium`
- Tags: `['client', 'ui_refresh', 'vendor_price']`
- Lines: `167-179`

### E-0050 — `vendor_ui_price_refresh`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `medium`
- Tags: `['client', 'ui_refresh', 'vendor_price']`
- Lines: `154-166`

### E-0051 — `vendor_ui_price_refresh`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `medium`
- Tags: `['client', 'ui_refresh', 'vendor_price']`
- Lines: `158-170`

### E-0052 — `vendor_ui_price_update_handler`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `medium`
- Tags: `['client', 'ui_refresh', 'vendor_price']`
- Lines: `169-181`

### E-0053 — `vendor_ui_price_update_handler`

- Check: `TV-002`
- File: `plugins/vendor/derma/cl_vendor.lua`
- Role: `vendor_trade_ui`
- Confidence: `medium`
- Tags: `['client', 'ui_refresh', 'vendor_price']`
- Lines: `172-184`

### E-0054 — `vendor_open_event_emit`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `high`
- Tags: `['hook_event', 'server', 'ui_open']`
- Lines: `51-63`

### E-0055 — `vendor_receiver_cleanup_entry`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `high`
- Tags: `['server', 'vendor_cleanup']`
- Lines: `284-296`

### E-0056 — `unclassified`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `149-161`

### E-0057 — `unclassified`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `171-183`

### E-0058 — `unclassified`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `180-192`

### E-0059 — `unclassified`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `199-211`

### E-0060 — `vendor_metadata_creation_entry`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `high`
- Tags: `['server', 'vendor_metadata']`
- Lines: `209-221`

### E-0061 — `unclassified`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `22-34`

### E-0062 — `unclassified`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `25-37`

### E-0063 — `unclassified`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `64-76`

### E-0064 — `unclassified`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `114-126`

### E-0065 — `unclassified`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `131-143`

### E-0066 — `unclassified`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `233-245`

### E-0067 — `unclassified`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `234-246`

### E-0068 — `unclassified`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `236-248`

### E-0069 — `unclassified`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `241-253`

### E-0070 — `unclassified`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `242-254`

### E-0076 — `vendor_receiver_cleanup_entry`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `high`
- Tags: `['server', 'vendor_cleanup']`
- Lines: `290-302`

### E-0077 — `vendor_metadata_creation_entry`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `high`
- Tags: `['server', 'vendor_metadata']`
- Lines: `212-224`

### E-0078 — `vendor_exit_metadata_cleanup`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `high`
- Tags: `['item_metadata', 'server', 'vendor_cleanup']`
- Lines: `293-305`

### E-0079 — `vendor_metadata_creation_entry`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `high`
- Tags: `['server', 'vendor_metadata']`
- Lines: `210-222`

### E-0080 — `vendor_exit_metadata_cleanup`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `high`
- Tags: `['item_metadata', 'server', 'vendor_cleanup']`
- Lines: `291-303`

### E-0081 — `vendor_metadata_creation_entry`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `high`
- Tags: `['server', 'vendor_metadata']`
- Lines: `211-223`

### E-0082 — `vendor_exit_metadata_cleanup`

- Check: `TV-004`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `high`
- Tags: `['item_metadata', 'server', 'vendor_cleanup']`
- Lines: `292-304`

### E-0094 — `inventory_membership_add`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `high`
- Tags: `['inventory_membership', 'server']`
- Lines: `12-24`

### E-0095 — `inventory_membership_sync_entry`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `high`
- Tags: `['inventory_membership', 'network_send', 'server']`
- Lines: `30-42`

### E-0096 — `inventory_membership_sync_entry`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `high`
- Tags: `['inventory_membership', 'network_send', 'server']`
- Lines: `32-44`

### E-0097 — `unclassified`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `low`
- Tags: `['server_inventory']`
- Lines: `24-36`

### E-0098 — `inventory_metadata_network_send`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `high`
- Tags: `['inventory_metadata', 'network_send', 'server_to_client']`
- Lines: `163-175`

### E-0099 — `unclassified`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `low`
- Tags: `['server_inventory']`
- Lines: `195-207`

### E-0100 — `unclassified`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `low`
- Tags: `['server_inventory']`
- Lines: `196-208`

### E-0101 — `unclassified`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `low`
- Tags: `['server_inventory']`
- Lines: `197-209`

### E-0102 — `unclassified`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `low`
- Tags: `['server_inventory']`
- Lines: `1-13`

### E-0103 — `inventory_membership_remove`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `high`
- Tags: `['inventory_membership', 'server']`
- Lines: `99-111`

### E-0104 — `inventory_metadata_mutation_entry`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `high`
- Tags: `['inventory_metadata', 'server']`
- Lines: `128-140`

### E-0105 — `inventory_metadata_mutation_entry`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `high`
- Tags: `['inventory_metadata', 'server']`
- Lines: `130-142`

### E-0106 — `inventory_metadata_mutation_entry`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `high`
- Tags: `['inventory_metadata', 'server']`
- Lines: `134-146`

### E-0107 — `unclassified`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `low`
- Tags: `['server_inventory']`
- Lines: `25-37`

### E-0108 — `inventory_membership_sync_entry`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `high`
- Tags: `['inventory_membership', 'network_send', 'server']`
- Lines: `35-47`

### E-0109 — `inventory_membership_sync_entry`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `high`
- Tags: `['inventory_membership', 'network_send', 'server']`
- Lines: `36-48`

### E-0110 — `inventory_recipient_resolution`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `high`
- Tags: `['inventory_membership', 'recipient_resolution', 'server']`
- Lines: `42-54`

### E-0111 — `inventory_metadata_network_send`

- Check: `TV-010`
- File: `gamemode/core/meta/inventory/sv_base_inventory.lua`
- Role: `server_inventory`
- Confidence: `high`
- Tags: `['inventory_metadata', 'network_send', 'server_to_client']`
- Lines: `158-170`

### E-0112 — `grid_panel_item_metadata_listener`

- Check: `TV-007`
- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Confidence: `high`
- Tags: `['client', 'item_metadata', 'ui_refresh']`
- Lines: `270-282`

### E-0113 — `unclassified`

- Check: `TV-007`
- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Confidence: `low`
- Tags: `['client_grid_panel']`
- Lines: `8-20`

### E-0114 — `unclassified`

- Check: `TV-007`
- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Confidence: `low`
- Tags: `['client_grid_panel']`
- Lines: `287-299`

### E-0115 — `grid_panel_item_position_read`

- Check: `TV-007`
- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Confidence: `medium`
- Tags: `['client', 'item_metadata', 'ui_render']`
- Lines: `27-39`

### E-0116 — `grid_panel_item_icon_create`

- Check: `TV-007`
- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Confidence: `medium`
- Tags: `['client', 'item_icon', 'ui_construct']`
- Lines: `108-120`

### E-0117 — `grid_panel_item_position_read`

- Check: `TV-007`
- File: `plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua`
- Role: `client_grid_panel`
- Confidence: `medium`
- Tags: `['client', 'item_metadata', 'ui_render']`
- Lines: `188-200`

### E-0159 — `unclassified`

- Check: `TV-008`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `3-15`

### E-0160 — `unclassified`

- Check: `TV-008`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `4-16`

### E-0161 — `unclassified`

- Check: `TV-008`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `59-71`

### E-0162 — `unclassified`

- Check: `TV-008`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `82-94`

### E-0163 — `unclassified`

- Check: `TV-008`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `111-123`

### E-0169 — `vendor_open_event_emit`

- Check: `TV-008`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `high`
- Tags: `['hook_event', 'server', 'ui_open']`
- Lines: `48-60`

### E-0170 — `unclassified`

- Check: `TV-008`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `63-75`

### E-0171 — `unclassified`

- Check: `TV-008`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `261-273`

### E-0172 — `unclassified`

- Check: `TV-008`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `low`
- Tags: `['server_vendor_entity']`
- Lines: `264-276`

### E-0178 — `vendor_receiver_cleanup_entry`

- Check: `TV-008`
- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Role: `server_vendor_entity`
- Confidence: `high`
- Tags: `['server', 'vendor_cleanup']`
- Lines: `285-297`

### E-0197 — `storage_panel_created_event`

- Check: `TV-014`
- File: `plugins/gridinv/plugins/gridstorage/sh_plugin.lua`
- Role: `grid_storage_ui`
- Confidence: `medium`
- Tags: `['client', 'hook_event', 'ui_construct']`
- Lines: `207-219`

### E-0198 — `storage_open_ui_handler`

- Check: `TV-014`
- File: `plugins/gridinv/plugins/gridstorage/sh_plugin.lua`
- Role: `grid_storage_ui`
- Confidence: `high`
- Tags: `['client', 'storage', 'ui_construct']`
- Lines: `147-159`

### E-0215 — `storage_open_receive`

- Check: `TV-012`
- File: `plugins/storage/cl_networking.lua`
- Role: `storage_client_networking`
- Confidence: `high`
- Tags: `['client', 'network_receive', 'storage']`
- Lines: `1-12`

### E-0216 — `storage_open_receive`

- Check: `TV-012`
- File: `plugins/storage/cl_networking.lua`
- Role: `storage_client_networking`
- Confidence: `high`
- Tags: `['client', 'network_receive', 'storage']`
- Lines: `2-14`
