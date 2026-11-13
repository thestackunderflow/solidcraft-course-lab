#!/bin/bash
# fx13 take C (LAB-fx13 section 3): Q3 the second cup (~/cup-bottom.sc: only the bottom edge rounded), chain left ON,
# the top: what lights, built?, Properties (33,990.00); Q5 the your-turn cup (~/cup40.sc), chain off, the top, 2 mm,
# Properties (11,532.86); Q4 the bonus (~/cup-r3.sc, rounds 3), chain off, the top, 2 mm: the rim line expected.
# Each file opens in its own tab (the plug's open).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx13C.sh
set -u
. /work/lab/fx13lib.sh
take C
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc cup-bottom; still
rec_start
ev "recording started: full SolidCraft window, ~/cup-bottom.sc (the second cup): hold 3 s"
nap 3.0
ev "the second cup held 5 s (Short S2 end frame)"; nap 5.0; cp_shot second-cup
shell_open dialog-bottom
pick "click the top face, chain left on" $TOP60
ev "second cup chain on: lit faces as shown in preview-bottom.png: hold 4 s"; nap 4.0; cp_shot preview-bottom
thick "2 mm"
cp_shot before-ok-bottom
ev "OK"; g $SH_OK 14; click; nap 3.0; still; cp_shot after-ok-bottom
vol c-bottom
ev "second cup: $(cut -c1-300 "$O/read-c-bottom.txt")"
props_body props-bottom
ev "open ~/cup40.sc (the your-turn cup, a new tab)"; open_sc cup40; still; nap 2.0
shell_open dialog-40
chain_off untick-40
pick "click the top face, chain off" $TOP40
thick "2 mm"
ev "your-turn cup chain off as shown in preview-40.png: hold 3 s"; nap 3.0; cp_shot preview-40
ev "OK"; g $SH_OK 14; click; nap 3.0; still; cp_shot after-ok-40
vol c-40
ev "your-turn cup: $(cut -c1-300 "$O/read-c-40.txt")"
props_body props-40
ev "open ~/cup-r3.sc (rounds 3, a new tab)"; open_sc cup-r3; still; nap 2.0
shell_open dialog-r3
chain_off untick-r3
pick "click the top face, chain off" $TOP60
thick "2 mm"
ev "r3 chain off: as shown in r3.png: hold 4 s"; nap 4.0; cp_shot r3
ev "OK"; g $SH_OK 14; click; nap 3.0; still; cp_shot after-ok-r3
vol c-r3
ev "r3 after OK: $(cut -c1-300 "$O/read-c-r3.txt")"
ev "close the dialog if open (its x)"; g $SH_CLOSE_X 14; click; nap 1.5; still
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "C done"
