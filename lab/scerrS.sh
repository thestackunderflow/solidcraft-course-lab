#!/bin/bash
# scerr take S (thread, 0.30.1, filmed): lesson 4's hook (holes + rounds) open; right-click Body1 > Send to Slicer >
# Send (PrusaSlicer 2.9.2, default 3MF); the slicer window held while it loads. Part 1 only: what PrusaSlicer shows
# decides part 2 (size boxes).
#   docker exec scerr-s bash /work/lab/scerrS.sh
set -u
. /work/lab/scerrlib.sh
take ${TAKE:-S}
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
still; sleep 1
rec_start
ev "recording started: lesson 4's hook in SolidCraft 0.30.1, full window"
nap 4.0
ev "send: right-click Body1"
g 95 311 22; nap 1.0; xdotool click 3; nap 1.5
ev "send: Send to Slicer"
g 162 464 16; click; nap 2.0
ev "send: dialog held 3 s (Slicer: PrusaSlicer)"
g 1340 437 14; nap 3.0
ev "send: Send"
g 1388 486 14; click
for i in $(seq 1 60); do xdotool search --name "PrusaSlicer" >/dev/null 2>&1 && break; sleep 0.5; done
ev "slicer: window up"
nap 14.0
cp_shot slicer
ls -la "$HOME/.cache/solidcraft/slicer" | sed "s#$HOME#~#g" > "$O/ls-cache-slicer.txt"
ev "slicer: window held (size row)"; nap 2.0
[ -n "${FINISH:-}" ] && { ev "recording stopped"; rec_stop; }
echo "S part 1 done"
