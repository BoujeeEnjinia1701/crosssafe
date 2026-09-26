---
doc_id: CRS-CAL-001
title: CrossSafe sizing calculations
project: CrossSafe
doc_type: Calculation
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First issue for TRL 3 (flash timing, energy budget and autonomy, enclosure heat, radio link and latency, photometry screening, heights, wind load, clamps and footing, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002); sun-shielded heat case, anti-rotation bolt and keyed saddles, shielded enclosure wind area, cost
---

# CrossSafe sizing calculations

On paper, CrossSafe meets eleven of its fifteen requirements (five by calculation, six by design), has one at risk, and leaves three that only photometry, a site trial or a timed installation can settle. None is outright not met. The fixes Amish accepted on 2026-09-25 (CRS-DDR-001 and CRS-DDR-002) do their job. Gating the radar with a PIR sensor, together with the IA-21 flash sequence (each head lit 25 % of the time, not the 35 % assumed at TRL 2), cuts the daily load from about 29.8 to 16.0 Wh and lifts autonomy from about 4.1 to 7.7 days (R6 met, 5.4 days at -20 °C). The ventilated sun shield cuts the enclosure's rise in full sun from 14.7 to 3.9 K when dusty, so the interior stays at 53.9 °C at 50 °C ambient and charging continues up to 41.1 °C ambient (R8 met on paper). The 114.3 x 3.6 mm post reaches 44 % of yield in a 40 m/s gust (R9 target 60 %). An eccentric gust on the sign twists it with 175 N·m; on new posts an M10 through-bolt carries this at 12 % of its bearing resistance, and on existing poles keyed saddles hold on poles of about 70 mm and larger, so R9 stays at risk only on smaller poles. One assembly on an existing pole costs $332.00 against the $350 budget, and a two-sided crossing on existing poles $664.00 (R15 met). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B4], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that the device is safe to put beside a road. Photometry, detection, the battery in a sun-heated box, clamp preload and the foundation must be checked on hardware and by a qualified engineer, and the device needs road authority approval before any use on a public road. See CRS-PRC-001, Safety.

## Scope and method

