"""Lesson 2: the expected volume is worked out from the J outline itself (not typed in), and the two designs (drawn by
hand, made by Claude) are compared by what SolidCraft reports: the profile area, the volume and the timeline steps."""
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from checker import outline, recipe  # noqa: E402


def test_the_j_walk_closes_and_has_the_lesson_sizes():
    pts = outline.walk(outline.J_MOVES)
    assert pts[0] == (0.0, 0.0)
    assert pts[-1] == (0.0, 0.0), 'the eighth line ends where the first began'
    assert len(pts) == 9
    box = outline.bbox(pts)
    assert box == ((0.0, 0.0), (25.0, 60.0)), 'hook arm 25 deep, back plate 60 tall'


def test_area_by_the_shoelace_rule_matches_the_three_rectangles():
    pts = outline.walk(outline.J_MOVES)
    # back plate 5 x 60 + hook arm (25 - 5) x 5 + lip 5 x (10 - 5)
    assert outline.area(pts) == pytest.approx(5 * 60 + 20 * 5 + 5 * 5)
    assert outline.area(pts) == pytest.approx(425.0)


def test_expected_volume_is_area_times_width():
    e = outline.expected(outline.J_MOVES, width=20)
    assert e['area_mm2'] == pytest.approx(425.0)
    assert e['volume_mm3'] == pytest.approx(8500.0)
    assert e['bbox_mm'] == [25.0, 20.0, 60.0]


def test_an_open_walk_is_refused():
    with pytest.raises(ValueError):
        outline.expected([('right', 10), ('up', 10)], width=5)


def test_area_does_not_depend_on_direction():
    square_cw = outline.walk([('up', 10), ('right', 10), ('down', 10), ('left', 10)])
    square_ccw = outline.walk([('right', 10), ('up', 10), ('left', 10), ('down', 10)])
    assert outline.area(square_cw) == outline.area(square_ccw) == pytest.approx(100.0)


INSPECT = {
    'timeline': [
        {'id': 1, 'name': 'Sketch1', 'type': 'Sketch', 'error': None, 'suppressed': False, 'rolled_back': False},
        {'id': 2, 'name': 'Extrude1', 'type': 'ExtrudeFeature', 'error': None, 'suppressed': False, 'rolled_back': False},
    ],
    'sketches': [{'name': 'Sketch1', 'fully_constrained': True, 'curves': [{'type': 'line'}] * 8,
                  'profiles': [{'area_mm2': 425.0, 'holes': []}],
                  'plane': {'origin': [0.0, 0.0, 0.0], 'x_dir': [1.0, 0.0, 0.0], 'y_dir': [-0.0, -0.0, 1.0]},
                  'points': [{'id': 'origin', 'at': [0.0, 0.0]}, {'id': 'l1.end', 'at': [25.0, 0.0]},
                             {'id': 'l2.end', 'at': [25.0, 10.0]}, {'id': 'l3.end', 'at': [20.0, 10.0]},
                             {'id': 'l4.end', 'at': [20.0, 5.0]}, {'id': 'l5.end', 'at': [5.0, 5.0]},
                             {'id': 'l6.end', 'at': [5.0, 60.0]}, {'id': 'l7.end', 'at': [0.0, 60.0]}]}],
}
MEASURE = {'bodies': [{'name': 'Body1', 'volume_mm3': 8500.0, 'closed': True,
                       'bbox': {'min': [0.0, -20.0, 0.0], 'max': [25.0, 0.0, 60.0]}}],
           'body_count': 1, 'total': {'volume_mm3': 8500.0}}


def test_steps_are_the_timeline_types_in_order():
    assert recipe.steps(INSPECT) == ['Sketch', 'ExtrudeFeature']


def test_steps_skip_suppressed_and_rolled_back_features():
    d = {'timeline': INSPECT['timeline'] + [{'id': 3, 'name': 'Fillet1', 'type': 'FilletFeature', 'suppressed': True},
                                            {'id': 4, 'name': 'Shell1', 'type': 'ShellFeature', 'rolled_back': True}]}
    assert recipe.steps(d) == ['Sketch', 'ExtrudeFeature']


def test_summary_reads_lines_profile_volume_and_size():
    s = recipe.summary(INSPECT, MEASURE)
    assert s == {'steps': ['Sketch', 'ExtrudeFeature'], 'step_names': ['Sketch1', 'Extrude1'], 'sketch_lines': [8],
                 'profile_areas_mm2': [425.0], 'bodies': 1, 'volume_mm3': 8500.0, 'closed': True,
                 'bbox_mm': [25.0, 20.0, 60.0], 'bbox_min': [0.0, -20.0, 0.0], 'bbox_max': [25.0, 0.0, 60.0],
                 'plane_normal': [0.0, -1.0, 0.0], 'sketch_up': [0.0, 0.0, 1.0],
                 'corners': [[0.0, 0.0], [0.0, 60.0], [5.0, 5.0], [5.0, 60.0], [20.0, 5.0], [20.0, 10.0],
                             [25.0, 0.0], [25.0, 10.0]], 'errors': 0}


