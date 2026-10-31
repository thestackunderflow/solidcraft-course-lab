"""Lesson 6: a no-AI read of the open design, the referee for every run (by hand, each Claude run, each replay):
  - lesson 4's reader (measure, body_topology, parameters.list: holes, round faces, bounding box, volume);
  - the body saved as an STL (file.save_mesh: a copy, the design doesn't change) and measured with rays
    (checker.l6geom: opening, plate, lip, base, lip height) and our mesh checker (closed, bodies);
  - with --send: a Send to Slicer by this script (file.send_to_slicer, PrusaSlicer; the design doesn't move) and the
    file it wrote, read for how it lies (lab/l5slice.lie_of);
  - the pass rule applied (lab/l6score.py).
    python3 lab/l6read.py OUT.json [--entry ENTRY_JSON] [--send] [--keep-slicer]"""
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
from checker import l6geom, stl  # noqa: E402
from client.mcp import McpClient  # noqa: E402
import l4read  # noqa: E402
import l6score  # noqa: E402
from l6part import plug_cmd  # noqa: E402

SLICED = '/root/.cache/solidcraft/slicer'
TMP = '/tmp/l6read'


def read(c, out_base, send=False, keep_slicer=False):
    os.makedirs(TMP, exist_ok=True)
    r = l4read.read(c)
    meas = r['measure']
    bodies = meas.get('bodies') or []
    res = {'summary': r['summary'], 'body_count': meas.get('body_count', len(bodies)),
           'closed': bool(bodies) and all(b.get('closed') is True for b in bodies),
           'parameters': [{k: p.get(k) for k in ('name', 'expression', 'value')} for p in
                          ((r.get('parameters_list') or {}).get('parameters') or []) if str(p.get('source', '')).startswith('user')]}
    raw = McpClient.text(c.call_tool('inspect_design', {'measure': False, 'sketches': False}))
    res['headless'] = 'headless session' in raw            # the read must land in the user's open window
    stl_path = out_base + '-body.stl'
    names = [b.get('name') for b in bodies]
    target = os.path.join(TMP, 'body.stl')
    rep = McpClient.text(c.call_tool('execute', {'command': 'file.save_mesh', 'params': {'path': target, 'bodies': names}}))
    if 'outside the folders' in rep:
        # the window's agent session keeps the folders of the plug that connected first: try the folders it names
        m = re.search(r'may use \(([^)]*)\)', rep)
        for folder in sorted((m.group(1).split(', ') if m else []), key=lambda f: 'recovery' in f):
            target = os.path.join(folder.strip(), 'l6read-body.stl')
            rep = McpClient.text(c.call_tool('execute', {'command': 'file.save_mesh', 'params': {'path': target, 'bodies': names}}))
            if os.path.exists(target):
                break
    res['save_mesh'] = rep[:300]
    if os.path.exists(target):
        shutil.copy(target, stl_path)
        os.remove(target)
        tris = stl.read(stl_path)
        chk = stl.check(stl_path)
        res['mesh'] = {'closed': chk.get('closed'), 'bodies': chk.get('bodies'), 'size_mm': chk.get('size_mm')}
        res['geom'] = l6geom.measure_hook(tris)
    else:
        res['mesh'], res['geom'] = {}, {}
    res['sent'] = None
    if send:
        from l5slice import lie_of
        subprocess.run(['pkill', '-x', 'slic3r_main'])
        time.sleep(1.0)
        for f in glob.glob(SLICED + '/*'):
            os.remove(f)
        res['send_reply'] = McpClient.text(c.call_tool('execute', {'command': 'file.send_to_slicer', 'params': {
            'slicer': 'prusa', 'bodies': names, 'wait': 'no'}}))[:400]
        time.sleep(3.0)
        got = sorted(glob.glob(SLICED + '/*'))
        if got:
            dst = out_base + '-sent.3mf'
            shutil.copy(got[-1], dst)
            res['sent'] = lie_of(dst)
        if not keep_slicer:
            subprocess.run(['pkill', '-x', 'slic3r_main'])
    res['score'] = l6score.score(res)
    return res


def main():
    a = sys.argv[1:]
    out = a[0]
    entry_json = a[a.index('--entry') + 1] if '--entry' in a else None
    c = McpClient(plug_cmd(entry_json, ['--allow-path', TMP]), timeout_s=180,
                  log_path=out.replace('.json', '-transcript.jsonl'))
    c.start()
    res = read(c, out.replace('.json', ''), send='--send' in a, keep_slicer='--keep-slicer' in a)
    c.close()
    json.dump(res, open(out, 'w'), indent=1)
    s = res['score']
    print('passed', s['passed'], ' '.join('%s=%s' % (x['id'], 'ok' if x['ok'] else 'BROKEN') for x in s['lines']),
          'opening', (res.get('geom') or {}).get('opening_mm'), 'sent', (res.get('sent') or {}).get('height_mm'))


if __name__ == '__main__':
    main()
