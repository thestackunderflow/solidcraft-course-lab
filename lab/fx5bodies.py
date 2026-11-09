"""fx5 take B steps 8-9 (no AI, no footage): does the hand-over file name depend on the bodies sent, and does the
stem hold across a SolidCraft restart for a saved design? Over the plug (the MCP entry in ~/.claude.json) with the
GUI open: add a second body (solid.box), send Body1 alone, the new body alone, both together; list the folder each
time. The restart part is done by fx5B.sh (close SolidCraft, start it on the saved file, send Body1 again).
    python3 -I /work/lab/fx5bodies.py OUT_DIR"""
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

O = sys.argv[1]
SLICED = '/root/.cache/solidcraft/slicer'


def ls(tag):
    out = subprocess.run(['ls', '-l', '--time-style=full-iso', SLICED], capture_output=True, text=True).stdout
    open(os.path.join(O, f'ls-{tag}.txt'), 'w').write(out)
    print(tag, sorted(os.listdir(SLICED)))


e = entry.read(os.path.expanduser('~/.claude.json'))
c = McpClient([e['command']] + e['args'], timeout_s=120, log_path=os.path.join(O, 'bodies-transcript.jsonl'))
c.start()
ex = lambda cmd, **p: McpClient.text(c.call_tool('execute', {'command': cmd, 'params': p}))  # noqa: E731
print('describe solid.box:', McpClient.text(c.call_tool('describe_command', {'id': 'solid.box'}))[:600])
r = ex('solid.box', corner=[60, 0, 0], length=10, width=10, height=10, body_name='Tag')
print('solid.box:', r[:300])
insp = McpClient.text_json(c.call_tool('inspect_design', {}))
names = [b.get('name') for b in insp.get('bodies', [])] if isinstance(insp, dict) else []
print('bodies:', names)
other = [n for n in names if n != 'Body1'][:1]
for tag, bodies in (('body1', ['Body1']), ('other', other), ('both', ['Body1'] + other)):
    if not bodies:
        continue
    print('send', tag, ex('file.send_to_slicer', slicer='prusa', bodies=bodies, wait='no')[:400])
    time.sleep(3)
    ls(tag)
c.close()
