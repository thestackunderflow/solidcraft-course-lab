#!/bin/bash
# scerr take Y ("your turn", 0.30.1, filmed): lesson 3's hook unfilleted, full window 4 s, Inspect > Measure, the lip's
# outer top edge then its inner top edge: Distance 5.00 mm (the face beside the edge), held 7 s, Close.
#   docker exec scerr-s bash /work/lab/scerrY.sh
set -u
. /work/lab/scerrlib.sh
take Y
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
still; sleep 1
rec_start
ev "recording started: lesson 3's hook (no fillet) in SolidCraft 0.30.1, full window"
nap 4.0
ev "measure: Inspect tab"
g 382 50 22; click; nap 1.2
ev "measure: Measure"
g 120 90 18; click; nap 1.4
ev "measure: lip outer top edge"
g 910 610 24; click; nap 1.4
ev "measure: lip inner top edge"
g 878 594 12; click; nap 1.5
ev "measure: Distance 5.00 mm held 7 s"
g 1310 407 18; nap 7.0
cp_shot measure
ev "measure: Close"
g 1399 575 14; click; nap 1.5
still; nap 2.0
ev "recording stopped"
rec_stop
echo "Y done"
