"""CrossSafe concept options as detailed part lists (kit 1.9, STANDARDS section 24), detail level D3.

    option_a()   pole-top flashing beacon: the current design (CRS-DDR-003), built from the parametric
                 components in model.py and split into one part per physical item
    option_b()   kerbside solar bollard with in-road solar studs
    option_c()   pull-up retroreflective panel on a rope, no electronics

All three share the frame of model.py: the pole or bollard axis is Z, the sidewalk top is z = 0, traffic runs
along X, the sign or main face looks at approaching traffic on +X, the kerb and the waiting zone are on +Y.
Every function returns cad_parts.part() dicts. BOM line numbers are given for option A (the chosen design).
CONCEPT, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Circle, Cylinder, Pos, Rot, Sketch, extrude  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402
from crs_parts import soft, weld_on, ring_weld, washed, module, pframe  # noqa: E402

SS, AL, STEEL, HD = "stainless", "aluminium", "painted_steel", "hdpe_black"


# =============================================================================================== option A
def option_a(M):
    """Option A from the model's own components (existing-pole kit, the prototype that budget_usd covers)."""
    import build123d as b
    p = M.PARAMS
    D = M.derived(p)
    C = M.build_components(p, own_post=False)
    out = []

    def add(key, label, mat, kind, bom, group="shell", explode=(0, 0, 0), names=None, edge=True):
        shape, _ = C[key]
        sols = list(shape.solids())
        for i, s in enumerate(sols):
            nm = label if len(sols) == 1 else (f"{label} {names[i]}" if names else f"{label} {i + 1}")
            if edge and kind in ("made", "bought") and len(sols) == 1 and len(s.faces()) <= 12:
                s = soft(s, 0.8)
            out.append(part(nm, s, mat, kind=kind, bom=bom, group=group, explode=explode))

    # saddles and bands
    exs = {"button": (0, 600, 0), "plate": (0, 600, 100), "bar": (900, 0, -150), "sign_low": (500, 0, 0),
           "radar": (0, 500, 0), "enc_low": (-500, 0, 0), "sign_up": (500, 0, 0), "enc_up": (-500, 0, 0)}
    for n in D["stations"]:
        add(f"saddle_{n}", f"Keyed pole saddle, {n.replace('_', ' ')}", AL, "made", 20, explode=exs[n], edge=False)
        add(f"band_{n}", f"Band clamp with buckle, {n.replace('_', ' ')}", SS, "bought", 13, explode=exs[n])

    # M8 bolts get a plain washer under the head (ISO 7089): lift the bolt, add the washer
    def bolts_with_washers(key, label, axis, sign, group="shell", explode=(0, 0, 0)):
        shape, _ = C[key]
        for i, s in enumerate(shape.solids()):
            lifted, w = washed(s, axis, sign, 5.3, 1.6, 8.4, 16.0)
            out.append(part(f"{label} {i + 1}, M8 hex bolt (ISO 4017)", lifted, SS, kind="fastener", bom=15, group=group, explode=explode))
            out.append(part(f"{label} {i + 1}, M8 washer (ISO 7089)", w, "zinc_plated", kind="fastener", bom=15, group=group, explode=explode))

    add("sign", "Crossing warning sign, 750 mm diamond", AL, "bought", 1, explode=(500, 0, 250))
    bolts_with_washers("sign_bolts", "Sign bolt", 0, -1, explode=(500, 0, 250))
    add("bar_channel", "Light bar housing, folded channel", AL, "made", 2, explode=(900, 0, -150))
    add("bar_cover", "Light bar bottom cover", AL, "made", 2, explode=(900, 0, -350))
    add("bar_caps", "Light bar end cap", AL, "made", 2, explode=(900, 0, -150), names=["far", "kerb"])
    bolts_with_washers("bar_bolts", "Light bar saddle bolt", 0, -1, explode=(900, 0, -150))
    add("bar_gland", "Cable gland, light bar", HD, "bought", 15, explode=(900, 0, -450))
    add("heads", "Amber LED head", "matte_black", "bought", 3, explode=(1400, 0, -350))
    add("head_bezels", "LED head bezel", HD, "bought", 3, explode=(1400, 0, -350))
    add("head_visors", "LED head visor", HD, "bought", 3, explode=(1400, 0, -300))
    add("pilot", "Pedestrian pilot light", "polycarbonate", "bought", 17, explode=(900, 500, -300))
    add("button", "Push-button station", "matte_black", "bought", 4, explode=(0, 600, 0))
    add("inst_plate", "Instruction plate", AL, "made", 4, explode=(0, 750, 100))
    bolts_with_washers("plate_bolts", "Instruction plate bolt", 1, -1, explode=(0, 750, 100))
    add("radar_arm", "Radar arm, bent flat bar", AL, "made", 22, explode=(0, 500, -250))
    bolts_with_washers("arm_bolts", "Radar arm bolt", 1, -1, explode=(0, 500, -250))
    add("radar", "Presence radar module", "matte_black", "bought", 5, explode=(0, 500, 200))
    add("pir", "PIR wake sensor", "matte_black", "bought", 16, explode=(0, 500, -300), edge=False)
    add("enc_plate", "Enclosure mounting plate", AL, "made", 21, group="shell", explode=(-600, 0, 450))
    bolts_with_washers("enc_plate_bolts", "Mounting plate bolt", 0, 1, explode=(-600, 0, 450))
    add("enc_body", "Enclosure body, IP65 polycarbonate", "polycarbonate", "bought", 8, explode=(-1000, 0, 450))
    add("lid", "Enclosure lid", "polycarbonate", "bought", 8, explode=(-1500, 0, 450))
    add("vent", "Membrane vent", HD, "bought", 8, explode=(-1000, 0, 200), edge=False)
    add("glands", "Cable gland M20", HD, "bought", 15, explode=(-1000, 0, 200), names=["1", "2", "3", "4"])
    add("antenna", "LoRa whip antenna with bulkhead", "matte_black", "bought", 12, explode=(-1000, 0, 800), edge=False)
    add("lugs", "Enclosure mounting lug", "polycarbonate", "bought", 8, explode=(-800, 0, 450))
    add("lug_screws", "Lug screw M5 with nut", SS, "fastener", 15, explode=(-800, 0, 450), edge=False)
    add("mplate", "Internal mounting plate", "hdpe_natural", "bought", 8, group="internal", explode=(-1300, 0, 450))
    add("mppt", "MPPT charge controller", "matte_black", "bought", 10, group="internal", explode=(-1500, 500, 150))
    add("board", "Controller and radio board", "matte_black", "bought", 11, group="internal", explode=(-1500, 0, 750))
    add("fuse_block", "Fuse block", "matte_black", "bought", 15, group="internal", explode=(-1500, -500, 150))
    add("battery", "LiFePO4 battery 12.8 V 12 Ah", HD, "bought", 9, group="internal", explode=(-1400, 0, -300))
    add("strap", "Battery strap", AL, "made", 23, group="internal", explode=(-1400, 0, 100))
    add("shield", "Ventilated sun shield", AL, "made", 18, explode=(-1000, 0, 900))
    add("shield_screws", "Sun shield screw M5", SS, "fastener", 15, explode=(-1000, 0, 900), edge=False)

    # panel bracket (welded) with weld beads, set screws, rails, panel as frame and laminate
    xf = D["saddle_front"]
    so_d, so_t, so_l = p["socket"]
    cap_w, cap_t = p["cap"]
    ph_ = p["post_h"]
    add("bracket", "Panel bracket, welded socket, cap plate and cheeks", STEEL, "made", 7, group="accessory", explode=(0, 0, 300), edge=False)
    # beads: cap plate to socket tube (ring) and cheeks to cap plate
    out.append(part("Weld, cap plate to socket tube", ring_weld(so_d / 2, 3.0, ph_), STEEL, kind="weld", bom=7, group="accessory", explode=(0, 0, 300)))
    ct, cx = p["cheek"]
    rl, rt, rx = p["rail"]
    Zc0 = D["panel_zc"]
    zb_ = -p["panel"][2] / 2

    def g2(yp, zp):
        return (yp * math.cos(tilt) - zp * math.sin(tilt), Zc0 + yp * math.sin(tilt) + zp * math.cos(tilt))
    tilt = math.radians(p["panel_tilt"])
    piv = g2(p["pivot_yp"], zb_ - rt - (rl - rt) / 2)
    slo = g2(p["slot_yp"], zb_ - rt - (rl - rt) / 2)
    y_lo, y_hi = min(piv[0], slo[0]) - 22, max(piv[0], slo[0]) + 22
    for sx in (-1, 1):
        for side in (0, 1):
            x_edge = sx * (cx + ct) if side else sx * cx
            d_x = (sx if side else -sx)
            out.append(part(f"Weld, cheek to cap plate {'kerb' if sx > 0 else 'far'} {'outer' if side else 'inner'}",
                            weld_on((x_edge, y_lo, ph_ + cap_t), (0, 1, 0), y_hi - y_lo, 4.0, (d_x, 0, 0), (0, 0, 1)),
                            STEEL, kind="weld", bom=7, group="accessory", explode=(0, 0, 300)))
    add("set_screws", "Security set screw M10", SS, "fastener", 15, group="accessory", explode=(0, 0, 300), edge=False)
    add("rails", "Panel rail, angle 40 x 40 x 4", AL, "made", 7, group="accessory", explode=(0, -500, 600), names=["far", "kerb"])
    add("panel_bolts", "Rail bolt with nut", SS, "fastener", 15, group="accessory", explode=(0, -500, 600), edge=False)
    px, py, ptk = p["panel"]
    Zc = D["panel_zc"]
    F = b.Pos(0, 0, Zc) * b.Rot(p["panel_tilt"], 0, 0)
    fr, lam = pframe(px, py, ptk)
    out.append(part("Solar panel frame, aluminium 12 x 25 mm", F * fr, AL, kind="bought", bom=6, group="accessory", explode=(0, -500, 600)))
    out.append(part("Solar panel laminate, 20 W", F * lam, "matte_black", kind="bought", bom=6, group="accessory", explode=(0, -500, 600)))
    # the pole the existing-pole kit is built on (context)
    r = p["post_od"] / 2
    pole = b.Pos(0, 0, (ph_ - 800) / 2) * (b.Cylinder(r, ph_ + 800) - b.Cylinder(r - p["post_wall"], ph_ + 802))
    out.append(part("Existing pole 114.3 x 3.6 mm (site)", pole, "galvanised", kind="context", group="context"))
    return out


