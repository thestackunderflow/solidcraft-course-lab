"""fx13 take D no-AI client (LAB-fx13 section 3, Q6; from out/fx12/D/noai.py): it starts SolidCraft's MCP plug from the
entry `solidcraft-cli mcp setup` wrote (plus lesson 7's --allow-path for the home folder), `open`s ~/cup.sc, then
`execute` solid.shell {"faces": [[0, 0, 80]], "thickness": 2, "tangent_chain": true}; then `open`s ~/cup.sc again and
sends the same call WITHOUT tangent_chain (parameter names from list_commands, logged in D/shell-cmd.txt). It prints
each request and the raw reply text word for word. Every JSON-RPC message goes to D/rpc.jsonl.
    python3 -I D/noai.py |& tee D/reply.txt          (cwd /work/out/fx13)"""
import json
import os
import sys
import textwrap
import time

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

OUT = '/work/out/fx13/D'
T0 = open('/tmp/fx13/T0').read().strip() if os.path.exists('/tmp/fx13/T0') else ''
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


def shell(c, tag, params):
    r, t = call(c, 'execute', {'command': 'solid.shell', 'params': params, 'verbose': False})
    for x in t:
        say(x.split('\nNote:')[0] if not r.get('isError') else x, 3)
    ev(f'{tag}: solid.shell {json.dumps(params)}: ' + ('refused' if r.get('isError') else 'built'))
    ev(f'{tag} reply: ' + json.dumps(t[0] if t else '') + ', isError: ' + json.dumps(bool(r.get('isError'))))
    with open(os.path.join(OUT, 'replies.json'), 'a') as f:
        f.write(json.dumps([{'tool': 'execute', 'arguments': {'command': 'solid.shell', 'params': params},
                             'isError': bool(r.get('isError')), 'texts': t, 'raw': r}]) + '\n')
    time.sleep(3)


def main():
    e = entry.read(os.path.expanduser('~/.claude.json'))
    c = McpClient([e['command']] + e['args'] + ['--allow-path', os.path.expanduser('~')], timeout_s=120,
                  log_path=os.path.join(OUT, 'rpc.jsonl'))
    c.start()
    path = os.path.expanduser('~/cup.sc')
    r, t = call(c, 'open', {'path': path})
    say(t[0].replace('\n', ' ')[:140] if t else '', 3)
    shell(c, 'call 1 (tangent_chain true)', {'faces': [[0, 0, 80]], 'thickness': 2, 'tangent_chain': True})
    r, t = call(c, 'open', {'path': path})
    say(t[0].replace('\n', ' ')[:140] if t else '', 3)
    shell(c, 'call 2 (tangent_chain not given)', {'faces': [[0, 0, 80]], 'thickness': 2})
    c.close()


main()
