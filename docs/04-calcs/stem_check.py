"""CrossSafe STEM check calculations (CRS-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv. Option A is the pole-top beacon (the TRL 2 design, recommended); B is the kerbside
solar bollard with in-road studs; C is the pull-up retroreflective panel. The sizing itself is in CRS-CAL-001
(docs/04-calcs/sizing.py), which this script imports (about a minute: it builds the model) to close the rows of option A.
Three rows failed on first run and were fixed under Amish's standing instruction of 2026-10-23 (CRS-DDR-005): S3 (battery charge
limit), S5 (light bar finish) and S22 (end-of-travel damper on option C). S15 (flash area) fails its analogue screen and has a fix proposed
that goes to Amish. The record is printed by the main block. Independent review changes of 2026-10-31 are marked "review".
"""
import math, sys
sys.path.insert(0, ".kit")
from stem_check import Check, G, WITHIN, PLAUSIBLE, FIX  # noqa: F401
sys.path.insert(0, "docs/04-calcs")
import sizing as CAL  # noqa: E402  CRS-CAL-001, reads cad/src/model.py

c = Check()
CAL_ID = "CRS-CAL-001"

# ---------------------------------------------------------------- option A: pole-top beacon
c.claim("S1", "The battery carries the design-case load for 5 days or more without sun", "Physics", "Thermodynamics and energy",
        "Stored energy / daily load, usable 80 % of 154 Wh, load 16 Wh/day (flash, pilot, radio, standby)", round(CAL.aut, 2), 5.0, "days",
        rule="above", closed_by=f"{CAL_ID} B4")
stored25 = CAL.PANEL_W * 2.5 * CAL.chain
c.balance("S2", "At 2.5 peak sun hours the 20 W panel stores at least the daily load", "Physics", "Thermodynamics and energy",
          {"stored by the panel": stored25}, {"daily load": CAL.e_day}, "Wh/day", closed_by=f"{CAL_ID} B6")
# S3: first run with the 45 C charge limit failed (see main block); the design now uses a cell rated for charge to 55 C.
f_sens = CAL.sens_c
c.claim("S3", "On a 50 C peak day the cell stays below its 55 C charge limit and the battery charges at least the daily load (CRS-DDR-005)", "Chemistry", "Electrochemistry and batteries",
        f"Cell = ambient + shielded rise (3.9 K at 70 deg sun, shield factor 0.25 borrowed); stored {CAL.hot_e:.1f} Wh/day against {CAL.e_day:.1f}; review sensitivity: at 45 deg sun and shield 0.50 the cell reaches {CAL.sens_c['sun 45 deg, shield 0.50'][1]:.1f} C and {CAL.worst_store:.1f} Wh/day is still stored",
        round(50 + CAL.dt_d, 1), CAL.CHG_MAX, "C", margin=0.1, closed_by=f"{CAL_ID} C4, C6; CRS-DDR-005")
c.claim("S4", "The sun-heated enclosure stays below the 60 C discharge limit of LiFePO4 at 50 C ambient", "Physics", "Heat transfer",
        "Steady-state balance: absorbed sun (shield factor 0.25, borrowed) plus internal loss over the convection area", round(50 + CAL.dt_d, 1), CAL.CELL_DIS_MAX, "C",
        margin=0.15, closed_by=f"{CAL_ID} C3, C6")
c.claim("S5", "The sealed light bar, white finish, stays below the 74 C upper limit of an LED traffic signal module at 50 C ambient in the worst case (CRS-DDR-005)", "Physics", "Heat transfer",
        "Same method as S4 for a 2 mm aluminium bar, no shield, dusty white (alpha 0.55, assumed), sun at the worst elevation, LEDs flashing continuously; the 74 C figure is a datasheet class figure",
        round(50 + CAL.bar_worst, 1), CAL.BAR_LIMIT, "C", margin=0.1, closed_by=f"{CAL_ID} C5; CRS-DDR-005")
c.claim("S6", "Both sides flash within 0.5 s of a trigger, including two radio retries", "Engineering and technology", "Control and communications",
        "LoRa time on air at SF7 plus processing and acknowledgement timeouts", round(CAL.lat_worst * 1000, 0), 500.0, "ms", closed_by=f"{CAL_ID} D2")
prx15 = CAL.TX_DBM + 2 * CAL.ANT_DBI - 2 * CAL.CABLE_DB - CAL.fspl(15.0) - CAL.BLOCK_DB
c.claim("S7", "The 868 MHz link across 15 m with a 25 dB blockage keeps at least 10 dB of margin", "Physics", "Electromagnetism and optics",
        "Free-space path loss plus a blockage allowance against SF7 sensitivity", round(prx15 - CAL.SENS_SF7, 1), 10.0, "dB", rule="above", closed_by=f"{CAL_ID} D3")
c.claim("S8", "Radio on-air time in the busiest hour stays inside the 1 % duty cycle of the 868 MHz sub-band", "Engineering and technology", "Standards practice",
        "Time on air per packet times packets in the busiest hour (the duty-cycle rule is ETSI practice; the US band has other rules, to assess in REG)", round(CAL.air_h, 1), CAL.EU_DUTY * 3600, "s",
        closed_by=f"{CAL_ID} D4")
