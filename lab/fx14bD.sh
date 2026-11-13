#!/bin/bash
# fx14b take D (LAB-fx14b section 3, Q27; F9 left): MCP, no AI. The fx7alt layout: SolidCraft as the top pane, the
# terminal strip below (the whole terminal window in the frame). ~/conv.sc copied in off camera; on camera the typed
# command `python3 -I D/noai.py |& tee D/reply.txt` (it opens ~/conv.sc, sketch.create {plane: {face: [20, 15, 20]}};
# then the same call with fixed: true); reply held 5 s.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx14bD.sh
set -u
. /work/lab/fx14blib.sh
take D
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup split
cp /work/out/fx14b/P/conv.sc "$HOME/conv.sc"
python3 /work/lab/fx9.py cmds sketch.create > "$O/sketch-cmd.txt" 2>&1
cd /work/out/fx14b
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
nap 2.0
ev "recording stopped"
rec_stop
pane
echo "D done"
