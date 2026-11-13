#!/bin/bash
# fx14 probe step: docker exec fx14bp bash /work/lab/fx14bpx.sh 'SHELL CMDS' [SHOTNAME]: runs the commands with the
# fx14blib helpers in the probe's display, then a halved screenshot to out/scratch/fx14bp/SHOTNAME.png
. /work/lab/fx14blib.sh
O=/work/out/scratch/fx14bp
eval "$1"
if [ -n "${2:-}" ]; then shot /tmp/fx14b/full.png; convert /tmp/fx14b/full.png -resize 50% "$O/$2.png"; fi
