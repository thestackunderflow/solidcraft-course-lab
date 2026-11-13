#!/bin/bash
# fx11 take B, step 5 (Q3, logged only), attempt 2 in its own container (out/fx11/B-q3): in take B the plug's `open` of
# ~/tower.sc went back to the open, already split tab (no new tab), so the Midplane was made in the split design and
# the Split pick missed (DEVIATIONS). Here: ~/tower.sc opened off camera; Midplane between XY (the base face's plane; the
# base face cannot be clicked in this view) and the top face; Split Body, the tower, that plane; the bodies read.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx11Bq3.sh
set -u
. /work/lab/fx11lib.sh
take B-q3
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc tower; still
rec_start
ev "recording started: full SolidCraft window, ~/tower.sc: hold 3 s"
nap 3.0
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
vol q3-mid
ev "midplane: timeline $(sed 's/.*timeline //' "$O/read-q3-mid.txt")"
cp_shot midplane
split_open
pick_row "Body to split: the tower" $BODY1_ROW
pick_row "Splitting tool: Plane1 (the midplane)" 96 592
still
split_state "split midplane"
cp_shot midplane-split
if [ "$(cat /tmp/fx11/last)" = built ]; then split_ok; else split_cancel; fi
vol q3-split
ev "midplane split: $(bodies q3-split | tr '\n' ';')"
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "B-q3 done"
