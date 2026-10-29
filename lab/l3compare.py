"""L3-Q6: every lesson 3 part scored by the rules written before the runs (out/l3/prereg.json): names used, the edit
followed, the edit by parameter, and how "40 deep" was read. Inputs: the no-AI reads (read.json) and, for Claude's
runs, the logged tool calls (transcript.jsonl) split into turns by the run's events.jsonl.
    python3 lab/l3compare.py            -> out/l3/compare.json"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from checker import outline  # noqa: E402

L3 = os.path.join(HERE, '..', 'out', 'l3')
SIZES40 = {'plate_height': 60, 'width': 20, 'thickness': 5, 'hook_depth': 40, 'lip_height': 10}
EDIT_CMDS = ('parameters.change', 'set_parameter')


def corners40():
    return sorted({(float(x), float(y)) for x, y in outline.walk(outline.j_moves(SIZES40))})


def _corner_sets(summary):
    """The sketch's corner points as 2D sets, with the sketch's second axis either way up (the plug's XZ has up -Z)."""
    pts = [tuple(c[:2]) for c in summary.get('corners') or []]
    return [sorted(pts), sorted((x, -y) for x, y in pts)]


def edit_followed(s):
    exp = corners40()
    ok_c = any(len(c) == len(exp) and all(abs(a[0] - b[0]) <= 0.01 and abs(a[1] - b[1]) <= 0.01 for a, b in zip(c, exp))
               for c in _corner_sets(s))
    z = (s.get('bbox_min') or [0, 0, None])[2], (s.get('bbox_max') or [0, 0, None])[2]
    vol = s.get('volume_mm3')
    box = s.get('bbox_mm') or []
    res = {'corners': ok_c, 'z_0_60': z == (0.0, 60.0), 'volume_10000': vol is not None and abs(vol - 10000) <= 0.1,
           'box_40_20_60': len(box) == 3 and all(abs(a - b) <= 0.01 for a, b in zip(box, (40, 20, 60)))}
    res['all'] = all(res.values())
    return res


def names_used(s):
    user = s.get('user_parameter_names') or []
    return {'user_parameters': len(user), 'names': user, 'sizes_written_from_names': s.get('model_parameters_from_names', 0),
            'of_sizes': len(s.get('model_parameters') or [])}


def calls_by_turn(run_dir):
    ev = [json.loads(x) for x in open(os.path.join(run_dir, 'events.jsonl'), encoding='utf-8') if x.strip()]
    t2 = next(e['t'] for e in ev if e['event'] == 'turn 2: Enter')
    seq_t = {e.get('seq'): e['t'] for e in ev if e['event'].startswith('tool call:')}
    turns = {1: [], 2: []}
    for line in open(os.path.join(run_dir, 'transcript.jsonl'), encoding='utf-8'):
        r = json.loads(line)
        m = r.get('msg')
        if isinstance(m, dict) and r.get('dir') == 'client->server' and m.get('method') == 'tools/call':
            t = seq_t.get(r.get('seq'))
            p = m.get('params') or {}
            turns[2 if t is not None and t > t2 else 1].append({'seq': r.get('seq'), 'name': p.get('name'),
                                                                 'arguments': p.get('arguments')})
    return turns


def commands(call):
    a = call.get('arguments') or {}
    if call['name'] == 'batch':
        return [c.get('command') for c in a.get('commands') or []]
    if call['name'] == 'execute':
        return [a.get('command')]
    return [call['name']]


def edit_kind(turn2):
    cmds = [c for call in turn2 for c in commands(call)]
    by_param = any(c in EDIT_CMDS for c in cmds)
    redraw = any(c and c.startswith('sketch.') for c in cmds)
    fresh = any(c == 'new_design' for c in cmds)
    if by_param and not redraw:
        kind = 'one parameter change'
    elif fresh and redraw:
        kind = 'drew it again in a new design'
    elif redraw:
        kind = 'moved sketch points'
    else:
        kind = 'other'
    return {'kind': kind, 'by_parameter': by_param and not redraw, 'commands': cmds}


def reading(s):
    box = s.get('bbox_mm') or [None]
    if box[0] is not None and abs(box[0] - 40) <= 0.01:
        return 'outside depth 40 (box 40)'
    if box[0] is not None and abs(box[0] - 45) <= 0.01:
        return 'arm 40 (box 45)'
    return f'other (box {box})'


def main():
    out = {'prereg': json.load(open(os.path.join(L3, 'prereg.json'))), 'parts': {}}
    for name in ('hand', 'plain'):
        s = json.load(open(os.path.join(L3, name, 'read.json')))['summary']
        out['parts'][name] = {'names_used': names_used(s), 'edit_followed': edit_followed(s), 'reading': reading(s),
                              'volume_mm3': s['volume_mm3'], 'bbox_mm': s['bbox_mm']}
    ar = os.path.join(L3, 'plain', 'after-refusal', 'read.json')
    if os.path.exists(ar):
        a = json.load(open(ar))
        d1 = next(p for p in a['parameters_list']['parameters'] if p['name'] == 'd1')
        out['parts']['plain']['after_refusal'] = {'d1_expression': d1['expression'], 'd1_value': d1['value'],
                                                  'volume_mm3': a['summary']['volume_mm3'], 'bbox_mm': a['summary']['bbox_mm']}
        out['parts']['plain']['refused_constraints'] = [
            {k: c.get(k) for k in ('id', 'type', 'param', 'expression', 'l')}
            for c in (a['inspect_design']['sketches'][0].get('constraints') or [])
            if c.get('id') in ('k2', 'k3', 'k6', 'k7', 'k10', 'k11', 'k14', 'k15')]
    runs = os.path.join(L3, 'runs')
    for r in sorted(os.listdir(runs)) if os.path.isdir(runs) else []:
        d = os.path.join(runs, r)
        if not os.path.exists(os.path.join(d, 'read.json')):
            continue
        s = json.load(open(os.path.join(d, 'read.json')))['summary']
        t = calls_by_turn(d)
        out['parts'][r] = {'asked_for_names': r.startswith('B'), 'names_used': names_used(s), 'edit_followed': edit_followed(s),
                           'edit': edit_kind(t[2]), 'reading': reading(s), 'volume_mm3': s['volume_mm3'], 'bbox_mm': s['bbox_mm'],
                           'bbox_min': s['bbox_min'], 'bbox_max': s['bbox_max'],
                           'turn1_calls': [c['name'] for c in t[1]], 'turn2_calls': [c['name'] for c in t[2]]}
    json.dump(out, open(os.path.join(L3, 'compare.json'), 'w'), indent=1)
    for k, v in out['parts'].items():
        print(k, json.dumps({x: v.get(x) for x in ('names_used', 'edit_followed', 'edit', 'reading')}))
    return out


if __name__ == '__main__':
    main()
