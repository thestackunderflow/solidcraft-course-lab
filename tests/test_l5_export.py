"""Lesson 5 (export + slicer check): our checker counts bodies in an STL, reads the 3MF SolidCraft hands to a slicer
(its unit, size, closed, bodies), the slicer helpers read support, plastic and time from a G-code, and the scorer
names how a sent part lies on the bed and which checks a Claude run read before it sent."""
import io
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'lab'))
from checker import stl, m3mf  # noqa: E402
from slicer import gcode  # noqa: E402
from tests import fixtures  # noqa: E402
import l5score  # noqa: E402


def write(tmp_path, name, data):
    p = tmp_path / name
    p.write_bytes(data)
    return str(p)


def model_xml(objects, unit='millimeter'):
    """objects: list of triangle lists (each triangle = 3 (x, y, z)); one <object> each, shared-vertex meshes."""
    out = [f'<?xml version="1.0" encoding="UTF-8"?>\n<model unit="{unit}" '
           'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources>']
    for i, tris in enumerate(objects, start=1):
        verts, idx = [], {}
        faces = []
        for t in tris:
            f = []
            for v in t:
                k = tuple(round(c, 6) for c in v)
                if k not in idx:
                    idx[k] = len(verts)
                    verts.append(k)
                f.append(idx[k])
            faces.append(f)
        out.append(f'<object id="{i}" type="model" name="Body{i}"><mesh><vertices>')
        out += [f'<vertex x="{x}" y="{y}" z="{z}"/>' for x, y, z in verts]
        out.append('</vertices><triangles>')
        out += [f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in faces]
        out.append('</triangles></mesh></object>')
    out.append('</resources><build>' + ''.join(f'<item objectid="{i}"/>' for i in range(1, len(objects) + 1))
               + '</build></model>')
    return '\n'.join(out)


def three_mf(objects, unit='millimeter'):
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w') as z:
        z.writestr('[Content_Types].xml', '<Types/>')
        z.writestr('3D/3dmodel.model', model_xml(objects, unit))
    return b.getvalue()


# --- one body (STL) ---
def test_one_cube_is_one_body(tmp_path):
    r = stl.check(write(tmp_path, 'c.stl', fixtures.binary_stl(fixtures.box_triangles(20, 20, 20))))
    assert r['bodies'] == 1


def test_two_separate_cubes_are_two_bodies_even_in_one_file(tmp_path):
    tris = fixtures.box_triangles(10, 10, 10) + fixtures.box_triangles(10, 10, 10, (30, 0, 0))
    r = stl.check(write(tmp_path, 'two.stl', fixtures.binary_stl(tris)))
    assert r['bodies'] == 2
    assert r['closed'] is True


# --- the 3MF a slicer gets ---
def test_3mf_in_millimetres_gives_size_closed_and_one_body(tmp_path):
    p = write(tmp_path, 'h.3mf', three_mf([fixtures.box_triangles(25, 20, 60)]))
    r = m3mf.check(p)
    assert r['unit'] == 'millimeter'
    assert r['size_mm'] == [25.0, 20.0, 60.0]
    assert r['closed'] is True
    assert r['bodies'] == 1 and r['objects'] == 1
    assert abs(r['volume_mm3'] - 30000.0) < 1e-6


def test_3mf_in_inches_is_converted_to_mm(tmp_path):
    p = write(tmp_path, 'i.3mf', three_mf([fixtures.box_triangles(1, 1, 2)], unit='inch'))
    r = m3mf.check(p)
    assert r['unit'] == 'inch'
    assert r['size_mm'] == [25.4, 25.4, 50.8]


def test_3mf_with_a_hole_in_the_mesh_is_not_closed(tmp_path):
    p = write(tmp_path, 'o.3mf', three_mf([fixtures.box_triangles(10, 10, 10)[:-1]]))
    assert m3mf.check(p)['closed'] is False


def test_3mf_two_objects_are_two_bodies(tmp_path):
    p = write(tmp_path, 't.3mf', three_mf([fixtures.box_triangles(10, 10, 10),
                                           fixtures.box_triangles(10, 10, 10, (20, 0, 0))]))
    r = m3mf.check(p)
    assert r['objects'] == 2 and r['bodies'] == 2


