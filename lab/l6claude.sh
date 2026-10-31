#!/bin/bash
# L6-Q4: one Claude Code session in its real terminal, beside SolidCraft 0.28.0's window with lesson 5's finished hook
# open (lesson 4's hook + the print face on the J side, built by script before the recording, no AI, lab/l6part.py),
# PrusaSlicer 2.9.2 installed and seeded, all filmed; the run's one message from M1, driven by lab/l6drive.py (copies
# every file sent to the slicer, moves a slicer window beside the terminal); after the turn, still filmed, our no-AI
# read (lab/l6read.py --send: the referee) sends the design to PrusaSlicer and the driver presses Slice now. Started by
# claude-run/l6run.sh on the host (it passes the session's sign-in as an environment variable; nothing about it is
# written to the run folder). The plug is added the documented way (`solidcraft-cli mcp setup`), then wrapped in the
# logging proxy so every JSON-RPC line is kept. The session: a fresh home folder, an empty project folder, no
# CLAUDE.md, auto memory off, Claude Code's own defaults otherwise. Approvals, if asked, get the prompt's "Yes".
set -u
RUN=${1:-A1}
O=/work/out/l6/runs/$RUN; [ -n "${DRY:-}" ] && O=/work/out/scratch/l6claude-dry/$RUN
: "${M1:?M1 (message 1) is required}"
[ -e "$O/read.json" ] && { echo "refusing: $O/read.json exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
. /work/lab/l2common.sh
. /work/lab/l5slicerseed.sh
record30() {      # lesson 6 (amended after B1): as l2common's, but a fragmented MP4, playable even if the run is killed
  ffmpeg -loglevel error -y -f x11grab -draw_mouse 0 -framerate 30 -video_size ${W}x${H} -i :99     -c:v libx264 -preset ultrafast -crf 14 -pix_fmt yuv420p -movflags +frag_keyframe+empty_moov "$1" &
  REC=$!; T0=$(date +%s.%N); sleep 0.5
  python3 /work/lab/cursorlog.py "$2" "$T0" 30 & CUR=$!
  CURSOR_LOG=$2
}
SCALE=1.5           # SolidCraft in the right 1730 px of the 2880x1800 display (a 1153x1200 layout)
TERM_W=1150
E=$O/events.jsonl; : > "$E"; : > "$O/cursor.jsonl"
mkdir -p "$HOME/.config/Claude" "$HOME/.claude" /root/hook
python3 - <<'EOF'
import json, os
json.dump({'hasCompletedOnboarding': True, 'theme': 'light',
           'projects': {'/root/hook': {'hasTrustDialogAccepted': True, 'hasCompletedProjectOnboarding': True}}},
          open(os.path.expanduser('~/.claude.json'), 'w'), indent=1)
EOF
solidcraft-cli mcp setup > "$O/setup.txt" 2>&1
seed_slicer
python3 - "$O" <<'EOF'
import json, os, sys
o = sys.argv[1]
p = os.path.expanduser('~/.claude.json')
d = json.load(open(p))
e = d['mcpServers']['solidcraft']
json.dump({'mcpServers': {'solidcraft': e}}, open(os.path.join(o, 'entry-solidcraft-wrote.json'), 'w'), indent=1)
d['mcpServers']['solidcraft'] = dict(e, command='python3', args=['/work/proxy/mcp_log_proxy.py', '--log', o + '/transcript.jsonl',
                                     '--png-dir', o, '--watchdog', '330', '--', e['command']] + list(e.get('args') or []))
json.dump(d, open(p, 'w'), indent=1)
json.dump({'mcpServers': {'solidcraft': d['mcpServers']['solidcraft']}}, open(os.path.join(o, 'entry-as-run.json'), 'w'), indent=1)
EOF
printf 'set -g status off\nset -g mouse on\n' > "$HOME/.tmux.conf"
start_display
start_app "$O/app.log"
sleep 10
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
fill_window $TERM_W 0 $((W - TERM_W)) $H; sleep 1
ENTRY=$O/entry-solidcraft-wrote.json python3 - "$O" <<'PY' > "$O/part-setup.txt" 2>&1
import json, os, sys
sys.path.insert(0, '/work'); sys.path.insert(0, '/work/lab')
from client.mcp import McpClient
from l6part import L6_START
o = sys.argv[1]
e = json.load(open(os.environ['ENTRY']))['mcpServers']['solidcraft']
c = McpClient([e['command']] + list(e.get('args') or []), timeout_s=120, log_path=os.path.join(o, 'part-setup-transcript.jsonl'))
c.start()
b = McpClient.text_json(c.call_tool('batch', {'commands': L6_START, 'verbose': False}))
m = McpClient.text_json(c.call_tool('measure', {}))
s = McpClient.text_json(c.call_tool('execute', {'command': 'file.slicers', 'params': {}}))
c.call_tool('execute', {'command': 'view.home', 'params': {}})
c.close()
json.dump({'batch_ok': b.get('ok'), 'measure': m, 'slicers': s}, open(os.path.join(o, 'part-setup.json'), 'w'), indent=1)
print('part', (m.get('total') or {}).get('volume_mm3'), 'slicers', s)
PY
xdotool key Escape; sleep 1.5                           # the start page shows over the design: Esc = Back to Untitled
xdotool mousemove $((TERM_W + 900)) 1100; sleep 0.5
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 DISABLE_AUTOUPDATER=1
export LANG=C.UTF-8 LC_ALL=C.UTF-8      # run claude-1 had no locale: xterm drew a minus sign and ³ as "_"
CMD="claude --model claude-sonnet-5-5"; [ -n "${DRY:-}" ] && CMD=bash
xterm -u8 -geometry 46x36+0+0 -fa "DejaVu Sans Mono" -fs 30 -bg white -fg black -T "Claude Code" \
  -e tmux -u new-session -s cc -c /root/hook "$CMD" > /dev/null 2>&1 &
sleep 12
tmux capture-pane -p -t cc > "$O/pane-start.txt"
claude --version > "$O/claude-version.txt" 2>&1
for w in $(xdotool search --onlyvisible --name ".*"); do echo "$w $(xdotool getwindowname "$w") $(xdotool getwindowgeometry "$w" | tr '\n' ' ')"; done > "$O/windows.txt"
xdotool mousemove $((TERM_W + 900)) 1102; sleep 0.5
shot "$O/before.png"
[ -n "${DRY:-}" ] && { echo "DRY: layout only"; quit_app; exit 0; }
record30 "$O/screen.mp4" "$O/cursor.jsonl" nomouse
mark "$E" "recording started: Claude Code (left), SolidCraft with a new design (right)"
sleep 2
python3 /work/lab/l6drive.py "$O" "$T0" "$M1" "$TERM_W"
xdotool mousemove 1300 700; sleep 0.5; xdotool mousemove 1302 702; sleep 2
mark "$E" "recording stopped"
stop_record30
shot "$O/after.png"
# the session's own record, then its cost line (after the recording)
cp /root/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
tmux capture-pane -p -t cc > "$O/pane-cost.txt"
for f in "$O"/sent-*; do [ -e "$f" ] && python3 -c "import sys, json; sys.path.insert(0, '/work'); from checker import m3mf, stl; f = sys.argv[1]; print(json.dumps(m3mf.check(f) if f.endswith('.3mf') else stl.check(f)))" "$f"; done > "$O/sent-check.jsonl" 2>&1
pkill -x slic3r_main
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
quit_app
