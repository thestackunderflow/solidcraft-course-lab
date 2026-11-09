# LAB-fx7alt: SolidCraft Fillet over MCP: "edges meet: give a point along one edge"? Name One Edge — pre-registration v1, 2026-11-04 (before any run)

Lab repo: solidcraft-course-lab. Folder: out/fx7alt/ (takes A, B, C, D, E, F; run runs/R1). Written from PLAN §4 rev 2
after fx7-alt gate round 1 (DECISIONS "fx7-alt gate round 1"). Committed before the first container starts (commit
hash into out/fx7alt/PREREG.txt). Every command captures output with `| tee`; deviations go to
out/fx7alt/DEVIATIONS.md with the time; nothing is re-scored afterwards.

## 0. Pins (exactly as LAB-fx6.md section 0)
- App image `sc5-app:0.28.0` (local ID 55ad2987ef14 on 4 Nov), built by
  `docker build -t sc5-app:0.28.0 --build-arg SC_VER=0.28.0 --build-arg SC_OLD=0.27.1 -f docker/app.Dockerfile docker`
  (the release tarball is checked against the release's SHA256SUMS.txt inside the build).
- Run image `sc5-l5:0.28.0` (local ID 2992c9ecbca2): Xvfb, xdotool, ffmpeg, Claude Code 2.1.311.
- Check at run start, into out/fx7alt/env.txt: `/opt/solidcraft/bin/solidcraft --version` (must print 0.28.0),
  `claude --version`, `docker image inspect --format '{{.Id}}' sc5-l5:0.28.0`. Wrong version: stop (rule P0).
- Takes run with `--network none` (`docker run --rm --memory 5g --shm-size 1g --network none -v "$PWD:/work"
  sc5-l5:0.28.0 bash /work/lab/fx7altX.sh`, as lab/fx2E.sh). Only R1 has network (the Claude API), as lesson 7.
- Model: claude-sonnet-5-5 expected, read from session.jsonl after R1.
- No-AI client: LAB-fx6 Take D's `noai.py` (lesson-7 Story pattern), copied to out/fx7alt/noai.py; it prints each
  request and the raw reply (JSON-RPC as received) to the terminal and to TAKE/rpc.jsonl.

## 1. Questions (PLAN §4.12): QA1-QA9.

## 2. Common to every take
- Xvfb display 1920x1080; fresh home; SolidCraft 0.28.0 started as in lesson 5, MCP server connected as lesson 7.
- **Fresh box rule (accuracy MUST-FIX 3):** every call in every take starts on a NEW 20 mm box: new document, then
  `solid.box` length 20, width 20, height 20 sent by noai.py (as #5173), or undo back to it. Before each call: Measure
  volume, event `volume before: N` (expected 8000). After: `volume after: N`. A box that is not 8000: stop (rule V1).
- **Full-window recording**: the whole display from before the first action to after the last (TAKE/screen.mp4,
  ffmpeg x11grab 30 fps + cursor log, lab/l2common.sh). Never a window crop at record time. Layout: the SolidCraft
  window is the larger pane (top, about 70% of the height), the terminal running noai.py a strip below it.
- **Filming rule (owner, 4 Nov; producer MUST-FIX 3):** takes A and B start typing at once (no hold); every other take
  opens on the full window held 3 s. footage.py later adds the locator box, then the zoom. Every reply line, point and
  number the viewer must read is held 4 s still so the zoom has a clean source.
- Events written as they happen to TAKE/events.txt (`HH:MM:SS.s  event`); xdotool at a person's pace (type delay 80
  ms, 1 s pause before each click).
- Axes, once, off-camera (QA1, teacher MUST-FIX 1): with the view cube or Measure, record `up axis: Z?`, `corner 0,0,0
  at: ...`, `corner 20,20,20 at: ...` (screen position), and which top edge contains [10, 20, 20] (`edge [10,20,20]:
  top, at the back/front/...` as it looks on screen). F1's tags are drawn only from these events.

## 3. Takes, in run order

### Take A: the corner refusal (F0, F1, F4, F5 left; Short S0; QA1)
1. Fresh box (volume event). Orbit once slowly (F1 source), 8 s.
2. noai.py sends `solid.fillet` `{"edges": [[20, 20, 20]], "radius": 3}`. Event `corner: refused` or `corner: built`.
3. Type the reply verbatim into events (`reply: "..."`), with its JSON fields (`isError`/`ok`, as received); expected
   "invalid parameters for `solid.fillet`: [20, 20, 20] is where 3 edges meet: give a point along one edge, such as
   its midpoint" (ACCURACY E.1-E.2; note how the numbers print: "20" or "20.0"). A/reply.png.
4. The window: status bar or toast line, if any, typed verbatim (`window line: "..."`, expected to start "Fillet: ",
   E.3); A/window.png. Volume after (expected 8000).
5. Hold 5 s.

### Take B: the midpoint (F2; Short S1; QA2)
Fresh box. noai.py sends `{"edges": [[10, 20, 20]], "radius": 3}`. Event `midpoint: built` / `refused "reply"`;
reply typed; B/after.png; which edge rounded (as seen, matches the axes event?); volume after. Hold 5 s on the round.

### Take C: any point inside one edge (F5 right; QA3)
Fresh box. `{"edges": [[20, 20, 5]], "radius": 3}`. Event `upright 5: built` / `refused "reply"`; C/after.png from
two angles (is the WHOLE upright edge rounded, both ends?); volume after. For the split screen F5, film A step 2 and
this call once more in one clean pass on two fresh boxes if needed.

### Take D: the window click (F6; QA4)
Fresh box in the window (no script). Full window 3 s. Fillet from the toolbar; click the same top edge as Take B
(hold 4 s on the dialog's edge row); radius 3; OK. Event `window click: built` / `refused "line"`. Then the point the
dialog sent: from the session journal or the app's command log (the path that lesson 7 used; at most 2 tries to
find it), typed into events `window sent: [x, y, z]` (expected the edge's middle by length, viewport.rs 2638) and a
crop D/log.png. If no log shows it: events `window sent: not visible`, and F6 drops "the log shows it" (rule D1).

### Take E: the tool list (F7; QA8)
noai.py lists the MCP tools (`tools/list`) and prints the `solid.fillet` entry; hold 4 s on its edges line. Type it
into events verbatim (`fillet edges line: "..."`, expected to contain "point on edge", E.16). Then one try at getting
an edge index for `{body, index}` (the tool that lists a body's edges, if the list has one): `index route: ...`.

### Take F: checks for the pinned comment and the description (not filmed for the video; QA5, QA6, QA7)
1. QA5, fresh box: `{"edges": [[20, 20, 19]], "radius": 3}`. **Expected before the run (ACCURACY E.13): built, the
   upright edge.** Event `upright 19: built` / `refused "reply"`; F/q5.png. Refused: stop rule F1.
2. QA7, fresh box: `solid.chamfer` `{"edges": [[20, 20, 20]], "distance": 2}`. Event and reply verbatim (expected the
   same line naming `solid.chamfer`).
3. QA6, the window, at most 2 tries: #11516's steps (a box, a round cut from its side with a cylinder or a Hole, then
   Fillet by clicking an edge of the cut). Event `window case: reproduced "line"` / `not reproduced`; F/q6.png. Record
   only; nothing here is narrated.

### R1: the Claude run, section 4.

## 4. The Claude run R1 (pre-registered)
Prompt, the first and only message: `Round the edge of the box that ends at the corner 20, 20, 20 with a 3 mm fillet.`
State: fresh home; SolidCraft open on a fresh 20 mm box (volume 8000), saved as ~/box20.sc; MCP server connected as
lesson 7 (`claude mcp list | tee runs/R1/mcp-list.txt` shows it before the prompt); auto mode as lesson 7.
**Filmed as a real terminal recording** (producer MUST-FIX 5): the Claude Code window full screen under Xvfb,
runs/R1/screen.mp4, from before the prompt to the final reply; no type-on.
Capture: reply.png (greyed suggested prompt cropped later, crop.txt), reply.txt (typed from the screen), tools.txt
(tool calls and their points from session.jsonl), the box after the run (after.png from two angles, volume), cost.txt.
Classes (scored on reply.txt + tools.txt + after.png only):
- A: the reply says three edges end at that corner and asks which, or names the one it rounded with the point it
  used (built only if it says so).
- B: one edge is rounded and the reply does not say there were three to choose from.
- C: the reply says an edge is rounded and the box is unchanged (volume 8000).
- D: anything else; reply recorded; F9 rewritten at the script gate.
Also recorded (not scored): every point R1 sent, and whether any call got "is where N edges meet".
Evidence frame: after.png and tools.txt. One run, no retry.

## 5. Measurements table
| value | used in | how | expected | source |
|---|---|---|---|---|
| axes and corner positions | F1, F2 tags | section 2 axes events | Z up; 0,0,0 and 20,20,20 opposite corners | E.12 |
| corner reply (MCP) | F0, F4, S0, title, desc line 1 | A events, rpc.jsonl | E.1/E.2 text with 3 | E.1, E.2, E.5 |
| window line for the same call | §4.1 (not narrated) | A step 4 | starts "Fillet: " | E.3 |
| volumes before/after | F5 left, every take | Measure | 8000 / 8000 on refusal | E.14 |
| midpoint call | F2, S1 | B | built, one top edge | E.12 |
| [20, 20, 5] | F5 right | C | built, whole upright edge | E.5, E.15 |
| window click and the point sent | F6 | D | built; the edge's middle | E.9 |
| tool list edges line | F7 | E | contains "point on edge" | E.16 |
| [20, 20, 19] | pinned comment | F1 | built, upright edge | E.13 |
| chamfer at the corner | description | F2 | same line, `solid.chamfer` | E.7 |
| window case (2 edges etc.) | description | F3 | measure | E.11 |
| take-day report count | F4 card (optional), desc | host: `gh api search/issues` FILLET newest 100, filter "edges meet" | about 1 in 10 | E.10 |
| R1 class, cost, model | F9 | section 4 | measure | — |

## 6. Stop rules
- P0: `solidcraft --version` is not 0.28.0, or the image ID differs from section 0: stop, report.
- V1: a fresh box does not measure 8000 mm3: stop, report (the recipe's coordinates would be wrong).
- A1: the corner call BUILDS: stop; the premise fails on 0.28.0; report.
- A2: the reply's words differ from E.1/E.2: continue, type them verbatim; title and F0/F4 change to the words on
  screen at the script gate. The count is not 3: stop and report (E.5 predicts 3).
- B1: the midpoint call is refused: stop; report (the fix as taught fails).
- C1: [20, 20, 5] is refused, or rounds only part of the edge: record; F5 drops "any point" and uses the midpoint
  only; the teacher's "the round runs its whole length" line is checked against C/after.png before it stays.
- D1: the window click is refused: record; F6 rewritten at the script gate; the sent point not visible: F6 drops "the
  log shows it".
- E1: the tool list's edges words differ: F7 quotes the words filmed. No edges line at all: F7 holds on Take A's
  reply with the pitch, its "help says point on edge" sentence is cut (source code is never shown as the app), and
  retime.py is re-run at the script gate.
- F1: [20, 20, 19] is refused: stop; re-read features.rs 1531-1546 before anything is written; the question changes
  at the script gate.
- D2: the no-AI client cannot reach the MCP server: fix as lesson 7 did, max 2 attempts, then stop (this video's
  main footage is the client; no substitute).
- R1-1: server not connected: fix off-camera before typing. R1-2: no reply within 10 minutes: stopped run, report.
- Any dialog whose text differs from an EXPECTED quote: screenshot, type it, continue with the default button, flag.
- Anything else unexpected: stop the take, DEVIATIONS.md, report; no improvised route; at most 2 fix attempts per step.

## 7. Deliverables
out/fx7alt/env.txt, PREREG.txt, noai.py, {A,B,C,D,E,F}/events.txt + screen.mp4 + rpc.jsonl + the screenshots named
above, runs/R1/*, count.txt, ANSWERS.md with one line per question (QA1-QA9).