c.cited("S9", "Each amber head gives about 3,900 cd on axis, enough to be seen at 100 m in sun", "Physics", "Electromagnetism and optics",
        f"Screening from LED power, efficacy and optic efficiency over the beam solid angle gives {CAL.i_cd:,.0f} cd; the SAE J595 class figure cited in IA-21 and the heads' photometric data are not checked",
        "No calculation closes it at P3; photometry from the datasheet of the heads bought, then a field check", PLAUSIBLE, closed_by="")
ratio_post = CAL.ratios[CAL.P["post_od"]] * 100
c.claim("S10", "The 114.3 x 3.6 mm post carries sign, panel and enclosure in a 40 m/s gust at 60 % of yield or less", "Physics", "Strength of materials",
        "Drag force on each part at 980 Pa, bending moment at the base, sigma = M / S against S235 yield", round(ratio_post, 0), 60.0, "% of yield", closed_by=f"{CAL_ID} G3")
req_mm = CAL.d * 304.8
c.claim("S11", "A 1,800 mm embedment in a 500 mm clay footing resists the overturning moment", "Physics", "Mechanics and statics",
        "Non-constrained pole footing, IBC 1807.3.2.1 screening, lateral bearing 100 psf per ft of depth (clay, class 5 screening value, assumed)", round(req_mm, 0), CAL.P["embed"], "mm", margin=0.1, closed_by=f"{CAL_ID} G7")
c.claim("S12", "The M10 anti-rotation through-bolt carries the sign torque on a new post", "Physics", "Strength of materials",
        "Couple on the two post walls against bolt shear and wall bearing (Eurocode 3 practice, gamma 1.25)", round(CAL.f_bear, 0), round(min(CAL.v_rd, CAL.b_rd), 0), "N", closed_by=f"{CAL_ID} G6b")
c.claim("S13", "On the smallest existing pole (76 mm) two keyed saddles resist the sign torque", "Physics", "Mechanics and statics",
        "Capstan-style friction of a 1,000 N band at friction 0.4 (assumed) on two saddles, against the eccentric gust torque", round(CAL.key_tq(CAL.P["pole_min_od"]), 0), round(CAL.t_sign, 0), "N m",
        rule="above", margin=0.1, closed_by=f"{CAL_ID} G6c")
c.cited("S14", "The LiFePO4 pack charges and discharges safely from -20 to +50 C ambient", "Chemistry", "Electrochemistry and batteries",
        "Charging below 0 C plates lithium, so the BMS must cut charge there (low-temperature cut-off is in BOM line 9); commercial packs list charge 0 to 55 C and discharge -20 to 60 C; fuse at the terminal; vent and fire risk in H2 of CRS-RSK-001",
        "Cell datasheet and BMS thresholds to assess when the pack is chosen", PLAUSIBLE, closed_by="")
c.cited("S15", "The flashing is not a photosensitivity hazard for people beside the beacon", "Biology", "Human factors and physiology",
        f"Lit area of two heads ({CAL.a_lit * 1e4:.0f} cm2) seen from 1.5 m is {CAL.a_lit / 1.5 ** 2 * 1000:.1f} msr and from 1.2 m (button 1 m from the pole, bar centre 2.17 m up, eye 1.5 m) about {CAL.a_lit / 1.2 ** 2 * 1000:.0f} msr, against the 6 msr WCAG 2.1 analogue (no road or clinical standard checked); the IA-21 sequence is five pulses a second inside a sequence; the heads face the road, so the angle from the button reduces the apparent area",
        "Fails the analogue screen. Fix proposed: a viewing-angle check, then dim the heads while the button is held or add a pedestrian-end baffle; a road-authority and clinical-safety review is to assess. Moving the bar or dimming is a safety trade-off, so it goes to Amish (O3)", FIX, closed_by="")
c.claim("S16", "A driver at 60 km/h can stop within the 100 m seeing distance of the warning", "Physics", "Mechanics and statics",
        "Stopping distance = u t + u^2 / (2 a), t = 2.5 s (AASHTO design value), a = 3.4 m/s2 (assumed); the 100 m seeing distance is PR-002, itself not verifiable at P3", round(CAL.s_stop_max, 0), 100.0, "m", closed_by=f"{CAL_ID} I2")
c.order_of_magnitude("S17", "The daily load is 16 Wh against the 29.8 Wh/day of the TRL 2 estimate", "Mathematics", "Units and dimensional analysis",
                     claimed=round(CAL.e_day, 1), estimate=29.8, unit="Wh/day", law="Cross-check of the bottom-up build-up against the earlier lumped estimate (PIR gating and IA-21 duty explain the drop)",
                     closed_by=f"{CAL_ID} B3")
c.claim("S18", "A two-person crew installs one assembly on an existing pole in 2 hours or less", "Engineering and technology", "Manufacturing tolerances",
        "Sum of task times for clamps, bar and sign, enclosure, battery and wiring, panel, button, radar (estimate)", 120.0, 120.0, "min", margin=0.1, closed_by=f"{CAL_ID} F3")

