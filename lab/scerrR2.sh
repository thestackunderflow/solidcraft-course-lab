#!/bin/bash
# scerr take R2 (error 2 re-check on 0.30.1, filmed): fx7alt take A + C + F's calls in one take, no AI: a fresh 20 mm
# box from out/fx7alt/noai.py before the recording; on camera the scripted solid.fillet at the corner [20, 20, 20]
# (refused, held 5 s), solid.chamfer at the same corner (refused, held 4 s), then solid.fillet at [20, 20, 5], a point
# partway along the upright edge (built, held), a slow orbit.
#   docker run --rm --name scerr-r2 --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc-wf-l5:0.30.1 bash /work/lab/scerrR2.sh
set -u
. /work/lab/fx7altlib.sh
take() { O=/work/out/scerr/$1; mkdir -p "$O"; echo "$O" > /tmp/fx7/O; }
take R2
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
/opt/solidcraft/bin/solidcraft --version > "$O/env.txt" 2>&1
grep -q '0.30.1' "$O/env.txt" || { echo "wrong SolidCraft version"; exit 3; }
setup
cd /work/out/fx7alt
tt 'python3 -I noai.py box'
nap 1.0; tmux send-keys -t t "clear" Enter; nap 1.0; still
rec_start
ev "recording started: SolidCraft 0.30.1 window (top) + terminal strip, a fresh 20 mm box"
nap 2.0
tt 'python3 -I noai.py fillet 20 20 20'
ev "corner fillet: reply + toast held 5 s"
nap 5.0
tt 'python3 -I noai.py chamfer 20 20 20'
ev "corner chamfer: reply held 4 s"
nap 4.0
tmux send-keys -t t "clear" Enter; nap 0.8
tt 'python3 -I noai.py fillet 20 20 5'
ev "edge point fillet: built, held 5 s"
nap 5.0
ev "orbit: slow swing, 8 s"
orbit 8
nap 2.0
ev "recording stopped"
rec_stop
pane
vol r2-after
echo "R2 done"
