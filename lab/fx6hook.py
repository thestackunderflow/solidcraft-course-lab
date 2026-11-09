"""fx6: lesson 3's hook (lab/l7story.py HOOK, 8,500 mm3) built with no AI over the entry SolidCraft wrote, into the open
window, then saved as ~/hook-l3.sc; or a read-only look at the open design (faces of the lip, measured from the body).
    python3 lab/fx6hook.py build OUT_DIR       build + save ~/hook-l3.sc + view.home; writes OUT_DIR/hook-setup.json
    python3 lab/fx6hook.py read OUT_DIR TAG    read only: measure + body_topology; writes OUT_DIR/read-TAG.json
Prints one line: volume and the lip's faces (top face across in x, front face height in z)."""
import json
import os
import sys

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402
from l7story import HOOK  # noqa: E402

HOME = os.path.expanduser('~')


def faces_summary(topo):
    """One row per face: index, name, centroid, plane normal (None = curved), area."""
    return [{'index': f.get('index'), 'name': f.get('name'), 'centroid': [round(x, 3) for x in f.get('centroid') or []],
             'normal': f.get('plane_normal'), 'area': round(f.get('area') or 0, 3)} for f in (topo or {}).get('faces') or []]


WIDTH = 20.0   # the extrude distance (HOOK: width 20): a side face's size across = its area / 20


def lip(topo):
    """The lip's faces, from body_topology: the top face (normal +z, the face of largest x below z 30) and the outer front
    face (normal +x, largest x below z 30). Sizes across = area / width (both are rectangles 20 mm long)."""
    up, front, curved = [], [], 0
    for f in (topo or {}).get('faces') or []:
        n, c = f.get('plane_normal'), f.get('centroid') or [0, 0, 99]
        if not n:
            curved += 1
            continue
        if c[2] < 30 and abs(n[2] - 1) < 1e-6:
            up.append(f)
        if c[2] < 30 and abs(n[0] - 1) < 1e-6:
            front.append(f)
    res = {'faces': len((topo or {}).get('faces') or []), 'curved_faces': curved}
    if up:
        t = max(up, key=lambda f: f['centroid'][0])
        res['lip_top_face_mm'] = round(t['area'] / WIDTH, 4)
        res['lip_top_centroid'] = [round(x, 3) for x in t['centroid']]
    if front:
        t = max(front, key=lambda f: f['centroid'][0])
        res['lip_front_face_mm'] = round(t['area'] / WIDTH, 4)
        res['lip_front_centroid'] = [round(x, 3) for x in t['centroid']]
    return res


def client():
    if os.environ.get('FX6_ENTRY'):     # the entry as SolidCraft wrote it (the R1 run wraps ~/.claude.json in a proxy)
        e = json.load(open(os.environ['FX6_ENTRY']))['mcpServers']['solidcraft']
        return [e['command']] + list(e.get('args') or []) + ['--allow-path', HOME]
    e = entry.read(os.path.expanduser('~/.claude.json'))
    return [e['command']] + e['args'] + ['--allow-path', HOME]


def read(c):
    m = McpClient.text_json(c.call_tool('measure', {}))
    bodies = [b.get('name') or b.get('id') for b in m.get('bodies') or []]
    t = McpClient.text_json(c.call_tool('body_topology', {'body': bodies[0]})) if bodies else {}
    return m, t


def main():
    mode, o = sys.argv[1], sys.argv[2]
    tag = sys.argv[3] if len(sys.argv) > 3 else mode
    c = McpClient(client(), timeout_s=120, log_path=os.path.join(o, f'hook-{tag}-transcript.jsonl'))
    c.start()
    res = {}
    if mode == 'build':
        res['batch'] = McpClient.text_json(c.call_tool('batch', {'commands': HOOK, 'verbose': False}))
        res['save'] = McpClient.text(c.call_tool('execute', {'command': 'file.save', 'params': {'path': HOME + '/hook-l3.sc'}}))
    m, t = read(c)
    if mode == 'build':
        c.call_tool('execute', {'command': 'view.home', 'params': {}})
    c.close()
    res.update({'measure': m, 'lip': lip(t), 'faces': faces_summary(t), 'topology': t})
    json.dump(res, open(os.path.join(o, 'hook-setup.json' if mode == 'build' else f'read-{tag}.json'), 'w'), indent=1)
    print(tag, 'volume', (m.get('total') or {}).get('volume_mm3'), 'lip', json.dumps(res['lip']))


main()
