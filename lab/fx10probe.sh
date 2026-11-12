#!/bin/bash
# fx10 probe session (not filmed, not scored; out/scratch/fx10p is gitignored): the take layout with ~/knob-full.sc
# open, then it waits so the GUI positions (Revolve dialog, sketch edit, Measure) can be found with docker exec.
#   docker run -d --name fx10p --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx10probe.sh
set -u
. /work/lab/fx10lib.sh
O=/work/out/scratch/fx10p; mkdir -p "$O"; echo "$O" > /tmp/fx10/O
setup
open_knob knob-full; still
python3 /work/lab/fx9.py tools "$O" > "$O/tools.txt" 2>&1
echo ready > "$O/ready"
while kill -0 "$APP" 2>/dev/null; do sleep 2; done
