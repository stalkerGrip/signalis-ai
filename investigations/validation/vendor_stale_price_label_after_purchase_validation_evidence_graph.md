# SIGNALIS AI — Evidence Graph

- Source: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_deduped.json`
- Query: `vendor stale price label after purchase`
- Nodes: `36`
- Edges: `65`
- Chains: `5`

## Runtime Chains

### Vendor Price Update / UI Refresh

- Confidence: `medium`
- Reason: trade and item metadata evidence connect to vendor price hook and UI refresh

1. `net:nutVendorTrade` — `plugins/vendor/derma/cl_vendor.lua:67-98` (client, score 115)
   ↓ `item_data:vendorQty` — `plugins/vendor/entities/entities/nut_vendor/init.lua:209-228` (unknown, score 113)
   ↓ `hook:VendorItemPriceUpdated` — `plugins/vendor/cl_networking.lua:62-80` (client, score 130)
   ↓ `ui_call:updatePrice` — `plugins/vendor/derma/cl_vendor.lua:148-183` (client, score 75)

### Vendor Exit / Metadata Clear

- Confidence: `medium`
- Reason: vendor exit evidence connects to vendor presentation metadata clearing

1. `net:nutVendorExit` — `plugins/vendor/derma/cl_vendor.lua:229-245` (client, score 115)
   ↓ `item_data:vendorBPrice` — `plugins/vendor/entities/entities/nut_vendor/init.lua:290-309` (unknown, score 103)
   ↓ `hook:VendorExited` — `plugins/vendor/cl_networking.lua:49-68` (client, score 74)

### Vendor Open / Initial Sync

- Confidence: `medium`
- Reason: vendor info sync and vendor opened hook are both client-side sync/open evidence

1. `netstream:sendVendorInfo` — `plugins/vendor/entities/entities/nut_vendor/init.lua:117-153` (unknown, score 67)
   ↓ `hook:VendorSynchronized` — `plugins/vendor/cl_networking.lua:15-42` (client, score 85)
   ↓ `hook:VendorOpened` — `plugins/vendor/cl_networking.lua:44-60` (client, score 149)

### Inventory UI Sync

- Confidence: `medium`
- Reason: inventory data and inventory panel creation connect to vendor trade interface

1. `net:nutInventoryData` — `gamemode/core/meta/inventory/cl_base_inventory.lua:1-13` (client, score 117)
   ↓ `hook:CreateNewInventoryPanel` — `plugins/inventory/cl_hooks.lua:101-141` (client, score 74)
   ↓ `netstream:vendorTradeInterface` — `plugins/inventory/cl_hooks.lua:117-146` (client, score 44)

### Hook Dispatch: VendorMoneyUpdated

- Confidence: `high`
- Reason: hook.Run dispatches to listener for VendorMoneyUpdated

1. `hook:VendorMoneyUpdated` — `plugins/vendor/cl_networking.lua:53-72` (client, score 140)
   ↓ `hook:VendorMoneyUpdated` — `plugins/vendor/derma/cl_vendor.lua:194-214` (client, score 154)

## Edges

- `net:nutVendorTrade` → `state:\bvendor\b`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `state:\bvendor\b` → `ui_call:updatePrice`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `hook:OnCharVarChanged` → `net:nutVendorExit`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `net:nutVendorExit` → `state:\bvendor\b`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `net:OpenMyInv` → `hook:CreateNewInventoryPanel`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `hook:OnCreateStoragePanel` → `netstream:itemSplitTake`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `hook:VendorSynchronized` → `hook:VendorOpened`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `hook:VendorItemPriceUpdated` → `hook:VendorItemStockUpdated`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `function:ENT:SetItemInStock` → `netstream:sendVendorInfo`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `item_data:vendorQty` → `state:\bprice\b`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `state:\bprice\b` → `hook:StorageEntityRemoved`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `hook:StorageEntityRemoved` → `item_data:vendorBPrice`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `item_data:vendorBPrice` → `state:\bvendor\b`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `state:\bvendor\b` → `hook:StorageRestored`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `hook:StorageRestored` → `hook:StorageInventorySet`
  - Kind: `file_order`
  - Confidence: `low`
  - Reason: same file and source order
- `hook:VendorMoneyUpdated` → `hook:VendorMoneyUpdated`
  - Kind: `hook_dispatch`
  - Confidence: `high`
  - Reason: hook.Run dispatches to listener for VendorMoneyUpdated
- `net:OpenMyInv` → `hook:CreateNewInventoryPanel`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorOpened` → `hook:VendorMoneyUpdated`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorOpened` → `hook:VendorItemPriceUpdated`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorOpened` → `hook:VendorExited`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorMoneyUpdated` → `hook:VendorItemPriceUpdated`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorMoneyUpdated` → `hook:VendorItemStockUpdated`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorItemPriceUpdated` → `hook:VendorItemStockUpdated`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorSynchronized` → `hook:VendorOpened`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorSynchronized` → `hook:VendorMoneyUpdated`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorSynchronized` → `hook:VendorItemPriceUpdated`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorSynchronized` → `hook:VendorExited`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorExited` → `hook:VendorMoneyUpdated`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorExited` → `hook:VendorItemPriceUpdated`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorExited` → `hook:VendorItemStockUpdated`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorClassUpdated` → `hook:VendorOpened`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorClassUpdated` → `hook:VendorMoneyUpdated`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorClassUpdated` → `hook:VendorItemPriceUpdated`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorClassUpdated` → `hook:VendorItemStockUpdated`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorClassUpdated` → `hook:VendorSynchronized`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `hook:VendorClassUpdated` → `hook:VendorExited`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `netstream:vendorTradeInterface` → `hook:OnCreateStoragePanel`
  - Kind: `network_handler_emits_hook`
  - Confidence: `medium`
  - Reason: network handler and hook emission are local in client networking file
- `item_data:vendorQty` → `hook:VendorMoneyUpdated`
  - Kind: `state_mutation_to_sync_event`
  - Confidence: `medium`
  - Reason: vendor item data mutation is related to vendor sync/update hook
- `item_data:vendorQty` → `hook:VendorMoneyUpdated`
  - Kind: `state_mutation_to_sync_event`
  - Confidence: `medium`
  - Reason: vendor item data mutation is related to vendor sync/update hook
- `item_data:vendorQty` → `hook:VendorItemPriceUpdated`
  - Kind: `state_mutation_to_sync_event`
  - Confidence: `medium`
  - Reason: vendor item data mutation is related to vendor sync/update hook
- `item_data:vendorQty` → `hook:VendorItemStockUpdated`
  - Kind: `state_mutation_to_sync_event`
  - Confidence: `medium`
  - Reason: vendor item data mutation is related to vendor sync/update hook
- `item_data:vendorQty` → `hook:VendorSynchronized`
  - Kind: `state_mutation_to_sync_event`
  - Confidence: `medium`
  - Reason: vendor item data mutation is related to vendor sync/update hook
- `item_data:vendorBPrice` → `hook:VendorMoneyUpdated`
  - Kind: `state_mutation_to_sync_event`
  - Confidence: `medium`
  - Reason: vendor item data mutation is related to vendor sync/update hook
- `item_data:vendorBPrice` → `hook:VendorMoneyUpdated`
  - Kind: `state_mutation_to_sync_event`
  - Confidence: `medium`
  - Reason: vendor item data mutation is related to vendor sync/update hook
- `item_data:vendorBPrice` → `hook:VendorItemPriceUpdated`
  - Kind: `state_mutation_to_sync_event`
  - Confidence: `medium`
  - Reason: vendor item data mutation is related to vendor sync/update hook
- `item_data:vendorBPrice` → `hook:VendorItemStockUpdated`
  - Kind: `state_mutation_to_sync_event`
  - Confidence: `medium`
  - Reason: vendor item data mutation is related to vendor sync/update hook
- `item_data:vendorBPrice` → `hook:VendorSynchronized`
  - Kind: `state_mutation_to_sync_event`
  - Confidence: `medium`
  - Reason: vendor item data mutation is related to vendor sync/update hook
- `hook:VendorMoneyUpdated` → `ui_call:updatePrice`
  - Kind: `hook_to_ui_refresh`
  - Confidence: `high`
  - Reason: vendor update hook leads to vendor panel price refresh
- `hook:VendorMoneyUpdated` → `ui_call:updatePrice`
  - Kind: `hook_to_ui_refresh`
  - Confidence: `high`
  - Reason: vendor update hook leads to vendor panel price refresh
- `hook:VendorItemPriceUpdated` → `ui_call:updatePrice`
  - Kind: `hook_to_ui_refresh`
  - Confidence: `high`
  - Reason: vendor update hook leads to vendor panel price refresh
- `hook:VendorItemStockUpdated` → `ui_call:updatePrice`
  - Kind: `hook_to_ui_refresh`
  - Confidence: `high`
  - Reason: vendor update hook leads to vendor panel price refresh
- `hook:VendorSynchronized` → `ui_call:updatePrice`
  - Kind: `hook_to_ui_refresh`
  - Confidence: `high`
  - Reason: vendor update hook leads to vendor panel price refresh
- `net:nutVendorTrade` → `item_data:vendorQty`
  - Kind: `trade_to_vendor_state`
  - Confidence: `medium`
  - Reason: vendor trade path connects to server-side vendor item data evidence
- `net:nutVendorTrade` → `item_data:vendorBPrice`
  - Kind: `trade_to_vendor_state`
  - Confidence: `medium`
  - Reason: vendor trade path connects to server-side vendor item data evidence
- `net:nutVendorTrade` → `function:ENT:AddItemAndSetQty`
  - Kind: `trade_to_vendor_state`
  - Confidence: `medium`
  - Reason: vendor trade path connects to server-side vendor item data evidence
- `net:nutVendorTrade` → `state:\bprice\b`
  - Kind: `trade_to_vendor_state`
  - Confidence: `medium`
  - Reason: vendor trade path connects to server-side vendor item data evidence
- `netstream:vendorTradeInterface` → `item_data:vendorQty`
  - Kind: `trade_to_vendor_state`
  - Confidence: `medium`
  - Reason: vendor trade path connects to server-side vendor item data evidence
- `netstream:vendorTradeInterface` → `item_data:vendorBPrice`
  - Kind: `trade_to_vendor_state`
  - Confidence: `medium`
  - Reason: vendor trade path connects to server-side vendor item data evidence
- `netstream:vendorTradeInterface` → `function:ENT:AddItemAndSetQty`
  - Kind: `trade_to_vendor_state`
  - Confidence: `medium`
  - Reason: vendor trade path connects to server-side vendor item data evidence
- `netstream:vendorTradeInterface` → `state:\bprice\b`
  - Kind: `trade_to_vendor_state`
  - Confidence: `medium`
  - Reason: vendor trade path connects to server-side vendor item data evidence
- `net:nutInventoryData` → `net:OpenMyInv`
  - Kind: `inventory_sync_to_ui`
  - Confidence: `medium`
  - Reason: inventory data receiver is related to client inventory UI evidence
- `net:nutInventoryData` → `netstream:itemSplitTake`
  - Kind: `inventory_sync_to_ui`
  - Confidence: `medium`
  - Reason: inventory data receiver is related to client inventory UI evidence
- `net:nutInventoryData` → `hook:CreateNewInventoryPanel`
  - Kind: `inventory_sync_to_ui`
  - Confidence: `medium`
  - Reason: inventory data receiver is related to client inventory UI evidence
- `net:nutInventoryData` → `hook:OnCreateStoragePanel`
  - Kind: `inventory_sync_to_ui`
  - Confidence: `medium`
  - Reason: inventory data receiver is related to client inventory UI evidence
- `net:nutInventoryData` → `netstream:vendorTradeInterface`
  - Kind: `inventory_sync_to_ui`
  - Confidence: `medium`
  - Reason: inventory data receiver is related to client inventory UI evidence

## Nodes

### hook:VendorMoneyUpdated

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `194-214`
- Realm: `client`
- Score: `154`
- Classification: `hook_listener_explicit`

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

### net:OpenMyInv

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `85-101`
- Realm: `client`
- Score: `153`
- Classification: `hook_listener_plugin_method`

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

### hook:VendorOpened

- File: `plugins/vendor/cl_networking.lua`
- Lines: `44-60`
- Realm: `client`
- Score: `149`
- Classification: `network_receiver`

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

### hook:OnCharVarChanged

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `201-217`
- Realm: `client`
- Score: `142`
- Classification: `hook_listener_explicit`

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

### hook:VendorMoneyUpdated

- File: `plugins/vendor/cl_networking.lua`
- Lines: `53-72`
- Realm: `client`
- Score: `140`
- Classification: `hook_emitter`

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

### hook:StorageEntityRemoved

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `263-279`
- Realm: `unknown`
- Score: `134`
- Classification: `network_send_or_start`

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

### hook:VendorItemPriceUpdated

- File: `plugins/vendor/cl_networking.lua`
- Lines: `62-80`
- Realm: `client`
- Score: `130`
- Classification: `hook_emitter`

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

### hook:VendorItemStockUpdated

- File: `plugins/vendor/cl_networking.lua`
- Lines: `85-101`
- Realm: `client`
- Score: `125`
- Classification: `hook_emitter`

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

### net:nutInventoryData

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Lines: `1-13`
- Realm: `client`
- Score: `117`
- Classification: `network_receiver`

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

### net:nutVendorTrade

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `67-98`
- Realm: `client`
- Score: `115`
- Classification: `network_send_or_start`

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

### net:nutVendorExit

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `229-245`
- Realm: `client`
- Score: `115`
- Classification: `network_send_or_start`

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

### item_data:vendorQty

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `209-228`
- Realm: `unknown`
- Score: `113`
- Classification: `item_data_mutation`

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

### item_data:vendorBPrice

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `290-309`
- Realm: `unknown`
- Score: `103`
- Classification: `item_data_mutation`

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

### function:ENT:AddItemAndSetQty

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `149-215`
- Realm: `unknown`
- Score: `95`
- Classification: `item_data_mutation`

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

### netstream:itemSplitTake

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `181-197`
- Realm: `client`
- Score: `87`
- Classification: `ui_presentation_logic`

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

### hook:VendorSynchronized

- File: `plugins/vendor/cl_networking.lua`
- Lines: `15-42`
- Realm: `client`
- Score: `85`
- Classification: `ui_presentation_logic`

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

### state:\bprice\b

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `171-215`
- Realm: `unknown`
- Score: `80`
- Classification: `item_data_mutation`

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
  184: 						if (newItem && !newItem.error)
  185: 						then
  186: 							self:VendorItemSetData(newItem, self.items[uniqueID].qty, self.items[uniqueID].price, self.items[uniqueID].maxQty, client)
  187: 						end
```

