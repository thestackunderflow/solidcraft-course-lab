"""Lesson 4: reading holes and fillets from SolidCraft's own replies (measure + body_topology + parameters.list), and
scoring them by the rules written before the Claude runs (out/l4/prereg.json)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'lab'))
sys.path.insert(0, os.path.join(HERE, '..'))
import l4read as r  # noqa: E402
import l4compare as c  # noqa: E402


def bore(y, z, rad=2.25, half=0, feat=3):
    return {'name': f'F{feat}:bore:side:{half}', 'cylinder': {'axis': [1.0, 0.0, 0.0], 'origin': [5.0, y, z], 'radius': rad}}


def blend(x, y, z=58.0, rad=2.0, axis=(0.0, -1.0, 0.0)):
    return {'name': 'F5:blend', 'cylinder': {'axis': list(axis), 'origin': [x, y, z], 'radius': rad}}


def plane(i):
    return {'name': f'F2:side:l{i}', 'plane_normal': [1.0, 0.0, 0.0]}


def measure(vol, lo, hi):
    return {'bodies': [{'volume_mm3': vol, 'bbox': {'min': lo, 'max': hi}}], 'total': {'volume_mm3': vol}}


def hook(y=-10.0, width=20.0, blends=True, vol=8306.62):
    faces = [plane(1), bore(y, 45, half=0), bore(y, 45, half=1, feat=3), bore(y, 15, half=0, feat=4), bore(y, 15, half=1, feat=4)]
    if blends:
        faces += [blend(2.0, 0.0), blend(3.0, -width, axis=(0.0, 1.0, 0.0))]
    return measure(vol, [0.0, -width, 0.0], [25.0, 0.0, 60.0]), {'faces': faces}


def test_two_half_bores_make_one_hole_and_the_diameter_is_twice_the_radius():
    m, t = hook()
    s = r.summarise(m, t, {})
    assert len(s['holes']) == 2
    assert {h['z'] for h in s['holes']} == {45.0, 15.0}
    assert all(abs(h['diameter'] - 4.5) < 1e-9 for h in s['holes'])


def test_a_hole_in_the_middle_of_a_20_wide_plate_is_centred():
    m, t = hook()
    s = r.summarise(m, t, {})
    assert all(h['centred'] for h in s['holes'])
    assert s['holes'][0]['from_sides'] == [10.0, 10.0]


def test_typed_10_after_width_30_is_off_centre_10_and_20():
    m, t = hook(y=-20.0, width=30.0, vol=12539.44)
    s = r.summarise(m, t, {})
    assert not any(h['centred'] for h in s['holes'])
    assert sorted(s['holes'][0]['from_sides']) == [10.0, 20.0]


def test_fillet_faces_are_cylinders_along_the_width_and_holes_are_along_x():
    m, t = hook()
    s = r.summarise(m, t, {})
    assert len(s['fillets']) == 2 and all(abs(f['radius'] - 2.0) < 1e-9 for f in s['fillets'])
    assert s['top_edges_rounded'] == 2


def test_no_fillet_is_reported_as_zero_rounded_edges():
    m, t = hook(blends=False)
    assert r.summarise(m, t, {})['top_edges_rounded'] == 0


def test_hole_parameters_from_names():
    plist = {'parameters': [
        {'name': 'hole_d', 'source': 'user', 'expression': '4.5', 'value': 4.5},
        {'name': 'd2', 'source': 'feature', 'feature': 'Hole1', 'input': 'Diameter', 'expression': 'hole_d', 'value': 4.5},
        {'name': 'd4', 'source': 'feature', 'feature': 'Hole1', 'input': 'Reference distance', 'expression': '15', 'value': 15},
        {'name': 'd5', 'source': 'feature', 'feature': 'Hole1', 'input': 'Reference distance', 'expression': 'width / 2', 'value': 10},
        {'name': 'd6', 'source': 'feature', 'feature': 'Hole2', 'input': 'Diameter', 'expression': '4.5', 'value': 4.5}]}
    p = r.hole_params(plist)
    assert p['hole_d_parameter'] is True
    assert p['diameters'] == {'Hole1': 'hole_d', 'Hole2': '4.5'}
    assert p['distances_from_width'] == {'Hole1': True}


# --- scoring (prereg rules)
def test_build_right_needs_two_centred_holes_two_fillets_and_the_volume():
    m, t = hook()
    s = r.summarise(m, t, {})
    b = c.build_right(s, width=20)
    assert b['all'], b
    m, t = hook(blends=False, vol=8341.0)
    assert not c.build_right(r.summarise(m, t, {}), width=20)['all']


def test_after_the_change_off_centre_holes_fail_centred_but_keep_the_fillet():
    m, t = hook(y=-20.0, width=30.0, vol=12539.44)
    a = c.after_change(r.summarise(m, t, {}))
    assert not a['holes_centred'] and a['fillets_kept'] and a['box_25_30_60'] and a['volume']
    assert not a['all']


def test_after_the_change_centred_holes_pass():
    m, t = hook(y=-15.0, width=30.0, vol=12539.44)
    assert c.after_change(r.summarise(m, t, {}))['all']


def test_centred_counts_either_extrude_direction():
    m, t = hook(y=15.0, width=30.0, vol=12539.44)
    m['bodies'][0]['bbox'] = {'min': [0.0, 0.0, 0.0], 'max': [25.0, 30.0, 60.0]}
    assert all(h['centred'] for h in r.summarise(m, t, {})['holes'])


def call(tool, **a):
    return {'name': tool, 'arguments': a}


def test_width_change_by_parameter():
    assert c.edit_by_parameter([call('set_parameter', name='width', value=30), call('measure')])
    assert c.edit_by_parameter([call('execute', command='parameters.change', params={'name': 'width', 'expression': '30'})])
    assert not c.edit_by_parameter([call('new_design'), call('batch', commands=[{'command': 'sketch.line'}])])


def test_hole_positions_from_logged_calls():
    calls = [call('execute', command='solid.hole', params={'position': [5, -10, 45], 'diameter': 'hole_d',
                                                           'references': [{'edge': [5, 0, 30], 'distance': 'width / 2'}]}),
             call('batch', commands=[{'command': 'solid.hole', 'params': {'position': ['thickness', '-width / 2', 15], 'diameter': 4.5}}])]
    h = c.logged_holes(calls)
    assert len(h) == 2
    assert h[0]['uses_width'] and h[0]['diameter'] == 'hole_d'
    assert h[1]['uses_width'] and h[1]['diameter'] == 4.5


# --- run verdicts (prereg: follow test after turn 1 + message 2's calls + the live read after message 2)
def test_verdict_kept_centred_by_formula():
    assert c.verdict(follow1=True, turn2=[call('set_parameter', name='width', value=30)], centred_after=True) == 'kept centred by formula'


def test_verdict_recentred_by_hand_when_the_holes_were_moved_in_message_2():
    t2 = [call('set_parameter', name='width', value=30),
          call('execute', command='parameters.change', params={'name': 'd5', 'expression': '15'})]
    assert c.hole_edits(t2)
    assert c.verdict(follow1=False, turn2=t2, centred_after=True) == 're-centred by hand'


def test_verdict_a_formula_that_follows_but_message_2_also_moved_holes_is_not_kept_by_formula():
    t2 = [call('set_parameter', name='width', value=30), call('execute', command='solid.hole', params={'position': [5, -15, 45]})]
    assert c.verdict(follow1=True, turn2=t2, centred_after=True) == 're-centred by hand'


def test_verdict_off_centre():
    assert c.verdict(follow1=False, turn2=[call('set_parameter', name='width', value=30)], centred_after=False) == 'off-centre'
