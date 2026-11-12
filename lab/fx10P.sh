#!/bin/bash
# fx10 take P (LAB-fx10 section 3, not filmed): env.txt (rule P0), then the knob sketches by out/fx10/P/knob.py (no AI)
# in the window; ~/knob-full.sc and ~/knob-half.sc copied to out/fx10/P/ for the other takes (each a fresh container).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx10P.sh
set -u
. /work/lab/fx10lib.sh
take P
envcheck
setup
cd /work/out/fx10/P
python3 -I knob.py /work/out/fx10/P 2>&1 | tee knob.log
cp ~/knob-full.sc ~/knob-half.sc /work/out/fx10/P/
FX9_ALLOW=1 python3 /work/lab/fx9.py open "$HOME/knob-full.sc" > open-full.txt 2>&1
sleep 4; cp_shot knob-full-window
echo "P done"
