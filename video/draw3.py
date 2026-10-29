"""Lesson 3's diagram cards and hook pictures. Every SolidCraft picture is a crop of a real lab recording (out/l3/stills,
from the 2880x1800 screen recordings, video/stills3.py); every number comes from a lab file (out/l3/compare.json,
replay-*.json). Diagrams are visibly diagrams. Cards 1632 x 1200, text >= 56 px; hooks 2560 x 1440 and 1080 x 1920.
    docker run --rm --network none -v "$PWD:/work" -w /work sc3-app:0.26.1 python3 video/draw3.py   (needs PIL: any image with it)
"""
import json
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw2 as d2  # noqa: E402  (helpers and colours only; draw2's own cards are not redrawn)
from draw2 import BG, INK, RED, GREEN, GREY, BLUE, PAPER, AMBER, W, H, B, R, M, font, canvas, text, chip, fit, paste_c  # noqa: E402

LAB = d2.LAB
L3 = os.path.join(LAB, 'out', 'l3')
ST = os.path.join(L3, 'stills')
F = os.path.join(LAB, 'video', 'frames-l3')
os.makedirs(F, exist_ok=True)
CMP = json.load(open(os.path.join(L3, 'compare.json')))['parts']
REP = {r: json.load(open(os.path.join(L3, f'replay-{r}.json'))) for r in ('A1', 'B1')}
HOOK = (1000, 250, 2150, 1650)       # the hook in the by-hand / plain recordings after the house (same zoom)
B1BOX = (1640, 300, 2760, 1700)      # Claude's window (right side) in the B1 recording


def still(name, box=None):
    im = Image.open(os.path.join(ST, name)).convert('RGB')
    return im.crop(box) if box else im


def save(im, name):
    im.save(os.path.join(F, name))
    print(name, im.size)


def n(v):
    return f'{v:,.0f}'


def j_pts(depth=25, plate=5):
    """The J's corners (x right, z up); plate = the back plate's thickness (B1 wrote it as depth - 10)."""
    return [(0, 0), (depth, 0), (depth, 10), (depth - 5, 10), (depth - 5, 5), (plate, 5), (plate, 60), (0, 60)]


def poly(pts, ox, oy, s):
    return [(ox + x * s, oy - z * s) for x, z in pts]


def draw_j(d, pts, ox, oy, s, fill=(214, 222, 236), outline=INK, width=8):
    p = poly(pts, ox, oy, s)
    d.polygon(p, fill=fill)
    d.line(p + [p[0]], fill=outline, width=width, joint='curve')
    return p


def card_recipe():
    im, d = canvas()
    text(d, (W / 2, 60), 'A recipe card with named amounts', 64, anchor='ma')
    d.rectangle((260, 170, 1372, 1110), fill=PAPER, outline=GREY, width=4)
    text(d, (320, 210), 'Amounts', 60, BLUE)
    text(d, (360, 300), 'flour  =  200 g', 64, path=M)
    d.line((360, 410, 1300, 410), fill=GREY, width=3)
    text(d, (360, 330 + 120), 'milk   =  300 ml', 64, path=M)
    text(d, (320, 600), 'Steps', 60, BLUE)
    text(d, (360, 690), '2. add the flour', 60, path=R)
    text(d, (360, 790), '3. stir in the milk', 60, path=R)
    text(d, (360, 890), '4. add the rest of the flour', 60, path=R)
    save(im, 'card-recipe-a.png')
    d.rectangle((560, 290, 1000, 380), fill=PAPER)
    text(d, (360, 300), 'flour  =  400 g', 64, RED, path=M)
    save(im, 'card-recipe-b.png')
    for y in (680, 880):
        d.rounded_rectangle((340, y, 1300, y + 86), radius=14, outline=GREEN, width=8)
    chip(d, (W / 2, 1000), 'change it once: every step follows', 54, anchor='m', bg=GREEN)
    save(im, 'card-recipe.png')


