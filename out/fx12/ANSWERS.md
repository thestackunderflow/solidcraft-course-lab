# fx12 lab answers (PLAN §0.4 Q8-Q14; Q15 = R1 on the PC), 13 Nov 2026 UTC

SolidCraft 0.28.0 in `sc5-l5:0.28.0` on the Ubuntu lab box, `--network none`, UI scale 1.8, 2880 x 1620, 30 fps.
Pre-registration 0bd748b (LAB-fx12.md v1). Deviations: DEVIATIONS.md. No stop rule fired (P0, A1, A2, C1, C2 no).
**The premise holds.** No AI in this stage: R1 (Q15) deferred to the PC. $0 spent.

**Take P.** ~/tray.sc: outline l1-l4 (corners p1-p4), ONE Offset 2 mm inward (copy l5-l8, corners p5-p8, param d4 in
the sketch, 2.00 mm dimension shown); regions 384.0 + 2,016.0 after save + reopen (expected). ~/tray-plain.sc 2,400.0;
~/box.sc 1,500.0. The association is the constraint `offset_distance` (k11 in tray.sc); `links` stays [].

**Q8, the refusal (take A).** Menu: Sketch tab > Modify > **Fillet**. Dialog: "click sketch curves / 1 of 1: Select
Corners", field Corners, Radius (typed `3 mm`), Cancel, OK. Clicking the copy's top-right corner (p7) adds "p7" and at
once, live, under Radius in red (A/refusal.png):
`` `l6` is an offset, and its corners follow its source curves: round or cut the source corners before offsetting, or
break the offset association first `` + a "Create Issue..." button. **No "Fillet:" prefix in the dialog; the id shown
is l6** (p7 = the end of l6 / start of l7). Report draft Summary: `FILLET: operation failed` (A/report.png; Close
draft, not submitted). After Cancel the sketch is unchanged: l1-l8, offset constraint kept, regions 384 + 2,016 (B.11).
Sketch > Modify (dropdown) > **Equal Distance Chamfer** (Distance default 2 mm) on p7: the **same line**, same place
(A/chamfer.png). The sketch unchanged after.

**Q9, one Break frees all four (take B).** Click the copy's top line, right-click > **Break Offset Association**
(B/menu.png). After: no `offset_distance` constraint left on any copy line, DOF 2 -> 6, and the 2.00 mm offset
dimension disappears from the sketch (B/after-break.png). Yes, one click freed all four.
Fillet 3 on the four inner corners (p5, p8, p7, p6): **4 built, 0 refused** (arcs a1-a4 R3); ring 391.73 mm2.

**Volumes (Properties).** Fix 1 (break, inside R3, sharp outside): **7,834.61 mm3** (plug 7,834.6147; predicted
7,834.51, +0.0013%). Fix 2 (round 5 first, offset 2): **7,405.25 mm3** (plug 7,405.2523; predicted 7,405.31, -0.0008%).
Q12 (round 1.5, offset 2): **7,641.35 mm3** (plug 7,641.3463; predicted 7,641.37). All 60.00 x 40.00 x 20.00 mm.

**Q10, round first (take C).** Fillet the outline 5 (a1-a4 R5), Offset (Sketch > Modify > Offset; Direction, Distance
`2 mm`, Options: Flip off, Chain on) from the top line: the copy is l5, a5, l6, a6, l7, a7, l8, a8 (lines + four arcs
**R3**, the convex path), still linked (`offset_distance` k29, 2.00 mm dimension shown). Regions 370.27 + 2,008.27.
Measure the inside top-right arc: **R 3.00 mm** (Ø 6.00, arc length 4.71, angle 90.00°; C/measure.png).

**Q11, wall at the corner.** Fix 1 (B-wall/wall.png): outside corner (30, 20) to the inner R3 arc: **Min 4.07 mm**
(centre to centre 7.07, Max 5.39). Fix 2 (C/wall.png): outer R5 arc to inner R3 arc: **Min 2.00 mm** (centre to
centre 0.00, Max 5.83). Both as pre-registered.

**Q12, outline 1.5 then offset 2 (take C2).** Built, **SHARP inside corners**: the copy is four lines only
(l5-l8, the R1.5 arcs retired), linked (k29); regions 382.07 + 2,016.0. Not "the offset collapses an arc".
New: the right panel shows **"Untied 4" with a "Tie" button** after the offset (C2/copy.png).

**Q13, MCP no AI (take D).** `open` ~/tray.sc, `execute` sketch.edit Sketch1 (ok), `execute` sketch.fillet
{points: [p7], radius: 3}: isError true,
`` invalid parameters for `sketch.fillet`: `l6` is an offset, and its corners follow its source curves: round or cut
the source corners before offsetting, or break the offset association first `` (B.10 with the prefix). Sketch unchanged.

**Q14, width 60 -> 70 after round-first (C14, plug only, not filmed).** Attempt 1, a new 70 mm distance between l2 and
l4: refused "that would over-constrain the sketch (conflicts with k1, ...)". Attempt 2, the existing width dimension
d1 = 70 mm (set_parameter): **the copy follows**: the same ids l5..a8, arcs still R 3, linked (k29); regions 410.27 +
2,368.27 (= 66 x 36 - 9(4 - pi)).

**Q15 (R1).** Run on the PC 13 Nov (DEVIATIONS 9). **Class A**, $0.1761 (claude-sonnet-5-5, Claude Code 2.1.311).
Claude's first fillet on the copy got the line (MCP, curve `l5`), it then broke the association and filleted 3 mm, and
said so ("SolidCraft won't let you fillet an offset curve. I broke that link"), plus that the inner edges no longer
follow the outline. Result = Fix 1 exactly: four R 3.00, outline 60 x 40, regions 391.73 + 2,008.27, corner wall 4.07,
ring x 20 = 7,834.51 mm3 analytic. Not saved. runs/R1/tools.txt.
