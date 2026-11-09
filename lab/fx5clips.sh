#!/bin/bash
# fx5 lab clips (4 Nov owner rule: context first, the FULL window before any zoom, no crop-only takes). For every cut two
# files from footage.py (Refream-Canvas/mcp-canvas/tools/video-qa, mounted at /vq):
#   NAME-full.mp4  the whole 2880x1800 display: footage.py clip --zoom 1 --size 2304x1440 (16:10, so nothing is
#                  cropped), then padded to 2560x1440 with a light band left and right;
#   NAME-zoom.mp4  footage.py clip --zoom 2 (2560x1440) following the cursor log, or a focus box where the action is
#                  a terminal the cursor does not visit.
#   docker run --rm -v "$LAB:/work" -v "$VQ:/vq:ro" sc5-fx5:0.28.0 bash /work/lab/fx5clips.sh [NAME ...]
set -eu
F=/vq/footage.py; D=/work/out/fx5; C=$D/clips; mkdir -p "$C" /tmp/fx5c
cut() {   # cut NAME TAKE T0 T1 [FOCUS_JSON]
  local n=$1 tk=$2 a=$3 b=$4 fo=${5:-}
  if [ -n "${ONLY:-}" ] && ! echo " $ONLY " | grep -q " $n "; then return; fi
  python3 "$F" clip "$D/$tk/screen.mp4" /tmp/fx5c/full.mp4 --src 2880x1800 --t0 "$a" --t1 "$b" --zoom 1 --size 2304x1440 \
    --cursor "$D/$tk/cursor.jsonl" > /dev/null
  ffmpeg -loglevel error -y -i /tmp/fx5c/full.mp4 -vf "pad=2560:1440:128:0:color=0xf2f2ee" -c:v libx264 -crf 18 \
    -pix_fmt yuv420p -an "$C/$n-full.mp4"
  if [ -n "$fo" ]; then
    echo "$fo" > /tmp/fx5c/focus.json
    python3 "$F" clip "$D/$tk/screen.mp4" "$C/$n-zoom.mp4" --src 2880x1800 --t0 "$a" --t1 "$b" --zoom 2 \
      --focus /tmp/fx5c/focus.json > /dev/null
  else
    python3 "$F" clip "$D/$tk/screen.mp4" "$C/$n-zoom.mp4" --src 2880x1800 --t0 "$a" --t1 "$b" --zoom 2 \
      --cursor "$D/$tk/cursor.jsonl" > /dev/null
  fi
  echo "$n: $tk $a-$b s -> $n-full.mp4, $n-zoom.mp4"
}
ONLY="$*"
TERM_B='[{"t": 0, "box": [1480, 1180, 880, 440]}]'
cut A-send1        A 0 45
cut A-send-again   A 88 140
cut A-first-25     A 160 175
cut A-reload       A 205 262
cut B-listings     B 0 110 "$TERM_B"
cut C-prefs-off    C 60 95
cut C-send2-second C 215 300
cut C-reload       C 300 336
cut C-pref-on      C 336 356
cut C-send3-lands  C 391 460
[ -f "$D/runs/R1/clips.env" ] && . "$D/runs/R1/clips.env"
if [ -n "${R1_A:-}" ]; then
  cut R1-reply       runs/R1 "$R1_A" "$R1_B" "${R1_FOCUS:-}"
  cut R1-slicer      runs/R1 "$R1_C" "$R1_D"
fi
