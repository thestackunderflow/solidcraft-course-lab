# R1: stopped by us (lab fault, not a result)

R1 ran the pre-registered protocol (out/l7/prereg.json, commit 27d0db2) but the driver's approval matcher looked for
"solidcraft - " (a hyphen). Claude Code 2.1.311 writes the prompt as "solidcraft — Inspect the design Tool: (MCP)"
(an em dash), so the driver answered No to Claude's first SolidCraft call (approval-1-1.txt), against the policy. Claude
Code then showed "Interrupted · What should Claude do instead?" (pane-turn1.txt). In turn 2 the first prompt was a shell
command (`ls -d ~/Documents ...`, approval-2-1.txt), answered No as the policy says; we stopped the container there
(docker stop, 40 s into the recording). The ledger counts R1 at its $0.25 cap (killed-floor); its real cost was not
read. The matcher was fixed (lab/l7drive.py, tested on R1's own prompt files) and the same protocol re-ran as R2.
Nothing from R1 is narrated as Claude's behaviour.
