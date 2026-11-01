---
doc_id: CRS-PRS-001
title: CrossSafe product requirements and specifications
project: CrossSafe
doc_type: Product requirements and specifications
version: "0.1"
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-31'
  author: Amish Chadha
  change: "Migrated from CRS-REQ-001 v0.8 (R1 to R15 became PR-001 to PR-015, same numbers) and traced to the new user requirements CRS-URS-001; PR-016 to PR-019 added; PR-008 restated for the 55 °C charge limit (CRS-DDR-005); status from CRS-CAL-001 v0.7"
---

# CrossSafe product requirements and specifications

What the pole-top beacon (option A, the TRL 2 design, recommended in CRS-OPT-001 and awaiting Amish) must do, each requirement traced to a user need in CRS-URS-001 (links in CRS-RTM-001). This document replaces CRS-REQ-001, whose numbers R1 to R15 are kept in the Was column. Targets are still proposals, not yet validated with users or a road authority; where a local rule is stricter, the local rule wins.

The **design case** is a marked crossing on a two-lane road 7 m kerb to kerb, one CrossSafe assembly on each side, 300 activations of 20 s per day, 2.5 peak sun hours per day in the worst month, and an ambient range of -20 to +50 °C. The design choices behind these requirements were accepted by Amish on 2026-09-25 and 2026-10-02 (CRS-DDR-001 to CRS-DDR-003).

