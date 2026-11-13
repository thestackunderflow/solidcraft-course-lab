# fx14b lab: deviations from LAB-fx14b.md v1.1 (pre-registration 516404a)

Nothing was re-scored or re-rolled. Every take ran once and is kept; one blocked step (the Hole's OK) got its second
attempt as take C2 (item 6).

1. **Where / image.** All containers on the Ubuntu lab box (~/jobs/fx14b), image sc5-l5:0.28.0, box image ID
   38a6f6787dc1 (not the PC's 2992c9ecbca2; as fx11-fx14); version line "solidcraft 0.28.0" (P0 ok). All `--network none`.
2. **Take P.** The first P run sourced a lab/fx14blib.sh whose last function (bodies) had lost its closing brace (bash
   reported "unexpected end of file" after setup); P uses none of the lost lines and every volume check passed. The lib
   was fixed before the probe. offset.sc's faces are named F2:top#1 (bottom, z 5) and F2:top#2 (top, z 25), exact true
   (logged only).
3. **Probe.** The probe container fx14bp ran twice (restarted once for conv30.sc's and offset.sc's positions), stopped
   and removed both times. To find positions it drove, on scratch copies, a fixed-plane cut (23,607.37 mm3, top face
   1,122.03 mm2), a Hole with the default Drill Point Angle 118 deg (23,528.73 mm3), the History icons' Edit Feature
   (nothing opened), and an Extrude on the converted top up to the preview (no line before OK; OK not pressed). Those
   probe results are not scored; the takes are. Probe shots kept in out/fx14b/probe/.
4. **Take B.** Properties before the cut was added at the start (F5 shows "before and after"). The Extrude dialog's
   default direction is out of the top face: Reverse was ticked so the 5 mm cut goes into the block.
5. **Take C, Hole.** The Hole dialog's Drill Point defaults to **Angle, Tip Angle 118 deg**; LAB says "Simple, Ø10,
   depth 5" with an expected 23,607.30, i.e. a flat bottom. The take holds the default on screen (C/hole-angle.png),
   then sets Drill Point **Flat** on camera. With the default tip the probe measured 23,528.73 mm3 (item 3).
6. **Take C -> C2 (blocked step, attempt 2).** With Drill Point Flat the Tip Angle row disappears and the dialog's OK
   moves up (1388 729 -> 1388 710 halved). Take C's OK click missed; no Hole was built (C/read-c-after-hole: 24,000.0,
   timeline conv, ConvertMesh1); the later Properties click landed on the still-open dialog (Face "2 selected"). Take C
   step 2 (Q26, your turn) is valid and kept. Take C2 (lab/fx14bC2.sh) = take C step 1 again with only the OK
   position changed: built. Clips for the Hole come from C2, the your-turn clips from C.
7. **Cancel.** With the red line showing, the Create Sketch dialog's Cancel is at 1322 554 (halved); G0's "sketch
   Cancel 1180 90" is the Sketch tab's ribbon Cancel inside an open sketch (used for Q21 and Q28).
8. **Q25 path.** The History bar tooltips say "Double-click to edit"; take E double-clicked ConvertMesh1, then used
   right-click > Edit Feature on both icons (conv = the Insert Mesh step, MeshFeature; ConvertMesh1,
   MeshConvertFeature). The Browser's Features folder (conv:1 > Features: "conv", "ConvertMesh1") was opened in take A.
   Menu names also read from Search commands: "mesh" (E/search.png).
9. **Numbers.** Properties/measure give 23,607.37 (not 23,607.30) and 8,607.37 (not 8,607.30); top face 1,122.03 mm2
   (not 1,121.46): all within 0.1% (0.0003%, 0.0008%, 0.05%), recorded as shown.
10. **Raw video.** A, B, C, E screen.mp4 are over 50 MB and gitignored (as fx13); C2 and D are committed.
11. **R1 path.** Predicted: the face pick gets the lineage line, then fixed:true or solid.hole. Filmed: Claude's
   `sketch.create {plane: {face: [20, 15, 20], body: "conv"}}` (in a batch) was refused earlier, isError "invalid
   parameters for `sketch.create`: an exact face pick requires both body and index"; it then gave the plane itself
   (origin [0, 0, 20], x/y directions) and cut -5. The lineage line never appeared; no Hole, no fixed:true. Class A as
   pre-registered. Checker lab/fx14bhole.py is new (tests/test_fx14bhole.py, 4 pass). session.jsonl: 5 lines of
   built-in skill/tool description text redacted to stubs (connector grep then zero). Footage: mask only Claude Code's
   greyed suggested prompt "take a screenshot".
