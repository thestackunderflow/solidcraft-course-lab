#!/bin/bash
# Q10, the proof ($0, no AI): a fresh container, the entry added with `solidcraft-cli mcp setup`, the app open; the
# tool calls Claude sent in RUN (from its transcript.jsonl) replayed in order over that entry; then the design exported
# as an STL into the server's own scratch folder and read by our checker (checker/stl.py). Host side:
#   docker run --rm --memory 3g --shm-size 1g --network none -v "$PWD:/work" sc1-app:0.24.1 bash /work/lab/replay.sh plug-1
set -u
RUN=$1
O=/work/out/l1/replay-$RUN
[ -e "$O" ] && { echo "refusing: $O exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
solidcraft-cli mcp setup > "$O/setup.txt" 2>&1
start_display
start_app "$O/app.log"
sleep 10
python3 /work/client/ctl.py ui.prefs '{"theme":"light"}' 27878 > /dev/null 2>&1
xdotool mousemove 442 228 click 1; sleep 3
python3 - "$RUN" "$O" <<'EOF'
import glob, json, os, re, shutil, subprocess, sys, time
sys.path.insert(0, '/work')
from checker import entry, stl
from client.mcp import McpClient
from client.replay import logged_calls, total_volume
run, o = sys.argv[1], sys.argv[2]
e = entry.read(os.path.expanduser('~/.claude.json'))
cmd = [e['command']] + e['args']
calls = logged_calls(f'/work/out/l1/runs/{run}/transcript.jsonl')
c = McpClient(cmd, timeout_s=330, log_path=os.path.join(o, 'transcript.jsonl'))
init = c.start()
rows = []
for call in calls:
    r = c.call_tool(call['name'], call['arguments'])
    rows.append({'logged_seq': call['seq'], 'name': call['name'], 'arguments': call['arguments'],
                 'isError': bool(r.get('isError')), 'reply': McpClient.text_json(r)})
for i in range(3):
    subprocess.run(['xdotool', 'mousemove', str(650 + i * 40), str(520 + i * 20)]); time.sleep(0.7)
subprocess.run(['import', '-window', 'root', os.path.join(o, 'window.png')])
scratch = sorted(glob.glob('/tmp/solidcraft-mcp-*'))
stl_path = os.path.join(scratch[-1], 'cube.stl') if scratch else '/tmp/cube.stl'
ex = c.call_tool('export', {'path': stl_path, 'format': 'stl'})
c.close()
res = {'replayed_from': f'out/l1/runs/{run}/transcript.jsonl', 'entry_command': cmd, 'calls': len(calls),
       'names': [x['name'] for x in rows], 'errors': sum(x['isError'] for x in rows),
       'solidcraft_measure_volume_mm3': next((total_volume(x['reply']) for x in reversed(rows) if x['name'] == 'measure'), None),
       'export': {'isError': bool(ex.get('isError')), 'reply': McpClient.text_json(ex)}}
if os.path.exists(stl_path):
    shutil.copy(stl_path, os.path.join(o, 'cube.stl'))
    res['our_checker'] = stl.check(os.path.join(o, 'cube.stl'))
res['rows'] = rows
json.dump(res, open(os.path.join(o, 'replay.json'), 'w'), indent=1)
json.dump({k: v for k, v in res.items() if k != 'rows'}, open('/work/out/l1/replay.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'rows'}, indent=1))
EOF
quit_app
