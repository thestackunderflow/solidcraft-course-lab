"""fx10 clips (SolidCraft Revolve refusal), cut by event time (the fx8clips.py pattern); takes A-D and
the Claude run runs/R1. Every clip comes twice:
NAME-full.mp4 (the whole 2880x1620 display = the full SolidCraft window, zoom 1) and NAME-zoom.mp4 (the same span, a
fixed close-up), so the edit shows the full window first, then the zoom (owner rule 4 Nov). Silent, 1920x1080, 30 fps.
    docker run --rm --network none -v "$PWD:/work" -v VIDEOQA:/footage:ro -w /work sc5-l5:0.28.0 \
        env FOOTAGE_PY=/footage/footage.py FX10_OUT=/work/out/fx10 python3 lab/fx10clips.py [name ...]
Writes out/fx10/clips/*.mp4 and out/fx10/clips/clips.json (spans, zoom boxes in source pixels).
Centres are source pixels (2880x1620) = 2 x the 1440x810 probe units of lab/fx10lib.sh."""
import importlib.util
import json
import os
import sys

OUT = os.environ.get('FX10_OUT', '/work/out/fx10')
SIZE = (1920, 1080)
SRC = (2880, 1620)
FULL = (1440, 810)
BROWSER = (300, 700)          # Browser > Origin (Z row 82,358) and Sketch1 (100,475)
VIEW = (1600, 860)            # the sketch / 3D view (the T, the knob, the ring)
DIALOG = (2680, 820)          # the Revolve dialog (Profile 1349,318 .. OK 1388,515)
REASON = (2640, 1100)         # the live red line under the dialog's fields (above 1322,579)
REPORT = (1440, 900)          # the Create Issue draft (Close at 734,670)
MEASURE = (2700, 800)         # the Measure panel (Close at 1396,456)
PROPS = (1440, 900)           # Properties (Close at 860,649)
TERM = (720, 1377)            # take D's terminal strip (y 1134..1620)
R1_PROMPT = (720, 1215)       # R1 (Claude Code full screen): the message typed in the input line (y ~1520, left)
R1_WORK = (720, 700)          # R1: the sent message (y ~523) and "Calling solidcraft N times" (y ~600); the login
                              # notice at the bottom right (x > 2150, y ~1450) stays out of both zooms: mask it in full
R1_REPLY = (1200, 800)        # R1: the reply (y ~670..1080, lines run to x ~2840: zoom 1.2 from the left edge, the
                              # words go in caption cards); the greyed suggested prompt (y ~1522) stays out


def ev(take):
    return [json.loads(line) for line in open(f'{OUT}/{take}/events.jsonl')]


def at(take, label, nth=0):
    rows = [e for e in ev(take) if e['event'].startswith(label)]
    return rows[nth]['t']


