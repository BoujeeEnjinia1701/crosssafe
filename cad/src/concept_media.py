"""CrossSafe concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. The road runs along X, the crossing runs across it along Y, Z is up.
Sidewalk top at Z = 0, road surface at Z = -150. One beacon assembly (the BOM) stands on the
near sidewalk; the matching far-side assembly and the street are grey context in the hero only.
The street is drawn for left-hand traffic so the near-side sign faces the camera; for
right-hand traffic the assemblies mirror.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all, cutaway_parts, _render

PX, PY = 1900.0, -4300.0     # pole axis, 800 mm back from the curb (curb at Y = -3500)
POLE_R, POLE_H = 44.5, 3700.0  # 89 mm x 4 mm post; 76 mm would yield in a 40 m/s gust and 89 mm is still above the 60 % target (CRS-PRC-001)
BAR_Z = 2165.0               # light bar centre; bar bottom at 2.1 m
SIGN_Z = BAR_Z + 65 + 20 + 530  # diamond sign centre, bottom point just above the bar
ENC_Z = 3000.0               # enclosure centre
ENC_X = PX - POLE_R - 80.0   # enclosure behind the pole (away from traffic)


def rod(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def ring(z, h=30):
    return Pos(PX, PY, z) * (Cylinder(POLE_R + 8, h) - Cylinder(POLE_R, h + 2))


# 1 Crossing warning sign, 750 mm diamond, retroreflective, facing approaching traffic (+X)
sign = Pos(PX + 48, PY, SIGN_Z) * Rot(45, 0, 0) * Box(8, 750, 750)

# 2 Light bar housing, double sided, bottom at 2.1 m
bar = Pos(PX + 75, PY, BAR_Z) * Box(70, 720, 130)

# 3 LED indication heads, two per face (127 x 51 mm), both faces
heads = None
for y in (-200, 200):
    for x in (PX + 114, PX + 36):
        h = Pos(x, PY + y, BAR_Z) * Box(8, 140, 62)
        heads = h if heads is None else heads + h

# 4 Push-button station with instruction plate, on the sidewalk face of the pole
button = (Pos(PX, PY - POLE_R - 30, 1050) * Box(70, 60, 160)
          + Pos(PX, PY - POLE_R - 62, 1330) * Box(230, 4, 300))

# 5 Presence radar on a short arm, aimed at the waiting area by the curb
radar = rod((PX, PY, 2450), (PX - 200, PY, 2450), 12) + Pos(PX - 240, PY + 20, 2450) * Box(80, 80, 80)

# 6 Solar panel, 20 W, tilted 30 degrees toward the equator (here -Y)
panel = Pos(PX, PY - 40, 3930) * Rot(30, 0, 0) * Box(500, 360, 25)

# 7 Panel bracket on the pole top
bracket = Pos(PX, PY, POLE_H + 60) * Box(60, 60, 120) + Pos(PX, PY - 30, POLE_H + 130) * Box(300, 160, 12)

# 8 Enclosure, IP65, hollow so the cutaway shows the inside
enc = Pos(ENC_X, PY, ENC_Z) * (Box(150, 260, 300) - Box(142, 252, 292))

# 9 LiFePO4 battery 12.8 V 12 Ah (about 151 x 98 x 95 mm)
battery = Pos(ENC_X, PY, ENC_Z - 146 + 49) * Box(95, 151, 98)

# 10 MPPT solar charge controller
mppt = Pos(ENC_X - 40, PY + 55, ENC_Z - 10) * Box(40, 90, 60)

# 11 Controller board (MCU, LED drivers, LoRa radio, RTC)
ctrl = Pos(ENC_X + 55, PY, ENC_Z + 60) * Box(14, 180, 100)

# 12 Antenna on the enclosure roof
antenna = Pos(ENC_X, PY + 90, ENC_Z + 150 + 110) * Cylinder(8, 220)

# 13 Pole clamps and brackets (stainless bands)
clamps = ring(BAR_Z) + ring(SIGN_Z - 250) + ring(SIGN_Z + 250) + ring(ENC_Z - 100) + ring(ENC_Z + 100) + ring(1050)

# 14 Post, 89 mm galvanized steel (or an existing pole)
post = Pos(PX, PY, POLE_H / 2) * Cylinder(POLE_R, POLE_H)

parts = [
    Part("Crossing warning sign, 750 mm", sign, "#FACC15", 1, (500, 0, 250)),
    Part("Light bar housing, double sided", bar, "#374151", 2, (900, 0, -150)),
    Part("Amber LED heads (4)", heads, "#F59E0B", 3, (1400, 0, -350)),
    Part("Push-button station", button, "#2563EB", 4, (0, -600, 0)),
    Part("Presence radar on arm", radar, "#7C3AED", 5, (-500, 0, -250)),
    Part("Solar panel, 20 W", panel, "#1E3A8A", 6, (0, -500, 600)),
    Part("Panel bracket", bracket, "#6B7280", 7, (0, 0, 300)),
    Part("Enclosure, IP65", enc, "#CBD5E1", 8, (-600, 0, 450), 1.0),
    Part("LiFePO4 battery 12.8 V 12 Ah", battery, "#C2410C", 9, (-1400, -700, -300)),
    Part("MPPT charge controller", mppt, "#16A34A", 10, (-1500, 500, 150)),
    Part("Controller and radio board", ctrl, "#0F766E", 11, (-900, 200, 750)),
    Part("Antenna", antenna, "#111827", 12, (-400, 900, 500)),
    Part("Pole clamps", clamps, "#94A3B8", 13, (500, 700, 0)),
    Part("Post, 89 mm (or existing pole)", post, "#9CA3AF", 14, (0, 0, 0)),
]

# ---------------- street context (hero and isometric only) ----------------
ROAD_W = 7000.0
road = Pos(0, 0, -200) * Box(8000, ROAD_W, 100)
walks = Pos(0, -ROAD_W / 2 - 1250, -125) * Box(8000, 2500, 250) + Pos(0, ROAD_W / 2 + 1250, -125) * Box(8000, 2500, 250)
stripes = None
for k in range(7):
    y = -3000 + k * 1000
    s = Pos(0, y, -148) * Box(3000, 500, 4)
    stripes = s if stripes is None else stripes + s
centre = None
for x in range(-3500, 3501, 2000):
    if abs(x) < 2200:
        continue
    d = Pos(x, 0, -148) * Box(1000, 120, 4)
    centre = d if centre is None else centre + d
far = [Part(f"Far-side {p.name}", Rot(0, 0, 180) * p.shape, p.color, None) for p in parts]
far_shape = far[0].shape
for p in far[1:]:
    far_shape = far_shape + p.shape
context = [
    Part("Road", road, "#4B5563"),
    Part("Sidewalks", walks, "#D6D3D1"),
    Part("Zebra markings", stripes, "#F9FAFB"),
    Part("Centre line", centre, "#FDE68A"),
    Part("Far-side assembly", far_shape, "#A8A29E"),
]

render_all(
    parts, project="CrossSafe", title="Solar crossing beacon concept", dwg_no="CRS-DWG-010",
    key_figures=["One assembly per side of a 7 m two-lane crossing (two per crossing)",
                 "Two amber heads per face, 127 x 51 mm min., wig-wag flash",
                 "Push button plus radar presence detection; LoRa link syncs both sides",
                 "20 W panel, 12.8 V 12 Ah LiFePO4; about 30 Wh/day at 300 uses (estimate)",
                 "About 4 days without sun (estimate); parts about $361 per side"],
    context=context,
    cut=False,
    flow={"title": "daily energy per assembly, Wh per day (estimates: 2.5 peak sun hours, 300 activations of 20 s)",
          "unit": "Wh",
          "stages": [("Sun on 20 W panel", 50), ("Panel output", 42.5), ("Charger output", 40),
                     ("Available to store", 38), ("Load demand", 29.8), ("LED flashing", 15.4)],
          "losses": [(0, "Heat, dust, wiring", 7.5), (1, "MPPT", 2.5), (2, "Cell charging", 2),
                     (3, "Surplus, battery full", 8.2), (4, "Standby: radar, radio", 14.4)]},
)

# Cutaway of the enclosure zone only (the full 3.7 m post would make the inside unreadable).
# A 700 mm length of post is drawn so the enclosure is not shown floating.
stub = Pos(PX, PY, ENC_Z) * Cylinder(POLE_R, 700)
zone = [p for p in parts if p.bom in (8, 9, 10, 11, 12)] + [Part("Post (section of)", stub, "#9CA3AF", 14),
                                                          Part("Pole clamps", ring(ENC_Z - 100) + ring(ENC_Z + 100), "#94A3B8", 13)]
# cutaway_parts centres its cutter at X = Z = 0, so move the zone to the origin first
zone = [Part(p.name, Pos(-PX, -PY, -ENC_Z) * p.shape, p.color, p.bom) for p in zone]
_render(cutaway_parts(zone), Path.cwd() / "media" / "cutaway.png", azim=-90, elev=18, labels=True,
        title="CrossSafe: cutaway of the pole-top enclosure",
        note="Enclosure cut on the pole axis; battery low, charger and controller above, antenna on the roof")

# Exploded view, rebuilt so small parts stay readable: the post is shortened to its upper 2 m and
# the push-button station is moved up 700 mm for this view only. Numbers match bom/bom.csv.
EXPLODE = {1: (600, 0, 200), 2: (900, 0, -250), 3: (1500, 0, -500), 4: (0, -700, -100),
           5: (-600, 0, -300), 6: (0, -400, 700), 7: (0, 0, 350), 8: (-700, 0, 300),
           9: (-1500, 0, -500), 10: (-1500, 0, -100), 11: (-1500, 0, 300), 12: (-1500, 0, 800),
           13: (500, 700, 0), 14: (0, 0, 0)}
xp = []
for p in parts:
    shape, name = p.shape, p.name
    if p.bom == 14:
        shape, name = Pos(PX, PY, 2700) * Cylinder(POLE_R, 2000), "Post, 89 mm (shortened in this view)"
    if p.bom == 4:
        shape = Pos(0, 0, 700) * shape
    xp.append(Part(name, shape, p.color, p.bom, EXPLODE[p.bom]))
_render(xp, Path.cwd() / "media" / "exploded.png", offsets=True, labels=True, size=(13, 8),
        title="CrossSafe: exploded view (one assembly)",
        note="Post shortened and push button moved up for this view; numbers match bom/bom.csv")
