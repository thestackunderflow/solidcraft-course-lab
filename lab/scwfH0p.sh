#!/bin/bash
# scwf take H0p (0.30.1, filmed): after H0c (one hole typed at 12 / 12.5), Parameters > Model parameters > Hole1 d6:
# 12.5 -> width / 2, held, OK. Then (not filmed, no AI) width 35: where the hole's centre goes, and back to 25.
#   docker exec scwf-s bash /work/lab/scwfH0p.sh
set -u
. /work/lab/scwflib.sh
take H0p
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
xdotool key Escape; sleep 1; still; sleep 1
rec_start
ev "recording started: the bracket with one hole typed at 12 and 12.5, full window"
nap 4.0
ev "parameters: Parameters button"
g 760 90 24; click; nap 2.0
ev "parameters: scroll to Model parameters"
g 1000 600 16; nap 0.6
for i in 1 2 3 4 5; do xdotool click 5; sleep 0.35; done; nap 1.5
ev "parameters: Hole1 d6 = 12.5 held 3 s"
g 1130 691 18; nap 3.0
ev "parameters: d6 = width / 2"
click; nap 0.5; xdotool key ctrl+a; typed "width / 2" 110; nap 0.5; xdotool key Tab; nap 2.0
cp_shot d6
ev "parameters: held 5 s"
nap 5.0
ev "parameters: OK"
g 1388 745 20; click; nap 1.5
still; nap 3.0
ev "recording stopped"
rec_stop
python3 /work/lab/scwfpart.py call "$O" w35 execute '{"command":"parameters.change","params":{"name":"width","value":35}}' > /dev/null
python3 /work/lab/scwfpart.py call "$O" topo35 body_topology '{"body":"Body1"}' > /dev/null
python3 /work/lab/scwfpart.py call "$O" w25 execute '{"command":"parameters.change","params":{"name":"width","value":25}}' > /dev/null
python3 /work/lab/scwfpart.py call "$O" plist execute '{"command":"parameters.list","params":{}}' > /dev/null
python3 /work/lab/scwfpart.py read "$O" after
echo "H0p done"
