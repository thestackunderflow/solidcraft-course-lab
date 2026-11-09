"""fx6 clips, cut by event time (footage.py hand-off; the fx1clips.py pattern). Every clip comes twice: NAME-full.mp4 (the
whole 2880x1620 display = the full SolidCraft window, zoom 1) and NAME-zoom.mp4 (the same span, a fixed close-up), so
the edit shows the full window first, then a locator, then the zoom (owner rule 4 Nov). Silent, 1920x1080, 30 fps.
    docker run --rm -v LAB:/lab -v VIDEOQA:/footage:ro screen-lab-base:1 \
        env FOOTAGE_PY=/footage/footage.py python3 /lab/lab/fx6clips.py [name ...]
Writes out/fx6/clips/*.mp4 and out/fx6/clips/clips.json (spans, zoom boxes in source pixels)."""
import importlib.util
import json
import os
import sys

spec = importlib.util.spec_from_file_location('footage', os.environ['FOOTAGE_PY'])
footage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(footage)

OUT = os.environ.get('FX6_OUT', '/lab/out/fx6')
SIZE = (1920, 1080)
SRC = (2880, 1620)
FULL = (1440, 810)            # centre of the display: zoom 1 = the whole frame
PANEL = (2200, 1150)          # the lip + the Fillet panel's red line (zoom 2)
REASON = (2630, 1140)         # the red line itself (zoom 3)
ROW = (2100, 1102)            # the Parameters thickness row (zoom 2.5)
LIP = (1800, 1200)            # the lip's round (zoom 2.5)
REPORT = (1440, 300)          # the Report a bug draft's Summary (zoom 2.5)
TERM = (720, 840)             # the terminal's two replies (zoom 2)


def ev(take):
    return [json.loads(l) for l in open(f'{OUT}/{take}/events.jsonl')]


def at(take, label, nth=0, prefix=False):
    rows = [e for e in ev(take) if (e['event'].startswith(label) if prefix else e['event'] == label)]
    return rows[nth]['t']


def segs():
    """(name, take, t0, t1, zoom, centre) ; every name gets -full and -zoom."""
    S = []
    a = 'A'
    S.append(('A-params-thickness5', a, at(a, 'params: hover Parameters') - 0.5, at(a, 'params: close (Cancel)') + 0.5, 2.5, ROW))
    S.append(('A-refusal', a, at(a, 'fillet: Fillet button') - 1.0, at(a, 'fillet 6: +5 s (screenshot refusal-5s.png)') + 2.0, 2.0, PANEL))
    S.append(('A-reason-line', a, at(a, 'fillet: radius 6 typed') + 1.5, at(a, 'fillet: OK') + 0.4, 3.0, REASON))   # the hold before OK: after it the cursor rests on the line
    S.append(('A-report-draft', a, at(a, 'report: hover Create Issue...') - 0.5, at(a, 'report: Close draft') + 1.0, 2.5, REPORT))
    S.append(('A-open-full-window', a, 0.0, at(a, 'params: hover Parameters'), 1.0, FULL))
    b = 'B'
    for r in ('4.0', '5.0'):
        S.append((f'B-r{r}', b, at(b, f'fillet {r}: Fillet button') - 0.5, at(b, f'fillet {r}: OK') + 4.0, 2.0, PANEL))
    for r in ('4.9', '5.1'):
        S.append((f'B-r{r}', b, at(b, f'fillet {r}: Fillet button (part 2)') - 0.5, at(b, f'fillet {r}: OK (part 2)') + 4.0, 2.0, PANEL))
    S.append(('B-F2-radius5-clean', b, at(b, 'F2 clean: full window 3 s'), at(b, 'F2 clean: toolbar Undo'), 2.5, LIP))
    c = 'C-clean'
    S.append(('C-thickness8-row', c, at(c, 'params: open (thickness to 8)'), at(c, 'params: OK') + 1.0, 2.5, ROW))
    S.append(('C-thick8-fillet6', c, at(c, 'thick-8: hold 3 s on the hook'), at(c, 'toolbar Undo'), 2.0, PANEL))
    S.append(('C-thickness5-back', c, at(c, 'params: open (thickness to 5)'), at(c, 'recording stopped'), 2.5, ROW))
    S.append(('C2-bottom-back-6', 'C2', 0.0, at('C2', 'recording stopped'), 1.6, (1900, 1150)))
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
