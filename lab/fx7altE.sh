#!/bin/bash
# fx7alt take E (LAB-fx7alt section 3): the tool list (tools/list), the solid.fillet entry (list_commands), hold 4 s
# on its edges line, then one try at the {body, index} route (body_topology) on a fresh box.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx7altE.sh
set -u
. /work/lab/fx7altlib.sh
take E
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
cd /work/out/fx7alt
tt 'python3 -I noai.py box'
nap 1.0; tmux send-keys -t t "clear" Enter; nap 1.0; still
rec_start
ev "recording started: full window held 3 s"
nap 3.0
tt 'python3 -I noai.py tools'
ev "tool list + fillet entry + edge indexes shown: hold 4 s"
nap 4.0
cp_shot tools
ev "recording stopped"
rec_stop
pane
echo "E done"
