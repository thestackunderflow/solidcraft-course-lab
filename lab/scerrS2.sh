#!/bin/bash
# scerr take S part 2: OK on PrusaSlicer's offline preset-download error (the container has no network; not a
# SolidCraft or 3MF message, cut from the clips), then the Size [World] row held 7 s: 25 x 20 x 60 mm, no inches dialog.
set -u
. /work/lab/scerrlib.sh
O=/work/out/scerr/S
ev "slicer: OK on the offline preset-download error (container has no network)"
g 820 463 16; click; nap 2.0
ev "slicer: Size row 25 x 20 x 60 mm held 7 s"
g 1320 258 20; nap 7.0
cp_shot slicer-size
ev "recording stopped"
rec_stop
cd /tmp && rm -rf m3 && mkdir m3 && cd m3 && python3 -c "import zipfile,glob;z=zipfile.ZipFile(glob.glob('/root/.cache/solidcraft/slicer/*.3mf')[0]);print([l for l in z.read('3D/3dmodel.model').decode().splitlines() if 'unit=' in l][0][:200])" > "$O/3mf-unit-line.txt"
cat "$O/3mf-unit-line.txt"
