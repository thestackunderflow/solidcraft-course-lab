"""fx7alt no-AI client (LAB-fx7alt section 0): LAB-fx6 Take D's noai.py (noai.fx6D.py, the lesson-7 Story pattern)
adapted: it starts SolidCraft's MCP plug from the entry `solidcraft-cli mcp setup` wrote (as a Claude app does), sends
tools/call requests into the open window, and prints each request and the raw reply text word for word. Every JSON-RPC
message, as received, goes to TAKE/rpc.jsonl. Events go to TAKE/events.txt (+ events.jsonl when T0 is set).
    python3 -I noai.py box                   fresh box: new design, solid.box 20 x 20 x 20 (#5173), its volume
    python3 -I noai.py fillet X Y Z          volume before, solid.fillet edges [[X, Y, Z]] radius 3, volume after
    python3 -I noai.py chamfer X Y Z         volume before, solid.chamfer edges [[X, Y, Z]] distance 2, volume after
    python3 -I noai.py tools                 tools/list, then the solid.fillet entry (list_commands), then the
                                             {body, index} route (body_topology), one try
cwd /work/out/fx7alt; the take folder from /tmp/fx7/O, the recording's T0 from /tmp/fx7/T0."""
import json
import os
import sys
import textwrap
import time

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

OUT = open('/tmp/fx7/O').read().strip()          # the take folder (lab/fx7altlib.sh `take`)
TAKE = os.path.basename(OUT)
T0 = open('/tmp/fx7/T0').read().strip() if os.path.exists('/tmp/fx7/T0') else ''
COLS = 150


def ev(what):
    with open(os.path.join(OUT, 'events.txt'), 'a') as f:
        f.write(time.strftime('%H:%M:%S', time.gmtime()) + ('%.1f' % (time.time() % 1))[1:] + '  ' + what + '\n')
    if T0:
        with open(os.path.join(OUT, 'events.jsonl'), 'a') as f:
            f.write(json.dumps({'t': round(time.time() - float(T0), 3), 'event': what}) + '\n')


def say(text, indent=0, pause=0.3):
    for line in textwrap.wrap(str(text), COLS - indent) or ['']:
        print(' ' * indent + line, flush=True)
        time.sleep(0.1)
    time.sleep(pause)


def call(c, tool, args):
    say(f'-> {tool} ' + json.dumps(args), pause=0.9)
    r = c.call_tool(tool, args)
    texts = [x.get('text', '') for x in r.get('content', []) if x.get('type') == 'text']
    say('<- ' + ('isError: true' if r.get('isError') else 'ok'), pause=0.2)
    return r, texts


def volume(c, when):
    r = c.call_tool('measure', {})
    v = (json.loads(McpClient.text(r).split('\nNote:')[0]).get('total') or {}).get('volume_mm3')
    v = round(v, 2) if isinstance(v, float) else v
    say(f'# volume {when}: {v} mm3', pause=0.4)
    ev(f'volume {when}: {v}')
    return v


def main():
    mode = sys.argv[1]
    e = entry.read(os.path.expanduser('~/.claude.json'))
    c = McpClient([e['command']] + e['args'], timeout_s=120, log_path=os.path.join(OUT, 'rpc.jsonl'))
    c.start()
    rows = []
    if mode == 'box':
        say('# fresh box: a new design, then solid.box 20 x 20 x 20')
        call(c, 'new_design', {})
        r, t = call(c, 'execute', {'command': 'solid.box', 'params': {'length': 20, 'width': 20, 'height': 20}, 'verbose': False})
        say(t[0][:140] if t else '', 3)
        volume(c, 'before')
    elif mode in ('fillet', 'chamfer'):
        pt = [float(v) if '.' in v else int(v) for v in sys.argv[2:5]]
        cmd = 'solid.' + mode
        params = {'edges': [pt], 'radius': 3} if mode == 'fillet' else {'edges': [pt], 'distance': 2}
        volume(c, 'before')
        r, t = call(c, 'execute', {'command': cmd, 'params': params, 'verbose': False})
        for x in t:
            say(x.split('\nNote:')[0] if not r.get('isError') else x, 3)
        ev(f'{cmd} {json.dumps(pt)}: ' + ('refused' if r.get('isError') else 'built'))
        ev('reply: ' + json.dumps(t[0] if t else '') + ', isError: ' + json.dumps(bool(r.get('isError'))))
        rows.append({'tool': 'execute', 'arguments': {'command': cmd, 'params': params}, 'isError': bool(r.get('isError')), 'texts': t})
        time.sleep(1.0)
        volume(c, 'after')
    elif mode == 'tools':
        say('-> tools/list', pause=0.9)
        tools = c.list_tools()
        say('<- ' + str(len(tools)) + ' tools: ' + ', '.join(x['name'] for x in tools), pause=0.6)
        hit = [x['name'] for x in tools if 'point on edge' in json.dumps(x)]
        ev('tools/list: ' + str(len(tools)) + ' tools; a solid.fillet tool: ' + str('solid.fillet' in [x['name'] for x in tools])
           + '; "point on edge" in tools/list: ' + (', '.join(hit) or 'none'))
        r, t = call(c, 'list_commands', {'filter': 'solid.fillet'})
        cmds = json.loads(t[0])
        f = [x for x in cmds if x['id'] == 'solid.fillet'][0]
        edges_line = f['params'].split('; ')[0]
        say(f'"id": "solid.fillet",  "label": "{f["label"]}"', 3)
        say('"params": "' + edges_line + '; ' + f['params'].split('; ')[1] + '; ..."', 3, pause=0.4)
        ev('fillet edges line: ' + json.dumps(edges_line) + ' (list_commands solid.fillet, params field, first clause)')
        rows.append({'tool': 'list_commands', 'entry': f})
        r, t = call(c, 'body_topology', {'body': 'Body1'})
        if r.get('isError'):
            say(t[0] if t else '', 3)
            ev('index route: body_topology refused: ' + json.dumps(t[0] if t else ''))
        else:
            topo = json.loads(t[0].split('\nNote:')[0])
            for x in topo.get('edges', []):
                say(json.dumps({k: x.get(k) for k in ('index', 'mid', 'length')}), 3, pause=0.05)
            m = [x for x in topo.get('edges', []) if [round(v, 3) for v in x.get('mid', [])] == [10, 20, 20]]
            ev('index route: body_topology lists ' + str(len(topo.get('edges', []))) + ' edges with index + midpoint; '
               + ('the edge with midpoint [10, 20, 20] is {"body": "Body1", "index": ' + str(m[0]['index']) + '}' if m else 'no edge with midpoint [10, 20, 20]'))
            rows.append({'tool': 'body_topology', 'edges': topo.get('edges')})
    c.close()
    if rows:
        with open(os.path.join(OUT, 'replies.json'), 'a') as f:
            f.write(json.dumps(rows) + '\n')


main()
