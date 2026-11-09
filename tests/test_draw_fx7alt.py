"""fx7alt cards (fillet at a corner: refused with the count): the drawn box corner matches the lab (a 20 mm box, the
corner 20, 20, 20 where three edges meet), the map's junction is a Y where three roads END (not a crossroads), and every
card is light, readable and builds in steps. Run in the QA image:
docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fx7alt.py"""
import os
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fx7alt as d  # noqa: E402

STEPS = {'card-map': 5, 'card-sofar': 3, 'card-question': 2}
EXPECTED = [f'{s}-{i}.png' for s, k in STEPS.items() for i in range(1, k + 1)]


def test_box_and_corner_match_the_lab():
    assert d.BOX == 20
    assert d.CORNER == (20, 20, 20)
    assert d.BOX ** 3 == 8000


def test_three_corner_edges_each_along_one_axis():
    assert len(d.EDGES) == 3
    axes = set()
    for name, (a, b, col) in d.EDGES.items():
        assert a == d.CORNER, name
        diff = [i for i in range(3) if a[i] != b[i]]
        assert len(diff) == 1, name
        assert abs(a[diff[0]] - b[diff[0]]) == d.BOX, name
        axes.add(diff[0])
    assert axes == {0, 1, 2}


def test_edge_colours_distinct_and_not_the_status_colours():
    cols = [col for _, _, col in d.EDGES.values()]
    assert len(set(cols)) == 3
    for col in cols:
        assert col not in (d.GREEN, d.RED, d.GREY, d.DONE)
        assert sum(col) / 3 < 160                        # dark enough on a light map


def test_junction_is_a_y_three_roads_end():
    ends = [(pts, col) for pts, col in d.ROADS if d.JUNCTION in (pts[0], pts[-1])]
    assert len(ends) == 3                                # a Y, not a plus (4)
    through = [pts for pts, _ in d.ROADS if d.JUNCTION in pts[1:-1]]
    assert through == []                                 # no road passes through it
    assert {col for _, col in ends} == {c for _, _, c in d.EDGES.values()}


def test_question_point_is_not_answered():
    assert d.QPOINT == (20, 20, 19)


@pytest.fixture(scope='module')
def drawn():
    d.PROBLEMS.clear()
    d.main()
    return d.OUT


def test_all_cards_drawn_without_problems(drawn):
    for n in EXPECTED:
        assert os.path.exists(os.path.join(drawn, n)), n
    assert d.PROBLEMS == []


def test_no_text_over_44_columns_and_44_px(drawn):
    for n in EXPECTED:
        assert d.LOG[n], n
        for s, size in d.LOG[n]:
            assert len(s) <= 44, (n, s)
            assert size >= 44, (n, s, size)


def test_sizes_modes_and_light(drawn):
    for n in EXPECTED:
        im = Image.open(os.path.join(drawn, n))
        assert im.size == (2560, 1440), n
        if n.startswith('card-question'):
            assert im.mode == 'RGBA', n
            continue
        assert im.mode == 'RGB', n
        assert min(im.getpixel((5, 5))) >= 240, n
        assert sum(im.convert('L').getdata()) / (2560 * 1440) > 200, n


def _ink(px, rgba):
    if rgba:
        return px[3] > 200 and sum(px[:3]) / 3 < 200
    return sum(px[:3]) / 3 < 200


def _background(px, rgba):
    return px[3] == 0 if rgba else px[:3] == (255, 255, 255)


def test_steps_only_add(drawn):
    """Each later step differs, keeps every earlier text line, and no pixel that was ink becomes background."""
    for stem, k in STEPS.items():
        for i in range(2, k + 1):
            na, nb = f'{stem}-{i - 1}.png', f'{stem}-{i}.png'
            ta, tb = [s for s, _ in d.LOG[na]], [s for s, _ in d.LOG[nb]]
            assert len(tb) > len(ta) and all(s in tb for s in ta), nb
            a, b = Image.open(os.path.join(drawn, na)), Image.open(os.path.join(drawn, nb))
            rgba = a.mode == 'RGBA'
            assert a.tobytes() != b.tobytes(), nb
            pa, pb = a.load(), b.load()
            lost = sum(1 for x in range(0, 2560, 3) for y in range(0, 1440, 3)
                       if _ink(pa[x, y], rgba) and _background(pb[x, y], rgba))
            assert lost == 0, f'{nb}: {lost} ink pixels erased'


def test_question_transparent_outside_the_panel(drawn):
    for i in (1, 2):
        im = Image.open(os.path.join(drawn, f'card-question-{i}.png'))
        bb = im.getchannel('A').getbbox()
        q = d.QUEST
        assert q[0] >= 1280                               # the right half
        assert bb[0] >= q[0] and bb[1] >= q[1] and bb[2] <= q[2] + 1 and bb[3] <= q[3] + 1, bb
        assert im.getpixel((100, 700))[3] == 0


def test_question_shows_no_answer(drawn):
    allowed = {'A question', 'Fresh box. Point [20, 20, 19].', 'Rounds, or refused?', 'Pause and think'}
    for i in (1, 2):
        assert {s for s, _ in d.LOG[f'card-question-{i}.png']} <= allowed
    assert 'Pause and think' in {s for s, _ in d.LOG['card-question-2.png']}
