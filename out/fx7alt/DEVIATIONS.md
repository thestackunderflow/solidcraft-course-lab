# fx7alt lab: deviations from LAB-fx7alt.md v1 (pre-registration commit 9346c4a), 6 Nov 2026 (UTC times)

- 12:2x Display 2880x1620 (16:9), SolidCraft at UI scale 1.8, not 1920x1080 as section 2 says: the fx6/fx8 convention
  (the same frame at 1.5x, sharp under the zoom). Layout as pre-registered: SolidCraft the top pane (2880 x 1134, 70%),
  the terminal running noai.py a strip below (2880 x 486, xterm + tmux, DejaVu Sans Mono 22, white).
- 12:2x Probe before the takes (not filmed, not scored; out/scratch/fx7p, gitignored): GUI positions (Fillet dialog,
  edge, view home, middle-drag orbit), the tool list, one corner call, one window Fillet click on the [10, 20, 20] edge
  and where the sent point is stored (SolidCraft's recovery journal, ~/.local/share/solidcraft/recovery/*.sc, a zip
  whose document.json keeps each feature's `edges`), and the QA6 cut set-up (no fillet tried on it). The probe's
  window click counts as finding the path for QA4 ("at most 2 tries to find it"); take D then used journal.py on its
  first try.
- 12:32 Take A's first start (A-start0.log): the lab helper had Windows line endings after an edit, so the container's
  shell failed before SolidCraft started; nothing was recorded and no call was sent. Line endings fixed, take A started
  again (A.log). Not a retry of a call.
- Take A order: the fresh box is sent by noai.py BEFORE the recording (cleared from the terminal), the recording opens
  on typing the corner call (filming rule: A and B start typing at once), and the 8 s orbit (step 1, F1 source) comes
  AFTER the call and the 5 s hold, ending on the home view. The pre-registration lists the orbit first.
- Fresh box: `noai.py box` = new_design + solid.box 20 x 20 x 20 (a new document each time), as section 2 allows. Every
  call is preceded by `volume before` (noai.py's own measure) and followed by `volume after`.
- Take D: "Fresh box in the window (no script)" read as: the box is sent by noai.py before the recording; on camera
  there is no script until the journal is shown.
- Take E (rule E1 applies): `tools/list` has NO solid.fillet entry. SolidCraft's MCP tools are generic (list_commands,
  describe_command, execute, ...); the fillet's parameter docs (the "edges: [[x,y,z] point on edge | {body, index}]"
  line) come from `list_commands` (filter "solid.fillet"), the catalog tool the tool list points to. Take E films
  tools/list (19 tool names) then the list_commands entry. "fillet edges line" is quoted from list_commands.
  Also seen in tools/list: the `execute` description's example `solid.fillet {edges: [[0,0,10]], radius: 3}` and the
  `body_topology` description "Use an edge midpoint as the [x,y,z] point that picks the edge for fillet and chamfer".
- Take F, QA6 set-up: the box's side round cut is sent over the plug (solid.cylinder radius 5, height 20, base
  [20, 0, 10], axis Y, operation cut: a half-round groove along the x = 20 face), then Fillet by clicking in the window.
  #11516 does the cut in the window; only the fillet click is the window case under test.
- R1 budget: LAB-fx7alt states none; the cap is the set's R1 cap ($0.80, as fx6 and fx8), ledger
  fixit-fx7alt-BUDGET.tsv.
- R1 layout: Claude Code full screen (pre-registered); SolidCraft is behind it during the recording and is raised
  after the recording stops for after.png (home view) and after-2.png (turned).
- 12:40 Take F QA6: the script's condition for a second try was written backwards (it would have tried again only if
  the first click was REFUSED); try 1 built, so only one try ran. Pre-registered "at most 2 tries": within the limit,
  but the second edge (the groove's straight edge) was not tried. Recorded as "not reproduced in 1 try".
- Summary events typed after a take from its screenshots (B which edge, C both ends, A window line, F summaries) carry
  the time they were written and say so; all other events were written as they happened.
- count.txt: the version field of each report was not parsed (shown "?"); the count and N per report are from the
  bodies.
- R1: `claude mcp list` also shows the signed-in account's claude.ai connectors (two remote servers) beside solidcraft;
  Claude used none of them. The run ended on Claude's question (AskUserQuestion) with no answer (one message, as
  pre-registered); /cost was read after Esc closed the question ($0.0761).
- R1 redaction: organizationUuid and the e-mail in session.jsonl replaced by "[redacted]" / "[email redacted]"
  (scrub.py does paths only).
