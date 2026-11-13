"""fx12 clips (SolidCraft sketch Fillet on an offset copy: "its corners follow its source curves"), cut by event time
(the fx11clips.py pattern); takes A, B, C, C2 (Q12), D (the Claude run runs/R1 is added when it runs on the PC).
Every clip comes twice: NAME-full.mp4 (the whole 2880x1620 display = the full SolidCraft window, zoom 1) and
NAME-zoom.mp4 (the same span, a fixed close-up), so the edit shows the full window first, then the zoom (owner rule
4 Nov). Silent, 1920x1080, 30 fps.
    docker run --rm --network none -v "$PWD:/work" -v VIDEOQA:/footage:ro -w /work sc5-l5:0.28.0         env FOOTAGE_PY=/footage/footage.py FX12_OUT=/work/out/fx12 python3 lab/fx12clips.py [name ...]
Writes out/fx12/clips/*.mp4 and out/fx12/clips/clips.json (spans, zoom boxes in source pixels).
Centres are source pixels (2880x1620) = 2 x the 1440x810 probe units of lab/fx12lib.sh."""
import importlib.util
import json
import os
import sys

OUT = os.environ.get('FX12_OUT', '/work/out/fx12')
SIZE = (1920, 1080)
SRC = (2880, 1620)
FULL = (1440, 810)
VIEW = (1440, 840)            # the sketch: outline x 438..1001, y 232..607 halved
CORNER = (1966, 500)          # the top-right corners (outline 1001,232; copy 983,251 halved)
TWO_MM = (1400, 1198)         # the 2.00 mm offset dimension (700,599 halved)
DIALOG = (712, 930)           # the sketch Fillet / Chamfer / Offset dialog (240..473 x 300..640 halved)
REASON = (710, 1024)          # the red line under the Fillet fields (250..460 x 485..540 halved)
MENU = (1424, 1000)           # the right-click menu (603..823 x 190..800 halved; Break Offset Association 695,388)
REPORT = (1440, 700)          # the Create Issue draft (Summary at 720,128; Close draft at 734,670)
PROPS = (1440, 684)           # Properties: Body1 (543..897 x 175..510 halved; Close at 860,487)
MEASURE = (710, 1060)         # the sketch-mode Measure panel (240..473 x 300..760 halved)
TERM = (720, 1377)            # take D's terminal strip (y 1134..1620)


def ev(take):
    return [json.loads(line) for line in open(f'{OUT}/{take}/events.jsonl')]


def at(take, label, nth=0):
    rows = [e for e in ev(take) if e['event'].startswith(label)]
    return rows[nth]['t']


def round_first(S, c, tag):
    """take C (round 5) or C2 (round 1.5, Q12): the same steps, lab/fx12C.sh"""
    S.append((f'{c}-open', c, 0.0, at(c, 'Browser: double-click'), 1.5, VIEW))
    S.append((f'{c}-round-{tag}', c, at(c, 'Sketch > Modify > Fillet') - 0.5, at(c, 'Sketch > Modify > Offset'), 1.5, VIEW))
    S.append((f'{c}-round-dialog', c, at(c, 'Sketch > Modify > Fillet') - 0.5, at(c, 'outline rounded'), 2.0, DIALOG))
    S.append((f'{c}-offset', c, at(c, 'Sketch > Modify > Offset') - 0.5, at(c, 'Inspect > Measure'), 1.5, VIEW))
    S.append((f'{c}-offset-dialog', c, at(c, 'Sketch > Modify > Offset') - 0.5, at(c, 'offset after round'), 2.0, DIALOG))
    S.append((f'{c}-corner', c, at(c, 'offset after round'), at(c, 'Inspect > Measure'), 2.5, CORNER))
    S.append((f'{c}-measure-r3' if c == 'C' else f'{c}-measure', c, at(c, 'Measure: the inside corner'),
              at(c, 'Measure: add'), 2.0, MEASURE))
    S.append((f'{c}-wall', c, at(c, 'Measure: add'), at(c, 'Finish Sketch'), 2.0, MEASURE))
    S.append((f'{c}-extrude', c, at(c, 'Model > Extrude'), at(c, 'Browser: Body1'), 1.5, VIEW))
    S.append((f'{c}-props', c, at(c, 'Browser: Body1'), at(c, 'hold 3 s'), 2.0, PROPS))


def segs():
    """(name, take, t0, t1, zoom, centre); one per filmed beat; every name gets -full and -zoom."""
    S = []
    a = 'A'
    S.append(('A-open-tray', a, 0.0, at(a, 'Browser: double-click'), 1.5, VIEW))
    S.append(('A-sketch-copy', a, at(a, 'Browser: double-click'), at(a, 'Sketch > Modify > Fillet'), 1.5, VIEW))
    S.append(('A-two-mm', a, at(a, 'the sketch with the copy'), at(a, 'Sketch > Modify > Fillet'), 2.5, TWO_MM))
    S.append(('A-fillet-refused', a, at(a, 'Sketch > Modify > Fillet') - 0.5, at(a, 'Create Issue'), 2.0, DIALOG))
    S.append(('A-refusal-line', a, at(a, 'fillet copy'), at(a, 'Create Issue') + 0.5, 3.0, REASON))
    S.append(('A-report-draft', a, at(a, 'Create Issue'), at(a, 'Close draft') + 0.5, 2.0, REPORT))
    S.append(('A-after-cancel', a, at(a, 'Cancel'), at(a, 'Sketch > Modify > Equal'), 1.5, VIEW))
    S.append(('A-chamfer-refused', a, at(a, 'Sketch > Modify > Equal') - 0.5, at(a, 'after:'), 2.0, DIALOG))
    b = 'B'
    S.append(('B-open', b, 0.0, at(b, "select the copy's top line"), 1.5, VIEW))
    S.append(('B-break-menu', b, at(b, "select the copy's top line"), at(b, 'after one Break'), 2.0, MENU))
    S.append(('B-fillet-4', b, at(b, 'Sketch > Modify > Fillet') - 0.5, at(b, 'fillet after break'), 1.5, VIEW))
    S.append(('B-rounded', b, at(b, 'fillet after break'), at(b, 'Finish Sketch'), 2.5, CORNER))
    S.append(('B-extrude', b, at(b, 'Model > Extrude'), at(b, 'Browser: Body1'), 1.5, VIEW))
    S.append(('B-props', b, at(b, 'Browser: Body1'), at(b, 'Edit Sketch again'), 2.0, PROPS))
    w = 'B-wall'      # Q11 Fix 1, attempt 2 in its own container, measured before Finish (DEVIATIONS)
    S.append(('Bw-wall', w, at(w, 'Inspect > Measure'), at(w, 'Finish Sketch'), 2.0, MEASURE))
    S.append(('Bw-wall-corner', w, at(w, 'Inspect > Measure'), at(w, 'Finish Sketch'), 2.5, CORNER))
    round_first(S, 'C', '5')
    round_first(S, 'C2', '1-5')
    d = 'D'
    S.append(('D-mcp-reply', d, 0.0, at(d, 'recording stopped'), 2.0, TERM))
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
