"""Lesson 6 (edit without breaking it): our mesh reader measures the hook's opening, walls and lip with rays through the
exported triangles, and the scorer applies the pre-registered pass rule (out/l6/prereg.json): the change (opening 30)
plus the seven must-stay-true lines, each with its tolerance."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'lab'))
from checker import l6geom  # noqa: E402
from tests import fixtures  # noqa: E402
import l6score  # noqa: E402


def hook_tris(depth=40.0, t=5.0, lip=10.0, plate=60.0, width=20.0, mirror=False):
    """The J hook as three touching boxes (plate, base between the walls, lip), y from -width to 0 like SolidCraft's."""
    boxes = [(t, width, plate, (0.0, -width, 0.0)),
             (depth - 2 * t, width, t, (t, -width, 0.0)),
             (t, width, lip, (depth - t, -width, 0.0))]
    tris = []
    for a, b, c, o in boxes:
        tris += fixtures.box_triangles(a, b, c, o)
    arr = np.array(tris, dtype=float)
    if mirror:
        arr[:, :, 0] = depth - arr[:, :, 0]
        arr = arr[:, ::-1, :].copy()          # a mirror turns the triangles inside out: flip them back
    return arr


def test_intervals_of_one_box():
    tris = np.array(fixtures.box_triangles(10, 4, 6, (2, -2, 0)), dtype=float)
    iv = l6geom.intervals(tris, origin=(-100, 0.013, 3.017), axis=0)
    assert len(iv) == 1
    assert abs(iv[0][0] - 2) < 1e-6 and abs(iv[0][1] - 12) < 1e-6


def test_touching_boxes_merge_into_one_interval():
    tris = np.array(fixtures.box_triangles(5, 4, 4, (0, -2, 0)) + fixtures.box_triangles(5, 4, 4, (5, -2, 0)), dtype=float)
    iv = l6geom.intervals(tris, origin=(-100, 0.011, 2.013), axis=0)
    assert len(iv) == 1 and abs(iv[0][1] - iv[0][0] - 10) < 1e-6


def test_hook_as_drawn_in_lesson5():
    g = l6geom.measure_hook(hook_tris(depth=25))
    assert abs(g['opening_mm'] - 15) < 1e-6
    assert abs(g['plate_mm'] - 5) < 1e-6 and abs(g['lip_mm'] - 5) < 1e-6 and abs(g['base_mm'] - 5) < 1e-6
    assert abs(g['lip_height_mm'] - 10) < 1e-6


def test_hook_depth_30_gives_a_20_opening():
    assert abs(l6geom.measure_hook(hook_tris(depth=30))['opening_mm'] - 20) < 1e-6


def test_hook_depth_40_gives_30_and_mirrored_reads_the_same():
    for m in (False, True):
        g = l6geom.measure_hook(hook_tris(depth=40, mirror=m))
        assert abs(g['opening_mm'] - 30) < 1e-6
        assert abs(g['lip_height_mm'] - 10) < 1e-6


def test_thicker_walls_are_seen():
    g = l6geom.measure_hook(hook_tris(depth=40, t=6))
    assert abs(g['plate_mm'] - 6) < 1e-6 and abs(g['opening_mm'] - 28) < 1e-6


def test_no_gap_reads_none():
    tris = np.array(fixtures.box_triangles(40, 20, 60, (0, -20, 0)), dtype=float)
    assert l6geom.measure_hook(tris)['opening_mm'] is None


def good_read():
    """A read like lab/l6read.py writes for the right edit (probe numbers: hook_depth 40)."""
    return {
        'summary': {'volume_mm3': 9806.62, 'bbox_mm': [40.0, 20.0, 60.0], 'bbox_min': [0, -20, 0], 'bbox_max': [40, 0, 60],
                    'holes': [{'y': -10.0, 'z': 45.0, 'diameter': 4.5, 'centred': True, 'from_sides': [10.0, 10.0]},
                              {'y': -10.0, 'z': 15.0, 'diameter': 4.5, 'centred': True, 'from_sides': [10.0, 10.0]}],
                    'fillets': [{'radius': 2.0, 'x': 2.0, 'z': 58.0}, {'radius': 2.0, 'x': 3.0, 'z': 58.0}],
                    'top_edges_rounded': 2},
        'body_count': 1, 'closed': True,
        'mesh': {'closed': True, 'bodies': 1},
        'geom': {'opening_mm': 30.0, 'plate_mm': 5.0, 'lip_mm': 5.0, 'base_mm': 5.0, 'lip_height_mm': 10.0},
        'sent': {'height_mm': 20.0, 'size_mm': [40.0, 60.0, 20.0], 'closed': True, 'bodies': 1},
    }


