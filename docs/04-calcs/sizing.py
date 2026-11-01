"""CrossSafe sizing calculations, CRS-CAL-001 v0.7 (TRL 3, constructable design of CRS-DDR-003, with the CRS-DDR-002 sun shield and anti-rotation detail;
STEM check fix CRS-DDR-005: battery charge limit 55 C; new sections C4, C5, I and J).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md (tags in brackets, for example [B3]) and
writes docs/04-calcs/results.csv. The script imports PARAMS and derived() from cad/src/model.py, so
heights, areas and post sizes are those of the STEP files and drawing CRS-DWG-001. It also reads
bom/bom.csv and budget_usd in project.yaml. First-principles paper estimates; nothing here is measured.
"""
import csv
import math
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, derived  # noqa: E402

D = derived(P)
rows = []


def out(tag, text):
    print(f"[{tag}] {text}")


def res(rid, name, value, target, status):
    rows.append((rid, name, value, target, status))


# =============================================================== assumptions
CROSS_M = 7.0            # design-case crossing, kerb to kerb
WALK = 0.9               # m/s design walking speed (R4)
ADD_S = 5.0              # s added to the walking time (R4)
T_ENERGY = 20.0          # s per activation used for the energy case (covers about 13.5 m)
ACTS = 300               # activations per day (design case)
# IA-21 flash sequence: 800 ms; each indication lit 4 x 50 ms (two single, two together)
SEQ_MS, LIT_MS = 800.0, 4 * 50.0
HEADS, HEAD_W = 4, 6.0   # heads per assembly, W per lit head in daytime (assumed, to be measured)
ETA_DRV = 0.91           # LED driver efficiency
PILOT_W = 0.3            # pedestrian pilot light, steady while flashing
# standby build-up
V_LOGIC = 3.3
I_RADIO_RX = 5.5e-3      # A, STM32WL-class radio in continuous LoRa receive (typical class figure, assumed)
I_MCU_PIR = 0.1e-3       # A, controller in stop mode with RTC, plus the PIR sensor
ETA_3V3 = 0.80           # 12 V to 3.3 V converter at light load
P_QUIESC_12V = 12.8 * 1e-3   # W, LED drivers disabled, fault indicator, BMS
P_CHARGER = 12.8 * 4e-3      # W, charger self-consumption 4 mA (BOM line 10 requirement)
P_RADAR = 0.4            # W, 24 GHz presence radar when on
RADAR_DUTY = 0.25        # fraction of the day the PIR keeps the radar on at a busy site (assumed)
TX_W, TX_S, PKTS = 0.15, 0.041, 2   # radio transmit power draw, time on air, packets per activation per side
# solar and storage
PANEL_W = 20.0
PSH_WORST, PSH_GOOD = 2.5, 5.0
DERATE, ETA_MPPT, ETA_CHG = 0.85, 0.94, 0.95   # panel heat and dust; charger; cell charge
BATT_V, BATT_AH, DOD = 12.8, 12.0, 0.80
CAP_COLD, CAP_EOL = 0.70, 0.80  # capacity at -20 C and at end of life (typical LiFePO4)
AUTONOMY_REQ = 5.0
# enclosure heat
G_BEAM, DIFFUSE = 900.0, 0.10     # W/m2 clear-sky beam; diffuse as a fraction of beam
SUN_EL = 70.0                      # deg, high summer sun in the tropics and mid latitudes
H_CONV = 10.0                      # W/m2K combined convection and radiation, still air
ALPHA_CLEAN, ALPHA_DUSTY = 0.45, 0.70
SHIELD = 0.25                      # fraction of solar gain passed by a ventilated shield (as WWT-CAL-001)
CHG_MAX, CELL_DIS_MAX = 55.0, 60.0 # C, charge limit (R8, 55 C since CRS-DDR-005; 45 C before) and discharge limit of LiFePO4
CHG_OLD = 45.0                     # C, the charge limit of CRS-REQ-001 v0.8, kept to show the hot-day failure it caused
BAR_LIMIT = 74.0                   # C, upper operating limit of an LED traffic signal module (Current Lighting TRAF336 datasheet)
BAR_ALPHA = {"clean": 0.30, "dusty": 0.55}   # white powder-coat finish of the light bar (CRS-DDR-005; assumed, to confirm); before: charcoal, 0.70 dusty
BAR_ALPHA_DARK = 0.70              # the charcoal finish of the first design, kept to show the failed STEM row S5
HEAT_LED = 0.85                    # fraction of LED electrical power leaving as heat
SOLID_ANGLE_LIM = 0.006            # sr, WCAG 2.1 general flash area limit (analogue; 25 % of a 10 degree field)
REACT_S, DECEL = 2.5, 3.4          # s perception-reaction time (AASHTO design value; 1.5 s in v0.7 draft) and m/s2 comfortable deceleration (assumed, to confirm)
SPEEDS_KMH = (40.0, 50.0, 60.0)    # approach speeds, 30 to 60 km/h roads (CRS-PRB-001)
# radio
SF, BW, CR, NPRE, PAYLOAD = 7, 125e3, 1, 8, 8
T_WAKE, T_PROC = 0.005, 0.006      # s, controller wake and processing each end
ACK_TIMEOUT_EXTRA = 0.020          # s beyond the ack time on air
RETRIES = 2
F_MHZ, TX_DBM, ANT_DBI, CABLE_DB = 868.0, 14.0, 2.0, 1.0
BLOCK_DB = 25.0                    # a bus or truck between the assemblies (assumed allowance)
SENS_SF7 = -123.0                  # dBm, SF7 125 kHz typical sensitivity
EU_DUTY = 0.01
PEAK_ACTS_H = 60                   # activations in the busiest hour (assumed)
# photometry screening
EFFICACY, OPTIC = 50.0, 0.80       # lm/W amber LED, optic efficiency (assumed)
BEAM_H, BEAM_V = 20.0, 10.0        # deg full beam widths
LANE_OFFSET, EYE_H = 3.5, 1.1      # m lateral offset of the near-lane driver's eye, eye height
# wind and structure
V_GUST, RHO, CD = 40.0, 1.225, 1.2
FY = 235.0                         # MPa, S235
STRESS_LIMIT = 0.60                # R9
E_STEEL = 210e3                    # MPa
ECC = 0.25                         # gust eccentricity as a fraction of sign width, for torsion
BAND_T, MU = 1000.0, 0.2           # N band tension (assumed), friction coefficient of a plain saddle
MU_KEY = 0.4                       # serrated keyed saddle grip friction (assumed, to be measured; CRS-DDR-002)
BOLT_D, BOLT_AS, BOLT_FUB = 10.0, 58.0, 700.0   # M10 A4-70 through-bolt: mm, tensile stress area mm2, MPa
FU_POST, GAMMA_M2 = 360.0, 1.25    # S235 ultimate strength MPa; partial factor (EN 1993-1-8 form)
ALPHA_B = 0.5                      # bearing factor, low-end value for a screening check
LAT_BEAR = 100.0                   # psf per ft of depth, clay (screening value, IBC Table 1806.2 class 5)
# cost
BUDGET_REC = 750.0                 # site-trial budget, decided by Amish 2026-09-25 (CRS-DDR-002), on hold with TRL 4


