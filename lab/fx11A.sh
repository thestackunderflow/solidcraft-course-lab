#!/bin/bash
# fx11 take A (LAB-fx11 section 3): the refusal (F0, F1, F4, F7 left; Short S0). ~/tower.sc opened off camera; full
# window 3 s; a slow orbit; Browser > Origin expanded, XY lit; Split Body (Model > Modify > Split Body): Body to split =
# the tower (Browser row), Splitting tool = Browser > Origin > XY: the line (Q1); Create Issue... draft (not submitted);
# Cancel; the timeline read; then F1's section view (Inspect > Section, XZ) for 2 s, cancelled.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx11A.sh
set -u
. /work/lab/fx11lib.sh
take A
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc tower; still
vol a-before
rec_start
ev "recording started: full SolidCraft window, ~/tower.sc (the tower on XY, 0 to 200): hold 3 s"
nap 3.0
orbit
origin_open
ev "XY lit: the Browser row clicked (the plane under the tower's base): hold 3 s"
g $XY_ROW 16; click; nap 1.0; still; nap 3.0
cp_shot origin
xdotool key Escape; nap 1.0
split_open
cp_shot dialog
pick_row "Body to split: the tower (Browser > Bodies > Tower)" $BODY1_ROW
pick_row "Splitting tool: XY in Browser > Origin" $XY_ROW
still
split_state "split XY"
ev "split XY: $(cat /tmp/fx11/last) (line as shown in refusal.png)"
cp_shot refusal
if [ "$(cat /tmp/fx11/last)" = refused ]; then
  ev "Create Issue... (draft only, not submitted)"
  g $S_ISSUE 14; click; nap 2.5; still
  ev "report draft: hold 4 s"; nap 4.0
  cp_shot report
  ev "Close draft"; g $ISSUE_CLOSE 14; click; nap 1.5; still
fi
split_cancel
vol a-after-cancel
ev "after Cancel: timeline $(sed 's/.*timeline //' "$O/read-a-after-cancel.txt")"
# F1: a 2 s section through the bore
g $INSPECT_TAB 16; click; nap 1.0
ev "F1: Inspect > Section, Plane = XZ: hold 3 s"
g $SECTION_BTN 16; click; nap 2.0; g $XZ_ROW 16; click; nap 2.0; still; nap 3.0
cp_shot section
ev "Cancel (section)"; g $SEC_CANCEL 14; click; nap 1.5; still
model_tab
vol a-after
ev "after: timeline $(sed 's/.*timeline //' "$O/read-a-after.txt")"
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "A done"
