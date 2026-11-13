# fx13 helpers (LAB-fx13): the generic part of lab/fx12lib.sh (setup, recording, events, open_sc, vol), sourced inside
# each) and by the probe session. Display 2880x1620 (16:9, the fx6-fx8 convention), SolidCraft at UI scale 1.8.
# GUI takes (A, B, C): SolidCraft fills the whole display. Take D: SolidCraft top pane + terminal strip (fx7alt layout).
# GUI positions in 1440x810 units (halved screenshots), as lab/fx7altlib.sh.
W2=2880 H2=1620
. /work/lab/common.sh
W2=2880 H2=1620 . /work/lab/l2common.sh
export DISPLAY=:99 LANG=C.UTF-8 LC_ALL=C.UTF-8
APP_H=${APP_H:-1620}; TERM_Y=${TERM_Y:-1134}; TERM_H=${TERM_H:-486}
mkdir -p /tmp/fx13
[ -f /tmp/fx13/T0 ] && T0=$(cat /tmp/fx13/T0)
O=${O:-$(cat /tmp/fx13/O 2>/dev/null)}
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
take() { O=/work/out/fx13/$1; mkdir -p "$O"; echo "$O" > /tmp/fx13/O; }
rec_start() {   # the whole display, 30 fps, cursor drawn
  : > "$O/cursor.jsonl"; : > "$O/events.jsonl"
  setsid ffmpeg -loglevel error -y -f x11grab -draw_mouse 1 -framerate 30 -video_size ${W}x${H} -i :99 \
    -c:v libx264 -preset ultrafast -crf 14 -pix_fmt yuv420p "$O/${1:-screen}.mp4" < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx13/rec.pid; date +%s.%N > /tmp/fx13/T0; T0=$(cat /tmp/fx13/T0); sleep 0.5
  setsid python3 /work/lab/cursorlog.py "$O/cursor.jsonl" "$T0" 30 < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx13/cur.pid
}
rec_stop() {
  touch "$O/cursor.jsonl.stop"; sleep 1; rm -f "$O/cursor.jsonl.stop"
  kill -INT "$(cat /tmp/fx13/rec.pid)"; for i in $(seq 1 30); do kill -0 "$(cat /tmp/fx13/rec.pid)" 2>/dev/null || break; sleep 0.5; done
  rm -f /tmp/fx13/T0; T0=
}
still() { g 1250 700 14; }                            # park the cursor in empty space (bottom right of the view)
envcheck() {    # rule P0 into out/fx13/env.txt
  local E=/work/out/fx13/env.txt
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
      -e env PS1='$ ' tmux -u new-session -s t -c /work/out/fx13 "bash --norc" > /dev/null 2>&1 &
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
  cp "/work/out/fx13/P/$1.sc" "$HOME/$1.sc"
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

# ---- fx13 positions: probe container fx13p (out/scratch/fx13p s0-s20, gitignored), 0.28.0 at UI scale 1.8, ~/cup.sc
# opened by the plug (fit view), halved units. Shell dialog: Faces/Body, Thickness (default 2 mm), Direction (Inside),
# OPTIONS > Tangent chain (ticked by default).
MODEL_TAB="122 50"; INSPECT_TAB="382 50"; HOME_BTN="870 737"; ORBIT_BTN="707 737"
SHELL_BTN="457 90"                                   # Model > Modify > Shell (on the ribbon; also Modify > Bodies > Shell)
SH_CHAIN="1215 438"; SH_THICK="1350 347"; SH_FACES_X="1410 317"; SH_CLOSE_X="1413 272"
SH_OK="1388 487"; SH_CANCEL="1322 487"               # no error line
SH_OK_ERR="1388 565"; SH_CANCEL_ERR="1322 565"; SH_ISSUE="1252 516"   # with the red line + Create Issue...
ISSUE_CLOSE="734 670"
TOP60="835 270"; SIDE60="837 450"                    # cup.sc / cup-bottom.sc / cup-r3.sc (D60 x 80): top face, side at mid-height
TOP40="837 290"                                      # cup40.sc (D40 x 40)
ORIGIN_ROW="31 264"; XZ_ROW="85 405"                 # Browser: Origin chevron; XZ with Origin expanded
BODY_ROW="94 311"; PROPS_ITEM="153 400"; PROPS_CLOSE="860 487"   # Body1 with Origin collapsed; its right-click menu; Properties Close
SECTION_BTN="296 90"; SEC_FLIP="1215 408"; SEC_OK="1388 458"; SEC_PILL_X="873 172"
MEASURE_BTN="120 85"; ME_ITEMS_X="1410 317"; ME_CLOSE_X="1410 272"
OUT_SIDE_SEC="962 450"; IN_SIDE_SEC="845 380"; FLOOR_SEC="880 560"   # with the XZ section (flipped) at the Home view
GIZMO_MINUS_Z="1387 220"; BOTTOM_FROM_BELOW="760 580"
model_tab() { g $MODEL_TAB 16; click; nap 1.0; }
inspect_tab() { g $INSPECT_TAB 16; click; nap 1.0; }
home_view() { ev "Home view"; g $HOME_BTN 16; click; nap 2.0; still; }
orbit() {        # orbit SECS: the Orbit button, a slow drag left and back over SECS seconds, then the Home view
  local s=${1:-4}; ev "slow orbit (Orbit button, drag)"; g $ORBIT_BTN 16; click; nap 0.8
  g 1000 450 14; xdotool mousedown 1; g 1120 440 $((s * 15)); nap 0.3; g 1000 450 $((s * 15)); xdotool mouseup 1; nap 0.8
  xdotool key Escape; nap 0.5; home_view
}
shell_open() {   # Model > Shell; the dialog with its defaults held 2 s, shot NAME
  model_tab; ev "Shell (Model tab > Modify > Shell)"; g $SHELL_BTN 18; click; nap 2.0; still
  ev "Shell dialog with its defaults (Tangent chain ticked?, Thickness, Direction) as shown in ${1:-dialog}.png: hold 2 s"
  nap 2.0; cp_shot "${1:-dialog}"
}
chain_off() { ev "zoom target: the Tangent chain checkbox (ticked): hold 2 s"; g $SH_CHAIN 16; nap 2.0
  ev "untick Tangent chain"; click; nap 1.5; still; cp_shot "${1:-untick}"; }
pick() { ev "$1"; g $2 $3 16; click; nap 2.0; still; }       # pick LABEL X Y: a face in the view
thick() { ev "Thickness: $1 (typed), Tab"; g $SH_THICK 16; click; xdotool key ctrl+a; nap 0.3; typed "$1" 140; nap 0.4; xdotool key Tab; nap 2.0; still; }
section_xz() {   # Inspect > Section, Plane = XZ (Browser > Origin), Flip, OK: the cut faces the camera
  inspect_tab; ev "Inspect > Section"; g $SECTION_BTN 16; click; nap 2.0
  ev "Browser: expand Origin, Plane = XZ"; g $ORIGIN_ROW 16; click; nap 1.2; g $XZ_ROW 16; click; nap 2.0
  ev "Flip"; g $SEC_FLIP 14; click; nap 2.0; ev "OK"; g $SEC_OK 14; click; nap 2.0; still
}
section_off() { ev "section off (the pill's x)"; g $SEC_PILL_X 14; click; nap 2.0; still; }
props_body() {  # props_body SHOT: Browser > Body1 right-click > Properties, held 4 s, shot, Close
  ev "Browser: Body1 right-click > Properties"; g $BODY_ROW 16; nap 1.0; xdotool click 3; nap 1.5
  g $PROPS_ITEM 14; click; nap 2.0; still; ev "Properties as shown in $1.png: hold 4 s"; nap 4.0; cp_shot "$1"
  ev "Close"; g $PROPS_CLOSE 14; click; nap 1.5; still
}
