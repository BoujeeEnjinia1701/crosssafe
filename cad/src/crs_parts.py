"""CrossSafe repo-specific CAD helpers for the kit 1.9 interface (STANDARDS section 24).

These sit beside .kit/cad_parts.py and are candidates for a future kit release (see docs/REVIEW.md):

    soft()        edge breaks on a bare box or cylinder, so it counts as a real part
    weld_on()     a cad_parts.weld_fillet bead placed along any axis with its two legs on any two faces
    ring_weld()   a round fillet bead under a plate round a tube
    washed()      move a bolt out by one washer thickness and return the washer under its head
    module()      a bought electronic module on four stand-off feet
    pframe()      a PV module as an aluminium frame ring and a laminate (frame and laminate as two parts)

All sizes in millimetres, in the model frame of cad/src/model.py (post axis Z, sidewalk top z = 0).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Circle, Cylinder, Location, Plane, Pos, Rot, Sketch, Solid, Vector, extrude  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import break_edges  # noqa: E402


def soft(shape, r=0.8):
    """Edge break, so a plain box or cylinder is a part with broken edges, not massing."""
    return break_edges(shape, r)


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def weld_on(origin, axis, length, leg, d1, d2):
    """Fillet weld bead from origin along axis for length, its two legs lying along d1 and d2 (unit axis directions)
    from the corner line. cad_parts.weld_fillet runs along +X with its legs on +Y and +Z."""
    c = _cross(axis, d1)
    if all(abs(c[i] - d2[i]) < 1e-9 for i in range(3)):
        z = d2
    else:                       # left-handed pair: the bead profile is symmetric, so swap the legs
        z = d1
    loc = Location(Plane(origin=tuple(origin), x_dir=tuple(axis), z_dir=tuple(z)))
    return loc * cp.weld_fillet(length, leg)


def ring_weld(r, leg, z_plate, below=True):
    """Round fillet bead round a tube of outer radius r, under (below) or over a plate whose face is at z_plate."""
    z0 = z_plate - leg if below else z_plate
    cone = Solid.make_cone(r if below else r + leg, r + leg if below else r, leg, Plane(origin=(0, 0, z0)))
    return cone - Cylinder(r, 4 * leg).moved(Location((0, 0, z0)))


def washed(bolt_shape, axis, sign, head_h, t=1.6, d_in=8.4, d_out=16.0):
    """Lift a bolt by one washer thickness. axis 0, 1 or 2, sign +1 if the shank runs toward +axis. Returns
    (lifted bolt, washer) with the washer between the old head underside and the lifted head."""
    bb = bolt_shape.bounding_box()
    lo, hi = (bb.min.X, bb.min.Y, bb.min.Z)[axis], (bb.max.X, bb.max.Y, bb.max.Z)[axis]
    head_at = (lo + head_h) if sign > 0 else (hi - head_h)
    ctr = [(bb.min.X + bb.max.X) / 2, (bb.min.Y + bb.max.Y) / 2, (bb.min.Z + bb.max.Z) / 2]
    out_dir = [0.0, 0.0, 0.0]
    out_dir[axis] = -sign * t
    lifted = Pos(*out_dir) * bolt_shape
    # washer: annulus of thickness t, from the surface outward
    ring = extrude(Sketch() + Circle(d_out / 2) - Circle(d_in / 2), t)
    # ring is built along +Z from z = 0; turn it to the bolt axis and put its surface face at head_at
    rot = {0: Rot(0, 90, 0), 1: Rot(-90, 0, 0), 2: Rot(0, 0, 0)}[axis]
    w = rot * ring                      # extends toward +axis from the origin
    pos = list(ctr); pos[axis] = head_at
    if sign > 0:                        # outward is -axis: the washer spans [head_at - t, head_at]
        pos[axis] = head_at - t
    return lifted, Pos(*pos) * w


def module(dims, x_back, yc, zlo, feet=3.0, h_feet=6.0):
    """A bought electronic module box dims (dx, dy, dz) whose back face is at x_back (it lies in front, toward -x),
    carried on four stand-off feet toward +x. Returns one solid."""
    dx, dy, dz = dims
    body = Pos(x_back - h_feet - dx / 2, yc, zlo + dz / 2) * Box(dx, dy, dz)
    for sy in (-1, 1):
        for sz in (0, 1):
            yy, zz = yc + sy * (dy / 2 - 5), zlo + 5 + sz * (dz - 10)
            body = body + Pos(x_back - h_feet / 2, yy, zz) * Rot(0, 90, 0) * Cylinder(feet, h_feet)
    return soft(body, 0.6)


def pframe(w, d, t, ring=12.0, lam=10.0):
    """PV module, centred, lying in the XY plane with its back face at z = -t/2: (aluminium frame ring, laminate). The
    ring is the full depth t and ring wide; the laminate fills its opening at the back, lam thick."""
    outer = Box(w, d, t)
    opening = Box(w - 2 * ring, d - 2 * ring, t + 2)
    frame = soft(outer - opening, 0.8)
    laminate = Pos(0, 0, -t / 2 + lam / 2) * Box(w - 2 * ring, d - 2 * ring, lam)
    return frame, soft(laminate, 0.5)