# =============================================================================================== shared helpers
def _pole(M, z0=-800.0):
    import build123d as b
    p = M.PARAMS
    r = p["post_od"] / 2
    h = p["post_h"]
    return part("Existing pole 114.3 x 3.6 mm (site)", b.Pos(0, 0, (h + z0) / 2) * (b.Cylinder(r, h - z0) - b.Cylinder(r - p["post_wall"], h - z0 + 2)),
                "galvanised", kind="context", group="context")


def _saddle_set(M, z, ang, label, explode=(0, 0, 0)):
    """A keyed saddle and its band, facing direction ang (deg about Z from +X), centred at height z."""
    import build123d as b
    loc = M.saddle_local(M.PARAMS["post_od"] / 2, M.PARAMS)
    T = b.Pos(0, 0, z) * b.Rot(0, 0, ang)
    return [part(f"Keyed pole saddle, {label}", T * loc["saddle"], AL, kind="made", group="shell", explode=explode),
            part(f"Band clamp with buckle, {label}", T * (loc["band"] + loc["buckle"]), SS, kind="bought", group="shell", explode=explode)]


def _bset(d, grip, loc, label, group="shell", explode=(0, 0, 0), mat=SS, bom=None):
    out = []
    for nm, shp in cp.hex_bolt_set(d, grip):
        out.append(part(f"{label}, {nm}", loc * shp, mat, kind="fastener", bom=bom, group=group, explode=explode))
    return out


