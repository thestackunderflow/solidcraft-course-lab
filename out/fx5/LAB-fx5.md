# LAB-fx5: SolidCraft Send to Slicer: Old Shape Still Showing After a Resend? Reload from Disk | PrusaSlicer (cut B) / SolidCraft Send to Slicer Opens a Second Bambu Studio or OrcaSlicer Window? Fix: Reload from Disk (cut A) — pre-registration v1, 2026-11-01 (before any run)

Lab repo: solidcraft-course-lab. Folder: out/fx5/ (takes out/fx5/G, out/fx5/A, out/fx5/B, out/fx5/C, run out/fx5/runs/R1). Pins: SolidCraft 0.28.0; PrusaSlicer 2.9.2 (stock MK4S presets as in lesson 5); Claude Code 2.1.31x (exact build written to out/fx5/runs/R1/pins.txt at run start); uv 0.13.6; model claude-sonnet-5-5 (expected, read from session.jsonl); OrcaSlicer Linux AppImage and Bambu Studio Linux AppImage: NOT in the pins, version strings written to out/fx5/G/pins.txt from the file name and the About dialog when they start (the source lines quoted in the plan are Orca v2.4.2 and Bambu Studio master). FreeCAD 1.1.4 and freecad-mcp are not used in fx5. Docker image notes: Linux, Xvfb (same display size as lesson 5), Mesa software GL (LIBGL_ALWAYS_SOFTWARE=1) for the slicers' 3D views, FUSE absent so every AppImage is run after --appimage-extract (write the extracted path to pins.txt), XDG_DATA_HOME and XDG_CACHE_HOME unset so the hand-over folder on screen is ~/.cache/solidcraft/slicer as the narration says, home user "maker" as in lesson 7, a fresh home per take unless the take says otherwise. The lesson-5 wall hook design file (hook-lesson4.sc, hook_depth 25) is copied into the home before takes A, B, C and R1 and SAVED (an unsaved design is hashed with the process id, slicer_files.rs). No AI in any take except R1.

This file is committed before any run. Shell note: every command captures its output with `| tee`; `|&` is bash's pipe that carries stderr too (no redirection operators are written in this file). The run follows it line by line. Any deviation is written into out/fx5/DEVIATIONS.md with the time, and the take is marked re-done or stopped (section 6); nothing is re-scored afterwards.

## 2. Questions this lab answers (PLAN §0.4)

9. fx5, Orca/Bambu: does OrcaSlicer's Linux AppImage (and/or Bambu Studio's) start and render in the Xvfb container with Mesa? If yes: with the preference at its default, does a second Send to Slicer open a second window? Is the preference labelled "Allow only one OrcaSlicer instance" (Bambu: "Keep only one Bambu Studio instance") and off by default? With it on, does a resend land in the open window? Does `OrcaSlicer --single-instance` print "Invalid option"? If no: the long video is held and the Short uses PrusaSlicer.
9. fx5, PrusaSlicer 2.9.2: on the second send with --single-instance, is a second object added beside the first, is the first replaced, or does the window still show the old shape? Is the right-click menu text "Reload from disk"? What are the hand-over folder path and the file name (design name plus a 16-hex-digit hash), and do two sends give one file, same name, newer `ls -l` time? What does the `file.send_to_slicer` parameter help say inside SolidCraft 0.28.0's command palette? Does SolidCraft 0.28.0 show a consent prompt before an agent's Send to Slicer?
11. fx5 Claude run: one pre-registered prompt, A/B/C scored before the run, one run, auto mode as lesson 7, the greyed suggested prompt cropped, the evidence frame (F8 size boxes) recorded with matches / does not match.

Q9 is answered in two parts because it gates two different cuts: the Orca/Bambu part (take G, take C) decides cut A vs cut B; the PrusaSlicer part (takes A, B) is needed for the Short and cut B in either case.

## 3. Takes, in run order

Run order: G (gate), A, B, C (only if G passed), R1. G runs first so the cut is known before any PrusaSlicer footage is filmed; the PrusaSlicer takes do not depend on G's result.

Common to every take: Xvfb running; screen recording of the whole display started before the first command and stopped after the last (out/fx5/TAKE/screen.mp4); a second terminal records every typed line with its wall-clock time (`script -t 2 out/fx5/TAKE/typescript.timing out/fx5/TAKE/typescript`); events are written as they happen to out/fx5/TAKE/events.txt as `HH:MM:SS.s  event name` with the names exactly as SCRIPT §1 uses them; every screenshot is `xwd -root | convert xwd:- out/fx5/TAKE/NAME.png` taken at the event named for it.

### Take G: the gate. OrcaSlicer (and Bambu Studio) AppImage in Xvfb

(a) Starting state: fresh home; no SolidCraft; only the two AppImages copied into ~/apps/ (orca.AppImage, bambu.AppImage; original file names written to pins.txt). Mesa present; LIBGL_ALWAYS_SOFTWARE=1 exported; DISPLAY set to the Xvfb display.

