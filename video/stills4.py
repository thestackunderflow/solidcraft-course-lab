"""Lesson 4: full-size stills (2880x1800 PNG) from the lab's screen recordings, taken at named events (seconds after the
event), for the video's cards, hook pictures and thumbnails. Masters: out/scratch/l4-masters (gitignored); stills:
out/l4/stills.
    docker run --rm --network none -v "$PWD:/work" -w /work sc4-app:0.27.1 python3 video/stills4.py"""
import json
import os
import subprocess

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
M = os.path.join(LAB, 'out', 'scratch', 'l4-masters')
L4 = os.path.join(LAB, 'out', 'l4')
OUT = os.path.join(L4, 'stills')
os.makedirs(OUT, exist_ok=True)
EV = {'hand': 'hand', 'dialog': 'dialog'}
for r in ('A1', 'A2', 'B1', 'B2'):
    EV['runs-' + r] = 'runs/' + r

# name: (master, event prefix, seconds after it)
STILLS = {
    'hand-start.png': ('hand', 'recording started', 2.0),
    'hand-params.png': ('hand', 'params: hole_d added', 1.6),
    'hand-hole1.png': ('hand', 'hole1: Diameter hole_d', 1.4),
    'hand-two-holes.png': ('hand', 'fillet: Fillet button', -0.6),
    'hand-sharp.png': ('hand', 'fillet: Fillet button', -0.6),
    'hand-round.png': ('hand', 'fillet: done', 1.0),
    'hand-props-before.png': ('hand', 'properties before: rows held', 2.0),
    'hand-right-20.png': ('hand', 'view width20: held', 1.5),
    'hand-right-30.png': ('hand', 'view width30: held', 2.0),
    'hand-props-30.png': ('hand', 'properties width30: rows held', 2.0),
    'hand-fix.png': ('hand', 'fix: Enter Hole1', 3.0),
    'hand-right-fixed.png': ('hand', 'view fixed: held', 2.0),
    'hand-right-20b.png': ('hand', 'view width20b: held', 2.0),
    'hand-3d-fixed.png': ('hand', 'view fixed: back to 3D', 1.6),
}


def at(master, prefix):
    for line in open(os.path.join(L4, EV[master], 'events.jsonl'), encoding='utf-8'):
        e = json.loads(line)
        if e['event'].startswith(prefix):
            return e['t']
    raise KeyError(f'{master}: {prefix}')


for name, (master, prefix, dt) in STILLS.items():
    src = os.path.join(M, master + '.mp4')
    if not os.path.exists(src):
        print('skip', name, '(no master)')
        continue
    t = at(master, prefix) + dt
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', src, '-frames:v', '1',
                    os.path.join(OUT, name)], check=True)
    print(name, round(t, 2))
