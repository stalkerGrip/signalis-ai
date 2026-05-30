# SIGNALIS AI — Source Validation Report

- Generated: `2026-05-30T20:28:55`
- Investigation report: `E:\signalis_ai\investigations\generated\vendor_stale_price_label_after_purchase.md`
- Query: `vendor stale price label after purchase`
- Workspace: `E:\signalis_ai`

## Source Roots

- `E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis`
- `E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript`

## Summary

- Priority files: `6`
- Files found: `6`
- Missing files: `0`
- Extracted fragments: `137`
- Hook fragments: `10`
- Network fragments: `6`
- State/UI fragments: `121`

## Validation Targets

### Priority Files

- `plugins/vendor/derma/cl_vendor.lua`
- `plugins/vendor/cl_networking.lua`
- `plugins/inventory/cl_hooks.lua`
- `gamemode/core/meta/inventory/cl_base_inventory.lua`
- `plugins/vendor/entities/entities/nut_vendor/init.lua`
- `plugins/vendor/entities/entities/nut_vendor/shared.lua`

### Priority Hooks

- `VendorItemPriceUpdated`
- `VendorItemStockUpdated`
- `VendorMoneyUpdated`
- `CanPlayerAccessVendor`
- `CanPlayerTradeWithVendor`
- `CreateNewInventoryPanel`
- `CreateInventoryPanel`

### Priority Network Messages

- `nutVendorTrade`
- `nutVendorExit`
- `nutInventoryData`

## Missing Files

- none

## Source Evidence

### `plugins/vendor/derma/cl_vendor.lua`

- Exists: `True`
- Resolved path: `E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\derma\cl_vendor.lua`
- Source root: `E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript`
- Realm: `client`
- Note: Client realm: likely presentation/UI or client request logic unless source shows otherwise.

#### Fragment 1: state / \bvendor\b

- Lines: `1-17`
- Realm: `client`
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

#### Fragment 2: state / \bvendor\b

- Lines: `2-18`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
   18: 	self.buttons = self:Add("DPanel")
```

#### Fragment 3: state / \bvendor\b

- Lines: `3-19`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
   18: 	self.buttons = self:Add("DPanel")
   19: 	self.buttons:DockMargin(0, 32, 0, 0)
```

#### Fragment 4: state / \bvendor\b

