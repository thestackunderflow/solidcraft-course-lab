"""fx6 cards: the drawn geometry matches the lab (out/fx6/ANSWERS.md Q2, Q3) and every card is light, readable and
builds in steps. Run in the QA image: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fx6.py"""
import os
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fx6 as d  # noqa: E402

EXPECTED = ([f'card-ball-{i}.png' for i in (1, 2, 3, 4, 5)] + [f'card-sofar-{i}.png' for i in (1, 2, 3)]
            + [f'card-recap-{i}.png' for i in (1, 2, 3)] + [f'card-report-{i}.png' for i in (1, 2)]
            + [f'card-limit-{i}.png' for i in (1, 2, 3, 4)] + ['card-question-1.png', 'card-question-2.png'])


@pytest.mark.parametrize('r,t,ok', [(4.0, 5, True), (4.9, 5, True), (5.0, 5, True), (5.1, 5, False),
                                    (6.0, 5, False), (6.0, 8, True)])
def test_fits_matches_the_lab(r, t, ok):
    assert d.fits(r, t) is ok


def test_flat_left_matches_the_lab():
    assert d.flat_left(4.0, 5) == pytest.approx(1.0)
    assert d.flat_left(5.0, 5) == pytest.approx(0.0)
    assert d.flat_left(6.0, 8) == pytest.approx(2.0)


def test_ball_centre_is_one_radius_from_both_faces():
    assert d.ball_centre(6.0) == (19.0, 4.0)


@pytest.fixture(scope='module')
def drawn():
    d.PROBLEMS.clear()
    d.main()
    return d.OUT


def test_all_cards_drawn_without_problems(drawn):
    for n in EXPECTED:
        assert os.path.exists(os.path.join(drawn, n)), n
    assert d.PROBLEMS == []


def test_full_cards_are_light(drawn):
    for n in EXPECTED:
        im = Image.open(os.path.join(drawn, n))
        assert im.size == (2560, 1440)
        if im.mode == 'RGB':
            assert min(im.getpixel((5, 5))) >= 240, n


def test_steps_only_add(drawn):
    """Each later step differs from the one before (something was added)."""
    for stem, k in (('card-ball', 5), ('card-sofar', 3), ('card-recap', 3), ('card-report', 2), ('card-limit', 4), ('card-question', 2)):
        for i in range(2, k + 1):
            a = Image.open(os.path.join(drawn, f'{stem}-{i - 1}.png')).convert('RGBA')
            b = Image.open(os.path.join(drawn, f'{stem}-{i}.png')).convert('RGBA')
            assert a.tobytes() != b.tobytes(), f'{stem}-{i}'


# ---- fx6 Short cut 2: the side-view ball card at the Short's view size (1080 x 960), built in three steps ----
SHORT = [f'card-short-ball-{i}.png' for i in (1, 2, 3)]


def test_short_ball_steps_match_the_lab():
    # step 1: 6 mm ball on the 5 mm face (no room), step 2: 5 mm ball (fits), step 3: 8 mm face, 6 mm ball (fits)
    assert [(r, t, d.fits(r, t)) for r, t in d.SHORT_BALL] == [(6.0, 5, False), (5.0, 5, True), (6.0, 8, True)]


def test_short_ball_card_light_view_size_and_steps(drawn):
    ims = []
    for n in SHORT:
        im = Image.open(os.path.join(drawn, n))
        assert im.size == (1080, 960), n
        assert im.mode == 'RGB' and min(im.getpixel((5, 5))) >= 240, n
        ims.append(im.tobytes())
    assert ims[0] != ims[1] != ims[2]
    assert d.PROBLEMS == []


# ---- fx6 cut 3 (5 Nov, watch-c2): the ball card in 5 steps, the Short's balls inside the part, both edges marked ----
def test_ball_card_steps_split_the_r2_claims(drawn):
    """cut 3: step 2 the ball + shaved sliver, step 3 its radius, step 4 one radius from each face (ticks), step 5 the
    6 mm ball; each later step adds something."""
    assert d.BALL_STEPS == ['ball', 'radius', 'ticks', 'six']
    assert not os.path.exists(os.path.join(drawn, 'card-ball-6.png'))


def _coloured(px):
    r, g, b = px[:3]
    return max(r, g, b) - min(r, g, b) > 60


def test_short_ball_nothing_drawn_below_the_part(drawn):
    """cut 3: no ball circle pokes out below the lip's bottom (the review read it as a ball bigger than the part)."""
    for n in SHORT:
        im = Image.open(os.path.join(drawn, n)).convert('RGB')
        bad = sum(_coloured(im.getpixel((x, y))) for x in range(0, 1080, 2) for y in range(d.SHORT_OY + 8, 735, 2))
        assert bad == 0, n


def test_short_ball_title_says_outer_top_edge(drawn):
    assert 'outer top edge' in d.SHORT_TITLE and 'corner' not in d.SHORT_TITLE


def test_question_card_marks_both_top_edges(drawn):
    """cut 3: the question card draws the 5 mm lip with both top edges marked (orange), one mark left, one right."""
    im = Image.open(os.path.join(drawn, 'card-question-1.png')).convert('RGBA')
    xs = [x for x in range(d.QUEST[0], d.QUEST[2], 2) for y in range(d.QUEST[1], d.QUEST[3], 2)
          if im.getpixel((x, y))[:3] == d.MARK and im.getpixel((x, y))[3] == 255]
    assert xs, 'no marks'
    mid = (min(xs) + max(xs)) / 2
    assert any(x < mid - 40 for x in xs) and any(x > mid + 40 for x in xs)


def test_report_card_is_full_frame(drawn):
    """cut 3: the report count fills the frame (RGB, light), step 1 drawn on the left half."""
    for i in (1, 2):
        im = Image.open(os.path.join(drawn, f'card-report-{i}.png'))
        assert im.mode == 'RGB', im.mode
    im = Image.open(os.path.join(drawn, 'card-report-1.png')).convert('L')
    assert im.crop((120, 230, 1250, 1180)).getextrema()[0] < 120
