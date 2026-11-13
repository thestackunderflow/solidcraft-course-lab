"""fx12 take P (LAB-fx12 section 3, not filmed): the start files, no AI, over the plug entry SolidCraft wrote
(lesson-7 client pattern, as out/fx11/P/tower.py):
  ~/tray.sc        sketch on XY: rectangle 60 x 40 centred on the origin (x -30..30, y -20..20), width 60 and height 40
                   dimensioned; ONE Offset of the 4 lines, 2 mm inward (linked). Expected regions: ring 384, inside 2,016
  ~/tray-plain.sc  the 60 x 40 rectangle only (dimensioned), for take C and the your-turn shot. Expected region 2,400
  ~/box.sc         rectangle 50 x 30 only (dimensioned), the F10 your-turn start. Expected region 1,500
Each file is saved, reopened, and its curve ids and region (profile) areas read back into OUT/check.txt; the outline and
copy ids go to OUT/ids.txt. A mismatch = P0 stop (exit 3).
    FX9_ALLOW=1 python3 -I tray.py OUT_DIR
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
log = open(os.path.join(OUT, 'check.txt'), 'w')
EXPECT = {'tray': [384.0, 2016.0], 'tray-plain': [2400.0], 'box': [1500.0]}


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
    out(f'{tag}: isError {err}; ' + json.dumps(r)[:400])
    return r


def rect(w, h):
    return [{'command': 'sketch.create', 'params': {'plane': 'XY'}},
            {'command': 'sketch.rectangle.two_point', 'params': {'p0': [-w / 2, -h / 2], 'p1': [w / 2, h / 2]}},
            {'command': 'sketch.dimension', 'params': {'entities': ['l1'], 'type': 'length', 'value': f'{w} mm'}},
            {'command': 'sketch.dimension', 'params': {'entities': ['l2'], 'type': 'length', 'value': f'{h} mm'}}]


def read(tag):
    _, s = jt('execute', {'command': 'sketch.inspect', 'params': {'sketch': 'Sketch1'}})
    json.dump(s, open(os.path.join(OUT, f'sketch-{tag}.json'), 'w'), indent=1)
    curves = [(x['id'], x['type'], x.get('start_at'), x.get('end_at')) for x in s.get('curves', [])]
    areas = sorted(round(p['area_mm2'], 2) for p in s.get('profiles', []))
    links = s.get('links')
    out(f'{tag}: curves {json.dumps(curves)}; region areas {areas}; links {json.dumps(links)[:300]}')
    return curves, areas


bad = 0
ids = open(os.path.join(OUT, 'ids.txt'), 'w')
for name, w, h, offset in (('tray', 60, 40, True), ('tray-plain', 60, 40, False), ('box', 50, 30, False)):
    jt('new_design', {})
    cmds = rect(w, h)
    if offset:
        cmds.append({'command': 'sketch.offset',
                     'params': {'curves': ['l1', 'l2', 'l3', 'l4'], 'distance': 2, 'side': [0, 0]}})
    r = batch(name, cmds)
    if offset:
        o = (r.get('results') or [{}])[-1]
        ids.write(f'outline l1 l2 l3 l4 (p1 p2 p3 p4 corners at (-30,-20) (30,-20) (30,20) (-30,20))\n'
                  f'offset copy {" ".join(c for sd in (o.get("sides") or []) for c in sd["curves"])}; points {" ".join(o.get("created", {}).get("points", []))};'
                  f' sides {json.dumps(o.get("sides"))}\n')
    jt('execute', {'command': 'sketch.finish', 'params': {}})
    made = read(f'{name}-made')
    path = os.path.expanduser(f'~/{name}.sc')
    err, r = jt('save', {'path': path})
    out(f'save {name}.sc: isError {err}; ' + json.dumps(r)[:200])
    jt('new_design', {})
    err, r = jt('open', {'path': path})
    out(f'reopen {name}.sc: isError {err}')
    back = read(f'{name}-reopened')
    ok = back[1] == sorted(EXPECT[name]) and [x[0] for x in back[0]] == [x[0] for x in made[0]]
    out(f'CHECK {name}: regions {back[1]} expected {sorted(EXPECT[name])}, ids kept {[x[0] for x in back[0]]}'
        f' -> {"OK" if ok else "MISMATCH (P0)"}')
    bad += 0 if ok else 1
ids.close()
c.close()
sys.exit(3 if bad else 0)
