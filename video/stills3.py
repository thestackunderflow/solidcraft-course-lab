"""Lesson 3: full-size stills (2880x1800 PNG) from the lab's screen recordings, taken at named events (seconds after the
event), for the video's cards and hook pictures. Masters: out/scratch/l3-masters (gitignored); stills: out/l3/stills.
    docker run --rm --network none -v "$PWD:/work" -w /work sc3-app:0.26.1 python3 video/stills3.py"""
import json
import os
import subprocess

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
M = os.path.join(LAB, 'out', 'scratch', 'l3-masters')
L3 = os.path.join(LAB, 'out', 'l3')
OUT = os.path.join(L3, 'stills')
os.makedirs(OUT, exist_ok=True)
EV = {'hand': 'hand', 'plain': 'plain', 'runs-A1': 'runs/A1', 'runs-A2': 'runs/A2', 'runs-B1': 'runs/B1', 'runs-B2': 'runs/B2'}

# name: (master, event prefix, seconds after it)
STILLS = {
    'hand-40.png': ('hand', 'home: the 40 hook', 2.6),
    'hand-25.png': ('hand', 'home: the 3D hook', 2.6),
    'hand-params.png': ('hand', 'params: OK', -0.4),
    'hand-props-before.png': ('hand', 'properties: rows held', 2.0),
    'hand-props-after.png': ('hand', 'properties after: rows held', 2.0),
    'hand-j.png': ('hand', 'sketch: closed', 2.5),
    'hand-formula.png': ('hand', 'line: left hook_depth - 2 * thickness placed', 0.4),
    'plain-25.png': ('plain', 'plain: the hook unchanged', 2.8),
    'plain-refused.png': ('plain', 'plain: the message held', 0.6),
    'plain-props.png': ('plain', 'plain properties: rows held', 2.0),
    'plain-remedy.png': ('plain', 'remedy properties: rows held', 2.0),
    'B1-thick.png': ('runs-B1', 'turn 2: typing', -2.0),
    'B1-40.png': ('runs-B1', 'turn 2: end-of-turn', 2.0),
    'B2-40.png': ('runs-B2', 'turn 2: end-of-turn', 2.0),
    'A1-40.png': ('runs-A1', 'turn 2: end-of-turn', 2.0),
    'A2-reply.png': ('runs-A2', 'turn 2: end-of-turn', 2.0),
    'B1-typed.png': ('runs-B1', 'turn 1: Enter', -0.6),
}


def at(master, prefix):
    for line in open(os.path.join(L3, EV[master], 'events.jsonl'), encoding='utf-8'):
        e = json.loads(line)
        if e['event'].startswith(prefix):
            return e['t']
    raise KeyError(f'{master}: {prefix}')


for name, (master, prefix, dt) in STILLS.items():
    t = at(master, prefix) + dt
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', os.path.join(M, master + '.mp4'), '-frames:v', '1',
                    os.path.join(OUT, name)], check=True)
    print(name, round(t, 2))
