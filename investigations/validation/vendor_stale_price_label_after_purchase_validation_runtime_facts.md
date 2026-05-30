# SIGNALIS AI — Runtime Facts

- Source: `E:\signalis_ai\investigations\validation\vendor_stale_price_label_after_purchase_validation_deduped.json`
- Query: `vendor stale price label after purchase`
- Facts total: `63`

## Fact Type Counts

- `hook_emit`: `14`
- `hook_listener`: `13`
- `vendor_network_handler`: `9`
- `network_receive`: `8`
- `network_send_start`: `7`
- `item_data_mutation`: `7`
- `ui_text_update`: `2`
- `ui_refresh_call`: `2`
- `function_context`: `1`

## Facts

### 1. `hook_listener` / `VendorMoneyUpdated`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `194-214`
- Realm: `client`
- Confidence: `high`
- Evidence score: `154`
- Evidence classification: `hook_listener_explicit`
- Details: `{"listener_owner": "self", "listener_function": "self.onVendorMoneyUpdated", "enclosing_function": null, "source_semantic_target": "hook:VendorMoneyUpdated", "source_bucket": "critical", "source_duplicate_count": 3}`

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

### 2. `hook_listener` / `VendorItemStockUpdated`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `194-214`
- Realm: `client`
- Confidence: `high`
- Evidence score: `154`
- Evidence classification: `hook_listener_explicit`
- Details: `{"listener_owner": "self", "listener_function": "self.onItemStockUpdated", "enclosing_function": null, "source_semantic_target": "hook:VendorMoneyUpdated", "source_bucket": "critical", "source_duplicate_count": 3}`

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

### 3. `hook_listener` / `VendorItemPriceUpdated`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `194-214`
- Realm: `client`
- Confidence: `high`
- Evidence score: `154`
- Evidence classification: `hook_listener_explicit`
- Details: `{"listener_owner": "self", "listener_function": "self.onVendorPriceUpdated", "enclosing_function": null, "source_semantic_target": "hook:VendorMoneyUpdated", "source_bucket": "critical", "source_duplicate_count": 3}`

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

### 4. `hook_listener` / `VendorItemMaxStockUpdated`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `194-214`
- Realm: `client`
- Confidence: `high`
- Evidence score: `154`
- Evidence classification: `hook_listener_explicit`
- Details: `{"listener_owner": "self", "listener_function": "self.onItemStockUpdated", "enclosing_function": null, "source_semantic_target": "hook:VendorMoneyUpdated", "source_bucket": "critical", "source_duplicate_count": 3}`

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

### 5. `hook_listener` / `OnCharVarChanged`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `194-214`
- Realm: `client`
- Confidence: `high`
- Evidence score: `154`
- Evidence classification: `hook_listener_explicit`
- Details: `{"listener_owner": "self", "listener_function": "self.onCharVarChanged", "enclosing_function": null, "source_semantic_target": "hook:VendorMoneyUpdated", "source_bucket": "critical", "source_duplicate_count": 3}`

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

