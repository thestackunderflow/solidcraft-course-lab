# fx11 lab: deviations from LAB-fx11.md v1 (pre-registration e482bd4)

Nothing was re-scored. Every take is kept, including the failed attempt in A-attempt1/.

1. **Where it ran / image ID.** All containers on the Ubuntu lab box (as fx10). Image tag `sc5-l5:0.28.0`; box ID
   `sha256:38a6f678...` vs the PC's `2992c9ec...` (store difference, same as fx10); `solidcraft --version` = 0.28.0
   (env.txt). No host ffmpeg on the box: recording, clips and stills used the image's ffmpeg.
2. **Take P volumes.** 113,479.66 mm3 measured for both towers vs 113,490.03 predicted (0.009% low, inside the 0.1% P0
   rule). Take P built the bore with a sketch on the top face and `solid.extrude` distance 195, direction negative,
   operation cut (the pre-registered geometry).
3. **Take A attempt 1 (A-attempt1/, not scored).** The helper that checks whether Browser > Origin is expanded (copied
   from fx10) read Sketch1's text on the Z row as "expanded"; Origin stayed collapsed, so the XY and Tower clicks hit
   other rows and the dialog showed neither a pick nor a line (refusal.png shows empty fields). The helper now tests
   the Bodies folder icon's place, and a second detector requires the red line before a take logs "refused". Attempt 2
   (A/) is the scored take. One of the two allowed attempts used.
4. **Take B step 5 (Q3).** In take B the plug's `open` of ~/tower.sc went back to the already open, split tab (no new
   tab for the same file), so the Midplane was made in the split design and the Split pick landed on the Construction
   folder row (B/events.txt: "OK greyed and no error line"). Q3 re-run once in its own container (B-q3/, lab/fx11Bq3.sh).
   In both, the first plane is XY (the base face's plane): the base face cannot be clicked from the home view.
5. **Orbit.** A short Orbit-button drag (60 px out and back), then Home view; not a full turn.
6. **Properties.** Inspect > Properties with nothing picked shows the whole design; per-body values came from the
   Browser row's right-click > Properties (as the dialog title "Properties: Tower" shows). Shots are named by row
   (props-row1 = Tower = top, props-row2 = Tower (1) = bottom) rather than top/bottom.
7. **R1 not run** (this stage was no-AI by the brief); runs/R1/DEFERRED.txt. env.txt has no R1 Claude Code version.
8. **R1 run on the PC (13 Nov 2026), takes P-D on the Ubuntu box, same image sc5-l5:0.28.0.** lab/fx11R1.sh +
   claude-run/fx11run.sh are copies of the fx10 pair (start file out/fx11/P/tower.sc, prompt and cap $0.25 from
   LAB-fx11 section 4; no other change). One run, no retry, no harness failure; class A, $0.1440. The cap is checked
   before the start (budget.py), not enforced mid-run (as fx6-fx10); the turn limit is l2drive's 420 s (wall 93 s).
   The owner's claude.ai connectors also showed as connected in `claude mcp list` (as fx9/fx10); none was called.
   Footage note: crop/mask Claude Code's greyed suggested prompt "Save it and export both halves as STLs to /root"
   (not Claude's words), as fx10. The terminal font drops a glyph in the tool summary ("Listed 1 d r ctory"); leave it.
