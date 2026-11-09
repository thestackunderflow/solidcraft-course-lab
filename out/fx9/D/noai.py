"""fx9 take D no-AI client (LAB-fx9 section 3): the fx7alt noai.py pattern (lesson 7): it starts SolidCraft's MCP plug
from the entry `solidcraft-cli mcp setup` wrote (plus lesson 7's --allow-path for the home folder), `open`s ~/nut.sc,
then one `execute` solid.thread {"face": [X, 0, 3.5], "designation": "M8", "modeled": true}, the point on the 8 mm
hole's wall (the hole's centre is [0, 0]; radius 4 along +X; half the nut's 7 mm height). It prints each request and
the raw reply text word for word. Every JSON-RPC message, as received, goes to D/rpc.jsonl; events to D/events.txt.
    python3 -I noai.py |& tee D/reply.txt          (cwd /work/out/fx9)"""
import json
import os
import sys
import textwrap
import time

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

OUT = '/work/out/fx9/D'
T0 = open('/tmp/fx9/T0').read().strip() if os.path.exists('/tmp/fx9/T0') else ''
COLS = 150
FACE = [4, 0, 3.5]


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


def main():
    e = entry.read(os.path.expanduser('~/.claude.json'))
    c = McpClient([e['command']] + e['args'] + ['--allow-path', os.path.expanduser('~')], timeout_s=120,
                  log_path=os.path.join(OUT, 'rpc.jsonl'))
    c.start()
    r, t = call(c, 'open', {'path': os.path.expanduser('~/nut.sc')})
    say(t[0].replace('\n', ' ')[:140] if t else '', 3)
    params = {'face': FACE, 'designation': 'M8', 'modeled': True}
    r, t = call(c, 'execute', {'command': 'solid.thread', 'params': params, 'verbose': False})
    for x in t:
        say(x.split('\nNote:')[0] if not r.get('isError') else x, 3)
    ev('solid.thread M8 modeled at ' + json.dumps(FACE) + ': ' + ('refused' if r.get('isError') else 'built'))
    ev('reply: ' + json.dumps(t[0] if t else '') + ', isError: ' + json.dumps(bool(r.get('isError'))))
    with open(os.path.join(OUT, 'replies.json'), 'a') as f:
        f.write(json.dumps([{'tool': 'execute', 'arguments': {'command': 'solid.thread', 'params': params},
                             'isError': bool(r.get('isError')), 'texts': t}]) + '\n')
    c.close()


main()
