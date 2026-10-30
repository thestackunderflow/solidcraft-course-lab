#!/bin/bash
# Lesson 7 ($0, no AI, no network): the failures a beginner meets, reproduced on purpose and filmed. A terminal (left)
# and SolidCraft 0.27.0's window (right) on one 2880x1800 virtual display, 30 fps, with a cursor log and events in
# seconds from the recording's start. Host side:
#   docker run --rm --name sc7-take --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc7-l7:0.27.0 bash /work/lab/l7take.sh TAKE
# TAKE:
#   setup     L7-Q2..Q5: Claude Code lists no plug -> "?" > Connect AI assistants -> Connected; a hand-typed entry
#             naming solidcraft-cli when it is not on PATH -> Failed to connect (ENOENT) -> Connect AI assistants again
#   headless  L7-Q6, Q7: the plug started before SolidCraft opens (lab/l7story.py headless)
#   errors    L7-Q8..Q10: a batch with a misspelt name, a refused save folder, then the saved file opened by
#             SolidCraft 0.26.1 (its window and its own plug) (lab/l7story.py errors)
set -u
TAKE=${1:?take}
O=/work/out/l7/$TAKE
[ -e "$O/events.jsonl" ] && { echo "refusing: $O exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
W=2880; H=1800
. /work/lab/l2common.sh
. /work/lab/l7common.sh
E=$O/events.jsonl; : > "$E"
NEWX=1976; NEWY=296            # the start page's New design (millimetres) at UI scale 1.3
HELPX=2448; HELPY=22           # the round "?" button
ITEMX=2564; ITEMY=306          # its last item, Connect AI assistants...
claude_home
start_display
solidcraft --version > "$O/version.txt" 2>&1; claude --version >> "$O/version.txt" 2>&1

newdesign() { glide $((NEWX * 2 / 3)) $((NEWY * 2 / 3)); nap 0.5; xdotool click 1; nap 2; }
connect() {       # connect TAG: the "?" button, then Connect AI assistants...; the dialog stays up 6 s; then closed
  mark "$E" "$1: hover ?"; glide $((HELPX * 2 / 3)) $((HELPY * 2 / 3)); nap 0.8; xdotool click 1; nap 1.6
  mark "$E" "$1: menu open"; shot "$O/$1-menu.png"
  glide $((ITEMX * 2 / 3)) $((ITEMY * 2 / 3)); nap 0.8; xdotool click 1; nap 1.5; wiggle
  mark "$E" "$1: dialog"; shot "$O/$1-dialog.png"; nap 6
  xdotool key Escape; nap 1; wiggle
  mark "$E" "$1: dialog closed"
  cp "$HOME/.claude.json" "$O/$1-claude.json"
}
run() {           # run TAG "command": typed in the terminal, waits for the prompt, keeps the screen text
  mark "$E" "$1: typing"; typecmd "$2"; mark "$E" "$1: Enter"
  waitprompt 120; mark "$E" "$1: done"; nap 1.5; pane_save "$O/$1-pane.txt"
}

if [ "$TAKE" = setup ]; then
  open_terminal
  xdotool mousemove 2000 900
  record30 "$O/screen.mp4" "$O/cursor.jsonl"
  mark "$E" "recording started: terminal (left); both Claude apps' settings folders exist; SolidCraft not started yet"
  nap 1
  run c0-folders "ls -a ~/.config/Claude ~/.claude.json"
  mark "$E" "SolidCraft starts (no flags)"; open_app "$O/app.log"; mark "$E" "SolidCraft open (start page)"
  # a person's first half minute: SolidCraft open, the mouse moving (does it add itself to the Claude apps?)
  for i in $(seq 1 15); do xdotool mousemove $((1800 + (i % 5) * 80)) $((700 + (i % 3) * 90)); sleep 2; done
  mark "$E" "30 s with SolidCraft open"
  cp "$HOME/.claude.json" "$O/claude.json-after-30s.json"; ls -la "$HOME/.config/Claude/" > "$O/desktop-folder-after-30s.txt"
  xdotool mousemove 2000 900
  run c0-grep "grep -c mcpServers ~/.claude.json"
  run c0-ls "ls -a ~/.config/Claude"
  run c1-list "claude mcp list"
  nap 2
  connect c1-connect
  run c1-list-after "claude mcp list"
  nap 2
  mark "$E" "case 2: the plug removed, then added by hand by its short name"
  run c2-remove "claude mcp remove solidcraft -s user"
  run c2-add "claude mcp add --scope user solidcraft -- solidcraft-cli mcp"
  run c2-list "claude mcp list"
  nap 2
  run c2-get "claude mcp get solidcraft"
  nap 2
  connect c2-connect
  run c2-list-after "claude mcp list"
  nap 2
  mark "$E" "case 5b: an entry edited by hand (--allow-path added), then Connect AI assistants"
  run c5-remove "claude mcp remove solidcraft -s user"
  run c5-add "claude mcp add --scope user solidcraft -- /opt/solidcraft-0.27.0/bin/solidcraft-cli mcp --allow-path /root/Documents"
  connect c5-connect
  run c5-list "claude mcp list"
  nap 3
  mark "$E" "recording stopped"
  stop_record30
  quit_app
fi

if [ "$TAKE" = headless ] || [ "$TAKE" = errors ]; then
  open_terminal; tmux send-keys -t t "cd /work; clear" Enter; sleep 1
  if [ "$TAKE" = errors ]; then open_app "$O/app.log"; newdesign; fi
  xdotool mousemove 2000 1000
  record30 "$O/screen.mp4" "$O/cursor.jsonl"
  mark "$E" "recording started ($TAKE)"
  nap 2
  mark "$E" "typing"; typecmd "python3 lab/l7story.py $TAKE out/l7/$TAKE"; mark "$E" "story started"
  cd /work
  while ! [ -f "$O/story.json" ]; do
    if [ -f "$O/wait-1" ] && ! [ -f "$O/go-1" ]; then
      nap 2; mark "$E" "SolidCraft opens"; open_app "$O/app.log"; newdesign; mark "$E" "SolidCraft open, new design"
      xdotool mousemove 2000 1000; nap 2; touch "$O/go-1"
    fi
    if [ -f "$O/wait-2" ] && ! [ -f "$O/go-2" ]; then
      nap 3; shot "$O/before-close.png"; mark "$E" "SolidCraft closes"; quit_app; mark "$E" "SolidCraft closed"; nap 2; touch "$O/go-2"
    fi
    if [ -f "$O/wait-3" ] && ! [ -f "$O/go-3" ]; then
      nap 2; mark "$E" "SolidCraft 0.27.0 closes"; quit_app; nap 1
      rm -rf "$HOME/.local/share/solidcraft/crashes"   # lab only: Ctrl+Q does not close the window under Xvfb, so
                                                       # quit_app stops it with TERM, which the next start reports as a crash
      mark "$E" "SolidCraft 0.26.1 opens"; open_app "$O/app-0.26.1.log" /opt/solidcraft-0.26.1/bin/solidcraft; newdesign
      mark "$E" "SolidCraft 0.26.1 open, new design"; xdotool mousemove 2000 1000; nap 2; touch "$O/go-3"
    fi
    sleep 0.3
  done
  waitprompt 60
  nap 3; wiggle
  shot "$O/end.png"
  mark "$E" "recording stopped"
  stop_record30
  pane_save "$O/pane.txt"
  [ -n "${APP:-}" ] && quit_app
fi
# events from the story script carry epoch times: convert to seconds from T0 beside the take's own events
python3 - "$O" "$T0" <<'EOF'
import json, os, sys
o, t0 = sys.argv[1], float(sys.argv[2])
p = os.path.join(o, 'story.jsonl')
if os.path.exists(p):
    rows = [json.loads(l) for l in open(p)]
    with open(os.path.join(o, 'events.jsonl'), 'a') as f:
        for r in rows:
            r['t'] = round(r['t'] - t0, 3); r['from'] = 'story'
            f.write(json.dumps(r) + '\n')
EOF
ls -la "$O"
