#!/bin/bash
# fx14 probe session (LAB-fx14 section 7): one container fx14p, SolidCraft at UI scale 1.8 on 2880x1620, held open so
# the GUI positions can be found once (docker exec ... bash /work/lab/fx14px.sh CMD). Stopped and removed after.
#   docker run -d --name fx14p --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx14probe.sh
set -u
. /work/lab/fx14lib.sh
O=/work/out/scratch/fx14p; mkdir -p "$O"; echo "$O" > /tmp/fx14/O
setup
echo ready > "$O/ready"
sleep infinity
