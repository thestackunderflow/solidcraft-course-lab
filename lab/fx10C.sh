#!/bin/bash
# fx10 take C (LAB-fx10 section 3): the endless line (Q10) and the question (Q12). Off camera, over the plug (no AI):
# ~/ring.sc (XZ: a square x 5..15, z 0..10) and ~/c12.sc (XZ: a construction line (0,0)-(0,10) in world z; rectangle
# 1 x 2..8, z 2..8 beside it; rectangle 2 x -3..3, z 20..26 past the line's drawn end, straddling its extension), c12
# left open. On camera: Revolve, Profile = rectangle 1, Axis = the construction line (does the window take a sketch
# line?): C1; Profile swapped to rectangle 2: C2; back to rectangle 1, OK. Then ~/ring.sc opened, Revolve about Z, OK,
# Measure outer and inner edges; the S2 end frame (the square, 5 s hold, no Revolve) first.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx10C.sh
set -u
. /work/lab/fx10lib.sh
take C
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
R() { FX9_ALLOW=1 python3 /work/lab/fx9.py raw "$O" "$1" "$2" | cut -c1-400 >> "$O/prep.txt"; echo >> "$O/prep.txt"; }
R new_design '{}'
R batch '{"commands":[{"command":"sketch.create","params":{"plane":"XZ"}},{"command":"sketch.line","params":{"closed":true,"points":[[5,0],[15,0],[15,-10],[5,-10]]}},{"command":"sketch.finish","params":{}}]}'
R save "{\"path\":\"$HOME/ring.sc\"}"
R new_design '{}'
R batch '{"commands":[{"command":"sketch.create","params":{"plane":"XZ"}},{"command":"sketch.line","params":{"points":[[0,0],[0,-10]],"construction":true}},{"command":"sketch.line","params":{"closed":true,"points":[[2,-2],[8,-2],[8,-8],[2,-8]]}},{"command":"sketch.line","params":{"closed":true,"points":[[-3,-20],[3,-20],[3,-26],[-3,-26]]}},{"command":"sketch.finish","params":{}}]}'
R save "{\"path\":\"$HOME/c12.sc\"}"
cp "$HOME/ring.sc" "$HOME/c12.sc" "$O/"
sleep 2; g $HOME_BTN 10; xdotool click 1; sleep 2; still
rec_start
ev "recording started: full SolidCraft window, ~/c12.sc: a short construction line (dashed, from the origin up 10 mm), rectangle 1 beside it, rectangle 2 above its drawn end: hold 3 s"
nap 3.0
ev "the line and the two rectangles: hold 4 s"; nap 4.0
cp_shot c-sketch
revolve_open
cp_shot dialog
ev "C1: Profile = rectangle 1 (beside the line)"
g 880 610 18; click; nap 1.5
ev "Axis: the construction line (a sketch line)"
g $R_AXIS 14; click; nap 1.0
g 799 520 18; click; nap 2.5; still
revolve_state "C1"
ev "C1: $(cat /tmp/fx10/last)"
cp_shot c1
ev "C2: Profile cleared, rectangle 2 (past the line's drawn end, straddling its extension)"
g $R_PROFILE_X 14; click; nap 1.2
g $R_PROFILE 14; click; nap 0.8
g 800 232 18; click; nap 2.5; still
revolve_state "C2"
ev "C2: $(cat /tmp/fx10/last) (line as shown in c2.png)"
cp_shot c2
ev "back to rectangle 1, OK"
g $R_PROFILE_X 14; click; nap 1.2
g $R_PROFILE 14; click; nap 0.8
g 880 610 18; click; nap 2.5; still
revolve_state "C1 again"
[ "$(cat /tmp/fx10/last)" = built ] && revolve_ok
home_view
cp_shot c1-built
vol c1
ev "C1 body: volume $(sed 's/.*volume \([^ ]*\).*/\1/' "$O/read-c1.txt"); timeline $(sed 's/.*timeline //' "$O/read-c1.txt")"
ev "Q12: ~/ring.sc opened (plug open, off screen): the square 5 mm off the axis"
FX9_ALLOW=1 python3 /work/lab/fx9.py open "$HOME/ring.sc" > "$O/open-ring.txt" 2>&1; nap 3.0
home_view
ev "S2 end frame: the square off the axis, no Revolve: hold 5 s"; nap 5.0
cp_shot s2-frame
revolve_open
origin_open
pick_z
revolve_state "Q12 ring 360"
ev "Q12: $(cat /tmp/fx10/last)"
[ "$(cat /tmp/fx10/last)" = built ] && revolve_ok
home_view
ev "the ring: hold 4 s"; nap 4.0
cp_shot ring
vol ring
ev "ring: volume $(sed 's/.*volume \([^ ]*\).*/\1/' "$O/read-ring.txt"); timeline $(sed 's/.*timeline //' "$O/read-ring.txt")"
measure_edge 838 509 ring-outer
measure_edge 838 411 ring-inner
props ring-props
g $MODEL_TAB 16; click; nap 1.0; still
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "C done"