# ---------------------------------------------------------------- option B: kerbside solar bollard with in-road studs
tile_w = 0.070 * 0.040 * 150.0 * 2.5 * 0.76          # 28 cm2 tile at 15 % of 1000 W/m2, 2.5 PSH, chain 0.76: Wh/day
stud_led = 4 * 0.021 * 2.1 / 0.85 * CAL.h_flash       # four 20 mA amber LEDs at 2.1 V, driver 85 %, flashing hours: Wh/day
stud_rx = 3.3 * 5.5e-3 * 24                           # radio listening continuously at 5.5 mA: Wh/day
c.claim("S19", "A 70 x 40 mm solar tile keeps a road stud flashing 20 s per crossing, 300 times a day", "Physics", "Thermodynamics and energy",
        f"Tile at 15 % and 2.5 peak sun hours stores {tile_w:.2f} Wh/day; LEDs {stud_led:.2f} plus a radio listening all day {stud_rx:.2f} Wh/day", round(stud_led + stud_rx, 3), round(tile_w, 3), "Wh/day",
        margin=0.1, closed_by="CRS-OPT-001 Table 1; script")
a_ring = math.pi * (60.0 ** 2 - 52.0 ** 2)
wheel = 50e3                                          # N, one wheel of a 10 t axle (assumed)
c.claim("S20", "A stud's raised lens ring carries a wheel of a heavy axle", "Physics", "Strength of materials",
        "Wheel load over the 2,800 mm2 lens ring; polycarbonate compressive yield about 60 MPa (assumed), safety factor 1.5", round(wheel / a_ring, 1), 60.0 / 1.5, "MPa",
        closed_by="CRS-OPT-001 Table 1")
prx_st = CAL.TX_DBM + (-3.0 + 2.0) - CAL.CABLE_DB - CAL.fspl(15.0) - CAL.BLOCK_DB - 10.0
c.claim("S21", "Studs at road level (antenna gain -3 dBi, 10 dB ground loss) hear the bollard across 15 m", "Physics", "Electromagnetism and optics",
        "Free-space path loss with extra ground-reflection and blockage allowances (estimate)", round(prx_st - CAL.SENS_SF7, 1), 10.0, "dB", rule="above", closed_by="CRS-OPT-001 Table 1")

# ---------------------------------------------------------------- option C: pull-up retroreflective panel
H_FALL, S_STOP_PAD, S_STROKE = 0.25, 0.004, 0.025       # m: drop height, EPDM pad stop, damper stroke
v_fall = math.sqrt(2 * G * H_FALL)
g_nodamper = v_fall ** 2 / (2 * S_STOP_PAD) / G
g_damper = v_fall ** 2 / (2 * S_STROKE) / G
c.claim("S22", "The released panel stops from a 250 mm fall below 20 g, with the peak taken as twice the mean (end-of-travel damper, 25 mm stroke, CRS-DDR-005)", "Physics", "Mechanics and statics",
        "a = v^2 / (2 s) for v = sqrt(2 g h), times 2 for a real damper curve; the 20 g limit protects sheeting and fixings (assumed)", round(2 * g_damper, 1), 20.0, "g", margin=0.1, closed_by="CRS-DDR-005; CRS-OPT-001")
m_panel = 1.8                                          # kg, 3 mm aluminium 400 x 500 with sheeting, clip, cord share (estimate)
f_pull = m_panel * G / 0.95 * 1.1                      # pulley efficiency 0.95, guide friction 10 %
c.claim("S23", "A person lifts the panel with a pull of 22 N or less", "Physics", "Mechanics and statics",
        "Weight over pulley efficiency plus 10 % guide friction; 22.2 N is 5 lbf, the ADA operable-part force", round(f_pull, 1), 22.2, "N", margin=0.1, closed_by="CRS-OPT-001 Table 1")
c.cited("S24", "A retroreflective panel is seen by a driver at night without electricity", "Physics", "Electromagnetism and optics",
        "Retroreflective sheeting returns headlight beams to the driver; it needs no power, but the return depends on the sheeting class, the dirt and the panel angle",
        "No calculation at P3; sheeting datasheet to assess", PLAUSIBLE, closed_by="")

if __name__ == "__main__":
    s3_old = CAL.hot_old_e
    print(f"Record of the fixes: S3 with the 45 C charge limit stored {s3_old:.1f} Wh/day on a 50 C peak day against a {CAL.e_day:.1f} Wh/day load (Fails; fixed by a 55 C rated cell, CRS-DDR-005)")
    print(f"S5 with the first charcoal finish (alpha 0.70) the light bar worst case was {50 + CAL.bar_worst_dark:.1f} C against the 74 C limit (Fails; fixed by a white finish, CRS-DDR-005)")
    print(f"S22 with a 4 mm EPDM pad the panel stops at {g_nodamper:.0f} g (Fails the 20 g limit); with a 25 mm damper {g_damper:.0f} g (CRS-DDR-005)")
    c.write()