# =============================================================== A. flash time and pattern (R1, R4)
t_walk = CROSS_M / WALK
t_flash = t_walk + ADD_S
cover = (T_ENERGY - ADD_S) * WALK
duty = LIT_MS / SEQ_MS
out("A1", f"flash time for {CROSS_M:.0f} m: {t_walk:.1f} s walking + {ADD_S:.0f} s = {t_flash:.1f} s; "
          f"the {T_ENERGY:.0f} s energy case covers crossings up to {cover:.1f} m")
out("A2", f"IA-21 sequence: {SEQ_MS:.0f} ms, {60000 / SEQ_MS:.0f} sequences per minute; each indication lit "
          f"{LIT_MS:.0f} ms, duty {duty * 100:.0f} % (TRL 2 assumed 35 %)")
hw, hh = P["head"]
out("A3", f"head lens {hw:.0f} x {hh:.0f} mm against the 127 x 51 mm minimum; two heads per face, bar bottom "
          f"{P['bar_bottom']:.0f} mm, sign bottom point {D['sign_bot']:.0f} mm")
res("R1", "Light geometry and pattern", f"{hw:.0f} x {hh:.0f} mm lens; 75 per min; bar directly under the sign",
    "127 x 51 mm min.; IA-21 pattern", "Met by design")
res("R4", "Flash duration", f"{t_flash:.1f} s for 7 m; energy case {T_ENERGY:.0f} s", "L/0.9 + 5 s, 10 to 40 s",
    "Met by design")

# =============================================================== B. energy (R6, R7)
h_flash = ACTS * T_ENERGY / 3600
p_led = HEADS * HEAD_W * duty / ETA_DRV
e_led = p_led * h_flash
e_pilot = PILOT_W * h_flash
e_tx = ACTS * PKTS * TX_S * TX_W / 3600
p_logic = V_LOGIC * (I_RADIO_RX + I_MCU_PIR) / ETA_3V3
p_standby = p_logic + P_QUIESC_12V + P_CHARGER + P_RADAR * RADAR_DUTY
e_standby = p_standby * 24
e_day = e_led + e_pilot + e_tx + e_standby
out("B1", f"flashing {h_flash:.2f} h/day; LED power while flashing {p_led:.2f} W; LEDs {e_led:.2f} Wh/day; "
          f"pilot {e_pilot:.2f} Wh; radio transmit {e_tx:.3f} Wh")
