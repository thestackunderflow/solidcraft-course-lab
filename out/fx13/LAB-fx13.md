# LAB-fx13: SolidCraft Shell: "Tangent Chain opens every face of this body" — pre-registration v1, 2026-11-13 (PLAN rev 2, DECISIONS round 1 applied) (before any run)

Lab repo: solidcraft-course-lab. Folder: out/fx13/ (takes P, A, B, C, D; run runs/R1). Committed before the first
container starts (hash into out/fx13/PREREG.txt); `| tee` on every command; deviations in out/fx13/DEVIATIONS.md;
nothing re-scored. Runs after fx14's gate G0 has written out/fx14/G0/VERDICT.txt (PLAN §3: G0 first; if G0 dropped
fx14, the replacement is picked before this lab) and the owner's GO; one lab at a time on the box. Never pushed by the
lab.

## 0. Pins
As LAB-fx11 section 0 (= `../2026-11-fixit-2/LAB-fx6.md` section 0): SolidCraft 0.28.0, run image `sc5-l5:0.28.0`
(`solidcraft --version` = "solidcraft 0.28.0"; image ID on the box checked against the PC's 2992c9ecbca2), all takes
`--network none`; env to out/fx13/env.txt (image ID, version line, Xvfb size, UI scale, Claude Code version for R1).
Stop rule P0 as LAB-fx6.

## 1. Questions (PLAN §0.4): Q1-Q7, Q3b, Q15 (R1).

## 2. Common to every take
As LAB-fx6 section 2 (full-window recording of the whole display, TAKE/screen.mp4 x11grab 30 fps + cursor log,
events.txt/events.jsonl, 3 s full-window open, 4 s holds on every line to read). Filmed on the Ubuntu box (section 7).

## 3. Takes, in run order

### Take P: start files (not filmed)
No-AI script out/fx13/P/cups.py (MCP client, no AI; tool and parameter names from the MCP tool list, logged). Every cup
is a circle centred on the origin on XY, extruded up (z 0 up), its outer edges rounded with Fillet:
- ~/cup.sc: Ø60, 80 tall; top and bottom outer edges rounded 1.5. Expected solid 226,014.67 mm3 (ACCURACY B.9).
- ~/cup-bottom.sc: Ø60 x 80; only the bottom edge rounded 1.5 (Q3, the second cup). Expected 226,104.67.
- ~/cup-r3.sc: Ø60 x 80; top and bottom edges rounded 3 (Q4, pinned bonus only). Expected 225,482.81.
- ~/cup40.sc: Ø40, 40 tall; top and bottom edges rounded 1 (Q5, the your-turn cup). Expected 50,212.15.
Each file reopened and its volume read back into P/volumes.txt; a mismatch over 0.1% = stop (P0). Face counts logged
(expected 5 faces on cup.sc, cup-r3.sc and cup40.sc: top, round, side, round, bottom; 4 on cup-bottom.sc).

### Take A: the refusal (F0, F1, F4 left, F7 left; Short S0; Q1, Q3b)
Open ~/cup.sc. Full window 3 s; slow orbit (F1); a 2 s section view if the window has one (else log and skip; F1 then
uses take B's section only).
1. Q1: Shell (record the menu path and the dialog with its defaults, A/dialog.png: is Tangent Chain ticked? the
   thickness default? inside/outside?). Click the top face at (0, 0, 80). Does the preview light EVERY face
   (dialogs.rs 1398-1410)? A/preview.png held 4 s. Thickness 2. Event `shell top chain on: "full line as shown"`;
   record whether the line is live in the dialog or after OK; A/refusal.png held 4 s. Report draft title if offered
   (not submitted), A/report.png. Does a failed Shell stay in the timeline?
2. A/hold.png: the line held 8 s for F4's slow zoom (the moving zoom is done in post by footage.py; F4's diagram builds
   every 6 s or less, so no still stays unchanged longer).
3. Q3b (the F10 question card): Cancel, Shell again (chain still on), click the SIDE at (30, 0, 40) instead of the top.
   Event `shell side chain on: N faces lit, "line" | built`; A/side.png held 4 s. Expected: all five light, the same
   line (F4's rule from another pick).

### Take B: the fix (F2, F5, F7 right, F11; Short S1; Q2, Q7)
Open ~/cup.sc.
1. Shell; the Tangent Chain checkbox zoomed (ticked), then unticked (B/untick.png); click the top: only the top lights
   (B/preview.png); thickness 2; OK. Event `shell top chain off: built | "line"`.
2. Q2: right-click the body in the Browser, Properties: expected 33,900.00 mm3 (226,014.67 - 192,114.67; B.9);
   B/props.png held 4 s.
3. Q7: Measure across the side wall at mid-height (z 40), outer side face to inner side face: pre-registered 2.00 mm;
   if Measure reports centre-to-centre for two cylinders, record Min (as fx12 Q11). B/wall.png held 4 s. Measure the
   floor (z 0 to z 2): expected 2.00. Never measured at the rim (0.5 mm wide at z 80: outer r 28.5, cavity r 28).
4. A section view of the hollow cup (B/section.png, F1's 2 s goal shot and F2's end); the inner bottom corner expected
   sharp (offset.rs 720: the 1.5 round is thinner than the 2 mm move; logged, not narrated).
5. F11: the hollow cup turning (5 s).

### Take C: the rule, the your-turn, the bonus (F6, F10; Short S2; Q3, Q4, Q5)
1. Q3: open ~/cup-bottom.sc (the SECOND cup, label added in post). Shell, Tangent Chain left ON; click the top. Event
   `second cup chain on: N faces lit`; C/preview.png held 4 s (expected only the top). Thickness 2; OK. Event
   `built | "line"`. Properties: expected 33,990.00 mm3 (226,104.67 - 192,114.67). Zoom target the sharp top edge.
   Before the Shell: a 5 s hold on the second cup (Short S2 end frame).
2. Q5 (F10): open ~/cup40.sc; the cursor on step 1 (Shell, untick Tangent Chain) is the F10 shot; the top only, 2 mm,
   OK; Properties: expected 11,532.86 mm3 (50,212.15 - 38,679.29).
3. Q4 (pinned bonus only, "On 0.28.0:"): open ~/cup-r3.sc; Shell, Tangent Chain OFF, the top only, 2 mm, OK. Event
   `r3 chain off: "full line" | built, volume`. Expected refused with "the rim would have no thickness: an open face
   meets a round of radius 3.0000 mm tangentially, and the shell is 2.0000 mm thick (make the round smaller than the
   thickness)" (polyhedron.rs 482-486; may be prefixed "Shell:").

### Take D: MCP, no AI (F9 left; Q6)
out/fx13/D/noai.py: `open` ~/cup.sc; `execute` `solid.shell` with faces = the top point (0, 0, 80), thickness 2,
`tangent_chain: true` (names from the MCP tool list, logged). Then reopen ~/cup.sc and send the same call WITHOUT
`tangent_chain`. `python3 -I out/fx13/D/noai.py |& tee D/reply.txt`. Film the terminal full window and the window's
notice. Expected: call 1 = the B.1 text in the reply fields (record every field and any prefix); call 2 = built,
33,900.00 mm3 (the plug defaults the chain off, features.rs 2755).

### R1: section 4.

## 4. The Claude run R1 (pre-registered; PC only)
Prompt, first and only message: `Hollow out this cup with 2 mm walls and leave the top open.`
State: SolidCraft 0.28.0 on the PC open on ~/cup.sc (Ø60 x 80, top and bottom edges rounded 1.5; copied from
out/fx13/P/); MCP connected as lesson 7; Claude Code auto mode; model Sonnet 5.5 (`claude-sonnet-5-5`, the id read
from session.jsonl); network on (owner's login); one try, the greyed suggested prompt cropped. Script lab/fx13R1.sh
from lab/fx10R1.sh (same pattern: ledger line in the fixit BUDGET.tsv, session.jsonl redacted with lab/fx9redact.py,
reply.txt, tools.txt, read-after.json, after.png). **Cap $0.25** (fx12's R1 cost $0.1761); a cap kill is filmed and
narrated as what happened (class D); no retry.
Pre-registered expectation (from the source, before the run): through MCP `solid.shell` defaults `tangent_chain` to
false (features.rs 2755 `unwrap_or(false)`), so Claude will almost surely NOT meet the line; expected class A or B. It
meets the line only if it sets `tangent_chain: true` itself (logged from tools.txt). F9 never says Claude "avoided" the
error by skill.
Classes (reply.txt + tools.txt + Properties and Measure after the run, read-after.json):
- A: an open-top cup, walls 2.00, volume 33,900 within 0.1%, and it says how (top face only, tangent chain off, or the
  refusal named).
- B: hollow another way or another thickness (outside, both, a cut), and says so.
- C: says the cup is hollow when Properties shows the solid volume, or misstates what opened.
- D: anything else (incl. a cap kill); recorded; F9 rewritten at the script gate.
Only whole sentences of Claude's reply are quoted; the R1 card counts only SolidCraft calls. Cost recorded (expected
about $0.15-0.18).

## 5. Measurements table (predicted BEFORE the lab)
| value | used in | how | expected | source |
|---|---|---|---|---|
| dialog defaults | F2 | A 1 | Tangent Chain ticked; thickness default: measure | B.3 |
| preview on the top pick, chain on | F0, F4 | A 1 | all 5 faces lit | B.2, B.3 |
| refusal line, full, where | F0, F4, S0 | A 1 | "Tangent Chain opens every face of this body, leaving no walls; turn off Tangent Chain to remove only the picked faces" (maybe "Shell:" prefix); live or after OK: measure | B.1 |
| report draft title | description | A 1 | "SHELL: operation failed" | A.1 |
| side pick, chain on | F10 question | A 3 | all 5 lit, the same line | B.2 |
| chain off, top, 2 mm | F2, F7, S1 | B 1 | built | B.6 (1.5 under 2) |
| hollow cup volume | F5 | B 2 | 33,900.00 mm3 | B.9 |
| side wall at mid-height / floor | F5 | B 3 | 2.00 / 2.00 mm | B.9 |
| inner bottom corner | logged | B 4 | sharp | B.7 |
| second cup, chain on: lit, built, volume | F6, S2 | C 1 | top only, built, 33,990.00 mm3 | B.2, B.9 |
| your-turn cup | F10 | C 2 | 11,532.86 mm3 | B.9 |
| rounds 3, chain off | pinned bonus | C 3 | refused, rim line | B.6 |
| MCP chain on / chain unset | F9 | D | B.1 text / built 33,900.00 | B.4 |
| R1 class, cost | F9 | section 4 | class A or B (chain default off); cap $0.25 | B.4 |

## 6. Stop rules
- P0: as LAB-fx6.
- A1: the window refuses earlier (the top cannot be picked, OK greys with no line, or another line): type what
  happens; if another window path shows the line (e.g. the side pick of A 3), film it; else stop: fx13 is dropped
  (PLAN §1.11).
- A2: the words differ: verbatim; the title follows the screen.
- B1 (stated before the run): the chain-off shell is refused for another reason: rerun take P with rounds 1.0 instead of
  1.5 (cup.sc only; expected solid and shell restated in DEVIATIONS.md first) and retake A and B; if that fails too,
  stop: fx13 is dropped. Never "it always works when unticked".
- C1: the second cup's top also chains (a tolerance surprise): log; F6 shows what the dialog lights, F8 build 3 is cut
  and the Short's S2 question changes (not a stop).
- C2: the side pick (Q3b) does not light all five, or builds: log; the question card changes (not a stop).
- R1 rules, unexpected dialogs, max 2 fix attempts per step: as LAB-fx6.

## 7. Filming on the Ubuntu box (local-zc), as fx11/fx12 (HANDOVER-fx11-lab.md, HANDOVER-fx12-lab.md in ../2026-11-fixit-4)
- Box 192.168.1.156, user aiagent1, key ~/.ssh/ubuntu_lab_ed25519 (keep key AND password login); docker group;
  image `sc5-l5:0.28.0` already loaded (ID into env.txt).
- Job dir ~/jobs/fx13 with copies of the lab repo's `lab/`, `checker/` and `client/` (scp from the PC); scripts
  lab/fx13lib.sh (GUI positions at UI scale 1.8, 2880x1620, from lab/fx12lib.sh), lab/fx13P.sh, fx13A.sh, fx13B.sh,
  fx13C.sh, fx13D.sh; box helpers ~/jobs/fx13/sm.sh, sheet.sh (as fx10, not in the repo).
- **Screen positions probed once, then reused** (the fx12 lesson: its probe container fx12p found every GUI path once,
  s0-s24, and lab/fx12lib.sh reused them): one probe container fx13p finds the Shell menu, the Tangent Chain checkbox,
  the thickness field, OK/Cancel, the top/side face click points on the cup at the take camera, Measure, Properties
  and the section view, writes them to the end of lab/fx13lib.sh, and is then stopped and removed. Positions already
  in lab/fx12lib.sh/fx14lib.sh (Browser, Properties) are reused, not re-probed. Re-probe only a dialog whose
  screenshot differs (logged in DEVIATIONS.md).
- No host ffmpeg: recording (x11grab 30 fps + cursor log), clip cuts, stills and contact sheets use the ffmpeg inside
  the container; all takes `--network none`.
- Results `scp` back into solidcraft-course-lab out/fx13/; footage.py zoom passes and renders run on the PC; clips
  script lab/fx13clips.py from each take's events.jsonl (as lab/fx12clips.py, test first). Commit locally only
  (prereg, P + scripts, takes + answers); never push. Marker out/fx13/fx13-lab.DONE. No fx13 containers left on the
  box.
- R1 runs on the PC only (section 4).

## 8. Deliverables
out/fx13/env.txt, PREREG.txt, P/* (cups.py, volumes.txt), {A,B,C,D}/events.txt + screen.mp4 + screenshots,
D/reply.txt, runs/R1/*, ANSWERS.md (Q1-Q7, Q3b, Q15), DEVIATIONS.md; RESULTS-fx13.md in this folder;
HANDOVER-fx13-lab.md.
