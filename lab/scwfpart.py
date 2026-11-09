"""scwf (8-9 Nov 2026): no-AI plug calls into the open SolidCraft 0.30.1 window, over the entry `solidcraft-cli mcp
setup` wrote (lab/fx8part.py pattern). Every request + reply goes to OUT_DIR/part-TAG-transcript.jsonl.
    python3 lab/scwfpart.py tools OUT_DIR                  tools/list names + the registered entry -> tools.json
    python3 lab/scwfpart.py call OUT_DIR TAG TOOL 'JSON'   one tools/call, reply printed (exploring, G0 diffs)
    python3 lab/scwfpart.py build OUT_DIR TAG [STAGE]      the pre-registered bracket (PREREG.txt), stages
                                                           shape | holes | fillet (cumulative), new design first
    python3 lab/scwfpart.py read OUT_DIR TAG               measure + inspect_design -> read-TAG.json
Prints short lines only."""
import json
import os
import sys

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

HOME = os.path.expanduser('~')

# The bracket (PREREG.txt): L profile on XZ, top leg 50 x 4, drop leg 4 thick, 30 overall, extruded `width` = 25.
SHAPE = [{'command': 'set_parameter', 'params': {'name': 'width', 'value': 25}},
         {'command': 'sketch.create', 'params': {'plane': 'XZ', 'flip': True}},
         {'command': 'sketch.line', 'params': {'closed': True, 'points': [
             [0, 0], [4, 0], [4, 26], [50, 26], [50, 30], [0, 30]]}},
         {'command': 'sketch.finish', 'params': {}},
         {'command': 'solid.extrude', 'params': {'distance': 'width', 'operation': 'new', 'name': 'Bracket'}}]


def client(o, tag):
    e = entry.read(os.path.expanduser('~/.claude.json'))
    c = McpClient([e['command']] + e['args'] + ['--allow-path', HOME], timeout_s=120,
                  log_path=os.path.join(o, f'part-{tag}-transcript.jsonl'))
    c.start()
    return c


def jt(c, name, args):
    s = McpClient.text(c.call_tool(name, args)).split('\nNote:')[0]
    try:
        return json.loads(s)
    except ValueError:
        return {'text': s}


def main():
    mode, o = sys.argv[1], sys.argv[2]
    os.makedirs(o, exist_ok=True)
    if mode == 'tools':
        c = client(o, 'tools')
        names = [t['name'] for t in c.list_tools()]
        c.close()
        json.dump({'tools': names, 'entry': entry.read(os.path.expanduser('~/.claude.json')),
                   'registered_as': list(json.load(open(HOME + '/.claude.json')).get('mcpServers', {}))},
                  open(os.path.join(o, 'tools.json'), 'w'), indent=1)
        print(len(names), 'tools:', ' '.join(names))
        return
    tag = sys.argv[3]
    c = client(o, tag)
    if mode == 'call':
        r = jt(c, sys.argv[4], json.loads(sys.argv[5]) if len(sys.argv) > 5 else {})
        json.dump(r, open(os.path.join(o, f'call-{tag}.json'), 'w'), indent=1)
        print(json.dumps(r)[:int(os.environ.get('CHARS', '900'))])
    elif mode == 'build':
        jt(c, 'new_design', {})
        r = jt(c, 'batch', {'commands': SHAPE, 'verbose': True})
        json.dump(r, open(os.path.join(o, f'build-{tag}.json'), 'w'), indent=1)
        print('shape ok', r.get('ok'), json.dumps(r)[:400])
    if mode in ('build', 'read'):
        m, d = jt(c, 'measure', {}), jt(c, 'inspect_design', {})
        json.dump({'measure': m, 'design': d}, open(os.path.join(o, f'read-{tag}.json'), 'w'), indent=1)
        t = m.get('total') or {}
        print(tag, 'volume', t.get('volume_mm3'), 'bbox', json.dumps(t.get('bbox') or t.get('bounding_box'))[:200])
    c.close()


if __name__ == "__main__":
    main()