### ui_call:updatePrice

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `148-183`
- Realm: `client`
- Score: `75`
- Classification: `ui_presentation_logic`

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

### hook:CreateNewInventoryPanel

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `101-141`
- Realm: `client`
- Score: `74`
- Classification: `hook_reference`

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

### hook:VendorExited

- File: `plugins/vendor/cl_networking.lua`
- Lines: `49-68`
- Realm: `client`
- Score: `74`
- Classification: `state_or_ui_reference`

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

### state:SetText\s*\(

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `20-50`
- Realm: `client`
- Score: `73`
- Classification: `ui_presentation_logic`

```lua
   20: 	self.buttons:Dock(TOP)
   21: 	self.buttons:SetPaintBackground(false)
   22: 	self.buttons:SetTall(36)
   23: 
   24: 	self.leave = self.buttons:Add("DButton")
   25: 	self.leave:SetFont("nutVendorButtonFont")
   26: 	self.leave:SetText(L("leave"):upper())
   27: 	self.leave:SetTextColor(color_white)
   28: 	self.leave:SetContentAlignment(9)
   29: 	self.leave:SetExpensiveShadow(2, color_black)
   30: 	self.leave.DoClick = function(button)
   31: 		self:Remove()
   32: 	end
   33: 	self.leave:SizeToContents()
   34: 	self.leave:SetPaintBackground(false)
   35: 	self.leave.x = ScrW() * 0.5 - (self.leave:GetWide() * 0.5)
   36: 
```

