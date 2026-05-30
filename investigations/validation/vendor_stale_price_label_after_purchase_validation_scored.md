# SIGNALIS AI — Scored Source Validation

- Source validation: `E:\signalis_ai\investigations\generated\vendor_stale_price_label_after_purchase.md`
- Query: `vendor stale price label after purchase`
- Total fragments: `137`
- Critical evidence: `50`
- Supporting evidence: `47`
- Noise evidence: `40`

## Interpretation

This is a ranking layer over exact source fragments.

Use `critical` first for investigation orchestration.
Use `supporting` for UI/sync context.
Use `noise` only when checking broad coverage.

## Critical Evidence

### 1. `plugins/vendor/derma/cl_vendor.lua` lines `194-210`

- Score: `154`
- Realm: `client`
- Match: `hook` / `VendorMoneyUpdated`
- Classification: `hook_listener_explicit`
- Reasons: critical classification: hook_listener_explicit, hook evidence, client-side evidence, Derma/UI file, important term: VendorItemPriceUpdated, important term: VendorItemStockUpdated, important term: VendorMoneyUpdated, explicit hook listener, price label/UI presentation evidence, query term overlap: price, vendor

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
  207: 	hook.Add("VendorItemStockUpdated", self, self.onItemStockUpdated)
  208: 	hook.Add("VendorItemMaxStockUpdated", self, self.onItemStockUpdated)
  209: 
  210: 	-- Item mode change.
```

### 2. `plugins/vendor/derma/cl_vendor.lua` lines `198-214`

- Score: `154`
- Realm: `client`
- Match: `hook` / `VendorItemPriceUpdated`
- Classification: `hook_listener_explicit`
- Reasons: critical classification: hook_listener_explicit, hook evidence, client-side evidence, Derma/UI file, important term: VendorItemPriceUpdated, important term: VendorItemStockUpdated, important term: VendorMoneyUpdated, explicit hook listener, price label/UI presentation evidence, query term overlap: price, vendor

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
  211: 	hook.Add("VendorItemModeUpdated", self, self.onVendorModeUpdated)
  212: 
  213: 	-- Name change.
  214: 	hook.Add("VendorEdited", self, self.onVendorPropEdited)
```

### 3. `plugins/inventory/cl_hooks.lua` lines `85-101`

- Score: `153`
- Realm: `client`
- Match: `hook` / `CreateNewInventoryPanel`
- Classification: `hook_listener_plugin_method`
- Reasons: critical classification: hook_listener_plugin_method, hook evidence, client-side evidence, inventory client UI hook file, important term: inventorySetPanelStatus, important term: CreateNewInventoryPanel, plugin/schema/gamemode hook listener, raw net operation, netstream operation

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
   98: 
   99: net.Receive(
  100: 	"OpenMyInv",
  101: 	function()
```

### 4. `plugins/vendor/cl_networking.lua` lines `44-60`

- Score: `149`
- Realm: `client`
- Match: `network` / `nutVendorExit`
- Classification: `network_receiver`
- Reasons: critical classification: network_receiver, network evidence, client-side evidence, client networking file, important term: VendorMoneyUpdated, important term: nutVendorExit, hook emitter call, raw net operation, query term overlap: vendor

```lua
   44: 	if (IsValid(vendor)) then
   45: 		nutVendorEnt = vendor
   46: 		hook.Run("VendorOpened", vendor)
   47: 	end
   48: end)
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
```

### 5. `plugins/vendor/derma/cl_vendor.lua` lines `201-217`

- Score: `142`
- Realm: `client`
- Match: `hook` / `VendorItemStockUpdated`
- Classification: `hook_listener_explicit`
- Reasons: critical classification: hook_listener_explicit, hook evidence, client-side evidence, Derma/UI file, important term: VendorItemPriceUpdated, important term: VendorItemStockUpdated, explicit hook listener, price label/UI presentation evidence, query term overlap: price, vendor

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
  214: 	hook.Add("VendorEdited", self, self.onVendorPropEdited)
  215: end
  216: 
  217: function PANEL:InventoryItemAdded(item)
```

### 6. `plugins/vendor/cl_networking.lua` lines `53-69`

- Score: `140`
- Realm: `client`
- Match: `hook` / `VendorMoneyUpdated`
- Classification: `hook_emitter`
- Reasons: critical classification: hook_emitter, hook evidence, client-side evidence, client networking file, important term: VendorMoneyUpdated, hook emitter call, price label/UI presentation evidence, query term overlap: price, vendor

```lua
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
   66: 
   67: 	vendor.items[itemType] = vendor.items[itemType] or {}
   68: 	vendor.items[itemType][VENDOR_PRICE] = value
   69: 
```

### 7. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `263-279`

- Score: `134`
- Realm: `unknown`
- Match: `network` / `nutVendorExit`
- Classification: `network_send_or_start`
- Reasons: critical classification: network_send_or_start, network evidence, vendor entity server init, important term: nutVendorExit, hook emitter call, raw net operation, query term overlap: vendor

```lua
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
```

### 8. `plugins/vendor/cl_networking.lua` lines `64-80`

- Score: `130`
- Realm: `client`
- Match: `hook` / `VendorItemPriceUpdated`
- Classification: `hook_emitter`
- Reasons: critical classification: hook_emitter, hook evidence, client-side evidence, client networking file, important term: VendorItemPriceUpdated, hook emitter call, query term overlap: price, vendor

```lua
   64: 	local value = net.ReadInt(32)
   65: 	if (value < 0) then value = nil end
   66: 
   67: 	vendor.items[itemType] = vendor.items[itemType] or {}
   68: 	vendor.items[itemType][VENDOR_PRICE] = value
   69: 
   70: 	hook.Run("VendorItemPriceUpdated", vendor, itemType, value)
   71: end)
   72: 
   73: addNetHandler("Mode", function(vendor)
   74: 	local itemType = net.ReadString()
   75: 	local value = net.ReadInt(8)
   76: 	if (value < 0) then value = nil end
   77: 
   78: 	vendor.items[itemType] = vendor.items[itemType] or {}
   79: 	vendor.items[itemType][VENDOR_MODE] = value
   80: 
```

