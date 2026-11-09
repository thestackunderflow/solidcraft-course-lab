# fx6 lab deviations (times UTC, 5 Nov 2026)

- 04:16 Display 2880x1620 (16:9) with SolidCraft at UI scale 1.8 filling it, not 1920x1080 as section 2 says: the same
  16:9 frame at 1.5x the pixels (the repo's l2common.sh pattern), so the full window is the whole frame and the zooms
  stay sharp. Positions were found by a dry probe (out/scratch/fx6p, gitignored): start page, the hook, the Fillet panel,
  and one 2 mm fillet on the lip edge (radius 2 is not a take value) to prove the click picks edge F2:side:l2|F2:side:l3.
- 04:16 Measurements of faces ("Measure") are read-only plug reads (lab/fx6hook.py read: body_topology, face area / 20 mm
  width), as lesson 4's l4hand.sh did, not the Measure tool on camera.
- Take A: OK was greyed after radius 6 (the refusal shows in the panel while Preview is on), so the OK click did nothing;
  recorded as is.
- Take B, first pass: Ctrl+Z after a GUI-built fillet did NOT undo it (keyboard focus after the panel closed). So the
  4.9 try ran on the 4.0-rounded body (picked the round's edge; refused with a different line, kept as evidence:
  "not supported yet: the blend is larger than a corner radius (site 1257) (the operation failed: not supported yet:
  only straight edges can be blended)") and the script's next Ctrl+Z removed the 4.0 round; same for 5.1 on the 5.0
  round. Valid first-pass results: 4.0 built (r 4.000), 5.0 built (r 5.000, on a clean hook). 4.9 and 5.1 are NOT
  scored from the first pass; they are re-run once on the clean hook (verified 8,500 mm3, 10 faces) with the toolbar's
  Undo button and a read after each undo (lab/fx6B2.sh). Not a re-score: the first pass never tried those radii on the
  pre-registered state.
- Take C2: the bottom-back edge is hidden in the home view, so the view turns to the back with the gizmo's -X ball on
  camera and the edge is picked on the back face's bottom line; the read confirms the blend sits on F2:side:l1|l8.
- Take C step 4 (Q4) ran unrecorded (screenshots + reads only), as section 3 says "NOT filmed".
- R1 (04:31): launched with Claude Code's default mode (auto, "as lesson 7" per section 4; lesson 7's script passed
  manual). The host wrapper's cost parse failed (a quoting bug) so the ledger line and scrub were run by hand ($0.1074,
  fixed in claude-run/fx6run.sh afterwards). session.jsonl carried the account's e-mail in its context block: replaced
  with you@example.com. SolidCraft shows an "Update" button in R1's window (the only take with network).
- Take A: after OK the cursor rests on the red line (OK sits under it once the line appears); the A-reason-line clip
  uses the 4 s hold before OK instead.