def segs():
    """(name, take, t0, t1, zoom, centre); one per filmed beat; every name gets -full and -zoom."""
    S = []
    a = 'A'
    S.append(('A-open-T', a, 0.0, at(a, 'Revolve (Model tab'), 2.0, BROWSER))
    S.append(('A-T-axis-hold', a, at(a, 'the T sketch, the vertical axis'), at(a, 'Revolve (Model tab'), 1.5, VIEW))
    S.append(('A-revolve-dialog', a, at(a, 'Revolve (Model tab') - 0.5, at(a, 'Axis: Z'), 2.0, DIALOG))
    S.append(('A-axis-z-refused', a, at(a, 'Axis: Z'), at(a, 'revolve full: refused') + 0.5, 2.0, DIALOG))
    S.append(('A-refusal-line', a, at(a, 'revolve full 360: live error'), at(a, 'revolve full: refused') + 0.5, 3.0, REASON))
    S.append(('A-report-draft', a, at(a, 'Create Issue'), at(a, 'B.14: Angle 180'), 2.0, REPORT))
    S.append(('A-180-refused', a, at(a, 'B.14: Angle 180'), at(a, 'Cancel') + 1.0, 2.0, DIALOG))
    S.append(('A-180-refusal-line', a, at(a, 'revolve full 180: live error'), at(a, 'revolve full 180: refused') + 0.5, 3.0, REASON))
    S.append(('A-split-line', a, at(a, 'Q11: double-click'), at(a, 'Finish Sketch') + 1.0, 1.5, VIEW))
    S.append(('A-split-refused', a, at(a, 'Revolve (Model tab', 1) - 0.5, at(a, 'Cancel', 1) + 1.0, 2.0, DIALOG))
    S.append(('A-split-refusal-line', a, at(a, 'split T: live error'), at(a, 'split T: refused') + 0.5, 3.0, REASON))
    b = 'B'
    S.append(('B-whole-T', b, 0.0, at(b, 'select the cap\'s left side'), 1.5, VIEW))
    S.append(('B-delete-left', b, at(b, 'select the cap\'s left side') - 0.3, at(b, 'Line tool'), 1.5, VIEW))
    S.append(('B-draw-axis-edge', b, at(b, 'Line tool') - 0.3, at(b, 'Finish Sketch') + 1.0, 1.5, VIEW))
    S.append(('B-revolve-half', b, at(b, 'Revolve (Model tab') - 0.5, at(b, 'OK') + 1.0, 2.0, DIALOG))
    S.append(('B-knob', b, at(b, 'Home view'), at(b, 'Inspect > Measure'), 1.5, VIEW))
    S.append(('B-measure-30', b, at(b, 'Inspect > Measure'), at(b, 'Inspect > Properties'), 2.0, MEASURE))
    S.append(('B-props-volume', b, at(b, 'Inspect > Properties'), at(b, 'recording stopped'), 2.0, PROPS))
    c = 'C'
    S.append(('C-line-rects', c, 0.0, at(c, 'Revolve (Model tab'), 1.5, VIEW))
    S.append(('C-c1-built', c, at(c, 'Revolve (Model tab') - 0.5, at(c, 'C2: Profile cleared'), 2.0, DIALOG))
    S.append(('C-c2-refused', c, at(c, 'C2: Profile cleared'), at(c, 'back to rectangle 1'), 2.0, DIALOG))
    S.append(('C-c2-refusal-line', c, at(c, 'C2: live error'), at(c, 'C2: refused') + 0.5, 3.0, REASON))
    S.append(('C-c1-ok', c, at(c, 'back to rectangle 1'), at(c, 'C1 body:'), 1.5, VIEW))
    S.append(('C-ring-square', c, at(c, 'Home view', 1), at(c, 'Revolve (Model tab', 1), 1.5, VIEW))
    S.append(('C-ring-revolve', c, at(c, 'Revolve (Model tab', 1) - 0.5, at(c, 'OK', 1) + 1.0, 2.0, DIALOG))
    S.append(('C-ring', c, at(c, 'Home view', 2), at(c, 'Inspect > Measure'), 1.5, VIEW))
    S.append(('C-ring-measure-outer', c, at(c, 'Inspect > Measure'), at(c, 'Inspect > Measure', 1), 2.0, MEASURE))
    S.append(('C-ring-measure-inner', c, at(c, 'Inspect > Measure', 1), at(c, 'Inspect > Properties'), 2.0, MEASURE))
    S.append(('C-ring-props', c, at(c, 'Inspect > Properties'), at(c, 'recording stopped'), 2.0, PROPS))
    d = 'D'
    S.append(('D-mcp-reply', d, 0.0, at(d, 'recording stopped'), 2.0, TERM))
    r = 'runs/R1'     # run on the PC (DEVIATIONS 13); the full clips show the greyed suggested prompt at the end: crop it
    S.append(('R1-prompt', r, 0.0, at(r, 'turn 1: Enter') + 0.3, 2.0, R1_PROMPT))
    S.append(('R1-working', r, at(r, 'turn 1: Claude working'), at(r, 'turn 1: end-of-turn line seen'), 2.0, R1_WORK))
    S.append(('R1-reply', r, at(r, 'turn 1: end-of-turn line seen') - 0.5, at(r, 'recording stopped'), 1.2, R1_REPLY))
    return S


def main():
    spec = importlib.util.spec_from_file_location('footage', os.environ['FOOTAGE_PY'])
    footage = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(footage)
    want = set(sys.argv[1:])
    os.makedirs(f'{OUT}/clips', exist_ok=True)
    out = []
    for name, take, t0, t1, zoom, centre in segs():
        if want and name not in want:
            continue
        for kind, z, c in (('full', 1.0, FULL), ('zoom', zoom, centre)):
            p = f'{OUT}/clips/{name}-{kind}.mp4'
            focus = [{'t': 0, 'box': [c[0] - 2, c[1] - 2, 4, 4]}]
            footage.clip(f'{OUT}/{take}/screen.mp4', p, src=SRC, t0=max(0.0, t0), t1=t1, zoom=z, size=SIZE, focus=focus)
            out.append({'clip': f'{name}-{kind}', 'take': take, 't0': round(t0, 2), 't1': round(t1, 2), 'zoom': z,
                        'box': list(footage.crop_box(c[0], c[1], z, SRC))})
    man = f'{OUT}/clips/clips.json'
    if want and os.path.exists(man):   # a partial re-cut keeps the other clips' rows, in segs() order
        new = {r['clip']: r for r in out}
        old = json.load(open(man))
        out = [new.pop(r['clip'], r) for r in old] + list(new.values())
    json.dump(out, open(man, 'w'), indent=1)
    print(len(out), 'clips')


if __name__ == '__main__':
    main()
