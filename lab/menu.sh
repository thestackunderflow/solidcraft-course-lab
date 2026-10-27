#!/bin/bash
# Q3, Q4, Q5: the menu Help > Connect AI assistants (the "?" button at the top right of the window, 0.24.1).
#   A. No Claude app yet (no config folders): SolidCraft open, the menu clicked.         -> what it says, the files
#   B. The Claude apps "installed" while SolidCraft runs (their config folders created): the menu clicked again.
#   C. SolidCraft quit and started again: does the start change the entry the menu wrote?
# The window is filmed; the dialog, the files and their hashes are kept. Host side:
#   docker run --rm --memory 3g --shm-size 1g --network none -v "$PWD:/work" sc1-app:0.24.1 bash /work/lab/menu.sh
set -u
O=/work/out/l1/menu
[ -e "$O" ] && { echo "refusing: $O exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
T=$O/timeline.jsonl
HELP_X=1269; HELP_Y=17; ITEM_X=1358; ITEM_Y=236; CLOSE_X=1022; CLOSE_Y=499

open_menu() {     # open_menu NAME: Help, then Connect AI assistants; screenshots of the menu and the dialog
  xdotool mousemove $HELP_X $HELP_Y click 1; sleep 1.5; shot "$O/$1-menu.png"
  xdotool mousemove $ITEM_X $ITEM_Y click 1; sleep 3; shot "$O/$1-dialog.png"
  event "$T" "$1: Help > Connect AI assistants clicked"
}

start_display
record "$O/menu.mp4"
start_app "$O/app-1.log"
sleep 8
python3 /work/client/ctl.py ui.prefs '{"theme":"light"}' 27878 > "$O/theme-reply.json" 2>&1
xdotool mousemove 442 228 click 1; sleep 3
client_files > "$O/files-A-before.txt"
open_menu A-no-claude
client_files > "$O/files-A-after.txt"
xdotool mousemove $CLOSE_X $CLOSE_Y click 1; sleep 1
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
event "$T" "B: Claude Desktop and Claude Code config folders created (the apps installed)"
sleep 5
client_files > "$O/files-B-before.txt"
open_menu B-claude-installed
client_files > "$O/files-B-after.txt"
cp "$HOME/.config/Claude/claude_desktop_config.json" "$O/claude_desktop_config.json" 2>/dev/null
cp "$HOME/.claude.json" "$O/claude.json" 2>/dev/null
ls -la "$HOME/.config/Claude/" | sed "s#$HOME#~#g" > "$O/ls-B.txt"
xdotool mousemove $CLOSE_X $CLOSE_Y click 1; sleep 1
quit_app
event "$T" "C: quit"
start_app "$O/app-2.log"
sleep 8; xdotool mousemove 442 228 click 1
for i in $(seq 1 15); do xdotool mousemove $(( 500 + (i % 10) * 60 )) $(( 400 + (i % 7) * 50 )); sleep 2; done
shot "$O/C-second-start.png"
client_files > "$O/files-C-after-second-start.txt"
event "$T" "C: second start, 38 s"
open_menu D-menu-again
client_files > "$O/files-D-after-menu-again.txt"
quit_app
stop_record
python3 - "$O" <<'EOF'
import json, os, sys
sys.path.insert(0, '/work')
from checker import entry
o = sys.argv[1]
home = os.path.expanduser('~')
def hashes(fn):
    return [l.split()[0] for l in open(os.path.join(o, fn)) if l.strip() and not l.startswith(('total', 'd', '-'))][:2]
res = {k: hashes(f'files-{k}.txt') for k in ('A-before', 'A-after', 'B-before', 'B-after', 'C-after-second-start', 'D-after-menu-again')}
out = {'hashes [claude_desktop_config.json, ~/.claude.json]': res,
       'A_menu_without_claude_wrote_files': res['A-before'] != res['A-after'],
       'B_menu_after_install_wrote_files': res['B-before'] != res['B-after'],
       'C_second_start_changed_files': res['B-after'] != res['C-after-second-start'],
       'D_menu_again_changed_files': res['C-after-second-start'] != res['D-after-menu-again'],
       'backups': sorted(f for f in os.listdir(home + '/.config/Claude')) + sorted(f for f in os.listdir(home) if f.startswith('.claude.json'))}
for name, f in (('claude_desktop', home + '/.config/Claude/claude_desktop_config.json'), ('claude_code', home + '/.claude.json')):
    e = entry.read(f)
    e['path'] = e['path'].replace(home, '~')
    out[name] = e
json.dump(out, open(os.path.join(o, 'menu.json'), 'w'), indent=1)
print(json.dumps(out, indent=1))
EOF