### netstream:sendVendorInfo

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `117-153`
- Realm: `unknown`
- Score: `67`
- Classification: `ui_presentation_logic`

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

### state:\bvendor\b

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `47-75`
- Realm: `client`
- Score: `60`
- Classification: `networked_var_read`

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

### function:ENT:SetItemInStock

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `82-111`
- Realm: `unknown`
- Score: `55`
- Classification: `ui_presentation_logic`

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

### state:\bprice\b

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `231-258`
- Realm: `unknown`
- Score: `55`
- Classification: `ui_presentation_logic`

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

### hook:VendorClassUpdated

- File: `plugins/vendor/cl_networking.lua`
- Lines: `4-138`
- Realm: `client`
- Score: `50`
- Classification: `state_or_ui_reference`

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

### hook:StorageRestored

- File: `plugins/vendor/entities/entities/nut_vendor/shared.lua`
- Lines: `66-108`
- Realm: `shared/conditional`
- Score: `50`
- Classification: `ui_presentation_logic`

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

### hook:OnCreateStoragePanel

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `131-171`
- Realm: `client`
- Score: `47`
- Classification: `state_or_ui_reference`

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

### netstream:vendorTradeInterface

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `117-146`
- Realm: `client`
- Score: `44`
- Classification: `state_or_ui_reference`

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