# =============================================================================================== option C
def option_c(M):
    """Pull-up retroreflective panel on a rope: a pedestrian pulls a handle and a 400 x 500 mm panel slides up two angle guides
    above a backing plate on the pole; a pulley turns the pull into a lift. Shown raised. No electricity."""
    import build123d as b
    p = M.PARAMS
    r = p["post_od"] / 2
    xf = M.saddle_geom(r, p)["xf"]
    out = []
    xp = xf + 5.0                                   # backing plate front face
    z_s = (1950.0, 2650.0)
    for z in z_s:
        out += _saddle_set(M, z, 0.0, f"panel plate, z {z:.0f}", (400, 0, 0))
    # backing plate 520 x 950 x 5 on the two saddles, four M8 bolts with washers
    plate = M.box(xf, xp, -260, 260, 1850, 2800)
    for z in z_s:
        for dz in (-20, 20):
            plate = plate - M.rod((xf - 1, 0, z + dz), (xp + 1, 0, z + dz), 4.5)
    for yy in (68.0, 92.0):
        plate = plate - M.rod((xf - 1, yy, 1945.0), (xp + 1, yy, 1945.0), 2.0)       # buffer bracket screws (tapped M4)
    out.append(part("Backing plate, aluminium 5 mm", soft(plate, 0.8), AL, kind="made", explode=(300, 0, 0)))
    for z in z_s:
        for dz in (-20, 20):
            bl = M.bolt((xp, 0, z + dz), (-1, 0, 0), 16)
            lifted, w = washed(bl, 0, -1, 5.3, 1.6, 8.4, 16.0)
            out.append(part(f"Plate bolt z {z + dz:.0f}, M8 hex bolt (ISO 4017)", lifted, SS, kind="fastener", explode=(300, 0, 0)))
            out.append(part(f"Plate bolt z {z + dz:.0f}, M8 washer (ISO 7089)", w, "zinc_plated", kind="fastener", explode=(300, 0, 0)))
    # two angle guides 32 x 30 x 3, 800 long, standing legs on the plate, lips at the front retain the panel edges
    g0, gl = 1900.0, 800.0
    ang = b.Rot(0, 0, 180) * cp.angle(32, 30, 3, gl)
    left = b.Pos(xp + 32, 210, g0) * ang
    right = b.mirror(left, b.Plane.XZ)
    out.append(part("Guide angle, kerb side, aluminium 32 x 30 x 3", left, AL, kind="made", explode=(600, 0, 0)))
    out.append(part("Guide angle, far side, aluminium 32 x 30 x 3", right, AL, kind="made", explode=(600, 0, 0)))
    for sy in (1, -1):
        for zz in (g0, g0 + gl - 150):
            out.append(part(f"Weld, guide to plate {'kerb' if sy > 0 else 'far'} z {zz:.0f}",
                            weld_on((xp, sy * 210, zz), (0, 0, 1), 150.0, 4.0, (0, sy, 0), (1, 0, 0)), AL, kind="weld", explode=(600, 0, 0)))
    # panel 400 x 500 x 3 raised to z 2150..2650, with a lift clip over its top edge bolted through
    px0, pt = xp + 22.0, 3.0
    panel = M.box(px0, px0 + pt, -200, 200, 2150, 2650) - M.rod((px0 - 1, 0, 2635), (px0 + pt + 1, 0, 2635), 2.75)
    out.append(part("Warning panel, aluminium 3 mm with retroreflective sheeting", soft(panel, 0.6), AL, kind="bought", explode=(1000, 0, 0)))
    cl = M.box(px0 - 3, px0 + pt + 3, -10, 10, 2620, 2653) - M.box(px0, px0 + pt, -11, 11, 2619, 2650.0)
    cl = cl + M.box(px0, px0 + pt, -10, 10, 2653, 2685)
    cl = cl - M.rod((px0 - 4, 0, 2635), (px0 + pt + 4, 0, 2635), 2.75) - M.rod((px0 - 1, 0, 2670), (px0 + pt + 1, 0, 2670), 3.0)
    out.append(part("Lift clip, aluminium 3 mm", cl, AL, kind="made", explode=(1000, 0, 200)))
    loc = b.Pos(px0 + pt + 3, 0, 2635) * b.Rot(0, 90, 0)
    out += _bset(5, 9.0, loc, "Lift clip bolt", explode=(1000, 0, 200))
    # pulley bracket: two ears welded to the plate's front face above the guides; a pulley on a pin
    xc, zc = xp + 22.0 + 1.5 + 29.5, 2800.0
    for sy in (-1, 1):
        y0, y1 = sorted((sy * 16.0, sy * 22.0))
        ear = M.box(xp, xc + 20, y0, y1, 2700, 2860) - M.rod((xc, y0 - 1, zc), (xc, y1 + 1, zc), 5.25)
        out.append(part(f"Pulley ear, {'kerb' if sy > 0 else 'far'}, aluminium 6 mm", soft(ear, 0.8), AL, kind="made", explode=(1000, sy * 100, 300)))
        yo = sy * 22.0
        out.append(part(f"Weld, pulley ear to plate {'kerb' if sy > 0 else 'far'}",
                        weld_on((xp, yo, 2700), (0, 0, 1), 100.0, 4.0, (0, sy, 0), (1, 0, 0)), AL, kind="weld", explode=(1000, sy * 100, 300)))
    pul = b.Pos(xc, 0, zc) * b.Rot(90, 0, 0) * cp.pulley(60, 28, 14)
    out.append(part("Rope pulley 60 mm, HDPE", pul, "hdpe_natural", kind="bought", explode=(1000, 0, 300)))
    bu = b.Pos(xc, 14, zc) * b.Rot(90, 0, 0) * cp.bush(14, 10.4, 28)
    out.append(part("Pulley bush, UHMW-PE", bu, "hdpe_natural", kind="bought", explode=(1000, 0, 300)))
    pin = b.Pos(xc, -22, zc) * b.Rot(90, 0, 0) * cp.clevis_pin(10, 44)
    out.append(part("Pulley axle, clevis pin 10 mm (ISO 2341), A4 stainless", pin, SS, kind="bought", explode=(1000, -200, 300)))
    out.append(part("Split pin 3.2 mm (ISO 1234)", b.Pos(xc, 32.0, zc) * cp.split_pin(10), SS, kind="fastener", explode=(1000, 200, 300)))
    # rope 5 mm over the pulley to the handle
    Rr = 29.5
    pts = [(px0 + pt / 2, 0, 2688.0), (px0 + pt / 2, 0, zc)]
    for k in range(1, 8):
        th = math.radians(180 - 22.5 * k)
        pts.append((xc + Rr * math.cos(th), 0, zc + Rr * math.sin(th)))
    xr = xc + Rr
    z_h = 1150.0
    pts += [(xr, 0, zc), (xr, 0, z_h + 16 + 2.6)]
    out.append(part("Pull rope 5 mm, polyester", cp.rope(pts, 5.0), "rope", kind="bought", explode=(1100, 0, 0)))
    h = b.Pos(xr, 0, z_h) * b.Rot(90, 0, 0) * b.Cylinder(16, 180)
    out.append(part("Pull handle, HDPE 32 mm", soft(h, 2.0), "hdpe_black", kind="bought", explode=(1100, 0, -400)))
    # end-of-travel buffer (CRS-DDR-005, STEM check S21): a hydraulic damper under the lowered panel, on a bracket with a barrel clip
    xb = xp + 3.0 + 8.0
    br = M.box(xp, xp + 3, 62, 98, 1925, 1965) + (b.Pos(xb, 80, 1945) * b.Cylinder(11.0, 40) - b.Pos(xb, 80, 1945) * b.Cylinder(8.2, 42))
    for yy in (68.0, 92.0):
        br = br - M.rod((xp - 1, yy, 1945.0), (xp + 4, yy, 1945.0), 2.2)
    out.append(part("Buffer bracket with barrel clip, aluminium 3 mm", br, AL, kind="made", explode=(300, 0, 0)))
    for yy in (68.0, 92.0):
        out.append(part(f"Buffer bracket screw y {yy:+.0f}, M4 hex bolt (ISO 4017)", M.bolt((xp + 3, yy, 1945.0), (-1, 0, 0), 7, d=4.0, af=7.0, head_h=2.8),
                        SS, kind="fastener", explode=(300, 0, 0)))
    out.append(part("Buffer damper, hydraulic, 16 mm barrel, 25 mm stroke", b.Pos(xb, 80, 1945) * b.Cylinder(8.0, 90) + b.Pos(xb, 80, 2000) * b.Cylinder(3.0, 100), SS,
                    kind="bought", explode=(300, 0, 200)))
    out.append(part("Buffer pad, EPDM", soft(b.Pos(xb, 80, 2053) * b.Cylinder(8.0, 6), 0.8), "epdm", kind="bought", explode=(300, 0, 200)))
    out.append(_pole(M))
    return out


