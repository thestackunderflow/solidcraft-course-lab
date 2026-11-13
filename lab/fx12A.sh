#!/bin/bash
# fx12 take A (LAB-fx12 section 3): the refusal. ~/tray.sc (outline 60 x 40 + the linked 2 mm offset) opened off camera;
# full window 3 s; Edit Sketch; the sketch held 4 s; Sketch > Fillet, Radius 3 mm, one inner corner (p7, top right):
# the line (Q8); Create Issue... draft (not submitted), Close draft; Cancel; the sketch read (B.11); Equal Distance
# Chamfer on the same corner (logged); Cancel; the sketch read again.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx12A.sh
set -u
. /work/lab/fx12lib.sh
take A
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc tray; still
rec_start
ev "recording started: full SolidCraft window, ~/tray.sc: hold 3 s"
nap 3.0
sk_edit $SK_ROW
sk a-before
ev "the sketch with the copy (outline 60 x 40, the 2 mm offset): hold 4 s"; nap 4.0
cp_shot sketch
ev "Sketch > Modify > Fillet"; g $FILLET_BTN 16; click; nap 2.0; still; cp_shot dialog
ev "Radius: 3 mm"; radius_field "3 mm"
corner "click one inner corner (the copy's top right, p7)" $IN_TR
still; nap 0.5
ev "fillet copy: full line as shown in refusal.png: hold 4 s"; nap 4.0
cp_shot refusal
ev "Create Issue... (draft only, not submitted)"; g $F_ISSUE 14; click; nap 2.5; still
ev "report draft: hold 4 s"; nap 4.0; cp_shot report
ev "Close draft"; g $ISSUE_CLOSE 14; click; nap 1.5
ev "Cancel"; g $F_CANCEL_ERR 14; click; nap 1.5; still
sk a-after-fillet
ev "after the Fillet: $(cut -c1-300 "$O/sketch-a-after-fillet.txt")"
ev "Sketch > Modify > Equal Distance Chamfer"; g $SK_MODIFY_DD 16; click; nap 1.5; g $EQ_CHAMFER_ITEM 14; click; nap 2.0
corner "click the same inner corner (p7)" $IN_TR
still; ev "chamfer copy: line as shown in chamfer.png: hold 4 s"; nap 4.0
cp_shot chamfer
ev "Cancel"; g $CH_CANCEL_ERR 14; click; nap 1.5; still
sk a-after
ev "after: $(cut -c1-300 "$O/sketch-a-after.txt")"
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "A done"
