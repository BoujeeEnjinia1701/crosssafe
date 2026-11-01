---
doc_id: CRS-CAL-001
title: CrossSafe sizing calculations
project: CrossSafe
doc_type: Calculation
version: "0.7"
status: Draft
date: '2026-10-31'
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
- version: "0.3"
  date: '2026-09-30'
  author: Amish Chadha
  change: Re-run for the constructable design (CRS-DDR-003); enclosure mounting plate in the wind area, PIR height, BOM of 23 lines; R15 now not met on paper
- version: "0.4"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target
- version: "0.5"
  date: '2026-10-02'
  author: Amish Chadha
  change: "N1 recorded as decided on 2026-10-02 (existing-pole kit 76 mm and up until a slip-torque test); text only, no number changed"
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Re-run for the approved decisions: R10 range 76 to 114.3 mm and R9 restated (met on paper for that range); visors in the light bar wind area; line 3 re-priced; cost $364.00"
- version: "0.7"
  date: '2026-10-31'
  author: Amish Chadha
  change: "Kit 1.9.1 upgrade. STEM check fix CRS-DDR-005: battery charge limit 55 C (was 45 C), with the hot-day charging window (C4); new sections C5 (light bar heat), I (flash area and stopping distance) and M (requirement trace to PR ids); R8 restated; R16 to R19 added; the part count of the model is now 117 with every fastener, weld and washer"
---

# CrossSafe sizing calculations

On paper, CrossSafe meets thirteen of its nineteen requirements (six by calculation, seven by design), has one not met (cost, R15), two at risk (R6, autonomy when the cold and end-of-life cases are taken together, and R16, flash area, a screen against an analogue limit) and leaves three that only photometry, a site trial or a timed installation can settle. Version 0.7 adds the STEM check fixes of CRS-DDR-005: with the 45 °C charge limit of the earlier versions the battery would stop charging for most of the sun on a 48 to 50 °C day and empty in about 16 days in a sustained hot spell, so the cell is specified for charge to 55 °C (section C4), and the light bar gets a white finish because a charcoal one would reach 76 °C in the worst case (section C5). The independent review of CRS-STM-001 added the sensitivity of section C6 and the cold-day limit of section C7. The one over target is cost (R15): the saddles, mounting plate, panel bracket and fixings that make the design buildable (CRS-DDR-003, 2026-09-30) and the bezels and visors on the LED heads take the estimated cost of one assembly $14.00 over its $350 value-engineering target. The fixes Amish accepted on 2026-09-25 (CRS-DDR-001 and CRS-DDR-002) do their job. Gating the radar with a PIR sensor, together with the IA-21 flash sequence (each head lit 25 % of the time, not the 35 % assumed at TRL 2), cuts the daily load from about 29.8 to 16.0 Wh and lifts autonomy from about 4.1 to 7.7 days (R6 met, 5.4 days at -20 °C). The ventilated sun shield cuts the enclosure's rise in full sun from 14.7 to 3.9 K when dusty, so the interior stays at 53.9 °C at 50 °C ambient and charging continues up to 51.1 °C ambient with the 55 °C charge limit (R8 met on paper). The 114.3 x 3.6 mm post reaches 45 % of yield in a 40 m/s gust (R9 target 60 %). An eccentric gust on the sign twists it with 175 N·m; on new posts an M10 through-bolt carries this at 12 % of its bearing resistance, and on existing poles keyed saddles hold on poles of about 70 mm and larger, so R9 is met on paper for the 76 to 114.3 mm range of the existing-pole kit (it was at risk on 60 mm poles, which the kit no longer covers). The estimated cost of one assembly on an existing pole is $364.00 against the $350 value-engineering target, and of a two-sided crossing on existing poles $728.00 against $700 (R15 over the target by $14.00 and $28.00; cost drivers and savings are in the design decisions register). Every number in this note is printed by `docs/04-calcs/sizing.py`; the tag in brackets, for example [B4], is the line of that script's output that carries it.

