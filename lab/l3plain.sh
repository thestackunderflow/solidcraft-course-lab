#!/bin/bash
# L3-Q4: the plain-number copy. Lesson 2's J (typed numbers, as lesson 2 filmed it) is drawn by xdotool before the
# recording starts; then filmed: Parameters, d1 (the 25) changed to 40, Enter, SolidCraft's answer, OK, Properties;
# then the remedy: d5 (the 15) written as d1 - 10 (the dialog's Filter finds the row), d1 = 40, Properties.
# After the recording a scripted MCP client (no AI) reads the design.
#   docker run --rm --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc3-l3:0.26.1 bash /work/lab/l3plain.sh plain
set -u
RUN=${1:-plain}
O=/work/out/l3/$RUN
[ -e "$O/read.json" ] && { echo "refusing: $O/read.json exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
. /work/lab/l2common.sh
E=$O/events.jsonl; : > "$E"; : > "$O/cursor.jsonl"
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
solidcraft-cli mcp setup > "$O/setup.txt" 2>&1
start_display
start_app "$O/app.log"
sleep 10
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
fill_window 0 0 $W $H; sleep 1
PACE=0.4
# --- not filmed: lesson 2's J with typed numbers, extruded 20 (lesson 2 filmed these exact clicks)
glide 530 274 10; sleep 0.5; xdotool click 1; sleep 2.5
glide 171 115 8; xdotool click 1; sleep 1.5
glide 40 353 8; xdotool click 1; sleep 1.0
glide 122 540 8; xdotool click 1; sleep 3
glide 960 620 10; sleep 1; xdotool mousedown 2; for i in $(seq 1 20); do rel 0 19; sleep 0.08; done; xdotool mouseup 2; sleep 1
glide 155 115 8; xdotool click 1; sleep 1; glide 960 1000 10; sleep 0.5; xdotool click 1; sleep 1; focus_app
s() { glide "$1" "$2" 12; sleep 0.8; xdotool type --delay 80 "$3"; sleep 0.4; xdotool key Return; sleep 0.9; }
s 1200 1000 25; s 1200 904 10; s 1152 904 5; s 1152 952 5; s 1008 952 15; s 1008 424 55; s 960 424 5
glide 960 1000 12; sleep 0.8; xdotool click 1; sleep 1; xdotool key Escape; sleep 1
glide 1348 125 10; xdotool click 1; sleep 2
glide 163 67 8; xdotool click 1; sleep 0.6; glide 258 115 8; xdotool click 1; sleep 2.5; focus_app
xdotool type --delay 100 20; sleep 1; glide 1851 772 8; xdotool click 1; sleep 2
glide 1160 1103 8; xdotool click 1; sleep 2
glide 1300 700 10; sleep 0.5
xdotool mousedown 2; for i in $(seq 1 20); do rel -22 -5; sleep 0.06; done; xdotool mouseup 2; sleep 1
python3 /work/lab/l3read.py "$O" > "$O/read-before.txt" 2>&1; mv "$O/read.json" "$O/read-before.json"; mv "$O/read-transcript.jsonl" "$O/read-before-transcript.jsonl"
shot "$O/before.png"
[ -n "${DRY:-}" ] && { echo ready > /tmp/ready; sleep infinity; }
PACE=1.0
# --- filmed
record30 "$O/screen.mp4" "$O/cursor.jsonl"
mark "$E" "recording started: lesson 2's plain-number hook"
nap 2.0
mark "$E" "plain: open Parameters"
glide 1013 117 22; nap 1.2; xdotool click 1; nap 2.6
mark "$E" "plain: d1 to d7 under Sketch1"
glide 1300 750 20; nap 2.6
mark "$E" "plain: click d1's 25"
glide 1440 788 20; nap 1.2; xdotool click 1; nap 0.6
focus_app
xdotool key ctrl+a; nap 0.8
mark "$E" "plain: type 40"
xdotool type --delay 300 40; nap 1.0
mark "$E" "plain: Enter"
xdotool key Return; nap 1.5
shot "$O/refused.png"
mark "$E" "plain: the message held"
glide 1500 528 20; nap 1.0
mkdir -p "$O/after-refusal"; python3 /work/lab/l3read.py "$O/after-refusal" > "$O/after-refusal/read.txt" 2>&1
nap 3.0
mark "$E" "plain: OK"
glide 1851 993 22; nap 0.8; xdotool click 1; nap 2.0
mark "$E" "plain: the hook unchanged"
glide 1160 1103; nap 1.0; xdotool click 1; nap 2.4
mark "$E" "plain properties: right-click Body1"
glide 135 634; nap 1.0; xdotool click 3; nap 1.4
glide 213 653; nap 0.8
mark "$E" "plain properties: open"
xdotool click 1; nap 1.6
shot "$O/props-refused.png"
mark "$E" "plain properties: rows held"
glide 900 500 16; nap 4.5
mark "$E" "plain properties: close"
xdotool key Escape; nap 1.2
glide 1300 700 16; nap 0.4
xdotool mousedown 2; for i in $(seq 1 20); do rel -22 -5; sleep 0.06; done; xdotool mouseup 2; nap 1.0
# --- the remedy: d5 (the 15) written as a formula of d1, then d1 = 40
mark "$E" "remedy: open Parameters"
glide 1013 117 22; nap 1.0; xdotool click 1; nap 2.0
mark "$E" "remedy: filter d5"
glide 1504 448 20; nap 0.8; xdotool click 1; nap 0.4; focus_app; xdotool key ctrl+a; xdotool type --delay 220 d5; nap 1.4
mark "$E" "remedy: click d5's 15"
glide 1440 788 20; nap 1.0; xdotool click 1; nap 0.5; xdotool key ctrl+a; nap 0.6
mark "$E" "remedy: type d1 - 10"
xdotool type --delay 220 "d1 - 10"; nap 1.0; xdotool key Return
mark "$E" "remedy: d5 accepted"
nap 2.4
mark "$E" "remedy: filter d1"
glide 1504 448 20; nap 0.8; xdotool click 1; nap 0.4; xdotool key ctrl+a; xdotool type --delay 220 d1; nap 1.4
mark "$E" "remedy: click d1's 25"
glide 1440 788 20; nap 1.0; xdotool click 1; nap 0.5; xdotool key ctrl+a; nap 0.6
mark "$E" "remedy: type 40"
xdotool type --delay 300 40; nap 1.0; xdotool key Return
mark "$E" "remedy: the hook grows"
nap 4.0
shot "$O/remedy-after-enter.png"
mark "$E" "remedy: OK"
glide 1851 858 22; nap 0.8; xdotool click 1; nap 1.6
mark "$E" "remedy properties: right-click Body1"
glide 135 634; nap 1.0; xdotool click 3; nap 1.4
glide 213 653; nap 0.8
mark "$E" "remedy properties: open"
xdotool click 1; nap 1.6
shot "$O/props-remedy.png"
mark "$E" "remedy properties: rows held"
glide 900 500 16; nap 4.5
mark "$E" "recording stopped"
stop_record30
xdotool key Escape; sleep 0.5
wiggle; shot "$O/end.png"
python3 /work/lab/l3read.py "$O"
quit_app
