#!/bin/bash
# fx10 take B (LAB-fx10 section 3): the fix. ~/knob-full.sc opened off camera; full window 3 s; Sketch1 edited: the
# five lines left of / across the axis deleted one by one (cap side, cap underside, stem side, cap end, stem end), the
# outline closed along the axis with the Line tool from the stem's corner to the origin, down the axis, to the cap's
# corner (snapped to the origin and the corners; vertical inferred); Finish; Revolve 360 about Z; Measure the cap's
# diameter; Properties (volume, bounding box = height).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx10B.sh
set -u
. /work/lab/fx10lib.sh
take B
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_knob knob-full; still
rec_start
ev "recording started: full SolidCraft window, ~/knob-full.sc (the whole T): hold 3 s"
nap 3.0
expand_origin
ev "double-click Sketch1 (edit the sketch)"
g $SKETCH1_ROW 16; dclick; nap 2.5; still
ev "the whole T in the sketch view, the axis through the middle: hold 3 s"; nap 3.0
cp_shot full-sketch
for spec in "-15 -21:the cap's left side" "-13 -15:the cap's left underside" "-6 -4.5:the stem's left side" \
            "-7 -23:the cap's end across the axis" "-3 0:the stem's end across the axis"; do
  xy=${spec%%:*}; what=${spec#*:}
  ev "select $what, Delete"
  g $(sk $xy) 18; click; nap 0.8; xdotool key Delete; nap 1.2; still
done
ev "the right half left, open along the axis: hold 3 s"; nap 3.0
cp_shot half-open
ev "Line tool: from the stem's corner to the origin, down the axis, to the cap's corner"
g $LINE_TOOL 16; click; nap 1.0
g $(sk 6 0) 18; nap 0.5; click; nap 0.8
g $(sk 0 0) 18; nap 0.5; click; nap 0.8
g $(sk 0 -23) 20; nap 0.5; click; nap 0.8
g $(sk 15 -23) 20; nap 0.5; click; nap 0.8
xdotool key Escape; nap 0.8; xdotool key Escape; nap 1.0; still
ev "the half outline, closed on the axis (constraint icons as shown): hold 4 s"; nap 4.0
cp_shot half-closed
ev "Finish Sketch"
g $FINISH_BTN 16; click; nap 2.5; still
FX9_ALLOW=1 python3 /work/lab/fx9.py raw "$O" execute '{"command":"timeline.inspect","params":{"feature":"Sketch1"}}' > "$O/sketch1-inspect.json" 2>&1
revolve_open
pick_z
revolve_state "revolve half 360"
ev "revolve half: $(cat /tmp/fx10/last)"
cp_shot preview
[ "$(cat /tmp/fx10/last)" = built ] && revolve_ok
home_view
ev "the knob: hold 4 s"; nap 4.0
cp_shot knob
vol b-after
ev "after: volume $(sed 's/.*volume \([^ ]*\).*/\1/' "$O/read-b-after.txt"); timeline $(sed 's/.*timeline //' "$O/read-b-after.txt")"
measure_edge 838 421 measure
props props
g $MODEL_TAB 16; click; nap 1.0; still
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "B done"
