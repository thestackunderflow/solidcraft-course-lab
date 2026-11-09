#!/bin/bash
# scwf take H0 (0.30.1, filmed): the redesigned Hole window on the bracket with no holes yet (lab/scwfpart.py build,
# no AI): full window 4 s, Hole, the top face, Reference 1 = the end edge (Distance 1: 12), Reference 2 = the front
# edge (Distance 2: width / 2), the preview held, OK; then a no-AI read (one 4 mm-less 5 mm hole -> volume).
#   docker exec scwf-s bash /work/lab/scwfH0.sh
set -u
. /work/lab/scwflib.sh
take ${TAKE:-H0}
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
python3 /work/lab/scwfpart.py build "$O" before > /dev/null 2>&1
python3 /work/lab/scwfpart.py call "$O" home execute '{"command":"view.home","params":{}}' > /dev/null 2>&1
xdotool key Escape; sleep 1; still; sleep 1
field() { g "$1" "$2" 16; click; nap 0.5; xdotool key ctrl+a; typed "$3" 110; nap 0.5; xdotool key Tab; nap 2.0; }
rec_start
ev "recording started: the bracket, no holes yet, SolidCraft 0.30.1, full window"
nap 4.0
ev "hole: Hole button"
g 297 90 24; click; nap 1.6
ev "hole: the top face"
g 800 250 24; click; nap 1.6
ev "hole: Reference 1 field"
g 1355 408 20; click; nap 1.0
ev "hole: the end edge"
g 659 207 24; click; nap 1.6
ev "hole: Distance 1 = 12"
field 1355 438 12
ev "hole: Reference 2 field"
g 1355 468 16; click; nap 1.0
ev "hole: the front edge"
g 748 360 24; click; nap 1.6
ev "hole: Distance 2 = ${D2:-width / 2}"
field 1355 498 "${D2:-width / 2}"
cp_shot w2
ev "hole: window held 6 s"
g 1240 650 12; nap 6.0
ev "hole: OK"
g 1388 781 20; click; nap 1.5
still; nap 4.0
cp_shot after
ev "recording stopped"
rec_stop
python3 /work/lab/scwfpart.py read "$O" after
echo "H0 done"
