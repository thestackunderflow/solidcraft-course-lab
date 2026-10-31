#!/usr/bin/env bash
# Lesson 5's Claude runs (paid): Claude Code 2.1.311 in its real terminal inside the lab container, beside
# SolidCraft 0.28.0's window with lesson 4's hook open and PrusaSlicer 2.9.2 installed, filmed (lab/l5claude.sh); messages in claude-run/l5messages.sh; a live cost guard (claude-run/costguard.py) kills the container at $CAP. The container needs the network (Claude's servers); it
# gets this PC's Claude sign-in as one environment variable, read here from the Claude Code credentials file and
# written to a temporary env file that is deleted when the run ends. Nothing about it reaches the run folder.
#   bash claude-run/l5run.sh A1     (order A1, B1; a run starts only if the sum since the L5 mark is $0.30 or less)
set -euo pipefail
RUN=${1:-A1}
cd "$(dirname "$0")/.."
LAB="$(pwd -W 2>/dev/null || pwd)"
S=out/l5/runs/$RUN
LEDGER="${LEDGER:-$LAB/../solidcraft-course-BUDGET.tsv}"
CAP="${CAP:-0.30}"
export BUDGET_MARK="# --- GO 31 Oct 2026 L5"
. claude-run/l5messages.sh "$RUN"
[ -e "$S/meta.json" ] && { echo "refusing to overwrite $S"; exit 3; }
python claude-run/budget.py check "$LEDGER" "$CAP" 0.60 || { echo "BUDGET STOP"; exit 2; }
mkdir -p out/scratch out/l5/runs "$S"; ENVF=out/scratch/l5run-$$.env   # gitignored, deleted below
trap 'rm -f "$ENVF"' EXIT
python - "$ENVF" <<'PY'
import json, os, sys
d = json.load(open(os.path.expanduser('~/.claude/.credentials.json')))
open(sys.argv[1], 'w').write('CLAUDE_CODE_OAUTH_TOKEN=' + d['claudeAiOauth']['accessToken'] + '\n')
PY
T0=$(date +%s)
( sleep 20; python claude-run/costguard.py "$CAP" sc5-claude > "$S/costguard.log" 2>&1 ) &
GUARD=$!
MSYS_NO_PATHCONV=1 docker run --rm --name sc5-claude -e M1 --memory 5g --shm-size 1g --env-file "$ENVF" -v "$LAB:/work" \
  sc5-l5:0.28.0 bash /work/lab/l5claude.sh "$RUN" > "$S.container.log" 2>&1 || echo "container exit $?"
wait "$GUARD" 2>/dev/null || true
rm -f "$ENVF"
mv "$S.container.log" "$S/container.log" 2>/dev/null || true
echo "{\"run\": \"$RUN\", \"wall_s\": $(( $(date +%s) - T0 )), \"model\": \"claude-sonnet-5-5\", \"claude_version\": \"2.1.311\", \"solidcraft\": \"0.28.0\", \"slicer\": \"PrusaSlicer 2.9.2\", \"launch\": \"claude --model claude-sonnet-5-5 (no permission flags: Claude Code's own default mode)\"}" > "$S/meta.json"
COST=$(python - "$S" <<'PY'
import re, sys
t = open(sys.argv[1] + '/pane-cost.txt', encoding='utf-8', errors='replace').read() if __import__('os').path.exists(sys.argv[1] + '/pane-cost.txt') else ''
m = re.findall(r'\$(\d+\.\d+)', t)
print(m[0] if m else '')
PY
)
python claude-run/budget.py record "$LEDGER" "sc5-$RUN" "$COST" "$CAP" sc5-lesson5
python claude-run/scrub.py "$S"
cat "$S/meta.json"
