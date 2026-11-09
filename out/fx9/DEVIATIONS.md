# fx9 lab: deviations from LAB-fx9.md v2 (pre-registration 862eb44)

Nothing was re-scored. Every clip is kept (including the failed attempt in C-attempt1/).

1. **All GUI takes: the start file is opened over the plug, off camera.** `~/nut.sc` is copied from P/ into the take's
   fresh home and opened with the plug's `open` tool before the recording (lab/fx9lib.sh `open_nut`), because File >
   Open shows no file window under Xvfb (fx8 stop rule A3). The take opens on the file already in its tab.
2. **Take A, "the Hole feature in the timeline held 4 s (diameter 8 visible)":** done by double-clicking Hole1 in the
   timeline (Edit Hole, Diameter 8 visible, held 4 s, A/hole8.png), then Cancel.
3. **Take A, the end of step 4:** the closing Cancel click missed. Cancel sits higher when the error line is shorter
   (the M10 "too narrow" line has 3 lines, the M8 "too wide" line 4), so the click at the M8 layout's Cancel hit
   nothing and the Thread dialog was still open when the recording stopped (A/after.png). Volume and timeline were
   read unchanged (672.70 mm3, Sketch1/Extrude1/Hole1). Takes B and C close the dialog with its title-bar X instead.
4. **Take B step 3, the bore's smallest diameter:** measured off camera, not with the GUI Measure tool: the plug's
   `export` (ASCII STL) and the smallest distance of any inner vertex from the hole's axis (lab/fx9.py `bore`).
   Result 6.738 mm. Method check (take C, off camera): the unthreaded 6.75 mm nut gives exactly 6.75 by the same
   method, so the 0.012 mm is in the threaded mesh, not the method. The volume is on camera (Inspect > Properties,
   733.54 mm3) and over the plug.
5. **Take B, close-ups:** section = Inspect > Section, plane XZ picked in Browser > Origin, Distance 0, Hatch on;
   close-up by six mouse-wheel steps at the cut wall; "low angle" = a short middle-button tilt. The Properties
   window was left open at the end.
6. **Take C, attempt 1 (C-attempt1/, not scored):** a script bug: the loop variable `X` was overwritten by the glide
   helper's `xdotool getmouselocation --shell` (it sets X and Y), so after the first try (a real 6.3: refused, too
   narrow) the diameters typed were mouse coordinates (2499, ...). The container was stopped during the fourth try.
   Fixed (loop variable `DIA`) and take C re-run in full; the re-run is the take of record.
7. **Take C, Q6:** the tapped option was set on a fresh copy of ~/nut.sc through Edit Hole (Hole Tap Type: Tapped,
   Size M8), not on a new Hole in a hexagon with no hole: the same Hole dialog and rows, and the hole stays at the
   centre without placement clicks.
8. **Takes B, C:** "Thread M8 Modeled" was done exactly as take A (Automatic size unticked, Size 8 mm first, then
   Modeled) for every try, so all tries share one sequence. In B the dialog's own pre-fill for the 6.75 hole was
   already M8 (B/dialog.png).
9. **Take D:** the pre-registered point [4, 0, 3.5] was used unchanged: the hole's centre is [0, 0] (P/volume.txt
   bbox), so no adjustment.
10. **env.txt:** the image ID line was added from the host after takes P and A (the container cannot inspect its own image);
    it matches section 0 (sha256:2992c9ec...).
11. **R1, the plan banner:** Claude Code's start banner names the plan. Before the recording the pane's screen is
    reset and its history cleared (`tmux send-keys -R`, `clear-history`), so the banner is not in screen.mp4 or the
    later pane captures; pane-start.txt (captured before the reset) is redacted to "[plan]". Tested twice off the
    record in out/scratch/fx9banner (Claude Code started with the sign-in, no message sent, then /exit; IS_DEMO=1 did
    not hide it).
12. **R1 cost:** $0.2472, above the plan's estimate (about $0.07) and under the $0.50 cap (ledger
    edu-visualization/fixit-fx9-BUDGET.tsv). Not a rule break; recorded.
13. **R1 footage:** with the network on, SolidCraft's title bar shows an "Update to 0.30.1" button (runs/R1/after.png);
    the takes (no network) do not. The run itself is on 0.28.0 (env.txt, meta.json).
