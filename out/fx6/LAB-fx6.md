# LAB-fx6: SolidCraft Fillet: "the blend is larger than the neighbouring faces"? Smaller Radius — pre-registration v2, 2026-11-04 (before any run)

Lab repo: solidcraft-course-lab. Folder: out/fx6/ (takes A, B, C, C2, D; run runs/R1). v2 applies DECISIONS round 1
(A2/P1: Take C is thickness 8, C2 the bottom-back edge; A3; SHOULD 2, 3). Committed before the first container starts
(commit hash into out/fx6/PREREG.txt). Every command captures output with `| tee`; deviations go to
out/fx6/DEVIATIONS.md with the time; nothing is re-scored afterwards.

## 0. Pins (exactly as solidcraft-course-lab uses SolidCraft 0.28.0)
- App image `sc5-app:0.28.0` (local ID 55ad2987ef14 on 4 Nov), built by
  `docker build -t sc5-app:0.28.0 --build-arg SC_VER=0.28.0 --build-arg SC_OLD=0.27.1 -f docker/app.Dockerfile docker`
  (the release tarball is checked against the release's SHA256SUMS.txt inside the build).
- Run image `sc5-l5:0.28.0` (local ID 2992c9ecbca2): `/opt/solidcraft-0.28.0` copied from the app image and linked to
  `/opt/solidcraft`, Xvfb, xdotool, ffmpeg, Claude Code 2.1.311 (`CLAUDE_VER` in docker/l5.Dockerfile).
- Check at run start, into out/fx6/env.txt: `/opt/solidcraft/bin/solidcraft --version` (must print 0.28.0),
  `claude --version`, `docker image inspect --format '{{.Id}}' sc5-l5:0.28.0`. Wrong version: stop (rule P0).
- Takes run with `--network none` (`docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work"
  sc5-l5:0.28.0 bash /work/lab/fx6X.sh`, as lab/fx2E.sh). Only R1 has network (the Claude API), as lesson 7.
- Model: claude-sonnet-5-5 expected, read from session.jsonl after R1.

## 1. Questions (PLAN §0.4): Q1-Q5, Q13.

## 2. Common to every take
- Xvfb display 1920x1080; fresh home; SolidCraft 0.28.0 started as in lesson 5.
- **Full-window recording**: the whole display from before the first action to after the last
  (TAKE/screen.mp4, ffmpeg x11grab 30 fps + cursor log, lab/l2common.sh). Never a window crop at record time.
- events written as they happen to TAKE/events.txt (`HH:MM:SS.s  event`); xdotool at a person's pace (type delay
  80 ms, 1 s pause before each click).
- **Filming rule (owner, 4 Nov):** every take opens on the full SolidCraft window held 3 s with the cursor still;
  footage.py later adds the locator box, then the zoom. Every number the viewer must read (radius box, Parameters
  row, reason line) is held 4 s still so the zoom has a clean source.
- Start file: lesson 3's hook rebuilt by the no-AI recipe (`HOOK` in lab/l7story.py), saved as ~/hook-l3.sc; Measure
  the lip's top face once off-camera: event `lip top face: N mm` (expected 5).

## 3. Takes, in run order

### Take A: the refusal (F0, F1, F4, F5; Short S0)
1. Full window 3 s. Parameters panel open: hold 4 s on `thickness 5`.
2. Select the lip's outer top edge (between the lip's top face, x 20..25, and its outer front face, x = 25). Fillet.
   Radius 6. OK.
3. Event `fillet 6: refused`. Screenshots A/refusal.png (at once) and A/refusal-5s.png (+5 s). Type the line(s)
   verbatim into events (`line 1: "..."`, `reason: "..."`) and `shown in: dialog / banner / timeline mark / Browser row`.
4. If a Report button is offered: click it, A/report.png, `report title: "..."`. Do NOT submit; close the draft.
5. If the timeline / Browser row carries a mark: hover, A/mark.png.
6. Undo / cancel so the hook is unchanged. Hold 5 s.

### Take B: the limit (F2, F6; Short S1)
Same edge. Radii in this order: 4.0, 4.9, 5.0, 5.1 (each: type, hold 4 s on the box, OK, event `fillet R: built` or
`fillet R: refused "reason"`, B/r-R.png, undo if built). 5.0 may be degenerate (the round eats the whole top face):
record what happens, do not interpret. If 4.0 is refused: halve towards 0.1 mm until one builds, then search up in
0.1 mm steps; at most 12 tries. B/limit.txt: `largest built: R1; smallest refused: R2; lip top face: N mm`. Then film
F2 cleanly: full window 3 s, Fillet at the largest built radius, OK, hold 5 s on the round.

### Take C: the contrast, one variable changed (F7, F8; Short S1)
1. Parameters: thickness 5 to 8 (hold 4 s on the row). Event `thickness 8: rebuilt`; Measure the lip's top face
   (expected 8, x 17..25) and the lip's front face (expected 10); events `lip top face: N`, `lip front: N`. Log the
   J's base (expected 2 mm = lip_height - thickness), not narrated.
2. Same edge, Fillet 6, OK. Event `thick-8 fillet 6: built` / `refused "reason"`; C/thick8.png; hold 5 s. Undo.
3. Thickness back to 5. For the split screen, film steps 1-2 once more in one clean pass if step 2 built.
4. Q4 (NOT filmed for the video): both lip top edges in one Fillet at 2.5 on thickness 5; event `both 2.5: built` /
   `refused "reason"`; C/both-2.5.png; also 2.4 if 2.5 is refused. (A default-branch fixture refuses two 2.5 mm
   chamfers on a 5 mm face; the fillet answer may differ; record only.)

