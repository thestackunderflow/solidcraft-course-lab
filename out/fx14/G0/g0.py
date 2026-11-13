"""fx14 gate G0 step 1 (LAB-fx14 section 3; no AI): the four rungs and the control over the plug entry SolidCraft wrote
(lesson-7 client pattern, as out/fx12/P/tray.py). Command and parameter names from G0/tools.txt (list_commands).
Per rung: build, model.faces BEFORE the edit, the edit, model.faces AFTER, save ~/g0X.sc (before the sketch, so the
window check in step 2 starts from the edited model), then sketch.create {plane: {face: P}}. Every reply verbatim.
    python3 -I G0/g0.py |& tee G0/client.txt        (cwd /work/out/fx14)"""
import json
import os
import sys

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

OUT = '/work/out/fx14/G0'
H = os.path.expanduser('~')
e = entry.read(os.path.expanduser('~/.claude.json'))
c = McpClient([e['command']] + e['args'] + ['--allow-path', H], timeout_s=180, log_path=os.path.join(OUT, 'rpc.jsonl'))
c.start()
REC = {}


def call(tool, args, show=True):
    r = c.call_tool(tool, args)
    t = '\n'.join(x.get('text', '') for x in r.get('content', []) if x.get('type') == 'text')
    if show:
        print(f'-> {tool} {json.dumps(args)}\n<- isError {bool(r.get("isError"))}: {t}\n', flush=True)
    return bool(r.get('isError')), t


def ex(cmd, params, show=True):
    return call('execute', {'command': cmd, 'params': params, 'verbose': False}, show)


def rect_extrude(p0, p1, dist, op):
    ex('sketch.create', {'plane': 'XY'})
    ex('sketch.rectangle.two_point', {'p0': p0, 'p1': p1})
    ex('sketch.finish', {})
    return ex('solid.extrude', {'distance': dist, 'operation': op})


def faces(tag, body):
    err, t = ex('model.faces', {'body': body}, show=False)
    print(f'== model.faces {body} {tag}: isError {err}\n{t}\n', flush=True)
    return t


def vol():
    err, t = call('measure', {}, show=False)
    try:
        m = json.loads(t.split('\nNote:')[0])
        return ((m.get('total') or {}).get('volume_mm3'),
                [(b.get('name'), b.get('volume_mm3')) for b in m.get('bodies') or []])
    except ValueError:
        return t[:200], []


def bodies():
    return [n for n, _ in vol()[1]]


def attempt(rung, point, body):
    path = f'{H}/{rung}.sc'
    call('save', {'path': path})
    print(f'== {rung}: volume {vol()}', flush=True)
    err, t = ex('sketch.create', {'plane': {'face': point}})
    REC[rung] = {'point': point, 'body': body, 'isError': err, 'reply': t}
    print(f'#### {rung} sketch.create face {point}: isError {err}\n#### reply: {t}\n', flush=True)
    if not err:
        ex('sketch.finish', {})


def guard(name, fn):
    try:
        fn()
    except Exception as x:  # a rung that cannot be driven is logged, the ladder goes on
        REC[name + '_blocker'] = repr(x)
        print(f'#### {name} BLOCKER: {x!r}', flush=True)


def control_and_g0a():
    call('new_design', {})
    rect_extrude([0, 0], [40, 30], 20, 'new')
    b = bodies()[0]
    REC['control_faces'] = faces('plain block (control)', b)
    err, t = ex('sketch.create', {'plane': {'face': [20, 15, 20]}})
    REC['control'] = {'point': [20, 15, 20], 'isError': err, 'reply': t}
    print(f'#### control sketch.create face [20,15,20]: isError {err}\n#### reply: {t}\n', flush=True)
    call('undo', {})
    print(f'after undo: {vol()}')
    REC['g0a_before'] = faces('G0a before Align', b)
    err, t = ex('solid.align', {'bodies': [b], 'from': [0, 0, 0], 'to': [0, 0, 5]})
    REC['g0a_edit'] = {'how': 'solid.align {bodies:[%s], from:[0,0,0], to:[0,0,5]} (two points)' % b,
                       'isError': err, 'reply': t}
    REC['g0a_after'] = faces('G0a after Align', b)
    attempt('g0a', [20, 15, 25], b)


def g0b():
    call('new_design', {})
    rect_extrude([0, 0], [20, 30], 20, 'new')
    rect_extrude([20, 0], [40, 30], 20, 'new')
    bs = bodies()
    print('bodies', bs)
    REC['g0b_before'] = faces('G0b before Combine (target)', bs[0]) + '\n' + faces('G0b before Combine (tool)', bs[1])
    err, t = ex('solid.combine', {'target': bs[0], 'tools': [bs[1]], 'operation': 'join'})
    REC['g0b_edit'] = {'how': 'solid.combine join', 'isError': err, 'reply': t}
    b = bodies()[0]
    REC['g0b_after'] = faces('G0b after Combine', b)
    attempt('g0b', [20, 15, 20], b)


def g0c():
    call('new_design', {})
    rect_extrude([0, 0], [40, 30], 20, 'new')
    b = bodies()[0]
    REC['g0c_before'] = faces('G0c before Shell', b)
    err, t = ex('solid.shell', {'faces': [[20, 15, 20]], 'thickness': 2})
    REC['g0c_edit'] = {'how': 'solid.shell {faces:[[20,15,20]], thickness:2}; tangent_chain not given (MCP default '
                       'false; sharp edges, so the chain is the top only either way)', 'isError': err, 'reply': t}
    REC['g0c_after'] = faces('G0c after Shell', b)
    attempt('g0c', [1, 15, 20], b)


def g0d():
    call('new_design', {})
    rect_extrude([0, 0], [40, 30], 20, 'new')
    b = bodies()[0]
    REC['g0d_before'] = faces('G0d block before Save As Mesh', b)
    err, t = ex('file.save_mesh', {'path': f'{H}/g0d.stl'})
    REC['g0d_save_mesh'] = t
    call('new_design', {})
    err, t = ex('file.insert_mesh', {'path': f'{H}/g0d.stl'})
    REC['g0d_insert'] = {'how': 'file.insert_mesh (Insert Mesh)', 'isError': err, 'reply': t}
    mb = bodies()
    print('bodies after insert', mb)
    err, t = ex('mesh.convert', {'body': mb[0]} if mb else {})
    REC['g0d_edit'] = {'how': 'mesh.convert', 'isError': err, 'reply': t}
    bs = bodies()
    print('bodies after convert', bs, vol())
    b = bs[-1] if bs else None
    REC['g0d_after'] = faces('G0d after Convert Mesh', b) if b else 'no body'
    attempt('g0d', [20, 15, 20], b)


for name, fn in (('g0a', control_and_g0a), ('g0b', g0b), ('g0c', g0c), ('g0d', g0d)):
    print(f'######## {name}', flush=True)
    guard(name, fn)

json.dump(REC, open(os.path.join(OUT, 'client.json'), 'w'), indent=1)
print('######## SUMMARY')
for r in ('control', 'g0a', 'g0b', 'g0c', 'g0d'):
    x = REC.get(r, {})
    print(f'{r}: isError {x.get("isError")}: {x.get("reply", "")[:600]}')
c.close()
