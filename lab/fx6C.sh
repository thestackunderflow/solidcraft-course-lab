#!/bin/bash
# fx6 take C part 1 (LAB-fx6 take C steps 1-3): Parameters thickness 5 to 8 (held 4 s), the lip's faces read, the same
# edge at 6 mm (built = a curved face in the read; then toolbar Undo), thickness back to 5.
#   docker exec fx6 bash /work/lab/fx6C.sh [PASS]      PASS=clean: the second, clean pass (no read events between)
set -u
. /work/lab/fx6lib.sh
P=${1:-1}
if [ "$P" = 1 ]; then take C; [ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
else take C-clean; fi
: > "$O/results.txt"
still; sleep 1
rec_start
ev "recording started: take C pass $P, full window"
nap 3.0
thick() {   # thick V
  ev "params: open (thickness to $1)"
  g $PARAMS_BTN 24; click; nap 1.5
  ev "params: thickness box"
  g $THICK_BOX 20; click; xdotool key ctrl+a; nap 0.3; typed "$1" 200; nap 0.5; xdotool key Return; nap 1.5
  g 900 551 14
  ev "params: thickness $1 held 4 s"
  nap 4.0
  cp_shot "params-thickness$1-p$P"
  ev "params: OK"
  g $PARAMS_OK 20; click; nap 2.0; still; nap 1.0
}
thick 8
read_now "thick8-p$P"
ev "thickness 8: rebuilt"
ev "thick-8: hold 3 s on the hook"
nap 3.0
ev "fillet 6 (thickness 8): Fillet button"
g $FILLET_BTN 22; click; nap 1.4
ev "fillet 6 (thickness 8): lip outer top edge"
g $LIP_EDGE 24; nap 0.6; click; nap 1.2
ev "fillet 6 (thickness 8): radius typed"
radius 6
cp_shot "thick8-radius6-p$P"
ev "fillet 6 (thickness 8): OK"
g $OK_BTN 18; click; nap 3.0
n=$(python3 /work/lab/fx6hook.py read "$O" "thick8-r6-p$P" | tee "$O/read-thick8-r6-p$P.txt" | python3 -c "import sys,json; l=sys.stdin.read(); print(json.loads(l.split(' lip ',1)[1])['curved_faces'])")
if [ "$n" -gt 0 ]; then
  still; ev "thick-8 fillet 6: built (curved faces $n), hold 5 s"; echo "thick8 6 built" >> "$O/results.txt"
  nap 5.0; cp_shot "thick8-p$P"
  ev "toolbar Undo"; g 215 15 18; click; nap 2.0; still
else
  cp_shot "thick8-p$P"; ev "thick-8 fillet 6: refused (panel open)"; echo "thick8 6 refused" >> "$O/results.txt"
  nap 3.0; g 1322 658 18; click; nap 1.5; still
fi
read_now "thick8-undone-p$P"
thick 5
read_now "thick5-back-p$P"
ev "recording stopped"
rec_stop
cat "$O/results.txt"
