"""fx7alt off-camera helper (LAB-fx7alt), over the plug entry SolidCraft wrote, into the open window, no AI.
    python3 lab/fx7alt.py new                     a new empty design
    python3 lab/fx7alt.py box                     a new design + solid.box 20 x 20 x 20 (#5173)
    python3 lab/fx7alt.py read OUT TAG            read only: measure + inspect_design + body_topology -> OUT/read-TAG.json
    python3 lab/fx7alt.py tools OUT               tools/list -> OUT/tools.json
    python3 lab/fx7alt.py raw OUT TOOL 'JSON'     one tools/call, the reply printed (probes and set-ups only)
Prints one line (or the reply)."""
import json
import os
import sys

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

BOX = {'command': 'solid.box', 'params': {'length': 20, 'width': 20, 'height': 20}}


def client(log=None):
    e = entry.read(os.path.expanduser('~/.claude.json'))
    extra = ['--allow-path', os.path.expanduser('~')] if os.environ.get('FX7_ALLOW') else []   # R1 set-up: save to ~
    c = McpClient([e['command']] + e['args'] + extra, timeout_s=120, log_path=log)
    c.start()
    return c


def jt(c, name, args):
    s = McpClient.text(c.call_tool(name, args)).split('\nNote:')[0]
    try:
        return json.loads(s)
    except ValueError:
        return {'text': s}


def main():
    mode = sys.argv[1]
    if mode == 'new':
        c = client()
        print('new', json.dumps(jt(c, 'new_design', {}))[:200])
    elif mode == 'box':
        c = client()
        jt(c, 'new_design', {})
        r = jt(c, 'execute', {'command': BOX['command'], 'params': BOX['params']})
        print('box', json.dumps(r)[:200], 'volume', (jt(c, 'measure', {}).get('total') or {}).get('volume_mm3'))
    elif mode == 'read':
        o, tag = sys.argv[2], sys.argv[3]
        c = client()
        m, d = jt(c, 'measure', {}), jt(c, 'inspect_design', {})
        body = ((m.get('bodies') or [{}])[0]).get('name')
        t = jt(c, 'body_topology', {'body': body}) if body else {}
        json.dump({'measure': m, 'design': d, 'topology': t}, open(os.path.join(o, f'read-{tag}.json'), 'w'), indent=1)
        print(tag, 'volume', (m.get('total') or {}).get('volume_mm3'), 'bodies', len(m.get('bodies') or []),
              'timeline', [f.get('name') or f.get('type') for f in (d.get('timeline') or [])] if isinstance(d, dict) else d)
    elif mode == 'tools':
        o = sys.argv[2]
        c = client()
        t = c.list_tools()
        json.dump(t, open(os.path.join(o, 'tools.json'), 'w'), indent=1)
        print('tools', [x['name'] for x in t])
    elif mode == 'raw':
        o, tool, args = sys.argv[2], sys.argv[3], json.loads(sys.argv[4])
        c = client(os.path.join(o, 'raw-transcript.jsonl'))
        print(json.dumps(c.call_tool(tool, args)))
    c.close()


main()
