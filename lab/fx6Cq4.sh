#!/bin/bash
# fx6 take C step 4 (Q4, NOT filmed for the video: screenshots and reads only): both lip top edges in one Fillet at 2.5
# on thickness 5; 2.4 only if 2.5 is refused. Undo with the toolbar.
set -u
. /work/lab/fx6lib.sh
O=/work/out/fx6/C; T0=
both() {
  ev "Q4: Fillet, outer + inner lip top edges, radius $1"
  g $FILLET_BTN 14; click; nap 1.2
  g $LIP_EDGE 14; click; nap 1.0
  g 881 594 10; click; nap 1.0
  radius "$1"
  cp_shot "both-$1-panel"
  g $OK_BTN 14; click; nap 3.0
  python3 /work/lab/fx6hook.py read "$O" "both-$1" > /dev/null
  N=$(python3 -c "import json; d=json.load(open('$O/read-both-$1.json')); print(sum(1 for f in d['topology']['faces'] if f.get('cylinder')))")
  still; nap 1.0; cp_shot "both-$1"
}
both 2.5
if [ "$N" -gt 0 ]; then ev "both 2.5: built (curved faces $N)"; g 215 15 14; click; nap 2.0
else ev "both 2.5: refused (see both-2.5.png)"; g 1322 658 14; click; nap 1.5; both 2.4
  [ "$N" -gt 0 ] && { ev "both 2.4: built (curved faces $N)"; g 215 15 14; click; nap 2.0; } || { ev "both 2.4: refused"; g 1322 658 14; click; nap 1.5; }
fi
still; read_now q4-undone
