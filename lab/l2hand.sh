#!/bin/bash
# L2-Q2 + Q3: the J drawn by hand through SolidCraft 0.25.0's real window, filmed. Only xdotool clicks, mouse moves
# and typed numbers reach the app (no control channel, no MCP) until the recording stops; then a scripted MCP client
# (no AI) reads the result over the entry `solidcraft-cli mcp setup` wrote: inspect_design and measure.
#   docker run --rm --memory 3g --shm-size 1g --network none -v "$PWD:/work" sc2-l2:0.25.0 bash /work/lab/l2hand.sh hand
# Writes out/l2/RUN/: screen.mp4 (30 fps, the full 2880x1800 display), cursor.jsonl, events.jsonl, shots, read.json.
set -u
RUN=${1:-hand}
O=/work/out/l2/$RUN
[ -e "$O/read.json" ] && { echo "refusing: $O/read.json exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
. /work/lab/l2common.sh
E=$O/events.jsonl; : > "$E"; : > "$O/cursor.jsonl"
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
solidcraft-cli mcp setup > "$O/setup.txt" 2>&1
start_display
start_app "$O/app.log"
sleep 10
# settings only (theme, UI scale), not modelling: the control channel, before the recording starts
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
fill_window 0 0 $W $H; sleep 1
glide 1300 760 4; sleep 0.5
record30 "$O/screen.mp4" "$O/cursor.jsonl"
mark "$E" "recording started: the start page"
nap 2.0
mark "$E" "start page: New design (millimetres)"
glide 530 274 24; nap 1.4; xdotool click 1; nap 2.5
glide 1300 760 20; nap 1.5
# --- F4: the whole window held still (the five areas are outlined in the edit), then F5-F7 in one take
mark "$E" "window: held for the five areas"
nap 7.0
mark "$E" "new sketch: Model tab"
glide 163 67 20; nap 1.2; xdotool click 1; nap 0.8
mark "$E" "new sketch: hover New Sketch"
glide 171 115 16; nap 1.6; xdotool click 1; nap 1.8
mark "$E" "new sketch: the plane panel"
glide 1700 450 24; nap 2.2
mark "$E" "browser: open Origin"
glide 40 353 30; nap 1.0; xdotool click 1; nap 1.0
glide 122 384 10; nap 0.5; glide 122 478 14; nap 0.5; glide 122 509 6; nap 0.5; glide 122 540 6; nap 0.5; glide 122 572 6; nap 1.4
mark "$E" "axis view: the directions"
glide 1850 262 34; nap 2.8
mark "$E" "new sketch: XZ in the Browser"
glide 122 540 34; nap 1.4; xdotool click 1; nap 2.5
mark "$E" "sketch: view faces XZ"
glide 960 620; nap 1.0
mark "$E" "sketch: middle-drag pan"
xdotool mousedown 2; for i in $(seq 1 20); do rel 0 19; sleep 0.035; done; xdotool mouseup 2; nap 1.0
mark "$E" "sketch: Line tool"
glide 155 115; nap 1.0; xdotool click 1; nap 1.2
mark "$E" "sketch: click the origin"
glide 960 1000; nap 1.0; xdotool click 1; nap 1.0
focus_app
seg() {   # seg X Y LENGTH NAME: point the way the line goes (to its end), type the length, Enter
  glide "$1" "$2" 22; nap "${5:-0.8}"
  mark "$E" "line: $4 type $3"
  xdotool type --delay "${6:-200}" "$3"; nap 0.6; xdotool key Return
  mark "$E" "line: $4 placed"; nap 0.9
}
seg 1200 1000 25 "right 25" 1.6 320
seg 1200 904 10 "up 10"
seg 1152 904 5 "left 5"
seg 1152 952 5 "down 5"
seg 1008 952 15 "left 15"
seg 1008 424 55 "up 55"
seg 960 424 5 "left 5"
mark "$E" "line: close on the first point"
glide 960 1000 22; nap 0.9; xdotool click 1; nap 1.0
mark "$E" "line: Esc puts the Line tool down"
nap 0.6; xdotool key Escape; nap 1.0
mark "$E" "sketch: closed, fully constrained"
glide 1700 395; nap 2.4
mark "$E" "finish sketch"
glide 1372 125; nap 1.0; xdotool click 1; nap 2.0
mark "$E" "extrude: Model tab, Extrude"
glide 163 67; nap 0.5; xdotool click 1; nap 0.6; glide 258 115; nap 1.4; xdotool click 1; nap 2.6
mark "$E" "extrude: the panel"
glide 1750 470; nap 1.4; glide 1790 542; nap 1.0
focus_app
mark "$E" "extrude: type 20"
xdotool type --delay 320 20; nap 1.2
mark "$E" "extrude: OK"
glide 1851 771; nap 0.8; xdotool click 1; nap 2.0
mark "$E" "home: the 3D hook"
glide 1170 1109; nap 1.0; xdotool click 1; nap 2.2
glide 1250 650; nap 0.4
mark "$E" "home: right-drag turns"
xdotool mousedown 3; for i in $(seq 1 26); do rel -8 1; sleep 0.04; done; xdotool mouseup 3; nap 1.2
mark "$E" "home: wheel zooms"
for i in 1 2 3; do xdotool click 4; sleep 0.3; done; nap 0.8; for i in 1 2 3; do xdotool click 5; sleep 0.3; done; nap 0.8
mark "$E" "home: the house again"
glide 1170 1109; nap 0.6; xdotool click 1; nap 1.8
mark "$E" "history: two chips"
glide 271 1167; nap 1.6; glide 309 1167; nap 2.2
mark "$E" "properties: right-click Body1"
glide 135 634; nap 1.0; xdotool click 3; nap 1.4
glide 213 653; nap 0.8
mark "$E" "properties: open"
xdotool click 1; nap 1.2
mark "$E" "properties: drag the panel aside"
glide 842 317 14; nap 0.4; xdotool mousedown 1; glide 480 317 24; xdotool mouseup 1; nap 0.8
mark "$E" "properties: volume row"
glide 640 493 16; nap 2.4
mark "$E" "properties: bounding box row"
glide 640 611 12; nap 2.4
mark "$E" "properties: close"
glide 785 710; nap 0.6; xdotool click 1; nap 1.5
glide 1300 760; nap 1.0
mark "$E" "recording stopped"
stop_record30
wiggle; shot "$O/end.png"
# --- L2-Q3: read the result (no AI): a scripted MCP client over the entry SolidCraft wrote, bridged to this window
python3 - "$O" <<'EOF'
import json, os, sys
sys.path.insert(0, '/work')
from checker import entry, outline, recipe
from client.mcp import McpClient
o = sys.argv[1]
e = entry.read(os.path.expanduser('~/.claude.json'))
c = McpClient([e['command']] + e['args'], timeout_s=120, log_path=os.path.join(o, 'read-transcript.jsonl'))
init = c.start()
json.dump(c.list_tools(), open(os.path.join(o, 'tools.json'), 'w'), indent=1)
ins = McpClient.text_json(c.call_tool('inspect_design', {}))
mea = McpClient.text_json(c.call_tool('measure', {}))
c.close()
s = recipe.summary(ins, mea)
exp = outline.expected(outline.J_MOVES, width=20)
sk = (ins.get('sketches') or [{}])[0]
res = {'entry_command': [e['command']] + e['args'], 'summary': s, 'expected': {k: v for k, v in exp.items() if k != 'vertices'},
       'volume_matches_expected': abs((s['volume_mm3'] or 0) - exp['volume_mm3']) < 1e-6,
       'sketch': {'fully_constrained': sk.get('fully_constrained'), 'dof': sk.get('dof'),
                  'dimensions': sum(1 for k in sk.get('constraints') or [] if k.get('param')),
                  'constraints': len(sk.get('constraints') or []), 'plane': sk.get('plane')},
       'inspect_design': ins, 'measure': mea}
json.dump(res, open(os.path.join(o, 'read.json'), 'w'), indent=1)
print(json.dumps({k: res[k] for k in ('summary', 'volume_matches_expected', 'sketch')}, indent=1))
EOF
quit_app
