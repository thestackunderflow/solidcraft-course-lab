#!/bin/bash
# L4-Q8, the proof and the follow test ($0, no AI): a fresh container and SolidCraft 0.27.1 window, the entry added with
# `solidcraft-cli mcp setup`, a new design; lesson 3's hook built the way the run's setup built it (lab/l4hook.py's
# batch); Claude's turn-1 tools/call requests replayed in order exactly as logged (failed calls too); read; `width` set
# to 26 and to 40, read each (does each bore stay at the body's middle?); `width` back to 20; the turn-2 calls replayed;
# read; width 26 and 40 again; an STL export read by our checker (closed, one body; its volume is not narrated).
#   docker run --rm --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc4-l4:0.27.1 bash /work/lab/l4replay.sh B1
set -u
RUN=${1:-B1}
O=/work/out/l4/replay-$RUN
[ -e "$O/replay.json" ] && { echo "refusing: $O/replay.json exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
solidcraft-cli mcp setup > "$O/setup.txt" 2>&1
start_display
start_app "$O/app.log"
sleep 10
python3 /work/client/ctl.py ui.prefs '{"theme":"light"}' 27878 > /dev/null 2>&1
xdotool mousemove 442 228 click 1; sleep 3
python3 /work/lab/l4replay.py "$RUN" "$O"
quit_app
