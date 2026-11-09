#!/bin/bash
# fx7alt take D (LAB-fx7alt section 3): the window click. The fresh box is made before the recording (noai.py box);
# on camera no script: full window 3 s, Fillet from the toolbar, click the same top edge as take B (hold 4 s on the
# Edges row), radius 3, OK; then the point the dialog sent, from SolidCraft's session journal (journal.py, 1st try).
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx7altD.sh
set -u
. /work/lab/fx7altlib.sh
take D
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
cd /work/out/fx7alt
tt 'python3 -I noai.py box'
nap 1.0; tmux send-keys -t t "clear" Enter; nap 1.0; still
rec_start
ev "recording started: full window held 3 s, a fresh 20 mm box (no script from here)"
nap 3.0
ev "Fillet button"
g $FILLET_BTN 22; click; nap 1.6
ev "click the top edge (y 20, z 20)"
g $TOP_EDGE_MID 22; click; nap 1.0
ev "Edges row: hold 4 s"
g $EDGES_ROW 16; nap 4.0
cp_shot dialog
ev "radius 3"
g $RADIUS_BOX 14; click; xdotool key ctrl+a; nap 0.3; typed 3 160; nap 0.6; xdotool key Tab; nap 3.0
ev "OK"
g $OK_BTN 14; click; nap 1.5; still
ev "the round: hold 4 s"
nap 4.0
cp_shot after
nap 4.0
ev "the journal: typed into the terminal"
tt 'python3 -I journal.py'
ev "journal shown: hold 4 s"
nap 4.0
cp_shot log
ev "recording stopped"
rec_stop
pane
grep -o '"edges": \[\[[^]]*\]\]' "$O/pane.txt" | head -1 | sed 's/"edges": \[\(.*\)\]/\1/' > "$O/sent.txt"
if [ -s "$O/sent.txt" ]; then ev "window sent: $(cat "$O/sent.txt") (session journal, recovery document.json)"; else ev "window sent: not visible"; fi
vol d-after
echo "D done"
