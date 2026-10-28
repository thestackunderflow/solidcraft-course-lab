#!/bin/bash
# L2-Q6, the proof ($0, no AI): a fresh container (same image as the run), the entry added with `solidcraft-cli mcp
# setup`, a new design open in the window; every tools/call Claude sent in RUN (from its transcript.jsonl) replayed in
# order exactly as logged (a failed call too); then measure, inspect_design, and an STL export read by our checker.
#   docker run --rm --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc2-l2:0.25.0 bash /work/lab/l2replay.sh claude-1
set -u
RUN=${1:-claude-1}
O=/work/out/l2/replay-$RUN
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
sys.path.insert(0, '/work')
from checker import entry, outline, recipe, stl
from client.mcp import McpClient
from client.replay import logged_calls
run, o = sys.argv[1], sys.argv[2]
e = entry.read(os.path.expanduser('~/.claude.json'))
calls = logged_calls(f'/work/out/l2/runs/{run}/transcript.jsonl')
c = McpClient([e['command']] + e['args'], timeout_s=330, log_path=os.path.join(o, 'transcript.jsonl'))
c.start()
rows = []
for call in calls:
    r = c.call_tool(call['name'], call['arguments'])
    rows.append({'logged_seq': call['seq'], 'name': call['name'], 'isError': bool(r.get('isError')),
                 'reply': McpClient.text_json(r)})
ins = McpClient.text_json(c.call_tool('inspect_design', {}))
mea = McpClient.text_json(c.call_tool('measure', {}))
subprocess.run(['xdotool', 'mousemove', '700', '520']); time.sleep(0.8)
subprocess.run(['import', '-window', 'root', os.path.join(o, 'window.png')])
scratch = sorted(glob.glob('/tmp/solidcraft-mcp-*'))
stl_path = os.path.join(scratch[-1], 'hook.stl') if scratch else '/tmp/hook.stl'
ex = c.call_tool('export', {'path': stl_path, 'format': 'stl'})
c.close()
s = recipe.summary(ins, mea)
exp = outline.expected(outline.J_MOVES, width=20)
res = {'replayed_from': f'out/l2/runs/{run}/transcript.jsonl', 'calls': len(calls), 'names': [x['name'] for x in rows],
       'errors': sum(x['isError'] for x in rows), 'summary': s,
       'volume_matches_expected': abs((s['volume_mm3'] or 0) - exp['volume_mm3']) < 1e-6,
       'export': {'isError': bool(ex.get('isError')), 'reply': McpClient.text_json(ex)}}
if os.path.exists(stl_path):
    shutil.copy(stl_path, os.path.join(o, 'hook.stl'))
    res['our_checker'] = stl.check(os.path.join(o, 'hook.stl'))
json.dump(dict(res, rows=rows), open(os.path.join(o, 'replay.json'), 'w'), indent=1)
json.dump(res, open('/work/out/l2/replay.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != 'summary'}, indent=1))
EOF
quit_app