(b) Commands, in order (Orca first, then the same block for Bambu with bambu.AppImage, bambu-* file names):
1. `cd ~/apps && ./orca.AppImage --appimage-extract | tail -n 1 | tee out/fx5/G/orca-extract.txt` (if the extract fails: stop rule G1).
2. `mv squashfs-root orca-root`
3. `./orca-root/AppRun --help |& head -n 40 | tee out/fx5/G/orca-help.txt` (written only for the record: which options the build lists).
4. `(./orca-root/AppRun |& tee out/fx5/G/orca-start.log) &` then wait 60 s.
5. `xwd -root | convert xwd:- out/fx5/G/orca-window.png`; `xdotool search --name "" getwindowname %@ | tee out/fx5/G/orca-windows.txt` (the window list; the Orca main window title is read off it).
6. If a first-run wizard appears (printer/filament choice): go through it with the first printer offered, screenshot each page as out/fx5/G/orca-wizard-N.png, write the choice into out/fx5/G/orca-wizard.txt. Do not install any network profile.
7. With the main window up: File, Import (or the build's own open item; record the exact item text) the lesson-5 hook 3MF from out/fx5/A if take A has run, else any 3MF in the image; `xwd` as out/fx5/G/orca-model.png. The 3D view must show the part (Mesa renders) for PASS.
8. Help, About (or the build's own About item): screenshot out/fx5/G/orca-about.png; write the version string to pins.txt.
9. Leave the window open and run, for the record, from a second shell: `./orca-root/AppRun --single-instance |& head -n 5 | tee out/fx5/G/orca-single-instance.txt` (EXPECTED "Invalid option", PLAN §5.1 / ACCURACY row F.4: PrintConfig.cpp 10948-10952 commented out, Config.cpp read_cli prints "Invalid option --"). Then screenshot out/fx5/G/orca-after-flag.png (did the flag start a second window, or nothing?).
10. Close Orca (window close; if it hangs, `pkill -f orca-root`); `tail -n 30 out/fx5/G/orca-start.log`.
11. Repeat 1-10 for Bambu Studio (bambu-root, bambu-* files; the About item and the wizard are Bambu's own; --single-instance EXPECTED "Invalid option", Bambu master PrintConfig.cpp 10305-10309).

(c) Events: `orca: started`, `orca: window up`, `orca: model rendered`, `orca: single-instance flag`, `orca: closed`; `bambu: started`, `bambu: window up`, `bambu: model rendered`, `bambu: single-instance flag`, `bambu: closed`. Any `... : no window after 60 s` or `... : crashed` is logged with the last log line.

(d) Capture: orca-extract.txt, orca-help.txt, orca-start.log, orca-window.png, orca-windows.txt, orca-wizard-N.png, orca-wizard.txt, orca-model.png, orca-about.png, orca-single-instance.txt, orca-after-flag.png; the same with bambu-; pins.txt; out/fx5/G/RESULT.txt with one line per slicer: `orca: PASS` / `orca: FAIL (reason)`, `bambu: PASS` / `bambu: FAIL (reason)`.

(e) EXPECTED: starts and renders: measure (PLAN §0.3: "Neither is tested in the Xvfb container"). `--single-instance`: "Invalid option" (source, ACCURACY F.4). The help text: measure.

(f) PASS/FAIL rule (the gate):
- orca: PASS = the main window is up within 60 s and the imported part is drawn in the 3D view (orca-model.png shows geometry, not a black or empty view). FAIL = no window, a crash in orca-start.log, or an empty 3D view after 120 s.
- bambu: the same rule, scored separately.
- What each outcome means (PLAN §5.8 gate, SCRIPT header, §0.3 row "Bambu Studio / OrcaSlicer second window"):
  - orca PASS (bambu either): take C runs for OrcaSlicer. CUT A is possible: title A, thumbnail A, description line 1 (A); F0 opens on `orca send 2: second window`; F6 becomes [REC] take C; F0 and F6 take the cut-A alternate narrations; retime.py rerun for cut A (SCRIPT: end 3:40.6, share 71%). The lab reports cut A as available; the owner still decides whether to ship A or B.
  - orca FAIL and bambu PASS: take C runs for Bambu Studio only, with Bambu's labels ("Keep only one Bambu Studio instance"); cut A as above with Bambu's footage in F0/F6 and the F4/F6 narration naming Bambu first (the owner decides; the script's cut-A cells are written for Orca and need a word swap, within two words, before retime.py).
  - both FAIL: take C is "not run". CUT B only: title B, thumbnail B, description line 1 (B); F6 stays [DIA]; the long video stays HELD (owner decision: ship cut B or record Bambu Studio on their PC). The Short fx5-01-reload ships from takes A and B regardless of G.
- G never blocks A and B. The --single-instance text is recorded for the description either way; if the text differs from "Invalid option", the description quotes the real text and the "Do not say" line "SolidCraft can turn it on" is kept only if the flag did not start a hand-over (orca-after-flag.png decides).

### Take A: PrusaSlicer 2.9.2: send, change, resend, Reload from disk, size boxes (Short S0/S2; cut B F0, F1, F5, F7, F8, F11, F12)

(a) Starting state: fresh home; SolidCraft 0.28.0 installed as in lesson 5; PrusaSlicer 2.9.2 AppImage extracted and on PATH as lesson 5 had it (so SolidCraft finds it); the MK4S stock presets already chosen in a first PrusaSlicer start, then PrusaSlicer closed; ~/hook-lesson4.sc present, hook_depth 25, SAVED (open it in SolidCraft, Ctrl+S once, confirm the title bar shows no unsaved mark); ~/.cache/solidcraft/slicer absent (`ls ~/.cache/solidcraft |& tee out/fx5/A/cache-before.txt`). No slicer window open. SolidCraft open on the hook, Body1 visible, the lesson-5 print face chosen in the Send dialog once before recording (so the dialog shows it as in lesson 5; record which face).

(b) Steps, in order (clicks are written as the on-screen item text; every item text is read off the screen, not assumed):
1. Right-click Body1, Send to Slicer. Screenshot the Send dialog: out/fx5/A/send-dialog-1.png (slicer field, format field, print face). Click Send. Event `send 1: Send clicked`.
2. PrusaSlicer opens with the hook. Wait until the sidebar shows the object. Screenshot out/fx5/A/send1-slicer.png. Event `send 1: slicer opened (25)`. Read the size boxes aloud into events.txt as `size boxes: 25 (X x Y x Z as shown)`.
3. `ps -o pid,args -C prusa-slicer | tee out/fx5/A/ps-send1.txt` (the exact command line SolidCraft used; EXPECTED to contain `--single-instance`, slicers.rs).
4. In SolidCraft: set hook_depth to 40 (the same field lesson 5 edited). Event `hook_depth: 40 typed`. Ctrl+S (the design stays saved under the same path). Screenshot out/fx5/A/hook-40.png.
5. Right-click Body1, Send to Slicer, Send. Event `send 2: Send clicked`. Do not touch PrusaSlicer for 10 s.
6. Screenshot out/fx5/A/send2-slicer.png at +3 s and out/fx5/A/send2-slicer-10s.png at +10 s. Score the window (rule f) and log ONE of: `send 2: slicer still 25` (B1), `send 2: second copy` (B2), `send 2: replaced` (B3: the object changed to 40 without a reload). Also `xdotool search --name PrusaSlicer | wc -l | tee out/fx5/A/windows-send2.txt` (EXPECTED 1 window).
7. `ps -o pid,args -C prusa-slicer | tee out/fx5/A/ps-send2.txt` (EXPECTED: the same pid as step 3, one process).
8. In PrusaSlicer: right-click the hook object in the 3D view. Event `right-click: menu open`. Screenshot out/fx5/A/menu.png with the menu fully open. Read the reload item text off the screen into events.txt as `menu text: "..."` (EXPECTED "Reload from disk", GUI_Factories.cpp at version_2.9.2, ACCURACY row C/F). In B2: first delete the extra copy (select it, Delete key), event `extra copy: deleted`, then right-click the first.
9. Click that item. Event `reload: done (40)` when the shape changes. Screenshot out/fx5/A/reload-done.png. If a dialog appears during reload (any text): screenshot out/fx5/A/reload-dialog.png and type its exact text into events.txt before clicking anything.
10. Read the size boxes: screenshot out/fx5/A/size-boxes-40.png; event `size boxes: 40`; write the three numbers into events.txt as shown. Confirm the print face: the orientation in the 3D view is the same as after send 1 (compare send1-slicer.png); event `print face: kept` or `print face: changed`.
11. Hold the slicer idle for 15 s (F12 outro footage), cursor still.
12. The command palette: in SolidCraft, open the command palette (the lesson-5 key), type `file.send_to_slicer`, open its help. Screenshot out/fx5/A/palette-help.png (every scrollable part: -1, -2, ...). Transcribe the help text verbatim into out/fx5/A/palette-help.txt (typed by hand from the screen; no OCR).
13. The consent prompt (no-AI): with SolidCraft still open and PrusaSlicer open, run the lesson-5 no-AI test script that calls SolidCraft's send-to-slicer tool through its MCP server (the script as the lab has it from lesson 5; the tool name as that script has it; copied to out/fx5/A/noai-send.py; run with `python3 -I out/fx5/A/noai-send.py |& tee out/fx5/A/noai-send.txt`). Watch the SolidCraft window for 10 s. Screenshot out/fx5/A/consent.png at +3 s. Event `agent send: consent prompt shown` (type its exact text and buttons into events.txt) or `agent send: no prompt`. Record the tool's reply text (noai-send.txt). If the script is not available in the lab: stop rule A3.
14. Close PrusaSlicer, close SolidCraft. `ls -l ~/.cache/solidcraft/slicer | tee out/fx5/A/ls-after.txt`.

(c) Events: `send 1: Send clicked`, `send 1: slicer opened (25)`, `hook_depth: 40 typed`, `send 2: Send clicked`, `send 2: slicer still 25` / `send 2: second copy` / `send 2: replaced`, `extra copy: deleted` (B2 only), `right-click: menu open`, `reload: done (40)`, `size boxes: 40`, `print face: kept` / `print face: changed`, `agent send: consent prompt shown` / `agent send: no prompt`.

(d) Capture: screen.mp4, typescript, events.txt, cache-before.txt, send-dialog-1.png, send1-slicer.png, ps-send1.txt, hook-40.png, send2-slicer.png, send2-slicer-10s.png, windows-send2.txt, ps-send2.txt, menu.png, reload-dialog.png (if any), reload-done.png, size-boxes-40.png, palette-help-N.png, palette-help.txt, noai-send.py, noai-send.txt, consent.png, ls-after.txt.

(e) EXPECTED:
- size boxes after send 1: 25 x 20 x 60 (SCRIPT §0 take A "expected 25 x 20 x 60"); measure.
- the second send's effect: measure (ACCURACY row F.6 "lab: measure (Q9)"); the plan carries narrations for B1 (still 25), B2 (second copy) and B3 (replaced).
- window count after send 2: 1 (slicers.rs passes --single-instance to PrusaSlicer; file.rs line 71: "PrusaSlicer, SuperSlicer and Cura load the file in the window that is open").
- menu text: "Reload from disk" (GUI_Factories.cpp at version_2.9.2, ACCURACY row C); must be read off the screen.
- size boxes after reload: 40.00 where 25 was (SCRIPT F8 "[lab: 40.00 mm where 25 was]"); measure.
- print face: kept (PLAN §5.6 step 4); measure.
- palette help: expected to match file.rs line 71: `single_instance?: bool` default true, "PrusaSlicer, SuperSlicer and Cura load the file in the window that is open"; "The file name stays the same for the same design and bodies, so sending again replaces it (use the slicer's Reload from disk)"; format default 3mf "in millimetres" (ACCURACY row F.1); the on-screen words are quoted as seen.
- consent prompt: none expected (lesson 5: "no such prompt appeared in our two runs", PLAN §5.1); measure.

(f) PASS/FAIL:
- B1 (window still shows 25 after 10 s, one object, one window): F0 and F5 use the default narration ("The slicer still shows the old shape" / "leaves the old shape"); label "old shape"; S0 as written.
- B2 (two hooks in the window): F0 takes the cut-B2 alternate narration, label "two copies"; F5 clause "adds a second copy beside the first"; F1 shows the extra copy deleted; S0 text "Sent 40. Shows 25." stays only if the first copy still reads 25 when selected (check the size boxes with the first copy selected, screenshot out/fx5/A/send2-first-selected.png); otherwise S0 is re-cut on the second copy's boxes and the Short narration is flagged for the script gate.
- B3 (the window shows 40 without a reload, one object): the F0 premise fails for PrusaSlicer. F5 clause "replaces it"; F0/F1/S0/S2 cannot be filmed as written: STOP (rule A1), report; the plan's Short premise is then wrong for PrusaSlicer and the owner decides.
- A second PrusaSlicer window after send 2 (windows-send2.txt 2 or more): STOP (rule A2); the single-instance claim for PrusaSlicer fails on screen and F4/F5 need a rewrite.
- Menu text not "Reload from disk": the text as seen replaces it on F1/S2 labels and in §5.6; the "Do not say" line is honoured (quote the screen); the lab reports the exact words.
- Size boxes after reload not 40 where 25 was: re-do the take once from step 1 on a fresh home; if the same, STOP (rule A1).
- Consent prompt shown: F9 outcome C's "if one appears this time we show it" applies; the prompt's text is filmed and added to the R1 expectations; the description line "SolidCraft's docs say it asks" is rewritten to "it asked".

### Take B: the hand-over folder across two sends (Short S1; cut B F2, F11 question)

(a) Starting state: the take-A home may be reused ONLY if the design is still saved and SolidCraft was restarted in between (the stem must hold across a restart for a saved design; that is part of the test). Default: fresh home, hook-lesson4.sc copied and SAVED, hook_depth 25, PrusaSlicer closed, SolidCraft open on the hook. A terminal is on screen beside SolidCraft (the F2 left pane: terminal crop at most three lines, so the terminal font is large enough to read after the crop).

(b) Steps:
1. `ls -l ~/.cache/solidcraft/slicer |& tee out/fx5/B/ls-0.txt` (EXPECTED: no such directory, or empty; the 7-day sweep is not filmed).
2. Right-click Body1, Send to Slicer, Send. Event `send 1: Send clicked`. Wait for PrusaSlicer.
3. `ls -l ~/.cache/solidcraft/slicer | tee out/fx5/B/ls-1.txt`. Event `ls 1: listed`. Screenshot out/fx5/B/ls-1.png. `ls -l --time-style=full-iso ~/.cache/solidcraft/slicer | tee out/fx5/B/ls-1-full.txt` (second-resolution times for the table; the on-screen listing is the plain `ls -l`).
4. In SolidCraft: hook_depth 40, Ctrl+S. Event `hook_depth: 40 typed`. Wait at least 61 s so the minute in `ls -l` changes (the plain listing shows minutes; the narration says "newer time"; if the two sends fall in the same minute the on-screen times would read the same).
5. Right-click Body1, Send to Slicer, Send. Event `send 2: Send clicked`.
6. `ls -l ~/.cache/solidcraft/slicer | tee out/fx5/B/ls-2.txt`. Event `ls 2: listed`. Screenshot out/fx5/B/ls-2.png. `ls -l --time-style=full-iso ~/.cache/solidcraft/slicer | tee out/fx5/B/ls-2-full.txt`. `sha256sum ~/.cache/solidcraft/slicer/* | tee out/fx5/B/sha-2.txt`.
7. The file name: `basename ~/.cache/solidcraft/slicer/*.3mf | tee out/fx5/B/name.txt`; check with `basename -s .3mf ~/.cache/solidcraft/slicer/*.3mf | grep -E -c '[0-9a-f]{16}$' | tee out/fx5/B/hash-check.txt` (EXPECTED 1: the stem ends in 16 hex digits, slicer_files.rs 49-66).
8. The F11 question, for the description: add a second body in SolidCraft (lesson-5 way; any name), send Body1 and the new body in two separate sends; `ls -l ~/.cache/solidcraft/slicer | tee out/fx5/B/ls-two-bodies.txt` (EXPECTED two files, two stems: the hash covers the sorted body names). Then send both bodies in one send: `ls -l ... | tee out/fx5/B/ls-both.txt` (EXPECTED a third stem). This step is for the description and the question's answer only; not footage.
9. The restart check: close SolidCraft, reopen hook-lesson4.sc, send Body1 once more: `ls -l ~/.cache/solidcraft/slicer | tee out/fx5/B/ls-after-restart.txt` (EXPECTED: the Body1 stem unchanged, saved design).
10. Close PrusaSlicer and SolidCraft.

(c) Events: `send 1: Send clicked`, `ls 1: listed`, `hook_depth: 40 typed`, `send 2: Send clicked`, `ls 2: listed`.

(d) Capture: screen.mp4, typescript, events.txt, ls-0.txt, ls-1.txt, ls-1.png, ls-1-full.txt, ls-2.txt, ls-2.png, ls-2-full.txt, sha-2.txt, name.txt, hash-check.txt, ls-two-bodies.txt, ls-both.txt, ls-after-restart.txt.

(e) EXPECTED: folder `~/.cache/solidcraft/slicer` (slicer_files.rs lines 14-15, `$XDG_CACHE_HOME/solidcraft/slicer`); one file after each send, same name, newer time (file.rs line 71 "The file name stays the same for the same design and bodies, so sending again replaces it"); the stem = sanitised design name plus 16 hex digits (slicer_files.rs 49-66); extension .3mf (format default 3mf, file.rs 71); the actual name and times: measure.

(f) PASS/FAIL: PASS = ls-2 lists exactly one file, same name as ls-1, newer time; then F2 and S1 are cut as written and the name goes into F2's "[lab: the folder and file name with its hash]". FAIL cases: two files after send 2 (a numbered copy or a new hash on Linux): F2's "nothing piles up" and S1's "same file name" are cut from the narration, the real listing is shown, retime.py rerun, and the lab reports the second name (the Windows stem-2 clause is then checked against what Linux did). Folder elsewhere than ~/.cache/solidcraft/slicer: card-folders-1 and the F2 spoken path take the real path; the description's "three hand-over folders" line is corrected. Stem without a 16-hex suffix: the F2 description "named after the saved design and the bodies" is kept only if the two-bodies step still gives distinct names; the hash wording is dropped from the description.

### Take C: OrcaSlicer (Bambu Studio) preference off, on, resend lands; only if take G passed for that slicer (cut A F0, F1, F4 bridge, F6)

(a) Starting state: fresh home; SolidCraft 0.28.0; the passing AppImage extracted as in G, with the wizard already completed (copy the G home's Orca config folder, path recorded in out/fx5/C/pins.txt) so no wizard appears on screen; hook-lesson4.sc SAVED, hook_depth 25; SolidCraft's Send dialog set to OrcaSlicer (the dialog's own slicer field; if a path must be typed, screenshot out/fx5/C/send-dialog-slicer.png and record it); no slicer window open. The same block is repeated for Bambu Studio in out/fx5/C-bambu/ if it passed G.

(b) Steps:
1. Preferences before anything: start Orca once by hand, open its Preferences (the build's own menu item; record the text), find the instance item. Screenshot out/fx5/C/prefs-default.png with the item and its checkbox visible. Write the exact label and its state into events.txt as `orca prefs label: "..." default: off/on` (EXPECTED "Allow only one OrcaSlicer instance", off; Preferences.cpp 1553-1562, AppConfig.cpp 171-172; Bambu: "Keep only one Bambu Studio instance", Preferences.cpp 1404, AppConfig.cpp 133-134). Hover for the tooltip, screenshot out/fx5/C/prefs-tooltip.png (EXPECTED tooltip "If this is enabled, when starting OrcaSlicer and another instance of the same OrcaSlicer is already running, that instance will be reactivated instead."). Leave it OFF. Close Orca. `grep -n single_instance ~/.config/OrcaSlicer/OrcaSlicer.conf |& tee out/fx5/C/conf-default.txt` (the config file path as the build really writes it; if elsewhere, `find ~ -name '*.conf' -newer out/fx5/C/prefs-default.png | tee out/fx5/C/conf-find.txt`).
2. In SolidCraft: right-click Body1, Send to Slicer, Send. Event `orca send 1: Send clicked`. Orca opens with the hook. Screenshot out/fx5/C/send1-orca.png. Event `orca send 1: window up`. `xdotool search --name OrcaSlicer | wc -l | tee out/fx5/C/windows-send1.txt`; `ps -o pid,args -C orca-slicer,OrcaSlicer |& tee out/fx5/C/ps-send1.txt` (the process name as the build has it; adjust and record).
3. hook_depth 40, Ctrl+S. Event `hook_depth: 40 typed`.
4. Right-click Body1, Send to Slicer, Send. Event `orca send 2: Send clicked`. Wait 20 s. Screenshot out/fx5/C/send2-orca.png (both windows in frame if two). `xdotool search --name OrcaSlicer | wc -l | tee out/fx5/C/windows-send2.txt`; `ps ... | tee out/fx5/C/ps-send2.txt`. Log ONE of: `orca send 2: second window` (two main windows), `orca send 2: still 25` (one window, old shape), `orca send 2: replaced` (one window, 40), `orca send 2: second copy` (one window, two objects).
5. If a second window: close the second window (the newer one; the ps order and the window stack decide; record which). Event `orca: close second`. Screenshot out/fx5/C/closed-second.png.
6. In the first window: right-click the object. Screenshot out/fx5/C/orca-menu.png. Read every item; write them into events.txt. If an item reads like a reload (any wording), click it and log `orca reload: "exact text"`; if none, File, Import the hand-over file again (or close and reopen; record the item texts) and log `orca reload: close and open the file again`. Screenshot out/fx5/C/orca-reload-done.png. Event `orca reload`. Read the size boxes (Orca's own sidebar; screenshot out/fx5/C/orca-size-40.png).
7. Preferences: turn the instance item ON. Screenshot out/fx5/C/prefs-on.png. Event `orca prefs: on`. Apply/OK as the dialog has it. `grep -n single_instance ...conf | tee out/fx5/C/conf-on.txt` (EXPECTED the key set to 1/true). Keep this one Orca window open.
8. In SolidCraft: hook_depth 30, Ctrl+S (a third value so a landed file is visibly different). Right-click Body1, Send to Slicer, Send. Event `orca send 3: Send clicked`. Wait 20 s. Screenshot out/fx5/C/send3-orca.png. `xdotool ... | tee out/fx5/C/windows-send3.txt`; `ps ... | tee out/fx5/C/ps-send3.txt`. Log ONE of: `orca send 3: lands in open window` (one window; the file opened there: either the shape updated, or Orca's own open/replace prompt appeared, screenshot out/fx5/C/send3-prompt.png with the exact text), `orca send 3: second window` (the preference did not take), `orca send 3: nothing` (one window, nothing changed after 20 s; then check `tail -n 20 out/fx5/C/orca-start.log`).
9. `tail -n 40 ~/.config/OrcaSlicer/log/* |& tee out/fx5/C/orca-log-tail.txt` (log path as the build has it; record).
10. Close everything.

(c) Events: `orca prefs label: "..." default: ...`, `orca send 1: Send clicked`, `orca send 1: window up`, `hook_depth: 40 typed`, `orca send 2: Send clicked`, `orca send 2: second window` / `orca send 2: still 25` / `orca send 2: replaced` / `orca send 2: second copy`, `orca: close second`, `orca reload`, `orca prefs: on`, `orca send 3: Send clicked`, `orca send 3: lands in open window` / `orca send 3: second window` / `orca send 3: nothing`.

(d) Capture: screen.mp4, typescript, events.txt, pins.txt, send-dialog-slicer.png, prefs-default.png, prefs-tooltip.png, conf-default.txt, send1-orca.png, windows-send1.txt, ps-send1.txt, send2-orca.png, windows-send2.txt, ps-send2.txt, closed-second.png, orca-menu.png, orca-reload-done.png, orca-size-40.png, prefs-on.png, conf-on.txt, send3-orca.png, send3-prompt.png (if any), windows-send3.txt, ps-send3.txt, orca-log-tail.txt.

(e) EXPECTED: preference off by default (AppConfig.cpp 171-172, Orca v2.4.2; ACCURACY F.4); label "Allow only one OrcaSlicer instance" (Preferences.cpp 1553-1562); send 2 with it off: a second window ("expected: yes", PLAN §0.4 Q9; the narration keeps "may"); send 3 with it on: lands in the open window ("expected: yes, GUI_Init.cpp 47-48 calls instance_check at every start", InstanceCheck.cpp 296-357); Orca's reload menu text: UNCONFIRMED, measure (SCRIPT §0 take C); size boxes in Orca: measure.

(f) PASS/FAIL:
- Second window on send 2 AND lands in the open window on send 3: cut A fully confirmed: F0 cut-A narration, F6 [REC] with the cut-A narration and "[lab: confirm]" filled "confirmed", F4 card-knock-5 as written; retime.py rerun for cut A.
- Second window on send 2 but send 3 does NOT land (second window again, or nothing): F6's last clause "the next send lands in the open window" is cut; card-knock-5 "turn it on" is cut from F4 and the narration loses "Turn it on yourself ... on screen" (retime.py); §5.6 step 2 keeps only "close the extra window and open the file again"; the description's "real fix" line is rewritten to what was seen; the lab reports the conf-on.txt value and the log tail so the plan can say whether the preference was read.
- No second window on send 2 with the preference off (still 25 / replaced / second copy): the cut-A F0 premise fails; cut A is not available from Orca; the long video stays cut B with F6 [DIA] rewritten from "not filmed on Linux" to what was filmed ("one window, old shape" or as seen), which is a script change for the gate; "may open a second window" stays in F4 as the source-based clause only if the lab cannot explain the difference (record orca-start.log around send 2).
- Orca reload item exists with its own words: the words go into F6's cut-A cell and §5.6 step 2 "(their reload menu text is unconfirmed)" is replaced; the "Do not say" line stays for Bambu unless its take reads one too.
- Label text differs from "Allow only one OrcaSlicer instance": the screen text replaces it on card-knock-4, F4 narration (within two words), §5.6, the description and the "Do not say" list.

### R1: the Claude run, see section 4.

## 4. The Claude run R1 (pre-registered)

Prompt, one wording only, typed as the first and only message: `Change hook_depth to 40 and send it to the slicer again.`

State before the run: fresh home (not take A's); SolidCraft 0.28.0 open on hook-lesson4.sc, SAVED, hook_depth 25; SolidCraft's MCP server connected to Claude Code exactly as lesson 5 (`claude mcp list | tee out/fx5/runs/R1/mcp-list.txt` must show the SolidCraft server connected before the prompt); PrusaSlicer 2.9.2 open from a first send done BY HAND before the run (right-click Body1, Send to Slicer, Send; so "again" is true and the window shows 25; screenshot out/fx5/runs/R1/before-slicer-25.png); `claude` started in ~/fx5-run (empty folder), auto mode as lesson 7 (the same flag lesson 7 used, written to pins.txt), model as the default of the build (read back from session.jsonl; EXPECTED claude-sonnet-5-5); Claude Code build: `claude --version | tee out/fx5/runs/R1/pins.txt`. No system prompt, no CLAUDE.md, no prior messages.

Run: type the prompt, event `claude: typed`; wait until the reply ends, event `turn 1: reply done`; screenshot out/fx5/runs/R1/reply.png (full reply; the greyed suggested next prompt is in the raw screenshot and is cropped out in the cut, crop box noted in out/fx5/runs/R1/crop.txt); screenshot the PrusaSlicer window at `turn 1: reply done` + 10 s, out/fx5/runs/R1/slicer-after.png, and after a by-hand Reload from disk, out/fx5/runs/R1/slicer-after-reload.png with the size boxes. No second message. Exit claude. Copy the session file (`cp ~/.claude/projects/*/*.jsonl out/fx5/runs/R1/session.jsonl`; the path as lesson 7 found it), `claude` cost line from the exit screen into out/fx5/runs/R1/cost.txt, the model from session.jsonl into pins.txt, the tool calls (name and arguments, in order) into out/fx5/runs/R1/tools.txt, the reply verbatim into out/fx5/runs/R1/reply.txt, SolidCraft's tool reply text (what the send tool returned) into out/fx5/runs/R1/tool-reply.txt.

Outcome classes (PLAN §5.7, SCRIPT §0 R1), scored on reply.txt and tools.txt only:
- A: the tool calls include a change of hook_depth to 40 and a send; the reply says to reload the slicer (or to close and reopen it, or that the slicer may still show the old shape). Storyboard: F9 outcome A narration; label "matches" if the evidence frame (F8 `size boxes: 40`, take A) shows 40 after a reload, which it does by construction, so A gives "matches".
- B: the tool calls include the change and the send; the reply states or implies that the slicer now shows 40 (any wording that reports the slicer's state) without a reload instruction. Storyboard: F9 outcome B narration; the evidence frame is take A's `size boxes: 40` AFTER reload beside the R1 slicer-after.png BEFORE reload: label "does not match" if slicer-after.png still reads 25 (expected from take A B1), "matches" if PrusaSlicer replaced the object by itself (take A B3; then the half-answer clause is kept because Claude still had no evidence).
- C: the reply asks a question before sending (consent or clarification), or SolidCraft shows a consent prompt and Claude waits. Storyboard: F9 outcome C narration; label "matches"; the prompt text filmed if SolidCraft's.
- Not A/B/C (no send at all, an error, a refusal): recorded as D with the reply; F9 is cut to "It did not send the file" and the rest of F9 is re-written at the script gate; no second run.

Evidence frame: F8 size boxes (take A `size boxes: 40`). The split screen shows R1's reply on the left and that frame on the right with one label, "matches" or "does not match", as scored above.

Rule: one run, scored before it runs, no second try. A crash of claude before the reply ends is a stopped run, reported as such with the session file; it is not re-run inside this pre-registration.

## 5. Measurements table

| value | where it is used | how measured | expected | source |
|---|---|---|---|---|
| Claude Code exact build | SCRIPT §0 pins; description "Tested:" | `claude --version` at R1 start, pins.txt | 2.1.31x | PLAN §0 pins; measure |
| R1 model | SCRIPT §0 pins; F9 chip | session.jsonl model field | claude-sonnet-5-5 | lesson 7 (SCRIPT-L7 §0); measure |
| Lab folder | SCRIPT §0 pins | this file | out/fx5/ | this file |
| Size boxes after send 1 | SCRIPT §0 take A; F5 "first send"; S0 "Shows 25" | take A step 2, send1-slicer.png, events `size boxes: 25` | 25 x 20 x 60 | SCRIPT §0 "expected 25 x 20 x 60"; measure |
| PrusaSlicer's behaviour on send 2 (B1 still 25 / B2 second copy / B3 replaced) | F0 narration choice and label; F5 clause; S0 | take A step 6, send2-slicer-10s.png, windows-send2.txt, ps-send2.txt | measure | ACCURACY F.6 "lab: measure" |
| PrusaSlicer window count after send 2 | F5 "no second window"; F4 card-knock-1 | windows-send2.txt | 1 | slicers.rs (--single-instance passed); file.rs 71 |
| PrusaSlicer command line from SolidCraft | F5 on-screen note "started by SolidCraft with --single-instance" | ps-send1.txt | contains --single-instance | slicers.rs v0.28.0 (ACCURACY F.3) |
| Right-click menu text | F1 zoom label; S2 label; §5.6 step 1 | take A step 8, menu.png, read off the screen | "Reload from disk" | GUI_Factories.cpp at version_2.9.2 (ACCURACY row C, F.6); confirm on screen |
| Size boxes after reload | F8 "[lab: 40.00 mm where 25 was]"; F9 evidence frame; S2 "40" | take A step 10, size-boxes-40.png | 40.00 where 25 was | SCRIPT F8; measure |
| Print face kept after reload | F8 "the print face from lesson five kept" | take A step 10, compare send1-slicer.png and reload-done.png | kept | PLAN §5.6 step 4; measure |
| Consent prompt before an agent's send | SCRIPT §0 take A; F9 outcome C; description | take A step 13 consent.png; R1 | none | PLAN §5.1 lesson 5 "no such prompt"; measure |
| `file.send_to_slicer` help text in the palette | SCRIPT §0 take A; §5.1; description | take A step 12 palette-help.txt, transcribed | matches file.rs line 71 wording | ACCURACY F.1 (raw file.rs at v0.28.0); quote the screen |
| Hand-over folder path | F2 terminal, card-folders-1, F2 narration; S1 | take B ls-1.txt | ~/.cache/solidcraft/slicer | slicer_files.rs 14-15 (ACCURACY F.2); measure |
| Hand-over file name (stem + 16 hex + .3mf) | F2 "[lab: the folder and file name with its hash]"; S1 | take B name.txt, hash-check.txt | design name + 16 hex digits + .3mf | slicer_files.rs 49-66; measure |
| Two `ls -l` times, one file | F2 "same name, newer"; S1 | take B ls-1.txt, ls-2.txt, ls-1-full.txt, ls-2-full.txt | one file, same name, newer time | file.rs 71 "sending again replaces it"; measure |
| Two bodies: one file or two | F11 question's answer (description) | take B ls-two-bodies.txt, ls-both.txt | two stems; a third for both together | slicer_files.rs 49-66 (sorted body names in the hash); measure |
| Stem after SolidCraft restart (saved design) | description "an unsaved design gets a new name after SolidCraft restarts" (contrast) | take B ls-after-restart.txt | unchanged | slicer_files.rs (saved path hashed); measure |
| Orca AppImage starts and renders in Xvfb | cut A vs cut B; F6 type; title/thumbnail choice | take G orca-window.png, orca-model.png, RESULT.txt | measure | PLAN §0.3 "neither is tested"; Q9 |
| Bambu Studio AppImage starts and renders | the same, Bambu line | take G bambu-* | measure | Q9 |
| Orca and Bambu version strings | description "Tested:" | take G orca-about.png, pins.txt | measure | not pinned |
| `--single-instance` on Orca's command line | description; "Do not say" "SolidCraft can turn it on"; §5.1 | take G orca-single-instance.txt | "Invalid option" | PrintConfig.cpp 10948-10952, Config.cpp read_cli (ACCURACY F.4) |
| `--single-instance` on Bambu's command line | description | take G bambu-single-instance.txt | "Invalid option" | Bambu master PrintConfig.cpp 10305-10309 |
| Orca preference label | card-knock-4; F4 and F6 narration; §5.6 step 2 | take C prefs-default.png | "Allow only one OrcaSlicer instance" | Preferences.cpp 1553-1562 v2.4.2 |
| Orca preference default | card-knock-5 "off by default"; F6 | take C prefs-default.png, conf-default.txt | off | AppConfig.cpp 171-172 |
| Orca preference tooltip | description | take C prefs-tooltip.png | "If this is enabled, when starting OrcaSlicer and another instance of the same OrcaSlicer is already running, that instance will be reactivated instead." | Preferences.cpp (ACCURACY F.4) |
| Bambu preference label and default | card-knock-4; description | take C-bambu prefs-default.png | "Keep only one Bambu Studio instance", off | Bambu Preferences.cpp 1404, AppConfig.cpp 133-134 |
| Second window on send 2, preference off | cut-A F0, F4 bridge, F6 | take C send2-orca.png, windows-send2.txt | second window (narration keeps "may") | Q9 "expected: yes"; measure |
| Orca reload menu text | F6 cut A; §5.6 step 2; "Do not say" | take C orca-menu.png | UNCONFIRMED, measure | SCRIPT §0 take C |
| Send 3 with the preference on | F6 cut A "[lab: confirm]"; card-knock-5 | take C send3-orca.png, windows-send3.txt | lands in the open window | GUI_Init.cpp 47-48, InstanceCheck.cpp 296-357; measure |
| R1 outcome A/B/C | F9 narration choice | reply.txt, tools.txt, scored by section 4 | measure | PLAN §5.7 |
| R1 reply words | F9 type-on | reply.txt | measure | lab |
| R1 cost and model | SCRIPT §0 R1 | cost.txt, session.jsonl | measure | lab |
| R1 evidence frame matches / does not match | F9 label | section 4 rule, slicer-after.png vs take A size-boxes-40.png | measure | PLAN §5.7 "The size boxes decide" |
| SolidCraft tool reply on send | F9 outcome B clause "SolidCraft only told it the file was written" | tool-reply.txt, noai-send.txt | says the file was written, nothing about the slicer | PLAN §5.7; measure |

## 6. Stop rules

- G1: an AppImage will not extract or AppRun exits at once (missing libraries in orca-start.log): try once more after installing the named library in the image (recorded in out/fx5/G/image-fixes.txt, max 2 attempts), then score FAIL for that slicer; cut B; the plan's fallback: "not run", F6 [DIA], title B (PLAN §5.8 gate).
- G2: the window starts but the 3D view stays empty or black after 120 s with LIBGL_ALWAYS_SOFTWARE=1: FAIL for that slicer (no footage of a part is usable); same fallback.
- G3: a first-run wizard needs a network profile download the container cannot reach: pick any offline printer; if none can be chosen offline, FAIL with the wizard screenshot.
- A1: PrusaSlicer shows 40 without a reload (B3) or the size boxes do not read 40 after the reload on a second fresh-home take: stop; report; the Short's premise is in question and the owner decides (no fallback named in the plan).
- A2: a second PrusaSlicer window opens on send 2: stop; report with ps-send2.txt; F4/F5 claim a single instance for PrusaSlicer and must be rewritten.
- A3: the lesson-5 no-AI send script is not in the lab repo: skip step 13, mark the consent-prompt measurement "from R1 only", report.
- A4: PrusaSlicer's first start shows a configuration wizard the lesson-5 image did not have: complete it with MK4S stock presets off-camera before the take; if the presets are absent, stop.
- A5: the right-click menu has no reload-like item at all: stop; screenshot; report (the storyboard's fix sentence depends on it).
- A6: SolidCraft's Send dialog differs from lesson 5 (no print-face choice, no slicer field, different button text): screenshot, record the texts, continue; the lab reports the differences for the script gate.
- B1: the hand-over folder is not under ~/.cache (XDG_CACHE_HOME found set in the container): unset it, fresh home, re-do once; if still elsewhere, record the real path, continue, report.
- C1: SolidCraft cannot be pointed at OrcaSlicer (no entry for it in the Send dialog, or it does not find the extracted AppRun): try the AppRun path in the dialog's field or a symlink named as SolidCraft expects (recorded); max 2 attempts; then take C is "not run (SolidCraft could not start Orca)" and the gate falls to cut B even though G passed; report with send-dialog-slicer.png.
- C2: Orca shows a modal on the second send (any dialog text) instead of a window: screenshot, type the text, click nothing for 10 s, then the dialog's default button; record which; continue.
- R1-1: `claude mcp list` does not show the SolidCraft server connected: fix the connection as lesson 5 did, off-camera, before typing the prompt; the prompt is not typed until it is connected.
- R1-2: claude crashes or the reply never ends within 10 minutes: stop the run, keep session.jsonl, report "stopped run"; no second run under this file.
- Windows-only steps (the stem-2 numbered copy; %LOCALAPPDATA%): not attempted; card-folders-2/-4 stay "from SolidCraft's code".
- Any dialog whose text differs from an EXPECTED quote: screenshot, type the text verbatim into events.txt, continue with the dialog's default button, and flag the row in the report; the storyboard quotes the screen.
- Anything else unexpected: stop the take, write out/fx5/DEVIATIONS.md, report; do not improvise a different route.

## 7. Deliverables back to Cowork

Files (all under solidcraft-course-lab out/fx5/): G/RESULT.txt, G/pins.txt, G/orca-*.{png,txt,log}, G/bambu-*; A/events.txt, A/screen.mp4, A/send1-slicer.png, A/send2-slicer-10s.png, A/menu.png, A/size-boxes-40.png, A/palette-help.txt and palette-help-N.png, A/consent.png, A/noai-send.txt, A/ps-send1.txt, A/windows-send2.txt; B/events.txt, B/screen.mp4, B/ls-1.txt, B/ls-2.txt, B/ls-1.png, B/ls-2.png, B/name.txt, B/hash-check.txt, B/ls-two-bodies.txt, B/ls-both.txt, B/ls-after-restart.txt; C/events.txt, C/screen.mp4, C/prefs-default.png, C/prefs-tooltip.png, C/send2-orca.png, C/orca-menu.png, C/prefs-on.png, C/send3-orca.png, C/conf-default.txt, C/conf-on.txt (and C-bambu/ the same) or C/NOT-RUN.txt with the G reason; runs/R1/pins.txt, session.jsonl, cost.txt, tools.txt, reply.txt, reply.png, crop.txt, tool-reply.txt, before-slicer-25.png, slicer-after.png, slicer-after-reload.png; DEVIATIONS.md (may be empty); the prereg commit hash of this file and the commit hash of the results.

One-line answers to section 2 (filled by the lab, one line each):
- Q9 Orca/Bambu: "OrcaSlicer VERSION: runs / does not run in Xvfb (reason); Bambu Studio VERSION: runs / does not run; cut A available / not available."
- Q9 preference: "label as seen: '...'; default as seen: off/on; send 2 with it off: second window / one window (what); send 3 with it on: lands in the open window / does not (what); --single-instance: 'exact text'."
- Q9 PrusaSlicer send 2: "B1 still 25 / B2 second copy beside the first / B3 replaced; windows: N; command line contained --single-instance: yes/no."
- Q9 menu text: "right-click item reads '...' on the 2.9.2 screen."
- Q9 folder and name: "folder: PATH; file: NAME; ls -l times: T1, T2; one file after send 2: yes/no; two bodies: two files / one."
- Q9 palette help: "quoted verbatim in A/palette-help.txt; matches file.rs line 71: yes / differs at: ...".
- Q9 consent prompt: "none / shown with text '...' (no-AI script; R1)."
- Q11: "R1 outcome A/B/C/D; model; cost; reply in runs/R1/reply.txt; evidence frame F8 size boxes: matches / does not match; suggested prompt cropped: yes."
- Size boxes: "after send 1: X x Y x Z; after reload: X x Y x Z; print face kept: yes/no."
- Gate result: "cut A possible (Orca / Bambu filmed) / cut B only; Short fx5-01-reload footage complete: yes/no."