def card_catch():
    im, d = canvas()
    text(d, (W / 2, 50), 'Two lengths depend on the depth', 64, anchor='ma')
    s = 13
    ox, oy = 640, 1100
    p = draw_j(d, j_pts(), ox, oy, s)
    d.line((p[0], p[1]), fill=RED, width=18)
    text(d, ((p[0][0] + p[1][0]) / 2, oy + 20), '25 = hook_depth', 56, RED, anchor='ma')
    save(im, 'card-catch-a.png')
    d.line((p[4], p[5]), fill=BLUE, width=18)
    text(d, ((p[4][0] + p[5][0]) / 2, p[4][1] - 100), '15', 72, BLUE, anchor='ma')
    save(im, 'card-catch-b.png')
    chip(d, (1180, 360), '15 = hook_depth − 5 − 5', 56, anchor='m', bg=BLUE)
    chip(d, (1180, 470), 'a formula of the names', 52, anchor='m', bg=GREEN)
    save(im, 'card-catch.png')


def card_expected():
    im, d = canvas()
    text(d, (W / 2, 50), 'Expected for hook_depth = 40', 64, anchor='ma')
    s = 13
    ox, oy = 90, 1100
    draw_j(d, j_pts(40), ox, oy, s)
    rows = [('25 → 40', '+15 mm', INK), ('plate 5 x 60', '300', INK), ('arm 35 x 5', '175', INK), ('lip 5 x 5', '25', INK),
            ('500 mm² x 20', '10,000 mm³', GREEN)]
    for i, (a, b, c) in enumerate(rows):
        y = 230 + i * 150
        text(d, (1110, y), a, 58, c, anchor='ra')
        text(d, (1170, y), b, 58, c, path=B)
        if i < 4:
            save(im, f'card-expected-{i + 1}.png')
    save(im, 'card-expected.png')


def card_plainwhy():
    im, d = canvas()
    text(d, (W / 2, 50), 'Plain numbers: d1 = 40', 64, anchor='ma')
    s = 13
    ox, oy = 160, 1100
    pts = j_pts()
    p = draw_j(d, pts, ox, oy, s)
    # the wanted bottom: 40
    d.line((p[0], (ox + 40 * s, oy)), fill=RED, width=14)
    text(d, (ox + 20 * s, oy + 20), 'd1 = 40', 56, RED, anchor='ma')
    for a, b, lab in ((p[3], p[2], '5'), (p[5], p[4], '15'), ((ox, p[6][1]), p[6], '5')):
        d.line((a, b), fill=BLUE, width=14)
        text(d, ((a[0] + b[0]) / 2 + (40 if lab == '5' and a[0] == ox else 0), a[1] - 80), lab, 60, BLUE, anchor='ma')
    chip(d, (1150, 420), '5 + 15 + 5 = 25, not 40', 58, anchor='m', bg=RED)
    save(im, 'card-plainwhy-a.png')
    chip(d, (1150, 560), 'fix: d5 = d1 − 10', 58, anchor='m', bg=GREEN)
    save(im, 'card-plainwhy.png')


def card_compare():
    im, d = canvas()
    text(d, (W / 2, 40), 'hook_depth 25 → 40, measured', 62, anchor='ma')
    cols = [('By hand,\nnames', '5 names', 'one number', '10,000', GREEN),
            ('By hand,\nplain', 'd1 to d7', 'refused', 'still 8,500', RED),
            ('Claude,\nnot asked', '0 names\n(2 runs)', 'drew it again /\nread "deep"\nas the push', '10,000 /\n17,000', AMBER),
            ('Claude,\nasked', '5 names\n(2 runs)', 'one change', '10,000 /\n37,500', BLUE)]
    cw = 390
    for i, (head, names, edit, after, c) in enumerate(cols):
        x = 30 + i * (cw + 10)
        d.rounded_rectangle((x, 140, x + cw, 1090), radius=24, fill=PAPER, outline=c, width=8)
        for j, ln in enumerate(head.split('\n')):
            text(d, (x + cw / 2, 170 + j * 64), ln, 54, c, anchor='ma')
        for k, (lab, val) in enumerate((('names', names), ('the edit', edit), ('after', after))):
            y = 340 + k * 240
            text(d, (x + cw / 2, y), lab, 40, GREY, path=R, anchor='ma')
            for j, ln in enumerate(val.split('\n')):
                fs = 52
                while font(B, fs).getlength(ln) > cw - 30:
                    fs -= 2
                text(d, (x + cw / 2, y + 56 + j * 56), ln, fs, INK, anchor='ma')
        save(im, f'card-compare-{i + 1}.png')
    text(d, (W / 2, 1110), f'replay, no AI: A1 {n(REP["A1"]["summary"]["volume_mm3"])} · B1 {n(REP["B1"]["summary"]["volume_mm3"])} mm³', 52, INK, anchor='ma')
    save(im, 'card-compare.png')


