"""CrossSafe parametric model (build123d), TRL 3, constructable design (CRS-DDR-003).

Sun shield, keyed sign saddles and the new-post anti-rotation bolt were added under CRS-DDR-002. Under
CRS-DDR-003 (design for construction, 2026-09-30) every part now has a stated way of being made and a
fixing to the part next to it: eight identical keyed pole saddles with stainless bands carry everything
on the pole, the light bar is a folded housing with a removable cover, the enclosure hangs by its lugs
on a mounting plate with a bolted sun shield, and the panel sits on two rails on a welded post-top
bracket with a tilt slot.

Run from the repo root:
    python cad/src/model.py            export STEP and STL into cad/step and cad/stl
    python cad/src/model.py --check    run the constructability checks only

Exports:
    crosssafe-assembly.step / .stl       one beacon assembly on its own 114.3 mm post, with footing
    crosssafe-existing-pole.step / .stl  the same assembly without post, footing and anti-rotation bolt (existing-pole kit, the
                                         prototype that budget_usd covers, CRS-DDR-001 D1)
    sign-and-light-bar.step / .stl       sign, light bar, LED heads and pilot light
    pole-top-enclosure.step / .stl       mounting plate, enclosure with battery, charger, controller, antenna and sun shield

Axes (local frame): the post axis is the Z axis, Z is up with the sidewalk top at z = 0. Traffic runs
along X and the sign faces approaching traffic on +X. The kerb and the waiting zone are on +Y; the solar
panel faces the equator on -Y. For right-hand traffic the assembly mirrors. cad/src/concept_media.py
places this frame in the street scene.

Main dimensions, interfaces and fixings. Holes are modelled at the size of the fastener that goes in
them (a tapped M8 hole is drawn 8 mm). Not for fabrication. The same PARAMS feed docs/04-calcs/sizing.py
(CRS-CAL-001), drawing CRS-DWG-001 (cad/src/sheets.py) and the build plan pictures
(cad/src/build_plan_media.py).
"""
import math
import sys
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 14 post: 114.3 x 3.6 mm galvanized steel (CRS-DDR-001 D3), height above the sidewalk, embedment
    "post_od": 114.3, "post_wall": 3.6, "post_h": 3700.0, "embed": 1800.0, "footing_d": 500.0,
    # existing poles the saddles and bands must fit (R10)
    "pole_min_od": 60.0, "pole_max_od": 114.3,
    # 1 crossing warning sign: square side (diamond), thickness; bolted flat on its two saddles (CRS-DDR-003)
    "sign_side": 750.0, "sign_t": 3.0, "sign_gap": 0.0,
    # 2 light bar housing (X depth, Y length, Z height), bottom height, gap to the sign point, sheet thickness
    "bar": (70.0, 720.0, 130.0), "bar_bottom": 2100.0, "bar_sign_gap": 20.0, "bar_t": 2.0,
    # 3 LED heads: lens (Y width, Z height), head centers from bar center along Y, two per face;
    #   flange depth, body (Y, Z, X depth) behind the flange, wall cut-out (Y, Z)
    "head": (140.0, 62.0), "head_dy": 200.0, "head_flange": 8.0, "head_body": (120.0, 44.0, 25.0),
    "head_cut": (128.0, 50.0),
    # 17 pedestrian pilot light on the kerb end of the light bar
    "pilot_d": 30.0,
    # 4 push-button station: body center height, body (X, Y, Z), instruction plate (X width, Z height)
    "button_z": 1050.0, "button": (70.0, 60.0, 160.0), "plate": (230.0, 300.0), "plate_t": 4.0,
    # 5 presence radar and 16 PIR sensor at the end of the radar arm (22), toward the kerb (+Y)
    "radar_z": 2600.0, "arm_l": 200.0, "radar": 80.0, "pir_d": 40.0, "arm_bar": (40.0, 5.0),
    # 6 solar panel (X, Y, thickness), tilt toward the equator (-Y), rise of its center above the post top
    "panel": (500.0, 360.0, 25.0), "panel_tilt": 30.0, "panel_rise": 230.0,
    # 7 panel bracket: socket tube (OD, wall, length), cap plate (side, thickness), cheeks (thickness,
    #   inner face from the centre line), rails (angle leg, thickness, inner face from the centre line),
    #   pivot and slot bolt positions on the rail (along the panel slope), slot radius and swing
    "socket": (139.7, 4.0, 120.0), "cap": (140.0, 6.0), "cheek": (6.0, 55.0), "rail": (40.0, 4.0, 61.0),
    "pivot_yp": 0.0, "slot_yp": -60.0, "slot_swing": 10.0,
    # 8 enclosure (X depth, Y width, Z height), wall, center height, lid thickness
    "enc": (150.0, 260.0, 300.0), "enc_wall": 4.0, "enc_z": 3000.0, "lid_t": 4.0,
    # 21 enclosure mounting plate (Y width, Z height, thickness) with a saddle tab above and below
    "enc_plate": (350.0, 300.0, 4.0), "tab": (90.0, 90.0),
    # 9 to 12 parts inside and on the enclosure; module stand-off height; internal plate (Y, Z, t) and boss height
    "battery": (95.0, 151.0, 98.0), "mppt": (40.0, 90.0, 60.0), "board": (14.0, 180.0, 100.0),
    "fuse_block": (30.0, 60.0, 30.0), "standoff": 6.0, "mplate": (220.0, 270.0, 2.0), "boss_h": 10.0,
    "antenna": (8.0, 220.0),
    # 13 band clamps: stainless strapping thickness and width (19 mm x 0.76 mm, CRS-DDR-003)
    "band_t": 0.76, "band_w": 19.0,
    # 18 ventilated sun shield over the enclosure (CRS-DDR-002): air gap to the enclosure, sheet thickness, flange width
    "shield_gap": 25.0, "shield_t": 2.0, "shield_flange": 15.0,
    # 20 keyed pole saddles, eight identical (CRS-DDR-003): Y width, Z height, X depth; V included angle,
    #   V half width at the back face, band groove depth, bolt hole offset from the saddle centre
    "saddle": (80.0, 60.0), "saddle_d": 40.0, "saddle_v": 120.0, "saddle_vhw": 35.0, "groove": 1.0, "bolt_dz": 20.0,
    # 19 anti-rotation bolt, new posts only: diameter
    "bolt_d": 10.0,
}

