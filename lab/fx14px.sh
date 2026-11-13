#!/bin/bash
# fx14 probe step: docker exec fx14p bash /work/lab/fx14px.sh 'SHELL CMDS' [SHOTNAME]: runs the commands with the
# fx14lib helpers in the probe's display, then a halved screenshot to out/scratch/fx14p/SHOTNAME.png
. /work/lab/fx14lib.sh
O=/work/out/scratch/fx14p
eval "$1"
if [ -n "${2:-}" ]; then shot /tmp/fx14/full.png; convert /tmp/fx14/full.png -resize 50% "$O/$2.png"; fi
