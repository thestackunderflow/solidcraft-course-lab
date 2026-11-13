#!/bin/bash
# fx12 take C (LAB-fx12 section 3): Fix 2, round first. ~/tray-plain.sc; Edit Sketch; Fillet the outline's four corners
# 5 mm; Offset 2 mm inward from the top line (Chain); the sketch read (Q10 ids, linked?); Measure the inner arc (R 3.00
# expected) and the wall outer arc to inner arc (2.00 expected); Finish; Extrude the ring 20; Properties (7,405.31).
# RAD=1.5 TAKE=C2 runs Q12 the same way (outline 1.5, the outline held 5 s before the Offset).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx12C.sh
set -u
. /work/lab/fx12lib.sh
RAD=${RAD:-5}
take ${TAKE:-C}
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc tray-plain; still
rec_start
ev "recording started: full SolidCraft window, ~/tray-plain.sc (outline 60 x 40 only): hold 3 s"
nap 3.0
sk_edit $SK_ROW
ev "Sketch > Modify > Fillet"; g $FILLET_BTN 16; click; nap 2.0
ev "Radius: $RAD mm"; radius_field "$RAD mm"
for c in "bottom left:$OUT_BL" "top left:$OUT_TL" "top right:$OUT_TR" "bottom right:$OUT_BR"; do
  corner "outline corner ${c%%:*}" ${c#*:}
done
still; nap 1.0; cp_shot fillet4
ev "OK"; g $F_OK 14; click; nap 2.5; still
sk c-rounded
ev "outline rounded $RAD: hold 5 s"; nap 5.0; cp_shot rounded
ev "Sketch > Modify > Offset"; g $OFFSET_SK_BTN 16; click; nap 2.0
ev "the outline's top line (Chain on)"; g $OUT_TOP_LINE 12; click; nap 2.0
ev "Distance: 2 mm"; g $OFF_DIST 16; click; xdotool key ctrl+a; typed "2 mm"; xdotool key Tab; nap 1.5; still
cp_shot offset-dialog
ev "OK"; g $OFF_OK 14; click; nap 2.5; still
sk c-offset
ev "offset after round $RAD: $(cut -c1-500 "$O/sketch-c-offset.txt")"
ev "the copy: hold 4 s"; nap 4.0; cp_shot copy
g $INSPECT_TAB 16; click; nap 1.0; ev "Inspect > Measure"; g $MEASURE_BTN 16; click; nap 2.0
ev "Measure: the inside corner (top right)"; g $IN_ARC_MID 12; click; nap 2.0; still
ev "inside corner as shown in measure.png: hold 4 s"; nap 4.0; cp_shot measure
ev "Measure: add the outline's arc (top right)"; g $OUT_ARC_MID 12; click; nap 2.0; still
ev "wall at the corner as shown in wall.png: hold 4 s"; nap 4.0; cp_shot wall
xdotool key Escape; nap 1.0; ev "Finish Sketch"; g $FINISH_SK_PANEL 14; click; nap 2.5; still
extrude_ring
vol c-after-extrude
props_body props
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "${TAKE:-C} done"
