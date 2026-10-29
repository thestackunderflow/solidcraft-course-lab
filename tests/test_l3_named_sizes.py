"""Lesson 3: the J written from five named sizes. The walk with names must give lesson 2's corners at the lesson's
sizes; changing hook_depth to 40 must give the numbers the lesson works out (500 mm², 10,000 mm³, 40 x 20 x 60);
and the plain-number walk with only its first length changed must not close (why SolidCraft refuses it)."""
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from checker import outline  # noqa: E402

SIZES = {'plate_height': 60, 'width': 20, 'thickness': 5, 'hook_depth': 25, 'lip_height': 10}


def test_the_named_walk_is_lesson_twos_walk_at_the_lesson_sizes():
    assert outline.j_moves(SIZES) == outline.J_MOVES


def test_the_named_walk_lists_the_typed_expressions_in_order():
    assert [e for _, e in outline.J_EXPRESSIONS] == [
        'hook_depth', 'lip_height', 'thickness', 'lip_height - thickness', 'hook_depth - 2 * thickness',
        'plate_height - thickness', 'thickness']


def test_hook_depth_40_gives_the_lessons_numbers():
    e = outline.expected(outline.j_moves(dict(SIZES, hook_depth=40)), width=SIZES['width'])
    assert e['area_mm2'] == pytest.approx(5 * 60 + 35 * 5 + 5 * 5)
    assert e['area_mm2'] == pytest.approx(500.0)
    assert e['volume_mm3'] == pytest.approx(10000.0)
    assert e['bbox_mm'] == [40.0, 20.0, 60.0]


def test_the_plain_walk_with_only_the_25_changed_does_not_close():
    moves = list(outline.J_MOVES)
    moves[0] = ('right', 40)
    with pytest.raises(ValueError):
        outline.expected(moves, width=20)
    gap = outline.walk(moves[:-1])[-1]
    assert gap == (15.0, 60.0), 'the plate top would end 15 mm off the wall: the straight back plate cannot close'


def test_unknown_names_are_refused():
    with pytest.raises(KeyError):
        outline.j_moves({'hook_depth': 25})