> **Safety:** These are first-principles estimates for a paper proof of concept. They do not show that the device is safe to put beside a road. Photometry, detection, the battery in a sun-heated box, clamp preload and the foundation must be checked on hardware and by a qualified engineer, and the device needs road authority approval before any use on a public road. See CRS-PRC-001, Safety.

## Scope and method

The note checks every requirement in CRS-REQ-001 v0.8 against the design in CRS-PRC-001 v0.8 and the parametric model `cad/src/model.py`. The script imports the model's `PARAMS` and `derived()`, so heights, wind areas, the post section and the footing are those of the STEP files and drawing CRS-DWG-001. It also reads `bom/bom.csv` and `budget_usd` in `project.yaml`. Run it from the repo root with `python docs/04-calcs/sizing.py`; it also writes `docs/04-calcs/results.csv`.

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
| Battery | 12.8 V 12 Ah LiFePO4, 80 % usable; 70 % capacity at -20 °C; 80 % at end of life; charge 0 to 55 °C (CRS-DDR-005; 45 °C in v0.6); discharge to about 60 °C | Typical LiFePO4 data |
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
| Dusty, with the ventilated shield (design) | 3.9 K | 48.9 °C | 53.9 °C | 51.1 °C ambient (41.1 °C with a 45 °C limit) |

The BMS and charger stop charging above the cell's rated charge limit, 55 °C since CRS-DDR-005 (45 °C in v0.6 and earlier, see C4). Without a shield the device would lose harvest on hot, clear days above about 30 °C ambient, and at 50 °C ambient a dusty enclosure would reach 64.7 °C, above the typical 60 °C discharge limit of LiFePO4 cells. Amish accepted the recommended fix on 2026-09-25 (CRS-DDR-002): a ventilated white sun shield (part 18, about $8, as in WaterWatch and FieldNode) over the roof and three walls with a 25 mm air gap. With it the rise is 3.9 K, the interior 53.9 °C at 50 °C ambient and charging continues up to 51.1 °C ambient with the 55 °C limit [C3], so R8 is met on paper. The steady-state model ignores the battery's thermal mass, which lags the peak, and gives no credit for shade from the panel 0.78 m above the enclosure top; the shield factor of 0.25 is borrowed from WWT-CAL-001 and not measured. Moving the enclosure under the panel's shadow is to be considered when the bracket is detailed.

### C4. Hot-day charging window (STEM check S3, fixed by CRS-DDR-005)

The earlier versions let the charger stop at 45 °C cell temperature. A day with a 50 °C peak (7.5 K either side of the mean, peak at 15:00; sun a half sine from 06:00 to 18:00; cell at ambient plus the shielded rise of 3.9 K) has the cell above 45 °C for most of the sun. With 6.5 peak sun hours, the usable share of the sun and the energy stored are:

*Table 3a. Hot-day charging, 20 W panel [C4].*

| Peak ambient | Usable sun, 45 °C limit | Stored, 45 °C limit | Usable sun, 55 °C limit | Stored, 55 °C limit | Daily load |
| --- | --- | --- | --- | --- | --- |
| 45 °C | 36 % | 35.2 Wh | 100 % | 98.7 Wh | 16.0 Wh |
| 48 °C | 17 % | 17.2 Wh | 100 % | 98.7 Wh | 16.0 Wh |
| 50 °C | 9 % | 8.5 Wh | 100 % | 98.7 Wh | 16.0 Wh |

At 48 to 50 °C the old limit stores about the daily load or less; in a sustained spell of 50 °C days the battery empties in about 16 days (R6, R7). A commercial LiFePO4 pack with a BMS rated for charge to 55 °C and discharge to 60 °C is the fix; the BMS cut-off still protects the cell, it is only set to the cell's own rating (to be confirmed against the datasheet of the cell bought, "Proposed, awaiting Amish" because it is a safety limit; CRS-DDR-005). BOM line 9 states the rating; its price is unchanged and to quote.

### C5. Light bar heat (PR-017)

