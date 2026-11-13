#!/bin/bash
# fx12 probe step (docker exec fx12p bash /work/lab/fx12px.sh NAME 'shell using fx12lib'): run the steps, then a
# screenshot halved to 1440x810 (the g() units) at out/scratch/fx12p/NAME.png
set -u
. /work/lab/fx12lib.sh
O=/work/out/scratch/fx12p
eval "$2"
sleep "${3:-1.5}"
shot /tmp/fx12/full.png; ffmpeg -loglevel error -y -i /tmp/fx12/full.png -vf scale=1440:-1 "$O/$1.png"
