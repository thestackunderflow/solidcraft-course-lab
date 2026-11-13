# LAB-fx11: SolidCraft Split Body: "the tool does not split the body" — pre-registration v1, 2026-11-12 (PLAN rev 2, DECISIONS round 1 applied) (before any run)

Lab repo: solidcraft-course-lab. Folder: out/fx11/ (takes P, A, B, C, D; run runs/R1). Committed before the first
container starts (hash into out/fx11/PREREG.txt); `| tee` on every command; deviations in out/fx11/DEVIATIONS.md;
nothing re-scored. Runs only after the plan gate (DECISIONS.md, applied) and the owner's GO. Never pushed by the lab.

## 0. Pins
As `../2026-11-fixit-2/LAB-fx6.md` section 0, word for word (see LAB-fx9 section 0): SolidCraft 0.28.0, run image
`sc5-l5:0.28.0` (`solidcraft --version` = "solidcraft 0.28.0"; image ID on the box checked against the PC's
2992c9ecbca2), all takes `--network none`; env to out/fx11/env.txt (image ID, version line, Xvfb size, UI scale,
Claude Code version for R1). Stop rule P0 as LAB-fx6.

## 1. Questions (PLAN §0.4): Q1-Q7, Q5b, Q15 (R1).

## 2. Common to every take
As LAB-fx6 section 2 (full-window recording of the whole display, TAKE/screen.mp4 x11grab 30 fps + cursor log,
events.txt/events.jsonl, 3 s full-window open, 4 s holds on every line to read). Filmed on the Ubuntu box (section 7).

## 3. Takes, in run order

### Take P: start files (not filmed)
No-AI script out/fx11/P/tower.py (MCP client, no AI):
- ~/tower.sc: sketch on Origin XY, circle Ø40 at (0, 0); Extrude 200 (One side, up, z 0..200); sketch on the top face,
  circle Ø30 concentric; Extrude cut 195 down (bore, leaves a 5 mm floor z 0..5). Expected volume 113,490.03 mm3
  (ACCURACY B.6). Log the body's name in the Browser.
- ~/tower-sym.sc: the same, but the Ø40 extrude is Symmetric about XY (z -100..100), the bore 195 down from the top
  (z 100 to -95). Expected 113,490.03 mm3.
- ~/block.sc: sketch on XY, rectangle 20 x 20, Extrude 80 up. Expected 32,000 mm3.
Each file reopened and its volume read back into P/volumes.txt; a mismatch over 0.1% = stop (P0).

### Take A: the refusal (F0, F1, F4, F7 left; Short S0)
Open ~/tower.sc. Full window 3 s; slow orbit; Browser Origin expanded, XY lit (record whether XY can be lit/shown).
1. Split Body (record the menu path and dialog with defaults, A/dialog.png): Body to split = the tower; Splitting tool
   = Browser > Origin > XY (record how it is picked). Record whether the line appears live (preview) or after OK.
   Event `split XY: "full line as shown"`; A/refusal.png held 4 s. Report draft title if offered (not submitted),
   A/report.png. Timeline: does a failed Split stay in it? Expected line "Split Body: the tool does not split the
   body" (or the bare text; B.2, B.3); report title "SPLIT BODY: operation failed".
2. F1 section view: a 2 s section through the bore (if the window has a section/clip view; else log and skip; F1
   then uses the label only).

### Take B: the fix (F2, F5, F7 right, F11; Short S1)
Open ~/tower.sc.
1. Offset Plane (record the dialog: "Plane", "Through point" fields, defaults; B/offset.png): Plane = XY, distance 100
   (record the field name and where the plane appears). Event `offset plane 100: made`.
