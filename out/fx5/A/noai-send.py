"""fx5 take A step 13 (no AI): call SolidCraft 0.28.0's Send to Slicer through its MCP server (the entry
`solidcraft-cli mcp setup` wrote into ~/.claude.json, as lab/l5saveface.py does), with SolidCraft and PrusaSlicer open,
and print the tool's reply; also print the file.send_to_slicer help the server gives an agent (tools/list and
the server's own help command, if it has one), for the palette-help comparison. Run with python3 -I.
    python3 -I /work/out/fx5/A/noai-send.py"""
import json
import os
import sys

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

O = '/work/out/fx5/A'
e = entry.read(os.path.expanduser('~/.claude.json'))
c = McpClient([e['command']] + e['args'], timeout_s=120, log_path=os.path.join(O, 'noai-transcript.jsonl'))
c.start()
tools = c.list_tools()
names = [t.get('name') for t in (tools.get('tools') if isinstance(tools, dict) else tools) or []]
print('tools:', names)
for t in (tools.get('tools') if isinstance(tools, dict) else tools) or []:
    if t.get('name') == 'execute':
        print('execute description (first 400 chars):', (t.get('description') or '')[:400])
for cmd, params in (('help', {'command': 'file.send_to_slicer'}), ('describe', {'command': 'file.send_to_slicer'})):
    if cmd in names:
        print(f'{cmd} file.send_to_slicer:', McpClient.text(c.call_tool(cmd, params)))
r = c.call_tool('execute', {'command': 'file.send_to_slicer', 'params': {'slicer': 'prusa', 'bodies': ['Body1'], 'wait': 'no'}})
print('send reply:', McpClient.text(r))
c.close()
