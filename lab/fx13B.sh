#!/bin/bash
# fx13 take B (LAB-fx13 section 3): the fix. ~/cup.sc; Shell; the Tangent chain checkbox (ticked) then unticked; the
# top only; 2 mm; OK (Q2: built?); Properties (33,900.00 pre-registered); section XZ; Measure the side wall (outer
# side to inner side: Min) and the floor (inner floor to the outer bottom, picked from below) (Q7: 2.00 / 2.00);
# Home; section off; the hollow cup turning 5 s (F11).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx13B.sh
set -u
. /work/lab/fx13lib.sh
take B
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc cup; still
rec_start
ev "recording started: full SolidCraft window, ~/cup.sc: hold 3 s"
nap 3.0
shell_open dialog
chain_off untick
pick "click the top face at (0, 0, 80), chain off" $TOP60
ev "preview on the top pick, chain off, as shown in preview.png: hold 4 s"; nap 4.0; cp_shot preview
thick "2 mm"
cp_shot before-ok
ev "OK"; g $SH_OK 14; click; nap 3.0; still; cp_shot after-ok
vol b-after
ev "shell top chain off: $(cut -c1-300 "$O/read-b-after.txt")"
props_body props
section_xz
ev "the hollow cup in section as shown in section.png: hold 3 s"; nap 3.0; cp_shot section
inspect_tab; ev "Inspect > Measure"; g $MEASURE_BTN 16; click; nap 2.0
ev "Measure: the outer side face"; g $OUT_SIDE_SEC 14; click; nap 1.5
ev "Measure: the inner side face"; g $IN_SIDE_SEC 14; click; nap 2.0; still
ev "side wall (Min) as shown in wall.png: hold 4 s"; nap 4.0; cp_shot wall
ev "Measure: clear"; g $ME_ITEMS_X 14; click; nap 1.5
ev "Measure: the inner floor"; g $FLOOR_SEC 14; click; nap 1.5
ev "view from below (the gizmo's -Z)"; g $GIZMO_MINUS_Z 14; click; nap 2.5
ev "Measure: the outer bottom face"; g $BOTTOM_FROM_BELOW 14; click; nap 2.0; still
ev "floor as shown in floor.png: hold 4 s"; nap 4.0; cp_shot floor
ev "Measure: close"; g $ME_CLOSE_X 14; click; nap 1.5
home_view
ev "the hollow cup in section, Home view: hold 2 s"; nap 2.0; cp_shot section-home
section_off
ev "F11: the hollow cup turning"; orbit 5
cp_shot hollow
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "B done"
