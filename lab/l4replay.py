"""L4-Q8 inside the replay container (see l4replay.sh): the hook, Claude's turn-1 calls, read + follow test, width
back to 20, the turn-2 calls, read + follow test, STL export. Writes OUT/replay.json and out/l4/replay-RUN.json.
    python3 lab/l4replay.py RUN OUT"""
import glob
import json
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from checker import entry, stl  # noqa: E402
from client.mcp import McpClient  # noqa: E402
from l7story import HOOK  # noqa: E402
import l4compare  # noqa: E402
import l4read  # noqa: E402

TEST_WIDTHS = (26, 40)


def summary(c):
    return l4read.read(c)['summary']


def follow(c):
    """Set width to each test value and report every bore against the body's middle; width is left at the last value."""
    out = {}
    for w in TEST_WIDTHS:
        r = McpClient.text_json(c.call_tool('set_parameter', {'name': 'width', 'value': w}))
        s = summary(c)
        out[str(w)] = {'set': r, 'bbox_mm': s['bbox_mm'], 'holes': s['holes'],
                       'all_centred': bool(s['holes']) and all(h['centred'] for h in s['holes']),
                       'top_edges_rounded': s['top_edges_rounded']}
    out['pass'] = all(out[str(w)]['all_centred'] for w in TEST_WIDTHS)
    return out


def replay(c, calls):
    rows = []
    for call in calls:
        r = c.call_tool(call['name'], call['arguments'])
        rows.append({'logged_seq': call['seq'], 'name': call['name'], 'isError': bool(r.get('isError')),
                     'reply': McpClient.text_json(r)})
    return rows


def main(run, o):
    e = entry.read(os.path.expanduser('~/.claude.json'))
    t1, t2 = l4compare.calls_by_turn(f'/work/out/l4/runs/{run}')
    c = McpClient([e['command']] + e['args'], timeout_s=330, log_path=os.path.join(o, 'transcript.jsonl'))
    c.start()
    hook = McpClient.text_json(c.call_tool('batch', {'commands': HOOK, 'verbose': False}))
    rows1 = replay(c, t1)
    s1 = summary(c)
    f1 = follow(c)
    back = McpClient.text_json(c.call_tool('set_parameter', {'name': 'width', 'value': 20}))
    rows2 = replay(c, t2)
    s2 = summary(c)
    subprocess.run(['xdotool', 'mousemove', '700', '520']); time.sleep(0.8)
    subprocess.run(['import', '-window', 'root', os.path.join(o, 'window.png')])
    f2 = follow(c)
    c.call_tool('set_parameter', {'name': 'width', 'value': 30})
    scratch = sorted(glob.glob('/tmp/solidcraft-mcp-*'))
    stl_path = os.path.join(scratch[-1], 'hook.stl') if scratch else '/tmp/hook.stl'
    ex = c.call_tool('export', {'path': stl_path, 'format': 'stl'})
    c.close()
    res = {'replayed_from': f'out/l4/runs/{run}/transcript.jsonl', 'hook_ok': hook.get('ok'),
           'turn1_calls': len(t1), 'turn2_calls': len(t2), 'errors': sum(x['isError'] for x in rows1 + rows2),
           'after_turn1': {k: s1[k] for k in ('volume_mm3', 'bbox_mm', 'holes', 'top_edges_rounded', 'hole_params')},
           'build_right': l4compare.build_right(s1, 20), 'follow_after_turn1': f1, 'width_back_to_20': back,
           'after_turn2': {k: s2[k] for k in ('volume_mm3', 'bbox_mm', 'holes', 'top_edges_rounded', 'hole_params')},
           'after_change': l4compare.after_change(s2), 'follow_after_turn2': f2,
           'export': {'isError': bool(ex.get('isError'))}}
    if os.path.exists(stl_path):
        shutil.copy(stl_path, os.path.join(o, 'hook.stl'))
        res['our_checker'] = stl.check(os.path.join(o, 'hook.stl'))
    json.dump(dict(res, rows1=rows1, rows2=rows2), open(os.path.join(o, 'replay.json'), 'w'), indent=1)
    json.dump(res, open(f'/work/out/l4/replay-{run}.json', 'w'), indent=1)
    print(json.dumps({k: res[k] for k in ('turn1_calls', 'turn2_calls', 'errors', 'build_right', 'after_change')}, indent=1))
    print('follow after turn 1:', f1['pass'], ' after turn 2:', f2['pass'])


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
