#!/bin/bash
# fx11 probe step (docker exec fx11p bash /work/lab/fx11px.sh NAME 'shell using fx11lib'): run the steps, then a
# screenshot halved to 1440x810 (the g() units) at out/scratch/fx11p/NAME.png
set -u
. /work/lab/fx11lib.sh
O=/work/out/scratch/fx11p
eval "$2"
sleep "${3:-1.5}"
shot /tmp/fx11/full.png; ffmpeg -loglevel error -y -i /tmp/fx11/full.png -vf scale=1440:-1 "$O/$1.png"
