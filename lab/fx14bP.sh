#!/bin/bash
# fx14b take P (LAB-fx14b section 3, not filmed): env.txt (rule P0), then the start files by out/fx14b/P/blocks.py
# (no AI) in the window; ~/conv.sc, conv2, conv3, block, conv30, offset (+ the STLs) copied to out/fx14b/P/.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx14bP.sh
set -u
. /work/lab/fx14blib.sh
take P
envcheck
echo "Xvfb: ${W}x${H}; UI scale: $SCALE" >> /work/out/fx14b/env.txt
setup
cd /work/out/fx14b/P
python3 -I blocks.py /work/out/fx14b/P 2>&1 | tee blocks.log
rc=${PIPESTATUS[0]}
cp ~/conv.sc ~/conv2.sc ~/conv3.sc ~/block.sc ~/conv30.sc ~/offset.sc ~/conv.stl ~/conv30.stl /work/out/fx14b/P/
FX9_ALLOW=1 python3 /work/lab/fx9.py open "$HOME/conv.sc" > open-conv.txt 2>&1
sleep 4; cp_shot conv-window
[ "$rc" = 0 ] || { echo "P0: a volume mismatch (blocks.py exit $rc)"; exit 3; }
echo "P done"
