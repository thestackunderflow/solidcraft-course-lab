"""The cursor log for the footage crop: polls `xdotool getmouselocation` and writes one JSONL row per sample,
{"t": seconds since the recording started, "x", "y"} (display pixels). Run beside the recorder:
    python3 /work/lab/cursorlog.py OUT.jsonl T0_EPOCH [HZ]      (stops when OUT.jsonl.stop exists)"""
import json
import os
import re
import subprocess
import sys
import time

LOC = re.compile(r'x:(-?\d+)\s+y:(-?\d+)')


def parse(line):
    m = LOC.search(line or '')
    return (int(m.group(1)), int(m.group(2))) if m else None


def write_row(f, t0, t, xy):
    f.write(json.dumps({'t': round(t - t0, 3), 'x': xy[0], 'y': xy[1]}) + '\n')


def main(out, t0, hz=20.0):
    stop = out + '.stop'
    last = None
    with open(out, 'a') as f:
        while not os.path.exists(stop):
            t = time.time()
            r = subprocess.run(['xdotool', 'getmouselocation'], capture_output=True, text=True)
            xy = parse(r.stdout)
            if xy and xy != last:
                write_row(f, t0, t, xy)
                f.flush()
                last = xy
            time.sleep(max(0.0, 1.0 / hz - (time.time() - t)))


if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]) if len(sys.argv) > 3 else 20.0)
