"""Lesson 5's starting part = lesson 4's finished hook, built with no AI over the plug before a recording starts:
lesson 3's hook (l7story.HOOK: five names, the J, extrude width; 8,500 mm³), hole_d 4.5, two through holes 15 and 45
below the top, each placed from the top edge and from the left edge at width / 2 (lesson 4's fix), and the plate's
two long top edges filleted 2 mm (8,306.62 mm³). Writes OUT_DIR/part-setup.json.
    python3 lab/l5part.py OUT_DIR [--allow-path DIR] [--save FILE.solidcraft]"""
import json
import os
import sys

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from l7story import HOOK  # noqa: E402

HOLES_FILLET = [
    {'command': 'set_parameter', 'params': {'name': 'hole_d', 'value': 4.5}},
    {'command': 'solid.hole', 'params': {'position': [5, -10, 45], 'diameter': 'hole_d', 'references': [
        {'edge': [5, -10, 60], 'distance': '15'}, {'edge': [5, -20, 30], 'distance': 'width / 2'}]}},
    {'command': 'solid.hole', 'params': {'position': [5, -10, 15], 'diameter': 'hole_d', 'references': [
        {'edge': [5, -10, 60], 'distance': '45'}, {'edge': [5, -20, 30], 'distance': 'width / 2'}]}},
    {'command': 'solid.fillet', 'params': {'edges': [[0, -10, 60], [5, -10, 60]], 'radius': 2}},
]
L5_START = HOOK + HOLES_FILLET
EXPECTED_VOLUME = 8306.62     # lesson 4, measured 8,306.621 (worked out 8,306.62)
EXPECTED_BOX = (25.0, 20.0, 60.0)


def main():
    from checker import entry
    from client.mcp import McpClient
    a = sys.argv[1:]
    o = a[0]
    extra = []
    if '--allow-path' in a:
        extra = ['--allow-path', a[a.index('--allow-path') + 1]]
    e = entry.read(os.path.expanduser('~/.claude.json'))
    c = McpClient([e['command']] + e['args'] + extra, timeout_s=120,
                  log_path=os.path.join(o, 'part-setup-transcript.jsonl'))
    c.start()
    b = McpClient.text_json(c.call_tool('batch', {'commands': L5_START, 'verbose': False}))
    m = McpClient.text_json(c.call_tool('measure', {}))
    res = {'batch_ok': b.get('ok'), 'measure': m}
    if '--save' in a:
        res['save'] = McpClient.text(c.call_tool('execute', {'command': 'file.save',
                                                              'params': {'path': a[a.index('--save') + 1]}}))
    c.call_tool('execute', {'command': 'view.home', 'params': {}})       # display only
    c.close()
    json.dump(res, open(os.path.join(o, 'part-setup.json'), 'w'), indent=1)
    print('part', (m.get('total') or {}).get('volume_mm3'), 'bodies', m.get('body_count'))


if __name__ == '__main__':
    main()