# =============================================================================================== option B
def _stud():
    """One solar road stud in its own frame: road surface z = 0, body below it, lens above. Returns a list of
    (name, shape, material, kind, colour) with the body, gasket, lens, circuit board, cell, solar tile and four screws."""
    import build123d as b
    R, Rp = 60.0, 52.0
    body = b.Pos(0, 0, -15) * b.Cylinder(R, 30) - b.Pos(0, 0, -12) * b.Cylinder(Rp, 24)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        body = body + b.Pos(40 * math.cos(a), 40 * math.sin(a), -15) * b.Cylinder(4.0, 18)      # bosses, floor z -24 to top -6
    for k in range(4):
        a = math.radians(45 + 90 * k)
        body = body - b.Pos(56 * math.cos(a), 56 * math.sin(a), -3) * b.Cylinder(2.5, 6)         # tapped holes
    gasket = b.Pos(0, 0, 1) * (b.Cylinder(R, 2) - b.Cylinder(Rp, 3))
    lens = b.Pos(0, 0, 9) * b.Cylinder(R, 14) - b.Pos(0, 0, 5) * b.Cylinder(Rp, 6)
    lens = soft(lens, 2.0)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        hole = b.Pos(56 * math.cos(a), 56 * math.sin(a), 8) * b.Cylinder(2.75, 16)
        lens = lens - hole
        gasket = gasket - b.Pos(56 * math.cos(a), 56 * math.sin(a), 1) * b.Cylinder(2.75, 3)
    board = b.Pos(0, 0, -5) * b.Cylinder(51.8, 2)
    for k in range(4):
        a = math.radians(90 * k)
        board = board + b.Pos(42 * math.cos(a), 42 * math.sin(a), -2) * b.Cylinder(5.0, 4)       # amber LEDs, z -4 to 0
    cell = b.Pos(0, 0, -15) * b.Rot(0, 90, 0) * b.Cylinder(9.0, 65)
    tile = b.Pos(0, 0, -3) * b.Box(70, 40, 2)
    out = [("Stud body, cast aluminium", body, "cast_aluminium", "made", None),
           ("Stud gasket, EPDM", gasket, "epdm", "bought", None),
           ("Stud lens, amber polycarbonate", lens, "polycarbonate", "bought", "#E8A33D"),
           ("Stud LED board", board, "matte_black", "bought", None),
           ("Stud cell, Li-ion 18650", soft(cell, 0.5), "matte_black", "bought", None),
           ("Stud solar tile", soft(tile, 0.3), "glass", "bought", "#1E2A4A")]
    for k in range(4):
        a = math.radians(45 + 90 * k)
        out.append((f"Stud screw {k + 1}, M5 hex bolt (ISO 4017)", b.Pos(56 * math.cos(a), 56 * math.sin(a), 16) * cp.hex_bolt(5, 20), "stainless", "fastener", None))
    return out


