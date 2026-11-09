#!/bin/bash
# fx6 take A part 2 (take A steps 3-4): the words read off part 1's screenshots typed into events; Create Issue... opened
# (the dialog's report button), report.png; nothing submitted.
set -u
. /work/lab/fx6lib.sh
ev 'line 1: "not supported yet: the blend is larger than the neighbouring faces; the largest radius that fits is 5 mm"'
ev 'reason: "the blend is larger than the neighbouring faces"'
ev 'shown in: dialog (red text in the Fillet panel, under Advanced, while Preview is on; OK greyed out, so the click on OK did nothing)'
ev 'fillet 6: refused'
nap 2.0
ev "report: hover Create Issue..."
g 1252 609 22; nap 1.5
ev "report: Create Issue... clicked"
click; nap 3.0
cp_shot report
ev "report: draft shown (report.png)"
nap 4.0