out("B2", f"standby: logic {p_logic * 1000:.1f} mW, 12 V quiescent {P_QUIESC_12V * 1000:.1f} mW, charger "
          f"{P_CHARGER * 1000:.1f} mW, radar {P_RADAR * RADAR_DUTY * 1000:.0f} mW average ({RADAR_DUTY * 100:.0f} % on); "
          f"total {p_standby * 1000:.0f} mW, {e_standby:.2f} Wh/day")
out("B3", f"daily load {e_day:.1f} Wh/day (TRL 2 estimate 29.8 Wh/day)")
usable = BATT_V * BATT_AH * DOD
aut = usable / e_day
out("B4", f"battery {BATT_V * BATT_AH:.1f} Wh, usable {usable:.1f} Wh; autonomy {aut:.2f} days; at -20 C "
          f"{aut * CAP_COLD:.2f} days; end of life {aut * CAP_EOL:.2f} days; 18 Ah fallback {aut * 1.5:.2f} days")
# sensitivity cases
cases = {
    "radar ungated (no PIR)": p_standby - P_RADAR * RADAR_DUTY + P_RADAR,
    "radar on 50 % of the day": p_standby + P_RADAR * (0.5 - RADAR_DUTY),
    "TRL 2 controller 0.15 W and 10 mA charger, gated": 0.15 + 0.128 + P_QUIESC_12V + P_RADAR * RADAR_DUTY,
    "TRL 2 lumped standby 0.6 W": 0.6,
}
sens = {}
for k, ps in cases.items():
    ed = e_led + e_pilot + e_tx + ps * 24
    sens[k] = (ed, usable / ed)
    out("B5", f"sensitivity, {k}: standby {ps * 1000:.0f} mW, load {ed:.1f} Wh/day, autonomy {usable / ed:.2f} days")
e_store_worst = PANEL_W * PSH_WORST * DERATE * ETA_MPPT * ETA_CHG
chain = DERATE * ETA_MPPT * ETA_CHG
breakeven = e_day / (PANEL_W * chain)
e_store_good = PANEL_W * PSH_GOOD * chain
recover = usable / (e_store_good - e_day)
out("B6", f"system efficiency {chain * 100:.1f} %; stored at {PSH_WORST} PSH {e_store_worst:.1f} Wh/day, margin "
          f"{e_store_worst - e_day:.1f} Wh/day; break-even {breakeven:.2f} PSH; at {PSH_GOOD} PSH surplus "
          f"{e_store_good - e_day:.1f} Wh/day, 20 % to full in {recover:.2f} days")
i_chg = PANEL_W * DERATE * ETA_MPPT / BATT_V
i_dis = (p_led + PILOT_W + p_standby + P_RADAR * (1 - RADAR_DUTY)) / BATT_V
out("B7", f"peak charge current {i_chg:.2f} A ({i_chg / BATT_AH:.2f} C); peak discharge {i_dis:.2f} A; LED peak "
          f"with all four heads lit {HEADS * HEAD_W / ETA_DRV / BATT_V:.2f} A; 5 A fuse")
st6 = "At risk" if min(sens[k][1] for k in list(sens)[:3]) < AUTONOMY_REQ or aut * CAP_COLD * CAP_EOL < AUTONOMY_REQ else "Met on paper"
res("R6", "Autonomy", f"{aut:.1f} days ({aut * CAP_COLD:.1f} at -20 C; {aut * CAP_EOL:.1f} at end of life; {aut * CAP_COLD * CAP_EOL:.1f} at both)",
    "5 days or more", st6)
res("R7", "Energy balance", f"break-even {breakeven:.2f} PSH; recovery {recover:.1f} days",
    "neutral at 2.5 PSH; 3 days or fewer", "Met on paper")

# =============================================================== C. enclosure heat (R8)
ex, ey, ez = (v / 1000 for v in P["enc"])
a_tot = 2 * (ex * ey + ex * ez + ey * ez)
a_top = ex * ey
a_side = math.hypot(ey * ez, ex * ez)            # worst azimuth on the two visible walls
el = math.radians(SUN_EL)
a_proj = a_top * math.sin(el) + a_side * math.cos(el)
p_int = PANEL_W * DERATE * (1 - ETA_MPPT) + p_logic
therm = {}
for name, alpha, f in (("clean", ALPHA_CLEAN, 1.0), ("dusty", ALPHA_DUSTY, 1.0), ("dusty, shielded", ALPHA_DUSTY, SHIELD)):
    q = alpha * G_BEAM * (1 + DIFFUSE) * a_proj * f + p_int
    dt = q / (H_CONV * a_tot)
    therm[name] = dt
    out("C1", f"{name}: solar gain {q - p_int:.1f} W + internal {p_int:.1f} W; rise {dt:.1f} K; interior "
              f"{45 + dt:.1f} C at 45 C and {50 + dt:.1f} C at 50 C ambient; charging stops above {CHG_MAX - dt:.1f} C ambient")