def option_b(M):
    """Kerbside solar bollard (button, radar, controller, battery, 10 W panel) with eight solar LED studs in the road across the
    crossing. The bollard is at the origin of the model frame, the kerb at y = 800 and the road beyond it."""
    import build123d as b
    out = []
    T = 5.0
    # base plate 260 x 260 x 10 on four M12 through-bolt anchors
    holes = [(sx * 100.0, sy * 100.0) for sx in (-1, 1) for sy in (-1, 1)]
    base = M.box(-130, 130, -130, 130, 0, 10)
    for x, y in holes:
        base = base - M.rod((x, y, -1), (x, y, 11), 7.0)
    out.append(part("Base plate, steel 10 mm", soft(base, 1.0), STEEL, kind="made", explode=(0, 0, -300)))
    for i, (x, y) in enumerate(holes, 1):
        out.append(part(f"Anchor {i}, M12 through-bolt, zinc plated", b.Pos(x, y, 10) * cp.anchor_bolt(12, 100), "zinc_plated", kind="fastener", explode=(0, 0, -500)))
    # bollard tube 150 x 150 x 5, 1250 long, with the window, screw holes and shelf bolt holes
    tube = b.Pos(0, 0, 10) * cp.shs(150, T, 1250)
    tube = tube - M.box(-50, 50, -80, -60, 700, 1150)                              # access window, -Y face
    for x in (-57.0, 57.0):
        for z in (695.0, 1155.0):
            tube = tube - M.rod((x, -76, z), (x, -69, z), 2.5)                   # door screw holes (tapped M5)
    for y in (-45.0, 45.0):
        tube = tube - M.rod((-80, y, 686), (80, y, 686), 4.25)                   # shelf bolts through both walls
    for x in (-22.0, 22.0):
        tube = tube - M.rod((x, 69, 1210), (x, 76, 1210), 2.5)                   # radar screws
    for x in (-25.0, 25.0):
        tube = tube - M.rod((x, 69, 1050), (x, 76, 1050), 2.5)                   # button screws
    out.append(part("Bollard tube, SHS 150 x 150 x 5", tube, STEEL, kind="made", explode=(0, 0, 0)))
    # four gussets 60 x 60 x 6 and the welds: gusset to plate (both sides), tube to plate (two beads a side)
    for k in range(4):
        R = b.Rot(0, 0, 90 * k)
        g = b.extrude(b.Plane.XZ * b.Polygon((75, 10), (135, 10), (75, 70), align=None), 6)    # XZ plane: extrudes toward -y
        g = b.Pos(0, 3, 0) * g
        out.append(part(f"Gusset {k + 1}, steel 6 mm", R * g, STEEL, kind="made", explode=(0, 0, -200)))
        for sy in (-1, 1):
            out.append(part(f"Weld, gusset {k + 1} to plate {'a' if sy > 0 else 'b'}",
                            R * weld_on((75, sy * 3, 10), (1, 0, 0), 60.0, 4.0, (0, sy, 0), (0, 0, 1)), STEEL, kind="weld", explode=(0, 0, -200)))
            y0, y1 = (8.0, 75.0) if sy > 0 else (-75.0, -8.0)
            out.append(part(f"Weld, tube {k + 1} to plate {'a' if sy > 0 else 'b'}",
                            R * weld_on((75, y0, 10), (0, 1, 0), y1 - y0, 5.0, (1, 0, 0), (0, 0, 1)), STEEL, kind="weld", explode=(0, 0, -200)))
    # cap plate 360 x 290 x 5 with beads, antenna, panel and four clips
    cap = M.box(-180, 180, -145, 145, 1260, 1265)
    cap = cap - M.rod((-165, 0, 1259), (-165, 0, 1266), 8.0)
    clip_pos = [(sx * 164.0, sy * 60.0) for sx in (-1, 1) for sy in (-1, 1)]
    for x, y in clip_pos:
        cap = cap - M.rod((x, y, 1259), (x, y, 1266), 2.75)
    out.append(part("Cap plate, steel 5 mm", soft(cap, 0.8), STEEL, kind="made", explode=(0, 0, 400)))
    for k in range(4):
        R = b.Rot(0, 0, 90 * k)
        out.append(part(f"Weld, cap plate to tube {k + 1}", R * weld_on((75, -75, 1260), (0, 1, 0), 150.0, 4.0, (1, 0, 0), (0, 0, -1)), STEEL, kind="weld", explode=(0, 0, 400)))
    ant = (M.rod((-165, 0, 1265), (-165, 0, 1271), 10) + M.rod((-165, 0, 1260), (-165, 0, 1265), 8) + M.rod((-165, 0, 1271), (-165, 0, 1421), 6)
           + M.rod((-165, 0, 1255), (-165, 0, 1260), 10))
    out.append(part("LoRa whip antenna with bulkhead", ant, "matte_black", kind="bought", explode=(0, 0, 800)))
    fr, lam = pframe(300.0, 250.0, 25.0)
    out.append(part("Solar panel frame, 10 W, aluminium", b.Pos(0, 0, 1265 + 12.5) * fr, AL, kind="bought", explode=(0, 0, 700)))
    out.append(part("Solar panel laminate, 10 W", b.Pos(0, 0, 1265 + 12.5) * lam, "matte_black", kind="bought", explode=(0, 0, 700)))
    pts = [(0, 0), (25, 0), (25, 3), (3, 3), (3, 28), (-9, 28), (-9, 25), (0, 25)]
    for i, (x, y) in enumerate(clip_pos, 1):
        c = b.extrude(b.Polygon(*pts, align=None), 30)
        c = b.Pos(150.0, 15.0, 1265.0) * b.Rot(90, 0, 0) * c                       # leg on the panel edge x = 150
        if x < 0:
            c = b.mirror(c, b.Plane.YZ)
        c = b.Pos(0, y, 0) * c                                                       # 30 wide, centred on y
        c = c - M.rod((x, y, 1264), (x, y, 1270), 2.75)
        out.append(part(f"Panel clip {i}, aluminium 3 mm", c, AL, kind="made", explode=(x * 2, y * 2, 700)))
        out += _bset(5, 8.0, b.Pos(x, y, 1268), f"Panel clip {i} bolt", explode=(x * 2, y * 2, 700))
    # access door 130 x 480 x 3 and four M5 screws; the board is carried on the door's inner face
    door = M.box(-65, 65, -78, -75, 685, 1165)
    for x in (-57.0, 57.0):
        for z in (695.0, 1155.0):
            door = door - M.rod((x, -79, z), (x, -74, z), 2.75)
    out.append(part("Access door, aluminium 3 mm", soft(door, 0.6), AL, kind="made", explode=(0, -400, 0)))
    for x in (-57.0, 57.0):
        for z in (695.0, 1155.0):
            out.append(part(f"Door screw x {x:.0f} z {z:.0f}, M5 hex bolt (ISO 4017)", b.Pos(x, -78, z) * b.Rot(90, 0, 0) * cp.hex_bolt(5, 10), SS, kind="fastener", explode=(0, -400, 0)))
    brd = M.box(-45, 45, -69, -55, 760, 860)
    for sx in (-1, 1):
        for z in (770.0, 850.0):
            brd = brd + M.rod((sx * 40.0, -75, z), (sx * 40.0, -69, z), 3.0)
    out.append(part("Controller, radio and MPPT board", soft(brd, 0.6), "matte_black", kind="bought", group="internal", explode=(0, -600, 0)))
    # shelf 138 x 138 x 3 on two M8 through-bolts, battery on the shelf
    out.append(part("Shelf, aluminium 3 mm", soft(M.box(-69, 69, -69, 69, 690, 693), 0.5), AL, kind="made", group="internal", explode=(0, 0, 0)))
    for y in (-45.0, 45.0):
        out += _bset(8, 150.0, b.Pos(75, y, 686) * b.Rot(0, 90, 0), f"Shelf bolt y {y:.0f}", group="internal")
    out.append(part("LiFePO4 battery 12.8 V 6 Ah", soft(M.box(-47.5, 47.5, -49, 49, 693, 844), 1.5), "hdpe_black", kind="bought", group="internal", explode=(0, 0, 400)))
    # radar module and button station on the +Y face
    rad = M.box(-30, 30, 75, 100, 1180, 1240) - M.rod((-22, 74, 1210), (-22, 101, 1210), 2.75) - M.rod((22, 74, 1210), (22, 101, 1210), 2.75)
    out.append(part("Presence radar module", soft(rad, 0.8), "matte_black", kind="bought", explode=(0, 500, 200)))
    for x in (-22.0, 22.0):
        out.append(part(f"Radar screw x {x:.0f}, M5 hex bolt (ISO 4017)", b.Pos(x, 100, 1210) * b.Rot(-90, 0, 0) * cp.hex_bolt(5, 30), SS, kind="fastener", explode=(0, 500, 200)))
    btn = M.box(-35, 35, 75, 135, 970, 1130) - M.rod((-25, 74, 1050), (-25, 136, 1050), 2.75) - M.rod((25, 74, 1050), (25, 136, 1050), 2.75)
    out.append(part("Push-button station", soft(btn, 1.0), "matte_black", kind="bought", explode=(0, 700, 0)))
    for x in (-25.0, 25.0):
        out.append(part(f"Button screw x {x:.0f}, M5 hex bolt (ISO 4017)", b.Pos(x, 135, 1050) * b.Rot(-90, 0, 0) * cp.hex_bolt(5, 65), SS, kind="fastener", explode=(0, 700, 0)))
    # eight studs: two lines at x = -350 and x = -1850 (the crossing edges), four studs a line across the road
    base_parts = _stud()
    n = 0
    for x in (-350.0, -1850.0):
        for y in (1500.0, 3000.0, 4500.0, 6000.0):
            n += 1
            loc = b.Pos(x, y, -150.0)
            for nm, sh, mat, kind, col in base_parts:
                out.append(part(f"Stud {n}: {nm}", loc * sh, mat, kind=kind, group="studs", color=col, explode=(0, 0, 200)))
    # site
    out.append(part("Sidewalk slab (site)", b.Pos(0, -350, -150) * b.Box(1400, 2300, 300), "concrete", kind="context", group="context"))
    road = b.Pos(-1100, 4500, -300) * b.Box(3600, 7400, 300)
    out.append(part("Road pavement (site)", road, "concrete", kind="context", group="context"))
    return out
