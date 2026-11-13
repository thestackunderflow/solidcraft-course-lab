#!/bin/bash
# fx11 take P (LAB-fx11 section 3, not filmed): env.txt (rule P0), then the start files by out/fx11/P/tower.py (no AI)
# in the window; ~/tower.sc, ~/tower-sym.sc, ~/block.sc copied to out/fx11/P/ for the other takes (each a fresh container).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx11P.sh
set -u
. /work/lab/fx11lib.sh
take P
envcheck
echo "Xvfb: ${W}x${H}; UI scale: $SCALE" >> /work/out/fx11/env.txt
setup
cd /work/out/fx11/P
python3 -I tower.py /work/out/fx11/P 2>&1 | tee tower.log
rc=${PIPESTATUS[0]}
cp ~/tower.sc ~/tower-sym.sc ~/block.sc /work/out/fx11/P/
FX9_ALLOW=1 python3 /work/lab/fx9.py open "$HOME/tower.sc" > open-tower.txt 2>&1
sleep 4; cp_shot tower-window
[ "$rc" = 0 ] || { echo "P0: a volume mismatch (tower.py exit $rc)"; exit 3; }
echo "P done"
