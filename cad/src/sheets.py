"""CrossSafe general arrangement sheet CRS-DWG-001, Rev P5 (TRL 3; constructable design, CRS-DDR-003).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/CRS-DWG-001.svg, .pdf and .png from the parametric model in cad/src/model.py
with .kit/drawing.py. Dimensions come from PARAMS and derived(), so they follow any parameter
change. The concept blueprint in media/ is CRS-DWG-010, so CRS-DWG-001 was free.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, assembly, derived  # noqa: E402

DATE = "2026-09-25"
DATE_P4 = "2026-09-30"
DATE_P5 = "2026-10-02"


def safe_project_views(part, workdir, line_weight=0.35):
    """Same views as drawing.project_views, but edge by edge, so that a degenerate edge from the
    hidden-line projection is skipped instead of stopping the export."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", hidden if name != "iso" else [])):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    dl = 11  # room the kit leaves left of and above the views for overall dimensions
    ax += (aw - (k * (max(fw, tw) + rw) + gap + dl)) / 2 + dl
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab + dl)) / 2 + dl
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text, right=False):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            (_t(x2 + 2.0, y + 0.8, text, 2.3, 400, INK, "start", mono=True) if right
             else _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True))]


def dim_v(x, y1, y2, text, side=-1, low=False):
    a = 1.4
    cx, cy = x + (3.4 if side > 0 else -1.0), (max(y1, y2) - 1.5 if low else (y1 + y2) / 2)
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="translate({cx:.2f} {cy:.2f}) rotate(-90)">{_t(0, 0, text, 2.3, 400, INK, "start" if low else "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    D = derived(P)
    work = ROOT / "cad" / "drawings" / "_views"
    asm = assembly(own_post=True)
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="CrossSafe", title="General arrangement, one beacon assembly", dwg_no="CRS-DWG-001", rev="P5",
              author="Amish Chadha", date=DATE_P5, scale=None, theme="technical",
              material="Galvanized steel post; bought-in parts per bom/bom.csv. PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "Sun shield, keyed saddles, anti-rotation bolt (DDR-002)", DATE, "AC"),
                         ("P3", "Layout and labels tidied", DATE, "AC"),
                         ("P4", "Constructable design: saddles, bands, plate, bracket (DDR-003)", DATE_P4, "AC"),
                         ("P5", "Bezels and visors on the LED heads; kit limited to 76 to 114.3 mm poles", DATE_P5, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = [_t(M + 6, M + 14, "PRELIMINARY, NOT FOR FABRICATION", 2.6, 600, "#B45309")]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    zg = Z(0)
    L.append(f'<line x1="{x - 30:.2f}" y1="{zg:.2f}" x2="{x + w + 6:.2f}" y2="{zg:.2f}" stroke="{INK}" stroke-width="0.35"/>')
    L.append(_t(x + w + 7, zg - 1, "SIDEWALK", 2.0, 600, MUTED, "start"))
    xl = X(bb.min.X) - 12
    marks = ((P["button_z"], f"{P['button_z']:.0f} button"), (P["bar_bottom"], f"{P['bar_bottom']:.0f} bar"),
             (D["sign_bot"], f"{D['sign_bot']:.0f} sign"), (D["enc_bot"], f"{D['enc_bot']:.0f} encl."),
             (D["overall_h"], f"{D['overall_h']:,.0f} overall"))
    for i, (zz, label) in enumerate(marks):
        xd = xl - 6 * i
        L += [ext(X(0), Z(zz), xd - 1, Z(zz))]
        L += dim_v(xd, Z(zz), zg, label, low=(i == 0))
    xr = X(P["footing_d"] / 2) + 11
    L += [ext(X(P["footing_d"] / 2), Z(-P["embed"]), xr + 1, Z(-P["embed"]))]
    L += dim_v(xr, zg, Z(-P["embed"]), f"{P['embed']:.0f} embed", side=1)
    L += dim_h(X(-P["footing_d"] / 2), X(P["footing_d"] / 2), zg + 5, f"{P['footing_d']:.0f}", right=True)

    # top view (from +Z): X to the right, Y up the sheet
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    L.append(_t(Xt(0), Yt(bb.max.Y) - 18, "KERB AND WAITING ZONE (+Y)", 1.9, 400, MUTED, "middle"))
    L.append(_t(Xt(bb.max.X) + 14, Yt(bb.min.Y) + 1, "PANEL FACES THE EQUATOR (-Y)", 1.9, 400, MUTED))
    L.append(_t(Xt(bb.max.X) + 14, Yt(0) - 2, "TRAFFIC SIDE (+X)", 1.9, 400, MUTED))

    # right view (from +X): Y to the right
    x, y, w, h = c["right"]
    Yr = lambda my: x + (my - bb.min.Y) * k
    Zr = lambda mz: y + h - (mz - bb.min.Z) * k
    L += dim_h(Yr(-P["sign_side"] / 2 ** 0.5), Yr(P["sign_side"] / 2 ** 0.5), Zr(D["sign_top"]) - 9,
               f"{P['sign_side'] * 2 ** 0.5:,.0f} ({P['sign_side']:.0f} sq. sign)")
    L += dim_h(Yr(-P["bar"][1] / 2), Yr(P["bar"][1] / 2), Zr(P["bar_bottom"]) + 9, f"{P['bar'][1]:.0f} bar", right=True)
    s._layers += L
    s.add_svg(views["iso"], 276, 42, 140, 86, label="Isometric view", sublabel="Not to scale")
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Post {P['post_od']} x {P['post_wall']} galvanized, {P['post_h']:.0f} above sidewalk, {P['embed']:.0f} in a {P['footing_d']:.0f} footing",
        f"Existing-pole kit: 8 keyed saddles and bands, {P['pole_min_od']:.0f} to {P['pole_max_od']:.1f} mm poles",
        f"Sign {P['sign_side']:.0f} diamond, {D['sign_bot']:.0f} to {D['sign_top']:.0f}; faces traffic on +X",
        f"Light bar {P['bar'][1]:.0f} x {P['bar'][0]:.0f} x {P['bar'][2]:.0f}, bottom {P['bar_bottom']:.0f}; two {P['head'][0]:.0f} x {P['head'][1]:.0f} heads per face, each with bezel and {P['visor_d']:.0f} visor",
        f"Pilot light on the kerb end of the bar; button centre {P['button_z']:.0f}",
        f"Radar and PIR on a {P['arm_l']:.0f} arm at {P['radar_z']:.0f}, toward the kerb",
        f"Enclosure IP65 {P['enc'][0]:.0f} x {P['enc'][1]:.0f} x {P['enc'][2]:.0f}, bottom {D['enc_bot']:.0f}, on a mounting plate",
        f"Ventilated sun shield, {P['shield_gap']:.0f} air gap, roof and three walls, open bottom",
        f"Sign flat on two saddles; new post: M{P['bolt_d']:.0f} bolt through sign, saddle and post",
        f"Panel 20 W {P['panel'][0]:.0f} x {P['panel'][1]:.0f} on rails and a welded bracket, tilt {P['panel_tilt']:.0f} deg",
        "Wind case 40 m/s gust: 45 % of S235 yield (CRS-CAL-001 v0.6)",
        "Third-angle; front view from -Y; post on the Z axis",
    ], x=276, y=150, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "CRS-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
