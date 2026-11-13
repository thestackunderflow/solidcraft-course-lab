"""fx13wall.py (R1 checker): side wall, floor and top lid of a cup from its mesh triangles (no window, no AI)."""
import importlib.util
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('fx13wall', os.path.join(ROOT, 'lab', 'fx13wall.py'))
fx13wall = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx13wall)


def p(r, a, z):
    return (r * math.cos(a), r * math.sin(a), z)


def band(r0, za, r1, zb, n=32):
    """triangles between ring (r0, za) and ring (r1, zb): a cylinder side when r0 == r1, a round or flat face else"""
    out = []
    for i in range(n):
        a, b = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        out += [(p(r0, a, za), p(r0, b, za), p(r1, a, zb)), (p(r0, b, za), p(r1, b, zb), p(r1, a, zb))]
    return out


def disk(r, z, n=32):
    return [((0, 0, z), p(r, 2 * math.pi * i / n, z), p(r, 2 * math.pi * (i + 1) / n, z)) for i in range(n)]


def rounded_outside():   # outer r 30 from z 1.5 to 78.5, 1.5 rounds (two short bands each) to r 28.5 at z 0 / 80
    return (band(30, 1.5, 30, 78.5) + band(30, 1.5, 29.56, 0.44) + band(29.56, 0.44, 28.5, 0)
            + band(30, 78.5, 29.56, 79.56) + band(29.56, 79.56, 28.5, 80) + disk(28.5, 0))


def test_open_cup_2mm():
    f = rounded_outside() + band(28, 2, 28, 80) + disk(28, 2) + band(28, 80, 28.5, 80)
    w = fx13wall.walls(f)
    assert (w['hollow'], w['wall_mm'], w['floor_mm'], w['lid_mm']) == (True, 2.0, 2.0, 0.0)


def test_solid_cup():
    w = fx13wall.walls(rounded_outside() + disk(28.5, 80))
    assert w['hollow'] is False and w['wall_mm'] is None and w['outer_r_mm'] == 30.0


def test_closed_hollow():  # every face shelled 2 mm: a 2 mm lid
    f = rounded_outside() + disk(28.5, 80) + band(28, 2, 28, 78) + disk(28, 2) + disk(28, 78)
    w = fx13wall.walls(f)
    assert (w['lid_mm'], w['floor_mm'], w['wall_mm']) == (2.0, 2.0, 2.0)
