#!/bin/bash
# Q6 + Q7 (see lab/startorder.py). Host side:
#   docker run --rm --memory 3g --shm-size 1g --network none -v "$PWD:/work" sc1-app:0.24.1 bash /work/lab/startorder.sh
set -u
O=/work/out/l1/startorder
[ -e "$O" ] && { echo "refusing: $O exists"; exit 1; }
mkdir -p "$O"
. /work/lab/common.sh
start_display
record "$O/startorder.mp4"
python3 /work/lab/startorder.py
stop_record
