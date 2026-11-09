#!/bin/bash
# fx6 take B part 2 (DEVIATIONS.md): 4.9 and 5.1 again on the clean hook, the same steps as lab/fx6B.sh, but undo is the
# toolbar's Undo button and a read-only read must show 8,500 mm3 before the next try. The recording keeps running.
set -u
. /work/lab/fx6lib.sh
vol() { python3 /work/lab/fx6hook.py read "$O" "$1" | awk '{print $3}'; }
undo_ok() {   # undo_ok TAG: toolbar Undo, then the read must be 8500.0 (max 2 clicks)
  local i v
  for i in 1 2; do
    ev "undo: toolbar Undo"; g 215 15 18; click; nap 2.0; still
    v=$(vol "$1-undo$i"); ev "undo: volume $v"
    [ "$v" = 8500.0 ] && return 0
  done
  ev "undo: FAILED"; return 1
}
[ "$(vol before-part2)" = 8500.0 ] || { ev "part 2: hook not clean"; exit 1; }
ev "part 2: hook clean (8500.0), 4.9 and 5.1 again"
try() {
  local R=$1 n
  ev "fillet $R: Fillet button (part 2)"
  g $FILLET_BTN 22; click; nap 1.4
  ev "fillet $R: lip outer top edge (part 2)"
  g $LIP_EDGE 24; nap 0.6; click; nap 1.2
  ev "fillet $R: radius typed (part 2)"
  radius "$R"
  cp_shot "p2-r-$R"
  ev "fillet $R: OK (part 2)"
  g $OK_BTN 18; click; nap 3.0
  n=$(python3 /work/lab/fx6hook.py read "$O" "p2-r$R" | python3 -c "import sys,json; l=sys.stdin.read(); print(json.loads(l.split(' lip ',1)[1])['curved_faces'])")
  if [ "$n" -gt 0 ]; then
    ev "fillet $R: built (part 2, curved faces $n)"; echo "$R built (part 2)" >> "$O/results.txt"
    still; nap 3.0; cp_shot "p2-r-$R-built"
    undo_ok "p2-$R" || exit 1
  else
    cp_shot "p2-r-$R-after-ok"
    ev "fillet $R: refused (part 2)"; echo "$R refused (part 2)" >> "$O/results.txt"
    g 1322 658 18; click; nap 1.5
  fi
  still; nap 1.5
}
for R in 4.9 5.1; do try $R; done
ev "part 2 done"
tail -2 "$O/results.txt"