### function:PANEL:onVendorModeUpdated

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `163-197`
- Realm: `client`
- Score: `40`
- Classification: `state_or_ui_reference`

```lua
  163: 			if (not IsValid(panel)) then continue end
  164: 			panel:updatePrice()
  165: 		end
  166: 	end
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

### hook:StorageInventorySet

- File: `plugins/vendor/entities/entities/nut_vendor/shared.lua`
- Lines: `116-132`
- Realm: `shared/conditional`
- Score: `12`
- Classification: `state_or_ui_reference`

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

### state:\bvendor\b

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `327-343`
- Realm: `unknown`
- Score: `5`
- Classification: `state_or_ui_reference`

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

### state:\bvendor\b

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `1-21`
- Realm: `client`
- Score: `1`
- Classification: `state_or_ui_reference`

```lua
    1: local PANEL = {}
    2: 
    3: local PADDING = 64
    4: local PADDING_HALF = PADDING / 2
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
```

### state:\bvendor\b

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `98-126`
- Realm: `client`
- Score: `1`
- Classification: `state_or_ui_reference`

```lua
   98: 
   99: 		if (mode ~= VENDOR_SELLONLY) then
  100: 			self:updateItem(itemType, self.me):setIsSelling(true)
  101: 		end
  102: 
  103: 		if (mode ~= VENDOR_BUYONLY) then
  104: 			self:updateItem(itemType, self.vendor)
  105: 		end
  106: 	end
  107: end
  108: 
  109: function PANEL:shouldItemBeVisible(itemType, parent)
  110: 	local mode = nutVendorEnt:getTradeMode(itemType)
  111: 
  112: 	if (parent == self.me and mode == VENDOR_SELLONLY) then
  113: 		return false
  114: 	end
```

### state:\bvendor\b

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `256-264`
- Realm: `client`
- Score: `1`
- Classification: `state_or_ui_reference`

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

### state:\bvendor\b

- File: `plugins/vendor/entities/entities/nut_vendor/shared.lua`
- Lines: `1-12`
- Realm: `shared/conditional`
- Score: `-15`
- Classification: `state_or_ui_reference`

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
