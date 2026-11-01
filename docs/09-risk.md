---
doc_id: CRS-RSK-001
title: CrossSafe risk register and hazard analysis
project: CrossSafe
doc_type: Risk register
version: "0.1"
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-31'
  author: Amish Chadha
  change: "First risk register, preliminary hazard analysis and design FMEA (kit 1.9.1 upgrade); scores are the author's first estimate"
---

# CrossSafe risk register and hazard analysis

The top risks are that detection and visibility cannot be shown on paper (H3, F5), that the flash area near the button is above an analogue limit (H5, PR-016 At risk), and that a hot battery is a safety trade-off awaiting Amish (H2, O2). CrossSafe is a research and educational prototype at TRL 3; nothing here is a statement that the device is safe to put beside a road. Method: STANDARDS section 23. Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high), by the author, first pass.

## Project risk register

*Table 1. Project risks.*

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | The pilot road authority will not accept a non-standard beacon | IA-21 and MUTCD status for this form not yet checked; local rules vary | No site; the project stays on paper | 3 | 5 | Design lead | Early review of the design against local rules (TRL 4); keep the pattern in firmware |
| P2 | Cost stays above the value-engineering target | Saddles, plate, bracket and visors added for construction (CRS-DDR-003) | A school or market group cannot fund a crossing | 4 | 3 | Design lead | Quotes for the sign and enclosure; Amish decides O4 |
| P3 | Detection quality is not good enough (false or missed activations) | PIR plus radar behaviour in rain, wind and crowds is unknown | Drivers learn to ignore it, or pedestrians are not warned | 3 | 4 | Design lead | The button always works; site trial with manual counts (TRL 4) |
| P4 | Hot-box battery ages quickly at the 55 C charge limit | CRS-DDR-005 raises the limit; shield factor is borrowed, not measured | Short battery life, early replacement | 3 | 3 | Design lead | Cell datasheet and ageing data (to assess); measure the shield |
| P5 | Pole owner refuses a clamp-on kit | Utility poles are not the road authority's | No mounting point | 3 | 3 | Pilot partner | Own-post variant is costed ($437.00) |
| P6 | Theft or vandalism takes the panel or battery | Panels and batteries have resale value | Lost device, cost | 3 | 3 | Local technician | Mount at 2.8 m or more; security fasteners (PR-014) |
| P7 | The author's scoring of the options is wrong | Judgment from first-order numbers | Wrong concept continues | 2 | 3 | Design lead | Both A and C go to Amish; co-design tests UR-001 and UR-006 first |
| P8 | Autonomy falls below 5 days in a cold region with an old battery and no heater | Charging inhibited below 0 C; end-of-life capacity 80 %; 70 % at -20 C (CAL-001 C7) | Beacon goes dark in a long cold spell | 3 | 4 | Design lead | 18 Ah pack or a heater (O4); site climate check |
| P9 | The existing pole cannot carry the 2,601 N m the kit adds | Thin or corroded pole; 76.1 x 3.2 mm pole has too little section modulus (CAL-001 G9) | Pole bends or falls | 3 | 5 | Pole owner | Owner verifies the pole; own-post variant; Amish decides O5 |

## Preliminary hazard analysis

*Table 2. Hazards.*

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Sign, bar or panel falls on a person | Wind overload, band slip, corrosion, vehicle strike | Head or crush injury | 5 | 2 | Post at 45 % of yield in a 40 m/s gust (PR-009); keyed saddles; bar at 2.1 m or higher; all fasteners security type | Medium: wind and strike loads are assumed; site check needed |
| H2 | Lithium battery overheats, vents or burns | Hot box, overcharge, short circuit, crush | Fire, toxic gas, burns | 5 | 2 | LiFePO4 chemistry; BMS with low-temperature cut-off; 5 A fuse at the terminal; shield; battery at 2.8 m; charge limit set to the cell's rating (CRS-DDR-005) | Medium: charge at 55 C is a safety trade-off awaiting Amish (O2) |
| H3 | Pedestrian steps out trusting a warning that is not working | Fault, dead battery, lost link, missed detection | Collision | 5 | 3 | Fault indicator and log (PR-012); timer-limited flashing; the sign still stands; wording that the device does not stop traffic | High until a trial: detection and visibility are not verifiable at TRL 3 (PR-002, PR-005) |
| H4 | Fall from a ladder or lift during installation | Working at 4 m beside a road | Fall injury, traffic strike | 4 | 2 | Two-person crew; traffic control per local rules; shield fitted on the ground; install plan in the build plan | Medium |
| H5 | Photosensitive reaction or discomfort from the flashing | Lit area of the bar near the button (7.7 msr at 1.5 m against a 6 msr analogue); five pulses a second in a sequence | Headache, in rare cases a seizure | 4 | 2 | Bar faces the road; the bar is above eye height (centre at 2.17 m) and faces the road; dimming at night; review by the road authority and a clinical-safety reviewer (to assess) | Open: PR-016 At risk; Amish decides O3 |
| H6 | Night glare or dazzle for drivers | Full-power amber at night | Reduced vision, a crash | 4 | 2 | Automatic dimming (PR-002); lens visors | Medium: dimming levels not set |
| H7 | Electric shock or burns from the panel and wiring | 20 W panel open circuit near 22 V; 12 V battery with 154 Wh | Burn from a short circuit | 3 | 2 | Low voltage only; fuse; covered cable entries; enclosure at 2.8 m | Low |
| H8 | Cuts and pinches while building the made parts | Sheet metal edges, drill, grinder | Cuts | 2 | 3 | Edges broken (kit model includes edge breaks); gloves and guards in BLD-001 safety stops | Low |
| H9 | Radio interference with other devices | 868 MHz LoRa duty cycle; US band differs | Interference, rule breach | 2 | 2 | Duty cycle 4.3 s against 36 s per hour (S8); US band to assess in REG | Low |

