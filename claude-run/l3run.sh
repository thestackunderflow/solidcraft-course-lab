#!/usr/bin/env bash
# Lesson 3's Claude runs (paid): Claude Code 2.1.311 in its real terminal inside the lab container, beside
# SolidCraft 0.26.1's window, both filmed (lab/l3claude.sh). The run's two messages are in claude-run/l3messages.sh. The container needs the network (Claude's servers); it
# gets this PC's Claude sign-in as one environment variable, read here from the Claude Code credentials file and
# written to a temporary env file that is deleted when the run ends. Nothing about it reaches the run folder.
#   bash claude-run/l3run.sh A1     (A1, A2: not asked for names; B1, B2: asked)
set -euo pipefail
RUN=${1:-A1}
cd "$(dirname "$0")/.."
LAB="$(pwd -W 2>/dev/null || pwd)"
S=out/l3/runs/$RUN
LEDGER="${LEDGER:-$LAB/../solidcraft-course-BUDGET.tsv}"
CAP="${CAP:-0.20}"
export BUDGET_MARK="# --- GO 29 Oct 2026 L3"
. claude-run/l3messages.sh "$RUN"
[ -e "$S/meta.json" ] && { echo "refusing to overwrite $S"; exit 3; }
python claude-run/budget.py check "$LEDGER" "$CAP" || { echo "BUDGET STOP"; exit 2; }
mkdir -p out/scratch out/l3/runs; ENVF=out/scratch/l3run-$$.env   # gitignored, deleted below
trap 'rm -f "$ENVF"' EXIT
python - "$ENVF" <<'PY'
import json, os, sys
d = json.load(open(os.path.expanduser('~/.claude/.credentials.json')))
open(sys.argv[1], 'w').write('CLAUDE_CODE_OAUTH_TOKEN=' + d['claudeAiOauth']['accessToken'] + '\n')
PY
T0=$(date +%s)
MSYS_NO_PATHCONV=1 docker run --rm --name sc3-claude -e M1 -e M2 --memory 4g --shm-size 1g --env-file "$ENVF" -v "$LAB:/work" \
  sc3-l3:0.26.1 bash /work/lab/l3claude.sh "$RUN" > "$S.container.log" 2>&1 || echo "container exit $?"
rm -f "$ENVF"
mv "$S.container.log" "$S/container.log" 2>/dev/null || true
echo "{\"run\": \"$RUN\", \"wall_s\": $(( $(date +%s) - T0 )), \"model\": \"claude-sonnet-5-5\", \"claude_version\": \"2.1.311\", \"solidcraft\": \"0.26.1\", \"launch\": \"claude --model claude-sonnet-5-5 (no permission flags: Claude Code's own default mode)\"}" > "$S/meta.json"
COST=$(python - "$S" <<'PY'
import re, sys
t = open(sys.argv[1] + '/pane-cost.txt', encoding='utf-8', errors='replace').read() if __import__('os').path.exists(sys.argv[1] + '/pane-cost.txt') else ''
m = re.findall(r'\$(\d+\.\d+)', t)
print(m[0] if m else '')
PY
)
python claude-run/budget.py record "$LEDGER" "sc3-$RUN" "$COST" "$CAP" sc3-lesson3
python claude-run/scrub.py "$S"
cat "$S/meta.json"
