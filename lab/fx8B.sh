#!/bin/bash
# fx8 take B (LAB-fx8 section 3): the plain hook converts, then a 5 mm through Hole as a normal feature. Before the
# recording the lab script opens ~/hook-plain.stl over the plug (stop rule A3). On camera: full window 3 s, Convert Mesh,
# the timeline 4 s, Properties (volume), Hole on the back plate (Extents All, 5 mm), the timeline 4 s, Properties after.
#   docker exec fx8 bash /work/lab/fx8B.sh
set -u
. /work/lab/fx8lib.sh
take B
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
python3 /work/lab/fx8part.py open "$O" /root/hook-plain.stl > "$O/open.txt" 2>&1
g 122 50 8; click; nap 1.0; still; nap 2.0
rec_start
ev "recording started: hook-plain.stl opened by the lab script (stop rule A3), full window"
nap 3.0
ev "browser: the mesh body row held 4 s"
g 105 311 18; nap 4.0
ev "convert: select the mesh body"
click; nap 1.0
ev "convert: Surface tab"
g 183 50 18; click; nap 1.2
ev "convert: Convert Mesh button"
g 684 92 18; click; nap 1.8
ev "convert: dialog held 4 s"
g 1300 330 12; nap 4.0
ev "convert hook-plain: OK"
g 1388 397 14; click; nap 2.0
still; nap 0.5
cp_shot converted
ev "convert hook-plain: timeline held 4 s"
g 330 786 16; nap 4.0
cp_shot timeline
read_now b-converted
ev "measure: Inspect tab"
g 105 311 18; click; nap 0.8
g 382 50 18; click; nap 1.0
ev "measure: Properties"
g 229 90 16; click; nap 1.6
ev "measure: volume held 4 s"
g 760 220 14; nap 4.0
cp_shot measure-converted
ev "measure: Close"
g 860 649 16; click; nap 1.5
ev "hole: Model tab"
g 122 50 18; click; nap 1.0
ev "hole: Hole button"
g 296 90 22; click; nap 1.6
ev "hole: click the back plate's face"
g 790 400 22; click; nap 1.6
ev "hole: Extents menu"
g 1355 468 18; click; nap 1.2
ev "hole: All (through)"
g 1310 545 12; click; nap 1.5
ev "hole: diameter 5 mm held 4 s"
g 1360 601 14; nap 4.0
cp_shot hole-panel
ev "hole on converted: OK"
g 1388 682 14; click; nap 2.0
still; nap 0.5
cp_shot hole
ev "hole on converted: timeline held 4 s"
g 360 786 16; nap 4.0
cp_shot hole-timeline
read_now b-hole
ev "measure: Properties after the hole"
g 105 311 18; click; nap 0.8
g 382 50 18; click; nap 1.0
g 229 90 16; click; nap 1.6
ev "measure: volume after held 4 s"
g 760 220 14; nap 4.0
cp_shot measure-hole
ev "measure: Close"
g 860 649 16; click; nap 1.5
g 122 50 18; click; still; nap 2.0
ev "recording stopped"
rec_stop
echo "B done"