def card_recap():
    im, d = canvas()
    text(d, (W / 2, 60), 'Remember the recipe card', 66, anchor='ma')
    lines = [('Named amounts at the top', BLUE), ('Lengths that depend: a formula', GREEN), ('Check the first build: 8,500', RED)]
    for i, (s, c) in enumerate(lines):
        y = 260 + i * 260
        d.rounded_rectangle((160, y, 1472, y + 170), radius=24, fill=PAPER, outline=c, width=8)
        text(d, (W / 2, y + 50), s, 64, c, anchor='ma')
    save(im, 'card-recap.png')


def card_bwrong():
    """B1: Claude's corner list against the right one (from its logged sketch.line points)."""
    im, d = canvas()
    text(d, (W / 2, 50), "Claude's run B1: one corner", 64, anchor='ma')
    s = 12
    draw_j(d, j_pts(25, 5), 200, 1040, s, fill=(214, 236, 220), outline=GREEN)
    text(d, (350, 150), 'needed', 56, GREEN, anchor='ma')
    text(d, (350, 230), 'x = thickness', 52, GREEN, path=M, anchor='ma')
    chip(d, (350, 1110), 'plate 5 · 8,500', 46, anchor='m', bg=GREEN)
    save(im, 'card-bwrong-1.png')
    draw_j(d, j_pts(25, 15), 950, 1040, s, fill=(240, 214, 214), outline=RED)
    text(d, (350, 150), 'needed', 56, GREEN, anchor='ma')
    text(d, (350, 230), 'x = thickness', 52, GREEN, path=M, anchor='ma')
    text(d, (1100, 160), 'Claude wrote', 56, RED, anchor='ma')
    text(d, (1100, 230), 'x = hook_depth − 2·thickness', 44, RED, path=M, anchor='ma')
    chip(d, (350, 1110), 'plate 5 · 8,500', 46, anchor='m', bg=GREEN)
    chip(d, (1100, 1110), 'plate 15 · 19,500', 46, anchor='m', bg=RED)
    save(im, 'card-bwrong.png')


