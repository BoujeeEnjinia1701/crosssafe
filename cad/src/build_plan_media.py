"""CrossSafe prototype build plan pictures (CRS-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything; a single picture can be drawn with, for example, `joints 5`.
Every picture is drawn from cad/src/model.py (build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/CRS-DWG-101 to 109        making sketches for the made and drilled components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/*-holes.png         drilling layouts (matplotlib)
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import build123d as b  # noqa: E402
from model import PARAMS as P, build_components, derived, pole_context, saddle_local, box, rod  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
D = derived(P)
C = {k: v[0] for k, v in build_components(P, own_post=False).items()}
R = D["post_r"]
XF = D["saddle_front"]
EB = D["enc_back"]
ST = D["stations"]
REPO = "github.com/BoujeeEnjinia1701/crosssafe"

COL = {"saddle": "#475569", "band": "#0EA5E9", "pole": "#D6D3D1", "bar": "#94A3B8", "cover": "#CBD5E1", "heads": "#F59E0B",
       "pilot": "#EAB308", "sign": "#FACC15", "button": "#2563EB", "plate": "#93C5FD", "arm": "#64748B", "radar": "#7C3AED",
       "pir": "#DB2777", "encplate": "#94A3B8", "body": "#D1D5DB", "lid": "#E5E7EB", "lugs": "#374151", "pens": "#B45309",
       "antenna": "#111827", "mplate": "#A8A29E", "mppt": "#16A34A", "board": "#0F766E", "fuse": "#7C3AED", "battery": "#C2410C",
       "strap": "#E11D48", "shield": "#F5F5F4", "bracket": "#A8A29E", "rails": "#0E7490", "panel": "#1E3A8A", "bolt": "#111827"}


def S(*ks):
    out = None
    for k in ks:
        out = C[k] if out is None else out + C[k]
    return out


def G(*ks):
    return b.Compound(children=[C[k] for k in ks])


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & box(x0, x1, y0, y1, z0, z1)


def pole(z0, z1):
    return part("Pole (test post)", pole_context(P, z0, z1), COL["pole"])


def split(shape, x_min=None, x_max=None):
    """The pieces of a grouped part on one side of a plane x = const."""
    x0 = -1e4 if x_min is None else x_min
    x1 = 1e4 if x_max is None else x_max
    return shape & box(x0, x1, -1e4, 1e4, -1e4, 1e4)


def saddles(names):
    return b.Compound(children=[C[f"saddle_{n}"] for n in names])


def bands(names):
    return b.Compound(children=[C[f"band_{n}"] for n in names])


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "bar": part("Light bar housing", G("bar_channel", "bar_cover", "bar_caps"), COL["bar"]),
        "heads": part("Amber LED heads with bezels and visors (4)", G("heads", "head_bezels", "head_visors"), COL["heads"]),
        "pilot": part("Pilot light", C["pilot"], COL["pilot"]),
        "body": part("Enclosure body, drilled", S("enc_body", "vent"), COL["body"]),
        "pens": part("Glands and antenna", G("glands", "antenna"), COL["pens"]),
        "mplate": part("Internal plate", C["mplate"], COL["mplate"]),
        "modules": part("Charger, controller, fuse block", G("mppt", "board", "fuse_block"), COL["mppt"]),
        "strap": part("Battery strap", C["strap"], COL["strap"]),
        "battery": part("Battery", C["battery"], COL["battery"]),
        "lugs": part("Enclosure lugs (4)", G("lugs", "lug_screws"), COL["lugs"]),
        "encplate": part("Enclosure mounting plate", C["enc_plate"], COL["encplate"]),
        "lid": part("Enclosure lid", C["lid"], COL["lid"]),
        "panel": part("Solar panel", C["panel"], COL["panel"]),
        "rails": part("Panel rails (2)", C["rails"], COL["rails"]),
        "saddles": part("Keyed pole saddles (8)", saddles(ST), COL["saddle"]),
        "bands": part("Band clamps (8)", bands(ST), COL["band"]),
        "sign": part("Crossing warning sign", C["sign"], COL["sign"]),
        "button": part("Push-button station", C["button"], COL["button"]),
        "iplate": part("Instruction plate", C["inst_plate"], COL["plate"]),
        "arm": part("Radar arm", C["radar_arm"], COL["arm"]),
        "radar": part("Radar", C["radar"], COL["radar"]),
        "pir": part("PIR sensor", C["pir"], COL["pir"]),
        "bracket": part("Panel bracket", C["bracket"], COL["bracket"]),
        "shield": part("Sun shield", G("shield", "shield_screws"), "#E7E5E4"),
    }


# ----------------------------------------------------------------- overview
OV_ELEV, OV_AZIM = 14, -35


def _at(shape, u, v):
    """Offset that puts a shape's centre at screen position u (across the picture) and height v, for the
    overview camera, so the pulled-apart parts can be laid out in tidy rows."""
    a = math.radians(OV_AZIM)
    right = (-math.sin(a), math.cos(a))
    c = shape.bounding_box().center()
    return (u * right[0] - c.X, u * right[1] - c.Y, v - c.Z)


def _row(shapes, u0, du, v):
    """Shapes laid side by side in one row (each moved, then grouped)."""
    out = []
    for k, sh in enumerate(shapes):
        out.append(b.Pos(*_at(sh, u0 + k * du, v)) * sh)
    return b.Compound(children=out)


def overview():
    M = made()
    order = ["bar", "heads", "pilot", "body", "pens", "mplate", "modules", "strap", "battery", "lugs", "encplate", "lid",
             "panel", "rails", "saddles", "bands", "sign", "button", "iplate", "arm", "radar", "pir", "bracket", "shield"]
    names = list(ST)
    M["saddles"] = part("Keyed pole saddles (8)", _row([C[f"saddle_{n}"] for n in names], -1150, 125, 1350), COL["saddle"])
    M["bands"] = part("Band clamps (8)", _row([C[f"band_{n}"] for n in names], -1150, 125, 1080), COL["band"])
    for k, src in (("pilot", "pilot"), ("pir", "pir")):            # small parts drawn at 2.5 times size so they show
        c = C[src].bounding_box().center()
        M[k] = part(M[k].name + " (2.5 x size)", b.Pos(c.X, c.Y, c.Z) * (b.Pos(-c.X, -c.Y, -c.Z) * C[src]).scale(2.5), M[k].color)
    place = {"panel": (-650, 3800), "rails": (-250, 3800), "bracket": (80, 3800),
             "encplate": (-1180, 3000), "lugs": (-1000, 2560), "body": (-800, 3000), "pens": (-800, 2620),
             "mplate": (-560, 3000), "modules": (-380, 3000), "strap": (-210, 3060), "battery": (-210, 2860),
             "lid": (-10, 3000), "shield": (260, 3000),
             "bar": (-640, 2250), "heads": (-640, 2050), "pilot": (-180, 2250), "sign": (520, 2200),
             "button": (-60, 1300), "iplate": (130, 1300), "arm": (420, 1300), "radar": (650, 1430), "pir": (650, 1180)}
    parts = []
    for k in order:
        p = M[k]
        p.explode = _at(p.shape, *place[k]) if k in place else (0, 0, 0)
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "CrossSafe prototype: every component, pulled apart",
                       subtitle="One assembly, numbered in build order and laid out by group: panel, enclosure, light bar and sign, "
                                "then the parts on the pole. Seen from the traffic side",
                       elev=OV_ELEV, azim=OV_AZIM, size=(11, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    out = []
    M = made()
    base = dict(project="CrossSafe", date=DATE)
    zb = D["bar_zc"]
    sg = D["saddle"]
    stub = lambda z0, z1: part("Pole", pole_context(P, z0, z1), COL["pole"])  # noqa: E731

    def want(n):
        return only is None or n in only

    # 101 light bar housing
    if want(101):
        hb = G("bar_channel", "bar_cover", "bar_caps")
        out.append(bv.component_sheet(
            Part("Light bar housing", hb, COL["bar"]),
            [M["heads"], M["pilot"], part("Saddle", C["saddle_bar"], COL["saddle"]), part("Band", C["band_bar"], COL["band"]), stub(1950, 2450),
             part("Sign", win(C["sign"], -1e3, 1e3, -1e3, 1e3, 2200, 2500), COL["sign"])],
            dwg_no="CRS-DWG-101", title="CrossSafe light bar housing: making sketch", material="Aluminium sheet 2 mm, 5052 class",
            view_shape=b.Pos(-D["bar_xc"], 0, -zb) * hb, inset_view=(18, -40),
            notes=["Three parts: a folded channel, a bottom cover and two end caps.",
                   "Channel: blank 716 x 346 mm (check the developed length with a test",
                   "  bend). Fold a 10 mm lip, the 128 mm back wall, the 70 mm top,",
                   "  the 128 mm front wall and a 10 mm lip; both lips point inward.",
                   "Head cut-outs: four, 128 x 50 mm, two in each wall, centred 200 mm",
                   "  each side of the middle and 65 mm up from the underside.",
                   "Back wall: two 9 mm holes on the middle, 45 and 85 mm up.",
                   "Cover: 70 x 716 mm, a 16 mm gland hole 60 mm from the middle on",
                   "  the road-side half; M4 screws into rivet nuts in the lips.",
                   "End caps: 70 x 130 mm with 15 mm flanges folded in on three sides;",
                   "  rivet into the channel ends. Kerb-end cap: 22 mm pilot light hole.",
                   "Fit: the back wall bolts flat to its saddle; the cover comes off for",
                   "  the two bolts. Check: square, cover seats on both lips."],
            **base))

    # 102 enclosure body, drilled; drawn upside down so the top view shows the bottom face
    if want(102):
        exc, ezc = D["enc_xc"], P["enc_z"]
        flip = b.Rot(180, 0, 0) * b.Pos(-exc, 0, -ezc) * C["enc_body"]
        out.append(bv.component_sheet(
            Part("Enclosure body", C["enc_body"], COL["body"]),
            [M["encplate"], M["pens"], M["lugs"], M["shield"]],
            dwg_no="CRS-DWG-102", title="CrossSafe enclosure body: drilling sketch",
            material="Bought IP65 polycarbonate box 150 x 260 x 300 mm",
            view_shape=flip, inset_view=(-25, -130),
            notes=["Drawn upside down: the top view shows the bottom face as you see it",
                   "  with the box standing on its roof, back face toward you.",
                   "Back face: the face that goes on the mounting plate. Measure from it,",
                   "  and sideways from the centre line.",
                   "Bottom face, four 20 mm holes for M20 glands: 40 and 100 mm from the",
                   "  back face, 105 mm each side of the centre line.",
                   "Vent: one 12 mm hole 130 mm from the back face on the centre line.",
                   "Roof: one 16 mm hole for the antenna, 75 mm from the back face and",
                   "  90 mm toward the kerb side.",
                   "Tape the faces, pilot drill 3 mm with wood behind, open out with a",
                   "  step drill at low speed. No solvents: polycarbonate crazes.",
                   "Fit the lug kit to the four back corners as its maker describes.",
                   "Check: each hole size against the part's datasheet; no cracks."],
            **base))

    # 103 battery strap
    if want(103):
        st = C["strap"]
        out.append(bv.component_sheet(
            Part("Battery strap", st, COL["strap"]), [M["battery"], M["mplate"], part("Enclosure", C["enc_body"], COL["body"])],
            dwg_no="CRS-DWG-103", title="CrossSafe battery strap: making sketch", material="Aluminium strip 25 x 2 mm, 5052 or 6061 class",
            view_shape=b.Rot(0, 0, 90) * b.Pos(-st.bounding_box().center().X, 0, -st.bounding_box().center().Z) * st,
            inset_view=(20, -140),
            notes=["Cut 180 mm of 25 x 2 mm strip; round the corners.",
                   "Bend to a Z, inside bend radius about 2 mm: a 40 mm leg that stands",
                   "  on the internal plate, a 97 mm top that lies on the battery and",
                   "  a 40 mm leg that comes down the battery's front.",
                   "Two 4 mm holes on the centre of the plate leg, 15 and 30 mm above",
                   "  the top's underside.",
                   "Fit: tap two M4 holes in the internal plate to match, on its",
                   "  centre line 113 and 128 mm above the enclosure's inside floor.",
                   "The top lies on the battery and the front leg stops it sliding",
                   "  out; the battery stands on the floor against the plate.",
                   "Check: the battery cannot move with the strap screwed down."],
            **base))

    # 104 enclosure mounting plate, turned so its face is in the front view
    if want(104):
        mp = C["enc_plate"]
        out.append(bv.component_sheet(
            Part("Enclosure mounting plate", mp, COL["encplate"]),
            [part("Saddles", S("saddle_enc_low", "saddle_enc_up"), COL["saddle"]), stub(2650, 3350)],
            dwg_no="CRS-DWG-104", title="CrossSafe enclosure mounting plate: making sketch", material="Aluminium sheet 4 mm, 5052 class",
            view_shape=b.Rot(0, 0, -90) * b.Pos(XF + 2, 0, -P["enc_z"]) * mp, inset_view=(18, -150),
            notes=["Cut 350 x 300 mm with a 90 x 90 mm tab centred above and below:",
                   "  480 mm tall overall. Round the outside corners to about 5 mm.",
                   "Heights from the bottom edge of the lower tab; sideways from the",
                   "  centre line. The plate-holes picture repeats every position.",
                   "Saddle bolts: four 9 mm holes on the centre line, 10 and 50 mm up,",
                   "  and 430 and 470 mm up (one pair in each tab).",
                   "Lug screws: four 5.5 mm holes 142 mm each side, 100 and 380 mm up.",
                   "Shield screws: drill 4.2 mm and tap M5, 164.5 mm each side,",
                   "  140 and 340 mm up.",
                   "Fit: the back face bolts flat on two saddles with four M8 bolts from",
                   "  the front; the enclosure hangs on its front by the four lugs.",
                   "Check: lay a saddle on each tab and look through the holes."],
            **base))

    # 105 panel rail
    if want(105):
        F = b.Pos(0, 0, D["panel_zc"]) * b.Rot(P["panel_tilt"], 0, 0)
        loc = F.inverse() * C["rails"]
        one = split(loc, x_min=0)
        bbr = one.bounding_box()
        vs = b.Rot(0, 0, 90) * b.Pos(-bbr.center().X, 0, -bbr.center().Z) * one
        out.append(bv.component_sheet(
            Part("Panel rail", C["rails"], COL["rails"]), [M["panel"], M["bracket"], stub(3500, 3720)],
            dwg_no="CRS-DWG-105", title="CrossSafe panel rail (make 2, a left and a right): making sketch",
            material="Aluminium equal angle 40 x 40 x 4 mm, 6063 class", view_shape=vs, inset_view=(-25, 30),
            notes=["Cut two 360 mm lengths of 40 x 40 x 4 angle; square and deburr.",
                   "Flat leg (goes on the back of the panel frame): two 6.5 mm holes,",
                   "  10 mm from each end, 20 mm out from the upright leg's outer face.",
                   "Upright leg: two 10.5 mm holes, 22 mm out from the flat leg's",
                   "  outer face: the pivot at mid-length (180 mm from each end) and",
                   "  the tilt bolt 60 mm from the pivot toward the panel's low edge.",
                   "Left and right rails are mirror images: drill the upright legs",
                   "  clamped back to back so the holes line up.",
                   "Fit: the flat legs bolt across the frame's back lip at its two long",
                   "  edges, 61 to 101 mm each side of the panel's centre line; the",
                   "  upright legs stand down and bolt to the outside of the cheeks.",
                   "Check: hole centres 60 and 340 mm apart, within 0.5 mm."],
            **base))

    # 106 keyed pole saddle
    if want(106):
        loc = saddle_local(R, P)
        sad = loc["saddle"]
        nb = [part("Pole", rod((0, 0, -60), (0, 0, 60), R) - rod((0, 0, -61), (0, 0, 61), R - P["post_wall"]), COL["pole"]),
              part("Band", loc["band"] + loc["buckle"], COL["band"])]
        out.append(bv.component_sheet(
            Part("Keyed pole saddle", sad, COL["saddle"]), nb,
            dwg_no="CRS-DWG-106", title="CrossSafe keyed pole saddle (make 8, all the same): making sketch",
            material="Aluminium flat bar 80 x 40 mm, 6082 class", view_shape=b.Pos(-(sg["xb"] + sg["xf"]) / 2, 0, 0) * sad,
            inset_view=(35, -40),
            notes=["Saw 60 mm slices off 80 x 40 mm bar: blocks 80 wide x 40 deep x",
                   "  60 tall. The 80 x 60 face without the V is the front.",
                   "V: 120 degrees, centred, 70 mm wide at the back face, its point",
                   "  20.2 mm in from the back. Saw inside the lines, file to them.",
                   "Key the V: hacksaw cuts 1 mm deep, 3 mm apart, running the full",
                   "  60 mm height on both V faces. The ridges grip the pole.",
                   "Front: a groove 21 mm wide and 1 mm deep across the full width,",
                   "  centred on the height, for the band. Mill or file it flat.",
                   "Front: two M8 holes on the centre line, 20 mm above and below the",
                   "  middle: drill 6.8 mm 18 deep, tap 14 deep.",
                   "Fit: the pole sits in the V touching both faces (6 mm in from the",
                   "  back corners on 114 mm, 20 mm on 60 mm); the band runs round the",
                   "  pole and across the saddle's front in the groove.",
                   "Check: on a 114 mm tube the block must not rock."],
            **base))

    # 107 radar arm
    if want(107):
        arm = C["radar_arm"]
        abb = arm.bounding_box()
        out.append(bv.component_sheet(
            Part("Radar arm", arm, COL["arm"]),
            [part("Saddle", C["saddle_radar"], COL["saddle"]), M["radar"], M["pir"], stub(2450, 2700),
             part("Band", C["band_radar"], COL["band"])],
            dwg_no="CRS-DWG-107", title="CrossSafe radar arm: making sketch", material="Aluminium flat bar 40 x 5 mm, 6082 class",
            view_shape=b.Rot(0, 0, -90) * b.Pos(0, -abb.center().Y, -abb.center().Z) * arm, inset_view=(22, -30),
            notes=["Cut 320 mm of 40 x 5 mm bar. Bend 90 degrees the easy way (across",
                   "  the 5 mm) in a vice with a radius block, to an L: long leg 251 mm",
                   "  and short leg 70 mm, outside sizes. The short leg stands up.",
                   "Short leg: two 9 mm holes on the centre line, 20 and 60 mm up",
                   "  from the long leg's underside.",
                   "Long leg, measured from its far end: a 12 mm hole for the PIR's",
                   "  neck on the centre line 40 mm in; two 4.5 mm holes for the",
                   "  radar's screws, 15 and 65 mm in.",
                   "Fit: the short leg bolts flat on its saddle with two M8 bolts; the",
                   "  long leg points at the kerb, the radar sits on top of its far end",
                   "  and the PIR hangs underneath.",
                   "Check: the legs are square and the long leg is level when fitted."],
            **base))

    # 108 panel bracket (welded)
    if want(108):
        br = C["bracket"]
        out.append(bv.component_sheet(
            Part("Panel bracket", br, COL["bracket"]), [M["rails"], M["panel"], stub(3400, 3700)],
            dwg_no="CRS-DWG-108", title="CrossSafe panel bracket: making sketch",
            material="Steel tube 139.7 x 4 mm, plate 6 mm, S235; galvanized or painted",
            view_shape=b.Pos(0, 0, -P["post_h"]) * br, inset_view=(20, -60),
            notes=["Socket: 120 mm of 139.7 x 4 mm tube. Three 10.5 mm holes 60 mm",
                   "  below its top, 120 degrees apart, one toward the kerb; weld an",
                   "  M10 nut over each.",
                   "Cap: 140 x 140 x 6 mm plate, welded on top of the socket all round.",
                   "Cheeks: two from 6 mm plate, 96 mm wide, cut to the outline in the",
                   "  right view (top edge sloped at 30 degrees), standing on the cap",
                   "  with their inside faces 110 mm apart; weld both sides.",
                   "Each cheek: a 10.5 mm pivot hole, and a tilt slot 10.5 mm wide on a",
                   "  60 mm radius round the pivot, 20 degrees long (chain drill, file).",
                   "Clean the welds; galvanize or prime and paint.",
                   "Fit: the socket slides over the post top until the cap sits on it;",
                   "  three M10 set screws centre and lock it. The rails bolt to the",
                   "  outside of the cheeks.",
                   "Check: the cheeks are parallel and square to the cap."],
            **base))

    # 109 sun shield
    if want(109):
        sh = C["shield"]
        sbb = sh.bounding_box()
        out.append(bv.component_sheet(
            Part("Sun shield", sh, "#E7E5E4"), [M["encplate"], M["body"], M["lid"], M["pens"]],
            dwg_no="CRS-DWG-109", title="CrossSafe sun shield: making sketch", material="White powder-coated aluminium sheet 2 mm",
            view_shape=b.Rot(0, 0, 90) * b.Pos(-sbb.center().X, 0, -sbb.center().Z) * sh, inset_view=(22, -140),
            notes=["One blank, folded: a back 314 x 327 mm in the middle, a side 177 mm",
                   "  deep on each long edge, a roof 177 mm deep on the top edge,",
                   "  and a 15 mm flange on the free edge of each side (300 mm long,",
                   "  starting at the bottom), with corner tabs on the roof.",
                   "Cut with snips; drill 3 mm relief holes where bend lines cross.",
                   "Fold the sides and roof 90 degrees forward, the tabs down over the",
                   "  sides (rivet, two 3.2 mm rivets each), the flanges 90 degrees out.",
                   "Flanges: two 5.5 mm holes each, 7.5 mm from the fold, 50 and",
                   "  250 mm up from the bottom edge.",
                   "Roof: a 22 mm hole 75 mm back from its front edge, 90 mm toward",
                   "  the kerb side, for the antenna.",
                   "Fit: flanges flat on the mounting plate; four M5 security screws.",
                   "  25 mm air gap at the back, sides and roof; open at the bottom.",
                   "Check: the gap is 25 mm, plus or minus 3, all round."],
            **base))
    return out


# ----------------------------------------------------------------- joints
def joints(only=None):
    out = []
    zb = D["bar_zc"]

    def want(n):
        return only is None or n in only
    pc = lambda z0, z1: pole_context(P, z0, z1)  # noqa: E731

    # 01 LED head in the light bar wall, cut through the head centres
    if want(1):
        bx_ = (XF - 40, XF + 110, 110, 215, zb - 70, zb + 70)
        out.append(bv.joint([
            part("Light bar channel", win(C["bar_channel"], *bx_), COL["bar"]),
            part("Bottom cover", win(C["bar_cover"], *bx_), COL["cover"]),
            part("LED head, traffic face", win(split(G("heads", "head_bezels", "head_visors"), x_min=XF + 35), *bx_), COL["heads"]),
            part("LED head, far face", win(split(G("heads", "head_bezels", "head_visors"), x_max=XF + 35), *bx_), "#D97706")],
            OUT / "joint-01.png", "Joint 1: LED heads, bezels and visors on the light bar walls (cut through two heads)",
            subtitle="Each head's flange sits on its wall over the 128 x 50 mm cut-out, four M4 screws; bezel and visor come fitted",
            elev=18, azim=62, size=(8, 6)))
    # 02 light bar on its saddle, cut on the centre line
    if want(2):
        bx_ = (25, XF + 75, -70, 0, zb - 75, zb + 75)
        out.append(bv.joint([
            part("Pole", win(pc(1900, 2400), *bx_), COL["pole"]),
            part("Keyed saddle", win(C["saddle_bar"], *bx_), COL["saddle"]),
            part("Band in its groove", win(C["band_bar"], *bx_), COL["band"]),
            part("Light bar back wall", win(C["bar_channel"], *bx_), COL["bar"]),
            part("Bottom cover (off to reach the bolts)", win(C["bar_cover"], *bx_), COL["cover"]),
            part("Two M8 bolts from inside", win(C["bar_bolts"], *bx_), COL["bolt"])],
            OUT / "joint-02.png", "Joint 2: light bar on its saddle (cut on the centre line)",
            subtitle="The back wall sits flat on the saddle's front and covers the band; two M8 bolts go in from inside the bar",
            elev=8, azim=88, size=(8, 6)))
    # 03 enclosure bottom face from below
    if want(3):
        exc = D["enc_xc"]
        bx_ = (EB - 160, EB + 5, -140, 140, D["enc_bot"] - 30, D["enc_bot"] + 14)
        out.append(bv.joint([
            part("Enclosure bottom", win(C["enc_body"], *bx_), COL["body"]),
            part("M20 cable glands (4)", win(C["glands"], *bx_), COL["pens"]),
            part("Membrane vent", win(C["vent"], *bx_), "#64748B"),
            part("Mounting plate", win(C["enc_plate"], *bx_), COL["encplate"])],
            OUT / "joint-03.png", "Joint 3: the enclosure's bottom face, seen from below",
            subtitle="Glands in two rows each side of the battery; the vent at the lid end. Each goes in from below, nut inside",
            elev=-50, azim=-120, size=(8, 6)))
    # 04 internal plate, battery and strap, cut on the centre line
    if want(4):
        fin = D["enc_bot"] + P["enc_wall"]
        bx_ = (EB - 152, EB + 6, 0, 135, D["enc_bot"] - 2, fin + 170)
        out.append(bv.joint([
            part("Enclosure body", win(C["enc_body"], *bx_), COL["body"]),
            part("Mounting plate", win(C["enc_plate"], *bx_), COL["encplate"]),
            part("Internal plate on its bosses", win(C["mplate"], *bx_), COL["mplate"]),
            part("Battery", win(C["battery"], *bx_), COL["battery"]),
            part("Battery strap, two M4 screws", win(C["strap"], *bx_), COL["strap"]),
            part("Fuse block", win(C["fuse_block"], *bx_), COL["fuse"])],
            OUT / "joint-04.png", "Joint 4: battery, strap and internal plate (enclosure cut on the centre line)",
            subtitle="The battery stands on the floor against the internal plate; the strap holds it down and in",
            elev=12, azim=-105, size=(8, 6)))
    # 05 lug on the mounting plate (upper kerb-side corner)
    if want(5):
        bx_ = (EB - 40, -XF + 8, 100, 185, D["enc_top"] - 45, D["enc_top"] + 10)
        out.append(bv.joint([
            part("Mounting plate", win(C["enc_plate"], *bx_), COL["encplate"]),
            part("Enclosure body", win(C["enc_body"], *bx_), COL["body"]),
            part("Lug (maker's kit)", win(C["lugs"], *bx_), COL["lugs"]),
            part("M5 screw, nyloc nut behind", win(C["lug_screws"], *bx_), COL["bolt"])],
            OUT / "joint-05.png", "Joint 5: enclosure lug on the mounting plate (upper corner, kerb side)",
            subtitle="The box back sits flat on the plate; each lug lies on the plate and takes one M5 screw",
            elev=20, azim=150, size=(8, 6)))
    # 06 saddle and band on the pole, seen from above, cut through the band
    if want(6):
        z = ST["sign_low"][1]
        bx_ = (-75, 100, -90, 90, z - 6, z + 3)
        out.append(bv.joint([
            part("Pole", win(pc(z - 100, z + 100), *bx_), COL["pole"]),
            part("Keyed saddle", win(C["saddle_sign_low"], *bx_), COL["saddle"]),
            part("Band and buckle", win(C["band_sign_low"], *bx_), COL["band"]),
            part("Sign", win(C["sign"], *bx_), COL["sign"])],
            OUT / "joint-06.png", "Joint 6: keyed saddle, pole and band, seen from above (cut through the band)",
            subtitle="The pole touches both faces of the V; the band runs round the pole and across the saddle's front, in its groove",
            elev=78, azim=-90, size=(8, 6)))
    # 07 sign on its saddle, cut on the centre line
    if want(7):
        z = ST["sign_low"][1]
        bx_ = (25, XF + 12, -60, 0, z - 50, z + 50)
        out.append(bv.joint([
            part("Pole", win(pc(z - 150, z + 150), *bx_), COL["pole"]),
            part("Keyed saddle", win(C["saddle_sign_low"], *bx_), COL["saddle"]),
            part("Band in its groove", win(C["band_sign_low"], *bx_), COL["band"]),
            part("Sign", win(C["sign"], *bx_), COL["sign"]),
            part("Two M8 security bolts", win(C["sign_bolts"], *bx_), COL["bolt"])],
            OUT / "joint-07.png", "Joint 7: sign on its lower saddle (cut on the centre line)",
            subtitle="The sign lies flat on the saddle's front over the band; two M8 bolts through the sign into the saddle",
            elev=8, azim=88, size=(8, 6)))
    # 08 radar arm on its saddle, with the radar and PIR
    if want(8):
        bx_ = (-60, 60, 20, 345, D["pir_bot"] - 5, D["arm_top"] + 90)
        out.append(bv.joint([
            part("Pole", win(pc(2450, 2700), *bx_), COL["pole"]),
            part("Keyed saddle", win(C["saddle_radar"], *bx_), COL["saddle"]),
            part("Band", win(C["band_radar"], *bx_), COL["band"]),
            part("Radar arm", win(C["radar_arm"], *bx_), COL["arm"]),
            part("Two M8 bolts", win(C["arm_bolts"], *bx_), COL["bolt"]),
            part("Radar on top", win(C["radar"], *bx_), COL["radar"]),
            part("PIR underneath", win(C["pir"], *bx_), COL["pir"])],
            OUT / "joint-08.png", "Joint 8: radar arm on its saddle, with the radar and PIR",
            subtitle="The short leg bolts flat on the saddle; the long leg carries the radar on top and the PIR below",
            elev=30, azim=-20, size=(8, 6)))
    # 09 mounting plate tab on the upper enclosure saddle, cut on the centre line
    if want(9):
        z = ST["enc_up"][1]
        bx_ = (-XF - 14, -25, 0, 70, D["enc_top"] - 10, z + 40)
        out.append(bv.joint([
            part("Pole", win(pc(3000, 3400), *bx_), COL["pole"]),
            part("Keyed saddle", win(C["saddle_enc_up"], *bx_), COL["saddle"]),
            part("Band in its groove", win(C["band_enc_up"], *bx_), COL["band"]),
            part("Mounting plate tab", win(C["enc_plate"], *bx_), COL["encplate"]),
            part("Two M8 bolts from the front", win(C["enc_plate_bolts"], *bx_), COL["bolt"]),
            part("Sun shield roof", win(C["shield"], *bx_), "#D6D3D1"),
            part("Enclosure", win(C["enc_body"], *bx_), COL["body"])],
            OUT / "joint-09.png", "Joint 9: mounting plate tab on the upper enclosure saddle (cut on the centre line)",
            subtitle="Both bolts sit above the shield roof, so the enclosure can be lifted on and off as one unit",
            elev=8, azim=-92, size=(8, 6)))
    # 10 socket on the post top, cut through one set screw (turned so that screw points at the viewer's right)
    if want(10):
        zt = P["post_h"]
        T = b.Rot(0, 0, -90)
        bx_ = (-80, 95, -90, 0, zt - 130, zt + 30)
        out.append(bv.joint([
            part("Pole top", win(T * pc(zt - 300, zt), *bx_), "#E7E5E4"),
            part("Socket, cap and cheeks (welded)", win(T * C["bracket"], *bx_), "#78716C"),
            part("M10 set screw in its welded nut", win(T * C["set_screws"], *bx_), COL["bolt"])],
            OUT / "joint-10.png", "Joint 10: panel bracket socket on the post top (cut through a set screw)",
            subtitle="The cap sits on the pole's top edge; three set screws close the 8.7 mm gap and lock the socket",
            elev=15, azim=70, size=(8, 6)))
    # 11 rail on the cheek: pivot and tilt slot, seen from inside the bracket
    if want(11):
        bx_ = (40, 110, -80, 60, P["post_h"] + 120, D["panel_zc"] + 30)
        out.append(bv.joint([
            part("Cheek (panel bracket)", win(C["bracket"], *bx_), COL["bracket"]),
            part("Panel rail", win(C["rails"], *bx_), COL["rails"]),
            part("Pivot and tilt bolts, nuts inside", win(C["panel_bolts"], *bx_), COL["bolt"]),
            part("Solar panel", win(C["panel"], *bx_), COL["panel"])],
            OUT / "joint-11.png", "Joint 11: panel rail on its cheek, seen from inside the bracket",
            subtitle="Pivot bolt at the top; the tilt bolt runs in the slot, 20 to 40 degrees. The rail's flat leg bolts to the panel frame",
            elev=18, azim=55, size=(8, 6)))
    # 12 shield flange on the mounting plate
    if want(12):
        zz = P["enc_z"] + 100
        bx_ = (EB - 30, -XF + 2, 128, 180, zz - 40, zz + 40)
        out.append(bv.joint([
            part("Mounting plate", win(C["enc_plate"], *bx_), COL["encplate"]),
            part("Enclosure body", win(C["enc_body"], *bx_), COL["body"]),
            part("Sun shield side and flange", win(C["shield"], *bx_), "#D6D3D1"),
            part("M5 security screw", win(C["shield_screws"], *bx_), COL["bolt"])],
            OUT / "joint-12.png", "Joint 12: sun shield flange on the mounting plate (kerb side, upper screw)",
            subtitle="The flange folds out from the side sheet and lies flat on the plate; 25 mm air gap to the box",
            elev=20, azim=150, size=(8, 6)))
    # 13 new posts: the anti-rotation bolt
    if want(13):
        CV = {k: v[0] for k, v in build_components(P, own_post=True).items()}
        z = ST["sign_up"][1]
        bx_ = (-R - 20, XF + 14, -60, 0, z - 40, z + 45)
        out.append(bv.joint([
            part("New post", win(CV["post"], *bx_), COL["pole"]),
            part("Upper keyed saddle", win(CV["saddle_sign_up"], *bx_), COL["saddle"]),
            part("Band", win(CV["band_sign_up"], *bx_), COL["band"]),
            part("Sign", win(CV["sign"], *bx_), COL["sign"]),
            part("M10 anti-rotation bolt and nut", win(CV["arb"], *bx_), COL["bolt"]),
            part("M8 sign bolt", win(CV["sign_bolts"], *bx_), "#374151")],
            OUT / "joint-13.png", "Joint 13 (new posts only): the anti-rotation bolt (cut on the centre line)",
            subtitle="On a new post the saddle's upper hole is drilled through: one M10 bolt passes the sign, saddle and both post walls",
            elev=12, azim=60, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    out = []

    def want(n):
        return only is None or n in only

    def st(n, done, new, title, sub, **kw):
        if want(n):
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)
    M = made()
    zb = D["bar_zc"]
    HV = G("heads", "head_bezels", "head_visors")
    front = split(HV, x_min=XF + 35)
    back = split(HV, x_max=XF + 35)
    st(1, [part("Channel and end caps", G("bar_channel", "bar_caps"), COL["bar"])],
       [mv(part("Heads, traffic face", front, COL["heads"]), (120, 0, 0)), mv(part("Heads, far face", back, "#D97706"), (-120, 0, 0)),
        mv(part("Pilot light", C["pilot"], COL["pilot"]), (0, 90, 0))],
       "LED heads and pilot light into the light bar",
       "End caps first; each head (bezel and visor fitted) through its cut-out, four M4 screws; pilot light in the kerb end",
       elev=22, azim=-50, label_done=True, size=(9, 5.5))
    st(2, [part("Light bar", G("bar_channel", "bar_caps", "heads", "head_bezels", "head_visors", "pilot"), COL["bar"])],
       [mv(part("Bottom cover with cable gland", G("bar_cover", "bar_gland"), COL["cover"]), (0, 0, -90))],
       "close the light bar",
       "Lead the head and pilot wires out through the gland; gasket on the lips; cover on with M4 screws (it comes off again in step 9)",
       elev=-28, azim=-50, label_done=True, size=(9, 5.5))
    st(3, [part("Enclosure body", C["enc_body"], COL["body"])],
       [mv(part("Cable glands (4)", C["glands"], COL["pens"]), (0, 0, -90)), mv(part("Membrane vent", C["vent"], "#64748B"), (0, 0, -60)),
        mv(part("Antenna", C["antenna"], COL["antenna"]), (0, 0, 120))],
       "glands, vent and antenna into the enclosure",
       "Each from outside with its seal outside and its nut inside, to the maker's torque; blanking plugs in unused glands",
       elev=-18, azim=-130, label_done=True)
    st(4, [part("Internal plate", C["mplate"], COL["mplate"])],
       [mv(part("Charger", C["mppt"], COL["mppt"]), (-60, 0, 0)), mv(part("Controller and radio board", C["board"], COL["board"]), (-60, 0, 0)),
        mv(part("Fuse block (fuse out)", C["fuse_block"], COL["fuse"]), (-60, 0, 0)),
        mv(part("Battery strap", C["strap"], COL["strap"]), (-120, 0, -60))],
       "build the internal plate",
       "Modules on M3 screws and 6 mm nylon stand-offs; strap on two M4 screws; wire as the wiring diagram. No battery yet",
       elev=32, azim=-120, label_done=True)
    inside = part("Internal plate with modules and strap", G("mplate", "mppt", "board", "fuse_block", "strap"), COL["mplate"])
    st(5, [part("Enclosure body", G("enc_body", "glands", "vent", "antenna"), COL["body"])], [mv(inside, (-200, 0, 0))],
       "internal plate into the enclosure",
       "In through the open lid face; four M4 screws into the bosses. Plug the antenna lead to the board",
       elev=18, azim=-135, label_done=True)
    box_ = G("enc_body", "glands", "vent", "antenna", "mplate", "mppt", "board", "fuse_block", "strap")
    st(6, [part("Mounting plate", C["enc_plate"], COL["encplate"])],
       [mv(part("Enclosure with lugs", G("enc_body", "glands", "vent", "antenna", "mplate", "mppt", "board", "fuse_block", "strap", "lugs"), COL["body"]), (-160, 0, 0)),
        mv(part("Four M5 screws, nyloc nuts behind", C["lug_screws"], COL["bolt"]), (-60, 0, 0))],
       "enclosure onto the mounting plate",
       "Lugs on the box's back corners; box back flat on the plate; M5 screws from the front, nyloc nuts behind",
       elev=18, azim=-135, label_done=True)
    F = b.Pos(0, 0, D["panel_zc"]) * b.Rot(P["panel_tilt"], 0, 0)
    t = math.radians(P["panel_tilt"])
    down = (0, 80 * math.sin(t), -80 * math.cos(t))
    st(7, [part("Solar panel, seen from below", C["panel"], COL["panel"])],
       [mv(part("Panel rails, flat legs on the frame lip", C["rails"], COL["rails"]), down)],
       "rails onto the panel",
       "Panel face down on a soft cloth; drill the frame's back lip through each rail; two M6 bolts per rail, nuts inside the frame",
       elev=-40, azim=-120, label_done=True)
    # on the post
    labels8 = {"button": "Button saddle, 1,050", "plate": "Plate saddle, 1,300", "bar": "Light bar saddle, 2,165",
               "sign_low": "Lower sign saddle, 2,530", "radar": "Radar arm saddle, 2,595", "enc_low": "Lower enclosure saddle, 2,790",
               "sign_up": "Upper sign saddle, 3,030", "enc_up": "Upper enclosure saddle, 3,210"}
    new8 = []
    for n, (ang, _z) in ST.items():
        a_ = math.radians(ang)
        new8.append(mv(part(labels8[n], C[f"saddle_{n}"], COL["saddle"]), (110 * math.cos(a_), 110 * math.sin(a_), 0)))
    new8.append(part("Bands (8), buckles behind the pole", bands(ST), COL["band"]))
    st(8, [pole(950, 3300)], new8,
       "saddles and bands onto the post",
       "Heights in Table 2 of the plan (mm above the sidewalk). Band round the pole and across the saddle's front in its groove; snug",
       elev=12, azim=-35, label_done=False, size=(8, 10))
    near = lambda names: [part("Saddles and bands", b.Compound(children=[C[f"saddle_{n}"] for n in names] + [C[f"band_{n}"] for n in names]), COL["saddle"])]  # noqa: E731
    bar_all = part("Light bar", G("bar_channel", "bar_caps", "bar_cover", "heads", "head_bezels", "head_visors", "pilot", "bar_gland"), COL["bar"])
    st(9, [pole(1950, 2450)] + near(["bar"]), [mv(bar_all, (220, 0, 0))],
       "light bar onto its saddle",
       "Cover off; back wall flat on the saddle; two M8 bolts from inside; cover back on. The bar is level and square to the road",
       elev=15, azim=-40, label_done=True)
    bar_done = part("Light bar", bar_all.shape, "#9CA3AF")
    st(10, [pole(1950, 3500), bar_done] + near(["bar", "sign_low", "sign_up"]),
       [mv(part("Sign with four M8 security bolts", G("sign", "sign_bolts"), COL["sign"]), (300, 0, 0))],
       "sign onto its two saddles",
       "Two M8 bolts into each saddle through the sign; check the sign is upright, then tighten both bands",
       elev=12, azim=-35, label_done=False, size=(8, 7))
    st(11, [pole(850, 1550)] + near(["button", "plate"]),
       [mv(part("Push-button station", C["button"], COL["button"]), (0, 200, -70)),
        mv(part("Instruction plate, two M8 bolts", G("inst_plate", "plate_bolts"), COL["plate"]), (0, 200, 70))],
       "push-button station and instruction plate",
       "Station on its saddle with its own two bolts; plate on the saddle above; button centre 1,050 mm above the walking surface",
       elev=15, azim=-30, label_done=True, size=(8, 6.5))
    st(12, [pole(2400, 2750)] + near(["radar"]),
       [mv(part("Radar arm, two M8 bolts", G("radar_arm", "arm_bolts"), COL["arm"]), (0, 200, 0)),
        mv(part("Radar (screwed on at the bench)", C["radar"], COL["radar"]), (0, 200, 150)),
        mv(part("PIR sensor", C["pir"], COL["pir"]), (0, 200, -150))],
       "radar arm, radar and PIR",
       "Radar and PIR fitted to the arm on the bench; short leg flat on the saddle, two M8 bolts; long leg level, toward the kerb",
       elev=24, azim=-60, label_done=True)
    unit = part("Enclosure unit (plate, lugs, enclosure)", G("enc_plate", "lugs", "lug_screws", "enc_body", "glands", "vent", "antenna",
                                                           "mplate", "mppt", "board", "fuse_block", "strap"), COL["body"])
    st(13, [pole(2650, 3350)] + near(["enc_low", "enc_up"]),
       [mv(unit, (-220, 0, 0)), mv(part("Four M8 bolts", C["enc_plate_bolts"], COL["bolt"]), (-120, 0, 0))],
       "enclosure unit onto its saddles",
       "Two people: hold the plate tabs flat on the saddles, two M8 bolts into each. Lid still off, battery not fitted",
       elev=15, azim=-140, label_done=True)
    st(14, [pole(3350, P["post_h"])],
       [mv(part("Panel bracket", C["bracket"], COL["bracket"]), (0, 0, 180)),
        mv(part("Three M10 set screws", C["set_screws"], COL["bolt"]), (0, 0, 180))],
       "panel bracket onto the post top",
       "Slide the socket down until the cap sits on the pole; turn the cheeks square to the road; tighten the three set screws evenly",
       elev=18, azim=-50, label_done=True)
    up = (0, -220 * math.sin(t), 220 * math.cos(t))
    st(15, [pole(3350, P["post_h"]), part("Panel bracket", C["bracket"], COL["bracket"])],
       [mv(part("Panel with rails", G("panel", "rails", "panel_bolts"), COL["panel"]), up)],
       "panel onto the bracket",
       "Rails outside the cheeks; pivot bolt first, then the tilt bolt in its slot; set 30 degrees with an angle finder, tighten",
       elev=6, azim=-12, label_done=True)
    stubs = []
    for k, (dx, yy) in {"1": (40.0, 105.0), "2": (100.0, 105.0), "3": (40.0, -105.0), "4": (100.0, -105.0)}.items():
        x = EB - dx
        stubs.append(rod((x, yy, D["enc_bot"] - 170), (x, yy, D["enc_bot"] - 22), 4.0))
    st(16, [unit, pole(2600, 3300)] + near(["enc_low", "enc_up"]),
       [mv(part("Cables from the bar, button, radar and panel", b.Compound(children=stubs), "#B91C1C"), (0, 0, -120)),
        part("Glands (fitted in step 3)", C["glands"], COL["pens"])],
       "cables into the enclosure",
       "Each cable up the pole under the cable cover and in through its gland; tighten the gland caps. Wire as the wiring diagram",
       elev=-20, azim=-135, label_done=False)
    st(17, [part("Enclosure unit, lid off", G("enc_plate", "lugs", "enc_body", "glands", "vent", "antenna", "mplate", "mppt", "board", "fuse_block"), COL["body"])],
       [mv(part("Battery", C["battery"], COL["battery"]), (-200, 0, 0)), mv(part("Battery strap", C["strap"], COL["strap"]), (-120, 0, 60)),
        mv(part("Lid", C["lid"], COL["lid"]), (-330, 0, 0))],
       "battery in, lid on",
       "Only after safety stops S1 to S4. Battery on the floor against the plate; strap on; leads to the fuse block; fuse in; lid on",
       elev=15, azim=-140, label_done=False)
    unit_lid = part("Enclosure unit, lid on (plate, lugs, enclosure)", b.Compound(children=[unit.shape, C["lid"]]), COL["body"])
    st(18, [unit_lid, pole(2650, 3350)] + near(["enc_low", "enc_up"]),
       [mv(part("Sun shield (white; drawn in colour here)", G("shield", "shield_screws"), "#F59E0B"), (-40, 0, 470))],
       "sun shield onto the mounting plate",
       "Lower it over the enclosure, the antenna through its roof hole; flanges flat on the plate; four M5 security screws",
       elev=20, azim=70, label_done=True)
    return out


# ----------------------------------------------------------------- drilling layouts
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    res = []
    # mounting plate, seen from the front (the face the enclosure sits on)
    pw, ph, pt = P["enc_plate"]
    tw, th = P["tab"]
    z0 = P["enc_z"] - ph / 2 - th
    fig = plt.figure(figsize=(9.5, 11), dpi=150)
    ax = fig.add_axes([0.08, 0.06, 0.6, 0.86]); ax.set_aspect("equal"); ax.set_axis_off()
    outline = [(-tw / 2, 0), (tw / 2, 0), (tw / 2, th), (pw / 2, th), (pw / 2, th + ph), (tw / 2, th + ph), (tw / 2, 2 * th + ph),
               (-tw / 2, 2 * th + ph), (-tw / 2, th + ph), (-pw / 2, th + ph), (-pw / 2, th), (-tw / 2, th), (-tw / 2, 0)]
    xs_, ys_ = zip(*outline)
    ax.fill(xs_, ys_, fc="#F5F5F4", ec=INK, lw=1.2)
    ax.axvline(0, color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    holes = []
    for k in ("enc_low", "enc_up"):
        for dz in (-P["bolt_dz"], P["bolt_dz"]):
            holes.append((0.0, ST[k][1] + dz - z0, 9.0, "saddle"))
    lug_y = P["enc"][1] / 2 + 12
    for sy in (-1, 1):
        for zz in (D["enc_bot"] + 10, D["enc_top"] - 10):
            holes.append((sy * lug_y, zz - z0, 5.5, "lug"))
        for zz in (P["enc_z"] - 100, P["enc_z"] + 100):
            holes.append((sy * (P["enc"][1] / 2 + P["shield_gap"] + P["shield_t"] + P["shield_flange"] / 2), zz - z0, 4.2, "shield"))
    xs, zs = set(), set()
    for x, z, d, kind in holes:
        ax.add_patch(Circle((x, z), d / 2 * 1.6, fc="white", ec=INK, lw=1))
        ax.plot([x - d, x + d], [z, z], color=MUT, lw=0.4); ax.plot([x, x], [z - d, z + d], color=MUT, lw=0.4)
        if x > 0.5:
            xs.add(round(x, 1))
        zs.add(round(z, 1))
    ax.add_patch(Rectangle((-P["enc"][1] / 2, th), P["enc"][1], ph, fc="none", ec=AC, lw=0.8, ls="--"))
    ax.text(0, th + ph / 2 + 60, "enclosure outline", ha="center", fontsize=8, color=AC, bbox=dict(boxstyle="round,pad=0.2", fc="#F5F5F4", ec="none"), zorder=4)
    for i, x in enumerate(sorted(xs)):
        ax.plot([x, x], [0, -12 - 9 * (i % 2)], color=AC, lw=0.4, ls=":")
        ax.text(x, -14 - 9 * (i % 2), f"{x:g}", ha="center", va="top", fontsize=7.5, color=AC)
    ax.text(0, -46, "sideways from the centre line, mm (same each side)", ha="center", fontsize=8, color=MUT, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"), zorder=4)
    for i, z in enumerate(sorted(zs)):
        xl = -pw / 2 - 10 - 26 * (i % 2)
        ax.plot([xl + 2, -pw / 2 if th < z < th + ph else -tw / 2], [z, z], color=AC, lw=0.4, ls=":")
        ax.text(xl, z, f"{z:g}", ha="right", va="center", fontsize=7.5, color=AC)
    ax.text(-pw / 2 - 66, th + ph / 2, "up from the bottom edge of the lower tab, mm", rotation=90, ha="center", va="center", fontsize=8, color=MUT)
    ax.set_xlim(-pw / 2 - 75, pw / 2 + 10); ax.set_ylim(-52, 2 * th + ph + 10)
    fig.text(0.04, 0.975, "Enclosure mounting plate: hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.04, 0.95, "Seen from the front (the face the enclosure sits on). Full size figures in mm, taken from the model.", fontsize=8.5, color=MUT, va="top")
    key = ["Saddle bolts: 9 mm, on the", "  centre line, two in each tab", "Lug screws: 5.5 mm, at 142", "Shield screws: drill 4.2 mm,",
           "  tap M5, at 164.5", "", "Dashed: where the enclosure", "  sits (350 x 300 mm plate,", "  90 x 90 mm tabs)"]
    fig.text(0.71, 0.86, "What each hole is (mm)", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, tx in enumerate(key):
        fig.text(0.71, 0.83 - i * 0.022, tx, fontsize=8, color=INK, va="top")
    fig.text(0.04, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.96, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "plate-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "plate-holes.png")

    # enclosure bottom face, seen from below, back face at the top of the page
    ex, ey, ez = P["enc"]
    fig = plt.figure(figsize=(11, 7.2), dpi=150)
    ax = fig.add_axes([0.05, 0.1, 0.9, 0.74]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((-ey / 2, 0), ey, ex - P["lid_t"], fc="#F3F4F6", ec=INK, lw=1.2))
    ax.add_patch(Rectangle((-ey / 2, ex - P["lid_t"]), ey, P["lid_t"], fc="white", ec=MUT, lw=0.8, ls="--"))
    ax.text(0, -6, "back face (goes against the mounting plate), toward you", ha="center", va="bottom", fontsize=8, color=MUT, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"), zorder=4)
    ax.text(0, ex + 4, "lid end (do not drill the lid)", ha="center", va="top", fontsize=7.5, color=MUT, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"), zorder=4)
    ax.axvline(0, ymin=0.05, ymax=0.95, color=MUT, lw=0.6, ls=(0, (8, 3, 2, 3)))
    bx_, by_, _ = P["battery"]
    so = P["enc_wall"] + P["boss_h"] + P["mplate"][2]
    ax.add_patch(Rectangle((-by_ / 2, so), by_, bx_, fc="none", ec="#C2410C", lw=0.8, ls="--"))
    ax.text(0, so + bx_ / 2, "battery footprint\n(inside, on the floor)", ha="center", va="center", fontsize=7.5, color="#C2410C", bbox=dict(boxstyle="round,pad=0.2", fc="#F3F4F6", ec="none"), zorder=4)
    pens = [("Gland 1, panel", 40.0, 105.0, 20.0, 28.0), ("Gland 2, light bar", 100.0, 105.0, 20.0, 28.0),
            ("Gland 3, button", 40.0, -105.0, 20.0, 28.0), ("Gland 4, radar and PIR", 100.0, -105.0, 20.0, 28.0),
            ("Vent", 130.0, 0.0, 12.0, 20.0)]
    for name, dx, yy, d, df in pens:
        # seen from below with the back face toward you, the kerb side (+Y) is on the left
        x = -yy
        ax.add_patch(Circle((x, dx), df / 2, fc="none", ec=MUT, lw=0.6, ls="--"))
        ax.add_patch(Circle((x, dx), d / 2, fc="white", ec=INK, lw=1.1))
        sg = 1 if x >= 0 else -1
        xt = sg * (ey / 2 + 6)
        ax.plot([x + sg * df / 2, xt - sg * 1], [dx, dx], color=MUT, lw=0.6, zorder=1)
        ax.text(xt, dx, f"{name}\n{d:g} hole, {dx:g} from back",
                ha=("left" if sg > 0 else "right"), va="center", fontsize=7.2, color=INK, linespacing=1.2,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"), zorder=4)
    ax.annotate("", xy=(-ey / 2 - 235, 20), xytext=(-ey / 2 - 235, 130), arrowprops=dict(arrowstyle="-", color=AC, lw=1.2))
    ax.text(-ey / 2 - 241, 75, "kerb side", rotation=90, ha="center", va="center", fontsize=8.5, color=AC)
    ax.text(ey / 2 + 241, 75, "road side", rotation=90, ha="center", va="center", fontsize=8.5, color=AC)
    ax.text(0, ex + 14, "glands 105 mm each side of the centre line", ha="center", va="top", fontsize=8, color=AC, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none"), zorder=4)
    ax.set_xlim(-ey / 2 - 250, ey / 2 + 250); ax.set_ylim(-14, ex + 24)
    ax.invert_yaxis()
    fig.text(0.03, 0.97, "Enclosure bottom face: drilling layout", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.93, "Box standing upside down on its roof, back face toward you (at the top of this picture); the kerb side is then on your left.\n"
             "Distances in mm from the back face and the centre line. Solid circle: the hole to drill. Dashed circle: the outside of the gland.", fontsize=8.2, color=MUT, va="top")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, REPO, fontsize=7, color=AC, ha="right", family="monospace")
    fig.savefig(OUT / "base-holes.png", facecolor="white"); plt.close(fig); res.append(OUT / "base-holes.png")
    return res


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.4), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 74); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 72, "CrossSafe prototype: block-level wiring (one assembly)", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 68.6, "Bought modules wired at block level; no circuit board is laid out. Stranded copper; a ferrule on every screw terminal. "
            "All circuits are extra-low voltage (12.8 V battery, about 22 V panel open circuit).", fontsize=8.3, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, REPO, fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((25, 12), 62, 50, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(26.5, 60.8, "Inside the enclosure", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.3, title, ha="center", va="top", fontsize=8.8, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.1, sub, ha="center", va="top", fontsize=7, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7, color=color, ha=ha, va="center", zorder=3, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, RF = "#B91C1C", "#1D4ED8", "#6B7280", "#374151"
    blk(3, 46, 16, 12, "Solar panel", "20 W, about 18 V,\nlead down the pole", "#1E3A8A")
    blk(29, 46, 17, 12, "Charger", "MPPT, LiFePO4\nprofile, cold cut-off", "#16A34A")
    blk(29, 16, 17, 13, "Battery", "12.8 V 12 Ah\nLiFePO4, own BMS", "#C2410C")
    blk(52, 30, 13, 13, "Fuse block", "5 A battery fuse,\n2 A board fuse", "#7C3AED")
    blk(68, 40, 17, 18, "Controller and\nradio board", "\n\nLoRa module, four LED\ndrivers, clock, fault\nLED, 12 V to 3.3 V", "#0F766E")
    blk(68, 16, 17, 10, "Antenna", "bulkhead on the roof", RF)
    blk(98, 50, 19, 9, "Light bar (gland 2)", "4 LED heads, pilot light", "#F59E0B")
    blk(98, 36, 19, 9, "Push button (gland 3)", "button, tone, LED", "#2563EB")
    blk(98, 22, 19, 9, "Radar and PIR (gland 4)", "presence output, wake", "#7C3AED")
    wire([(19, 52), (29, 52)], RED); lab(19.6, 55.4, "PV in, gland 1,\n1.5 mm²\n(16 AWG)", RED)
    wire([(37.5, 46), (37.5, 38), (52, 38)], RED); lab(38.3, 41.5, "charge to the fuse block,\n1.5 mm²", RED)
    wire([(46, 22.5), (58.5, 22.5), (58.5, 30)], RED); lab(47, 25, "battery out,\n1.5 mm²", RED)
    ax.text(48, 19.6, "5 A fuse in the block,\nas near the battery as it goes", fontsize=6.6, color=MUT, va="top")
    wire([(65, 38), (68, 46)], RED); lab(66.4, 35.5, "12 V,\n0.75 mm²", RED)
    wire([(76.5, 40), (76.5, 26)], RF, 1.2); lab(77.2, 33, "RF pigtail", RF)
    wire([(85, 55), (98, 55)], RED); lab(88.4, 57.8, "LED and pilot,\n0.75 mm², 6 cores", RED)
    wire([(85, 49), (95, 49), (95, 40.5), (98, 40.5)], BLU); lab(88.4, 45.8, "0.5 mm²,\n4 cores", BLU)
    wire([(85, 42.5), (89, 42.5), (89, 26.5), (98, 26.5)], BLU); lab(89.8, 33, "0.5 mm²,\n4 cores", BLU)
    wire([(46, 50), (68, 50)], GRY, 1.2); lab(55, 51.8, "charger status, 0.25 mm²", GRY, "center")
    ax.text(26, 9.8, "Safety: the battery fuse stays out, and the battery out of the box, until safety stops S1 to S4 in section 6 are passed.\n"
            "Charge only between 0 and 45 °C cell temperature. The charger and the controller both reach the battery through the 5 A fuse.",
            fontsize=7.4, color="#B45309", fontweight="bold", va="center")
    ax.text(26, 5.6, "Red: power. Blue: signal and low-current supply to the sensors and button. Grey: monitoring. "
            "Cables outside the enclosure run up the pole under the cable cover.", fontsize=7, color=MUT)
    out = OUT / "wiring.png"
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    what = [a for a in args if not a.isdigit()] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    nums = [int(a) for a in args if a.isdigit()] or None
    fns = {"overview": lambda: overview(), "sheets": lambda: sheets(nums), "layouts": layouts, "joints": lambda: joints(nums),
           "steps": lambda: steps(nums), "wiring": wiring}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
