---
doc_id: CRS-DEC-001
title: CrossSafe design decisions register
project: CrossSafe
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
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
---

# CrossSafe design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

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
| 2026-09-30 | Make the design physically buildable while drawing the build plan | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | CRS-DDR-003 (changes accepted on 2026-10-02, below) |
| 2026-10-02 | Design for construction accepted: the changes P1 to P11 of CRS-DDR-003 and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | CRS-DDR-003, Tables 1 and 2 and A3 |
| 2026-10-02 | Panel mount on existing poles: the prototype is built for free-topped poles of about 114 mm (option c); a side-of-pole panel arm on two more saddles (option b) is designed once the pilot site's poles are known | Amish: "i approve your recommendations for all 555 open decisions." | CRS-DDR-003, A2 |
| 2026-10-02 | Sign rotation on small poles: the existing-pole kit is limited to poles of 76 mm and larger (option b) until a slip-torque test on the keyed saddle confirms the assumed grip; then a third saddle and band at the sign (option a) brings 60 to 75 mm poles back. This changes the earlier recommendation of (a) | Amish: "i approve your recommendations for all 555 open decisions." | CRS-DDR-002, N1 |
| 2026-10-02 | Pilot partner: a United States city traffic engineering department with a Safe Routes to School or Vision Zero programme, since the design follows FHWA IA-21. First candidate to approach: a North Texas city near the team | Amish: "i approve your recommendations for all 555 open decisions." | CRS-DDR-001, O1; CRS-DDR-002 |
| 2026-10-02 | Visors and bezels on the LED heads: added to the model, and the light bar wind area, at the next calculation revision; head modules are bought with visors | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 2 |
| 2026-10-02 | Louvre slots in the sun shield: appearance only until the shield is measured; the shield stays plain sheet | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 3 |
| 2026-10-02 | Sign colour: fluorescent yellow-green in the renders; the sheeting is bought to the local road authority's design | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 4 |
| 2026-10-02 | Small appearance differences in the renders (pilot light housing, saddle flange at the sign, band screw housings) accepted as appearance detail | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26, item 5 |
