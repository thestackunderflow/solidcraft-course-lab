#!/bin/bash
# fx5 take B (LAB-fx5 section 3), run inside the fx5 session (lab/fx5session.sh B):
#   docker exec fx5-B bash /work/lab/fx5B.sh film      the filmed part: steps 1-7 (two sends, two listings)
#   docker exec fx5-B bash /work/lab/fx5B.sh bodies    steps 8-9 (no footage): two bodies, both together, restart
# The listing typed on screen is the plain `ls -l ~/.cache/solidcraft/slicer` in an xterm (large font) at the bottom
# right; the same listing (and the full-iso one) is written to files by this script, as the lab file says.
set -u
. /work/lab/fx5lib.sh
STEP=${1:?film or bodies}
term_type() { xdotool windowactivate --sync "$(xdotool search --name fx5term | head -1)"; sleep 0.6; xdotool type --delay 70 "$1"; sleep 0.5; xdotool key Return; }
if [ "$STEP" = film ]; then
  setsid xterm -T fx5term -geometry 46x9+1500+1230 -fa 'DejaVu Sans Mono' -fs 22 -bg white -fg black \
    -e bash --norc -c 'cd ~; PS1="$ "; export PS1; exec bash --norc -i' < /dev/null > /dev/null 2>&1 &
  sleep 3
  rec_start
  ev "recording started: SolidCraft with the saved hook, a terminal bottom right"
  ls -l "$SLICED" |& tee "$O/ls-0.txt" > /dev/null
  term_type "ls -l ~/.cache/solidcraft/slicer"; nap 4
  ev "ls 0: listed (no folder yet)"
  sc_front; nap 1.5
  ev "send 1: right-click Body1"; send_open; nap 1.5
  ev "send 1: Send clicked"; send_click
  for i in $(seq 1 120); do [ -n "$(prusa_win)" ] && break; sleep 0.5; done; sleep 6
  ev "send 1: slicer window up"
  max_win "$(prusa_win)"; nap 3
  term_type "ls -l ~/.cache/solidcraft/slicer"; nap 1
  ls -l "$SLICED" | tee "$O/ls-1.txt" > /dev/null
  ev "ls 1: listed"; nap 4
  shot "$O/ls-1.png"
  ls -l --time-style=full-iso "$SLICED" > "$O/ls-1-full.txt"
  sc_front; nap 1.5
  ev "hook_depth: 40 open Parameters"; depth 40
  ev "hook_depth: 40 typed"
  ev "save: click the Save icon"; g 184 16 18; nap 0.6; click; nap 2.5
  shot "$O/hook-40.png"
  # wait until the minute in ls -l changes (at least 61 s after send 1's listing)
  t1=$(stat -c %Y "$SLICED"/*.3mf); while [ $(( $(date +%s) - t1 )) -lt 62 ]; do sleep 1; done
  ev "send 2: right-click Body1"; send_open; nap 1.5
  ev "send 2: Send clicked"; send_click; sleep 8
  term_type "ls -l ~/.cache/solidcraft/slicer"; nap 1
  ls -l "$SLICED" | tee "$O/ls-2.txt" > /dev/null
  ev "ls 2: listed"; nap 5
  shot "$O/ls-2.png"
  ls -l --time-style=full-iso "$SLICED" > "$O/ls-2-full.txt"
  sha256sum "$SLICED"/* > "$O/sha-2.txt"
  basename "$SLICED"/*.3mf | tee "$O/name.txt" > /dev/null
  basename -s .3mf "$SLICED"/*.3mf | grep -E -c '[0-9a-f]{16}$' > "$O/hash-check.txt"
  winlist > "$O/windows-end.txt"
  nap 3
  rec_stop
  echo "film done"
fi
if [ "$STEP" = bodies ]; then
  python3 -I /work/lab/fx5bodies.py "$O" |& tee "$O/bodies.txt" | tail -n 3
fi
