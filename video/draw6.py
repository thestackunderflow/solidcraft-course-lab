"""Lesson 6's diagram cards, hook pictures, Short assets and thumbnails. Every SolidCraft, PrusaSlicer and Claude Code
picture is a crop of a real lab recording (out/l6/stills, video/stills6.py); every number comes from a lab file
(out/l6/compare.json, replay-*.json, hand/read-*.json, slices.json). Diagrams are visibly diagrams. Cards 1632 x 1200,
text 46 px or more; hooks 2560 x 1440 and 1080 x 1920; thumbnails 1280 x 720.
    docker run --rm --network none -v "$PWD:/work" -w /work cadcmp-openscad:2021.01 python3 video/draw6.py [cards|hooks|all]
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw2 as d2  # noqa: E402  (helpers and colours only)
from draw2 import BG, INK, RED, GREEN, GREY, BLUE, PAPER, AMBER, W, H, B, R, font, canvas, text, chip, fit, paste_c  # noqa: E402

LAB = d2.LAB
L6 = os.path.join(LAB, 'out', 'l6')
ST = os.path.join(L6, 'stills')
F = os.path.join(LAB, 'video', 'frames-l6')
os.makedirs(F, exist_ok=True)
CMP = json.load(open(os.path.join(L6, 'compare.json')))
R30 = json.load(open(os.path.join(L6, 'hand', 'read-30.json')))
R40 = json.load(open(os.path.join(L6, 'hand', 'read-40.json')))
assert CMP['with_list'] == {'runs': 3, 'passed': 3}
assert R30['geom']['opening_mm'] == 20.0 and R40['geom']['opening_mm'] == 30.0
assert [x['id'] for x in R30['score']['lines'] if not x['ok']] == ['C'] and R40['score']['passed']

# crops of the 2880x1800 stills (checked on the stills)
HOOK = (1250, 280, 2150, 1660)          # the hook in the 3D view (after Fit)
DIST = (2400, 784, 2780, 846)           # Measure panel: the Distance row
PROW = (1600, 1134, 2400, 1198)         # Parameters: the hook_depth row
SIDE = (1700, 150, 2100, 740)           # the J side straight on (the opening)


def save(im, name):
    im.save(os.path.join(F, name))
    print(name, im.size)


def st(name, box=None):
    im = Image.open(os.path.join(ST, name)).convert('RGB')
    return im.crop(box) if box else im


def steps(name, title, rows, draw_extra=None):
    """A card revealed in steps: rows = [(text, size, colour)], one more each step."""
    for k in range(len(rows)):
        im, d = canvas()
        text(d, (W / 2, 50), title, 64, anchor='ma')
        y = 230
        for i in range(k + 1):
            t, size, col = rows[i]
            for ln in t.split('\n'):
                text(d, (110, y), ln, size, col)
                y += int(size * 1.35)
            y += 40
        if draw_extra:
            draw_extra(im, d, k)
        save(im, f'card-{name}-{k + 1}.png')


def card_hair():
    steps('hair', 'At the hairdresser', [('"2 cm off the back"', 72, INK), ('"and keep the fringe"', 72, BLUE),
                                        ('then: check in the mirror', 72, GREEN)],
          lambda im, d, k: text(d, (W / 2, 1050), 'the change  +  a must-stay-true list', 58, GREY, anchor='ma') if k == 2 else None)


LIST = ['1  one closed body', '2  plate 60 tall × 20 wide', '3  walls 5 thick', '4  lip 10 tall',
        '5  holes 4.5, centred,|    15 & 45 below the top', '6  round top edges', '7  on its side in the slicer']


def card_list():
    bg = st('hand-start.png', HOOK).resize((520, 800))
    for k in range(7):
        im, d = canvas()
        text(d, (60, 40), 'Must stay true', 66, anchor='la')
        im.paste(bg, (W - 560, 260))
        y = 170
        for i in range(k + 1):
            for ln in LIST[i].split('|'):
                text(d, (60, y), ln, 50, GREEN if i == k else INK)
                y += 68
            y += 52
        save(im, f'card-list-{k + 1}.png')


def card_depth():
    for k in range(3):
        im, d = canvas()
        text(d, (W / 2, 50), 'Hook depth = the whole depth', 64, anchor='ma')
        s = 18
        ox, oy = 180, 900
        depth = (25, 30, 40)[k]
        pts = [(0, 0), (depth, 0), (depth, 10), (depth - 5, 10), (depth - 5, 5), (5, 5), (5, 30), (0, 30)]
        d.polygon([(ox + x * s, oy - y * s) for x, y in pts], fill=(176, 190, 212), outline=INK)
        d.line((ox, oy + 50, ox + depth * s, oy + 50), fill=INK, width=6)
        text(d, (ox + depth * s / 2, oy + 70), f'hook depth {depth}', 54, anchor='ma')
        gap = depth - 10
        d.line((ox + 5 * s, oy - 7.5 * s, ox + (depth - 5) * s, oy - 7.5 * s), fill=(RED if k == 1 else GREEN if k == 2 else BLUE), width=8)
        text(d, (ox + depth * s / 2, oy - 7.5 * s - 70), f'opening {gap}', 54, RED if k == 1 else GREEN if k == 2 else BLUE, anchor='ma')
        sums = ['5 + opening + 5', '5 + 20 + 5 = 30', '5 + 30 + 5 = 40']
        text(d, (W / 2, 260), sums[k], 72, (RED if k == 1 else GREEN if k == 2 else INK), anchor='ma')
        if k == 2:
            text(d, (W / 2, 370), 'for a 30 opening, type 40', 56, GREEN, anchor='ma')
        save(im, f'card-depth-{k + 1}.png')


def card_key():
    steps('key', 'The pass rule: an answer key', [('written first, before any run', 64, INK),
                                                  ('PASS = opening 30\n         + all 7 lines', 64, GREEN),
                                                  ("measured by our script,\nnot by Claude's words", 64, BLUE)])


def card_table():
    """Run by run, over the run's real final frame: the rows tick for run 2, run 3, then run 1 (replay)."""
    runs = {r['run']: r for r in CMP['runs']}
    cols = [('run 2', 'B2', 'B2-after.png'), ('run 3', 'B3', 'B3-after.png'), ('run 1 (replay)', 'B1', 'B2-after.png')]
    rows = ['opening 30'] + [x[3:].split(',')[0] for x in LIST]
    for k in range(3):
        im, d = canvas()
        d = ImageDraw.Draw(im)
        text(d, (90, 90), 'the pass rule, run by run', 52, GREY)
        for c in range(3):
            colr = INK if c <= k else (200, 205, 215)
            text(d, (980 + c * 200, 90), cols[c][0].replace(' (replay)', ''), 46, colr, anchor='ma')
            if c == 2:
                text(d, (980 + c * 200, 140), 'replay', 40, colr, anchor='ma')
        for i, r in enumerate(rows):
            y = 200 + i * 100
            text(d, (90, y), r, 48, INK)
            for c in range(k + 1):
                ok = all(x['ok'] for x in runs[cols[c][1]]['lines']) if i == 0 else runs[cols[c][1]]['lines'][i]['ok']
                text(d, (980 + c * 200, y - 6), '✓' if ok else '✗', 64, GREEN if ok else RED, path=R, anchor='ma')
        if k == 2:
            chip(d, (W / 2, H - 150), '3 of 3 kept every line', 56, anchor='m', bg=GREEN)
        save(im, f'card-table-{k + 1}.png')


