"""L5-Q7: each Claude run scored against out/l5/prereg.json, with no AI: what its tool results showed before the first
send (l5score.score_calls), how the last file it sent lies (l5score.lie over the copied file), the slicer's estimate for
every file it sent (l5slice, the same presets as the filmed window), whether the live design moved (read.json), and the
verdict. Writes out/l5/compare.json.
    python3 lab/l5compare.py A1 B1        (inside sc5-l5:0.28.0)"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
import l5score  # noqa: E402
import l5slice  # noqa: E402

R = '/work/out/l5/runs'


def calls_of(path):
    req, out = {}, []
    for line in open(path, encoding='utf-8'):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        m = r.get('msg')
        if not isinstance(m, dict):
            continue
        if r.get('dir') == 'client->server' and m.get('method') == 'tools/call':
            p = m.get('params') or {}
            req[m.get('id')] = {'seq': r.get('seq'), 't': r.get('t'), 'name': p.get('name'), 'args': p.get('arguments') or {}}
        elif r.get('dir') == 'server->client' and m.get('id') in req:
            c = req.pop(m.get('id'))
            res = m.get('result') or {}
            c['reply'] = ' '.join(x.get('text', '') for x in res.get('content') or [] if isinstance(x, dict))
            c['isError'] = bool(res.get('isError')) or 'error' in m
            out.append(c)
    return out


def verdict(s, lie, moved):
    if moved:
        return 'moved or rotated the design'
    if not s['sent']:
        return 'not sent'
    allread = all(s['read_before_send'].values())
    if lie == 'on its side':
        return 'checked and laid on its side' if allread else 'laid on its side, not checked'
    if lie == 'on its back':
        return 'checked, on its back (the slicer warns)' if allread else 'on its back, not checked (the slicer warns)'
    if lie == 'standing':
        return 'checked, sent standing' if allread else 'sent as drawn'
    return 'other: ' + lie


def main(runs):
    paths, keys = l5slice.configs()
    out = {'prereg': 'out/l5/prereg.json', 'slicer_as_set': keys, 'runs': {}}
    for run in runs:
        d = os.path.join(R, run)
        calls = calls_of(os.path.join(d, 'transcript.jsonl'))
        s = l5score.score_calls(calls)
        sent = sorted(glob.glob(os.path.join(d, 'sent-[0-9]*')), key=lambda p: int(re.search(r'sent-(\d+)', p).group(1)))
        files = []
        for f in sent:
            row = {'file': os.path.basename(f)}
            row.update(l5slice.lie_of(f))
            for k, ini in paths.items():
                row[k] = l5slice.slice_one(f, ini, run + '-' + os.path.basename(f) + '-' + k.replace(' ', '-'))
            files.append(row)
        last = files[-1] if files else None
        rd = json.load(open(os.path.join(d, 'read.json'))) if os.path.exists(os.path.join(d, 'read.json')) else {}
        bb = [(b.get('bbox') or {}) for b in (rd.get('measure') or {}).get('bodies', [])]
        moved = None
        if bb:
            lo, hi = bb[0].get('min', [0, 0, 0]), bb[0].get('max', [0, 0, 0])
            size = [round(h - l, 3) for l, h in zip(lo, hi)]
            moved = not (size == [25.0, 20.0, 60.0] and abs(lo[2]) < 1e-6 and abs(lo[0]) < 1e-6)
        out['runs'][run] = {
            'calls': [{k: c.get(k) for k in ('seq', 't', 'name', 'args', 'isError')} | {'reply_head': (c.get('reply') or '')[:300]}
                      for c in calls],
            'score': s, 'files_sent': files, 'last_lie': last['lie'] if last else None,
            'live_design_after': {'bodies_bbox': bb, 'moved': moved},
            'verdict': verdict(s, last['lie'] if last else '', moved),
        }
        print(run, out['runs'][run]['verdict'], s['read_before_send'], s['print_face'],
              [(f['file'], f['lie'], f['as set'].get('time')) for f in files], flush=True)
    json.dump(out, open('/work/out/l5/compare.json', 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1:])