The sealed 2 mm aluminium bar (0.306 m², 0.0795 m² sunlit at 70°) in still air and full sun, with the day-average LED heat inside it, rises 7.8 K clean and 14.3 K dusty with the white finish of CRS-DDR-005 (alpha 0.30 clean, 0.55 dusty, assumed), so it is 64.3 °C inside at 50 °C ambient when dusty [C5]. The independent review asked for the worst case: sun at the elevation that maximises the sunlit area (0.1067 m²) and the LEDs flashing continuously (5.6 W). That gives 70.8 °C with the white finish and 76.0 °C with the charcoal finish of the first design (alpha 0.70), against the upper operating limit of an LED traffic signal module of 74 °C (Current Lighting TRAF336 datasheet class figure, to confirm for the heads bought). So the charcoal bar failed the STEM check (S5) and the white finish is the fix; the margin is 4 %, so the row is Plausible. The visors shade the lenses but not the bar.

### C6. Sensitivity of the 55 °C fix (independent review)

The shielded rise of 3.9 K assumes a 70° sun and a shield that passes 0.25 of the solar gain, a factor borrowed from another project. The table shows the cell and the hot-day charging at a 50 °C peak for lower sun and a less effective shield [C6].

*Table 3b. Sensitivity of the charging window at a 50 °C peak, 55 °C limit.*

| Case | Rise | Cell at 50 °C ambient | Usable sun | Stored per day |
| --- | --- | --- | --- | --- |
| Sun 70°, shield 0.25 (design) | 3.9 K | 53.9 °C | 100 % | 98.7 Wh |
| Sun 45°, shield 0.25 | 5.2 K | 55.2 °C | 84 % | 82.5 Wh |
| Sun 70°, shield 0.50 | 7.5 K | 57.5 °C | 47 % | 46.2 Wh |
| Sun 45°, shield 0.50 | 10.1 K | 60.1 °C | 28 % | 27.6 Wh |

The cell margin to 55 °C is only 1.1 K in the design case, so S3 is Plausible, but the energy case is robust: even the worst row stores 27.6 Wh a day against the 16.0 Wh load. The shield factor must be measured at TRL 4.

### C7. Cold days

The BMS stops charging below 0 °C cell temperature (BOM line 9). In full sun the cell sits about 3.9 K above ambient, so below about -3.9 °C ambient nothing is stored by day, and nothing at night [C7]. Autonomy then is 5.38 days at -20 °C and 4.31 days when end-of-life capacity (0.80) is also taken, below the 5-day target. R6 is therefore At risk for a cold region with an old battery and no heater; the 18 Ah fallback pack (11.5 days nominal) or a heater is the fix and costs money, so it is with Amish (CRS-DEC-001, O4). R7 (energy neutral at 2.5 peak sun hours) holds only above about -4 °C ambient.

## D. Radio link and latency (R3)

- **Time on air.** An 8-byte packet at SF7 and 125 kHz takes 36.1 ms [D1].
- **Latency.** Wake, transmit, receive and switch on the far side take 48 ms; with two retries after lost acknowledgements, 244 ms, inside the 500 ms target [D2].
- **Link budget.** Across 7 m with 25 dB of blockage from a bus, the far side receives -57.1 dBm, 65.9 dB above sensitivity; across 15 m, -63.7 dBm and 59.3 dB [D3]. The link will not limit the design; interference and regional band rules are the real questions.
- **Duty cycle.** Sixty activations in the busiest hour use 4.3 s of airtime per side against 36 s allowed at 1 % [D4].

The lost-link check-in of PR-012 (one packet a minute per side) adds 2.5 s on air per hour and 2.5 mWh a day, so the busiest hour is 6.8 s against 36 s [D5]. The sizing uses the EU 868 MHz band and its 1 % duty cycle; a US site needs a 915 MHz radio under FCC rules and a recheck (CRS-REG-001, G7).

## E. Photometry screening (R2)

