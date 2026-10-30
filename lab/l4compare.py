"""L4-Q7: lesson 4's parts scored by the rules written before the Claude runs (out/l4/prereg.json): names used, the
build right after message 1, the part after message 2 (30 wide), the change by parameter, and the logged hole calls.
Inputs: the no-AI reads (read-*.json, l4read.py) and each run's logged tool calls split into turns by events.jsonl.
    python3 lab/l4compare.py            -> out/l4/compare.json"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
L4 = os.path.join(HERE, '..', 'out', 'l4')
VOL20, VOL30 = 8306.62, 12539.44
EDIT_CMDS = ('parameters.change', 'set_parameter')


def _near(a, b, tol):
    return a is not None and abs(a - b) <= tol


def _holes_ok(s):
    hs = s.get('holes') or []
    return (len(hs) == 2 and all(abs(h['diameter'] - 4.5) <= 0.02 for h in hs)
            and sorted(round(h['z'] - (s.get('bbox_min') or [0, 0, 0])[2], 2) for h in hs) == [15.0, 45.0])


def build_right(s, width=20):
    res = {'two_holes_4_5_at_15_45': _holes_ok(s),
           'holes_centred': bool(s.get('holes')) and all(h['centred'] for h in s['holes']),
           'two_top_fillets_r2': s.get('top_edges_rounded') == 2 and all(abs(f['radius'] - 2) <= 0.01 for f in s.get('fillets') or []),
           'volume': _near(s.get('volume_mm3'), VOL20 if width == 20 else VOL30, 0.5)}
    res['all'] = all(res.values())
    return res


def after_change(s):
    box = s.get('bbox_mm') or []
    res = {'box_25_30_60': len(box) == 3 and all(abs(a - b) <= 0.01 for a, b in zip(box, (25, 30, 60))),
           'two_holes_4_5_at_15_45': _holes_ok(s),
           'holes_centred': bool(s.get('holes')) and all(h['centred'] for h in s['holes']),
           'fillets_kept': s.get('top_edges_rounded') == 2,
           'volume': _near(s.get('volume_mm3'), VOL30, 0.5)}
    res['all'] = all(res.values())
    return res


def _steps(calls):
    for cl in calls:
        a = cl.get('arguments') or {}
        if cl.get('name') == 'execute':
            yield a.get('command'), a.get('params') or {}
        elif cl.get('name') == 'batch':
            for st in a.get('commands') or []:
                yield st.get('command'), st.get('params') or {}
        else:
            yield cl.get('name'), a


def edit_by_parameter(calls):
    """Message 2's calls change `width` as a parameter and draw nothing new."""
    names = [(cmd, p) for cmd, p in _steps(calls)]
    by_param = any(cmd in EDIT_CMDS and (p.get('name') == 'width' or 'width' in (p.get('changes') or {})) for cmd, p in names)
    redraw = any(cmd in ('new_design',) or str(cmd).startswith('sketch.') or cmd == 'solid.extrude' for cmd, p in names)
    return by_param and not redraw


def hole_edits(calls):
    """Message 2 moved or remade a hole itself: a new solid.hole, or a parameter change other than width."""
    for cmd, p in _steps(calls):
        if cmd == 'solid.hole':
            return True
        if cmd in EDIT_CMDS:
            names = [p.get('name')] + list((p.get('changes') or {}).keys())
            if any(n and n != 'width' for n in names):
                return True
    return False


def verdict(follow1, turn2, centred_after):
    if follow1 and not hole_edits(turn2) and centred_after:
        return 'kept centred by formula'
    if centred_after:
        return 're-centred by hand'
    return 'off-centre'


def logged_holes(calls):
    """How each hole was asked for, from the logged calls: solid.hole (position / references) or a sketch circle."""
    out = []
    for cmd, p in _steps(calls):
        if cmd == 'solid.hole':
            txt = json.dumps({k: p.get(k) for k in ('position', 'references', 'points')})
            out.append({'how': 'solid.hole', 'diameter': p.get('diameter', p.get('clearance')), 'position': p.get('position'),
                        'references': p.get('references'), 'uses_width': 'width' in txt})
        elif str(cmd).startswith('sketch.circle'):
            dia = p.get('diameter', None)
            if dia is None and p.get('radius') is not None:
                dia = p['radius'] if isinstance(p['radius'], (int, float)) and not isinstance(p['radius'], bool) else f"{p['radius']} (radius)"
                if isinstance(dia, (int, float)):
                    dia = f'{dia} (radius)'
            out.append({'how': 'sketch circle', 'diameter': dia, 'position': p.get('center'), 'references': None,
                        'uses_width': 'width' in json.dumps(p.get('center'))})
    return out


