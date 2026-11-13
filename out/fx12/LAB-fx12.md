# LAB-fx12: SolidCraft Offset: "its corners follow its source curves" — pre-registration v1, 2026-11-12 (PLAN rev 2, DECISIONS round 1 applied) (before any run)

Lab repo: solidcraft-course-lab. Folder: out/fx12/ (takes P, A, B, C, D; run runs/R1). Committed before the first
container starts (hash into out/fx12/PREREG.txt); `| tee` on every command; deviations in out/fx12/DEVIATIONS.md;
nothing re-scored. Runs after fx11's lab (one lab at a time on the box) and the owner's GO. Never pushed by the lab.

## 0. Pins
As LAB-fx11 section 0 (= `../2026-11-fixit-2/LAB-fx6.md` section 0): SolidCraft 0.28.0, image `sc5-l5:0.28.0`, image
ID checked against 2992c9ecbca2, takes `--network none`; env to out/fx12/env.txt. Stop rule P0 as LAB-fx6.

## 1. Questions (PLAN §0.4): Q8-Q14, Q15 (R1).

## 2. Common to every take
As LAB-fx6 section 2 (full-window recording, events.txt/events.jsonl, 3 s full-window open, 4 s holds on every line
to read). Filmed on the Ubuntu box (LAB-fx11 section 7, job dir ~/jobs/fx12).

## 3. Takes, in run order

### Take P: start files (not filmed)
No-AI script out/fx12/P/tray.py (MCP client, no AI):
- ~/tray.sc: sketch on XY, rectangle 60 x 40 centred on the origin (x -30..30, y -20..20); ONE Offset of the 4 lines,
  2 mm inward (linked). Log the curve ids (outline and copy) into P/ids.txt. Expected regions: ring 2,400 - 2,016 =
  384 mm2.
- ~/tray-plain.sc: the 60 x 40 rectangle only (for take C and the your-turn shot).
- ~/box.sc: rectangle 50 x 30 only (F10 your-turn start).
Each file reopened; ids and region areas read back into P/check.txt; a mismatch = stop (P0).

### Take A: the refusal (F0, F4, F7 left; Short S0)
Open ~/tray.sc, edit the sketch. Full window 3 s; the sketch with the copy held 4 s; zoom target the 2 mm dimension.
1. Q8: Fillet (sketch), radius 3 (record the menu path, the field, defaults; A/dialog.png); click one inner corner.
   Event `fillet copy: "full line as shown"`; A/refusal.png held 4 s; record the curve id shown (`lN`); Report draft
   title if offered (not submitted). Expected "Fillet: `lN` is an offset, and its corners follow its source curves:
   round or cut the source corners before offsetting, or break the offset association first" (prefix measured;
   B.10, B.3); title "FILLET: operation failed". The sketch unchanged after (B.11): compare ids/regions to P/ids.txt.
2. Also Chamfer on the same corner (logged only, same rule expected).

### Take B: Fix 1, break the association (F2, F6 left)
Open ~/tray.sc.
1. Q9: select one inner line; right-click; "Break Offset Association" (B/menu.png zoomed); event. Do the other three
   inner lines still show as offset (tick/marker)? Expected one click frees all four (B.12).
2. Fillet 3 on the four inner corners: event `fillet after break: 4 built | N refused`.
3. Finish the sketch; Extrude the ring region 20; Properties volume. Expected 7,834.51 mm3 (B.13).
4. Q11 Fix 1: Measure the wall along a corner's diagonal, from the outside (sharp) corner to the inner arc's
   midpoint. Pre-registered 4.07 mm (5 x sqrt(2) - 3). B/wall.png held 4 s.

### Take C: Fix 2, round first (F5, F6 right, F7 right, F10, F11; Short S1, S2)
1. Q10: open ~/tray-plain.sc; Fillet the outline's four corners 5 FIRST (the F5 label "want 3 + wall 2 = round 5" is
   added in post, BEFORE the Fillet); then Offset 2 inward (one offset). Event `offset after round: built | refused`.
   Log the offset path: a closed loop of lines plus tangent arcs takes the convex G1 path (offset_topology.rs 140-230);
   record the copy's ids (expected topology outputs, arcs "aN") into C/ids.txt. Is the copy still linked (marker /
   right-click shows Break Offset Association)?
2. Measure one inside arc: expected R 3.00. C/measure.png held 4 s.
3. Extrude the ring 20; Properties: expected 7,405.31 mm3 (B.13).
4. Q11 Fix 2: Measure the wall along the diagonal, outer arc's midpoint to inner arc's midpoint: pre-registered
   2.00 mm. (Sharp/sharp reference 2.83 mm is arithmetic only, not filmed.)
5. Q14 (logged; F8 "stays tied"): before the extrude in a copy of step 1, change the rectangle width 60 to 70:
   does the copy follow (ids from C/ids.txt kept), inside corners still R 3.00? Event.
