#!/bin/bash
# fx8 session (LAB-fx8 sections 2-3): Xvfb 2880x1620, a fresh home, SolidCraft 0.28.0 at UI scale 1.8 filling the display,
# a new design; take P (not filmed) over the plug: lab/fx8part.py prep writes ~/hook-l3.sc, ~/hook-plain.stl,
# ~/hook-l4.sc, ~/hook.stl, ~/box-round.stl and ends on a new empty design. Then it waits; the takes are
# `docker exec fx8 bash /work/lab/fx8X.sh` steps.
#   docker run -d --name fx8 --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx8session.sh
set -u
. /work/lab/fx8lib.sh
S=/work/out/fx8/session; mkdir -p "$S" /work/out/fx8/P
{ /opt/solidcraft/bin/solidcraft --version; claude --version; } > "$S/versions.txt" 2>&1
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
solidcraft-cli mcp setup > "$S/setup.txt" 2>&1
start_display
openbox > /dev/null 2>&1 &
sleep 1
start_app "$S/app.log" /opt/solidcraft/bin/solidcraft
echo "$APP" > /tmp/fx8/app.pid
sleep 10
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
fill_window 0 0 $W $H; sleep 2
g 398 206 6; sleep 0.5; xdotool click 1; sleep 3                # start page: New design
python3 /work/lab/fx8part.py prep /work/out/fx8/P > "$S/prep.txt" 2>&1
sleep 6; still; sleep 1
shot "$S/start.png"
echo ready > /tmp/fx8/ready
while kill -0 "$APP" 2>/dev/null; do sleep 2; done
echo "app exited" >> "$S/app.log"