### Take C2: the fallback contrast edge (F7 only if Take C step 2 is refused)
Thickness 5. Select the outer bottom-back edge (x = 0, z = 0, along the 20 mm width): faces = back face (60 mm
across) and underside (25 mm across). Fillet 6, OK. Event `bottom-back 6: built` / `refused "reason"`; C2/edge.png;
Measure both faces (events). Always filmed (cheap), used only by stop rule C1.

### Take D: the same call over MCP, no AI (F9 left; Q5)
SolidCraft open on ~/hook-l3.sc; the lab's no-AI MCP client (lesson-7 `lab/l7story.py` Story pattern, copied to
out/fx6/D/noai.py) sends `solid.fillet` with the lip edge given by its MIDPOINT (x = 25, z = 10, halfway along the 20 mm
width in sketch terms; the XZ sketch is flipped in x, so the script reads the edge from the body and prints the
world point it used) and radius 6; `python3 -I out/fx6/D/noai.py |& tee D/reply.txt`. Then the same with
the edge given by a CORNER point (for fx7-alt, Q5). Film the terminal full window (three-line crop later). Also
D/count.txt: the take-day `gh api search/issues ... --jq .total_count` for "FILLET: operation failed" (run on the host).

### R1: the Claude run, section 4.

## 4. The Claude run R1 (pre-registered)
Prompt, the first and only message: `Round the outer top edge of the hook's lip with a 6 mm fillet.`
State: fresh home; SolidCraft open on ~/hook-l3.sc (thickness 5, saved); MCP server connected as lesson 7
(`claude mcp list | tee runs/R1/mcp-list.txt` shows it before the prompt); auto mode as lesson 7.
Capture: reply.png (greyed suggested prompt cropped later, crop.txt), reply.txt (typed from the screen), tools.txt
(tool calls from session.jsonl), the hook after the run (after.png, Measure on the lip if changed), cost.txt.
Classes (scored on reply.txt + tools.txt + after.png only):
- A: a 6 mm fillet is tried, the refusal and its reason are reported, and a radius under the lip's width is proposed
  or asked about (applied only if it says so).
- B: a smaller radius is applied and the reply does not say the 6 mm round was refused.
- C: the reply says a 6 mm round was made (after.png decides "does not match").
- D: anything else; reply recorded; F9 rewritten at the script gate.
Also recorded (not scored): how R1 named the edge, and any "where N edges meet" reply.
Evidence frame: take B's limit table and after.png. One run, no retry.

## 5. Measurements table
| value | used in | how | expected | source |
|---|---|---|---|---|
| line(s) on screen at 6 mm | F0, F4, S0, title | A events | "not supported yet: the blend is larger than the neighbouring faces" (or the ball sibling: title B) | ACCURACY B.1, B.2, B.15 |
| where it is shown | F0 | A `shown in:` | measure | — |
| report draft title | F5 | A report.png | "FILLET: operation failed" | A.1 |
| lip top face width | F1, F3, F6 | Measure | 5 mm | HOOK |
| largest built / smallest refused | F2, F6, S1, thumbnail | B/limit.txt | just under 5 | C.1 |
| thickness 8: lip faces, fillet 6 | F7, F8, S1 | C | 8 and 10 mm; built | C.6 |
| bottom-back edge at 6 | F7 fallback | C2 | built; 60 and 25 mm | review A2 |
| both lip edges at 2.5 | pinned comment | C step 4 | measure | — |
| MCP reply fields | F9 | D/reply.txt | ok false + reason | measure |
| corner-point reply | PLAN §4 (fx7-alt) | D | "... is where N edges meet ..." | A.3 |
| take-day count | F5 card | D/count.txt | over 300 | A.2 |
| R1 class, cost, model | F9 | section 4 | measure | — |

## 6. Stop rules
- P0: `solidcraft --version` is not 0.28.0, or the image ID differs from section 0: stop, report.
- A1: the 6 mm lip fillet BUILDS: stop; the premise fails on 0.28.0; report.
- A2: the reason is neither B.1 nor B.2: continue, type it verbatim; the title changes to the words on screen at the
  script gate.
- B1: no radius between 0.1 and 6 builds on the lip edge: stop; report.
- C1: the thickness-8 round is refused: record the reason; F7/F8/S1 use Take C2 (if C2 builds) with its measured face
  widths; if C2 is refused too, stop and report (the rule as taught does not hold; no other edge is substituted).
- D1: the no-AI client cannot reach the MCP server: fix as lesson 7 did, max 2 attempts, then F9's left pane uses
  R1's tool reply from session.jsonl and says so.
- R1-1: server not connected: fix off-camera before typing. R1-2: no reply within 10 minutes: stopped run, report.
- Any dialog whose text differs from an EXPECTED quote: screenshot, type it, continue with the default button, flag.
- Anything else unexpected: stop the take, DEVIATIONS.md, report; no improvised route; at most 2 fix attempts per step.

## 7. Deliverables
out/fx6/env.txt, PREREG.txt, {A,B,C,C2,D}/events.txt + screen.mp4 + the screenshots named above, B/limit.txt,
D/reply.txt, D/count.txt, runs/R1/*, ANSWERS.md with one line per question (Q1-Q5, Q13).
