#!/usr/bin/env bash
# scwf R1 (pre-registered in out/scwf/PREREG.txt, one try): lab/scwfR1.sh in sc-wf-l5:0.30.1 with the network (Claude's
# servers). The sign-in file is mounted read-only (tb-lab/ab pattern), copied in by the container, deleted before it exits.
#   bash claude-run/scwfrun.sh   (live cost guard: claude-run/costguard.py 0.70 scwf-claude, started alongside)
set -euo pipefail
cd "$(dirname "$0")/.."
LAB="$(pwd -W 2>/dev/null || pwd)"
S=out/scwf/R1
LEDGER="$LAB/../solidcraft-course-BUDGET.tsv"; CAP=0.70
export BUDGET_MARK="# --- GO 8 Nov 2026 scwf"
export M1="In SolidCraft, start a new design and build an under-desk bracket with named sizes. Draw an L profile on the XZ plane: a top leg 50 mm long and 4 mm thick, and a drop leg 4 mm thick, 30 mm tall overall. Extrude it by a parameter named width = 25 mm. After extruding, check the part's height runs from 0 up, and tell me the volume."
export M2="Change width to 35 and tell me the new volume. Then set it back to 25."
export M3="Add two 4 mm holes through the top leg, 12 mm and 38 mm from the end, centred across the width. Use width / 2 for the centre so the holes stay centred when the width changes."
export M4="Round the inside corner of the L with a 3 mm fillet, then tell me the volume."
export M5="Save the design as ~/bracket.sc and export it as ~/bracket.stl."     # = PREREG.txt
[ -e "$S/events.jsonl" ] && { echo "refusing to overwrite $S"; exit 3; }
python claude-run/budget.py check "$LEDGER" "$CAP" 1.40 || { echo "BUDGET STOP"; exit 2; }
creds="$(cd ~ && (pwd -W 2>/dev/null || pwd))/.claude/.credentials.json"
mkdir -p "$S"; T0=$(date +%s)
MSYS_NO_PATHCONV=1 docker run --rm --name scwf-claude -e M1 -e M2 -e M3 -e M4 -e M5 --memory 5g --shm-size 1g -v "$creds:/creds.json:ro" -v "$LAB:/work" \
  sc-wf-l5:0.30.1 bash /work/lab/scwfR1.sh > "$S.container.log" 2>&1 || echo "container exit $?"
mv "$S.container.log" "$S/container.log" 2>/dev/null || true
echo "{\"run\": \"R1\", \"wall_s\": $(( $(date +%s) - T0 )), \"claude_version\": \"$(cat $S/claude-version.txt 2>/dev/null)\", \"solidcraft\": \"0.30.1\", \"launch\": \"claude --model claude-sonnet-5-5\"}" > "$S/meta.json"
COST=$(python -c "
import re,os,sys; p=sys.argv[1]+'/pane-cost.txt'; t=open(p,encoding='utf-8',errors='replace').read() if os.path.exists(p) else ''
m=re.findall(r'[$]([0-9]+[.][0-9]+)',t); print(m[0] if m else '')" "$S")   # fixed after R1: the first form broke (cost recorded by hand)
python claude-run/budget.py record "$LEDGER" "scwf-R1" "$COST" "$CAP" scwf
python claude-run/scrub.py "$S"
echo "cost $COST" | tee "$S/cost.txt"
