#!/bin/bash
# fx8 take A2 part 2: Cancel the Extrude panel (refusal shown), hold the full window, stop the recording.
set -u
. /work/lab/fx8lib.sh
O=$(cat /tmp/fx8/O); T0=$(cat /tmp/fx8/T0)
ev "cut: Cancel"
g 1322 656 12; click; nap 1.5
still; nap 2.0
ev "recording stopped"
rec_stop
read_now a2-after
echo "A2 done"