### 6. `network_send_start` / `inventorySetPanelStatus`

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `85-101`
- Realm: `client`
- Confidence: `medium`
- Evidence score: `153`
- Evidence classification: `hook_listener_plugin_method`
- Details: `{"network_api": "netstream", "sender_function": null, "source_semantic_target": "net:OpenMyInv", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 7. `network_receive` / `OpenMyInv`

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `85-101`
- Realm: `client`
- Confidence: `high`
- Evidence score: `153`
- Evidence classification: `hook_listener_plugin_method`
- Details: `{"network_api": "gmod_net", "receiver_function": null, "source_semantic_target": "net:OpenMyInv", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 8. `hook_listener` / `CreateTargetNewInventoryPanel`

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `85-101`
- Realm: `client`
- Confidence: `medium`
- Evidence score: `153`
- Evidence classification: `hook_listener_plugin_method`
- Details: `{"listener_owner": "PLUGIN", "listener_function": "PLUGIN:CreateTargetNewInventoryPanel", "registration_model": "NutScript implicit plugin/schema hook listener", "source_semantic_target": "net:OpenMyInv", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 9. `hook_listener` / `CreateNewInventoryPanel`

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `85-101`
- Realm: `client`
- Confidence: `medium`
- Evidence score: `153`
- Evidence classification: `hook_listener_plugin_method`
- Details: `{"listener_owner": "PLUGIN", "listener_function": "PLUGIN:CreateNewInventoryPanel", "registration_model": "NutScript implicit plugin/schema hook listener", "source_semantic_target": "net:OpenMyInv", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 10. `vendor_network_handler` / `Money`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `44-60`
- Realm: `client`
- Confidence: `high`
- Evidence score: `149`
- Evidence classification: `network_receiver`
- Details: `{"handler_function": null, "semantic_note": "vendor client-side submessage handler", "source_semantic_target": "hook:VendorOpened", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 11. `network_receive` / `nutVendorExit`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `44-60`
- Realm: `client`
- Confidence: `high`
- Evidence score: `149`
- Evidence classification: `network_receiver`
- Details: `{"network_api": "gmod_net", "receiver_function": null, "source_semantic_target": "hook:VendorOpened", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 12. `hook_emit` / `VendorOpened`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `44-60`
- Realm: `client`
- Confidence: `high`
- Evidence score: `149`
- Evidence classification: `network_receiver`
- Details: `{"emitter_function": null, "runtime_meaning": "event emission", "source_semantic_target": "hook:VendorOpened", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 13. `hook_emit` / `VendorMoneyUpdated`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `44-60`
- Realm: `client`
- Confidence: `high`
- Evidence score: `149`
- Evidence classification: `network_receiver`
- Details: `{"emitter_function": null, "runtime_meaning": "event emission", "source_semantic_target": "hook:VendorOpened", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 14. `hook_emit` / `VendorExited`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `44-60`
- Realm: `client`
- Confidence: `high`
- Evidence score: `149`
- Evidence classification: `network_receiver`
- Details: `{"emitter_function": null, "runtime_meaning": "event emission", "source_semantic_target": "hook:VendorOpened", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 15. `hook_listener` / `VendorItemStockUpdated`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `201-217`
- Realm: `client`
- Confidence: `high`
- Evidence score: `142`
- Evidence classification: `hook_listener_explicit`
- Details: `{"listener_owner": "self", "listener_function": "self.onItemStockUpdated", "enclosing_function": null, "source_semantic_target": "hook:OnCharVarChanged", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 16. `hook_listener` / `VendorItemPriceUpdated`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `201-217`
- Realm: `client`
- Confidence: `high`
- Evidence score: `142`
- Evidence classification: `hook_listener_explicit`
- Details: `{"listener_owner": "self", "listener_function": "self.onVendorPriceUpdated", "enclosing_function": null, "source_semantic_target": "hook:OnCharVarChanged", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 17. `hook_listener` / `VendorItemModeUpdated`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `201-217`
- Realm: `client`
- Confidence: `high`
- Evidence score: `142`
- Evidence classification: `hook_listener_explicit`
- Details: `{"listener_owner": "self", "listener_function": "self.onVendorModeUpdated", "enclosing_function": null, "source_semantic_target": "hook:OnCharVarChanged", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 18. `hook_listener` / `VendorItemMaxStockUpdated`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `201-217`
- Realm: `client`
- Confidence: `high`
- Evidence score: `142`
- Evidence classification: `hook_listener_explicit`
- Details: `{"listener_owner": "self", "listener_function": "self.onItemStockUpdated", "enclosing_function": null, "source_semantic_target": "hook:OnCharVarChanged", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 19. `hook_listener` / `VendorEdited`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `201-217`
- Realm: `client`
- Confidence: `high`
- Evidence score: `142`
- Evidence classification: `hook_listener_explicit`
- Details: `{"listener_owner": "self", "listener_function": "self.onVendorPropEdited", "enclosing_function": null, "source_semantic_target": "hook:OnCharVarChanged", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 20. `hook_listener` / `OnCharVarChanged`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `201-217`
- Realm: `client`
- Confidence: `high`
- Evidence score: `142`
- Evidence classification: `hook_listener_explicit`
- Details: `{"listener_owner": "self", "listener_function": "self.onCharVarChanged", "enclosing_function": null, "source_semantic_target": "hook:OnCharVarChanged", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 21. `vendor_network_handler` / `Price`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `53-72`
- Realm: `client`
- Confidence: `high`
- Evidence score: `140`
- Evidence classification: `hook_emitter`
- Details: `{"handler_function": null, "semantic_note": "vendor client-side submessage handler", "source_semantic_target": "hook:VendorMoneyUpdated", "source_bucket": "critical", "source_duplicate_count": 3}`

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

### 22. `vendor_network_handler` / `Money`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `53-72`
- Realm: `client`
- Confidence: `high`
- Evidence score: `140`
- Evidence classification: `hook_emitter`
- Details: `{"handler_function": null, "semantic_note": "vendor client-side submessage handler", "source_semantic_target": "hook:VendorMoneyUpdated", "source_bucket": "critical", "source_duplicate_count": 3}`

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

### 23. `hook_emit` / `VendorMoneyUpdated`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `53-72`
- Realm: `client`
- Confidence: `high`
- Evidence score: `140`
- Evidence classification: `hook_emitter`
- Details: `{"emitter_function": null, "runtime_meaning": "event emission", "source_semantic_target": "hook:VendorMoneyUpdated", "source_bucket": "critical", "source_duplicate_count": 3}`

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

### 24. `network_send_start` / `nutVendorExit`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `263-279`
- Realm: `unknown`
- Confidence: `high`
- Evidence score: `134`
- Evidence classification: `network_send_or_start`
- Details: `{"network_api": "gmod_net", "sender_function": null, "source_semantic_target": "hook:StorageEntityRemoved", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 25. `hook_emit` / `StorageEntityRemoved`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `263-279`
- Realm: `unknown`
- Confidence: `high`
- Evidence score: `134`
- Evidence classification: `network_send_or_start`
- Details: `{"emitter_function": null, "runtime_meaning": "event emission", "source_semantic_target": "hook:StorageEntityRemoved", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 26. `vendor_network_handler` / `Mode`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `62-80`
- Realm: `client`
- Confidence: `high`
- Evidence score: `130`
- Evidence classification: `hook_emitter`
- Details: `{"handler_function": null, "semantic_note": "vendor client-side submessage handler", "source_semantic_target": "hook:VendorItemPriceUpdated", "source_bucket": "critical", "source_duplicate_count": 3}`

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

### 27. `hook_emit` / `VendorItemPriceUpdated`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `62-80`
- Realm: `client`
- Confidence: `high`
- Evidence score: `130`
- Evidence classification: `hook_emitter`
- Details: `{"emitter_function": null, "runtime_meaning": "event emission", "source_semantic_target": "hook:VendorItemPriceUpdated", "source_bucket": "critical", "source_duplicate_count": 3}`

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

### 28. `vendor_network_handler` / `MaxStock`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `85-101`
- Realm: `client`
- Confidence: `high`
- Evidence score: `125`
- Evidence classification: `hook_emitter`
- Details: `{"handler_function": null, "semantic_note": "vendor client-side submessage handler", "source_semantic_target": "hook:VendorItemStockUpdated", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 29. `hook_emit` / `VendorItemStockUpdated`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `85-101`
- Realm: `client`
- Confidence: `high`
- Evidence score: `125`
- Evidence classification: `hook_emitter`
- Details: `{"emitter_function": null, "runtime_meaning": "event emission", "source_semantic_target": "hook:VendorItemStockUpdated", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 30. `network_receive` / `nutInventoryData`

- File: `gamemode/core/meta/inventory/cl_base_inventory.lua`
- Lines: `1-13`
- Realm: `client`
- Confidence: `high`
- Evidence score: `117`
- Evidence classification: `network_receiver`
- Details: `{"network_api": "gmod_net", "receiver_function": null, "source_semantic_target": "net:nutInventoryData", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 31. `network_send_start` / `nutVendorTrade`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `67-98`
- Realm: `client`
- Confidence: `high`
- Evidence score: `115`
- Evidence classification: `network_send_or_start`
- Details: `{"network_api": "gmod_net", "sender_function": null, "source_semantic_target": "net:nutVendorTrade", "source_bucket": "critical", "source_duplicate_count": 3}`

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

### 32. `network_send_start` / `nutVendorExit`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `229-245`
- Realm: `client`
- Confidence: `high`
- Evidence score: `115`
- Evidence classification: `network_send_or_start`
- Details: `{"network_api": "gmod_net", "sender_function": null, "source_semantic_target": "net:nutVendorExit", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 33. `item_data_mutation` / `vendorSPrice`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `209-228`
- Realm: `unknown`
- Confidence: `high`
- Evidence score: `113`
- Evidence classification: `item_data_mutation`
- Details: `{"mutator_function": null, "runtime_meaning": ["server item metadata mutation", "database persistence unless noSave", "conditional immediate client sync", "future owner/open inventory sync source"], "human_validated": true, "source_semantic_target": "item_data:vendorQty", "source_bucket": "critical", "source_duplicate_count": 9}`

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

### 34. `item_data_mutation` / `vendorQty`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `209-228`
- Realm: `unknown`
- Confidence: `high`
- Evidence score: `113`
- Evidence classification: `item_data_mutation`
- Details: `{"mutator_function": null, "runtime_meaning": ["server item metadata mutation", "database persistence unless noSave", "conditional immediate client sync", "future owner/open inventory sync source"], "human_validated": true, "source_semantic_target": "item_data:vendorQty", "source_bucket": "critical", "source_duplicate_count": 9}`

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

### 35. `item_data_mutation` / `vendorMQty`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `209-228`
- Realm: `unknown`
- Confidence: `high`
- Evidence score: `113`
- Evidence classification: `item_data_mutation`
- Details: `{"mutator_function": null, "runtime_meaning": ["server item metadata mutation", "database persistence unless noSave", "conditional immediate client sync", "future owner/open inventory sync source"], "human_validated": true, "source_semantic_target": "item_data:vendorQty", "source_bucket": "critical", "source_duplicate_count": 9}`

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

### 36. `item_data_mutation` / `vendorSPrice`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `290-309`
- Realm: `unknown`
- Confidence: `high`
- Evidence score: `103`
- Evidence classification: `item_data_mutation`
- Details: `{"mutator_function": "ENT:RemoveReceiverFromVendor", "runtime_meaning": ["server item metadata mutation", "database persistence unless noSave", "conditional immediate client sync", "future owner/open inventory sync source"], "human_validated": true, "source_semantic_target": "item_data:vendorBPrice", "source_bucket": "critical", "source_duplicate_count": 8}`

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

### 37. `item_data_mutation` / `vendorQty`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `290-309`
- Realm: `unknown`
- Confidence: `high`
- Evidence score: `103`
- Evidence classification: `item_data_mutation`
- Details: `{"mutator_function": "ENT:RemoveReceiverFromVendor", "runtime_meaning": ["server item metadata mutation", "database persistence unless noSave", "conditional immediate client sync", "future owner/open inventory sync source"], "human_validated": true, "source_semantic_target": "item_data:vendorBPrice", "source_bucket": "critical", "source_duplicate_count": 8}`

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

### 38. `item_data_mutation` / `vendorMQty`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `290-309`
- Realm: `unknown`
- Confidence: `high`
- Evidence score: `103`
- Evidence classification: `item_data_mutation`
- Details: `{"mutator_function": "ENT:RemoveReceiverFromVendor", "runtime_meaning": ["server item metadata mutation", "database persistence unless noSave", "conditional immediate client sync", "future owner/open inventory sync source"], "human_validated": true, "source_semantic_target": "item_data:vendorBPrice", "source_bucket": "critical", "source_duplicate_count": 8}`

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

### 39. `item_data_mutation` / `vendorBPrice`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `290-309`
- Realm: `unknown`
- Confidence: `high`
- Evidence score: `103`
- Evidence classification: `item_data_mutation`
- Details: `{"mutator_function": "ENT:RemoveReceiverFromVendor", "runtime_meaning": ["server item metadata mutation", "database persistence unless noSave", "conditional immediate client sync", "future owner/open inventory sync source"], "human_validated": true, "source_semantic_target": "item_data:vendorBPrice", "source_bucket": "critical", "source_duplicate_count": 8}`

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

### 40. `function_context` / `ENT:AddItemAndSetQty`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `149-215`
- Realm: `unknown`
- Confidence: `low`
- Evidence score: `95`
- Evidence classification: `item_data_mutation`
- Details: `{"note": "no explicit runtime operation extracted; kept as context only", "source_semantic_target": "function:ENT:AddItemAndSetQty", "source_bucket": "critical", "source_duplicate_count": 5}`

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

### 41. `ui_text_update` / `SetText`

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `181-197`
- Realm: `client`
- Confidence: `medium`
- Evidence score: `87`
- Evidence classification: `ui_presentation_logic`
- Details: `{"caller_function": null, "source_semantic_target": "netstream:itemSplitTake", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 42. `network_receive` / `itemSplitTake`

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `181-197`
- Realm: `client`
- Confidence: `high`
- Evidence score: `87`
- Evidence classification: `ui_presentation_logic`
- Details: `{"network_api": "netstream", "receiver_function": null, "source_semantic_target": "netstream:itemSplitTake", "source_bucket": "critical", "source_duplicate_count": 1}`

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

### 43. `network_receive` / `nutVendorOpen`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `15-42`
- Realm: `client`
- Confidence: `high`
- Evidence score: `85`
- Evidence classification: `ui_presentation_logic`
- Details: `{"network_api": "gmod_net", "receiver_function": null, "source_semantic_target": "hook:VendorSynchronized", "source_bucket": "critical", "source_duplicate_count": 3}`

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

### 44. `hook_emit` / `VendorSynchronized`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `15-42`
- Realm: `client`
- Confidence: `high`
- Evidence score: `85`
- Evidence classification: `ui_presentation_logic`
- Details: `{"emitter_function": null, "runtime_meaning": "event emission", "source_semantic_target": "hook:VendorSynchronized", "source_bucket": "critical", "source_duplicate_count": 3}`

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

### 45. `ui_refresh_call` / `updatePrice`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `148-183`
- Realm: `client`
- Confidence: `high`
- Evidence score: `75`
- Evidence classification: `ui_presentation_logic`
- Details: `{"caller_function": null, "ui_context": "vendor/inventory presentation", "source_semantic_target": "ui_call:updatePrice", "source_bucket": "critical", "source_duplicate_count": 4}`

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

### 46. `vendor_network_handler` / `Price`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `49-68`
- Realm: `client`
- Confidence: `high`
- Evidence score: `74`
- Evidence classification: `state_or_ui_reference`
- Details: `{"handler_function": null, "semantic_note": "vendor client-side submessage handler", "source_semantic_target": "hook:VendorExited", "source_bucket": "critical", "source_duplicate_count": 2}`

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

### 47. `vendor_network_handler` / `Money`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `49-68`
- Realm: `client`
- Confidence: `high`
- Evidence score: `74`
- Evidence classification: `state_or_ui_reference`
- Details: `{"handler_function": null, "semantic_note": "vendor client-side submessage handler", "source_semantic_target": "hook:VendorExited", "source_bucket": "critical", "source_duplicate_count": 2}`

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

### 48. `network_receive` / `vendorTradeInterface`

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `101-141`
- Realm: `client`
- Confidence: `high`
- Evidence score: `74`
- Evidence classification: `hook_reference`
- Details: `{"network_api": "netstream", "receiver_function": null, "source_semantic_target": "hook:CreateNewInventoryPanel", "source_bucket": "critical", "source_duplicate_count": 3}`

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

### 49. `network_receive` / `nutVendorExit`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `49-68`
- Realm: `client`
- Confidence: `high`
- Evidence score: `74`
- Evidence classification: `state_or_ui_reference`
- Details: `{"network_api": "gmod_net", "receiver_function": null, "source_semantic_target": "hook:VendorExited", "source_bucket": "critical", "source_duplicate_count": 2}`

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

### 50. `hook_emit` / `VendorMoneyUpdated`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `49-68`
- Realm: `client`
- Confidence: `high`
- Evidence score: `74`
- Evidence classification: `state_or_ui_reference`
- Details: `{"emitter_function": null, "runtime_meaning": "event emission", "source_semantic_target": "hook:VendorExited", "source_bucket": "critical", "source_duplicate_count": 2}`

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

### 51. `hook_emit` / `VendorExited`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `49-68`
- Realm: `client`
- Confidence: `high`
- Evidence score: `74`
- Evidence classification: `state_or_ui_reference`
- Details: `{"emitter_function": null, "runtime_meaning": "event emission", "source_semantic_target": "hook:VendorExited", "source_bucket": "critical", "source_duplicate_count": 2}`

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

### 52. `ui_text_update` / `SetText`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `20-50`
- Realm: `client`
- Confidence: `medium`
- Evidence score: `73`
- Evidence classification: `ui_presentation_logic`
- Details: `{"caller_function": null, "source_semantic_target": "state:SetText\\s*\\(", "source_bucket": "critical", "source_duplicate_count": 2}`

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

### 53. `network_send_start` / `sendVendorInfo`

- File: `plugins/vendor/entities/entities/nut_vendor/init.lua`
- Lines: `117-153`
- Realm: `unknown`
- Confidence: `medium`
- Evidence score: `67`
- Evidence classification: `ui_presentation_logic`
- Details: `{"network_api": "netstream", "recipient_expr": "client", "sender_function": null, "source_semantic_target": "netstream:sendVendorInfo", "source_bucket": "supporting", "source_duplicate_count": 4}`

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

### 54. `vendor_network_handler` / `Price`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `4-138`
- Realm: `client`
- Confidence: `high`
- Evidence score: `50`
- Evidence classification: `state_or_ui_reference`
- Details: `{"handler_function": null, "semantic_note": "vendor client-side submessage handler", "source_semantic_target": "hook:VendorClassUpdated", "source_bucket": "supporting", "source_duplicate_count": 33}`

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

### 55. `vendor_network_handler` / `Mode`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `4-138`
- Realm: `client`
- Confidence: `high`
- Evidence score: `50`
- Evidence classification: `state_or_ui_reference`
- Details: `{"handler_function": null, "semantic_note": "vendor client-side submessage handler", "source_semantic_target": "hook:VendorClassUpdated", "source_bucket": "supporting", "source_duplicate_count": 33}`

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

### 56. `hook_emit` / `VendorItemPriceUpdated`

- File: `plugins/vendor/cl_networking.lua`
- Lines: `4-138`
- Realm: `client`
- Confidence: `high`
- Evidence score: `50`
- Evidence classification: `state_or_ui_reference`
- Details: `{"emitter_function": null, "runtime_meaning": "event emission", "source_semantic_target": "hook:VendorClassUpdated", "source_bucket": "supporting", "source_duplicate_count": 33}`

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

### 57. `hook_emit` / `StorageRestored`

- File: `plugins/vendor/entities/entities/nut_vendor/shared.lua`
- Lines: `66-108`
- Realm: `shared/conditional`
- Confidence: `high`
- Evidence score: `50`
- Evidence classification: `ui_presentation_logic`
- Details: `{"emitter_function": null, "runtime_meaning": "event emission", "source_semantic_target": "hook:StorageRestored", "source_bucket": "supporting", "source_duplicate_count": 3}`

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

### 58. `network_send_start` / `removeReceiverFromVendor`

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `131-171`
- Realm: `client`
- Confidence: `medium`
- Evidence score: `47`
- Evidence classification: `state_or_ui_reference`
- Details: `{"network_api": "netstream", "sender_function": null, "source_semantic_target": "hook:OnCreateStoragePanel", "source_bucket": "supporting", "source_duplicate_count": 2}`

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

### 59. `network_send_start` / `inventorySetPanelStatus`

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `131-171`
- Realm: `client`
- Confidence: `medium`
- Evidence score: `47`
- Evidence classification: `state_or_ui_reference`
- Details: `{"network_api": "netstream", "sender_function": null, "source_semantic_target": "hook:OnCreateStoragePanel", "source_bucket": "supporting", "source_duplicate_count": 2}`

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

### 60. `hook_emit` / `OnCreateStoragePanel`

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `131-171`
- Realm: `client`
- Confidence: `high`
- Evidence score: `47`
- Evidence classification: `state_or_ui_reference`
- Details: `{"emitter_function": null, "runtime_meaning": "event emission", "source_semantic_target": "hook:OnCreateStoragePanel", "source_bucket": "supporting", "source_duplicate_count": 2}`

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

### 61. `network_receive` / `vendorTradeInterface`

- File: `plugins/inventory/cl_hooks.lua`
- Lines: `117-146`
- Realm: `client`
- Confidence: `high`
- Evidence score: `44`
- Evidence classification: `state_or_ui_reference`
- Details: `{"network_api": "netstream", "receiver_function": null, "source_semantic_target": "netstream:vendorTradeInterface", "source_bucket": "supporting", "source_duplicate_count": 4}`

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

### 62. `ui_refresh_call` / `updatePrice`

- File: `plugins/vendor/derma/cl_vendor.lua`
- Lines: `163-197`
- Realm: `client`
- Confidence: `high`
- Evidence score: `40`
- Evidence classification: `state_or_ui_reference`
- Details: `{"caller_function": null, "ui_context": "vendor/inventory presentation", "source_semantic_target": "function:PANEL:onVendorModeUpdated", "source_bucket": "supporting", "source_duplicate_count": 7}`

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

### 63. `hook_emit` / `StorageInventorySet`

- File: `plugins/vendor/entities/entities/nut_vendor/shared.lua`
- Lines: `116-132`
- Realm: `shared/conditional`
- Confidence: `high`
- Evidence score: `12`
- Evidence classification: `state_or_ui_reference`
- Details: `{"emitter_function": null, "runtime_meaning": "event emission", "source_semantic_target": "hook:StorageInventorySet", "source_bucket": "noise", "source_duplicate_count": 1}`

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
