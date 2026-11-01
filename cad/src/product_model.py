"""CrossSafe product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3.

Every product part is components(CHOSEN) from cad/src/model.py as it is (option A, the pole-top beacon): sign,
light bar, LED heads, push-button station, radar arm, enclosure with sun shield, battery, boards and glands, the
panel and its bracket, band clamps and keyed saddles, every bolt, nut, washer and weld bead. Only the site is
added, as context parts: a raised concrete sidewalk with a kerb and tactile paving, the asphalt road with the
zebra markings, and a 1.75 m mannequin waiting at the kerb for scale.

The hero is rendered by .kit/photoreal.py as an outdoor scene, the ground plane being the asphalt of the road at
model z = -150 (the sidewalk top is model z = 0, as in cad/src/model.py); every site part reaches below the
ground (RENDER_VIEWS "args"). APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION. A research prototype, not
a certified traffic control device.

Axes of model.py: post axis Z, sidewalk top z = 0, sign faces approaching traffic on +X, kerb and waiting zone on
+Y (kerb face at y = 800 mm), the crossing toward -X of the post.

Groups: "shell" (the beacon and the post), "internal", "accessory" (kept from components(), used by the exploded
view) and "context" (site and mannequin).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Cylinder, Pos, Rot, Sphere  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part, break_edges  # noqa: E402

TITLE = "CrossSafe: solar crossing beacon that warns drivers when a pedestrian waits"

ROAD_Z = -150.0                       # asphalt surface, model mm; the photoreal ground plane sits here
_SITE = ["--scene=outdoor", "--ground=concrete", f"--ground-z={ROAD_Z:.0f}", "--sun=32,60", "--lens=45"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 18, "az": 40, "args": _SITE,
     "note": "Site render at a marked crossing, from the road side, right and a little above (about 18 deg "
             "elevation): the crossing sign and lit light bar facing approaching traffic, push button, radar and "
             "pilot light toward the kerb, enclosure with its sun shield and the panel on the pole top; kerb, "
             "tactile paving and zebra markings; 1.75 m person waiting at the kerb for scale"},
    {"name": "studio", "groups": ["shell", "internal", "accessory"], "explode": False, "el": 20, "az": 38,
     "note": "Studio render from the front right and above (about 20 deg elevation): sign, light bar with amber "
             "heads and visors, push-button station, radar arm, sun shield, enclosure and panel on the post"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 26, "az": -50,
     "note": "Exploded view from the front right and above (about 26 deg elevation): sign, saddles and clamps; "
             "light bar, heads and pilot light; radar and PIR; button station; shield, enclosure, battery and "
             "boards; panel and bracket"},
    {"name": "detail", "groups": ["shell", "internal", "accessory"], "explode": False, "el": 10, "az": 62,
     "note": "Detail from the kerb side and the approach side, slightly above (about 10 deg elevation): lamp head "
             "with the amber heads, the pilot light, and the radar and PIR detector on their arm"},
]

KERB_Y = 800.0
PERSON_AT = (-1100.0, 470.0)          # waiting on the tactile paving, facing the road (+Y)
CROSS_X = (-1750.0, -450.0)           # zebra bars along X


def site():
    """Sidewalk, kerb, road and mannequin. Ground (the asphalt) is model z = -150; the sidewalk slab and kerb reach
    below it and the road slab top sits 2 mm above it, so nothing floats and the plane never z-fights."""
    out = []
    ctx = lambda n, sh, mat, g="context": out.append(part(n, sh, mat, kind="context", group=g))
    x0, x1 = -4200.0, 2600.0
    xm, xl = (x0 + x1) / 2, x1 - x0
    walk = Pos(xm, (-1500 + KERB_Y - 150) / 2, -250) * Box(xl, KERB_Y - 150 + 1500, 500)
    ctx("Concrete sidewalk (site)", break_edges(walk, 8), "concrete")
    kerb = Pos(xm, KERB_Y - 75, -250) * Box(xl, 150, 500)
    ctx("Kerb stone (site)", break_edges(kerb, 12), "concrete")
    road = Pos(xm, (KERB_Y + 6000) / 2 + 0.0, ROAD_Z - 198) * Box(xl, 6000 - KERB_Y, 400)
    ctx("Asphalt road (site)", road, "matte_black")
    cx0, cx1 = CROSS_X
    for k in range(6):
        y = KERB_Y + 450 + k * 800
        ctx(f"Zebra bar {k + 1} (site)", Pos((cx0 + cx1) / 2, y, ROAD_Z + 2.0 + 1.5) * Box(cx1 - cx0, 450, 3), "label")
    tx, ty = PERSON_AT[0], KERB_Y - 150 - 300
    pad = Pos(tx, ty, 2) * Box(900, 600, 4)
    ctx("Tactile paving pad (site)", pad, "safety_yellow")
    try:
        import context_parts
        man = Pos(PERSON_AT[0], PERSON_AT[1], 0) * Rot(0, 0, 180) * context_parts.mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:   # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    out = []
    for p in M.components(M.CHOSEN):
        q = dict(p)
        if q["kind"] == "context":          # the existing pole: shown in every view, left out of the framing by its name
            q["group"] = "shell"
        out.append(q)
    return out + site()


if __name__ == "__main__":
    ps = product_parts()
    print(len(ps), "parts;", sum(p["group"] == "shell" for p in ps), "shell,", sum(p["group"] == "context" for p in ps), "context")
