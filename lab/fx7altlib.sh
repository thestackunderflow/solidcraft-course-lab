# fx7alt helpers (LAB-fx7alt), sourced inside sc5-l5:0.28.0 by every lab/fx7altX.sh take (one container per take, a
# fresh home each) and by the probe session. Display 2880x1620 (16:9; the fx6/fx8 convention), SolidCraft at UI scale
# 1.8 as the top pane (2880 x 1134, about 70%), the terminal running noai.py a strip below (2880 x 486).
# GUI positions in 1440x810 units (halved screenshots), as lab/fx8lib.sh.
W2=2880 H2=1620
. /work/lab/common.sh
W2=2880 H2=1620 . /work/lab/l2common.sh
export DISPLAY=:99 LANG=C.UTF-8 LC_ALL=C.UTF-8
APP_H=1134; TERM_Y=1134; TERM_H=486
mkdir -p /tmp/fx7
[ -f /tmp/fx7/T0 ] && T0=$(cat /tmp/fx7/T0)
O=${O:-$(cat /tmp/fx7/O 2>/dev/null)}
g() { glide "$(awk -v v="$1" 'BEGIN{printf "%d", v*4/3}')" "$(awk -v v="$2" 'BEGIN{printf "%d", v*4/3}')" "${3:-20}"; }
click() { nap 1.0; xdotool click 1; }                 # a 1 s pause before each click
typed() { xdotool type --delay "${2:-80}" "$1"; }
cp_shot() { shot "$O/$1.png"; }
ev() {          # LAB events.txt line (wall clock) + events.jsonl (seconds since T0, for footage.py)
  printf '%s  %s\n' "$(date -u +%H:%M:%S.%1N)" "$1" >> "$O/events.txt"
  [ -n "${T0:-}" ] && mark "$O/events.jsonl" "$(printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g')"
  echo "ev: $1"
}
take() { O=/work/out/fx7alt/$1; mkdir -p "$O"; echo "$O" > /tmp/fx7/O; }
rec_start() {   # the whole display, 30 fps, cursor drawn
  : > "$O/cursor.jsonl"; : > "$O/events.jsonl"
  setsid ffmpeg -loglevel error -y -f x11grab -draw_mouse 1 -framerate 30 -video_size ${W}x${H} -i :99 \
    -c:v libx264 -preset ultrafast -crf 14 -pix_fmt yuv420p "$O/screen.mp4" < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx7/rec.pid; date +%s.%N > /tmp/fx7/T0; T0=$(cat /tmp/fx7/T0); sleep 0.5
  setsid python3 /work/lab/cursorlog.py "$O/cursor.jsonl" "$T0" 30 < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx7/cur.pid
}
rec_stop() {
  touch "$O/cursor.jsonl.stop"; sleep 1; rm -f "$O/cursor.jsonl.stop"
  kill -INT "$(cat /tmp/fx7/rec.pid)"; for i in $(seq 1 30); do kill -0 "$(cat /tmp/fx7/rec.pid)" 2>/dev/null || break; sleep 0.5; done
  rm -f /tmp/fx7/T0
}
still() { g 1100 420 14; }                            # park the cursor in empty space
# setup: a fresh home's SolidCraft (lesson 5), the MCP entry (lesson 7: `solidcraft-cli mcp setup`), the window as the
# top pane, a new design, and the terminal strip (xterm + tmux, white) below; env.txt checks (rule P0)
setup() {
  mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
  solidcraft-cli mcp setup > "$O/setup.txt" 2>&1
  start_display
  openbox > /dev/null 2>&1 &
  sleep 1
  start_app "$O/app.log" /opt/solidcraft/bin/solidcraft
  sleep 10
  python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
  fill_window 0 0 $W $APP_H; sleep 2
  shot "$O/start-page.png"
  g 398 206 6; xdotool click 1; sleep 3                          # start page: New design (fx8 position)
  printf 'set -g status off\nset -g history-limit 5000\n' > "$HOME/.tmux.conf"
  xterm -u8 -geometry 160x12+0+$TERM_Y -fa "DejaVu Sans Mono" -fs 22 -bg white -fg black -T "Terminal" \
    -e env PS1='$ ' tmux -u new-session -s t -c /work/out/fx7alt "bash --norc" > /dev/null 2>&1 &
  sleep 3
  local w; w=$(xdotool search --name "^Terminal$" | head -1)
  xdotool windowsize --sync "$w" $W $TERM_H; xdotool windowmove "$w" 0 $TERM_Y
  tmux send-keys -t t "export PS1='\$ '; clear" Enter; sleep 1
  fill_window 0 0 $W $APP_H; sleep 1
  still
}
# tt CMD: type a command into the terminal strip at a person's pace, Enter, wait for the prompt to come back
tt() {
  local cmd=$1 i
  for ((i = 0; i < ${#cmd}; i++)); do tmux send-keys -t t -l "${cmd:i:1}"; sleep 0.08; done
  nap 0.8; tmux send-keys -t t Enter
  for i in $(seq 1 480); do [ "$(tmux capture-pane -p -t t | sed '/^[[:space:]]*$/d' | tail -1)" = '$' ] && break; sleep 0.25; done
}
pane() { tmux capture-pane -p -J -S -500 -t t > "$O/pane.txt"; }
# GUI positions (probe out/scratch/fx7p, 0.28.0 at UI scale 1.8, window 2880 x 1134, home view)
FILLET_BTN="353 90"; EDGES_ROW="1349 259"; RADIUS_BOX="1349 289"; OK_BTN="1388 522"; CANCEL_BTN="1322 522"
TOP_EDGE_MID="905 194"     # the top edge y=20, z=20 (F1:+y|F1:+z), whose middle is [10, 20, 20]
HOME_BTN="870 494"
orbit() {       # orbit SECONDS: a slow middle-button swing right and back, then the home view
  local n; n=$(awk -v s="$1" 'BEGIN{printf "%d", s/0.06}')
  g 1000 330 10; xdotool mousedown 2
  for i in $(seq 1 $((n / 2))); do xdotool mousemove_relative -- 6 0; sleep 0.05; done
  for i in $(seq 1 $((n / 2))); do xdotool mousemove_relative -- -6 0; sleep 0.05; done
  xdotool mouseup 2; nap 0.5; g $HOME_BTN 14; click; nap 1.0; still
}
vol() { python3 /work/lab/fx7alt.py read "$O" "$1" > "$O/read-$1.txt" 2>&1; cat "$O/read-$1.txt"; }