The note checks every requirement in CRS-REQ-001 v0.4 against the design in CRS-PRC-001 v0.4 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and `derived()`, so heights, wind areas, the post section and the footing are those of the STEP files and drawing CRS-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`; it also writes `docs/04-calcs/results.csv`.

The design case is CRS-REQ-001's: a marked crossing on a two-lane road 7 m kerb to kerb, one assembly on each side, 300 activations of 20 s per day, 2.5 peak sun hours in the worst month and -20 to +50 °C ambient. Decisions referred to as D1 to D9 are in CRS-DDR-001; the sun shield and anti-rotation detail (E1, E2) are in CRS-DDR-002.

## Assumptions

*Table 1. Main assumptions.*

| Area | Assumption | Basis |
| --- | --- | --- |
| Flash pattern | 800 ms sequence, 75 per minute; each indication lit 4 x 50 ms per sequence | FHWA IA-21, checked on the FHWA page on 2026-09-25 |
| LED heads | 6 W per lit head in daytime; drivers 91 % efficient; no credit taken for night dimming | As CRS-PRC-001 v0.2; to be measured |
| Pilot light | 0.3 W, steady while flashing | Assumed |
| Standby | STM32WL-class radio in continuous LoRa receive 5.5 mA and controller plus PIR 0.1 mA, both at 3.3 V through an 80 % converter; 1 mA at 12.8 V for LED drivers off, fault indicator and BMS; charger self-consumption 4 mA at 12.8 V; radar 0.4 W when on | Typical class figures, assumed; the charger figure is written into BOM line 10 |
| Radar gating | The PIR keeps the radar on 25 % of the day at a busy site | Assumed; sensitivity at 50 % and ungated |
| Solar | 20 W panel; 2.5 peak sun hours worst month, 5 in a good month; panel heat and dust 0.85, MPPT 0.94, cell charge 0.95 | As CRS-PRC-001 v0.2, now split into factors |
| Battery | 12.8 V 12 Ah LiFePO4, 80 % usable; 70 % capacity at -20 °C; 80 % at end of life; charge 0 to 45 °C; discharge to about 60 °C | Typical LiFePO4 data |
| Heat | Clear-sky beam 900 W/m², diffuse 10 % of beam, sun at 70° elevation on the worst azimuth; combined convection and radiation 10 W/m²K; absorptance 0.45 clean light grey, 0.70 dusty; a ventilated shield passes 25 % of the solar gain; no credit for panel shade | Handbook ranges; the shield factor matches WWT-CAL-001 and is not measured |
| Radio | 8-byte packet, SF7, 125 kHz, coding rate 4/5, 8-symbol preamble, explicit header; +14 dBm; 2 dBi antennas; 1 dB cable each end; 25 dB allowance for a bus between the assemblies; -123 dBm sensitivity; up to 2 retries; 868 MHz band with 1 % duty cycle | LoRa time-on-air formula; screening values |
| Photometry | Amber LED 50 lm/W; optic 80 %; beam 20° wide by 10° high | Assumed, for screening only |
| Wind | 40 m/s gust; air 1.225 kg/m³; drag coefficient 1.2 on every part including the post; S235 post, yield 235 MPa | As CRS-REQ-001; not a code check |
| Clamps | Band tension 1,000 N; friction 0.2; torsion from a quarter-width eccentricity of the sign pressure | Tension assumed, to be measured; eccentricity is a common allowance for uneven gust pressure on signboards |
| Anti-rotation | M10 A4-70 through-bolt, stress area 58 mm², shear resistance 0.6 fub As / 1.25; post wall bearing 2.5 α fu d t / 1.25 with α = 0.5 and fu = 360 MPa; keyed saddle grip friction 0.4 | EN 1993-1-8 forms used as a screening check; the grip friction is assumed, to be measured |
| Footing | Non-constrained pole formula after IBC section 1807.3.2.1; lateral soil bearing 100 psf per ft of depth (clay), not doubled | Screening method; a local geotechnical and structural check governs |

## A. Flash time and pattern (R1, R4)

- **Time.** A 7 m crossing at 0.9 m/s takes 7.8 s; with 5 s added the set time is 12.8 s. The 20 s energy case covers crossings up to 13.5 m [A1].
- **Pattern.** IA-21 lights each indication for 200 ms of every 800 ms sequence, a duty of 25 %, not the 35 % assumed at TRL 2 [A2]. This alone cuts LED energy by 29 %.
- **Geometry.** Lenses of 140 x 62 mm exceed the 127 x 51 mm minimum; the bar bottom is at 2,100 mm and the sign's bottom point at 2,250 mm, so the bar sits directly under the sign as IA-21 allows [A3].

## B. Energy, autonomy and recovery (R6, R7)

- **Loads.** The lights flash 1.67 h a day. Four heads draw 6.59 W on average while flashing, 10.99 Wh a day; the pilot light adds 0.50 Wh and radio transmission 0.001 Wh [B1].
- **Standby.** Logic 23.1 mW, 12 V quiescent 12.8 mW, charger 51.2 mW and the gated radar 100 mW average: 187 mW, or 4.49 Wh a day [B2]. At TRL 2 standby was a lumped 0.6 W, almost half the load.
- **Daily load.** 16.0 Wh a day, against the TRL 2 estimate of 29.8 Wh [B3].
- **Autonomy.** 122.9 Wh usable gives 7.69 days; 5.38 days at -20 °C and 6.15 days at end of life. The 18 Ah fallback (not adopted) would give 11.5 days [B4].

*Table 2. Autonomy sensitivity [B5].*

| Case | Standby | Load | Autonomy |
| --- | --- | --- | --- |
| Baseline (PIR-gated radar, 25 % on) | 187 mW | 16.0 Wh/day | 7.69 days |
| Radar on 50 % of the day | 287 mW | 18.4 Wh/day | 6.69 days |
| TRL 2 controller (0.15 W) and a 10 mA charger, gated | 391 mW | 20.9 Wh/day | 5.89 days |
| Radar ungated (no PIR) | 487 mW | 23.2 Wh/day | 5.30 days |
| TRL 2 lumped standby (0.6 W) | 600 mW | 25.9 Wh/day | 4.75 days |

R6 holds in every case except the TRL 2 lump, which the build-up above replaces. The margin rests on a low self-consumption charger and on the PIR gating, both of which are in the BOM.

- **Harvest.** The chain from panel rating to stored energy is 75.9 % efficient. In the worst month the panel stores 38.0 Wh a day, a margin of 22.0 Wh. Break-even is 1.05 peak sun hours. At 5 peak sun hours the surplus is 59.9 Wh a day, which refills the battery from 20 % in 2.05 days [B6].
- **Currents.** Peak charge 1.25 A (0.10 C); average discharge while flashing 0.58 A, and 2.06 A in the 50 ms when all four heads are lit, so the 5 A battery fuse has margin [B7].

## C. Enclosure heat and the charging window (R8)

The 150 x 260 x 300 mm enclosure has 0.324 m² of surface and presents 0.0674 m² to a 70° sun on its worst azimuth [C2].

*Table 3. Enclosure temperature in full sun [C1, C3]. The dusty, shielded case is the design case (CRS-DDR-002).*

| Case | Rise over ambient | Interior at 45 °C | Interior at 50 °C | Charging stops above |
| --- | --- | --- | --- | --- |
| Clean light grey | 9.6 K | 54.6 °C | 59.6 °C | 35.4 °C ambient |
| Dusty | 14.7 K | 59.7 °C | 64.7 °C | 30.3 °C ambient |
| Dusty, with the ventilated shield (design) | 3.9 K | 48.9 °C | 53.9 °C | 41.1 °C ambient |

The BMS and charger stop charging above 45 °C cell temperature as R8 requires. Without a shield the device would lose harvest on hot, clear days above about 30 °C ambient, and at 50 °C ambient a dusty enclosure would reach 64.7 °C, above the typical 60 °C discharge limit of LiFePO4 cells. Amish accepted the recommended fix on 2026-09-25 (CRS-DDR-002): a ventilated white sun shield (part 18, about $8, as in WaterWatch and FieldNode) over the roof and three walls with a 25 mm air gap. With it the rise is 3.9 K, the interior 53.9 °C at 50 °C ambient and charging continues up to 41.1 °C ambient [C3], so R8 is met on paper. The steady-state model ignores the battery's thermal mass, which lags the peak, and gives no credit for shade from the panel 0.78 m above the enclosure top; the shield factor of 0.25 is borrowed from WWT-CAL-001 and not measured. Moving the enclosure under the panel's shadow is to be considered when the bracket is detailed.

## D. Radio link and latency (R3)

- **Time on air.** An 8-byte packet at SF7 and 125 kHz takes 36.1 ms [D1].
- **Latency.** Wake, transmit, receive and switch on the far side take 48 ms; with two retries after lost acknowledgements, 244 ms, inside the 500 ms target [D2].
- **Link budget.** Across 7 m with 25 dB of blockage from a bus, the far side receives -57.1 dBm, 65.9 dB above sensitivity; across 15 m, -63.7 dBm and 59.3 dB [D3]. The link will not limit the design; interference and regional band rules are the real questions.
- **Duty cycle.** Sixty activations in the busiest hour use 4.3 s of airtime per side against 36 s allowed at 1 % [D4].

## E. Photometry screening (R2)

A 6 W amber head with the assumed efficacy and a 20° x 10° beam gives about 3,939 cd on axis: 0.39 lx at a driver's eye at 100 m and 4.38 lx at 30 m. At 100 m the near-lane driver is 2.0° off axis horizontally and 0.6° below the head; at 30 m, 6.7° and 2.0°, both inside the beam [E1]. IA-21 requires the daytime intensity to meet the SAE J595 Class 1 yellow peak luminous intensity; that standard's figures were not available to check, so R2 is not verifiable at TRL 3. The numbers above are the input a photometric check will need, not a result.

## F. Heights, mounting and installation (R10, R11, R14)

- **Heights.** Button center 1,050 mm (R11: 0.9 to 1.1 m); light bar bottom 2,100 mm; enclosure bottom 2,850 mm (R14: 2.8 m), with the shield open at the bottom; radar arm at 2,600 mm with the PIR underside at 2,520 mm, so no part or cable of the sensing head is below 2.5 m; overall height 4,031 mm [F1].
- **Poles.** The band clamps fit 60 to 114.3 mm poles; the new-post variant uses 114.3 x 3.6 mm [F2].
- **Installation.** A task estimate for a two-person crew on an existing pole comes to 120 min, exactly the 2 h limit of R10, with the sun shield fitted to the enclosure on the ground and the keyed saddles in place of plain ones [F3]. Only a timed trial can settle it; Amish accepted that trial on 2026-09-25, and it is on hold with TRL 4.

## G. Wind, clamps and footing (R9)

- **Loads.** The dynamic pressure at 40 m/s is 980 Pa. Wind along the road, on the sign face, gives 1,419 N and a base moment of 3,434 N·m (sign 1,839, post 920, shielded enclosure 362, light bar 238 N·m) [G1]. The shield enlarges the enclosure's wind area. Wind across the road gives 759 N and 1,644 N·m, of which the panel is 416 N·m [G2]. Along the road governs.
- **Post.** *Table 4. Post stress in the 40 m/s gust [G3, G4].*

| Post | Section modulus | Stress | Share of S235 yield | R9 (60 %) |
| --- | --- | --- | --- | --- |
| 76.1 x 3.2 mm | 12,820 mm³ | 244 MPa | 104 % | Yields |
| 88.9 x 4.0 mm | 21,674 mm³ | 149 MPa | 63 % | Not met |
| 88.9 x 4.0 mm with a 600 mm sign | 21,674 mm³ | 118 MPa | 50 % | Met |
| 114.3 x 3.6 mm (decided, D3) | 33,593 mm³ | 102 MPa | 44 % | Met |

The TRL 2 figures (169 MPa and 72 % on the 88.9 mm post) counted the panel face-on in the same gust as the sign; here the two act in different wind directions. The top of the 114.3 mm post deflects about 30 mm (0.8 % of its height) in the gust [G5].

- **Clamps.** A gust whose pressure centre sits a quarter of the sign's width off the pole axis twists the sign clamps with 175 N·m. Two bands at the assumed 1,000 N tension resist about 144 N·m by friction on a 114.3 mm pole and only 75 N·m on a 60 mm pole [G6]. With plain saddles the sign could rotate on its pole in a storm. Amish accepted the recommended anti-rotation detail on 2026-09-25 (CRS-DDR-002):
  - **New posts:** an M10 through-bolt in the upper sign saddle (part 19). The 175 N·m couple puts 1,535 N on each post wall: 8 % of the bolt's shear resistance and 12 % of the wall's bearing resistance [G6b]. Met.
  - **Existing poles:** keyed saddles with serrated grip faces (part 20). At an assumed grip friction of 0.4 two bands resist 287 N·m on a 114.3 mm pole and 151 N·m on a 60 mm pole, so the sign holds on poles of about 70 mm and larger [G6c]. Smaller poles remain at risk, and the friction and band tension must be measured (TRL 4, on hold). A third band on small poles is proposed, awaiting Amish (CRS-DDR-002, N1).
- **Footing.** The resultant of 1,419 N (319 lbf) acts 2.42 m (7.9 ft) above the sidewalk. The non-constrained pole formula gives 1,776 mm of embedment for a 500 mm footing in clay, so the model uses 1,800 mm [G7]. This is a screening size; the local code and soil govern.
- **Existing poles.** An assembly adds 2,514 N·m at the sidewalk to the host pole [G8]. The pole owner must confirm the pole and its foundation can carry it; that check is outside this repo.

## H. Cost (R15)

The BOM has 20 lines, all priced. One assembly on an existing pole costs $332.00 (the shield and keyed saddles add $14.00), and $405.00 with its own post and anti-rotation bolt, footing concrete excluded [H1]. Against `budget_usd` of $350 that is $18.00 under on an existing pole and $55.00 over with a new post [H2]. Under D1 the budget covers the existing-pole assembly, so R15 is met. A two-sided crossing costs $664.00 on existing poles and $810.00 with new posts: $86.00 under and $60.00 over the $750 site-trial budget, which Amish accepted on 2026-09-25 for when a site trial starts (on hold with TRL 4) [H3].

## L. Results against every requirement

*Table 5. Requirement status at TRL 3 (also in `docs/04-calcs/results.csv`).*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R9 | Structure | 44 % of yield on the 114.3 mm post; bolt 12 % of bearing; keyed saddles hold on poles of 70 mm and up | 60 % of yield or less; no sign rotation | **At risk** (poles under about 70 mm) |
| R2 | Visibility | About 3,939 cd per head (screening) | Seen at 100 m in sun; dimmed at night | Not verifiable at TRL 3 |
| R5 | Detection quality | PIR wakes the radar; 1 s dwell | 5 % false, 2 % missed | Not verifiable at TRL 3 |
| R10 | Mounting | Fits 60 to 114.3 mm poles; bar at 2.1 m; about 120 min estimate | Fit; 2.1 m; 2 h | Not verifiable at TRL 3 (install time) |
| R3 | Activation and sync | 48 ms; 244 ms with two retries | 0.5 s or less | Met on paper |
| R6 | Autonomy | 7.7 days (5.4 at -20 °C; 6.2 at end of life) | 5 days or more | Met on paper |
| R7 | Energy balance | Break-even 1.05 peak sun hours; recovery 2.1 days | Neutral at 2.5 h; 3 days or fewer | Met on paper |
| R8 | Environment | 53.9 °C inside at 50 °C ambient (dusty, shielded); charging to 41.1 °C ambient | IP65; -20 to +50 °C; charge 0 to 45 °C | Met on paper |
| R15 | Affordable | $332.00 per assembly; $664.00 per crossing on existing poles | $350; $700 per crossing | Met on paper |
| R1 | Light geometry and pattern | 140 x 62 mm lenses; IA-21 pattern; bar under the sign | 127 x 51 mm min.; IA-21 | Met by design |
| R4 | Flash duration | 12.8 s for 7 m; 20 s energy case | L/0.9 + 5 s; 10 to 40 s | Met by design |
| R11 | Accessibility | Button 1.05 m; piezo; tone, tactile arrow, pilot light | 0.9 to 1.1 m; 22 N or less | Met by design |
| R12 | Fail-safe | Timer-limited flashing; local flashing without link; fault log | Never continuous | Met by design |
| R13 | Privacy | Presence and counts only | No images or audio | Met by design |
| R14 | Theft and vandal resistance | Enclosure bottom 2.85 m; lowest sensing part 2.52 m | 2.8 m; no cables below 2.5 m | Met by design |

## Checks against the TRL 2 figures

| Quantity | TRL 2 (CRS-PRC-001 v0.2) | TRL 3 (this note) | Reason |
| --- | --- | --- | --- |
| Flash time, 7 m | About 13 s | 12.8 s | Confirmed |
| LED energy | About 15.4 Wh/day | 10.99 Wh/day | IA-21 duty 25 %, not 35 % |
| Standby | About 14.4 Wh/day | 4.49 Wh/day | PIR gating (D2) and a component build-up |
| Daily load | About 29.8 Wh/day | 16.0 Wh/day | As above, plus the pilot light (D8) |
| Autonomy | About 4.1 days | 7.69 days | As above |
| Break-even | About 2.0 peak sun hours | 1.05 | Lower load |
| Recovery at 5 peak sun hours | About 2.7 days | 2.05 days | Lower load |
| Latency | About 0.1 s | 48 ms, 244 ms with retries | Confirmed |
| Base moment | About 3.7 kN·m | 3.43 kN·m | Panel and sign loads in different wind directions; shielded enclosure |
| 88.9 x 4 mm post | 169 MPa, 72 % | 149 MPa, 63 % | As above; still not met |
| 114.3 x 3.6 mm post | 110 MPa, 47 % | 102 MPa, 44 % | As above |
| Cost per assembly | $361 own post; $311 existing pole | $405.00; $332.00 | PIR, pilot light, larger post, sun shield, saddles, bolt |

CRS-PRC-001, CRS-REQ-001 and `README.md` have been brought in line with the TRL 3 column.
