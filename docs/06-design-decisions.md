---
doc_id: CRS-DEC-001
title: CrossSafe design decisions register
project: CrossSafe
doc_type: Design decisions register
version: "0.5"
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-30'
  author: Amish Chadha
  change: Register opened with the open decisions from the review note, CRS-DDR-001 to CRS-DDR-003 and the build plan work
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Amish approved the recommendations for all open decisions 1 to 8 on 2026-10-02 (CRS-DDR-003 accepted; existing-pole kit limited to 76 mm and up); moved to decisions made"
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Value engineering figures updated for the head bezels and visors: USD 364.00, USD 14.00 over the target"
- version: "0.5"
  date: '2026-10-31'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade: open decisions O1 to O5 (concept choice, 55 C charge limit, flash area review, cost and cold autonomy, existing-pole check); STEM check fixes F1 to F3 recorded as decided under the standing instruction of 2026-10-23 (CRS-DDR-005); concept selection CRS-DDR-004"
---

# CrossSafe design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 0. Decisions awaiting Amish (kit 1.9.1 upgrade, 2026-10-31).*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| O1 | Concept: keep A (pole-top beacon), take C (pull-up panel), or both | A; B; C; A and C as two tiers | Proposed, awaiting Amish: A and C are within 10 % (138 against 128), so no pick is made; the author leans to A, with C as a low-cost tier | Nothing changes if A stays; C would need its own BOM, build plan and calculations at TRL 3, and a changed pitch | CRS-DDR-004, CRS-OPT-001 |
| O2 | Confirm the 55 C battery charge limit (cell and BMS rated for it) | Keep 45 C (the battery starves on 48 to 50 C days); 55 C; another fix | Proposed, awaiting Amish: 55 C against the cell datasheet; it is a safety limit even though the fix was made under the standing instruction | BOM line 9; PR-008 | CRS-DDR-005, CRS-STM-001 S3 |
| O3 | Flash area at the button (PR-016 At risk: 7.7 msr at 1.5 m against a 6 msr analogue) | Accept; move the button further from the bar; a diffuser or dimmer; get a clinical-safety review | Proposed, awaiting Amish: ask the pilot road authority and a clinical-safety reviewer; moving the bar is a safety trade-off | Light bar and button heights | CRS-RSK-001 H5 |
| O4 | Cost over the value-engineering target ($364.00 against $350), and autonomy at -20 C with an end-of-life battery (4.3 days, PR-006 At risk) | Accept both; cheaper quotes for the sign and enclosure; drop the pilot light; for autonomy the 18 Ah pack (11.5 days nominal, price to quote, above $364) or a heater | Proposed, awaiting Amish: accept the cost gap and keep the 12 Ah pack for a warm-climate pilot; use the 18 Ah pack for a cold one | BOM line 9 | CRS-CAL-001 H and C7 |
| O5 | Existing poles: the 76 mm limit decided on 2026-10-02 covers sign grip only; the 2,601 N m the kit adds needs a pole section modulus of 18,447 mm3 or more (a 76.1 x 3.2 mm pole has 12,820) | Keep 76 mm and make the pole owner verify; raise the limit to poles of 88.9 x 4.0 mm and up; own post only | Proposed, awaiting Amish: keep the kit and require owner verification of the pole, stated in the build plan and PR-009 | PR-009, R10 scope | CRS-CAL-001 G9, CRS-STM-001 review |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The enclosure model: its internal plate and boss positions, its lug kit, and that the lid is on the 260 x 300 face away from the back | They set the internal plate layout, the lug holes in the mounting plate and the shield fit | CRS-DDR-003, P4 |
| 2 | The solar panel frame has a flat back lip at least 15 mm wide on its long edges | The rails bolt through it | CRS-DDR-003, P8 |
| 3 | Each LED head's flange covers a 128 x 50 mm window, its body is no deeper than 25 mm, and its screw pattern | They set the light bar windows and leave 16 mm between facing heads | CRS-DDR-003, P3 |
| 4 | The push-button station fixes to a flat face with two bolts 40 mm apart (or an adaptor plate is needed) | It bolts to a saddle's two tapped holes | CRS-DDR-003, P9 |
| 5 | The radar housing's two base screws are 50 mm apart and the PIR's neck is 12 mm or less | They set the radar arm's holes | CRS-DDR-003, P7 |
| 6 | The battery, charger and controller board fit the sizes in the build plan (151 x 95 x 98, 40 x 90 x 60, 180 x 100 mm) | The internal layout and the battery strap are drawn to them | CRS-DDR-003, P4 |
| 7 | The band and buckle reach 1,000 N of tension with the banding tool, and the keyed saddle's grip friction is about 0.4 | CRS-CAL-001 assumes both for the sign torsion; until a slip-torque test confirms them the existing-pole kit is limited to poles of 76 mm and larger (decided 2026-10-02) | CRS-CAL-001, [G6c] |
| 8 | The test post's top is square and open (or capped flush) so the bracket cap sits on it | The socket's cap rests on the pole's top edge | CRS-DDR-003, P8 |

