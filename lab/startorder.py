"""Q6 + Q7: what the entry SolidCraft writes does in four start orders, driven by a scripted MCP client (no AI).
The entry is written the documented way (`solidcraft-cli mcp setup`, what Help > Connect AI assistants runs) and read
back from ~/.claude.json; the client starts exactly that command. Each case keeps what the server says at start
(`instructions`), every reply, and a screenshot of the whole display (is the cube in the window?).
    bash lab/startorder.sh   (inside sc1-app; it starts the display and runs this)"""
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, '/work')
from checker import entry  # noqa: E402
from client.mcp import McpClient  # noqa: E402

O = '/work/out/l1/startorder'
HOME = os.path.expanduser('~')
CUBE = [{'command': 'sketch.create', 'params': {'plane': 'XY'}},
        {'command': 'sketch.rectangle.two_point', 'params': {'p0': [0, 0], 'p1': [20, 20]}},
        {'command': 'sketch.finish', 'params': {}},
        {'command': 'solid.extrude', 'params': {'distance': 20}}]
app = None
timeline = open(os.path.join(O, 'timeline.jsonl'), 'a')


def ev(what):
    timeline.write(json.dumps({'t': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'event': what}) + '\n')
    timeline.flush()


def shot(name):
    subprocess.run(['import', '-window', 'root', os.path.join(O, name + '.png')], check=False)


def start_app(tag):
    global app
    app = subprocess.Popen(['solidcraft'], stdout=open(os.path.join(O, f'app-{tag}.log'), 'w'), stderr=subprocess.STDOUT)
    time.sleep(10)
    subprocess.run(['python3', '/work/client/ctl.py', 'ui.prefs', '{"theme":"light"}', '27878'], capture_output=True)
    subprocess.run(['xdotool', 'mousemove', '442', '228', 'click', '1'])
    time.sleep(3)
    ev(f'{tag}: app started (no flags), light theme, New design')


def quit_app(tag):
    global app
    subprocess.run(['xdotool', 'search', '--name', 'SolidCraft', 'windowactivate', '--sync', 'key', '--clearmodifiers', 'ctrl+q'],
                   capture_output=True)
    for _ in range(20):
        if app.poll() is not None:
            break
        time.sleep(0.5)
    how = 'Ctrl+Q'
    if app.poll() is None:
        app.terminate()
        app.wait(10)
        how = 'Ctrl+Q did not close it: TERM'
    ev(f'{tag}: app closed ({how})')
    app = None
    time.sleep(2)


def wiggle(n=3):
    for i in range(n):
        subprocess.run(['xdotool', 'mousemove', str(600 + i * 40), str(500 + i * 20)])
        time.sleep(0.7)


def call(c, name, args, rows, tag):
    t0 = time.time()
    r = c.call_tool(name, args)
    rows.append({'case': tag, 'tool': name, 'arguments': args, 'isError': bool(r.get('isError')),
                 'seconds': round(time.time() - t0, 2), 'reply': McpClient.text_json(r)})
    ev(f'{tag}: {name} -> {"ERROR" if r.get("isError") else "ok"}')
    return r


def volume(rows):
    m = [x for x in rows if x['tool'] == 'measure' and not x['isError']]
    if not m or not isinstance(m[-1]['reply'], dict):
        return None
    return (m[-1]['reply'].get('total') or {}).get('volume_mm3')


def main():
    os.makedirs(os.path.join(HOME, '.config', 'Claude'), exist_ok=True)
    os.makedirs(os.path.join(HOME, '.claude'), exist_ok=True)
    open(os.path.join(HOME, '.claude.json'), 'w').write('{}\n')
    setup = subprocess.run(['solidcraft-cli', 'mcp', 'setup'], capture_output=True, text=True)
    open(os.path.join(O, 'setup.txt'), 'w').write(setup.stdout + setup.stderr)
    e = entry.read(os.path.join(HOME, '.claude.json'))
    cmd = [e['command']] + e['args']
    res = {'entry_command': cmd, 'cases': {}}
    rows = []

    # Case 1: SolidCraft open before the Claude app starts the plug.
    start_app('case1')
    c = McpClient(cmd, timeout_s=330, log_path=os.path.join(O, 'case1-transcript.jsonl'))
    init = c.start()
    tools = c.list_tools()
    json.dump({'count': len(tools), 'names': [t['name'] for t in tools], 'tools': tools},
              open('/work/out/l1/tools.json', 'w'), indent=1)
    r1 = []
    call(c, 'inspect_design', {}, r1, 'case1')
    call(c, 'batch', {'commands': CUBE}, r1, 'case1')
    wiggle()
    shot('case1-after-cube')
    call(c, 'measure', {}, r1, 'case1')
    res['cases']['1_app_open_first'] = {'instructions': init.get('instructions'), 'tools': len(tools),
                                        'volume_mm3': volume(r1), 'errors': sum(x['isError'] for x in r1)}
    rows += r1

    # Case 3: the app closed mid-session (same plug process).
    quit_app('case3')
    r3 = []
    call(c, 'inspect_design', {}, r3, 'case3')
    shot('case3-after-close')
    res['cases']['3_app_closed_mid_session'] = {'reply': r3[0]['reply'], 'isError': r3[0]['isError']}
    rows += r3

    # Case 4: the app opened again (same plug process).
    start_app('case4')
    r4 = []
    call(c, 'inspect_design', {}, r4, 'case4')
    call(c, 'batch', {'commands': CUBE}, r4, 'case4')
    wiggle()
    shot('case4-after-cube')
    call(c, 'measure', {}, r4, 'case4')
    res['cases']['4_app_reopened'] = {'first_reply_isError': r4[0]['isError'], 'volume_mm3': volume(r4),
                                      'errors': sum(x['isError'] for x in r4)}
    rows += r4
    c.close()
    quit_app('case4-end')

    # Case 2: the Claude app starts the plug before SolidCraft is open; then SolidCraft opens.
    c = McpClient(cmd, timeout_s=330, log_path=os.path.join(O, 'case2-transcript.jsonl'))
    init2 = c.start()
    r2 = []
    call(c, 'inspect_design', {}, r2, 'case2-no-app')
    start_app('case2')
    call(c, 'batch', {'commands': CUBE}, r2, 'case2-app-opened')
    wiggle()
    shot('case2-after-cube')
    call(c, 'measure', {}, r2, 'case2-app-opened')
    call(c, 'inspect_design', {'sketches': False}, r2, 'case2-app-opened')
    res['cases']['2_plug_started_before_app'] = {'instructions': init2.get('instructions'),
                                                 'first_reply': r2[0]['reply'], 'first_isError': r2[0]['isError'],
                                                 'volume_mm3': volume(r2), 'errors': sum(x['isError'] for x in r2)}
    rows += r2
    c.close()
    quit_app('case2-end')
    res['rows'] = rows
    json.dump(res, open(os.path.join(O, 'startorder.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != 'rows'}, indent=1)[:6000])


if __name__ == '__main__':
    main()
