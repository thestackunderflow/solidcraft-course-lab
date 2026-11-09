#!/bin/bash
# fx9 probe session (not filmed, not scored; out/scratch/fx9p is gitignored): the take layout, then it waits so the
# GUI positions (Thread dialog, timeline, Hole dialog) and the plug's command list can be found with docker exec.
#   docker run -d --name fx9p --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx9probe.sh
set -u
. /work/lab/fx9lib.sh
O=/work/out/scratch/fx9p; mkdir -p "$O"; echo "$O" > /tmp/fx9/O
setup
python3 /work/lab/fx9.py tools "$O" > "$O/tools.txt" 2>&1
echo ready > "$O/ready"
while kill -0 "$APP" 2>/dev/null; do sleep 2; done
