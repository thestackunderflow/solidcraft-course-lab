"""L6-Q5: each Claude run scored against out/l6/prereg.json, with no AI: the pass rule on our read of the live design
after the turn (read.json, lab/l6score.py), what Claude changed (its logged calls that can change the design), what it
said at the end (its last reply, verbatim, for the hand coding of "said OK / no number / not checked"), its cost (the
ledger), whether the body was turned (the bounding box's sizes swapped), and the replay's verdict if there is one.
Writes out/l6/compare.json.
    python3 lab/l6compare.py B1 B2 B3 [A1]        (inside sc5-l5:0.28.0)"""
import json
import os
import sys

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from l5compare import calls_of  # noqa: E402

R = '/work/out/l6/runs'
READS = {'parameters.list', 'inspect.measure', 'file.slicers', 'view.home', 'view.fit', 'view.set', 'selection.get'}


def changes(calls):
    out = []
    for c in calls:
        a = c.get('args') or {}
        if c['name'] == 'set_parameter':
            out.append({'seq': c['seq'], 'call': 'set_parameter', 'args': a, 'error': c.get('isError')})
        elif c['name'] == 'execute' and a.get('command') not in READS and not str(a.get('command', '')).startswith('view.'):
            out.append({'seq': c['seq'], 'call': 'execute ' + str(a.get('command')), 'args': a.get('params'),
                        'error': c.get('isError')})
        elif c['name'] in ('batch', 'undo', 'redo', 'new_design', 'open'):
            out.append({'seq': c['seq'], 'call': c['name'], 'args': a, 'error': c.get('isError')})
    return out


def last_reply(session_path):
    if not os.path.exists(session_path):
        return None
    text = None
    for line in open(session_path, encoding='utf-8'):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        m = r.get('message') or {}
        if r.get('type') == 'assistant' and isinstance(m.get('content'), list):
            t = ' '.join(x.get('text', '') for x in m['content'] if isinstance(x, dict) and x.get('type') == 'text').strip()
            if t:
                text = t
    return text


def cost(run):
    p = '/work/../solidcraft-course-BUDGET.tsv'
    for path in (p, '/ledger/solidcraft-course-BUDGET.tsv'):
        if os.path.exists(path):
            for line in open(path, encoding='utf-8'):
                f = line.rstrip('\n').split('\t')
                if f[0] == 'sc6-' + run:
                    return {'usd': float(f[1]), 'kind': f[2]}
    return None


def turned(summary):
    bb = sorted(round(x, 2) for x in (summary or {}).get('bbox_mm') or [])
    want = sorted([40.0, 20.0, 60.0])
    return bb == want and [round(x, 2) for x in summary['bbox_mm']] != [40.0, 20.0, 60.0]


def one(run):
    d = os.path.join(R, run)
    read = json.load(open(os.path.join(d, 'read.json')))
    calls = calls_of(os.path.join(d, 'transcript.jsonl')) if os.path.exists(os.path.join(d, 'transcript.jsonl')) else []
    s = read['score']
    rep = '/work/out/l6/replay-%s.json' % run
    replay = json.load(open(rep)) if os.path.exists(rep) else None
    trig = os.path.join(d, 'trigger.json')
    return {'run': run, 'passed': s.get('passed'), 'broken': [x['id'] for x in s.get('lines', []) if not x['ok']],
            'lines': s.get('lines'), 'also': s.get('also'), 'turned': turned(read.get('summary')),
            'sizes_after': {p['name']: p.get('expression') for p in read.get('parameters') or []},
            'calls': len(calls), 'tools': [c['name'] + (' ' + str((c.get('args') or {}).get('command')) if c['name'] == 'execute' else '')
                                           for c in calls],
            'changes': changes(calls), 'last_reply': last_reply(os.path.join(d, 'session.jsonl')),
            'trigger': json.load(open(trig)) if os.path.exists(trig) else None,
            'sent_by_script': read.get('sent'), 'cost': cost(run),
            'replay_passed': replay and replay.get('passed'), 'replay_same': replay and replay.get('same_verdict')}


def main(runs):
    res = {'runs': [one(r) for r in runs if os.path.exists(os.path.join(R, r, 'read.json'))]}
    b = [r for r in res['runs'] if r['run'].startswith('B')]
    res['with_list'] = {'runs': len(b), 'passed': sum(1 for r in b if r['passed'])}
    a = [r for r in res['runs'] if r['run'].startswith('A')]
    res['without_list'] = {'runs': len(a), 'passed': sum(1 for r in a if r['passed'])}
    json.dump(res, open('/work/out/l6/compare.json', 'w'), indent=1)
    for r in res['runs']:
        print(r['run'], 'PASS' if r['passed'] else 'FAIL', r['broken'], [c['call'] + ' ' + json.dumps(c['args'])[:80] for c in r['changes']])
    print('with the list:', res['with_list'], 'without:', res['without_list'])


if __name__ == '__main__':
    main(sys.argv[1:])
