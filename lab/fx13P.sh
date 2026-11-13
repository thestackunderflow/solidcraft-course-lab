#!/bin/bash
# fx13 take P (LAB-fx13 section 3, not filmed): env.txt (rule P0), then the start files by out/fx13/P/cups.py (no AI)
# in the window; ~/cup.sc, ~/cup-bottom.sc, ~/cup-r3.sc, ~/cup40.sc copied to out/fx13/P/ for the other takes.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx13P.sh
set -u
. /work/lab/fx13lib.sh
take P
envcheck
echo "Xvfb: ${W}x${H}; UI scale: $SCALE" >> /work/out/fx13/env.txt
setup
cd /work/out/fx13/P
python3 -I cups.py /work/out/fx13/P 2>&1 | tee cups.log
rc=${PIPESTATUS[0]}
cp ~/cup.sc ~/cup-bottom.sc ~/cup-r3.sc ~/cup40.sc /work/out/fx13/P/
FX9_ALLOW=1 python3 /work/lab/fx9.py open "$HOME/cup.sc" > open-cup.txt 2>&1
sleep 4; cp_shot cup-window
[ "$rc" = 0 ] || { echo "P0: a volume mismatch (cups.py exit $rc)"; exit 3; }
echo "P done"