- Lines: `5-21`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 5: state / SetText\s*\(

- Lines: `20-36`
- Realm: `client`
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

#### Fragment 6: state / SetText\s*\(

- Lines: `34-50`
- Realm: `client`
- Classification: `ui_presentation_logic`

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

#### Fragment 7: state / \bvendor\b

- Lines: `47-63`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 8: state / \bvendor\b

- Lines: `48-64`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 9: state / \bvendor\b

- Lines: `49-65`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
   65: 	self.me:SetPos(ScrW() * 0.5 + PADDING_HALF, self.vendor.y)
```

#### Fragment 10: state / \bvendor\b

- Lines: `50-66`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
   65: 	self.me:SetPos(ScrW() * 0.5 + PADDING_HALF, self.vendor.y)
   66: 	self.me:setName(L"you")
```

#### Fragment 11: state / \bvendor\b

- Lines: `53-69`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
   65: 	self.me:SetPos(ScrW() * 0.5 + PADDING_HALF, self.vendor.y)
   66: 	self.me:setName(L"you")
   67: 	self.me:setMoney(LocalPlayer():getChar():getMoney())
   68: 
   69: 	self:listenForChanges()
```

#### Fragment 12: state / \bvendor\b

- Lines: `54-70`
- Realm: `client`
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

#### Fragment 13: state / \bvendor\b

- Lines: `55-71`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 14: state / \bvendor\b

- Lines: `58-74`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 15: state / \bvendor\b

- Lines: `59-75`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 16: state / \bvendor\b

- Lines: `67-83`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 17: network / nutVendorTrade

- Lines: `75-91`
- Realm: `client`
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

#### Fragment 18: network / nutVendorTrade

- Lines: `82-98`
- Realm: `client`
- Classification: `network_send_or_start`

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

#### Fragment 19: state / \bvendor\b

- Lines: `98-114`
- Realm: `client`
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

#### Fragment 20: state / \bvendor\b

- Lines: `110-126`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 21: state / \bvendor\b

- Lines: `148-164`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 22: state / \bvendor\b

- Lines: `150-166`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 23: state / \bvendor\b

- Lines: `152-168`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 24: state / \bvendor\b

- Lines: `163-179`
- Realm: `client`
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

#### Fragment 25: state / \bvendor\b

- Lines: `164-180`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
  180: 
```

#### Fragment 26: state / \bvendor\b

- Lines: `167-183`
- Realm: `client`
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

#### Fragment 27: state / \bvendor\b

- Lines: `168-184`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 28: state / \bvendor\b

- Lines: `175-191`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 29: state / \bvendor\b

- Lines: `176-192`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 30: state / \bvendor\b

- Lines: `180-196`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
  193: 	if (key == "money") then
  194: 		self.me:setMoney(newValue)
  195: 	end
  196: end
```

#### Fragment 31: state / \bvendor\b

- Lines: `181-197`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
  193: 	if (key == "money") then
  194: 		self.me:setMoney(newValue)
  195: 	end
  196: end
  197: 
```

#### Fragment 32: hook / VendorMoneyUpdated

- Lines: `194-210`
- Realm: `client`
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

#### Fragment 33: state / \bprice\b

- Lines: `197-213`
- Realm: `client`
- Classification: `ui_presentation_logic`

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

#### Fragment 34: hook / VendorItemPriceUpdated

- Lines: `198-214`
- Realm: `client`
- Classification: `hook_listener_explicit`

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

#### Fragment 35: hook / VendorItemStockUpdated

- Lines: `201-217`
- Realm: `client`
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

#### Fragment 36: network / nutVendorExit

- Lines: `229-245`
- Realm: `client`
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

#### Fragment 37: state / \bvendor\b

- Lines: `256-264`
- Realm: `client`
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

### `plugins/vendor/cl_networking.lua`

- Exists: `True`
- Resolved path: `E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\cl_networking.lua`
- Source root: `E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript`
- Realm: `client`
- Note: Client realm: likely presentation/UI or client request logic unless source shows otherwise.

#### Fragment 1: state / \bvendor\b

- Lines: `4-20`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 2: state / \bvendor\b

- Lines: `5-21`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
   21: 		local price = net.ReadInt(32)
```

#### Fragment 3: state / \bvendor\b

- Lines: `7-23`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
   21: 		local price = net.ReadInt(32)
   22: 		local stock = net.ReadInt(32)
   23: 		local maxStock = net.ReadInt(32)
```

#### Fragment 4: state / \bvendor\b

- Lines: `8-24`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
   21: 		local price = net.ReadInt(32)
   22: 		local stock = net.ReadInt(32)
   23: 		local maxStock = net.ReadInt(32)
   24: 		local mode = net.ReadInt(8)
```

#### Fragment 5: state / \bvendor\b

- Lines: `9-25`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
   21: 		local price = net.ReadInt(32)
   22: 		local stock = net.ReadInt(32)
   23: 		local maxStock = net.ReadInt(32)
   24: 		local mode = net.ReadInt(8)
   25: 
```

#### Fragment 6: state / \bprice\b

- Lines: `15-31`
- Realm: `client`
- Classification: `ui_presentation_logic`

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

#### Fragment 7: state / \bprice\b

- Lines: `20-36`
- Realm: `client`
- Classification: `ui_presentation_logic`

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

#### Fragment 8: state / \bvendor\b

- Lines: `25-41`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
   37: 	end
   38: 
   39: 	hook.Run("VendorSynchronized", vendor)
   40: end)
   41: 
```

#### Fragment 9: state / \bprice\b

- Lines: `26-42`
- Realm: `client`
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

#### Fragment 10: state / \bvendor\b

- Lines: `33-49`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
   43: 	local vendor = net.ReadEntity()
   44: 	if (IsValid(vendor)) then
   45: 		nutVendorEnt = vendor
   46: 		hook.Run("VendorOpened", vendor)
   47: 	end
   48: end)
   49: 
```

#### Fragment 11: state / \bvendor\b

- Lines: `37-53`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 12: state / \bvendor\b

- Lines: `38-54`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 13: state / \bvendor\b

- Lines: `39-55`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 14: state / \bvendor\b

- Lines: `40-56`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 15: network / nutVendorExit

- Lines: `44-60`
- Realm: `client`
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

#### Fragment 16: state / \bvendor\b

- Lines: `49-65`
- Realm: `client`
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

#### Fragment 17: state / \bvendor\b

- Lines: `52-68`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 18: hook / VendorMoneyUpdated

- Lines: `53-69`
- Realm: `client`
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

#### Fragment 19: state / \bvendor\b

