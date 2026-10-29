#!/bin/bash
# L3-Q2 + Q3: the J drawn from five named sizes through SolidCraft 0.26.1's real window, then hook_depth changed from
# 25 to 40, filmed. Only xdotool clicks, mouse moves and typed text reach the app (no control channel, no MCP) until
# the recording stops. The "before" numbers are the Properties rows filmed before the change (props-before.png); after
# the recording a scripted MCP client (no AI) reads the result over the entry `solidcraft-cli mcp setup` wrote.
#   docker run --rm --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc3-l3:0.26.1 bash /work/lab/l3hand.sh hand
# Writes out/l3/RUN/: screen.mp4 (30 fps, 2880x1800), cursor.jsonl, events.jsonl, shots, read.json.
# Positions are in 1920x1200 units (l2common.sh), learned in the $0 probe (out/scratch/l3p, not committed).
set -u
RUN=${1:-hand}
O=/work/out/l3/$RUN
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
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
fill_window 0 0 $W $H; sleep 1
glide 1300 760 4; sleep 0.5
typed() { xdotool type --delay "${2:-150}" "$1"; }
record30 "$O/screen.mp4" "$O/cursor.jsonl"
mark "$E" "recording started: the start page"
nap 1.5
mark "$E" "start page: New design"
glide 530 274 24; nap 1.2; xdotool click 1; nap 2.0
glide 1300 760 16; nap 1.0
# --- F6-F8: Parameters, five names
mark "$E" "params: hover Parameters"
glide 1013 117 24; nap 1.8
mark "$E" "params: open"
xdotool click 1; nap 2.4
mark "$E" "params: Add parameter"
glide 1063 628 22; nap 1.4; xdotool click 1; nap 1.2
focus_app
row() {   # row NAME VALUE [DELAY]: type the name, Tab twice, the value, Enter
  mark "$E" "params: type $1"
  typed "$1" "${3:-150}"; nap 0.7
  mark "$E" "params: Tab Tab"
  xdotool key Tab; nap 0.5; xdotool key Tab; nap 0.7
  mark "$E" "params: $1 value $2"
  typed "$2" 220; nap 0.8; xdotool key Return
  mark "$E" "params: $1 added"; nap "${4:-1.0}"
}
row hook_depth 25 170 2.6
row thickness 5 90
row lip_height 10 90
row plate_height 60 90
row width 20 90 1.6
mark "$E" "params: OK"
glide 1851 972 22; nap 1.0; xdotool click 1; nap 1.6
# --- F9: New Sketch, XZ, slide down, Line, origin
mark "$E" "new sketch: New Sketch"
glide 171 115 20; nap 1.0; xdotool click 1; nap 1.4
mark "$E" "browser: open Origin"
glide 40 353 22; nap 0.8; xdotool click 1; nap 1.0
mark "$E" "new sketch: XZ in the Browser"
glide 122 540 20; nap 1.0; xdotool click 1; nap 2.2
glide 960 620 22; nap 1.0
mark "$E" "sketch: middle-drag pan"
xdotool mousedown 2; for i in $(seq 1 20); do rel 0 19; sleep 0.1; done; xdotool mouseup 2; nap 1.0
mark "$E" "sketch: Line tool"
glide 155 115; nap 1.0; xdotool click 1; nap 1.0
mark "$E" "sketch: click the origin"
glide 960 1000; nap 1.0; xdotool click 1; nap 1.0
focus_app
seg() {   # seg X Y TEXT NAME [HOLD DELAY STEPS AFTER]: point the way the line goes, type the name or sum, Enter
  glide "$1" "$2" "${7:-22}"; nap "${5:-0.9}"
  mark "$E" "line: $4 type"
  typed "$3" "${6:-150}"; nap 0.8; xdotool key Return
  mark "$E" "line: $4 placed"; nap "${8:-1.0}"
}
seg 1200 1000 hook_depth "right hook_depth" 3.4 220 60 3.4
seg 1200 904 lip_height "up lip_height"
seg 1152 904 thickness "left thickness"
seg 1152 952 "lip_height - thickness" "down lip_height - thickness"
seg 1008 952 "hook_depth - 2 * thickness" "left hook_depth - 2 * thickness" 1.2 150 22 1.6
seg 1008 424 "plate_height - thickness" "up plate_height - thickness" 1.2 150 22 1.4
seg 960 424 thickness "left thickness (top)"
mark "$E" "line: close on the first point"
glide 960 1000 22; nap 0.9; xdotool click 1; nap 1.0
mark "$E" "line: Esc puts the Line tool down"
nap 0.6; xdotool key Escape; nap 1.0
mark "$E" "sketch: closed, fully constrained"
glide 1700 395; nap 3.0
# --- F13: Finish, Extrude width, OK, the house
mark "$E" "finish sketch"
glide 1348 125; nap 1.0; xdotool click 1; nap 1.8
mark "$E" "extrude: Model tab, Extrude"
glide 163 67; nap 0.5; xdotool click 1; nap 0.6; glide 258 115; nap 1.2; xdotool click 1; nap 2.2
focus_app
mark "$E" "extrude: type width"
typed width 200; nap 1.6
mark "$E" "extrude: OK"
glide 1851 772; nap 0.8; xdotool click 1; nap 1.8
mark "$E" "home: the 3D hook"
glide 1160 1103; nap 1.0; xdotool click 1; nap 2.0
# --- F14: Properties before the change
mark "$E" "properties: right-click Body1"
glide 135 634; nap 1.0; xdotool click 3; nap 1.4
glide 213 653; nap 0.8
mark "$E" "properties: open"
xdotool click 1; nap 1.6
shot "$O/props-before.png"
mark "$E" "properties: rows held"
glide 900 500 16; nap 4.5
mark "$E" "properties: close"
xdotool key Escape; nap 1.2
# --- F16: slide the hook left so the dialog doesn't cover it, then hook_depth 25 -> 40
glide 1300 700 16; nap 0.6
mark "$E" "view: slide left"
xdotool mousedown 2; for i in $(seq 1 20); do rel -22 -5; sleep 0.06; done; xdotool mouseup 2; nap 1.0
mark "$E" "change: open Parameters"
glide 1013 117 22; nap 1.0; xdotool click 1; nap 2.0
mark "$E" "change: click hook_depth's 25"
glide 1428 608 22; nap 1.2; xdotool click 1; nap 0.6
focus_app
xdotool key ctrl+a; nap 0.8
mark "$E" "change: type 40"
typed 40 300; nap 1.0
mark "$E" "change: Enter"
xdotool key Return; nap 4.0
shot "$O/after-enter.png"
mark "$E" "change: OK"
glide 1851 993 22; nap 0.8; xdotool click 1; nap 1.6
mark "$E" "home: the 40 hook"
glide 1160 1103; nap 1.0; xdotool click 1; nap 2.0
mark "$E" "properties after: right-click Body1"
glide 135 634; nap 1.0; xdotool click 3; nap 1.4
glide 213 653; nap 0.8
mark "$E" "properties after: open"
xdotool click 1; nap 1.6
shot "$O/props-after.png"
mark "$E" "properties after: rows held"
glide 900 500 16; nap 4.5
mark "$E" "recording stopped"
stop_record30
xdotool key Escape; sleep 0.5
wiggle; shot "$O/end.png"
# --- L3-Q3: read the result (no AI) over the entry SolidCraft wrote, bridged to this window
python3 /work/lab/l3read.py "$O" hand
quit_app
