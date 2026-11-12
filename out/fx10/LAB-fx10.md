# LAB-fx10: SolidCraft Revolve: "the profile crosses the revolve axis" — pre-registration v2, 2026-11-06 (DECISIONS round 1 applied) (before any run)

Lab repo: solidcraft-course-lab. Folder: out/fx10/ (takes P, A, B, C, D; run runs/R1). Committed before the first
container starts (hash into out/fx10/PREREG.txt); `| tee` on every command; deviations in out/fx10/DEVIATIONS.md;
nothing re-scored. Runs only after the plan gate GO (DECISIONS.md) and the owner's GO.

## 0. Pins
As `../2026-11-fixit-2/LAB-fx6.md` section 0, word for word (see LAB-fx9 section 0); env to out/fx10/env.txt.

## 1. Questions (PLAN §0.4): Q8-Q12, Q13.

## 2. Common to every take
As LAB-fx6 section 2 (full-window recording, events.txt, 3 s full-window open, 4 s holds on every line to read).

## 3. Takes, in run order

### Take P: the knob sketches (not filmed)
No-AI script (out/fx10/P/knob.py): on the XZ plane (record which origin axis is vertical in the window), one closed
polyline, the full T silhouette centred on the vertical axis: cap 30 wide (x -15..15) x 8 tall (z 15..23), stem 12
wide (x -6..6) x 15 tall (z 0..15). Save ~/knob-full.sc (sketch only, not revolved). A copy with only x 0..15 / 0..6
(the half, touching the axis): ~/knob-half.sc. Expected volume after a 360 revolve: 7,351 mm3 (ACCURACY B.13).

### Take A: the refusal (F0, F1, F4; Short S0)
Open ~/knob-full.sc. Full window 3 s; the sketch with the axis through its middle held 4 s.
1. Revolve (record the menu path and dialog fields with defaults, A/dialog.png); profile = the T region; axis = the
   vertical origin axis (record how it is picked); angle 360; OK. Event `revolve full: "full line as shown"`;
   A/refusal.png; Report draft title if offered (not submitted). Expected "invalid input: the profile crosses the
   revolve axis", prefixed "Revolve:".
2. The same at 180 degrees (ACCURACY B.14). Event.
3. Q11 (logged only): a normal (not construction) line drawn on the axis through the T; Revolve with both resulting
   regions picked and that line as axis. Expected REFUSED with the same line (touching regions are merged back into
   one T: profiles.rs 1801). Event `split T: built | refused "line"`; volume if built.

### Take B: the fix (F2, F5, F7; Short S1)
1. Open ~/knob-full.sc; in the sketch select the left half's lines and delete them; close the outline along the axis
   and constrain/snap that edge onto the axis (log whether it is constrained; within 1e-7 counts as on the axis) (record each step; if the GUI cannot do it in under 2 fix attempts, open ~/knob-half.sc and log it).
2. Revolve 360 about the same axis. Event `revolve half: built | refused`; B/knob.png.
3. Measure: cap diameter (expected 30), height (23), volume (expected 7,351). B/measure.png held 4 s.

### Take C: the endless line (F6) and the question (Q12)
First confirm the Revolve window accepts a sketch line as the axis (AxisRef::SketchLine, eval.rs 4319-4327); if it
takes only origin axes, use a construction axis instead (same unbounded maths) and log it.
Fresh design, XZ sketch:
- C1: a construction line from (0, 0) to (0, 10) (the axis); a rectangle x 2..8, z 2..8 (beside it). Revolve about the
  line: event; C/c1.png.
- C2: the same line; a rectangle x -3..3, z 20..26 (above the line's drawn end, straddling its extension). Revolve
  about the line: event `C2: refused "line" | built`; C/c2.png. Expected refused (B.12).
- Q12 (pinned comment): a square x 5..15, z 0..10 about the vertical axis, 360: event, Measure (expected a ring with a
  10 mm hole, outer 30); C/ring.png; also the S2 end frame (5 s hold, no Revolve).

### Take D: MCP, no AI (F9 left)
out/fx10/D/noai.py: `open` ~/knob-full.sc, `execute` solid.revolve on its sketch with the vertical axis, angle 360
(parameter names from the MCP tool list, logged); `python3 -I out/fx10/D/noai.py |& tee D/reply.txt`. Film the
terminal full window. Expected: the B.10 line.

### R1: section 4.

## 4. The Claude run R1 (pre-registered)
Prompt, first and only message: `Revolve this sketch around the vertical axis to make the knob.`
State: SolidCraft open on ~/knob-full.sc; MCP connected as lesson 7; auto mode.
Classes (reply.txt + tools.txt + the timeline, the sketch and Measure of every body after the run, after.png):
- A: reports the refusal (or the crossing) and edits the sketch to one half, or redraws a half profile, saying so;
  the knob measures 30 across and within 1% of take B's volume.
- B: makes a knob another way (e.g. extrudes two cylinders) and says so; or a different size, said.
- C: says the knob is made when the timeline shows no revolved body, or a body whose size it misstates.
- D: anything else; recorded; F9 rewritten at the script gate.
Evidence frame: take C's endless-line takes and Measure after the run. One run, no retry. Cost recorded (expected
about $0.07, cap $0.50).

## 5. Measurements table
| value | used in | how | expected | source |
|---|---|---|---|---|
| refusal, full T, full line | F0, F4, S0 | A step 1 | "Revolve: invalid input: the profile crosses the revolve axis" | ACCURACY B.10 |
| 180 degrees | R1 judging | A step 2 | refused | B.14 |
| split T with a normal line | F7 wording | A step 3 | measure | — |
| half revolve, size, volume | F2, F5, F7, S1 | B | built, 30 across, 7,351 mm3 | B.13 |
| C1 / C2 | F6 | C | built / refused | B.12 |
| square off the axis | pinned | C Q12 | ring, outer 30, hole 10 | geometry |
| MCP reply | F9 | D | B.10 text | B.15 |
| R1 class, cost | F9 | section 4 | measure | — |

## 6. Stop rules
- P0: as LAB-fx6.
- A1: the full T is not refused in the window (Revolve greys out, picks only one region, or builds): type what
  happens; if a window path to the refusal exists (e.g. the origin axis via another control), film it; if none, stop;
  fx10 is dropped (PLAN §2.11).
- A2: the words differ: type them verbatim; the title follows the screen.
- C1: C2 builds (the axis is NOT endless in practice): F6 is rewritten without "endless" at the script gate; peg 2 is
  dropped.
- R1 rules, unexpected dialogs, max 2 fix attempts per step: as LAB-fx6.

## 7. Deliverables
out/fx10/env.txt, PREREG.txt, P/*, {A,B,C,D}/events.txt + screen.mp4 + screenshots, D/reply.txt, runs/R1/*,
ANSWERS.md (Q8-Q12, Q13).
