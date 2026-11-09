# fx9 helpers (LAB-fx9), sourced inside sc5-l5:0.28.0 by every lab/fx9X.sh take (one container per take, a fresh home
# each) and by the probe session. Display 2880x1620 (16:9, the fx6-fx8 convention), SolidCraft at UI scale 1.8.
# GUI takes (A, B, C): SolidCraft fills the whole display. Take D: SolidCraft top pane + terminal strip (fx7alt layout).
# GUI positions in 1440x810 units (halved screenshots), as lab/fx7altlib.sh.
W2=2880 H2=1620
. /work/lab/common.sh
W2=2880 H2=1620 . /work/lab/l2common.sh
export DISPLAY=:99 LANG=C.UTF-8 LC_ALL=C.UTF-8
APP_H=${APP_H:-1620}; TERM_Y=${TERM_Y:-1134}; TERM_H=${TERM_H:-486}
mkdir -p /tmp/fx9
[ -f /tmp/fx9/T0 ] && T0=$(cat /tmp/fx9/T0)
O=${O:-$(cat /tmp/fx9/O 2>/dev/null)}
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
take() { O=/work/out/fx9/$1; mkdir -p "$O"; echo "$O" > /tmp/fx9/O; }
rec_start() {   # the whole display, 30 fps, cursor drawn
  : > "$O/cursor.jsonl"; : > "$O/events.jsonl"
  setsid ffmpeg -loglevel error -y -f x11grab -draw_mouse 1 -framerate 30 -video_size ${W}x${H} -i :99 \
    -c:v libx264 -preset ultrafast -crf 14 -pix_fmt yuv420p "$O/${1:-screen}.mp4" < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx9/rec.pid; date +%s.%N > /tmp/fx9/T0; T0=$(cat /tmp/fx9/T0); sleep 0.5
  setsid python3 /work/lab/cursorlog.py "$O/cursor.jsonl" "$T0" 30 < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx9/cur.pid
}
rec_stop() {
  touch "$O/cursor.jsonl.stop"; sleep 1; rm -f "$O/cursor.jsonl.stop"
  kill -INT "$(cat /tmp/fx9/rec.pid)"; for i in $(seq 1 30); do kill -0 "$(cat /tmp/fx9/rec.pid)" 2>/dev/null || break; sleep 0.5; done
  rm -f /tmp/fx9/T0; T0=
}
still() { g 1250 700 14; }                            # park the cursor in empty space (bottom right of the view)
envcheck() {    # rule P0 into out/fx9/env.txt
  local E=/work/out/fx9/env.txt
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
      -e env PS1='$ ' tmux -u new-session -s t -c /work/out/fx9 "bash --norc" > /dev/null 2>&1 &
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
# the nut (take P's file) opened into the window, off camera: copied to ~ then the plug's `open`
open_nut() {    # open_nut [nut|nut-675]
  cp "/work/out/fx9/P/${1:-nut}.sc" "$HOME/${1:-nut}.sc"
  FX9_ALLOW=1 python3 /work/lab/fx9.py open "$HOME/${1:-nut}.sc" > "$O/open-${1:-nut}.txt" 2>&1; sleep 3
}
vol() { FX9_ALLOW=1 python3 /work/lab/fx9.py read "$O" "$1" > "$O/read-$1.txt" 2>&1; cat "$O/read-$1.txt"; }
# GUI positions (probe out/scratch/fx9p, 0.28.0 at UI scale 1.8, window 2880 x 1620, home view, halved units)
CREATE_MENU="245 130"; THREAD_ITEM="220 483"; HOLE_WALL="837 300"; HOLE_TL="284 786"
T_MODELED="1215 408"; T_AUTO="1215 438"; T_SIZE="1361 468"; T_SIZE8="1334 665"; T_SIZE10="1334 689"
T_ISSUE="1252 649"; ISSUE_CLOSE="734 670"; T_OK_ERR="1388 698"; T_CANCEL_ERR="1322 698"; T_CANCEL="1322 607"
H_DIAM="1361 601"; H_OK="1388 682"; H_CANCEL="1322 682"; H_TAP="1355 528"; H_TAPPED="1322 581"
H_TSIZE="1364 587"; H_TM8="1328 540"; H_OK_TAPPED="1388 781"
INSPECT_TAB="382 50"; SECTION_BTN="296 90"; ORIGIN_ROW="31 264"; XZ_ROW="85 404"; SECTION_OK="1388 458"
PROPS_BTN="229 90"; MODEL_TAB="122 50"; HOME_BTN="870 737"
okpos() { shot /tmp/fx9/ok.png; python3 /work/lab/fx9findok.py /tmp/fx9/ok.png; }    # "blue Y" or "none"
thread_open() { # Model > Create > Thread, pick the hole wall; hold 4 s on the pre-filled dialog
  ev "Thread: Model tab > Create menu > Thread"
  g $CREATE_MENU 20; click; nap 1.2
  g $THREAD_ITEM 16; click; nap 1.6
  ev "pick the hole's wall"
  g $HOLE_WALL 20; click; nap 2.0; still
  ev "dialog after the pick: hold 4 s"; nap 4.0
}
thread_m8() {   # untick Automatic size, Size 8 mm FIRST, then Modeled (never Modeled first)
  ev "untick Automatic size"
  g $T_AUTO 16; click; nap 1.0
  ev "Size: 8 mm"
  g $T_SIZE 12; click; nap 1.0; g $T_SIZE8 10; click; nap 1.5; still
  ev "Size 8 mm set (Designation shown): hold 2 s"; nap 2.0
  cp_shot ${1:-size8}
  ev "tick Modeled"
  g $T_MODELED 16; click; nap 3.0; still
}
thread_ok() {   # thread_ok LABEL: OK if enabled, else click the greyed OK; event built | refused; screenshots
  local p y; p=$(okpos)
  if [ "${p%% *}" = blue ]; then
    y=${p#blue }; ev "$1: OK enabled (no live error): OK"
    g 1388 "$y" 14; click; nap 4.0; still; echo built > /tmp/fx9/last
  else
    ev "$1: live error under the fields, OK greyed: hold 4 s"; nap 4.0; echo refused > /tmp/fx9/last
  fi
}
hole_edit() {   # hole_edit D: double-click the Hole in the timeline, diameter D, hold 4 s, OK
  ev "double-click Hole1 in the timeline"
  g $HOLE_TL 20; dclick; nap 2.0
  ev "diameter: $1"
  g $H_DIAM 16; click; xdotool key ctrl+a; nap 0.3; typed "$1" 160; nap 0.6; xdotool key Tab; nap 1.5; still
  ev "diameter $1 in the box: hold 4 s"; nap 4.0
  cp_shot ${2:-hole$1}
  ev "OK"
  g $H_OK 14; click; nap 3.0; still
}
T_CLOSE="1413 272"     # the Thread dialog's title-bar X: same place at every dialog height (Cancel moves with the error line)
