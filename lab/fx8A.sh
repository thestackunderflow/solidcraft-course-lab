#!/bin/bash
# fx8 take A (LAB-fx8 section 3): the refusals on a mesh. Before the recording (stop rule A3: File > Insert Mesh... opens
# no file window under Xvfb): the lab script opens ~/hook.stl over the plug and sketches one 5 mm circle on the back
# plate's inner face (lab/fx8sketch.py). On camera: full window 3 s, the Browser's mesh body row 4 s, Extrude cut
# (refused), Hole on the mesh (extra, refused), Fillet (refused), Properties (size + volume), Convert Mesh (refused),
# Create Issue... draft (title only, closed, not submitted).
#   docker exec fx8 bash /work/lab/fx8A.sh
set -u
. /work/lab/fx8lib.sh
take A
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
python3 /work/lab/fx8part.py open "$O" /root/hook.stl > "$O/open.txt" 2>&1
python3 /work/lab/fx8sketch.py "$O" > "$O/sketch.txt" 2>&1
g 122 50 8; click; nap 1.0; still; nap 2.0                      # Model tab
rec_start
ev "recording started: hook.stl opened by the lab script (stop rule A3), full window"
nap 3.0
ev "browser: the mesh body row held 4 s"
g 91 311 18; nap 4.0
cp_shot browser-row
still; nap 1.0
# 1. Extrude cut through the plate from the circle
ev "cut: Extrude button"
g 194 90 22; click; nap 1.6
ev "cut: pick the circle"
g 793 407 22; click; nap 1.4
ev "cut: Operation menu"
g 1350 437 18; click; nap 1.2
ev "cut: Cut"
g 1301 514 12; click; nap 1.4
ev "cut: Reverse (into the plate)"
g 1325 497 14; click; nap 1.5
ev "cut: refusal shown, hold 4 s"
g 1300 610 12; nap 4.0
cp_shot cut
ev "cut: OK"
g 1388 656 14; click; nap 0.3
cp_shot cut-after-ok
nap 3.0
ev "cut: Cancel"
g 1322 656 12; click; nap 1.5
still; nap 1.0
# 1b. Hole on the mesh (extra; the same idea as the tool you'd reach for first)
ev "hole on mesh: Hole button"
g 296 90 22; click; nap 1.6
ev "hole on mesh: click the plate face"
g 765 470 22; click; nap 1.6
ev "hole on mesh: refusal shown, hold 4 s"
g 1300 740 12; nap 4.0
cp_shot hole
ev "hole on mesh: Cancel"
g 1322 777 12; click; nap 1.5
still; nap 1.0
# 2. Fillet one edge of the mesh
ev "fillet on mesh: Fillet button"
g 353 90 22; click; nap 1.6
ev "fillet on mesh: click the plate's top edge"
g 790 195 22; click; nap 1.6
ev "fillet on mesh: refusal shown, hold 4 s"
g 1270 570 12; nap 4.0
cp_shot fillet
ev "fillet on mesh: Cancel"
g 1322 629 12; click; nap 1.5
still; nap 1.0
# 3. Measure: Inspect > Properties on the mesh body
ev "measure: select the mesh body"
g 91 311 18; click; nap 1.0
ev "measure: Inspect tab"
g 382 50 18; click; nap 1.0
ev "measure: Properties"
g 229 90 16; click; nap 1.6
ev "measure: volume and bounding box held 4 s"
g 760 220 14; nap 4.0
cp_shot measure
ev "measure: Close"
g 860 649 16; click; nap 1.5
# 4. Convert Mesh
ev "convert: select the mesh body"
g 91 311 18; click; nap 1.0
ev "convert: Surface tab"
g 183 50 18; click; nap 1.2
ev "convert: Convert Mesh button"
g 684 92 18; click; nap 1.8
ev "convert: dialog held 4 s"
g 1300 330 12; nap 4.0
cp_shot convert-dialog
ev "convert hook.stl: OK"
g 1388 397 14; click; nap 0.6
still; nap 0.6
ev "convert hook.stl: refusal shown, hold 4 s"
nap 4.0
cp_shot convert
ev "report: Create Issue..."
g 1251 425 16; click; nap 2.0
ev "report: draft title held 4 s"
g 600 128 14; nap 4.0
cp_shot report
ev "report: Close draft"
g 734 670 16; click; nap 1.5
ev "convert: Cancel"
g 1322 475 14; click; nap 1.5
still; nap 2.0
ev "recording stopped"
rec_stop
read_now a-after
echo "A done"
