"""fx8 clips, cut by event time (footage.py hand-off; the fx6clips.py pattern). Every clip comes twice: NAME-full.mp4 (the
whole 2880x1620 display = the full SolidCraft window, zoom 1) and NAME-zoom.mp4 (the same span, a fixed close-up), so
the edit shows the full window first, then a locator, then the zoom (owner rule 4 Nov). Silent, 1920x1080, 30 fps.
    docker run --rm -v LAB:/lab -v VIDEOQA:/footage:ro screen-lab-base:1 \
        env FOOTAGE_PY=/footage/footage.py FX8_OUT=/lab/out/fx8 python3 /lab/lab/fx8clips.py [name ...]
Writes out/fx8/clips/*.mp4 and out/fx8/clips/clips.json (spans, zoom boxes in source pixels).
Centres are source pixels (2880x1620) = 2 x the 1440x810 probe units."""
import importlib.util
import json
import os
import sys

spec = importlib.util.spec_from_file_location('footage', os.environ['FOOTAGE_PY'])
footage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(footage)

OUT = os.environ.get('FX8_OUT', '/lab/out/fx8')
SIZE = (1920, 1080)
SRC = (2880, 1620)
FULL = (1440, 810)
BROWSER = (300, 560)          # the Browser panel (mesh body rows)
PANEL = (2560, 800)           # a right-hand dialog (Convert Mesh, Extrude, Hole, Fillet)
REASON_CONVERT = (2620, 772)  # the Convert Mesh dialog's red line
REASON_CUT = (2610, 1136)     # the Extrude panel's red line
REASON_HOLE = (2610, 1408)    # the Hole panel's red line on the mesh
REASON_FILLET = (2560, 1110)  # the Fillet panel's red line
PROPS = (1440, 420)           # Properties: volume, area, bounding box, faces
TIMELINE = (500, 1500)        # the History bar
REPORT = (1440, 250)          # the Report a bug draft's Summary
HOOKS = (1680, 860)           # the two hooks side by side
TERM = (720, 840)


def ev(take):
    return [json.loads(l) for l in open(f'{OUT}/{take}/events.jsonl')]


def at(take, label, nth=0):
    rows = [e for e in ev(take) if e['event'].startswith(label)]
    return rows[nth]['t']


def segs():
    """(name, take, t0, t1, zoom, centre); every name gets -full and -zoom."""
    S = []
    a = 'A'
    S.append(('A-open-full-window', a, 0.0, at(a, 'browser:') + 4.5, 2.5, BROWSER))
    # take A's cut step missed OK (no cut tried); the cut is take A2, the same design (DEVIATIONS)
    S.append(('A-cut-refused', 'A2', at('A2', 'cut: Extrude button') - 0.5, at('A2', 'cut: Cancel'), 2.0, PANEL))
    S.append(('A-cut-reason-line', 'A2', at('A2', 'cut: result held'), at('A2', 'cut: Cancel'), 3.0, REASON_CUT))
    S.append(('A-hole-on-mesh', a, at(a, 'hole on mesh: Hole button') - 0.5, at(a, 'hole on mesh: Cancel'), 3.0, REASON_HOLE))
    S.append(('A-fillet-refused', a, at(a, 'fillet on mesh: Fillet button') - 0.5, at(a, 'fillet on mesh: Cancel'), 3.0, REASON_FILLET))
    S.append(('A-measure', a, at(a, 'measure: select'), at(a, 'measure: Close') + 0.5, 2.0, PROPS))
    S.append(('A-convert-refused', a, at(a, 'convert: select') - 0.5, at(a, 'report: Create Issue'), 2.0, PANEL))
    S.append(('A-convert-reason-line', a, at(a, 'convert hook.stl: refusal shown'), at(a, 'report: Create Issue'), 3.0, REASON_CONVERT))
    S.append(('A-report-draft', a, at(a, 'report: Create Issue'), at(a, 'report: Close draft') + 0.5, 2.5, REPORT))
    b = 'B'
    S.append(('B-convert-plain', b, 0.0, at(b, 'measure: Inspect tab'), 2.5, BROWSER))
    S.append(('B-converted-timeline', b, at(b, 'convert hook-plain: timeline'), at(b, 'measure: Inspect tab'), 2.5, TIMELINE))
    S.append(('B-measure-converted', b, at(b, 'measure: Properties'), at(b, 'measure: Close') + 0.5, 2.0, PROPS))
    S.append(('B-hole-built', b, at(b, 'hole: Model tab'), at(b, 'measure: Properties after'), 2.0, PANEL))
    S.append(('B-hole-timeline', b, at(b, 'hole on converted: timeline'), at(b, 'measure: Properties after'), 2.5, TIMELINE))
    S.append(('B-measure-hole', b, at(b, 'measure: Properties after'), at(b, 'measure: Close', 1) + 0.5, 2.0, PROPS))
    c = 'C'
    S.append(('C-both-convert', c, 0.0, at(c, 'convert hook: Cancel') + 1.0, 1.5, HOOKS))
    S.append(('C-both-browser', c, at(c, 'convert hook-plain: select'), at(c, 'convert hook: Cancel'), 2.5, BROWSER))
    S.append(('C-hook-reason-line', c, at(c, 'convert hook: result held'), at(c, 'convert hook: Cancel'), 3.0, REASON_CONVERT))
    S.append(('C-box-endframe', c, at(c, 'box: S2 end frame'), at(c, 'convert box-round: select'), 1.5, HOOKS))
    S.append(('C-box-convert', c, at(c, 'convert box-round: select'), at(c, 'recording stopped'), 2.0, PANEL))
    S.append(('D-mcp-replies', 'D', 0.0, at('D', 'recording stopped'), 2.0, TERM))
    if os.path.exists(f'{OUT}/runs/R1/events.jsonl'):
        r = ev('runs/R1')
        S.append(('R1-claude', 'runs/R1', 0.0, r[-1]['t'], 2.0, (720, 890)))
    return S


def main():
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
    json.dump(out, open(f'{OUT}/clips/clips.json', 'w'), indent=1)
    print(len(out), 'clips')


main()