## Value engineering

Value-engineering target: USD 350 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 364.00 (USD 14.00 over the target). A crossing needs two assemblies: USD 728.00 against a target of USD 700; with new posts USD 437.00 and USD 874.00, which are costed and reported, not held to the target.

Main cost drivers: the eight keyed saddles in place of two (USD 18.00 more), the enclosure mounting plate (USD 8.00), the panel bracket (USD 6.00 more), the radar arm and battery strap (USD 3.00) and the fixings (USD 4.00 more) and the bezels and visors bought with the LED heads (USD 4.00), less the sign maker's brackets (USD 5.00) and the bought band brackets (USD 6.00). All prices are indicative until quoted at TRL 4.

Savings worth trying: a cheaper enclosure or sign quote, aiming at the USD 14.00 gap. The site-trial target of USD 750 for a two-sided crossing applies when a trial starts (on hold with TRL 4).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D9: `budget_usd` covers one assembly on an existing pole; PIR gating of the radar; existing poles first and a 114.3 x 3.6 mm post where a new one is needed; FHWA IA-21 baseline; button plus passive detection; LoRa side-to-side link; FieldNode radio core with CrossSafe's own 12 V power; pedestrian pilot light where allowed; no change to the pitch | Amish: "i accept all your recommendations, go with them across all repos." | CRS-DDR-001, CRS-DDR-002 |
| 2026-09-25 | $750 site-trial value-engineering target for a two-sided crossing, to apply when a site trial starts (on hold with TRL 4); `budget_usd` stays $350 | Amish, same instruction | CRS-DDR-002, O2 |
| 2026-09-25 | Ventilated sun shield on the enclosure (E1); anti-rotation bolt on new posts and keyed saddles on existing poles (E2); timed installation trial, on hold with TRL 4 (E3) | Amish, same instruction | CRS-DDR-002 |
| 2026-09-26 | CrossSafe chosen for the first batch of product renders | Amish | REVIEW 2026-09-26 |
| 2026-09-30 | Build plan format approved; open decisions kept in this register, not in the build plan | Amish: "this is the correct build plan ... this is a good quality document format. Extend this across all the other repos" | This register; CRS-BLD-001 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | CRS-DDR-003 (changes accepted on 2026-10-02, below) |
| 2026-10-02 | Design for construction accepted: the changes P1 to P11 of CRS-DDR-003 and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | CRS-DDR-003, Tables 1 and 2 and A3 |
| 2026-10-02 | Panel mount on existing poles: the prototype is built for free-topped poles of about 114 mm (option c); a side-of-pole panel arm on two more saddles (option b) is designed once the pilot site's poles are known | Amish: "i approve your recommendations for all 555 open decisions." | CRS-DDR-003, A2 |
| 2026-10-02 | Sign rotation on small poles: the existing-pole kit is limited to poles of 76 mm and larger (option b) until a slip-torque test on the keyed saddle confirms the assumed grip; then a third saddle and band at the sign (option a) brings 60 to 75 mm poles back. This changes the earlier recommendation of (a) | Amish: "i approve your recommendations for all 555 open decisions." | CRS-DDR-002, N1 |
| 2026-10-02 | Pilot partner: a United States city traffic engineering department with a Safe Routes to School or Vision Zero programme, since the design follows FHWA IA-21. First candidate to approach: a North Texas city near the team | Amish: "i approve your recommendations for all 555 open decisions." | CRS-DDR-001, O1; CRS-DDR-002 |
| 2026-10-02 | Visors and bezels on the LED heads: added to the model (CRS-CAL-001 v0.6 includes them in the light bar wind area); head modules are bought with visors | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 2 |
| 2026-10-02 | Louvre slots in the sun shield: appearance only until the shield is measured; the shield stays plain sheet | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 3 |
| 2026-10-02 | Sign colour: fluorescent yellow-green in the renders; the sheeting is bought to the local road authority's design | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 4 |
| 2026-10-02 | Small appearance differences in the renders (pilot light housing, saddle flange at the sign, band screw housings) accepted as appearance detail | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 5 |
| 2026-10-31 | STEM check row S3 failed (battery would not charge above 45 C cell temperature on a 50 C day): LiFePO4 pack and BMS rated for charge to 55 C specified in BOM line 9 | Decided under the standing instruction of 2026-10-23 (Amish, "when a STEM check row fails, propose and implement the best fix"); the 55 C safety limit is also open decision O2 | `docs/decisions/0005-stem-check-fixes.md` (F1) |
| 2026-10-31 | STEM check row S5 failed in the independent review's worst case (light bar 76.0 C against 74 C): white finish specified in BOM line 2 | Decided under the standing instruction of 2026-10-23 | `docs/decisions/0005-stem-check-fixes.md` (F3) |
| 2026-10-31 | STEM check row S22 failed (option C panel stops from a fall at about 62 g): hydraulic end-of-travel damper, bracket, two M4 screws and an EPDM pad added to option C | Decided under the standing instruction of 2026-10-23 | `docs/decisions/0005-stem-check-fixes.md` (F2) |
