"""Lesson 4: a no-AI read of the open design over the entry SolidCraft wrote: measure, body_topology and
parameters.list, summarised as holes (bores along X: diameter, height, distance to each side, centred or not), fillet
faces (round faces along the width) and which hole sizes are written from names. Read-only: it changes nothing.
    python3 lab/l4read.py OUT.json [ENTRY_JSON]"""
import json
import os
import sys

sys.path.insert(0, '/work')

TOL = 0.01


def _body(m):
    b = (m.get('bodies') or [{}])[0]
    return b.get('volume_mm3'), (b.get('bbox') or {}).get('min'), (b.get('bbox') or {}).get('max')


def _along(axis, k):
    return abs(abs(axis[k]) - 1.0) < 1e-6


def summarise(meas, topo, plist):
    vol, lo, hi = _body(meas)
    lo = [round(x, 6) for x in (lo or [0, 0, 0])]
    hi = [round(x, 6) for x in (hi or [0, 0, 0])]
    mid_y = (lo[1] + hi[1]) / 2.0
    holes, fillets = {}, []
    for f in (topo or {}).get('faces') or []:
        cyl = f.get('cylinder')
        if not cyl:
            continue
        ax, o, rad = cyl['axis'], cyl['origin'], cyl['radius']
        if _along(ax, 0):                      # a bore through the plate (the plate's thickness is along X)
            key = (round(o[1], 3), round(o[2], 3), round(rad, 4))
            holes.setdefault(key, {'y': round(o[1], 4), 'z': round(o[2], 4), 'diameter': round(2 * rad, 6), 'faces': 0})
            holes[key]['faces'] += 1
        elif _along(ax, 1):                    # a round face along the width: a fillet on an edge across the hook
            fillets.append({'radius': round(rad, 6), 'x': round(o[0], 4), 'z': round(o[2], 4), 'name': f.get('name')})
    out = []
    for h in sorted(holes.values(), key=lambda h: -h['z']):
        sides = [round(h['y'] - lo[1], 4), round(hi[1] - h['y'], 4)]
        h.update({'from_sides': sides, 'centred': abs(h['y'] - mid_y) <= TOL})
        out.append(h)
    top = [f for f in fillets if f['z'] > hi[2] - 5.0]
    return {'volume_mm3': vol, 'bbox_min': lo, 'bbox_max': hi,
            'bbox_mm': [round(hi[i] - lo[i], 4) for i in range(3)], 'holes': out, 'fillets': fillets,
            'top_edges_rounded': len(top), 'hole_params': hole_params(plist)}


def hole_params(plist):
    ps = (plist or {}).get('parameters') or []
    user = {p['name'] for p in ps if str(p.get('source', '')).startswith('user')}
    diam, dist = {}, {}
    for p in ps:
        feat, inp, ex = p.get('feature'), str(p.get('input') or ''), str(p.get('expression') or '')
        if not feat or 'hole' not in str(feat).lower():
            continue
        if inp.lower().startswith('diameter'):
            diam[feat] = ex
        elif 'distance' in inp.lower():
            dist[feat] = dist.get(feat, False) or ('width' in ex)
    return {'hole_d_parameter': 'hole_d' in user, 'user_parameters': sorted(user), 'diameters': diam,
            'distances_from_width': dist}


def read(client):
    from client.mcp import McpClient
    m = McpClient.text_json(client.call_tool('measure', {}))
    bodies = [b.get('name') for b in m.get('bodies') or []]
    t = McpClient.text_json(client.call_tool('body_topology', {'body': bodies[0]})) if bodies else {}
    pl = McpClient.text_json(client.call_tool('execute', {'command': 'parameters.list', 'params': {}}))
    return {'summary': summarise(m, t, pl if isinstance(pl, dict) else {}), 'measure': m, 'body_topology': t,
            'parameters_list': pl}


def main(out, entry_json=None):
    from checker import entry
    from client.mcp import McpClient
    if entry_json:
        e = json.load(open(entry_json))['mcpServers']['solidcraft']
        cmd = [e['command']] + list(e.get('args') or [])
    else:
        e = entry.read(os.path.expanduser('~/.claude.json'))
        cmd = [e['command']] + e['args']
    c = McpClient(cmd, timeout_s=120, log_path=out.replace('.json', '-transcript.jsonl'))
    c.start()
    res = read(c)
    c.close()
    json.dump(res, open(out, 'w'), indent=1)
    s = res['summary']
    print(json.dumps({k: s[k] for k in ('volume_mm3', 'bbox_mm', 'holes', 'top_edges_rounded', 'hole_params')}))
    return res


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
