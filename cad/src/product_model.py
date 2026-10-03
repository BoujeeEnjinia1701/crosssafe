"""CrossSafe product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a 750 mm crossing sign with rounded corners,
retroreflective sheeting, a black border and a walking-figure symbol on an aluminium blank; a
charcoal double-sided light bar with visors, bezels, clear lenses and amber LED arrays behind them
(one head per face lit, as in the wig-wag), and a lit pilot light on its kerb end; the presence
radar with its radome on a round arm and the PIR dome under it; stainless band clamps with their
screw housings and the keyed sign saddles; the push-button station with a large piezo button, a
tactile arrow, a lit acknowledgement ring and an instruction plate; and the pole top with the
ventilated white sun shield (louvre slots, security fasteners), the IP65 enclosure and its glands,
the battery, charger and controller board inside, the antenna, and the 20 W panel on its bracket.
Context is a compact patch of sidewalk, kerb, road and crossing markings with tactile paving, and
the shared clay mannequin waiting at the kerb.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.
A research prototype, not a certified traffic control device.

Every main dimension, height and interface comes from PARAMS, derived() and build_parts() in
model.py, in the same axes: the post axis is Z with the sidewalk top at z = 0, the sign faces
approaching traffic on +X, the kerb and waiting zone are on +Y and the panel faces -Y. The post is
the 114.3 mm new-post variant (BOM 14). For framing only it is split into three touching sections
in different render groups (lower section as context, sign zone as shell, top as accessory); the
geometry is one continuous 3.7 m post as in model.py. See docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))

from build123d import (Axis, Box, Compound, Cylinder, Plane, Pos, RegularPolygon, Rot, Solid, Sphere,
                       Vector, extrude, fillet)
from model import PARAMS, derived

TITLE = "CrossSafe: solar crossing beacon that warns drivers when a pedestrian waits"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 22, "az": 38,
     "note": "Product render from the kerb side and the approach side, right and above (about 22 deg "
             "elevation); sign and lit light bar facing approaching traffic, push button, radar and pilot "
             "light toward the waiting pedestrian, solar pole top above"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 26, "az": -50,
     "note": "Exploded view from the front right and above (about 26 deg elevation): sign, saddles and "
             "clamps; light bar, LED heads and pilot light; radar and PIR; push-button station; sun "
             "shield, enclosure, battery, charger, controller board and antenna; panel and bracket"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 10, "az": 62,
     "note": "Detail from the kerb side and the approach side, slightly above (about 12 deg elevation), "
             "without the street or the pole top: lamp head with one amber head per face lit, pilot light, "
             "and the radar and PIR detector on their arm"},
]

# Context layout (mm, local frame): kerb line 800 mm in front of the post axis on +Y, as the
# concept media place the post; the crossing lies toward -X of the post.
KERB_Y = 800.0
ROAD_Z = -150.0
PATCH_X = (-1900.0, 700.0)
PATCH_Y = (-500.0, 2000.0)
CROSS_X = (-1750.0, -450.0)     # visible part of the zebra bars along X
PERSON_AT = (-1100.0, 470.0)    # mannequin waiting on the tactile paving, facing the road (+Y)
POST_SPLIT = (1950.0, 3350.0)   # render-group split heights of the one post

# Colours (restrained product palette; kit accent)
C_SHEET = "#D8DE3F"       # fluorescent yellow-green retroreflective sheeting
C_INK = "#16181C"
C_ALU = "#C3C8CE"
C_GALV = "#A9AFB6"
C_STEEL = "#B8BEC6"
C_BAR = "#2B2F36"
C_BLACK = "#1C1F24"
C_LENS = "#F3E6C4"
C_LED_ON = "#FFB020"
C_LED_OFF = "#7A5A1E"
C_BOARD = "#1F2328"
C_WHITE = "#F2F3F4"
C_SHELL = "#E4E6E9"
C_SHELL2 = "#C9CDD3"
C_ACCENT = "#0F766E"
C_ACK = "#2DD4BF"
C_CELL = "#1B2A44"
C_BUS = "#AEB6C0"
C_BATT = "#3B4A5C"
C_PCB = "#166534"
C_CHIP = "#111827"
C_LABEL = "#F4F4F2"
C_WALK = "#D6D3CD"
C_KERB = "#B9B6B0"
C_ROAD = "#4A4F57"
C_PAINT = "#F4F4F0"
C_TACT = "#E0B227"
C_CLAY = "#9CA3AF"


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _rod(a, b, r):
    a, b = Vector(*a), Vector(*b)
    d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _hex_x(x, y, z, af, length):
    return Pos(x - length / 2, y, z) * extrude(Plane.YZ * RegularPolygon(af / 1.732, 6), amount=length)


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _edges_par(s, axis):
    return s.edges().filter_by(axis)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _face_edges(s, axis, last):
    f = s.faces().sort_by(axis)
    return (f[-1] if last else f[0]).edges()


def product_parts(P=PARAMS):
    D = derived(P)
    r = D["post_r"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ------------------------------------------------------------ post (BOM 14), one tube in three render sections
    z0, z1 = POST_SPLIT
    tube = lambda za, zb: Pos(0, 0, (za + zb) / 2) * (Cylinder(r, zb - za) - Cylinder(r - P["post_wall"], zb - za + 2))
    add("Post, sign zone section", tube(z0, z1), C_GALV, "metal", 14, "shell", (0, 0, 0))
    add("Post, top section", tube(z1, P["post_h"]), C_GALV, "metal", 14, "accessory", (0, 0, 0))
    add("Post, lower section", tube(0.0, z0), C_GALV, "metal", 14, "context", (0, 0, 0))

    # ------------------------------------------------------------ sign (BOM 1) and saddles (BOM 20)
    side, st = P["sign_side"], P["sign_t"]
    sx, szc = D["sign_xc"], D["sign_zc"]
    ES = (650, 0, 320)
    place = lambda s: Pos(sx, 0, szc) * Rot(45, 0, 0) * s
    blank = Box(st, side, side)
    blank = _fillet_try(blank, _edges_par(blank, Axis.X), [40.0, 30.0, 20.0])
    add("Sign blank (aluminium)", place(blank), C_ALU, "metal", 1, "shell", ES)
    xf = st / 2
    sheet = Pos(xf + 0.4, 0, 0) * Box(0.8, side - 8, side - 8)
    sheet = _fillet_try(sheet, _edges_par(sheet, Axis.X), [36.0, 26.0, 16.0])
    add("Retroreflective sheeting", place(sheet), C_SHEET, "painted", 1, "shell", ES)
    bo = side - 34
    border = Box(0.4, bo, bo)
    border = _fillet_try(border, _edges_par(border, Axis.X), [26.0, 18.0, 10.0])
    bi = Box(1.0, bo - 36, bo - 36)
    bi = _fillet_try(bi, _edges_par(bi, Axis.X), [12.0, 8.0])
    border = Pos(xf + 1.0, 0, 0) * (border - bi)
    add("Sign border", place(border), C_INK, "painted", 1, "shell", ES)
    # walking figure (upright in the world, drawn in the Y-Z plane on the sheeting)
    xi = sx + xf + 1.0
    zc = szc - 10

    def limb(ya, za, yb, zb, w):
        a, b = Vector(xi, ya, za), Vector(xi, yb, zb)
        d = b - a
        ang = math.degrees(math.atan2(d.Y, d.Z))
        c = (a + b) * 0.5
        return Pos(c.X, c.Y, c.Z) * Rot(-ang, 0, 0) * Box(0.4, w, d.length + w * 0.6)

    fig = _union([
        _xcyl(xi, 18, zc + 205, 38, 0.4),                          # head
        limb(10, zc + 150, -18, zc - 20, 70),                      # torso
        limb(-18, zc - 20, 60, zc - 175, 44), limb(60, zc - 175, 48, zc - 250, 40),     # front leg
        limb(-18, zc - 20, -80, zc - 150, 44), limb(-80, zc - 150, -130, zc - 235, 40),  # back leg
        limb(5, zc + 125, 75, zc + 40, 32), limb(75, zc + 40, 110, zc + 80, 28),       # arm forward
        limb(0, zc + 125, -70, zc + 50, 32),                       # arm back
    ])
    fig = fig & _box(xi, 0, zc, 0.4, 600, 600)
    add("Sign symbol, walking figure", fig, C_INK, "painted", 1, "shell", ES)

    sw, sh = P["saddle"]
    sx0, sx1 = r, sx - st / 2
    sad = []
    for zz in D["sign_clamp_z"]:
        b_ = _box((sx0 + sx1) / 2 + 3, 0, zz, sx1 - sx0 - 6, sw, sh)
        b_ = _fillet_try(b_, _edges_par(b_, Axis.X), [6.0, 4.0])
        b_ -= Pos(0, 0, zz) * Cylinder(r + 0.5, sh + 2)
        for k in range(-3, 4):                                  # serrated grip face on the post side
            b_ -= _box(r + 1.0, k * 9.0, zz, 3.0, 2.0, sh + 2)
        b_ += _box(sx1 - 3, 0, zz, 6, sw + 10, sh + 10)           # sign bracket flange
        sad.append(b_)
    add("Keyed sign saddles (stainless)", _union(sad), C_STEEL, "metal", 20, "shell", (330, 0, 320))
    nuts = []
    for zz in D["sign_clamp_z"]:
        for dy in (-28, 28):
            n = _hex_x(sx + st / 2 + 3.0, dy, zz, 13.0, 6.0)
            n = n + _xcyl(sx + st / 2 + 7.0, dy, zz, 4.0, 4.0)
            nuts.append(n)
    add("Sign bracket nuts", _union(nuts), C_STEEL, "metal", 1, "shell", (700, 0, 320))

    # ------------------------------------------------------------ light bar (BOM 2), heads (BOM 3), pilot (BOM 17)
    bx, by, bz = P["bar"]
    bxc, bzc = D["bar_xc"], D["bar_zc"]
    EB = (300, 0, -380)
    hous = _box(bxc, 0, bzc, bx, by, bz)
    hous = _fillet_try(hous, _edges_par(hous, Axis.Y), [12.0, 9.0, 6.0])
    hous = _fillet_try(hous, _face_edges(hous, Axis.Y, True), [4.0, 2.0])
    hous = _fillet_try(hous, _face_edges(hous, Axis.Y, False), [4.0, 2.0])
    # parting line of the two folded halves, round the bar at its centre plane
    hous -= _box(bxc, 0, bzc, bx + 2, by + 2, 1.2) - _box(bxc, 0, bzc, bx - 1.6, by - 1.6, 2)
    hw, hh = P["head"]
    for y in (-P["head_dy"], P["head_dy"]):                     # recesses for the LED heads
        for s in (1, -1):
            hous -= _box(bxc + s * (bx / 2 - 2), y, bzc, 4.2, hw + 1, hh + 1)
    add("Light bar housing", hous, C_BAR, "painted", 2, "shell", EB)
    visors = []
    for y in (-P["head_dy"], P["head_dy"]):
        for s in (1, -1):
            vw = hw + 2 * P["bezel_w"] + 2 * P["visor_over"]             # visor and bezel sizes from model.py
            za = bzc + hh / 2 + P["bezel_w"]
            v = _box(bxc + s * (bx / 2 + P["visor_d"] / 2), y, za + P["visor_t"] / 2, P["visor_d"], vw, P["visor_t"])
            v += _box(bxc + s * (bx / 2 + P["visor_d"] - P["visor_t"] / 2), y, za - P["visor_lip"] / 2, P["visor_t"], vw, P["visor_lip"])
            visors.append(v)
    add("Head visors", _union(visors), C_BAR, "painted", 2, "shell", EB)
    add("Light bar post saddle", _box(r + 8, 0, bzc, 16, 80, 100), C_STEEL, "metal", 2, "shell", EB)

    lit_y = -P["head_dy"]
    for y in (-P["head_dy"], P["head_dy"]):
        for s in (1, -1):
            fx = bxc + s * bx / 2                                   # housing face
            EH = (EB[0] + s * 110, 0, EB[2])
            bez = _box(fx + s * P["head_flange"] / 2, y, bzc, P["head_flange"], hw + 2 * P["bezel_w"], hh + 2 * P["bezel_w"])
            bez = _fillet_try(bez, _edges_par(bez, Axis.X), [5.0, 3.0])
            bez -= _box(fx + s * 4, y, bzc, 10, hw, hh)
            face = "front" if s > 0 else "back"
            side_ = "left" if y < 0 else "right"
            add(f"LED head bezel, {face} {side_}", bez, C_BLACK, "plastic", 3, "shell", EH)
            lens = _box(fx + s * 6.5, y, bzc, 2.0, hw, hh)
            add(f"LED head lens, {face} {side_}", lens, C_LENS, "clear", 3, "shell", EH)
            board = _box(fx - s * 1.0, y, bzc, 2.0, hw, hh)
            add(f"LED head reflector board, {face} {side_}", board, C_BOARD, "plastic", 3, "internal", EH)
            dots = []
            for i in range(8):
                for j in range(3):
                    dy = (i - 3.5) * 16.0
                    dz = (j - 1) * 17.0
                    dots.append(_xcyl(fx + s * 1.5, y + dy, bzc + dz, 4.2, 3.0))
            on = (y == lit_y)
            add(f"LED head array, {face} {side_}" + (" (lit)" if on else ""), _union(dots),
                C_LED_ON if on else C_LED_OFF, "emissive" if on else "plastic", 3, "internal", EH)

    pd = P["pilot_d"]
    py0 = by / 2
    pil = _ycyl(bxc, py0 + 6, bzc, pd / 2 + 3, 12)
    pil = _fillet_try(pil, _face_edges(pil, Axis.Y, True), [2.0, 1.0])
    add("Pilot light housing", pil, C_BLACK, "plastic", 17, "shell", (EB[0], 120, EB[2]))
    dome = (_ycyl(bxc, py0 + 14, bzc, pd / 2 - 1, 4) + Pos(bxc, py0 + 14, bzc) * Sphere(pd / 2 - 1))
    dome &= _box(bxc, py0 + 20, bzc, pd + 4, 12, pd + 4)
    add("Pilot light lens (lit)", dome, C_LED_ON, "emissive", 17, "shell", (EB[0], 150, EB[2]))

    # ------------------------------------------------------------ radar (BOM 5) and PIR (BOM 16)
    rz, al, rs = P["radar_z"], P["arm_l"], P["radar"]
    ER = (0, 550, -600)
    arm = _rod((0, r, rz), (0, r + al, rz), 12)
    arm += _box(0, r + 10, rz, 50, 20, 60)                     # arm foot on the post
    arm = _fillet_try(arm, [], [1.0])
    add("Radar arm", arm, C_STEEL, "metal", 5, "shell", ER)
    ry = r + al + rs / 2
    rad = _box(0, ry, rz, rs, rs, rs)
    rad = _fillet_try(rad, rad.edges(), [10.0, 7.0, 4.0])
    rad -= _box(0, ry, rz, rs + 2, 0.8, rs + 2) - _box(0, ry, rz, rs - 1.4, 2, rs - 1.4)   # parting line
    add("Radar housing", rad, C_SHELL, "plastic", 5, "shell", ER)
    rdm = _box(0, ry + rs / 2 + 1.0, rz + 4, rs - 22, 2.0, rs - 30)
    rdm = _fillet_try(rdm, _edges_par(rdm, Axis.Y), [8.0, 5.0])
    rdm = _fillet_try(rdm, _face_edges(rdm, Axis.Y, True), [0.8, 0.5])
    add("Radar radome", rdm, C_SHELL2, "plastic", 5, "shell", ER)
    rl = _box(0, ry + rs / 2 + 0.2, rz - rs / 2 + 10, 34, 0.4, 5)
    add("Radar accent band", rl, C_ACCENT, "painted", 5, "shell", ER)
    pr = P["pir_d"] / 2
    pz = rz - rs / 2 - pr
    pir = _zcyl(0, ry, pz + pr / 2, pr, pr)
    pir = _fillet_try(pir, _top(pir), [2.0, 1.0])
    add("PIR sensor collar", pir, C_SHELL, "plastic", 16, "shell", (0, 550, -720))
    lens = Pos(0, ry, pz + 0.5) * Sphere(pr - 3) & _box(0, ry, pz - pr / 2, 2 * pr, 2 * pr, pr + 1)
    for k in range(1, 4):                                       # Fresnel facet rings
        lens -= Pos(0, ry, pz + 0.5) * (Sphere(pr - 2.5) - Sphere(pr - 3.4)) & _box(0, ry, pz - k * 5.0, 2 * pr, 2 * pr, 0.8)
    add("PIR Fresnel dome", lens, C_WHITE, "plastic", 16, "shell", (0, 550, -770))

    # ------------------------------------------------------------ clamps (BOM 13)
    t, w = P["band_t"], P["band_w"]

    def band(z, a=0.0):
        """Band with its screw housing turned `a` degrees about the post from -X, clear of the enclosure and bolt."""
        b = Pos(0, 0, z) * (Cylinder(r + t, w) - Cylinder(r, w + 2))
        b = _fillet_try(b, b.edges().filter_by_position(Axis.Z, z - w / 2 - 1, z + w / 2 + 1), [1.5, 1.0])
        hsg = _box(-(r + t + 6), 0, z, 14, 22, w - 4) - _box(-(r + t + 6), 0, z, 16, 8, w - 8)
        screw = _xcyl(-(r + t + 14), 0, z, 5.0, 4.0) - _box(-(r + t + 16), 0, z, 2, 1.4, 7)
        return Rot(0, 0, a) * (b + hsg + screw)

    add("Band clamps, lamp head and radar", _union([band(bzc), band(rz)] + [band(z, 90.0) for z in D["sign_clamp_z"]]),
        C_STEEL, "metal", 13, "shell", (0, 0, 0))
    add("Band clamps, enclosure", _union([band(P["enc_z"] - 100, 180.0), band(P["enc_z"] + 100, 180.0)]),
        C_STEEL, "metal", 13, "accessory", (-250, 0, 0))

    # ------------------------------------------------------------ push-button station (BOM 4)
    ux, uy, uz = P["button"]
    wx, wz = P["plate"]
    bzb = P["button_z"]
    EU = (0, 450, -420)
    body = _box(0, r + uy / 2, bzb, ux, uy, uz)
    body = _fillet_try(body, _edges_par(body, Axis.Y), [10.0, 7.0, 4.0])
    body = _fillet_try(body, _face_edges(body, Axis.Y, True), [4.0, 2.0])
    body -= Pos(0, 0, bzb) * Cylinder(r + 0.3, uz + 2)
    add("Push-button housing", body, C_SHELL2, "painted", 4, "accessory", EU)
    yb = r + uy
    btn = _ycyl(0, yb + 3, bzb + 20, 26, 6)
    btn = _fillet_try(btn, _face_edges(btn, Axis.Y, True), [2.5, 1.5])
    add("Piezo button (stainless)", btn, C_STEEL, "metal", 4, "accessory", EU)
    ring = _ycyl(0, yb + 0.8, bzb + 20, 31, 1.6) - _ycyl(0, yb + 0.8, bzb + 20, 27, 3)
    add("Acknowledgement light ring (lit)", ring, C_ACK, "emissive", 4, "accessory", EU)
    arrow = (_box(-6, yb + 6.4, bzb + 20, 22, 0.8, 7)
             + Pos(14, yb + 6.4, bzb + 20) * Rot(90, 0, 0) * extrude(RegularPolygon(9, 3), amount=0.8, both=True))
    add("Tactile arrow", arrow, C_INK, "painted", 4, "accessory", EU)
    spk = [_ycyl(dx, yb + 0.3, bzb - 50, 1.6, 0.6) for dx in (-12, -6, 0, 6, 12)]
    spk += [_ycyl(dx, yb + 0.3, bzb - 58, 1.6, 0.6) for dx in (-9, -3, 3, 9)]
    add("Tone speaker grille", _union(spk), C_BLACK, "plastic", 4, "accessory", EU)
    pz_ = bzb + uz / 2 + 20 + wz / 2
    plate = _box(0, r + 4, pz_, wx, 4, wz)
    plate = _fillet_try(plate, _edges_par(plate, Axis.Y), [10.0, 6.0])
    add("Instruction plate", plate, C_WHITE, "painted", 4, "accessory", EU)
    yp = r + 6.2
    ink = [_box(0, yp, pz_ + wz / 2 - 30, wx - 30, 0.4, 26)]    # header band
    ink += [_box(-10, yp, pz_ + 60 - k * 22, wx - 70 - 20 * (k % 2), 0.4, 7) for k in range(3)]
    ink.append(_ycyl(0, yp, pz_ - 70, 32, 0.4) - _ycyl(0, yp, pz_ - 70, 26, 1))
    ink.append(Pos(0, yp, pz_ - 70) * Rot(90, 0, 0) * extrude(RegularPolygon(16, 3), amount=0.2, both=True))
    add("Instruction plate print", _union(ink[1:]), C_INK, "painted", 4, "accessory", EU)
    add("Instruction plate header", ink[0], C_ACCENT, "painted", 4, "accessory", EU)
    riv = [_ycyl(sx_ * (wx / 2 - 12), r + 6.5, pz_ + sz_ * (wz / 2 - 12), 4.0, 1.5)
           for sx_ in (-1, 1) for sz_ in (-1, 1)]
    add("Plate security fasteners", _union(riv), C_STEEL, "metal", 15, "accessory", EU)
    add("Band clamp, push button", band(bzb), C_STEEL, "metal", 13, "accessory", EU)

    # ------------------------------------------------------------ enclosure (BOM 8) and contents (BOM 9 to 12)
    ex, ey, ez = P["enc"]
    ew = P["enc_wall"]
    xc, ezc = D["enc_xc"], P["enc_z"]
    EE = (-200, -120, 0)
    eo = _box(xc, 0, ezc, ex, ey, ez)
    eo = _fillet_try(eo, _edges_par(eo, Axis.Z), [8.0, 5.0])
    eo = _fillet_try(eo, _bottom(eo), [3.0, 2.0])
    enc = eo - _box(xc, 0, ezc, ex - 2 * ew, ey - 2 * ew, ez - 2 * ew)
    enc -= _box(xc, 0, ezc + ez / 2 - 30, ex + 2, ey + 2, 1.0) - _box(xc, 0, ezc + ez / 2 - 30, ex - 1.4, ey - 1.4, 2)
    add("Enclosure (IP65 polycarbonate)", enc, C_SHELL, "plastic", 8, "accessory", EE)
    bp = _box(-(r + (P["enc_gap"] - ex / 2) / 2), 0, ezc, P["enc_gap"] - ex / 2, 120, 200)
    add("Enclosure back plate", bp, C_STEEL, "metal", 8, "accessory", (-120, 0, 0))
    gl = []
    for dy in (-70, 0, 70):
        g = _hex_z(xc, dy, D["enc_bot"] - 2.5, 20.0, 5.0) + _zcyl(xc, dy, D["enc_bot"] - 9.0, 8.0, 8.0)
        g = _fillet_try(g, _bottom(g), [2.0, 1.0])
        gl.append(g)
    gl.append(_zcyl(xc + 40, 95, D["enc_bot"] - 3, 7.0, 6.0))    # membrane vent
    add("Cable glands and membrane vent", _union(gl), C_BLACK, "plastic", 8, "accessory", (-200, -120, -120))

    b = P["battery"]
    EI = (-420, -120, -330)
    bat = _box(xc, 0, D["enc_bot"] + ew + b[2] / 2, *b)
    bat = _fillet_try(bat, _edges_par(bat, Axis.Z), [4.0, 2.0])
    bat = _fillet_try(bat, _top(bat), [2.0, 1.0])
    add("LiFePO4 battery", bat, C_BATT, "plastic", 9, "accessory", EI)
    bt = D["enc_bot"] + ew + b[2]
    term = _zcyl(xc - 25, -50, bt + 4, 5, 8) + _zcyl(xc - 25, 50, bt + 4, 5, 8)
    add("Battery terminals", term, "#B91C1C", "plastic", 9, "accessory", EI)
    blab = _box(xc + b[0] / 2 + 0.2, 0, D["enc_bot"] + ew + b[2] / 2, 0.4, 110, 50)
    add("Battery label", blab, C_LABEL, "paper", 9, "accessory", EI)
    m = P["mppt"]
    EM = (-420, -120, -120)
    mp = _box(xc - 30, 55, ezc + 10, *m)
    mp = _fillet_try(mp, mp.edges(), [2.0, 1.0])
    for k in range(6):
        mp -= _box(xc - 30 - m[0] / 2, 55 - 37.5 + 15 * k, ezc + 10, 8, 4, m[2] - 10)
    add("MPPT charge controller", mp, "#1F2937", "metal", 10, "accessory", EM)
    c = P["board"]
    EC = (-420, -120, 80)
    cbx = xc + ex / 2 - ew - c[0] / 2 - 4
    pcb = _box(cbx + c[0] / 2 - 1, 0, ezc + 60, 2, c[1], c[2])
    add("Controller and radio board PCB", pcb, C_PCB, "plastic", 11, "accessory", EC)
    comps = (_box(cbx + c[0] / 2 - 6, -40, ezc + 70, 8, 40, 30) + _box(cbx + c[0] / 2 - 5, 45, ezc + 45, 6, 30, 22)
             + _box(cbx + c[0] / 2 - 4, 30, ezc + 88, 4, 50, 8))
    add("LoRa module and LED drivers", comps, C_CHIP, "plastic", 11, "accessory", EC)
    can = _box(cbx + c[0] / 2 - 10.5, -40, ezc + 70, 1.0, 36, 26)
    add("Radio shield can", can, C_STEEL, "metal", 11, "accessory", EC)
    ad, al_ = P["antenna"]
    ant = _zcyl(xc, 90, D["enc_top"] + 10, ad + 2, 20)
    ant += _zcyl(xc, 90, D["enc_top"] + al_ / 2 + 10, ad, al_ - 20)
    ant += Pos(xc, 90, D["enc_top"] + al_) * Sphere(ad)
    ant = _fillet_try(ant, [], [1.0])
    add("LoRa antenna", ant, C_BLACK, "rubber", 12, "accessory", (-450, -120, 560))

    # sun shield (BOM 18): roof and three walls, louvre slots, security fasteners
    g, sht = P["shield_gap"], P["shield_t"]
    shx, shy, shz = D["shield"]
    x_front = xc + ex / 2
    x_back = x_front - shx
    z_top = D["enc_top"] + g
    SH = (-450, -120, 330)
    roof = _box(x_front - shx / 2, 0, z_top + sht / 2, shx, shy, sht)
    back = _box(x_back + sht / 2, 0, z_top - shz / 2 + sht / 2, sht, shy, shz)
    walls = [_box(x_front - shx / 2, sy * (shy / 2 - sht / 2), z_top - shz / 2 + sht / 2, shx, sht, shz)
             for sy in (-1, 1)]
    shield = roof + back + walls[0] + walls[1]
    shield = _fillet_try(shield, [], [1.0])
    shield -= _zcyl(xc, 90, z_top, ad + 3, 3 * sht)
    for k in range(5):
        zz = z_top - 70 - 45 * k
        for sy in (-1, 1):
            shield -= _box(x_front - shx / 2 + 8, sy * (shy / 2 - sht / 2), zz, shx - 70, 3 * sht, 9)
        shield -= _box(x_back + sht / 2, 0, zz, 3 * sht, shy - 70, 9)
    add("Sun shield (white aluminium)", shield, C_WHITE, "painted", 18, "accessory", SH)
    sf = []
    for sy in (-1, 1):
        for dz in (-60, 90):
            sf.append(_ycyl(x_front - 30, sy * (shy / 2 + 0.6), z_top - shz / 2 + dz, 4.0, 1.2))
    add("Shield security fasteners", _union(sf), C_STEEL, "metal", 15, "accessory", SH)

    # ------------------------------------------------------------ panel (BOM 6) on bracket (BOM 7)
    px, py, pt = P["panel"]
    tilt = P["panel_tilt"]
    pzc = D["panel_zc"]
    EP = (0, -330, 520)
    pl = lambda s: Pos(0, 0, pzc) * Rot(tilt, 0, 0) * s
    frame = Box(px, py, pt)
    frame = _fillet_try(frame, _edges_par(frame, Axis.Z), [4.0, 2.0])
    frame -= Pos(0, 0, pt / 2) * Box(px - 24, py - 24, 8)
    frame -= Pos(0, 0, -pt / 2) * Box(px - 12, py - 12, pt - 6)
    add("Solar panel frame", pl(frame), C_ALU, "metal", 6, "accessory", EP)
    lam = Pos(0, 0, pt / 2 - 4) * Box(px - 24, py - 24, 3.0)
    add("Solar cells under glass", pl(lam), C_CELL, "screen", 6, "accessory", EP)
    nx_, ny_ = 6, 4
    cw_, ch_ = (px - 24) / nx_, (py - 24) / ny_
    grid = [Pos(-(px - 24) / 2 + cw_ * i, 0, pt / 2 - 2.35) * Box(1.6, py - 26, 0.3) for i in range(1, nx_)]
    grid += [Pos(0, -(py - 24) / 2 + ch_ * j, pt / 2 - 2.35) * Box(px - 26, 1.6, 0.3) for j in range(1, ny_)]
    for i in range(nx_):
        for q in (-1, 1):
            grid.append(Pos(-(px - 24) / 2 + cw_ * (i + 0.5) + q * cw_ / 4, 0, pt / 2 - 2.4) * Box(0.8, py - 26, 0.2))
    add("Cell gaps and busbars", pl(_union(grid)), C_BUS, "metal", 6, "accessory", EP)
    jb = Pos(0, py / 4, -pt / 2 + 2) * Box(80, 60, 18)
    add("Panel junction box", pl(jb), C_BLACK, "plastic", 6, "accessory", EP)

    br = _zcyl(0, 0, P["post_h"] + 60, r + 6, 120) - _zcyl(0, 0, P["post_h"] + 60 - 20, r + 0.2, 120)
    br = _fillet_try(br, _top(br), [4.0, 2.0])
    br += _box(0, 0, P["post_h"] + 150, 60, 60, 80)
    br += Pos(0, 0, pzc - 25) * Rot(tilt, 0, 0) * Box(300, 160, 10)
    add("Panel bracket (steel)", br, C_GALV, "metal", 7, "accessory", (0, -150, 260))
    bolts = []
    for sx_ in (-1, 1):
        bolts.append(_ycyl(sx_ * 18, -30.8, P["post_h"] + 150, 6.5, 3.0))
        bolts.append(_xcyl(sx_ * (r + 7.5), 0, P["post_h"] + 40, 6.0, 3.0))
    add("Bracket security bolts", _union(bolts), C_STEEL, "metal", 7, "accessory", (0, -150, 260))

    # ------------------------------------------------------------ anti-rotation bolt (BOM 19), new posts only
    zb = D["sign_clamp_z"][1]
    x_end = sx - st / 2 - 2
    bolt = _rod((-r - 15, 0, zb), (x_end, 0, zb), P["bolt_d"] / 2)
    bolt += _hex_x(-r - 12, 0, zb, 16.0, 6.5)
    bolt += _xcyl(-r - 1.5, 0, zb, 10.0, 2.0)
    add("Anti-rotation bolt (M10, new posts)", bolt, C_STEEL, "metal", 19, "accessory", (-260, 0, 320))

    # ------------------------------------------------------------ context: sidewalk, kerb, road, crossing, person
    x0, x1 = PATCH_X
    y0, y1 = PATCH_Y
    xm, xl = (x0 + x1) / 2, x1 - x0
    walk = _box(xm, (y0 + KERB_Y - 150) / 2, -60, xl, KERB_Y - 150 - y0, 120)
    add("Sidewalk slab", walk, C_WALK, "painted", None, "context", (0, 0, 0))
    kerb = _box(xm, KERB_Y - 75, -135, xl, 150, 270)
    kerb = _fillet_try(kerb, kerb.edges().filter_by(Axis.X).filter_by_position(Axis.Z, -1, 1).filter_by_position(Axis.Y, KERB_Y - 1, KERB_Y + 1), [15.0, 8.0])
    add("Kerb stone", kerb, C_KERB, "painted", None, "context", (0, 0, 0))
    road = _box(xm, (KERB_Y + y1) / 2, ROAD_Z - 60, xl, y1 - KERB_Y, 120)
    add("Road surface (asphalt)", road, C_ROAD, "paper", None, "context", (0, 0, 0))
    cx0, cx1 = CROSS_X
    bars = [_box((cx0 + cx1) / 2, yc, ROAD_Z + 1.5, cx1 - cx0, 500, 3) for yc in (KERB_Y + 350,)]
    bars.append(_box((cx0 + cx1) / 2, (KERB_Y + 1100 + y1) / 2, ROAD_Z + 1.5, cx1 - cx0, y1 - KERB_Y - 1100, 3))
    add("Crossing markings", _union(bars), C_PAINT, "painted", None, "context", (0, 0, 0))
    tx, ty = PERSON_AT[0], KERB_Y - 150 - 300
    pad = _box(tx, ty, 2, 900, 600, 4)
    studs = [Pos(tx - 400 + 57 * i, ty - 250 + 62.5 * j, 4) * Sphere(11) & _box(tx - 400 + 57 * i, ty - 250 + 62.5 * j, 8, 30, 30, 8)
             for i in range(15) for j in range(9)]
    add("Tactile paving at the kerb", Compound(children=[pad] + studs), C_TACT, "rubber", None, "context", (0, 0, 0))
    from context_parts import mannequin
    person = Pos(PERSON_AT[0], PERSON_AT[1], 4) * Rot(0, 0, 180) * mannequin(1750, "stand")
    add("Person waiting, 1.75 m (clay mannequin)", person, C_CLAY, "clay", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:44s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
