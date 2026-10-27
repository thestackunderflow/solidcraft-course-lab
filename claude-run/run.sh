#!/usr/bin/env bash
# The lesson's two Claude chats (each a fresh headless Claude Code session on this PC, pinned version logged):
#   bash claude-run/run.sh noplug 1   no SolidCraft plug, no tools at all: "Make a 20 mm cube in SolidCraft."
#   bash claude-run/run.sh plug 1     the live container (lab/live.sh: window open, filmed, entry added with Help >
#                                     Connect AI assistants); Claude Code starts that entry inside the container through
#                                     the logging proxy; three messages, one at a time
# Sealed like the earlier labs: no session persistence, auto memory off, CLAUDE.md files excluded, user settings not
# loaded, only the solidcraft tools (approved in advance: a viewer's Claude app may ask first), no built-in tools.
set -euo pipefail
MODE=$1; N=$2
cd "$(dirname "$0")/.."
LAB="$(pwd -W 2>/dev/null || pwd)"
RUN=$MODE-$N; S=out/l1/runs/$RUN; W=out/scratch/work-$RUN
LEDGER="${LEDGER:-$LAB/../solidcraft-course-BUDGET.tsv}"
MODEL="${MODEL:-claude-sonnet-5-5}"
BUDGET="${BUDGET:-0.30}"
CUBE="Make a 20 mm cube in SolidCraft."
[ -e "$S/meta.json" ] && { echo "refusing to overwrite $S"; exit 3; }
python claude-run/budget.py check "$LEDGER" "$BUDGET" || { echo "BUDGET STOP"; exit 2; }
mkdir -p "$S" "$W"
python claude-run/prerun.py "$W" > "$S/prerun-files.txt" 2>&1 || true
case $MODE in
  noplug)
    echo '{"mcpServers": {}}' > "$S/mcp-config.json"
    MSGS=("$CUBE") ;;
  plug)
    NAME=sc1-live-$N
    docker rm -f "$NAME" >/dev/null 2>&1 || true
    MSYS_NO_PATHCONV=1 docker run -d --name "$NAME" --memory 3g --shm-size 1g --network none -v "$LAB:/work" sc1-app:0.24.1 \
      bash /work/lab/live.sh "$RUN" > /dev/null
    for i in $(seq 1 120); do [ -e "$S/READY" ] && break; sleep 1; done
    [ -e "$S/READY" ] || { echo "live container not ready"; docker logs "$NAME" | tail; exit 4; }
    # The entry SolidCraft wrote for Claude Code, started unchanged inside the container, through the proxy.
    python - "$S" "$NAME" <<'PY'
import json, sys
s, name = sys.argv[1], sys.argv[2]
e = json.load(open(s + '/claude.json-entry.json'))['mcpServers']['solidcraft']
args = ['exec', '-i', name, 'python3', '/work/proxy/mcp_log_proxy.py', '--log', f'/work/{s}/transcript.jsonl',
        '--png-dir', f'/work/{s}', '--watchdog', '330', '--', e['command']] + e['args']
json.dump({'mcpServers': {'solidcraft': {'command': 'docker', 'args': args}}}, open(s + '/mcp-config.json', 'w'), indent=1)
PY
    cat > "$S/after-turn.sh" <<SH
MSYS_NO_PATHCONV=1 docker exec $NAME bash -c 'export DISPLAY=:99; xdotool mousemove 700 520; sleep 0.5; xdotool mousemove 800 600; sleep 1; import -window root /work/$S/turn-\$1.png'
SH
    export AFTER_TURN="$S/after-turn.sh"
    MSGS=("What's in my SolidCraft design?" "$CUBE" "Measure it.") ;;
  *) echo "mode: noplug | plug"; exit 2 ;;
esac
T0=$(date +%s)
COST=$(python claude-run/chat.py "$LAB/$S" "$W" "$LAB/$S/mcp-config.json" "$BUDGET" "$MODEL" "${MSGS[@]}" | tail -1) || COST=
if [ "$MODE" = plug ]; then
  touch "$S/STOP"
  for i in $(seq 1 60); do [ "$(docker inspect -f '{{.State.Running}}' "$NAME" 2>/dev/null)" = true ] || break; sleep 1; done
  docker logs "$NAME" > "$S/container.log" 2>&1 || true
  docker rm -f "$NAME" > /dev/null 2>&1 || true
fi
python claude-run/budget.py record "$LEDGER" "sc1-$RUN" "$COST" "$BUDGET" sc1-lesson1
echo "{\"mode\": \"$MODE\", \"run\": \"$N\", \"wall_s\": $(( $(date +%s) - T0 )), \"cost\": \"${COST:-killed}\", \"model\": \"$MODEL\", \"claude_version\": \"$(${CLAUDE:-claude} --version | head -1)\", \"solidcraft\": \"0.24.1\"}" > "$S/meta.json"
python claude-run/scrub.py "$S"
cat "$S/meta.json"
