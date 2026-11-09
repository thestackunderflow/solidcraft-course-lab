"""fx8 take D (LAB-fx8 section 3): Convert Mesh over SolidCraft's MCP plug, no AI. The lesson-7 Story pattern
(lab/l7story.py): start the plug from the entry `solidcraft-cli mcp setup` wrote, `open` ~/hook.stl, read the body
(measure), then `execute` mesh.convert on it, and print each reply word for word.
    python3 -I D/noai.py |& tee D/reply.txt        (cwd /work/out/fx8)"""
import json
import os
import sys

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from checker import entry  # noqa: E402
from l7story import Story  # noqa: E402

OUT = '/work/out/fx8/D'
HOME = os.path.expanduser('~')


def main():
    s = Story(OUT)
    e = entry.read(os.path.expanduser('~/.claude.json'))
    c = s.plug([e['command']] + e['args'] + ['--allow-path', HOME], 'SolidCraft 0.28.0: open an STL, then Convert Mesh, sent by a script')
    s.call(c, 'open', {'path': HOME + '/hook.stl'}, '~/hook.stl', 'open')
    m = s.call(c, 'measure', {}, '', 'measure')[1] or {}
    body = (m.get('bodies') or [{}])[0]
    s.say('')
    s.say(f'# the body: {body.get("name")}  faces {body.get("face_types")}  volume {round(body.get("volume_mm3") or 0, 2)} mm3')
    s.call(c, 'execute', {'command': 'mesh.convert', 'params': {'body': body.get('name')}},
           f'mesh.convert  body {body.get("name")}', 'convert')
    c.close()
    json.dump(s.rows, open(os.path.join(OUT, 'replies.json'), 'w'), indent=1)


main()
