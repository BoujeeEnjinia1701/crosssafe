---
doc_id: CRS-DEC-001
title: CrossSafe design decisions register
project: CrossSafe
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-01'
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
---

# CrossSafe design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design for construction changes P1 to P11 (keyed saddles and bands for every part on the pole, sign nearer the pole, folded light bar, mounting plate, radar arm, welded panel bracket and rails, gland layout, anti-rotation bolt through the sign) | (a) accept; (b) ask for a different arrangement of any of them | (a) | The whole build plan | CRS-DDR-003, Table 1 and A3 |
| 2 | Panel mount on existing poles that the post-top socket does not fit (poles other than about 114 mm, poles that are taller or carry a luminaire) | (a) reducing sleeves for 76 and 89 mm poles; (b) a side-of-pole panel arm on two more saddles; (c) limit the existing-pole kit to free-topped poles of about 114 mm | (b), designed once the pilot site's poles are known; the prototype uses (c) | Panel bracket (section 3.8) for site kits; not the prototype | CRS-DDR-003, A2 |
| 3 | Sign rotation on existing poles under about 70 mm, where keyed saddles alone do not hold the 175 N·m gust torsion (R9 at risk) | (a) a third saddle and band at the sign on poles under 76 mm; (b) limit the existing-pole range to 76 mm and up; (c) a through-bolt where the pole owner allows drilling | (a) | One more saddle and band on small poles; not the prototype (114.3 mm post) | CRS-DDR-002, N1 |
| 4 | Pilot partner, site and jurisdiction, including a road authority willing to review the design | Not yet named | None yet; no preference stated | Antenna band, sign design and colour, flash pattern, mounting heights, whether the pilot light is allowed | CRS-DDR-001, O1; CRS-DDR-002 |
| 5 | Visors and bezels on the LED heads (in the renders, not in the model) | (a) add them to the model and the wind area; (b) leave them out | (a): they cut sun phantom on the lenses | Head modules bought with visors; light bar wind area | REVIEW 2026-09-26, item 2 |
| 6 | Louvre slots in the sun shield walls (in the renders, not in the model) | (a) keep as appearance only until the shield is measured; (b) adopt now | (a) | Sun shield (section 3.9) stays plain sheet | REVIEW 2026-09-26, item 3 |
| 7 | Sign colour shown in the renders (fluorescent yellow-green) | (a) show it in renders and leave the colour to the road authority; (b) another colour | (a) | Sign sheeting is bought to the local design | REVIEW 2026-09-26, item 4 |
| 8 | Small appearance differences in the renders (pilot light housing 36 mm, saddle flange at the sign, band screw housings turned away) | (a) accept as appearance detail; (b) bring the renders into line with the model | (a); the renders are stale anyway after item 2 | None | REVIEW 2026-09-26, item 5 |

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The enclosure model: its internal plate and boss positions, its lug kit, and that the lid is on the 260 x 300 face away from the back | They set the internal plate layout, the lug holes in the mounting plate and the shield fit | CRS-DDR-003, P4 |
| 2 | The solar panel frame has a flat back lip at least 15 mm wide on its long edges | The rails bolt through it | CRS-DDR-003, P8 |
| 3 | Each LED head's flange covers a 128 x 50 mm window, its body is no deeper than 25 mm, and its screw pattern | They set the light bar windows and leave 16 mm between facing heads | CRS-DDR-003, P3 |
| 4 | The push-button station fixes to a flat face with two bolts 40 mm apart (or an adaptor plate is needed) | It bolts to a saddle's two tapped holes | CRS-DDR-003, P9 |
| 5 | The radar housing's two base screws are 50 mm apart and the PIR's neck is 12 mm or less | They set the radar arm's holes | CRS-DDR-003, P7 |
| 6 | The battery, charger and controller board fit the sizes in the build plan (151 x 95 x 98, 40 x 90 x 60, 180 x 100 mm) | The internal layout and the battery strap are drawn to them | CRS-DDR-003, P4 |
| 7 | The band and buckle reach 1,000 N of tension with the banding tool, and the keyed saddle's grip friction is about 0.4 | CRS-CAL-001 assumes both for the sign torsion | CRS-CAL-001, [G6c] |
| 8 | The test post's top is square and open (or capped flush) so the bracket cap sits on it | The socket's cap rests on the pole's top edge | CRS-DDR-003, P8 |

## Value engineering

Value-engineering target: USD 350 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 360.00 (USD 10.00 over the target). A crossing needs two assemblies: USD 720.00 against a target of USD 700; with new posts USD 433.00 and USD 866.00, which are costed and reported, not held to the target.

Main cost drivers: the eight keyed saddles in place of two (USD 18.00 more), the enclosure mounting plate (USD 8.00), the panel bracket (USD 6.00 more), the radar arm and battery strap (USD 3.00) and the fixings (USD 4.00 more), less the sign maker's brackets (USD 5.00) and the bought band brackets (USD 6.00). All prices are indicative until quoted at TRL 4.

Savings worth trying: a cheaper enclosure or sign quote, aiming at the USD 10.00 gap. The site-trial target of USD 750 for a two-sided crossing applies when a trial starts (on hold with TRL 4).

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items D1 to D9: `budget_usd` covers one assembly on an existing pole; PIR gating of the radar; existing poles first and a 114.3 x 3.6 mm post where a new one is needed; FHWA IA-21 baseline; button plus passive detection; LoRa side-to-side link; FieldNode radio core with CrossSafe's own 12 V power; pedestrian pilot light where allowed; no change to the pitch | Amish: "i accept all your recommendations, go with them across all repos." | CRS-DDR-001, CRS-DDR-002 |
| 2026-09-25 | $750 site-trial value-engineering target for a two-sided crossing, to apply when a site trial starts (on hold with TRL 4); `budget_usd` stays $350 | Amish, same instruction | CRS-DDR-002, O2 |
| 2026-09-25 | Ventilated sun shield on the enclosure (E1); anti-rotation bolt on new posts and keyed saddles on existing poles (E2); timed installation trial, on hold with TRL 4 (E3) | Amish, same instruction | CRS-DDR-002 |
| 2026-09-26 | CrossSafe chosen for the first batch of product renders | Amish | REVIEW 2026-09-26 |
| 2026-09-30 | Build plan format approved; open decisions kept in this register, not in the build plan | Amish: "this is the correct build plan ... this is a good quality document format. Extend this across all the other repos" | This register; CRS-BLD-001 |
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | CRS-DDR-003 (changes open for his review, open decision 2) |
