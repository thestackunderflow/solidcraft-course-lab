"""Lesson 5: full-size stills (2880x1800 PNG) from the lab's screen recordings, taken at named events (seconds after the
event), for the video's cards, hook pictures and thumbnails. Masters: out/scratch/l5-masters (gitignored); stills:
out/l5/stills.
    docker run --rm --network none -v "$PWD:/work" -w /work sc5-l5:0.28.0 python3 video/stills5.py"""
import json
import os
import subprocess

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
M = os.path.join(LAB, 'out', 'scratch', 'l5-masters')
L5 = os.path.join(LAB, 'out', 'l5')
OUT = os.path.join(L5, 'stills')
os.makedirs(OUT, exist_ok=True)
EV = {'hand': 'hand', 'closed': 'closed', 'runs-A1': 'runs/A1', 'runs-B1': 'runs/B1'}

# name: (master, event prefix, seconds after it)
STILLS = {
    'hand-start.png': ('hand', 'recording started', 2.5),
    'hand-menu.png': ('hand', 'ways out: hover Send to Slicer', 1.5),
    'hand-props.png': ('hand', 'props: hover Bounding box', 2.0),
    'hand-send1.png': ('hand', 'send1: hover Slicer PrusaSlicer', 1.5),
    'hand-standing-open.png': ('hand', 'slicer standing: hover size boxes', 1.5),
    'hand-standing-sliced.png': ('hand', 'slicer standing: estimate shown', 2.0),
    'hand-standing-warning.png': ('hand', 'slicer standing: open the warning', 4.0),
    'hand-send2.png': ('hand', 'send2: face 1 held', 1.0),
    'hand-side-sliced.png': ('hand', 'slicer side: estimate shown', 2.0),
    'hand-save.png': ('hand', 'save: hover 3MF', 0.8),
    'closed-bad.png': ('closed', 'bad: tooltip held', 0.0),
    'closed-place-before.png': ('closed', 'place: F (Place on face)', 2.0),
    'closed-place-after.png': ('closed', 'place: done', 1.0),
    'A1-typed.png': ('runs-A1', 'turn 1: Enter', -0.6),
    'A1-after.png': ('runs-A1', 'slicer estimate held', 1.0),
    'B1-typed.png': ('runs-B1', 'turn 1: Enter', -0.6),
    'B1-after.png': ('runs-B1', 'slicer estimate held', 1.0),
}


def at(master, prefix):
    for line in open(os.path.join(L5, EV[master], 'events.jsonl'), encoding='utf-8'):
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