out("C2", f"enclosure area {a_tot:.3f} m2, sunlit projection {a_proj:.4f} m2 at {SUN_EL:.0f} deg elevation")
dt_d = therm["dusty, shielded"]          # design case: the sun shield is fitted (CRS-DDR-002)
out("C3", f"design case with the sun shield (CRS-DDR-002): interior {50 + dt_d:.1f} C at 50 C ambient against the "
          f"{CELL_DIS_MAX:.0f} C discharge limit; charging stops above {CHG_MAX - dt_d:.1f} C ambient "
          f"(unshielded, dusty: {50 + therm['dusty']:.1f} C and {CHG_MAX - therm['dusty']:.1f} C)")
# C4. Hot-day charging window (STEM check S3, fixed by CRS-DDR-005). Daily ambient 7.5 K either side of its mean, peak at 15:00;
# sun a half sine from 06:00 to 18:00; the cell temperature is the ambient plus the shielded rise; no charge above the limit.
def hot_day(peak_c, limit, psh=6.5, rise=None):
    rise = dt_d if rise is None else rise
    tot = ok = 0.0
    for k in range(1440):
        t = k / 60
        sun = max(0.0, math.sin(math.pi * (t - 6) / 12)) if 6 <= t <= 18 else 0.0
        amb = peak_c - 7.5 + 7.5 * math.sin(2 * math.pi * (t - 9) / 24)
        tot += sun
        ok += sun if amb + rise <= limit else 0.0
    return ok / tot, PANEL_W * psh * chain * ok / tot
for peak in (45.0, 48.0, 50.0):
    f45, e45 = hot_day(peak, CHG_OLD)
    f55, e55 = hot_day(peak, CHG_MAX)
    d_old = (usable / max(e_day - e45, 1e-9)) if e45 < e_day else float("inf")
    out("C4", f"hot day, {peak:.0f} C peak, 6.5 peak sun hours: with a {CHG_OLD:.0f} C charge limit {f45 * 100:.0f} % of the sun is usable, {e45:.1f} Wh/day stored "
              f"against a {e_day:.1f} Wh/day load ({'battery empties in ' + format(d_old, '.0f') + ' days' if e45 < e_day else 'neutral'}); with {CHG_MAX:.0f} C: {f55 * 100:.0f} %, {e55:.1f} Wh/day")
hot_f, hot_e = hot_day(50.0, CHG_MAX)
hot_old_f, hot_old_e = hot_day(50.0, CHG_OLD)
# C5. Light bar heat (PR-017): sealed 2 mm aluminium channel, same method as C1, dusty (alpha 0.70), still air, no shield.
bx_, by_, bz_ = (v / 1000 for v in P["bar"])
a_bar = 2 * (bx_ * by_ + bx_ * bz_ + by_ * bz_)
a_bar_proj = bx_ * by_ * math.sin(el) + math.hypot(by_ * bz_, bx_ * bz_) * math.cos(el)
p_bar_led = HEADS * HEAD_W * duty / ETA_DRV * HEAT_LED * (T_ENERGY * ACTS / 86400)   # day-average LED heat inside the bar, W
bar = {}
for name, alpha in (("clean", BAR_ALPHA["clean"]), ("dusty", BAR_ALPHA["dusty"])):
    q = alpha * G_BEAM * (1 + DIFFUSE) * a_bar_proj + p_bar_led
    bar[name] = q / (H_CONV * a_bar)
    out("C5", f"light bar {name}: area {a_bar:.3f} m2, sunlit {a_bar_proj:.4f} m2, solar gain {alpha * G_BEAM * (1 + DIFFUSE) * a_bar_proj:.1f} W, "
              f"rise {bar[name]:.1f} K, interior {50 + bar[name]:.1f} C at 50 C ambient against the {BAR_LIMIT:.0f} C module limit")
# C6. Sensitivity of the 55 C fix (independent review of CRS-STM-001): lower sun at the hottest hour, a less effective shield, both.
def shielded_rise(el_deg, shield):
    e = math.radians(el_deg)
    ap = a_top * math.sin(e) + a_side * math.cos(e)
    return (ALPHA_DUSTY * G_BEAM * (1 + DIFFUSE) * ap * shield + p_int) / (H_CONV * a_tot)
