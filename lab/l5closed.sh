#!/bin/bash
# L5-Q5 (+ L5-Q4's Place on face): PrusaSlicer 2.9.2 alone, filmed. (1) The hook's STL saved by SolidCraft (closed),
# then a copy we broke on purpose (6 triangles removed: lab/l5break.py): the warning sign by the name and its tooltip.
# (2) The STL Save As Mesh wrote after a print face was picked (it stands, as drawn): Place on face (F) and a click on
# the J side. xdotool only; `--info` and our checker on both files after the recording.
#   docker run --rm --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/l5closed.sh
set -u
O=/work/out/l5/closed
[ -e "$O/screen.mp4" ] && [ -z "${DRY:-}" ] && { echo "refusing: $O/screen.mp4 exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
. /work/lab/l2common.sh
. /work/lab/l5slicerseed.sh
E=$O/events.jsonl; : > "$E"; : > "$O/cursor.jsonl"
GOOD=/work/out/l5/saveface/save-before-face.stl
BAD=$O/hook-broken.stl
STAND=/work/out/l5/saveface/save-after-face.stl
python3 /work/lab/l5break.py "$GOOD" "$BAD" 6
seed_slicer
start_display
openbox > /dev/null 2>&1 &
sleep 1
c43() { awk -v v="$1" 'BEGIN{printf "%d", v*4/3}'; }
g() { glide "$(c43 "$1")" "$(c43 "$2")" "${3:-20}"; }
click() { xdotool click 1; }
slicer_win() { xdotool search --name "PrusaSlicer-2.9" 2>/dev/null | head -1; }
open_in_slicer() {   # open_in_slicer FILE TAG: start PrusaSlicer on the file, wait for its window
  prusa-slicer --single-instance "$1" > "$O/slicer-$2.log" 2>&1 &
  local i; for i in $(seq 1 120); do [ -n "$(slicer_win)" ] && break; sleep 0.5; done; sleep 7
}
if [ -z "${DRY:-}" ]; then record30 "$O/screen.mp4" "$O/cursor.jsonl"; else T0=$(date +%s.%N); fi
mark "$E" "recording started"
open_in_slicer "$GOOD" good
mark "$E" "good: window up"
g 1040 336 22; nap 3.0
shot "$O/good.png"
mark "$E" "good: name, no sign"
nap 2.0
xdotool windowactivate --sync "$(slicer_win)" key --clearmodifiers ctrl+q; sleep 3
pkill -x slic3r_main; sleep 1
open_in_slicer "$BAD" bad
mark "$E" "bad: window up"
g 1040 336 22; nap 1.5
mark "$E" "bad: hover the warning sign"
g 996 335 14; nap 4.5
shot "$O/bad-tooltip.png"
mark "$E" "bad: tooltip held"
nap 1.5
xdotool windowactivate --sync "$(slicer_win)" key --clearmodifiers ctrl+q; sleep 3
pkill -x slic3r_main; sleep 1
open_in_slicer "$STAND" stand
mark "$E" "place: window up (the saved file, standing)"
g 470 450 22; nap 1.0; click; nap 1.5
mark "$E" "place: F (Place on face)"
xdotool key f; nap 2.5
shot "$O/place-f.png"
mark "$E" "place: click the J side"
g "${PX:-500}" "${PY:-470}" 22; nap 1.0; click; nap 3.0
shot "$O/place-after.png"
mark "$E" "place: done"
g 1190 506 22; nap 3.0
mark "$E" "recording stopped"
[ -z "${DRY:-}" ] && stop_record30
pkill -x slic3r_main
for f in "$GOOD" "$BAD" "$STAND"; do echo "== $f"; prusa-slicer --info "$f" 2>&1 | grep -E "manifold|open_edges|facets|size_"; python3 -m checker.stl "$f" | tr -d '\n '; echo; done > "$O/info.txt" 2>&1