def calls_by_turn(run_dir):
    ev = [json.loads(x) for x in open(os.path.join(run_dir, 'events.jsonl'), encoding='utf-8') if x.strip()]
    t2 = next(e['t'] for e in ev if e['event'] == 'turn 2: Enter')
    seq_t = {e.get('seq'): e['t'] for e in ev if e['event'].startswith('tool call:')}
    t1, t2c = [], []
    for line in open(os.path.join(run_dir, 'transcript.jsonl'), encoding='utf-8'):
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        m = rec.get('msg')
        if rec.get('dir') == 'client->server' and isinstance(m, dict) and m.get('method') == 'tools/call':
            cl = {'seq': rec.get('seq'), 'name': (m.get('params') or {}).get('name'), 'arguments': (m.get('params') or {}).get('arguments') or {}}
            t = seq_t.get(rec.get('seq'))
            (t2c if t is not None and t >= t2 else t1).append(cl)
    return t1, t2c


def score_run(run):
    d = os.path.join(L4, 'runs', run)
    s2 = json.load(open(os.path.join(d, 'read.json')))['summary']
    rp_path = os.path.join(L4, f'replay-{run}.json')
    rp = json.load(open(rp_path)) if os.path.exists(rp_path) else None
    t1, t2 = calls_by_turn(d)
    h = logged_holes(t1)
    hp2 = s2['hole_params']
    ac = after_change(s2)
    f1 = rp['follow_after_turn1']['pass'] if rp else None
    return {'run': run,
            'names': {'hole_d_parameter': hp2['hole_d_parameter'], 'diameters': hp2['diameters'],
                      'distances_from_width': hp2['distances_from_width'], 'logged_holes_use_width': [x['uses_width'] for x in h],
                      'user_parameters': hp2['user_parameters']},
            'build_right_replay_turn1': rp['build_right'] if rp else None,
            'follow_after_turn1': f1, 'follow_after_turn2': rp['follow_after_turn2']['pass'] if rp else None,
            'after_change': ac, 'edit_by_parameter': edit_by_parameter(t2), 'hole_edits_in_turn2': hole_edits(t2),
            'verdict': verdict(bool(f1), t2, ac['holes_centred']) if rp else None,
            'logged_holes': h, 'turn1_calls': [c['name'] for c in t1], 'turn2_calls': [c['name'] for c in t2],
            'after': {k: s2[k] for k in ('volume_mm3', 'bbox_mm', 'holes', 'top_edges_rounded')},
            'first_build_replay': rp['after_turn1'] if rp else None}


def main():
    res = {'prereg': 'out/l4/prereg.json', 'hand': {}, 'runs': {}}
    hd = os.path.join(L4, 'hand')
    for k in ('fillet', 'width30', 'fixed', 'width20'):
        p = os.path.join(hd, f'read-{k}.json')
        if os.path.exists(p):
            s = json.load(open(p))['summary']
            res['hand'][k] = {'summary': {x: s[x] for x in ('volume_mm3', 'bbox_mm', 'holes', 'top_edges_rounded', 'hole_params')},
                              'build_right': build_right(s, 30 if k in ('width30', 'fixed') else 20) if k in ('fillet', 'width20') else None,
                              'after_change': after_change(s) if k in ('width30', 'fixed') else None}
    rd = os.path.join(L4, 'runs')
    for run in sorted(os.listdir(rd)) if os.path.isdir(rd) else []:
        if os.path.exists(os.path.join(rd, run, 'read.json')):
            res['runs'][run] = score_run(run)
    json.dump(res, open(os.path.join(L4, 'compare.json'), 'w'), indent=1)
    print(json.dumps({r: {'hole_d': v['names']['hole_d_parameter'], 'verdict': v['verdict'], 'follow1': v['follow_after_turn1'],
                          'after': v['after_change'], 'by_param': v['edit_by_parameter']} for r, v in res['runs'].items()}, indent=1))


if __name__ == '__main__':
    main()
