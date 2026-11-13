"""fx14b R1 checker (LAB-fx14b section 4), no AI: one hole in the top of the block, from its mesh.
    python3 lab/fx14bhole.py OUT TAG     export the open body as ASCII STL (the plug's `export`), then OUT/hole-TAG.json
Hole vertices = mesh corners strictly inside the box's x/y bounds (a plain or converted box has corners only on its
bounds). Centre = mid of their x/y range, diameter = x range; wall = vertices at the hole radius (top z, wall bottom z,
depth = top - wall bottom); flat floor = 3+ vertices at the lowest z (a pointed tip has one). Rounded to 0.01 mm."""
import json
import math
import os
import sys

TOL = 0.05


def find_hole(facets):
    vs = {tuple(round(c, 4) for c in v) for f in facets for v in f}
    xs, ys, zs = [v[0] for v in vs], [v[1] for v in vs], [v[2] for v in vs]
    box = [round(min(xs), 2), round(min(ys), 2), round(min(zs), 2), round(max(xs), 2), round(max(ys), 2), round(max(zs), 2)]
    ins = [v for v in vs if box[0] + TOL < v[0] < box[3] - TOL and box[1] + TOL < v[1] < box[4] - TOL]
    if len(ins) < 3:
        return {'hole': False, 'box': box, 'inside_vertices': len(ins)}
    cx = (min(v[0] for v in ins) + max(v[0] for v in ins)) / 2
    cy = (min(v[1] for v in ins) + max(v[1] for v in ins)) / 2
    r = (max(v[0] for v in ins) - min(v[0] for v in ins)) / 2
    wall = [v for v in ins if abs(math.hypot(v[0] - cx, v[1] - cy) - r) <= TOL]
    top, wb = max(v[2] for v in wall), min(v[2] for v in wall)
    low = min(v[2] for v in ins)
    return {'hole': True, 'box': box, 'inside_vertices': len(ins), 'centre_xy': [round(cx, 2), round(cy, 2)],
            'diameter_mm': round(2 * r, 2), 'top_z': round(top, 2), 'wall_bottom_z': round(wb, 2),
            'depth_mm': round(top - wb, 2), 'lowest_z': round(low, 2),
            'flat_floor': sum(1 for v in ins if abs(v[2] - low) <= TOL) >= 3, 'through': low <= box[2] + TOL}


def main():
    sys.path.insert(0, '/work')
    from checker import entry  # noqa: E402
    from client.mcp import McpClient  # noqa: E402
    o, tag = sys.argv[1], sys.argv[2]
    p = os.path.join(os.path.expanduser('~'), f'hole-{tag}.stl')
    e = entry.read(os.path.expanduser('~/.claude.json'))       # as lab/fx13wall.py
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
    res = dict(find_hole(f), export=r[:200], facets=len(f), method=__doc__.split('\n')[2:5])
    json.dump(res, open(os.path.join(o, f'hole-{tag}.json'), 'w'), indent=1)
    os.remove(p)
    print('hole', tag, json.dumps({k: res.get(k) for k in ('hole', 'centre_xy', 'diameter_mm', 'depth_mm', 'flat_floor', 'box')}))


if __name__ == '__main__':
    main()