A 6 W amber head with the assumed efficacy and a 20° x 10° beam gives about 3,939 cd on axis: 0.39 lx at a driver's eye at 100 m and 4.38 lx at 30 m. At 100 m the near-lane driver is 2.0° off axis horizontally and 0.6° below the head; at 30 m, 6.7° and 2.0°, both inside the beam [E1]. IA-21 requires the daytime intensity to meet the SAE J595 Class 1 yellow peak luminous intensity; that standard's figures were not available to check, so R2 is not verifiable at TRL 3. The numbers above are the input a photometric check will need, not a result.

## F. Heights, mounting and installation (R10, R11, R14)

- **Heights.** Button center 1,050 mm (R11: 0.9 to 1.1 m); light bar bottom 2,100 mm; enclosure bottom 2,850 mm (R14: 2.8 m), with the shield open at the bottom; radar at 2,600 mm on its arm with the PIR underside at 2,515 mm, so no part or cable of the sensing head is below 2.5 m; overall height 4,031 mm [F1].
- **Poles.** The band clamps and saddles are used on 76 to 114.3 mm poles (decided 2026-10-02); the new-post variant uses 114.3 x 3.6 mm [F2].
- **Installation.** A task estimate for a two-person crew on an existing pole comes to 120 min, exactly the 2 h limit of R10, with the sun shield fitted to the enclosure on the ground and the keyed saddles in place of plain ones [F3]. Only a timed trial can settle it; Amish accepted that trial on 2026-09-25, and it is on hold with TRL 4.

## G. Wind, clamps and footing (R9)

- **Loads.** The dynamic pressure at 40 m/s is 980 Pa. Wind along the road, on the sign face, gives 1,448 N and a base moment of 3,521 N·m (sign 1,839, post 920, shielded enclosure with its mounting plate 449, light bar 238 N·m) [G1]. The shield, and the mounting plate's edges and saddle tabs beside it (CRS-DDR-003), enlarge the enclosure's wind area. The four visors on the LED heads (26 mm deep, with a 15 mm drip lip) lie inside the light bar's outline along the road and add only about 0.0005 m² across it, so no base moment changes by more than 2 N·m. Wind across the road gives 760 N and 1,646 N·m, of which the panel is 416 N·m [G2]. Along the road governs.
- **Post.** *Table 4. Post stress in the 40 m/s gust [G3, G4].*

| Post | Section modulus | Stress | Share of S235 yield | R9 (60 %) |
| --- | --- | --- | --- | --- |
| 76.1 x 3.2 mm | 12,820 mm³ | 251 MPa | 107 % | Yields |
| 88.9 x 4.0 mm | 21,674 mm³ | 153 MPa | 65 % | Not met |
| 88.9 x 4.0 mm with a 600 mm sign | 21,674 mm³ | 122 MPa | 52 % | Met |
| 114.3 x 3.6 mm (decided, D3) | 33,593 mm³ | 105 MPa | 45 % | Met |

The TRL 2 figures (169 MPa and 72 % on the 88.9 mm post) counted the panel face-on in the same gust as the sign; here the two act in different wind directions. The top of the 114.3 mm post deflects about 31 mm (0.8 % of its height) in the gust [G5].

- **Clamps.** A gust whose pressure centre sits a quarter of the sign's width off the pole axis twists the sign clamps with 175 N·m. Two bands at the assumed 1,000 N tension resist about 144 N·m by friction on a 114.3 mm pole and only 75 N·m on a 60 mm pole [G6]. With plain saddles the sign could rotate on its pole in a storm. Amish accepted the recommended anti-rotation detail on 2026-09-25 (CRS-DDR-002):
  - **New posts:** an M10 through-bolt in place of the upper sign saddle's upper sign bolt (part 19), through the sign, the saddle and both post walls. The 175 N·m couple puts 1,535 N on each post wall: 8 % of the bolt's shear resistance and 12 % of the wall's bearing resistance [G6b]. Met.
  - **Existing poles:** keyed saddles with serrated grip faces (part 20). At an assumed grip friction of 0.4 two bands resist 287 N·m on a 114.3 mm pole and 191 N·m on a 76 mm pole, so the sign holds on poles of about 70 mm and larger, which covers the 76 to 114.3 mm range of the existing-pole kit with a 9 % margin on the 76 mm pole [G6c]. The friction and band tension are assumptions that must be measured (TRL 4, on hold). Decided 2026-10-02 (CRS-DDR-002, N1): the existing-pole kit is limited to poles of 76 mm and larger until a slip-torque test confirms the grip, then a third saddle and band brings 60 to 75 mm poles back.
