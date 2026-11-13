#!/bin/bash
# fx14 gate G0 step 2 (LAB-fx14 section 3, not filmed; screenshots only), run inside the probe container fx14p:
#   docker exec fx14p bash /work/lab/fx14G0w.sh RUNG X Y
# opens out/fx14/G0/RUNG.sc (the plug's `open`, off camera), Home view, Model > New Sketch (Create Sketch), clicks the
# target face at the halved-screen point X Y, holds 4 s, G0/RUNG-window.png (full size) + a halved copy for reading.
. /work/lab/fx14lib.sh
O=/work/out/fx14/G0; R=$1
cp "$O/$R.sc" "$HOME/$R.sc"
FX9_ALLOW=1 python3 /work/lab/fx9.py open "$HOME/$R.sc" > "$O/open-$R-window.txt" 2>&1; sleep 3
g $HOME_BTN 16; click; nap 2.0; still
shot "$O/$R-window-before.png"
g 128 88; click; nap 2.0                      # Model > Sketch > New Sketch: the Create Sketch dialog
g "$2" "$3" 16; click; nap 2.5; still; nap 4.0  # the face pick, held 4 s
shot "$O/$R-window.png"
convert "$O/$R-window.png" -resize 50% "/work/out/scratch/fx14p/w-$R.png"
