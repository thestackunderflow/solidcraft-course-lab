#!/bin/bash
# fx8 take C (LAB-fx8 section 3): both hook STLs in one design (inserted by the lab script, the drilled one moved 40 mm
# along +y; stop rule A3), Convert Mesh on each in turn with the same camera (S0, F2). Then the rounded box: the lab
# script opens ~/box-round.stl, a 5 s hold with no Convert (S2's end frame), then Convert Mesh on it (Q11).
#   docker exec fx8 bash /work/lab/fx8C.sh
set -u
. /work/lab/fx8lib.sh
take C
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
python3 /work/lab/fx8part.py both "$O" > "$O/both.txt" 2>&1
g 122 50 8; click; nap 1.0; still; nap 2.0
rec_start
ev "recording started: both hook STLs side by side (plain left, drilled right), full window"
nap 3.0
convert_row() {   # convert_row NAME Y: select the Browser row, Surface > Convert Mesh, OK
  ev "convert $1: select the row"
  g 105 "$2" 18; click; nap 1.0
  ev "convert $1: Surface tab"
  g 183 50 18; click; nap 1.2
  ev "convert $1: Convert Mesh button"
  g 684 92 18; click; nap 1.8
  ev "convert $1: OK"
  g 1388 397 14; click; nap 0.8
  still; nap 0.4
  ev "convert $1: result held 4 s"
  nap 4.0
  cp_shot "convert-$1"
}
convert_row hook-plain 335
ev "browser + timeline held 4 s (hook-plain converted)"
g 150 335 14; nap 4.0
convert_row hook 405
cp_shot both
ev "convert hook: Cancel"
g 1322 475 14; click; nap 1.5
still; nap 3.0
read_now c-both
# Q11 + S2: the rounded box
ev "box: opened by the lab script"
python3 /work/lab/fx8part.py open "$O" /root/box-round.stl > "$O/open-box.txt" 2>&1
g 122 50 8; click; nap 0.5; still; nap 1.0
ev "box: S2 end frame, 5 s hold, no Convert"
nap 5.0
cp_shot box-endframe
ev "convert box-round: select the row"
g 105 311 18; click; nap 1.0
ev "convert box-round: Surface tab"
g 183 50 18; click; nap 1.2
ev "convert box-round: Convert Mesh button"
g 684 92 18; click; nap 1.8
ev "convert box-round: OK"
g 1388 397 14; click; nap 0.8
still; nap 0.4
ev "convert box-round: result held 4 s"
nap 4.0
cp_shot box
read_now c-box
g 1322 475 14; click; nap 1.0; still; nap 2.0
ev "recording stopped"
rec_stop
echo "C done"
