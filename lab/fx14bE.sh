#!/bin/bash
# fx14b take E (LAB-fx14b section 3; F8 inset, question card, Short S2; Q21, Q23, Q25, Q28).
# 1. Q25: ~/conv.sc; the History bar's ConvertMesh1 icon double-clicked (the tooltip says "Double-click to edit"), then
#    right-click > Edit Feature; the same for the first icon (conv, the Insert Mesh step); every field recorded as seen.
# 2. Q21: ~/block.sc (plain Extrude); 5 s hold; Create Sketch, click the top: attaches? Cancel (Sketch tab > Cancel).
# 3. Q23: ~/conv3.sc; Model > Extrude, click the top FACE (no sketch), Distance 5, OK: the line or built.
# 4. Q28 (recorded only): ~/offset.sc; Create Sketch, click the top at (20, 15, 25): attaches?
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx14bE.sh
set -u
. /work/lab/fx14blib.sh
take E
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc conv; g $HOME_BTN 16; click; nap 2.0; still
rec_start
ev "recording started: full SolidCraft window, ~/conv.sc: hold 3 s"
nap 3.0
ev "Q25: History bar: ConvertMesh1 icon hovered: hold 2 s"; g $HIST_CONVERT 16; nap 2.0; cp_shot convert-tip
ev "Q25: double-click ConvertMesh1"; dclick; nap 3.0; still
ev "Q25: after the double-click as shown in convert-edit.png: hold 3 s"; nap 3.0; cp_shot convert-edit
xdotool key Escape; nap 1.0
ev "Q25: right-click ConvertMesh1"; g $HIST_CONVERT 16; nap 1.0; xdotool click 3; nap 1.5; cp_shot convert-menu
ev "Q25: Edit Feature"; g 415 532 14; click; nap 3.0; still
ev "Q25: after Edit Feature (ConvertMesh1) as shown in convert-edit2.png: hold 3 s"; nap 3.0; cp_shot convert-edit2
xdotool key Escape; nap 1.0
ev "Q25: History bar: the first icon (conv, Insert Mesh) hovered: hold 2 s"; g $HIST_INSERT 16; nap 2.0; cp_shot insert-tip
ev "Q25: right-click the first icon"; xdotool click 3; nap 1.5; cp_shot insert-menu
ev "Q25: Edit Feature"; g 385 532 14; click; nap 3.0; still
ev "Q25: after Edit Feature (Insert Mesh) as shown in insert-edit.png: hold 3 s"; nap 3.0; cp_shot insert-edit
xdotool key Escape; nap 1.0
ev "Q25: Search commands: mesh (menu names) as shown in search.png: hold 4 s"
g $SEARCH_BOX 16; click; nap 1.0; typed "mesh" 140; nap 2.0; still; nap 4.0; cp_shot search
xdotool key Escape; nap 1.0
ev "Q21: open ~/block.sc (a plain Extrude, not converted)"
open_sc block; home_view
ev "Q21: the plain block: hold 5 s"; nap 5.0; cp_shot block
sk_dialog_face $TOP_FACE "Q21: click the top at (20, 15, 20)"
ev "sketch on extruded top: as shown in control.png: hold 4 s"; nap 4.0; cp_shot control
ev "Cancel (Sketch tab > Cancel)"; g $SK_CANCEL 14; click; nap 2.0; still; cp_shot control-after
ev "Q23: open ~/conv3.sc (a fresh copy of the converted block)"
open_sc conv3; home_view
model_tab
ev "Q23: Model > Extrude"; g $EXTRUDE_BTN 16; click; nap 2.0; still
pick "Q23: click the top FACE (no sketch)" $TOP_FACE
ev "Q23: Distance 5 mm (typed), Tab"; g $EX_DIST 16; click; xdotool key ctrl+a; typed "5 mm" 140; xdotool key Tab; nap 2.0; still
ev "Q23: the Extrude dialog as shown in extrude-dialog.png: hold 4 s"; nap 4.0; cp_shot extrude-dialog
ev "Q23: OK"; g $EX_OK 14; click; nap 3.0; still
ev "extrude face: as shown in extrude-face.png: hold 4 s"; nap 4.0; cp_shot extrude-face
vol e-after-extrude
ev "Q23 after OK: $(cut -c1-200 "$O/read-e-after-extrude.txt")"
xdotool key Escape; nap 1.0; still
ev "Q28: open ~/offset.sc (Extrude with a start offset 5, top at z 25)"
open_sc offset; home_view
sk_dialog_face $TOP_FACE "Q28: click the top at (20, 15, 25)"
ev "sketch on offset-start top: as shown in offset.png: hold 4 s"; nap 4.0; cp_shot offset
ev "Cancel (Sketch tab > Cancel)"; g $SK_CANCEL 14; click; nap 2.0; still; cp_shot offset-after
vol e-after
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "E done"
