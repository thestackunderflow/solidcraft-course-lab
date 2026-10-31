"""L5-Q4: does Save As Mesh to a file keep the print face? With no AI, over the plug (headless SolidCraft 0.28.0): lesson
4's hook (also saved as out/l5/hook-lesson4.sc for viewers who skipped lessons 2-4), Save As Mesh to STL and 3MF
before and after marking the J face as the print face, and Send to Slicer's own file after the same mark (and after
marking the plate's back, for L5-Q3's third way). Hashes, sizes and how each file lies (l5score.lie).
    python3 lab/l5saveface.py            (inside sc5-l5:0.28.0, a display for the slicer it starts)"""
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402
from l5part import L5_START  # noqa: E402
from l5slice import lie_of  # noqa: E402

O = '/work/out/l5/saveface'
SLICED = '/root/.cache/solidcraft/slicer'
J_FACE = [12, 0, 2.5]        # on the hook's side at y = 0: the J outline
BACK = [0, -10, 30]          # the plate's back (x = 0)


def main():
    os.makedirs(O, exist_ok=True)
    e = entry.read(os.path.expanduser('~/.claude.json'))
    c = McpClient([e['command']] + e['args'] + ['--allow-path', '/work/out/l5'], timeout_s=180,
                  log_path=os.path.join(O, 'transcript.jsonl'))
    c.start()
    ex = lambda cmd, **p: McpClient.text(c.call_tool('execute', {'command': cmd, 'params': p}))  # noqa: E731
    res = {'steps': []}
    b = McpClient.text_json(c.call_tool('batch', {'commands': L5_START, 'verbose': False}))
    res['part_ok'] = b.get('ok')
    res['save_design'] = ex('file.save', path='/work/out/l5/hook-lesson4.sc')

    def save(tag):
        for ext in ('stl', '3mf'):
            p = f'{O}/{tag}.{ext}'
            res['steps'].append({'tag': f'{tag}.{ext}', 'reply': ex('file.save_mesh', path=p)})

    def send(tag):
        for f in glob.glob(SLICED + '/*'):
            os.remove(f)
        r = ex('file.send_to_slicer', slicer='prusa', bodies=['Body1'], wait='no')
        time.sleep(2)
        got = sorted(glob.glob(SLICED + '/*'))
        if got:
            shutil.copy(got[-1], f'{O}/{tag}.3mf')
        res['steps'].append({'tag': f'{tag}.3mf', 'reply': r})
        subprocess.run(['pkill', '-x', 'slic3r_main'])

    save('save-before-face')
    res['steps'].append({'tag': 'print face: J', 'reply': ex('body.print_face', body='Body1', point=J_FACE)})
    save('save-after-face')
    send('send-j-face')
    res['steps'].append({'tag': 'print face: back', 'reply': ex('body.print_face', body='Body1', point=BACK)})
    send('send-back')
    res['steps'].append({'tag': 'print face: cleared', 'reply': ex('body.print_face', body='Body1')})
    send('send-no-face')
    c.close()
    res['files'] = {}
    for p in sorted(glob.glob(O + '/*.stl') + glob.glob(O + '/*.3mf')):
        row = {'sha256': hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16], 'bytes': os.path.getsize(p)}
        row.update(lie_of(p))
        res['files'][os.path.basename(p)] = row
    json.dump(res, open('/work/out/l5/saveface.json', 'w'), indent=1)
    for k, v in res['files'].items():
        print(k, v['sha256'], v['lie'], v['size_mm'])


if __name__ == '__main__':
    main()
