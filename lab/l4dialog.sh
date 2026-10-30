#!/bin/bash
# L4-Q4 (rule written in PLAN-L4 rev 2 before this ran): does SolidCraft 0.27.1's Hole window take `width / 2` in its
# Distance 2 box? Each try: a fresh design with lesson 3's hook and hole_d (plug, no AI), then the Hole window through
# the real UI (xdotool): the face, Extents All, Reference 1 = the top edge (15, or 45 for the second hole), Reference 2
# = an edge, Distance 2 = the expression, Diameter hole_d. Recorded per try: a screenshot, whether OK is enabled
# (its blue) and whether a red message line shows; after an error, 10 is retyped and OK checked again. Try 1 is filmed.
#   docker run --rm --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc4-l4:0.27.1 bash /work/lab/l4dialog.sh
# Writes out/l4/dialog/: tries.jsonl, try-N*.png, screen.mp4 (try 1), events.jsonl.
set -u
O=/work/out/l4/dialog
[ -e "$O/tries.jsonl" ] && { echo "refusing: $O/tries.jsonl exists"; exit 1; }
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
c43() { awk -v v="$1" 'BEGIN{printf "%d", v*4/3}'; }
g() { glide "$(c43 "$1")" "$(c43 "$2")" "${3:-14}"; }
click() { xdotool click 1; }
typed() { xdotool type --delay "${2:-90}" "$1"; }
g 398 230 4; sleep 0.5; click; sleep 3                           # start page: New design
fresh() {   # fresh 1|2: a new design with the hook and hole_d (and, for the second hole, the first hole by plug)
  python3 - "$1" <<'PY'
import json, os, sys
sys.path.insert(0, '/work'); sys.path.insert(0, '/work/lab')
from checker import entry
from client.mcp import McpClient
from l7story import HOOK
e = entry.read(os.path.expanduser('~/.claude.json'))
c = McpClient([e['command']] + e['args'], timeout_s=120)
c.start()
c.call_tool('new_design', {})
c.call_tool('batch', {'commands': HOOK, 'verbose': False})
c.call_tool('set_parameter', {'name': 'hole_d', 'value': 4.5})
if sys.argv[1] == '2':
    c.call_tool('execute', {'command': 'solid.hole', 'params': {'position': [5, -10, 45], 'diameter': 'hole_d',
                'references': [{'edge': [5, -10, 60], 'distance': '15'}, {'edge': [5, -20, 30], 'distance': '10'}]}})
c.call_tool('execute', {'command': 'view.home', 'params': {}})
c.close()
PY
  sleep 1.5
}
okstate() {   # okstate PNG -> "ok_enabled red_line": OK's blue at y 742 or 758 (1440 units), red text in the dialog
  convert "$1" -resize 1440x900! /tmp/s.png
  python3 - /tmp/s.png <<'PY'
import subprocess, sys
def px(x, y):
    o = subprocess.run(['convert', sys.argv[1], '-format', '%[pixel:p{%d,%d}]' % (x, y), 'info:'], capture_output=True, text=True).stdout
    v = [float(t) for t in o[o.find('(') + 1:o.find(')')].replace('%', '').split(',')[:3]]
    return [t * 2.55 if '%' in o else t for t in v]
blue = any((lambda p: p[2] > 150 and p[0] < 90)(px(1395, y)) for y in (742, 758))
o = subprocess.run(['convert', sys.argv[1], '-crop', '230x40+1205+665', '-format', '%c', 'histogram:info:'], capture_output=True, text=True).stdout
red = 0
for line in o.splitlines():
    try:
        n = int(line.split(':')[0]); rgb = line[line.find('(') + 1:line.find(')')].split(',')[:3]
        r, g, b = [float(x) for x in rgb]
        if r > 150 and g < 90 and b < 90: red += n
    except Exception:
        pass
print(int(blue), int(red > 40))
PY
}
TRY=0
try() {   # try HOLE EDGE EXPR  (HOLE 1|2; EDGE left|right)
  TRY=$((TRY + 1))
  fresh "$1"
  local fy=330 d1=15 ex=666 ey=470
  [ "$1" = 2 ] && { fy=560; d1=45; }
  [ "$2" = right ] && { ex=802; ey=420; }
  mark "$E" "try $TRY: Hole button"
  g 297 90; sleep 0.8; click; sleep 1.4
  mark "$E" "try $TRY: the face"
  g 737 "$fy"; sleep 0.8; click; sleep 1.6
  g 1355 468; click; sleep 0.8; g 1310 546 8; click; sleep 1.0
  mark "$E" "try $TRY: Reference 1, top edge"
  g 1355 409; click; sleep 0.6; g 733 211; sleep 0.6; click; sleep 1.0
  g 1355 438; click; sleep 0.3; xdotool key ctrl+a; typed "$d1"; xdotool key Tab; sleep 1.0
  mark "$E" "try $TRY: Reference 2, $2 edge"
  g 1355 468; click; sleep 0.6; g "$ex" "$ey"; sleep 0.6; click; sleep 1.0
  g 1360 660; click; sleep 0.3; xdotool key ctrl+a; typed hole_d; xdotool key Tab; sleep 0.8
  mark "$E" "try $TRY: Distance 2 = $3"
  g 1355 498; click; sleep 0.3; xdotool key ctrl+a; typed "$3" 150; xdotool key Tab; sleep 2.5
  g 1000 820 8; sleep 0.8
  shot "$O/try-$TRY.png"
  read -r ok red < <(okstate "$O/try-$TRY.png")
  mark "$E" "try $TRY: result ok=$ok red=$red"
  local ok2="" red2=""
  if [ "$ok" = 0 ] || [ "$red" = 1 ]; then
    mark "$E" "try $TRY: retype 10"
    g 1355 498; click; sleep 0.3; xdotool key ctrl+a; typed 10 150; xdotool key Tab; sleep 2.5
    g 1000 820 8; sleep 0.8
    shot "$O/try-$TRY-retyped.png"
    read -r ok2 red2 < <(okstate "$O/try-$TRY-retyped.png")
    mark "$E" "try $TRY: after retype ok=$ok2 red=$red2"
  fi
  printf '{"try": %d, "hole": %s, "edge": "%s", "expression": "%s", "ok_enabled": %s, "red_line": %s, "after_retype_ok": "%s", "after_retype_red": "%s"}\n' \
    "$TRY" "$1" "$2" "$3" "$ok" "$red" "$ok2" "$red2" >> "$O/tries.jsonl"
  mark "$E" "try $TRY: Cancel"
  g 1322 742; click; sleep 0.6; g 1322 758; click; sleep 0.6; xdotool key Escape; sleep 1.0
}
record30 "$O/screen.mp4" "$O/cursor.jsonl"
mark "$E" "recording started"
try 1 left "width / 2"
mark "$E" "recording stopped"
stop_record30
try 1 left "width / 2"
try 1 left "width / 2"
try 2 left "width / 2"
try 2 left "width / 2"
try 2 left "width / 2"
try 1 left "10"
try 1 left "20 / 2"
try 1 left "hole_d * 2"
try 1 right "width / 2"
try 2 right "width / 2"
cat "$O/tries.jsonl"
quit_app
