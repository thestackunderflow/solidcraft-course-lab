#!/usr/bin/env bash
# fx8 R1 (pre-registered in out/fx8/LAB-fx8.md section 4, one try): lab/fx8R1.sh in sc5-l5:0.28.0 with the network (Claude's
# servers). The sign-in file is mounted read-only (tb-lab/ab pattern), copied in by the container, deleted before it exits.
#   bash claude-run/fx8run.sh
set -euo pipefail
cd "$(dirname "$0")/.."
LAB="$(pwd -W 2>/dev/null || pwd)"
S=out/fx8/runs/R1
LEDGER="$LAB/../fixit-fx8-BUDGET.tsv"; CAP=0.80
export BUDGET_MARK="# --- GO 5 Nov 2026 fx8"
export M1="Open hook.stl and drill a 5 mm hole through the back plate."     # = LAB-fx8 section 4
[ -e "$S/events.jsonl" ] && { echo "refusing to overwrite $S"; exit 3; }
python claude-run/budget.py check "$LEDGER" "$CAP" || { echo "BUDGET STOP"; exit 2; }
creds="$(cd ~ && (pwd -W 2>/dev/null || pwd))/.claude/.credentials.json"
mkdir -p "$S"; T0=$(date +%s)
MSYS_NO_PATHCONV=1 docker run --rm --name fx8-claude -e M1 --memory 5g --shm-size 1g -v "$creds:/creds.json:ro" -v "$LAB:/work" \
  sc5-l5:0.28.0 bash /work/lab/fx8R1.sh > "$S.container.log" 2>&1 || echo "container exit $?"
mv "$S.container.log" "$S/container.log" 2>/dev/null || true
echo "{\"run\": \"R1\", \"wall_s\": $(( $(date +%s) - T0 )), \"claude_version\": \"$(cat $S/claude-version.txt 2>/dev/null)\", \"solidcraft\": \"0.28.0\", \"launch\": \"claude --model claude-sonnet-5-5\"}" > "$S/meta.json"
COST=$(python -c "
import re,os,sys; p=sys.argv[1]+'/pane-cost.txt'; t=open(p,encoding='utf-8',errors='replace').read() if os.path.exists(p) else ''
m=re.findall(r'[$]([0-9]+[.][0-9]+)',t); print(m[0] if m else '')" "$S")   # fixed after R1: the first form broke (cost recorded by hand)
python claude-run/budget.py record "$LEDGER" "fx8-R1" "$COST" "$CAP" fixit-fx8
python claude-run/scrub.py "$S"
echo "cost $COST" | tee "$S/cost.txt"
