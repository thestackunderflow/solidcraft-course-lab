#!/bin/bash
# fx5 take G (LAB-fx5 section 3): does the OrcaSlicer / Bambu Studio Linux AppImage start and draw a part in Xvfb with
# Mesa software GL? One slicer per run (argument orca or bambu), fresh container = fresh home.
#   docker run --rm --memory 6g --shm-size 1g --network none -v "$PWD:/work" -v "$PWD/out/scratch/fx5-apps:/apps:ro" \
#     sc5-fx5:0.28.0 bash /work/lab/fx5G.sh orca
set -u
S=${1:?orca or bambu}
O=/work/out/fx5/G; mkdir -p "$O"
. /work/lab/common.sh
. /work/lab/l2common.sh
export LIBGL_ALWAYS_SOFTWARE=1 GDK_SCALE=2
unset XDG_DATA_HOME XDG_CACHE_HOME
E=$O/$S-events.txt; : > "$E"
ev() { printf '%s  %s\n' "$(date -u +%H:%M:%S.%1N)" "$1" | tee -a "$E"; }
case $S in
  orca)  SRC=$(ls /apps/OrcaSlicer_Linux_AppImage_*.AppImage | head -1); NAME=OrcaSlicer ;;
  bambu) SRC=$(ls /apps/BambuStudio_*.AppImage | head -1); NAME=BambuStudio ;;
esac
echo "$S: file $(basename "$SRC") sha256 $(sha256sum "$SRC" | cut -c1-64)" >> "$O/pins.txt"
mkdir -p ~/.config ~/apps && cp "$SRC" ~/apps/$S.AppImage && chmod +x ~/apps/$S.AppImage && cd ~/apps
eval "$(dbus-launch --sh-syntax)"
start_display
openbox > /dev/null 2>&1 &
sleep 1
./$S.AppImage --appimage-extract | tail -n 1 | tee "$O/$S-extract.txt"
mv squashfs-root $S-root || { ev "$S: extract failed"; echo "$S: FAIL (extract)" >> "$O/RESULT.txt"; exit 0; }
echo "$S: extracted to ~/apps/$S-root (AppRun)" >> "$O/pins.txt"
timeout 30 ./$S-root/AppRun --help |& head -n 40 | tee "$O/$S-help.txt" > /dev/null
( ./$S-root/AppRun |& tee "$O/$S-start.log" > /dev/null ) &
ev "$S: started"
up=
for i in $(seq 1 120); do
  w=$(xdotool search --onlyvisible --name "$NAME|Orca|Bambu" 2>/dev/null | head -1)
  [ -n "$w" ] && { up=1; break; }; sleep 1
done
sleep 20
shot "$O/$S-window.png"
xdotool search --onlyvisible --name "" 2>/dev/null | while read -r id; do printf '%s  %s\n' "$id" "$(xdotool getwindowname "$id")"; done | grep -v '  $' | tee "$O/$S-windows.txt" > /dev/null
if [ -n "$up" ]; then ev "$S: window up"; else ev "$S: no window after 120 s ($(tail -n 1 "$O/$S-start.log"))"; fi
pgrep -fa "$S-root" | head -5 > "$O/$S-ps.txt"
ev "$S: hold for the next step (wizard / import is done by fx5G-drive.sh in the same container)"
# keep the container alive for the driver: the driver writes $O/$S-done when finished
for i in $(seq 1 1800); do [ -f "$O/$S-done" ] && break; sleep 1; done
rm -f "$O/$S-done"
pkill -f "$S-root"; sleep 2
ev "$S: closed"
tail -n 30 "$O/$S-start.log" > "$O/$S-start-tail.txt"
