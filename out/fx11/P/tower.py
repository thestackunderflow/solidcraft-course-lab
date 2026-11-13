"""fx11 take P (LAB-fx11 section 3, not filmed): the start files, no AI, over the plug entry SolidCraft wrote
(lesson-7 client pattern, as out/fx10/P/knob.py):
  ~/tower.sc      circle 40 on XY, Extrude 200 up (z 0..200); sketch on the top face, circle 30 concentric, Extrude cut
                  195 down (bore, 5 mm floor z 0..5). Expected 113,490.03 mm3 (ACCURACY B.6)
  ~/tower-sym.sc  the same, the 40 extrude Symmetric about XY (z -100..100), the bore 195 down from the top (z 100..-95)
  ~/block.sc      rectangle 20 x 20 on XY, Extrude 80 up. Expected 32,000 mm3
Each file is saved, reopened and its volume read back into OUT/volumes.txt; a mismatch over 0.1% = P0 stop (exit 3).
    FX9_ALLOW=1 python3 -I tower.py OUT_DIR
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
EXPECT = {'tower': 113490.03, 'tower-sym': 113490.03, 'block': 32000.0}


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


def batch(tag, cmds):
    err, r = jt('batch', {'commands': cmds, 'verbose': False})
    out(f'{tag}: isError {err}; ' + json.dumps(r)[:600])


def read(tag):
    _, m = jt('measure', {})
    _, d = jt('inspect_design', {})
    json.dump({'measure': m, 'design': d}, open(os.path.join(OUT, f'read-{tag}.json'), 'w'), indent=1)
    bodies = (m.get('bodies') or []) if isinstance(m, dict) else []
    vol = (m.get('total') or {}).get('volume_mm3') if isinstance(m, dict) else None
    out(f'{tag}: volume_mm3 {vol} bodies {[b.get("name") for b in bodies]} '
        f'bbox {json.dumps([b.get("bbox") or b.get("bounding_box") for b in bodies])} '
        f'timeline {json.dumps([f.get("name") or f.get("type") for f in (d.get("timeline") or [])]) if isinstance(d, dict) else d}')
    return vol


def tower(sym):
    jt('new_design', {})
    first = {'distance': 200, 'body_name': 'Tower'}
    if sym:
        first['direction'] = 'symmetric'
    top = 100 if sym else 200
    batch('tower-sym' if sym else 'tower', [
        {'command': 'sketch.create', 'params': {'plane': 'XY'}},
        {'command': 'sketch.circle.center', 'params': {'center': [0, 0], 'diameter': 40}},
        {'command': 'sketch.finish', 'params': {}},
        {'command': 'solid.extrude', 'params': first},
        {'command': 'sketch.create', 'params': {'plane': {'face': [0, 0, top]}}},
        {'command': 'sketch.circle.center', 'params': {'center': [0, 0], 'diameter': 30}},
        {'command': 'sketch.finish', 'params': {}},
        {'command': 'solid.extrude', 'params': {'distance': 195, 'direction': 'negative', 'operation': 'cut'}}])


def block():
    jt('new_design', {})
    batch('block', [
        {'command': 'sketch.create', 'params': {'plane': 'XY'}},
        {'command': 'sketch.rectangle.two_point', 'params': {'p0': [-10, -10], 'p1': [10, 10]}},
        {'command': 'sketch.finish', 'params': {}},
        {'command': 'solid.extrude', 'params': {'distance': 80, 'body_name': 'Block'}}])


bad = 0
for name, make in (('tower', lambda: tower(False)), ('tower-sym', lambda: tower(True)), ('block', block)):
    make()
    v0 = read(f'{name}-made')
    path = os.path.expanduser(f'~/{name}.sc')
    err, r = jt('save', {'path': path})
    out(f'save {name}.sc: isError {err}; ' + json.dumps(r)[:200])
    jt('new_design', {})
    err, r = jt('open', {'path': path})
    out(f'reopen {name}.sc: isError {err}')
    v = read(f'{name}-reopened')
    ok = isinstance(v, (int, float)) and abs(v - EXPECT[name]) / EXPECT[name] <= 0.001
    out(f'CHECK {name}: reopened {v} expected {EXPECT[name]} -> {"OK" if ok else "MISMATCH (P0)"}')
    bad += 0 if ok else 1
c.close()
sys.exit(3 if bad else 0)
