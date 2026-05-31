# Runtime Chain: vendor purchase price label cleanup

## Status

- Artifact type: promoted runtime chain
- Source schema: `runtime_chain.v1`
- Confidence: **high**
- Score: **0.7484**

## Scope

vendor purchase item setData vendorSPrice invData ItemDataChanged populateItems

## Chain

1. **cl_vendor.lua** — realm=`client`, `plugins/vendor/derma/cl_vendor.lua:75-87`
2. **cl_vendor.lua** — realm=`client`, `plugins/vendor/derma/cl_vendor.lua:82-94`
3. **cl_vendor.lua** — realm=`client`, `plugins/vendor/derma/cl_vendor.lua:154-166`
4. **cl_vendor.lua** — realm=`client`, `plugins/vendor/derma/cl_vendor.lua:158-170`
5. **cl_vendor.lua** — realm=`client`, `plugins/vendor/derma/cl_vendor.lua:167-179`
6. **cl_vendor.lua** — realm=`client`, `plugins/vendor/derma/cl_vendor.lua:169-181`
7. **cl_vendor.lua** — realm=`client`, `plugins/vendor/derma/cl_vendor.lua:172-184`
8. **cl_vendor.lua** — realm=`client`, `plugins/vendor/derma/cl_vendor.lua:198-210`
9. **cl_vendor.lua** — realm=`client`, `plugins/vendor/derma/cl_vendor.lua:229-241`
10. **targeted_validation step 3** — realm=`unknown`
11. **targeted_validation step 9** — realm=`unknown`
12. **targeted_validation step 2** — realm=`unknown`
13. **targeted_validation step 8** — realm=`unknown`
14. **targeted_validation step 4** — realm=`unknown`
15. **targeted_validation step 5** — realm=`unknown`
16. **targeted_validation step 6** — realm=`unknown`
17. **targeted_validation step 7** — realm=`unknown`
18. **hook.Run** — realm=`unknown`, `docs/runtime/runtime_chains/vendor_purchase_price_label_cleanup.md`
19. **setData** — realm=`unknown`, `docs/runtime/runtime_chains/vendor_purchase_price_label_cleanup.md`
20. **sync** — realm=`unknown`, `docs/runtime/runtime_chains/vendor_purchase_price_label_cleanup.md`
21. **vendor_purchase_price_label_cleanup.md** — realm=`unknown`, `docs/runtime/runtime_chains/vendor_purchase_price_label_cleanup.md`
22. **init.lua** — realm=`unknown`, `plugins/vendor/entities/entities/nut_vendor/init.lua:51-63`
23. **init.lua** — realm=`unknown`, `plugins/vendor/entities/entities/nut_vendor/init.lua:209-221`
24. **init.lua** — realm=`unknown`, `plugins/vendor/entities/entities/nut_vendor/init.lua:284-296`

## Missing causal steps

- none

## Promotion notes

- This document is a durable runtime-chain anchor.
- It does not modify raw Lua.
- It should be regenerated or superseded if targeted validation contradicts any step.
