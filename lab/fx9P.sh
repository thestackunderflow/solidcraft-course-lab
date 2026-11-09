#!/bin/bash
# fx9 take P (LAB-fx9 section 3, not filmed): env.txt (rule P0), then the nut by out/fx9/P/nut.py (no AI) into the
# window; ~/nut.sc and ~/nut-675.sc copied to out/fx9/P/ for the other takes (each a fresh container).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx9P.sh
set -u
. /work/lab/fx9lib.sh
take P
envcheck
setup
cd /work/out/fx9/P
python3 -I nut.py /work/out/fx9/P 2>&1 | tee nut.log
cp ~/nut.sc ~/nut-675.sc /work/out/fx9/P/
sleep 3; cp_shot nut-675-window
echo "P done"
