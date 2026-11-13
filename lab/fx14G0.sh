#!/bin/bash
# fx14 gate G0 step 1 (LAB-fx14 section 3, not filmed): the no-AI client builds the rungs and tries sketch.create on
# each; ~/g0a.sc .. ~/g0d.sc copied to out/fx14/G0/ for the window checks (step 2).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx14G0.sh
set -u
. /work/lab/fx14lib.sh
take G0
setup
cd /work/out/fx14 && python3 -I G0/g0.py 2>&1 | tee G0/client.txt
cp ~/g0?.sc ~/g0d.stl /work/out/fx14/G0/ 2>/dev/null
cp_shot g0-client-window
ls -la /work/out/fx14/G0/
