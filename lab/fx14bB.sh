#!/bin/bash
# fx14b take B (LAB-fx14b section 3; F2, F5, F7 left, Short S1 first half; Q22): the fix, Use fixed plane.
# ~/conv.sc opened off camera; Properties before (F5's "before"); Create Sketch, click the top: the line; Use fixed plane
# (no OK: the sketch opens at once); circle centre (20, 15), diameter 10 typed; Finish; Extrude, Cut, 5 mm, Reverse
# (into the block); OK; Properties (expected 23,607.30); Measure the top face (expected 1,121.46); the block turning 5 s.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx14bB.sh
set -u
. /work/lab/fx14blib.sh
take B
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc conv; g $HOME_BTN 16; click; nap 2.0; still
vol b-before
rec_start
ev "recording started: full SolidCraft window, ~/conv.sc (converted block): hold 3 s"
nap 3.0
props_at $BODY_ROW_CONV props-before
sk_dialog_face $TOP_FACE "click the top at (20, 15, 20)"
ev "the line again, hint and Use fixed plane as shown in line.png: hold 4 s"; nap 4.0; cp_shot line
ev "zoom target: Use fixed plane: hold 2 s"; g $USE_FIXED 16; nap 2.0
ev "click Use fixed plane"; click; nap 2.5; still
ev "fixed plane: sketch opened as shown in fixed.png: hold 3 s"; nap 3.0; cp_shot fixed
circle_d10 $SK_CENTRE40
ev "circle 10 mm drawn as shown in circle.png: hold 2 s"; nap 2.0; cp_shot circle
cut5 cut-preview
vol b-after-cut
ev "fixed-plane cut: $(cut -c1-200 "$O/read-b-after-cut.txt")"
ev "the cut as shown in cut.png: hold 3 s"; nap 3.0; cp_shot cut
props_at $BODY_ROW_CUT props
inspect_tab
ev "Inspect > Measure"; g $MEASURE_BTN 16; click; nap 2.0
ev "Measure: click the top face"; g $ME_TOP 16; click; nap 2.0; still
ev "Measure: top face area as shown in area.png: hold 4 s"; nap 4.0; cp_shot area
ev "Measure: close"; g $ME_CLOSE 14; click; nap 1.5; still
model_tab; home_view
ev "F11: the block with its hole turning (5 s)"
g $ORBIT_BTN 16; click; nap 0.8; g 1000 450 14; xdotool mousedown 1; g 1150 440 75; nap 0.3; g 1000 450 75; xdotool mouseup 1
nap 0.8; xdotool key Escape; nap 0.5; home_view; cp_shot end
vol b-after
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "B done"
