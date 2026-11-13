"""fx14 G0 step 0 (no AI): the MCP tool list and every command's id/params from list_commands -> G0/tools.txt,
G0/commands.json (so g0.py's tool and parameter names are read, not guessed).
    python3 -I G0/tools.py        (cwd /work/out/fx14)"""
import json
import os
import sys

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

OUT = '/work/out/fx14/G0'
e = entry.read(os.path.expanduser('~/.claude.json'))
c = McpClient([e['command']] + e['args'] + ['--allow-path', os.path.expanduser('~')], timeout_s=120,
              log_path=os.path.join(OUT, 'rpc-tools.jsonl'))
c.start()
tools = c.list_tools()
with open(os.path.join(OUT, 'tools.txt'), 'w') as f:
    for t in tools.get('tools', tools) if isinstance(tools, dict) else tools:
        f.write(f"TOOL {t['name']}: {t.get('description', '')}\n  schema {json.dumps(t.get('inputSchema'))}\n")
r = c.call_tool('list_commands', {})
txt = McpClient.text(r)
open(os.path.join(OUT, 'commands.json'), 'w').write(txt)
try:
    cmds = json.loads(txt.split('\nNote:')[0])
except ValueError:
    cmds = []
    print('list_commands not JSON:', txt[:300])
items = cmds if isinstance(cmds, list) else cmds.get('commands', [])
with open(os.path.join(OUT, 'tools.txt'), 'a') as f:
    for x in items:
        f.write(f"CMD {x.get('id')} [{x.get('tab')}/{x.get('panel')}] {x.get('label')}: {x.get('params')}\n")
print(len(items), 'commands')
c.close()
