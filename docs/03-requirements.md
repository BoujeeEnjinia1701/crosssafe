---
doc_id: CRS-REQ-001
title: CrossSafe requirements
project: CrossSafe
doc_type: Requirements
version: "0.2"
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
---

# CrossSafe requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users or a road authority, and will be checked by calculation at TRL 3 and revised after co-design (see CRS-PRB-001). Where a local rule is stricter, the local rule wins.

The **design case** is a marked crossing on a two-lane road 7 m kerb to kerb, one CrossSafe assembly on each side, 300 activations of 20 s per day, 2.5 peak sun hours per day in the worst month, and an ambient range of -20 to +50 °C.

Table 1. Requirements and status against the TRL 2 estimates in CRS-PRC-001.

| ID | Requirement | Target | Verification (TRL 3 or later) | Status at TRL 2 |
| --- | --- | --- | --- | --- |
| R1 | Warning light geometry and pattern | Two amber rectangular indications per face, each at least 127 x 51 mm (5 x 2 in); wig-wag pattern at 75 flashing sequences per minute, as in FHWA IA-21; pattern set in firmware for other jurisdictions | Design review against the pilot jurisdiction's rules | Met by design |
| R2 | Visibility | Indications distinguishable by a driver at 100 m or more in direct sun and not glaring at night (automatic dimming) | Photometric calculation from LED data; later field check | Unverified |
| R3 | Activation | Push button and passive presence detection; both sides of the road flash within 0.5 s of a trigger on either side | Timing budget; later bench test | Met by estimate (radio link about 0.1 s) |
| R4 | Flash duration | Set per site from crossing length / 0.9 m/s + 5 s, adjustable 10 to 40 s; a new trigger while flashing extends the time | Firmware review | Met by design (about 13 s for 7 m) |
| R5 | Detection quality | Passive detection triggers for a person waiting 1 s or more in the waiting zone; false activations 5 % or fewer of all activations; missed waiting pedestrians 2 % or fewer | Site trial with manual counts | Unverified |
| R6 | Autonomy without sun | 5 days or more of design-case use from a full battery | Energy calculation | **Not met: about 4.1 days (estimate)** |
| R7 | Energy balance | Energy neutral at 2.5 peak sun hours; recover from 20 % to full in 3 days or fewer at 5 peak sun hours | Solar yield calculation | Met by estimate (break-even about 2.0 h; recovery about 2.7 days) |
| R8 | Environment | Enclosures and connectors IP65 or better; operate -20 to +50 °C ambient; battery charges only at 0 to 45 °C cell temperature | Datasheets; later spray and thermal tests | Met by design, thermal margin in sun unverified |
| R9 | Structure | Post and clamps carry the sign and panel in a 40 m/s gust with stress 60 % or less of yield | Wind load calculation | **Not met with the modeled 89 x 4 mm post: about 169 MPa, 72 % of S235 yield (estimate)**; met with a 114.3 x 3.6 mm post (about 110 MPa, 47 %) |
| R10 | Mounting | Fits the project's own post or an existing 60 to 114 mm pole with band clamps; sign bottom at 2.1 m or more (or local rule); two-person crew installs one assembly in 2 h or less | Design review; later timed trial | Unverified (install time) |
| R11 | Accessibility | Push button 0.9 to 1.1 m above the walking surface, operable with 22 N or less, with an audible and tactile acknowledgement and a pedestrian-facing confirmation light | Design review with disability groups | Met by design, to be checked in co-design |
| R12 | Fail-safe behavior | Never flashes continuously; a fault (low battery, open LED, lost radio link) is shown on a maintenance indicator and logged; with the link lost, each side still flashes on a local trigger | Firmware review; fault injection at TRL 4 | Met by design |
| R13 | Privacy | No images or audio are recorded or leave the device; only activation counts, faults and battery state are logged or sent | Design review | Met by design |
| R14 | Theft and vandal resistance | Battery, charger and controller 2.8 m or more above the walking surface; security fasteners; no exposed cables below 2.5 m | Design review | Met by design (enclosure at about 2.85 m) |
| R15 | Affordable | Parts for one assembly $350 or less; parts for a two-sided crossing $700 or less | Priced BOM (`bom/bom.csv`) | **Not met: about $361 per assembly, about $722 per crossing (estimate)**; about $311 per assembly on an existing pole |

## Requirements not met or at risk

- **R6 not met.** About 123 Wh usable against about 30 Wh/day gives about 4.1 days. Options are in CRS-PRC-001 (gate the radar with a PIR sensor, or fit an 18 Ah battery).
- **R15 not met.** About 3 % over for one assembly and for a crossing when the project supplies its own posts.
- **R9 not met with the modeled post.** A 76 x 3.2 mm post would yield (about 287 MPa); the modeled 89 x 4 mm post reaches about 72 % of yield against a 60 % target. A 114.3 x 3.6 mm post, a 600 mm sign, or mounting on an existing lighting pole meets it; see CRS-PRC-001.
- **R2 and R5 are unverified** and carry the most risk: they decide whether drivers respond and whether passive detection is trusted.

## Assumptions

- LED heads draw about 6 W each when lit in daytime and are lit about 35 % of each flash cycle; LED drivers are about 91 % efficient.
- Standby draw about 0.6 W: radar about 0.4 W, controller and receiving radio about 0.15 W, charger about 0.05 W.
- Solar system efficiency about 76 % from panel rating to energy available to store (temperature, dust, wiring, MPPT and charging).
- Walking speed of 0.9 m/s allows for children and older people; the US MUTCD basis is faster, and local rules decide.
- Gust wind speed of 40 m/s and a drag coefficient of 1.2 for flat plates; S235 steel for the post.
