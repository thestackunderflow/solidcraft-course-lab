# fx11 lab answers (PLAN §0.4 Q1-Q7, Q5b; Q15 = R1 on the PC), 12-13 Nov 2026 UTC

SolidCraft 0.28.0 in `sc5-l5:0.28.0` on the Ubuntu lab box, `--network none`, UI scale 1.8, 2880 x 1620, 30 fps.
Pre-registration e482bd4 (LAB-fx11.md v1). Deviations: DEVIATIONS.md (7 items, none changes a result). No stop rule
fired (P0 no, A1 no, A2 no, B1 no). **The premise holds.** No AI in this stage: R1 (Q15) deferred to the PC.

**Take P.** ~/tower.sc, ~/tower-sym.sc: 113,479.66 mm3 each after save + reopen (expected 113,490.03: 0.009% lower,
within the 0.1% rule; SolidCraft's figure, narrate the measured one). tower z 0..200, tower-sym z -100..100. ~/block.sc
32,000.00 mm3, 20 x 20 x 80. The body is named **Tower** in the Browser (Bodies > Tower).

**Q1, the refusal (take A).** Menu path: Model tab > Modify (dropdown) > Bodies > **Split Body**. Dialog: two fields,
"Body to split" (Select, focused) and "Splitting tool" (Select); Cancel, OK greyed (A/dialog.png). Body: clicked the
Tower row in the Browser (the field reads "Tower", focus moves to Splitting tool); tool: Browser > Origin > XY (reads
"XY"). At once, live (no OK needed), under the fields in red: `the tool does not split the body`, a "Create Issue..."
button, OK greyed (A/refusal.png). **No "Split Body:" prefix in the dialog.** Report draft Summary:
`SPLIT BODY: operation failed` (A/report.png; Close draft, not submitted). Cancel: nothing enters the timeline
(Sketch1, Extrude1, Sketch2, Extrude2 only). XY can be lit: clicking its Browser row highlights the row; in the view
only the small origin plane glyph at the tower's foot turns blue (A/origin.png). F1 section: Inspect > Section, Plane
XZ: the tower cut in half lengthwise (A/section.png); from the home view the cut face and the 5 mm floor are hard to see.

**Q2, the fix (take B).** Model > Construct > **Offset Plane**: fields "Plane" (Select), "Through point" (Select),
"Distance" (0 mm), OK blue (B/offset.png). Plane = XY (Browser), Distance typed `100 mm`: a preview square at mid
height with an on-canvas "Distance 100 mm" tag (B/offset-preview.png); OK: **Plane1** in a new Browser folder
"Construction". Split Body, Tower, Plane1: no error, OK enabled, preview shows the cut ring; OK: Browser header
"2 bodies", rows **Tower** and **Tower (1)**; timeline adds Split1. Properties (right-click the row > Properties;
Inspect > Properties with nothing picked shows the whole design instead):
- Tower = the TOP piece: **54,972.98 mm3**, bounding box 40.00 x 40.00 x 100.00 mm (z 100..200), mass 70.915 g, 4 faces.
- Tower (1) = the BOTTOM piece: **58,506.68 mm3**, 40.00 x 40.00 x 100.00 mm (z 0..100), 75.474 g, 5 faces.
- Sum 113,479.66 = the whole tower's 113,479.66 (difference 0.00): they add up. (Expected 54,977.87 / 58,512.16:
  both 0.009% lower, the same scale as the whole.) Note: the new name "(1)" goes to the bottom piece, not the top.
F11: each piece hidden in turn with its Browser eye (no new geometry; B/hide-row1.png shows the bottom piece alone).

**Q3, Midplane (B-q3, logged only).** Model > Construct (dropdown) > Midplane: fields "First plane", "Second plane".
XY (Browser) + the top face clicked in the view ("Tower - face 4"): OK enabled; Plane1 made; Split with it: the same
two bodies, 54,972.98 (z 100..200) and 58,506.68 (z 0..100). Same split, same numbers. The base face itself could not
be clicked from this view, so XY (its plane) stood in (DEVIATIONS 4). Offset Plane stays F2's default.

**Q4, plane above the part (take C).** Offset Plane 210 from XY, Split: **refused, the same line**, OK greyed
(C/above.png). Cancel: timeline gains only Plane1.

**Q5, the Symmetric tower (take C).** ~/tower-sym.sc, Split with XY: no error, OK; 2 bodies: Tower 54,972.98 mm3
(z 0..100), Tower (1) 58,506.68 mm3 (z -100..0), each 40 x 40 x 100 (C/sym.png, sym-props-row1/2.png).

**Q5b, the your-turn block (take C).** ~/block.sc, Offset Plane 40, Split: 2 bodies, Block (z 40..80) and Block (1)
(z 0..40), **16,000.00 mm3 each**, Properties 20.00 x 20.00 x 40.00 mm (C/block-props-row1/2.png). The teacher's
"20 x 20 x 80 = 16,000 mm3 per half" is **confirmed**.

**Q6, at the top face (take C, pinned comment).** Offset Plane 200 (exactly the top face): Split **refused, the same
line** (C/at200.png). The top face itself as the tool ("Tower - face 4", planes hidden first): **refused, the same
line** (C/topface.png). S2 end frame: C/s2-frame.png (the tower, Plane1 at 210 and Plane2 at 200 both drawn at the top).

**Q7, MCP no AI (take D).** `execute solid.split_body {"body": "Tower", "plane": "XY"}`: isError true, the only text
`the tool does not split the body` (no prefix). The window shows a toast **with** the prefix: `Split Body: the tool
does not split the body` (D/reply.png). Timeline unchanged after.

**Q15 (R1).** Run on the PC 13 Nov (DEVIATIONS 8). **Class A**, $0.1440 (claude-sonnet-5-5, Claude Code 2.1.311). Claude
never tried XY: from inspect_design it said "the XY plane at the origin only touches its bottom face" and split with a
plane parallel to XY at z = 100, saying so. Two bodies: Tower (1) bottom 58,506.68, Tower top 54,972.98 mm3 = take B
exactly; sum 113,479.66. Not saved. It guessed the bore was "a pocket near z = 200" (it runs to z = 5). runs/R1/tools.txt.
