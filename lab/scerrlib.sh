# scerr helpers (8 Nov 2026, video "SolidCraft MCP: 5 Errors and the Rule That Avoids Each"): the fx8 helpers (display
# 2880x1620, UI scale 1.8, positions in 1440x810 units) with the take folders under out/scerr and SolidCraft 0.30.1
# (sc-wf-l5:0.30.1). Sourced by lab/scerrsession.sh and by every `docker exec scerr-s bash /work/lab/scerrX.sh` step.
. /work/lab/fx8lib.sh
take() { O=/work/out/scerr/$1; mkdir -p "$O"; echo "$O" > /tmp/fx8/O; }
open_file() {   # open_file FILE: open a design or a mesh over the plug (fx8 stop rule A3: no file window under Xvfb)
  python3 /work/lab/fx8part.py open "$O" "$1" > "$O/open-$(basename "$1").txt" 2>&1
}
# fx6 positions (0.28.0 probe; re-checked on 0.30.1 by lab/scerrprobe.sh screenshots)
FILLET_BTN="353 90"; LIP_EDGE="910 609"; RADIUS_BOX="1349 347"; OK_BTN="1388 581"; CANCEL_BTN="1322 581"   # OK sits at 581 while the size fits, 659 under the red line (0.30.1)
radius() { g $RADIUS_BOX 18; click; xdotool key ctrl+a; nap 0.3; typed "$1" 160; nap 0.6; xdotool key Tab; nap 4.0; }
