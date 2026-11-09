#!/bin/bash
# scwf session: Xvfb 2880x1620, a fresh home, SolidCraft 0.30.1 at UI scale 1.8 filling the display, a new design,
# then it waits; the takes are `docker exec scwf-s bash /work/lab/scwfX.sh` steps (scerr pattern, lab/scerrsession.sh).
#   docker run -d --name scwf-s --memory 4g --shm-size 1g --network none -e SEED=1 -v "$PWD:/work" sc-wf-l5:0.30.1 bash /work/lab/scwfsession.sh
set -u
. /work/lab/scwflib.sh
S=/work/out/scwf/${SESSION:-session}; mkdir -p "$S"
/opt/solidcraft/bin/solidcraft --version > "$S/versions.txt" 2>&1
grep -q '0.30.1' "$S/versions.txt" || { echo "wrong SolidCraft version"; cat "$S/versions.txt"; exit 3; }
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
solidcraft-cli mcp setup > "$S/setup.txt" 2>&1
cp "$HOME/.claude.json" "$S/claude-json-after-setup.json"
start_display
openbox > /dev/null 2>&1 &
sleep 1
[ -n "${SEED:-}" ] && { . /work/lab/l5slicerseed.sh; seed_slicer; }      # PrusaSlicer seeded as lesson 5 (no wizard)
start_app "$S/app.log" /opt/solidcraft/bin/solidcraft
echo "$APP" > /tmp/fx8/app.pid
sleep 10
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
fill_window 0 0 $W $H; sleep 2
shot "$S/start-page.png"
g 398 206 6; sleep 0.5; xdotool click 1; sleep 3                # start page: New design
still; sleep 1
shot "$S/start.png"
echo ready > /tmp/fx8/ready
while kill -0 "$APP" 2>/dev/null; do sleep 2; done
echo "app exited" >> "$S/app.log"