def test_compare_two_designs_with_the_expected_numbers():
    a = recipe.summary(INSPECT, MEASURE)
    b = dict(a, step_names=['Sketch 1', 'Extrude 1'])
    v = recipe.compare(a, b, outline.expected(outline.J_MOVES, width=20))
    assert v['same_steps'] is True
    assert v['same_volume'] is True and v['volume_matches_expected'] is True
    assert v['verdict'] == 'same part, same recipe'


def test_compare_flags_a_different_volume():
    a = recipe.summary(INSPECT, MEASURE)
    m2 = {'bodies': [dict(MEASURE['bodies'][0], volume_mm3=9000.0)], 'body_count': 1, 'total': {'volume_mm3': 9000.0}}
    b = recipe.summary(INSPECT, m2)
    v = recipe.compare(a, b, outline.expected(outline.J_MOVES, width=20))
    assert v['same_volume'] is False
    assert v['verdict'] != 'same part, same recipe'


def test_compare_flags_different_steps():
    a = recipe.summary(INSPECT, MEASURE)
    b = dict(a, steps=['Sketch', 'ExtrudeFeature', 'ExtrudeFeature'])
    v = recipe.compare(a, b, outline.expected(outline.J_MOVES, width=20))
    assert v['same_steps'] is False


def test_the_corners_match_the_walk():
    pts = outline.walk(outline.J_MOVES)[:-1]
    assert recipe.summary(INSPECT, MEASURE)['corners'] == sorted([list(p) for p in pts])


def test_a_mirrored_j_with_the_same_volume_is_not_the_same_part():
    a = recipe.summary(INSPECT, MEASURE)
    mirrored = dict(a, corners=sorted([[-x, y] for x, y in a['corners']]), bbox_min=[-25.0, -20.0, 0.0],
                    bbox_max=[0.0, 0.0, 60.0])
    v = recipe.compare(a, mirrored, outline.expected(outline.J_MOVES, width=20))
    assert v['same_volume'] is True
    assert v['same_shape'] is False
    assert v['verdict'] != 'same part, same recipe'


def test_a_j_on_another_plane_is_not_the_same_part():
    a = recipe.summary(INSPECT, MEASURE)
    flat = dict(a, plane_normal=[0.0, 0.0, 1.0], bbox_min=[0.0, 0.0, 0.0], bbox_max=[25.0, 60.0, 20.0])
    v = recipe.compare(a, flat, outline.expected(outline.J_MOVES, width=20))
    assert v['same_plane'] is False
    assert v['verdict'] != 'same part, same recipe'


def test_the_same_j_pushed_the_other_way_is_the_same_shape_in_another_place():
    a = recipe.summary(INSPECT, MEASURE)
    other = dict(a, bbox_min=[0.0, 0.0, 0.0], bbox_max=[25.0, 20.0, 60.0])
    v = recipe.compare(a, other, outline.expected(outline.J_MOVES, width=20))
    assert v['same_shape'] is True and v['same_place'] is False
    assert v['verdict'] == 'same part and recipe, pushed the other way'


def test_a_closing_point_listed_twice_is_one_corner():
    d = dict(INSPECT)
    d['sketches'] = [dict(INSPECT['sketches'][0], points=INSPECT['sketches'][0]['points'] + [{'id': 'p9', 'at': [0.0, 0.0]}])]
    assert len(recipe.summary(d, MEASURE)['corners']) == 8


def test_the_same_j_on_xz_with_its_up_pointing_down_is_named_upside_down():
    # lab runs claude-1 and claude-2 (27 Oct): sketch.create {plane: "XZ"} gave y_dir (0,0,-1), the Browser's XZ (0,0,1);
    # same corners in the sketch, same volume and steps, but the hook hangs below the floor (z -60..0)
    a = recipe.summary(INSPECT, MEASURE)
    d = dict(INSPECT)
    d['sketches'] = [dict(INSPECT['sketches'][0], plane={'origin': [0.0, 0.0, 0.0], 'x_dir': [1.0, 0.0, 0.0],
                                                          'y_dir': [0.0, 0.0, -1.0]})]
    m = {'bodies': [dict(MEASURE['bodies'][0], bbox={'min': [0.0, 0.0, -60.0], 'max': [25.0, 20.0, 0.0]})],
         'body_count': 1, 'total': {'volume_mm3': 8500.0}}
    b = recipe.summary(d, m)
    v = recipe.compare(a, b, outline.expected(outline.J_MOVES, width=20))
    assert v['same_shape'] is True and v['same_steps'] is True and v['same_volume'] is True
    assert v['same_plane'] is True, 'both are the XZ plane'
    assert v['same_up'] is False
    assert v['verdict'] == 'same shape, size and steps, but upside down'
