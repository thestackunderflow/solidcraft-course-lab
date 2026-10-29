"""Lesson 3 scoring (out/l3/prereg.json rules): how an edit is classed, and when it counts as followed."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'lab'))
sys.path.insert(0, os.path.join(HERE, '..'))
import l3compare as c  # noqa: E402


def call(tool, **a):
    return {'name': tool, 'arguments': a}


def test_a_parameter_change_with_no_sketch_command_is_by_parameter():
    k = c.edit_kind([call('set_parameter', name='hook_depth', value=40), call('measure')])
    assert k['kind'] == 'one parameter change' and k['by_parameter']


def test_a_parameter_change_inside_execute_counts():
    k = c.edit_kind([call('execute', command='parameters.change', params={'name': 'hook_depth', 'expression': '40'})])
    assert k['by_parameter']


def test_a_new_design_and_new_points_is_a_redraw():
    k = c.edit_kind([call('new_design'), call('batch', commands=[{'command': 'sketch.create'}, {'command': 'sketch.line'}])])
    assert k['kind'] == 'drew it again in a new design' and not k['by_parameter']


def test_moving_points_is_not_by_parameter_even_with_a_parameter_call():
    k = c.edit_kind([call('set_parameter', name='x', value=1), call('execute', command='sketch.move_point')])
    assert not k['by_parameter']


def summary(corners, lo, hi, vol, box):
    return {'corners': corners, 'bbox_min': lo, 'bbox_max': hi, 'volume_mm3': vol, 'bbox_mm': box}


def test_the_40_hook_standing_up_is_followed_either_way_the_sketch_points():
    up = [[x, y] for x, y in c.corners40()]
    down = [[x, -y] for x, y in c.corners40()]
    for pts in (up, down):
        r = c.edit_followed(summary(pts, [0, -20, 0], [40, 0, 60], 10000.0, [40, 20, 60]))
        assert r['all'], r


def test_a_hook_hanging_below_the_floor_is_not_followed():
    r = c.edit_followed(summary([[x, -y] for x, y in c.corners40()], [0, 0, -60], [40, 20, 0], 10000.0, [40, 20, 60]))
    assert not r['z_0_60'] and not r['all']


def test_reading_of_40_deep():
    assert c.reading({'bbox_mm': [45, 20, 60]}).startswith('arm 40')
    assert c.reading({'bbox_mm': [40, 20, 60]}).startswith('outside depth 40')
