# Lesson 7 helpers (sourced after common.sh and l2common.sh inside sc7-l7:0.27.0): a 2880x1800 display, a terminal
# (xterm + tmux, so the script types into it at a person's pace and reads it back) in the left half and SolidCraft's
# window in the right half at UI scale 1.3, both filmed by record30. Events: seconds since the recording started.
TERM_W=1440
SCALE=1.3
export LANG=C.UTF-8 LC_ALL=C.UTF-8 DISABLE_AUTOUPDATER=1 CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
# The terminal's PATH has no SolidCraft folder: like a computer where the installer did not add it (lesson 7, case 2).
# The scripts start SolidCraft by its full path, off camera.
TPATH=/usr/local/bin:/usr/bin:/bin

claude_home() {   # both Claude apps "installed" (their folders), Claude Code onboarded, a project folder trusted
  mkdir -p "$HOME/.config/Claude" "$HOME/.claude" "$HOME/Documents" /root/hook
  python3 - <<'EOF'
import json, os
json.dump({'hasCompletedOnboarding': True, 'theme': 'light',
           'projects': {'/root/hook': {'hasTrustDialogAccepted': True, 'hasCompletedProjectOnboarding': True}}},
          open(os.path.expanduser('~/.claude.json'), 'w'), indent=1)
EOF
  printf 'set -g status off\nset -g history-limit 5000\n' > "$HOME/.tmux.conf"
}

open_app() {      # open_app LOG [BIN]: SolidCraft in the right half, light theme, a new design
  start_app "$1" "${2:-/opt/solidcraft/bin/solidcraft}"
  for i in $(seq 1 40); do [ -f "$HOME/.local/share/solidcraft/control/27878.token" ] && break; sleep 0.5; done
  sleep 6
  python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
  fill_window $TERM_W 0 $((W - TERM_W)) $H; sleep 1
}

open_terminal() { # open_terminal: bash in tmux session "t" in the left half, prompt "$ ", 30 px font
  xterm -u8 -geometry 80x40+0+0 -fa "DejaVu Sans Mono" -fs 22 -bg white -fg black -T "Terminal" \
    -e env PATH=$TPATH PS1='$ ' tmux -u new-session -s t -c /root/hook "bash --norc" > /dev/null 2>&1 &
  sleep 3
  local w; w=$(xdotool search --name "^Terminal$" | head -1)
  xdotool windowsize --sync "$w" $TERM_W $H; xdotool windowmove "$w" 0 0
  tmux send-keys -t t "export PS1='\$ ' PATH=$TPATH; clear" Enter; sleep 1
}

typecmd() {       # typecmd "text": typed into the terminal one character at a time (about 14 a second), then Enter
  local s=$1 i
  for ((i = 0; i < ${#s}; i++)); do tmux send-keys -t t -l "${s:i:1}"; sleep 0.07; done
  nap 0.6; tmux send-keys -t t Enter
}

waitprompt() {    # waitprompt [SECONDS]: until the terminal's last non-empty line is the bare prompt again
  local n=${1:-90} i
  for ((i = 0; i < n * 4; i++)); do
    [ "$(tmux capture-pane -p -t t | sed '/^[[:space:]]*$/d' | tail -1)" = '$' ] && return 0
    sleep 0.25
  done
  return 1
}

pane_save() { tmux capture-pane -p -J -S -300 -t t > "$1"; }
