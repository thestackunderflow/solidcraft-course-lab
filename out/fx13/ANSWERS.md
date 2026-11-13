# fx13 lab answers (LAB-fx13 v1, prereg 0c8e59e), 13 Nov 2026, Ubuntu box, SolidCraft 0.28.0, no AI, $0

Strings are copied from the screenshots (the app log does not carry them) and the plug's reply text.

| Q | Pre-registered | Filmed | Where |
|---|---|---|---|
| Q1 menu, defaults | Tangent Chain ticked; thickness: measure | Model tab > Modify > **Shell** (ribbon button; also Modify > Bodies > Shell). Dialog: Faces/Body "Select", Thickness **2 mm**, Direction **Inside**, OPTIONS > checkbox **"Tangent chain"** (lower-case c) **ticked** | A/dialog.png |
| Q1 preview, top pick, chain on | all 5 faces lit | the whole body lit; Faces/Body **"8 selected"** (the plug lists 8 faces: top, bottom, the side as two halves, 4 round pieces; P/faces-cup.json) | A/preview.png |
| Q1 line | B.1 text, maybe "Shell:" prefix; live or after OK | live in the dialog, red, under the checkbox, OK greyed, no prefix: **"Tangent Chain opens every face of this body, leaving no walls; turn off Tangent Chain to remove only the picked faces"** + button "Create Issue..." | A/refusal.png, A/hold.png |
| Q1 report draft | "SHELL: operation failed" | Summary **"SHELL: operation failed"** (draft only, not submitted) | A/report.png |
| Q1 failed Shell in the timeline? | measure | no: after Cancel the timeline is Sketch1, Extrude1, Fillet1; volume unchanged 226,012.52 | A/read-a-after-cancel.txt |
| Q3b side pick, chain on | all 5 lit, same line | **"8 selected"**, the same line, word for word | A/side.png |
| Q2 chain off, top, 2 mm | built, 33,900.00 mm3 | unticked: **"1 selected"**, only the top lit, OK enabled; built (Shell1); Properties **33899.75 mm3** (plug 33,899.754), 7 faces / 6 edges / 6 vertices, box 60 x 60 x 80 | B/untick.png, B/preview.png, B/props.png |
| Q7 wall / floor | 2.00 / 2.00 | wall: Measure on the outer and inner side faces: Item 1 D 60.00, Item 2 D 56.00, "Center to center 0.00 mm", **Min 2.00 mm**, Max 97.60 mm. Floor: inner floor (Area 2458.10 mm2) to the outer bottom (Area 2546.68 mm2, picked after the gizmo's -Z view): **Distance 2.00 mm**, dZ 2.00 | B/wall.png, B/floor.png |
| inner bottom corner | sharp (logged) | not judged from the frames; cavity by the plug's numbers 226,012.52 - 33,899.75 = 192,112.77 (sharp analytic 192,114.67) | B/section.png |
| Q3 second cup, chain ON | top only, built, 33,990.00 | **"1 selected"**, only the top lit with the chain ON; built; Properties **33989.77 mm3**, 6/5/5 | C/preview-bottom.png, C/props-bottom.png |
| Q5 your-turn cup | 11,532.86 | chain off, top, 2 mm: built; Properties **11532.79 mm3**, 7/6/6, box 40 x 40 x 40 | C/props-40.png |
| Q4 rounds 3, chain off | refused, rim line (maybe "Shell:") | NOT live: OK enabled before OK; **after OK** the dialog stays open with: **"not supported yet: the rim would have no thickness: an open face meets a round of radius 3.0000 mm tangentially, and the shell is 2.0000 mm thick (make the round smaller than the thickness)"** + Create Issue...; no Shell1, volume unchanged 225,477.37 | C/r3.png, C/after-ok-r3.png, C/read-c-r3.txt |
| Q6 MCP chain true / unset | B.1 text / built 33,900.00 | call 1 `isError: true`, reply text = the B.1 line, bare (no prefix); call 2 (no `tangent_chain`) built Shell1, measure 33,899.754: the plug defaults the chain OFF. No window notice seen in D/reply.png | D/reply.txt, D/events.txt, D/read-d-after.txt |
| Q15 R1 | class A or B | not run (PC only; this stage is no-AI) | - |

Second cause (#8536, every face of a plain cylinder picked, no rounds): not a take in LAB-fx13 v1, so not run.
