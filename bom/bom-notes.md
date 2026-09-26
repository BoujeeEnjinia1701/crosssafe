# BOM notes

- Costs are indicative USD parts prices for one beacon assembly at TRL 3. Suppliers are named by type; no vendor is selected.
- Every line is priced. One assembly on an existing pole (lines 1 to 13 and 15 to 17) is $318.00; with its own 114.3 mm post (line 14, marked "Variant only") it is $388.00. `docs/04-calcs/sizing.py` sums the file and prints both totals (CRS-CAL-001, section H).
- Budget: `budget_usd` in `project.yaml` is $350 and, under CRS-DDR-001 D1 (adopted for TRL 3, open for Amish's review), covers one assembly on an existing pole: $32.00 under. A new-post assembly is $38.00 over.
- A two-sided crossing is $636.00 on existing poles and $776.00 with new posts. The recommended $750 site-trial budget is awaiting Amish (CRS-DDR-001 O2); `budget_usd` is unchanged.
- Changes at TRL 3: PIR wake sensor (line 16, D2), pedestrian pilot light (line 17, D8), post changed to 114.3 x 3.6 mm with a 1.8 m embedment (line 14, D3), controller specified as the FieldNode STM32WL-class radio core (line 11, D7), charger self-consumption limit added (line 10).
- Item numbers match the callouts in `media/exploded.png`. Item 15 has no callout.
- Installation, footing concrete, traffic management and road authority fees are not included.
