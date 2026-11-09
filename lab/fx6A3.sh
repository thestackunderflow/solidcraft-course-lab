#!/bin/bash
# fx6 take A part 3 (take A steps 4-6): report title typed into events, Close draft (nothing submitted), no timeline or
# Browser mark (nothing was added), Cancel, hold 5 s; a read-only read shows the hook unchanged; recording stopped.
set -u
. /work/lab/fx6lib.sh
ev 'report title: "FILLET: operation failed"'
ev "report: Close draft"
g 734 671 22; click; nap 1.5
ev "mark: none (no feature was added: History and Browser unchanged)"
cp_shot after-close
ev "fillet: Cancel"
g 1322 658 22; click; nap 1.0
still
ev "hook unchanged: hold 5 s"
nap 5.0
cp_shot end
read_now after
ev "recording stopped"
rec_stop
