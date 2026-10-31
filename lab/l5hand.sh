#!/bin/bash
# L5-Q2 + Q3: lesson 4's finished hook leaves SolidCraft 0.28.0 for PrusaSlicer 2.9.2, through the real windows,
# filmed: the checks (the Browser's "1 body", Properties), the right-click menu's two ways out, Send to Slicer with no
# print face (standing) + Slice now, then Send to Slicer with the J face as the print face + Slice now, then Save As
# Mesh's window (format list). Before the recording the hook is built by script (no AI, lab/l5part.py) and PrusaSlicer's
# settings are seeded (lab/l5slicerseed.sh: the wizard's own file). During the recording only xdotool moves, clicks and
# keys change anything. The files SolidCraft writes for the slicer are copied out after each send (they don't change
# the design).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/l5hand.sh hand
#   DRY=1 ... : the same moves without the recording (checkpoint screenshots only), into out/scratch/l5dry
# Writes out/l5/RUN/: screen.mp4 (30 fps, 2880x1800), cursor.jsonl, events.jsonl, cp-*.png, sent-*.3mf, slicer-*.png.
# Positions are in 1440x900 units (the probe's screenshots, out/scratch/l5p/ui), SolidCraft UI scale 1.8, GDK scale 2.
set -u
RUN=${1:-hand}
O=/work/out/l5/$RUN
[ -n "${DRY:-}" ] && O=/work/out/scratch/l5dry/$RUN
[ -e "$O/sent-side.3mf" ] && { echo "refusing: $O/sent-side.3mf exists"; exit 1; }
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
cp_shot() { shot "$O/cp-$1.png"; }
SLICED=/root/.cache/solidcraft/slicer
slicer_win() { xdotool search --name "PrusaSlicer-2.9" 2>/dev/null | head -1; }
wait_slicer() {   # wait_slicer TAG: until PrusaSlicer's window is up and has drawn the plate (max 60 s)
  local i
  for i in $(seq 1 120); do [ -n "$(slicer_win)" ] && break; sleep 0.5; done
  sleep 6
  mark "$E" "slicer $1: window up"
}
sliced_copy() { cp "$SLICED"/*.3mf "$O/sent-$1.3mf" 2>/dev/null; ls -la "$SLICED" >> "$O/sent-files.txt"; }
slice_now() {    # slice_now TAG: Slice now, wait for the estimate, hold on it
  mark "$E" "slicer $1: hover size boxes"
  g 1190 506 22; nap 2.4
  mark "$E" "slicer $1: Slice now"
  g 1208 877 22; nap 0.8; click
  sleep 14
  mark "$E" "slicer $1: estimate shown"
  shot "$O/slicer-$1.png"
  g 1170 826 18; nap 3.0
  mark "$E" "slicer $1: layer slider top"
  g 885 140 22; nap 3.0
}
quit_slicer_ui() {  # a person closes it: Ctrl+Q in its window (no save prompt: the seeded settings)
  mark "$E" "slicer: Ctrl+Q"
  xdotool windowactivate --sync "$(slicer_win)" key --clearmodifiers ctrl+q 2>/dev/null
  local i; for i in $(seq 1 40); do [ -z "$(slicer_win)" ] && break; sleep 0.5; done
  [ -n "$(slicer_win)" ] && { echo "slicer still up after Ctrl+Q: TERM" >> "$O/notes.txt"; quit_slicer; }
  sleep 1; focus_app
  mark "$E" "slicer: closed"
}
body_menu() {   # right-click Body1 in the Browser
  g 94 311 22; nap 1.0; xdotool click 3; nap 1.4
}
# --- setup (not filmed): a new design, lesson 4's hook from its names, the 3D view
g 398 206 4; sleep 0.5; click; sleep 3                           # start page: New design (millimetres)
python3 /work/lab/l5part.py "$O" > "$O/part-setup.txt" 2>&1
g 1354 164 4; sleep 0.4; click; sleep 1.5                         # the house: the 3D view
g 1000 600 4; sleep 0.5
if [ -z "${DRY:-}" ]; then record30 "$O/screen.mp4" "$O/cursor.jsonl"; else T0=$(date +%s.%N); fi
mark "$E" "recording started: lesson 4's hook"
nap 4.0
# --- the two ways out (right-click menu), then close it
mark "$E" "ways out: right-click Body1"
body_menu
mark "$E" "ways out: hover Save As Mesh"
g 163 486 12; nap 2.2
mark "$E" "ways out: hover Send to Slicer"
g 162 513 10; nap 2.2
cp_shot menu
xdotool key Escape; nap 1.0
g 1000 600 14; nap 0.8
# --- check 1: one body
mark "$E" "check1: hover 1 body"
g 190 164 22; nap 3.0
mark "$E" "check1: hover Body1"
g 94 311 16; nap 2.0
# --- checks 2 and 3: Properties
mark "$E" "props: right-click Body1"
body_menu
g 153 449 12; nap 0.8
mark "$E" "props: open"
click; nap 1.6
cp_shot props
mark "$E" "props: hover Volume"
g 720 368 18; nap 3.0
mark "$E" "props: hover Bounding box"
g 760 457 14; nap 3.5
mark "$E" "props: close"
g 860 532 16; nap 0.6; click; nap 1.2
# --- check 4, first without a print face: Send to Slicer, standing
mark "$E" "send1: right-click Body1"
body_menu
g 162 513 12; nap 0.8
mark "$E" "send1: open Send to Slicer"
click; nap 2.0
cp_shot send1
mark "$E" "send1: hover Print face (empty)"
g 1349 348 20; nap 2.0
mark "$E" "send1: hover Slicer PrusaSlicer"
g 1349 437 16; nap 2.0
mark "$E" "send1: Send"
g 1388 486 16; nap 0.6; click
wait_slicer standing
sliced_copy standing
shot "$O/slicer-standing-open.png"
slice_now standing
mark "$E" "slicer standing: open the warning (More)"
g 687 840 22; nap 0.8; click; nap 4.5
shot "$O/slicer-standing-warning.png"
quit_slicer_ui
# --- check 4 with the J face: Send to Slicer, Print face, the green Y ball, the face
mark "$E" "send2: right-click Body1"
body_menu
g 162 513 12; nap 0.8
mark "$E" "send2: open Send to Slicer"
click; nap 2.0
mark "$E" "send2: click Print face box"
g 1349 348 20; nap 0.8; click; nap 1.6
mark "$E" "send2: the green Y ball"
g 1408 186 24; nap 1.0; click; nap 2.4
mark "$E" "send2: click the J face"
g 610 740 24; nap 1.2; click; nap 2.4
cp_shot send2
mark "$E" "send2: face 1 held"
g 1349 348 16; nap 2.0
mark "$E" "send2: Send"
g 1388 486 16; nap 0.6; click
wait_slicer side
sliced_copy side
shot "$O/slicer-side-open.png"
slice_now side
quit_slicer_ui
# --- back to the 3D view; Save As Mesh's window (format list), then Cancel
mark "$E" "home: the house"
g 1354 164 22; nap 0.6; click; nap 1.8
mark "$E" "save: right-click Body1"
body_menu
g 163 486 12; nap 0.8
mark "$E" "save: open Save As Mesh"
click; nap 2.0
mark "$E" "save: open Format"
g 1349 407 18; nap 0.8; click; nap 2.4
cp_shot save-formats
mark "$E" "save: hover 3MF"
g 1302 460 10; nap 1.6
mark "$E" "save: pick STL"
g 1300 436 10; nap 0.6; click; nap 1.6
mark "$E" "save: hover Save"
g 1388 486 16; nap 2.4
mark "$E" "save: Cancel"
g 1322 486 12; nap 0.6; click; nap 1.6
mark "$E" "recording stopped"
[ -z "${DRY:-}" ] && stop_record30
wiggle; shot "$O/end.png"
quit_app
# --- the files sent: our checker on each (no AI, no window)
for f in "$O"/sent-*.3mf; do python3 -c "import sys, json; sys.path.insert(0, '/work'); from checker import m3mf; print(json.dumps(m3mf.check(sys.argv[1])))" "$f"; done > "$O/sent-check.jsonl"