*Table 1. Product requirements and specifications. Status at TRL 3 from CRS-CAL-001 v0.7 (`python docs/04-calcs/sizing.py`).*

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001, UR-006 | Performance | Light geometry and pattern | Two amber rectangular indications per face, each at least 127 x 51 mm (5 x 2 in); the FHWA IA-21 wig-wag sequence at 75 flashing sequences per minute; pattern set in firmware for other jurisdictions; an optional pedestrian pilot light where allowed | 2 indications of 127 x 51; 75 sequences per minute | min; nominal | mm; per min | Design review against the pilot jurisdiction's rules | Met by design | R1 |
| PR-002 | UR-001, UR-014 | Performance | Visibility | Indications distinguishable by a driver at 100 m or more in direct sun (IA-21 cites SAE J595 Class 1 yellow peak intensity) and not glaring at night (automatic dimming) | 100 m daytime | min | m | Photometric calculation from LED data; later field check | Not verifiable at TRL 3 | R2 |
| PR-003 | UR-002 | Performance | Activation and sync | Push button and passive presence detection; both sides of the road flash within 0.5 s of a trigger on either side | 0.5 | max | s | Timing budget; later bench test | Met on paper | R3 |
| PR-004 | UR-004 | Performance | Flash duration | Set per site from crossing length / 0.9 m/s + 5 s, adjustable 10 to 40 s; a new trigger while flashing extends the time | L / 0.9 + 5; 10 to 40 | range | s | Firmware review | Met by design | R4 |
| PR-005 | UR-002 | Performance | Detection quality | Passive detection triggers for a person waiting 1 s or more in the waiting zone; false activations 5 % or fewer of all activations; missed waiting pedestrians 2 % or fewer | 5 false; 2 missed | max | % | Site trial with manual counts | Not verifiable at TRL 3 | R5 |
| PR-006 | UR-005 | Electrical | Autonomy without sun | 5 days or more of design-case use from a full battery. At risk: 4.3 days at -20 °C and end-of-life capacity together (CAL-001 C7); the 18 Ah pack or a heater is the fix, awaiting Amish (O4) | 5 | min | days | Energy calculation | At risk | R6 |
| PR-007 | UR-005 | Electrical | Energy balance | Energy neutral at 2.5 peak sun hours; recover from 20 % to full in 3 days or fewer at 5 peak sun hours | 2.5; 3 at 5 peak sun hours | max | peak sun hours; days | Solar yield calculation | Met on paper | R7 |
| PR-008 | UR-006 | Materials | Environment | Enclosures and connectors IP65 or better; operate -20 to +50 °C ambient; battery charges only at 0 to 55 °C cell temperature (cell and BMS rated for it, CRS-DDR-005; 45 °C in CRS-REQ-001 v0.8) | IP65; -20 to +50; charge 0 to 55 | range | °C | Datasheets and heat balance; later spray and thermal tests | Met on paper | R8 |
| PR-009 | UR-006 | Physical architecture | Structure | Post and clamps carry the sign and panel in a 40 m/s gust with stress 60 % or less of yield; new posts are 114.3 x 3.6 mm (CRS-DDR-001 D3); the sign cannot rotate on its pole (anti-rotation bolt on new posts, keyed saddles on existing poles, CRS-DDR-002). On an existing pole the pole owner verifies the pole: the added 2,601 N m alone needs a section modulus of at least 18,447 mm3 (CAL-001 G9); the 76 mm limit is raised to Amish (O5) | 60 of yield; 40 m/s gust | max | % of yield; m/s | Wind load calculation | Met on paper | R9 |
| PR-010 | UR-008 | Physical architecture | Mounting | Fits the project's own post or an existing 76 to 114 mm pole with band clamps (60 to 75 mm poles only after a slip-torque test confirms the keyed saddle's grip, with a third saddle and band at the sign); the prototype's panel socket fits free-topped poles of about 114 mm; sign bottom at 2.1 m or more (or local rule); two-person crew installs one assembly in 2 h or less | 76 to 114; 2.1; 120 | range; min; max | mm; m; min | Design review; later timed trial | Not verifiable at TRL 3 | R10 |
| PR-011 | UR-003 | Usability | Accessibility | Push button 0.9 to 1.1 m above the walking surface, operable with 22 N or less, with an audible and tactile acknowledgement and a pedestrian-facing pilot light | 0.9 to 1.1; 22 | range; max | m; N | Design review with disability groups | Met by design | R11 |
| PR-012 | UR-007 | Safety | Fail-safe behavior | Never flashes continuously; a fault (low battery, open LED, lost radio link) is shown on a maintenance indicator and logged; with the link lost, each side still flashes on a local trigger | never continuous | n/a | n/a | Firmware review; fault injection later | Met by design | R12 |
| PR-013 | UR-011 | Software | Privacy | No images or audio are recorded or leave the device; only activation counts, faults and battery state are logged or sent | no images or audio | n/a | n/a | Design review | Met by design | R13 |
| PR-014 | UR-012 | Safety | Theft and vandal resistance | Battery, charger and controller 2.8 m or more above the walking surface; security fasteners; no exposed cables below 2.5 m | 2.8; 2.5 | min | m | Design review | Met by design | R14 |
| PR-015 | UR-009 | Packaging and transport | Affordable | Parts for one assembly on an existing pole $350 or less (the prototype `budget_usd` covers, CRS-DDR-001 D1); parts for a two-sided crossing on existing poles $700 or less. Crossings that need new posts are costed and reported, not held to this target | 350; 700 per crossing | max | USD | Priced BOM (`bom/bom.csv`) | Over target | R15 |
| PR-016 | UR-013 | Safety | Flash area | The two lit heads shall subtend no more than the WCAG 2.1 general flash area (6 msr) at 1.5 m from the light bar, used as an analogue for photosensitivity; no road standard has been checked | 6 | max | msr | Analysis (CAL-001 section I); a road-authority and clinical-safety review is to assess | At risk | R16 |
| PR-017 | UR-006 | Materials | Light bar temperature | The light bar interior shall stay at or below the upper operating limit of an LED traffic signal module at 50 °C ambient, dusty, in full sun (worst case: sun at the worst elevation, LEDs flashing continuously, white finish, CRS-DDR-005) | 74 | max | °C | Analysis (CAL-001 C5); datasheet of the heads bought | Met on paper | R17 |
| PR-018 | UR-014 | Performance | Warning in time to stop | The seeing distance of PR-002 shall exceed the stopping distance at 60 km/h (2.5 s reaction, 3.4 m/s2 braking); holds only while PR-002 holds | 100 vs 83 | max | m | Analysis (CAL-001 section I); AASHTO values to confirm | Met on paper | R18 |
| PR-019 | UR-010 | Physical architecture | Buildable and repairable | Every made part shall be cut, drilled, bent or welded from stock sections with ordinary workshop tools; every other part is bought; no special tooling | n/a | n/a | n/a | Build plan BLD-001 (paper); model of 117 parts, none bare (CAL-001) | Met by design | R19 |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. PR-015 (cost) is over its value-engineering target and PR-006 and PR-016 are at risk; all three are in the section below.

