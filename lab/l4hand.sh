#!/bin/bash
# L4-Q2 + Q3: two screw holes and a fillet on lesson 3's hook through SolidCraft 0.27.1's real window, then width 20 to
# 30 (typed 10: the holes stay 10 from the left edge), then the fix in Parameters (d5, d9 = width / 2), then width 20
# again. Filmed. Before the recording, the hook is built from lesson 3's five names by script (no AI, lab/l4hook.py).
# During the recording only xdotool clicks, mouse moves and typed text change the design; at four points a read-only
# plug read (lab/l4read.py: measure, body_topology, parameters.list) records the numbers (it changes nothing).
#   docker run --rm --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc4-l4:0.27.1 bash /work/lab/l4hand.sh hand
#   DRY=1 ... : the same moves without the recording (checkpoint screenshots only), into out/scratch/l4dry
# Writes out/l4/RUN/: screen.mp4 (30 fps, 2880x1800), cursor.jsonl, events.jsonl, shots, read-*.json.
# Positions are in 1440x900 units (the probe's screenshots, out/scratch/l4p), UI scale 1.8.
set -u
RUN=${1:-hand}
O=/work/out/l4/$RUN
[ -n "${DRY:-}" ] && O=/work/out/scratch/l4dry/$RUN
[ -e "$O/read-width20.json" ] && { echo "refusing: $O/read-width20.json exists"; exit 1; }
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
c43() { awk -v v="$1" 'BEGIN{printf "%d", v*4/3}'; }
g() { glide "$(c43 "$1")" "$(c43 "$2")" "${3:-20}"; }          # g X Y [STEPS], 1440x900 units
click() { xdotool click 1; }
typed() { xdotool type --delay "${2:-150}" "$1"; }
cp_shot() { shot "$O/cp-$1.png"; }                                # checkpoint screenshot
read_now() { python3 /work/lab/l4read.py "$O/read-$1.json" > "$O/read-$1.txt" 2>&1; }
# --- setup (not filmed): a new design, lesson 3's hook from its names, the 3D view
g 398 230 4; sleep 0.5; click; sleep 3                           # start page: New design
python3 /work/lab/l4hook.py "$O" > "$O/hook-setup.txt" 2>&1
g 870 827 4; sleep 0.4; click; sleep 1.5                        # the house: the 3D view
g 1000 600 4; sleep 0.5
if [ -z "${DRY:-}" ]; then record30 "$O/screen.mp4" "$O/cursor.jsonl"; else T0=$(date +%s.%N); fi
mark "$E" "recording started: lesson 3's hook"
nap 3.0
# --- F6: Parameters, one new name
mark "$E" "params: hover Parameters"
g 760 90 24; nap 1.6
mark "$E" "params: open"
click; nap 2.4
mark "$E" "params: five names held"
nap 2.0
mark "$E" "params: Add parameter"
g 797 613 22; nap 1.2; click; nap 1.2
focus_app
mark "$E" "params: type hole_d"
typed hole_d 170; nap 0.8
mark "$E" "params: Tab Tab"
xdotool key Tab; nap 0.5; xdotool key Tab; nap 0.7
mark "$E" "params: hole_d value 4.5"
typed 4.5 220; nap 0.8; xdotool key Tab
mark "$E" "params: hole_d added"; nap 2.4
cp_shot params
mark "$E" "params: OK"
g 1388 745 22; nap 0.8; click; nap 1.6
# --- F8-F12: the first hole
hole() {   # hole N FACE_Y D1
  mark "$E" "hole$1: Hole button"
  g 297 90 22; nap 1.2; click; nap 1.6
  mark "$E" "hole$1: click the face"
  g 737 "$2" 24; nap 1.4; click; nap 2.2
  mark "$E" "hole$1: Extents"
  g 1355 468 22; nap 1.0; click; nap 1.2
  mark "$E" "hole$1: All"
  g 1310 546 12; nap 0.9; click; nap 1.6
  mark "$E" "hole$1: Reference 1"
  g 1355 409 18; nap 1.0; click; nap 1.0
  mark "$E" "hole$1: top edge"
  g 733 211 26; nap 1.4; click; nap 1.4
  focus_app
  mark "$E" "hole$1: Distance 1 $3"
  g 1355 438 18; nap 0.6; click; nap 0.4; xdotool key ctrl+a; typed "$3" 260; nap 0.6; xdotool key Tab; nap 1.8
  mark "$E" "hole$1: Reference 2"
  g 1355 468 18; nap 1.0; click; nap 1.0
  mark "$E" "hole$1: left edge"
  g 666 470 26; nap 1.4; click; nap 1.4
  focus_app
  mark "$E" "hole$1: Distance 2 10"
  g 1355 498 18; nap 0.6; click; nap 0.4; xdotool key ctrl+a; typed 10 260; nap 0.6; xdotool key Tab; nap 2.2
  mark "$E" "hole$1: Diameter hole_d"
  g 1360 660 18; nap 0.6; click; nap 0.4; xdotool key ctrl+a; typed hole_d 170; nap 0.6; xdotool key Tab; nap 1.6
  cp_shot "hole$1"
  mark "$E" "hole$1: OK"
  g 1388 742 22; nap 0.8; click; nap 2.4
  mark "$E" "hole$1: done"
}
hole 1 330 15
g 1000 600 16; nap 1.0
hole 2 560 45
g 1000 600 16; nap 1.0
# --- F14: the fillet
mark "$E" "fillet: Fillet button"
g 353 90 22; nap 1.2; click; nap 1.6
mark "$E" "fillet: front top edge"
g 733 211 26; nap 1.4; click; nap 1.4
mark "$E" "fillet: back top edge"
g 701 193 14; nap 1.2; click; nap 1.6
mark "$E" "fillet: Radius 2"
g 1350 348 20; nap 1.0; click; nap 0.4; xdotool key ctrl+a; typed "2" 260; nap 0.6; xdotool key Tab; nap 2.4
cp_shot fillet
mark "$E" "fillet: OK"
g 1388 581 22; nap 0.8; click; nap 2.4
mark "$E" "fillet: done"
g 1000 600 16; nap 1.5
read_now fillet
# --- F16: Properties
props() {   # props TAG
  mark "$E" "properties $1: right-click Body1"
  g 101 311 22; nap 1.0; xdotool click 3; nap 1.4
  g 160 449 14; nap 0.8
  mark "$E" "properties $1: open"
  click; nap 1.6
  cp_shot "props-$1"
  mark "$E" "properties $1: rows held"
  g 900 600 16; nap 4.5
  mark "$E" "properties $1: close"
  xdotool key Escape; nap 1.2
}
props before
# the plate straight on (Right view), fitted
rightview() {   # rightview TAG HOLD
  mark "$E" "view $1: Right view"
  g 300 700 16; nap 0.4; click; nap 0.4; xdotool key ctrl+4; nap 1.4
  g 809 827 18; nap 0.6; click; nap 1.6                          # fit
  cp_shot "right-$1"
  mark "$E" "view $1: held"
  g 1100 300 12; nap "$2"
  mark "$E" "view $1: back to 3D"
  g 870 827 18; nap 0.6; click; nap 1.6
}
rightview width20 3.0
# slide the hook left so the Parameters dialog doesn't cover it
slide() {
  g 1000 600 12; nap 0.4
  mark "$E" "view: slide left"
  xdotool mousedown 2; for i in $(seq 1 20); do rel -26 0; sleep 0.06; done; xdotool mouseup 2; nap 1.0
}
slide
# --- F17: width 20 -> 30
mark "$E" "change: open Parameters"
g 760 90 22; nap 1.0; click; nap 2.0
mark "$E" "change: click width's 20"
g 1123 488 22; nap 1.2; click; nap 0.6
focus_app
xdotool key ctrl+a; nap 0.8
mark "$E" "change: type 30"
typed 30 300; nap 1.0
mark "$E" "change: Enter"
xdotool key Return; nap 4.0
cp_shot change30
mark "$E" "change: OK"
g 1388 745 22; nap 0.8; click; nap 1.6
read_now width30
rightview width30 4.5
props width30
slide
# --- F20: the fix in Parameters: d5 and d9 = width / 2
rowpos() {   # rowpos FEATURE: "ROW_Y OK_Y" of the feature's distance row whose value is 10, from the last read (no AI)
  python3 - "$O/read-width30.json" "$1" <<'PY'
import json, sys
ps = [p for p in json.load(open(sys.argv[1]))['parameters_list']['parameters'] if p.get('feature') == sys.argv[2]]
k = next(i for i, p in enumerate(ps) if 'distance' in str(p.get('input', '')).lower() and abs(p['value'] - 10) < 1e-6)
print(int(590 + 32.5 * k), int(708 + 32.5 * (len(ps) - 3)), ps[k]['name'])
PY
}
fixrow() {   # fixrow Hole1|Hole2
  read -r RY OKY DN < <(rowpos "$1")
  echo "$1: row y $RY, OK y $OKY, $DN" >> "$O/fixrows.txt"
  mark "$E" "fix: Filter $1"
  g 1128 336 20; nap 0.8; click; nap 0.4; xdotool key ctrl+a; typed "$1" 220; nap 2.4
  mark "$E" "fix: click $1's 10 ($DN)"
  g 1130 "$RY" 20; nap 1.0; click; nap 0.5; xdotool key ctrl+a; nap 0.6
  mark "$E" "fix: type width / 2 into $1"
  typed "width / 2" 170; nap 0.8
  mark "$E" "fix: Enter $1"
  xdotool key Return; nap 3.4
  cp_shot "fix-$1"
}
mark "$E" "fix: open Parameters"
g 760 90 22; nap 1.0; click; nap 2.0
fixrow Hole1
fixrow Hole2
mark "$E" "fix: OK"
g 1388 "$OKY" 22; nap 0.8; click; nap 1.6
read_now fixed
rightview fixed 4.5
# --- F21: back to 20 wide, still centred
slide
mark "$E" "back: open Parameters"
g 760 90 22; nap 1.0; click; nap 2.0
mark "$E" "back: Filter cleared"
g 1128 336 20; nap 0.6; click; nap 0.3; xdotool key ctrl+a; xdotool key BackSpace; nap 1.2
mark "$E" "back: click width's 30"
g 1123 488 22; nap 1.0; click; nap 0.5; xdotool key ctrl+a; nap 0.5
mark "$E" "back: type 20"
typed 20 300; nap 0.8; xdotool key Return; nap 3.0
mark "$E" "back: OK"
g 1388 745 22; nap 0.8; click; nap 1.6
read_now width20
rightview width20b 4.0
mark "$E" "recording stopped"
[ -z "${DRY:-}" ] && stop_record30
wiggle; shot "$O/end.png"
quit_app
