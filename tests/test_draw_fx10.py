"""fx10 cards (SolidCraft Revolve: "invalid input: the profile crosses the revolve axis"; draw only half): every card in
SCRIPT-fx10.md section 4 is drawn, light, 2560 x 1440, text 44 px+ and 44 columns at most, each step only adds, the
side-panel overlays stay transparent on the recording's side, the source-space overlays (2880 x 1620, for the derived
takes) are transparent except their marks, the numbers match the lab (30 across = 15 x 2, 5 mm off the axis), and the
question card never shows the ring answer. Run in the QA image:
docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fx10.py"""
import os
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fx10 as d  # noqa: E402

STEPS = {'card-wheel': 3, 'card-sofar': 2, 'card-sides': 2, 'card-radius': 2, 'card-question': 2}
EXPECTED = [f'{s}-{i}.png' for s, k in STEPS.items() for i in range(1, k + 1)]
SIDE = {'card-sides': 1300, 'card-question': 1300, 'card-radius': 1620}   # nothing left of this x
OVS = ('ov-axis-3d.png', 'ov-axis-sketch.png', 'ov-tint-3d.png', 'ov-tint-sketch.png', 'ov-ext-c.png', 'ov-ring-dim.png',
       'ov-inset.png')
FORBIDDEN = ('7,351', '7351', 'bug', 'wrong', 'timeline', 'fully constrained', 'impossible')
ANSWER = ('ring', 'disc', 'hole', 'tube', 'washer', '6,283', '10 mm')


@pytest.fixture(scope='module')
def drawn():
    d.main()
    return d


def test_all_cards_and_overlays_drawn_without_problems(drawn):
    assert drawn.PROBLEMS == []
    have = set(os.listdir(drawn.OUT))
    for n in EXPECTED + list(OVS):
        assert n in have, n


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
            assert sum(g.getdata()) / (64 * 36) > 200, n         # light background


def test_steps_only_add(drawn):
    for s, k in STEPS.items():
        names = [x for x, _ in drawn.LOG.items() if x.startswith(s + '-')]
        texts = [[t for t, _ in drawn.LOG[f'{s}-{i}.png']] for i in range(1, k + 1)]
        for a, b in zip(texts, texts[1:]):
            assert all(t in b for t in a), (s, set(a) - set(b))
            assert len(b) > len(a), s
        assert len(names) == k


def test_side_panels_transparent_on_the_recording_side(drawn):
    for n in EXPECTED:
        for pre, x in SIDE.items():
            if n.startswith(pre):
                im = Image.open(os.path.join(drawn.OUT, n))
                assert im.mode == 'RGBA', n
                assert im.crop((0, 0, x, 1440)).getchannel('A').getextrema() == (0, 0), n


def test_source_overlays_2880_and_mostly_clear(drawn):
    for n in OVS:
        im = Image.open(os.path.join(drawn.OUT, n))
        assert im.size == (2880, 1620) and im.mode == 'RGBA', n
        a = im.getchannel('A').resize((288, 162))
        clear = sum(1 for v in a.getdata() if v == 0) / (288 * 162)
        assert clear > 0.5, (n, clear)


def test_numbers_match_the_lab(drawn):
    assert drawn.ACROSS == 30.0 and drawn.HALF == 15.0 and drawn.HALF * 2 == drawn.ACROSS
    assert drawn.OFF == 5
    assert drawn.AXIS_3D_X == 1675 and drawn.AXIS_SKETCH_X == 1440


def test_no_forbidden_text_and_question_unanswered(drawn):
    for name, items in drawn.LOG.items():
        for s, _ in items:
            low = s.lower()
            for f in FORBIDDEN:
                assert f not in low, (name, s)
            if name.startswith('card-question'):
                for f in ANSWER:
                    assert f not in low, (name, s)


def test_labels_from_the_script(drawn):
    t = lambda n: ' '.join(s for s, _ in drawn.LOG[n])  # noqa: E731
    assert 'card edge = profile' in t('card-wheel-3.png') and 'spindle = axis' in t('card-wheel-3.png')
    assert 'one outline, one side of the axis' in t('card-sides-1.png')
    # cut 2 (watch-through c1 must-fix 3): the sweep before "every ring twice"; each circle labelled with its angle
    s2 = drawn.LOG['card-sides-2.png']
    said = [s for s, _ in s2]
    assert said.index('each point sweeps a ring round the axis') < said.index('every ring twice')
    assert 'seen from above:' in said and 'at 360 degrees' in said and 'at 180 degrees' in said
    assert 'no overlap: refused' in said
    assert 'half-width 15 mm' in t('card-radius-1.png') and '15 x 2 = 30 mm across' in t('card-radius-2.png')
    assert 'one side of an endless line' in t('card-sofar-2.png')
    assert 'Square 5 mm off the axis.' in t('card-question-1.png')
    assert 'Revolve 360. What shape?' in t('card-question-2.png') and 'Pause and think' in t('card-question-2.png')
