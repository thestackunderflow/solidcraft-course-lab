#!/bin/bash
# fx8 take D (LAB-fx8): a terminal (xterm + tmux, white, 22 pt) in the left half over SolidCraft's window, the no-AI
# client typed at a person's pace: python3 -I D/noai.py |& tee D/reply.txt. The whole display is filmed.
set -u
. /work/lab/fx8lib.sh
take D
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
export LANG=C.UTF-8 LC_ALL=C.UTF-8
printf 'set -g status off\nset -g history-limit 5000\n' > "$HOME/.tmux.conf"
xterm -u8 -geometry 80x40+0+0 -fa "DejaVu Sans Mono" -fs 22 -bg white -fg black -T "Terminal" \
  -e env PS1='$ ' tmux -u new-session -s t -c /work/out/fx8 "bash --norc" > /dev/null 2>&1 &
sleep 3
w=$(xdotool search --name "^Terminal$" | head -1)
xdotool windowsize --sync "$w" 1440 $H; xdotool windowmove "$w" 0 0
tmux send-keys -t t "export PS1='\$ '; clear" Enter; sleep 1
xdotool mousemove 2200 900; sleep 0.5
rec_start
ev "recording started: terminal (left) over SolidCraft, an empty design (right), full display"
nap 3.0
cmd='python3 -I D/noai.py |& tee D/reply.txt'
ev "typed: $cmd"
for ((i = 0; i < ${#cmd}; i++)); do tmux send-keys -t t -l "${cmd:i:1}"; sleep 0.08; done
nap 0.8; tmux send-keys -t t Enter
ev "Enter"
for i in $(seq 1 240); do [ "$(tmux capture-pane -p -t t | sed '/^[[:space:]]*$/d' | tail -1)" = '$' ] && break; sleep 0.25; done
ev "replies shown: hold 6 s"
nap 6.0
tmux capture-pane -p -J -S -300 -t t > "$O/pane.txt"
cp_shot terminal
ev "recording stopped"
rec_stop
read_now d-after
tmux kill-server; sleep 1
