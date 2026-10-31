"""Lesson 6: measure the hook's opening, walls and lip from its exported triangles (numpy only), the way a ruler would.

Rays are shot through the mesh and the solid stretches along each ray are read (enter, exit pairs; touching stretches
merged). Positions are taken from the part's own bounding box, so a moved part reads the same:
  - along X, 30% across the width (off the middle, where face diagonals and the bores are), at the middle of the
    heights where a level ray crosses two walls (above the base, below the lip's top: found, not assumed): the
    plate, the gap (the opening), the lip;
  - down (along Z) through the middle of the gap: the base's thickness;
  - down through each wall's middle: the lower top is the lip's height (the lip may be on either side).
The small offsets keep rays off triangle edges; a ray that still meets an edge counts that hit once.

    python3 -m checker.l6geom FILE.stl    prints the JSON"""
import json
import sys

import numpy as np

EPS = 1e-7
OFF = 0.0137          # nudge rays off the edges of the triangles that tile flat faces


def intervals(tris, origin, axis):
    """Solid stretches [(start, end)] along a ray parallel to `axis` (0 = X, 1 = Y, 2 = Z) through `origin`, as
    coordinates on that axis. Möller-Trumbore on every triangle; hits closer than 1e-6 are one hit."""
    t = np.asarray(tris, dtype=float)
    d = np.zeros(3)
    d[axis] = 1.0
    o = np.asarray(origin, dtype=float)
    v0, e1, e2 = t[:, 0], t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]
    p = np.cross(d, e2)
    det = np.einsum('ij,ij->i', e1, p)
    ok = np.abs(det) > EPS
    inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
    s = o - v0
    u = np.einsum('ij,ij->i', s, p) * inv
    q = np.cross(s, e1)
    v = (q @ d) * inv
    tt = np.einsum('ij,ij->i', e2, q) * inv
    hit = ok & (u >= -1e-9) & (v >= -1e-9) & (u + v <= 1 + 1e-9)
    # outward-facing triangles: det > 0 = the ray enters the solid, det < 0 = it leaves
    ev = []
    for sign in (1, -1):
        xs = np.sort(tt[hit & (np.sign(det) == sign)] + o[axis])
        last = None
        for x in xs:
            if last is None or x - last > 1e-6:      # a ray through an edge shared by two triangles: one hit
                ev.append((float(x), sign))
            last = x
    ev.sort(key=lambda e: (e[0], e[1]))             # at one spot, leave before enter: touching solids join below
    out, depth, start = [], 0, None
    for x, sign in ev:
        if depth == 0 and sign > 0:
            start = x
        depth += sign
        if depth == 0 and start is not None:
            if out and abs(start - out[-1][1]) < 1e-6:
                out[-1] = (out[-1][0], x)
            else:
                out.append((start, x))
            start = None
    return out


def measure_hook(tris):
    t = np.asarray(tris, dtype=float)
    lo, hi = t.reshape(-1, 3).min(axis=0), t.reshape(-1, 3).max(axis=0)
    yr = lo[1] + 0.3 * (hi[1] - lo[1]) + OFF        # off the width's middle: no face diagonal, clear of the bores
    res = {'bbox_min': [round(float(x), 6) for x in lo], 'bbox_max': [round(float(x), 6) for x in hi],
           'opening_mm': None, 'plate_mm': None, 'lip_mm': None, 'base_mm': None, 'lip_height_mm': None,
           'ray_z_mm': None, 'across': None}
    # the window where a level ray crosses two walls: above the base, below the lip's top (found, not assumed)
    zs = [z for z in np.arange(0.25, min(30.0, hi[2] - lo[2]), 0.25)
          if len(intervals(t, (lo[0] - 100.0, yr, lo[2] + z + OFF), 0)) >= 2]
    if not zs:
        return res
    run = [zs[0]]
    for z in zs[1:]:
        if abs(z - run[-1] - 0.25) > 1e-9:
            break
        run.append(z)
    zr = lo[2] + (run[0] + run[-1]) / 2.0 + OFF
    res['ray_z_mm'] = round(zr - lo[2], 4)
    across = intervals(t, (lo[0] - 100.0, yr, zr), 0)
    res['across'] = [[round(a - lo[0], 4), round(b - lo[0], 4)] for a, b in across]
    first, second = across[0], across[1]
    res['opening_mm'] = round(second[0] - first[1], 4)
    xm = (first[1] + second[0]) / 2.0 + OFF
    down = intervals(t, (xm, yr, lo[2] - 100.0), 2)
    if down:
        res['base_mm'] = round(down[0][1] - down[0][0], 4)
    walls = [first, across[-1]]
    tops = []
    for a, b in walls:
        iv = intervals(t, ((a + b) / 2.0 + OFF, yr, lo[2] - 100.0), 2)
        tops.append(iv[0][1] - lo[2] if iv else None)
    k = 0 if (tops[0] or 0) <= (tops[1] or 0) else 1          # the lower wall is the lip
    lip, plate = walls[k], walls[1 - k]
    res['lip_mm'] = round(lip[1] - lip[0], 4)
    res['plate_mm'] = round(plate[1] - plate[0], 4)
    res['lip_height_mm'] = round(tops[k], 4) if tops[k] is not None else None
    return res


if __name__ == '__main__':
    from checker import stl
    print(json.dumps(measure_hook(stl.read(sys.argv[1])), indent=1))
