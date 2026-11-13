#!/usr/bin/env bash
# fx14b R1 (pre-registered in LAB-fx14b.md section 4, one run, no retry): lab/fx14bR1.sh in sc5-l5:0.28.0
# with the network (Claude's servers). The sign-in file is mounted read-only, copied in, deleted before it exits.
#   bash claude-run/fx14brun.sh
set -euo pipefail
cd "$(dirname "$0")/.."
LAB="$(pwd -W 2>/dev/null || pwd)"
S=out/fx14b/runs/R1
LEDGER="$LAB/../fixit-fx14b-BUDGET.tsv"; CAP=0.25
export BUDGET_MARK="# --- GO 13 Nov 2026 fx14b"
export M1="Put a 10 mm hole, 5 mm deep, in the middle of the top face of this block."     # = LAB-fx14b section 4
[ -e "$S/events.jsonl" ] && { echo "refusing to overwrite $S"; exit 3; }
[ -f "$LEDGER" ] || echo "$BUDGET_MARK (lab stage: one pre-registered R1 run, cap $CAP, as fx6-fx10; run on the PC)" > "$LEDGER"
python claude-run/budget.py check "$LEDGER" "$CAP" || { echo "BUDGET STOP"; exit 2; }
creds="$(cd ~ && (pwd -W 2>/dev/null || pwd))/.claude/.credentials.json"
mkdir -p "$S"; T0=$(date +%s)
MSYS_NO_PATHCONV=1 docker run --rm --name fx14b-claude -e M1 --memory 5g --shm-size 1g -v "$creds:/creds.json:ro" -v "$LAB:/work" \
  sc5-l5:0.28.0 bash /work/lab/fx14bR1.sh > "$S.container.log" 2>&1 || echo "container exit $?"
mv "$S.container.log" "$S/container.log" 2>/dev/null || true
echo "{\"run\": \"R1\", \"wall_s\": $(( $(date +%s) - T0 )), \"claude_version\": \"$(cat $S/claude-version.txt 2>/dev/null)\", \"solidcraft\": \"0.28.0\", \"launch\": \"claude --model claude-sonnet-5-5 --strict-mcp-config --mcp-config entry-as-run.json\"}" > "$S/meta.json"
COST=$(python -c "
import re,os,sys; p=sys.argv[1]+'/pane-cost.txt'; t=open(p,encoding='utf-8',errors='replace').read() if os.path.exists(p) else ''
m=re.findall(r'[\$]([0-9]+[.][0-9]+)',t); print(m[0] if m else '')" "$S")
python claude-run/budget.py record "$LEDGER" "fx14b-R1" "$COST" "$CAP" fixit-fx14b
python claude-run/scrub.py "$S"
python lab/fx9redact.py "$S"
echo "cost $COST" | tee "$S/cost.txt"
