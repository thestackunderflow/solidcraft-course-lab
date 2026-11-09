"""fx8 (LAB-fx8 take P and read-only reads), over the plug entry SolidCraft wrote, into the open window, no AI.
    python3 lab/fx8part.py prep OUT_DIR       take P: lesson 3's hook -> ~/hook-l3.sc + Save As Mesh ~/hook-plain.stl;
                                              lesson 4's hook (l5part.HOLES_FILLET on it) -> ~/hook-l4.sc + ~/hook.stl;
                                              a 40 x 40 x 20 box, four upright edges filleted 5 -> ~/box-round.stl;
                                              then a new empty design. Writes OUT_DIR/prep.json, counts.txt, settings.txt
    python3 lab/fx8part.py read OUT_DIR TAG   read only: measure + inspect_design (timeline); OUT_DIR/read-TAG.json
    python3 lab/fx8part.py open OUT_DIR FILE  (stop rule A3 only) open FILE over the plug
Prints one line."""
import json
import os
import struct
import sys

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402
from l7story import HOOK  # noqa: E402
from l5part import HOLES_FILLET  # noqa: E402

HOME = os.path.expanduser('~')
BOX = [{'command': 'solid.box', 'params': {'length': 40, 'width': 40, 'height': 20}},
       {'command': 'solid.fillet', 'params': {'edges': [[0, 0, 10], [40, 0, 10], [0, 40, 10], [40, 40, 10]], 'radius': 5}}]


def stl_triangles(path):
    """Binary STL: 80-byte header, then a little-endian uint32 triangle count."""
    with open(path, 'rb') as f:
        f.seek(80)
        return struct.unpack('<I', f.read(4))[0]


def client(o, tag):
    if os.environ.get('FX8_ENTRY'):     # the entry as SolidCraft wrote it (R1 wraps ~/.claude.json in a logging proxy)
        e = json.load(open(os.environ['FX8_ENTRY']))['mcpServers']['solidcraft']
        e = {'command': e['command'], 'args': [a for a in e.get('args') or [] if a not in ('--allow-path', HOME)]}
    else:
        e = entry.read(os.path.expanduser('~/.claude.json'))
    c = McpClient([e['command']] + e['args'] + ['--allow-path', HOME], timeout_s=120,
                  log_path=os.path.join(o, f'part-{tag}-transcript.jsonl'))
    c.start()
    return c


def jt(c, name, args):
    s = McpClient.text(c.call_tool(name, args)).split('\nNote:')[0]
    try:
        return json.loads(s)
    except ValueError:
        return {'text': s}


def summary(m, d):
    bodies = [(b.get('name'), round(b.get('volume_mm3') or 0, 2), (b.get('face_types') or {})) for b in m.get('bodies') or []]
    tl = [(f.get('name') or f.get('type'), f.get('type')) for f in (d.get('timeline') or [])] if isinstance(d, dict) else []
    return {'bodies': bodies, 'timeline': tl}


def main():
    mode, o = sys.argv[1], sys.argv[2]
    os.makedirs(o, exist_ok=True)
    if mode == 'prep':
        c = client(o, 'prep')
        res = {'l3': jt(c, 'batch', {'commands': HOOK, 'verbose': False}).get('ok')}
        res['save_l3'] = jt(c, 'execute', {'command': 'file.save', 'params': {'path': HOME + '/hook-l3.sc'}})
        res['mesh_l3'] = jt(c, 'execute', {'command': 'file.save_mesh', 'params': {'path': HOME + '/hook-plain.stl'}})
        res['measure_l3'] = jt(c, 'measure', {}).get('total')
        res['l4'] = jt(c, 'batch', {'commands': HOLES_FILLET, 'verbose': False}).get('ok')
        res['save_l4'] = jt(c, 'execute', {'command': 'file.save', 'params': {'path': HOME + '/hook-l4.sc'}})
        res['mesh_l4'] = jt(c, 'execute', {'command': 'file.save_mesh', 'params': {'path': HOME + '/hook.stl'}})
        res['measure_l4'] = jt(c, 'measure', {}).get('total')
        jt(c, 'new_design', {})
        res['box'] = jt(c, 'batch', {'commands': BOX, 'verbose': False}).get('ok')
        res['mesh_box'] = jt(c, 'execute', {'command': 'file.save_mesh', 'params': {'path': HOME + '/box-round.stl'}})
        res['measure_box'] = jt(c, 'measure', {}).get('total')
        jt(c, 'new_design', {})
        c.close()
        json.dump(res, open(os.path.join(o, 'prep.json'), 'w'), indent=1)
        with open(os.path.join(o, 'counts.txt'), 'w') as f:
            for n in ('hook-plain', 'hook', 'box-round'):
                p = f'{HOME}/{n}.stl'
                f.write(f'{n}.stl  triangles {stl_triangles(p)}  bytes {os.path.getsize(p)}\n')
        with open(os.path.join(o, 'settings.txt'), 'w') as f:
            f.write('Exporter: Save As Mesh (file.save_mesh, the toolbar command), format from the .stl extension = binary STL.\n'
                    'file.save_mesh in 0.28.0 has no quality/tolerance option (params: path, format, bodies, ascii, slicer...),\n'
                    'so every file is the default ("standard") tessellation.\n')
        print('prep', json.dumps({k: res[k] for k in ('l3', 'l4', 'box')}), open(os.path.join(o, 'counts.txt')).read().replace('\n', '; '))
        return
    if mode == 'both':     # take C set-up: a new design, both hook STLs inserted, the drilled one moved 40 mm along +y
        c = client(o, 'both')
        res = {'new': jt(c, 'new_design', {})}
        for n in ('hook-plain', 'hook'):
            res[n] = jt(c, 'execute', {'command': 'file.insert_mesh', 'params': {'path': f'{HOME}/{n}.stl'}})
        res['move'] = jt(c, 'execute', {'command': 'solid.move', 'params': {'bodies': ['hook'], 'translate': [0, 40, 0]}})
        jt(c, 'execute', {'command': 'view.home', 'params': {}})
        m, d = jt(c, 'measure', {}), jt(c, 'inspect_design', {})
        c.close()
        json.dump({'setup': res, 'measure': m, 'design': d}, open(os.path.join(o, 'read-both-setup.json'), 'w'), indent=1)
        print('both', json.dumps(res['move'])[:200], json.dumps(summary(m, d)))
        return
    tag = sys.argv[3] if mode == 'read' else 'open-' + os.path.basename(sys.argv[3])
    c = client(o, tag)
    if mode == 'open':
        r = jt(c, 'open', {'path': sys.argv[3]})
        print('open', json.dumps(r)[:300])
    m, d = jt(c, 'measure', {}), jt(c, 'inspect_design', {})
    c.close()
    json.dump({'measure': m, 'design': d}, open(os.path.join(o, f'read-{tag}.json'), 'w'), indent=1)
    print(tag, json.dumps(summary(m, d)))


main()
