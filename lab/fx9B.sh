#!/bin/bash
# fx9 take B (LAB-fx9 section 3): the fix. ~/nut.sc opened off camera; full window 3 s; Hole1 diameter 8 -> 6.75 (held
# 4 s); Thread, Automatic size off, Size 8 mm, Modeled, OK; the teeth (section on XZ, close-up, low angle); Properties.
# Volumes before/after and the bore's smallest diameter read off camera over the plug (fx9.py read / bore).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx9B.sh
set -u
. /work/lab/fx9lib.sh
take B
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_nut nut; still
vol b-before
rec_start
ev "recording started: full SolidCraft window, ~/nut.sc (8 mm hole): hold 3 s"
nap 3.0
hole_edit 6.75 hole675
vol b-hole675
ev "Hole1 now 6.75: volume $(sed 's/.*volume \([^ ]*\).*/\1/' "$O/read-b-hole675.txt"); timeline $(sed 's/.*timeline //' "$O/read-b-hole675.txt")"
cp_shot hole675-done
thread_open
cp_shot dialog
thread_m8 size8
cp_shot preview
thread_ok "M8 in 6.75"
ev "M8 in 6.75: $(cat /tmp/fx9/last)"
cp_shot thread
[ "$(cat /tmp/fx9/last)" = refused ] && { cp_shot refused; g $T_CLOSE 14; click; nap 2.0; }
vol b-after
ev "after: volume $(sed 's/.*volume \([^ ]*\).*/\1/' "$O/read-b-after.txt"); timeline $(sed 's/.*timeline //' "$O/read-b-after.txt")"
ev "the threaded nut: hold 4 s"; nap 4.0
cp_shot thread-held
ev "section: Inspect > Section, plane XZ (Browser > Origin > XZ), OK"
g $INSPECT_TAB 20; click; nap 1.0
g $SECTION_BTN 14; click; nap 1.5
g $ORIGIN_ROW 20; click; nap 1.0
g $XZ_ROW 12; click; nap 1.5
g $SECTION_OK 20; click; nap 3.0; still
ev "section view: hold 4 s"; nap 4.0
cp_shot section
ev "close-up of the teeth: zoom at the cut wall"
g 760 360 20; nap 0.5
for i in 1 2 3 4 5 6; do xdotool click 4; sleep 0.35; done; nap 2.0; still
ev "teeth close-up: hold 4 s"; nap 4.0
cp_shot teeth
ev "low angle: a slow middle-button tilt"
g 1000 450 10; xdotool mousedown 2
for i in $(seq 1 30); do xdotool mousemove_relative -- 0 -4; sleep 0.05; done
xdotool mouseup 2; nap 1.5; still
ev "teeth, low angle: hold 4 s"; nap 4.0
cp_shot teeth-low
ev "home view"
g $HOME_BTN 14; click; nap 2.0; still
ev "Properties (Inspect > Properties)"
g $PROPS_BTN 14; click; nap 2.5; still
ev "Properties: hold 4 s"; nap 4.0
cp_shot props
ev "recording stopped"
rec_stop
FX9_ALLOW=1 python3 /work/lab/fx9.py bore "$O" b-after > "$O/bore.txt" 2>&1; cat "$O/bore.txt"
ev "bore (off camera, STL vertices): $(cat "$O/bore.txt" | head -c 400)"
echo "B done"
