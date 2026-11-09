#!/bin/bash
# fx7alt take C (LAB-fx7alt section 3): [20, 20, 5] on a fresh box; full window held 3 s first; after.png from two
# angles (the home view, then turned so the upright edge's both ends show).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx7altC.sh
set -u
. /work/lab/fx7altlib.sh
take C
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
cd /work/out/fx7alt
tt 'python3 -I noai.py box'
nap 1.0; tmux send-keys -t t "clear" Enter; nap 1.0; still
rec_start
ev "recording started: full window held 3 s, a fresh 20 mm box"
nap 3.0
tt 'python3 -I noai.py fillet 20 20 5'
ev "reply shown, the round: hold 5 s"
nap 5.0
cp_shot after
ev "second angle: turn the view (middle drag), hold 4 s"
g 1000 330 10; xdotool mousedown 2
for i in $(seq 1 40); do xdotool mousemove_relative -- -6 1; sleep 0.05; done
xdotool mouseup 2; still; nap 4.0
cp_shot after-2
g $HOME_BTN 14; click; nap 1.0; still; nap 2.0
ev "recording stopped"
rec_stop
pane
vol c-after
echo "C done"
