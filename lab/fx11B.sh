#!/bin/bash
# fx11 take B (LAB-fx11 section 3): the fix (F2, F5, F7 right, F11; Short S1). ~/tower.sc opened off camera; Offset Plane
# from XY, 100 (Q2); Split Body, the tower, Plane1; the Browser; Properties of each body (right-click > Properties) held
# 4 s; F11: each piece hidden in turn (the eye), no new geometry; then Q3 (logged only): ~/tower.sc opened again, a
# Midplane between XY (the base face's plane; the base face cannot be clicked in this view) and the top face, Split with it.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx11B.sh
set -u
. /work/lab/fx11lib.sh
take B
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc tower; still
rec_start
ev "recording started: full SolidCraft window, ~/tower.sc: hold 3 s"
nap 3.0
origin_open
offset_plane 100 offset
vol b-plane
ev "offset plane 100: $(grep -q Plane1 "$O/read-b-plane.txt" && echo made || echo 'not made'); timeline $(sed 's/.*timeline //' "$O/read-b-plane.txt")"
split_open
pick_row "Body to split: the tower (Browser > Bodies > Tower)" $BODY1_ROW
pick_row "Splitting tool: Plane1 (Browser > Construction)" 96 592
still
split_state "split 100"
cp_shot split-preview
if [ "$(cat /tmp/fx11/last)" = built ]; then split_ok; else cp_shot split-refused; split_cancel; fi
vol b-split
ev "split 100: $(sed 's/.* bodies \([0-9]*\) .*/\1/' "$O/read-b-split.txt") bodies; $(bodies b-split | tr '\n' ';')"
ev "the Browser: two body rows: hold 4 s"; g 100 486 14; nap 4.0; still
cp_shot browser
props $BODY1_ROW props-row1
props $BODY2_ROW props-row2
ev "F11: hide the first body (eye): hold 3 s"; eye $(row_y "$BODY1_ROW"); nap 3.0; cp_shot hide-row1
ev "show it again"; eye $(row_y "$BODY1_ROW"); nap 1.0
ev "F11: hide the second body (eye): hold 3 s"; eye $(row_y "$BODY2_ROW"); nap 3.0; cp_shot hide-row2
ev "show it again"; eye $(row_y "$BODY2_ROW"); nap 2.0
# Q3 (logged only)
ev "Q3: ~/tower.sc opened again (a new tab, unsplit)"
open_sc tower; still; nap 1.0
origin_open
model_tab
ev "Midplane (Model > Construct > Midplane): hold 2 s"
g $CONSTRUCT_DD 18; click; nap 1.5; g $MIDPLANE_ITEM 18; click; nap 2.0; still; nap 2.0
cp_shot midplane-dialog
pick_row "First plane: XY (Browser > Origin; the base face's plane)" $XY_ROW
ev "Second plane: the tower's top face (clicked in the view)"; g $TOP_FACE 16; click; nap 2.0; still; nap 2.0
cp_shot midplane-picks
p=$(okpos)
if [ "${p%% *}" = blue ]; then ev "Midplane: OK enabled"; g $MP_OK 14; click; nap 2.5; still; else ev "Midplane: OK greyed (refused)"; fi
vol b-mid
ev "midplane: timeline $(sed 's/.*timeline //' "$O/read-b-mid.txt")"
python3 - "$O/read-b-mid.json" > "$O/midplane-z.txt" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))['design']
print(json.dumps([f for f in d.get('timeline') or [] if 'Plane' in (f.get('type') or '')])[:1500])
PY
split_open
pick_row "Body to split: the tower" $BODY1_ROW
pick_row "Splitting tool: Plane1 (the midplane)" 96 592
still
split_state "split midplane"
cp_shot midplane-split
if [ "$(cat /tmp/fx11/last)" = built ]; then split_ok; else split_cancel; fi
vol b-mid-split
ev "midplane split: $(bodies b-mid-split | tr '\n' ';')"
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "B done"
