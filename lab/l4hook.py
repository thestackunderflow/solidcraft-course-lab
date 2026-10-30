"""Lesson 4: lesson 3's hook (lab/l7story.py HOOK: five names, the J, extrude width; 8,500 mm³), built with no AI over
the entry SolidCraft wrote, into the open window, before a recording starts. Writes OUT_DIR/hook-setup.json.
    python3 lab/l4hook.py OUT_DIR [ENTRY_JSON]"""
import json
import os
import sys

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402
from l7story import HOOK  # noqa: E402

o = sys.argv[1]
if len(sys.argv) > 2:
    e = json.load(open(sys.argv[2]))['mcpServers']['solidcraft']
    cmd = [e['command']] + list(e.get('args') or [])
else:
    e = entry.read(os.path.expanduser('~/.claude.json'))
    cmd = [e['command']] + e['args']
c = McpClient(cmd, timeout_s=120, log_path=os.path.join(o, 'hook-setup-transcript.jsonl'))
c.start()
b = McpClient.text_json(c.call_tool('batch', {'commands': HOOK, 'verbose': False}))
m = McpClient.text_json(c.call_tool('measure', {}))
c.call_tool('execute', {'command': 'view.home', 'params': {}})       # display only: the 3D view of the hook
c.close()
json.dump({'batch': b, 'measure': m}, open(os.path.join(o, 'hook-setup.json'), 'w'), indent=1)
print('hook', (m.get('total') or {}).get('volume_mm3'))
