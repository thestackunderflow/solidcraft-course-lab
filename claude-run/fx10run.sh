#!/usr/bin/env bash
# fx10 R1 (pre-registered in out/fx10/LAB-fx10.md section 4, one run, no retry): lab/fx10R1.sh in sc5-l5:0.28.0
# with the network (Claude's servers). The sign-in file is mounted read-only, copied in, deleted before it exits.
#   bash claude-run/fx10run.sh
set -euo pipefail
cd "$(dirname "$0")/.."
LAB="$(pwd -W 2>/dev/null || pwd)"
S=out/fx10/runs/R1
LEDGER="$LAB/../fixit-fx10-BUDGET.tsv"; CAP=0.50
export BUDGET_MARK="# --- GO 11 Nov 2026 fx10"
export M1="Revolve this sketch around the vertical axis to make the knob."     # = LAB-fx10 section 4
[ -e "$S/events.jsonl" ] && { echo "refusing to overwrite $S"; exit 3; }
[ -f "$LEDGER" ] || echo "$BUDGET_MARK (lab stage: one pre-registered R1 run, cap $CAP, as fx6-fx9; run on the PC)" > "$LEDGER"
python claude-run/budget.py check "$LEDGER" "$CAP" || { echo "BUDGET STOP"; exit 2; }
creds="$(cd ~ && (pwd -W 2>/dev/null || pwd))/.claude/.credentials.json"
mkdir -p "$S"; T0=$(date +%s)
MSYS_NO_PATHCONV=1 docker run --rm --name fx10-claude -e M1 --memory 5g --shm-size 1g -v "$creds:/creds.json:ro" -v "$LAB:/work" \
  sc5-l5:0.28.0 bash /work/lab/fx10R1.sh > "$S.container.log" 2>&1 || echo "container exit $?"
mv "$S.container.log" "$S/container.log" 2>/dev/null || true
echo "{\"run\": \"R1\", \"wall_s\": $(( $(date +%s) - T0 )), \"claude_version\": \"$(cat $S/claude-version.txt 2>/dev/null)\", \"solidcraft\": \"0.28.0\", \"launch\": \"claude --model claude-sonnet-5-5\"}" > "$S/meta.json"
COST=$(python -c "
import re,os,sys; p=sys.argv[1]+'/pane-cost.txt'; t=open(p,encoding='utf-8',errors='replace').read() if os.path.exists(p) else ''
m=re.findall(r'[\$]([0-9]+[.][0-9]+)',t); print(m[0] if m else '')" "$S")
python claude-run/budget.py record "$LEDGER" "fx10-R1" "$COST" "$CAP" fixit-fx10
python claude-run/scrub.py "$S"
python lab/fx9redact.py "$S"
echo "cost $COST" | tee "$S/cost.txt"
