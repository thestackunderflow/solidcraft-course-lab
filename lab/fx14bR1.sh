#!/bin/bash
# fx14b R1 (LAB-fx14b section 4, pre-registered, one run, no retry): Claude Code full screen in its real
# terminal (xterm + tmux) over SolidCraft 0.28.0, which is open on ~/conv.sc (take P: block 40 x 30 x 20 saved as a mesh,
# inserted and converted, 24,000.00 mm3, top F4:face:5 exact false; opened by lab/fx9.py before the recording). A copy of
# lab/fx13R1.sh as fixed in ddb6e4e (--strict-mcp-config, SolidCraft only; claude.ai lines dropped from mcp-list.txt) with
# the hole checker lab/fx14bhole.py before/after in place of fx13wall.py. Plug added by `solidcraft-cli mcp setup` + lesson 7 --allow-path.
# Auto mode as lesson 7 (lab/l7drive.py). One message.
# After the recording: SolidCraft raised, after.png (home view) + after-2.png (turned), Measure of every body + the
# timeline (read-after.json), session.jsonl, /cost. Started by claude-run/fx14brun.sh: the sign-in file is mounted read-only at /creds.json, copied in, deleted on exit.
set -u
O=/work/out/fx14b/runs/R1
: "${M1:?M1 is required}"
[ -e "$O/events.jsonl" ] && { echo "refusing: $O exists"; exit 1; }
mkdir -p "$O"
unset ANTHROPIC_API_KEY
mkdir -p "$HOME/.claude"; cp /creds.json "$HOME/.claude/.credentials.json"
trap 'rm -f "$HOME/.claude/.credentials.json"' EXIT
. /work/lab/fx13lib.sh
APP_H=$H
E=$O/events.jsonl; : > "$E"; : > "$O/cursor.jsonl"
mkdir -p "$HOME/.config/Claude"
python3 - <<'PY'
import json, os
json.dump({'hasCompletedOnboarding': True, 'theme': 'light',
           'projects': {'/root': {'hasTrustDialogAccepted': True, 'hasCompletedProjectOnboarding': True}}},
          open(os.path.expanduser('~/.claude.json'), 'w'), indent=1)
PY
solidcraft-cli mcp setup > "$O/setup.txt" 2>&1
start_display
openbox > /dev/null 2>&1 &
sleep 1
start_app "$O/app.log" /opt/solidcraft/bin/solidcraft
sleep 10
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
fill_window 0 0 $W $H; sleep 2
g 398 206 6; xdotool click 1; sleep 3                          # start page: New design
cp /work/out/fx14b/P/conv.sc /root/conv.sc
FX9_ALLOW=1 python3 /work/lab/fx9.py open /root/conv.sc > "$O/open.txt" 2>&1; sleep 3
FX9_ALLOW=1 python3 /work/lab/fx9.py read "$O" before > "$O/read-before.txt" 2>&1
FX9_ALLOW=1 python3 /work/lab/fx14bhole.py "$O" before > "$O/hole-before.txt" 2>&1   # the STL is removed by the checker
sleep 2; shot "$O/block-before.png"
python3 - "$O" <<'PY'
import json, os, sys
o = sys.argv[1]
p = os.path.expanduser('~/.claude.json')
d = json.load(open(p))
e = d['mcpServers']['solidcraft']
e = dict(e, args=list(e.get('args') or []) + ['--allow-path', '/root'])     # lesson 7's fix
json.dump({'mcpServers': {'solidcraft': e}}, open(os.path.join(o, 'entry-solidcraft-wrote.json'), 'w'), indent=1)
d['mcpServers']['solidcraft'] = dict(e, command='python3', args=['/work/proxy/mcp_log_proxy.py', '--log', o + '/transcript.jsonl',
                                     '--png-dir', o, '--watchdog', '330', '--', e['command']] + list(e.get('args') or []))
json.dump(d, open(p, 'w'), indent=1)
json.dump({'mcpServers': {'solidcraft': d['mcpServers']['solidcraft']}}, open(os.path.join(o, 'entry-as-run.json'), 'w'), indent=1)
PY
printf 'set -g status off\nset -g mouse on\n' > "$HOME/.tmux.conf"
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 DISABLE_AUTOUPDATER=1
# 13 Nov: never record the owner's claude.ai account connectors (names/URLs are personal account details)
(cd /root && claude mcp list) 2>&1 | grep -v '^claude\.ai ' > "$O/mcp-list.txt"
cat "$O/mcp-list.txt"
grep -qi 'solidcraft.*connected' "$O/mcp-list.txt" || echo "R1-1: the server is not listed as connected (see mcp-list.txt)"
claude --version > "$O/claude-version.txt" 2>&1
xterm -u8 -geometry 120x40+0+0 -fa "DejaVu Sans Mono" -fs 22 -bg white -fg black -T "Claude Code" \
  -e tmux -u new-session -s cc -c /root "claude --model claude-sonnet-5-5 --strict-mcp-config --mcp-config $O/entry-as-run.json" > /dev/null 2>&1 &
sleep 12
w=$(xdotool search --name "^Claude Code$" | head -1); [ -n "$w" ] && { xdotool windowsize --sync "$w" $W $H; xdotool windowmove "$w" 0 0; xdotool windowactivate --sync "$w"; }
sleep 2
tmux capture-pane -p -t cc > "$O/pane-start.txt"
# the plan banner (logo, model, plan name) is kept out of the footage: reset the pane's screen and drop its history
# before the recording (tested off the record in out/scratch/fx9banner, fx9 R1: Claude Code redraws its prompt on the next key)
tmux send-keys -t cc -R; tmux clear-history -t cc; sleep 1
tmux capture-pane -p -t cc > "$O/pane-after-reset.txt"
xdotool mousemove 2700 1500; sleep 0.5
shot "$O/before.png"
record30 "$O/screen.mp4" "$O/cursor.jsonl" nomouse
mark "$E" "recording started: Claude Code full screen; SolidCraft behind it on ~/conv.sc (the converted 40 x 30 x 20 block, top at z 20)"
sleep 3
python3 /work/lab/l7drive.py "$O" "$T0" "$M1"
sleep 4
tmux capture-pane -p -J -S -2000 -t cc > "$O/pane-reply.txt"
shot "$O/reply.png"
mark "$E" "recording stopped"
stop_record30
# the block after the run (not part of the terminal recording)
s=$(xdotool search --name SolidCraft | head -1); xdotool windowactivate --sync "$s"; sleep 2
shot "$O/after.png"
xdotool mousemove 1333 440; xdotool mousedown 2
for i in $(seq 1 40); do xdotool mousemove_relative -- -8 1; sleep 0.05; done
xdotool mouseup 2; sleep 1; xdotool mousemove 2700 1500; sleep 1
shot "$O/after-2.png"
FX9_ALLOW=1 python3 /work/lab/fx9.py read "$O" after > "$O/read-after.txt" 2>&1
FX9_ALLOW=1 python3 /work/lab/fx14bhole.py "$O" after > "$O/hole-after.txt" 2>&1
cp /root/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
w=$(xdotool search --name "^Claude Code$" | head -1); xdotool windowactivate --sync "$w"; sleep 1
tmux send-keys -t cc Escape; sleep 1
tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
tmux capture-pane -p -t cc > "$O/pane-cost.txt"
tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 2
pkill -x solidcraft
rm -f "$HOME/.claude/.credentials.json"
echo "R1 done"
