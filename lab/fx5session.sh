#!/bin/bash
# fx5 session (takes A, B, C, R1): a fresh home, the display, a session bus, PrusaSlicer's seeded settings, SolidCraft
# 0.28.0 on lesson 5's finished hook rebuilt with no AI (lab/l6part.py: lesson 4's hook + the J-side print face) and
# SAVED as ~/hook-lesson4.sc; optionally the OrcaSlicer AppImage extracted behind an `orca-slicer` launcher on PATH
# (slicers.rs looks for orca-slicer) with the G home's settings (wizard done). Then it waits; every step is a
# `docker exec NAME bash -c '. /work/lab/fx5lib.sh; ...'`. Touch $O/.end to finish.
#   docker run -d --name fx5-A --memory 6g --shm-size 1g --network none -v "$PWD:/work" \
#     -v "$PWD/out/scratch/fx5-apps:/apps:ro" sc5-fx5:0.28.0 bash /work/lab/fx5session.sh A [orca]
set -u
TAKE=${1:?take}; WITH=${2:-}
O=/work/out/fx5/$TAKE; mkdir -p "$O"; echo "$O" > /dev/null
mkdir -p /tmp/fx5; echo "$O" > /tmp/fx5/O
. /work/lab/fx5lib.sh
. /work/lab/l5slicerseed.sh
: > "$O/events.txt"
dbus-launch --sh-syntax > /tmp/fx5/bus; . /tmp/fx5/bus
mkdir -p "$HOME/.config/Claude" "$HOME/.claude"; echo '{}' > "$HOME/.claude.json"
solidcraft-cli mcp setup > "$O/setup.txt" 2>&1
seed_slicer
if [ "$WITH" = orca ]; then
  mkdir -p ~/apps ~/.config/OrcaSlicer && cd ~/apps
  cp /apps/OrcaSlicer_Linux_AppImage_*.AppImage orca.AppImage && chmod +x orca.AppImage
  ./orca.AppImage --appimage-extract > /dev/null && mv squashfs-root orca-root
  cp -a /work/out/scratch/fx5-orca-config/. ~/.config/OrcaSlicer/
  printf '#!/bin/sh\nexec /root/apps/orca-root/AppRun "$@"\n' > /usr/local/bin/orca-slicer; chmod +x /usr/local/bin/orca-slicer
  { echo "OrcaSlicer: $(ls /apps/OrcaSlicer_Linux_AppImage_*.AppImage | xargs -n1 basename), extracted to ~/apps/orca-root";
    echo "launcher: /usr/local/bin/orca-slicer (exec ~/apps/orca-root/AppRun \"\$@\")";
    echo "Orca settings copied from take G's home (wizard done): ~/.config/OrcaSlicer"; } > "$O/pins.txt"
  cd /root
fi
start_display
openbox > /dev/null 2>&1 &
sleep 1
start_app "$O/app.log"
sleep 10
python3 /work/client/ctl.py ui.prefs "{\"theme\":\"light\",\"ui_scale\":$SCALE}" 27878 > /dev/null 2>&1
fill_window 0 0 $W $H; sleep 1
g 398 206 4; sleep 0.5; click; sleep 3                                  # start page: New design (millimetres)
python3 /work/lab/l6part.py "$O" --allow-path /root --save /root/hook-lesson4.sc > "$O/part-setup.txt" 2>&1
g 1354 164 4; sleep 0.4; click; sleep 1.5                                # the house: the 3D view
g 1000 600 4; sleep 0.5
echo ready > /tmp/fx5/ready
for i in $(seq 1 14400); do [ -f "$O/.end" ] && break; sleep 1; done
rm -f "$O/.end"
