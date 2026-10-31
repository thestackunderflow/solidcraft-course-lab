#!/bin/bash
# L6-Q2: change lesson 5's finished hook by hand in SolidCraft 0.28.0 and check the must-stay-true list, through the
# real windows, filmed: the opening measured (Inspect > Measure: the plate's front face, then the lip's top face), the
# J side straight on, Parameters: hook_depth 25 -> 30 (the number that looks right) and Measure again, hook_depth 30 ->
# 40 and Measure again, then the list line by line (a hole's size and its centre to the side, the round top edge, the
# lip's front edge (its height) and top edge (its thickness), the
# Browser's "1 body", Properties' bounding box), Send to Slicer (the Print face row) -> PrusaSlicer on its side, Slice
# now. Before the recording the hook is built by script (no AI, lab/l6part.py) and PrusaSlicer's settings are seeded.
# During the recording only xdotool moves, clicks and keys change anything. After it (not filmed) our no-AI read
# (lab/l6read.py --send) scores the design, then hook_depth 30 is set over the plug and read again, then 40 again.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/l6hand.sh hand
#   DRY=1 ... : the same moves without the recording (checkpoint screenshots only), into out/scratch/l6dry
# Positions are in 1440x900 units (the probe's screenshots, out/scratch/l6p/ui), SolidCraft UI scale 1.8, GDK scale 2.
set -u
RUN=${1:-hand}
O=/work/out/l6/$RUN
[ -n "${DRY:-}" ] && O=/work/out/scratch/l6dry/$RUN
[ -e "$O/read-final.json" ] && { echo "refusing: $O/read-final.json exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
. /work/lab/l2common.sh
. /work/lab/l5slicerseed.sh
E=$O/events.jsonl; : > "$E"; : > "$O/cursor.jsonl"
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
solidcraft-cli mcp setup > "$O/setup.txt" 2>&1
seed_slicer
start_display
openbox > /dev/null 2>&1 &
sleep 1
start_app "$O/app.log"
sleep 10
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
fill_window 0 0 $W $H; sleep 1
c43() { awk -v v="$1" 'BEGIN{printf "%d", v*4/3}'; }
g() { glide "$(c43 "$1")" "$(c43 "$2")" "${3:-20}"; }          # g X Y [STEPS], 1440x900 units
click() { xdotool click 1; }
typed() { xdotool type --delay "${2:-150}" "$1"; }
cp_shot() { shot "$O/cp-$1.png"; }
SLICED=/root/.cache/solidcraft/slicer
slicer_win() { xdotool search --name "PrusaSlicer-2.9" 2>/dev/null | head -1; }
body_menu() { g 94 311 22; nap 1.0; xdotool click 3; nap 1.4; }
tab() { g "$1" 50 18; nap 0.5; click; nap 1.0; }                  # tab X: Model 122, Inspect 381
measure_open() { tab 381; mark "$E" "measure: open"; g 120 90 16; nap 0.5; click; nap 1.2; }
measure_close() { mark "$E" "measure: close"; g 1411 272 18; nap 0.5; click; nap 1.0; }
measure_clear() { g 1408 318 14; nap 0.4; click; nap 0.8; }
pick() { g "$1" "$2" "${3:-20}"; nap 0.6; click; nap 1.4; }      # pick X Y: one click on a face or edge
fit() { mark "$E" "view: Fit"; g 809 827 18; nap 0.5; click; nap 1.6; }
slide() {      # slide the hook left so the Parameters dialog doesn't cover it (middle-button drag)
  g 1000 600 12; nap 0.4
  mark "$E" "view: slide left"
  xdotool mousedown 2; for i in $(seq 1 20); do rel -26 0; sleep 0.06; done; xdotool mouseup 2; nap 1.0
}
depth() {      # depth VALUE: Parameters, hook_depth's field, the value, Enter (applies live), hold, OK
  tab 122
  slide
  mark "$E" "params $1: open Parameters"
  g 760 90 22; nap 0.8; click; nap 2.0
  mark "$E" "params $1: click hook_depth's value"
  g 1123 583 22; nap 1.0; click; nap 0.5
  xdotool key ctrl+a; nap 0.6
  mark "$E" "params $1: type $1"
  typed "$1" 300; nap 0.8
  mark "$E" "params $1: Enter"
  xdotool key Return; nap 3.0
  cp_shot "params-$1"
  mark "$E" "params $1: OK"
  g 1388 745 22; nap 0.6; click; nap 1.4
}
# --- setup (not filmed): a new design, lesson 5's hook from its names + its print face, the 3D view
g 398 206 4; sleep 0.5; click; sleep 3                           # start page: New design (millimetres)
python3 /work/lab/l6part.py "$O" > "$O/part-setup.txt" 2>&1
g 1354 164 4; sleep 0.4; click; sleep 1.5                         # the house: the 3D view
g 1000 600 4; sleep 0.5
if [ -z "${DRY:-}" ]; then record30 "$O/screen.mp4" "$O/cursor.jsonl"; else T0=$(date +%s.%N); fi
mark "$E" "recording started: lesson 5's hook"
nap 4.0
cp_shot start
# --- the J side straight on: the opening
mark "$E" "side: the green Y ball"
g 1408 186 24; nap 0.8; click; nap 2.0
cp_shot side
mark "$E" "side: hover the opening"
g 640 760 24; nap 4.0
mark "$E" "side: back to 3D (the house)"
g 1354 164 22; nap 0.6; click; nap 1.8
# --- the opening before: 15
measure_open
mark "$E" "measure 25: the plate's front face"
pick 760 450
mark "$E" "measure 25: the lip's top face"
pick 905 672
cp_shot measure-25
mark "$E" "measure 25: Distance held"
g 1300 407 18; nap 3.5
measure_close
# --- the number that looks right: 30
depth 30
fit
cp_shot fit-30
measure_open
mark "$E" "measure 30: the plate's front face"
pick "${P30X:-720}" "${P30Y:-420}"
mark "$E" "measure 30: the lip's top face"
pick "${L30X:-905}" "${L30Y:-690}"
cp_shot measure-30
mark "$E" "measure 30: Distance held"
g 1300 407 18; nap 4.0
measure_close
# --- 40
depth 40
fit
measure_open
mark "$E" "measure 40: the plate's front face"
pick 720 420
mark "$E" "measure 40: the lip's top face"
pick 948 690
cp_shot measure-40
mark "$E" "measure 40: Distance held"
g 1300 407 18; nap 3.5
# --- the list: a hole, its centre to the side, the round top edge
measure_clear
mark "$E" "list: the hole"
pick 739 318
cp_shot hole
mark "$E" "list: hole size held"
g 1310 348 16; nap 3.0
mark "$E" "list: the side edge"
pick 803 400
cp_shot hole-side
mark "$E" "list: centre to the side held"
g 1310 496 16; nap 3.5
measure_clear
mark "$E" "list: the round top edge"
pick 700 236
cp_shot fillet
mark "$E" "list: radius held"
g 1310 377 16; nap 3.0
measure_clear
mark "$E" "list: the lip's front edge (its height)"
pick 900 766
cp_shot lip-height
mark "$E" "list: lip height held"
g 1310 348 16; nap 3.0
measure_clear
mark "$E" "list: the lip's top edge (its thickness)"
pick 884 720
cp_shot lip-wall
mark "$E" "list: lip wall held"
g 1310 348 16; nap 3.0
measure_close
tab 122
# --- one body; Properties' bounding box
mark "$E" "list: hover 1 body"
g 190 164 22; nap 3.0
mark "$E" "props: right-click Body1"
body_menu
g 153 449 12; nap 0.8
mark "$E" "props: open"
click; nap 1.6
cp_shot props
mark "$E" "props: hover Bounding box"
g 760 457 14; nap 3.5
mark "$E" "props: close"
g 860 532 16; nap 0.6; click; nap 1.2
# --- Send to Slicer: the Print face row; PrusaSlicer on its side; Slice now
mark "$E" "send: right-click Body1"
body_menu
g 162 513 12; nap 0.8
mark "$E" "send: open Send to Slicer"
click; nap 2.0
cp_shot send
mark "$E" "send: hover Print face (filled)"
g 1349 348 20; nap 3.0
mark "$E" "send: Send"
g 1388 486 16; nap 0.6; click
for i in $(seq 1 120); do [ -n "$(slicer_win)" ] && break; sleep 0.5; done
sleep 6
mark "$E" "slicer: window up"
cp "$SLICED"/*.3mf "$O/sent-hand.3mf" 2>/dev/null
shot "$O/slicer-open.png"
mark "$E" "slicer: hover size boxes"
g 1190 506 22; nap 3.0
mark "$E" "slicer: hover the name (no sign)"
g 1180 336 18; nap 2.4
mark "$E" "slicer: Slice now"
g 1208 877 22; nap 0.8; click
sleep 14
mark "$E" "slicer: estimate shown"
shot "$O/slicer-estimate.png"
g 1170 826 18; nap 3.0
mark "$E" "slicer: layer slider top"
g 885 140 22; nap 3.0
mark "$E" "recording stopped"
[ -z "${DRY:-}" ] && stop_record30
wiggle; shot "$O/end.png"
quit_slicer
# --- after the recording (not filmed): our read of the design as left, then hook_depth 30 and 40 again, read each time
python3 /work/lab/l6read.py "$O/read-final.json" --send > "$O/read-final.txt" 2>&1
python3 - "$O" <<'PY' > "$O/read-30-40.txt" 2>&1
import json, os, sys
sys.path.insert(0, '/work'); sys.path.insert(0, '/work/lab')
from client.mcp import McpClient
import l6read
from l6part import plug_cmd
o = sys.argv[1]
c = McpClient(plug_cmd(None, ['--allow-path', l6read.TMP]), timeout_s=180, log_path=os.path.join(o, 'recheck-transcript.jsonl'))
c.start()
for v in (30, 40):
    c.call_tool('set_parameter', {'name': 'hook_depth', 'value': v})
    r = l6read.read(c, os.path.join(o, 'read-%d' % v), send=True)
    json.dump(r, open(os.path.join(o, 'read-%d.json' % v), 'w'), indent=1)
    print(v, r['score']['passed'], r['geom'].get('opening_mm'), [x['id'] for x in r['score']['lines'] if not x['ok']])
c.close()
PY
python3 -c "import sys, json; sys.path.insert(0, '/work'); from checker import m3mf; print(json.dumps(m3mf.check(sys.argv[1])))" "$O/sent-hand.3mf" > "$O/sent-check.jsonl" 2>&1
quit_app
cat "$O/read-final.txt" "$O/read-30-40.txt"
