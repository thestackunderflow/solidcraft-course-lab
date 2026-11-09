# fx6 helpers (sourced inside sc5-l5:0.28.0 by lab/fx6session.sh and by every `docker exec` step into the session).
# The session keeps the display and SolidCraft alive; each step is one docker exec that sources this file, so the
# recording's T0 and the take folder live in /tmp/fx6 files, not in a shell (the fx5 pattern, lab/fx5lib.sh).
# Display 2880x1620 (16:9), SolidCraft UI scale 1.8 filling it; positions in 1440x810 units (halved screenshots).
W2=2880 H2=1620
. /work/lab/common.sh
W2=2880 H2=1620 . /work/lab/l2common.sh
export DISPLAY=:99
mkdir -p /tmp/fx6
[ -f /tmp/fx6/T0 ] && T0=$(cat /tmp/fx6/T0)
O=${O:-$(cat /tmp/fx6/O 2>/dev/null)}
g() { glide "$(awk -v v="$1" 'BEGIN{printf "%d", v*4/3}')" "$(awk -v v="$2" 'BEGIN{printf "%d", v*4/3}')" "${3:-20}"; }
click() { nap 1.0; xdotool click 1; }                 # LAB-fx6 section 2: a 1 s pause before each click
typed() { xdotool type --delay "${2:-80}" "$1"; }
cp_shot() { shot "$O/$1.png"; }
# ev NAME: LAB-fx6 events.txt line (wall clock) + events.jsonl (seconds since T0, for footage.py)
ev() {
  printf '%s  %s\n' "$(date -u +%H:%M:%S.%1N)" "$1" >> "$O/events.txt"
  [ -n "${T0:-}" ] && mark "$O/events.jsonl" "$(printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g')"
  echo "ev: $1"
}
take() {        # take NAME: the folder for the next recording
  O=/work/out/fx6/$1; mkdir -p "$O"; echo "$O" > /tmp/fx6/O
}
rec_start() {   # the whole display, 30 fps, cursor drawn; survives the docker exec that started it
  : > "$O/cursor.jsonl"; : > "$O/events.jsonl"
  setsid ffmpeg -loglevel error -y -f x11grab -draw_mouse 1 -framerate 30 -video_size ${W}x${H} -i :99 \
    -c:v libx264 -preset ultrafast -crf 14 -pix_fmt yuv420p "$O/screen.mp4" < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx6/rec.pid; date +%s.%N > /tmp/fx6/T0; T0=$(cat /tmp/fx6/T0); sleep 0.5
  setsid python3 /work/lab/cursorlog.py "$O/cursor.jsonl" "$T0" 30 < /dev/null > /dev/null 2>&1 &
  echo $! > /tmp/fx6/cur.pid
}
rec_stop() {
  touch "$O/cursor.jsonl.stop"; sleep 1; rm -f "$O/cursor.jsonl.stop"
  kill -INT "$(cat /tmp/fx6/rec.pid)"; for i in $(seq 1 30); do kill -0 "$(cat /tmp/fx6/rec.pid)" 2>/dev/null || break; sleep 0.5; done
  rm -f /tmp/fx6/T0
}
sc_win() { xdotool search --name "SolidCraft" 2>/dev/null | head -1; }
read_now() {    # read_now TAG: read-only plug read (measure + body_topology), one line into events
  python3 /work/lab/fx6hook.py read "$O" "$1" > "$O/read-$1.txt" 2>&1
  cat "$O/read-$1.txt"
}
still() { g 1100 450 14; }                            # park the cursor in empty space (the view stays still)
# Fillet dialog (probe out/scratch/fx6p, 0.28.0 at UI scale 1.8)
FILLET_BTN="353 90"; LIP_EDGE="910 609"; RADIUS_BOX="1349 347"; OK_BTN="1388 581"; CANCEL_BTN="1322 581"
PARAMS_BTN="760 90"; THICK_BOX="1124 551"; PARAMS_OK="1388 745"
radius() {      # radius R: replace the Radius box's text, Tab (preview), hold 4 s on the box
  g $RADIUS_BOX 18; click; xdotool key ctrl+a; nap 0.3; typed "$1" 160; nap 0.6; xdotool key Tab; nap 4.0
}
