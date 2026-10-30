#!/bin/bash
# L7-Q11 (R1, pre-registered in out/l7/prereg.json): one Claude Code session in manual permission mode, in its real
# terminal; SolidCraft 0.27.0 is NOT running when it starts; after turn 1 the window opens beside it and lesson 3's hook
# is built there by a no-AI batch (lab/l7hook.py); both filmed. Lesson 3's l3claude.sh with two messages (M1, M2) and
# lesson 7's approval answers (lab/l7drive.py). Started by claude-run/l7run.sh on the host (it passes the session's sign-in as an environment variable; nothing about it is
# written to the run folder). The plug is added the documented way (`solidcraft-cli mcp setup`, what "?" > Connect AI
# assistants runs; lesson 1 filmed the menu), then wrapped in the logging proxy so every JSON-RPC line is kept.
# The session: a fresh home folder, an empty project folder, no CLAUDE.md, auto memory off, Claude Code's own defaults
# otherwise (2.1.311: auto mode). Messages are typed into the TUI; approvals, if asked, get the prompt's "Yes".
set -u
RUN=${1:-R1}
O=/work/out/l7/runs/$RUN
: "${M1:?M1 is required}" "${M2:?M2 is required}"
[ -e "$O/events.jsonl" ] && { echo "refusing: $O exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
. /work/lab/l2common.sh
SCALE=1.3           # SolidCraft in the right 1440 px of the 2880x1800 display (lesson 7 layout)
TERM_W=1440
E=$O/events.jsonl; : > "$E"; : > "$O/cursor.jsonl"
mkdir -p "$HOME/.config/Claude" "$HOME/.claude" "$HOME/Documents" /root/hook
python3 - <<'EOF'
import json, os
json.dump({'hasCompletedOnboarding': True, 'theme': 'light',
           'projects': {'/root/hook': {'hasTrustDialogAccepted': True, 'hasCompletedProjectOnboarding': True}}},
          open(os.path.expanduser('~/.claude.json'), 'w'), indent=1)
EOF
solidcraft-cli mcp setup > "$O/setup.txt" 2>&1
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
xdotool mousemove $((TERM_W + 900)) 1100; sleep 0.5
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 DISABLE_AUTOUPDATER=1
export LANG=C.UTF-8 LC_ALL=C.UTF-8      # run claude-1 had no locale: xterm drew a minus sign and ³ as "_"
CMD="claude --model claude-sonnet-5-5 --permission-mode manual"; [ -n "${DRY:-}" ] && CMD=bash
xterm -u8 -geometry 64x40+0+0 -fa "DejaVu Sans Mono" -fs 26 -bg white -fg black -T "Claude Code" \
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
cat > /tmp/between.sh <<EOS
. /work/lab/common.sh; W=2880; H=1800; . /work/lab/l2common.sh; . /work/lab/l7common.sh; export DISPLAY=:99
open_app "$O/app.log"; xdotool mousemove 1976 296 click 1; sleep 3
python3 /work/lab/l7hook.py "$O" "$O/entry-solidcraft-wrote.json" > "$O/hook-setup.txt" 2>&1
xdotool mousemove 2000 1100; sleep 0.5; xdotool mousemove 2002 1102; sleep 1
EOS
L7_BETWEEN="bash /tmp/between.sh" python3 /work/lab/l7drive.py "$O" "$T0" "$M1" "$M2"
xdotool mousemove 1300 700; sleep 0.5; xdotool mousemove 1302 702; sleep 2
mark "$E" "recording stopped"
stop_record30
shot "$O/after.png"
# the session's own record, then its cost line (after the recording)
cp /root/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
tmux capture-pane -p -t cc > "$O/pane-cost.txt"
ls -la "$HOME/Documents" > "$O/documents-after.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
pkill -x solidcraft
