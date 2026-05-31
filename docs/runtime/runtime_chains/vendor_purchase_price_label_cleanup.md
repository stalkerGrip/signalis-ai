# Runtime Chain: vendor_purchase_price_label_cleanup

Confidence: `high`

## Question

Why do vendor price labels sometimes remain visible after buying items?

## Chain

### 1. purchase_transfer

- Status: `evidence_found`
- Source: `E:/steam/steamapps/common/GarrysMod/garrysmod/gamemodes/nutscript/plugins/gridinv/sv_transfer.lua`
- Line: `218`
- Evidence source: `targeted_validation`
- Matched terms: `plugins/gridinv/sv_transfer.lua, vendorsellitem, oldinventory.vendor, item:setdata("vendorsprice", nil, client), item:setdata("vendorqty", nil, client), item:setdata("vendormqty", nil, client)`

```text
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
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
225: 				end
226: 			end
E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
plugins/gridinv/sv_transfer.lua
E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
```

### 2. inventory_membership_sync

- Status: `evidence_found`
- Source: `E:/steam/steamapps/common/GarrysMod/garrysmod/gamemodes/nutscript/plugins/gridinv/sv_transfer.lua`
- Line: `16`
- Evidence source: `targeted_validation`
- Matched terms: `inventory.items`

```text
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
18: 	local status, reason = hook.Run("CanItemBeTransfered", item, oldInventory, inventory, client)
19: 
20: 	if (status == false) then client:notify(reason or "You can't do that right now.") return end
21: 	local context = {
22: 		client = client,
23: 		item = item,
24: 		from = oldInventory,
E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
plugins/gridinv/sv_transfer.lua
E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
```

### 3. item_initial_sync

- Status: `evidence_found`
- Source: `E:/steam/steamapps/common/GarrysMod/garrysmod/gamemodes/nutscript/plugins/gridinv/sv_transfer.lua`
- Line: `78`
- Evidence source: `targeted_validation`
- Matched terms: ``

```text
70: 			inventory.vendor:HandleStock(item.uniqueID, false, qty, item.isStackable, client)
71: 		else
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
85: 			vendorSellItem = true
86: 		else
E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
plugins/gridinv/sv_transfer.lua
E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
```

### 4. purchase_metadata_cleanup

- Status: `evidence_found`
- Source: `E:/steam/steamapps/common/GarrysMod/garrysmod/gamemodes/nutscript/plugins/gridinv/sv_transfer.lua`
- Line: `218`
- Evidence source: `targeted_validation`
- Matched terms: `vendorsprice, vendorqty, vendormqty, vendorbprice, setdata`

```text
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
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
225: 				end
226: 			end
E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
plugins/gridinv/sv_transfer.lua
E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
```

### 5. item_metadata_network_sync

- Status: `evidence_found`
- Source: `E:/steam/steamapps/common/GarrysMod/garrysmod/gamemodes/nutscript/plugins/gridinv/sv_transfer.lua`
- Line: `218`
- Evidence source: `targeted_validation`
- Matched terms: `item:setdata`

```text
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
220: 					item:setData("vendorMQty", nil, client)
221: 					if (oldInventory.vendor.items[item.uniqueID])
222: 					then
223: 						item:setData("vendorBPrice", oldInventory.vendor.items[item.uniqueID].buyPrice, client)
224: 					end
225: 				end
226: 			end
E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
plugins/gridinv/sv_transfer.lua
E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
```

### 6. client_item_data_apply

- Status: `evidence_found`
- Source: `E:/steam/steamapps/common/GarrysMod/garrysmod/gamemodes/nutscript/plugins/gridinv/sv_transfer.lua`
- Line: `78`
- Evidence source: `targeted_validation`
- Matched terms: ``

```text
70: 			inventory.vendor:HandleStock(item.uniqueID, false, qty, item.isStackable, client)
71: 		else
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
85: 			vendorSellItem = true
86: 		else
E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
plugins/gridinv/sv_transfer.lua
E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
```

### 7. grid_inventory_ui_refresh

- Status: `evidence_found`
- Source: `E:/steam/steamapps/common/GarrysMod/garrysmod/gamemodes/nutscript/plugins/gridinv/sv_transfer.lua`
- Line: `78`
- Evidence source: `targeted_validation`
- Matched terms: ``

```text
70: 			inventory.vendor:HandleStock(item.uniqueID, false, qty, item.isStackable, client)
71: 		else
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
85: 			vendorSellItem = true
86: 		else
E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
plugins/gridinv/sv_transfer.lua
E:\steam\steamapps\common\GarrysMod\garrysmod\gamemodes\nutscript\plugins\gridinv\sv_transfer.lua
```

## Confidence Reasons

- `authoritative_purchase_transfer_source_validated`
- `client_ui_refresh_present`
- `item_metadata_sync_boundary_present`
- `targeted_validation:client_item_data_apply`
- `targeted_validation:grid_inventory_ui_refresh`
- `targeted_validation:inventory_membership_sync`
- `targeted_validation:item_initial_sync`
- `targeted_validation:item_metadata_network_sync`
- `targeted_validation:purchase_metadata_cleanup`
- `targeted_validation:purchase_transfer`

## Promotion Notes

- Promoted from deterministic runtime chain candidate.
- This document is a semantic runtime-chain artifact, not a raw source patch.
- Raw Lua bugfixing is intentionally deferred until investigation pipeline reliability is proven.
