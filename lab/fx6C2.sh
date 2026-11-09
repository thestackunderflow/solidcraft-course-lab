#!/bin/bash
# fx6 take C2 (LAB-fx6): thickness 5; the outer bottom-back edge (x = 0, z = 0, along the width) at 6 mm. The edge is
# hidden in the home view, so the view turns to the back (the gizmo's -X ball, on camera) and the edge is picked on the
# bottom line of the back face; the read names the edge the round sits on. Built: hold 5 s, toolbar Undo; home view.
set -u
. /work/lab/fx6lib.sh
take C2
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
still; sleep 1
rec_start
ev "recording started: take C2, full window (thickness 5)"
nap 3.0
read_now c2-before
ev "view: back (gizmo -X)"
g 1367 185 22; click; nap 2.0; still; nap 2.0
ev "fillet 6 (bottom-back): Fillet button"
g $FILLET_BTN 22; click; nap 1.4
ev "fillet 6 (bottom-back): bottom edge of the back face"
g 642 676 24; nap 0.6; click; nap 1.2
cp_shot edge-picked
ev "fillet 6 (bottom-back): radius typed"
radius 6
ev "fillet 6 (bottom-back): OK"
g $OK_BTN 18; click; nap 3.0
python3 /work/lab/fx6hook.py read "$O" c2-r6 > "$O/read-c2-r6.txt"
n=$(python3 -c "import json; d=json.load(open('$O/read-c2-r6.json')); print(sum(1 for f in d['topology']['faces'] if f.get('cylinder')))")
if [ "$n" -gt 0 ]; then
  still; ev "bottom-back 6: built (curved faces $n), hold 5 s"; nap 5.0; cp_shot edge
  ev "toolbar Undo"; g 215 15 18; click; nap 2.0; still
else
  cp_shot edge; ev "bottom-back 6: refused (panel open)"; nap 3.0; g 1322 658 18; click; nap 1.5; still
fi
read_now c2-undone
ev "view: home"
g 870 737 20; click; nap 2.0; still; nap 2.0
ev "recording stopped"
rec_stop
