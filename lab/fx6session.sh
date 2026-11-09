#!/bin/bash
# fx6 session (LAB-fx6 section 2): Xvfb 2880x1620, a fresh home, SolidCraft 0.28.0 at UI scale 1.8 filling the display,
# a new design with lesson 3's hook built by the no-AI recipe (lab/fx6hook.py, HOOK in lab/l7story.py) and saved as
# ~/hook-l3.sc, the 3D view. Then it waits; the takes are `docker exec fx6 bash /work/lab/fx6X.sh` steps.
#   docker run -d --name fx6 --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx6session.sh
set -u
. /work/lab/fx6lib.sh
S=/work/out/fx6/session; mkdir -p "$S"
{ /opt/solidcraft/bin/solidcraft --version; claude --version; } > "$S/versions.txt" 2>&1
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
solidcraft-cli mcp setup > "$S/setup.txt" 2>&1
start_display
openbox > /dev/null 2>&1 &
sleep 1
start_app "$S/app.log" /opt/solidcraft/bin/solidcraft
echo "$APP" > /tmp/fx6/app.pid
sleep 10
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
fill_window 0 0 $W $H; sleep 2
g 398 206 6; sleep 0.5; xdotool click 1; sleep 3                # start page: New design
python3 /work/lab/fx6hook.py build "$S" > "$S/hook.txt" 2>&1
sleep 8; still; sleep 1                                          # the "Saved" note fades
shot "$S/start.png"
echo ready > /tmp/fx6/ready
while kill -0 "$APP" 2>/dev/null; do sleep 2; done
echo "app exited" >> "$S/app.log"