sens_c = {}
for label, el_d, sh in (("sun 70 deg, shield 0.25 (design)", 70.0, SHIELD), ("sun 45 deg, shield 0.25", 45.0, SHIELD),
                        ("sun 70 deg, shield 0.50", 70.0, 0.5), ("sun 45 deg, shield 0.50", 45.0, 0.5)):
    rise = shielded_rise(el_d, sh)
    f55, e55 = hot_day(50.0, CHG_MAX, rise=rise)
    sens_c[label] = (rise, 50.0 + rise, f55, e55)
    out("C6", f"{label}: rise {rise:.1f} K, cell {50 + rise:.1f} C at 50 C ambient, {f55 * 100:.0f} % of the sun usable at a 50 C peak with the {CHG_MAX:.0f} C limit, {e55:.1f} Wh/day stored against {e_day:.1f}")
worst_store = min(v[3] for v in sens_c.values())
# Cold days: the BMS stops charging below 0 C cell temperature; the cell sits at most the shielded rise above ambient.
cold_amb = 0.0 - dt_d
out("C7", f"cold: charging is inhibited below 0 C cell temperature, so below about {cold_amb:.1f} C ambient in full sun (and always at night) nothing is stored; "
          f"autonomy at -20 C is {aut * CAP_COLD:.2f} days and {aut * CAP_COLD * CAP_EOL:.2f} days at end of life as well (no heater, R6)")
# C5b. Worst case for the bar (independent review): sun at the elevation that maximises the sunlit area, dusty, and the LEDs lit continuously.
a_bar_worst = math.hypot(bx_ * by_, math.hypot(by_ * bz_, bx_ * bz_))
p_bar_cont = HEADS * HEAD_W * duty / ETA_DRV * HEAT_LED                      # LED heat with the sequence running continuously, W
bar_worst = (BAR_ALPHA["dusty"] * G_BEAM * (1 + DIFFUSE) * a_bar_worst + p_bar_cont) / (H_CONV * a_bar)
bar_worst_dark = (BAR_ALPHA_DARK * G_BEAM * (1 + DIFFUSE) * a_bar_worst + p_bar_cont) / (H_CONV * a_bar)
out("C5", f"light bar worst case with the first (charcoal, 0.70) finish: {50 + bar_worst_dark:.1f} C at 50 C ambient (failed S5); with the white finish below")
out("C5", f"light bar worst case: sunlit {a_bar_worst:.4f} m2 at the worst elevation, LEDs flashing continuously ({p_bar_cont:.1f} W): rise {bar_worst:.1f} K, "
          f"interior {50 + bar_worst:.1f} C at 50 C ambient against the {BAR_LIMIT:.0f} C module limit")
res("R8", "Environment", f"interior {50 + dt_d:.1f} C at 50 C (dusty, shielded); charging to {CHG_MAX - dt_d:.1f} C ambient; "
    f"light bar {50 + bar_worst:.1f} C", f"IP65; -20 to +50 C; charge 0 to {CHG_MAX:.0f} C",
    "Met on paper" if (50 + dt_d <= CELL_DIS_MAX and CHG_MAX - dt_d >= 50.0 and 50 + bar_worst <= BAR_LIMIT) else "At risk")
res("R17", "Light bar temperature", f"{50 + bar['dusty']:.1f} C at 50 C ambient (dusty, 70 deg sun); {50 + bar_worst:.1f} C worst case", f"{BAR_LIMIT:.0f} C or less",
    "Met on paper" if 50 + bar_worst <= BAR_LIMIT else "At risk")

# =============================================================== D. radio link and latency (R3)
tsym = 2 ** SF / BW
npay = 8 + max(math.ceil((8 * PAYLOAD - 4 * SF + 28 + 16) / (4 * SF)) * (CR + 4), 0)
toa = (NPRE + 4.25) * tsym + npay * tsym
lat1 = T_WAKE + toa + T_PROC + 0.001
timeout = toa + ACK_TIMEOUT_EXTRA
lat_worst = lat1 + RETRIES * (timeout + T_PROC + toa)
out("D1", f"time on air, {PAYLOAD}-byte packet at SF{SF} 125 kHz: {toa * 1000:.1f} ms")
out("D2", f"latency, first attempt {lat1 * 1000:.0f} ms; with {RETRIES} retries {lat_worst * 1000:.0f} ms (target 500 ms)")
fspl = lambda d: 20 * math.log10(d) + 20 * math.log10(F_MHZ * 1e6) - 147.55
for dist in (7.0, 15.0):
    prx = TX_DBM + 2 * ANT_DBI - 2 * CABLE_DB - fspl(dist) - BLOCK_DB
    out("D3", f"{dist:.0f} m with {BLOCK_DB:.0f} dB blockage: path loss {fspl(dist):.1f} dB, received {prx:.1f} dBm, "
              f"margin {prx - SENS_SF7:.1f} dB")
