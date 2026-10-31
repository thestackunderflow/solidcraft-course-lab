"""Lesson 5: a copy of a binary STL with its last N triangles removed (a file broken on purpose, for the "closed" check).
    python3 lab/l5break.py IN.stl OUT.stl N"""
import struct
import sys

d = open(sys.argv[1], 'rb').read()
n = struct.unpack('<I', d[80:84])[0]
keep = n - int(sys.argv[3])
open(sys.argv[2], 'wb').write(d[:80] + struct.pack('<I', keep) + d[84:84 + 50 * keep])
