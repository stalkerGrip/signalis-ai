# SIGNALIS AI — Deduplicated Validation Evidence

- Source: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_scored.json`
- Query: `vendor stale price label after purchase`
- Original fragments: `137`
- Deduped evidence: `46`
- Removed duplicates: `91`

## Evidence

### 1. `plugins/vendor/derma/cl_vendor.lua` lines `194-210`

- Bucket: `critical`
- Score: `154`
- Realm: `client`
- Classification: `hook_listener_explicit`
- Match: `hook` / `VendorMoneyUpdated`
- Duplicate count: `1`
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

- Bucket: `critical`
- Score: `154`
- Realm: `client`
- Classification: `hook_listener_explicit`
- Match: `hook` / `VendorItemPriceUpdated`
- Duplicate count: `1`
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

- Bucket: `critical`
- Score: `153`
- Realm: `client`
- Classification: `hook_listener_plugin_method`
- Match: `hook` / `CreateNewInventoryPanel`
- Duplicate count: `1`
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

- Bucket: `critical`
- Score: `149`
- Realm: `client`
- Classification: `network_receiver`
- Match: `network` / `nutVendorExit`
- Duplicate count: `1`
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

- Bucket: `critical`
- Score: `142`
- Realm: `client`
- Classification: `hook_listener_explicit`
- Match: `hook` / `VendorItemStockUpdated`
- Duplicate count: `1`
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

- Bucket: `critical`
- Score: `140`
- Realm: `client`
- Classification: `hook_emitter`
- Match: `hook` / `VendorMoneyUpdated`
- Duplicate count: `1`
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

- Bucket: `critical`
- Score: `134`
- Realm: `unknown`
- Classification: `network_send_or_start`
- Match: `network` / `nutVendorExit`
- Duplicate count: `1`
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

- Bucket: `critical`
- Score: `130`
- Realm: `client`
- Classification: `hook_emitter`
- Match: `hook` / `VendorItemPriceUpdated`
- Duplicate count: `1`
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

- Bucket: `critical`
- Score: `125`
- Realm: `client`
- Classification: `hook_emitter`
- Match: `hook` / `VendorItemStockUpdated`
- Duplicate count: `1`
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

- Bucket: `critical`
- Score: `117`
- Realm: `client`
- Classification: `network_receiver`
- Match: `network` / `nutInventoryData`
- Duplicate count: `1`
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

### 11. `plugins/vendor/derma/cl_vendor.lua` lines `75-98`

- Bucket: `critical`
- Score: `115`
- Realm: `client`
- Classification: `network_send_or_start`
- Match: `network` / `nutVendorTrade`
- Duplicate count: `2`
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

### 12. `plugins/vendor/derma/cl_vendor.lua` lines `229-245`

- Bucket: `critical`
- Score: `115`
- Realm: `client`
- Classification: `network_send_or_start`
- Match: `network` / `nutVendorExit`
- Duplicate count: `1`
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

### 13. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `171-228`

- Bucket: `critical`
- Score: `113`
- Realm: `unknown`
- Classification: `item_data_mutation`
- Match: `state` / `setData\s*\(`
- Duplicate count: `7`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, price label/UI presentation evidence, query term overlap: price, vendor, item/inventory data access

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

### 14. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `210-228`

- Bucket: `critical`
- Score: `113`
- Realm: `unknown`
- Classification: `item_data_mutation`
- Match: `state` / `:SetData\s*\(`
- Duplicate count: `3`
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

### 15. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `290-309`

- Bucket: `critical`
- Score: `103`
- Realm: `unknown`
- Classification: `item_data_mutation`
- Match: `state` / `:SetData\s*\(`
- Duplicate count: `4`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, item/inventory data access, query term overlap: price, vendor

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
  306: 	self:SetThdPos(Vector(pos3))
  307: 	self:SetFirstAngle(Angle(ang1))
  308: 	self:SetSecAngle(Angle(ang2))
  309: 	self:SetThdAngle(Angle(ang3))
```

### 16. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `290-309`

- Bucket: `critical`
- Score: `103`
- Realm: `unknown`
- Classification: `item_data_mutation`
- Match: `state` / `setData\s*\(`
- Duplicate count: `4`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, item/inventory data access, query term overlap: price, vendor

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
  306: 	self:SetThdPos(Vector(pos3))
  307: 	self:SetFirstAngle(Angle(ang1))
  308: 	self:SetSecAngle(Angle(ang2))
  309: 	self:SetThdAngle(Angle(ang3))
```

### 17. `plugins/vendor/derma/cl_vendor.lua` lines `197-213`

- Bucket: `critical`
- Score: `99`
- Realm: `client`
- Classification: `ui_presentation_logic`
- Match: `state` / `\bprice\b`
- Duplicate count: `1`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, client-side evidence, Derma/UI file, important term: VendorItemPriceUpdated, important term: VendorItemStockUpdated, important term: VendorMoneyUpdated, explicit hook listener, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
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
  211: 	hook.Add("VendorItemModeUpdated", self, self.onVendorModeUpdated)
  212: 
  213: 	-- Name change.
```

### 18. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `171-227`

- Bucket: `critical`
- Score: `98`
- Realm: `unknown`
- Classification: `item_data_mutation`
- Match: `state` / `\bprice\b`
- Duplicate count: `5`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor, item/inventory data access

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

### 19. `plugins/vendor/cl_networking.lua` lines `56-80`

- Bucket: `critical`
- Score: `97`
- Realm: `client`
- Classification: `ui_presentation_logic`
- Match: `state` / `\bvendor\b`
- Duplicate count: `3`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, client-side evidence, client networking file, important term: VendorItemPriceUpdated, important term: VendorMoneyUpdated, hook emitter call, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
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
   70: 	hook.Run("VendorItemPriceUpdated", vendor, itemType, value)
   71: end)
   72: 
```

### 20. `plugins/vendor/cl_networking.lua` lines `56-72`

- Bucket: `critical`
- Score: `97`
- Realm: `client`
- Classification: `ui_presentation_logic`
- Match: `state` / `\bprice\b`
- Duplicate count: `1`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, client-side evidence, client networking file, important term: VendorItemPriceUpdated, important term: VendorMoneyUpdated, hook emitter call, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
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
   70: 	hook.Run("VendorItemPriceUpdated", vendor, itemType, value)
   71: end)
   72: 
```

### 21. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `149-165`

- Bucket: `critical`
- Score: `95`
- Realm: `unknown`
- Classification: `item_data_mutation`
- Match: `state` / `setData\s*\(`
- Duplicate count: `1`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, price label/UI presentation evidence, query term overlap: price, vendor

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
  162: function ENT:HandleStock(uniqueID, isRemove, qty, isStackable, client)
  163: 	local inv = nut.inventory.instances[self.invId]
  164: 	if (self.items[uniqueID])
  165: 	then
```

### 22. `plugins/inventory/cl_hooks.lua` lines `181-197`

- Bucket: `critical`
- Score: `87`
- Realm: `client`
- Classification: `ui_presentation_logic`
- Match: `state` / `SetText\s*\(`
- Duplicate count: `1`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, client-side evidence, inventory client UI hook file, important term: SetText, netstream operation, price label/UI presentation evidence

```lua
  181: 	return text
  182: end
  183: 
  184: local function createButton(frame, text, x, y, w, h)
  185: 	local button = frame:Add("DButton")
  186: 	button:SetFont("nutWriteFont")
  187: 	button:SetText(text)
  188: 	button:SetPos(x, y)
  189: 	button:SetSize(w, h)
  190: 	return button
  191: end
  192: 
  193: netstream.Hook(
  194: 	"itemSplitTake",
  195: 	function(qty, itemID, x, y, invID, hookName)
  196: 		local splitFrame = vgui.Create("DFrame")
  197: 		splitFrame:SetTitle("Разделить")
```

### 23. `plugins/vendor/cl_networking.lua` lines `15-42`

- Bucket: `critical`
- Score: `85`
- Realm: `client`
- Classification: `ui_presentation_logic`
- Match: `state` / `\bprice\b`
- Duplicate count: `3`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, client-side evidence, client networking file, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor, hook emitter call, raw net operation

```lua
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

### 24. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `149-165`

- Bucket: `critical`
- Score: `80`
- Realm: `unknown`
- Classification: `item_data_mutation`
- Match: `state` / `\bprice\b`
- Duplicate count: `1`
- Reasons: critical classification: item_data_mutation, state/UI evidence, vendor entity server init, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

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
  162: function ENT:HandleStock(uniqueID, isRemove, qty, isStackable, client)
  163: 	local inv = nut.inventory.instances[self.invId]
  164: 	if (self.items[uniqueID])
  165: 	then
```

### 25. `plugins/vendor/derma/cl_vendor.lua` lines `167-183`

- Bucket: `critical`
- Score: `75`
- Realm: `client`
- Classification: `ui_presentation_logic`
- Match: `state` / `\bvendor\b`
- Duplicate count: `1`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, client-side evidence, Derma/UI file, important term: VendorMoneyUpdated, important term: updatePrice, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

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
  180: 
  181: function PANEL:onVendorModeUpdated(vendor, itemType, mode)
  182: 	self:updateItem(itemType, self.vendor)
  183: 	self:updateItem(itemType, self.me)
```

### 26. `plugins/vendor/cl_networking.lua` lines `4-138`

- Bucket: `critical`
- Score: `74`
- Realm: `client`
- Classification: `state_or_ui_reference`
- Match: `state` / `\bvendor\b`
- Duplicate count: `35`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, client networking file, raw net operation, generic keyword match, query term overlap: vendor, price label/UI presentation evidence, query term overlap: price, vendor, hook emitter call, important term: nutVendorExit, important term: VendorMoneyUpdated, important term: VendorItemPriceUpdated, important term: VendorItemStockUpdated

```lua
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

### 27. `plugins/inventory/cl_hooks.lua` lines `101-141`

- Bucket: `critical`
- Score: `74`
- Realm: `client`
- Classification: `hook_reference`
- Match: `hook` / `CreateNewInventoryPanel`
- Duplicate count: `3`
- Reasons: low-signal classification: hook_reference, hook evidence, client-side evidence, inventory client UI hook file, important term: CreateNewInventoryPanel, netstream operation, important term: vendorTradeInterface, query term overlap: vendor

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
  127: 	local localInv = LocalPlayer():getChar() && LocalPlayer():getChar():getInv(true)
  128: 	local loadedInv = nut.inventory.instances[invId]
  129: 	if (!loadedInv) then return end
  130: 
```

### 28. `plugins/vendor/derma/cl_vendor.lua` lines `20-50`

- Bucket: `critical`
- Score: `73`
- Realm: `client`
- Classification: `ui_presentation_logic`
- Match: `state` / `SetText\s*\(`
- Duplicate count: `2`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, client-side evidence, Derma/UI file, important term: SetText, price label/UI presentation evidence, query term overlap: vendor

```lua
   34: 	self.leave:SetPaintBackground(false)
   35: 	self.leave.x = ScrW() * 0.5 - (self.leave:GetWide() * 0.5)
   36: 
   37: 	if (LocalPlayer():IsAdmin()) then
   38: 		self.editor = self.buttons:Add("DButton")
   39: 		self.editor:SetFont("nutVendorButtonFont")
   40: 		self.editor:SetText(L("editor"):upper())
   41: 		self.editor:SetTextColor(color_white)
   42: 		self.editor:SetContentAlignment(9)
   43: 		self.editor:SetExpensiveShadow(2, color_black)
   44: 		self.editor.DoClick = function(button)
   45: 			vgui.Create("nutVendorEditor"):SetZPos(99)
   46: 		end
   47: 		self.editor:SizeToContents()
   48: 		self.editor:SetPaintBackground(false)
   49: 		self.leave.x = self.leave.x + 16 + self.leave:GetWide() * 0.5
   50: 		self.editor.x = ScrW() * 0.5 - 16 - self.editor:GetWide()
```

### 29. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `117-153`

- Bucket: `supporting`
- Score: `67`
- Realm: `unknown`
- Classification: `ui_presentation_logic`
- Match: `state` / `\bprice\b`
- Duplicate count: `4`
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

### 30. `plugins/vendor/derma/cl_vendor.lua` lines `54-70`

- Bucket: `supporting`
- Score: `60`
- Realm: `client`
- Classification: `networked_var_read`
- Match: `state` / `\bvendor\b`
- Duplicate count: `1`
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

### 31. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `82-111`

- Bucket: `supporting`
- Score: `55`
- Realm: `unknown`
- Classification: `ui_presentation_logic`
- Match: `state` / `\bprice\b`
- Duplicate count: `3`
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

### 32. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `231-258`

- Bucket: `supporting`
- Score: `55`
- Realm: `unknown`
- Classification: `ui_presentation_logic`
- Match: `state` / `\bprice\b`
- Duplicate count: `2`
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

### 33. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `189-205`

- Bucket: `supporting`
- Score: `55`
- Realm: `unknown`
- Classification: `ui_presentation_logic`
- Match: `state` / `\bprice\b`
- Duplicate count: `1`
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

### 34. `plugins/vendor/entities/entities/nut_vendor/shared.lua` lines `71-87`

- Bucket: `supporting`
- Score: `50`
- Realm: `shared/conditional`
- Classification: `ui_presentation_logic`
- Match: `state` / `\bprice\b`
- Duplicate count: `1`
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

### 35. `plugins/inventory/cl_hooks.lua` lines `155-171`

- Bucket: `supporting`
- Score: `47`
- Realm: `client`
- Classification: `state_or_ui_reference`
- Match: `state` / `\bvendor\b`
- Duplicate count: `1`
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

### 36. `plugins/inventory/cl_hooks.lua` lines `117-147`

- Bucket: `supporting`
- Score: `44`
- Realm: `client`
- Classification: `state_or_ui_reference`
- Match: `state` / `\bvendor\b`
- Duplicate count: `5`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, inventory client UI hook file, important term: vendorTradeInterface, important term: CreateNewInventoryPanel, netstream operation, generic keyword match, query term overlap: vendor

```lua
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
  134: 	storageInvPanel.vendor = vendor
  135: 	storageInvPanel:SetUpPanel(loadedInv)
```

### 37. `plugins/vendor/derma/cl_vendor.lua` lines `148-197`

- Bucket: `supporting`
- Score: `40`
- Realm: `client`
- Classification: `state_or_ui_reference`
- Match: `state` / `\bvendor\b`
- Duplicate count: `10`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, important term: updatePrice, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor, important term: VendorMoneyUpdated, query term overlap: vendor

```lua
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
  180: 
  181: function PANEL:onVendorModeUpdated(vendor, itemType, mode)
  182: 	self:updateItem(itemType, self.vendor)
  183: 	self:updateItem(itemType, self.me)
  184: end
```

### 38. `plugins/vendor/derma/cl_vendor.lua` lines `47-83`

- Bucket: `supporting`
- Score: `37`
- Realm: `client`
- Classification: `state_or_ui_reference`
- Match: `state` / `\bvendor\b`
- Duplicate count: `9`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, important term: nutVendorTrade, generic keyword match, query term overlap: vendor, important term: nutListenForInventoryChanges, raw net operation

```lua
   67: 	self.me:setMoney(LocalPlayer():getChar():getMoney())
   68: 
   69: 	self:listenForChanges()
   70: 	self:nutListenForInventoryChanges(LocalPlayer():getChar():getInv())
   71: 
   72: 	self.items = {
   73: 		[self.vendor] = {},
   74: 		[self.me] = {}
   75: 	}
   76: 
   77: 	self:initializeItems()
   78: end
   79: 
   80: function PANEL:buyItemFromVendor(itemType)
   81: 	net.Start("nutVendorTrade")
   82: 		net.WriteString(itemType)
   83: 		net.WriteBool(false)
```

### 39. `plugins/vendor/entities/entities/nut_vendor/shared.lua` lines `92-108`

- Bucket: `supporting`
- Score: `35`
- Realm: `shared/conditional`
- Classification: `ui_presentation_logic`
- Match: `state` / `\bprice\b`
- Duplicate count: `1`
- Reasons: supporting classification: ui_presentation_logic, state/UI evidence, price label/UI presentation evidence, generic keyword match, query term overlap: price, vendor

```lua
   92: 								
   93: 										return newItem
   94: 									end)
   95: 								end
   96: 							end
   97: 			
   98: 							if (!v.price && v.buyPrice)
   99: 							then
  100: 								v.qty = 0
  101: 							end
  102: 						end
  103: 					end
  104: 				elseif (IsValid(self))
  105: 				then
  106: 					timer.Simple(1, function()
  107: 						if (IsValid(self))
  108: 						then
```

### 40. `plugins/vendor/entities/entities/nut_vendor/shared.lua` lines `66-82`

- Bucket: `noise`
- Score: `15`
- Realm: `shared/conditional`
- Classification: `state_or_ui_reference`
- Match: `state` / `\bvendor\b`
- Duplicate count: `1`
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

### 41. `plugins/vendor/entities/entities/nut_vendor/shared.lua` lines `116-132`

- Bucket: `noise`
- Score: `12`
- Realm: `shared/conditional`
- Classification: `state_or_ui_reference`
- Match: `state` / `\bvendor\b`
- Duplicate count: `1`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, important term: storageInventory, hook emitter call, generic keyword match, query term overlap: vendor

```lua
  116: 			:next(
  117: 			function(inventory)
  118: 				if (IsValid(self))
  119: 				then
  120: 					self.invId = inventory:getID()
  121: 					hook.Run("StorageInventorySet", self, inventory)
  122: 					inventory.vendor = self
  123: 				end
  124: 			end,
  125: 			function(err)
  126: 				ErrorNoHalt("Unable to create lut entity\n".. err .."\n")
  127: 				if (IsValid(self)) then self:Remove() end
  128: 			end)
  129: 		end
  130: 	
  131: 		self:SetMoney(self:GetMoney() == 0 && 5000 || self:GetMoney())
  132: 		self.factions = self.factions || {}
```

### 42. `plugins/vendor/entities/entities/nut_vendor/init.lua` lines `327-343`

- Bucket: `noise`
- Score: `5`
- Realm: `unknown`
- Classification: `state_or_ui_reference`
- Match: `state` / `\bvendor\b`
- Duplicate count: `1`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, vendor entity server init, generic keyword match, query term overlap: vendor

```lua
  327: 	then
  328: 		return
  329: 	end
  330: 
  331: 	self:SetPos(poss[newPos])
  332: 	self:SetAngles(angs[newPos])
  333: 	print("Vendor " .. self:GetVendorName() .. " moved to " .. tostring(poss[newPos]))
  334: end
  335: 
  336: function ENT:MakeMovable()
  337: 	self:SetIsMovable(!self:GetIsMovable())
  338: 
  339: 	if (self:GetIsMovable())
  340: 	then
  341: 		self:SetCustomTimer(
  342: 			"moveVendor::" .. self:EntIndex(),
  343: 			3600,
```

### 43. `plugins/vendor/derma/cl_vendor.lua` lines `1-21`

- Bucket: `noise`
- Score: `1`
- Realm: `client`
- Classification: `state_or_ui_reference`
- Match: `state` / `\bvendor\b`
- Duplicate count: `4`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, generic keyword match, query term overlap: vendor

```lua
    5: 
    6: function PANEL:Init()
    7: 	if (IsValid(nut.gui.vendor)) then
    8: 		nut.gui.vendor.noSendExit = true
    9: 		nut.gui.vendor:Remove()
   10: 	end
   11: 	nut.gui.vendor = self
   12: 
   13: 	self:SetSize(ScrW(), ScrH())
   14: 	self:MakePopup()
   15: 	self:SetAlpha(0)
   16: 	self:AlphaTo(255, 0.2, 0)
   17: 
   18: 	self.buttons = self:Add("DPanel")
   19: 	self.buttons:DockMargin(0, 32, 0, 0)
   20: 	self.buttons:Dock(TOP)
   21: 	self.buttons:SetPaintBackground(false)
```

### 44. `plugins/vendor/derma/cl_vendor.lua` lines `98-126`

- Bucket: `noise`
- Score: `1`
- Realm: `client`
- Classification: `state_or_ui_reference`
- Match: `state` / `\bvendor\b`
- Duplicate count: `2`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, generic keyword match, query term overlap: vendor

```lua
  110: 	local mode = nutVendorEnt:getTradeMode(itemType)
  111: 
  112: 	if (parent == self.me and mode == VENDOR_SELLONLY) then
  113: 		return false
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

### 45. `plugins/vendor/derma/cl_vendor.lua` lines `256-264`

- Bucket: `noise`
- Score: `1`
- Realm: `client`
- Classification: `state_or_ui_reference`
- Match: `state` / `\bvendor\b`
- Duplicate count: `1`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, client-side evidence, Derma/UI file, generic keyword match, query term overlap: vendor

```lua
  256: 	end
  257: end
  258: 
  259: 
  260: vgui.Register("nutVendor", PANEL, "EditablePanel")
  261: 
  262: if (IsValid(nut.gui.vendor)) then
  263: 	vgui.Create("nutVendor")
  264: end
```

### 46. `plugins/vendor/entities/entities/nut_vendor/shared.lua` lines `1-12`

- Bucket: `noise`
- Score: `-15`
- Realm: `shared/conditional`
- Classification: `state_or_ui_reference`
- Match: `state` / `\bvendor\b`
- Duplicate count: `1`
- Reasons: low-signal classification: state_or_ui_reference, state/UI evidence, generic keyword match, query term overlap: vendor

```lua
    1: ENT.Type = "anim"
    2: ENT.PrintName = "Vendor"
    3: ENT.Category = "NutScript"
    4: ENT.Spawnable = true
    5: ENT.AdminOnly = true
    6: ENT.isVendor = true
    7: ENT.invType = "grid"
    8: ENT.invData = {
    9: 	w = 10,
   10: 	h = 9,
   11: }
   12: 
```

## File Counts

- `plugins/vendor/derma/cl_vendor.lua`: `14`
- `plugins/vendor/entities/entities/nut_vendor/init.lua`: `13`
- `plugins/vendor/cl_networking.lua`: `8`
- `plugins/inventory/cl_hooks.lua`: `5`
- `plugins/vendor/entities/entities/nut_vendor/shared.lua`: `5`
- `gamemode/core/meta/inventory/cl_base_inventory.lua`: `1`