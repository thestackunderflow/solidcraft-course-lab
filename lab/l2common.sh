# Lesson 2 helpers (sourced after common.sh inside sc2-l2:0.25.0): a 2880x1800 display, the window filled at UI scale
# 1.8 (the same layout as a 1600x1000 window, sharp when the video zooms in), 30 fps recording with a cursor log,
# events with seconds from the recording's start (so footage can be cut by event), and a smooth, eased mouse (glide).
# Scripts give positions in 1920x1200 units (the probe's layout at UI scale 1.2); glide/rel multiply them by K.
W=${W2:-2880}; H=${H2:-1800}
SCALE=${SCALE:-1.8}
K=$(awk -v w="$W" 'BEGIN{print w/1920}')
kx() { awk -v v="$1" -v k="$K" 'BEGIN{printf "%d", v*k + (v<0?-0.5:0.5)}'; }
PACE=${PACE:-1.0}          # every pause is multiplied by this (re-recording to fit the narration's timing)

nap() { sleep "$(awk -v s="$1" -v p="$PACE" 'BEGIN{print s*p}')"; }

fill_window() {   # fill_window X Y WIDTH HEIGHT
  local w; w=$(xdotool search --name SolidCraft | head -1)
  xdotool windowsize --sync "$w" "$3" "$4"; xdotool windowmove "$w" "$1" "$2"; xdotool windowfocus --sync "$w"
}

focus_app() { xdotool windowfocus --sync "$(xdotool search --name SolidCraft | head -1)"; }

record30() {      # record30 OUT.mp4 CURSOR.jsonl [nomouse]: the whole display, 30 fps, near-lossless; T0 = first frame
  local dm=1; [ "${3:-}" = nomouse ] && dm=0     # the Claude run: nobody uses the mouse, so none is drawn
  ffmpeg -loglevel error -y -f x11grab -draw_mouse $dm -framerate 30 -video_size ${W}x${H} -i :99 \
    -c:v libx264 -preset ultrafast -crf 14 -pix_fmt yuv420p "$1" &
  REC=$!; T0=$(date +%s.%N); sleep 0.5
  python3 /work/lab/cursorlog.py "$2" "$T0" 30 & CUR=$!
  CURSOR_LOG=$2
}

stop_record30() {
  touch "$CURSOR_LOG.stop"; wait "$CUR" 2>/dev/null; rm -f "$CURSOR_LOG.stop"
  kill -INT "$REC" && wait "$REC" 2>/dev/null; REC=
}

mark() {          # mark FILE what: one event, seconds since the recording started
  printf '{"t": %s, "event": "%s"}\n' "$(awk -v a="$(date +%s.%N)" -v b="$T0" 'BEGIN{printf "%.3f", a-b}')" "$2" >> "$1"
}

glide() {         # glide X Y [STEPS]: move the mouse along a straight line, eased in and out, about 30 ms a step
  eval "$(xdotool getmouselocation --shell)"
  local tx ty n=${3:-18} i
  tx=$(kx "$1"); ty=$(kx "$2")
  for i in $(seq 1 "$n"); do
    read -r px py < <(awk -v i="$i" -v n="$n" -v x="$X" -v y="$Y" -v tx="$tx" -v ty="$ty"       'BEGIN{e=(1-cos(3.14159265*i/n))/2; printf "%d %d", x+(tx-x)*e, y+(ty-y)*e}')
    xdotool mousemove "$px" "$py"; sleep 0.03
  done
}

rel() { xdotool mousemove_relative -- "$(kx "$1")" "$(kx "$2")"; }   # rel DX DY in 1920 units

wiggle() { eval "$(xdotool getmouselocation --shell)"; xdotool mousemove_relative 2 0; sleep 0.2; xdotool mousemove "$X" "$Y"; sleep 0.4; }
