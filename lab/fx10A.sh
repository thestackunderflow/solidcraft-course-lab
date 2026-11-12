#!/bin/bash
# fx10 take A (LAB-fx10 section 3): the refusal. ~/knob-full.sc opened off camera; full window 3 s; the T with the axis
# through its middle held 4 s; Revolve (Model > Create > Revolve), Axis = Z picked in Browser > Origin, 360: the line
# (Q8); Create Issue... draft (not submitted); 180 degrees (B.14); Cancel. Then Q11 (logged only): a normal line drawn
# on the axis through the T in Sketch1, Revolve with both regions picked and that line as the axis.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx10A.sh
set -u
. /work/lab/fx10lib.sh
take A
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_knob knob-full; still
vol a-before
rec_start
ev "recording started: full SolidCraft window, ~/knob-full.sc (the T sketch): hold 3 s"
nap 3.0
expand_origin
ev "the T sketch, the vertical axis Z through its middle: hold 4 s"; g 82 358 14; nap 4.0; still
cp_shot sketch
revolve_open
cp_shot dialog
pick_z
revolve_state "revolve full 360"
ev "revolve full: $(cat /tmp/fx10/last) (line as shown in refusal.png)"
cp_shot refusal
ev "Create Issue... (draft only, not submitted)"
g $R_ISSUE 14; click; nap 2.5; still
ev "report draft: hold 4 s"; nap 4.0
cp_shot report
g $ISSUE_CLOSE 14; click; nap 1.5; still
ev "B.14: Angle 180 deg"
g $R_ANGLE 14; click; xdotool key ctrl+a; nap 0.3; typed "180 deg" 140; nap 0.5; xdotool key Tab; nap 2.0; still
revolve_state "revolve full 180"
ev "revolve full 180: $(cat /tmp/fx10/last)"
cp_shot refusal-180
if [ "$(cat /tmp/fx10/last)" = refused ]; then ev "Cancel"; g $R_CANCEL_ERR 14; click; else ev "Cancel"; g $R_CANCEL 14; click; fi
nap 2.0; still
vol a-after-cancel
ev "after Cancel: timeline $(sed 's/.*timeline //' "$O/read-a-after-cancel.txt")"
# Q11 (logged only): a normal line on the axis through the T
ev "Q11: double-click Sketch1 (edit the sketch)"
g $SKETCH1_ROW 16; dclick; nap 2.5; still
ev "Line tool: a normal line on the axis, from the stem's end to the cap's end"
g $LINE_TOOL 16; click; nap 1.0
g $(sk 0 0) 18; nap 0.5; click; nap 0.8
g $(sk 0 -23) 20; nap 0.5; click; nap 0.8
xdotool key Escape; nap 0.8; xdotool key Escape; nap 1.0; still
ev "the T split by the line: hold 2 s"; nap 2.0
cp_shot split-sketch
ev "Finish Sketch"
g $FINISH_BTN 16; click; nap 2.5; still
revolve_open
cp_shot split-dialog
ev "Profile: the left region, then the right region"
g 580 555 18; click; nap 1.2
g 900 555 18; click; nap 1.2
ev "Axis: the drawn line"
g $R_AXIS 14; click; nap 1.0
g 720 400 18; click; nap 2.5; still
revolve_state "split T"
ev "split T: $(cat /tmp/fx10/last) (line as shown in split.png)"
cp_shot split
if [ "$(cat /tmp/fx10/last)" = built ]; then
  revolve_ok; vol a-split; ev "split T built: volume $(sed 's/.*volume \([^ ]*\).*/\1/' "$O/read-a-split.txt")"
else
  ev "Cancel"; g $R_CANCEL_ERR 14; click; nap 2.0; still
fi
vol a-after
ev "after: timeline $(sed 's/.*timeline //' "$O/read-a-after.txt")"
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "A done"
