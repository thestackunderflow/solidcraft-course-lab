"""fx9 cards (SolidCraft Thread: an 8 mm hole is too wide for a modelled M8 thread; drill 6.75): the numbers match the
lab (M8 pitch 1.25, tooth height 0.68, hole 8 - 1.25 = 6.75; M5 5 - 0.8 = 4.2; the filmed window 6.3 refused, 6.5 and
7.6 built, 7.7 refused), the tooth is drawn about half a pitch tall, every card is light, readable and builds in steps,
the overlays stay off the left half, and the question card never shows the M10 answer. Run in the QA image:
docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 -m pytest -q tests/test_draw_fx9.py"""
import os
import sys

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video'))
import draw_fx9 as d  # noqa: E402

STEPS = {'card-lid': 3, 'card-cut': 2, 'card-pitch': 3, 'card-sofar': 2, 'card-question': 2}
EXPECTED = [f'{s}-{i}.png' for s, k in STEPS.items() for i in range(1, k + 1)]
OVERLAYS = ('card-cut', 'card-question')
FORBIDDEN = ('6.4', '7.66', '6.8', 'bug', 'wrong')


def test_thread_numbers_match_the_lab():
    assert d.M8 == (8, 1.25)
    assert d.TOOTH == 0.68
    assert d.HOLE_M8 == 6.75 == round(d.M8[0] - d.M8[1], 2)
    assert d.M5 == (5, 0.8)
    assert round(d.M5[0] - d.M5[1], 2) == 4.2


def test_window_rows_match_the_filmed_tries():
    assert [(h, r) for h, _, r in d.ROWS] == [(6.3, 'refused'), (6.5, 'built'), (7.6, 'built'), (7.7, 'refused')]
    for h, diff, _ in d.ROWS:
        assert diff == f'{h - d.HOLE_M8:+.2f}', (h, diff)
    assert d.FIFTH == ('8 for M10', '-0.5 vs 8.5', '?')


def test_tooth_drawn_about_half_a_pitch_tall():
    assert abs(d.TOOTH_PX / d.PITCH_PX - d.TOOTH / d.M8[1]) < 0.02
    assert d.TOOTH_PX / d.PITCH_PX < 0.6                 # not the full 60 degree V (0.866)


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
        if n.startswith(OVERLAYS):
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


def test_overlays_transparent_on_the_left_half(drawn):
    for stem in OVERLAYS:
        for i in range(1, STEPS[stem] + 1):
            im = Image.open(os.path.join(drawn, f'{stem}-{i}.png'))
            assert im.crop((0, 0, 1300, 1440)).getchannel('A').getextrema() == (0, 0), (stem, i)
            assert im.getchannel('A').getbbox()[2] <= 2541, (stem, i)


def test_sofar_shows_the_same_lid_picture(drawn):
    lid3 = {s for s, _ in d.LOG['card-lid-3.png']} - {d.HEAD_LID}
    assert lid3 <= {s for s, _ in d.LOG['card-sofar-1.png']}
    assert "8 = outside of the bolt's teeth" in lid3
    assert "hole = tips of the nut's ridges: smaller" in lid3


def test_card_labels_from_the_script(drawn):
    want = {'card-lid-2.png': 'ridge tips = the hole', 'card-cut-1.png': 'grooves = the gaps between teeth',
            'card-cut-2.png': '0.00 mm to cut', 'card-pitch-1.png': 'pitch = 1.25 mm for M8',
            'card-pitch-3.png': '8 minus 1.25 = 6.75', 'card-sofar-2.png': 'SolidCraft: hole = size minus pitch',
            'card-question-1.png': '8 mm hole. Message says M10.', 'card-question-2.png': 'Pause and think'}
    for n, s in want.items():
        assert s in {t for t, _ in d.LOG[n]}, (n, s)
    p1 = {t for t, _ in d.LOG['card-pitch-1.png']}
    assert 'about half a pitch: 0.68' in p1
    assert not any('M5' in t for t, _ in d.LOG['card-pitch-3.png'])     # cut 2: M5 dropped (never spoken)
    assert 'M10 wants 8.5. Builds?' in {t for t, _ in d.LOG['card-question-2.png']}


def test_no_forbidden_text(drawn):
    for n in EXPECTED:
        for s, _ in d.LOG[n]:
            for f in FORBIDDEN:
                assert f not in s.lower(), (n, s, f)
            if not n.startswith('card-question'):
                assert 'M10' not in s, (n, s)


def test_question_shows_no_answer(drawn):
    rows = {x for h, diff, r in d.ROWS for x in (f'{h}', diff, r)}
    allowed = {'A question', 'hole', 'vs 6.75', 'result', '8 mm hole. Message says M10.', 'M10 wants 8.5. Builds?',
               'Pause and think'} | rows | set(d.FIFTH)
    for i in (1, 2):
        texts = [s for s, _ in d.LOG[f'card-question-{i}.png']]
        assert set(texts) <= allowed, set(texts) - allowed
        assert texts.count('refused') == 2 and texts.count('built') == 2      # only the four filmed rows
        assert all(f in texts for f in d.FIFTH)


def test_pitch_bar_cut2_8mm_spans_the_whole_bar_and_no_sum(drawn):
    """Watch-through c1 MUST-FIX 2: "8 mm" spans the whole bar, the hole (6.75) is the middle only, and the bar
    carries no tooth numbers that would add up (0.68 + 6.75 + 0.68 = 8.11)."""
    g = d.PITCH_GEOM
    assert g['8 mm'] == (d.BAR[0], d.BAR[1])
    a, b = g['hole']
    assert d.BAR[0] < a < b < d.BAR[1]
    assert abs((b - a) / (d.BAR[1] - d.BAR[0]) - d.HOLE_M8 / d.M8[0]) < 0.01
    for i in (2, 3):
        texts = [t for t, _ in d.LOG[f'card-pitch-{i}.png']]
        assert texts.count('0.68') == 0, i
        assert texts.count('about half a pitch: 0.68') == 1, i           # step 1's tooth label only
        assert '8 mm' in texts and 'each end: about half a pitch tall' in texts, i
    assert 'hole: 6.75 mm' in {t for t, _ in d.LOG['card-pitch-3.png']}


def test_short_wall_card_cut2(drawn):
    """Short c2 (watch-through MUST-FIX 4): a cross-section card in the 1080 x 960 Short view that builds in two steps,
    the cause before the fix: 1 the wall already at 8 (nothing to cut), 2 the wall at 6.75 with grooves cut out to 8.
    Step 2 keeps step 1 on screen; text 44 px+ and inside the view."""
    for i in (1, 2):
        im = Image.open(os.path.join(drawn, f'card-short-wall-{i}.png'))
        assert im.size == (1080, 960)
    t1 = [t for t, _ in d.LOG['card-short-wall-1.png']]
    t2 = [t for t, _ in d.LOG['card-short-wall-2.png']]
    assert set(t1) <= set(t2)
    assert 'hole 8: wall already at 8' in t1 and 'nothing left to cut' in t1
    assert 'hole 6.75: grooves cut out to 8' in t2
    assert not any('6.75' in t for t in t1)                  # the fix number only in step 2
    assert all(px >= 44 for _, px in d.LOG['card-short-wall-2.png'])
    g = d.SHORT_GEOM
    assert g['wall8'] == g['line8']                          # step 1: the wall sits ON the 8 line
    assert g['wall675'] > g['line8']                         # step 2: the wall inside the 8 line
    assert abs((g['wall675'][1] - g['wall675'][0]) / (g['line8'][1] - g['line8'][0]) - 6.75 / 8) < 0.01
