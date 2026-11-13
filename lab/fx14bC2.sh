#!/bin/bash
# fx14b take C2 = take C step 1 (Q24, the Hole), attempt 2: in take C the Flat drill point removes the Tip Angle row,
# the dialog shrinks and OK moves up to 1388 710 (halved); the OK click at 1388 729 missed, no Hole was built
# (DEVIATIONS). Step 2 (Q26) is kept from take C. Only the OK position changed.
# (was: fx14b take C, LAB-fx14b section 3; F6, F7 right, F10; Short S1 second half; Q24, Q26).
# 1. Q24: ~/conv2.sc (a fresh copy of the converted block); Model > Hole; click the top; Depth 5, Diameter 10 typed;
#    the Drill Point default held (Angle 118 deg), then Flat (so the hole is the same flat-bottomed hole as take B's
#    cut; DEVIATIONS); OK; Properties (expected 23,607.30); the History bar's new icon hovered (Hole1).
# 2. Q26 (F10): ~/conv30.sc (30 x 30 x 10, converted); Create Sketch, top, the line, Use fixed plane; circle centre
#    (15, 15), diameter 10; Finish; Extrude Cut 5; Properties (expected 8,607.30).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx14bC2.sh
set -u
. /work/lab/fx14blib.sh
take C2
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc conv2; g $HOME_BTN 16; click; nap 2.0; still
vol c-before
rec_start
ev "recording started: full SolidCraft window, ~/conv2.sc (a fresh copy of the converted block): hold 3 s"
nap 3.0
model_tab
ev "zoom target: Model tab > Create > Hole: hold 2 s"; g $HOLE_BTN 16; nap 2.0; cp_shot menu
ev "Model > Hole"; click; nap 2.0; still
ev "Hole dialog with its defaults as shown in hole-dialog.png: hold 2 s"; nap 2.0; cp_shot hole-dialog
pick "click the top at (20, 15, 20)" $TOP_FACE
ev "Depth: 5 mm (typed), Tab"; g $HOLE_DEPTH 16; click; xdotool key ctrl+a; typed "5 mm" 140; xdotool key Tab; nap 1.0
ev "Diameter: 10 mm (typed), Tab"; g $HOLE_DIAM 16; click; xdotool key ctrl+a; typed "10 mm" 140; xdotool key Tab; nap 2.0; still
ev "hole preview, Drill Point Angle (default) as shown in hole-angle.png: hold 3 s"; nap 3.0; cp_shot hole-angle
ev "Drill Point: Flat"; g $HOLE_DRILL 16; click; nap 1.2; g $HOLE_FLAT 14; click; nap 2.0; still
ev "hole preview, Drill Point Flat as shown in hole-flat.png: hold 3 s"; nap 3.0; cp_shot hole-flat
ev "OK"; g $HOLE_OK_FLAT 14; click; nap 3.0; still
vol c-after-hole
ev "hole on converted top: $(cut -c1-200 "$O/read-c-after-hole.txt")"
ev "the hole as shown in hole.png: hold 3 s"; nap 3.0; cp_shot hole
props_at $BODY_ROW_HOLE props
ev "History bar: the new icon hovered (tooltip): hold 3 s"; g 381 785 16; nap 3.0; cp_shot timeline
still
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "C2 done"
