"""fx11 clips (SolidCraft Split Body refusal), cut by event time (the fx10clips.py pattern); takes A-D (the Claude
run runs/R1 is added when it runs on the PC). Every clip comes twice:
NAME-full.mp4 (the whole 2880x1620 display = the full SolidCraft window, zoom 1) and NAME-zoom.mp4 (the same span, a
fixed close-up), so the edit shows the full window first, then the zoom (owner rule 4 Nov). Silent, 1920x1080, 30 fps.
    docker run --rm --network none -v "$PWD:/work" -v VIDEOQA:/footage:ro -w /work sc5-l5:0.28.0         env FOOTAGE_PY=/footage/footage.py FX11_OUT=/work/out/fx11 python3 lab/fx11clips.py [name ...]
Writes out/fx11/clips/*.mp4 and out/fx11/clips/clips.json (spans, zoom boxes in source pixels).
Centres are source pixels (2880x1620) = 2 x the 1440x810 probe units of lab/fx11lib.sh."""
import importlib.util
import json
import os
import sys

OUT = os.environ.get('FX11_OUT', '/work/out/fx11')
SIZE = (1920, 1080)
SRC = (2880, 1620)
FULL = (1440, 810)
BROWSER = (300, 900)          # Browser > Origin (XY row 85,381), Bodies (94,475 / 100,498), Construction (96,568..615)
VIEW = (1674, 860)            # the 3D view: the tower (x 837 halved), the planes, the block
DIALOG = (2630, 720)          # the Split Body / Offset Plane / Midplane dialog (fields 1352,317..377, OK 1388,397..445)
REASON = (2580, 744)          # the live red line under the Split Body fields (1209..1366, 372 halved)
REPORT = (1440, 700)          # the Create Issue draft (Summary at 720,128; Close draft at 734,670)
PROPS = (1440, 684)           # Properties: BODY (543..897 x 175..510 halved; Close at 860,487)
TERM = (720, 1377)            # take D's terminal strip (y 1134..1620)


def ev(take):
    return [json.loads(line) for line in open(f'{OUT}/{take}/events.jsonl')]


def at(take, label, nth=0):
    rows = [e for e in ev(take) if e['event'].startswith(label)]
    return rows[nth]['t']


def segs():
    """(name, take, t0, t1, zoom, centre); one per filmed beat; every name gets -full and -zoom."""
    S = []
    a = 'A'
    S.append(('A-open-tower', a, 0.0, at(a, 'slow orbit'), 1.5, VIEW))
    S.append(('A-orbit', a, at(a, 'slow orbit'), at(a, 'Browser: expand Origin'), 1.5, VIEW))
    S.append(('A-xy-lit', a, at(a, 'Browser: expand Origin'), at(a, 'Split Body (Model tab'), 2.0, BROWSER))
    S.append(('A-split-dialog', a, at(a, 'Split Body (Model tab') - 0.5, at(a, 'Body to split'), 2.0, DIALOG))
    S.append(('A-split-xy-refused', a, at(a, 'Body to split'), at(a, 'split XY: refused') + 0.5, 2.0, DIALOG))
    S.append(('A-refusal-line', a, at(a, 'split XY: live error'), at(a, 'split XY: refused') + 0.5, 3.0, REASON))
    S.append(('A-report-draft', a, at(a, 'Create Issue'), at(a, 'Close draft') + 0.5, 2.0, REPORT))
    S.append(('A-after-cancel', a, at(a, 'Cancel'), at(a, 'F1: Inspect'), 1.5, VIEW))
    S.append(('A-section', a, at(a, 'F1: Inspect'), at(a, 'Cancel (section)') + 0.5, 1.5, VIEW))
    b = 'B'
    S.append(('B-open', b, 0.0, at(b, 'Offset Plane (Model tab'), 1.5, VIEW))
    S.append(('B-offset-dialog', b, at(b, 'Offset Plane (Model tab') - 0.5, at(b, 'Distance: 100'), 2.0, DIALOG))
    S.append(('B-offset-100', b, at(b, 'Distance: 100'), at(b, 'offset plane 100:'), 1.5, VIEW))
    S.append(('B-split-100', b, at(b, 'Split Body (Model tab') - 0.5, at(b, 'split 100:', 1), 2.0, DIALOG))
    S.append(('B-two-bodies', b, at(b, 'the Browser: two body rows'), at(b, 'right-click the body row'), 2.0, BROWSER))
    S.append(('B-props-row1', b, at(b, 'right-click the body row'), at(b, 'right-click the body row', 1), 2.0, PROPS))
    S.append(('B-props-row2', b, at(b, 'right-click the body row', 1), at(b, 'F11: hide the first'), 2.0, PROPS))
    S.append(('B-pieces', b, at(b, 'F11: hide the first'), at(b, 'Q3:'), 1.5, VIEW))
    q = 'B-q3'        # Q3 attempt 2 in its own container (take B's Midplane landed in the split tab: DEVIATIONS)
    S.append(('B-midplane', q, at(q, 'Midplane (Model'), at(q, 'midplane split:'), 1.5, VIEW))
    c = 'C'
    S.append(('C-sym-open', c, 0.0, at(c, 'Split Body (Model tab'), 1.5, VIEW))
    S.append(('C-sym-split', c, at(c, 'Split Body (Model tab') - 0.5, at(c, 'sym split XY:', 1), 2.0, DIALOG))
    S.append(('C-sym-props-row1', c, at(c, 'right-click the body row'), at(c, 'right-click the body row', 1), 2.0, PROPS))
    S.append(('C-sym-props-row2', c, at(c, 'right-click the body row', 1), at(c, 'Q4:'), 2.0, PROPS))
    S.append(('C-above-210', c, at(c, 'Q4:'), at(c, 'split 210: '), 1.5, VIEW))
    S.append(('C-above-refused', c, at(c, 'Split Body (Model tab', 1) - 0.5, at(c, 'after Cancel'), 2.0, DIALOG))
    S.append(('C-above-refusal-line', c, at(c, 'split 210: live error'), at(c, 'split 210: refused') + 0.5, 3.0, REASON))
    S.append(('C-s2-frame', c, at(c, 'S2 end frame'), at(c, 'Split Body (Model tab', 2), 1.5, VIEW))
    S.append(('C-at-200', c, at(c, 'Split Body (Model tab', 2) - 0.5, at(c, 'the planes hidden'), 2.0, DIALOG))
    S.append(('C-top-face', c, at(c, 'Split Body (Model tab', 3) - 0.5, at(c, 'after Q6'), 2.0, DIALOG))
    S.append(('C-block-open', c, at(c, 'Q5b:'), at(c, 'Offset Plane (Model tab', 2), 1.5, VIEW))
    S.append(('C-block-split', c, at(c, 'Offset Plane (Model tab', 2), at(c, 'block split 40:', 1), 1.5, VIEW))
    S.append(('C-block-props-row1', c, at(c, 'right-click the body row', 2), at(c, 'right-click the body row', 3), 2.0, PROPS))
    S.append(('C-block-props-row2', c, at(c, 'right-click the body row', 3), at(c, 'hold 3 s'), 2.0, PROPS))
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
