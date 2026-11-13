#!/bin/bash
# fx12 take B (LAB-fx12 section 3): Fix 1, break the association. ~/tray.sc; Edit Sketch; the copy's top line
# right-click > Break Offset Association (Q9: do the other three lines still carry it? sketch read); Fillet 3 on the
# four inner corners; Finish Sketch; Extrude the ring 20; Properties (B.13); then Edit Sketch, Inspect > Measure from
# the outside corner (30, 20) to the inner arc (Q11 Fix 1, 4.07 pre-registered); Close; Finish Sketch.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx12B.sh
set -u
. /work/lab/fx12lib.sh
take B
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc tray; still
rec_start
ev "recording started: full SolidCraft window, ~/tray.sc: hold 3 s"
nap 3.0
sk_edit $SK_ROW
sk b-before
ev "select the copy's top line"; g $IN_TOP_LINE 16; click; nap 1.5
ev "right-click: the menu"; xdotool click 3; nap 2.0; cp_shot menu
ev "Break Offset Association"; g $BREAK_ITEM 14; click; nap 2.0; xdotool key Escape; nap 1.0; still
nap 3.0; cp_shot after-break
sk b-after-break
ev "after one Break: $(cut -c1-400 "$O/sketch-b-after-break.txt")"
ev "Sketch > Modify > Fillet"; g $FILLET_BTN 16; click; nap 2.0
ev "Radius: 3 mm"; radius_field "3 mm"
for c in "bottom left:$IN_BL" "top left:$IN_TL" "top right:$IN_TR" "bottom right:$IN_BR"; do
  corner "inner corner ${c%%:*}" ${c#*:}
done
still; nap 1.0; cp_shot fillet4
ev "OK"; g $F_OK 14; click; nap 2.5; still
sk b-after-fillet
ev "fillet after break: $(cut -c1-400 "$O/sketch-b-after-fillet.txt")"
ev "the sketch with four inside R3: hold 4 s"; nap 4.0; cp_shot rounded
ev "Finish Sketch"; g $FINISH_SK 16; click; nap 2.5; still
extrude_ring
vol b-after-extrude
props_body props
ev "Edit Sketch again (Bodies listed) for Measure"; sk_edit $SK_ROW_B
g $INSPECT_TAB 16; click; nap 1.0; ev "Inspect > Measure"; g $MEASURE_BTN 16; click; nap 2.0
ev "Measure: the outside corner (30, 20)"; g $OUT_TR 12; click; nap 1.5
ev "Measure: the inner arc (top right)"; g $IN_ARC_MID 12; click; nap 2.0; still
ev "wall at the corner (Min) as shown in wall.png: hold 4 s"; nap 4.0; cp_shot wall
xdotool key Escape; nap 1.0; ev "Finish Sketch"; g $FINISH_SK_PANEL 14; click; nap 2.5; still
vol b-after
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "B done"
