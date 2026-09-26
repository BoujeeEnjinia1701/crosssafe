# BOM notes

- Costs are indicative USD parts prices for one beacon assembly at TRL 3. Suppliers are named by type; no vendor is selected.
- Every line is priced. One assembly on an existing pole (all lines except 14 and 19) is $332.00; with its own 114.3 mm post and anti-rotation bolt (lines 14 and 19, marked "Variant only") it is $405.00. `docs/04-calcs/sizing.py` sums the file and prints both totals (CRS-CAL-001, section H).
- Budget: `budget_usd` in `project.yaml` is $350 and, under CRS-DDR-001 D1 (decided by Amish, 2026-09-25), covers one assembly on an existing pole: $18.00 under. A new-post assembly is $55.00 over.
- A two-sided crossing is $664.00 on existing poles and $810.00 with new posts. Amish accepted the $750 site-trial budget on 2026-09-25 (CRS-DDR-001 O2); it applies when a site trial starts, which is on hold with TRL 4, so `budget_usd` is unchanged.
- Changes at TRL 3: PIR wake sensor (line 16, D2), pedestrian pilot light (line 17, D8), post changed to 114.3 x 3.6 mm with a 1.8 m embedment (line 14, D3), controller specified as the FieldNode STM32WL-class radio core (line 11, D7), charger self-consumption limit added (line 10).
- Changes under CRS-DDR-002 (recommendations accepted by Amish, 2026-09-25): ventilated sun shield (line 18, $8.00), anti-rotation bolt for new posts (line 19, $3.00, variant) and two keyed sign saddles (line 20, $6.00).
- Item numbers match the callouts in `media/exploded.png`. Item 15 has no callout.
- Installation, footing concrete, traffic management and road authority fees are not included.