def test_the_right_edit_passes_every_line():
    s = l6score.score(good_read())
    assert s['passed'] is True
    assert [r['id'] for r in s['lines']] == ['C', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7']
    assert all(r['ok'] for r in s['lines'])


def test_depth_30_fails_only_the_change():
    r = good_read()
    r['geom']['opening_mm'] = 20.0
    r['summary']['bbox_mm'] = [30.0, 20.0, 60.0]
    s = l6score.score(r)
    assert s['passed'] is False
    assert [x['id'] for x in s['lines'] if not x['ok']] == ['C']


def test_lost_print_face_fails_m7():
    r = good_read()
    r['sent']['height_mm'] = 60.0
    s = l6score.score(r)
    assert [x['id'] for x in s['lines'] if not x['ok']] == ['M7']


def test_missing_hole_or_moved_hole_fails_m5():
    r = good_read()
    r['summary']['holes'] = r['summary']['holes'][:1]
    assert [x['id'] for x in l6score.score(r)['lines'] if not x['ok']] == ['M5']
    r = good_read()
    r['summary']['holes'][0]['z'] = 44.0
    assert [x['id'] for x in l6score.score(r)['lines'] if not x['ok']] == ['M5']
    r = good_read()
    r['summary']['holes'][1]['centred'] = False
    assert [x['id'] for x in l6score.score(r)['lines'] if not x['ok']] == ['M5']


def test_holes_are_measured_from_the_top_even_if_the_part_moved():
    r = good_read()
    r['summary']['bbox_min'] = [0, -20, 10]
    r['summary']['bbox_max'] = [40, 0, 70]
    for h, z in zip(r['summary']['holes'], (55.0, 25.0)):
        h['z'] = z
    for f in r['summary']['fillets']:
        f['z'] = 68.0
    assert l6score.score(r)['passed'] is True


def test_lost_fillet_and_two_bodies_fail_their_lines():
    r = good_read()
    r['summary']['top_edges_rounded'] = 1
    r['summary']['fillets'] = r['summary']['fillets'][:1]
    r['body_count'] = 2
    bad = [x['id'] for x in l6score.score(r)['lines'] if not x['ok']]
    assert bad == ['M1', 'M6']


def test_thin_wall_or_short_lip_fail():
    r = good_read()
    r['geom']['lip_mm'] = 4.0
    r['geom']['lip_height_mm'] = 8.0
    bad = [x['id'] for x in l6score.score(r)['lines'] if not x['ok']]
    assert bad == ['M3', 'M4']


def test_a_missing_measure_is_a_fail_not_a_crash():
    r = good_read()
    r['geom']['opening_mm'] = None
    r['sent'] = None
    bad = [x['id'] for x in l6score.score(r)['lines'] if not x['ok']]
    assert bad == ['C', 'M7']


def test_a_ray_exactly_through_a_face_diagonal_counts_once():
    tris = np.array(fixtures.box_triangles(10, 4, 6, (0, -2, 0)), dtype=float)
    # the box's -y face is split along its diagonal; this ray (along Y) goes through that diagonal's middle
    iv = l6geom.intervals(tris, origin=(5, -100, 3), axis=1)
    assert len(iv) == 1 and abs(iv[0][0] + 2) < 1e-6 and abs(iv[0][1] - 2) < 1e-6


def test_the_level_ray_finds_the_window_when_the_lip_is_taller():
    g = l6geom.measure_hook(hook_tris(depth=40, lip=20))
    assert abs(g['opening_mm'] - 30) < 1e-6 and abs(g['lip_height_mm'] - 20) < 1e-6
    assert 5 < g['ray_z_mm'] < 20


def test_a_headless_read_is_not_scored():
    r = good_read()
    r['headless'] = True
    s = l6score.score(r)
    assert s['passed'] is None and s['refused']