- Lines: `53-69`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 20: state / \bprice\b

- Lines: `56-72`
- Realm: `client`
- Classification: `ui_presentation_logic`

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

#### Fragment 21: state / \bvendor\b

- Lines: `56-72`
- Realm: `client`
- Classification: `ui_presentation_logic`

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

#### Fragment 22: state / \bvendor\b

- Lines: `61-77`
- Realm: `client`
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

#### Fragment 23: state / \bvendor\b

- Lines: `62-78`
- Realm: `client`
- Classification: `ui_presentation_logic`

```lua
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
   78: 	vendor.items[itemType] = vendor.items[itemType] or {}
```

#### Fragment 24: hook / VendorItemPriceUpdated

- Lines: `64-80`
- Realm: `client`
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

#### Fragment 25: state / \bvendor\b

- Lines: `64-80`
- Realm: `client`
- Classification: `ui_presentation_logic`

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

#### Fragment 26: state / \bvendor\b

- Lines: `67-83`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
   81: 	hook.Run("VendorItemModeUpdated", vendor, itemType, value)
   82: end)
   83: 
```

#### Fragment 27: state / \bvendor\b

- Lines: `72-88`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 28: state / \bvendor\b

- Lines: `73-89`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 29: state / \bvendor\b

- Lines: `75-91`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
   90: 
   91: 	hook.Run("VendorItemStockUpdated", vendor, itemType, value)
```

#### Fragment 30: state / \bvendor\b

