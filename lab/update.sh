#!/bin/bash
# Q11: does an older install (0.23.1) offer the update? Started with network, a design open, the mouse moving; the
# title bar photographed at 20 s and 60 s. Host side (network on):
#   docker run --rm --memory 3g --shm-size 1g -v "$PWD:/work" sc1-app:0.24.1 bash /work/lab/update.sh
set -u
O=/work/out/l1/update
[ -e "$O" ] && { echo "refusing: $O exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
start_display
start_app "$O/app.log" /opt/solidcraft-0.23.1/bin/solidcraft
sleep 10
python3 /work/client/ctl.py ui.prefs '{"theme":"light"}' 27878 > /dev/null 2>&1
xdotool mousemove 442 228 click 1
for i in $(seq 1 10); do xdotool mousemove $(( 500 + i * 30 )) 500; sleep 1; done
shot "$O/title-20s.png"
for i in $(seq 1 40); do xdotool mousemove $(( 500 + (i % 10) * 30 )) 520; sleep 1; done
shot "$O/title-60s.png"
convert "$O/title-60s.png" -crop 1600x40+0+0 "$O/titlebar-60s.png"
quit_app
