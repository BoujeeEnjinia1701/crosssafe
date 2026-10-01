---
doc_id: CRS-REQ-001
title: CrossSafe requirements
project: CrossSafe
doc_type: Requirements
version: "0.5"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with status against the concept estimates
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: TRL 3 status from CRS-CAL-001; R15 redefined to the existing-pole assembly (CRS-DDR-001 D1); R1, R9 and R11 updated for D3, D4 and D8
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-09-30'
  author: Amish Chadha
  change: Status from CRS-CAL-001 v0.3 for the constructable design (CRS-DDR-003); R15 now not met on paper
---

# CrossSafe requirements

These requirements are checked by calculation in CRS-CAL-001 at TRL 3. Targets are still proposals, not yet validated with users or a road authority, and will be revised after co-design (see CRS-PRB-001). Where a local rule is stricter, the local rule wins. The design choices behind them were accepted by Amish on 2026-09-25 (CRS-DDR-001 and CRS-DDR-002).

The **design case** is a marked crossing on a two-lane road 7 m kerb to kerb, one CrossSafe assembly on each side, 300 activations of 20 s per day, 2.5 peak sun hours per day in the worst month, and an ambient range of -20 to +50 °C.

Table 1. Requirements and status at TRL 3 (CRS-CAL-001 v0.3, Table 5).

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 3 |
| --- | --- | --- | --- | --- |
| R1 | Warning light geometry and pattern | Two amber rectangular indications per face, each at least 127 x 51 mm (5 x 2 in); the FHWA IA-21 wig-wag sequence at 75 flashing sequences per minute; pattern set in firmware for other jurisdictions; an optional pedestrian pilot light where allowed | Design review against the pilot jurisdiction's rules | Met by design (140 x 62 mm lenses) |
| R2 | Visibility | Indications distinguishable by a driver at 100 m or more in direct sun (IA-21 cites SAE J595 Class 1 yellow peak intensity) and not glaring at night (automatic dimming) | Photometric calculation from LED data; later field check | Not verifiable at TRL 3 (screening: about 3,939 cd per head) |
| R3 | Activation | Push button and passive presence detection; both sides of the road flash within 0.5 s of a trigger on either side | Timing budget; later bench test | Met on paper (48 ms; 244 ms with two retries) |
| R4 | Flash duration | Set per site from crossing length / 0.9 m/s + 5 s, adjustable 10 to 40 s; a new trigger while flashing extends the time | Firmware review | Met by design (12.8 s for 7 m) |
| R5 | Detection quality | Passive detection triggers for a person waiting 1 s or more in the waiting zone; false activations 5 % or fewer of all activations; missed waiting pedestrians 2 % or fewer | Site trial with manual counts | Not verifiable at TRL 3 |
| R6 | Autonomy without sun | 5 days or more of design-case use from a full battery | Energy calculation | Met on paper (7.7 days; 5.4 at -20 °C) |
| R7 | Energy balance | Energy neutral at 2.5 peak sun hours; recover from 20 % to full in 3 days or fewer at 5 peak sun hours | Solar yield calculation | Met on paper (break-even 1.05 h; recovery 2.1 days) |
| R8 | Environment | Enclosures and connectors IP65 or better; operate -20 to +50 °C ambient; battery charges only at 0 to 45 °C cell temperature | Datasheets and heat balance; later spray and thermal tests | Met on paper with the sun shield (53.9 °C inside at 50 °C ambient when dusty; charging to 41.1 °C ambient) |
| R9 | Structure | Post and clamps carry the sign and panel in a 40 m/s gust with stress 60 % or less of yield; new posts are 114.3 x 3.6 mm (CRS-DDR-001 D3); the sign cannot rotate on its pole (anti-rotation bolt on new posts, keyed saddles on existing poles, CRS-DDR-002) | Wind load calculation | **At risk on poles under about 70 mm only: post 45 % of yield and bolt 12 % of bearing (met); keyed saddles resist 151 N·m on a 60 mm pole against 175 N·m** |
| R10 | Mounting | Fits the project's own post or an existing 60 to 114 mm pole with band clamps; sign bottom at 2.1 m or more (or local rule); two-person crew installs one assembly in 2 h or less | Design review; later timed trial | Not verifiable at TRL 3 (fit met; install estimate 120 min, at the limit) |
| R11 | Accessibility | Push button 0.9 to 1.1 m above the walking surface, operable with 22 N or less, with an audible and tactile acknowledgement and a pedestrian-facing pilot light | Design review with disability groups | Met by design (button at 1.05 m), to be checked in co-design |
| R12 | Fail-safe behavior | Never flashes continuously; a fault (low battery, open LED, lost radio link) is shown on a maintenance indicator and logged; with the link lost, each side still flashes on a local trigger | Firmware review; fault injection later | Met by design |
| R13 | Privacy | No images or audio are recorded or leave the device; only activation counts, faults and battery state are logged or sent | Design review | Met by design |
| R14 | Theft and vandal resistance | Battery, charger and controller 2.8 m or more above the walking surface; security fasteners; no exposed cables below 2.5 m | Design review | Met by design (enclosure bottom 2.85 m; sensing head 2.515 m and up) |
| R15 | Affordable | Parts for one assembly on an existing pole $350 or less (the prototype `budget_usd` covers, CRS-DDR-001 D1); parts for a two-sided crossing on existing poles $700 or less. Crossings that need new posts are costed and reported, not held to this target | Priced BOM (`bom/bom.csv`) | **Not met on paper ($360.00 per assembly, $10.00 over; $720.00 per crossing, $20.00 over)**; new posts $433.00 and $866.00 |