air_h = PEAK_ACTS_H * PKTS * toa
out("D4", f"busiest hour {PEAK_ACTS_H} activations: {air_h:.1f} s on air per side against {EU_DUTY * 3600:.0f} s (1 % duty)")
checkin_s = 60 * 1 * TX_S                                                      # one 1 min check-in packet per side (PR-012 lost-link detection), s per hour
out("D5", f"lost-link check-in, one packet a minute: {checkin_s:.1f} s on air per hour, {1440 * TX_S * TX_W / 3600 * 1000:.1f} mWh/day; with the busiest hour {air_h + checkin_s:.1f} s against {EU_DUTY * 3600:.0f} s")
res("R3", "Activation and sync", f"{lat1 * 1000:.0f} ms, {lat_worst * 1000:.0f} ms with retries", "0.5 s or less",
    "Met on paper")

# =============================================================== E. photometry screening (R2)
omega = math.radians(BEAM_H) * math.radians(BEAM_V)
i_cd = HEAD_W * EFFICACY * OPTIC / omega
for dist in (100.0, 30.0):
    e_lx = i_cd / dist ** 2
    ang_h = math.degrees(math.atan(LANE_OFFSET / dist))
    ang_v = math.degrees(math.atan((D["bar_zc"] / 1000 - EYE_H) / dist))
    out("E1", f"at {dist:.0f} m: about {i_cd:,.0f} cd on axis, {e_lx:.2f} lx at the eye; driver {ang_h:.1f} deg off "
              f"axis horizontally, {ang_v:.1f} deg below the head (beam half widths {BEAM_H / 2:.0f} and {BEAM_V / 2:.0f} deg)")
res("R2", "Visibility", f"about {i_cd:,.0f} cd per head (screening)", "seen at 100 m in sun; dimmed at night",
    "Not verifiable at TRL 3")
res("R5", "Detection quality", "PIR wakes radar; 1 s dwell", "5 % false, 2 % missed", "Not verifiable at TRL 3")

# =============================================================== F. heights and mounting (R10, R11, R14)
enc_bot = D["enc_bot"]
radar_low = D["pir_bot"]
out("F1", f"button centre {P['button_z']:.0f} mm; bar bottom {P['bar_bottom']:.0f} mm; enclosure bottom {enc_bot:.0f} mm; "
          f"radar arm {P['radar_z']:.0f} mm (PIR underside {radar_low:.0f} mm); overall height {D['overall_h']:.0f} mm")
out("F2", f"band clamps fit {P['pole_min_od']:.0f} to {P['pole_max_od']:.1f} mm poles; post {P['post_od']} x {P['post_wall']} mm")
install = {"clamps, saddles and bar with sign": 30, "enclosure (shield fitted on the ground), battery and wiring": 35, "panel and bracket": 20,
           "button, radar, PIR and cable cover": 20, "setup and radio pairing": 15}
t_inst = sum(install.values())
out("F3", f"installation estimate, two-person crew on an existing pole: {t_inst} min ({', '.join(f'{k} {v}' for k, v in install.items())})")
res("R10", "Mounting", f"76 to 114.3 mm poles; bar at {P['bar_bottom'] / 1000:.1f} m; about {t_inst} min estimate",
    "fit; 2.1 m; 2 h", "Not verifiable at TRL 3")   # range restated 2026-10-02: 76 mm and up (CRS-DEC-001)
res("R11", "Accessibility", f"button {P['button_z'] / 1000:.2f} m; piezo; tone, tactile arrow, pilot light",
    "0.9 to 1.1 m; 22 N or less", "Met by design")
res("R12", "Fail-safe", "timer-limited flashing; local flashing without link; fault log", "never continuous",
    "Met by design")
res("R13", "Privacy", "presence and counts only", "no images or audio", "Met by design")
res("R14", "Theft and vandal resistance", f"enclosure bottom {enc_bot / 1000:.2f} m; lowest arm part {radar_low / 1000:.2f} m",
    "2.8 m; no cables below 2.5 m", "Met by design")

# =============================================================== G. wind and structure (R9)
q = 0.5 * RHO * V_GUST ** 2
H = D["heights"]


def loads(areas):
    F = {k: CD * q * a for k, a in areas.items()}
    M = {k: F[k] * H[k] / 1000 for k in F}
    return F, M


Fx, Mx = loads(D["area_x"])
Fy, My = loads(D["area_y"])
mx, my = sum(Mx.values()), sum(My.values())
out("G1", f"q = {q:.0f} Pa; wind along the road: force {sum(Fx.values()):.0f} N, base moment {mx:.0f} N m "
          f"(sign {Mx['sign']:.0f}, post {Mx['post']:.0f}, enclosure {Mx['enc']:.0f}, bar {Mx['bar']:.0f})")
