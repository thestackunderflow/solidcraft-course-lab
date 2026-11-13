#!/bin/bash
# fx13 probe step (docker exec fx13p bash /work/lab/fx13px.sh NAME 'shell using fx13lib'): run the steps, then a
# screenshot halved to 1440x810 (the g() units) at out/scratch/fx13p/NAME.png
set -u
. /work/lab/fx13lib.sh
O=/work/out/scratch/fx13p
eval "$2"
sleep "${3:-1.5}"
shot /tmp/fx13/full.png; ffmpeg -loglevel error -y -i /tmp/fx13/full.png -vf scale=1440:-1 "$O/$1.png"
