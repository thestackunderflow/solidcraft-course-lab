#!/bin/bash
# fx12 Q14 (LAB-fx12 section 3 C5; logged only, not filmed): out/fx12/C14/q14.py in a fresh window.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx12Q14.sh
set -u
. /work/lab/fx12lib.sh
take C14
setup
cp /work/out/fx12/P/tray-plain.sc "$HOME/tray-plain.sc"
cd /work/out/fx12 && python3 -I C14/q14.py 2>&1 | tee C14/q14.txt
sleep 2; cp_shot window
echo "C14 done"
