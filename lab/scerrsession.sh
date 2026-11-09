#!/bin/bash
# scerr session: Xvfb 2880x1620, a fresh home, SolidCraft 0.30.1 at UI scale 1.8 filling the display, a new design;
# the fx8 take P files (lab/fx8part.py prep: ~/hook-l3.sc, ~/hook-plain.stl, ~/hook-l4.sc, ~/hook.stl, ~/box-round.stl),
# then it waits; the takes are `docker exec scerr-s bash /work/lab/scerrX.sh` steps.
#   docker run -d --name scerr-s --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc-wf-l5:0.30.1 bash /work/lab/scerrsession.sh
set -u
. /work/lab/scerrlib.sh
S=/work/out/scerr/${SESSION:-session}; mkdir -p "$S" /work/out/scerr/P
/opt/solidcraft/bin/solidcraft --version > "$S/versions.txt" 2>&1
grep -q '0.30.1' "$S/versions.txt" || { echo "wrong SolidCraft version"; cat "$S/versions.txt"; exit 3; }
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
solidcraft-cli mcp setup > "$S/setup.txt" 2>&1
start_display
openbox > /dev/null 2>&1 &
sleep 1
[ -n "${SEED:-}" ] && { . /work/lab/l5slicerseed.sh; seed_slicer; }      # take S2: PrusaSlicer seeded as lesson 5 (no wizard)
start_app "$S/app.log" /opt/solidcraft/bin/solidcraft
echo "$APP" > /tmp/fx8/app.pid
sleep 10
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
fill_window 0 0 $W $H; sleep 2
shot "$S/start-page.png"
g 398 206 6; sleep 0.5; xdotool click 1; sleep 3                # start page: New design
python3 /work/lab/fx8part.py prep /work/out/scerr/P > "$S/prep.txt" 2>&1
sleep 6; still; sleep 1
shot "$S/start.png"
echo ready > /tmp/fx8/ready
while kill -0 "$APP" 2>/dev/null; do sleep 2; done
echo "app exited" >> "$S/app.log"
