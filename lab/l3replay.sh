#!/bin/bash
# L3-Q7, the proof ($0, no AI): a fresh container, the entry added with `solidcraft-cli mcp setup`, a new design open in
# the window; every tools/call Claude sent in RUN (its transcript.jsonl) replayed in order exactly as logged (failed
# calls too); then the same no-AI read as the runs (inspect_design, measure, parameters.list) and an STL export read
# by our checker.
#   docker run --rm --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc3-l3:0.26.1 bash /work/lab/l3replay.sh B1
set -u
RUN=${1:-B1}
O=/work/out/l3/replay-$RUN
[ -e "$O/replay.json" ] && { echo "refusing: $O/replay.json exists"; exit 1; }
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
import glob, json, os, shutil, subprocess, sys, time
sys.path.insert(0, '/work'); sys.path.insert(0, '/work/lab')
from checker import entry, stl
from client.mcp import McpClient
from client.replay import logged_calls
import l3read
run, o = sys.argv[1], sys.argv[2]
e = entry.read(os.path.expanduser('~/.claude.json'))
calls = logged_calls(f'/work/out/l3/runs/{run}/transcript.jsonl')
c = McpClient([e['command']] + e['args'], timeout_s=330, log_path=os.path.join(o, 'transcript.jsonl'))
c.start()
rows = []
for call in calls:
    r = c.call_tool(call['name'], call['arguments'])
    rows.append({'logged_seq': call['seq'], 'name': call['name'], 'isError': bool(r.get('isError')),
                 'reply': McpClient.text_json(r)})
ins = McpClient.text_json(c.call_tool('inspect_design', {}))
mea = McpClient.text_json(c.call_tool('measure', {}))
pl = McpClient.text_json(c.call_tool('execute', {'command': 'parameters.list', 'params': {}}))
subprocess.run(['xdotool', 'mousemove', '700', '520']); time.sleep(0.8)
subprocess.run(['import', '-window', 'root', os.path.join(o, 'window.png')])
scratch = sorted(glob.glob('/tmp/solidcraft-mcp-*'))
stl_path = os.path.join(scratch[-1], 'hook.stl') if scratch else '/tmp/hook.stl'
ex = c.call_tool('export', {'path': stl_path, 'format': 'stl'})
c.close()
s = l3read.summarise(ins, mea, pl if isinstance(pl, dict) else {})
res = {'replayed_from': f'out/l3/runs/{run}/transcript.jsonl', 'calls': len(calls), 'names': [x['name'] for x in rows],
       'errors': sum(x['isError'] for x in rows), 'summary': s,
       'export': {'isError': bool(ex.get('isError')), 'reply': McpClient.text_json(ex)}}
if os.path.exists(stl_path):
    shutil.copy(stl_path, os.path.join(o, 'hook.stl'))
    res['our_checker'] = stl.check(os.path.join(o, 'hook.stl'))
json.dump(dict(res, rows=rows), open(os.path.join(o, 'replay.json'), 'w'), indent=1)
json.dump(res, open(f'/work/out/l3/replay-{run}.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ('summary', 'export')}, indent=1))
print(json.dumps({k: s[k] for k in ('volume_mm3', 'bbox_mm', 'user_parameter_names')}))
EOF
quit_app
