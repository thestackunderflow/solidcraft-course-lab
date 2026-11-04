#!/bin/bash
# fx2 take E (LAB-fx2 section 3): SolidCraft 0.28.0 washer -> Save As Mesh STL (file written over the plug, the window's Save
# opens no file picker in the container) -> PrusaSlicer asks; Send to Slicer (3MF) -> PrusaSlicer does not ask.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx2E.sh
set -u
O=/work/out/fx2/E
mkdir -p "$O"
. /work/lab/common.sh
. /work/lab/l2common.sh
. /work/lab/l5slicerseed.sh
E=$O/events.jsonl; : > "$E"; : > "$O/cursor.jsonl"
mkdir -p "$HOME/.config/Claude" "$HOME/.claude" /root/fx2; echo '{}' > "$HOME/.claude.json"
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
# --- setup (not filmed): a new design, the washer, the 3D view
g 398 206 4; sleep 0.5; click; sleep 3
python3 /work/lab/fx2part.py "$O" --mesh > "$O/part-setup.txt" 2>&1
g 1354 164 4; sleep 0.4; click; sleep 1.5
g 1000 600 4; sleep 0.5
record30 "$O/screen.mp4" "$O/cursor.jsonl"
mark "$E" "recording started: the washer in SolidCraft"
mark "$E" "washer: shown in SolidCraft"
nap 5.0
# --- right-click, Save As Mesh, the format list, STL
mark "$E" "menu: right-click Body1"
body_menu
cp_shot menu
g 163 486 12; nap 1.6
mark "$E" "menu: open Save As Mesh"
click; nap 2.0
mark "$E" "save: open Format"
g 1349 407 18; nap 0.8; click; nap 2.4
cp_shot save-formats
g 1300 436 10; nap 0.8
mark "$E" "Save As Mesh STL: clicked"
click; nap 1.6
cp_shot save-stl
g 1322 486 12; nap 0.6; click; nap 1.6          # Cancel: the file was written over the plug (notes.txt)
# --- PrusaSlicer by hand: the STL
mark "$E" "PrusaSlicer: started by hand"
xdotool key super+Right 2>/dev/null
( prusa-slicer --datadir "$HOME/.config/PrusaSlicer" > "$O/slicer-hand.log" 2>&1 & )
for i in $(seq 1 120); do [ -n "$(slicer_win)" ] && break; sleep 0.5; done; sleep 8
wmctrl -i -r "$(slicer_win)" -b add,maximized_vert,maximized_horz; sleep 3
shot "$O/slicer-open.png"
glide 300 1500 10; click; nap 0.5
xdotool key ctrl+i; nap 3
xdotool type --delay 80 "/root/fx2/washer-sc.stl"; nap 0.8; xdotool key Return; nap 4
mark "$E" "dialog: shown"
shot "$O/slicer-dialog.png"; nap 8
glide 1663 1022 20; nap 0.6; click; nap 3
glide 300 1500 10; click; nap 0.4; xdotool key ctrl+a; nap 2.5
mark "$E" "size boxes: shown"
shot "$O/slicer-size-stl.png"; nap 8
xdotool key Delete; nap 1.5
quit_slicer_ui
# --- Send to Slicer, the default format
mark "$E" "send: right-click Body1"
body_menu
g 162 513 12; nap 0.8
mark "$E" "send: open Send to Slicer"
click; nap 2.0
cp_shot send
mark "$E" "send: hover Slicer PrusaSlicer"
g 1349 437 16; nap 2.0
mark "$E" "Send to Slicer: clicked (3MF)"
g 1388 486 16; nap 0.6; click
wait_slicer send
sliced_copy washer
mark "$E" "PrusaSlicer: opened, no dialog"
shot "$O/slicer-send-open.png"; nap 4
glide 300 1500 10; click; nap 0.4; xdotool key ctrl+a; nap 2.5
mark "$E" "size boxes: shown (send)"
shot "$O/slicer-size-3mf.png"; nap 8
quit_slicer_ui
mark "$E" "recording stopped"
stop_record30
wiggle; shot "$O/end.png"
quit_app
ls -l "$SLICED" | tee "$O/ls-cache-slicer.txt"
cp /root/fx2/washer-sc.stl "$O/"
for f in "$O"/sent-*.3mf; do unzip -p "$f" 3D/3dmodel.model | grep -n 'unit=' | tee "$O/3mf-unit-line-sc.txt"; unzip -l "$f" > "$O/3mf-list-sc.txt"; done
echo "take E done"
