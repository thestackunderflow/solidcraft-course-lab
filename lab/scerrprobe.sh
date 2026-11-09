#!/bin/bash
# scerr probe (not filmed): open ~/hook-l3.sc, home view, screenshot; open the Fillet panel on the fx6 lip edge position,
# screenshot; Escape. Halved screenshots in out/scerr/probe/ give the 1440x810 positions.
#   docker exec scerr-s bash /work/lab/scerrprobe.sh STEP
set -u
. /work/lab/scerrlib.sh
take probe
case "$1" in
  open) open_file /root/hook-l3.sc; sleep 3; still; sleep 1; shot "$O/p-open.png" ;;
  fillet) g $FILLET_BTN 10; click; sleep 1.5; shot "$O/p-fillet1.png"; g $LIP_EDGE 10; click; sleep 1.5; shot "$O/p-fillet2.png" ;;
  shot) shot "$O/p-$2.png" ;;
  key) xdotool key "$2"; sleep 1; shot "$O/p-key.png" ;;
  click) g $2 $3 10; click; sleep 1.5; shot "$O/p-click.png" ;;
esac
for f in "$O"/p-*.png; do convert "$f" -resize 50% "${f%.png}.half.jpg"; done 2>/dev/null
echo done
