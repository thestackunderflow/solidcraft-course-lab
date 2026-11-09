#!/bin/bash
# fx6 R1 (LAB-fx6 section 4, pre-registered, one try): Claude Code 2.1.311 in its real terminal (left half) beside
# SolidCraft 0.28.0 (right half, UI scale 1.3) with lesson 3's hook open and saved as ~/hook-l3.sc (thickness 5). The plug
# added the documented way (`solidcraft-cli mcp setup`), wrapped in the logging proxy (lesson 7). Claude Code's own
# default permission mode (auto); approval prompts get lesson 7's pre-registered answers (lab/l7drive.py). One message.
# Started by claude-run/fx6run.sh: the sign-in file is mounted read-only at /creds.json, copied in, deleted on exit.
set -u
O=/work/out/fx6/runs/R1; [ -n "${DRY:-}" ] && O=/work/out/scratch/fx6R1dry && rm -rf "$O"
: "${M1:?M1 is required}"
[ -e "$O/events.jsonl" ] && { echo "refusing: $O exists"; exit 1; }
mkdir -p "$O"
unset ANTHROPIC_API_KEY
mkdir -p "$HOME/.claude"; [ -z "${DRY:-}" ] && cp /creds.json "$HOME/.claude/.credentials.json"
trap 'rm -f "$HOME/.claude/.credentials.json"' EXIT
W2=2880 H2=1620
. /work/lab/common.sh
W2=2880 H2=1620 . /work/lab/l2common.sh
SCALE=1.3; TERM_W=1440
E=$O/events.jsonl; : > "$E"; : > "$O/cursor.jsonl"
mkdir -p "$HOME/.config/Claude" /root/hook
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
openbox > /dev/null 2>&1 &
sleep 1
# SolidCraft in the right half, a new design, the hook built with no AI and saved (off camera, before the recording)
start_app "$O/app.log" /opt/solidcraft/bin/solidcraft
sleep 10
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
fill_window $TERM_W 0 $((W - TERM_W)) $H; sleep 2
shot "$O/start-page.png"
NEWX=${NEWX:-1976}; NEWY=${NEWY:-296}
xdotool mousemove "$NEWX" "$NEWY" click 1; sleep 3
FX6_ENTRY="$O/entry-solidcraft-wrote.json" python3 /work/lab/fx6hook.py build "$O" > "$O/hook-setup.txt" 2>&1
sleep 8
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 DISABLE_AUTOUPDATER=1 LANG=C.UTF-8 LC_ALL=C.UTF-8
(cd /root/hook && claude mcp list) > "$O/mcp-list.txt" 2>&1
claude --version > "$O/claude-version.txt" 2>&1
CMD="claude --model claude-sonnet-5-5"; [ -n "${DRY:-}" ] && CMD=bash
xterm -u8 -geometry 64x40+0+0 -fa "DejaVu Sans Mono" -fs 26 -bg white -fg black -T "Claude Code" \
  -e tmux -u new-session -s cc -c /root/hook "$CMD" > /dev/null 2>&1 &
sleep 12
w=$(xdotool search --name "^Claude Code$" | head -1); [ -n "$w" ] && { xdotool windowsize --sync "$w" $TERM_W $H; xdotool windowmove "$w" 0 0; }
sleep 2
tmux capture-pane -p -t cc > "$O/pane-start.txt"
xdotool mousemove $((TERM_W + 900)) 1100; sleep 0.5
shot "$O/before.png"
[ -n "${DRY:-}" ] && { echo "DRY: layout only"; exit 0; }
record30 "$O/screen.mp4" "$O/cursor.jsonl" nomouse
mark "$E" "recording started: Claude Code (left), SolidCraft with lesson 3's hook (right)"
sleep 3
python3 /work/lab/l7drive.py "$O" "$T0" "$M1"
sleep 3
mark "$E" "recording stopped"
stop_record30
shot "$O/after.png"
FX6_ENTRY="$O/entry-solidcraft-wrote.json" python3 /work/lab/fx6hook.py read "$O" after > "$O/read-after.txt" 2>&1
cp /root/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
tmux capture-pane -p -t cc > "$O/pane-cost.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
pkill -x solidcraft
rm -f "$HOME/.claude/.credentials.json"
echo "R1 done"
