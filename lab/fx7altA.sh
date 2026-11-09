#!/bin/bash
# fx7alt take A (LAB-fx7alt section 3): the corner refusal. env.txt (rule P0) first. The fresh box is sent by noai.py
# before the recording (the take opens on typing, filming rule); the call at [20, 20, 20]; the window's toast; hold 5 s;
# then the slow orbit (F1 source, 8 s) and the home view.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx7altA.sh
set -u
. /work/lab/fx7altlib.sh
take A
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
E=/work/out/fx7alt/env.txt
{ echo "solidcraft --version: $(/opt/solidcraft/bin/solidcraft --version 2>&1)"; echo "claude --version: $(claude --version 2>&1)";
  echo "date: $(date -u)"; } > "$E"
grep -q '0.28.0' "$E" || { echo "P0: wrong SolidCraft version"; cat "$E"; exit 3; }
setup
cd /work/out/fx7alt
tt 'python3 -I noai.py box'
nap 1.0; tmux send-keys -t t "clear" Enter; nap 1.0; still
cp_shot box
rec_start
ev "recording started: SolidCraft window (top) + terminal strip, a fresh 20 mm box, typing at once"
tt 'python3 -I noai.py fillet 20 20 20'
nap 0.3; cp_shot reply; cp_shot window
ev "reply + window toast shown: hold 5 s"
nap 5.0
ev "orbit: slow swing, 8 s (F1 source)"
orbit 8
ev "home view: hold 3 s"
nap 3.0
cp_shot after
ev "recording stopped"
rec_stop
pane
vol a-after
echo "A done"
