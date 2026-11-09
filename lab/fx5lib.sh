# fx5 helpers (sourced inside sc5-fx5:0.28.0, by lab/fx5session.sh and by every `docker exec` step into the session).
# The session keeps the display, the session bus and SolidCraft alive; each step is one docker exec that sources this
# file, so the timeline (T0 of the recording) and the bus address live in /tmp/fx5 files, not in a shell.
# Positions are in 1440x900 units (as lab/l6hand.sh and lab/fx2E.sh), SolidCraft UI scale 1.8, GDK scale 2.
. /work/lab/common.sh
. /work/lab/l2common.sh
export DISPLAY=:99 LIBGL_ALWAYS_SOFTWARE=1 GDK_SCALE=2
unset XDG_DATA_HOME XDG_CACHE_HOME
mkdir -p /tmp/fx5
[ -f /tmp/fx5/bus ] && . /tmp/fx5/bus
[ -f /tmp/fx5/T0 ] && T0=$(cat /tmp/fx5/T0)
O=${O:-$(cat /tmp/fx5/O 2>/dev/null)}
SLICED=/root/.cache/solidcraft/slicer
c43() { awk -v v="$1" 'BEGIN{printf "%d", v*4/3}'; }
g() { glide "$(c43 "$1")" "$(c43 "$2")" "${3:-20}"; }
click() { xdotool click 1; }
typed() { xdotool type --delay "${2:-150}" "$1"; }
# ev NAME: LAB-fx5 events.txt line (wall clock) + events.jsonl (seconds since T0, for footage.py)
ev() {
  printf '%s  %s\n' "$(date -u +%H:%M:%S.%1N)" "$1" >> "$O/events.txt"
  [ -n "${T0:-}" ] && mark "$O/events.jsonl" "$(printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g')"   # JSON-escaped
  echo "ev: $1"
}
rec_start() {   # the whole display, 30 fps, cursor drawn; survives the docker exec that started it
  : > "$O/cursor.jsonl"
  setsid ffmpeg -loglevel error -y -f x11grab -draw_mouse 1 -framerate 30 -video_size ${W}x${H} -i :99 \
    -c:v libx264 -preset ultrafast -crf 14 -pix_fmt yuv420p "$O/screen.mp4" < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx5/rec.pid; date +%s.%N > /tmp/fx5/T0; T0=$(cat /tmp/fx5/T0); sleep 0.5
  setsid python3 /work/lab/cursorlog.py "$O/cursor.jsonl" "$T0" 30 < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx5/cur.pid
  : > "$O/events.jsonl"
}
rec_stop() {
  touch "$O/cursor.jsonl.stop"; sleep 1; rm -f "$O/cursor.jsonl.stop"
  kill -INT "$(cat /tmp/fx5/rec.pid)"; for i in $(seq 1 30); do kill -0 "$(cat /tmp/fx5/rec.pid)" 2>/dev/null || break; sleep 0.5; done
  rm -f /tmp/fx5/T0
}
sc_win() { xdotool search --name "SolidCraft" 2>/dev/null | head -1; }
sc_front() { xdotool windowactivate --sync "$(sc_win)" 2>/dev/null; sleep 0.8; }
prusa_win() { xdotool search --onlyvisible --name "PrusaSlicer-2.9" 2>/dev/null | head -1; }
orca_wins() { xdotool search --onlyvisible --name "OrcaSlicer" 2>/dev/null; }
max_win() { wmctrl -i -r "$1" -b add,maximized_vert,maximized_horz; sleep 2; }
body_menu() { g 94 311 22; nap 1.0; xdotool click 3; nap 1.4; }
send_open() { body_menu; g 162 513 12; nap 0.8; click; nap 2.0; }   # right-click Body1 > Send to Slicer
send_click() { g 1388 486 16; nap 0.6; click; }                      # the Send window's Send button
depth() {      # depth VALUE: Model tab, Parameters, hook_depth's value, Enter, OK (lab/l6hand.sh)
  g 122 50 18; nap 0.5; click; nap 1.0
  g 760 90 22; nap 0.8; click; nap 2.0
  g 1123 583 22; nap 1.0; click; nap 0.5
  xdotool key ctrl+a; nap 0.6
  typed "$1" 300; nap 0.8
  xdotool key Return; nap 3.0
  shot "$O/params-$1.png"
  g 1388 745 22; nap 0.6; click; nap 1.4
}
small() { import -window root -resize 1200x750 "/work/out/scratch/fx5-$1.png"; }   # a look for the operator only
winlist() { for i in $(xdotool search --onlyvisible --name "" 2>/dev/null); do n=$(xdotool getwindowname "$i" 2>/dev/null); [ -n "$n" ] && echo "$i  $n"; done; }
