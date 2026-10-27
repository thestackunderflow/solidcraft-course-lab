#!/bin/bash
# The live container for a Claude run: SolidCraft's window on the virtual display, filmed for the whole run.
# The Claude apps' folders exist first; the entry is added the way the lesson shows it (Help > Connect AI assistants,
# clicked in the window); SolidCraft runs with no --control flag. The host's Claude Code then starts that entry
# inside this container (docker exec) through the logging proxy. The container waits until $O/STOP appears.
#   docker run -d --name sc1-live --memory 3g --shm-size 1g --network none -v "$PWD:/work" sc1-app:0.24.1 bash /work/lab/live.sh RUN
set -u
RUN=$1
O=/work/out/l1/runs/$RUN
mkdir -p "$O"
. /work/lab/common.sh
T=$O/timeline.jsonl
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
start_display
start_app "$O/app.log"
sleep 10
python3 /work/client/ctl.py ui.prefs '{"theme":"light"}' 27878 > "$O/theme-reply.json" 2>&1
xdotool mousemove 442 228 click 1; sleep 3
record "$O/screen.mp4"
event "$T" "recording started; app open (no flags), light theme, New design"
xdotool mousemove 1269 17 click 1; sleep 1.5
xdotool mousemove 1358 236 click 1; sleep 3; shot "$O/connect-dialog.png"
event "$T" "Help > Connect AI assistants clicked"
xdotool mousemove 1022 499 click 1; sleep 1
cp "$HOME/.claude.json" "$O/claude.json-entry.json"
cp "$HOME/.config/Claude/claude_desktop_config.json" "$O/claude_desktop_config.json" 2>/dev/null
xdotool mousemove 800 600
shot "$O/ready.png"
event "$T" "ready for the Claude app"
touch "$O/READY"
until [ -e "$O/STOP" ]; do sleep 1; done
event "$T" "stop asked"
sleep 2
stop_record
quit_app
event "$T" "app closed"
