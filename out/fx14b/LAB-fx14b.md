# LAB-fx14b: SolidCraft Create Sketch: "this face has no supported stable semantic lineage" — pre-registration v1.1, 2026-11-13 (PLAN rev 4) (before any run)

v1.1 = wording only, from the fx14b plan gate (DECISIONS.md "plan gate fx14b"): the History bar / Browser wording
(take A, Q25), no OK after Use fixed plane (take B), fx8's Hole went through (take C), a reviewer note on Q25. No
prediction, pass rule, stop rule or class changed.

Lab repo: solidcraft-course-lab. Folder: out/fx14b/ (takes P, A, B, C, D, E; run runs/R1). Committed before the first
container starts (hash into out/fx14b/PREREG.txt); `| tee` on every command; deviations in out/fx14b/DEVIATIONS.md;
nothing re-scored. Runs only after (1) the 3-reviewer plan gate on PLAN section 2 and its DECISIONS (applied: PLAN rev 4), (2) the
fx13 lab has finished and left no containers on the box, and (3) the owner's GO; one lab at a time on the box. Never
pushed by the lab. Replaces LAB-fx14.md (rev 2's fx14, run as gate G0 on 13 Nov, result none, closed); G0d's record
(out/fx14/G0/rungs.tsv, client.txt, g0d-*.png) is this lab's prior: the line was already seen once, window and client.

## 0. Pins
As LAB-fx11 section 0 (= `../2026-11-fixit-2/LAB-fx6.md` section 0): SolidCraft 0.28.0, run image `sc5-l5:0.28.0`
(`solidcraft --version` = "solidcraft 0.28.0"; the box's copy is sha256:38a6f6787dc1..., the PC's 2992c9ecbca2, as
out/fx14/DEVIATIONS.md 1), all takes `--network none`; env to out/fx14b/env.txt (image ID, version line, Xvfb size, UI
scale, Claude Code version for R1). Stop rule P0 as LAB-fx6.

## 1. Questions (PLAN §0.4): Q20 (gate G1), Q21-Q28, Q29 (R1).

## 2. Common to every take
As LAB-fx6 section 2 (full-window recording of the whole display, TAKE/screen.mp4 x11grab 30 fps + cursor log,
events.txt/events.jsonl, 3 s full-window open, 4 s holds on every line to read). Filmed on the Ubuntu box (section 7).

## 3. Takes, in run order

### Take P: start files (not filmed)
No-AI script out/fx14b/P/blocks.py (MCP client, no AI; command and parameter names from G0's tool list,
out/fx14/G0/tools.txt and commands.json, re-read and logged). The converted files repeat G0d's recipe exactly:
rectangle on XY, Extrude New Body, `file.save_mesh` to an STL, `new_design`, `file.insert_mesh`, `mesh.convert`.
- ~/conv.sc: block 40 x 30 x 20 (corner at the origin), converted. Expected 24,000.00 mm3 (G0d measured it).
- ~/conv2.sc, ~/conv3.sc: copies of conv.sc for takes C and Q23 (fresh, no cut).
- ~/block.sc: block 40 x 30 x 20, plain Extrude, NOT converted (Q21 control). Expected 24,000.00.
- ~/conv30.sc: block 30 x 30 x 10, converted (Q26, the your-turn block). Expected 9,000.00.
- ~/offset.sc: rectangle 40 x 30 on XY, Extrude New Body 20 with a start offset of 5 (Q28 only). Expected 24,000.00,
  top at z 25.
Each file reopened and its volume read back into P/volumes.txt; a mismatch over 0.1% = stop (P0). Face names logged
with `model.faces` for conv.sc and block.sc (expected: conv.sc top "F4:face:5"-style, exact false, as G0d; block.sc top
"F2:top", exact true).

### Take A: the refusal (F0, F1, F4 left; Short S0; Q20 = gate G1)
Open ~/conv.sc. Full window 3 s; slow orbit (F1); the History bar (in 0.28.0 icons with no names) and then the Browser's Features
folder or a hover tooltip, zoomed on the Insert Mesh step and ConvertMesh1 (F1).
1. Q20: Create Sketch (G0's path: New Sketch 128 88, halved units), click the top at (20, 15, 20) (G0's top-face point
   830 330 at the Home view). Event `sketch on converted top: "full line as shown"`; A/refusal.png held 4 s; the hint
   and the "Use fixed plane" button recorded (A/dialog.png) but they are NOT the pass. Create Issue: the draft title
   (expected "CREATE SKETCH: operation failed"), A/report.png, then Close draft (not submitted).
   **Gate G1 pass = the red line in full: "Create Sketch: this face has no supported stable semantic lineage; choose a
   supported exact face or explicitly use fixed:true".**
2. A/hold.png: the line held 8 s for F4's slow zoom (moving zoom in post by footage.py; F4's diagram builds every 6 s
   or less).
