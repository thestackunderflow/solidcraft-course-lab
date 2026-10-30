"""Lesson 7: lesson 3's hook (lab/l7story.py HOOK, B2's logged batch), built with no AI over the entry SolidCraft
wrote, in the open window, before a filmed Claude run. Writes RUN_DIR/hook-setup.json (the batch reply and measure).
    python3 lab/l7hook.py RUN_DIR ENTRY_JSON"""
import json
import os
import sys

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from client.mcp import McpClient  # noqa: E402
from l7story import HOOK  # noqa: E402

o, ej = sys.argv[1], sys.argv[2]
e = json.load(open(ej))['mcpServers']['solidcraft']
c = McpClient([e['command']] + list(e.get('args') or []), timeout_s=120, log_path=os.path.join(o, 'hook-setup-transcript.jsonl'))
c.start()
b = McpClient.text_json(c.call_tool('batch', {'commands': HOOK, 'verbose': False}))
m = McpClient.text_json(c.call_tool('measure', {}))
c.close()
json.dump({'batch': b, 'measure': m}, open(os.path.join(o, 'hook-setup.json'), 'w'), indent=1)
print('hook', (m.get('total') or {}).get('volume_mm3'))
