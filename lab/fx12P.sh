#!/bin/bash
# fx12 take P (LAB-fx12 section 3, not filmed): env.txt (rule P0), then the start files by out/fx12/P/tray.py (no AI)
# in the window; ~/tray.sc, ~/tray-plain.sc, ~/box.sc copied to out/fx12/P/ for the other takes (each a fresh container).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx12P.sh
set -u
. /work/lab/fx12lib.sh
take P
envcheck
echo "Xvfb: ${W}x${H}; UI scale: $SCALE" >> /work/out/fx12/env.txt
setup
cd /work/out/fx12/P
python3 -I tray.py /work/out/fx12/P 2>&1 | tee tray.log
rc=${PIPESTATUS[0]}
cp ~/tray.sc ~/tray-plain.sc ~/box.sc /work/out/fx12/P/
FX9_ALLOW=1 python3 /work/lab/fx9.py open "$HOME/tray.sc" > open-tray.txt 2>&1
sleep 4; cp_shot tray-window
[ "$rc" = 0 ] || { echo "P0: a region/id mismatch (tray.py exit $rc)"; exit 3; }
echo "P done"
