#!/bin/bash
# fx14b take A (LAB-fx14b section 3; F0, F1, F4 left, Short S0; Q20 = gate G1): the refusal. ~/conv.sc (40 x 30 x 20,
# Save As Mesh -> Insert Mesh -> Convert Mesh) opened off camera; full window 3 s; slow orbit; the History bar icons
# (no names) hovered for their tooltips; the Browser's Features folder opened (conv = the Insert Mesh step,
# ConvertMesh1); Create Sketch, click the top at (20, 15, 20): the line held 4 s + 8 s; Create Issue... draft (not
# submitted); Cancel.
#   docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work" sc5-l5:0.28.0 bash /work/lab/fx14bA.sh
set -u
. /work/lab/fx14blib.sh
take A
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
setup
open_sc conv; g $HOME_BTN 16; click; nap 2.0; still
vol a-before
rec_start
ev "recording started: full SolidCraft window, ~/conv.sc (converted block): hold 3 s"
nap 3.0
orbit 4
ev "History bar: the first icon hovered (tooltip): hold 3 s"; g $HIST_INSERT 16; nap 3.0; cp_shot hist-insert
ev "History bar: the second icon hovered (tooltip): hold 3 s"; g $HIST_CONVERT 16; nap 3.0; cp_shot hist-convert
ev "Browser: open conv:1 > Features: hold 3 s"; g $FEAT_FOLDER 16; click; nap 1.5; still; nap 3.0; cp_shot features
sk_dialog_face $TOP_FACE "click the top at (20, 15, 20)"
ev "sketch on converted top: full line as shown in refusal.png: hold 4 s"; nap 4.0; cp_shot refusal; cp_shot dialog
ev "the line held 8 s (F4 slow zoom)"; nap 8.0; cp_shot hold
ev "Create Issue... (draft only, not submitted)"; g $SK_ISSUE 14; click; nap 2.5; still
ev "report draft as shown in report.png: hold 4 s"; nap 4.0; cp_shot report
ev "Close draft"; g $ISSUE_CLOSE 14; click; nap 1.5; still; cp_shot after-draft
ev "Cancel"; g $SKD_CANCEL_ERR 14; click; nap 2.0; still; cp_shot after-cancel
vol a-after
ev "after Cancel: $(cut -c1-300 "$O/read-a-after.txt")"
ev "hold 3 s"; nap 3.0
ev "recording stopped"
rec_stop
echo "A done"
