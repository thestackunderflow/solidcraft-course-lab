#!/bin/bash
# fx7alt take B (LAB-fx7alt section 3): the midpoint [10, 20, 20] on a fresh box; typing at once; hold 5 s on the round.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx7altB.sh
set -u
. /work/lab/fx7altlib.sh
take B
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
cd /work/out/fx7alt
tt 'python3 -I noai.py box'
nap 1.0; tmux send-keys -t t "clear" Enter; nap 1.0; still
cp_shot box
rec_start
ev "recording started: SolidCraft window (top) + terminal strip, a fresh 20 mm box, typing at once"
tt 'python3 -I noai.py fillet 10 20 20'
ev "reply shown, the round: hold 5 s"
nap 5.0
cp_shot after
ev "orbit: slow swing, 6 s"
orbit 6
nap 2.0
ev "recording stopped"
rec_stop
pane
vol b-after
echo "B done"
