#!/bin/bash
# fx9 take A (LAB-fx9 section 3): the refusal. ~/nut.sc opened off camera; full window 3 s; the Hole (diameter 8) held
# 4 s; Thread from Model > Create; the pre-fill (Q2); Automatic size off, Size 8 mm FIRST, then Modeled; the line;
# Create Issue... draft (not submitted); OK; then M10 on the same hole (Q3); volume after.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx9A.sh
set -u
. /work/lab/fx9lib.sh
take A
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_nut nut; still
vol a-before
rec_start
ev "recording started: full SolidCraft window, ~/nut.sc (8 mm hole): hold 3 s"
nap 3.0
ev "the Hole in the timeline: double-click to show its diameter"
g $HOLE_TL 20; dclick; nap 2.0; still
ev "Hole diameter 8: hold 4 s"; nap 4.0
cp_shot hole8
g $H_CANCEL 14; click; nap 1.5; still
thread_open
cp_shot dialog
ev "Q2 Automatic size suggestion: hold 2 s"; nap 2.0
cp_shot auto
thread_m8 size8
cp_shot refusal
thread_ok "M8 in 8"
ev "M8 in 8: $(cat /tmp/fx9/last) (line as shown in refusal.png)"
cp_shot refusal-held
ev "Create Issue... (draft only, not submitted)"
g $T_ISSUE 14; click; nap 2.5; still
ev "report draft: hold 4 s"; nap 4.0
cp_shot report
g $ISSUE_CLOSE 14; click; nap 1.5; still
ev "click the greyed OK"
g $T_OK_ERR 14; click; nap 3.0; still
cp_shot after-ok
vol a-after-ok
ev "after OK: timeline $(sed 's/.*timeline //' "$O/read-a-after-ok.txt")"
ev "Q3: Size 10 mm (M10), Modeled still ticked, same hole"
g $T_SIZE 12; click; nap 1.0; g $T_SIZE10 10; click; nap 3.0; still
cp_shot m10
thread_ok "M10 in 8"
ev "M10 in 8: $(cat /tmp/fx9/last)"
cp_shot m10-held
if [ "$(cat /tmp/fx9/last)" = refused ]; then ev "Cancel"; g $T_CANCEL_ERR 14; click; nap 2.0; still; fi
cp_shot after
vol a-after
ev "volume after: $(sed 's/.*volume \([^ ]*\).*/\1/' "$O/read-a-after.txt"); timeline $(sed 's/.*timeline //' "$O/read-a-after.txt")"
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "A done"
