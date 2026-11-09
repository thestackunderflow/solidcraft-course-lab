"""fx8 take A step 1 set-up (off camera, before the recording): a sketch on the YZ plane offset 5 (the back plate's
inner face, x = 5), one 5 mm circle at the plate's middle (y -10, z 30), finished. Over the plug, no AI.
    python3 lab/fx8sketch.py OUT_DIR"""
import json
import os
import sys

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

o = sys.argv[1]
U, V = float(os.environ.get('FX8_U', '-10')), float(os.environ.get('FX8_V', '30'))
e = entry.read(os.path.expanduser('~/.claude.json'))
c = McpClient([e['command']] + e['args'], timeout_s=120, log_path=os.path.join(o, 'sketch-setup-transcript.jsonl'))
c.start()
r = McpClient.text(c.call_tool('batch', {'commands': [
    {'command': 'sketch.create', 'params': {'plane': 'YZ', 'offset': '5'}},
    {'command': 'sketch.circle.center', 'params': {'center': [U, V], 'diameter': 5}},
    {'command': 'sketch.finish', 'params': {}}], 'verbose': False})).split('\nNote:')[0]
c.close()
open(os.path.join(o, 'sketch-setup.json'), 'w').write(r)
d = json.loads(r)
print('sketch', d.get('ok'), (d.get('failed') or {}).get('error'))