### 9. `plugins/vendor/cl_networking.lua` lines `85-101`

- Score: `125`
- Realm: `client`
- Match: `hook` / `VendorItemStockUpdated`
- Classification: `hook_emitter`
- Reasons: critical classification: hook_emitter, hook evidence, client-side evidence, client networking file, important term: VendorItemStockUpdated, hook emitter call, query term overlap: vendor

```lua
   85: 	local itemType = net.ReadString()
   86: 	local value = net.ReadUInt(32)
   87: 
   88: 	vendor.items[itemType] = vendor.items[itemType] or {}
   89: 	vendor.items[itemType][VENDOR_STOCK] = value
   90: 
   91: 	hook.Run("VendorItemStockUpdated", vendor, itemType, value)
   92: end)
   93: 
   94: addNetHandler("MaxStock", function(vendor)
   95: 	local itemType = net.ReadString()
   96: 	local value = net.ReadUInt(32)
   97: 	if (value == 0) then value = nil end
   98: 
   99: 	vendor.items[itemType] = vendor.items[itemType] or {}
  100: 	vendor.items[itemType][VENDOR_MAXSTOCK] = value
  101: 
```

### 10. `gamemode/core/meta/inventory/cl_base_inventory.lua` lines `1-13`

- Score: `117`
- Realm: `client`
- Match: `network` / `nutInventoryData`
- Classification: `network_receiver`
- Reasons: critical classification: network_receiver, network evidence, client-side evidence, client base inventory sync file, important term: nutInventoryData, raw net operation

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
   10: 		return
   11: 	end
   12: 
   13: 	local oldValue = instance.data[key]
```

### 11. `plugins/vendor/derma/cl_vendor.lua` lines `75-91`

- Score: `115`
- Realm: `client`
- Match: `network` / `nutVendorTrade`
- Classification: `network_send_or_start`
- Reasons: critical classification: network_send_or_start, network evidence, client-side evidence, Derma/UI file, important term: nutVendorTrade, raw net operation, query term overlap: vendor

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
   88: 	net.Start("nutVendorTrade")
   89: 		net.WriteString(itemType)
   90: 		net.WriteBool(true)
   91: 	net.SendToServer()
```

### 12. `plugins/vendor/derma/cl_vendor.lua` lines `82-98`

- Score: `115`
- Realm: `client`
- Match: `network` / `nutVendorTrade`
- Classification: `network_send_or_start`
- Reasons: critical classification: network_send_or_start, network evidence, client-side evidence, Derma/UI file, important term: nutVendorTrade, raw net operation, query term overlap: vendor

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
   95: 	for itemType in SortedPairs(nutVendorEnt.items) do
   96: 		local mode = nutVendorEnt:getTradeMode(itemType)
   97: 		if (not mode) then continue end
   98: 
```

### 13. `plugins/vendor/derma/cl_vendor.lua` lines `229-245`

- Score: `115`
- Realm: `client`
- Match: `network` / `nutVendorExit`
- Classification: `network_send_or_start`
- Reasons: critical classification: network_send_or_start, network evidence, client-side evidence, Derma/UI file, important term: nutVendorExit, raw net operation, query term overlap: vendor

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
  242: 	end
  243: 
  244: 	if (IsValid(nut.gui.vendorFactionEditor)) then
  245: 		nut.gui.vendorFactionEditor:Remove()
```

### 14. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `209-225`

