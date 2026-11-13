#!/bin/bash
# fx11 take D (LAB-fx11 section 3): MCP, no AI. The fx7alt layout: SolidCraft as the top pane, the terminal strip below
# (the whole terminal window in the frame). ~/tower.sc copied in off camera; on camera the typed command
# `python3 -I D/noai.py |& tee D/reply.txt` (it opens ~/tower.sc and sends solid.split_body body Tower, plane XY); reply held 5 s.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx11D.sh
set -u
. /work/lab/fx11lib.sh
take D
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup split
cp /work/out/fx11/P/tower.sc "$HOME/tower.sc"
python3 /work/lab/fx9.py cmds split_body > "$O/split-cmd.txt" 2>&1
cd /work/out/fx11
rec_start
ev "recording started: SolidCraft window (top) + terminal strip: hold 3 s"
nap 3.0
ev "typed: python3 -I D/noai.py |& tee D/reply.txt"
tt 'python3 -I D/noai.py |& tee D/reply.txt'
nap 0.3; cp_shot reply
ev "reply + window shown: hold 5 s"
nap 5.0
cp_shot window
vol d-after
ev "after: timeline $(sed 's/.*timeline //' "$O/read-d-after.txt"); volume $(sed 's/.*volume \([^ ]*\).*/\1/' "$O/read-d-after.txt")"
nap 2.0
ev "recording stopped"
rec_stop
pane
echo "D done"
