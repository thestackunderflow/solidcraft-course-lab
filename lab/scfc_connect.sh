#!/bin/bash
# scfc (8 Nov 2026, $0, no AI): step 1 "connect" filmed on SolidCraft 0.30.1: the start page, the "?" button, then
# Connect AI assistants... (Claude Code's config file exists, as after installing it); the dialog held; files kept.
#   docker run --rm --name scfc-connect --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc-wf-l4:0.30.1 \
#     bash /work/lab/scfc_connect.sh
# Writes out/scfc/connect-0.30.1/: screen.mp4, cursor.jsonl, events.jsonl, dialog.png, files-*.txt, app.log.
set -u
O=/work/out/scfc/connect-0.30.1
[ -e "$O/screen.mp4" ] && { echo "refusing: $O/screen.mp4 exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
. /work/lab/l2common.sh
E=$O/events.jsonl; : > "$E"
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
client_files > "$O/files-before.txt"
start_display
start_app "$O/app.log"
sleep 10
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
fill_window 0 0 $W $H; sleep 2
c43() { awk -v v="$1" 'BEGIN{printf "%d", v*4/3}'; }
g() { glide "$(c43 "$1")" "$(c43 "$2")" "${3:-18}"; }
xdotool mousemove 1400 900
record30 "$O/screen.mp4" "$O/cursor.jsonl"
mark "$E" "recording started: SolidCraft 0.30.1 start page"
sleep 3.5
mark "$E" "glide to the ? button"
g 1141 15 24; sleep 1.2; xdotool click 1
mark "$E" "? menu open"
sleep 2.5
g 1200 238 16; sleep 1.2
mark "$E" "click Connect AI assistants"
xdotool click 1; sleep 1.0
mark "$E" "dialog"
sleep 6
shot "$O/dialog.png"
client_files > "$O/files-after.txt"
mark "$E" "dialog held 6 s"
xdotool key Escape; sleep 2
mark "$E" "recording stopped"
stop_record30
cp "$HOME/.claude.json" "$O/claude.json" 2>/dev/null
quit_app
