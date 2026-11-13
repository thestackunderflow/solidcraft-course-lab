"""fx12 cards (SolidCraft Offset: "its corners follow its source curves"): every card in SCRIPT-fx12.md section 4 is drawn,
light, 2560 x 1440, text 44 px+ and 44 columns at most, each step only adds, side panels stay transparent on the
recording's side, the source overlays (2880 x 1620) are transparent except their marks, the numbers are the measured
ones (7,834.61 / 7,405.25 / 429.36; walls 4.07 / 2.00), the tool-log card quotes runs/R1/tools.txt's line word for word,
the question is never answered, and the masked after.png differs from after.png only in the update button. Run in the
draw image: docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fx12.py"""
import os
import sys

import pytest
from PIL import Image, ImageChops

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fx12 as d  # noqa: E402

STEPS = {'card-rails': 3, 'card-sofar': 3, 'card-decode': 3, 'card-walls': 2, 'card-question': 2, 'card-recipe': 2}
EXPECTED = [f'{s}-{i}.png' for s, k in STEPS.items() for i in range(1, k + 1)]
SIDE = {'card-decode': 1430, 'card-walls': 1430, 'card-question': 1300}
OVS = ('ov-wall-a.png', 'ov-qmm.png', 'ov-r1-mask.png', 'ov-toollog.png')
FORBIDDEN = ('7,834.51', '7,405.31', '7,641.37', 'bug', 'wrong', 'snap', 'pulled back', 'untied', 'undo', 'ready to print',
             'fillet: `l6', 'you can never', 'box', '50 x 30', 'update to')
ANSWER = ('sharp.', 'sharp:', 'answer:', 'it is sharp', 'refused.')
TOOLS = os.path.join(d.TAKES, 'runs', 'R1', 'tools.txt')


@pytest.fixture(scope='module')
def drawn():
    d.main()
    return d


def all_text(drawn):
    return [s for items in drawn.LOG.values() if isinstance(items, list) and items and isinstance(items[0], tuple)
            for s, _ in items]


def test_all_cards_and_overlays_drawn_without_problems(drawn):
    assert drawn.PROBLEMS == []
    have = set(os.listdir(drawn.OUT))
    for n in EXPECTED + list(OVS) + ['after-masked.png', 'short-stack.png']:
        assert n in have, n
    assert Image.open(os.path.join(drawn.OUT, 'short-stack.png')).size == (1080, 960)


def test_no_text_over_44_columns_and_44_px(drawn):
    for name, items in drawn.LOG.items():
        if not (isinstance(items, list) and items and isinstance(items[0], tuple)):
            continue
        for s, px in items:
            assert px >= 44, (name, s, px)
            for ln in s.split('\n'):
                assert len(ln) <= 44, (name, ln)


def test_cards_light_sized_and_side_panels_transparent(drawn):
    for n in EXPECTED:
        im = Image.open(os.path.join(drawn.OUT, n))
        assert im.size == (2560, 1440), n
        side = [x for p, x in SIDE.items() if n.startswith(p)]
        if side:
            assert im.mode == 'RGBA' and im.crop((0, 0, side[0], 1440)).getchannel('A').getextrema() == (0, 0), n
        else:
            assert sum(im.convert('L').resize((64, 36)).getdata()) / (64 * 36) > 200, n


def test_each_step_only_adds_text(drawn):
    for pre, k in STEPS.items():
        for i in range(2, k + 1):
            a = {s for s, _ in drawn.LOG[f'{pre}-{i - 1}.png']}
            b = {s for s, _ in drawn.LOG[f'{pre}-{i}.png']}
            assert a <= b, (pre, i, a - b)


def test_measured_numbers_and_do_not_say(drawn):
    txt = ' '.join(all_text(drawn)).lower()
    for v in ('7,834.61', '7,405.25', '429.36', '4.07', '2.00', '5 - 2 = 3'):
        assert v.lower() in txt, v
    for bad in FORBIDDEN:
        assert bad not in txt, bad
    assert 'checked by a script, not filmed' in txt
    assert '<' not in txt and '>' not in txt


def test_question_never_answered(drawn):
    q = ' '.join(s for s, _ in drawn.LOG['card-question-2.png']).lower()
    assert 'round, sharp or refused?' in q
    for a in ANSWER:
        assert a not in q, a


def test_toollog_card_is_the_tool_log_line_word_for_word(drawn):
    lines = drawn.LOG['ov-toollog.lines']
    assert ' '.join(lines) == d.LINE_R1
    if os.path.exists(TOOLS):
        log = ' '.join(open(TOOLS, encoding='utf-8').read().split())
        assert d.LINE_R1 in log
    hdr = ' '.join(s for s, _ in drawn.LOG['ov-toollog.png'])
    assert 'Its 4th solidcraft call, from the tool log' in hdr and '(not on its screen):' in hdr


def test_overlays_transparent_except_marks(drawn):
    for n in OVS:
        im = Image.open(os.path.join(drawn.OUT, n))
        assert im.size == (2880, 1620) and im.mode == 'RGBA', n
        a = im.getchannel('A')
        assert a.getpixel((5, 5)) == 0 or n == 'ov-r1-mask.png', n
    m = Image.open(os.path.join(drawn.OUT, 'ov-r1-mask.png')).getchannel('A')
    assert m.crop((0, 0, 2880, 1488)).getextrema() == (0, 0)          # only the suggestion row is covered


def test_after_masked_only_the_update_button(drawn):
    a = Image.open(os.path.join(d.TAKES, 'runs', 'R1', 'after.png')).convert('RGB')
    m = Image.open(os.path.join(drawn.OUT, 'after-masked.png')).convert('RGB')
    bbox = ImageChops.difference(a, m).getbbox()
    x, y, w, h = d.UPDATE_BTN
    assert bbox and bbox[0] >= x and bbox[1] >= y and bbox[2] <= x + w and bbox[3] <= y + h, bbox