- Lines: `78-94`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
   90: 
   91: 	hook.Run("VendorItemStockUpdated", vendor, itemType, value)
   92: end)
   93: 
   94: addNetHandler("MaxStock", function(vendor)
```

#### Fragment 31: state / \bvendor\b

- Lines: `82-98`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
   82: end)
   83: 
   84: addNetHandler("Stock", function(vendor)
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
```

#### Fragment 32: state / \bvendor\b

- Lines: `83-99`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
   83: 
   84: addNetHandler("Stock", function(vendor)
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
```

#### Fragment 33: hook / VendorItemStockUpdated

- Lines: `85-101`
- Realm: `client`
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

#### Fragment 34: state / \bvendor\b

- Lines: `85-101`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 35: state / \bvendor\b

- Lines: `88-104`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
  102: 	hook.Run("VendorItemMaxStockUpdated", vendor, itemType, value)
  103: end)
  104: 
```

#### Fragment 36: state / \bvendor\b

- Lines: `93-109`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 37: state / \bvendor\b

- Lines: `94-110`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 38: state / \bvendor\b

- Lines: `96-112`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 39: state / \bvendor\b

- Lines: `99-115`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 40: state / \bvendor\b

- Lines: `104-120`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 41: state / \bvendor\b

- Lines: `106-122`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 42: state / \bvendor\b

- Lines: `109-125`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 43: state / \bvendor\b

- Lines: `112-128`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 44: state / \bvendor\b

- Lines: `117-133`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
  129: end)
  130: 
  131: net.Receive("nutVendorEdit", function()
  132: 	local key = net.ReadString()
  133: 	-- Give some time to receive the update.
```

#### Fragment 45: state / \bvendor\b

- Lines: `119-135`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
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
  129: end)
  130: 
  131: net.Receive("nutVendorEdit", function()
  132: 	local key = net.ReadString()
  133: 	-- Give some time to receive the update.
  134: 	timer.Simple(0.25, function()
  135: 		if (not IsValid(nutVendorEnt)) then return end
```

#### Fragment 46: state / \bvendor\b

- Lines: `122-138`
- Realm: `client`
- Classification: `state_or_ui_reference`

```lua
  122: 	if (allowed) then
  123: 		vendor.classes[id] = true
  124: 	else
  125: 		vendor.classes[id] = nil
  126: 	end
  127: 
  128: 	hook.Run("VendorClassUpdated", vendor, id, allowed)
  129: end)
  130: 
  131: net.Receive("nutVendorEdit", function()
  132: 	local key = net.ReadString()
  133: 	-- Give some time to receive the update.
  134: 	timer.Simple(0.25, function()
  135: 		if (not IsValid(nutVendorEnt)) then return end
  136: 		hook.Run("VendorEdited", nutVendorEnt, key)
  137: 	end)
  138: end)
```

### `plugins/inventory/cl_hooks.lua`

- Exists: `True`
- Resolved path: `E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis\plugins\inventory\cl_hooks.lua`
- Source root: `E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\signalis`
- Realm: `client`
- Note: Client realm: likely presentation/UI or client request logic unless source shows otherwise.

#### Fragment 1: hook / CreateNewInventoryPanel

- Lines: `85-101`
- Realm: `client`
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

#### Fragment 2: hook / CreateNewInventoryPanel

- Lines: `101-117`
- Realm: `client`
- Classification: `hook_reference`

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

#### Fragment 3: hook / CreateNewInventoryPanel

- Lines: `114-130`
- Realm: `client`
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

#### Fragment 4: state / \bvendor\b

- Lines: `117-133`
- Realm: `client`
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

#### Fragment 5: state / \bvendor\b

- Lines: `119-135`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 6: hook / CreateNewInventoryPanel

- Lines: `125-141`
- Realm: `client`
- Classification: `hook_reference`

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

#### Fragment 7: state / \bvendor\b

- Lines: `128-144`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 8: state / \bvendor\b

- Lines: `130-146`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 9: state / \bvendor\b

- Lines: `131-147`
- Realm: `client`
- Classification: `state_or_ui_reference`

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

#### Fragment 10: state / \bvendor\b

- Lines: `155-171`
- Realm: `client`
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

#### Fragment 11: state / SetText\s*\(

- Lines: `181-197`
- Realm: `client`
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

### `gamemode/core/meta/inventory/cl_base_inventory.lua`

- Exists: `True`
- Resolved path: `E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\gamemode\core\meta\inventory\cl_base_inventory.lua`
- Source root: `E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript`
- Realm: `client`
- Note: Client realm: likely presentation/UI or client request logic unless source shows otherwise.

#### Fragment 1: network / nutInventoryData

- Lines: `1-13`
- Realm: `client`
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

### `plugins/vendor/entities/entities/nut_vendor/init.lua`

- Exists: `True`
- Resolved path: `E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\entities\entities\nut_vendor\init.lua`
- Source root: `E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript`
- Realm: `unknown`

#### Fragment 1: state / \bprice\b

- Lines: `82-98`
- Realm: `unknown`
- Classification: `ui_presentation_logic`

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

#### Fragment 2: state / \bprice\b

- Lines: `88-104`
- Realm: `unknown`
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

#### Fragment 3: state / \bprice\b

- Lines: `95-111`
- Realm: `unknown`
- Classification: `ui_presentation_logic`

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

#### Fragment 4: state / \bprice\b

- Lines: `117-133`
- Realm: `unknown`
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

#### Fragment 5: state / \bprice\b

- Lines: `121-137`
- Realm: `unknown`
- Classification: `ui_presentation_logic`

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

#### Fragment 6: state / \bprice\b

- Lines: `126-142`
- Realm: `unknown`
- Classification: `ui_presentation_logic`

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

#### Fragment 7: state / \bprice\b

- Lines: `137-153`
- Realm: `unknown`
- Classification: `ui_presentation_logic`

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

#### Fragment 8: state / setData\s*\(

- Lines: `149-165`
- Realm: `unknown`
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

#### Fragment 9: state / \bprice\b

- Lines: `149-165`
- Realm: `unknown`
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

#### Fragment 10: state / setData\s*\(

- Lines: `171-187`
- Realm: `unknown`
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

#### Fragment 11: state / \bprice\b

- Lines: `171-187`
- Realm: `unknown`
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

#### Fragment 12: state / setData\s*\(

- Lines: `180-196`
- Realm: `unknown`
- Classification: `item_data_mutation`

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
  193: 		else
  194: 			self.items[uniqueID].qty = self.items[uniqueID].qty + qty
  195: 			if (self.items[uniqueID].price)
  196: 			then
```

#### Fragment 13: state / \bprice\b

- Lines: `180-196`
- Realm: `unknown`
- Classification: `item_data_mutation`

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
  193: 		else
  194: 			self.items[uniqueID].qty = self.items[uniqueID].qty + qty
  195: 			if (self.items[uniqueID].price)
  196: 			then
```

#### Fragment 14: state / \bprice\b

- Lines: `189-205`
- Realm: `unknown`
- Classification: `ui_presentation_logic`

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

#### Fragment 15: state / setData\s*\(

- Lines: `199-215`
- Realm: `unknown`
- Classification: `item_data_mutation`

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
  212: 	end
  213: end
  214: 
  215: function ENT:VendorItemSetData(item, qty, price, maxQty, client)
```

#### Fragment 16: state / \bprice\b

- Lines: `199-215`
- Realm: `unknown`
- Classification: `item_data_mutation`

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
  212: 	end
  213: end
  214: 
  215: function ENT:VendorItemSetData(item, qty, price, maxQty, client)
```

#### Fragment 17: state / setData\s*\(

- Lines: `209-225`
- Realm: `unknown`
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

#### Fragment 18: state / \bprice\b

- Lines: `209-225`
- Realm: `unknown`
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

#### Fragment 19: state / :SetData\s*\(

- Lines: `210-226`
- Realm: `unknown`
- Classification: `item_data_mutation`

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

#### Fragment 20: state / setData\s*\(

- Lines: `210-226`
- Realm: `unknown`
- Classification: `item_data_mutation`

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

#### Fragment 21: state / :SetData\s*\(

- Lines: `211-227`
- Realm: `unknown`
- Classification: `item_data_mutation`

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

#### Fragment 22: state / setData\s*\(

- Lines: `211-227`
- Realm: `unknown`
- Classification: `item_data_mutation`

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

#### Fragment 23: state / \bprice\b

- Lines: `211-227`
- Realm: `unknown`
- Classification: `item_data_mutation`

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

#### Fragment 24: state / :SetData\s*\(

- Lines: `212-228`
- Realm: `unknown`
- Classification: `item_data_mutation`

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

#### Fragment 25: state / setData\s*\(

- Lines: `212-228`
- Realm: `unknown`
- Classification: `item_data_mutation`

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

#### Fragment 26: state / \bprice\b

- Lines: `231-247`
- Realm: `unknown`
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

#### Fragment 27: state / \bprice\b

- Lines: `242-258`
- Realm: `unknown`
- Classification: `ui_presentation_logic`

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

#### Fragment 28: network / nutVendorExit

- Lines: `263-279`
- Realm: `unknown`
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

#### Fragment 29: state / :SetData\s*\(

- Lines: `290-306`
- Realm: `unknown`
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

#### Fragment 30: state / setData\s*\(

- Lines: `290-306`
- Realm: `unknown`
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

#### Fragment 31: state / :SetData\s*\(

- Lines: `291-307`
- Realm: `unknown`
- Classification: `item_data_mutation`

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

#### Fragment 32: state / setData\s*\(

- Lines: `291-307`
- Realm: `unknown`
- Classification: `item_data_mutation`

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

#### Fragment 33: state / :SetData\s*\(

- Lines: `292-308`
- Realm: `unknown`
- Classification: `item_data_mutation`

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

#### Fragment 34: state / setData\s*\(

- Lines: `292-308`
- Realm: `unknown`
- Classification: `item_data_mutation`

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

#### Fragment 35: state / :SetData\s*\(

- Lines: `293-309`
- Realm: `unknown`
- Classification: `item_data_mutation`

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

#### Fragment 36: state / setData\s*\(

- Lines: `293-309`
- Realm: `unknown`
- Classification: `item_data_mutation`

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

#### Fragment 37: state / \bvendor\b

- Lines: `327-343`
- Realm: `unknown`
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

### `plugins/vendor/entities/entities/nut_vendor/shared.lua`

- Exists: `True`
- Resolved path: `E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\vendor\entities\entities\nut_vendor\shared.lua`
- Source root: `E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript`
- Realm: `shared/conditional`
- Note: Conditional realm evidence: validate SERVER/CLIENT branches manually.

#### Fragment 1: state / \bvendor\b

- Lines: `1-12`
- Realm: `shared/conditional`
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

#### Fragment 2: state / \bvendor\b

- Lines: `66-82`
- Realm: `shared/conditional`
- Classification: `state_or_ui_reference`

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

#### Fragment 3: state / \bprice\b

- Lines: `71-87`
- Realm: `shared/conditional`
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

#### Fragment 4: state / \bprice\b

- Lines: `92-108`
- Realm: `shared/conditional`
- Classification: `ui_presentation_logic`

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

#### Fragment 5: state / \bvendor\b

- Lines: `116-132`
- Realm: `shared/conditional`
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

## Validation Interpretation

This report extracts source evidence only.

Do not treat matches as confirmed causes without human/source review.

Use the extracted fragments to answer:

- Which file is authoritative?
- Which hook/listener/network path actually runs?
- Is the logic server-authoritative, client presentation-only, or mixed?
- Does the code mutate persisted state or only UI/item presentation metadata?

## Promotion Rule

Promote findings only after validation:

investigation -> source validation -> human validation -> subsystem docs -> doctrine/project memory
