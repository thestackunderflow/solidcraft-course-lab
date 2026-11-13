"""fx11 cards (SolidCraft Split Body: "the tool does not split the body"): every card in SCRIPT-fx11.md section 4 is drawn,
light, 2560 x 1440, text 44 px+ and 44 columns at most, each step only adds, side panels stay transparent on the
recording's side, the source overlays (2880 x 1620) are transparent except their marks, the numbers are the measured
ones (58,506.68 + 54,972.98 = 113,479.66; bore 30 from 200 down to 5; block 16,000.00), the question is never answered,
and the masked after.png hides only the title bar's update button. Run in the draw image:
docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fx11.py"""
import os
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fx11 as d  # noqa: E402

STEPS = {'card-cake': 4, 'card-sofar': 4, 'card-floor': 2, 'card-pieces': 3, 'card-question': 2, 'card-recipe': 3}
EXPECTED = [f'{s}-{i}.png' for s, k in STEPS.items() for i in range(1, k + 1)]
SIDE = {'card-floor': 1300, 'card-question': 1300, 'card-pieces': 1620}
OVS = ('ov-xy-a.png', 'ov-xy-c.png', 'ov-s2.png', 'ov-r1-mask.png')
FORBIDDEN = ('58,512', '54,978', '113,490', 'bug', 'wrong', 'timeline', 'glue', 'ready to print', 'midplane')
ANSWER = ('refused.', 'it splits', 'no split', 'yes', 'answer:')


@pytest.fixture(scope='module')
def drawn():
    d.main()
    return d


def test_all_cards_and_overlays_drawn_without_problems(drawn):
    assert drawn.PROBLEMS == []
    have = set(os.listdir(drawn.OUT))
    for n in EXPECTED + list(OVS) + ['after-masked.png', 'short-split.png']:
        assert n in have, n
    assert Image.open(os.path.join(drawn.OUT, 'short-split.png')).size == (1080, 960)


def test_no_text_over_44_columns_and_44_px(drawn):
    for name, items in drawn.LOG.items():
        for s, px in items:
            assert px >= 44, (name, s, px)
            for ln in s.split('\n'):
                assert len(ln) <= 44, (name, ln)


def test_cards_light_and_sized(drawn):
    for n in EXPECTED:
        im = Image.open(os.path.join(drawn.OUT, n))
        assert im.size == (2560, 1440), n
        if not n.startswith(tuple(SIDE)):
            g = im.convert('L').resize((64, 36))
            assert sum(g.getdata()) / (64 * 36) > 200, n


def test_steps_only_add(drawn):
    for s, k in STEPS.items():
        texts = [[t for t, _ in drawn.LOG[f'{s}-{i}.png']] for i in range(1, k + 1)]
        for a, b in zip(texts, texts[1:]):
            assert all(t in b for t in a), (s, set(a) - set(b))
            assert len(b) > len(a) or s == 'card-cake', s


def test_side_panels_transparent_on_the_recording_side(drawn):
    for n in EXPECTED:
        for pre, x in SIDE.items():
            if n.startswith(pre):
                im = Image.open(os.path.join(drawn.OUT, n))
                assert im.mode == 'RGBA'
                assert im.crop((0, 0, x, 1440)).getchannel('A').getextrema() == (0, 0), n


def test_overlays_source_size_mostly_clear(drawn):
    for n in OVS:
        im = Image.open(os.path.join(drawn.OUT, n))
        assert im.size == (2880, 1620) and im.mode == 'RGBA', n
        a = im.getchannel('A').resize((96, 54))
        assert sum(1 for v in a.getdata() if v) < 0.25 * 96 * 54, n


def test_measured_numbers_only(drawn):
    alltext = ' '.join(t for items in drawn.LOG.values() for t, _ in items)
    for bad in FORBIDDEN:
        assert bad not in alltext.lower(), bad
    for good in ('58,506.68 + 54,972.98', '= 113,479.66 mm3', '16,000.00 mm3 each?'):
        assert good in alltext, good
    assert (drawn.BORE_D, drawn.BORE_FLOOR, drawn.OUTER_D, drawn.TALL) == (30, 5, 40, 200)


def test_question_never_answered(drawn):
    q = ' '.join(t for n in ('card-question-1.png', 'card-question-2.png', 'ov-s2.png') for t, _ in drawn.LOG[n]).lower()
    for bad in ANSWER:
        assert bad not in q, bad
    assert 'split or refused?' in q


def test_after_masked_only_the_update_button(drawn):
    a = Image.open(os.path.join(drawn.TAKES, 'runs', 'R1', 'after.png')).convert('RGB')
    b = Image.open(os.path.join(drawn.OUT, 'after-masked.png')).convert('RGB')
    x, y, w, h = drawn.UPDATE_BTN
    diff = [(i, j) for i in range(0, 2880, 8) for j in range(0, 1620, 8) if a.getpixel((i, j)) != b.getpixel((i, j))]
    assert diff and all(x <= i < x + w and y <= j < y + h for i, j in diff)
