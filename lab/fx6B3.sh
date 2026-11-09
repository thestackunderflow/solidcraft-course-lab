#!/bin/bash
# fx6 take B part 3: F2 filmed cleanly at the largest built radius (5), full window 3 s, OK, hold 5 s on the round;
# then the toolbar's Undo (checked 8,500) and the recording stops.
set -u
. /work/lab/fx6lib.sh
ev 'fillet 5.1: refused "not supported yet: the blend is larger than the neighbouring faces; the largest radius that fits is 5 mm"'
still
ev "F2 clean: full window 3 s"
nap 3.0
ev "F2 clean: Fillet button"
g $FILLET_BTN 22; click; nap 1.4
ev "F2 clean: lip outer top edge"
g $LIP_EDGE 24; nap 0.6; click; nap 1.2
ev "F2 clean: radius 5 typed"
radius 5
cp_shot F2-radius5
ev "F2 clean: OK"
g $OK_BTN 18; click; nap 2.0
still
ev "F2 clean: the round held 5 s"
nap 5.0
cp_shot F2-round
read_now F2-round
ev "F2 clean: toolbar Undo"
g 215 15 18; click; nap 2.0; still
read_now F2-undone
nap 2.0
ev "recording stopped"
rec_stop
