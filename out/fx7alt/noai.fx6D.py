"""fx6 take D (LAB-fx6 section 3): the same Fillet over SolidCraft's MCP plug, no AI. The lesson-7 Story pattern
(lab/l7story.py): start the plug from the entry `solidcraft-cli mcp setup` wrote, read the lip's outer top edge from the
body (body_topology), send solid.fillet with the edge given by its MIDPOINT at radius 6, then by a CORNER point (an
end of that edge), and print each reply's fields word for word.
    python3 -I D/noai.py |& tee D/reply.txt        (cwd /work/out/fx6)"""
import json
import os
import sys

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
from checker import entry  # noqa: E402
from l7story import Story  # noqa: E402

OUT = '/work/out/fx6/D'
LIP = 'F2:side:l2|F2:side:l3'      # the lip's outer front face | the lip's top face


def main():
    s = Story(OUT)
    e = entry.read(os.path.expanduser('~/.claude.json'))
    c = s.plug([e['command']] + e['args'], 'SolidCraft 0.28.0, the hook open: the same Fillet, sent by a script')
    m = s.call(c, 'measure', {}, '', 'measure')[1] or {}
    body = (m.get('bodies') or [{}])[0].get('name')
    r = c.call_tool('body_topology', {'body': body})
    topo = json.loads([x['text'] for x in r['content'] if x.get('type') == 'text'][0])
    edge = [x for x in topo['edges'] if x['name'] == LIP][0]
    s.say('')
    s.say(f'# the lip\'s outer top edge, read from the body: {LIP}')
    s.say(f'#   midpoint {edge["mid"]}   corner {edge["start"]}   length {edge["length"]}')
    s.mark('edge read', edge=edge)
    mid = [round(v, 4) for v in edge['mid']]
    corner = [round(v, 4) for v in edge['start']]
    s.call(c, 'execute', {'command': 'solid.fillet', 'params': {'edges': [mid], 'radius': 6}},
           f'solid.fillet  edges [{mid}]  radius 6   (the edge by its midpoint)', 'fillet midpoint 6')
    s.call(c, 'execute', {'command': 'solid.fillet', 'params': {'edges': [corner], 'radius': 6}},
           f'solid.fillet  edges [{corner}]  radius 6   (the edge by a corner point)', 'fillet corner 6')
    s.call(c, 'measure', {}, '', 'measure after')
    c.close()
    json.dump(s.rows, open(os.path.join(OUT, 'replies.json'), 'w'), indent=1)


main()