- Score: `113`
- Realm: `unknown`
- Match: `state` / `setData\s*\(`
- Classification: `item_data_mutation`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, item/inventory data access, price label/UI presentation evidence, query term overlap: price, vendor

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
  222: 	local vendorNeed = true
  223: 	if (self.items[uniqueID]
  224: 		&& self.items[uniqueID].maxQty
  225: 		&& self.items[uniqueID].maxQty > 0
```

### 15. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `210-226`

- Score: `113`
- Realm: `unknown`
- Match: `state` / `:SetData\s*\(`
- Classification: `item_data_mutation`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, item/inventory data access, price label/UI presentation evidence, query term overlap: price, vendor

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
  223: 	if (self.items[uniqueID]
  224: 		&& self.items[uniqueID].maxQty
  225: 		&& self.items[uniqueID].maxQty > 0
  226: 		&& (self.items[uniqueID].qty || 0 + qty) > self.items[uniqueID].maxQty)
```

### 16. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `210-226`

- Score: `113`
- Realm: `unknown`
- Match: `state` / `setData\s*\(`
- Classification: `item_data_mutation`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, item/inventory data access, price label/UI presentation evidence, query term overlap: price, vendor

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
  223: 	if (self.items[uniqueID]
  224: 		&& self.items[uniqueID].maxQty
  225: 		&& self.items[uniqueID].maxQty > 0
  226: 		&& (self.items[uniqueID].qty || 0 + qty) > self.items[uniqueID].maxQty)
```

### 17. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `211-227`

- Score: `113`
- Realm: `unknown`
- Match: `state` / `:SetData\s*\(`
- Classification: `item_data_mutation`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, item/inventory data access, price label/UI presentation evidence, query term overlap: price, vendor

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
  224: 		&& self.items[uniqueID].maxQty
  225: 		&& self.items[uniqueID].maxQty > 0
  226: 		&& (self.items[uniqueID].qty || 0 + qty) > self.items[uniqueID].maxQty)
  227: 	then
```

### 18. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `211-227`

- Score: `113`
- Realm: `unknown`
- Match: `state` / `setData\s*\(`
- Classification: `item_data_mutation`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, item/inventory data access, price label/UI presentation evidence, query term overlap: price, vendor

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
  224: 		&& self.items[uniqueID].maxQty
  225: 		&& self.items[uniqueID].maxQty > 0
  226: 		&& (self.items[uniqueID].qty || 0 + qty) > self.items[uniqueID].maxQty)
  227: 	then
```

### 19. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `212-228`

- Score: `113`
- Realm: `unknown`
- Match: `state` / `:SetData\s*\(`
- Classification: `item_data_mutation`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, item/inventory data access, price label/UI presentation evidence, query term overlap: price, vendor

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
  225: 		&& self.items[uniqueID].maxQty > 0
  226: 		&& (self.items[uniqueID].qty || 0 + qty) > self.items[uniqueID].maxQty)
  227: 	then
  228: 		vendorNeed = false
```

### 20. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `212-228`

- Score: `113`
- Realm: `unknown`
- Match: `state` / `setData\s*\(`
- Classification: `item_data_mutation`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, item/inventory data access, price label/UI presentation evidence, query term overlap: price, vendor

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
  225: 		&& self.items[uniqueID].maxQty > 0
  226: 		&& (self.items[uniqueID].qty || 0 + qty) > self.items[uniqueID].maxQty)
  227: 	then
  228: 		vendorNeed = false
```

### 21. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `290-306`

- Score: `103`
- Realm: `unknown`
- Match: `state` / `:SetData\s*\(`
- Classification: `item_data_mutation`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, item/inventory data access, query term overlap: price, vendor

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
  303: function ENT:ApplyVendorPos(pos1, pos2, pos3, ang1, ang2, ang3)
  304: 	self:SetFirstPos(Vector(pos1))
  305: 	self:SetSecPos(Vector(pos2))
  306: 	self:SetThdPos(Vector(pos3))
```

### 22. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `290-306`

- Score: `103`
- Realm: `unknown`
- Match: `state` / `setData\s*\(`
- Classification: `item_data_mutation`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, item/inventory data access, query term overlap: price, vendor

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
  303: function ENT:ApplyVendorPos(pos1, pos2, pos3, ang1, ang2, ang3)
  304: 	self:SetFirstPos(Vector(pos1))
  305: 	self:SetSecPos(Vector(pos2))
  306: 	self:SetThdPos(Vector(pos3))
```

### 23. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `291-307`

- Score: `103`
- Realm: `unknown`
- Match: `state` / `:SetData\s*\(`
- Classification: `item_data_mutation`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, item/inventory data access, query term overlap: price, vendor

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
  304: 	self:SetFirstPos(Vector(pos1))
  305: 	self:SetSecPos(Vector(pos2))
  306: 	self:SetThdPos(Vector(pos3))
  307: 	self:SetFirstAngle(Angle(ang1))
```

### 24. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `291-307`

- Score: `103`
- Realm: `unknown`
- Match: `state` / `setData\s*\(`
- Classification: `item_data_mutation`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, item/inventory data access, query term overlap: price, vendor

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
  304: 	self:SetFirstPos(Vector(pos1))
  305: 	self:SetSecPos(Vector(pos2))
  306: 	self:SetThdPos(Vector(pos3))
  307: 	self:SetFirstAngle(Angle(ang1))
```

### 25. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `292-308`

- Score: `103`
- Realm: `unknown`
- Match: `state` / `:SetData\s*\(`
- Classification: `item_data_mutation`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, item/inventory data access, query term overlap: price, vendor

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
  305: 	self:SetSecPos(Vector(pos2))
  306: 	self:SetThdPos(Vector(pos3))
  307: 	self:SetFirstAngle(Angle(ang1))
  308: 	self:SetSecAngle(Angle(ang2))
```

_Omitted 25 lower-ranked `critical` fragments._

## Supporting Evidence

### 1. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `117-133`

- Score: `67`
- Realm: `unknown`
- Match: `state` / `\bprice\b`
- Classification: `ui_presentation_logic`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, vendor entity server init, netstream operation, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
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
  127: 		self.items[uniqueID].buyPrice = tonumber(price)
  128: 		self.items[uniqueID].qty = self.items[uniqueID].qty || 0
  129: 	else
  130: 		self.items[uniqueID] = {
  131: 			maxQty = tonumber(qty) || 0,
  132: 			buyPrice = tonumber(price),
  133: 			qty = 0
```

### 2. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `121-137`

- Score: `67`
- Realm: `unknown`
- Match: `state` / `\bprice\b`
- Classification: `ui_presentation_logic`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, vendor entity server init, netstream operation, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
  121: end
  122: 
  123: function ENT:SetItemToBuy(uniqueID, qty, price)
  124: 	if (self.items[uniqueID])
  125: 	then
  126: 		self.items[uniqueID].maxQty = tonumber(qty) || 0
  127: 		self.items[uniqueID].buyPrice = tonumber(price)
  128: 		self.items[uniqueID].qty = self.items[uniqueID].qty || 0
  129: 	else
  130: 		self.items[uniqueID] = {
  131: 			maxQty = tonumber(qty) || 0,
  132: 			buyPrice = tonumber(price),
  133: 			qty = 0
  134: 		}
  135: 	end
  136: 
  137: 	netstream.Start(client, "sendVendorInfo", self:EntIndex(), self.factions, self.items)
```

### 3. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `126-142`

- Score: `67`
- Realm: `unknown`
- Match: `state` / `\bprice\b`
- Classification: `ui_presentation_logic`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, vendor entity server init, netstream operation, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
  126: 		self.items[uniqueID].maxQty = tonumber(qty) || 0
  127: 		self.items[uniqueID].buyPrice = tonumber(price)
  128: 		self.items[uniqueID].qty = self.items[uniqueID].qty || 0
  129: 	else
  130: 		self.items[uniqueID] = {
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
```

### 4. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `137-153`

- Score: `67`
- Realm: `unknown`
- Match: `state` / `\bprice\b`
- Classification: `ui_presentation_logic`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, vendor entity server init, netstream operation, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
  137: 	netstream.Start(client, "sendVendorInfo", self:EntIndex(), self.factions, self.items)
  138: end
  139: 
  140: function ENT:GetItemPrice(uniqueID, isSell, client)
  141: 	if (self.items[uniqueID])
  142: 	then
  143: 		return isSell && self.items[uniqueID].price || self.items[uniqueID].buyPrice
  144: 	end
  145: 
  146: 	client:notify("Нет цены для товара")
  147: end
  148: 
  149: function ENT:AddItemAndSetQty(inv, uniqueID, client)
  150: 	inv:add(uniqueID, self.items[uniqueID].x, self.items[uniqueID].y, true)
  151: 	:next(function(newItem)
  152: 		if (newItem && !newItem.error && newItem.isStackable)
  153: 		then
```

### 5. `plugins/inventory/cl_hooks.lua` lines `125-141`

- Score: `62`
- Realm: `client`
- Match: `hook` / `CreateNewInventoryPanel`
- Classification: `hook_reference`
- Reasons: low-signal classification: hook_reference, hook evidence, client-side evidence, inventory client UI hook file, important term: vendorTradeInterface, important term: CreateNewInventoryPanel, query term overlap: vendor

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
  138: 
  139: 	localParent:ShowCloseButton(true)
  140: 	storageInvPanel:ShowCloseButton(true)
  141: 
```

### 6. `plugins/vendor/derma/cl_vendor.lua` lines `54-70`

- Score: `60`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `networked_var_read`
- Reasons: supporting classification: networked_var_read, state/UI evidence, client-side evidence, Derma/UI file, important term: nutVendorTrade, important term: nutListenForInventoryChanges, generic keyword match, query term overlap: vendor

```lua
   54: 	self.vendor:SetWide(math.max(ScrW() * 0.25, 220))
   55: 	self.vendor:SetPos(
   56: 		ScrW() * 0.5 - self.vendor:GetWide() - PADDING_HALF,
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
   70: 	self:nutListenForInventoryChanges(LocalPlayer():getChar():getInv())
```

### 7. `plugins/vendor/cl_networking.lua` lines `15-31`

- Score: `58`
- Realm: `client`
- Match: `state` / `\bprice\b`
- Classification: `ui_presentation_logic`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, client-side evidence, client networking file, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
   15: 		vendor.money = nil
   16: 	end
   17: 
   18: 	local count = net.ReadUInt(16)
   19: 	for i = 1, count do
   20: 		local itemType = net.ReadString()
   21: 		local price = net.ReadInt(32)
   22: 		local stock = net.ReadInt(32)
   23: 		local maxStock = net.ReadInt(32)
   24: 		local mode = net.ReadInt(8)
   25: 
   26: 		if (price < 0) then price = nil end
   27: 		if (stock < 0) then stock = nil end
   28: 		if (maxStock <= 0) then maxStock = nil end
   29: 		if (mode < 0) then mode = nil end
   30: 
   31: 		vendor.items[itemType] = {
```

### 8. `plugins/vendor/cl_networking.lua` lines `20-36`

- Score: `58`
- Realm: `client`
- Match: `state` / `\bprice\b`
- Classification: `ui_presentation_logic`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, client-side evidence, client networking file, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
   20: 		local itemType = net.ReadString()
   21: 		local price = net.ReadInt(32)
   22: 		local stock = net.ReadInt(32)
   23: 		local maxStock = net.ReadInt(32)
   24: 		local mode = net.ReadInt(8)
   25: 
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
```

### 9. `plugins/inventory/cl_hooks.lua` lines `101-117`

- Score: `57`
- Realm: `client`
- Match: `hook` / `CreateNewInventoryPanel`
- Classification: `hook_reference`
- Reasons: low-signal classification: hook_reference, hook evidence, client-side evidence, inventory client UI hook file, important term: CreateNewInventoryPanel, netstream operation

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
  114: 	function()
  115: 		if (IsValid(currInvPanel))
  116: 		then
  117: 			return
```

### 10. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `82-98`

- Score: `55`
- Realm: `unknown`
- Match: `state` / `\bprice\b`
- Classification: `ui_presentation_logic`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, vendor entity server init, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

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
   95: 		self.items[uniqueID].x = tonumber(x)
   96: 		self.items[uniqueID].y = tonumber(y)
   97: 	else
   98: 		self.items[uniqueID] = {
```

### 11. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `88-104`

- Score: `55`
- Realm: `unknown`
- Match: `state` / `\bprice\b`
- Classification: `ui_presentation_logic`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, vendor entity server init, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
   88: function ENT:SetItemInStock(uniqueID, qty, price, x, y, client)
   89: 	local numberQty = tonumber(qty || 1)
   90: 	if (self.items[uniqueID])
   91: 	then
   92: 		self.items[uniqueID].initQty = numberQty
   93: 		self.items[uniqueID].qty = numberQty
   94: 		self.items[uniqueID].price = tonumber(price)
   95: 		self.items[uniqueID].x = tonumber(x)
   96: 		self.items[uniqueID].y = tonumber(y)
   97: 	else
   98: 		self.items[uniqueID] = {
   99: 			initQty = numberQty,
  100: 			qty = numberQty,
  101: 			price = tonumber(price),
  102: 			x = tonumber(x),
  103: 			y = tonumber(y)
  104: 		}
```

### 12. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `95-111`

- Score: `55`
- Realm: `unknown`
- Match: `state` / `\bprice\b`
- Classification: `ui_presentation_logic`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, vendor entity server init, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
   95: 		self.items[uniqueID].x = tonumber(x)
   96: 		self.items[uniqueID].y = tonumber(y)
   97: 	else
   98: 		self.items[uniqueID] = {
   99: 			initQty = numberQty,
  100: 			qty = numberQty,
  101: 			price = tonumber(price),
  102: 			x = tonumber(x),
  103: 			y = tonumber(y)
  104: 		}
  105: 	end
  106: 
  107: 	local inv = nut.inventory.instances[self.invId]
  108: 	local item = inv:getFirstItemOfType(uniqueID)
  109: 	if (item)
  110: 	then
  111: 		inv:removeItem(item.id, true)
```

### 13. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `189-205`

- Score: `55`
- Realm: `unknown`
- Match: `state` / `\bprice\b`
- Classification: `ui_presentation_logic`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, vendor entity server init, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
  189: 						return newItem
  190: 					end)
  191: 				end
  192: 			end
  193: 		else
  194: 			self.items[uniqueID].qty = self.items[uniqueID].qty + qty
  195: 			if (self.items[uniqueID].price)
  196: 			then
  197: 				if (self.items[uniqueID].qty == 0)
  198: 				then
  199: 					self:AddItemAndSetQty(inv, uniqueID, client)
  200: 				else
  201: 					local item = inv:getFirstItemOfType(uniqueID)
  202: 					if (item)
  203: 					then
  204: 						item:setQuantity(self.items[uniqueID].qty >= item.maxQuantity && item.maxQuantity || self.items[uniqueID].qty, client)
  205: 						self:VendorItemSetData(item, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
```

### 14. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `231-247`

- Score: `55`
- Realm: `unknown`
- Match: `state` / `\bprice\b`
- Classification: `ui_presentation_logic`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, vendor entity server init, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
  231: 	return self.items[uniqueID] && self.items[uniqueID].buyPrice && vendorNeed
  232: end
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
  246: 		then
  247: 			self.items[uniqueID].initQty = nil
```

### 15. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `242-258`

- Score: `55`
- Realm: `unknown`
- Match: `state` / `\bprice\b`
- Classification: `ui_presentation_logic`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, vendor entity server init, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

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
  255: 		local inv = nut.inventory.instances[self.invId]
  256: 		local item = inv:getFirstItemOfType(uniqueID)
  257: 		if (item)
  258: 		then
```

### 16. `plugins/vendor/cl_networking.lua` lines `52-68`

- Score: `50`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, important term: VendorMoneyUpdated, hook emitter call, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
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
   66: 
   67: 	vendor.items[itemType] = vendor.items[itemType] or {}
   68: 	vendor.items[itemType][VENDOR_PRICE] = value
```

### 17. `plugins/vendor/cl_networking.lua` lines `53-69`

- Score: `50`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, important term: VendorMoneyUpdated, hook emitter call, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
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
   66: 
   67: 	vendor.items[itemType] = vendor.items[itemType] or {}
   68: 	vendor.items[itemType][VENDOR_PRICE] = value
   69: 
```

### 18. `plugins/vendor/cl_networking.lua` lines `61-77`

- Score: `50`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, important term: VendorItemPriceUpdated, hook emitter call, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
   61: 
   62: addNetHandler("Price", function(vendor)
   63: 	local itemType = net.ReadString()
   64: 	local value = net.ReadInt(32)
   65: 	if (value < 0) then value = nil end
   66: 
   67: 	vendor.items[itemType] = vendor.items[itemType] or {}
   68: 	vendor.items[itemType][VENDOR_PRICE] = value
   69: 
   70: 	hook.Run("VendorItemPriceUpdated", vendor, itemType, value)
   71: end)
   72: 
   73: addNetHandler("Mode", function(vendor)
   74: 	local itemType = net.ReadString()
   75: 	local value = net.ReadInt(8)
   76: 	if (value < 0) then value = nil end
   77: 
```

### 19. `plugins/vendor/entities/entities/nut_vendor/shared.lua` lines `71-87`

- Score: `50`
- Realm: `shared/conditional`
- Match: `state` / `\bprice\b`
- Classification: `ui_presentation_logic`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, hook emitter call, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
   71: 					hook.Run("StorageRestored", self, inventory)
   72: 					inventory.vendor = self
   73: 
   74: 					if (next(self.items))
   75: 					then
   76: 						for k, v in pairs(self.items) do
   77: 							if (v.price)
   78: 							then
   79: 								v.qty = v.initQty
   80: 								local item = inventory:getFirstItemOfType(k)
   81: 								if (item && item.isStackable)
   82: 								then
   83: 									item:setQuantity(item.maxQuantity, nil)
   84: 								elseif (!item)
   85: 								then
   86: 									inventory:add(k, v.x, v.y)
   87: 									:next(function(newItem)
```

### 20. `plugins/vendor/cl_networking.lua` lines `37-53`

- Score: `47`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, important term: nutVendorExit, hook emitter call, raw net operation, generic keyword match, query term overlap: vendor

```lua
   37: 	end
   38: 
   39: 	hook.Run("VendorSynchronized", vendor)
   40: end)
   41: 
   42: net.Receive("nutVendorOpen", function()
   43: 	local vendor = net.ReadEntity()
   44: 	if (IsValid(vendor)) then
   45: 		nutVendorEnt = vendor
   46: 		hook.Run("VendorOpened", vendor)
   47: 	end
   48: end)
   49: 
   50: net.Receive("nutVendorExit", function()
   51: 	nutVendorEnt = nil
   52: 	hook.Run("VendorExited")
   53: end)
```

### 21. `plugins/vendor/cl_networking.lua` lines `38-54`

- Score: `47`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, important term: nutVendorExit, hook emitter call, raw net operation, generic keyword match, query term overlap: vendor

```lua
   38: 
   39: 	hook.Run("VendorSynchronized", vendor)
   40: end)
   41: 
   42: net.Receive("nutVendorOpen", function()
   43: 	local vendor = net.ReadEntity()
   44: 	if (IsValid(vendor)) then
   45: 		nutVendorEnt = vendor
   46: 		hook.Run("VendorOpened", vendor)
   47: 	end
   48: end)
   49: 
   50: net.Receive("nutVendorExit", function()
   51: 	nutVendorEnt = nil
   52: 	hook.Run("VendorExited")
   53: end)
   54: 
```

### 22. `plugins/vendor/cl_networking.lua` lines `39-55`

- Score: `47`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, important term: nutVendorExit, hook emitter call, raw net operation, generic keyword match, query term overlap: vendor

```lua
   39: 	hook.Run("VendorSynchronized", vendor)
   40: end)
   41: 
   42: net.Receive("nutVendorOpen", function()
   43: 	local vendor = net.ReadEntity()
   44: 	if (IsValid(vendor)) then
   45: 		nutVendorEnt = vendor
   46: 		hook.Run("VendorOpened", vendor)
   47: 	end
   48: end)
   49: 
   50: net.Receive("nutVendorExit", function()
   51: 	nutVendorEnt = nil
   52: 	hook.Run("VendorExited")
   53: end)
   54: 
   55: addNetHandler("Money", function(vendor)
```

### 23. `plugins/vendor/cl_networking.lua` lines `40-56`

- Score: `47`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, important term: nutVendorExit, hook emitter call, raw net operation, generic keyword match, query term overlap: vendor

```lua
   40: end)
   41: 
   42: net.Receive("nutVendorOpen", function()
   43: 	local vendor = net.ReadEntity()
   44: 	if (IsValid(vendor)) then
   45: 		nutVendorEnt = vendor
   46: 		hook.Run("VendorOpened", vendor)
   47: 	end
   48: end)
   49: 
   50: net.Receive("nutVendorExit", function()
   51: 	nutVendorEnt = nil
   52: 	hook.Run("VendorExited")
   53: end)
   54: 
   55: addNetHandler("Money", function(vendor)
   56: 	local money = net.ReadInt(32)
```

### 24. `plugins/inventory/cl_hooks.lua` lines `155-171`

- Score: `47`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, inventory client UI hook file, important term: inventorySetPanelStatus, hook emitter call, netstream operation, generic keyword match, query term overlap: vendor

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
  168: 	localInvPanel.MainInvPanel.pair = storageInvPanel.mainInvPanel
  169: 	storageInvPanel.mainInvPanel.pair = localInvPanel.MainInvPanel
  170: 
  171: 	localParent.OnRemove = exitStorageOnRemove
```

### 25. `plugins/inventory/cl_hooks.lua` lines `117-133`

- Score: `44`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, inventory client UI hook file, important term: vendorTradeInterface, important term: CreateNewInventoryPanel, netstream operation, generic keyword match, query term overlap: vendor

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
  130: 
  131: 	local localInvPanel = PLUGIN:CreateNewInventoryPanel(LocalPlayer(), nil)
  132: 	local localParent = localInvPanel:GetParent()
  133: 	local storageInvPanel = vgui.Create("vendor_grid_inventory")
```

_Omitted 22 lower-ranked `supporting` fragments._

## Noise Evidence

### 1. `plugins/inventory/cl_hooks.lua` lines `128-144`

- Score: `32`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, inventory client UI hook file, important term: vendorTradeInterface, important term: CreateNewInventoryPanel, generic keyword match, query term overlap: vendor

```lua
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
  140: 	storageInvPanel:ShowCloseButton(true)
  141: 
  142: 	local extraWidth = (storageInvPanel:GetWide() + PADDING) / 2
  143: 	localParent:Center()
  144: 	storageInvPanel:Center()
```

### 2. `plugins/inventory/cl_hooks.lua` lines `130-146`

- Score: `32`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, inventory client UI hook file, important term: vendorTradeInterface, important term: CreateNewInventoryPanel, generic keyword match, query term overlap: vendor

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
  143: 	localParent:Center()
  144: 	storageInvPanel:Center()
  145: 	localParent.x = localParent.x + extraWidth
  146: 	storageInvPanel:MoveLeftOf(localParent, PADDING)
```

### 3. `plugins/inventory/cl_hooks.lua` lines `131-147`

- Score: `32`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, inventory client UI hook file, important term: vendorTradeInterface, important term: CreateNewInventoryPanel, generic keyword match, query term overlap: vendor

```lua
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
  143: 	localParent:Center()
  144: 	storageInvPanel:Center()
  145: 	localParent.x = localParent.x + extraWidth
  146: 	storageInvPanel:MoveLeftOf(localParent, PADDING)
  147: 
```

### 4. `plugins/vendor/derma/cl_vendor.lua` lines `148-164`

- Score: `28`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, important term: updatePrice, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
  148: 
  149: 	panel:setQuantity(quantity)
  150: 
  151: 	return panel
  152: end
  153: 
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
```

### 5. `plugins/vendor/derma/cl_vendor.lua` lines `150-166`

- Score: `28`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, important term: updatePrice, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
  150: 
  151: 	return panel
  152: end
  153: 
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

### 6. `plugins/vendor/derma/cl_vendor.lua` lines `152-168`

- Score: `28`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, important term: updatePrice, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
  152: end
  153: 
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
  167: end
  168: 
```

### 7. `plugins/vendor/derma/cl_vendor.lua` lines `175-191`

- Score: `28`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, important term: updatePrice, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
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
  185: 
  186: function PANEL:onItemStockUpdated(vendor, itemType)
  187: 	self:updateItem(itemType, self.vendor)
  188: end
  189: 
  190: function PANEL:onCharVarChanged(character, key, oldValue, newValue)
  191: 	if (character ~= LocalPlayer():getChar()) then return end
```

### 8. `plugins/vendor/derma/cl_vendor.lua` lines `176-192`

- Score: `28`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, important term: updatePrice, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
  176: 
  177: 	panel = self.items[self.me][itemType]
  178: 	if (IsValid(panel)) then panel:updatePrice() end
  179: end
  180: 
  181: function PANEL:onVendorModeUpdated(vendor, itemType, mode)
  182: 	self:updateItem(itemType, self.vendor)
  183: 	self:updateItem(itemType, self.me)
  184: end
  185: 
  186: function PANEL:onItemStockUpdated(vendor, itemType)
  187: 	self:updateItem(itemType, self.vendor)
  188: end
  189: 
  190: function PANEL:onCharVarChanged(character, key, oldValue, newValue)
  191: 	if (character ~= LocalPlayer():getChar()) then return end
  192: 
```

### 9. `plugins/vendor/derma/cl_vendor.lua` lines `55-71`

- Score: `25`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, important term: nutVendorTrade, important term: nutListenForInventoryChanges, generic keyword match, query term overlap: vendor

```lua
   55: 	self.vendor:SetPos(
   56: 		ScrW() * 0.5 - self.vendor:GetWide() - PADDING_HALF,
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
   70: 	self:nutListenForInventoryChanges(LocalPlayer():getChar():getInv())
   71: 
```

### 10. `plugins/vendor/derma/cl_vendor.lua` lines `58-74`

- Score: `25`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, important term: nutVendorTrade, important term: nutListenForInventoryChanges, generic keyword match, query term overlap: vendor

```lua
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
   70: 	self:nutListenForInventoryChanges(LocalPlayer():getChar():getInv())
   71: 
   72: 	self.items = {
   73: 		[self.vendor] = {},
   74: 		[self.me] = {}
```

### 11. `plugins/vendor/derma/cl_vendor.lua` lines `59-75`

- Score: `25`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, important term: nutVendorTrade, important term: nutListenForInventoryChanges, generic keyword match, query term overlap: vendor

```lua
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
   70: 	self:nutListenForInventoryChanges(LocalPlayer():getChar():getInv())
   71: 
   72: 	self.items = {
   73: 		[self.vendor] = {},
   74: 		[self.me] = {}
   75: 	}
```

### 12. `plugins/vendor/cl_networking.lua` lines `72-88`

- Score: `23`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, hook emitter call, generic keyword match, query term overlap: vendor

```lua
   72: 
   73: addNetHandler("Mode", function(vendor)
   74: 	local itemType = net.ReadString()
   75: 	local value = net.ReadInt(8)
   76: 	if (value < 0) then value = nil end
   77: 
   78: 	vendor.items[itemType] = vendor.items[itemType] or {}
   79: 	vendor.items[itemType][VENDOR_MODE] = value
   80: 
   81: 	hook.Run("VendorItemModeUpdated", vendor, itemType, value)
   82: end)
   83: 
   84: addNetHandler("Stock", function(vendor)
   85: 	local itemType = net.ReadString()
   86: 	local value = net.ReadUInt(32)
   87: 
   88: 	vendor.items[itemType] = vendor.items[itemType] or {}
```

### 13. `plugins/vendor/cl_networking.lua` lines `73-89`

- Score: `23`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, hook emitter call, generic keyword match, query term overlap: vendor

```lua
   73: addNetHandler("Mode", function(vendor)
   74: 	local itemType = net.ReadString()
   75: 	local value = net.ReadInt(8)
   76: 	if (value < 0) then value = nil end
   77: 
   78: 	vendor.items[itemType] = vendor.items[itemType] or {}
   79: 	vendor.items[itemType][VENDOR_MODE] = value
   80: 
   81: 	hook.Run("VendorItemModeUpdated", vendor, itemType, value)
   82: end)
   83: 
   84: addNetHandler("Stock", function(vendor)
   85: 	local itemType = net.ReadString()
   86: 	local value = net.ReadUInt(32)
   87: 
   88: 	vendor.items[itemType] = vendor.items[itemType] or {}
   89: 	vendor.items[itemType][VENDOR_STOCK] = value
```

### 14. `plugins/vendor/cl_networking.lua` lines `93-109`

- Score: `23`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, hook emitter call, generic keyword match, query term overlap: vendor

```lua
   93: 
   94: addNetHandler("MaxStock", function(vendor)
   95: 	local itemType = net.ReadString()
   96: 	local value = net.ReadUInt(32)
   97: 	if (value == 0) then value = nil end
   98: 
   99: 	vendor.items[itemType] = vendor.items[itemType] or {}
  100: 	vendor.items[itemType][VENDOR_MAXSTOCK] = value
  101: 
  102: 	hook.Run("VendorItemMaxStockUpdated", vendor, itemType, value)
  103: end)
  104: 
  105: addNetHandler("AllowFaction", function(vendor)
  106: 	local id = net.ReadUInt(8)
  107: 	local allowed = net.ReadBool()
  108: 
  109: 	if (allowed) then
```

### 15. `plugins/vendor/cl_networking.lua` lines `94-110`

- Score: `23`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, hook emitter call, generic keyword match, query term overlap: vendor

```lua
   94: addNetHandler("MaxStock", function(vendor)
   95: 	local itemType = net.ReadString()
   96: 	local value = net.ReadUInt(32)
   97: 	if (value == 0) then value = nil end
   98: 
   99: 	vendor.items[itemType] = vendor.items[itemType] or {}
  100: 	vendor.items[itemType][VENDOR_MAXSTOCK] = value
  101: 
  102: 	hook.Run("VendorItemMaxStockUpdated", vendor, itemType, value)
  103: end)
  104: 
  105: addNetHandler("AllowFaction", function(vendor)
  106: 	local id = net.ReadUInt(8)
  107: 	local allowed = net.ReadBool()
  108: 
  109: 	if (allowed) then
  110: 		vendor.factions[id] = true
```

### 16. `plugins/vendor/cl_networking.lua` lines `96-112`

- Score: `23`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, hook emitter call, generic keyword match, query term overlap: vendor

```lua
   96: 	local value = net.ReadUInt(32)
   97: 	if (value == 0) then value = nil end
   98: 
   99: 	vendor.items[itemType] = vendor.items[itemType] or {}
  100: 	vendor.items[itemType][VENDOR_MAXSTOCK] = value
  101: 
  102: 	hook.Run("VendorItemMaxStockUpdated", vendor, itemType, value)
  103: end)
  104: 
  105: addNetHandler("AllowFaction", function(vendor)
  106: 	local id = net.ReadUInt(8)
  107: 	local allowed = net.ReadBool()
  108: 
  109: 	if (allowed) then
  110: 		vendor.factions[id] = true
  111: 	else
  112: 		vendor.factions[id] = nil
```

### 17. `plugins/vendor/cl_networking.lua` lines `99-115`

- Score: `23`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, hook emitter call, generic keyword match, query term overlap: vendor

```lua
   99: 	vendor.items[itemType] = vendor.items[itemType] or {}
  100: 	vendor.items[itemType][VENDOR_MAXSTOCK] = value
  101: 
  102: 	hook.Run("VendorItemMaxStockUpdated", vendor, itemType, value)
  103: end)
  104: 
  105: addNetHandler("AllowFaction", function(vendor)
  106: 	local id = net.ReadUInt(8)
  107: 	local allowed = net.ReadBool()
  108: 
  109: 	if (allowed) then
  110: 		vendor.factions[id] = true
  111: 	else
  112: 		vendor.factions[id] = nil
  113: 	end
  114: 
  115: 	hook.Run("VendorFactionUpdated", vendor, id, allowed)
```

### 18. `plugins/vendor/cl_networking.lua` lines `104-120`

- Score: `23`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, hook emitter call, generic keyword match, query term overlap: vendor

```lua
  104: 
  105: addNetHandler("AllowFaction", function(vendor)
  106: 	local id = net.ReadUInt(8)
  107: 	local allowed = net.ReadBool()
  108: 
  109: 	if (allowed) then
  110: 		vendor.factions[id] = true
  111: 	else
  112: 		vendor.factions[id] = nil
  113: 	end
  114: 
  115: 	hook.Run("VendorFactionUpdated", vendor, id, allowed)
  116: end)
  117: 
  118: addNetHandler("AllowClass", function(vendor)
  119: 	local id = net.ReadUInt(8)
  120: 	local allowed = net.ReadBool()
```

### 19. `plugins/vendor/cl_networking.lua` lines `106-122`

- Score: `23`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, hook emitter call, generic keyword match, query term overlap: vendor

```lua
  106: 	local id = net.ReadUInt(8)
  107: 	local allowed = net.ReadBool()
  108: 
  109: 	if (allowed) then
  110: 		vendor.factions[id] = true
  111: 	else
  112: 		vendor.factions[id] = nil
  113: 	end
  114: 
  115: 	hook.Run("VendorFactionUpdated", vendor, id, allowed)
  116: end)
  117: 
  118: addNetHandler("AllowClass", function(vendor)
  119: 	local id = net.ReadUInt(8)
  120: 	local allowed = net.ReadBool()
  121: 
  122: 	if (allowed) then
```

### 20. `plugins/vendor/cl_networking.lua` lines `109-125`

- Score: `23`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, hook emitter call, generic keyword match, query term overlap: vendor

```lua
  109: 	if (allowed) then
  110: 		vendor.factions[id] = true
  111: 	else
  112: 		vendor.factions[id] = nil
  113: 	end
  114: 
  115: 	hook.Run("VendorFactionUpdated", vendor, id, allowed)
  116: end)
  117: 
  118: addNetHandler("AllowClass", function(vendor)
  119: 	local id = net.ReadUInt(8)
  120: 	local allowed = net.ReadBool()
  121: 
  122: 	if (allowed) then
  123: 		vendor.classes[id] = true
  124: 	else
  125: 		vendor.classes[id] = nil
```

### 21. `plugins/vendor/cl_networking.lua` lines `112-128`

- Score: `23`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, hook emitter call, generic keyword match, query term overlap: vendor

```lua
  112: 		vendor.factions[id] = nil
  113: 	end
  114: 
  115: 	hook.Run("VendorFactionUpdated", vendor, id, allowed)
  116: end)
  117: 
  118: addNetHandler("AllowClass", function(vendor)
  119: 	local id = net.ReadUInt(8)
  120: 	local allowed = net.ReadBool()
  121: 
  122: 	if (allowed) then
  123: 		vendor.classes[id] = true
  124: 	else
  125: 		vendor.classes[id] = nil
  126: 	end
  127: 
  128: 	hook.Run("VendorClassUpdated", vendor, id, allowed)
```

### 22. `plugins/vendor/cl_networking.lua` lines `4-20`

- Score: `20`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, raw net operation, generic keyword match, query term overlap: vendor

```lua
    4: 		if (not IsValid(nutVendorEnt)) then return end
    5: 		handler(nutVendorEnt)
    6: 	end)
    7: end
    8: 
    9: net.Receive("nutVendorSync", function()
   10: 	local vendor = net.ReadEntity()
   11: 	if (not IsValid(vendor)) then return end
   12: 
   13: 	vendor.money = net.ReadInt(32)
   14: 	if (vendor.money < 0) then
   15: 		vendor.money = nil
   16: 	end
   17: 
   18: 	local count = net.ReadUInt(16)
   19: 	for i = 1, count do
   20: 		local itemType = net.ReadString()
```

### 23. `plugins/vendor/entities/entities/nut_vendor/shared.lua` lines `66-82`

- Score: `15`
- Realm: `shared/conditional`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, hook emitter call, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
   66: 		then
   67: 			nut.inventory.loadByID(self.invId)
   68: 			:next(function(inventory)
   69: 				if (inventory and IsValid(self))
   70: 				then
   71: 					hook.Run("StorageRestored", self, inventory)
   72: 					inventory.vendor = self
   73: 
   74: 					if (next(self.items))
   75: 					then
   76: 						for k, v in pairs(self.items) do
   77: 							if (v.price)
   78: 							then
   79: 								v.qty = v.initQty
   80: 								local item = inventory:getFirstItemOfType(k)
   81: 								if (item && item.isStackable)
   82: 								then
```

### 24. `plugins/vendor/derma/cl_vendor.lua` lines `47-63`

- Score: `13`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, important term: nutVendorTrade, generic keyword match, query term overlap: vendor

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
   60: 	self.vendor:setName(nutVendorEnt:getNetVar("name"))
   61: 	self.vendor:setMoney(nutVendorEnt:getMoney())
   62: 
   63: 	self.me = self:Add("nutVendorTrader")
```

### 25. `plugins/vendor/derma/cl_vendor.lua` lines `48-64`

- Score: `13`
- Realm: `client`
- Match: `state` / `\bvendor\b`
- Classification: `state_or_ui_reference`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, important term: nutVendorTrade, generic keyword match, query term overlap: vendor

```lua
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
   60: 	self.vendor:setName(nutVendorEnt:getNetVar("name"))
   61: 	self.vendor:setMoney(nutVendorEnt:getMoney())
   62: 
   63: 	self.me = self:Add("nutVendorTrader")
   64: 	self.me:SetSize(self.vendor:GetSize())
```

_Omitted 15 lower-ranked `noise` fragments._

## File Evidence Counts

- `plugins/vendor/cl_networking.lua`: `46`
- `plugins/vendor/derma/cl_vendor.lua`: `37`
- `plugins/vendor/entities/entities/nut_vendor/init.lua`: `37`
- `plugins/inventory/cl_hooks.lua`: `11`
- `plugins/vendor/entities/entities/nut_vendor/shared.lua`: `5`
- `gamemode/core/meta/inventory/cl_base_inventory.lua`: `1`