BOM = {1: "Crossing warning sign", 2: "Light bar housing", 3: "Amber LED heads", 4: "Push-button station",
       5: "Presence radar", 6: "Solar panel", 7: "Panel bracket", 8: "Enclosure", 9: "LiFePO4 battery",
       10: "MPPT charge controller", 11: "Controller and radio board", 12: "Antenna", 13: "Band clamps",
       14: "Post", 15: "Wiring and protection", 16: "PIR wake sensor", 17: "Pedestrian pilot light", 18: "Sun shield",
       19: "Anti-rotation bolt", 20: "Keyed pole saddles", 21: "Enclosure mounting plate", 22: "Radar arm",
       23: "Battery strap"}


def saddle_geom(r, p=PARAMS):
    """Where a saddle sits on a pole of radius r, measured out from the pole axis along the saddle's
    centre line: back face xb, V point xv, front face xf; and where the pole touches the V faces."""
    half = math.radians(p["saddle_v"] / 2)
    xv = r / math.sin(half)                     # V point: the pole touches both faces
    xb = xv - p["saddle_vhw"] / math.tan(half)  # back face, where the V is saddle_vhw each side of centre
    xf = xb + p["saddle_d"]
    s_touch = r / math.tan(half)                # contact distance from the V point along each face
    contact = (xv - s_touch * math.cos(half), s_touch * math.sin(half))
    return {"xb": xb, "xv": xv, "xf": xf, "contact": contact, "contact_in": p["saddle_vhw"] - contact[1]}


# the enclosure's distance behind the post follows from the saddle; kept as a parameter for the appearance model
PARAMS["enc_gap"] = round(saddle_geom(PARAMS["post_od"] / 2)["xf"] + PARAMS["enc_plate"][2] + PARAMS["enc"][0] / 2, 2)