def hook(w, h, vertical=False):
    im = Image.new('RGB', (w, h), BG)
    d = ImageDraw.Draw(im)
    a0 = still('hand-40.png', HOOK)
    b0 = still('plain-25.png', HOOK)
    if not vertical:
        a, b = fit(a0, w // 2 - 60, h - 300), fit(b0, w // 2 - 60, h - 300)
        paste_c(im, a, w // 4, h / 2 + 50)
        paste_c(im, b, 3 * w // 4, h / 2 + 50)
        chip(d, (w // 4, 30), 'NAMED SIZES · 40 x 20 x 60', 66, anchor='m', bg=GREEN)
        chip(d, (3 * w // 4, 30), 'PLAIN NUMBERS · REFUSED', 66, anchor='m', bg=RED)
        chip(d, (w // 2, h - 140), '25 → 40', 84, anchor='m', bg=INK)
    else:
        text(d, (w // 2, 70), 'Same change: 25 → 40', 76, anchor='ma')
        a = fit(still('hand-40.png', (1000, 450, 2150, 1600)), w - 120, 760)
        b = fit(still('plain-25.png', (1000, 450, 2150, 1600)), w - 120, 760)
        paste_c(im, a, w // 2, 190 + a.height // 2)
        paste_c(im, b, w // 2, 1000 + b.height // 2)
        chip(d, (w // 2, 190 + a.height - 10), 'NAMES · 40', 64, anchor='m', bg=GREEN)
        chip(d, (w // 2, 1000 + b.height - 10), 'PLAIN · REFUSED', 64, anchor='m', bg=RED)
    return im


def short_assets():
    im, d = canvas(1000, 1000)
    text(d, (500, 40), 'Plain numbers: d1 = 40', 54, anchor='ma')
    s = 11
    ox, oy = 160, 900
    p = draw_j(d, j_pts(), ox, oy, s)
    d.line((p[0], (ox + 40 * s, oy)), fill=RED, width=12)
    text(d, (ox + 20 * s, oy + 16), '40', 52, RED, anchor='ma')
    for a, b, lab in ((p[3], p[2], '5'), (p[5], p[4], '15'), ((ox, p[6][1]), p[6], '5')):
        d.line((a, b), fill=BLUE, width=12)
        text(d, ((a[0] + b[0]) / 2 + (36 if lab == '5' and a[0] == ox else 0), a[1] - 62), lab, 48, BLUE, anchor='ma')
    chip(d, (640, 300), '5 + 15 + 5 = 25', 50, anchor='m', bg=RED)
    save(im, 'sc3s-why.png')
    im = Image.new('RGB', (1000, 1000), BG)
    d = ImageDraw.Draw(im)
    a = fit(still('hand-40.png', (1000, 300, 2150, 1650)), 480, 820)
    b = fit(still('plain-25.png', (1000, 300, 2150, 1650)), 480, 820)
    paste_c(im, a, 255, 520)
    paste_c(im, b, 745, 520)
    chip(d, (255, 20), 'NAMES · 40', 50, anchor='m', bg=GREEN)
    chip(d, (745, 20), 'PLAIN · REFUSED', 44, anchor='m', bg=RED)
    chip(d, (500, 900), '25 → 40', 56, anchor='m', bg=INK)
    save(im, 'sc3s-pair.png')
    for name, src, box in (('sc3s-formula.png', 'hand-formula.png', (1150, 900, 2150, 1650)),
                           ('sc3s-thick.png', 'B1-thick.png', B1BOX)):
        im = Image.new('RGB', (1000, 1000), BG)
        paste_c(im, fit(still(src, box), 960, 960), 500, 500)
        save(im, name)


def thumbs():
    for name, words, pic in (('thumbnail-primary.jpg', 'REFUSED', 'pair'), ('thumbnail-altA.jpg', '19,500, NOT 8,500', 'b1')):
        im = Image.new('RGB', (1280, 720), (24, 30, 40))
        d = ImageDraw.Draw(im)
        if pic == 'pair':
            a = fit(still('hand-40.png', HOOK), 600, 600)
            b = fit(still('plain-25.png', HOOK), 600, 600)
            im.paste(a, (20, 110)); im.paste(b, (660, 110))
            chip(d, (320, 20), 'NAMES: 40', 60, anchor='m', bg=GREEN)
            chip(d, (960, 20), '25 → 40', 60, anchor='m', bg=INK)
            f = font(B, 96)
            w = f.getlength(words)
            d.rounded_rectangle((960 - w / 2 - 30, 470, 960 + w / 2 + 30, 630), radius=24, fill=RED)
            d.text((960, 550), words, font=f, fill=PAPER, anchor='mm')
        else:
            a = fit(still('B1-thick.png', B1BOX), 760, 640)
            im.paste(a, (260, 70))
            chip(d, (640, 10), 'CLAUDE, ASKED FOR NAMES', 52, anchor='m', bg=BLUE)
            f = font(B, 100)
            w = f.getlength(words)
            d.rounded_rectangle((640 - w / 2 - 30, 540, 640 + w / 2 + 30, 690), radius=24, fill=RED)
            d.text((640, 615), words, font=f, fill=PAPER, anchor='mm')
        im.save(os.path.join(F, name), quality=92)
        print(name)


if __name__ == '__main__':
    card_recipe(); card_catch(); card_expected(); card_plainwhy(); card_compare(); card_recap(); card_bwrong()
    save(hook(2560, 1440), 'hook-landscape.png')
    save(hook(1080, 1920, vertical=True), 'hook-vertical.png')
    short_assets()
    thumbs()
