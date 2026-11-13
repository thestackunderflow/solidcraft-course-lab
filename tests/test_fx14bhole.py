"""fx14bhole.py (R1 checker): a hole in the top of a box, from its mesh triangles (no window, no AI)."""
import importlib.util
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location('fx14bhole', os.path.join(ROOT, 'lab', 'fx14bhole.py'))
fx14bhole = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx14bhole)

BOX = [((0, 0, 0), (40, 0, 0), (40, 30, 0)), ((0, 0, 20), (40, 30, 20), (0, 30, 20)),
       ((0, 0, 0), (0, 30, 20), (0, 0, 20)), ((40, 0, 0), (40, 30, 20), (40, 30, 0))]


def ring(cx, cy, r, z, n=32):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n), z) for i in range(n + 1)]


def hole(cx, cy, r, z0, z1, tip=None):
    a, b = ring(cx, cy, r, z1), ring(cx, cy, r, z0)
    f = [(a[i], a[i + 1], b[i]) for i in range(32)]
    if tip is None:
        f += [((cx, cy, z0), b[i], b[i + 1]) for i in range(32)]
    else:
        f += [((cx, cy, z0 - tip), b[i], b[i + 1]) for i in range(32)]
    return f


def test_no_hole():
    h = fx14bhole.find_hole(BOX)
    assert h['hole'] is False and h['box'] == [0.0, 0.0, 0.0, 40.0, 30.0, 20.0]


def test_flat_hole_centred():
    h = fx14bhole.find_hole(BOX + hole(20, 15, 5, 15, 20))
    assert (h['hole'], h['centre_xy'], h['diameter_mm'], h['top_z'], h['wall_bottom_z'], h['depth_mm'], h['flat_floor']) \
        == (True, [20.0, 15.0], 10.0, 20.0, 15.0, 5.0, True)


def test_pointed_hole():
    h = fx14bhole.find_hole(BOX + hole(20, 15, 5, 15, 20, tip=3.0))
    assert h['flat_floor'] is False and h['depth_mm'] == 5.0 and h['lowest_z'] == 12.0


def test_off_centre():
    h = fx14bhole.find_hole(BOX + hole(10, 10, 4, 12, 20))
    assert h['centre_xy'] == [10.0, 10.0] and h['diameter_mm'] == 8.0 and h['depth_mm'] == 8.0
