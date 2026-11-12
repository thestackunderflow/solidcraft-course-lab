# fx10 helpers (LAB-fx10; a copy of fx9lib.sh), sourced inside sc5-l5:0.28.0 by every lab/fx10X.sh take (one container per take, a fresh home
# each) and by the probe session. Display 2880x1620 (16:9, the fx6-fx8 convention), SolidCraft at UI scale 1.8.
# GUI takes (A, B, C): SolidCraft fills the whole display. Take D: SolidCraft top pane + terminal strip (fx7alt layout).
# GUI positions in 1440x810 units (halved screenshots), as lab/fx7altlib.sh.
W2=2880 H2=1620
. /work/lab/common.sh
W2=2880 H2=1620 . /work/lab/l2common.sh
export DISPLAY=:99 LANG=C.UTF-8 LC_ALL=C.UTF-8
APP_H=${APP_H:-1620}; TERM_Y=${TERM_Y:-1134}; TERM_H=${TERM_H:-486}
mkdir -p /tmp/fx10
[ -f /tmp/fx10/T0 ] && T0=$(cat /tmp/fx10/T0)
O=${O:-$(cat /tmp/fx10/O 2>/dev/null)}
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
take() { O=/work/out/fx10/$1; mkdir -p "$O"; echo "$O" > /tmp/fx10/O; }
rec_start() {   # the whole display, 30 fps, cursor drawn
  : > "$O/cursor.jsonl"; : > "$O/events.jsonl"
  setsid ffmpeg -loglevel error -y -f x11grab -draw_mouse 1 -framerate 30 -video_size ${W}x${H} -i :99 \
    -c:v libx264 -preset ultrafast -crf 14 -pix_fmt yuv420p "$O/${1:-screen}.mp4" < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx10/rec.pid; date +%s.%N > /tmp/fx10/T0; T0=$(cat /tmp/fx10/T0); sleep 0.5
  setsid python3 /work/lab/cursorlog.py "$O/cursor.jsonl" "$T0" 30 < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx10/cur.pid
}
rec_stop() {
  touch "$O/cursor.jsonl.stop"; sleep 1; rm -f "$O/cursor.jsonl.stop"
  kill -INT "$(cat /tmp/fx10/rec.pid)"; for i in $(seq 1 30); do kill -0 "$(cat /tmp/fx10/rec.pid)" 2>/dev/null || break; sleep 0.5; done
  rm -f /tmp/fx10/T0; T0=
}
still() { g 1250 700 14; }                            # park the cursor in empty space (bottom right of the view)
envcheck() {    # rule P0 into out/fx10/env.txt
  local E=/work/out/fx10/env.txt
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
      -e env PS1='$ ' tmux -u new-session -s t -c /work/out/fx10 "bash --norc" > /dev/null 2>&1 &
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
# the knob (take P's file) opened into the window, off camera: copied to ~ then the plug's `open` (fx9 deviation 1)
open_knob() {   # open_knob [knob-full|knob-half]
  cp "/work/out/fx10/P/${1:-knob-full}.sc" "$HOME/${1:-knob-full}.sc"
  FX9_ALLOW=1 python3 /work/lab/fx9.py open "$HOME/${1:-knob-full}.sc" > "$O/open-${1:-knob-full}.txt" 2>&1; sleep 3
}
vol() { FX9_ALLOW=1 python3 /work/lab/fx9.py read "$O" "$1" > "$O/read-$1.txt" 2>&1; cat "$O/read-$1.txt"; }
# GUI positions (probe out/scratch/fx10p, 0.28.0 at UI scale 1.8, window 2880 x 1620, halved units)
MODEL_TAB="122 50"; INSPECT_TAB="382 50"; REVOLVE_BTN="245 85"; ORIGIN_ROW="31 264"; Z_ROW="82 358"
SKETCH1_ROW="100 475"                  # with Origin expanded
R_PROFILE="1349 318"; R_PROFILE_X="1410 318"; R_AXIS="1349 347"; R_ANGLE="1349 437"
R_OK="1388 515"; R_CANCEL="1322 515"; R_ISSUE="1252 530"; R_CANCEL_ERR="1322 579"; ISSUE_CLOSE="734 670"
LINE_TOOL="118 85"; FINISH_BTN="1127 92"; HOME_BTN="870 737"
MEASURE_BTN="120 85"; PROPS_BTN="229 85"; PROPS_CLOSE="860 649"; MEASURE_CLOSE="1396 456"; MEASURE_X="1410 318"
# the knob's sketch view (Sketch1 edited): sketch (x, y) -> screen (720 + 18 x, 214 - 18 y); the XZ sketch's y is world -Z
sk() { awk -v x="$1" -v y="$2" 'BEGIN{printf "%d %d", 720 + 18*x, 214 - 18*y}'; }
okpos() { shot /tmp/fx10/ok.png; python3 /work/lab/fx10findok.py /tmp/fx10/ok.png; }    # "blue Y" or "none"
expand_origin() { ev "Browser: expand Origin"; g $ORIGIN_ROW 16; click; nap 1.2; }
revolve_open() {   # Model > Revolve; hold 2 s on the dialog with its defaults
  ev "Revolve (Model tab, Create group)"
  g $REVOLVE_BTN 20; click; nap 2.0; still
  ev "Revolve dialog with its defaults: hold 2 s"; nap 2.0
}
pick_z() { ev "Axis: Z in Browser > Origin"; g $Z_ROW 16; click; nap 2.5; still; }
revolve_state() {  # revolve_state LABEL: built (OK enabled) | refused (live line, OK greyed) -> /tmp/fx10/last
  local p; p=$(okpos)
  if [ "${p%% *}" = blue ]; then ev "$1: OK enabled, preview shown (no live error)"; echo built > /tmp/fx10/last
  else ev "$1: live error under the fields, OK greyed: hold 4 s"; nap 4.0; echo refused > /tmp/fx10/last; fi
}
revolve_ok() { local p y; p=$(okpos); y=${p#blue }; ev "OK"; g 1388 "$y" 14; click; nap 3.5; still; }
home_view() { ev "Home view"; g $HOME_BTN 16; click; nap 2.0; still; }
props() {        # props SHOT: Inspect > Properties held 4 s, then Close
  g $INSPECT_TAB 16; click; nap 1.0
  ev "Inspect > Properties: hold 4 s"; g $PROPS_BTN 16; click; nap 2.0; still; nap 4.0
  cp_shot "$1"; g $PROPS_CLOSE 14; click; nap 1.2; still
}
measure_edge() { # measure_edge X Y SHOT: Inspect > Measure, the edge, held 4 s, then Close
  g $INSPECT_TAB 16; click; nap 1.0
  ev "Inspect > Measure: the edge at $1 $2: hold 4 s"; g $MEASURE_BTN 16; click; nap 1.5
  g "$1" "$2" 18; click; nap 2.0; still; nap 4.0
  cp_shot "$3"; g $MEASURE_CLOSE 14; click; nap 1.2; still
}
origin_open() {  # expand Browser > Origin only if its Z row is not showing (the tree state carries across tabs)
  shot /tmp/fx10/tree.png
  local m; m=$(convert /tmp/fx10/tree.png -crop 40x24+112+704 -colorspace gray -format "%[fx:mean]" info:)
  if awk -v m="$m" 'BEGIN{exit !(m > 0.97)}'; then expand_origin; else ev "Browser: Origin already expanded"; fi
}
