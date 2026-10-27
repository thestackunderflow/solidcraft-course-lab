"""Meshes with known answers, written by hand (no CAD program): a box as 12 triangles, outward-facing."""
import struct


def box_triangles(a, b, c, origin=(0.0, 0.0, 0.0)):
    x0, y0, z0 = origin
    x1, y1, z1 = x0 + a, y0 + b, z0 + c
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    quads = [(0, 3, 2, 1),  # bottom, normal -z
             (4, 5, 6, 7),  # top, +z
             (0, 1, 5, 4),  # front, -y
             (2, 3, 7, 6),  # back, +y
             (1, 2, 6, 5),  # right, +x
             (3, 0, 4, 7)]  # left, -x
    tris = []
    for p, q, r, s in quads:
        tris.append((v[p], v[q], v[r]))
        tris.append((v[p], v[r], v[s]))
    return tris


def binary_stl(tris):
    out = bytearray(b'fixture'.ljust(80, b' '))
    out += struct.pack('<I', len(tris))
    for t in tris:
        out += struct.pack('<3f', 0, 0, 0)
        for p in t:
            out += struct.pack('<3f', *p)
        out += b'\0\0'
    return bytes(out)


def ascii_stl(tris):
    lines = ['solid fixture']
    for t in tris:
        lines += ['  facet normal 0 0 0', '    outer loop']
        lines += [f'      vertex {p[0]} {p[1]} {p[2]}' for p in t]
        lines += ['    endloop', '  endfacet']
    lines.append('endsolid fixture')
    return ('\n'.join(lines) + '\n').encode()
