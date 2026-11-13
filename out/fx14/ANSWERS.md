# fx14 answers (LAB-fx14; G0 only: stop rule S1)

| Q | Question | Predicted | Measured |
|---|---|---|---|
| Q8 G0a | Align (0,0,0) -> (0,0,5), sketch on the top | attaches (lean) | **attaches**, client and window (exact_face) |
| Q8 G0b | Combine Join, merged coplanar top | refused with the line (moderate) | **attaches**, client and window; the merged top keeps the name F2:top |
| Q8 G0c | Shell 2, top open, sketch on the rim | refused, the line or another (low) | **attaches**, client and window; rim = F2:top, 264 mm2 |
| Q8 G0d | Save As Mesh, Insert Mesh, Convert Mesh, sketch on the top | refused with the line (highest) | **refused with ANOTHER line**: "Create Sketch: this face has no supported stable semantic lineage; choose a supported exact face or explicitly use fixed:true" (client: same after "invalid parameters for `sketch.create`: "); hint + Use fixed plane button shown; report draft "CREATE SKETCH: operation failed" |
| Q8 verdict | first passing rung | G0d most likely | **none: S1, fx14 dropped** |
| Q14 | face name before / after | measure | control F2:top exact; G0a F2:top -> F3:face:5, exact false on all six faces, still attaches; G0b F2:top kept; G0c F2:top kept (rim); G0d F4:face:5 exact false after Convert Mesh |
| Q9-Q13, Q11b, Q15 | takes P-E, R1 | — | not run (S1) |
