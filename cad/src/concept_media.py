"""CrossSafe concept media from the TRL 3 model (option A, constructable design, CRS-DDR-003; kit 1.9.1).

Run from the repo root:  python cad/src/concept_media.py [hero|cutaway|exploded|flow|web|blueprint|all ...]
With no argument it draws everything with .kit/concept.py render_all and then replaces the cutaway with a section
through the enclosure zone. On a small machine run one picture per process; "web" alone rewrites media/model.glb
and media/viewer.html from the model without redrawing anything (keeps the .glb under about 20 MB).
Geometry is components(CHOSEN) of cad/src/model.py as it is: every part, bolt, washer and weld bead. The flow values
come from CRS-CAL-001 (docs/04-calcs/sizing.py).

Axes as model.py: post axis Z, sidewalk top z = 0, sign faces approaching traffic on +X, kerb on +Y. The existing
pole is cut at the sidewalk so the 1.75 m person stands on the same floor as the beacon.
CONCEPT, NOT FOR FABRICATION.
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src"), str(ROOT / "docs/04-calcs")]
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
from build123d import Box, Pos  # noqa: E402
import model as M  # noqa: E402

PROJECT, TITLE, DWG, DATE = "CrossSafe", "Solar crossing beacon concept", "CRS-DWG-010", "2026-10-31"
MD = ROOT / "media"
GREY = "#9CA3AF"


def _bom_names():
    out = {}
    for r in csv.DictReader((ROOT / "bom/bom.csv").open()):
        n, _, name = r["Item"].partition(" ")
        out[int(n)] = name
    return out


def parts(context=True):
    names = _bom_names()
    above = Pos(0, 0, 3000) * Box(1000, 1000, 6000)          # keeps what is above the sidewalk
    out = []
    for p in M.components(M.CHOSEN):
        if p["kind"] == "context":
            if context:
                out.append(Part("Existing pole 114.3 mm", p["shape"] & above, GREY, 14, (0, 0, 0)))
            continue
        out.append(Part(names.get(p["bom"], p["name"]) if p["bom"] else p["name"], p["shape"], p["color"], p["bom"], tuple(p["explode"])))
    return out


def street():
    """Sidewalk, kerb and road, grey, for the hero only."""
    return [Part("Sidewalk", Pos(-700, -200, -40) * Box(3400, 2000, 80), "#D6D3D1"),
            Part("Kerb", Pos(-700, 800, -40) * Box(3400, 150, 80), "#B9B6B0"),
            Part("Road", Pos(-700, 2050, -190) * Box(3400, 2500, 100), "#4B5563")]


def key_figures():
    return ["One assembly per side of a 7 m two-lane crossing (two per crossing)",
            "Two amber heads per face, 140 x 62 mm lens, IA-21 wig-wag flash",
            "Button plus PIR-gated radar; LoRa link syncs both sides",
            "20 W panel, 12.8 V 12 Ah LiFePO4; 16.0 Wh/day at 300 uses (CRS-CAL-001 v0.7)",
            "7.7 days without sun; sun shield keeps the box at 53.9 C at 50 C ambient",
            "117 modelled parts, 27.6 kg; $364 per side on an existing pole"]


def flow_spec():
    return {"title": "daily energy per assembly, Wh per day (CRS-CAL-001 estimates: 2.5 peak sun hours, 300 activations of 20 s)",
            "unit": "Wh",
            "stages": [("Sun on 20 W panel", 50), ("Panel output", 42.5), ("Charger output", 40),
                       ("Available to store", 38), ("Load demand", 16), ("LED flashing", 11)],
            "losses": [(0, "Heat, dust, wiring", 7.5), (1, "MPPT", 2.5), (2, "Cell charging", 2),
                       (3, "Surplus, battery full", 22), (4, "Standby and pilot light", 5)]}


def cutaway():
    """Enclosure zone cut on the pole axis (front half removed), from the front and above."""
    zone = [p for p in parts(context=False)
            if p.shape.bounding_box().min.Z > 2700 and p.shape.bounding_box().max.Z < 3300]
    pole = [p for p in parts(context=True) if p.bom == 14]
    box = Pos(0, 0, 3000) * Box(1000, 1000, 700)
    zone += [Part(p.name + " (section of)", p.shape & box, GREY, 14) for p in pole]
    keep = Pos(0, 2000, 3000) * Box(4000, 4000, 4000)             # the half with y >= 0: the pole axis is the cut plane
    cut = []
    for p in zone:
        try:
            sh = p.shape & keep
            if sh.volume > 1e-6:
                cut.append(Part(p.name, sh, p.color, p.bom))
        except Exception:
            cut.append(p)
    return K._render(cut, MD / "cutaway.png", azim=-90, elev=18, labels=True,
                     title="CrossSafe: cutaway of the pole-top enclosure and sun shield",
                     note="Enclosure and shield cut on the pole axis; battery low, charger and controller above, antenna through the shield roof")


def everything():
    outs = K.render_all(parts(context=True), PROJECT, TITLE, DWG, key_figures(), date=DATE, rev="P3", cut=False, web_model=False,
                        flow=flow_spec(), context=street())
    outs["cutaway"] = cutaway()
    return outs


if __name__ == "__main__":
    fns = {"hero": lambda: K._render(K.with_scale_figure(parts()) + street(), MD / "hero.png", title=PROJECT,
                                     note="Seen from the front right and above, 24 deg elevation. Grey figure: 1.75 m person for scale"),
           "cutaway": cutaway,
           "exploded": lambda: K._render(parts(context=True), MD / "exploded.png", offsets=True, labels=True, title=f"{PROJECT}: exploded view",
                                         note="Seen from the front right and above, 24 deg elevation; numbers match bom/bom.csv"),
           "flow": lambda: K.flow_diagram(flow_spec()["stages"], MD / "flow.png", f"{PROJECT}: {flow_spec()['title']}", "Wh", flow_spec()["losses"]),
           "web": lambda: K.export_web_model(parts(context=True), "media", title=f"{PROJECT}: {TITLE}"),
           "all": everything}
    for w in sys.argv[1:] or ["all"]:
        print(w, "->", fns[w]())
