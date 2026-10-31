"""L6-Q6: is a Claude run real? Its logged tools/call requests repeated in order (failed ones too, reads too) with no AI,
over the plug of a fresh SolidCraft 0.28.0 window with lesson 5's hook built first (lab/l6part.py) and PrusaSlicer
seeded; then the same read and pass rule as the live run (lab/l6read.py --send). The live verdict is the score; a replay
that differs is reported and that run's "replayed" line is dropped (prereg). Writes out/l6/replay-RUN.json.
    bash: . lab/common.sh; . lab/l5slicerseed.sh; seed_slicer; start_display; (solidcraft &); python3 lab/l6replay.py RUN"""
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from client.mcp import McpClient  # noqa: E402
from l5compare import calls_of  # noqa: E402
from l6part import L6_START, plug_cmd  # noqa: E402
import l6read  # noqa: E402


def main(run):
    d = f'/work/out/l6/runs/{run}'
    o = f'/work/out/l6/replay-{run}'
    os.makedirs(o, exist_ok=True)
    calls = calls_of(os.path.join(d, 'transcript.jsonl'))
    c = McpClient(plug_cmd(None, ['--allow-path', l6read.TMP]), timeout_s=180, log_path=os.path.join(o, 'transcript.jsonl'))
    c.start()
    b = McpClient.text_json(c.call_tool('batch', {'commands': L6_START, 'verbose': False}))
    rows = []
    for call in calls:
        if call['name'] in ('screenshot',):
            rows.append({'seq': call['seq'], 'name': call['name'], 'skipped': 'a picture only'})
            continue
        r = c.call_tool(call['name'], call['args'])
        rows.append({'seq': call['seq'], 'name': call['name'], 'live_error': call.get('isError'),
                     'replay_error': bool(r.get('isError')), 'reply_head': McpClient.text(r)[:160]})
        time.sleep(0.3)
    subprocess.run(['pkill', '-x', 'slic3r_main'])
    time.sleep(1.0)
    rd = l6read.read(c, os.path.join(o, 'read'), send=True)
    c.close()
    live = json.load(open(os.path.join(d, 'read.json')))
    lv, rp = live['score'], rd['score']
    same = lv.get('passed') == rp.get('passed') and [x['ok'] for x in lv['lines']] == [x['ok'] for x in rp['lines']]
    res = {'run': run, 'hook_ok': b.get('ok'), 'calls_replayed': len(rows), 'rows': rows, 'read': rd,
           'passed': rp.get('passed'), 'live_passed': lv.get('passed'), 'same_verdict': same,
           'opening_mm': (rd.get('geom') or {}).get('opening_mm'), 'volume_mm3': rd['summary'].get('volume_mm3')}
    json.dump(res, open(f'/work/out/l6/replay-{run}.json', 'w'), indent=1)
    print(run, 'calls', len(rows), 'replay passed', rp.get('passed'), 'live', lv.get('passed'), 'same', same)


if __name__ == '__main__':
    main(sys.argv[1])
