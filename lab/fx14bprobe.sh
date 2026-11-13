#!/bin/bash
# fx14 probe session (LAB-fx14b section 7): one container fx14bp, SolidCraft at UI scale 1.8 on 2880x1620, held open so
# the GUI positions can be found once (docker exec ... bash /work/lab/fx14bpx.sh CMD). Stopped and removed after.
#   docker run -d --name fx14bp --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx14bprobe.sh
set -u
. /work/lab/fx14blib.sh
O=/work/out/scratch/fx14bp; mkdir -p "$O"; echo "$O" > /tmp/fx14b/O
setup
echo ready > "$O/ready"
sleep infinity
