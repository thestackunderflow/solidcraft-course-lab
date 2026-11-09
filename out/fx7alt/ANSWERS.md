# fx7alt lab answers (LAB-fx7alt v1, prereg 9346c4a; SolidCraft 0.28.0, sc5-l5:0.28.0 2992c9ecbca2; 6 Nov 2026)

- QA1 (take A): REFUSED, as E.1/E.2 word for word: `isError: true`, text "invalid parameters for `solid.fillet`: [20, 20, 20]
  is where 3 edges meet: give a point along one edge, such as its midpoint" (numbers print "20", count 3). Window toast
  "Fillet: [20, 20, 20] is where 3 edges meet: give a point along one edge, such as its midpoint" (E.3). Volume 8000 before
  and after. Axes: Z up; 0,0,0 the left bottom corner in the home view, 20,20,20 the right top corner; the [10,20,20] edge
  is the top edge at the back right. Stop rules A1/A2/V1: not triggered.
- QA2 (take B): [10, 20, 20] BUILT (Fillet1), the top edge at the back right (y 20, z 20) rounds, as the axes event
  predicts; volume 7961.35.
- QA3 (take C): [20, 20, 5] BUILT; the WHOLE upright edge (x 20, y 20) rounds, both ends (C/after.png + after-2.png);
  volume 7961.35, the same as the 20 mm top edge in B. C1 not triggered: F5 "any point inside one edge" and "the round
  runs its whole length" hold.
- QA4 (take D): window click on the same top edge, radius 3, OK: BUILT (7961.35). The point the dialog sent, from
  SolidCraft's session journal (recovery document.json, journal.py, D/log.png): edges [[10.0, 20.0, 20.0]] = the edge's
  middle (edge F1:+y|F1:+z). D1 not triggered: F6 "the log shows it" holds (the "log" is the session journal).
- QA5 (take F): [20, 20, 19] BUILT, the upright edge (7961.35), as ACCURACY E.13 expected. F1 not triggered.
- QA6 (take F): NOT REPRODUCED in 1 try (a side half-round cut, then Fillet by clicking its curved edge: built, 7214.75 ->
  7180.30, no line). The second try was not run (script fault, DEVIATIONS).
- QA7 (take F): chamfer at [20, 20, 20] REFUSED with the same line naming `solid.chamfer`: "invalid parameters for
  `solid.chamfer`: [20, 20, 20] is where 3 edges meet: give a point along one edge, such as its midpoint"; 8000 kept.
- QA8 (take E, rule E1): `tools/list` (19 tools) has NO solid.fillet entry and no "point on edge" text; the fillet's
  parameter docs come from the `list_commands` tool (filter solid.fillet): edges line "edges: [[x,y,z] point on edge |
  {body, index}]". tools/list itself does say, in `body_topology`: "Use an edge midpoint as the [x,y,z] point that picks
  the edge for fillet and chamfer". Index route (one try): body_topology lists 12 edges with index + midpoint; the
  [10, 20, 20] edge is {"body": "Body1", "index": 10}. F7 must say "the command list" / quote list_commands, not
  "the tool list".
- QA9 (R1): class A. Claude (claude-sonnet-5-5, Claude Code 2.1.311) made one SolidCraft call (inspect_design), sent no
  point, and asked: "Three edges of the box meet at the corner (20,20,20). Which one should get the 3 mm fillet?" with
  the three edges listed by their two ends (plus "All three edges"). Box unchanged (8000), no claim of a fillet. No
  "edges meet" reply was triggered. Cost $0.0761 (/cost). The run ends on the open question (one message, no answer).
- Take-day count (count.txt): 13 of the newest 100 FILLET reports carry "is where N edges meet" (N = 2 in 9, 4 in 3,
  3 in 1); total FILLET reports 342.