# --- the slicer's numbers from a G-code ---
GCODE = """;TYPE:Perimeter
G1 X10 Y10 E1.0
;Z:0.4
;TYPE:Support material
G1 X20 Y20 E2.0
G1 X21 Y20 E-0.5
;TYPE:Support material interface
G1 X22 Y20 E0.5
; filament_diameter = 1.75
; filament_density = 1.24
; total filament used [g] = 5.37
; estimated printing time (normal mode) = 32m 45s
"""


def test_gcode_support_and_footer():
    s = gcode.stats(GCODE)
    assert s['support_lines'] == 1 and s['support_interface_lines'] == 1
    assert s['total_g'] == 5.37
    assert s['time'] == '32m 45s'
    assert s['support_g'] > 0


def test_gcode_time_in_minutes():
    assert gcode.minutes('32m 45s') == 32.75
    assert gcode.minutes('1h 2m 30s') == 62.5
    assert gcode.minutes('14m 22s') == round(14 + 22 / 60, 4)


# --- how a sent part lies, and which checks a run read ---
def test_orientation_from_the_sent_size():
    assert l5score.orientation([25, 20, 60]) == 'standing'
    assert l5score.orientation([25, 60, 20]) == 'on its side'
    assert l5score.orientation([60, 20, 25]) == 'on its back'
    assert l5score.orientation([20, 25, 60.0004]) == 'standing'
    assert l5score.orientation([33, 33, 33]) == 'other'


def call(seq, name, args, reply=None):
    return {'seq': seq, 'name': name, 'args': args, 'reply': reply}


def test_checks_read_before_the_send():
    calls = [call(1, 'inspect_design', {}, '{"bodies": [{"name": "Body1"}]}'),
             call(2, 'measure', {}, '{"body_count": 1, "bodies": [{"closed": true, "bbox": {}}]}'),
             call(3, 'execute', {'command': 'body.print_face', 'params': {'body': 'Body1', 'point': [12, 0, 2.5]}}, '{}'),
             call(4, 'execute', {'command': 'file.send_to_slicer', 'params': {'slicer': 'prusa'}}, '{"path": "x"}'),
             call(5, 'measure', {}, '{"body_count": 1, "closed": true}')]
    s = l5score.score_calls(calls)
    assert s['sent'] is True and s['send_seq'] == 4
    assert s['read_before_send'] == {'one body': True, 'closed': True, 'size': True}
    assert s['print_face'] == {'body': 'Body1', 'point': [12, 0, 2.5]}


def test_no_read_and_no_print_face():
    calls = [call(1, 'execute', {'command': 'file.send_to_slicer', 'params': {'slicer': 'PrusaSlicer'}}, '{}')]
    s = l5score.score_calls(calls)
    assert s['sent'] is True
    assert s['read_before_send'] == {'one body': False, 'closed': False, 'size': False}
    assert s['print_face'] is None


def test_a_send_inside_a_batch_counts_and_a_save_mesh_is_not_a_send():
    calls = [call(1, 'execute', {'command': 'file.save_mesh', 'params': {'path': '/tmp/h.stl'}}, '{}'),
             call(2, 'batch', {'commands': [{'command': 'body.print_face', 'params': {'body': 'Body1',
                                                                                     'point': [1, 0, 1]}},
                                            {'command': 'file.send_to_slicer', 'params': {'slicer': 'prusa'}}]}, '{}')]
    s = l5score.score_calls(calls)
    assert s['saved_mesh'] == ['/tmp/h.stl']
    assert s['sent'] is True and s['send_seq'] == 2
    assert s['print_face'] == {'body': 'Body1', 'point': [1, 0, 1]}


# --- plan gate (accuracy M4): the face down is named from the height AND the area touching the bed
def test_bed_contact_area_of_a_box():
    import numpy as np
    t = np.array(fixtures.box_triangles(25, 20, 60), dtype=float)
    assert abs(l5score.bed_contact(t) - 500.0) < 1e-6


def test_lie_names_a_face_by_height_and_contact():
    assert l5score.lie(60.0, 500.0) == 'standing'
    assert l5score.lie(20.0, 423.0) == 'on its side'
    assert l5score.lie(25.0, 1128.0) == 'on its back'
    assert l5score.lie(25.0, 200.0).startswith('other')      # e.g. the lip's 10 x 20 face: 25 tall, little contact
    assert l5score.lie(60.0, 40.0).startswith('other')       # upside down on the fillet: 60 tall, no flat face
