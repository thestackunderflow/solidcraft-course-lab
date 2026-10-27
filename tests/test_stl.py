"""Our checker reads an STL and gives the volume, the size and whether it is closed (watertight)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from checker import stl  # noqa: E402
from tests import fixtures  # noqa: E402


def write(tmp_path, name, data):
    p = tmp_path / name
    p.write_bytes(data)
    return str(p)


def test_a_20_mm_cube_is_8000_cubic_mm_binary(tmp_path):
    r = stl.check(write(tmp_path, 'c.stl', fixtures.binary_stl(fixtures.box_triangles(20, 20, 20))))
    assert abs(r['volume_mm3'] - 8000.0) < 1e-6
    assert r['size_mm'] == [20.0, 20.0, 20.0]
    assert r['closed'] is True
    assert r['triangles'] == 12


def test_the_same_cube_in_ascii(tmp_path):
    r = stl.check(write(tmp_path, 'c.stl', fixtures.ascii_stl(fixtures.box_triangles(20, 20, 20, (5, -3, 2)))))
    assert abs(r['volume_mm3'] - 8000.0) < 1e-6
    assert r['closed'] is True


def test_a_box_that_is_not_a_cube(tmp_path):
    r = stl.check(write(tmp_path, 'b.stl', fixtures.binary_stl(fixtures.box_triangles(10, 20, 30))))
    assert abs(r['volume_mm3'] - 6000.0) < 1e-6
    assert r['size_mm'] == [10.0, 20.0, 30.0]


def test_a_missing_triangle_is_not_closed(tmp_path):
    tris = fixtures.box_triangles(20, 20, 20)[:-1]
    r = stl.check(write(tmp_path, 'o.stl', fixtures.binary_stl(tris)))
    assert r['closed'] is False


def test_an_inside_out_mesh_is_flagged(tmp_path):
    tris = [(a, c, b) for a, b, c in fixtures.box_triangles(20, 20, 20)]
    r = stl.check(write(tmp_path, 'i.stl', fixtures.binary_stl(tris)))
    assert r['closed'] is True
    assert r['outward'] is False
    assert abs(r['volume_mm3'] - 8000.0) < 1e-6
