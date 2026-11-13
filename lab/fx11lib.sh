# fx11 helpers (LAB-fx11; a copy of fx10lib.sh), sourced inside sc5-l5:0.28.0 by every lab/fx11X.sh take (one container per take, a fresh home
# each) and by the probe session. Display 2880x1620 (16:9, the fx6-fx8 convention), SolidCraft at UI scale 1.8.
# GUI takes (A, B, C): SolidCraft fills the whole display. Take D: SolidCraft top pane + terminal strip (fx7alt layout).
# GUI positions in 1440x810 units (halved screenshots), as lab/fx7altlib.sh.
W2=2880 H2=1620
. /work/lab/common.sh
W2=2880 H2=1620 . /work/lab/l2common.sh
export DISPLAY=:99 LANG=C.UTF-8 LC_ALL=C.UTF-8
APP_H=${APP_H:-1620}; TERM_Y=${TERM_Y:-1134}; TERM_H=${TERM_H:-486}
mkdir -p /tmp/fx11
[ -f /tmp/fx11/T0 ] && T0=$(cat /tmp/fx11/T0)
O=${O:-$(cat /tmp/fx11/O 2>/dev/null)}
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
take() { O=/work/out/fx11/$1; mkdir -p "$O"; echo "$O" > /tmp/fx11/O; }
rec_start() {   # the whole display, 30 fps, cursor drawn
  : > "$O/cursor.jsonl"; : > "$O/events.jsonl"
  setsid ffmpeg -loglevel error -y -f x11grab -draw_mouse 1 -framerate 30 -video_size ${W}x${H} -i :99 \
    -c:v libx264 -preset ultrafast -crf 14 -pix_fmt yuv420p "$O/${1:-screen}.mp4" < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx11/rec.pid; date +%s.%N > /tmp/fx11/T0; T0=$(cat /tmp/fx11/T0); sleep 0.5
  setsid python3 /work/lab/cursorlog.py "$O/cursor.jsonl" "$T0" 30 < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx11/cur.pid
}
rec_stop() {
  touch "$O/cursor.jsonl.stop"; sleep 1; rm -f "$O/cursor.jsonl.stop"
  kill -INT "$(cat /tmp/fx11/rec.pid)"; for i in $(seq 1 30); do kill -0 "$(cat /tmp/fx11/rec.pid)" 2>/dev/null || break; sleep 0.5; done
  rm -f /tmp/fx11/T0; T0=
}
still() { g 1250 700 14; }                            # park the cursor in empty space (bottom right of the view)
envcheck() {    # rule P0 into out/fx11/env.txt
  local E=/work/out/fx11/env.txt
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
      -e env PS1='$ ' tmux -u new-session -s t -c /work/out/fx11 "bash --norc" > /dev/null 2>&1 &
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
  cp "/work/out/fx11/P/$1.sc" "$HOME/$1.sc"
  FX9_ALLOW=1 python3 /work/lab/fx9.py open "$HOME/$1.sc" > "$O/open-$1.txt" 2>&1; sleep 3
}
vol() { FX9_ALLOW=1 python3 /work/lab/fx9.py read "$O" "$1" > "$O/read-$1.txt" 2>&1; cat "$O/read-$1.txt"; }
# GUI positions (probe out/scratch/fx11p, 0.28.0 at UI scale 1.8, window 2880 x 1620, halved units)
MODEL_TAB="122 50"; INSPECT_TAB="382 50"; ORIGIN_ROW="31 264"; Z_ROW="82 358"; HOME_BTN="870 737"; ORBIT_BTN="707 737"
MODIFY_DD="433 130"; SPLIT_ITEM="388 493"; OFFSET_BTN="881 93"; CONSTRUCT_DD="880 130"; MIDPLANE_ITEM="908 510"
XY_ROW="85 381"; XZ_ROW="85 405"                     # with Origin expanded
BODY1_ROW="94 475"; BODY2_ROW="100 498"              # Bodies: the first and second body rows (Origin expanded)
S_OK="1388 397"; S_CANCEL="1322 397"; S_ISSUE="1252 396"; S_CANCEL_ERR="1322 445"; ISSUE_CLOSE="734 670"   # Split Body
OP_DIST="1355 377"; OP_OK="1388 426"                 # Offset Plane: Plane / Through point / Distance
MP_OK="1388 397"                                     # Midplane: First plane / Second plane
SECTION_BTN="296 85"; SEC_CANCEL="1322 458"
PROPS_CLOSE="860 487"                                # Properties: BODY (from the Browser's right-click menu)
TOP_FACE="837 226"                                   # the tower's top annulus, front, in the opening view
EYE_X=209
row_y() { echo "${1#* }"; }
okpos() { shot /tmp/fx11/ok.png; python3 /work/lab/fx11findok.py /tmp/fx11/ok.png; }    # "blue Y" or "none"
expand_origin() { ev "Browser: expand Origin"; g $ORIGIN_ROW 16; click; nap 1.2; }
origin_open() {  # expand Browser > Origin only if it is collapsed: with it expanded the Bodies folder icon sits at
  # (54, 451) halved; collapsed, that spot is the light grey view under a short Browser (A attempt 1: the fx10 Z-row test
  # read Sketch1's text on that row as "expanded")
  shot /tmp/fx11/tree.png
  local m; m=$(convert /tmp/fx11/tree.png -crop 40x30+88+888 -colorspace gray -format "%[fx:minima]" info:)
  if awk -v m="$m" 'BEGIN{exit !(m > 0.5)}'; then expand_origin; else ev "Browser: Origin already expanded"; fi
}
model_tab() { g $MODEL_TAB 16; click; nap 1.0; }
split_open() {   # Model > Modify > Split Body; the dialog with its defaults held 2 s
  model_tab
  ev "Split Body (Model tab > Modify > Bodies > Split Body)"
  g $MODIFY_DD 18; click; nap 1.5; g $SPLIT_ITEM 18; click; nap 2.0; still
  ev "Split Body dialog with its defaults: hold 2 s"; nap 2.0
}
pick_row() { ev "$1"; g $2 $3 16; click; nap 1.5; }   # pick_row LABEL X Y: a Browser row
split_state() {  # split_state LABEL: built (OK enabled) | refused (the red line shows, OK greyed) | nothing (neither)
  nap 1.0; local p l; p=$(okpos); l=$(python3 /work/lab/fx11findline.py /tmp/fx11/ok.png)
  if [ "${p%% *}" = blue ]; then ev "$1: OK enabled, preview shown (no live error): hold 3 s"; nap 3.0; echo built > /tmp/fx11/last
  elif [ "$l" != none ]; then ev "$1: live error under the fields, OK greyed: hold 4 s"; nap 4.0; echo refused > /tmp/fx11/last
  else ev "$1: OK greyed and no error line (a pick missing?)"; echo nothing > /tmp/fx11/last; fi
}
split_ok() { ev "OK"; g $S_OK 14; click; nap 3.5; still; }
split_cancel() {   # Cancel (its place moves down when the error line shows)
  ev "Cancel"; if [ "$(cat /tmp/fx11/last)" = refused ]; then g $S_CANCEL_ERR 14; else g $S_CANCEL 14; fi; click; nap 2.0; still
}
offset_plane() { # offset_plane DIST SHOT: Model > Construct > Offset Plane, Plane = XY, Distance DIST mm, OK
  model_tab
  ev "Offset Plane (Model tab > Construct): the dialog with its defaults: hold 2 s"
  g $OFFSET_BTN 18; click; nap 2.0; still; nap 2.0
  [ -n "${2:-}" ] && cp_shot "$2"
  pick_row "Plane: XY in Browser > Origin" $XY_ROW
  ev "Distance: $1 mm (typed), Tab"
  g $OP_DIST 16; click; xdotool key ctrl+a; nap 0.3; typed "$1 mm" 140; nap 0.5; xdotool key Tab; nap 2.0; still
  ev "the plane preview at $1: hold 3 s"; nap 3.0
  [ -n "${2:-}" ] && cp_shot "$2-preview"
  ev "OK"; g $OP_OK 14; click; nap 2.5; still
}
home_view() { ev "Home view"; g $HOME_BTN 16; click; nap 2.0; still; }
orbit() {        # a slow orbit (Orbit button, a short drag), then the Home view
  ev "slow orbit (Orbit button, drag)"; g $ORBIT_BTN 16; click; nap 0.8
  g 1000 450 14; xdotool mousedown 1; g 1060 445 90; nap 0.3; g 1000 450 90; xdotool mouseup 1; nap 0.8
  xdotool key Escape; nap 0.5; home_view
}
props() {        # props ROW_X ROW_Y SHOT: the Browser row's right-click > Properties, held 4 s, then Close
  ev "right-click the body row > Properties: hold 4 s"
  g "$1" "$2" 16; nap 0.8; xdotool click 3; nap 1.5
  g $(( $1 + 59 )) 400 14; click; nap 2.0; still; nap 4.0
  cp_shot "$3"; g $PROPS_CLOSE 14; click; nap 1.2; still
}
eye() { g $EYE_X "$1" 14; click; nap 1.0; still; }   # eye ROW_Y: the Browser row's show/hide toggle
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