out("G2", f"wind across the road: force {sum(Fy.values()):.0f} N, base moment {my:.0f} N m (panel {My['panel']:.0f})")


def smod(D_, t):
    d = D_ - 2 * t
    return math.pi / 32 * (D_ ** 4 - d ** 4) / D_, math.pi / 64 * (D_ ** 4 - d ** 4)


posts = [(76.1, 3.2), (88.9, 4.0), (P["post_od"], P["post_wall"])]
ratios = {}
for od, t in posts:
    S, I = smod(od, t)
    # the post's own wind area scales with its diameter
    m = mx - Mx["post"] + Mx["post"] * od / P["post_od"]
    sig = m * 1e3 / S
    ratios[od] = sig / FY
    out("G3", f"post {od} x {t} mm: S = {S:,.0f} mm3, M = {m:.0f} N m, stress {sig:.0f} MPa, {sig / FY * 100:.0f} % of yield")
# 600 mm sign on the 88.9 post
S89, _ = smod(88.9, 4.0)
m600 = mx - Mx["sign"] * (1 - (0.6 / 0.75) ** 2) - Mx["post"] * (1 - 88.9 / P["post_od"])
out("G4", f"600 mm sign on 88.9 x 4 mm: {m600 * 1e3 / S89:.0f} MPa, {m600 * 1e3 / S89 / FY * 100:.0f} % of yield")
# deflection of the 114.3 post at the top under wind along the road
S, I = smod(P["post_od"], P["post_wall"])
L = P["post_h"]
defl = sum(Fx[k] * (H[k]) ** 2 * (3 * L - H[k]) / (6 * E_STEEL * I) for k in Fx if H[k] <= L)
out("G5", f"top deflection of the 114.3 mm post in the 40 m/s gust: {defl:.0f} mm ({defl / L * 100:.1f} % of height)")
# clamp torsion
sign_w = P["sign_side"] * math.sqrt(2) / 1000
t_sign = Fx["sign"] * ECC * sign_w
r = P["post_od"] / 2000
t_band = MU * 2 * math.pi * BAND_T * r
out("G6", f"sign torsion with {ECC:.2f} x width eccentricity: {t_sign:.0f} N m; two bands at {BAND_T:.0f} N resist "
          f"{2 * t_band:.0f} N m on 114.3 mm and {2 * MU * 2 * math.pi * BAND_T * 0.030:.0f} N m on a 60 mm pole (a plain saddle, friction {MU}; shown for comparison)")
# footing depth, non-constrained pole (screening, after IBC 1807.3.2.1)
Pl = sum(Fx.values()) * 0.2248                     # lbf
h_ft = mx / sum(Fx.values()) * 3.281               # height of the resultant, ft
b = P["footing_d"] / 304.8
d = 3.0
for _ in range(50):
    S1 = LAT_BEAR * d / 3
    A = 2.34 * Pl / (S1 * b)
    d = 0.5 * A * (1 + math.sqrt(1 + 4.36 * h_ft / A))
out("G7", f"footing: lateral {Pl:.0f} lbf at {h_ft:.1f} ft; required depth {d:.2f} ft ({d * 304.8:.0f} mm) for a "
          f"{P['footing_d']:.0f} mm footing in clay; modeled {P['embed']:.0f} mm")
# anti-rotation (CRS-DDR-002): through-bolt on new posts, keyed saddles on existing poles
f_bear = t_sign / (P["post_od"] / 1000)           # couple on the two post walls, N
v_rd = 0.6 * BOLT_FUB * BOLT_AS / GAMMA_M2
b_rd = 2.5 * ALPHA_B * FU_POST * BOLT_D * P["post_wall"] / GAMMA_M2
out("G6b", f"new post, M10 through-bolt: {f_bear:.0f} N per wall; bolt shear {v_rd:,.0f} N per plane "
           f"({f_bear / v_rd * 100:.0f} %); wall bearing {b_rd:,.0f} N ({f_bear / b_rd * 100:.0f} %)")
key_tq = lambda od: 2 * MU_KEY * 2 * math.pi * BAND_T * od / 2000
od_min = t_sign / (2 * MU_KEY * 2 * math.pi * BAND_T) * 2000
out("G6c", f"existing poles, keyed saddles at friction {MU_KEY}: two bands resist {key_tq(P['pole_max_od']):.0f} N m on "
           f"114.3 mm and {key_tq(P['pole_min_od']):.0f} N m on {P['pole_min_od']:.0f} mm against {t_sign:.0f} N m; holds on poles of "
           f"{od_min:.0f} mm and up")
