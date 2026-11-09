#!/bin/bash
# scwf probe (not filmed): the 0.30.1 panels the check takes use, screenshotted after each click (1440x810 units).
#   docker exec scwf-s bash /work/lab/scwfprobe.sh STEP
set -u
. /work/lab/scwflib.sh
P=/work/out/scwf/probe; mkdir -p "$P"; O=$P
case "$1" in
  part) python3 /work/lab/scwfg0.py /work/out/scwf/probe > "$P/g0.txt" 2>&1; tail -1 "$P/g0.txt"; sleep 3; shot "$P/0-part.png" ;;
  measure) g 382 50 10; click; sleep 1.2; shot "$P/1-inspect.png"; g 120 90 10; click; sleep 1.5; shot "$P/2-measure.png" ;;
  click) g "$2" "$3" 10; click; sleep 1.5; shot "$P/$4.png" ;;
  key) xdotool key "$2"; sleep 1.2; shot "$P/$3.png" ;;
  type) typed "$2" 90; sleep 1.2; shot "$P/$3.png" ;;
  shot) shot "$P/$2.png" ;;
esac