## Design FMEA (first pass, P3)

*Table 3. Failure modes of option A. RPN = severity x occurrence x detection (detection 1 easy to catch, 5 hard).*

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Light bar and LED heads | Show the IA-21 pattern | Head stays dark | No warning although the sign says one | LED driver failure, open circuit | 5 | 3 | 3 | 45 | Open-LED detection in firmware (PR-012) |
| F2 | Light bar and LED heads | Show the IA-21 pattern | Moisture inside the bar | LED corrosion, short circuit, reduced light | Failed seal at the visor or cover | 4 | 3 | 4 | 48 | Seal detail and a drain lip in the model; inspect yearly |
| F3 | Controller and radio board | Start both sides within 0.5 s | Link lost | Only the local side warns | Antenna damage, blockage, interference | 3 | 3 | 2 | 18 | Local flashing without link (PR-012); fault log |
| F4 | Controller and radio board | Limit flash time | Timer fails, flashing continues | Driver learns to ignore it; battery drained | Firmware fault | 4 | 2 | 2 | 16 | Hardware watchdog and a fixed upper limit (PR-012); to specify in firmware at TRL 4 |
| F5 | Presence radar and PIR | Detect a waiting pedestrian | Missed detection | Pedestrian is not warned | Occlusion, rain, a child below the beam | 5 | 3 | 4 | 60 | The button remains; trial counts (PR-005) |
| F6 | Presence radar and PIR | Detect a waiting pedestrian | False activation | Warnings with nobody waiting; ignored | Wind, traffic, animals, a branch | 3 | 4 | 3 | 36 | PIR gates the radar; threshold set in trial |
| F7 | Battery and BMS | Store energy for 5 days or more | Battery cut-off in cold or heat | No power, no warning | Charging below 0 C, or above the rated limit | 4 | 3 | 3 | 36 | BMS cut-off; 55 C rated cell (CRS-DDR-005); low-battery alarm |
| F8 | Battery and BMS | Store energy safely | Thermal runaway | Fire in the enclosure | Overcharge, short, heat | 5 | 1 | 3 | 15 | LiFePO4, BMS, fuse, shield, 2.8 m mounting |
| F9 | Solar panel and bracket | Charge the battery | Shaded or dirty panel | Less charge than 38 Wh/day | Dust, bird droppings, leaves | 3 | 4 | 2 | 24 | Margin of 22 Wh/day and break-even at 1.05 peak sun hours; clean yearly |
| F10 | Enclosure and sun shield | Keep the battery below 60 C | Shield blocked or missing | Interior above 60 C | Fouled slots, lost shield | 4 | 2 | 3 | 24 | Shield part of the kit; check at inspection; measure at TRL 4 |
| F11 | Keyed pole saddles and bands | Hold the sign and enclosure on the pole | Band slackens, sign twists | Sign points away from the road | Creep, corrosion, vandalism | 4 | 3 | 3 | 36 | Keyed saddles; two bands; check at inspection |
| F12 | Post and footing | Carry wind loads | Footing too shallow for the soil | Post leans in a storm | Soil softer than assumed | 5 | 2 | 3 | 30 | Site check; deeper footing; the model uses 1,800 mm |
| F13 | Push-button station | Start the warning; confirm by tone and light | Button jams or is out of reach | No activation, or the user cannot press it | Dirt, vandalism, height error | 4 | 3 | 3 | 36 | Passive detection still works; button at 1.05 m (PR-011); co-design |
| F14 | Wiring and glands | Carry power and signals | Water enters at a gland | Short circuit, corrosion | Wrong gland, loose nut | 4 | 3 | 3 | 36 | Glands at the enclosure floor; drip loop; inspect |

Highest RPN: F5 (60), F2 (48) and F1 (45). Failures that put a person at risk (F5, F8, F12) are kept on the list even when their RPN is lower, because their severity is 5.

Options B and C have their own failure modes, not analysed here beyond the STEM check; they would be analysed if Amish picks one (O1).
