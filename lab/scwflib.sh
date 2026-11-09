# scwf helpers (8-9 Nov 2026, video "SolidCraft Tutorial: Build and Print a Part with Claude"): the fx8/scerr helpers
# (display 2880x1620, UI scale 1.8, positions in 1440x810 units) with the take folders under out/scwf and SolidCraft
# 0.30.1 (sc-wf-l5:0.30.1). Sourced by lab/scwfsession.sh and by every `docker exec scwf-s bash /work/lab/scwfX.sh` step.
. /work/lab/fx8lib.sh
take() { O=/work/out/scwf/$1; mkdir -p "$O"; echo "$O" > /tmp/fx8/O; }
plug() { python3 /work/lab/scwfpart.py "$@"; }      # no-AI plug calls into the open window
