#!/bin/bash
# scerr take F (error 1 re-check on 0.30.1, filmed): lesson 3's hook (8,500 mm3, lip top face 5 mm), full window 4 s,
# Fillet on the lip's outer top edge, radius 5.1 (the red line held 7 s), then 5.0 (held), OK, the built round held 6 s.
#   docker exec scerr-s bash /work/lab/scerrF.sh
set -u
. /work/lab/scerrlib.sh
take ${TAKE:-F}
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
xdotool key Escape; sleep 0.5; g 870 737 10; click; sleep 1.5; still; sleep 1   # home view (bottom bar), panels closed
rec_start
ev "recording started: lesson 3's hook in SolidCraft 0.30.1, full window"
nap 4.0
ev "fillet: Fillet button"
g $FILLET_BTN 24; click; nap 1.6
ev "fillet: lip outer top edge"
g $LIP_EDGE 26; nap 0.6; click; nap 1.4
ev "fillet: radius 5.1 typed"
radius 5.1
cp_shot r51
ev "fillet 5.1: red line held 7 s"
g 1310 570 14; nap 7.0
ev "fillet: radius 5.0 typed"
radius 5.0
cp_shot r50
ev "fillet 5.0: preview held 3 s"
nap 3.0
ev "fillet 5.0: OK"
g $OK_BTN 20; click; nap 1.0
still; nap 6.0
cp_shot built
ev "recording stopped"
rec_stop
read_now f-after
echo "F done"
