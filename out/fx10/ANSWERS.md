# fx10 lab answers (PLAN §0.4 Q8-Q12, Q13), 12 Nov 2026 UTC

SolidCraft 0.28.0 in `sc5-l5:0.28.0` on the Ubuntu lab box, `--network none`, UI scale 1.8, 2880 x 1620. Pre-registration
bdc85c2 (LAB-fx10.md v2). Deviations: DEVIATIONS.md (12 items, none changes a result). No stop rule fired (A1 no;
A2 yes for the prefix only; C1 no).

**Q8, the refusal (take A).** Model > Create > Revolve on ~/knob-full.sc: the dialog opens with Profile "1 selected"
(the T, picked automatically), Axis "Select", Type Angle, Direction One Side, Angle 360 deg, Operation New Body
(A/dialog.png). Axis = Browser > Origin > Z. At once, under the fields, in red:
`invalid input: the profile crosses the revolve axis`, OK greyed, a "Create Issue..." button (A/refusal.png). **No
"Revolve:" prefix in the dialog.** Report draft Summary: `REVOLVE: operation failed` (A/report.png; closed, not
submitted). Angle 180 deg: the same line, OK greyed (A/refusal-180.png; B.14 holds). Cancel: timeline Sketch1 only.
When the same revolve is sent over MCP (take D) the window shows a toast **with** the prefix:
`Revolve: invalid input: the profile crosses the revolve axis` (D/reply.png).

**Q9, the fix (take B).** In Sketch1 the five lines left of or across the axis deleted, the outline closed along the
axis with one Line chain (stem corner -> origin -> (0, 23) -> cap corner); Finish; Revolve 360 about Z: no error,
built (Revolve1). Measure on the cap's top edge: **Ø 30.00 mm** (R 15.00, circumference 94.25). Properties: **volume
7,350.78 mm3**, bounding box 30.00 x 30.00 x 23.00 mm, mass 9.483 g, 5 faces (B/measure.png, B/props.png). Plug read
7,350.775708796922, the same as take P's plug-built half. (pi x 2,340 = 7,351.33; SolidCraft's figure is 0.55 mm3
lower; narrate the measured 7,350.78 or "about 7,350".)

**Q10, the endless line (take C).** The Revolve window takes a sketch line as the axis: clicking the dashed
construction line fills Axis with `l1`. C1, rectangle x 2..8, z 2..8 beside the line: built (preview, then OK:
1,130.93 mm3, a ring). C2, rectangle x -3..3, z 20..26, past the line's drawn end (the line runs z 0..10) but
straddling its extension: **refused**, the same line, OK greyed (C/c2.png). The axis is treated as endless in the
window: F6 and peg 2 stand.

**Q11, a normal line through the T (take A, logged only).** A Line drawn on the axis from the stem's end to the cap's
end splits the T into two regions (Profile picks "2 selected"; Axis = that line, `l9`): **refused**, the same line
(A/split.png). F7 must not say "a line through the middle fixes it".

**Q12, the question's answer (take C).** A square x 5..15, z 0..10, Revolve 360 about Z: built, **a ring with a hole**:
Measure outer edge Ø 30.00 mm, inner edge Ø 10.00 mm; volume 6,283.02 mm3 (pi x 2,000 = 6,283.19) (C/ring.png,
C/ring-outer.png, C/ring-inner.png, C/ring-props.png). The S2 end frame (the square alone, 5 s) is C/s2-frame.png.

**MCP, no AI (take D).** `execute solid.revolve {"axis": "Z", "angle": "360 deg"}` on ~/knob-full.sc: `isError: true`,
text word for word `invalid input: the profile crosses the revolve axis` (no prefix), timeline unchanged (D/reply.txt).
Parameter names from list_commands (D/revolve-cmd.txt): `axis` (sketch line id | x | y | X|Y|Z | ...), `angle?`.

**Q13, the Claude run R1: class A** (run on the PC 12 Nov, same image tag sc5-l5:0.28.0, Claude Code 2.1.311,
claude-sonnet-5-5; one message, one try; runs/R1/tools.txt). Claude tried solid.revolve about the sketch's y axis at
180 deg (its own choice), got "invalid input: the profile crosses the revolve axis", said so in the reply, redrew the
right half (x >= 0) as a new closed sketch Sketch2 on XZ, revolved it 360 deg: timeline Sketch1, Sketch2, Knob (one
Revolve); Body1 30 across (x/y -15..15), 23 tall, 7,350.78 mm3 = take B. Sketch1 untouched (said). Its words: "The
knob is built, but not by revolving your sketch directly" ... "Instead I redrew one half of the profile". Statements
checked: stem radius 6 x 15, flange radius 15 x 8, "z = 0 to -23", "about 7351 mm3": all hold. Greyed suggested
prompt: "Flip it so the stem points up from z = 0" (crop it). Cost $0.1411 (ledger fixit-fx10-BUDGET.tsv, cap $0.50).
