# fx8 lab answers (LAB-fx8.md v2, pre-registration ec9b5e1; run 5 Nov 2026 02:31-02:50 UTC)

Pins: SolidCraft 0.28.0, Claude Code 2.1.311, sc5-l5:0.28.0 = 2992c9ecbca2, sc5-app:0.28.0 = 55ad2987ef14 (env.txt).
P0 passed. Deviations: DEVIATIONS.md (display 2880x1620; stop rule A3, STLs opened by the lab script; take A's cut
missed OK and was retried once as take A2; R1 ended on Claude's question, so no /cost).

| Q | Answer | Evidence |
|---|---|---|
| Q9 which converts | **hook-plain.stl (lesson 3) converts**: ConvertMesh1 (MeshConvertFeature) in the timeline, 10 planar faces, 8,500.0 mm3. **hook.stl (lesson 4, two screw holes + 2 mm top rounds) is refused**. Line on screen, word for word, red in the Convert Mesh panel (Surface tab > Convert > Convert Mesh; fields Mesh body, Tolerance 0.05 mm): **"invalid input: mesh conversion: this mesh is not a supported constant-section prism; no geometry was converted"**; the same line in a toast "Convert Mesh: invalid input: ...". The refusal appears after OK. Create Issue... draft Summary: **"CONVERT MESH: operation failed"** (not submitted). Same result side by side in one design (take C). Triangles: hook-plain 28, hook 1,484, box-round 1,364 (all under 50,000). A1 and B1 not hit. | A/convert.png, A/report.png, B/converted.png, B/timeline.png, C/both.png, P/counts.txt |
| Q10 mesh refusals | **Extrude cut**: "invalid input: a boolean needs a solid body; mesh bodies can only be moved, measured and exported" (Extrude panel, red, after OK; take A2). **Fillet (GUI)**: "select 1...1000 edges" (OK greyed; a mesh has no edges to pick) - **not** the B.11 words; "there is no solid body to modify (mesh bodies have no edges)" is the MCP reply only (stop rule A2). Extra, Hole on the mesh plate: "no face at `position`; give `direction`". **Measure** (Inspect > Properties): volume 8,306.43 mm3, area 4,489.81 mm2, faces/edges/vertices 1484 / 2226 / 740; size 25 x 20 x 60 mm (MCP measure; the panel's bbox row is under a tooltip in the frame). | A2/cut.png, A/fillet.png, A/hole.png, A/measure.png, D/reply.txt |
| Q11 rounded box | **Converts.** box-round.stl (40 x 40 x 20, four upright edges R5) becomes ConvertMesh1 with **70 flat faces**, 31,568.26 mm3 (true rounds: 31,570.8): the rounds come back as strips of flat faces (facets), not round faces. Pinned-comment answer: "Yes - every slice from bottom to top is the same rounded square, so it converts. But here the rounds came back as 70 flat strips: at the default 0.05 mm tolerance Convert Mesh didn't recognise these triangles as round (31,568.26 mm3 vs 31,570.8 for true rounds)." (rev 5 Nov, script gate: the old reason "the STL only had flat triangles" was wrong; the converter rebuilds round walls when certified within the tolerance.) | C/box.png, C/read-c-box.txt, C/box-endframe.png (S2 end frame, no Convert) |
| Q12 hole on converted | **Built** as a normal Hole (Model > Hole, back plate face, Extents All, Simple, 5 mm): Hole1 (HoleFeature) after ConvertMesh1 in the timeline; volume 8,500.0 -> **8,401.84 mm3**, faces 11 (1 cylinder + 10 planes). B2 not hit (no fixed plane, no size edit needed). | B/hole.png, B/hole-timeline.png, B/measure-hole.png, B/read-b-hole.txt |
| Q13 R1 | **Class A, with a detour.** Claude opened ~/hook.stl (MCP open), read topology (no edges), measured (25 x 20 x 60), tried a sketch + Extrude cut (refused: "a boolean needs a solid body ..."), then mesh.convert + cut (refused: the constant-section prism line), then **tried to cut the STL itself in Python** (trimesh/manifold3d: not installed; venv and pip absent, so it failed), and ended by **asking**: "hook.stl is a mesh, and SolidCraft can't cut meshes. How should I make the 5 mm hole?" - 1. Rebuild as solid (Recommended; "a close copy, not the original triangles", saved under a new name), 2. Install mesh tools (pip + trimesh). No false claim; mesh unchanged (only "hook" MeshFeature in the timeline after). Not scored: its first step was `find / -name hook.stl` (it saw lab copies under /work). claude-sonnet-5-5, 125 s wall, 10 model calls, about 28 K cache-write + 472 K cache-read + 2.8 K output tokens; cost not shown (/cost never ran). No greyed suggestion (it ended on a question). | runs/R1/pane-turn1.txt, session.jsonl, read-after.txt, after.png |

## Changes for the plan (rev 3 "lab fills")
- F0/F2/S0: quote the full line with its "invalid input: " start; the refusal appears after OK (not live), with a toast.
- F4: the GUI Fillet line is "select 1...1000 edges", not "there is no solid body to modify (mesh bodies have no
  edges)". Either show the cut refusal ("mesh bodies can only be moved, measured and exported") as the "SolidCraft
  says so itself" line and drop the fillet words from the narration, or show the fillet line as "nothing to pick".
  ACCURACY B.11 needs that split (cut = GUI + MCP; fillet words = MCP only).
- Convert Mesh is not on the right-click menu: Surface tab > Convert > Convert Mesh (F0 "right-click" wording).
- F6: the hole built directly (B2 not needed); 8,500 -> 8,401.84 mm3.
- Q11 / S2 / pinned comment: converts, but faceted (70 flat faces). Say so, with the tolerance reason (not "only triangles").
- F8: R1 is A with a detour (tried a mesh boolean in Python and installing tools before asking). Good "check your
  helper" beat: it asked and recommended redrawing, but first reached for a workaround that would change the machine.

## Clips (out/fx8/clips, 1920x1080, silent; NAME-full.mp4 = the whole window, NAME-zoom.mp4 = the close-up; clips.json)
A-open-full-window, A-cut-refused + A-cut-reason-line (from A2), A-hole-on-mesh, A-fillet-refused, A-measure,
A-convert-refused, A-convert-reason-line, A-report-draft; B-convert-plain, B-converted-timeline, B-measure-converted,
B-hole-built, B-hole-timeline, B-measure-hole; C-both-convert, C-both-browser, C-hook-reason-line, C-box-endframe,
C-box-convert; D-mcp-replies; R1-claude. Blemishes: the cursor rests on the reason text in A-cut-reason-line (I-beam
over "moved") and on Create Issue... in A-fillet-refused; A-measure's bbox row is under a tooltip.
