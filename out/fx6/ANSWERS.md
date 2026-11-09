# fx6 lab answers (LAB-fx6.md v2, pre-registration 088b177; run 5 Nov 2026 04:16-04:40 UTC)

Pins: SolidCraft 0.28.0 (`solidcraft --version`), Claude Code 2.1.311, sc5-l5:0.28.0 = 2992c9ecbca2, sc5-app:0.28.0 =
55ad2987ef14 (env.txt). P0 passed. Deviations: DEVIATIONS.md (display 2880x1620; first-pass Ctrl+Z did not undo, so
4.9 and 5.1 re-run once on the clean hook).

| Q | Answer | Evidence |
|---|---|---|
| Q1 reason line | On screen, word for word: **"not supported yet: the blend is larger than the neighbouring faces; the largest radius that fits is 5 mm"** (B.1 plus a clause the plan did not expect: the app states the limit itself). Shown in: the Fillet panel, red text under Advanced, as soon as Radius 6 is typed (Preview on); OK is greyed, so nothing is added (no History or Browser mark). The panel offers **Create Issue...**; its draft's Summary is **"FILLET: operation failed"** (not submitted, draft closed). Stop rule A1 not hit (6 mm refused); A2 not hit (reason = B.1). | A/refusal.png, A/refusal-5s.png, A/report.png, A/events.txt |
| Q2 limit | Largest built **5.0**, smallest refused **5.1**; lip top face 5.0 mm. 4.0 built (1.0 mm of flat left), 4.9 built (0.1 mm left), **5.0 built: the round takes the whole top face** (a full round lip, 10 faces, 8,392.63 mm3), 5.1 refused with the same line. So "under 5" is not the rule on 0.28.0: **up to and including 5 mm** (radius = the face width) builds. | B/limit.txt, B/read-*.json, B/r-*.png |
| Q3 contrast | Thickness 5 to 8 in Parameters: lip top face **8.0 mm**, lip front face **10.0 mm**, the J's base 2 mm (inner floor at z = 2; logged). The same edge at 6 mm **builds** (r 6.000, 2.0 mm of flat left, 11,405.39 mm3). Filmed twice (C pass 1 with reads, C-clean for the split screen). C2 (thickness 5, bottom-back edge, back face 60 mm, underside 25 mm) at 6 mm also builds (blend on F2:side:l1/l8, r 6.000); not needed (C1 not hit). | C/, C-clean/, C2/ |
| Q4 pinned comment | Both lip top edges in one Fillet at **2.5 mm on thickness 5: builds** (two r 2.5 rounds meeting: no flat left on the 5 mm face, 8,446.31 mm3). 2.4 not tried. | C/both-2.5.png, C/read-both-2.5.json |
| Q5 MCP reply | `solid.fillet` with the edge's midpoint [25, -10, 10], radius 6: `isError: true`, one text: "not supported yet: the blend is larger than the neighbouring faces; the largest radius that fits is 5 mm" (the same words as the panel; no JSON fields such as ok/false). Corner point [25, 0, 10]: `isError: true`, "invalid parameters for `solid.fillet`: [25, 0, 10] is where 3 edges meet: give a point along one edge, such as its midpoint". Hook unchanged (8,500). Take-day count of "FILLET: operation failed" issues: **325**. | D/reply.txt, D/replies.json, D/count.txt |
| Q13 R1 | **Class A.** Claude read the design (inspect_design), tried solid.fillet radius 6 on [25, -10, 10] (the midpoint), got the refusal, applied nothing, quoted "SolidCraft reports 5 mm as the largest radius that fits", and asked: 5 mm (largest that fits), a thicker lip then 6 mm, or under 5 (e.g. 4). Model claude-sonnet-5-5, $0.1074, about 17 s. Recorded, not scored: it named the edge by its midpoint; it also ran `ls -la /root/hook` (auto mode); **one false line**: "the lip ... isn't driven by a parameter" (thickness drives it; Take C changes it in Parameters). Greyed suggestion "Use a 5 mm fillet" to crop (crop.txt). | runs/R1/reply.txt, tools.txt, after.png, cost.txt |

## Changes for the plan (rev 3 "lab fills")
- The on-screen line carries the limit: "...; the largest radius that fits is 5 mm". Title/description line 1 can quote
  the B.1 part; F0/F4 should show the whole line; the fix is told by the app itself.
- Q2: 5.0 builds (degenerate: no flat left). Say "5 mm or less" / "up to the face's width", not "just under five";
  thumbnail "RADIUS UNDER 5 MM" becomes e.g. "RADIUS 5 MM OR LESS" (5.1 is refused).
- The refusal is live in the panel (OK greyed), not after OK: F0 shows it appearing as 6 is typed.
- R1's "isn't driven by a parameter" is wrong: F9 should show it as a check-the-helper moment (or not quote it).
- MCP reply is plain text with isError true (no ok/false fields).

## Clips (out/fx6/clips, 1920x1080, silent; each NAME-full.mp4 = the whole window, NAME-zoom.mp4 = the close-up; spans and boxes in clips.json)
A-open-full-window, A-params-thickness5, A-refusal, A-reason-line, A-report-draft; B-r4.0, B-r4.9, B-r5.0, B-r5.1,
B-F2-radius5-clean; C-thickness8-row, C-thick8-fillet6, C-thickness5-back (from the C-clean pass); C2-bottom-back-6;
D-mcp-replies; R1-claude (crop the greyed "Use a 5 mm fillet" row).
