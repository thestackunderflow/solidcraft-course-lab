#!/bin/bash
# fx7alt take F (LAB-fx7alt section 3; not for the video): QA5 [20, 20, 19] and QA7 chamfer at the corner, each on a
# fresh box; then QA6, at most 2 tries: a box, a round cut from its side (solid.cylinder r 5 along Y through the x = 20
# face, operation cut, sent by the lab script as #11516's set-up), then Fillet by clicking an edge of the cut.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx7altF.sh
set -u
. /work/lab/fx7altlib.sh
take F
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
cd /work/out/fx7alt
rec_start
ev "recording started (record only)"
tt 'python3 -I noai.py box'
tt 'python3 -I noai.py fillet 20 20 19'
nap 2.0; cp_shot q5
tt 'clear'
tt 'python3 -I noai.py box'
tt 'python3 -I noai.py chamfer 20 20 20'
nap 2.0; cp_shot q7
tt 'clear'
qa6() {   # qa6 TRY X Y: a fresh box with the side round cut, then Fillet by clicking (X, Y), radius 3, OK
  tt 'python3 -I noai.py box'
  python3 /work/lab/fx7alt.py raw "$O" execute '{"command":"solid.cylinder","params":{"radius":5,"height":20,"base":[20,0,10],"axis":"Y","operation":"cut"}}' > "$O/q6-cut-$1.txt" 2>&1
  nap 2.0; vol q6-before-$1
  ev "q6 try $1: Fillet, click the cut's edge at ($2, $3) in 1440 units, radius 3, OK"
  g $FILLET_BTN 22; click; nap 1.6
  g $2 $3 22; click; nap 1.5
  cp_shot q6-$1-picked
  g $RADIUS_BOX 14; click; xdotool key ctrl+a; nap 0.3; typed 3 160; nap 0.6; xdotool key Tab; nap 2.0
  g $OK_BTN 14; click; nap 2.0; still
  cp_shot q6-$1
  vol q6-after-$1
}
qa6 1 807 386       # the half-round edge on the y = 0 face, at the middle of its arc
grep -q 'timeline.*Fillet' "$O/read-q6-after-1.txt" || {
  g $CANCEL_BTN 14; click; nap 1.0
  qa6 2 888 318     # the straight edge where the groove meets the x = 20 face (upper)
}
nap 2.0
ev "recording stopped"
rec_stop
pane
echo "F done"
