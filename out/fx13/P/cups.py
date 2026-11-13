"""fx13 take P (LAB-fx13 section 3, not filmed): the start files, no AI, over the plug entry SolidCraft wrote
(lesson-7 client pattern, as out/fx12/P/tray.py). Every cup: a circle centred on the origin on XY, Extrude up (z 0 up),
its outer edges rounded with solid.fillet (edge points on the circles at x = r):
  ~/cup.sc         D60 x 80, top + bottom edges 1.5   expected 226,014.67 mm3, 5 faces
  ~/cup-bottom.sc  D60 x 80, bottom edge only 1.5     expected 226,104.67 mm3, 4 faces
  ~/cup-r3.sc      D60 x 80, top + bottom edges 3     expected 225,482.81 mm3, 5 faces
  ~/cup40.sc       D40 x 40, top + bottom edges 1     expected  50,212.15 mm3, 5 faces
Each file is saved, reopened, and its volume (measure) and faces (model.faces) read back into OUT/volumes.txt.
A volume off by more than 0.1% = P0 stop (exit 3). Tool and parameter names: list_commands, logged in OUT/commands.txt.
    FX9_ALLOW=1 python3 -I cups.py OUT_DIR
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
log = open(os.path.join(OUT, 'volumes.txt'), 'w')
CUPS = [  # name, diameter, height, round radius, round the top too, expected volume, expected faces
    ('cup', 60, 80, 1.5, True, 226014.67, 5),
    ('cup-bottom', 60, 80, 1.5, False, 226104.67, 4),
    ('cup-r3', 60, 80, 3, True, 225482.81, 5),
    ('cup40', 40, 40, 1, True, 50212.15, 5),
]


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


with open(os.path.join(OUT, 'commands.txt'), 'w') as f:
    for flt in ('solid.shell', 'solid.fillet', 'solid.extrude', 'sketch.circle', 'model.faces'):
        f.write(f'== list_commands {flt}\n' + McpClient.text(c.call_tool('list_commands', {'filter': flt})) + '\n\n')

bad = 0
for name, d, h, rr, top, want, nfaces in CUPS:
    jt('new_design', {})
    edges = [[d / 2, 0, 0]] + ([[d / 2, 0, h]] if top else [])
    err, r = jt('batch', {'verbose': False, 'commands': [
        {'command': 'sketch.create', 'params': {'plane': 'XY'}},
        {'command': 'sketch.circle.center', 'params': {'center': [0, 0], 'diameter': d}},
        {'command': 'sketch.finish', 'params': {}},
        {'command': 'solid.extrude', 'params': {'distance': h}},
        {'command': 'solid.fillet', 'params': {'edges': edges, 'radius': rr}}]})
    out(f'{name}: batch isError {err}; ' + json.dumps(r)[:500])
    path = os.path.expanduser(f'~/{name}.sc')
    err, r = jt('save', {'path': path})
    out(f'save {name}.sc: isError {err}; ' + json.dumps(r)[:200])
    jt('new_design', {})
    err, r = jt('open', {'path': path})
    out(f'reopen {name}.sc: isError {err}')
    _, m = jt('measure', {})
    bodies = m.get('bodies') or []
    vol = (m.get('total') or {}).get('volume_mm3')
    bname = bodies[0]['name'] if bodies else 'Body1'
    _, fl = jt('execute', {'command': 'model.faces', 'params': {'body': bname}})
    json.dump(fl, open(os.path.join(OUT, f'faces-{name}.json'), 'w'), indent=1)
    faces = fl.get('faces') if isinstance(fl, dict) else None
    nf = len(faces) if isinstance(faces, list) else None
    ok = vol is not None and abs(vol - want) <= want * 0.001
    out(f'CHECK {name}: volume {vol} expected {want} ({len(bodies)} bodies, {bname}); faces {nf} expected {nfaces}'
        f' -> {"OK" if ok else "MISMATCH (P0)"}{"" if nf == nfaces else " (face count differs: logged)"}')
    bad += 0 if ok else 1
c.close()
sys.exit(3 if bad else 0)
