"""fx12 Q14 (LAB-fx12 section 3 C5, logged, not filmed): round first then offset, then the outline's width 60 -> 70
before any extrude. By the plug (no AI): open ~/tray-plain.sc, sketch.edit, sketch.fillet points p1-p4 radius 5,
sketch.offset curves [l1] distance 2 side [0, 0] (as take P), sketch.inspect; then set_parameter d1 (the 60 mm
width dimension k5) = 70 mm; sketch.inspect. Does the copy follow (ids kept), inside arcs still R 3?
    python3 -I C14/q14.py |& tee C14/q14.txt     (cwd /work/out/fx12, in the take container, the window open)"""
import json
import os
import sys

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

OUT = '/work/out/fx12/C14'
e = entry.read(os.path.expanduser('~/.claude.json'))
c = McpClient([e['command']] + e['args'] + ['--allow-path', os.path.expanduser('~')], timeout_s=120,
              log_path=os.path.join(OUT, 'rpc.jsonl'))
c.start()


def ex(cmd, params):
    r = c.call_tool('execute', {'command': cmd, 'params': params, 'verbose': False})
    t = r['content'][0]['text'].split('\nNote:')[0]
    print(f'-> {cmd} {json.dumps(params)}\n<- isError {bool(r.get("isError"))}: {t[:600]}', flush=True)
    return r, t


def summary(tag):
    r, t = ex('sketch.inspect', {})
    if r.get('isError'):
        return None
    d = json.loads(t)
    json.dump(d, open(os.path.join(OUT, f'sketch-{tag}.json'), 'w'), indent=1)
    cs = [(x['id'], x['type'], x.get('radius')) for x in d['curves']]
    offs = [k['id'] for k in d['constraints'] if 'offset' in k['type']]
    print(f'SUMMARY {tag}: curves {cs} | offset constraints {offs} | regions',
          sorted(round(p['area_mm2'], 2) for p in d['profiles']), flush=True)
    return d


print('open', c.call_tool('open', {'path': os.path.expanduser('~/tray-plain.sc')})['content'][0]['text'][:200])
ex('sketch.edit', {'sketch': 'Sketch1'})
ex('sketch.fillet', {'points': ['p1', 'p2', 'p3', 'p4'], 'radius': 5})
ex('sketch.offset', {'curves': ['l1'], 'distance': 2, 'side': [0, 0]})
summary('before')
# attempt 1 (q14-attempt1.txt): sketch.dimension [l2, l4] 70 mm was refused as over-constraining (the 60 is already
# the driving dimension k5 = d1). Attempt 2: change d1 itself, as a person edits the 60.00 mm dimension.
r = c.call_tool('set_parameter', {'name': 'd1', 'value': '70 mm'})
print('-> set_parameter d1 = 70 mm\n<- isError', bool(r.get('isError')), r['content'][0]['text'][:600], flush=True)
summary('after')
c.close()
