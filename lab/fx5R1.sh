#!/bin/bash
# fx5 R1 (LAB-fx5 section 4, pre-registered in 025e2f2; one run, no second try). Runs inside the fx5 session container
# (lab/fx5session.sh runs/R1, started WITH the network for Claude's servers and the subscription login mounted
# read-only at /creds.json): docker exec fx5-R1 bash /work/lab/fx5R1.sh part1 | part2
#   part1: recording on, the first send BY HAND (PrusaSlicer shows 25), Claude Code set up (login copied in), mcp list.
#   part2: claude started with no flags (Claude Code's default auto mode, as lesson 7 R1), the one prompt typed, the
#          reply waited for, screenshots, the session file copied, /cost, /exit, the login deleted.
# The by-hand Reload from disk after the run is done step by step with fx5lib.sh helpers (events in events.txt).
set -u
. /work/lab/fx5lib.sh
PROMPT='Change hook_depth to 40 and send it to the slicer again.'
case "${1:?part1|part2}" in
part1)
  rec_start
  ev "recording started: SolidCraft with the saved hook (hook_depth 25), no slicer open (R1)"
  nap 2
  ev "send 1 (by hand): right-click Body1"; send_open
  ev "send 1 (by hand): Send window"; send_click
  ev "send 1 (by hand): Send clicked"
  for i in $(seq 1 60); do [ -n "$(prusa_win)" ] && break; sleep 1; done
  ev "send 1 (by hand): slicer window up"
  sleep 12
  shot "$O/before-slicer-25.png"
  ev "send 1 (by hand): slicer shows the hook (25)"
  unset ANTHROPIC_API_KEY
  mkdir -p /root/.claude /root/fx5-run
  cp /creds.json /root/.claude/.credentials.json            # copied in; deleted in part2 before the container ends
  python3 - <<'EOF'
import json, os
p = os.path.expanduser('~/.claude.json')
d = json.load(open(p))
d.update(hasCompletedOnboarding=True, theme='light')
d.setdefault('projects', {})['/root/fx5-run'] = {'hasTrustDialogAccepted': True, 'hasCompletedProjectOnboarding': True}
json.dump(d, open(p, 'w'), indent=1)
EOF
  { claude --version; echo "launch: claude (no flags: Claude Code's own default mode, auto mode, and default model), as lesson 7 R1"; echo "folder: ~/fx5-run (empty), no CLAUDE.md, no prior messages"; } > "$O/pins.txt" 2>&1
  (cd /root/fx5-run && ENABLE_CLAUDEAI_MCP_SERVERS=false claude mcp list) > "$O/mcp-list.txt" 2>&1
  cat "$O/mcp-list.txt" | tail -3
  ;;
part2)
  grep -qi connected "$O/mcp-list.txt" || { echo "R1-1: not connected"; exit 1; }
  unset ANTHROPIC_API_KEY
  export ENABLE_CLAUDEAI_MCP_SERVERS=false CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 DISABLE_AUTOUPDATER=1 LANG=C.UTF-8 LC_ALL=C.UTF-8
  printf 'set -g status off\nset -g mouse on\n' > /root/.tmux.conf
  setsid xterm -u8 -geometry 64x40+0+0 -fa "DejaVu Sans Mono" -fs 26 -bg white -fg black -T "Claude Code" \
    -e tmux -u new-session -s cc -c /root/fx5-run claude < /dev/null > /dev/null 2>&1 &
  sleep 12
  ev "claude: started (no flags)"
  tmux capture-pane -p -t cc > "$O/pane-start.txt"
  ev "claude: typed"
  python3 - "$O" "$T0" "$PROMPT" <<'EOF'
import sys
sys.path.insert(0, '/work/lab')
import l7drive
l7drive.main(sys.argv[1], float(sys.argv[2]), [sys.argv[3]])
EOF
  ev "turn 1: reply done"
  shot "$O/reply.png"
  sleep 10
  w=$(prusa_win); [ -n "$w" ] && { xdotool windowactivate --sync "$w"; sleep 2; }
  shot "$O/slicer-after.png"
  ev "slicer: 10 s after the reply"
  winlist > "$O/windows-after.txt"
  ps -o pid,args -C prusa-slicer > "$O/ps-after.txt" 2>&1
  cp /root/.claude/projects/*/*.jsonl "$O/session.jsonl" 2>/dev/null
  tmux send-keys -t cc -l "/cost"; sleep 0.5; tmux send-keys -t cc Enter; sleep 3
  tmux capture-pane -p -t cc -S -3000 > "$O/pane-cost.txt"
  tmux send-keys -t cc -l "/exit"; sleep 0.3; tmux send-keys -t cc Enter; sleep 3
  tmux capture-pane -p -t cc -S -3000 > "$O/pane-exit.txt" 2>/dev/null
  rm -f /root/.claude/.credentials.json; ls /root/.claude/.credentials.json 2>&1 | tail -1
  ;;
esac
