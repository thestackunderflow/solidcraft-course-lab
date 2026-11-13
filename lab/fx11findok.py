"""fx11 (a copy of fx10findok.py, rows 350-500 halved for the Split Body / Offset Plane dialogs): where the dialog's OK button is now, and whether it is enabled (blue). Reads one pixel column of a full-size
screenshot (ImageMagick txt: output), x = 2776 (1388 in halved units), y 700-1000 (350-500 halved).
    python3 lab/fx10findok.py SHOT.png        prints "blue Y" (halved units, middle of the blue run) or "none"
"""
import re
import subprocess
import sys

X, Y0, N = 2776, 700, 300
txt = subprocess.run(['convert', sys.argv[1], '-crop', f'1x{N}+{X}+{Y0}', 'txt:-'], capture_output=True, text=True).stdout
blue = []
for line in txt.splitlines():
    m = re.match(r'\s*0,(\d+):\s*\((\d+),(\d+),(\d+)', line)
    if not m:
        continue
    y, r, g, b = (int(v) for v in m.groups())
    if b > 140 and r < 90 and b - r > 80:
        blue.append(y)
if len(blue) < 20:
    print('none')
else:
    # the longest run of blue rows
    runs, cur = [], [blue[0]]
    for y in blue[1:]:
        if y == cur[-1] + 1:
            cur.append(y)
        else:
            runs.append(cur); cur = [y]
    runs.append(cur)
    r = max(runs, key=len)
    print('blue', (Y0 + (r[0] + r[-1]) // 2) // 2)