## Requirements at risk or not verifiable

One requirement is not met on paper (R15, cost), one is at risk and three need evidence that a paper study cannot give.

- **R15 not met on paper after the design for construction (CRS-DDR-003).** The saddles, mounting plate, panel bracket, radar arm, battery strap and fixings that make every part buildable and fixed add $28.00: one assembly on an existing pole is $360.00 against $350, and a crossing $720.00 against $700. Raising `budget_usd` to $375 is proposed, awaiting Amish (design decisions register, item 1).

- **R9 at risk on small poles.** The 114.3 x 3.6 mm post meets the stress target at 45 % of yield, and a 1,800 mm embedment in a 500 mm footing is a screening size. On new posts the M10 through-bolt stops the sign rotating with a wide margin. On existing poles the keyed saddles hold on poles of about 70 mm and larger at an assumed grip friction of 0.4; below that the sign could still slip. A third band on small poles is proposed, awaiting Amish (CRS-DDR-002, N1). On existing poles the host pole must carry about 2.5 kN·m more at the sidewalk, which the owner must confirm.
- **R8 met on paper after the sun shield (CRS-DDR-002).** Unshielded, a dusty enclosure ran 14.7 K above ambient and reached 64.7 °C at 50 °C ambient; with the ventilated shield the rise is 3.9 K and the interior 53.9 °C, below the typical 60 °C discharge limit. The shield factor is borrowed, not measured.
- **R2, R5 and R10 are not verifiable at TRL 3.** R2 and R5 decide whether drivers respond and whether passive detection is trusted.
- **R6, not met at TRL 2, is now met on paper** after the PIR gating (D2).

## Assumptions

The full list is in CRS-CAL-001, Table 1. The main ones are:

- LED heads draw about 6 W each when lit in daytime and are lit 25 % of each IA-21 sequence; LED drivers are about 91 % efficient.
- Standby about 187 mW: radio in continuous receive and controller about 23 mW, 12 V quiescent about 13 mW, charger about 51 mW, radar 0.4 W on 25 % of the day under PIR gating.
- Solar system efficiency about 76 % from panel rating to energy stored (panel heat and dust 0.85, MPPT 0.94, cell charge 0.95).
- Walking speed of 0.9 m/s allows for children and older people; the US MUTCD basis is faster, and local rules decide.
- Gust wind speed of 40 m/s and a drag coefficient of 1.2 for every part; S235 steel for the post; band tension 1,000 N; keyed saddle grip friction 0.4; a ventilated shield passes 25 % of the solar gain.
