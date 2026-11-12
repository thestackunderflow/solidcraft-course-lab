# fx10 lab: deviations from LAB-fx10.md v2 (pre-registration bdc85c2)

Nothing was re-scored. Every clip is kept (including the failed attempts in P-attempt1/ and C-attempt1/).

1. **Where it ran.** Every container ran on the owner's Ubuntu lab box (192.168.1.156, Docker 29.4.3, overlay2), not on
   the PC (the PC ran an unattended Gemma lab that night). Same image tag `sc5-l5:0.28.0`; the box's store reports the
   image ID `sha256:38a6f678...` (config digest) where the PC's containerd store reports `sha256:2992c9ec...`; rule P0
   is the version check, and `solidcraft --version` = 0.28.0 (env.txt). The box has no host ffmpeg: contact sheets
   and scaling ran inside the image. Results were copied back into this repo after each take.
2. **Take P attempt 1 (kept in P-attempt1/, not used): the T came out upside down.** On the XZ plane the sketch's y
   runs along world **-Z** in 0.28.0 (attempt 1: bounding box z -23..0, cap at the bottom). Attempt 2 negates the
   sketch y (out/fx10/P/knob.py comment), so the knob sits at world z 0..23 with the cap on top, as LAB-fx10 states
   in world z. Both attempts: half revolved 7,350.78 mm3; full T refused with the B.10 line over the plug.
3. **The sketch edit view is upside down.** Editing Sketch1 (takes A Q11 and B) shows the sketch in its own frame
   (view gizmo Z pointing down): the stem is at the top of the screen and the cap at the bottom. The 3D views (home
   view, the knob) are the right way up. Script-gate note in RESULTS-fx10.md.
4. **Start files opened over the plug, off camera** (fx9 deviation 1: File > Open shows no file window under Xvfb):
   ~/knob-full.sc for A and B; in take C the plug's `open` of ~/ring.sc happens during the recording (event logged).
   lab/fx9.py is reused for open / read / raw (FX9_ALLOW=1), unchanged.
5. **Axis pick.** "The vertical origin axis" is picked as Browser > Origin > Z (Origin expanded first); the Axis field
   then reads "Z". The axis was not clicked in the view.
6. **Stop rule A2 (the words differ):** the line on screen is `invalid input: the profile crosses the revolve axis`
   with **no "Revolve:" prefix**, shown live under the dialog's fields as soon as the axis is picked; OK greyed. The
   report draft title is "REVOLVE: operation failed". The title follows the screen. A1 did not fire. (The prefixed
   form `Revolve: invalid input: ...` does appear, but only as the window's toast when the revolve comes over MCP,
   take D, D/reply.png.)
7. **Take B, the fix:** the five lines on the left of or across the axis were deleted one by one (the cap's left side,
   its left underside, the stem's left side, and the cap's and stem's end lines, which cross the axis), then the
   outline was closed with one Line-tool chain: stem corner (6, 0) -> origin -> (0, 23) on the axis -> cap corner
   (15, 23), snapping to the corner points and the origin, horizontal/vertical inferred (constraint icons in
   B/half-closed.png; the sketch reports 7 degrees of freedom left, so it is not fully constrained). "On the axis"
   is checked by the result, not by sketch coordinates (the plug's timeline.inspect omits the sketch geometry,
   B/sketch1-inspect.json): the knob's volume 7,350.775708796922 equals take P's plug-built half to 1e-10. The
   knob-half.sc fallback was not needed.
8. **Take B, height:** read from Inspect > Properties (bounding box 30.00 x 30.00 x 23.00 mm), not a second Measure.
   Diameter from Inspect > Measure on the cap's top edge (30.00 mm).
9. **Take C, the sketches were built over the plug, off camera** (not drawn on camera): ~/c12.sc holds the
   construction line and both rectangles in one sketch (C1 and C2 are picked as separate profiles in one Revolve
   dialog), ~/ring.sc the square. C1 is first shown as a preview (OK enabled), then C2 (refused), then rectangle 1 again
   and OK (C1 built, 1,130.93 mm3). The construction line is drawn from world (0, 0) to (0, 10) (sketch y negated,
   item 2); rectangle 2 sits at world z 20..26.
10. **Take C attempt 1 (kept in C-attempt1/, not scored):** C1 / C2 ran as in attempt 2, but at Q12 the helper that
    checks whether Browser > Origin is expanded read the light grey view under the short Browser as "expanded", so
    the click meant for Z hit empty view, no axis was set and the event "Q12 ring 360: ... refused" is a script error
    (no error line on screen, Axis "Select"; C-attempt1/ring.png). Fix 1: test the darkest pixel instead of the mean
    (lab/fx10lib.sh origin_open); take C re-run whole.
11. **R1 deferred to the PC after the Gemma lab (owner's login stays on the PC).** Not run on the box. runs/R1/ is
    empty; Q13 for fx10 is open.
12. **Clips not cut** (lab/fx10clips.py not written); left for the next stage.
13. **R1 run on the PC, takes P-D on the Ubuntu box, same image sc5-l5:0.28.0** (12 Nov 2026, after the Gemma lab).
    Tag and versions match (SolidCraft 0.28.0, Claude Code 2.1.311); the PC's local image ID is 2992c9ec (fx9's pin),
    the box's store lists 38a6f678. Start file = take P's out/fx10/P/knob-full.sc, opened by lab/fx9.py as in the takes.
    lab/fx10R1.sh + claude-run/fx10run.sh are copies of the fx9 pair (no other change; one run, no retry, no harness
    failure). The owner's claude.ai connectors also showed as connected in `claude mcp list` (as fx9); none was called.
14. **Observation, R1 orientation (12 Nov, video cut 3; NOT a re-score).** R1's knob (after.png; reply "Position")
    spans world z = 0 to -23 with the stem at the top (z = 0) and the cap/flange at the bottom: upside down and below
    the ground plane, the mirror of take B's knob (z 0..23, cap on top; P attempt 2 negated the sketch y for this
    reason, deviation 2). Claude said so in its reply and offered to flip or move it. LAB-fx10 section 4's class A
    checks size (30 across) and volume (within 1% of take B), not orientation, so R1 stays class A as pre-registered.
    The greyed "Flip it so the stem points up from z = 0" in R1's prompt box is Claude Code's suggested next prompt,
    not Claude's words; it stays masked. The video (fx10 cut 3) now shows after.png and says the orientation plainly.
