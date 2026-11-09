#!/bin/bash
# scfc stage 2 step 0 (8 Nov 2026, $0, no AI): on SolidCraft 0.30.1 (stable, 2 Nov 2026), does the lesson 2 hook still
# come out upside down? A fresh container, the entry added with `solidcraft-cli mcp setup`, a new design open in the
# window, then every tools/call Claude sent in lesson 2 RUN (its transcript.jsonl, logged on 0.25.0) replayed in order
# exactly as logged; then inspect_design + measure (bounding box, sketch up-axis). Also: the "?" menu (Connect AI
# assistants) screenshotted. The whole display is filmed (screen.mp4, 30 fps) with events, for a re-check insert.
#   docker run --rm --name scfc-recheck --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc-wf-l4:0.30.1 \
#     bash /work/lab/scfc_recheck.sh claude-1
# Writes out/scfc/recheck-RUN/: replay.json, events.jsonl, cursor.jsonl, screen.mp4, *.png, setup.txt, app.log.
set -u
RUN=${1:-claude-1}
O=/work/out/scfc/recheck-$RUN
[ -e "$O/replay.json" ] && { echo "refusing: $O/replay.json exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
. /work/lab/l2common.sh
E=$O/events.jsonl; : > "$E"
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
solidcraft-cli mcp setup > "$O/setup.txt" 2>&1
solidcraft --version > "$O/version.txt" 2>&1
start_display
record30 "$O/screen.mp4" "$O/cursor.jsonl"; export T0
mark "$E" "recording started"
start_app "$O/app.log"
sleep 10
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > "$O/prefs-reply.json" 2>&1
fill_window 0 0 $W $H; sleep 1
shot "$O/0-start.png"
mark "$E" "start page"
c43() { awk -v v="$1" 'BEGIN{printf "%d", v*4/3}'; }
g() { glide "$(c43 "$1")" "$(c43 "$2")" "${3:-14}"; }
g 398 230 4; sleep 0.5; xdotool click 1; sleep 3                # start page: New design (0.27.1 layout)
shot "$O/1-new-design.png"
mark "$E" "new design"
python3 - "$RUN" "$O" <<'EOF'
import json, os, sys, time
sys.path.insert(0, '/work')
from checker import entry, outline, recipe
from client.mcp import McpClient
from client.replay import logged_calls
run, o = sys.argv[1], sys.argv[2]
def mark(what):
    t0 = float(os.environ.get('T0', '0') or 0)
    open(os.path.join(o, 'events.jsonl'), 'a').write(json.dumps({'t': round(time.time() - t0, 3) if t0 else None, 'event': what}) + '\n')
e = entry.read(os.path.expanduser('~/.claude.json'))
json.dump({'command': os.path.basename(e['command']), 'args': e['args']}, open(os.path.join(o, 'entry.json'), 'w'))
calls = logged_calls(f'/work/out/l2/runs/{run}/transcript.jsonl')
c = McpClient([e['command']] + e['args'], timeout_s=330, log_path=os.path.join(o, 'transcript.jsonl'))
init = c.start()
tools = c.request('tools/list', {}) if hasattr(c, 'request') else None
rows = []
mark('replay: first logged call')
for call in calls:
    r = c.call_tool(call['name'], call['arguments'])
    rows.append({'logged_seq': call['seq'], 'name': call['name'], 'isError': bool(r.get('isError')),
                 'reply': McpClient.text_json(r)})
    time.sleep(1.0)
mark('replay: done, view home')
c.call_tool('execute', {'command': 'view.home', 'params': {}})
time.sleep(2)
ins = McpClient.text_json(c.call_tool('inspect_design', {}))
mea = McpClient.text_json(c.call_tool('measure', {}))
c.close()
s = recipe.summary(ins, mea)
exp = outline.expected(outline.J_MOVES, width=20)
res = {'solidcraft': open(os.path.join(o, 'version.txt')).read().strip(),
       'replayed_from': f'out/l2/runs/{run}/transcript.jsonl (logged on 0.25.0)', 'calls': len(calls),
       'names': [x['name'] for x in rows], 'errors': sum(x['isError'] for x in rows), 'summary': s,
       'volume_matches_expected': abs((s.get('volume_mm3') or 0) - exp['volume_mm3']) < 1e-6,
       'upside_down': (s.get('bbox_max') or [0, 0, 1])[2] <= 0 and (s.get('bbox_min') or [0, 0, 0])[2] < 0}
json.dump(dict(res, rows=rows, inspect=ins, measure=mea), open(os.path.join(o, 'replay.json'), 'w'), indent=1)
print(json.dumps({k: res[k] for k in ('solidcraft', 'calls', 'errors', 'volume_matches_expected', 'upside_down')}))
print(json.dumps({k: s.get(k) for k in ('volume_mm3', 'bbox_min', 'bbox_max', 'sketch_up', 'plane_normal')}))
EOF
sleep 3
g 700 520 10; sleep 1.5
shot "$O/2-after-replay.png"
mark "$E" "after replay (view home)"
sleep 4
# the "?" button, top right (0.24.1 layout at 1600 wide = 1269,17; here in 1440 units it is found by the screenshot)
g 1428 13 12; sleep 0.8; xdotool click 1; sleep 1.5
shot "$O/3-help-menu.png"
mark "$E" "? menu opened"
sleep 2; xdotool key Escape; sleep 1
mark "$E" "recording stopped"
stop_record30
quit_app