3. Cancel the sketch dialog.

### Take B: the fix, Use fixed plane (F2, F5, F7 left; Short S1 first half; Q22)
Open ~/conv.sc.
1. Create Sketch, click the top: the line again; click "Use fixed plane" (zoom; no OK click: the sketch opens at once,
   dialogs.rs 3396-3411). Event `fixed plane: sketch opened |
   "line"`; B/fixed.png.
2. Circle Ø10 centred (20, 15); Finish; Extrude, Cut, 5 into the block. Event `fixed-plane cut: built | "line"`
   (record first whether a cut builds on a converted body; fx8 Q12 only drilled one with Hole). B/cut.png.
3. Q22: right-click the body in the Browser, Properties: expected 23,607.30 mm3 (24,000 - 392.70); B/props.png held
   4 s. Measure the top face: expected 1,121.46 mm2 (1,200 - 78.54); B/area.png.
4. F7 left / F11: the block with its hole turning (5 s).

### Take C: the better way and the your-turn (F6, F7 right, F10; Short S1 second half; Q24, Q26)
1. Q24: open ~/conv2.sc. Model, Hole (record the menu path, C/menu.png); click the top at (20, 15, 20); Simple, Ø10,
   depth 5; OK (fx8 Q12's Hole went through, Extents All; this depth-5 Hole is new). Event `hole on converted top: built | "line"`; Properties: expected 23,607.30; C/hole.png,
   C/props.png. Timeline shows Hole1 after ConvertMesh1 (as fx8 B/hole-timeline.png).
2. Q26 (F10): open ~/conv30.sc; the cursor on step 1 (Create Sketch, top, the line, Use fixed plane) is the F10 shot;
   circle Ø10 at (15, 15), Finish, Extrude Cut 5; Properties: expected 8,607.30 (9,000 - 392.70).

### Take D: MCP, no AI (F9 left; Q27)
out/fx14b/D/noai.py: `open` ~/conv.sc; `execute` `sketch.create` with `plane: {face: [20, 15, 20]}` (names from the
tool list, logged); then the same call with `fixed: true`. `python3 -I out/fx14b/D/noai.py |& tee D/reply.txt`. Film
the terminal full window and the window's notice. Expected: call 1 isError true, "invalid parameters for
`sketch.create`: this face has no supported stable semantic lineage; choose a supported exact face or explicitly use
fixed:true" (as G0d, out/fx14/G0/client.txt); call 2 a sketch created on a fixed plane (record every reply field).

### Take E: the control and the trade-off evidence (F8 inset, question card, Short S2; Q21, Q23, Q25, Q28)
1. Q25: open ~/conv.sc; double-click ConvertMesh1 in the History bar or the Browser's Features folder, then the Insert Mesh step: record every field each
   offers (E/convert-edit.png, E/insert-edit.png; expected no length or size field). Reviewer note (accuracy SHOULD 4, not a prediction change): `mesh.convert`
   takes `tolerance` (default 0.05 mm), so a Tolerance field may show; record it as seen. Cancel both.
2. Q21: open ~/block.sc; a 5 s hold on the plain block (Short S2 end frame); Create Sketch, click the top. Event
   `sketch on extruded top: attached | "line"`; expected attaches, "SketchN — fully constrained" (E/control.png).
   Cancel.
3. Q23: open ~/conv3.sc; Extrude, pick the top FACE itself (no sketch), distance 5. Event `extrude face: "full line" |
   built`; E/extrude-face.png held 4 s; record the prefix (expected "invalid parameters for `face profile`:" or a
   window label) and whether the Extrude dialog offers a fixed-plane control.
4. Q28 (recorded only): open ~/offset.sc; Create Sketch, click the top at (20, 15, 25). Event `sketch on offset-start
   top: attached | "line"`; source prediction attaches (eval.rs 5525-5534). Not filmed for the video unless refused.

### R1: section 4.

## 4. The Claude run R1 (pre-registered; PC only)
Prompt, first and only message: `Put a 10 mm hole, 5 mm deep, in the middle of the top face of this block.`
State: SolidCraft 0.28.0 on the PC open on ~/conv.sc (copied from out/fx14b/P/; the converted 40 x 30 x 20 block, top
at z 20); MCP connected as lesson 7; Claude Code auto mode; model Sonnet 5.5 (`claude-sonnet-5-5`, the id read from
session.jsonl); network on (owner's login); one try, the greyed suggested prompt cropped. Script lab/fx14bR1.sh from
lab/fx13R1.sh (same pattern: ledger line in the fixit BUDGET.tsv, session.jsonl redacted with lab/fx9redact.py,
reply.txt, tools.txt, read-after.json, after.png). **Cap $0.25**; a cap kill is filmed and narrated as what happened
(class D); no retry.
Pre-registered expectation (from G0d's client reply, before the run): a `sketch.create` on the top face gets the line
with isError true; the reply says "explicitly use fixed:true", so Claude will probably retry with `fixed: true` or use
`solid.hole`; expected class A. F9 never says Claude "knew" the fix when it followed the reply (tools.txt shows which).
Classes (reply.txt + tools.txt + Properties after the run, read-after.json):
- A: a Ø10 hole 5 deep centred on the top (20, 15, from z 20 to 15), volume 23,607.30 within 0.1%, and it says how (a
  fixed plane, the Hole tool, or the refusal named).
- B: a hole another size, depth or place, or by rebuilding the block as a new Extrude, and says so.
- C: says the hole is made when Properties shows 24,000, or misstates where it is.
- D: anything else (incl. a cap kill); recorded; F9 rewritten at the script gate.
Only whole sentences of Claude's reply are quoted; the R1 card counts only SolidCraft calls. Cost recorded (expected
about $0.15-0.18).

## 5. Measurements table (predicted BEFORE the lab)
| value | used in | how | expected | source |
|---|---|---|---|---|
| converted block volume | F5 | P | 24,000.00 mm3 | G0d (rungs.tsv) |
| converted top's name | F4 build 3 | P | "F4:face:5"-style, exact false | G0d Q14 record |
| refusal line, full, where (gate G1) | F0, F4, S0 | A 1 | "Create Sketch: this face has no supported stable semantic lineage; choose a supported exact face or explicitly use fixed:true", red, in the Create Sketch dialog | F.1, F.2; G0d |
| hint and button | F2 | A 1 | "This face cannot provide a durable attachment. Choose another face or explicitly use a fixed plane." / "Use fixed plane" | F.4 |
| report draft title | description | A 1 | "CREATE SKETCH: operation failed" | G0d |
| Use fixed plane: sketch opens | F2, S1 | B 1 | opens | F.4 |
| fixed-plane cut on the converted body | F2, F5, F7 | B 2-3 | built, 23,607.30 mm3; top face 1,121.46 mm2 | F.8 |
| Hole tool on the converted top | F6, F7, S1 | C 1 | built, no message, 23,607.30 mm3 | fx8 Q12 (F.7) |
| your-turn block | F10 | C 2 | 8,607.30 mm3 | F.8 |
| MCP face / fixed:true | F9 | D | the line, isError true / sketch created | G0d client |
| ConvertMesh1 and Insert Mesh edit fields | F8 | E 1 | no size field | F.9 (to measure) |
| plain extruded top | F8, question card, S2 | E 2 | attaches, no message | G0 control (F.6) |
| Extrude on the converted face | F2 chip | E 3 | "... `face profile`: this face has no supported stable semantic lineage; ..." | F.3 (reports) |
| offset-start top (recorded only) | pinned comment if refused | E 4 | attaches | F.10 |
| R1 class, cost | F9 | section 4 | class A; cap $0.25 | F.2 |

## 6. Stop rules
- P0: as LAB-fx6.
- S1b (gate G1): take A does not show the red line in full (another line, the hint alone, or the sketch opens): type
  what happens; stop: fx14b is dropped and reported (PLAN §2.11). No improvised rungs.
- A2: the words differ from G0d's: verbatim; the title follows the screen.
- B1 (stated before the run): the fixed-plane Extrude Cut is refused on the converted body: type the line; the hole in
  F2/F5/F7 then comes from the Hole tool (take C) and the fixed-plane sketch is filmed only to the sketch opening;
  written into DEVIATIONS.md before take C. If the Hole tool is ALSO refused (C1 below), stop: fx14b is dropped.
- C1: the Hole tool refuses the converted top: log the line; F6/F7 are cut; S1 ends at "Use fixed plane" (not a stop
  unless B1 also fired).
- E1: the plain extruded top (Q21) is refused: stop and report (it contradicts G0's control; the question card and F8
  cannot be written).
- E2: Q23 or Q28 surprise: log only (not a stop); F2's chip is dropped if Q23 is not the line.
- R1 rules, unexpected dialogs, max 2 fix attempts per step: as LAB-fx6.

## 7. Filming on the Ubuntu box (local-zc), as fx11/fx12 (HANDOVER-fx11-lab.md, HANDOVER-fx12-lab.md in ../2026-11-fixit-4)
- Box 192.168.1.156, user aiagent1, key ~/.ssh/ubuntu_lab_ed25519 (keep key AND password login); docker group;
  image `sc5-l5:0.28.0` already loaded (ID into env.txt).
- Job dir ~/jobs/fx14b with copies of the lab repo's `lab/`, `checker/` and `client/` (scp from the PC); scripts
  lab/fx14blib.sh (GUI positions at UI scale 1.8, 2880x1620, from lab/fx14 G0's probe and lab/fx12lib.sh),
  lab/fx14bP.sh, fx14bA.sh, fx14bB.sh, fx14bC.sh, fx14bD.sh, fx14bE.sh; box helpers ~/jobs/fx14b/sm.sh, sheet.sh (as
  fx10, not in the repo).
- **Screen positions probed once, then reused**: G0's probe already found New Sketch 128 88, top face 830 330, sketch
  Cancel 1180 90, Create Issue 1252 504, Close draft 733 670 (halved units, Home view of a 40 x 30 x 20 block;
  out/fx14/DEVIATIONS.md 8), reused as they are. One probe container fx14bp finds only what is new (Use fixed plane,
  the circle tool, Finish, Extrude Cut fields, Model > Hole and its fields, Properties, Measure, the timeline's
  ConvertMesh1 and Insert Mesh rows), writes them to the end of lab/fx14blib.sh, and is then stopped and removed.
  Positions already in lab/fx12lib.sh / fx13lib.sh (Browser, Properties) are reused, not re-probed.
- No host ffmpeg: recording (x11grab 30 fps + cursor log), clip cuts, stills and contact sheets use the ffmpeg inside
  the container; all takes `--network none`.
- Results `scp` back into solidcraft-course-lab out/fx14b/; footage.py zoom passes and renders run on the PC; clips
  script lab/fx14bclips.py from each take's events.jsonl (as lab/fx12clips.py, test first). Commit locally only
  (prereg, P + scripts, takes + answers); never push. Marker out/fx14b/fx14b-lab.DONE. No fx14b containers left on the
  box.
- R1 runs on the PC only (section 4).

## 8. Deliverables
out/fx14b/env.txt, PREREG.txt, P/* (blocks.py, volumes.txt, faces.txt), {A,B,C,D,E}/events.txt + screen.mp4 +
screenshots, D/reply.txt, runs/R1/*, ANSWERS.md (Q20-Q29), DEVIATIONS.md; RESULTS-fx14b.md in this folder;
HANDOVER-fx14b-lab.md.
