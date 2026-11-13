#!/bin/bash
# fx13 probe session (not filmed, not scored; out/scratch/fx13p is gitignored): the take layout with ~/tower.sc
# open, then it waits so the GUI positions (Shell, Measure, Properties, section) can be found with docker exec.
#   docker run -d --name fx13p --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx13probe.sh
set -u
. /work/lab/fx13lib.sh
O=/work/out/scratch/fx13p; mkdir -p "$O"; echo "$O" > /tmp/fx13/O
setup
[ -f /work/out/fx13/P/cup.sc ] && open_sc cup; still
python3 /work/lab/fx9.py tools "$O" > "$O/tools.txt" 2>&1
echo ready > "$O/ready"
while kill -0 "$APP" 2>/dev/null; do sleep 2; done
