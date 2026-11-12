"""fx10 take P (LAB-fx10 section 3, not filmed): the knob sketches, no AI, over the plug entry SolidCraft wrote
(lesson-7 client pattern, as out/fx9/P/nut.py). On the XZ plane, one closed polyline:
  full T (centred on the vertical axis): cap x -15..15, z 15..23; stem x -6..6, z 0..15 -> ~/knob-full.sc
  half (x 0..15 / 0..6, touching the axis)                                         -> ~/knob-half.sc
Sketch only (finished, not revolved). Then, in throwaway designs (not saved), a check: the half revolved 360 about the
sketch's vertical axis (expected 7,351 mm3, ACCURACY B.13) and the full T the same way (expected refused, B.10).
    FX9_ALLOW=1 python3 -I knob.py OUT_DIR
Every JSON-RPC message -> OUT/rpc.jsonl; results -> OUT/volume.txt."""
import json
import os
import sys

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

OUT = sys.argv[1]
e = entry.read(os.path.expanduser('~/.claude.json'))
c = McpClient([e['command']] + e['args'] + ['--allow-path', os.path.expanduser('~')], timeout_s=120,
              log_path=os.path.join(OUT, 'rpc.jsonl'))
c.start()
log = open(os.path.join(OUT, 'volume.txt'), 'w')

# The XZ sketch's y runs along world -Z in 0.28.0 (attempt 1: bbox z -23..0, the T upside down in the window), so the
# sketch y is the negative of world z: the cap sits at world z 15..23, above the stem (DEVIATIONS 1).
FULL = [[-15, -23], [15, -23], [15, -15], [6, -15], [6, 0], [-6, 0], [-6, -15], [-15, -15]]
HALF = [[0, -23], [15, -23], [15, -15], [6, -15], [6, 0], [0, 0]]


def jt(name, args):
    r = c.call_tool(name, args)
    s = McpClient.text(r).split('\nNote:')[0]
    try:
        return r.get('isError'), json.loads(s)
    except ValueError:
        return r.get('isError'), {'text': s}


def out(line):
    print(line, flush=True)
    log.write(line + '\n')


def sketch(pts, tag):
    jt('new_design', {})
    err, r = jt('batch', {'commands': [
        {'command': 'sketch.create', 'params': {'plane': 'XZ'}},
        {'command': 'sketch.line', 'params': {'closed': True, 'points': pts}},
        {'command': 'sketch.finish', 'params': {}}], 'verbose': False})
    out(f'{tag} sketch: isError {err}; ' + json.dumps(r)[:300])


def save(path):
    err, r = jt('save', {'path': path})
    out(f'save {os.path.basename(path)}: isError {err}; ' + json.dumps(r)[:200])


def read(tag):
    _, m = jt('measure', {})
    _, d = jt('inspect_design', {})
    json.dump({'measure': m, 'design': d}, open(os.path.join(OUT, f'read-{tag}.json'), 'w'), indent=1)
    b = (m.get('bodies') or [{}])[0] if isinstance(m, dict) else {}
    out(f'{tag}: volume_mm3 {(m.get("total") or {}).get("volume_mm3") if isinstance(m, dict) else m} '
        f'bbox {json.dumps(b.get("bbox") or b.get("bounding_box") or ((m.get("total") or {}).get("bbox") if isinstance(m, dict) else None))} '
        f'timeline {json.dumps([f.get("name") or f.get("type") for f in (d.get("timeline") or [])]) if isinstance(d, dict) else d}')


sketch(FULL, 'full')
read('full-sketch')
save(os.path.expanduser('~/knob-full.sc'))
sketch(HALF, 'half')
save(os.path.expanduser('~/knob-half.sc'))
# checks in throwaway designs (not saved): the sketch's vertical axis is 'y' (sketch axes) on XZ
for pts, tag in ((HALF, 'check-half'), (FULL, 'check-full')):
    sketch(pts, tag)
    err, r = jt('execute', {'command': 'solid.revolve', 'params': {'axis': 'y', 'angle': '360 deg'}})
    out(f'{tag} revolve axis y 360: isError {err}; ' + json.dumps(r)[:400])
    read(tag)
c.close()
