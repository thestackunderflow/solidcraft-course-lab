"""L5-Q8: is a Claude run real? Its logged tools/call requests repeated in order (failed ones too) with no AI, over the
plug of a fresh SolidCraft 0.28.0 window with lesson 4's hook built first and PrusaSlicer seeded; every file the replay
sends is copied and checked (lie, closed, bodies) against the file the live run sent. Writes out/l5/replay-RUN.json.
    bash: . lab/common.sh; . lab/l5slicerseed.sh; seed_slicer; start_display; (solidcraft &); python3 lab/l5replay.py RUN"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402
from l5compare import calls_of  # noqa: E402
from l5part import L5_START  # noqa: E402
from l5slice import lie_of  # noqa: E402

SLICED = '/root/.cache/solidcraft/slicer'


def main(run):
    d = f'/work/out/l5/runs/{run}'
    o = f'/work/out/l5/replay-{run}'
    os.makedirs(o, exist_ok=True)
    calls = calls_of(os.path.join(d, 'transcript.jsonl'))
    e = entry.read(os.path.expanduser('~/.claude.json'))
    c = McpClient([e['command']] + e['args'], timeout_s=180, log_path=os.path.join(o, 'transcript.jsonl'))
    c.start()
    b = McpClient.text_json(c.call_tool('batch', {'commands': L5_START, 'verbose': False}))
    rows, n = [], 0
    for call in calls:
        before = {f: os.stat(f).st_mtime for f in glob.glob(SLICED + '/*')}
        r = c.call_tool(call['name'], call['args'])
        txt = McpClient.text(r)
        row = {'seq': call['seq'], 'name': call['name'], 'live_error': call.get('isError'),
               'replay_error': bool(r.get('isError')), 'reply_head': txt[:200]}
        time.sleep(1.0)
        for f in glob.glob(SLICED + '/*'):
            if before.get(f) != os.stat(f).st_mtime:
                n += 1
                dst = os.path.join(o, 'sent-%d-%s' % (n, os.path.basename(f)))
                shutil.copy(f, dst)
                row['sent'] = os.path.basename(dst)
                row['lie'] = lie_of(dst)
        rows.append(row)
    subprocess.run(['pkill', '-x', 'slic3r_main'])
    c.close()
    live = sorted(glob.glob(d + '/sent-[0-9]*'), key=lambda p: int(re.search(r'sent-(\d+)', p).group(1)))
    rep = sorted(glob.glob(o + '/sent-[0-9]*'), key=lambda p: int(re.search(r'sent-(\d+)', p).group(1)))
    lv, rp = (lie_of(live[-1]) if live else None), (lie_of(rep[-1]) if rep else None)
    same = bool(lv and rp and all(lv[k] == rp[k] for k in ('lie', 'closed', 'bodies', 'size_mm')))
    res = {'run': run, 'hook_ok': b.get('ok'), 'calls_replayed': len(rows), 'rows': rows,
           'live_last': lv, 'replay_last': rp, 'same_file': same}
    json.dump(res, open(f'/work/out/l5/replay-{run}.json', 'w'), indent=1)
    print(run, 'calls', len(rows), 'live', lv and lv['lie'], 'replay', rp and rp['lie'], 'same', same)


if __name__ == '__main__':
    main(sys.argv[1])
