# SolidCraft + Claude Course: the lab

The lab behind "How to Connect Claude to SolidCraft: MCP Setup and What Runs Where | SolidCraft + Claude Course 1"
(The Stack Underflow). One lab for the whole course; each lesson adds a folder under `out/`. Everything runs in
Docker with capped memory; nothing is installed on the host.

**Lab start day: 27 Oct 2026. Pinned build: SolidCraft 0.24.1** (the stable release on GitHub that day, published
2026-10-27 13:36 UTC; Linux x86_64 tarball checked against the release's `SHA256SUMS.txt`). 0.24.1 writes design
format 40, which 0.24.0 and older refuse.

## Lesson 1: what the lab must show (written before any run)
The lesson says only what these files show. Each question, and the file that answers it:

| # | Question | How it is measured | Answer file |
|---|---|---|---|
| Q1 | Which version does solidcraft.io/download offer today? | the page in a real browser (headless Chromium, JavaScript on) and with curl (no JavaScript), against GitHub's latest stable release | `out/l1/sitecheck.json` |
| Q2 | Does SolidCraft add itself to the Claude apps by itself? | a fresh home folder; the Claude Desktop folder `~/.config/Claude/` and Claude Code's `~/.claude.json` exist before SolidCraft's first start; the app started with no `--control` and no `SOLIDCRAFT_CONTROL_PORT`; every client file diffed before and after; the window filmed (the one-time notice) | `out/l1/autoreg/` |
| Q3 | Does a second start change the entry? | the same home, a second start; file hashes compared | `out/l1/autoreg/` |
| Q4 | Claude installed after SolidCraft: is the entry there? | SolidCraft started first, the Claude folder made while it runs; then the fix (`solidcraft-cli mcp setup`, what Help > Connect AI assistants runs) | `out/l1/order/` |
| Q5 | Is the menu Help > Connect AI assistants in this build? | the menu opened in the filmed window | `out/l1/menu/` |
| Q6 | Does the entry SolidCraft wrote drive the open window (bridged) or its own hidden session (headless)? | four cases with a scripted MCP client over the written entry (no AI): app open before the client starts; opened after; closed mid-session; reopened. Each: what the server says, what a call returns, a window screenshot | `out/l1/startorder.json` |
| Q7 | How many tools does the plug offer? | the server's own `tools/list` | `out/l1/tools.json` |
| Q8 | What does Claude say with no plug? | one Claude Code chat with no tools: "Make a 20 mm cube in SolidCraft." | `out/l1/runs/noplug-1/` |
| Q9 | Does the cube appear, and what does SolidCraft measure? | one Claude Code chat through the entry SolidCraft wrote, the window open and filmed: three requests (what's in my design; make a 20 mm cube; measure it) | `out/l1/runs/plug-1/` |
| Q10 | Is the result real? | the proof: a $0 script replays Claude's logged tool calls over the same entry in a fresh app, asserts the volume, exports an STL; our own checker reads that STL | `out/l1/replay.json` |
| Q11 | Does an older install offer the update? | 0.23.1 started with network; the title bar filmed | `out/l1/update/` |

Rules: Claude runs only where the lesson claims something about Claude (Q8, Q9: two chats). Every Claude chat is a
fresh headless Claude Code session (pinned version logged) with only SolidCraft's tools, no memory, no CLAUDE.md
files, no other tools; tool approvals are given in advance by the run's settings (`--allowedTools`), which a viewer's
app would ask about. Costs go to `../solidcraft-course-BUDGET.tsv`; paid runs stop at $0.90 of the $1.00 cap.

Claude Desktop screens: Claude Desktop is not run here (it needs a person to sign in). Its config folder is created
empty so SolidCraft treats it as installed, which is what SolidCraft's docs say it checks. The video shows Claude
Desktop's steps as labelled cards quoting the docs.

## The checker (`checker/`, tests first)
- `checker/stl.py`: reads binary and ASCII STL; the volume (divergence theorem), the bounding box and whether every
  edge is shared by exactly two triangles in opposite directions (closed).
- `checker/entry.py`: reads a client file and returns the `solidcraft` entry (command, args) and its problems.
- `client/mcp.py`: a small stdio MCP client (initialize, tools/list, tools/call) used by the start-order cases and the
  replay; it logs every line.

## Lesson 1: what it found (27 Oct 2026, SolidCraft 0.24.1, Linux x86_64 in Docker)
| # | Answer | File |
|---|---|---|
| Q1 | solidcraft.io/download in a real browser (Chromium, JavaScript on) offers **0.24.1**, the same as GitHub's latest stable (14:41 UTC). Without JavaScript (curl) the page shows its 0.22.0 fallback. The page says "current Windows builds are not signed yet". | `out/l1/sitecheck.json`, `out/l1/sitecheck/browser.png` |
| Q2 | **No.** With both Claude apps' folders in place and SolidCraft started plainly, neither file got an entry: idle 30 s (`autoreg-idle`), and with New design clicked and the mouse moving for 60 s (`autoreg`); 0.23.1 the same (`autoreg-0.23.1`). No notice appeared. In the 0.24.1 source the job that writes the entries (`ai_connect::tick`) runs once while the graphics start, before the app arms it (`ai_connect::begin`, second frame), and never again; so the automatic step never runs in these builds. Not reported upstream by us. | `out/l1/autoreg*/autoreg.json` |
| Q3 | The entry the menu wrote is not changed by a second start, nor by the menu clicked again (same SHA-256). | `out/l1/menu/menu.json` |
| Q4 | With no Claude app installed, the in-window **"?" (help) button > Connect AI assistants** (macOS menu-bar Help has no such item in 0.24.1) says "no supported client found (opencode, claude-desktop, claude-code, ...)" and writes nothing. After the Claude apps' folders exist, the same menu writes both entries and says "Restart each assistant to load the SolidCraft server. Each file was backed up as .bak before it changed." | `out/l1/menu/A-no-claude-dialog.png`, `B-claude-installed-dialog.png` |
| Q5 | The menu is the round "?" button at the top right of the window: Documentation, About, Keyboard Shortcuts, Messages, Report an Issue, Crash Reports, **Connect AI assistants...** | `out/l1/menu/*-menu.png` |
| Q6 | The entry is `solidcraft-cli` (full path) with one argument, `mcp`. App open first: the cube appears in the window, 8,000.0 mm³. Plug started before the app, app opened before any build: the next call drives the window (cube in the window, 8,000.0). App closed mid-session: the next call fails with "the SolidCraft app at 127.0.0.1:27878 did not answer (connection closed): it may have quit or crashed during this call, after running it or not. ..." App reopened: the same plug works again (8,000.0). | `out/l1/startorder/startorder.json`, `case*.png` |
| Q7 | **19 tools** in the server's own `tools/list` (also 19 in the Claude run's log). | `out/l1/tools.json` |
| Q8 | No plug (Claude Code 2.1.311, claude-sonnet-5-5, no tools): Claude wrote shell commands out as text (looking for SolidCraft); nothing ran them; no cube. $0.012. | `out/l1/runs/noplug-1/turns.json` |
| Q9 | Through the entry SolidCraft wrote, window open and filmed: "What's in my SolidCraft design?" one `inspect_design` call: "Your SolidCraft design is empty..."; "Make a 20 mm cube in SolidCraft." one `execute` call, `solid.box` 20 x 20 x 20 (no batch); the cube appears in the window; "Measure it." one `measure` call: volume 8000.0 mm³ (bbox 0 to 20). $0.147. | `out/l1/runs/plug-1/` (`screen.mp4`, `transcript.jsonl`, `turns.json`, `timeline.jsonl`) |
| Q10 | Proof: the 3 logged calls replayed in a fresh container over the same entry: SolidCraft measures 8000.0 mm³; our checker reads the exported STL: 12 triangles, closed, outward, 20 x 20 x 20, **8000.0 mm³**. | `out/l1/replay.json` |
| Q11 | 0.23.1 with network shows **"Update to 0.24.1"** in the title bar. | `out/l1/update/titlebar-60s.png` |

Lab notes: Ctrl+Q did not close the window under Xvfb (the scripts then stop the app with TERM; the next start shows a
Crash Reports dialog, as in `startorder/case4-after-cube.png`). The window repaints only on input, so the scripts move
the mouse before every screenshot. The light theme is set over the control channel (`ui.prefs`).

## Lesson 2: what the lab must show (written before the recorded runs)
"SolidCraft Tutorial for Beginners: Sketch a 3D Part by Hand vs Claude | SolidCraft + Claude Course 2". **Pinned
build: SolidCraft 0.25.0** (the stable release on GitHub on the lab's start day, 27 Oct 2026, published 22:53 UTC; it
writes design format 41, which 0.24.1 refuses). Claude Code 2.1.311 with Claude Sonnet 5.5. Images `sc2-app:0.25.0`
(`docker/app.Dockerfile` with `SC_VER=0.25.0 SC_OLD=0.24.1`) and `sc2-l2:0.25.0` (`docker/l2.Dockerfile`: xterm,
tmux, a large cursor theme, Claude Code).

The part: a wall hook's side outline, a J (back plate 60 tall and 5 thick, hook arm 25 deep, lip 10 high, all 5 thick)
on the front plane XZ, extruded 20. Worked out without SolidCraft (`checker/outline.py`, tested): area 425 mm²,
volume 8,500 mm³, outside size 25 x 20 x 60.

| # | Question | How it is measured | Answer file |
|---|---|---|---|
| L2-Q1 | Which version does the download page offer? | `sitecheck/check.sh` with `LESSON=l2` (and again on recording day, `l2/recday`) | `out/l2/sitecheck.json` |
| L2-Q2 | Does the by-hand path work as the lesson says? | `lab/l2hand.sh`: the real window at 2880x1800 (UI scale 1.8), filmed at 30 fps with a cursor log; xdotool moves, clicks and typed numbers only (no control channel or MCP until the recording stops) | `out/l2/hand/` |
| L2-Q3 | What does SolidCraft report for the hand-made part? | after Q2, a scripted MCP client (no AI) over the entry `solidcraft-cli mcp setup` wrote: `tools/list`, `inspect_design`, `measure` | `out/l2/hand/read.json`, `tools.json` |
| L2-Q4 | What does Claude do with the same moves? | `claude-run/l2run.sh` + `lab/l2claude.sh` + `lab/l2drive.py`: one Claude Code session in its real terminal (xterm + tmux) beside the window, filmed; two messages typed into it; approvals answered with their "Yes" if asked; the entry wrapped in the logging proxy | `out/l2/runs/claude-1/` |
| L2-Q5 | Same part? | `lab/l2compare.py`: steps, volume, profile area, plane, corner points, size; position reported apart | `out/l2/compare.json` |
| L2-Q6 | Is Claude's result real? | `lab/l2replay.sh`: Claude's logged calls replayed in a fresh window, no AI; measure; our STL checker | `out/l2/replay.json` |

How it is filmed, said plainly: the by-hand clicks are played by a script (xdotool) into the real SolidCraft window at
a person's pace, so the footage shows exactly the clicks a person makes. A $0 probe found that a change sent through
the plug repaints the window with no mouse input in 0.25.0 (`out/l2/probe/repaint.json`), so nobody touches the mouse
during Claude's run and no cursor is drawn in it. Claude Code is started with `claude --model claude-sonnet-5-5` and no
permission flags (its own default mode); it gets this PC's Claude sign-in as an environment variable that never
reaches the run folder. Keyboard input under Xvfb needs `xdotool windowfocus` first (Ctrl+Q still does not quit).

## Lesson 2: what it found (27-28 Oct 2026, SolidCraft 0.25.0, Linux x86_64 in Docker)
| # | Answer | File |
|---|---|---|
| L2-Q1 | The download page in a real browser offers **0.25.0**, GitHub's latest stable (read 00:05 and again 00:55 UTC on 28 Oct); curl alone sees the 0.22.0 fallback. | `out/l2/sitecheck.json`, `out/l2/recday/` |
| L2-Q2 | The by-hand path works as filmed: New design, New Sketch, Origin > XZ (no OK needed), Line, seven typed lengths with the H/V snap and a click on the first point, Esc, Finish Sketch, Extrude (the Distance box opens at 10 mm; typed 20), the house on the view's bar, right-drag, wheel, History tooltips, right-click Body1 > Properties. Take 2 (161 s) is the one used; it is take 1 with longer holds where the narration is longer. In take 1's first try the slower pan moved 20 px less, the last line missed its snap and the volume came out 8392.7: the script now pans the same distance more slowly. | `out/l2/hand/` (events, cursor log, 1440x900 copy of the recording) |
| L2-Q3 | By hand: **8,500.0 mm³**, 25 x 20 x 60, box z 0 to 60 (stands up), extruded toward -Y; History: Sketch1 (Sketch), Extrude1 (ExtrudeFeature); sketch fully constrained (dof 0), 8 lines, 7 dimensions, profile 425.0 mm². 0.25.0's plug offers **19 tools**. | `out/l2/hand/read.json`, `tools.json` |
| L2-Q4 | Claude Code 2.1.311, "Sonnet 5.5 · Claude API", started in **auto mode** (its start notice): no approval was asked. Two runs. claude-2 (the one filmed): one `batch` of four commands (`sketch.create {plane: "XZ"}`, `sketch.line` with the 8 corner points and `closed: true`, `sketch.finish`, `solid.extrude {distance: 20, operation: "new"}`), then `measure`; message 2: `inspect_design`. claude-1: three `describe_command` calls first, then the same batch. Both: **8,500.0 mm³**, but **z from -60 to 0**: the sketch made through the plug on "XZ" has its up along -Z (y_dir 0,0,-1), while the XZ picked in the Browser has up +Z. Claude's own reply said so both times and offered to flip it (not tested). Its sketch: no dimensions, 14 degrees of freedom. The window drew the part with nobody touching the mouse (no input during the run). Cost $0.1413 + $0.0890 (Claude Code's /cost). | `out/l2/runs/claude-1/`, `claude-2/` |
| L2-Q5 | **"same shape, size and steps, but upside down"**: same volume, size, corners in the sketch, steps and plane (XZ); the sketch's up is opposite. | `out/l2/compare.json` |
| L2-Q6 | Claude's three logged calls replayed in a fresh window with no AI: 0 errors, **8,500.0 mm³**, upside down again; our STL checker on the export: closed, **8,500.0 mm³**. | `out/l2/replay.json` |

