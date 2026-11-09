#!/bin/bash
# fx6 take B (LAB-fx6 section 3): the same edge at 4.0, 4.9, 5.0, 5.1 mm, in that order. Each: Fillet, the edge, the
# radius typed (held 4 s on the box, Preview on), r-R.png, OK; built = the read-only read finds a curved face (then
# Ctrl+Z); refused = OK stays greyed and the panel keeps the red line (then Cancel). The reason words are typed into
# events by part 2 from the screenshots. Then (lab/fx6B2.sh) F2 filmed cleanly at the largest built radius.
#   docker exec fx6 bash /work/lab/fx6B.sh
set -u
. /work/lab/fx6lib.sh
take B
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
: > "$O/results.txt"
still; sleep 1
rec_start
ev "recording started: take B, the limit search, full window"
nap 3.0
try() {   # try R
  local R=$1 n
  ev "fillet $R: Fillet button"
  g $FILLET_BTN 22; click; nap 1.4
  ev "fillet $R: lip outer top edge"
  g $LIP_EDGE 24; nap 0.6; click; nap 1.2
  ev "fillet $R: radius typed"
  radius "$R"
  cp_shot "r-$R"
  ev "fillet $R: OK"
  g $OK_BTN 18; click; nap 2.5
  n=$(python3 /work/lab/fx6hook.py read "$O" "r$R" | python3 -c "import sys,json; l=sys.stdin.read(); print(json.loads(l.split(' lip ',1)[1])['curved_faces'])")
  if [ "$n" -gt 0 ]; then
    ev "fillet $R: built (curved faces $n)"; echo "$R built" >> "$O/results.txt"
    still; nap 3.0; cp_shot "r-$R-built"
    ev "fillet $R: Ctrl+Z"
    xdotool key ctrl+z; nap 2.0
  else
    cp_shot "r-$R-after-ok"
    ev "fillet $R: refused (OK greyed, panel open)"; echo "$R refused" >> "$O/results.txt"
    ev "fillet $R: Cancel"
    g 1322 658 18; click; nap 1.5
  fi
  still; nap 1.5
}
for R in 4.0 4.9 5.0 5.1; do try $R; done
read_now after-search
ev "search done"
cat "$O/results.txt"
