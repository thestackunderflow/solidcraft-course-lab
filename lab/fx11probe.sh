#!/bin/bash
# fx11 probe session (not filmed, not scored; out/scratch/fx11p is gitignored): the take layout with ~/tower.sc
# open, then it waits so the GUI positions (Split Body, Offset Plane, Properties) can be found with docker exec.
#   docker run -d --name fx11p --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx11probe.sh
set -u
. /work/lab/fx11lib.sh
O=/work/out/scratch/fx11p; mkdir -p "$O"; echo "$O" > /tmp/fx11/O
setup
[ -f /work/out/fx11/P/tower.sc ] && open_sc tower; still
python3 /work/lab/fx9.py tools "$O" > "$O/tools.txt" 2>&1
echo ready > "$O/ready"
while kill -0 "$APP" 2>/dev/null; do sleep 2; done
