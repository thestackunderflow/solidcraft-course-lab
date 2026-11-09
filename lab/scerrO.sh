#!/bin/bash
# scerr take O (opening, 0.30.1, filmed): lesson 4's hook full window 3 s, a slow orbit right and back (10 s), the home
# view held 3 s. PrusaSlicer from take S is closed first (not filmed).
set -u
. /work/lab/scerrlib.sh
take O
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
pkill -f prusa-slicer; sleep 2; still; sleep 1
rec_start
ev "recording started: lesson 4's hook in SolidCraft 0.30.1, full window"
nap 3.0
ev "orbit: slow swing right and back, 10 s"
g 1000 330 10; xdotool mousedown 2
for i in $(seq 1 80); do xdotool mousemove_relative -- 5 0; sleep 0.06; done
for i in $(seq 1 80); do xdotool mousemove_relative -- -5 0; sleep 0.06; done
xdotool mouseup 2; nap 0.5
ev "home view: held 3 s"
g 870 737 14; click; nap 1.0; still; nap 3.0
ev "recording stopped"
rec_stop
echo "O done"