def card_run1():
    """Run 1 in plain words (its recording was lost): what it did, why it stopped, how it was scored."""
    im, d = canvas()
    text(d, (W / 2, 60), 'Run 1 (its recording was lost)', 64, anchor='ma')
    rows = [('it moved the sketch\'s 4 corner points,', INK), ('then set hook depth to 40', INK),
            ('our cost guard (a spending limit per run)', GREY), ('stopped it as its turn ended', GREY),
            ('scored on a replay: a rule written', GREEN), ('before run 2', GREEN)]
    for i, (t, c) in enumerate(rows):
        text(d, (110, 250 + i * 130 + (i // 2) * 40), t, 58, c)
    save(im, 'card-run1.png')


def card_replay():
    """The replay table (out/l6/replay-*.json) over run 3's real slicer frame, labelled as run 3, live."""
    reps = {r: json.load(open(os.path.join(L6, f'replay-{r}.json'))) for r in ('B1', 'B2', 'B3')}
    im, d = canvas()
    text(d, (100, 200), 'The replay: a script, no AI,', 60, INK)
    text(d, (100, 290), "repeats each run's steps on a fresh hook", 54, INK)
    hdr = ('run', 'steps repeated', 'opening', 'result')
    xs = (100, 330, 780, 1100)
    for x, hh in zip(xs, hdr):
        text(d, (x, 440), hh, 46, GREY)
    for i, (r, name) in enumerate((('B2', 'run 2'), ('B3', 'run 3'), ('B1', 'run 1'))):
        rp = reps[r]
        y = 540 + i * 130
        assert rp['passed'] is True
        res = 'same as live' if rp['same_verdict'] else 'its score'
        for x, v in zip(xs, (name, str(rp['calls_replayed']), f"{rp['opening_mm']:.1f} mm", res)):
            text(d, (x, y), v, 52, GREEN if x == xs[3] else INK)
    save(im, 'card-replay.png')


def hooks():
    p30 = st('hand-p30.png', PROW)
    m30 = st('hand-m30.png', DIST)
    h30 = st('hand-m30.png', HOOK)
    m40 = st('hand-m40.png', DIST)
    for name, (w, h), vertical in (('hook-landscape.png', (2560, 1440), False), ('hook-vertical.png', (1080, 1920), True)):
        im = Image.new('RGB', (w, h), BG)
        d = ImageDraw.Draw(im)
        if not vertical:
            paste_c(im, fit(h30, 1100, 1150), 640, 760)
            paste_c(im, fit(p30, 1250, 200), 1880, 420)
            a = fit(m30, 1250, 300)
            paste_c(im, a, 1880, 900)
            d2r = (1880 - a.width // 2 - 14, 900 - a.height // 2 - 14, 1880 + a.width // 2 + 14, 900 + a.height // 2 + 14)
            d.rounded_rectangle(d2r, radius=20, outline=RED, width=12)
            chip(d, (1880, 230), 'typed 30', 74, anchor='m', bg=INK)
            chip(d, (1880, 1080), 'measured 20', 74, anchor='m', bg=RED)
        else:
            text(d, (w // 2, 50), 'I asked for a 30 mm opening', 58, anchor='ma')
            paste_c(im, fit(p30, w - 80, 200), w // 2, 300)
            chip(d, (w // 2, 380), 'typed 30', 64, anchor='m', bg=INK)
            paste_c(im, fit(h30, w - 200, 900), w // 2, 1000)
            a = fit(m30, w - 80, 220)
            paste_c(im, a, w // 2, 1600)
            chip(d, (w // 2, 1700), 'measured 20', 70, anchor='m', bg=RED)
        save(im, name)
    pair = Image.new('RGB', (1000, 1000), BG)
    d = ImageDraw.Draw(pair)
    paste_c(pair, fit(m30, 900, 200), 500, 220)
    chip(d, (500, 20), 'hook depth 30 → 20.00', 50, anchor='m', bg=RED)
    paste_c(pair, fit(m40, 900, 200), 500, 720)
    chip(d, (500, 520), 'hook depth 40 → 30.00', 50, anchor='m', bg=GREEN)
    save(pair, 'sc6s-pair.png')
    for name in ('thumbnail-primary.jpg', 'thumbnail-altA.jpg'):
        th = Image.new('RGB', (1280, 720), (24, 30, 40))
        d = ImageDraw.Draw(th)
        if 'primary' in name:
            th.paste(fit(h30, 520, 700), (20, 10))
            a = fit(m30, 700, 160)
            th.paste(a, (560, 120))
            d.rounded_rectangle((552, 112, 568 + a.width, 128 + a.height), radius=14, outline=RED, width=8)
            for y, wd, colr in ((360, 'TYPED 30,', INK), (520, 'GOT 20', RED)):
                fo = font(B, 120)
                ww = fo.getlength(wd)
                d.rounded_rectangle((900 - ww / 2 - 24, y - 70, 900 + ww / 2 + 24, y + 70), radius=22, fill=colr if colr == RED else (60, 70, 90))
                d.text((900, y), wd, font=fo, fill=PAPER, anchor='mm')
        else:
            th.paste(fit(st('B2-after.png', (0, 0, 2880, 1800)), 1240, 560), (20, 10))
            fo = font(B, 120)
            wd = '3/3 KEPT'
            ww = fo.getlength(wd)
            d.rounded_rectangle((640 - ww / 2 - 30, 560, 640 + ww / 2 + 30, 710), radius=24, fill=GREEN)
            d.text((640, 635), wd, font=fo, fill=PAPER, anchor='mm')
        th.save(os.path.join(F, name), quality=92)
        print(name)


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('cards', 'all'):
        card_hair(); card_list(); card_depth(); card_key(); card_table(); card_run1(); card_replay()
    if what in ('hooks', 'all'):
        hooks()
