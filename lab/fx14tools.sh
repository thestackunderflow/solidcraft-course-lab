#!/bin/bash
# fx14 G0 step 0 (not filmed): the plug's tool list and list_commands into out/fx14/G0/ (no AI).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx14tools.sh
set -u
. /work/lab/fx14lib.sh
take G0
envcheck
echo "Xvfb: ${W}x${H}; UI scale: $SCALE" >> /work/out/fx14/env.txt
setup
cd /work/out/fx14 && python3 -I G0/tools.py
