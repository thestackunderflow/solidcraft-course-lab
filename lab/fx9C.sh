#!/bin/bash
# fx9 take C (LAB-fx9 section 3): the window (F6) and the tapped hole (Q6). For each X in 6.3 6.5 7.6 7.7: a fresh copy
# of ~/nut.sc opened off camera (cp + the plug's `open`, a new tab), Hole1 diameter X in the timeline, Thread M8 Modeled.
# Then Q6: a fresh copy, the Hole dialog's tapped option (Edit Hole > Hole Tap Type: Tapped, Size M8), the Tap drill
# diameter held 4 s, OK, then Thread M8 Modeled on it. Off camera first: the bore of the unthreaded 6.75 nut (the
# STL-vertex method's check, for take B's bore number).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx9C.sh
set -u
. /work/lab/fx9lib.sh
take C
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_nut nut-675
FX9_ALLOW=1 python3 /work/lab/fx9.py bore "$O" c-675-unthreaded > "$O/bore-unthreaded.txt" 2>&1; cat "$O/bore-unthreaded.txt"
fresh() { cp /work/out/fx9/P/nut.sc "$HOME/nut-$1.sc"; FX9_ALLOW=1 python3 /work/lab/fx9.py open "$HOME/nut-$1.sc" > "$O/open-$1.txt" 2>&1; sleep 3; still; }
fresh 6.3
rec_start
for DIA in 6.3 6.5 7.6 7.7; do   # not X: glide sets X and Y (xdotool --shell)
  [ "$DIA" != 6.3 ] && { ev "fresh copy of ~/nut.sc for $DIA (opened off camera, new tab)"; fresh "$DIA"; nap 1.0; }
  ev "try $DIA: full window, hold 3 s"; nap 3.0
  hole_edit "$DIA" "hole$DIA"
  thread_open
  thread_m8 "size8-$DIA"
  cp_shot "$DIA"
  thread_ok "M8 in $DIA"
  r=$(cat /tmp/fx9/last)
  [ "$r" = built ] && cp_shot "$DIA-built"
  vol "c-$DIA"
  ev "M8 in $DIA: $r (see $DIA.png); timeline $(sed 's/.*timeline //' "$O/read-c-$DIA.txt"); volume $(sed 's/.*volume \([^ ]*\).*/\1/' "$O/read-c-$DIA.txt")"
  [ "$r" = refused ] && { ev "close the dialog (title-bar X)"; g $T_CLOSE 14; click; nap 2.0; still; }
done
ev "Q6: fresh copy of ~/nut.sc (opened off camera, new tab)"; fresh tap; nap 1.0
ev "Q6: full window, hold 3 s"; nap 3.0
ev "double-click Hole1 in the timeline"
g $HOLE_TL 20; dclick; nap 2.0
ev "Hole Tap Type: Tapped"
g $H_TAP 16; click; nap 1.0; g $H_TAPPED 10; click; nap 2.0
ev "Size: M8"
g $H_TSIZE 14; click; nap 1.0; g $H_TM8 10; click; nap 2.0; still
ev "Tap drill diameter shown: hold 4 s"; nap 4.0
cp_shot tapdrill
ev "OK"
g $H_OK_TAPPED 14; click; nap 3.0; still
vol c-tapped-hole
ev "tapped hole: timeline $(sed 's/.*timeline //' "$O/read-c-tapped-hole.txt"); volume $(sed 's/.*volume \([^ ]*\).*/\1/' "$O/read-c-tapped-hole.txt")"
thread_open
cp_shot tapped-dialog
thread_m8 size8-tapped
cp_shot tapped-preview
thread_ok "M8 in the tapped hole"
r=$(cat /tmp/fx9/last)
cp_shot tapped
vol c-tapped
ev "M8 in the tapped hole: $r; timeline $(sed 's/.*timeline //' "$O/read-c-tapped.txt"); volume $(sed 's/.*volume \([^ ]*\).*/\1/' "$O/read-c-tapped.txt")"
[ "$r" = refused ] && { g $T_CLOSE 14; click; nap 2.0; still; }
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
FX9_ALLOW=1 python3 /work/lab/fx9.py bore "$O" c-tapped > "$O/bore-tapped.txt" 2>&1; cat "$O/bore-tapped.txt"
echo "C done"