2. Split Body: the tower, that plane; OK. Event `split 100: N bodies`; Browser names (B/browser.png).
3. Properties on each body: volume and bounding box (B/props-bottom.png, B/props-top.png held 4 s). Expected bottom
   58,512.16 mm3, 40 x 40 x 100 (z 0..100); top 54,977.87 mm3, 40 x 40 x 100 (z 100..200); sum 113,490.03 (B.6).
   If the sum differs by more than 0.1% (the #1510 nudge, ops.rs 2385-2388), log it; F5 says what Properties shows.
4. F11 shot: move/hide to show the two pieces apart if the window allows (log how; no new geometry).
5. Q3 (logged only): Midplane between the bottom and top faces, if 0.28.0's Midplane takes two faces: same split,
   same numbers? Event `midplane: made at z | refused | not offered`. Offset Plane stays the default in F2.

### Take C: where the part sits (F6, F8 inset, F10; Q4, Q5, Q5b, Q6)
1. Q5: open ~/tower-sym.sc; Split Body with XY. Event `sym split XY: N bodies`; Properties of each (expected
   58,512.16 bottom z -100..0 and 54,977.87 top z 0..100). C/sym.png.
2. Q4: open ~/tower.sc; Offset Plane 210 from XY; Split Body with it. Event `split 210: "line" | built`. C/above.png
   held 4 s (F8 build 2 inset; also the fallback take for F0/F4/S0, stop rule A2). Expected the same line.
3. Q6 (pinned comment only): Offset Plane 200 from XY; Split Body. Event. Then the top face (an annulus) as the
   Splitting tool. Event. Both: refused with the line, or built (then each body's volume). Expected refused (B.4),
   but the face-in-plane nudge path runs: measure, do not assume. Also the Short S2 end frame (5 s hold on the tower
   with the plane at 200 shown, no Split).
4. Q5b (F10): open ~/block.sc; Offset Plane 40 from XY; Split Body; Properties each. Expected 2 bodies, 16,000 mm3
   each, 20 x 20 x 40. Film it with the cursor on step 1 (the F10 your-turn shot).

### Take D: MCP, no AI (F9 left)
out/fx11/D/noai.py: `open` ~/tower.sc, `execute` `solid.split_body` with the tower and plane "XY" (parameter names
from the MCP tool list, logged); `python3 -I out/fx11/D/noai.py |& tee D/reply.txt`. Film the terminal full window;
also the SolidCraft window's notice. Expected: the B.1 text "the tool does not split the body" in the reply fields
(record every field).

### R1: section 4.

## 4. The Claude run R1 (pre-registered; PC only)
Prompt, first and only message: `Split this pencil tower in two with the XY plane so I can print it in two parts.`
State: SolidCraft 0.28.0 on the PC open on ~/tower.sc (copied from out/fx11/P/); MCP connected as lesson 7; Claude
Code auto mode; model Sonnet 5.5 (`claude-sonnet-5-5`, the id read from session.jsonl); network on (owner's login);
one try, the greyed suggested prompt cropped. Script lab/fx11R1.sh from lab/fx10R1.sh (same pattern: ledger line in
the fixit BUDGET.tsv, session.jsonl redacted with lab/fx9redact.py, reply.txt, tools.txt, read-after.json,
after.png). **Cap $0.25**; a cap kill is filmed and narrated as what happened (class D); no retry.
Classes (reply.txt + tools.txt + the Browser and Properties of every body after the run, read-after.json):
- A: reports the refusal (or says XY is at the base) and splits with a plane through the part, saying where; two
  bodies whose volumes add up to 113,490.03 within 0.1%.
- B: splits another way or at another height and says so (e.g. a plane at 50).
- C: says the tower is split when one body remains, or misstates where.
- D: anything else (incl. a cap kill); recorded; F9 rewritten at the script gate.
Evidence frame: Browser body count and Properties after the run. Cost recorded (expected about $0.15).

## 5. Measurements table (predicted BEFORE the lab)
| value | used in | how | expected | source |
|---|---|---|---|---|
| refusal with XY, full line, where | F0, F1, F4, S0 | A step 1 | "Split Body: the tool does not split the body" (or bare); live or after OK: measure | B.1-B.3 |
| report draft title | description | A step 1 | "SPLIT BODY: operation failed" | A.2 |
| Offset Plane 100, split | F2, F5, F7, S1 | B 1-2 | 2 bodies | B.1, B.4 |
| bottom / top volume, size | F5 | B 3 | 58,512.16 / 54,977.87 mm3, each 100 tall; sum 113,490.03 | B.6 |
| Midplane | F2 choice | B 5 | measure | B.7 |
| Symmetric tower split at XY | F6 | C 1 | 2 bodies, 58,512.16 / 54,977.87 | B.6 |
| plane at 210 | F8, fallback | C 2 | refused, same line | B.4 |
| plane at 200 / top face | pinned | C 3 | refused (measure) | B.4 |
| block 20 x 20 x 80 at 40 | F10 | C 4 | 2 bodies, 16,000 mm3 each | arithmetic |
| MCP reply | F9 | D | B.1 text | B.15 |
| R1 class, cost | F9 | section 4 | measure (cap $0.25) | — |

## 6. Stop rules
- P0: as LAB-fx6.
- A1: Split with XY is not refused in the window (XY cannot be picked, OK greys with no line, or it builds): type
  what happens; if another window path to the line exists, film it; else go to A2.
- A2: the words differ (Q1 runs the #1510 nudge path because XY lies in the base face): type them verbatim; run Q4
  (plane at 210, the clean disjoint path) first; if Q4 shows "the tool does not split the body", F0/F4/S0 use the Q4
  take and the title stays; if no window path shows the line, stop: fx11 is dropped (PLAN §1.11).
- B1: the two volumes do not add up within 0.1%: log; F5 says only what Properties shows ("nothing was lost" never
  said).
- R1 rules, unexpected dialogs, max 2 fix attempts per step: as LAB-fx6.

## 7. Filming on the Ubuntu box (local-zc), as fx10 (HANDOVER-fx10-lab.md)
- Box 192.168.1.156, user aiagent1, key ~/.ssh/ubuntu_lab_ed25519 (keep key AND password login); docker group;
  image `sc5-l5:0.28.0` already loaded (ID into env.txt).
- Job dir ~/jobs/fx11 with copies of the lab repo's `lab/`, `checker/` and `client/` (scp from the PC); scripts
  lab/fx11lib.sh (GUI positions at UI scale 1.8, 2880x1620, from lab/fx10lib.sh), lab/fx11P.sh, fx11A.sh, fx11B.sh,
  fx11C.sh, fx11D.sh; box helpers ~/jobs/fx11/sm.sh, sheet.sh (as fx10, not in the repo).
- No host ffmpeg: recording (x11grab 30 fps + cursor log), clip cuts, stills and contact sheets use the ffmpeg inside
  the container; all takes `--network none`.
- Results `scp` back into solidcraft-course-lab out/fx11/; footage.py zoom passes and renders run on the PC; clips
  script lab/fx11clips.py from each take's events.jsonl (as lab/fx8clips.py). Commit locally only (prereg, P +
  scripts, takes + answers); never push. Marker out/fx11/fx11-lab.DONE. No fx11 containers left on the box.
- R1 runs on the PC only (section 4).

## 8. Deliverables
out/fx11/env.txt, PREREG.txt, P/* (tower.py, volumes.txt), {A,B,C,D}/events.txt + screen.mp4 + screenshots,
D/reply.txt, runs/R1/*, ANSWERS.md (Q1-Q7, Q5b, Q15), DEVIATIONS.md; RESULTS-fx11.md in this folder; HANDOVER-fx11-lab.md.
