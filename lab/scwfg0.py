"""scwf Gate 0 (8-9 Nov 2026, $0, no AI): the full command set on SolidCraft 0.30.1 over the plug, every reply kept
(out/scwf/G0/g0.json) and checked against the keys the course's readers used (measure.total.volume_mm3,
bodies[].bbox, set_parameter value). Starts from lab/scwfpart.py build (the bracket, flip: true).
    python3 lab/scwfg0.py OUT_DIR"""
import json, os, sys
sys.path.insert(0, '/work'); sys.path.insert(0, '/work/lab')
from scwfpart import client, jt, SHAPE  # noqa: E402
HOME = os.path.expanduser('~')
o = sys.argv[1]
HOLES = [{'command': 'set_parameter', 'params': {'name': 'hole_d', 'value': 4}}] + [
    {'command': 'solid.hole', 'params': {'position': [x, -12.5, 30], 'diameter': 'hole_d', 'references': [
        {'edge': [0, -5, 30], 'distance': str(x)}, {'edge': [25, 0, 30], 'distance': 'width / 2'}]}} for x in (12, 38)]
FILLET = [{'command': 'solid.fillet', 'params': {'edges': [[4, -12.5, 26]], 'radius': 3}}]
c = client(o, 'g0')
R = {}
def step(k, name, args):
    R[k] = jt(c, name, args); return R[k]
def vol():
    m = jt(c, 'measure', {}); b = m['bodies'][0]
    return {'volume_mm3': round(m['total']['volume_mm3'], 2), 'bbox': b['bbox'], 'faces': b.get('faces'), 'face_types': b.get('face_types')}
def holes():   # cylinder faces' centres, from body_topology
    t = jt(c, 'body_topology', {'body': 'Body1'})
    cyl = [f for f in (t.get('faces') or []) if 'cyl' in json.dumps(f).lower()]
    return [{k: f.get(k) for k in ('id', 'type', 'center', 'axis', 'radius', 'centroid', 'origin') if k in f} for f in cyl]
step('new', 'new_design', {})
step('shape', 'batch', {'commands': SHAPE, 'verbose': False}); R['m_shape'] = vol()
step('holes', 'batch', {'commands': HOLES, 'verbose': False}); R['m_holes'] = vol(); R['holes_25'] = holes()
step('plist', 'execute', {'command': 'parameters.list', 'params': {}})
step('w35', 'execute', {'command': 'parameters.change', 'params': {'name': 'width', 'value': 35}}); R['m_35'] = vol(); R['holes_35'] = holes()
step('w25', 'execute', {'command': 'parameters.change', 'params': {'name': 'width', 'value': 25}}); R['m_25b'] = vol()
step('fillet', 'batch', {'commands': FILLET, 'verbose': False}); R['m_fillet'] = vol()
step('save', 'execute', {'command': 'file.save', 'params': {'path': HOME + '/bracket.sc'}})
step('mesh', 'execute', {'command': 'file.save_mesh', 'params': {'path': HOME + '/bracket.stl'}})
step('view', 'execute', {'command': 'view.home', 'params': {}})
c.close()
json.dump(R, open(os.path.join(o, 'g0.json'), 'w'), indent=1)
for k in ('m_shape', 'm_holes', 'm_35', 'm_25b', 'm_fillet'):
    print(k, R[k]['volume_mm3'], R[k]['bbox'])
print('holes_25', json.dumps(R['holes_25'])[:400]); print('holes_35', json.dumps(R['holes_35'])[:400])
print('plist', json.dumps(R['plist'])[:500]); print('w35', json.dumps(R['w35'])[:300])
print('ok', {k: (R[k].get('ok') if isinstance(R[k], dict) else None) for k in ('shape', 'holes', 'fillet', 'save', 'mesh')})