- **Footing.** The resultant of 1,448 N (326 lbf) acts 2.43 m (8.0 ft) above the sidewalk. The non-constrained pole formula gives 1,791 mm of embedment for a 500 mm footing in clay, so the model uses 1,800 mm [G7]. This is a screening size; the local code and soil govern.
- **Existing poles.** An assembly adds 2,601 N·m at the sidewalk to the host pole [G8]. The pole owner must confirm the pole and its foundation can carry it; that check is outside this repo. At 60 % of yield the added moment alone needs a section modulus of at least 18,447 mm³, which a 76.1 x 3.2 mm pole (12,820 mm³) does not have and a 88.9 x 4.0 mm pole (21,674 mm³) does [G9]; the keyed saddles hold the sign on poles of 70 mm and up, but the kit is not a structural upgrade, so the 76 mm limit decided on 2026-10-02 is raised again to Amish (CRS-DEC-001, O5).

## H. Cost (R15)

The BOM has 23 lines, all priced. One assembly on an existing pole costs $364.00 and $437.00 with its own post and anti-rotation bolt, footing concrete excluded [H1]. The design for construction (CRS-DDR-003) added $28.00 and the visors and bezels on the heads $4.00 (line 3, $1.00 a head): eight keyed saddles in place of two ($18.00 more), the enclosure mounting plate ($8.00), the radar arm and battery strap ($3.00), a fuller panel bracket ($6.00 more) and more fixings ($4.00 more), less the sign maker's brackets ($5.00) and the bought band brackets ($6.00). Against the value-engineering target of $350 (`budget_usd`, a hypothetical control target, not a limit) that is $14.00 over on an existing pole and $87.00 over with a new post [H2]. Under D1 the target covers the existing-pole assembly, so R15 is over the target on paper; cost drivers and savings worth trying are in the Value engineering section of `docs/06-design-decisions.md`. A two-sided crossing costs $728.00 on existing poles ($28.00 over R15's $700) and $874.00 with new posts: $22.00 under and $124.00 over the $750 site-trial value-engineering target, which Amish accepted on 2026-09-25 for when a site trial starts (on hold with TRL 4) [H3].

## I. Flash area and stopping distance (PR-016, PR-018)

Two lit heads (174 cm²) seen from 1.5 m, the nearest a pedestrian waits at the button, subtend 7.7 msr; from 3 m, 1.9 msr [I1]. The WCAG 2.1 general flash area limit (6 msr, 25 % of a 10° field) is used only as an analogue for photosensitivity: no road standard was checked, the IA-21 sequence is four 50 ms pulses in each 800 ms (five a second inside a sequence), and the bar faces the road, not the pedestrian. So PR-016 is **At risk** and goes to the risk register as hazard H5; it is not a clinical statement. A driver at 60 km/h needs about 83 m to stop (2.5 s perception-reaction, the AASHTO design value, and 3.4 m/s² braking, assumed, to confirm) is 83 m, against the 100 m seeing distance of PR-002 [I2]; PR-018 is met on paper only while PR-002 holds, and PR-002 is not verifiable at TRL 3.

## M. Requirement trace

CRS-REQ-001 R1 to R15 became PR-001 to PR-015 in CRS-PRS-001 (migration of 2026-10-31, same numbers). R16 to R19 are new in this version and are PR-016 to PR-019. Every PR id appears in Table 5 by its R number: PR-001 (R1), PR-002 (R2), PR-003 (R3), PR-004 (R4), PR-005 (R5), PR-006 (R6), PR-007 (R7), PR-008 (R8), PR-009 (R9), PR-010 (R10), PR-011 (R11), PR-012 (R12), PR-013 (R13), PR-014 (R14), PR-015 (R15), PR-016 (R16), PR-017 (R17), PR-018 (R18), PR-019 (R19).

