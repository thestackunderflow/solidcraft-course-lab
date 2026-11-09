#!/bin/bash
# scerr take M (error 5 re-check on 0.30.1, filmed): hook.stl (lesson 4's hook with holes + rounds, opened by the lab
# script before the take: no file window under Xvfb) refused by Convert Mesh (red line held 7 s); then hook-plain.stl
# (lesson 3's plain hook) opened by the lab script on camera and converted (timeline held).
#   docker exec scerr-s bash /work/lab/scerrM.sh
set -u
. /work/lab/scerrlib.sh
take M
[ -s "$O/events.txt" ] && { echo "refusing: $O/events.txt exists"; exit 1; }
still; sleep 1
rec_start
ev "recording started: hook.stl (a mesh) open in SolidCraft 0.30.1, full window"
nap 4.0
ev "convert: select the mesh body"
g 91 311 18; click; nap 1.0
ev "convert: Surface tab"
g 183 50 18; click; nap 1.2
ev "convert: Convert Mesh button"
g 684 92 18; click; nap 1.8
ev "convert: dialog held 3 s"
g 1300 330 12; nap 3.0
ev "convert hook.stl: OK"
g 1388 397 14; click; nap 0.6
still; nap 0.6
ev "convert hook.stl: refusal held 7 s"
nap 7.0
cp_shot refused
ev "convert: Cancel"
g 1322 475 14; click; nap 1.5
read_now m-refused
ev "plain hook: hook-plain.stl opened by the lab script"
open_file /root/hook-plain.stl
nap 3.0; still; nap 1.0
ev "convert plain: select the mesh body"
g 91 311 18; click; nap 1.0
ev "convert plain: Surface tab"
g 183 50 18; click; nap 1.2
ev "convert plain: Convert Mesh button"
g 684 92 18; click; nap 1.8
ev "convert plain: OK"
g 1388 397 14; click; nap 2.0
still; nap 0.5
ev "convert plain: converted, timeline held 5 s"
g 330 786 16; nap 5.0
cp_shot converted
ev "recording stopped"
rec_stop
read_now m-converted
echo "M done"