def derived(p=PARAMS):
    """Heights, envelopes and wind areas the calc note and drawing quote, computed from PARAMS."""
    r = p["post_od"] / 2
    sg = saddle_geom(r, p)
    xf = sg["xf"]
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
    shx, shy, shz = ex + g + st, ey + 2 * (g + st), ez + g + st   # shield envelope (open toward the post and at the bottom)
    pw, ph, pth = p["enc_plate"]
    plate_zc = p["button_z"] + p["button"][2] / 2 + 20 + p["plate"][1] / 2
    tab_h = p["tab"][1]
    arm_top = p["radar_z"] - p["radar"] / 2            # radar sits on the arm
    pir_bot = arm_top - p["arm_bar"][1] - p["pir_d"]
    enc_bot, enc_top = p["enc_z"] - ez / 2, p["enc_z"] + ez / 2
    # saddle stations: name -> (direction the saddle faces, degrees about Z from +X; height of its centre)
    stations = {
        "button": (90.0, p["button_z"]),
        "plate": (90.0, plate_zc),
        "bar": (0.0, bar_zc),
        "sign_low": (0.0, sign_zc - 250.0),
        "radar": (90.0, arm_top - p["arm_bar"][1] + p["saddle"][1] / 2 + 10.0),
        "enc_low": (180.0, enc_bot - tab_h / 2 - 15.0),
        "sign_up": (0.0, sign_zc + 250.0),
        "enc_up": (180.0, enc_top + tab_h / 2 + 15.0),
    }
    return {
        "post_r": r, "saddle": sg, "saddle_front": xf,
        "bar_xc": xf + bx / 2,
        "bar_zc": bar_zc, "bar_top": p["bar_bottom"] + bz,
        "sign_xc": xf + p["sign_gap"] + p["sign_t"] / 2,
        "sign_zc": sign_zc, "sign_bot": sign_zc - half_diag, "sign_top": sign_zc + half_diag,
        "sign_area_m2": p["sign_side"] ** 2 / 1e6,
        "enc_xc": -(xf + pth + ex / 2), "enc_back": -(xf + pth), "enc_bot": enc_bot, "enc_top": enc_top,
        "shield": (shx, shy, shz), "sign_clamp_z": (sign_zc - 250.0, sign_zc + 250.0),
        "plate_zc": plate_zc, "arm_top": arm_top, "pir_bot": pir_bot, "stations": stations,
        "panel_zc": panel_zc, "overall_h": panel_top,
        "panel_area_m2": px * py / 1e6,
        # wind areas (m2) normal to X (traffic direction) and to Y (across the road); along the road the
        # enclosure group is the shield, the strips of mounting plate beside it and the two saddle tabs
        "area_x": {"sign": p["sign_side"] ** 2 / 1e6, "bar": by * bz / 1e6,
                   "enc": (shy * shz + max(pw - shy, 0) * ph + 2 * p["tab"][0] * p["tab"][1] - p["tab"][0] * (g + st)) / 1e6,
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


# ----------------------------------------------------------------- geometry helpers
def _b():
    import build123d as b
    return b


def box(x0, x1, y0, y1, z0, z1):
    b = _b()
    return b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * b.Box(x1 - x0, y1 - y0, z1 - z0)


def rod(a, c, rad):
    b = _b()
    a = b.Vector(*a); c = b.Vector(*c); d = c - a
    return b.Solid.make_cylinder(rad, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def hexagon(a, c, af):
    """Hex prism (a bolt head or nut) from point a to point c, across flats af."""
    b = _b()
    a = b.Vector(*a); c = b.Vector(*c); d = c - a
    pl = b.Plane(origin=a, z_dir=d.normalized())
    rr = af / math.sqrt(3)
    pts = [pl.from_local_coords((rr * math.cos(math.radians(30 + 60 * i)), rr * math.sin(math.radians(30 + 60 * i)))) for i in range(6)]
    return b.extrude(b.Face(b.Wire.make_polygon(pts, close=True)), d.length, dir=d.normalized())


def bolt(head_at, direction, length, d=8.0, af=13.0, head_h=5.3):
    """Hex-head bolt: the underside of the head at head_at, shank running length along direction."""
    b = _b()
    u = b.Vector(*direction).normalized()
    h = b.Vector(*head_at)
    return hexagon(h - u * head_h, h, af) + rod(h, h + u * length, d / 2)


def nut(face_at, direction, d=8.0, af=13.0, h=6.5):
    b = _b()
    u = b.Vector(*direction).normalized()
    a = b.Vector(*face_at)
    return hexagon(a, a + u * h, af)


def prism(poly, plane, depth):
    """Extrude a shapely polygon (holes allowed) drawn in a build123d plane's local (x, y) by depth along its normal."""
    b = _b()

    def solid(coords):
        pts = [plane.from_local_coords((x, y)) for x, y in list(coords)[:-1]]
        return b.extrude(b.Face(b.Wire.make_polygon(pts, close=True)), depth, dir=plane.z_dir)
    s = solid(poly.exterior.coords)
    for hole in poly.interiors:
        s = s - solid(hole.coords)
    return s


def _fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def group(shapes):
    b = _b()
    return b.Compound(children=[s for s in shapes if s is not None])


# ----------------------------------------------------------------- saddles and bands
def saddle_local(r, p=PARAMS, through_hole=False):
    """One keyed pole saddle facing +X on a pole of radius r, centred at z = 0, and its band and buckle.
    The band runs round the back of the pole, straight from the pole to the saddle's front corners and across its front in a
    shallow groove, so tightening it pulls the saddle's V onto the pole. Whatever is fixed to the saddle
    bolts into its two tapped holes, above and below the band, and covers the band."""
    from shapely.geometry import Point, Polygon
    b = _b()
    sg = saddle_geom(r, p)
    xb, xv, xf = sg["xb"], sg["xv"], sg["xf"]
    sw, sh = p["saddle"]
    half = math.radians(p["saddle_v"] / 2)
    blk = box(xb, xf, -sw / 2, sw / 2, -sh / 2, sh / 2)
    reach = (xv - (xb - 5)) * math.tan(half)
    vcut = prism(Polygon([(xv, 0), (xb - 5, reach), (xb - 5, -reach)]), b.Plane.XY.offset(-sh / 2 - 1), sh + 2)
    g, bw = p["groove"], p["band_w"]
    groove = box(xf - g, xf + 1, -sw / 2 - 1, sw / 2 + 1, -(bw / 2 + 1), bw / 2 + 1)
    holes = []
    for dz in (-p["bolt_dz"], p["bolt_dz"]):
        if through_hole and dz > 0:
            holes.append(rod((xb - 1, 0, dz), (xf + 1, 0, dz), (p["bolt_d"] + 0.5) / 2))
        else:
            holes.append(rod((xf - 14, 0, dz), (xf + 1, 0, dz), 4.0))     # M8, tapped 14 deep (drawn at 8 mm)
    saddle = blk - vcut - groove - _fuse(holes)
    # band: the hull of the pole and the saddle's outline at the groove floor, thickened outward by the strap thickness
    t = p["band_t"]
    circ = Point(0, 0).buffer(r + 0.05, 24)
    inner = Polygon(list(circ.exterior.coords) + [(xb, sw / 2), (xf - g, sw / 2), (xf - g, -sw / 2), (xb, -sw / 2)]).convex_hull
    ring = inner.buffer(t, 2).difference(inner)
    band = prism(ring, b.Plane.XY.offset(-bw / 2), bw)
    # the buckle sits on the back of the pole, turned 40 degrees off the centre line, clear of a through-bolt
    buckle = b.Rot(0, 0, 140) * box(r + t, r + t + 5, -11, 11, -12.5, 12.5)
    return {"saddle": saddle, "band": band, "buckle": buckle, "geom": sg}


def station(name, p=PARAMS, through_hole=False):
    b = _b()
    D = derived(p)
    ang, z = D["stations"][name]
    loc = saddle_local(D["post_r"], p, through_hole)
    T = b.Pos(0, 0, z) * b.Rot(0, 0, ang)
    return {k: T * v for k, v in loc.items() if k != "geom"}


# ----------------------------------------------------------------- the components
def build_components(p=PARAMS, own_post=False):
    """Every component of one assembly as {name: (shape, bom line)}, in model coordinates. own_post adds
    the new-post variant (post with embedment and holes, footing, anti-rotation bolt); without it the
    assembly is the existing-pole kit and the pole is context (pole_context)."""
    from shapely.geometry import Polygon, Point, LineString
    b = _b()
    D = derived(p)
    r = D["post_r"]
    xf = D["saddle_front"]
    C = {}

    # 20 saddles and 13 bands
    for n in D["stations"]:
        s = station(n, p, through_hole=(own_post and n == "sign_up"))
        C[f"saddle_{n}"] = (s["saddle"], 20)
        C[f"band_{n}"] = (s["band"] + s["buckle"], 13)

    # 1 sign: a square turned 45 degrees in the Y-Z plane, flat on the two sign saddles, two M8 bolts each
    st = p["sign_t"]
    sign = b.Pos(D["sign_xc"], 0, D["sign_zc"]) * b.Rot(45, 0, 0) * b.Box(st, p["sign_side"], p["sign_side"])
    sb = []
    for zc in D["sign_clamp_z"]:
        for dz in (-p["bolt_dz"], p["bolt_dz"]):
            through = own_post and zc == D["sign_clamp_z"][1] and dz > 0
            dia = p["bolt_d"] + 0.5 if through else 9.0
            sign = sign - rod((xf - 1, 0, zc + dz), (xf + st + 1, 0, zc + dz), dia / 2)
            if not through:
                sb.append(bolt((xf + st, 0, zc + dz), (-1, 0, 0), 16))
    C["sign"] = (sign, 1)
    C["sign_bolts"] = (group(sb), 15)

    # 2 light bar: folded channel (back, top, front) with inward lips, bottom cover, two end caps
    bx, by, bz = p["bar"]
    t = p["bar_t"]
    z0, z1 = p["bar_bottom"], p["bar_bottom"] + bz
    zc = D["bar_zc"]
    x0, x1 = xf, xf + bx
    yl = by / 2 - t                       # channel ends; the end caps close them
    ch = (box(x0, x0 + t, -yl, yl, z0 + t, z1) + box(x1 - t, x1, -yl, yl, z0 + t, z1) + box(x0, x1, -yl, yl, z1 - t, z1)
          + box(x0 + t, x0 + t + 10, -yl, yl, z0 + t, z0 + 2 * t) + box(x1 - t - 10, x1 - t, -yl, yl, z0 + t, z0 + 2 * t))
    hw, hh = p["head_cut"]
    for y in (-p["head_dy"], p["head_dy"]):
        ch = ch - box(x0 - 1, x0 + t + 1, y - hw / 2, y + hw / 2, zc - hh / 2, zc + hh / 2)
        ch = ch - box(x1 - t - 1, x1 + 1, y - hw / 2, y + hw / 2, zc - hh / 2, zc + hh / 2)
    for dz in (-p["bolt_dz"], p["bolt_dz"]):
        ch = ch - rod((x0 - 1, 0, zc + dz), (x0 + t + 1, 0, zc + dz), 4.5)
    gland_y = -60.0
    cover = box(x0, x1, -yl, yl, z0, z0 + t) - rod(((x0 + x1) / 2, gland_y, z0 - 1), ((x0 + x1) / 2, gland_y, z0 + t + 1), 8.0)
    caps = []
    for sgn in (-1, 1):
        ye = sgn * (by / 2 - t / 2)
        cap = b.Pos((x0 + x1) / 2, ye, (z0 + z1) / 2) * b.Box(bx, t, bz)
        yi = sgn * (by / 2 - t)          # flanges inside the channel walls, 15 long
        ya, yb2 = sorted((yi, yi - sgn * 15))
        cap = cap + box(x0 + t, x0 + 2 * t, ya, yb2, z0 + 2 * t, z1 - t) + box(x1 - 2 * t, x1 - t, ya, yb2, z0 + 2 * t, z1 - t) \
            + box(x0 + 2 * t, x1 - 2 * t, ya, yb2, z1 - 2 * t, z1 - t)
        if sgn > 0:
            cap = cap - rod(((x0 + x1) / 2, by / 2 - t - 1, zc), ((x0 + x1) / 2, by / 2 + 1, zc), 11.0)
        caps.append(cap)
    C["bar_channel"] = (ch, 2)
    C["bar_cover"] = (cover, 2)
    C["bar_caps"] = (group(caps), 2)
    bb_ = []
    for dz in (-p["bolt_dz"], p["bolt_dz"]):
        bb_.append(bolt((x0 + t, 0, zc + dz), (-1, 0, 0), 16))
    C["bar_bolts"] = (group(bb_), 15)
    gx = (x0 + x1) / 2
    C["bar_gland"] = (rod((gx, gland_y, z0 - 16), (gx, gland_y, z0), 12) + rod((gx, gland_y, z0), (gx, gland_y, z0 + t), 8.0)
                      + rod((gx, gland_y, z0 + t), (gx, gland_y, z0 + t + 6), 12), 15)

    # 3 LED heads: flange outside the wall, body inside through the cut-out
    hfw, hfh = p["head"]
    fl = p["head_flange"]
    bw_, bh_, bd_ = p["head_body"]
    heads = []
    for y in (-p["head_dy"], p["head_dy"]):
        heads.append(box(x1, x1 + fl, y - hfw / 2, y + hfw / 2, zc - hfh / 2, zc + hfh / 2)
                     + box(x1 - t - bd_, x1, y - bw_ / 2, y + bw_ / 2, zc - bh_ / 2, zc + bh_ / 2))
        heads.append(box(x0 - fl, x0, y - hfw / 2, y + hfw / 2, zc - hfh / 2, zc + hfh / 2)
                     + box(x0, x0 + t + bd_, y - bw_ / 2, y + bw_ / 2, zc - bh_ / 2, zc + bh_ / 2))
    C["heads"] = (group(heads), 3)
    # 17 pilot light: lens outside the kerb end cap, threaded body through it
    C["pilot"] = (rod(((x0 + x1) / 2, by / 2, zc), ((x0 + x1) / 2, by / 2 + 20, zc), p["pilot_d"] / 2)
                  + rod(((x0 + x1) / 2, by / 2 - t - 15, zc), ((x0 + x1) / 2, by / 2, zc), 10.0), 17)

    # 4 push-button station (bought, on the button saddle) and its instruction plate (on its own saddle)
    ux, uy, uz = p["button"]
    wx, wz = p["plate"]
    pt_ = p["plate_t"]
    C["button"] = (box(-ux / 2, ux / 2, xf, xf + uy, p["button_z"] - uz / 2, p["button_z"] + uz / 2), 4)
    pz = D["plate_zc"]
    plate = box(-wx / 2, wx / 2, xf, xf + pt_, pz - wz / 2, pz + wz / 2)
    pb = []
    for dz in (-p["bolt_dz"], p["bolt_dz"]):
        plate = plate - rod((0, xf - 1, pz + dz), (0, xf + pt_ + 1, pz + dz), 4.5)
        pb.append(bolt((0, xf + pt_, pz + dz), (0, -1, 0), 16))
    C["inst_plate"] = (plate, 4)
    C["plate_bolts"] = (group(pb), 15)

    # 22 radar arm: 40 x 5 flat bar bent to an L; the short leg stands on the radar saddle, the long leg
    # carries the radar on top and the PIR underneath at its far end
    aw, at = p["arm_bar"]
    s = p["radar"]
    ry = r + p["arm_l"] + s / 2
    atop = D["arm_top"]
    zs = D["stations"]["radar"][1]
    sh = p["saddle"][1]
    long_leg = box(-aw / 2, aw / 2, xf, ry + s / 2, atop - at, atop)
    short_leg = box(-aw / 2, aw / 2, xf, xf + at, atop - at, zs + sh / 2)
    arm = long_leg + short_leg
    ab = []
    for dz in (-p["bolt_dz"], p["bolt_dz"]):
        arm = arm - rod((0, xf - 1, zs + dz), (0, xf + at + 1, zs + dz), 4.5)
        ab.append(bolt((0, xf + at, zs + dz), (0, -1, 0), 16))
    arm = arm - rod((0, ry, atop - at - 1), (0, ry, atop + 1), 6.0)              # PIR neck
    for dy in (-25.0, 25.0):
        arm = arm - rod((0, ry + dy, atop - at - 1), (0, ry + dy, atop + 1), 2.25)  # radar screws (M4)
    C["radar_arm"] = (arm, 22)
    C["arm_bolts"] = (group(ab), 15)
    C["radar"] = (box(-s / 2, s / 2, ry - s / 2, ry + s / 2, atop, atop + s), 5)
    C["pir"] = (rod((0, ry, D["pir_bot"]), (0, ry, atop - at), p["pir_d"] / 2) + rod((0, ry, atop - at), (0, ry, atop), 6.0), 16)

    # 21 enclosure mounting plate: flat on the two enclosure saddles by its tabs, enclosure on its front
    pw, ph, pth = p["enc_plate"]
    tw, th_ = p["tab"]
    eb = D["enc_back"]                    # plate front face (the enclosure's back face) x
    ebot, etop = D["enc_bot"], D["enc_top"]
    ezc = p["enc_z"]
    mp = (box(-xf - pth, -xf, -pw / 2, pw / 2, ezc - ph / 2, ezc + ph / 2)
          + box(-xf - pth, -xf, -tw / 2, tw / 2, ezc - ph / 2 - th_, ezc + ph / 2 + th_))
    ex, ey, ez = p["enc"]
    lug_y = ey / 2 + 12.0
    lug_z = (ebot + 10.0, etop - 10.0)
    sh_y = ey / 2 + p["shield_gap"] + p["shield_t"] + p["shield_flange"] / 2
    sh_z = (ezc - 100.0, ezc + 100.0)
    mb = []
    for k in ("enc_low", "enc_up"):
        zz = D["stations"][k][1]
        for dz in (-p["bolt_dz"], p["bolt_dz"]):
            mp = mp - rod((-xf + 1, 0, zz + dz), (-xf - pth - 1, 0, zz + dz), 4.5)
            mb.append(bolt((-xf - pth, 0, zz + dz), (1, 0, 0), 16))
    for sy in (-1, 1):
        for zz in lug_z:
            mp = mp - rod((-xf + 1, sy * lug_y, zz), (-xf - pth - 1, sy * lug_y, zz), 2.5)
        for zz in sh_z:
            mp = mp - rod((-xf + 1, sy * sh_y, zz), (-xf - pth - 1, sy * sh_y, zz), 2.5)
    C["enc_plate"] = (mp, 21)
    C["enc_plate_bolts"] = (group(mb), 15)

    # 8 enclosure: body (open on the far face), lid, four bosses inside the back wall, four lugs
    w = p["enc_wall"]
    lt = p["lid_t"]
    xb0, xb1 = eb - ex, eb               # x from the lid face to the back face
    body = box(xb0 + lt, xb1, -ey / 2, ey / 2, ebot, etop) - box(xb0 + lt - 1, xb1 - w, -ey / 2 + w, ey / 2 - w, ebot + w, etop - w)
    bh = p["boss_h"]
    for by_ in (-100.0, 100.0):
        for bz_ in (ezc - 125.0, ezc + 125.0):
            body = body + rod((xb1 - w, by_, bz_), (xb1 - w - bh, by_, bz_), 5.0)
    # bottom-face penetrations: four M20 glands and a vent; antenna bulkhead on the roof
    floor = ebot
    pens = {"gland_1": (40.0, 105.0), "gland_2": (100.0, 105.0), "gland_3": (40.0, -105.0), "gland_4": (100.0, -105.0),
            "vent": (130.0, 0.0)}
    gl, vt = [], None
    for k, (dx, yy) in pens.items():
        xx = eb - dx
        dia = 20.0 if k != "vent" else 12.0
        body = body - rod((xx, yy, floor - 1), (xx, yy, floor + w + 1), dia / 2)
        if k == "vent":
            vt = rod((xx, yy, floor - 8), (xx, yy, floor), 10) + rod((xx, yy, floor), (xx, yy, floor + w), 6) + rod((xx, yy, floor + w), (xx, yy, floor + w + 5), 10)
        else:
            gl.append(rod((xx, yy, floor - 22), (xx, yy, floor), 14) + rod((xx, yy, floor), (xx, yy, floor + w), 10)
                      + rod((xx, yy, floor + w), (xx, yy, floor + w + 7), 14))
    exc = D["enc_xc"]
    body = body - rod((exc, 90, etop - w - 1), (exc, 90, etop + 1), 8.0)
    ad, al = p["antenna"]
    ant = (rod((exc, 90, etop), (exc, 90, etop + 6), 10) + rod((exc, 90, etop - w), (exc, 90, etop), 8)
           + rod((exc, 90, etop + 6), (exc, 90, etop + al), ad) + rod((exc, 90, etop - w - 5), (exc, 90, etop - w), 10))
    C["enc_body"] = (body, 8)
    C["lid"] = (box(xb0, xb0 + lt, -ey / 2, ey / 2, ebot, etop), 8)
    C["glands"] = (group(gl), 15)
    C["vent"] = (vt, 8)
    C["antenna"] = (ant, 12)
    lugs, lsc = [], []
    for sy in (-1, 1):
        for zz in lug_z:
            y0_, y1_ = sorted((sy * ey / 2, sy * (ey / 2 + 22)))
            lug = box(eb - 4, eb, y0_, y1_, zz - 10, zz + 10) - rod((eb + 1, sy * lug_y, zz), (eb - 5, sy * lug_y, zz), 2.5)
            lugs.append(lug)
            lsc.append(bolt((eb - 4, sy * lug_y, zz), (1, 0, 0), 12, d=5.0, af=8.0, head_h=3.0)
                       + nut((-xf, sy * lug_y, zz), (1, 0, 0), d=5.0, af=8.0, h=4.0))
    C["lugs"] = (group(lugs), 8)
    C["lug_screws"] = (group(lsc), 15)

    # internal plate on the bosses, modules on stand-offs, battery on the floor under its strap
    mw, mh, mt = p["mplate"]
    xp_back = xb1 - w - bh               # the internal plate's back face x
    xp_front = xp_back - mt
    C["mplate"] = (box(xp_front, xp_back, -mw / 2, mw / 2, ezc - mh / 2, ezc + mh / 2), 8)
    so = p["standoff"]

    def module(dims, yc, zlo):
        dx, dy, dz = dims
        m = box(xp_front - so - dx, xp_front - so, yc - dy / 2, yc + dy / 2, zlo, zlo + dz)
        for sy_ in (-1, 1):
            for sz_ in (0, 1):
                yy, zz = yc + sy_ * (dy / 2 - 5), zlo + 5 + sz_ * (dz - 10)
                m = m + rod((xp_front, yy, zz), (xp_front - so, yy, zz), 3.0)
        return m
    fin = ebot + w                        # inner floor
    C["mppt"] = (module(p["mppt"], -70.0, fin + 110), 10)
    C["board"] = (module(p["board"], 0.0, fin + 180), 11)
    C["fuse_block"] = (module(p["fuse_block"], 60.0, fin + 110), 15)
    bxd, byd, bzd = p["battery"]
    C["battery"] = (box(xp_front - bxd, xp_front, -byd / 2, byd / 2, fin, fin + bzd), 9)
    stw, stt = 25.0, 2.0
    strap = (box(xp_front - stt, xp_front, -stw / 2, stw / 2, fin + bzd, fin + bzd + 40)
             + box(xp_front - bxd - stt, xp_front, -stw / 2, stw / 2, fin + bzd, fin + bzd + stt)
             + box(xp_front - bxd - stt, xp_front - bxd, -stw / 2, stw / 2, fin + bzd - 40, fin + bzd + stt))
    for zz in (fin + bzd + 15, fin + bzd + 30):
        strap = strap - rod((xp_front + 1, 0, zz), (xp_front - stt - 1, 0, zz), 2.0)
    C["strap"] = (strap, 23)

    # 18 sun shield: back, two sides and roof with an air gap; side flanges bolted to the mounting plate;
    # the roof gap is open toward the post above the plate, the bottom is open
    g, sth, sfl = p["shield_gap"], p["shield_t"], p["shield_flange"]
    sx_back = xb0 - g                    # inner face of the shield back
    sy_in = ey / 2 + g
    z_roof = etop + g
    roof = box(sx_back - sth, eb, -sy_in - sth, sy_in + sth, z_roof, z_roof + sth)
    back = box(sx_back - sth, sx_back, -sy_in - sth, sy_in + sth, ebot, z_roof + sth)
    sides = [box(sx_back - sth, eb, sy * sy_in + (0 if sy > 0 else -sth), sy * sy_in + (sth if sy > 0 else 0), ebot, z_roof + sth)
             for sy in (-1, 1)]
    flanges = [box(eb - sth, eb, *sorted((sy * sy_in, sy * (sy_in + sth + sfl))), ebot, etop) for sy in (-1, 1)]
    shield = roof + back + sides[0] + sides[1] + flanges[0] + flanges[1]
    shield = shield - rod((exc, 90, z_roof - 1), (exc, 90, z_roof + sth + 1), (2 * ad + 6) / 2)
    ss = []
    for sy in (-1, 1):
        for zz in sh_z:
            shield = shield - rod((eb + 1, sy * sh_y, zz), (eb - sth - 1, sy * sh_y, zz), 2.5)
            ss.append(bolt((eb - sth, sy * sh_y, zz), (1, 0, 0), 6, d=5.0, af=8.0, head_h=3.0))
    C["shield"] = (shield, 18)
    C["shield_screws"] = (group(ss), 15)

    # 7 panel bracket: socket over the post top, cap plate, two cheeks (welded), three set screws;
    # 6 panel on two rails bolted to the cheeks by a pivot bolt and a tilt-slot bolt each
    so_d, so_t, so_l = p["socket"]
    cap_w, cap_t = p["cap"]
    ph_ = p["post_h"]
    sock = (rod((0, 0, ph_ - so_l), (0, 0, ph_), so_d / 2) - rod((0, 0, ph_ - so_l - 1), (0, 0, ph_ + 1), so_d / 2 - so_t))
    capp = box(-cap_w / 2, cap_w / 2, -cap_w / 2, cap_w / 2, ph_, ph_ + cap_t)
    zset = ph_ - so_l / 2
    nuts, sets = [], []
    for k in range(3):
        a = math.radians(90 + 120 * k)
        u = (math.cos(a), math.sin(a), 0)
        ro = so_d / 2
        sock = sock - rod((u[0] * (ro - so_t - 1), u[1] * (ro - so_t - 1), zset), (u[0] * (ro + 1), u[1] * (ro + 1), zset), 5.0)
        nuts.append(hexagon((u[0] * (ro - 0.6), u[1] * (ro - 0.6), zset), (u[0] * (ro + 8), u[1] * (ro + 8), zset), 17)
                    - rod((u[0] * (ro - 2), u[1] * (ro - 2), zset), (u[0] * (ro + 9), u[1] * (ro + 9), zset), 5.0))
        sets.append(rod((u[0] * r, u[1] * r, zset), (u[0] * (ro + 12), u[1] * (ro + 12), zset), 5.0))
    # weld the nuts on: trim each nut where it meets the round tube
    nuts = [n - rod((0, 0, zset - 20), (0, 0, zset + 20), so_d / 2 - 0.01) for n in nuts]
    tilt = math.radians(p["panel_tilt"])
    Zc = D["panel_zc"]

    def g2(yp, zp):
        return (yp * math.cos(tilt) - zp * math.sin(tilt), Zc + yp * math.sin(tilt) + zp * math.cos(tilt))
    pt = p["panel"][2]
    rl, rt, rx = p["rail"]
    zb_ = -pt / 2                         # panel back face in panel coordinates
    ct, cx = p["cheek"]
    piv = g2(p["pivot_yp"], zb_ - rt - (rl - rt) / 2)
    slo = g2(p["slot_yp"], zb_ - rt - (rl - rt) / 2)
    rad = math.hypot(slo[0] - piv[0], slo[1] - piv[1])
    a0 = math.atan2(slo[1] - piv[1], slo[0] - piv[0])
    sw_ = math.radians(p["slot_swing"])
    arc = LineString([(piv[0] + rad * math.cos(a0 + sw_ * (i / 20 - 0.5) * 2), piv[1] + rad * math.sin(a0 + sw_ * (i / 20 - 0.5) * 2))
                      for i in range(21)])
    y_lo, y_hi = min(piv[0], slo[0]) - 22, max(piv[0], slo[0]) + 22
    ztop = lambda Y: g2((Y + (zb_ - rt) * math.sin(tilt)) / math.cos(tilt), zb_ - rt)[1]   # cheek top: just under the rail's flat leg level
    cheek_poly = Polygon([(y_lo, ph_ + cap_t), (y_hi, ph_ + cap_t), (y_hi, ztop(y_hi)), (y_lo, ztop(y_lo))])
    cheek_poly = cheek_poly.difference(Point(*piv).buffer(5.25, 32)).difference(arc.buffer(5.25, 16))
    cheeks = []
    for sx in (-1, 1):
        x_in = sx * cx
        pl = b.Plane(origin=(x_in if sx > 0 else -cx - ct, 0, 0), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
        cheeks.append(prism(cheek_poly, pl, ct))
    C["bracket"] = (_fuse([sock, capp] + cheeks + nuts), 7)
    C["set_screws"] = (group(sets), 15)
    rails, rbolts = [], []
    py_ = p["panel"][1]
    F = b.Pos(0, 0, Zc) * b.Rot(p["panel_tilt"], 0, 0)
    for sx in (-1, 1):
        xi = sx * (cx + ct)               # rail's upright leg against the cheek's outer face
        xo = sx * (cx + ct + rl)
        xa, xb_ = sorted((xi, xo))
        xr0, xr1 = sorted((xi, xi + sx * rt))
        flat_leg = box(xa, xb_, -py_ / 2, py_ / 2, zb_ - rt, zb_)
        up_leg = box(xr0, xr1, -py_ / 2, py_ / 2, zb_ - rl, zb_)
        rail = flat_leg + up_leg
        zl = zb_ - rt - (rl - rt) / 2
        for yp in (p["pivot_yp"], p["slot_yp"]):
            rail = rail - rod((xr0 - 1, yp, zl), (xr1 + 1, yp, zl), 5.25)
        xm = (xa + xb_) / 2
        for yp in (-py_ / 2 + 10, py_ / 2 - 10):
            rail = rail - rod((xm, yp, zb_ - rt - 1), (xm, yp, zb_ + 1), 3.25)
            rbolts.append(F * bolt((xm, yp, zb_ - rt), (0, 0, 1), rt, d=6.0, af=10.0, head_h=4.0))
        rails.append(F * rail)
        for yp in (p["pivot_yp"], p["slot_yp"]):
            xh = sx * (cx + ct + rt)
            rbolts.append(F * (bolt((xh, yp, zl), (-sx, 0, 0), rt + ct + 8, d=10.0, af=16.0, head_h=6.4)
                               + nut((sx * cx, yp, zl), (-sx, 0, 0), d=10.0, af=16.0, h=8.0)))
    C["rails"] = (group(rails), 7)
    C["panel_bolts"] = (group(rbolts), 15)
    px, py, ptk = p["panel"]
    C["panel"] = (F * b.Box(px, py, ptk), 6)

    if own_post:
        # 14 post with embedment and the anti-rotation bolt hole; 19 bolt through the sign, upper saddle and post
        zb = D["sign_clamp_z"][1] + p["bolt_dz"]
        post = b.Pos(0, 0, (ph_ - p["embed"]) / 2) * (b.Cylinder(r, ph_ + p["embed"]) - b.Cylinder(r - p["post_wall"], ph_ + p["embed"] + 2))
        post = post - rod((-r - 1, 0, zb), (r + 1, 0, zb), (p["bolt_d"] + 0.5) / 2)
        C["post"] = (post, 14)
        C["arb"] = (bolt((xf + st, 0, zb), (-1, 0, 0), xf + st + r + 14, d=p["bolt_d"], af=16.0, head_h=6.4)
                    + nut((-r, 0, zb), (-1, 0, 0), d=p["bolt_d"], af=16.0, h=8.0), 19)
        C["footing"] = (b.Pos(0, 0, -p["embed"] / 2 - 50) * (b.Cylinder(p["footing_d"] / 2, p["embed"] + 100) - b.Cylinder(r, p["embed"] + 102)), "footing")
    return C


def pole_context(p=PARAMS, z0=0.0, z1=None):
    """The pole the existing-pole kit is built on: a 114.3 x 3.6 mm tube (the prototype's test post)."""
    r = p["post_od"] / 2
    z1 = p["post_h"] if z1 is None else z1
    return rod((0, 0, z0), (0, 0, z1), r) - rod((0, 0, z0 - 1), (0, 0, z1 + 1), r - p["post_wall"])


def build_parts(p=PARAMS, own_post=True):
    """Return {bom_no: shape} for one assembly (each line's components grouped), plus 'footing' when own_post."""
    C = build_components(p, own_post)
    out = {}
    for name, (shape, n) in C.items():
        out.setdefault(n, []).append(shape)
    return {n: (v[0] if len(v) == 1 else group(v)) for n, v in out.items()}


def assembly(own_post=True, p=PARAMS):
    return group(list(build_parts(p, own_post).values()))


# ----------------------------------------------------------------- constructability checks
def _vol(a, c):
    try:
        bb1, bb2 = a.bounding_box(), c.bounding_box()
        if (bb1.min.X > bb2.max.X or bb2.min.X > bb1.max.X or bb1.min.Y > bb2.max.Y or bb2.min.Y > bb1.max.Y
                or bb1.min.Z > bb2.max.Z or bb2.min.Z > bb1.max.Z):
            return 0.0
        return (a & c).volume
    except Exception:
        return 0.0


def checks(p=PARAMS, own_post=False, verbose=True):
    """Constructability checks: no two components overlap; every joint touches; stated clearances hold.
    Returns a list of (ok, text)."""
    C = build_components(p, own_post)
    C = {k: v[0] for k, v in C.items() if v[1] != "footing"}
    if not own_post:
        C["pole"] = pole_context(p)
    D = derived(p)
    res = []

    def dist(a, c):
        return C[a].distance_to(C[c])

    # 1. no overlaps (more than 1 mm3) between any two components
    names = list(C)
    for i, a in enumerate(names):
        for c in names[i + 1:]:
            v = _vol(C[a], C[c])
            if v > 1.0:
                res.append((False, f"overlap {a} / {c}: {v:.1f} mm3"))
    n_pairs = len(names) * (len(names) - 1) // 2
    res.append((all(ok for ok, _ in res), f"no overlaps among {len(names)} components ({n_pairs} pairs)"))
    pole = "post" if own_post else "pole"
    # 2. joints that must touch (gap 0.05 mm or less)
    touch = []
    for n in D["stations"]:
        touch += [(f"saddle_{n}", pole), (f"band_{n}", pole), (f"band_{n}", f"saddle_{n}")]
    touch += [("sign", "saddle_sign_low"), ("sign", "saddle_sign_up"), ("sign_bolts", "sign"),
              ("bar_channel", "saddle_bar"), ("bar_cover", "bar_channel"), ("bar_caps", "bar_channel"),
              ("bar_bolts", "bar_channel"), ("heads", "bar_channel"), ("pilot", "bar_caps"), ("bar_gland", "bar_cover"),
              ("button", "saddle_button"), ("inst_plate", "saddle_plate"), ("plate_bolts", "inst_plate"),
              ("radar_arm", "saddle_radar"), ("arm_bolts", "radar_arm"), ("radar", "radar_arm"), ("pir", "radar_arm"),
              ("enc_plate", "saddle_enc_low"), ("enc_plate", "saddle_enc_up"), ("enc_plate_bolts", "enc_plate"),
              ("enc_body", "enc_plate"), ("lugs", "enc_plate"), ("lugs", "enc_body"), ("lug_screws", "lugs"),
              ("lid", "enc_body"), ("glands", "enc_body"), ("vent", "enc_body"), ("antenna", "enc_body"),
              ("mplate", "enc_body"), ("mppt", "mplate"), ("board", "mplate"), ("fuse_block", "mplate"),
              ("battery", "enc_body"), ("battery", "mplate"), ("strap", "battery"), ("strap", "mplate"),
              ("shield", "enc_plate"), ("shield_screws", "shield"),
              ("bracket", pole), ("set_screws", pole), ("rails", "bracket"), ("panel", "rails"), ("panel_bolts", "rails")]
    if own_post:
        touch += [("arb", "sign"), ("arb", "post")]
    for a, c in touch:
        d = dist(a, c)
        res.append((d <= 0.05, f"touch {a} / {c}: gap {d:.2f} mm"))
    # 3. clearances that must hold (mm)
    clear = [("shield", "enc_body", 20.0), ("shield", "lid", 20.0), ("shield", "lugs", 2.0), ("shield", "lug_screws", 2.0),
             ("shield", "antenna", 2.0), ("shield", "enc_plate_bolts", 2.0),
             ("sign", "bar_channel", 15.0), ("sign", "heads", 15.0), ("sign", "radar", 30.0), ("sign", "radar_arm", 30.0),
             ("sign", "band_radar", 20.0), ("sign", "band_enc_up", 15.0), ("sign", "saddle_radar", 30.0),
             ("saddle_radar", "saddle_sign_low", 2.0), ("band_radar", "saddle_sign_low", 5.0),
             ("band_sign_low", "saddle_radar", 5.0), ("button", "inst_plate", 10.0),
             ("battery", "glands", 5.0), ("battery", "vent", 5.0), ("board", "antenna", 10.0), ("mppt", "strap", 5.0),
             ("fuse_block", "strap", 5.0), ("bracket", "panel", 3.0), ("rails", "shield", 100.0),
             ("bracket", "antenna", 100.0), ("panel", "sign", 100.0), ("saddle_enc_up", "saddle_sign_up", 50.0),
             ("band_enc_up", "saddle_sign_up", 50.0), ("band_enc_low", "saddle_sign_low", 50.0)]
    for a, c, mn in clear:
        d = dist(a, c)
        res.append((d >= mn, f"clear {a} / {c}: {d:.1f} mm (at least {mn:g})"))
    # 4. pole range: the V seats both faces for the smallest and largest pole
    for od in (p["pole_min_od"], p["pole_max_od"]):
        sg = saddle_geom(od / 2, p)
        res.append((sg["contact_in"] > 2.0, f"pole {od:g} mm touches both V faces {sg['contact_in']:.1f} mm inside the saddle's back corners"))
    # 5. heights the requirements quote
    res.append((D["pir_bot"] >= 2500.0, f"lowest sensing part {D['pir_bot']:.0f} mm above the sidewalk (R14, 2,500 mm)"))
    res.append((D["enc_bot"] >= 2800.0, f"enclosure bottom {D['enc_bot']:.0f} mm (R14, 2,800 mm)"))
    if verbose:
        bad = [t for ok, t in res if not ok]
        for t in bad:
            print("FAIL", t)
        print(f"{sum(ok for ok, _ in res)} of {len(res)} checks pass")
    return res


def clash_check(p=PARAMS):
    """Kept for older callers: overlapping pairs of components, as (a, b, volume)."""
    return [t for ok, t in checks(p, own_post=True, verbose=False) if not ok and t.startswith("overlap")]


if __name__ == "__main__":
    if "--check" in sys.argv:
        r1 = checks(own_post=False)
        r2 = checks(own_post=True)
        sys.exit(0 if all(ok for ok, _ in r1 + r2) else 1)
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True); (out / "stl").mkdir(exist_ok=True)
    full = build_parts(PARAMS, True)
    groups = {
        "crosssafe-assembly": list(full.values()),
        "crosssafe-existing-pole": [v for k, v in full.items() if k not in (14, 19, "footing")],
        "sign-and-light-bar": [full[k] for k in (1, 2, 3, 17)],
        "pole-top-enclosure": [full[k] for k in (8, 9, 10, 11, 12, 18, 21, 23)],
    }
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.5, angular_tolerance=0.3)
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"overall height above sidewalk {D['overall_h']:.0f} mm; sign {D['sign_bot']:.0f} to {D['sign_top']:.0f}; "
          f"enclosure bottom {D['enc_bot']:.0f}; saddle front {D['saddle_front']:.1f} mm from the pole axis")
