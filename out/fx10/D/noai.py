"""fx10 take D no-AI client (LAB-fx10 section 3; a copy of out/fx9/D/noai.py): it starts SolidCraft's MCP plug from the
entry `solidcraft-cli mcp setup` wrote (plus lesson 7's --allow-path for the home folder), `open`s ~/knob-full.sc, then
one `execute` solid.revolve {"axis": "Z", "angle": "360 deg"} on its only sketch (parameter names from list_commands,
logged in D/revolve-cmd.txt: axis = X|Y|Z world axis; angle default 360 deg). It prints each request and the raw reply
text word for word. Every JSON-RPC message, as received, goes to D/rpc.jsonl; events to D/events.txt.
    python3 -I D/noai.py |& tee D/reply.txt          (cwd /work/out/fx10)"""
import json
import os
import sys
import textwrap
import time

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

OUT = '/work/out/fx10/D'
T0 = open('/tmp/fx10/T0').read().strip() if os.path.exists('/tmp/fx10/T0') else ''
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
    r, t = call(c, 'open', {'path': os.path.expanduser('~/knob-full.sc')})
    say(t[0].replace('\n', ' ')[:140] if t else '', 3)
    params = {'axis': 'Z', 'angle': '360 deg'}
    r, t = call(c, 'execute', {'command': 'solid.revolve', 'params': params, 'verbose': False})
    for x in t:
        say(x.split('\nNote:')[0] if not r.get('isError') else x, 3)
    ev('solid.revolve axis Z 360 deg: ' + ('refused' if r.get('isError') else 'built'))
    ev('reply: ' + json.dumps(t[0] if t else '') + ', isError: ' + json.dumps(bool(r.get('isError'))))
    with open(os.path.join(OUT, 'replies.json'), 'a') as f:
        f.write(json.dumps([{'tool': 'execute', 'arguments': {'command': 'solid.revolve', 'params': params},
                             'isError': bool(r.get('isError')), 'texts': t}]) + '\n')
    c.close()


main()
