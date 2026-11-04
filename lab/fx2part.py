"""fx2 take E start: the washer (outer 5 mm, hole 2.2 mm, 0.3 mm thick) built over the plug before the recording, no AI.
    python3 lab/fx2part.py OUT_DIR   (writes OUT_DIR/part-fx2.json; prints the volume)"""
import json
import os
import sys

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

WASHER = [{'command': 'sketch.create', 'params': {'plane': 'XY'}},
          {'command': 'sketch.line', 'params': {'closed': True, 'points': [['0', '0'], ['5', '0'], ['5', '5'], ['0', '5']]}},
          {'command': 'sketch.finish', 'params': {}},
          {'command': 'solid.extrude', 'params': {'distance': '0.3', 'operation': 'new', 'name': 'Washer'}},
          {'command': 'solid.hole', 'params': {'position': [2.5, 2.5, 0.3], 'diameter': 2.2}}]

o = sys.argv[1]
e = entry.read(os.path.expanduser('~/.claude.json'))
c = McpClient([e['command']] + e['args'] + ['--allow-path', '/root/fx2'], timeout_s=120,
              log_path=os.path.join(o, 'part-fx2-transcript.jsonl'))
c.start()
b = McpClient.text_json(c.call_tool('batch', {'commands': WASHER, 'verbose': True}))
m = McpClient.text_json(c.call_tool('measure', {}))
res = {'batch': b, 'measure': m}
if '--mesh' in sys.argv:
    res['save_mesh'] = McpClient.text(c.call_tool('execute', {'command': 'file.save_mesh', 'params': {'path': '/root/fx2/washer-sc.stl'}}))
c.call_tool('execute', {'command': 'view.home', 'params': {}})
c.close()
json.dump(res, open(os.path.join(o, 'part-fx2.json'), 'w'), indent=1)
print('ok', b.get('ok'), (m.get('total') or {}).get('volume_mm3'), 'bodies', m.get('body_count'))
