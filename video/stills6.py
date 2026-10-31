"""Lesson 6: full-size stills (2880x1800 PNG) from the lab's screen recordings, taken at named events (seconds after the
event), for the video's cards, hook pictures and thumbnails. Masters: out/scratch/l6-masters (gitignored); stills:
out/l6/stills.
    docker run --rm --network none -v "$PWD:/work" -w /work sc5-l5:0.28.0 python3 video/stills6.py"""
import json
import os
import subprocess

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
M = os.path.join(LAB, 'out', 'scratch', 'l6-masters')
L5 = os.path.join(LAB, 'out', 'l6')
OUT = os.path.join(L5, 'stills')
os.makedirs(OUT, exist_ok=True)
EV = {'hand': 'hand', 'runs-B2': 'runs/B2', 'runs-B3': 'runs/B3'}

# name: (master, event prefix, seconds after it)
STILLS = {
    'hand-start.png': ('hand', 'recording started', 2.5),
    'hand-side.png': ('hand', 'side: hover the opening', 1.5),
    'hand-m25.png': ('hand', "measure 25: the lip's top face", 2.2),
    'hand-p30.png': ('hand', 'params 30: Enter', 2.5),
    'hand-m30.png': ('hand', "measure 30: the lip's top face", 2.2),
    'hand-p40.png': ('hand', 'params 40: Enter', 2.5),
    'hand-m40.png': ('hand', "measure 40: the lip's top face", 2.2),
    'hand-hole.png': ('hand', 'list: hole size held', 1.0),
    'hand-holeside.png': ('hand', 'list: centre to the side held', 1.0),
    'hand-fillet.png': ('hand', 'list: radius held', 1.0),
    'hand-lipheight.png': ('hand', 'list: lip height held', 1.0),
    'hand-lipwall.png': ('hand', 'list: lip wall held', 1.0),
    'hand-props.png': ('hand', 'props: hover Bounding box', 2.0),
    'hand-send.png': ('hand', 'send: hover Print face', 1.5),
    'hand-slicer.png': ('hand', 'slicer: hover the name', 1.0),
    'hand-est.png': ('hand', 'slicer: estimate shown', 2.0),
    'B2-typed.png': ('runs-B2', 'turn 1: Enter', -0.6),
    'B2-reply.png': ('runs-B2', 'turn 1: reply done', 1.0),
    'B2-after.png': ('runs-B2', 'slicer estimate held', 1.0),
    'B3-reply.png': ('runs-B3', 'turn 1: reply done', 1.0),
    'B3-after.png': ('runs-B3', 'slicer estimate held', 1.0),
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
