"""fx8 cards (Convert Mesh): the drawn hook matches the lab (out/fx8/ANSWERS.md Q9: 8,500 mm3) and every card is light,
readable and builds in steps. Run in the QA image:
docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fx8.py"""
import os
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fx8 as d  # noqa: E402

STEPS = {'card-recipe': 3, 'card-cutter': 3, 'card-sofar': 3, 'card-question': 2}
EXPECTED = [f'{s}-{i}.png' for s, k in STEPS.items() for i in range(1, k + 1)]


def test_outline_area_and_extents_match_the_lab():
    assert d.area(d.HOOK) == pytest.approx(425.0)
    xs, zs = [p[0] for p in d.HOOK], [p[1] for p in d.HOOK]
    assert (max(xs) - min(xs), max(zs) - min(zs)) == (25, 60)


def test_volume_is_the_lab_volume():
    assert d.area(d.HOOK) * d.DEPTH == pytest.approx(8500.0)


def test_holes_in_the_back_plate_middle_of_the_depth():
    assert d.HOLE_Y == pytest.approx(d.DEPTH / 2)
    for z in d.HOLE_Z:
        assert 5 + d.HOLE_D / 2 < z < 60 - d.HOLE_D / 2


@pytest.fixture(scope='module')
def drawn():
    d.PROBLEMS.clear()
    d.main()
    return d.OUT


def test_all_cards_drawn_without_problems(drawn):
    for n in EXPECTED:
        assert os.path.exists(os.path.join(drawn, n)), n
    assert d.PROBLEMS == []


def test_sizes_modes_and_light(drawn):
    for n in EXPECTED:
        im = Image.open(os.path.join(drawn, n))
        assert im.size == (2560, 1440), n
        if n.startswith('card-question'):
            assert im.mode == 'RGBA', n
            continue
        assert im.mode == 'RGB', n
        assert min(im.getpixel((5, 5))) >= 240, n
        assert sum(Image.open(os.path.join(drawn, n)).convert('L').getdata()) / (2560 * 1440) > 200, n


def _ink(px, rgba):
    if rgba:
        return px[3] > 200 and sum(px[:3]) / 3 < 200
    return sum(px[:3]) / 3 < 200


def _background(px, rgba):
    return px[3] == 0 if rgba else px[:3] == (255, 255, 255)


def test_steps_only_add(drawn):
    """Each later step differs from the one before, and no pixel that was ink becomes background."""
    for stem, k in STEPS.items():
        for i in range(2, k + 1):
            a = Image.open(os.path.join(drawn, f'{stem}-{i - 1}.png'))
            rgba = a.mode == 'RGBA'
            b = Image.open(os.path.join(drawn, f'{stem}-{i}.png'))
            assert a.tobytes() != b.tobytes(), f'{stem}-{i}'
            pa, pb = a.load(), b.load()
            lost = sum(1 for x in range(0, 2560, 3) for y in range(0, 1440, 3)
                       if _ink(pa[x, y], rgba) and _background(pb[x, y], rgba))
            assert lost == 0, f'{stem}-{i}: {lost} ink pixels erased'


def test_question_transparent_outside_the_panel(drawn):
    for i in (1, 2):
        im = Image.open(os.path.join(drawn, f'card-question-{i}.png'))
        bb = im.getchannel('A').getbbox()
        q = d.QUEST
        assert bb[0] >= q[0] and bb[1] >= q[1] and bb[2] <= q[2] + 1 and bb[3] <= q[3] + 1, bb
        assert im.getpixel((100, 700))[3] == 0


def test_question_box_rounds_only_the_upright_edges():
    """fx8 cut 3 (watch-c2, 4:07): the old front view drew the top as a squashed rounded cap, so the box looked rounded
    on top too. The box is now drawn from a corner: one crisp top outline at the full height (a flat top), and the side
    shaded per strip, so the two flat faces are one shade each and the rounded upright edges grade between them."""
    top = d.qbox_outline(d.QBOX_H)
    assert top and all(p[4] == d.QBOX_H for p in top)
    shades = d.qbox_side_shades()
    flat = [s for n, s in shades if n in ('face+x', 'face+y')]
    rounds = [s for n, s in shades if n == 'round']           # the front upright edge (the side ones turn away)
    assert len(set(s for n, s in shades if n == 'face+x')) == 1
    assert len(set(s for n, s in shades if n == 'face+y')) == 1
    assert len(set(flat)) == 2
    assert len(set(rounds)) >= 4
    lo, hi = min(flat), max(flat)
    assert all(lo - 1 <= s <= hi + 1 for s in rounds)
    assert 'flat top' in d.QUESTION_LABELS
