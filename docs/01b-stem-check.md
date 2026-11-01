---
doc_id: CRS-STM-001
title: CrossSafe STEM check
project: CrossSafe
doc_type: STEM check
version: "0.1"
status: Draft
date: '2026-10-31'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-31'
  author: Amish Chadha
  change: "First STEM check (kit 1.9.1 upgrade) of the TRL 3 design (option A) and the two other concept options; three rows failed on first run and were fixed under the standing instruction of 2026-10-23 (CRS-DDR-005); one row (flash area) has a fix proposed for Amish; independent review recorded"
---

# CrossSafe STEM check

Verdict: of 24 claims, 11 are within known science, 12 are plausible and named for confirmation, 1 fails its screen with a fix proposed (S15, flash area, for Amish), and none fails outright. Three failed on first run and were fixed in the same session under Amish's standing instruction of 2026-10-23, none changing a working principle, pitch or scope: option A's battery would stop charging for most of the sun on a 50 °C day (S3, cell and BMS specified for charge to 55 °C), option A's light bar would reach 76 °C in the worst case against a 74 °C module limit (S5, white finish instead of charcoal), and option C's panel would hit its stop at about 62 g (S22, hydraulic damper). All three are in CRS-DDR-005. The check stays open. Method and rules: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py`, which imports the sizing script of CRS-CAL-001.

## Claims checked

*Table 1. Claims, governing science and verdicts. (A) is the pole-top beacon, (B) the kerbside solar bollard with in-road studs, (C) the pull-up retroreflective panel.*

| # | Claim (number and unit) | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | (A) The battery carries the design-case load for 5 days or more without sun | Physics | Thermodynamics and energy | Stored energy / daily load, usable 80 % of 154 Wh, load 16 Wh/day (flash, pilot, radio, standby) | 7.69 days >= 5 days | Within known science | CRS-CAL-001 B4 |
| S2 | (A) At 2.5 peak sun hours the 20 W panel stores at least the daily load | Physics | Thermodynamics and energy | Conservation of energy or mass | in 37.95 Wh/day, out 15.98 Wh/day | Within known science | CRS-CAL-001 B6 |
| S3 | (A) On a 50 °C peak day the cell stays below its 55 °C charge limit and the battery charges at least the daily load (CRS-DDR-005) | Chemistry | Electrochemistry and batteries | Cell = ambient + shielded rise (3.9 K at 70 deg sun, shield factor 0.25 borrowed); stored 98.7 Wh/day against 16.0; review sensitivity: at 45 deg sun and shield 0.50 the cell reaches 60.1 °C and 27.6 Wh/day is still stored | 53.9 °C <= 55 °C (first run with the 45 °C limit: 8.5 Wh/day, Fails; fixed) | Plausible, to confirm at TRL 3 | CRS-CAL-001 C4, C6; CRS-DDR-005 |
| S4 | (A) The sun-heated enclosure stays below the 60 °C discharge limit of LiFePO4 at 50 °C ambient | Physics | Heat transfer | Steady-state balance: absorbed sun (shield factor 0.25, borrowed) plus internal loss over the convection area | 53.9 °C <= 60 °C | Plausible, to confirm at TRL 3 | CRS-CAL-001 C3, C6 |
| S5 | (A) The sealed light bar, white finish, stays below the 74 °C upper limit of an LED traffic signal module at 50 °C ambient in the worst case (CRS-DDR-005) | Physics | Heat transfer | Same method as S4 for a 2 mm aluminium bar, no shield, dusty white (alpha 0.55, assumed), sun at the worst elevation, LEDs flashing continuously; the 74 °C figure is a datasheet class figure | 70.8 °C <= 74 °C (first run with the charcoal finish, alpha 0.70: 76.0 °C, Fails; fixed by a white finish) | Plausible, to confirm at TRL 3 | CRS-CAL-001 C5; CRS-DDR-005 |
| S6 | (A) Both sides flash within 0.5 s of a trigger, including two radio retries | Engineering and technology | Control and communications | LoRa time on air at SF7 plus processing and acknowledgement timeouts | 244 ms <= 500 ms | Within known science | CRS-CAL-001 D2 |
| S7 | (A) The 868 MHz link across 15 m with a 25 dB blockage keeps at least 10 dB of margin | Physics | Electromagnetism and optics | Free-space path loss plus a blockage allowance against SF7 sensitivity | 59.3 dB >= 10 dB | Within known science | CRS-CAL-001 D3 |
| S8 | (A) Radio on-air time in the busiest hour stays inside the 1 % duty cycle of the 868 MHz sub-band | Engineering and technology | Standards practice | Time on air per packet times packets in the busiest hour (the duty-cycle rule is ETSI practice; the US band has other rules, to assess in REG) | 4.3 s <= 36 s | Within known science | CRS-CAL-001 D4 |
| S9 | (A) Each amber head gives about 3,900 cd on axis, enough to be seen at 100 m in sun | Physics | Electromagnetism and optics | Screening from LED power, efficacy and optic efficiency over the beam solid angle gives 3,939 cd; the SAE J595 class figure cited in IA-21 and the heads' photometric data are not checked | No calculation closes it at P3; photometry from the datasheet of the heads bought, then a field check | Plausible, to confirm at TRL 3 | open |
| S10 | (A) The 114.3 x 3.6 mm post carries sign, panel and enclosure in a 40 m/s gust at 60 % of yield or less | Physics | Strength of materials | Drag force on each part at 980 Pa, bending moment at the base, sigma = M / S against S235 yield | 45 % of yield <= 60 % of yield | Within known science | CRS-CAL-001 G3 |
| S11 | (A) A 1,800 mm embedment in a 500 mm clay footing resists the overturning moment | Physics | Mechanics and statics | Non-constrained pole footing, IBC 1807.3.2.1 screening, lateral bearing 100 psf per ft of depth (clay, class 5 screening value, assumed) | 1791 mm <= 1800 mm | Plausible, to confirm at TRL 3 | CRS-CAL-001 G7 |
| S12 | (A) The M10 anti-rotation through-bolt carries the sign torque on a new post | Physics | Strength of materials | Couple on the two post walls against bolt shear and wall bearing (Eurocode 3 practice, gamma 1.25) | 1535 N <= 1.296e+04 N | Within known science | CRS-CAL-001 G6b |
| S13 | (A) On the smallest existing pole (76 mm) two keyed saddles resist the sign torque | Physics | Mechanics and statics | Capstan-style friction of a 1,000 N band at friction 0.4 (assumed) on two saddles, against the eccentric gust torque | 191 N m >= 175 N m | Plausible, to confirm at TRL 3 | CRS-CAL-001 G6c |
| S14 | (A) The LiFePO4 pack charges and discharges safely from -20 to +50 °C ambient | Chemistry | Electrochemistry and batteries | Charging below 0 °C plates lithium, so the BMS must cut charge there (low-temperature cut-off is in BOM line 9); commercial packs list charge 0 to 55 °C and discharge -20 to 60 °C; fuse at the terminal; vent and fire risk in H2 of CRS-RSK-001 | Cell datasheet and BMS thresholds to assess when the pack is chosen | Plausible, to confirm at TRL 3 | open |
| S15 | (A) The flashing is not a photosensitivity hazard for people beside the beacon | Biology | Human factors and physiology | Lit area of two heads (174 cm2) seen from 1.5 m is 7.7 msr and from 1.2 m (button 1 m from the pole, bar centre 2.17 m up, eye 1.5 m) about 12 msr, against the 6 msr WCAG 2.1 analogue (no road or clinical standard checked); the IA-21 sequence is five pulses a second inside a sequence; the heads face the road, so the angle from the button reduces the apparent area | Fails the analogue screen. Fix proposed: a viewing-angle check, then dim the heads while the button is held or add a pedestrian-end baffle; a road-authority and clinical-safety review is to assess. Moving the bar or dimming is a safety trade-off, so it goes to Amish (O3) | Fails, fix proposed | open |
| S16 | (A) A driver at 60 km/h can stop within the 100 m seeing distance of the warning | Physics | Mechanics and statics | Stopping distance = u t + u^2 / (2 a), t = 2.5 s (AASHTO design value), a = 3.4 m/s2 (assumed); the 100 m seeing distance is PR-002, itself not verifiable at P3 | 83 m <= 100 m | Within known science | CRS-CAL-001 I2 |
| S17 | (A) The daily load is 16 Wh against the 29.8 Wh/day of the TRL 2 estimate | Mathematics | Units and dimensional analysis | Cross-check of the bottom-up build-up against the earlier lumped estimate (PIR gating and IA-21 duty explain the drop) | claimed 16 Wh/day, estimate 29.8 Wh/day (ratio 0.54) | Within known science | CRS-CAL-001 B3 |
| S18 | (A) A two-person crew installs one assembly on an existing pole in 2 hours or less | Engineering and technology | Manufacturing tolerances | Sum of task times for clamps, bar and sign, enclosure, battery and wiring, panel, button, radar (estimate) | 120 min <= 120 min | Plausible, to confirm at TRL 3 | CRS-CAL-001 F3 |
| S19 | (B) A 70 x 40 mm solar tile keeps a road stud flashing 20 s per crossing, 300 times a day | Physics | Thermodynamics and energy | Tile at 15 % and 2.5 peak sun hours stores 0.80 Wh/day; LEDs 0.35 plus a radio listening all day 0.44 Wh/day | 0.781 Wh/day <= 0.798 Wh/day | Plausible, to confirm at TRL 3 | CRS-OPT-001 Table 1; script |
| S20 | (B) A stud's raised lens ring carries a wheel of a heavy axle | Physics | Strength of materials | Wheel load over the 2,800 mm2 lens ring; polycarbonate compressive yield about 60 MPa (assumed), safety factor 1.5 | 17.8 MPa <= 40 MPa | Within known science | CRS-OPT-001 Table 1 |
| S21 | (B) Studs at road level (antenna gain -3 dBi, 10 dB ground loss) hear the bollard across 15 m | Physics | Electromagnetism and optics | Free-space path loss with extra ground-reflection and blockage allowances (estimate) | 45.3 dB >= 10 dB | Within known science | CRS-OPT-001 Table 1 |
| S22 | (C) The released panel stops from a 250 mm fall below 20 g, with the peak taken as twice the mean (end-of-travel damper, 25 mm stroke, CRS-DDR-005) | Physics | Mechanics and statics | a = v^2 / (2 s) for v = sqrt(2 g h), times 2 for a real damper curve; the 20 g limit protects sheeting and fixings (assumed) | 20 g <= 20 g (first run with a 4 mm pad: 62 g, Fails; fixed) | Plausible, to confirm at TRL 3 | CRS-DDR-005; CRS-OPT-001 |
| S23 | (C) A person lifts the panel with a pull of 22 N or less | Physics | Mechanics and statics | Weight over pulley efficiency plus 10 % guide friction; 22.2 N is 5 lbf, the ADA operable-part force | 20.4 N <= 22.2 N | Plausible, to confirm at TRL 3 | CRS-OPT-001 Table 1 |
| S24 | (C) A retroreflective panel is seen by a driver at night without electricity | Physics | Electromagnetism and optics | Retroreflective sheeting returns headlight beams to the driver; it needs no power, but the return depends on the sheeting class, the dirt and the panel angle | No calculation at P3; sheeting datasheet to assess | Plausible, to confirm at TRL 3 | open |

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails, fix proposed**, **Fails**. "Open" in the last column means that no calculation at P3 closes the row; each open row is a "to assess" item for a datasheet, a road-authority review or the TRL 4 plan, and is carried into CRS-RSK-001.

Rows to read with care:

- **S3 (fixed).** With a 45 °C charge limit (CRS-REQ-001 v0.8, R8) and the shielded rise of 3.9 K, the cell is above its limit for most of the sun on a hot day: at a 50 °C peak 9 % of the sun is usable and 8.5 Wh is stored against a 16 Wh load. A cell and BMS rated for charge to 55 °C stores 98.7 Wh. The rating is the commercial LiFePO4 norm, so the fix is a specification (BOM line 9), not a design change. The cell margin is only 1.1 K and rests on a borrowed shield factor, so the row is Plausible; with a lower sun (45 deg) and a shield passing half the gain the cell reaches 60.1 °C but 27.6 Wh a day is still stored. Because it moves a safety limit, the 55 °C figure is also "Proposed, awaiting Amish" in CRS-DEC-001 (O2).
- **S5 (fixed).** The light bar has no shield. At the sun elevation that maximises its sunlit area, dusty and with the LEDs flashing continuously, a charcoal bar reaches 76.0 °C; a white finish (alpha 0.55 dusty, assumed) gives 70.8 °C. The finish is in BOM line 2; the model's render colour still shows the earlier charcoal.
- **S11, S13, S18, S23 are within 10 % of their limit** and Plausible by rule. S13 depends on an assumed friction of 0.4 for the keyed saddle and S11 on an assumed soil bearing.
- **S15 (fails the analogue screen).** The flash area at the button is above the 6 msr analogue limit (7.7 msr at 1.5 m, about 12 msr at 1.2 m); the analogue is not a road standard and the heads face the road, so the true value is lower, but it is not shown. The fix proposed (a viewing-angle check, dimming while the button is held, or a baffle at the pedestrian end) is a safety trade-off and goes to Amish (O3).
- **S19 is thin.** The stud tile gives 0.80 Wh/day and the LEDs plus a radio that listens all day use 0.78 Wh/day.
- **S9 is not closed.** Intensity at 100 m needs the heads' photometry.

## Fields not relevant

- Chemistry beyond the battery: no process chemistry; materials are galvanised or stainless steel, aluminium, polycarbonate and EPDM, covered by S14 and by corrosion notes in CRS-RSK-001.
- Biology: no living material and no emission above the visible; the only biological row is the photosensitivity screen S15.

## Concept options

STEM verdict for each option in CRS-OPT-001, one line each.

- **A, pole-top flashing beacon:** 18 rows, 9 within, 8 plausible, 1 fails with a fix proposed (S15); S3 and S5 fixed (CRS-DDR-005). Kept.
- **B, kerbside solar bollard with in-road studs:** 3 rows, 2 within and 1 plausible (S19 is thin). Kept.
- **C, pull-up retroreflective panel:** 3 rows, all plausible; S22 fixed by the damper (CRS-DDR-005). Kept.

No option is dropped.

## Independent review

A second reviewer (Claude Opus 5.5, run headless with `claude -p`, with no access to the author's reasoning) was given only this check, CRS-CAL-001, CRS-PRS-001 and `sizing.py` and asked to refute every "Within known science" verdict and the headline results. It could not refute the arithmetic of S1, S2, S6, S7, S8, S10, S12, S13 and S23, the sensitivity table, the cost sums or the verdict counts. It found ten things; what changed:

1. **Existing poles (PR-009).** A 76.1 x 3.2 mm pole is at 107 % of yield from the wind loads in CAL Table 4, and the 2,601 N m the kit adds alone needs a section modulus of about 18,450 mm3. CAL now states that the pole owner verifies the pole (G9) and PR-009 says so; the 76 mm limit decided on 2026-10-02 is left to Amish (O5).
2. **Cold days.** Charging is inhibited below 0 °C, and autonomy at -20 °C and end of life together is 4.3 days, below 5. PR-006 is now At risk (C7); the 18 Ah fallback pack (11.5 days nominal) is the fix and costs money, so it is with Amish (O4).
3. **S3, S4 and the 55 °C fix.** The margin is thin and depends on the borrowed shield factor and the 70 degree sun. Both rows are now Plausible and CAL C6 gives the sensitivity.
4. **S15.** The verdict was Plausible although the screen is exceeded; it is now "Fails, fix proposed" and the nearest viewing distance is taken as 1.2 m too.
5. **S19 and S22** were inside the 10 % band or assumed a perfect damper; both are Plausible, S22 with a peak of twice the mean deceleration.
6. **S5 / PR-017.** The light bar was checked at the average LED heat and 70 degree sun; the worst case was 76.0 °C and failed, which led to the white finish (fix F3).
7. **Radio basis.** The link is sized for EU 868 MHz at 1 % duty and the other basis is US; the lost-link check-in packets are now added (CAL D5, 6.8 s in the busiest hour against 36 s) and the US 915 MHz band is in REG as "to assess".
8. **S11** quoted 300 psf per ft; the script uses 100 (class 5 clay). The row is corrected.
9. **S16 / PR-018.** The reaction time is now 2.5 s (AASHTO design value, 83 m at 60 km/h) and the row states that the 100 m seeing distance is PR-002, not verifiable at P3.
10. **Slips:** PR-010 status aligned with CAL, a mis-cited row number in the script, and the 16-day sentence reworded. The shear factor of the stainless bolt (S12) and the 41 ms against 36.1 ms time on air are left to confirm.

## Sources

- Energy, heat and structural methods: CRS-CAL-001 (this repo, `docs/04-calcs/01-sizing.md`).
- SAE J595 class 1 yellow intensity, as cited in [FHWA IA-21](https://mutcd.fhwa.dot.gov/resources/interim_approval/ia21/index.htm).
- WCAG 2.1 general flash and red flash thresholds, W3C Recommendation (analogue only; no road standard checked), https://www.w3.org/TR/WCAG21/#three-flashes-or-below-threshold.
- ADA operable-part force of 5 lbf (22.2 N): U.S. Access Board, [Chapter 3: Operable Parts](https://www.access-board.gov/ada/guides/chapter-3-operable-parts/), checked 2026-10-31.
- LiFePO4 charge and discharge temperature ranges: manufacturer datasheets of commercial 12.8 V packs (class figures; the cell bought is to be confirmed).
- AASHTO Green Book perception-reaction time and comfortable deceleration (assumed values, to confirm).
- Current Lighting TRAF336 LED traffic signal module datasheet (74 °C upper operating class figure, to confirm for the heads bought).
- IBC 1807.3.2.1 non-constrained pole footing equation (screening only).