6. Q12 (pinned comment only): fresh ~/tray-plain.sc; Fillet the outline 1.5; Offset 2 inward. Event `R1.5 offset:
   sharp | round | refused "line"`. Expected SHARP inner corners (arcs retired, B.9), NOT "the offset collapses an
   arc". Extrude 20: expected 7,641.37 mm3. Also the Short S2 end frame: 5 s hold on the R1.5 outline before the
   Offset.
7. F10: open ~/box.sc, cursor on step 1 (Fillet on the outline), banner added in post. Your-turn answer (pinned):
   round 6, offset 3, inside R 3 (logged only if time allows; not narrated).

### Take D: MCP, no AI (F9 left)
out/fx12/D/noai.py: `open` ~/tray.sc, `execute` `sketch.fillet` (`points` = one inner corner of the copy, `radius`
3; names from the MCP tool list, logged); `python3 -I out/fx12/D/noai.py |& tee D/reply.txt`. Film the terminal full
window and the window's notice. Expected the B.10 text after "invalid parameters for `sketch.fillet`: " (Q13).

### R1: section 4.

## 4. The Claude run R1 (pre-registered; PC only)
Prompt, first and only message: `Round the four inside corners of this tray sketch to 3 mm.`
State: SolidCraft 0.28.0 on the PC open on ~/tray.sc (outer 60 x 40, the 2 mm offset linked; copied from
out/fx12/P/); MCP connected as lesson 7; auto mode; Sonnet 5.5 (`claude-sonnet-5-5`, id from session.jsonl); network
on; one try, greyed suggested prompt cropped. Script lab/fx12R1.sh from lab/fx10R1.sh (ledger, redact with
lab/fx9redact.py, reply.txt, tools.txt, read-after.json, after.png). **Cap $0.25**; cap kill = class D, filmed and
narrated as what happened; no retry.
Classes (reply + tool calls + the sketch after the run, Measure on each inside corner, the outline's size):
- A: reports the refusal (or the offset link) and ends with four inside corners of 3.00 mm, the outline still
  60 x 40, saying how (broke the association, or rounded the outline 5 and offset again, said).
- B: rounds them another way or to another radius, or changes the outline, and says so.
- C: says the corners are rounded when Measure shows sharp corners, or misstates the radius.
- D: anything else (incl. a cap kill); recorded; F9 rewritten at the script gate.
Cost recorded (expected about $0.15).

## 5. Measurements table (predicted BEFORE the lab)
| value | used in | how | expected | source |
|---|---|---|---|---|
| refusal on the copy's corner, full line, id | F0, F4, S0 | A 1 | "Fillet: `lN` is an offset, and its corners follow its source curves: round or cut ... first" | B.10, B.3 |
| sketch after the refusal | F4 | A 1 | unchanged | B.11 |
| one Break frees all four | F2 | B 1 | yes | B.12 |
| Fix 1 volume (inside R3, sharp outside) | F6 | B 3 | 7,834.51 mm3 | B.13 |
| Fix 1 wall at the corner (diagonal) | F6 | B 4 | 4.07 mm | 5 x sqrt(2) - 3 |
| round 5 then offset 2: inside radius | F5, S1 | C 2 | R 3.00 | B.9 |
| Fix 2 volume | F6 | C 3 | 7,405.31 mm3 | B.13 |
| Fix 2 wall at the corner | F6 | C 4 | 2.00 mm | concentric arcs |
| copy ids after round-first, linked | F8 | C 1 | arcs "aN", linked | offset_topology.rs 140-230 |
| width 60 to 70, copy follows | F8 | C 5 | follows, R 3.00 | B.14 |
| outline 1.5, offset 2 | pinned | C 6 | sharp inside, 7,641.37 mm3 | B.9, B.13 |
| MCP reply | F9 | D | B.10 text with the prefix | B.15 |
| R1 class, cost | F9 | section 4 | measure (cap $0.25) | — |

## 6. Stop rules
- P0: as LAB-fx6.
- A1: the window's Fillet refuses earlier, greys out on the copy, or shows a different line: type it verbatim; if
  another window path shows the line (e.g. chamfer, or picking the corner differently), film it; else stop: fx12 is
  dropped (PLAN §2.11).
- A2: the words differ: verbatim; the title follows the screen.
- C1: round-first does not give R 3.00, or the copy unlinks: log; F5 and the peg "tighter" are rewritten at the
  script gate to what Measure shows.
- C2: Q12 is refused with "the offset collapses an arc": log; only the pinned answer changes.
- R1 rules, unexpected dialogs, max 2 fix attempts per step: as LAB-fx6.

## 7. Filming
As LAB-fx11 section 7, with job dir ~/jobs/fx12, scripts lab/fx12lib.sh, fx12P/A/B/C/D.sh, lab/fx12clips.py, marker
out/fx12/fx12-lab.DONE. R1 on the PC only.

## 8. Deliverables
out/fx12/env.txt, PREREG.txt, P/* (tray.py, ids.txt, check.txt), {A,B,C,D}/events.txt + screen.mp4 + screenshots,
C/ids.txt, D/reply.txt, runs/R1/*, ANSWERS.md (Q8-Q14, Q15), DEVIATIONS.md; RESULTS-fx12.md in this folder;
HANDOVER-fx12-lab.md.
