#!/bin/bash
# fx7alt probe session (not filmed, not scored; out/scratch/fx7p is gitignored): the take layout, then it waits so the
# GUI positions (Fillet dialog, view cube, orbit) and the plug's tool list can be found with docker exec.
#   docker run -d --name fx7p --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx7altprobe.sh
set -u
. /work/lab/fx7altlib.sh
O=/work/out/scratch/fx7p; mkdir -p "$O"; echo "$O" > /tmp/fx7/O
setup
python3 /work/lab/fx7alt.py tools "$O" > "$O/tools.txt" 2>&1
python3 /work/lab/fx7alt.py box > "$O/box.txt" 2>&1
sleep 4; shot "$O/box.png"
echo ready > "$O/ready"
while kill -0 "$APP" 2>/dev/null; do sleep 2; done
