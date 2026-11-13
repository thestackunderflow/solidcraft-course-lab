# fx12 lab: deviations from LAB-fx12.md v1 (pre-registration 0bd748b)

Nothing was re-scored or re-rolled. Every take is kept.

1. **Restart.** The first lab agent ended (login expiry) after take P and an unfilmed probe session (container fx12p,
   out/scratch/fx12p s0-s24, gitignored). The probe already showed the refusal, the Break, Fix 1 7,834.61 / 4.07 and the
   round-first R 3.00; those probe results are not scored. fx12p was inspected, stopped and removed; the takes were
   then filmed fresh, one container each, with the probe's positions (lab/fx12lib.sh, fx12 section).
2. **Where it ran / image.** All containers on the Ubuntu lab box (as fx10, fx11). env.txt: solidcraft 0.28.0.
3. **Association evidence.** The plug reports the offset association as an `offset_distance` constraint, not in
   `links` (always []). "Linked" in ANSWERS = that constraint present.
4. **Take B step 4 (Q11 Fix 1) attempt 1 failed.** After Properties, the double-click on Sketch1's Browser row did not
   enter Edit Sketch; Inspect > Measure stayed on "Select" and the clicks hit nothing (B/wall.png shows the empty
   panel). Attempt 2 = take **B-wall**: the same Fix 1 in a fresh window (Break, Fillet 3 on four corners), measured
   inside the sketch BEFORE Finish (the same curves; order differs from LAB step 3 -> 4). Min 4.07 mm.
5. **Take C step 5 (Q14)** ran by the plug only (C14/q14.py), not filmed. Attempt 1 (C14/attempt1/, C14-attempt1.log):
   a new 70 mm dimension between l2 and l4 was refused as over-constraining. Attempt 2 changed the existing width
   dimension d1 with `set_parameter` (a first run of attempt 2 died on a Python syntax error in my script before any
   call; fixed and run once).
6. **Take C step 6 (Q12)** filmed as take C2 (lab/fx12C.sh with RAD=1.5 TAKE=C2): the outline held 5 s before the
   Offset (S2 end frame). The Measure clicks found no inside arc to pick (sharp corners): C2/wall.png shows Item 1
   "Area 2016.00 mm2" (the inner region) and Item 2 a point at (28.50, 18.50), distance 0.71 mm: not a radius, not used.
7. **Take C step 7 (F10, box.sc)** not filmed (LAB: "logged only if time allows").
8. **Clips.** lab/fx12clips.py, tests/test_fx12clips.py (red: no module; then 3 pass). Run on the box with
   -v ~/jobs/box-test/video-qa:/footage:ro.
