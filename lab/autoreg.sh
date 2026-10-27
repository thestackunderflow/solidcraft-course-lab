#!/bin/bash
# Q2 + Q3: does SolidCraft add itself to the Claude apps by itself, and does a second start change it?
# A fresh home folder; both Claude apps' config folders exist before SolidCraft's first start (Claude Desktop:
# ~/.config/Claude/ with no file in it; Claude Code: ~/.claude/ and a ~/.claude.json holding {}); SolidCraft started
# with no --control flag and no SOLIDCRAFT_CONTROL_PORT. Every client file is hashed before and after; the window is
# filmed. Host side:
#   docker run --rm --memory 3g --shm-size 1g --network none -v "$PWD:/work" sc1-app:0.24.1 bash /work/lab/autoreg.sh [NAME [VERSION]]
# A person's first minute: the app opens, New design is clicked, the mouse moves for 60 s (the window repaints only on
# input). The first run (out/l1/autoreg-idle) left the window idle for 30 s.
set -u
NAME=${1:-autoreg}; VER=${2:-0.24.1}
O=/work/out/l1/$NAME
BIN=/opt/solidcraft-$VER/bin
[ -e "$O" ] && { echo "refusing: $O exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
T=$O/timeline.jsonl
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"
echo '{}' > "$HOME/.claude.json"
"$BIN/solidcraft" --version > "$O/version.txt" 2>&1
sha256sum $BIN/solidcraft $BIN/solidcraft-cli | sed 's#/opt/solidcraft-[0-9.]*#/opt/solidcraft#' >> "$O/version.txt"
cat /opt/solidcraft-$VER/check-*.txt >> "$O/version.txt"
"$BIN/solidcraft-cli" mcp setup --dry-run > "$O/setup-dry-run.txt" 2>&1
client_files > "$O/files-0-before.txt"
start_display
record "$O/start1.mp4"
event "$T" "start 1: solidcraft (no flags)"
start_app "$O/app-start1.log" "$BIN/solidcraft"
sleep 8; shot "$O/start1-08s.png"
python3 /work/client/ctl.py ui.prefs '{"theme":"light"}' 27878 > "$O/theme-reply.json" 2>&1
event "$T" "start 1: light theme set over the control channel"
xdotool mousemove 442 228 click 1; event "$T" "start 1: New design clicked"; sleep 3; shot "$O/start1-design.png"
for i in $(seq 1 30); do xdotool mousemove $(( 500 + (i % 10) * 60 )) $(( 400 + (i % 7) * 50 )); sleep 2; done
shot "$O/start1-60s.png"
event "$T" "start 1: 60 s of mouse moves"
client_files > "$O/files-1-after-start1.txt"
cp "$HOME/.config/Claude/claude_desktop_config.json" "$O/claude_desktop_config-after-start1.json" 2>/dev/null
cp "$HOME/.claude.json" "$O/claude.json-after-start1.json" 2>/dev/null
ls -la "$HOME/.config/Claude/" "$HOME/" | sed "s#$HOME#~#g" > "$O/ls-after-start1.txt"
ls -la "$HOME/.local/share/solidcraft/control/" 2>/dev/null | sed "s#$HOME#~#g" >> "$O/ls-after-start1.txt"
quit_app
event "$T" "start 1: quit (Ctrl+Q)"
stop_record
prev=0
record "$O/start2.mp4"
event "$T" "start 2: solidcraft (no flags)"
start_app "$O/app-start2.log" "$BIN/solidcraft"
sleep 8; xdotool mousemove 442 228 click 1
for i in $(seq 1 15); do xdotool mousemove $(( 500 + (i % 10) * 60 )) $(( 400 + (i % 7) * 50 )); sleep 2; done
shot "$O/start2-40s.png"
client_files > "$O/files-2-after-start2.txt"
quit_app
event "$T" "start 2: quit"
stop_record
python3 - "$O" <<'EOF'
import json, os, sys
sys.path.insert(0, '/work')
from checker import entry
o = sys.argv[1]
home = os.path.expanduser('~')
res = {}
res['version'] = open(os.path.join(o, 'version.txt')).readline().strip()
for name, f in (('claude_desktop', home + '/.config/Claude/claude_desktop_config.json'), ('claude_code', home + '/.claude.json')):
    res[name] = entry.read(f)
    res[name]['path'] = res[name]['path'].replace(home, '~')
def hashes(fn):
    return [l.split()[0] for l in open(os.path.join(o, fn)) if l.strip() and not l.startswith(('total', 'd', '-'))][:2]
res['hashes'] = {k: hashes(f'files-{k}.txt') for k in ('0-before', '1-after-start1', '2-after-start2')}
res['first_start_wrote_an_entry'] = res['hashes']['0-before'] != res['hashes']['1-after-start1']
res['announced_file'] = os.path.exists(home + '/.local/share/solidcraft/ai-apps-connected.json')
res['second_start_changed_files'] = res['hashes']['1-after-start1'] != res['hashes']['2-after-start2']
json.dump(res, open(os.path.join(o, 'autoreg.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
EOF
