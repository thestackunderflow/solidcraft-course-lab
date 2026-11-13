#!/bin/bash
# fx11 take C (LAB-fx11 section 3): where the part sits (F6, F8 inset, F10; Q4, Q5, Q5b, Q6).
#  1 Q5: ~/tower-sym.sc (off camera), Split Body with XY: bodies, Properties of each.
#  2 Q4: ~/tower.sc (opened on camera, a new tab), Offset Plane 210 from XY, Split with it: the line (C/above.png).
#  3 Q6: Offset Plane 200 from XY; the S2 end frame (5 s, no Split); Split with it; then the planes hidden and the top
#    face (clicked in the view) as the Splitting tool.
#  4 Q5b: ~/block.sc, Offset Plane 40, Split, Properties of each (the F10 your-turn shot).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx11C.sh
set -u
. /work/lab/fx11lib.sh
take C
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc tower-sym; still
rec_start
ev "recording started: full SolidCraft window, ~/tower-sym.sc (pulled both ways from XY, -100 to 100): hold 3 s"
nap 3.0
origin_open
# 1 Q5
split_open
pick_row "Body to split: the tower" $BODY1_ROW
pick_row "Splitting tool: XY in Browser > Origin" $XY_ROW
still
split_state "sym split XY"
cp_shot sym
if [ "$(cat /tmp/fx11/last)" = built ]; then split_ok; else split_cancel; fi
vol c-sym
ev "sym split XY: $(sed 's/.* bodies \([0-9]*\) .*/\1/' "$O/read-c-sym.txt") bodies; $(bodies c-sym | tr '\n' ';')"
cp_shot sym-browser
props $BODY1_ROW sym-props-row1
props $BODY2_ROW sym-props-row2
# 2 Q4
ev "Q4: ~/tower.sc opened (a new tab)"
open_sc tower; still; nap 1.0
origin_open
offset_plane 210 plane210
split_open
pick_row "Body to split: the tower" $BODY1_ROW
pick_row "Splitting tool: Plane1 (210)" 96 592
still
split_state "split 210"
ev "split 210: $(cat /tmp/fx11/last) (line as shown in above.png)"
cp_shot above
split_cancel
vol c-210
ev "after Cancel: timeline $(sed 's/.*timeline //' "$O/read-c-210.txt")"
# 3 Q6
offset_plane 200 plane200
ev "S2 end frame: the tower with the plane at its top face (200), no Split: hold 5 s"
still; nap 5.0
cp_shot s2-frame
split_open
pick_row "Body to split: the tower" $BODY1_ROW
pick_row "Splitting tool: Plane2 (200)" 96 615
still
split_state "split 200"
ev "split 200: $(cat /tmp/fx11/last)"
cp_shot at200
if [ "$(cat /tmp/fx11/last)" = built ]; then split_ok; vol c-200; ev "split 200 built: $(bodies c-200 | tr '\n' ';')"; else split_cancel; fi
ev "the planes hidden (eye on Plane1 and Plane2) so the top face can be clicked"
eye 592; eye 615
split_open
pick_row "Body to split: the tower" $BODY1_ROW
ev "Splitting tool: the tower's top face (clicked in the view)"; g $TOP_FACE 16; click; nap 2.0; still
split_state "split top face"
ev "split top face: $(cat /tmp/fx11/last)"
cp_shot topface
if [ "$(cat /tmp/fx11/last)" = built ]; then split_ok; vol c-topface; ev "split top face built: $(bodies c-topface | tr '\n' ';')"; else split_cancel; fi
vol c-q6
ev "after Q6: timeline $(sed 's/.*timeline //' "$O/read-c-q6.txt")"
# 4 Q5b
ev "Q5b: ~/block.sc opened (a new tab): block 20 x 20, 80 tall, on XY: hold 3 s"
open_sc block; still; nap 3.0
origin_open
offset_plane 40 plane40
split_open
pick_row "Body to split: the block" $BODY1_ROW
pick_row "Splitting tool: Plane1 (40)" 96 568
still
split_state "block split 40"
cp_shot block-split
if [ "$(cat /tmp/fx11/last)" = built ]; then split_ok; else split_cancel; fi
vol c-block
ev "block split 40: $(sed 's/.* bodies \([0-9]*\) .*/\1/' "$O/read-c-block.txt") bodies; $(bodies c-block | tr '\n' ';')"
props $BODY1_ROW block-props-row1
props $BODY2_ROW block-props-row2
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "C done"
