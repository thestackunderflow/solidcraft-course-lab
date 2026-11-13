#!/bin/bash
# fx12 take B-wall (LAB-fx12 section 3, B step 4, attempt 2; DEVIATIONS): take B's Measure after the extrude found no
# sketch (the Sketch1 row double-click did not enter Edit Sketch; Measure stayed on "Select"). Here the same Fix 1 in a
# fresh window, measured inside the sketch BEFORE Finish (the same curves): ~/tray.sc; Edit Sketch; Break Offset
# Association on the copy's top line; Fillet 3 on the four inner corners; Inspect > Measure from the outside corner
# (30, 20) to the inner top-right arc: Q11 Fix 1, 4.07 mm pre-registered.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx12Bw.sh
set -u
. /work/lab/fx12lib.sh
take B-wall
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc tray; still
rec_start
ev "recording started: full SolidCraft window, ~/tray.sc: hold 3 s"
nap 3.0
sk_edit $SK_ROW
ev "select the copy's top line"; g $IN_TOP_LINE 16; click; nap 1.5
ev "right-click: the menu"; xdotool click 3; nap 2.0
ev "Break Offset Association"; g $BREAK_ITEM 14; click; nap 2.0; xdotool key Escape; nap 1.0; still
ev "Sketch > Modify > Fillet"; g $FILLET_BTN 16; click; nap 2.0
ev "Radius: 3 mm"; radius_field "3 mm"
for c in "bottom left:$IN_BL" "top left:$IN_TL" "top right:$IN_TR" "bottom right:$IN_BR"; do
  corner "inner corner ${c%%:*}" ${c#*:}
done
ev "OK"; g $F_OK 14; click; nap 2.5; still
sk bw-after-fillet
ev "fillet after break: $(cut -c1-300 "$O/sketch-bw-after-fillet.txt")"
g $INSPECT_TAB 16; click; nap 1.0; ev "Inspect > Measure"; g $MEASURE_BTN 16; click; nap 2.0
ev "Measure: the outside corner (30, 20)"; g $OUT_TR 12; click; nap 1.5
ev "Measure: the inner arc (top right)"; g $IN_ARC_MID 12; click; nap 2.0; still
ev "wall at the corner (Min) as shown in wall.png: hold 4 s"; nap 4.0; cp_shot wall
xdotool key Escape; nap 1.0; ev "Finish Sketch"; g $FINISH_SK_PANEL 14; click; nap 2.5; still
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "B-wall done"