## Requirements at risk or not verifiable

One requirement is over its value-engineering target on paper (PR-015, was R15, cost), two are at risk (PR-006, autonomy, 4.3 days when the -20 °C and end-of-life cases are combined; and PR-016, flash area, a screen against an analogue limit: 7.7 msr at 1.5 m against 6 msr; see hazard H5 in CRS-RSK-001) and three need evidence that a paper study cannot give (PR-002, PR-005 and PR-010).

- **R15 over the value-engineering target after the design for construction (CRS-DDR-003).** The saddles, mounting plate, panel bracket, radar arm, battery strap and fixings that make every part buildable and fixed add $28.00, and the bezels and visors on the four LED heads add $4.00: the estimated cost of one assembly on an existing pole is $364.00 against the $350 target ($14.00 over), and of a crossing $728.00 against $700 ($28.00 over). The target is a hypothetical control target, not a limit; cost drivers and savings worth trying are in the Value engineering section of the design decisions register.

- **R9 met on paper on poles of 76 mm and larger.** The 114.3 x 3.6 mm post meets the stress target at 45 % of yield, and a 1,800 mm embedment in a 500 mm footing is a screening size. On new posts the M10 through-bolt stops the sign rotating with a wide margin. On existing poles the keyed saddles hold on poles of about 70 mm and larger at an assumed grip friction of 0.4, so R9 is met on paper for the 76 to 114.3 mm range the existing-pole kit is now limited to (decided 2026-10-02, CRS-DDR-002, N1). The friction and band tension are assumptions, and the 191 N·m resistance on a 76 mm pole is only 9 % above the 175 N·m load. A slip-torque test on the keyed saddle must confirm the grip before the kit is used below 76 mm, when a third saddle and band would bring 60 to 75 mm poles back. On existing poles the host pole must carry about 2.5 kN·m more at the sidewalk, which the owner must confirm.
- **R8 met on paper after the sun shield (CRS-DDR-002) and the 55 °C charge limit (CRS-DDR-005).** Unshielded, a dusty enclosure ran 14.7 K above ambient and reached 64.7 °C at 50 °C ambient; with the ventilated shield the rise is 3.9 K and the interior 53.9 °C, below the typical 60 °C discharge limit. The shield factor is borrowed, not measured.
- **R2, R5 and R10 are not verifiable at TRL 3.** R2 and R5 decide whether drivers respond and whether passive detection is trusted.
- **R6, not met at TRL 2, is now met on paper** after the PIR gating (D2).

## Assumptions

The full list is in CRS-CAL-001, Table 1. The main ones are:

- LED heads draw about 6 W each when lit in daytime and are lit 25 % of each IA-21 sequence; LED drivers are about 91 % efficient.
- Standby about 187 mW: radio in continuous receive and controller about 23 mW, 12 V quiescent about 13 mW, charger about 51 mW, radar 0.4 W on 25 % of the day under PIR gating.
- Solar system efficiency about 76 % from panel rating to energy stored (panel heat and dust 0.85, MPPT 0.94, cell charge 0.95).
- Walking speed of 0.9 m/s allows for children and older people; the US MUTCD basis is faster, and local rules decide.
- Gust wind speed of 40 m/s and a drag coefficient of 1.2 for every part; S235 steel for the post; band tension 1,000 N; keyed saddle grip friction 0.4; a ventilated shield passes 25 % of the solar gain.
