"""fx13 R1 checker (LAB-fx13 section 4), no AI: the cup's side wall, floor and top lid from its mesh.
    python3 lab/fx13wall.py OUT TAG     export the open body as ASCII STL (the plug's `export`), then OUT/wall-TAG.json
The cup's axis is the Z axis. Side surfaces = tall mesh triangles at one radius; outer = the largest, cavity = the next
(wall = outer - cavity); floor = the cavity side's lowest z - the body's lowest z; lid = the body's top z - the cavity
side's highest z (0 = open top). Rounded to 0.01 mm. One side surface only = solid (hollow false)."""
import json
import math
import os
import sys

TOL = 0.05


def walls(facets):
    """facets: triangles ((x, y, z) x 3). A side surface (a cylinder about Z) = a triangle whose three corners share one
    radius and span at least a quarter of the height (the rounds' and end faces' triangles are short or flat)."""
    zs = [v[2] for f in facets for v in f]
    z0, z1 = min(zs), max(zs)
    sides = {}                        # radius (0.01 mm) -> the z values of its side triangles
    for f in facets:
        rr = [math.hypot(v[0], v[1]) for v in f]
        fz = [v[2] for v in f]
        if max(rr) - min(rr) <= TOL and min(rr) > TOL and max(fz) - min(fz) >= (z1 - z0) / 4:
            sides.setdefault(round(sum(rr) / 3, 2), []).extend(fz)
    radii = sorted(sides, reverse=True)
    res = {'z_min': round(z0, 2), 'z_max': round(z1, 2), 'side_radii': radii}
    if len(radii) < 2:
        return dict(res, outer_r_mm=radii[0] if radii else None, hollow=False, wall_mm=None, floor_mm=None,
                    lid_mm=None, cavity_r_mm=None)
    outer, inner = radii[0], radii[1]
    cz = sides[inner]
    return dict(res, outer_r_mm=outer, hollow=True, cavity_r_mm=inner, wall_mm=round(outer - inner, 2),
                floor_mm=round(min(cz) - z0, 2), lid_mm=round(z1 - max(cz), 2))


def main():
    sys.path.insert(0, '/work')
    from checker import entry  # noqa: E402
    from client.mcp import McpClient  # noqa: E402
    o, tag = sys.argv[1], sys.argv[2]
    p = os.path.join(os.path.expanduser('~'), f'wall-{tag}.stl')
    e = entry.read(os.path.expanduser('~/.claude.json'))       # as lab/fx9.py client(), FX9_ALLOW's --allow-path ~
    c = McpClient([e['command']] + e['args'] + ['--allow-path', os.path.expanduser('~')], timeout_s=120)
    c.start()
    r = McpClient.text(c.call_tool('export', {'path': p, 'format': 'stla'}))
    c.close()
    v = []
    for line in open(p):
        s = line.split()
        if s and s[0] == 'vertex':
            v.append((float(s[1]), float(s[2]), float(s[3])))
    f = [tuple(v[i:i + 3]) for i in range(0, len(v) - 2, 3)]
    res = dict(walls(f), export=r[:200], facets=len(f), method=__doc__.split('\n')[2:5])
    json.dump(res, open(os.path.join(o, f'wall-{tag}.json'), 'w'), indent=1)
    print('wall', tag, json.dumps({k: res[k] for k in ('hollow', 'wall_mm', 'floor_mm', 'lid_mm', 'outer_r_mm')}))


if __name__ == '__main__':
    main()
