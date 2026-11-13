# fx13 lab: deviations from LAB-fx13.md v1 (pre-registration 0c8e59e)

Nothing was re-scored or re-rolled. Every take ran once and is kept.

1. **Where / image.** All containers on the Ubuntu lab box (~/jobs/fx13), image sc5-l5:0.28.0, box image ID
   38a6f6787dc1 (not the PC's 2992c9ecbca2; the same box image as fx11, fx12, fx14); version line "solidcraft 0.28.0" (P0 ok).
2. **Order.** LAB says this lab runs after fx14's replacement is picked; the owner gave GO for fx13 with fx14 dropped
   (RESULTS-fx14.md). fx13 now follows fx12: its end screen / outro point back to fx12 (Offset), not fx14.
3. **Take P face counts.** Expected 5 / 4 faces; the plug lists 8 / 6 (the side is two halves with a seam, and each
   round is two pieces). Volumes all within 0.01%: cup 226,012.52 (226,014.67), cup-bottom 226,102.53 (226,104.67),
   cup-r3 225,477.37 (225,482.81), cup40 50,211.71 (50,212.15). Not a stop (rule P0 is on volume).
4. **Probe.** One probe container fx13p (out/scratch/fx13p s0-s20, gitignored, not scored) found every position, then
   was stopped and removed. It already showed the take A line and the take B numbers before the takes; those probe
   results are not used.
5. **Take A order.** The 2 s section (F1) is filmed before the Shell (orbit, section of the solid cup, section off),
   not inside step 1. Thickness "2 mm" was typed after the pick (default already 2 mm).
6. **Take B Measure.** Measure across two cylinder faces reports Center to center 0.00 and Min / Max; Min recorded
   (as fx12 Q11). Measured with the XZ section on (the inner wall and floor visible); the outer bottom face was picked
   from the gizmo's -Z view. Not a point measurement at z 40.
7. **Take C.** Each file opens in a new tab (the plug's open). The r3 dialog stayed open after the refusal and was
   closed with its x.
8. **Take D.** No window toast was captured in D/reply.png; the window shows the shelled cup after call 2.
9. **Report draft (logged only).** In A/report.png the Shell dialog's OK looks enabled while the draft is open; in
   A/refusal.png (before) it is greyed. Not interpreted.
10. **Second cause (#8536).** Not a take in LAB v1: not run.
11. **Clips.** lab/fx13clips.py, tests/test_fx13clips.py (red: no takes/module; then 3 pass). Cut on the box with
    -v ~/jobs/box-test/video-qa:/footage:ro. Raw A, B, C screen.mp4 over 50 MB are gitignored.
