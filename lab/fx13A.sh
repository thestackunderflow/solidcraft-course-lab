#!/bin/bash
# fx13 take A (LAB-fx13 section 3): the refusal. ~/cup.sc (D60 x 80, top + bottom edges rounded 1.5) opened off camera;
# full window 3 s; slow orbit; a 2 s section (XZ); Shell with its defaults (Tangent chain ticked), click the top:
# the preview and the line (Q1), thickness 2 typed, the line held 4 s + 8 s (F4); Create Issue... draft (not
# submitted); Cancel; the timeline read. Q3b: Shell again (chain on), click the SIDE: lit faces + line; closed.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx13A.sh
set -u
. /work/lab/fx13lib.sh
take A
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc cup; still
vol a-before
rec_start
ev "recording started: full SolidCraft window, ~/cup.sc: hold 3 s"
nap 3.0
orbit 4
section_xz
ev "section of the solid cup: hold 2 s"; nap 2.0; cp_shot section-solid
section_off; home_view
shell_open dialog
pick "click the top face at (0, 0, 80)" $TOP60
ev "preview on the top pick, chain on, as shown in preview.png: hold 4 s"; nap 4.0; cp_shot preview
thick "2 mm"
ev "shell top chain on: full line as shown in refusal.png: hold 4 s"; nap 4.0; cp_shot refusal
ev "the line held 8 s (F4 slow zoom)"; nap 8.0; cp_shot hold
ev "Create Issue... (draft only, not submitted)"; g $SH_ISSUE 14; click; nap 2.5; still
ev "report draft as shown in report.png: hold 4 s"; nap 4.0; cp_shot report
ev "Close draft"; g $ISSUE_CLOSE 14; click; nap 1.5; still; cp_shot after-draft
ev "Cancel"; g $SH_CANCEL_ERR 14; click; nap 2.0; still; cp_shot after-cancel
vol a-after-cancel
ev "after Cancel: $(cut -c1-300 "$O/read-a-after-cancel.txt")"
ev "Q3b: Shell again, chain left on"
shell_open dialog2
pick "click the SIDE at (30, 0, 40)" $SIDE60
thick "2 mm"
ev "shell side chain on: lit faces and line as shown in side.png: hold 4 s"; nap 4.0; cp_shot side
ev "close the dialog (its x)"; g $SH_CLOSE_X 14; click; nap 2.0; still
vol a-after
ev "after: $(cut -c1-300 "$O/read-a-after.txt")"
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "A done"
