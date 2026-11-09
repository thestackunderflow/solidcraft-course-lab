#!/bin/bash
# fx6 take A part 1 (LAB-fx6 section 3, take A steps 1-3): full window 3 s, Parameters held on thickness 5, Fillet on
# the lip's outer top edge at 6 mm, OK; screenshots at once and +5 s. The recording keeps running; part 2 (lab/fx6A2.sh)
# is written after reading what part 1's screenshots show (Report button, mark, undo).
#   docker exec fx6 bash /work/lab/fx6A.sh
set -u
. /work/lab/fx6lib.sh
take A
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
still; sleep 1
rec_start
ev "recording started: lesson 3's hook in SolidCraft 0.28.0, full window"
nap 3.0
ev "params: hover Parameters"
g $PARAMS_BTN 24; click
nap 1.5
ev "params: thickness 5 held"
g 900 551 18; nap 4.0
cp_shot params-thickness5
ev "params: close (Cancel)"
g 1322 745 18; click; nap 1.5
still; nap 1.0
ev "fillet: Fillet button"
g $FILLET_BTN 24; click; nap 1.6
ev "fillet: lip outer top edge"
g $LIP_EDGE 26; nap 0.6; click; nap 1.4
ev "fillet: radius 6 typed"
radius 6
cp_shot radius6-preview
ev "fillet: OK"
g $OK_BTN 20; click
nap 0.2
cp_shot refusal
ev "fillet 6: after OK (screenshot refusal.png)"
nap 5.0
cp_shot refusal-5s
ev "fillet 6: +5 s (screenshot refusal-5s.png)"
echo "part 1 done"