added = mx - Mx["post"]
out("G8", f"moment added to an existing pole at the sidewalk: {added:.0f} N m")
st9 = "Met on paper" if ratios[P["post_od"]] <= STRESS_LIMIT else "Not met"
ok_rot = f_bear < min(v_rd, b_rd) and key_tq(P["pole_min_od"]) >= t_sign
s_min = added * 1000 / (STRESS_LIMIT * FY)        # mm3, from the moment the kit adds alone (the pole's own load is on top)
out("G9", f"existing poles: the added {added:.0f} N m alone needs a section modulus of at least {s_min:,.0f} mm3 at 60 % of yield (a 76.1 x 3.2 mm pole has "
          f"{12820:,}); the pole owner verifies the pole, the kit is not a structural pole upgrade")
res("R9", "Structure", f"{ratios[P['post_od']] * 100:.0f} % of yield on 114.3 mm; bolt {f_bear / b_rd * 100:.0f} % of "
    f"bearing; keyed saddles hold on poles of {od_min:.0f} mm and up; existing poles need S of {s_min:,.0f} mm3 or more (owner verifies)", "60 % of yield or less",
    st9 if ok_rot else "At risk")

# =============================================================== H. cost (R15)
bom = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
tot = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom)
var = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in bom if r["notes"].startswith("Variant only"))  # new-post lines 14, 19
base = tot - var
budget = float(yaml.safe_load((ROOT / "project.yaml").read_text())["budget_usd"])
out("H1", f"{len(bom)} BOM lines, all priced; one assembly on an existing pole ${base:.2f}; with its own post ${tot:.2f}")
out("H2", f"against budget_usd ${budget:.0f}: existing pole {base - budget:+.2f}; own post {tot - budget:+.2f}")
out("H3", f"two-sided crossing: existing poles ${2 * base:.2f}, new posts ${2 * tot:.2f}; against the "
          f"decided ${BUDGET_REC:.0f} site-trial budget (on hold with TRL 4): {2 * base - BUDGET_REC:+.2f} and {2 * tot - BUDGET_REC:+.2f}")
res("R15", "Affordable", f"${base:.2f} per assembly; ${2 * base:.2f} per crossing (existing poles)",
    "$350; $700 per crossing", "Met on paper" if base <= budget and 2 * base <= 700 else "Not met")

# =============================================================== I. flash area and driver stopping distance (R16, R1, R2)
# Lit solid angle of the two lit heads at the nearest place a pedestrian stands (button, 1 m from the pole, 2.1 m up): a screen against
# the WCAG 2.1 general-flash area limit, used as an analogue for photosensitivity (no road standard checked; not a clinical statement).
a_lit = 2 * hw * hh / 1e6
for dist in (3.0, 1.5):
    om = a_lit / dist ** 2
    out("I1", f"two lit heads {a_lit * 1e4:.0f} cm2 seen from {dist:.1f} m subtend {om * 1000:.2f} msr against the {SOLID_ANGLE_LIM * 1000:.0f} msr analogue limit")
res("R16", "Flash area", f"{a_lit / 1.5 ** 2 * 1000:.2f} msr at 1.5 m", f"{SOLID_ANGLE_LIM * 1000:.0f} msr or less (analogue)",
    "Met on paper" if a_lit / 1.5 ** 2 <= SOLID_ANGLE_LIM else "At risk")
for v in SPEEDS_KMH:
    u = v / 3.6
    s_stop = u * REACT_S + u ** 2 / (2 * DECEL)
    out("I2", f"approach {v:.0f} km/h: stopping distance {s_stop:.0f} m ({u * REACT_S:.0f} m reaction + {u ** 2 / (2 * DECEL):.0f} m braking) against 100 m sight line")
    s_stop_max = s_stop
res("R18", "Warning in time to stop", f"{s_stop_max:.0f} m stopping distance at {SPEEDS_KMH[-1]:.0f} km/h against the 100 m seeing distance of PR-002",
    "stopping distance at 60 km/h within 100 m", "Met on paper" if s_stop_max <= 100.0 else "Not met")   # holds only while PR-002 holds (100 m seeing distance)
res("R19", "Buildable and repairable", "BLD-001: stock sections, bought parts, hand tools; 117 modelled parts, none bare", "ordinary tools only",
    "Met by design")

# =============================================================== results
order = [f"R{i}" for i in range(1, 20)]
rows.sort(key=lambda r: order.index(r[0]))
print("\nRequirement results")
for r in rows:
    print(f"  {r[0]:<4} {r[4]:<24} {r[2]}")
counts = {}
for r in rows:
    counts[r[4]] = counts.get(r[4], 0) + 1
print("  counts:", ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
with (ROOT / "docs/04-calcs/results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "requirement", "value", "target", "status"])
    w.writerows(rows)
