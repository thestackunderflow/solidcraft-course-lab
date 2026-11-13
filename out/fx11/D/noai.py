"""fx11 take D no-AI client (LAB-fx11 section 3; a copy of out/fx9/D/noai.py): it starts SolidCraft's MCP plug from the
entry `solidcraft-cli mcp setup` wrote (plus lesson 7's --allow-path for the home folder), `open`s ~/tower.sc, then
one `execute` solid.split_body {"body": "Tower", "plane": "XY"} (parameter names from list_commands, logged in
D/split-cmd.txt: body = name; plane = XY|XZ|YZ|plane name). It prints each request and the raw reply
text word for word. Every JSON-RPC message, as received, goes to D/rpc.jsonl; events to D/events.txt.
    python3 -I D/noai.py |& tee D/reply.txt          (cwd /work/out/fx11)"""
import json
import os
import sys
import textwrap
import time

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

OUT = '/work/out/fx11/D'
T0 = open('/tmp/fx11/T0').read().strip() if os.path.exists('/tmp/fx11/T0') else ''
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


def main():
    e = entry.read(os.path.expanduser('~/.claude.json'))
    c = McpClient([e['command']] + e['args'] + ['--allow-path', os.path.expanduser('~')], timeout_s=120,
                  log_path=os.path.join(OUT, 'rpc.jsonl'))
    c.start()
    r, t = call(c, 'open', {'path': os.path.expanduser('~/tower.sc')})
    say(t[0].replace('\n', ' ')[:140] if t else '', 3)
    params = {'body': 'Tower', 'plane': 'XY'}
    r, t = call(c, 'execute', {'command': 'solid.split_body', 'params': params, 'verbose': False})
    for x in t:
        say(x.split('\nNote:')[0] if not r.get('isError') else x, 3)
    ev('solid.split_body body Tower plane XY: ' + ('refused' if r.get('isError') else 'built'))
    ev('reply: ' + json.dumps(t[0] if t else '') + ', isError: ' + json.dumps(bool(r.get('isError'))))
    with open(os.path.join(OUT, 'replies.json'), 'a') as f:
        f.write(json.dumps([{'tool': 'execute', 'arguments': {'command': 'solid.split_body', 'params': params},
                             'isError': bool(r.get('isError')), 'texts': t}]) + '\n')
    c.close()


main()
