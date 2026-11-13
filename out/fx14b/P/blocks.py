"""fx14b take P (LAB-fx14b section 3, not filmed): the start files, no AI, over the plug entry SolidCraft wrote
(lesson-7 client pattern, as out/fx13/P/cups.py). The converted files repeat G0d's recipe exactly (out/fx14/G0/g0.py):
rectangle on XY, Extrude New Body, file.save_mesh to an STL, new_design, file.insert_mesh, mesh.convert.
  ~/conv.sc    40 x 30 x 20 (corner at the origin), converted      expected 24,000.00 mm3
  ~/conv2.sc, ~/conv3.sc  file copies of conv.sc (takes C and Q23)  expected 24,000.00
  ~/block.sc   40 x 30 x 20, plain Extrude, NOT converted (Q21)     expected 24,000.00
  ~/conv30.sc  30 x 30 x 10, converted (Q26, the your-turn block)    expected  9,000.00
  ~/offset.sc  40 x 30 on XY, Extrude New Body 20, start_offset 5    expected 24,000.00, top at z 25 (Q28)
Each file is reopened and its volume (measure) read back into OUT/volumes.txt; faces (model.faces) into
OUT/faces-NAME.json (conv and block also into OUT/faces.txt). A volume off by more than 0.1% = P0 stop (exit 3).
Command and parameter names: out/fx14/G0/commands.json (re-read and logged into OUT/commands.txt).
    python3 -I blocks.py OUT_DIR          (every JSON-RPC message -> OUT/rpc.jsonl)"""
import json
import os
import shutil
import sys

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

OUT = sys.argv[1]
H = os.path.expanduser('~')
e = entry.read(os.path.expanduser('~/.claude.json'))
c = McpClient([e['command']] + e['args'] + ['--allow-path', H], timeout_s=180, log_path=os.path.join(OUT, 'rpc.jsonl'))
c.start()
log = open(os.path.join(OUT, 'volumes.txt'), 'w')
flog = open(os.path.join(OUT, 'faces.txt'), 'w')


def jt(name, args):
    r = c.call_tool(name, args)
    s = McpClient.text(r).split('\nNote:')[0]
    try:
        return bool(r.get('isError')), json.loads(s)
    except ValueError:
        return bool(r.get('isError')), {'text': s}


def ex(cmd, params):
    err, r = jt('execute', {'command': cmd, 'params': params, 'verbose': False})
    out(f'  {cmd} {json.dumps(params)}: isError {err}; ' + json.dumps(r)[:400])
    return err, r


def out(line):
    print(line, flush=True)
    log.write(line + '\n')


def bodies():
    _, m = jt('measure', {})
    return m.get('bodies') or [], (m.get('total') or {}).get('volume_mm3')


def block(w, d, h, start_offset=None):
    jt('new_design', {})
    ex('sketch.create', {'plane': 'XY'})
    ex('sketch.rectangle.two_point', {'p0': [0, 0], 'p1': [w, d]})
    ex('sketch.finish', {})
    p = {'distance': h, 'operation': 'new'}
    if start_offset is not None:
        p['start_offset'] = start_offset
    ex('solid.extrude', p)


def convert(stl):
    ex('file.save_mesh', {'path': f'{H}/{stl}.stl'})
    jt('new_design', {})
    ex('file.insert_mesh', {'path': f'{H}/{stl}.stl'})
    bs, _ = bodies()
    ex('mesh.convert', {'body': bs[0]['name']} if bs else {})


def save(name):
    err, r = jt('save', {'path': f'{H}/{name}.sc'})
    out(f'save {name}.sc: isError {err}; ' + json.dumps(r)[:200])


with open(os.path.join(OUT, 'commands.txt'), 'w') as f:
    for flt in ('sketch.create', 'solid.extrude', 'file.save_mesh', 'file.insert_mesh', 'mesh.convert', 'model.faces',
                'solid.hole', 'sketch.circle.center'):
        f.write(f'== list_commands {flt}\n' + McpClient.text(c.call_tool('list_commands', {'filter': flt})) + '\n\n')

out('== conv: 40 x 30 x 20, Save As Mesh -> Insert Mesh -> Convert Mesh (G0d recipe)')
block(40, 30, 20); convert('conv'); save('conv')
shutil.copy(f'{H}/conv.sc', f'{H}/conv2.sc'); shutil.copy(f'{H}/conv.sc', f'{H}/conv3.sc')
out('conv2.sc, conv3.sc: file copies of conv.sc')
out('== block: 40 x 30 x 20, plain Extrude (control)')
block(40, 30, 20); save('block')
out('== conv30: 30 x 30 x 10, converted (your turn)')
block(30, 30, 10); convert('conv30'); save('conv30')
out('== offset: 40 x 30 on XY, Extrude 20 with start_offset 5')
block(40, 30, 20, start_offset=5); save('offset')

EXPECT = [('conv', 24000.0, 20), ('conv2', 24000.0, 20), ('conv3', 24000.0, 20), ('block', 24000.0, 20),
          ('conv30', 9000.0, 10), ('offset', 24000.0, 25)]
bad = 0
for name, want, ztop in EXPECT:
    jt('new_design', {})
    err, r = jt('open', {'path': f'{H}/{name}.sc'})
    out(f'reopen {name}.sc: isError {err}')
    bs, vol = bodies()
    bname = bs[0]['name'] if bs else None
    zmax = bs[0]['bbox']['max'][2] if bs and bs[0].get('bbox') else None
    _, fl = jt('execute', {'command': 'model.faces', 'params': {'body': bname}})
    json.dump(fl, open(os.path.join(OUT, f'faces-{name}.json'), 'w'), indent=1)
    faces = fl.get('faces') if isinstance(fl, dict) else None
    top = [f for f in faces or [] if abs((f.get('centroid') or [0, 0, -1])[2] - ztop) < 1e-6]
    if name in ('conv', 'block', 'conv30', 'offset'):
        flog.write(f'== {name}.sc body {bname}\n')
        for f in faces or []:
            flog.write(f"  {f.get('name')} exact {f.get('exact')} area {f.get('area')} centroid {f.get('centroid')}\n")
        flog.write(f"  TOP (z {ztop}): {[(f.get('name'), f.get('exact')) for f in top]}\n")
    ok = vol is not None and abs(vol - want) <= want * 0.001
    out(f'CHECK {name}: volume {vol} expected {want} ({len(bs)} bodies, {bname}, top z {zmax}); '
        f'top face {[(f.get("name"), f.get("exact")) for f in top]} -> {"OK" if ok else "MISMATCH (P0)"}')
    bad += 0 if ok else 1
c.close()
sys.exit(3 if bad else 0)
