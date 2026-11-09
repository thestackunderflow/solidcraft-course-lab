# fx9 lab answers (PLAN §0.4 Q1-Q7, Q13), SolidCraft 0.28.0, 7 Nov 2026 (UTC)

Pre-registration 862eb44 (PREREG.txt). Pins: env.txt (solidcraft 0.28.0, Claude Code 2.1.311, image sha256:2992c9ec...).
Nut (take P): hexagon 13.00 mm across flats (y), 15.01 across corners (x), 7 mm tall, body "Nut"; hole 8 through:
672.70 mm3; hole 6.75: 774.06 mm3 (P/volume.txt).

- **Q1 (line, where, draft title):** live, under the Thread dialog's fields, the moment Modeled is ticked (Size 8 mm
  already set), with OK greyed: "this 8 mm hole is too wide for a modelled M8 thread: it would cut 0.00 mm of the
  thread's 0.68 mm depth; drill 6.75 mm for M8, or thread this hole M10" (A/refusal.png). **No "Thread:" prefix on
  screen** (the dialog line starts with "this"; no toast). Create Issue... draft Summary: "THREAD: operation failed"
  (A/report.png; closed, not submitted). Clicking the greyed OK does nothing: no Thread feature is added, the timeline
  stays Sketch1/Extrude1/Hole1 (A/after-ok.png, read-a-after-ok). Stop rule A1 did not fire.
- **Q2 (Automatic size):** on picking the hole wall ("Nut · face 7") the dialog pre-fills Automatic size ticked, Size
  10 mm, Pitch 1.5 mm, Designation M10, Modeled off, Full Length on, Right-hand (A/dialog.png). Before the pick:
  Automatic size ticked (greyed), Size "Select size", Designation hint "fits the face, e.g. M8" (probe). Menu path:
  Model tab > Create menu > Thread.
- **Q3 (M10 on the same 8 mm hole, Modeled):** refused, live: "this 8 mm hole is too narrow for a modelled M10 thread
  (its teeth would fill the hole); drill 8.5 mm for M10" (A/m10.png). As B.5.
- **Q4 (the fix):** Hole1 edited to 6.75 in the timeline (774.06 mm3), Thread M8 Modeled: **built**, OK enabled, no
  line; Thread1 in the timeline; volume 733.54 mm3 (plug and Inspect > Properties, which also shows 1864 faces).
  For the 6.75 hole the dialog's own pre-fill is already M8. Bore's smallest diameter 6.738 mm, largest 8.00 (STL
  vertex method, off camera; the unthreaded 6.75 bore gives exactly 6.75 by the same method; DEVIATIONS 4). Section:
  Inspect > Section, plane XZ (B/section.png, teeth.png, teeth-low.png).
- **Q5 (window, M8):** 6.3 refused "this 6.3 mm hole is too narrow for a modelled M8 thread (its teeth would fill the
  hole); drill 6.75 mm for M8"; 6.5 built (737.94 mm3); 7.6 built (700.03 mm3); 7.7 refused "this 7.7 mm hole is too
  wide for a modelled M8 thread: it would cut 0.15 mm of the thread's 0.68 mm depth; drill 6.75 mm for M8, or thread
  this hole M10". Matches B.7; no other line appeared (C1 not fired). vs 6.75: -0.45, -0.25, +0.85, +0.95.
- **Q6 (tapped hole):** Edit Hole > Hole Tap Type: Tapped, Profile ISO metric, Size M8: "Tap drill diameter 6.75 mm"
  (C/tapdrill.png); OK: the hole is 6.75 (774.06 mm3); then Thread M8 Modeled: **built** (733.54 mm3, the same as B).
- **Q7 (MCP, no AI):** `execute` solid.thread {"face": [4, 0, 3.5], "designation": "M8", "modeled": true}: isError
  true, one text item, word for word the Q1 line (no prefix) (D/reply.txt, rpc.jsonl). Nothing changed (672.70).
- **Q13 (R1):** class **A** (RESULTS-fx9.md). One message, one try; Claude got the refusal, said so, changed Hole1 to
  6.75 (timeline.edit) and built a modelled M8 thread (Thread1, 733.54 mm3). Two statements for the script gate: it
  called 6.75 "the standard M8 drill size", and it offered "keep the 8 mm hole ... threaded as M10 instead", which
  SolidCraft refuses (Q3). Greyed suggested prompt after the reply: "save the design" (crop it). Cost $0.2472.