Lab notes: keyboard input under Xvfb needs `xdotool windowfocus` first; without a UTF-8 locale xterm draws a minus sign
and ³ as "_" (claude-1's terminal shows it; claude-2 runs with `LANG=C.UTF-8` and `xterm -u8`); Claude Code 2.1.311
ends a turn with a line like "Baked for 12s · done 1:21 AM" (no "esc to interrupt" was ever sampled), which the driver
now watches for; the input box shows Claude Code's own greyed suggestion for the next message (never sent).

## Lesson 3: what the lab must show (written before the recorded runs)
"SolidCraft Parameters by Hand vs Claude: Named Sizes for Beginners | SolidCraft + Claude Course 3". **Pinned build:
SolidCraft 0.26.1** (the stable release on GitHub on 29 Oct 2026, published 11:46 UTC; the download page in a real
browser offers the same; 0.26.0 writes design format 43, which 0.25.1 and older refuse). Claude Code 2.1.311 with
Claude Sonnet 5.5. Images `sc3-app:0.26.1` (`docker/app.Dockerfile`, `SC_VER=0.26.1 SC_OLD=0.25.0`) and `sc3-l3:0.26.1`
(`docker/l3.Dockerfile`).

The part: lesson 2's wall hook with five named sizes (user parameters): `plate_height` 60, `width` 20, `thickness` 5,
`hook_depth` 25, `lip_height` 10; the J typed with names and formulas (`checker/outline.py` `J_EXPRESSIONS`, tested:
the same corners as lesson 2). The change: `hook_depth` 25 to 40; expected 500 mm², 10,000 mm³, 40 x 20 x 60.
The Claude requests and the scoring rules were written to `out/l3/prereg.json` (committed) before the first run.

| # | Question | How it is measured | Answer file |
|---|---|---|---|
| L3-Q1 | Which version does the download page offer? | `sitecheck/check.sh` with `LESSON=l3` | `out/l3/sitecheck.json` |
| L3-Q2 | Does the by-hand path with names work? | `lab/l3hand.sh`: the real window, filmed, xdotool only | `out/l3/hand/` |
| L3-Q3 | What does SolidCraft report before and after the change? | Properties (filmed) and `lab/l3read.py` (no AI: inspect_design, measure, parameters.list) | `out/l3/hand/read.json` |
| L3-Q4 | Lesson 2's plain-number J: d1 25 to 40? | `lab/l3plain.sh`: filmed; reads after the refusal and after a formula fix | `out/l3/plain/` |
| L3-Q5 | Claude not asked (A1, A2) and asked in one sentence (B1, B2) | `claude-run/l3run.sh` + `lab/l3claude.sh` (lesson 2's driver), messages in `claude-run/l3messages.sh` | `out/l3/runs/*/` |
| L3-Q6 | Scored against the pre-registered rules | `lab/l3compare.py` | `out/l3/compare.json` |
| L3-Q7 | Is it real? | `lab/l3replay.sh A1`, `B1`: logged calls, fresh window, no AI; STL checker | `out/l3/replay-*.json` |

## Lesson 3: what it found (29 Oct 2026, SolidCraft 0.26.1, Linux x86_64 in Docker)
| # | Answer | File |
|---|---|---|
| L3-Q1 | The download page in a real browser offers **0.26.1** = GitHub latest; curl alone sees the 0.22.0 fallback. | `out/l3/sitecheck.json` |
| L3-Q2 | Works as filmed: Parameters is on the **Model** tab (the docs say Manage); Add parameter, name, Tab, Tab, value, Enter; the Line tool's length box takes names and formulas (`hook_depth - 2 * thickness`), the dimensions read "fx: 15.00 mm"; Extrude Distance `width`. | `out/l3/hand/` |
| L3-Q3 | Before: **8,500.0 mm³, 25 x 20 x 60**. After `hook_depth` 40 (the hook rebuilt with the dialog open): **10,000.0 mm³, 40 x 20 x 60**; 5 user parameters; all 8 sizes (7 dimensions + the extrude) written from names; fully constrained. | `out/l3/hand/read.json`, `props-*.png` |
| L3-Q4 | d1 = 40 is **refused**: "sketch `Sketch1`: its constraints would conflict (k2, k3, k6, k7, k10, k11, k14, k15); the values were not changed". The ids are d1, d3, d5, d7 (the lengths across: 25, 5, 15, 5) and the four upright lines. The dialog's box and Value column show 40, but the model keeps 25 (8,500, 25 x 20 x 60). Fix filmed: d5 = `d1 - 10` (the Filter finds the row), then d1 = 40: accepted, 10,000 / 40 x 20 x 60. | `out/l3/plain/`, `after-refusal/read.json` |
| L3-Q5 | **Not asked: 0 user parameters in 2 of 2.** A1: built it hanging (Z -60..0), checked, rebuilt it standing; the edit = a new design and the J drawn again with new corners: 40 x 20 x 60, 10,000. A2: read "40 deep" as the extrude: 25 x 40 x 60, 17,000, and said so. **Asked: 5 user parameters and a one-number edit (`set_parameter hook_depth 40`) in 2 of 2.** B1 placed the plate's inner edge at x = `hook_depth - 2 * thickness` (15) instead of `thickness` (5): **19,500 mm³** at 25 (its reply gave the number and did not flag it), **37,500 mm³** at 40 (plate 30 thick). B2: all corners right, **10,000 / 40 x 20 x 60**. Every run first built the hook hanging (lesson 2's plane) and rebuilt it standing. Cost $0.1312 + $0.1900 + $0.1805 + $0.1741. | `out/l3/runs/`, `compare.json` |
| L3-Q7 | A1's 9 logged calls, no AI: 0 errors, **10,000.0**; B1's 11: 0 errors, **37,500.0**; our STL checker: closed, the same volumes. | `out/l3/replay-A1.json`, `replay-B1.json` |

Lab notes: the turn-end line can carry a non-ASCII verb ("Sautéed for 41s"): the driver's pattern now takes `\w`
(B1 waited 6 minutes for its time-out before turn 2; the recording's idle part is not used). `parameters.list` does
not count point expressions in `sketch.line` as uses (B1/B2 show `used_by: []`), so the names-in-corners evidence is
the logged `sketch.line` points. The 2880x1800 masters stay in `out/scratch/l3-masters` (not committed); each run
folder has a 1440x900 copy.

## Run it
```bash
docker build -t sc1-app:0.24.1 -f docker/app.Dockerfile docker
docker build -t sc1-browser:1 -f docker/browser.Dockerfile docker
docker run --rm --memory 1g --network none -v "$PWD:/work" -w /work sc1-app:0.24.1 python3 -m pytest -q tests/
docker run --rm --memory 2g --shm-size 1g -v "$PWD:/work" sc1-browser:1 bash /work/sitecheck/check.sh
for s in autoreg menu startorder; do docker run --rm --memory 3g --shm-size 1g --network none -v "$PWD:/work" sc1-app:0.24.1 bash /work/lab/$s.sh; done
docker run --rm --memory 3g --shm-size 1g --network none -v "$PWD:/work" sc1-app:0.24.1 bash /work/lab/autoreg.sh autoreg-0.23.1 0.23.1
bash claude-run/run.sh noplug 1 && bash claude-run/run.sh plug 1      # paid: needs Claude Code on the host
docker run --rm --memory 3g --shm-size 1g --network none -v "$PWD:/work" sc1-app:0.24.1 bash /work/lab/replay.sh plug-1
docker run --rm --memory 3g --shm-size 1g -v "$PWD:/work" sc1-app:0.24.1 bash /work/lab/update.sh
# lesson 2
docker build -t sc2-app:0.25.0 --build-arg SC_VER=0.25.0 --build-arg SC_OLD=0.24.1 -f docker/app.Dockerfile docker
docker build -t sc2-l2:0.25.0 -f docker/l2.Dockerfile docker
docker run --rm --memory 1g --network none -v "$PWD:/work" -w /work sc2-app:0.25.0 python3 -m pytest -q tests/
docker run --rm --memory 2g --shm-size 1g -e LESSON=l2 -v "$PWD:/work" sc1-browser:1 bash /work/sitecheck/check.sh
docker run --rm --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc2-l2:0.25.0 bash /work/lab/l2hand.sh hand
bash claude-run/l2run.sh claude-2                                     # paid: uses this PC's Claude sign-in
docker run --rm --network none -v "$PWD:/work" -w /work sc2-app:0.25.0 python3 lab/l2compare.py claude-2
docker run --rm --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc2-l2:0.25.0 bash /work/lab/l2replay.sh claude-2
docker run --rm --network none -v "$PWD:/work" -w /work cadcmp-openscad:2021.01 python3 video/draw2.py   # cards (any image with PIL)
# lesson 3
docker build -t sc3-app:0.26.1 --build-arg SC_VER=0.26.1 --build-arg SC_OLD=0.25.0 -f docker/app.Dockerfile docker
docker build -t sc3-l3:0.26.1 -f docker/l3.Dockerfile docker
for t in l3hand.sh l3plain.sh; do docker run --rm --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc3-l3:0.26.1 bash /work/lab/$t; done
for r in A1 B1 A2 B2; do bash claude-run/l3run.sh $r; done                 # paid: uses this PC's Claude sign-in
python3 lab/l3compare.py
for r in A1 B1; do docker run --rm --memory 4g --shm-size 1g --network none -v "$PWD:/work" sc3-l3:0.26.1 bash /work/lab/l3replay.sh $r; done
docker run --rm --network none -v "$PWD:/work" -w /work sc3-app:0.26.1 python3 video/stills3.py
docker run --rm --network none -v "$PWD:/work" -w /work cadcmp-openscad:2021.01 python3 video/draw3.py
```

## Licence
Apache-2.0 (`LICENSE`). Not affiliated with SolidCraft (Tangency Labs) or Anthropic.
