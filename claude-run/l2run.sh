#!/usr/bin/env bash
# Lesson 2's one Claude run (paid): Claude Code 2.1.311 in its real terminal inside the lab container, beside
# SolidCraft 0.25.0's window, both filmed (lab/l2claude.sh). The container needs the network (Claude's servers); it
# gets this PC's Claude sign-in as one environment variable, read here from the Claude Code credentials file and
# written to a temporary env file that is deleted when the run ends. Nothing about it reaches the run folder.
#   bash claude-run/l2run.sh claude-1
set -euo pipefail
RUN=${1:-claude-1}
cd "$(dirname "$0")/.."
LAB="$(pwd -W 2>/dev/null || pwd)"
S=out/l2/runs/$RUN
LEDGER="${LEDGER:-$LAB/../solidcraft-course-BUDGET.tsv}"
CAP="${CAP:-0.40}"
export BUDGET_MARK="# --- GO 27 Oct 2026 L2"
[ -e "$S/meta.json" ] && { echo "refusing to overwrite $S"; exit 3; }
python claude-run/budget.py check "$LEDGER" "$CAP" || { echo "BUDGET STOP"; exit 2; }
mkdir -p out/scratch out/l2/runs; ENVF=out/scratch/l2run-$$.env   # gitignored, deleted below
trap 'rm -f "$ENVF"' EXIT
python - "$ENVF" <<'PY'
import json, os, sys
d = json.load(open(os.path.expanduser('~/.claude/.credentials.json')))
open(sys.argv[1], 'w').write('CLAUDE_CODE_OAUTH_TOKEN=' + d['claudeAiOauth']['accessToken'] + '\n')
PY
T0=$(date +%s)
MSYS_NO_PATHCONV=1 docker run --rm --name sc2-claude --memory 4g --shm-size 1g --env-file "$ENVF" -v "$LAB:/work" \
  sc2-l2:0.25.0 bash /work/lab/l2claude.sh "$RUN" > "$S.container.log" 2>&1 || echo "container exit $?"
rm -f "$ENVF"
mv "$S.container.log" "$S/container.log" 2>/dev/null || true
echo "{\"run\": \"$RUN\", \"wall_s\": $(( $(date +%s) - T0 )), \"model\": \"claude-sonnet-5-5\", \"claude_version\": \"2.1.311\", \"solidcraft\": \"0.25.0\", \"launch\": \"claude --model claude-sonnet-5-5 (no permission flags: Claude Code's own default mode)\"}" > "$S/meta.json"
COST=$(python - "$S" <<'PY'
import re, sys
t = open(sys.argv[1] + '/pane-cost.txt', encoding='utf-8', errors='replace').read() if __import__('os').path.exists(sys.argv[1] + '/pane-cost.txt') else ''
m = re.findall(r'\$(\d+\.\d+)', t)
print(m[0] if m else '')
PY
)
python claude-run/budget.py record "$LEDGER" "sc2-$RUN" "$COST" "$CAP" sc2-lesson2
python claude-run/scrub.py "$S"
cat "$S/meta.json"
