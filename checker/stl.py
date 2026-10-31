"""Our own checker for an exported STL (numpy only): volume, size, closed, outward-facing.

    python3 -m checker.stl FILE.stl     prints the JSON

Volume: the divergence theorem (sum of signed tetrahedra from the origin); positive when the triangles face outward.
Closed: every edge is used by exactly two triangles, once in each direction (vertices matched to 1e-6 mm).
Bodies: groups of triangles joined through shared vertices (lesson 5: two separate parts in one file count 2)."""
import json
import struct
import sys
from collections import Counter

import numpy as np


def read(path):
    data = open(path, 'rb').read()
    if len(data) >= 84:
        n = struct.unpack('<I', data[80:84])[0]
        if 84 + 50 * n == len(data):
            rec = np.frombuffer(data, dtype=np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]),
                                count=n, offset=84)
            return rec['v'].astype(np.float64)
    vs = [tuple(float(x) for x in line.split()[1:4]) for line in data.decode('utf-8', 'replace').splitlines()
          if line.strip().startswith('vertex')]
    return np.array(vs, dtype=np.float64).reshape(-1, 3, 3)


def components(idx, n_vertices):
    """Number of groups of triangles that share vertices (union-find over each triangle's three vertex ids)."""
    parent = list(range(n_vertices))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for i, j, k in idx:
        for a, b in ((i, j), (j, k)):
            ra, rb = find(int(a)), find(int(b))
            if ra != rb:
                parent[ra] = rb
    used = {int(v) for tri in idx for v in tri}
    return len({find(v) for v in used})


def mesh_check(t):
    """The checks on an array of triangles (N, 3, 3) in mm."""
    a, b, c = t[:, 0], t[:, 1], t[:, 2]
    signed = float(np.einsum('ij,ij->i', a, np.cross(b, c)).sum() / 6.0)
    lo, hi = t.reshape(-1, 3).min(0), t.reshape(-1, 3).max(0)
    key = np.round(t.reshape(-1, 3) / 1e-6).astype(np.int64)
    uniq, idx = np.unique(key, axis=0, return_inverse=True)
    idx = idx.reshape(-1, 3)
    directed = Counter()
    for i, j, k in idx:
        for e in ((i, j), (j, k), (k, i)):
            directed[e] += 1
    closed = all(n == 1 and directed.get((e[1], e[0]), 0) == 1 for e, n in directed.items())
    return {'triangles': int(len(t)),
            'volume_mm3': round(abs(signed), 6), 'outward': signed > 0,
            'size_mm': [round(float(x), 6) for x in (hi - lo)], 'min_mm': [round(float(x), 6) for x in lo],
            'closed': bool(closed), 'bodies': components(idx, len(uniq))}


def check(path):
    return dict({'file': path.replace('\\', '/').split('/')[-1]}, **mesh_check(read(path)))


if __name__ == '__main__':
    print(json.dumps(check(sys.argv[1]), indent=1))
