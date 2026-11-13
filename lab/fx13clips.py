"""fx13 clips (SolidCraft Shell: "Tangent Chain opens every face of this body, leaving no walls"), cut by event time
(the fx12clips.py pattern); takes A, B, C, D (the Claude run runs/R1 is added when it runs on the PC).
Every clip comes twice: NAME-full.mp4 (the whole 2880x1620 display = the full SolidCraft window, zoom 1) and
NAME-zoom.mp4 (the same span, a fixed close-up), so the edit shows the full window first, then the zoom (owner rule
4 Nov). Silent, 1920x1080, 30 fps.
    docker run --rm --network none -v "$PWD:/work" -v VIDEOQA:/footage:ro -w /work sc5-l5:0.28.0         env FOOTAGE_PY=/footage/footage.py FX13_OUT=/work/out/fx13 python3 lab/fx13clips.py [name ...]
Writes out/fx13/clips/*.mp4 and out/fx13/clips/clips.json (spans, zoom boxes in source pixels).
Centres are source pixels (2880x1620) = 2 x the 1440x810 probe units of lab/fx13lib.sh."""
import importlib.util
import json
import os
import sys

OUT = os.environ.get('FX13_OUT', '/work/out/fx13')
SIZE = (1920, 1080)
SRC = (2880, 1620)
FULL = (1440, 810)
VIEW = (1674, 860)            # the cup (D60 x 80 at the fit view: x 690..985, y 190..672 halved)
DIALOG = (2630, 840)          # the Shell dialog (1200..1430 x 255..590 halved)
REASON = (2610, 954)          # the red line under Tangent chain (1209..1405 x 455..500 halved)
CHAIN = (2500, 876)           # the Tangent chain checkbox and its label (1215,438 halved)
REPORT = (1440, 704)          # the Report a bug draft (412..1028 x 15..690 halved; Summary at 720,128)
PROPS = (1440, 680)           # Properties: Body1 (543..897 x 175..510 halved)
MEASURE = (2630, 860)         # the Measure panel (1200..1430 x 255..600 halved)
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
    S.append(('A-open-cup', a, 0.0, at(a, 'slow orbit'), 1.5, VIEW))
    S.append(('A-orbit', a, at(a, 'slow orbit'), at(a, 'Inspect > Section'), 1.5, VIEW))
    S.append(('A-section-solid', a, at(a, 'section of the solid cup'), at(a, 'section off'), 1.5, VIEW))
    S.append(('A-shell-dialog', a, at(a, 'Shell (Model') - 0.5, at(a, 'click the top'), 2.0, DIALOG))
    S.append(('A-preview-all', a, at(a, 'click the top'), at(a, 'Thickness'), 1.5, VIEW))
    S.append(('A-refusal-line', a, at(a, 'shell top chain on'), at(a, 'the line held'), 3.0, REASON))
    S.append(('A-line-hold', a, at(a, 'the line held'), at(a, 'Create Issue'), 2.0, REASON))
    S.append(('A-report-draft', a, at(a, 'Create Issue'), at(a, 'Close draft') + 0.5, 1.2, REPORT))
    S.append(('A-cancel', a, at(a, 'Cancel'), at(a, 'Q3b'), 1.5, VIEW))
    S.append(('A-side-pick', a, at(a, 'click the SIDE'), at(a, 'close the dialog'), 1.5, VIEW))
    S.append(('A-side-line', a, at(a, 'shell side chain on'), at(a, 'close the dialog'), 2.0, DIALOG))
    b = 'B'
    S.append(('B-open', b, 0.0, at(b, 'Shell (Model'), 1.5, VIEW))
    S.append(('B-untick', b, at(b, 'zoom target'), at(b, 'click the top'), 3.0, CHAIN))
    S.append(('B-preview-top', b, at(b, 'click the top'), at(b, 'Thickness'), 1.5, VIEW))
    S.append(('B-ok', b, at(b, 'Thickness'), at(b, 'Browser: Body1'), 1.5, VIEW))
    S.append(('B-props', b, at(b, 'Browser: Body1'), at(b, 'Close') + 0.5, 2.0, PROPS))
    S.append(('B-section', b, at(b, 'Inspect > Section'), at(b, 'Inspect > Measure'), 1.5, VIEW))
    S.append(('B-wall', b, at(b, 'Measure: the outer side'), at(b, 'Measure: clear'), 2.0, MEASURE))
    S.append(('B-floor', b, at(b, 'Measure: the inner floor'), at(b, 'Measure: close'), 2.0, MEASURE))
    S.append(('B-turning', b, at(b, 'F11'), at(b, 'recording stopped'), 1.5, VIEW))
    c = 'C'
    S.append(('C-second-cup', c, 0.0, at(c, 'Shell (Model'), 1.5, VIEW))
    S.append(('C-second-preview', c, at(c, 'click the top face, chain left on'), at(c, 'OK'), 1.5, VIEW))
    S.append(('C-second-ok', c, at(c, 'OK'), at(c, 'Browser: Body1'), 1.5, VIEW))
    S.append(('C-second-props', c, at(c, 'Browser: Body1'), at(c, 'Close') + 0.5, 2.0, PROPS))
    S.append(('C-yourturn-untick', c, at(c, 'zoom target'), at(c, 'click the top face, chain off'), 3.0, CHAIN))
    S.append(('C-yourturn-ok', c, at(c, 'click the top face, chain off'), at(c, 'Browser: Body1', 1), 1.5, VIEW))
    S.append(('C-yourturn-props', c, at(c, 'Browser: Body1', 1), at(c, 'Close', 1) + 0.5, 2.0, PROPS))
    S.append(('C-r3', c, at(c, 'open ~/cup-r3'), at(c, 'close the dialog'), 1.5, VIEW))
    S.append(('C-r3-dialog', c, at(c, 'r3 chain off'), at(c, 'OK', 2) + 2.5, 2.0, DIALOG))
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
