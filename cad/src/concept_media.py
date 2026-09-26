"""CrossSafe concept media (TRL 3), built from the parametric model in cad/src/model.py.

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
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all, cutaway_parts, _render
from model import PARAMS as MP, build_parts, derived

PX, PY = 1900.0, -4300.0     # post axis in the street scene, 800 mm back from the kerb (kerb at Y = -3500)
DM = derived(MP)
POLE_R = MP["post_od"] / 2
ENC_Z = MP["enc_z"]

# Parts come from the parametric model (cad/src/model.py), moved from its local frame (post on the Z axis,
# sign facing +X, kerb on +Y) into the scene. The embedded part of the post and the footing are left out
# of the media so the scale figure stands on the sidewalk.
local = build_parts(MP, own_post=True)
local[14] = Pos(0, 0, MP["post_h"] / 2) * (Cylinder(POLE_R, MP["post_h"]) - Cylinder(POLE_R - MP["post_wall"], MP["post_h"] + 2))
M = {k: Pos(PX, PY, 0) * v for k, v in local.items() if k != "footing"}

parts = [
    Part("Crossing warning sign, 750 mm", M[1], "#FACC15", 1, (500, 0, 250)),
    Part("Light bar housing, double sided", M[2], "#374151", 2, (900, 0, -150)),
    Part("Amber LED heads (4)", M[3], "#F59E0B", 3, (1400, 0, -350)),
    Part("Push-button station", M[4], "#2563EB", 4, (0, -600, 0)),
    Part("Presence radar on arm", M[5], "#7C3AED", 5, (-500, 0, -250)),
    Part("Solar panel, 20 W", M[6], "#1E3A8A", 6, (0, -500, 600)),
    Part("Panel bracket", M[7], "#6B7280", 7, (0, 0, 300)),
    Part("Enclosure, IP65", M[8], "#CBD5E1", 8, (-600, 0, 450), 1.0),
    Part("LiFePO4 battery 12.8 V 12 Ah", M[9], "#C2410C", 9, (-1400, -700, -300)),
    Part("MPPT charge controller", M[10], "#16A34A", 10, (-1500, 500, 150)),
    Part("Controller and radio board", M[11], "#0F766E", 11, (-900, 200, 750)),
    Part("Antenna", M[12], "#111827", 12, (-400, 900, 500)),
    Part("Pole clamps", M[13], "#94A3B8", 13, (500, 700, 0)),
    Part("Post, 114.3 mm (or existing pole)", M[14], "#9CA3AF", 14, (0, 0, 0)),
    Part("PIR wake sensor", M[16], "#DB2777", 16, (-500, 300, -500)),
    Part("Pedestrian pilot light", M[17], "#EAB308", 17, (900, 500, -300)),
    Part("Ventilated sun shield", M[18], "#F8FAFC", 18, (-600, 0, 900)),
    Part("Anti-rotation bolt (new post)", M[19], "#111827", 19, (-700, 0, 0)),
    Part("Keyed sign saddles", M[20], "#475569", 20, (300, 0, 0)),
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
                 "Two amber heads per face, 140 x 62 mm lens, IA-21 wig-wag flash",
                 "Button plus PIR-gated radar; LoRa link syncs both sides",
                 "20 W panel, 12.8 V 12 Ah LiFePO4; 16.0 Wh/day at 300 uses (CRS-CAL-001)",
                 "7.7 days without sun; sun shield keeps the battery below 60 C",
                 "$332 per side on an existing pole (CRS-DDR-002)"],
    context=context,
    cut=False,
    flow={"title": "daily energy per assembly, Wh per day (CRS-CAL-001 estimates: 2.5 peak sun hours, 300 activations of 20 s)",
          "unit": "Wh",
          "stages": [("Sun on 20 W panel", 50), ("Panel output", 42.5), ("Charger output", 40),
                     ("Available to store", 38), ("Load demand", 16), ("LED flashing", 11)],
          "losses": [(0, "Heat, dust, wiring", 7.5), (1, "MPPT", 2.5), (2, "Cell charging", 2),
                     (3, "Surplus, battery full", 22), (4, "Standby and pilot light", 5)]},
)

# Cutaway of the enclosure zone only (the full 3.7 m post would make the inside unreadable).
# A 700 mm length of post is drawn so the enclosure is not shown floating.
stub = Pos(PX, PY, ENC_Z) * Cylinder(POLE_R, 700)
ring = lambda z: Pos(PX, PY, z) * (Cylinder(POLE_R + MP["band_t"], MP["band_w"]) - Cylinder(POLE_R, MP["band_w"] + 2))
zone = [p for p in parts if p.bom in (8, 9, 10, 11, 12, 18)] + [Part("Post (section of)", stub, "#9CA3AF", 14),
                                                          Part("Pole clamps", ring(ENC_Z - 100) + ring(ENC_Z + 100), "#94A3B8", 13)]
# cutaway_parts centres its cutter at X = Z = 0, so move the zone to the origin first
zone = [Part(p.name, Pos(-PX, -PY, -ENC_Z) * p.shape, p.color, p.bom) for p in zone]
_render(cutaway_parts(zone), Path.cwd() / "media" / "cutaway.png", azim=-90, elev=18, labels=True,
        title="CrossSafe: cutaway of the pole-top enclosure and sun shield",
        note="Enclosure and shield cut on the pole axis; battery low, charger and controller above, antenna through the shield roof")

# Exploded view, rebuilt so small parts stay readable: the post is shortened to its upper 2 m and
# the push-button station is moved up 700 mm for this view only. Numbers match bom/bom.csv.
EXPLODE = {1: (600, 0, 200), 2: (900, 0, -250), 3: (1500, 0, -500), 4: (0, -700, -100),
           5: (-600, 500, -200), 6: (0, -400, 700), 7: (0, 0, 350), 8: (-700, 0, 300),
           9: (-1500, 0, -500), 10: (-1500, 0, -100), 11: (-1500, 0, 300), 12: (-1500, 0, 800),
           13: (1400, 900, 400), 14: (0, 0, 0), 16: (-900, 0, -900), 17: (1300, 0, 500),
           18: (-700, 0, 1100), 19: (-300, 0, -500), 20: (500, -700, 0)}
xp = []
for p in parts:
    shape, name = p.shape, p.name
    if p.bom == 14:
        shape, name = Pos(PX, PY, 2700) * Cylinder(POLE_R, 2000), "Post, 114.3 mm (shortened in this view)"
    if p.bom == 4:
        shape = Pos(0, 0, 700) * shape
    if p.bom == 19:  # rebuilt at three times size (scaling the located rod would move it)
        c = shape.bounding_box().center()
        bl = shape.bounding_box().size.X
        shape = Pos(c.X, c.Y, c.Z) * Rot(0, 90, 0) * Cylinder(3 * MP["bolt_d"] / 2, 3 * bl)
    if p.bom in (16, 17):  # drawn at three times size so they show at this scale
        c = shape.bounding_box().center()
        shape = Pos(c.X, c.Y, c.Z) * (Pos(-c.X, -c.Y, -c.Z) * shape).scale(3.0)
    xp.append(Part(name, shape, p.color, p.bom, EXPLODE[p.bom]))
_render(xp, Path.cwd() / "media" / "exploded.png", offsets=True, labels=True, size=(13, 8),
        title="CrossSafe: exploded view (one assembly)",
        note="Post shortened, push button moved up, PIR (16), pilot light (17) and bolt (19, new posts only) drawn at three times size; numbers match bom/bom.csv")
