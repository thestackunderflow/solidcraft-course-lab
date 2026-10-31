"""Lesson 6's starting part = lesson 5's finished hook, built with no AI over the plug before a recording starts:
lesson 4's hook (lab/l5part.L5_START: 8,306.62 mm³, 25 x 20 x 60, holes Ø 4.5 centred 15 and 45 below the top, two
round top edges R 2) and the print face on the J-shaped side (lesson 5: it goes to the slicer lying on its side).
Writes OUT_DIR/part-setup.json.
    python3 lab/l6part.py OUT_DIR [--entry ENTRY_JSON] [--allow-path DIR] [--save FILE.sc]"""
import json
import os
import sys

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from l5part import L5_START  # noqa: E402

J_FACE = [12, 0, 2.5]         # on the hook's side at y = 0: the J outline (lesson 5)
L6_START = L5_START + [{'command': 'body.print_face', 'params': {'body': 'Body1', 'point': J_FACE}}]
EXPECTED_VOLUME = 8306.62


def plug_cmd(entry_json=None, extra=()):
    from checker import entry
    if entry_json:
        e = json.load(open(entry_json))['mcpServers']['solidcraft']
        return [e['command']] + list(e.get('args') or []) + list(extra)
    e = entry.read(os.path.expanduser('~/.claude.json'))
    return [e['command']] + e['args'] + list(extra)


def main():
    from client.mcp import McpClient
    a = sys.argv[1:]
    o = a[0]
    opt = lambda k: a[a.index(k) + 1] if k in a else None  # noqa: E731
    extra = ['--allow-path', opt('--allow-path')] if opt('--allow-path') else []
    c = McpClient(plug_cmd(opt('--entry'), extra), timeout_s=120, log_path=os.path.join(o, 'part-setup-transcript.jsonl'))
    c.start()
    b = McpClient.text_json(c.call_tool('batch', {'commands': L6_START, 'verbose': False}))
    m = McpClient.text_json(c.call_tool('measure', {}))
    res = {'batch_ok': b.get('ok'), 'measure': m}
    if opt('--save'):
        res['save'] = McpClient.text(c.call_tool('execute', {'command': 'file.save', 'params': {'path': opt('--save')}}))
    c.call_tool('execute', {'command': 'view.home', 'params': {}})       # display only
    c.close()
    json.dump(res, open(os.path.join(o, 'part-setup.json'), 'w'), indent=1)
    print('part', (m.get('total') or {}).get('volume_mm3'), 'bodies', m.get('body_count'), 'ok', b.get('ok'))


if __name__ == '__main__':
    main()
