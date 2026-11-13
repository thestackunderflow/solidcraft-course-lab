# fx14 lab deviations (LAB-fx14 v1, prereg 8ad2ac7)

1. Image ID: the box's sc5-l5:0.28.0 is sha256:38a6f6787dc1..., not the PC's 2992c9ecbca2 (docker save / load into the
   box's store gives a different ID; as fx11/fx12 on the same box). The P0 check is the version line, "solidcraft 0.28.0": passed.
2. G0 step 0 added: G0/tools.py wrote the plug's tool list and list_commands into G0/tools.txt and G0/commands.json
   before g0.py was written, so the command and parameter names were read, not guessed (LAB says "read from the MCP
   tool list and logged into G0/tools.txt").
3. Model.faces has no certificate field (index, name, exact, area, centroid, plane_normal, point). Q14's "certificate"
   column is therefore the `attachment` field of sketch.create's reply (exact_face on every rung that attached).
4. Window checks: the LAB requires G0a, G0b and every rung whose client reply carried the line. No client reply carried
   it; G0c and G0d were also checked in the window (ladder order, step 2 lists all four) so every rung has its window
   result. Not a new rung.
5. G0a's window shot (g0a-window.png) was taken from the probe session (lab/fx14px.sh) after the sketch had opened,
   not by lab/fx14G0w.sh (written after the G0a probe); same file, same Home view, same New Sketch path, same face
   point (830, 330 halved). G0b-G0d used lab/fx14G0w.sh (4 s hold, full-size shot).
6. Each `open` of a G0 file added a tab in the window (g0a, g0b, g0c, g0d tabs visible in the shots); the active tab is
   the rung's.
7. Shell's tangent_chain was not passed through MCP (default false); the block's edges are sharp, so the chain is the
   top face only either way. The window's Shell dialog (chain on by default) was not used for G0c's build.
8. S1 applied: no rung passed. Takes P, A-E and R1 not run; no filming; fx14lib.sh positions not extended beyond the
   G0 probe (New Sketch 128 88, top face 830 330, rim 670 235, sketch Cancel 1180 90, Create Issue 1252 504, Close
   draft 733 670; halved units).
