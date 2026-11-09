"""fx9 take P (LAB-fx9 section 3, not filmed): the nut, no AI, over the plug entry SolidCraft wrote (lesson-7 client
pattern). A sketch on XY: a hexagon 13 mm across flats (sketch.polygon.circumscribed, radius 6.5 to the edge midpoints,
6 sides), finished, extruded 7 mm, the body named "Nut"; solid.hole at the centre of the top face, through. Saved as
~/nut.sc (hole 8) and ~/nut-675.sc (hole 6.75, a fresh design built the same way). Sizes + volumes -> OUT/volume.txt.
    FX9_ALLOW=1 python3 -I nut.py OUT_DIR
Every JSON-RPC message -> OUT/rpc.jsonl."""
import json
import os
import sys

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

OUT = sys.argv[1]
e = entry.read(os.path.expanduser('~/.claude.json'))
c = McpClient([e['command']] + e['args'] + ['--allow-path', os.path.expanduser('~')], timeout_s=120,
              log_path=os.path.join(OUT, 'rpc.jsonl'))
c.start()
log = open(os.path.join(OUT, 'volume.txt'), 'w')


def jt(name, args):
    r = c.call_tool(name, args)
    s = McpClient.text(r).split('\nNote:')[0]
    try:
        return r.get('isError'), json.loads(s)
    except ValueError:
        return r.get('isError'), {'text': s}


def out(line):
    print(line, flush=True)
    log.write(line + '\n')


def build(hole_d, path):
    jt('new_design', {})
    err, r = jt('batch', {'commands': [
        {'command': 'sketch.create', 'params': {'plane': 'XY'}},
        {'command': 'sketch.polygon.circumscribed', 'params': {'center': [0, 0], 'radius': 6.5, 'sides': 6}},
        {'command': 'sketch.finish', 'params': {}},
        {'command': 'solid.extrude', 'params': {'distance': 7, 'body_name': 'Nut'}},
        {'command': 'solid.hole', 'params': {'position': [0, 0, 7], 'diameter': hole_d}}], 'verbose': False})
    out(f'build hole {hole_d}: isError {err}; ' + json.dumps(r)[:300])
    _, m = jt('measure', {})
    b = (m.get('bodies') or [{}])[0]
    out(f'hole {hole_d}: body {b.get("name")} volume_mm3 {(m.get("total") or {}).get("volume_mm3")} '
        f'bbox {json.dumps(b.get("bbox") or b.get("bounding_box") or (m.get("total") or {}).get("bbox"))}')
    _, d = jt('inspect_design', {})
    out(f'hole {hole_d}: timeline ' + json.dumps([f.get('name') or f.get('type') for f in (d.get('timeline') or [])]))
    json.dump({'measure': m, 'design': d}, open(os.path.join(OUT, f'read-{hole_d}.json'), 'w'), indent=1)
    err, r = jt('save', {'path': path})
    out(f'save {os.path.basename(path)}: isError {err}; ' + json.dumps(r)[:200])


build(8, os.path.expanduser('~/nut.sc'))
build(6.75, os.path.expanduser('~/nut-675.sc'))
c.close()
