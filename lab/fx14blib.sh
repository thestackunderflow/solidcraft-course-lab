# fx14b helpers (LAB-fx14b section 7): the generic part of lab/fx13lib.sh (setup, recording, events, open_sc, vol),
# sourced inside sc5-l5:0.28.0 by every lab/fx14bX.sh take (one container per take, a fresh home each) and by the probe session. Display 2880x1620 (16:9, the fx6-fx8 convention), SolidCraft at UI scale 1.8.
# GUI takes (A, B, C): SolidCraft fills the whole display. Take D: SolidCraft top pane + terminal strip (fx7alt layout).
# GUI positions in 1440x810 units (halved screenshots), as lab/fx7altlib.sh.
W2=2880 H2=1620
. /work/lab/common.sh
W2=2880 H2=1620 . /work/lab/l2common.sh
export DISPLAY=:99 LANG=C.UTF-8 LC_ALL=C.UTF-8
APP_H=${APP_H:-1620}; TERM_Y=${TERM_Y:-1134}; TERM_H=${TERM_H:-486}
mkdir -p /tmp/fx14b
[ -f /tmp/fx14b/T0 ] && T0=$(cat /tmp/fx14b/T0)
O=${O:-$(cat /tmp/fx14b/O 2>/dev/null)}
g() { glide "$(awk -v v="$1" 'BEGIN{printf "%d", v*4/3}')" "$(awk -v v="$2" 'BEGIN{printf "%d", v*4/3}')" "${3:-20}"; }
click() { nap 1.0; xdotool click 1; }                 # a 1 s pause before each click
dclick() { nap 1.0; xdotool click --repeat 2 --delay 120 1; }
typed() { xdotool type --delay "${2:-80}" "$1"; }
cp_shot() { shot "$O/$1.png"; }
ev() {          # LAB events.txt line (wall clock) + events.jsonl (seconds since T0, for footage.py)
  printf '%s  %s\n' "$(date -u +%H:%M:%S.%1N)" "$1" >> "$O/events.txt"
  [ -n "${T0:-}" ] && mark "$O/events.jsonl" "$(printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g')"
  echo "ev: $1"
}
take() { O=/work/out/fx14b/$1; mkdir -p "$O"; echo "$O" > /tmp/fx14b/O; }
rec_start() {   # the whole display, 30 fps, cursor drawn
  : > "$O/cursor.jsonl"; : > "$O/events.jsonl"
  setsid ffmpeg -loglevel error -y -f x11grab -draw_mouse 1 -framerate 30 -video_size ${W}x${H} -i :99 \
    -c:v libx264 -preset ultrafast -crf 14 -pix_fmt yuv420p "$O/${1:-screen}.mp4" < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx14b/rec.pid; date +%s.%N > /tmp/fx14b/T0; T0=$(cat /tmp/fx14b/T0); sleep 0.5
  setsid python3 /work/lab/cursorlog.py "$O/cursor.jsonl" "$T0" 30 < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx14b/cur.pid
}
rec_stop() {
  touch "$O/cursor.jsonl.stop"; sleep 1; rm -f "$O/cursor.jsonl.stop"
  kill -INT "$(cat /tmp/fx14b/rec.pid)"; for i in $(seq 1 30); do kill -0 "$(cat /tmp/fx14b/rec.pid)" 2>/dev/null || break; sleep 0.5; done
  rm -f /tmp/fx14b/T0; T0=
}
still() { g 1250 700 14; }                            # park the cursor in empty space (bottom right of the view)
envcheck() {    # rule P0 into out/fx14b/env.txt
  local E=/work/out/fx14b/env.txt
  { echo "solidcraft --version: $(/opt/solidcraft/bin/solidcraft --version 2>&1)"; echo "claude --version: $(claude --version 2>&1)";
    echo "date: $(date -u)"; } > "$E"
  grep -q 'solidcraft 0.28.0' "$E" || { echo "P0: wrong SolidCraft version"; cat "$E"; exit 3; }
}
# setup [split]: a fresh home's SolidCraft (lesson 5), the MCP entry (lesson 7: `solidcraft-cli mcp setup`), the window
# filling the display (or the top pane + a terminal strip with `split`), a new design
setup() {
  mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
  solidcraft-cli mcp setup > "$O/setup.txt" 2>&1
  start_display
  openbox > /dev/null 2>&1 &
  sleep 1
  start_app "$O/app.log" /opt/solidcraft/bin/solidcraft
  sleep 10
  python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
  [ "${1:-}" = split ] && APP_H=$TERM_Y
  fill_window 0 0 $W $APP_H; sleep 2
  shot "$O/start-page.png"
  g 398 206 6; xdotool click 1; sleep 3                          # start page: New design (fx8 position)
  if [ "${1:-}" = split ]; then
    printf 'set -g status off\nset -g history-limit 5000\n' > "$HOME/.tmux.conf"
    xterm -u8 -geometry 160x12+0+$TERM_Y -fa "DejaVu Sans Mono" -fs 22 -bg white -fg black -T "Terminal" \
      -e env PS1='$ ' tmux -u new-session -s t -c /work/out/fx14b "bash --norc" > /dev/null 2>&1 &
    sleep 3
    local w; w=$(xdotool search --name "^Terminal$" | head -1)
    xdotool windowsize --sync "$w" $W $TERM_H; xdotool windowmove "$w" 0 $TERM_Y
    tmux send-keys -t t "export PS1='\$ '; clear" Enter; sleep 1
    fill_window 0 0 $W $APP_H; sleep 1
  fi
  still
}
tt() {          # tt CMD: type a command into the terminal strip at a person's pace, Enter, wait for the prompt
  local cmd=$1 i
  for ((i = 0; i < ${#cmd}; i++)); do tmux send-keys -t t -l "${cmd:i:1}"; sleep 0.08; done
  nap 0.8; tmux send-keys -t t Enter
  for i in $(seq 1 480); do [ "$(tmux capture-pane -p -t t | sed '/^[[:space:]]*$/d' | tail -1)" = '$' ] && break; sleep 0.25; done
}
pane() { tmux capture-pane -p -J -S -500 -t t > "$O/pane.txt"; }
# a take P file opened into the window, off camera: copied to ~ then the plug's `open` (fx9 deviation 1)
open_sc() {     # open_sc tower|tower-sym|block
  cp "/work/out/fx14b/P/$1.sc" "$HOME/$1.sc"
  FX9_ALLOW=1 python3 /work/lab/fx9.py open "$HOME/$1.sc" > "$O/open-$1.txt" 2>&1; sleep 3
}
vol() { FX9_ALLOW=1 python3 /work/lab/fx9.py read "$O" "$1" > "$O/read-$1.txt" 2>&1; cat "$O/read-$1.txt"; }
bodies() {       # bodies TAG: one line per body from read-TAG.json (name, volume, z range, bbox size)
  python3 - "$O/read-$1.json" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))['measure']
for b in m.get('bodies') or []:
    lo, hi = b['bbox']['min'], b['bbox']['max']
    print(f"{b['name']}: {b['volume_mm3']:.2f} mm3, z {lo[2]:.2f}..{hi[2]:.2f}, {hi[0]-lo[0]:.2f} x {hi[1]-lo[1]:.2f} x {hi[2]-lo[2]:.2f}")
print(f"total {(m.get('total') or {}).get('volume_mm3', 0):.2f} mm3, {m.get('body_count')} bodies")
PY
}

# ---- reused positions (halved units, UI scale 1.8, 2880x1620): G0's probe (out/fx14/DEVIATIONS.md 8, Home view of a
# 40 x 30 x 20 block) and lab/fx13lib.sh (tabs, view buttons, Browser Body row, Properties, Measure)
MODEL_TAB="122 50"; INSPECT_TAB="382 50"; HOME_BTN="870 737"; ORBIT_BTN="707 737"
NEW_SKETCH="128 88"; TOP_FACE="830 330"; SK_CANCEL="1180 90"; SK_ISSUE="1252 504"; ISSUE_CLOSE="733 670"
BODY_ROW="94 311"; PROPS_ITEM="153 400"; PROPS_CLOSE="860 487"; MEASURE_BTN="120 85"
model_tab() { g $MODEL_TAB 16; click; nap 1.0; }
inspect_tab() { g $INSPECT_TAB 16; click; nap 1.0; }
home_view() { ev "Home view"; g $HOME_BTN 16; click; nap 2.0; still; }
orbit() {        # orbit SECS: the Orbit button, a slow drag left and back over SECS seconds, then the Home view
  local s=${1:-4}; ev "slow orbit (Orbit button, drag)"; g $ORBIT_BTN 16; click; nap 0.8
  g 1000 450 14; xdotool mousedown 1; g 1120 440 $((s * 15)); nap 0.3; g 1000 450 $((s * 15)); xdotool mouseup 1; nap 0.8
  xdotool key Escape; nap 0.5; home_view
}
pick() { ev "$1"; g $2 $3 16; click; nap 2.0; still; }       # pick LABEL X Y: a face in the view

# ---- fx14b positions: probe container fx14bp (13 Nov; shots kept in out/fx14b/probe/), 0.28.0 at UI scale 1.8, the
# Home view of a 40 x 30 x 20 block (conv.sc, block.sc, offset.sc: top face at TOP_FACE), halved units
USE_FIXED="1254 413"; SKD_CANCEL_ERR="1322 554"      # Create Sketch dialog with the red line: Use fixed plane, Cancel
CIRCLE_BTN="231 90"; FINISH_PANEL="1329 537"         # Sketch tab > Circle (Center Diameter: a diameter field opens after the centre click)
SK_CENTRE40="968 234"                                # (20, 15) in the fixed-plane sketch on a 40 x 30 top (origin 720 420, 12.4 px/mm)
SK_CENTRE30="975 165"                                # (15, 15) on conv30.sc's top (origin 720 420, 17 px/mm; read 15.00, 15.00)
TOP30="837 362"                                      # conv30.sc's top face at its Home view
EXTRUDE_BTN="194 90"; EX_DIST="1350 407"; EX_OP="1350 437"; EX_OP_CUT="1301 514"; EX_REVERSE="1325 498"
EX_OK="1388 578"; EX_CANCEL="1322 578"
HOLE_BTN="296 90"; HOLE_DEPTH="1362 599"; HOLE_DIAM="1362 639"; HOLE_DRILL="1355 557"; HOLE_FLAT="1313 587"
HOLE_OK="1388 729"; HOLE_CANCEL="1322 729"; HOLE_OK_FLAT="1388 710"   # Flat drops the Tip Angle row: OK moves up (take C)           # Hole: Placement Single, Face, Extents Distance, Simple, Drill Point (Angle 118 deg by default)
BODY_ROW_CONV="90 311"; BODY_ROW_CUT="85 381"        # converted body row: fresh file | after Sketch1 + a cut (Sketches, Features rows added)
BODY_ROW_HOLE="90 335"                               # after Hole1 (a root Features row added)
PROPS_X_OFF=60; PROPS_Y=400                          # the body's right-click menu is clamped to the screen bottom: Properties at (row x + 60, 400)
ME_CLOSE="1396 397"; ME_TOP="700 300"                # Measure panel Close; a point on the top face away from the hole
HIST_INSERT="322 785"; HIST_CONVERT="352 785"        # History bar icons (no names): conv (Insert Mesh), ConvertMesh1
FEAT_FOLDER="43 335"                                 # Browser: conv:1 > Features chevron (fresh converted file)
SEARCH_BOX="1360 50"
sk_dialog_face() {   # sk_dialog_face X Y LABEL: Model > New Sketch (Create Sketch dialog), click the face
  model_tab; ev "Create Sketch (Model > New Sketch)"; g $NEW_SKETCH 16; click; nap 2.0
  ev "$3"; g "$1" "$2" 16; click; nap 2.5; still
}
props_at() {         # props_at ROW_X ROW_Y SHOT: the body row's right-click > Properties, held 4 s, shot, Close
  ev "Browser: the body row right-click > Properties"; g "$1" "$2" 16; nap 1.0; xdotool click 3; nap 1.5
  g $(( $1 + PROPS_X_OFF )) $PROPS_Y 14; click; nap 2.0; still; ev "Properties as shown in $3.png: hold 4 s"; nap 4.0
  cp_shot "$3"; ev "Close"; g $PROPS_CLOSE 14; click; nap 1.5; still
}
circle_d10() {       # circle_d10 X Y: Circle, the centre click, diameter 10 typed, Enter
  ev "Sketch > Circle"; g $CIRCLE_BTN 16; click; nap 1.5
  ev "circle centre click"; g "$1" "$2" 16; click; nap 1.0; g $(( $1 + 42 )) "$2" 16; nap 1.0
  ev "diameter 10 typed, Enter"; xdotool key ctrl+a; typed "10" 140; xdotool key Return; nap 1.5; xdotool key Escape; nap 1.0; still
}
cut5() {             # Model > Extrude (the circle profile preselected), Operation Cut, Distance 5, Reverse (into the block), OK
  ev "Finish Sketch"; g $FINISH_PANEL 16; click; nap 2.5; home_view; model_tab
  ev "Model > Extrude"; g $EXTRUDE_BTN 16; click; nap 2.0
  ev "Operation: Cut"; g $EX_OP 16; click; nap 1.2; g $EX_OP_CUT 14; click; nap 1.2
  ev "Distance: 5 mm (typed), Tab"; g $EX_DIST 16; click; xdotool key ctrl+a; typed "5 mm" 140; xdotool key Tab; nap 1.5
  ev "Reverse (into the block)"; g $EX_REVERSE 14; click; nap 2.0; still; ev "cut preview: hold 2 s"; nap 2.0
  cp_shot "${1:-cut-preview}"
  ev "OK"; g $EX_OK 14; click; nap 3.0; still
}
