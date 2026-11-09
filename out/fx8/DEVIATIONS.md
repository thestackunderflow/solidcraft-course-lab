# fx8 lab deviations (5 Nov 2026)

- Display 2880x1620 (16:9) with SolidCraft at UI scale 1.8 filling it, not 1920x1080 (as fx6: the same frame at 1.5x
  the pixels, so the full window is the whole frame and the zooms stay sharp). Positions came from a dry probe
  (out/scratch/fx8p, gitignored) on the same image; the probe also ran each GUI step once (nothing filmed or scored).
- Take P ran over the plug (lab/fx8part.py prep) with `file.save_mesh`, the command behind Save As Mesh. It has no
  quality option in 0.28.0 (P/settings.txt), so "standard quality" = the default; stop rule B1's "fine quality" retry
  does not exist (and was not needed).
- Stop rule A3: File > Open... and Insert > Insert Mesh (File menu item "Insert Mesh...") open no file window under
  Xvfb (no window is mapped). Every STL is opened by the lab script (`open` tool, lab/fx8part.py open) before the
  recording starts; events say "opened by the lab script".
- Convert Mesh is not in the Browser's or the 3D view's right-click menu: it is Surface tab > Convert panel > Convert
  Mesh (the command search says SURFACE > CONVERT). The takes use the toolbar button.
- Take A step 1: the 5 mm circle is sketched by the lab script before the recording (lab/fx8sketch.py: YZ plane offset
  5 = the back plate's inner face, centre y -10, z 30); Create Sketch can't pick a face of a mesh body (the click on the
  plate does nothing). Extrude, Cut, Reverse and OK are done in the GUI on camera.
- Take A extra step 1b (not pre-registered, recorded as evidence only): Hole on the mesh plate.
- Take A step 3: "Measure" = Inspect > Properties on the mesh body (it shows volume, area, bounding box and face count;
  the Measure tool measures between picks).
- Take C: the two STLs are inserted by the lab script (`file.insert_mesh`) into one new design and the drilled hook is
  moved 40 mm along +y (`solid.move`), before the recording.
- R1: the plug entry is `solidcraft-cli mcp setup`'s plus `--allow-path /root` (lesson 7's fix): without it the plug
  refuses ~/hook.stl ("outside the folders this agent may use"), which would test the path rule, not the mesh. Claude
  Code runs in ~ (where hook.stl is). The file entry-solidcraft-wrote.json therefore carries the added argument.

## Run day (5 Nov 2026, resumed after the C: pause)
- Session container restarted (the first one was removed during the memory pause); take P redone by fx8session.sh:
  the same counts (28 / 1484 / 1364); P/prep.json and the transcript differ only in timing.
- Take A step 1 (Extrude cut): the scripted OK click (probe position) landed below the Extrude panel, because on this
  run the refusal is not shown live; it appears only after OK, so the panel was shorter than in the probe. No cut was
  tried in take A (A/cut.png shows the panel without a refusal). Retried once as take A2 (lab/fx8A2.sh + fx8A2b.sh,
  the same design: hook.stl mesh + Sketch1): OK at the panel's real OK, the refusal shown and held 4 s, Cancel. The
  clips A-cut-refused and A-cut-reason-line come from A2.
- Take A step 2 (Fillet): the GUI line is "select 1...1000 edges" (the click on the plate's top edge selects nothing
  usable; "1 selected" shows but the mesh has no edges) - stop rule A2: typed verbatim; the B.11 words "there is no
  solid body to modify (mesh bodies have no edges)" are the MCP reply (probe), not the panel.
- Take A step 3: the Properties "Bounding box" row is covered by a hover tooltip (centre of mass) in the frame; size
  25 x 20 x 60 comes from the MCP measure (D/reply.txt: bbox min [0,-20,0] max [25,0,60]).
- R1 ended on Claude's question (AskUserQuestion) with no answer, so `/cost` never ran: cost.txt is empty and the
  budget ledger got an empty cost. Tokens are in session.jsonl (model claude-sonnet-5-5).
- R1 session.jsonl: organizationUuid and e-mail redacted by hand (scrub.py does paths only).
