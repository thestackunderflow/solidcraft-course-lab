#!/bin/bash
# fx6 probe (not a take, nothing filmed): the 0.28.0 window at 2880x1620 (16:9, UI scale 1.8), the start page, the hook,
# the toolbar. Screenshots halved to 1440x810 (the units the take scripts use) into out/scratch/fx6p.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx6probe.sh [STEP]
set -u
O=/work/out/scratch/fx6p; mkdir -p "$O"
W2=2880 H2=1620
. /work/lab/common.sh
W2=2880 H2=1620 . /work/lab/l2common.sh
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
solidcraft-cli mcp setup > "$O/setup.txt" 2>&1
start_display
openbox > /dev/null 2>&1 &
sleep 1
start_app "$O/app.log"
sleep 10
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
fill_window 0 0 $W $H; sleep 2
g() { glide "$(awk -v v="$1" 'BEGIN{printf "%d", v*4/3}')" "$(awk -v v="$2" 'BEGIN{printf "%d", v*4/3}')" "${3:-6}"; }
half() { shot /tmp/s.png; convert /tmp/s.png -resize 50% "$O/$1.png"; }
half 01-start
[ -f /work/out/scratch/fx6p/steps.sh ] && . /work/out/scratch/fx6p/steps.sh
quit_app
echo probe done
