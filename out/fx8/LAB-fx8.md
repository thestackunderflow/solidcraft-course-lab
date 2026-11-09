# LAB-fx8: SolidCraft Can't Edit Your STL? Convert Mesh: "not a supported constant-section prism" — pre-registration v2, 2026-11-04 (before any run)

Lab repo: solidcraft-course-lab. Folder: out/fx8/ (takes P, A, B, C, D; run runs/R1). v2 applies DECISIONS round 1
(A7: stop rule B2 and the "mesh conversion:" prefix; T8: the other reasons are description only). Committed before
the first container starts (hash into out/fx8/PREREG.txt); `| tee` on every command; deviations in
out/fx8/DEVIATIONS.md; nothing re-scored.

## 0. Pins
As LAB-fx6 section 0, word for word: `sc5-app:0.28.0` built from docker/app.Dockerfile with `SC_VER=0.28.0
SC_OLD=0.27.1` (tarball checked against SHA256SUMS.txt), run image `sc5-l5:0.28.0`, `/opt/solidcraft/bin/solidcraft
--version` = 0.28.0 written to out/fx8/env.txt with the image ID, Claude Code 2.1.311, takes `--network none`, R1 only
with network. Stop rule P0 as LAB-fx6.

## 1. Questions (PLAN §0.4): Q9, Q10, Q11, Q12, Q13.

## 2. Common to every take
As LAB-fx6 section 2: Xvfb 1920x1080, **full-window recording** of the whole display (TAKE/screen.mp4, x11grab 30 fps
+ cursor log), events.txt as they happen, every take opens on the full SolidCraft window held 3 s, every line the
viewer must read held 4 s still.

## 3. Takes, in run order

### Take P: prepare the STLs (not filmed)
1. Lesson 3's hook (HOOK recipe) saved as ~/hook-l3.sc; Save As Mesh, STL, standard quality: ~/hook-plain.stl.
2. Lesson 4's hook (two 2 mm top fillets, two screw holes; the lab's lesson-4 no-AI build) saved; Save As Mesh STL:
   ~/hook.stl (the "downloaded" file in the video).
3. A 40 x 40 x 20 box with all four vertical edges filleted 5 mm: ~/box-round.stl (Q11).
4. Triangle counts of the three files (`python3 -I` reading the binary STL header) to P/counts.txt; note the
   exporter's quality setting in P/settings.txt.

### Take A: the refusals on a mesh (F0, F1, F4)
Fresh design; open ~/hook.stl (record the menu item text). Full window 3 s; the Browser row of the mesh body (icon,
name) held 4 s.
1. Sketch a 5 mm circle on the back plate's face (if the GUI lets you sketch on a mesh face; if not, on the XZ plane
   at the plate) and Extrude cut through. Event `cut on mesh: "message"`; A/cut.png.
2. Fillet one edge of the mesh (or try to select one). Event `fillet on mesh: "message"`; A/fillet.png.
3. Measure the mesh body: size and volume (A/measure.png; values into events).
4. Right-click the mesh body, Convert Mesh (record the item text and dialog fields with defaults, A/convert-dialog.png).
   Event `convert hook.stl: refused "full line as shown"` or `converted`; A/convert.png (expected to start
   "mesh conversion: "); Report draft title if offered (not submitted).

### Take B: the plain hook converts, then a hole (F2 left, F5 build 2 reference, F6; Short S0, S1)
1. Fresh design; open ~/hook-plain.stl; Convert Mesh. Event `convert hook-plain: converted` / refused; B/converted.png;
   the timeline after it (B/timeline.png, held 4 s).
2. Measure volume. Then a 5 mm through Hole in the back plate as a normal Hole feature, from the back plate's face.
   Event `hole on converted: built` / `refused "message"`; B/hole.png; the timeline (converted feature, then hole);
   Measure the hole diameter and the volume after.
3. Only if step 2 is refused (stop rule B2): the same Hole on a fixed plane at the back plate (Create Sketch with the
   fixed-plane control, then Hole / Extrude cut); event `hole on fixed plane: built` / `refused "message"`.
4. Only if 3 is refused too: edit one size of the converted feature (if it offers one; record which); event and
   B/size-edit.png.

