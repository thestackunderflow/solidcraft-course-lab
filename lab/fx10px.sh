#!/bin/bash
# fx10 probe step (docker exec fx10p bash /work/lab/fx10px.sh NAME 'shell using fx10lib'): run the steps, then a
# screenshot halved to 1440x810 (the g() units) at out/scratch/fx10p/NAME.png
set -u
. /work/lab/fx10lib.sh
O=/work/out/scratch/fx10p
eval "$2"
sleep "${3:-1.5}"
shot /tmp/fx10/full.png; ffmpeg -loglevel error -y -i /tmp/fx10/full.png -vf scale=1440:-1 "$O/$1.png"