## L. Results against every requirement

*Table 5. Requirement status at TRL 3 (also in `docs/04-calcs/results.csv`).*

| ID | Requirement | Value | Target | Status |
| --- | --- | --- | --- | --- |
| R15 | Affordable | $364.00 per assembly; $728.00 per crossing on existing poles | $350; $700 per crossing | **Over the value-engineering target by $14.00** ($28.00 per crossing) |
| R2 | Visibility | About 3,939 cd per head (screening) | Seen at 100 m in sun; dimmed at night | Not verifiable at TRL 3 |
| R5 | Detection quality | PIR wakes the radar; 1 s dwell | 5 % false, 2 % missed | Not verifiable at TRL 3 |
| R10 | Mounting | Fits 76 to 114.3 mm poles; bar at 2.1 m; about 120 min estimate | Fit; 2.1 m; 2 h | Not verifiable at TRL 3 (install time) |
| R3 | Activation and sync | 48 ms; 244 ms with two retries | 0.5 s or less | Met on paper |
| R6 | Autonomy | 7.7 days (5.4 at -20 °C; 6.2 at end of life; 4.3 at both) | 5 days or more | **At risk** (cold and end of life together) |
| R7 | Energy balance | Break-even 1.05 peak sun hours; recovery 2.1 days | Neutral at 2.5 h; 3 days or fewer | Met on paper |
| R8 | Environment | 53.9 °C inside at 50 °C ambient (dusty, shielded); charging to 51.1 °C ambient; light bar 70.8 °C worst case | IP65; -20 to +50 °C; charge 0 to 55 °C | Met on paper (charge limit per CRS-DDR-005) |
| R9 | Structure | 45 % of yield on the 114.3 mm post; bolt 12 % of bearing; keyed saddles hold on poles of 70 mm and up; existing poles need S of 18,447 mm³ or more (owner verifies, G9) | 60 % of yield or less; no sign rotation | Met on paper (new post and clamps; friction and band tension assumed; the pole owner verifies an existing pole) |
| R1 | Light geometry and pattern | 140 x 62 mm lenses; IA-21 pattern; bar under the sign | 127 x 51 mm min.; IA-21 | Met by design |
| R4 | Flash duration | 12.8 s for 7 m; 20 s energy case | L/0.9 + 5 s; 10 to 40 s | Met by design |
| R11 | Accessibility | Button 1.05 m; piezo; tone, tactile arrow, pilot light | 0.9 to 1.1 m; 22 N or less | Met by design |
| R12 | Fail-safe | Timer-limited flashing; local flashing without link; fault log | Never continuous | Met by design |
| R13 | Privacy | Presence and counts only | No images or audio | Met by design |
| R16 | Flash area | 7.72 msr at 1.5 m | 6 msr (analogue only) | **At risk** |
| R17 | Light bar temperature | 64.3 °C at 50 °C ambient (dusty, 70° sun); 70.8 °C worst case, white finish | 74 °C or less | Met on paper (4 % margin in the worst case) |
| R18 | Warning in time to stop | 83 m at 60 km/h | 100 m or less | Met on paper |
| R19 | Buildable and repairable | BLD-001; 117 modelled parts, none bare | Ordinary tools only | Met by design |
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
| Base moment | About 3.7 kN·m | 3.52 kN·m | Panel and sign loads in different wind directions; shielded enclosure and its mounting plate |
| 88.9 x 4 mm post | 169 MPa, 72 % | 153 MPa, 65 % | As above; still not met |
| 114.3 x 3.6 mm post | 110 MPa, 47 % | 105 MPa, 45 % | As above |
| Cost per assembly | $361 own post; $311 existing pole | $437.00; $364.00 | PIR, pilot light, larger post, sun shield, saddles, bolt, parts added for construction (CRS-DDR-003) |

CRS-PRC-001, CRS-REQ-001 and `README.md` have been brought in line with the TRL 3 column.