### Take C: side by side and the question (F2 right, S0, S2)
1. Both STLs open in one design side by side (offset one by 40 mm); Convert Mesh on each in turn, the same camera:
   C/both.png. The S0 and F2 shot.
2. Q11 (pinned comment only): Convert Mesh on ~/box-round.stl; event and C/box.png. Also film the end frame of S2 on
   it (5 s hold, no Convert).

### Take D: MCP, no AI (F8 left)
The no-AI client (out/fx8/D/noai.py, the lesson-7 pattern) calls the MCP `open` tool on ~/hook.stl, then `execute`
mesh.convert on the body; `python3 -I out/fx8/D/noai.py |& tee D/reply.txt`. Film the terminal full window.
Expected: opened as a mesh body; the B.7 reason with the "mesh conversion: " prefix.

### R1: section 4.

## 4. The Claude run R1 (pre-registered)
Prompt, first and only message: `Open hook.stl and drill a 5 mm hole through the back plate.`
State: SolidCraft open on an empty design; ~/hook.stl present; MCP connected as lesson 7; auto mode.
Classes (reply.txt + tools.txt + the timeline and Measure of every body after the run, after.png):
- A: says the file is a mesh that cannot be drilled (and/or that conversion was refused) and offers to redraw it or
  asks; no false claim.
- B: redraws a new solid and drills it, and says so (record its size and volume against take A's Measure).
- C: says a hole was drilled into the STL / mesh (after.png decides).
- D: anything else; recorded; F8 rewritten at the script gate.
Evidence frame: take A's refusals, the Measure of the mesh body, and the timeline after the run. One run, no retry.

## 5. Measurements table
| value | used in | how | expected | source |
|---|---|---|---|---|
| refusal for a cut on a mesh | F1 | A step 1 | "... needs a solid body; mesh bodies can only be moved, measured and exported" | ACCURACY B.11 |
| refusal for a fillet on a mesh | F4 | A step 2 | "there is no solid body to modify (mesh bodies have no edges)" | B.11 |
| Measure on a mesh body | F4 | A step 3 | about 25 x 20 x 60; volume: measure | — |
| Convert hook.stl, full line | F0, F2, S0 | A step 4 | refused, "mesh conversion: this mesh is not a supported constant-section prism; no geometry was converted" | B.7, B.14 |
| Convert hook-plain.stl | F2, F6, S0 | B step 1 | converted, a timeline feature | B.10 |
| Hole on the converted body | F6 | B steps 2-4 | built, 5 mm | measure |
| triangle counts | description | P/counts.txt | all under 50,000 | B.9 |
| box-round | pinned comment | C step 2 | measure | — |
| MCP open + convert reply | F8 | D | mesh body; B.7 text | B.12, B.7 |
| R1 class, cost | F8 | section 4 | measure | — |

## 6. Stop rules
- P0: as LAB-fx6.
- A1: hook.stl CONVERTS: the contrast fails; try once with a hook that has only the holes (no fillets); if it still
  converts, stop; report (fx8 is re-planned around a real freeform part at the next gate).
- A2: the mesh refusals differ from B.11: type them verbatim; continue; the script quotes the screen.
- A3: SolidCraft cannot open an STL into a design under Xvfb: open it through the MCP `open` tool from the no-AI
  client, then film in the GUI (logged as "opened by the lab script").
- B1: hook-plain.stl is refused: try fine quality once; if still refused, stop; report (F2 and F6 depend on it).
- B2: the Hole on the converted body is refused: type the message, retry once on a fixed plane (B step 3); F6 says
  which one worked. If neither works, F6 becomes "edit a size of the converted feature" (B step 4) and the script gate
  re-checks F6, F7 and the subscribe timing; if no size can be edited either, F6 shows the converted timeline only.
- R1 rules, unexpected dialogs, max 2 fix attempts per step: as LAB-fx6.

## 7. Deliverables
out/fx8/env.txt, PREREG.txt, P/counts.txt, P/settings.txt, {A,B,C,D}/events.txt + screen.mp4 + screenshots,
D/reply.txt, runs/R1/*, ANSWERS.md (Q9-Q13).
