#!/bin/bash
# fx8 take A2 (retry of take A step 1, see DEVIATIONS): in take A the OK click landed below the Extrude panel (the probe's
# panel was taller), so no cut was attempted. Same design as take A (hook.stl mesh + Sketch1). Part 1 (this script):
# full window 3 s, Extrude, circle, Cut, Reverse, OK at the panel's real OK, hold 4 s. Part 2: fx8A2b.sh closes it.
#   docker exec fx8 bash /work/lab/fx8A2.sh
set -u
. /work/lab/fx8lib.sh
take A2
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
g 122 50 8; click; nap 1.0; still; nap 2.0                      # Model tab
rec_start
ev "recording started: take A's design (hook.stl mesh + Sketch1), full window"
nap 3.0
ev "cut: Extrude button"
g 194 90 22; click; nap 1.6
ev "cut: pick the circle"
g 793 407 22; click; nap 1.4
ev "cut: Operation menu"
g 1350 437 18; click; nap 1.2
ev "cut: Cut"
g 1301 514 12; click; nap 1.4
ev "cut: Reverse (into the plate)"
g 1325 497 14; click; nap 1.5
cp_shot cut-before-ok
ev "cut: OK"
g 1388 578 14; click; nap 1.0
ev "cut: result held 4 s"
nap 4.0
cp_shot cut
