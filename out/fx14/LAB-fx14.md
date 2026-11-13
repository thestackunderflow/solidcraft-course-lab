# LAB-fx14: SolidCraft Create Sketch: "this face can't keep an attachment" — pre-registration v1, 2026-11-13 (PLAN rev 2, DECISIONS round 1 applied) (before any run)

Lab repo: solidcraft-course-lab. Folder: out/fx14/ (gate G0, takes P, A, B, C, D, E; run runs/R1). Committed before
the first container starts (hash into out/fx14/PREREG.txt); `| tee` on every command; deviations in
out/fx14/DEVIATIONS.md; nothing re-scored. Runs only after the owner's GO. **G0 runs FIRST, alone, before the fx13
lab** (PLAN §3); the fx14 takes run after the fx13 lab, one lab at a time on the box. Never pushed by the lab.

## 0. Pins
As LAB-fx11 section 0 (= `../2026-11-fixit-2/LAB-fx6.md` section 0): SolidCraft 0.28.0, run image `sc5-l5:0.28.0`
(`solidcraft --version` = "solidcraft 0.28.0"; image ID on the box checked against the PC's 2992c9ecbca2), all takes
`--network none`; env to out/fx14/env.txt (image ID, version line, Xvfb size, UI scale, Claude Code version for R1).
Stop rule P0 as LAB-fx6.

## 1. Questions (PLAN §0.4): Q8 (G0), Q9-Q14, Q11b, Q15 (R1).

## 2. Common to every take
As LAB-fx6 section 2 (full-window recording of the whole display, TAKE/screen.mp4 x11grab 30 fps + cursor log,
events.txt/events.jsonl, 3 s full-window open, 4 s holds on every line to read). Filmed on the Ubuntu box (section 7).
G0 is NOT filmed (screenshots only).

## 3. Gate G0 and the takes, in run order

### Gate G0 (Q8, Q14): which edit shows the line (not filmed; a few minutes)
Pass rule, fixed now: a rung PASSES only if the **window** shows the exact line, read in full (with or without the
"Create Sketch:" prefix):
`this face can't keep an attachment: its history can't tell it apart from other faces (an edit reshaped it, or more
than one face could claim its name). Pick another face, or use a fixed plane here (fixed:true), which won't follow
later changes to the face`
NOT a pass: the hint "This face cannot provide a durable attachment. Choose another face or explicitly use a fixed
plane." or the "Use fixed plane" button alone (they show for any face error, dialogs_dense.rs 208); any other line,
e.g. "...; choose a supported exact face or explicitly use fixed:true" (sketch_face.rs 223) or "this face was split on
purpose (Split Face)..." (config_certificates.rs 859). Those are typed verbatim and the rung FAILS.

Step 1, the no-AI client, all four rungs (out/fx14/G0/g0.py, MCP client, no AI; tool and parameter names read from the
MCP tool list and logged into G0/tools.txt; `python3 -I out/fx14/G0/g0.py |& tee G0/client.txt`). For each rung: build
the model, call `model.faces` BEFORE the edit (the target face's name and certificate), make the edit, call
`model.faces` AFTER, then `sketch.create` with `plane: {face: [x, y, z]}` on the target face; save the file as
~/g0X.sc. Record each reply verbatim. A rung whose edit has no MCP tool is built in the window instead (logged).
- G0a Align: rectangle (0, 0)-(40, 30) on XY, Extrude 20 (New Body); Align the body from (0, 0, 0) to (0, 0, 5) (record
  how From and To are given). Face point [20, 15, 25].
- G0b Combine: rectangle (0, 0)-(20, 30) Extrude 20 New Body; rectangle (20, 0)-(40, 30) Extrude 20 New Body; Combine
  Join (the two tops are coplanar, so the merged top is one face 40 x 30). Face point [20, 15, 20]. Same 24,000 mm3
  block as G0a, so the hole numbers carry over.
- G0c shelled rim: G0a's block before Align; Shell, the top opened, thickness 2 (record the chain setting; sharp edges,
  so the chain stops at the top). Face point on the rim [1, 15, 20].
- G0d converted mesh (the vendor's example, 0.41.0 features.rs 56): G0a's block before Align; Save As Mesh to
  ~/g0d.stl; a new file; insert the STL (record the menu or tool name); Convert Mesh; face point [20, 15, 20].
- Control (Q14): `sketch.create` on [20, 15, 20] on the plain block before any edit (expected attaches; Extrude caps
  carry a construction certificate, face-attachments.md 9-12).

Step 2, the window, in ladder order (G0a, G0b, G0c, G0d): open ~/g0X.sc in SolidCraft (Xvfb, `--network none`),
Create Sketch, click the target face; screenshot G0/g0X-window.png held 4 s; type the full line (or "attached") into
G0/rungs.tsv; Report draft title if offered (not submitted; expected "CREATE SKETCH: operation failed"). Every rung
whose client reply carried the line is checked; also G0a and G0b once each even if their client reply did not (the
window path may differ). **The first rung, in ladder order, that passes becomes the video's model.**

Step 3, the verdict: G0/VERDICT.txt = the passing rung (or "none"), its window line verbatim, the face's name and
certificate before/after (Q14), written and committed BEFORE the fx13 lab starts. The PLAN goes to rev 3 nouns from it
(the takes below are written for G0a; for another rung, the edit in takes P, A and C changes to that rung's edit and
the face point to its own; the hole steps stay unless the face is the G0c rim, where the circle becomes Ø1 on the rim's
mid-line, logged).

Predictions (BEFORE G0, from the 0.28.0 source and reports):
| rung | predicted | basis |
|---|---|---|
| G0a Align | **attaches** (lean); refused with the line possible | Align keeps the kernel's face sources (ops.rs 2234, 2255); the certificate is tried before the name (face_anchor.rs 199-221); the source test checks names only (ACCURACY C.6, C.11) |
| G0b Combine | refused with the line (moderate) | users' most named cause (#14632, #12154, #15185); a merged coplanar top is "more than one face could claim its name" |
| G0c shelled rim | refused, the line or another line (low confidence on the exact words) | #11137, #5040 |
| G0d converted mesh | refused with the line (highest confidence) | vendor's own example (0.41.0 features.rs 56); a mesh face has no construction history |
| control | attaches | face-attachments.md 9-12 |

### Take P: start files (not filmed; after G0 passes)
No-AI script out/fx14/P/block.py (MCP client, no AI), for G0a:
- ~/aligned.sc: the G0a model (block lifted 5 with Align; top z 25). Expected volume 24,000.00 mm3.
- ~/moved.sc: the same block lifted with Move/Copy, translate z 5 (Q10). Expected 24,000.00.
- ~/yourturn.sc: rectangle (0, 0)-(30, 30) on XY, Extrude 10 (Q12 start). Expected 9,000.00.
Each file reopened and its volume read back into P/volumes.txt; a mismatch over 0.1% = stop (P0). For another rung,
~/aligned.sc is replaced by ~/g0X.sc and ~/moved.sc by the rung's better-way file if Q10 allows one (else not made).

### Take A: the refusal (F0, F1, F4 left, F7 left; Short S0)
Open ~/aligned.sc. Full window 3 s; slow orbit; the timeline zoomed on "Align1" (record the step's name).
1. Create Sketch (record the menu path and dialog, A/dialog.png); click the top face. Event
   `sketch top: "full line as shown"`; A/refusal.png held 4 s with the line, the hint and the button readable; record
   whether the line is live in the dialog or after OK. Report draft title if offered (not submitted), A/report.png.
2. A/hold.png: the line held 8 s for F4's slow zoom (moving zoom done in post by footage.py; no still is held on screen
   longer than the plan's 6 s build spacing).

### Take B: the fix, Use fixed plane (F2, F5, S1 second half, S2)
Open ~/aligned.sc.
1. Q9: Properties of the body (B/props-before.png): expected 24,000.00 mm3.
2. Create Sketch, click the top (the line again), click "Use fixed plane" (zoom target the button). Event
   `fixed plane: sketch opens | "line"`. Circle Ø10 centred (20, 15); Finish. Extrude Cut 5 (down). Event.
3. Properties: expected 23,607.30 mm3 (24,000 - 392.70), B/props-after.png held 4 s. Measure the top face area:
   expected 1,121.46 mm2 (1,200 - 78.54), B/area.png.
4. S2 end frame: 5 s hold on the finished fixed-plane hole.

### Take C: the better way and the your-turn (F6, F7 right, F10; Short S1 first half)
1. Q10 (G0a only): open ~/moved.sc. Full window; label added in post. Create Sketch, click the top. Event
   `moved top: attached | "line"`. Circle Ø10 at (20, 15); Finish; Extrude Cut 5. Properties: expected 23,607.30.
   Also `model.faces` on the top after Move/Copy (logged with Q14). Prediction: attaches. If G0a passed AND Move/Copy
   also attaches, F6/F7 stand; if G0a had attached (so G0 passed on another rung), Q10 is skipped and F6/F7 are cut
   or rewritten to the rung's better way at rev 3.
2. Q12 (F10): open ~/yourturn.sc; Move/Copy up 5 (the cursor on step 1 is the F10 shot); Create Sketch on the top;
   circle Ø10 at (15, 15); Finish; Cut 5; Properties: expected 8,607.30 mm3 (9,000 - 392.70).

### Take D: MCP, no AI (F9 left; Q13)
out/fx14/D/noai.py: `open` ~/aligned.sc, `execute` `sketch.create` with `plane: {face: [20, 15, 25]}`; then the same
with `fixed: true`. `python3 -I out/fx14/D/noai.py |& tee D/reply.txt`. Film the terminal full window and the
window's notice. Expected: the C.1 text in the reply fields (record every field and any prefix); with `fixed: true`
the sketch is created.

### Take E: the trade-off (F8 inset, question card; Q11, Q11b)
1. Q11 attached: copy of take C's moved file with its hole. Double-click Extrude1 in the timeline (film it: F8's real
   inset), 20 to 30, OK. Event. Expected: the hole rides up with the top (top z 35); Properties 35,607.30 mm3; top face
   area 1,121.46 mm2.
2. Q11 fixed: copy of take B's file. Extrude1 20 to 30. **First record whether 0.28.0 builds a cut that ends inside
   the solid** (a closed void z 20-25), refuses it (verbatim), or reports "no material". Expected: builds; the sketch
   stays at z 25; Properties 35,607.30; top face area 1,200.00; a section view through (20, 15) shows the pocket
   (E/section.png held 4 s).
3. Q11b (logged only): copy of take B's file; Extrude1 20 to 10 (top at 15, the fixed sketch at 25 above it). Event
   `shorter: refused "line" | no material | built, volume`. Expected: unknown, logged.

### R1: section 4.

## 4. The Claude run R1 (pre-registered; PC only)
Prompt, first and only message: `Put a 10 mm hole, 5 mm deep, in the middle of the top face of this block.`
State: SolidCraft 0.28.0 on the PC open on the G0 model (~/aligned.sc copied from out/fx14/P/ for G0a: block 40 x 30 x
20 lifted 5 with Align, top at z 25; for another rung, its file and its hole numbers restated in DEVIATIONS.md BEFORE
R1 runs); MCP connected as lesson 7; Claude Code auto mode; model Sonnet 5.5 (`claude-sonnet-5-5`, the id read from
session.jsonl); network on (owner's login); one try, the greyed suggested prompt cropped. Script lab/fx14R1.sh from
lab/fx10R1.sh (same pattern: ledger line in the fixit BUDGET.tsv, session.jsonl redacted with lab/fx9redact.py,
reply.txt, tools.txt, read-after.json, after.png). **Cap $0.25**; a cap kill is filmed and narrated as what happened
(class D); no retry.
Classes (reply.txt + tools.txt + Properties and the hole's position after the run, read-after.json):
- A: a Ø10 hole 5 deep centred on the top (20, 15, from z 25 down to 20), volume 23,607.30 within 0.1%, and it says
  how (a fixed plane, the refusal named, or another plane at z 25, said).
- B: a hole another size, depth or place, or by changing the model (undoing the Align), and says so.
- C: says the hole is made when Properties shows 24,000, or misstates where it is.
- D: anything else (incl. a cap kill); recorded; F9 rewritten at the script gate.
Only whole sentences of Claude's reply are quoted; the R1 card counts only SolidCraft calls. Cost recorded (expected
about $0.15-0.18).

## 5. Measurements table (predicted BEFORE the lab)
| value | used in | how | expected | source |
|---|---|---|---|---|
| G0 rung that passes | everything | G0 | G0d most likely; G0a leans attach | ACCURACY C.6, C.11, C.9 |
| face name/certificate before and after the edit | F4 (held slot) | G0 step 1, Q14 | measure | C.6, C.11 |
| refusal line in the window, full, where | F0, F1, F4, S0 | A 1 | the C.1 line, prefix "Create Sketch:" or bare: measure | C.1, C.4 |
| report draft title | description | A 1 | "CREATE SKETCH: operation failed" | A.1 |
| fixed plane opens the sketch | F2, S1 | B 2 | yes | C.4 |
| volume before / after the hole | F5 | B 1, 3 | 24,000.00 / 23,607.30 mm3 | C.10, C.13 |
| top face area with the hole | §2.5 | B 3 | 1,121.46 mm2 | C.10 |
| Move/Copy top attaches, same hole | F6, F7 | C 1 | attaches, 23,607.30 | C.7 |
| your-turn block | F10 | C 2 | 8,607.30 mm3 | C.10 |
| MCP reply, then fixed:true | F9 | D | C.1 text; then created | C.8 |
| attached hole after 20 to 30 | F8 | E 1 | rides up, 35,607.30, area 1,121.46 | C.10 |
| fixed hole after 20 to 30 | F8, question | E 2 | builds as an inside pocket, 35,607.30, area 1,200.00 | D.3 |
| fixed hole after 20 to 10 | question option | E 3 | unknown (logged) | — |
| R1 class, cost | F9 | section 4 | measure (cap $0.25) | — |

## 6. Stop rules
- P0: as LAB-fx6.
- **S1: no G0 rung shows the exact line in the window = fx14 is dropped and reported.** No take is filmed, no R1 run;
  G0/VERDICT.txt "none" with every rung's window line verbatim; a one-paragraph note to the owner in RESULTS-fx14.md;
  the replacement is picked before the fx13 lab (not pre-picked); fx13's end screen and outro go back to fx12.
- S2: a rung shows the line through the client but a different line in the window: the window decides (fail for that
  rung); both texts logged.
- B1: "Use fixed plane" does not open the sketch, or the cut fails: type what happens; if no window path gives the
  fixed-plane hole, stop: fx14 is dropped (its fix is the title's promise).
- C1: Move/Copy also refused, or G0a attached: F6/F7 cut or rewritten at rev 3 (not a stop).
- E1: the inside cut (Q11) is refused or reports no material: verbatim; F8 build 3 and the question rewritten (not a
  stop).
- R1 rules, unexpected dialogs, max 2 fix attempts per step: as LAB-fx6.

## 7. Filming on the Ubuntu box (local-zc), as fx11/fx12 (HANDOVER-fx11-lab.md, HANDOVER-fx12-lab.md in ../2026-11-fixit-4)
- Box 192.168.1.156, user aiagent1, key ~/.ssh/ubuntu_lab_ed25519 (keep key AND password login); docker group;
  image `sc5-l5:0.28.0` already loaded (ID into env.txt).
- Job dir ~/jobs/fx14 with copies of the lab repo's `lab/`, `checker/` and `client/` (scp from the PC); scripts
  lab/fx14lib.sh (GUI positions at UI scale 1.8, 2880x1620, from lab/fx12lib.sh), lab/fx14G0.sh, fx14P.sh, fx14A.sh,
  fx14B.sh, fx14C.sh, fx14D.sh, fx14E.sh; box helpers ~/jobs/fx14/sm.sh, sheet.sh (as fx10, not in the repo).
- **Screen positions probed once, then reused** (the fx12 lesson: its probe container fx12p found every GUI path once,
  s0-s24, and lab/fx12lib.sh reused them): one probe container fx14p finds Create Sketch, the face click, the "Use fixed
  plane" button, the circle tool, Finish, Extrude Cut, Move/Copy, Align, the timeline's Extrude1 and Properties, writes
  them to the end of lab/fx14lib.sh, and is then stopped and removed. G0's window checks reuse the same positions.
  Re-probe only a dialog whose screenshot differs (logged in DEVIATIONS.md).
- No host ffmpeg: recording (x11grab 30 fps + cursor log), clip cuts, stills and contact sheets use the ffmpeg inside
  the container; all takes `--network none`.
- Results `scp` back into solidcraft-course-lab out/fx14/; footage.py zoom passes and renders run on the PC; clips
  script lab/fx14clips.py from each take's events.jsonl (as lab/fx12clips.py, test first). Commit locally only (prereg,
  G0 verdict, P + scripts, takes + answers); never push. Markers out/fx14/G0.DONE (after G0) and
  out/fx14/fx14-lab.DONE. No fx14 containers left on the box.
- R1 runs on the PC only (section 4).

## 8. Deliverables
out/fx14/env.txt, PREREG.txt, G0/* (tools.txt, client.txt, rungs.tsv, g0X-window.png, VERDICT.txt), P/* (block.py,
volumes.txt), {A,B,C,D,E}/events.txt + screen.mp4 + screenshots, D/reply.txt, runs/R1/*, ANSWERS.md (Q8-Q14, Q11b,
Q15), DEVIATIONS.md; RESULTS-fx14.md in this folder; HANDOVER-fx14-G0.md (after G0) and HANDOVER-fx14-lab.md.
