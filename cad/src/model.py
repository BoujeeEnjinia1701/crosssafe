"""CrossSafe parametric model (build123d), TRL 3, massing-plus level of detail. Sun shield, keyed sign
saddles and the new-post anti-rotation bolt added under CRS-DDR-002.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    crosssafe-assembly.step / .stl       one beacon assembly on its own 114.3 mm post, with footing
    crosssafe-existing-pole.step / .stl  the same assembly without post, footing and anti-rotation bolt (existing-pole kit, the
                                         prototype that budget_usd covers, CRS-DDR-001 D1)
    sign-and-light-bar.step / .stl       sign, light bar, LED heads and pilot light
    pole-top-enclosure.step / .stl       enclosure with battery, charger, controller, antenna and sun shield

Axes (local frame): the post axis is the Z axis, Z is up with the sidewalk top at z = 0. Traffic runs
along X and the sign faces approaching traffic on +X. The kerb and the waiting zone are on +Y; the solar
panel faces the equator on -Y. For right-hand traffic the assembly mirrors. cad/src/concept_media.py
places this frame in the street scene.

Main dimensions and interfaces only. Not fabrication detail; not for fabrication. The same PARAMS feed
docs/04-calcs/sizing.py (CRS-CAL-001) and drawing CRS-DWG-001 (cad/src/sheets.py).
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 14 post: 114.3 x 3.6 mm galvanized steel (CRS-DDR-001 D3), height above the sidewalk, embedment
    "post_od": 114.3, "post_wall": 3.6, "post_h": 3700.0, "embed": 1800.0, "footing_d": 500.0,
    # existing poles the band clamps must fit (R10)
    "pole_min_od": 60.0, "pole_max_od": 114.3,
    # 1 crossing warning sign: square side (diamond), thickness, stand-off in front of the post
    "sign_side": 750.0, "sign_t": 3.0, "sign_gap": 6.0,
    # 2 light bar housing (X depth, Y length, Z height), bottom height, gap to the sign point
    "bar": (70.0, 720.0, 130.0), "bar_bottom": 2100.0, "bar_sign_gap": 20.0,
    # 3 LED heads: lens (Y width, Z height), head centers from bar center along Y, two per face
    "head": (140.0, 62.0), "head_dy": 200.0,
    # 17 pedestrian pilot light on the kerb end of the light bar
    "pilot_d": 30.0,
    # 4 push-button station: body center height, body (X, Y, Z), instruction plate (X width, Z height)
    "button_z": 1050.0, "button": (70.0, 60.0, 160.0), "plate": (230.0, 300.0),
    # 5 presence radar and 16 PIR sensor on a short arm toward the kerb (+Y)
    "radar_z": 2600.0, "arm_l": 200.0, "radar": 80.0, "pir_d": 40.0,
    # 6 solar panel (X, Y, thickness), tilt toward the equator (-Y), rise of its center above the post top
    "panel": (500.0, 360.0, 25.0), "panel_tilt": 30.0, "panel_rise": 230.0,
    # 8 enclosure (X depth, Y width, Z height), wall, center height, stand-off behind the post (-X)
    "enc": (150.0, 260.0, 300.0), "enc_wall": 4.0, "enc_z": 3000.0, "enc_gap": 80.0,
    # 9 to 12 parts inside and on the enclosure
    "battery": (95.0, 151.0, 98.0), "mppt": (40.0, 90.0, 60.0), "board": (14.0, 180.0, 100.0),
    "antenna": (8.0, 220.0),
    # 13 clamps: band thickness and width
    "band_t": 8.0, "band_w": 30.0,
    # 18 ventilated sun shield over the enclosure (CRS-DDR-002): air gap to the enclosure, sheet thickness
    "shield_gap": 25.0, "shield_t": 2.0,
    # 20 keyed sign saddles (two, at the sign clamps): Y width, Z height
    "saddle": (80.0, 60.0),
    # 19 anti-rotation bolt, new posts only: diameter
    "bolt_d": 10.0,
}

BOM = {1: "Crossing warning sign", 2: "Light bar housing", 3: "Amber LED heads", 4: "Push-button station",
       5: "Presence radar", 6: "Solar panel", 7: "Panel bracket", 8: "Enclosure", 9: "LiFePO4 battery",
       10: "MPPT charge controller", 11: "Controller and radio board", 12: "Antenna", 13: "Pole clamps",
       14: "Post", 16: "PIR wake sensor", 17: "Pedestrian pilot light", 18: "Sun shield",
       19: "Anti-rotation bolt", 20: "Keyed sign saddles"}


def derived(p=PARAMS):
    """Heights, envelopes and wind areas the calc note and drawing quote, computed from PARAMS."""
    r = p["post_od"] / 2
    bx, by, bz = p["bar"]
    bar_zc = p["bar_bottom"] + bz / 2
    half_diag = p["sign_side"] / math.sqrt(2)
    sign_zc = p["bar_bottom"] + bz + p["bar_sign_gap"] + half_diag
    ex, ey, ez = p["enc"]
    px, py, pt = p["panel"]
    tilt = math.radians(p["panel_tilt"])
    panel_zc = p["post_h"] + p["panel_rise"]
    panel_top = panel_zc + py / 2 * math.sin(tilt) + pt / 2 * math.cos(tilt)
    g, st = p["shield_gap"], p["shield_t"]
    shx, shy, shz = ex + g + st, ey + 2 * (g + st), ez + g + st   # shield envelope (open front and bottom)
    return {
        "post_r": r,
        "bar_xc": r + bx / 2 + 16.0,                   # bar just in front of the post, clear of the clamps
        "bar_zc": bar_zc, "bar_top": p["bar_bottom"] + bz,
        "sign_xc": r + bx + 16.0 + p["sign_gap"] + p["sign_t"] / 2,
        "sign_zc": sign_zc, "sign_bot": sign_zc - half_diag, "sign_top": sign_zc + half_diag,
        "sign_area_m2": p["sign_side"] ** 2 / 1e6,
        "enc_xc": -(r + p["enc_gap"]), "enc_bot": p["enc_z"] - ez / 2, "enc_top": p["enc_z"] + ez / 2,
        "shield": (shx, shy, shz), "sign_clamp_z": (sign_zc - 250.0, sign_zc + 250.0),
        "panel_zc": panel_zc, "overall_h": panel_top,
        "panel_area_m2": px * py / 1e6,
        # wind areas (m2) normal to X (traffic direction) and to Y (across the road)
        "area_x": {"sign": p["sign_side"] ** 2 / 1e6, "bar": by * bz / 1e6, "enc": shy * shz / 1e6,
                   "panel": py * pt / 1e6,                     # panel edge-on to X wind
                   "button": p["button"][1] * p["button"][2] / 1e6, "radar": p["radar"] ** 2 / 1e6,
                   "post": p["post_od"] * p["post_h"] / 1e6},
        "area_y": {"sign": p["sign_side"] * math.sqrt(2) * p["sign_t"] / 1e6, "bar": bx * bz / 1e6,
                   "enc": ex * ez / 1e6, "panel": px * py * math.sin(tilt) / 1e6,
                   "button": p["plate"][0] * p["plate"][1] / 1e6, "radar": p["radar"] ** 2 / 1e6,
                   "post": p["post_od"] * p["post_h"] / 1e6},
        "heights": {"sign": sign_zc, "bar": bar_zc, "enc": p["enc_z"], "panel": panel_zc,
                    "button": p["button_z"] + 140.0, "radar": p["radar_z"], "post": p["post_h"] / 2},
    }


def build_parts(p=PARAMS, own_post=True):
    """Return {bom_no: shape} for one assembly, plus 'footing' when own_post is True."""
    from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
    D = derived(p)
    r = D["post_r"]

    def rod(a, b, rad):
        a = Vector(*a); b = Vector(*b); d = b - a
        return Solid.make_cylinder(rad, d.length, Plane(origin=a, z_dir=d.normalized()))

    def band(z, rad=r):
        t, w = p["band_t"], p["band_w"]
        return Pos(0, 0, z) * (Cylinder(rad + t, w) - Cylinder(rad, w + 2))

    parts = {}
    # 1 sign, a square turned 45 degrees in the Y-Z plane
    parts[1] = Pos(D["sign_xc"], 0, D["sign_zc"]) * Rot(45, 0, 0) * Box(p["sign_t"], p["sign_side"], p["sign_side"])
    # 2 light bar, with a mounting saddle to the post
    bx, by, bz = p["bar"]
    parts[2] = (Pos(D["bar_xc"], 0, D["bar_zc"]) * Box(bx, by, bz)
                + Pos(r + 8, 0, D["bar_zc"]) * Box(16, 80, 100))
    # 3 LED heads, two per face (front +X faces traffic, back -X faces the other direction)
    hw, hh = p["head"]
    heads = None
    for y in (-p["head_dy"], p["head_dy"]):
        for x in (D["bar_xc"] + bx / 2 + 4, D["bar_xc"] - bx / 2 - 4):
            h = Pos(x, y, D["bar_zc"]) * Box(8, hw, hh)
            heads = h if heads is None else heads + h
    parts[3] = heads
    # 17 pilot light on the kerb end of the bar
    parts[17] = Pos(D["bar_xc"], by / 2 + 10, D["bar_zc"]) * Rot(90, 0, 0) * Cylinder(p["pilot_d"] / 2, 20)
    # 4 push-button station on the kerb side of the post, plate above it
    ux, uy, uz = p["button"]
    wx, wz = p["plate"]
    parts[4] = (Pos(0, r + uy / 2, p["button_z"]) * Box(ux, uy, uz)
                + Pos(0, r + 4, p["button_z"] + uz / 2 + 20 + wz / 2) * Box(wx, 4, wz))
    # 5 radar on an arm toward the kerb; 16 PIR under the radar
    z = p["radar_z"]; a = p["arm_l"]; s = p["radar"]
    parts[5] = rod((0, r, z), (0, r + a, z), 12) + Pos(0, r + a + s / 2, z) * Box(s, s, s)
    parts[16] = Pos(0, r + a + s / 2, z - s / 2 - p["pir_d"] / 2) * Cylinder(p["pir_d"] / 2, p["pir_d"])
    # 6 panel on 7 bracket, tilted toward -Y
    px, py, pt = p["panel"]
    parts[6] = Pos(0, 0, D["panel_zc"]) * Rot(p["panel_tilt"], 0, 0) * Box(px, py, pt)
    parts[7] = (Pos(0, 0, p["post_h"] + 60) * Cylinder(r + 6, 120)
                + Pos(0, 0, p["post_h"] + 150) * Box(60, 60, 80)
                + Pos(0, 0, D["panel_zc"] - 25) * Rot(p["panel_tilt"], 0, 0) * Box(300, 160, 10))
    # 8 enclosure behind the post, hollow shell with a back plate to the post
    ex, ey, ez = p["enc"]; w = p["enc_wall"]
    xc = D["enc_xc"]
    parts[8] = (Pos(xc, 0, p["enc_z"]) * (Box(ex, ey, ez) - Box(ex - 2 * w, ey - 2 * w, ez - 2 * w))
                + Pos(-(r + (p["enc_gap"] - ex / 2) / 2), 0, p["enc_z"]) * Box(p["enc_gap"] - ex / 2, 120, 200))
    # 9 battery low in the box, 10 charger and 11 controller above, 12 antenna on the roof
    b = p["battery"]
    parts[9] = Pos(xc, 0, D["enc_bot"] + w + b[2] / 2) * Box(*b)
    m = p["mppt"]
    parts[10] = Pos(xc - 30, 55, p["enc_z"] + 10) * Box(*m)
    c = p["board"]
    parts[11] = Pos(xc + ex / 2 - w - c[0] / 2 - 4, 0, p["enc_z"] + 60) * Box(*c)
    ad, al = p["antenna"]
    parts[12] = Pos(xc, 90, D["enc_top"] + al / 2) * Cylinder(ad, al)
    # 18 ventilated sun shield: roof and three walls with an air gap, open at the bottom and toward the post
    g, st = p["shield_gap"], p["shield_t"]
    shx, shy, shz = D["shield"]
    x_front = xc + ex / 2                       # enclosure face toward the post
    x_back = x_front - shx
    z_top = D["enc_top"] + g
    roof = Pos(x_front - shx / 2, 0, z_top + st / 2) * Box(shx, shy, st)
    back = Pos(x_back + st / 2, 0, z_top - shz / 2 + st / 2) * Box(st, shy, shz)
    walls = [Pos(x_front - shx / 2, sy * (shy / 2 - st / 2), z_top - shz / 2 + st / 2) * Box(shx, st, shz)
             for sy in (-1, 1)]
    shield = roof + back + walls[0] + walls[1]
    parts[18] = shield - Pos(xc, 90, z_top) * Cylinder(ad + 3, 3 * st)   # hole for the antenna
    # 20 keyed saddles between the post and the sign back at the two sign clamps (serrated grip face)
    sw, sh = p["saddle"]
    sx0, sx1 = r, D["sign_xc"] - p["sign_t"] / 2
    sad = None
    for zz in D["sign_clamp_z"]:
        b_ = Pos((sx0 + sx1) / 2, 0, zz) * Box(sx1 - sx0, sw, sh)
        sad = b_ if sad is None else sad + b_
    parts[20] = sad
    # 13 clamps: bar, sign (two), enclosure (two), button
    zs = [D["bar_zc"], *D["sign_clamp_z"], p["enc_z"] - 100, p["enc_z"] + 100, p["button_z"],
          p["radar_z"]]
    cl = None
    for zz in zs:
        cl = band(zz) if cl is None else cl + band(zz)
    parts[13] = cl
    if own_post:
        # 19 anti-rotation bolt through the upper sign saddle and the post (new posts only)
        zb = D["sign_clamp_z"][1]
        parts[19] = rod((-r - 15, 0, zb), (D["sign_xc"] - p["sign_t"] / 2 - 2, 0, zb), p["bolt_d"] / 2)
        parts[14] = Pos(0, 0, (p["post_h"] - p["embed"]) / 2) * (
            Cylinder(r, p["post_h"] + p["embed"]) - Cylinder(r - p["post_wall"], p["post_h"] + p["embed"] + 2))
        parts["footing"] = Pos(0, 0, -p["embed"] / 2 - 50) * (Cylinder(p["footing_d"] / 2, p["embed"] + 100) - Cylinder(r, p["embed"] + 102))
    return parts


def assembly(own_post=True, p=PARAMS):
    from build123d import Compound
    return Compound(children=list(build_parts(p, own_post).values()))


def clash_check(p=PARAMS):
    """Pairs of BOM parts whose solids overlap by more than 1 cm3 (clamps, post and the through-bolt excluded)."""
    parts = build_parts(p, True)
    keys = [k for k in parts if k not in (13, "footing", 14, 19)]
    hits = []
    for i, a in enumerate(keys):
        for bk in keys[i + 1:]:
            try:
                v = (parts[a] & parts[bk]).volume
            except Exception:
                v = 0.0
            if v > 1000.0:
                hits.append((a, bk, v))
    return hits


if __name__ == "__main__":
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    full = build_parts(PARAMS, True)
    groups = {
        "crosssafe-assembly": list(full.values()),
        "crosssafe-existing-pole": [v for k, v in full.items() if k not in (14, 19, "footing")],
        "sign-and-light-bar": [full[k] for k in (1, 2, 3, 17)],
        "pole-top-enclosure": [full[k] for k in (8, 9, 10, 11, 12, 18)],
    }
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"))
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"overall height above sidewalk {D['overall_h']:.0f} mm; sign {D['sign_bot']:.0f} to {D['sign_top']:.0f}; "
          f"enclosure bottom {D['enc_bot']:.0f}")
    print("clashes:", clash_check() or "none")
