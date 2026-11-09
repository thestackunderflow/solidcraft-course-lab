"""fx9 off-camera helper (LAB-fx9), over the plug entry SolidCraft wrote, into the open window, no AI.
    python3 lab/fx9.py tools OUT                 tools/list -> OUT/tools.json
    python3 lab/fx9.py cmds FILTER               list_commands FILTER, printed
    python3 lab/fx9.py raw OUT TOOL 'JSON'       one tools/call, the reply printed (probes and set-ups only)
    python3 lab/fx9.py read OUT TAG              read only: measure + inspect_design -> OUT/read-TAG.json
    python3 lab/fx9.py open PATH                 open a saved design into the window
Prints one line (or the reply). FX9_ALLOW=1 adds `--allow-path ~` (lesson 7's fix) so files in ~ can be opened/saved."""
import json
import os
import sys

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402


def client(log=None):
    e = entry.read(os.path.expanduser('~/.claude.json'))
    extra = ['--allow-path', os.path.expanduser('~')] if os.environ.get('FX9_ALLOW') else []
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
    if mode == 'tools':
        o = sys.argv[2]
        c = client()
        t = c.list_tools()
        json.dump(t, open(os.path.join(o, 'tools.json'), 'w'), indent=1)
        print('tools', [x['name'] for x in t])
    elif mode == 'cmds':
        c = client()
        print(McpClient.text(c.call_tool('list_commands', {'filter': sys.argv[2]})))
    elif mode == 'raw':
        o, tool, args = sys.argv[2], sys.argv[3], json.loads(sys.argv[4])
        c = client(os.path.join(o, 'raw-transcript.jsonl'))
        print(json.dumps(c.call_tool(tool, args)))
    elif mode == 'read':
        o, tag = sys.argv[2], sys.argv[3]
        c = client()
        m, d = jt(c, 'measure', {}), jt(c, 'inspect_design', {})
        json.dump({'measure': m, 'design': d}, open(os.path.join(o, f'read-{tag}.json'), 'w'), indent=1)
        print(tag, 'volume', (m.get('total') or {}).get('volume_mm3'), 'bodies', len(m.get('bodies') or []),
              'timeline', [f.get('name') or f.get('type') for f in (d.get('timeline') or [])] if isinstance(d, dict) else d)
    elif mode == 'bore':     # bore OUT TAG: export the body as ASCII STL, then the inner vertices' distance from the Z axis
        import math
        o, tag = sys.argv[2], sys.argv[3]
        p = os.path.join(os.path.expanduser('~'), f'bore-{tag}.stl')
        c = client()
        r = c.call_tool('export', {'path': p, 'format': 'stla'})
        rs = []
        for line in open(p):
            s = line.split()
            if s and s[0] == 'vertex':
                x, y = float(s[1]), float(s[2])
                rr = math.hypot(x, y)
                if rr < 5.5:              # inside the hexagon's 6.5 flats: the bore's surface only
                    rs.append(rr)
        res = {'export': McpClient.text(r)[:200], 'inner_vertices': len(rs),
               'smallest_diameter_mm': round(2 * min(rs), 4) if rs else None,
               'largest_inner_diameter_mm': round(2 * max(rs), 4) if rs else None,
               'method': 'export stla, vertices with sqrt(x^2+y^2) under 5.5 mm (the hole axis is the Z axis), 2 x min / max'}
        json.dump(res, open(os.path.join(o, f'bore-{tag}.json'), 'w'), indent=1)
        print('bore', tag, json.dumps(res))
    elif mode == 'open':
        c = client()
        print('open', json.dumps(c.call_tool('open', {'path': sys.argv[2]}))[:400])
    c.close()


main()
