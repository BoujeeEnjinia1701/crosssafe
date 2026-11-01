---
doc_id: CRS-DDR-005
title: CrossSafe STEM check fixes
project: CrossSafe
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-31'
  author: Amish Chadha
  change: "Three STEM check rows failed on first run (S3 battery charge limit, S5 light bar temperature, S22 panel stop) and were fixed in the same session under Amish's standing instruction of 2026-10-23; one safety limit also listed for his confirmation"
---

# 0005: STEM check fixes

- **Date:** 2026-10-31
- **Status:** decided under Amish's standing instruction of 2026-10-23 ("when a STEM check row fails, propose and implement the best fix for the design and its constructability in the same session"). The 55 C safety limit in F1 is also listed in CRS-DEC-001 as "Proposed, awaiting Amish" for confirmation.

## Context

The first run of `docs/04-calcs/stem_check.py` failed two rows, and the worst-case check asked for by the independent reviewer (CRS-STM-001) failed a third. None of the fixes changes the working principle, pitch or scope of its option.

## Options considered

*Table 1. Failed rows and fixes.*

| # | Row | First run | Options | Fix |
| --- | --- | --- | --- | --- |
| F1 | S3, option A, battery charging on a hot day | With the 45 C charge limit of CRS-REQ-001 R8 the cell (ambient plus 3.9 K) is above its limit for most of the sun at a 50 C peak: 9 % of the sun usable, 8.5 Wh/day stored against a 16.0 Wh/day load; the battery empties in about 16 days | (a) specify a LiFePO4 pack and BMS rated for charge to 55 C; (b) a larger panel (does not help, the charger is off); (c) move the battery to the shade under the panel (does not remove the sun heat); (d) a thermal mass or a fan (adds parts and power) | (a): BOM line 9 states "charge-rated to 55 C"; the price is unchanged and to quote; PR-008 and CRS-CAL-001 C4 restated: 98.7 Wh/day stored |
| F3 | S5, option A, light bar temperature | In the worst case (sun at the elevation that maximises the sunlit area, dusty, LEDs flashing continuously) the charcoal bar reaches 76.0 C at 50 C ambient against the 74 C upper limit of an LED traffic signal module | (a) a white finish (alpha 0.55 dusty, assumed): 70.8 C; (b) a ventilated shield on the bar (adds parts and cost); (c) derate the LEDs (cuts the light, PR-002) | (a): finish stated in BOM line 2 (white powder coat, no cost change); the render colour of the bar in the appearance model still shows charcoal (appearance, awaiting Amish) |
| F2 | S22, option C, the released panel hitting its stop | From a 250 mm fall onto a 4 mm EPDM pad the panel stops at about 62 g, which would tear the sheeting and the fixings | (a) a hydraulic end-of-travel damper with 25 mm stroke (10 g); (b) a slower fall by friction (unreliable); (c) a counterweight (adds mass, a new part) | (a): buffer damper, bracket, two M4 screws and an EPDM pad added to option C in `cad/src/crs_options.py` (40 parts, 10.9 kg, about $6 added to the estimate) |

## Decision

All three fixes were made as in the last column. F1 is a specification change within the cell's rated range, but a charge limit is a safety limit, so Amish is asked to confirm 55 C against the datasheet of the cell bought (CRS-DEC-001, open decision O1). The BMS cut-off is not removed or defeated; it is set to the cell's own rating, and the cut-off at 0 C stays.

## Consequences

CRS-CAL-001 moves to v0.7 (section C4), CRS-PRS-001 states the 55 C limit in PR-008, and BOM line 9 carries the rating. Lithium cells charged hot age faster; the cell life at 55 C is to assess in CRS-RSK-001 (hazard H2). F2 adds one bought part to option C only. F3 depends on an assumed dust-soiled absorptance of 0.55 for a white finish and is Plausible, not closed; it is measured at TRL 4.
