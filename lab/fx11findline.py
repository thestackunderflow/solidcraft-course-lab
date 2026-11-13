"""fx11: is the red error line showing under the Split Body dialog's fields? Counts red text pixels in a full-size
screenshot (ImageMagick txt: output), x 2410-2850, y 724-764 (halved 1205-1425, 362-382: the line's row in the probe).
    python3 lab/fx11findline.py SHOT.png        prints "red N" (N red pixels) or "none"
"""
import re
import subprocess
import sys

txt = subprocess.run(['convert', sys.argv[1], '-crop', '440x40+2410+724', 'txt:-'], capture_output=True, text=True).stdout
n = 0
for line in txt.splitlines():
    m = re.match(r'\s*\d+,\d+:\s*\((\d+),(\d+),(\d+)', line)
    if m:
        r, g, b = (int(v) for v in m.groups())
        n += r > 150 and g < 100 and b < 100
print(f'red {n}' if n >= 30 else 'none')
