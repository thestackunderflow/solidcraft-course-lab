"""fx14b clips (SolidCraft Create Sketch: "this face has no supported stable semantic lineage" after Convert Mesh), cut
by event time (the fx13clips.py pattern); takes A, B, C (your turn), C2 (the Hole), D, E (the Claude run runs/R1 is added when it runs on the PC).
Every clip comes twice: NAME-full.mp4 (the whole 2880x1620 display = the full SolidCraft window, zoom 1) and
NAME-zoom.mp4 (the same span, a fixed close-up), so the edit shows the full window first, then the zoom (owner rule
4 Nov). Silent, 1920x1080, 30 fps.
    docker run --rm --network none -v "$PWD:/work" -v VIDEOQA:/footage:ro -w /work sc5-l5:0.28.0 \
        env FOOTAGE_PY=/footage/footage.py FX14B_OUT=/work/out/fx14b python3 lab/fx14bclips.py [name ...]
Writes out/fx14b/clips/*.mp4 and out/fx14b/clips/clips.json (spans, zoom boxes in source pixels).
Centres are source pixels (2880x1620) = 2 x the 1440x810 probe units of lab/fx14blib.sh."""
import importlib.util
import json
import os
import sys

OUT = os.environ.get('FX14B_OUT', '/work/out/fx14b')
SIZE = (1920, 1080)
SRC = (2880, 1620)
FULL = (1440, 810)
VIEW = (1674, 860)            # the 40 x 30 x 20 block at the Home view (530..1145 x 153..710 halved)
DIALOG = (2630, 830)          # the Create Sketch / Extrude dialog (1200..1430 x 255..600 halved)
REASON = (2630, 916)          # the hint, Use fixed plane and the red line (1209..1420 x 355..490 halved)
USE_FIXED = (2508, 826)       # the Use fixed plane button (1254, 413 halved)
HOLE_DLG = (2630, 1100)       # the Hole dialog's lower half: Drill Point, Depth, Diameter (1200..1430 x 460..740 halved)
REPORT = (1440, 704)          # the Report a bug draft (412..1028 x 15..690 halved; Summary at 720,128)
PROPS = (1440, 680)           # Properties: conv (543..897 x 175..510 halved)
MEASURE = (2630, 660)         # the Measure panel (1200..1430 x 255..410 halved)
SKETCH40 = (1936, 520)        # the fixed-plane sketch on the 40 x 30 top, circle at (968, 234) halved
SKETCH30 = (1950, 440)        # the fixed-plane sketch on the 30 x 30 top, circle at (975, 165) halved
HIST = (900, 1520)            # the History bar icons and their tooltips (250..650 x 715..800 halved)
HIST_MENU = (900, 1300)       # a History icon's right-click menu (355..535 x 515..785 halved)
BROWSER = (240, 560)          # the Browser panel (8..230 x 150..420 halved)
MENU = (592, 190)             # Model tab > Create > Hole (296, 90 halved)
SEARCH = (2390, 680)          # Search commands: mesh (962..1428 x 40..640 halved)
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
    S.append(('A-open', a, 0.0, at(a, 'slow orbit'), 1.5, VIEW))
    S.append(('A-orbit', a, at(a, 'slow orbit'), at(a, 'History bar: the first'), 1.5, VIEW))
    S.append(('A-history', a, at(a, 'History bar: the first'), at(a, 'Browser: open'), 2.0, HIST))
    S.append(('A-features', a, at(a, 'Browser: open'), at(a, 'Create Sketch'), 2.0, BROWSER))
    S.append(('A-sketch-pick', a, at(a, 'Create Sketch'), at(a, 'sketch on converted top'), 1.5, VIEW))
    S.append(('A-refusal-line', a, at(a, 'sketch on converted top'), at(a, 'the line held'), 3.0, REASON))
    S.append(('A-line-hold', a, at(a, 'the line held'), at(a, 'Create Issue'), 2.0, REASON))
    S.append(('A-report-draft', a, at(a, 'Create Issue'), at(a, 'Close draft') + 0.5, 1.2, REPORT))
    S.append(('A-cancel', a, at(a, 'Cancel'), at(a, 'recording stopped'), 1.5, VIEW))
    b = 'B'
    S.append(('B-open', b, 0.0, at(b, 'Browser: the body row'), 1.5, VIEW))
    S.append(('B-props-before', b, at(b, 'Browser: the body row'), at(b, 'Close') + 0.5, 2.0, PROPS))
    S.append(('B-line', b, at(b, 'Create Sketch'), at(b, 'zoom target'), 2.0, DIALOG))
    S.append(('B-use-fixed', b, at(b, 'zoom target'), at(b, 'fixed plane: sketch opened'), 2.5, USE_FIXED))
    S.append(('B-sketch-opens', b, at(b, 'click Use fixed plane'), at(b, 'Sketch > Circle'), 1.5, SKETCH40))
    S.append(('B-circle', b, at(b, 'Sketch > Circle'), at(b, 'Finish Sketch'), 2.0, SKETCH40))
    S.append(('B-cut', b, at(b, 'Model > Extrude'), at(b, 'the cut as shown') + 3.0, 1.5, VIEW))
    S.append(('B-cut-dialog', b, at(b, 'Operation: Cut'), at(b, 'OK'), 2.0, DIALOG))
    S.append(('B-props', b, at(b, 'Browser: the body row', 1), at(b, 'Close', 1) + 0.5, 2.0, PROPS))
    S.append(('B-area', b, at(b, 'Inspect > Measure'), at(b, 'Measure: close'), 2.0, MEASURE))
    S.append(('B-turning', b, at(b, 'F11'), at(b, 'recording stopped'), 1.5, VIEW))
    c = 'C2'                  # the Hole (Q24): take C2 (take C's OK click missed the shrunken dialog; DEVIATIONS)
    S.append(('C-hole-menu', c, at(c, 'zoom target'), at(c, 'Hole dialog'), 2.5, MENU))
    S.append(('C-hole-pick', c, at(c, 'Hole dialog'), at(c, 'Depth'), 1.5, VIEW))
    S.append(('C-hole-fields', c, at(c, 'Depth'), at(c, 'Drill Point: Flat'), 2.0, HOLE_DLG))
    S.append(('C-hole-flat', c, at(c, 'Drill Point: Flat'), at(c, 'OK'), 2.0, HOLE_DLG))
    S.append(('C-hole-ok', c, at(c, 'OK'), at(c, 'Browser: the body row'), 1.5, VIEW))
    S.append(('C-hole-props', c, at(c, 'Browser: the body row'), at(c, 'Close') + 0.5, 2.0, PROPS))
    S.append(('C-timeline', c, at(c, 'History bar: the new icon'), at(c, 'recording stopped'), 2.0, HIST))
    c = 'C'                   # the your-turn block (Q26), take C step 2
    S.append(('C-yourturn-open', c, at(c, 'Q26: open'), at(c, 'Create Sketch'), 1.5, VIEW))
    S.append(('C-yourturn-line', c, at(c, 'Create Sketch'), at(c, 'click Use fixed plane'), 2.0, DIALOG))
    S.append(('C-yourturn-fixed', c, at(c, 'click Use fixed plane'), at(c, 'Finish Sketch'), 1.5, SKETCH30))
    S.append(('C-yourturn-cut', c, at(c, 'Finish Sketch'), at(c, 'your-turn cut'), 1.5, VIEW))
    S.append(('C-yourturn-props', c, at(c, 'Browser: the body row', 1), at(c, 'Close', 1) + 0.5, 2.0, PROPS))
    d = 'D'
    S.append(('D-mcp-reply', d, 0.0, at(d, 'recording stopped'), 2.0, TERM))
    e = 'E'
    S.append(('E-convert-edit', e, at(e, 'Q25: History bar: ConvertMesh1'), at(e, 'Q25: History bar: the first'), 1.5,
              HIST_MENU))
    S.append(('E-insert-edit', e, at(e, 'Q25: History bar: the first'), at(e, 'Q25: Search'), 1.5, HIST_MENU))
    S.append(('E-search', e, at(e, 'Q25: Search'), at(e, 'Q21: open'), 1.5, SEARCH))
    S.append(('E-plain-block', e, at(e, 'Q21: the plain block'), at(e, 'Create Sketch'), 1.5, VIEW))
    S.append(('E-control', e, at(e, 'Q21: click'), at(e, 'Cancel (Sketch tab'), 1.5, VIEW))
    S.append(('E-extrude-face', e, at(e, 'Q23: Model > Extrude'), at(e, 'Q23 after OK'), 1.5, DIALOG))
    S.append(('E-offset', e, at(e, 'Q28: click'), at(e, 'Cancel (Sketch tab', 1), 1.5, VIEW))
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
