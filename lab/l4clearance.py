"""L4-Q5: SolidCraft 0.27.1's clearance-hole setting for an M4 screw (solid.hole clearance "M4", fit close / normal /
loose; its docs say ISO 273), measured on lesson 3's hook through a headless plug (no AI, no window): the bore's radius
from body_topology. Writes out/l4/clearance.json.
    docker run --rm --network none -v "$PWD:/work" -w /work sc4-app:0.27.1 python3 lab/l4clearance.py"""
import json
import sys

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from client.mcp import McpClient  # noqa: E402
from l7story import HOOK  # noqa: E402
import l4read  # noqa: E402

c = McpClient(['solidcraft-cli', 'mcp'], timeout_s=120, log_path='/work/out/l4/clearance-transcript.jsonl')
c.start()
res = {'solidcraft': 'solidcraft-cli mcp (headless)', 'fits': {}}
for fit in ('close', 'normal', 'loose'):
    c.call_tool('new_design', {})
    c.call_tool('batch', {'commands': HOOK, 'verbose': False})
    r = McpClient.text_json(c.call_tool('execute', {'command': 'solid.hole', 'params': {
        'position': [5, -10, 45], 'clearance': 'M4', 'fit': fit}}))
    s = l4read.read(c)['summary']
    res['fits'][fit] = {'reply': r, 'diameters': sorted({h['diameter'] for h in s['holes']})}
c.close()
json.dump(res, open('/work/out/l4/clearance.json', 'w'), indent=1)
print(json.dumps({k: v['diameters'] for k, v in res['fits'].items()}))
