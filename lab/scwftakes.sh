#!/bin/bash
# scwf filmed takes on SolidCraft 0.30.1 (9 Nov 2026), one per call, in a clean session (lab/scwfsession.sh):
#   E   the empty design, full window (F1)                      O   Claude's bracket (R1/bracket.sc), slow orbit (F0)
#   C1  History stepped back to the extrude: Inspect > Properties (volume, bounding box), then Measure: the top corner
#       (hover: its X, Y, Z) and the corner at the origin (dZ)  (F6 hand check)
#   C3  same stage: Parameters, width 25 -> 35 -> 25 (F8)       C4  History to the end, width 35, Measure hole rim +
#       the side face: centre to centre (F15), width back to 25  P   Properties on the finished part (checklist)
#   S1  Send to Slicer as drawn, slice (F13)                     S2  print face = the side, Send to Slicer, slice
# Positions in 1440x810 units (probes in out/scwf/probe). Usage: docker exec scwf-s bash /work/lab/scwftakes.sh TAKE
set -u
. /work/lab/scwflib.sh
take "$1"
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
home() { python3 /work/lab/scwfpart.py call "$O" home execute '{"command":"view.home","params":{}}' > /dev/null 2>&1; sleep 1.5; }
props_hold() { ev "inspect: Inspect tab"; g 382 50 20; click; nap 1.2
  ev "inspect: Properties"; g 229 90 18; click; nap 1.5
  ev "inspect: Properties held $1 s"; g 1000 330 14; nap "$1"; cp_shot props
  ev "inspect: Close"; g 860 649 16; click; nap 1.2; }
params_width() { ev "parameters: Model tab"; g 122 50 18; click; nap 1.0
  ev "parameters: Parameters"; g 760 90 20; click; nap 1.8
  ev "parameters: width = $1"; g 1123 486 18; click; nap 0.4; xdotool key ctrl+a; typed "$1" 140; nap 0.4; xdotool key Tab; nap 1.0
  ev "parameters: held ${2:-5} s"; g 640 600 20; nap "${2:-5}"; cp_shot "w$1"; }
send() {   # the Browser's Body1, right-click, Send to Slicer, Send; then OK on the offline preset error, Ctrl+R
  ev "send: right-click Body1"; g 95 311 22; nap 1.0; xdotool click 3; nap 1.5
  ev "send: Send to Slicer"; g 162 464 16; click; nap 2.0
  ev "send: dialog held 3 s"; g 1340 437 14; nap 3.0
  ev "send: Send"; g 1388 486 14; click
  for i in $(seq 1 60); do xdotool search --name "PrusaSlicer" >/dev/null 2>&1 && break; sleep 0.5; done
  nap 8.0; cp_shot slicer-open
  ev "slicer: OK on the offline preset-download error (container has no network)"; g 820 463 16; click; nap 2.0
  ev "slicer: Ctrl+R slice"; xdotool key ctrl+r; nap 8.0
  ev "slicer: sliced, held 8 s"; g 1100 300 20; nap 8.0; cp_shot sliced; }
case "$1" in
E)  python3 /work/lab/scwfpart.py call "$O" new execute '{"command":"file.new","params":{}}' > /dev/null 2>&1
    xdotool key Escape; still; sleep 1; rec_start
    ev "recording started: an empty design, SolidCraft 0.30.1, full window"; nap 3.0
    ev "cursor along the Model tab"; g 128 90 40; nap 1.5; g 297 90 40; nap 1.5; g 353 90 30; nap 1.5; g 760 90 40; nap 2.0
    still; nap 3.0 ;;
O)  home; xdotool key Escape; still; sleep 1; rec_start
    ev "recording started: Claude's bracket in SolidCraft 0.30.1, full window"; nap 3.0
    ev "orbit: slow swing right and back, 10 s"; g 1000 330 10; xdotool mousedown 2
    for i in $(seq 1 80); do xdotool mousemove_relative -- 5 0; sleep 0.06; done
    for i in $(seq 1 80); do xdotool mousemove_relative -- -5 0; sleep 0.06; done
    xdotool mouseup 2; nap 0.5
    ev "home view: held 3 s"; g 870 737 14; click; nap 1.0; still; nap 3.0 ;;
C1) home; xdotool key Escape; still; sleep 1; rec_start
    ev "recording started: Claude's bracket, all five steps, full window"; nap 3.0
    ev "history: step back 3 (fillet, hole B, hole A off)"; g 118 785 24
    for i in 1 2 3; do click; nap 0.8; done; nap 1.5
    props_hold 7.0
    ev "measure: Measure"; g 382 50 14; click; nap 0.6; g 120 90 18; click; nap 1.4
    ev "measure: top corner"; g 1105 365 24; click; nap 1.0
    ev "measure: hover, X Y Z held 4 s"; g 1350 347 14; nap 4.0; cp_shot top
    ev "measure: the corner at the origin"; g 570 505 24; click; nap 1.5
    ev "measure: dZ held 6 s"; g 1310 600 14; nap 6.0; cp_shot dz
    ev "measure: Close"; xdotool key Escape; nap 1.0 ;;
C3) xdotool key Escape; still; sleep 1; rec_start
    ev "recording started: the bracket at the extrude step, full window"; nap 3.0
    params_width 35 6
    ev "parameters: width back to 25"; g 1123 486 18; click; nap 0.4; xdotool key ctrl+a; typed 25 140; nap 0.4; xdotool key Tab; nap 3.0
    ev "parameters: OK"; g 1388 745 18; click; nap 1.5; still; nap 2.0 ;;
C4) ev "setup: history to the end"; g 188 785 10; click; sleep 1.5; home; xdotool key Escape; still; sleep 1; rec_start
    ev "recording started: the finished bracket, full window"; nap 3.0
    params_width 35 4
    ev "parameters: OK"; g 1388 745 18; click; nap 1.5; home; still; nap 2.0
    ev "measure: Inspect, Measure"; g 382 50 18; click; nap 1.0; g 120 90 18; click; nap 1.4
    ev "measure: the first hole's rim"; g 751 276 24; click; nap 1.2
    ev "measure: the L-shaped side face"; g 720 394 24; click; nap 1.5
    ev "measure: centre to centre held 7 s"; g 1310 466 18; nap 7.0; cp_shot c2c
    ev "measure: Close"; xdotool key Escape; nap 1.0
    ev "parameters: width back to 25"; params_width 25 2; g 1388 745 18; click; nap 1.5; home; still; nap 2.0 ;;
P)  home; xdotool key Escape; still; sleep 1; rec_start
    ev "recording started: the finished bracket, full window"; nap 3.0
    props_hold 7.0; still; nap 2.0 ;;
S1) home; xdotool key Escape; still; sleep 1; rec_start
    ev "recording started: the finished bracket, as drawn, full window"; nap 3.0
    send ;;
S2) pkill -x slic3r_main; sleep 2; xdotool key Escape; still
    python3 /work/lab/scwfpart.py call "$O" face execute '{"command":"body.print_face","params":{"body":"Body1","point":[25,0,28]}}' > "$O/print-face.txt" 2>&1
    home; still; sleep 1; rec_start
    ev "recording started: the finished bracket, print face = the L-shaped side, full window"; nap 4.0
    send ;;
esac
ev "recording stopped"; rec_stop
ls -t "$HOME/.cache/solidcraft/slicer/" 2>/dev/null | head -3 > "$O/slicer-cache.txt"
echo "$1 done"
