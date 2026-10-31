"""Lesson 5's diagram cards, hook pictures, Short assets and thumbnails. Every SolidCraft and PrusaSlicer picture is a
crop of a real lab recording (out/l5/stills, video/stills5.py); every number comes from a lab file (out/l5/slices.json,
compare.json, saveface.json, hand/sent-check.jsonl). Diagrams are visibly diagrams. Cards 1632 x 1200, text 46 px or
more; hooks 2560 x 1440 and 1080 x 1920; thumbnails 1280 x 720.
    docker run --rm --network none -v "$PWD:/work" -w /work cadcmp-openscad:2021.01 python3 video/draw5.py [cards|hooks|all]
"""
import json
import math
import os
import struct
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw2 as d2  # noqa: E402  (helpers and colours only)
from draw2 import BG, INK, RED, GREEN, GREY, BLUE, PAPER, AMBER, W, H, B, R, font, canvas, text, chip, fit, paste_c  # noqa: E402

LAB = d2.LAB
L5 = os.path.join(LAB, 'out', 'l5')
ST = os.path.join(L5, 'stills')
F = os.path.join(LAB, 'video', 'frames-l5')
os.makedirs(F, exist_ok=True)
SL = json.load(open(os.path.join(L5, 'slices.json')))['files']
CMP = json.load(open(os.path.join(L5, 'compare.json')))['runs']


def save(im, name):
    im.save(os.path.join(F, name))
    print(name, im.size)


def st(name, box=None):
    im = Image.open(os.path.join(ST, name)).convert('RGB')
    return im.crop(box) if box else im


def ring(d, box, col=RED, w=10):
    d.rounded_rectangle(box, radius=24, outline=col, width=w)


def mins(t):
    return t.split('m')[0].strip() + ' min'


STAND, SIDE = SL['standing']['as set'], SL['side']['as set']
assert STAND['warnings'] and not SIDE['warnings'], 'standing must warn, side must not'
assert SL['standing']['supports on']['support_g'] == 0 and SL['side']['supports on']['support_g'] == 0
assert STAND['total_g'] == SIDE['total_g'] == 5.37
assert STAND['layers'] == 300 and SIDE['layers'] == 100

# crops of the 2880x1800 stills (checked on the stills)
HOOK_STAND = (700, 620, 1300, 1140)      # the standing hook on the plate
HOOK_SIDE = (740, 760, 1320, 1180)       # the side-lying hook on the plate
INFO = (1960, 1590, 2880, 1720)          # Sliced Info: Estimated printing time, normal / stealth
WARN = (880, 1410, 1730, 1720)           # the opened warning box (standing)


def mesh_png(size=(700, 700)):
    """The hook's real triangles (the STL Save As Mesh wrote), drawn as a wireframe in an iso view."""
    data = open(os.path.join(L5, 'saveface', 'save-before-face.stl'), 'rb').read()
    n = struct.unpack('<I', data[80:84])[0]
    tris = [struct.unpack('<9f', data[84 + 50 * i + 12:84 + 50 * i + 48]) for i in range(n)]
    a, e = math.radians(35), math.radians(25)

    def pr(x, y, z):
        u = x * math.cos(a) + y * math.sin(a)
        v = -x * math.sin(a) + y * math.cos(a)
        return u, z * math.cos(e) - v * math.sin(e)
    def depth(t):
        return sum(-t[k] * math.sin(a) * math.cos(e) + t[k + 1] * math.cos(a) * math.cos(e) + t[k + 2] * math.sin(e) for k in (0, 3, 6))
    order = sorted(tris, key=depth)
    pts = [[pr(*t[k:k + 3]) for k in (0, 3, 6)] for t in order]
    xs = [p[0] for t in pts for p in t]
    ys = [p[1] for t in pts for p in t]
    s = min((size[0] - 60) / (max(xs) - min(xs)), (size[1] - 60) / (max(ys) - min(ys)))
    im = Image.new('RGB', size, PAPER)
    d = ImageDraw.Draw(im)
    L = (0.4, -0.5, 0.75)
    for t, q2 in zip(order, pts):
        ux, uy, uz = t[3] - t[0], t[4] - t[1], t[5] - t[2]
        vx, vy, vz = t[6] - t[0], t[7] - t[1], t[8] - t[2]
        nx, ny, nz = uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx
        ln = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
        sh = max(0.0, (nx * L[0] + ny * L[1] + nz * L[2]) / ln)
        c = tuple(int(v * (0.55 + 0.45 * sh)) for v in (190, 205, 235))
        q = [(30 + (x - min(xs)) * s, size[1] - 30 - (y - min(ys)) * s) for x, y in q2]
        d.polygon(q, fill=c, outline=(60, 80, 120))
    return im, n


def card_copy():
    mesh, n = mesh_png()
    for k in range(3):
        im, d = canvas()
        text(d, (W / 2, 40), ('The recipe stays in SolidCraft', 'The printer gets a frozen copy', 'A frozen copy: an STL or 3MF')[k], 60, anchor='ma')
        d.rounded_rectangle((60, 200, 620, 760), radius=30, fill=(232, 238, 248), outline=INK, width=6)
        text(d, (340, 250), 'the recipe', 56, anchor='ma')
        for i, ln in enumerate(('plate_height 60', 'width 20', 'hole_d 4.5', 'fillet 2', '… history')):
            text(d, (110, 360 + i * 74), ln, 48, GREY)
        if k >= 1:
            d.line((650, 480, 820, 480), fill=INK, width=10)
            d.polygon([(820, 450), (870, 480), (820, 510)], fill=INK)
            paste_c(im, fit(mesh, 640, 640), 1230, 500)
            text(d, (1230, 840), 'frozen copy · STL / 3MF', 54, BLUE, anchor='ma')
        if k == 2:
            chip(d, (W / 2, 960), f'{n:,} triangles · no names · no history', 54, anchor='m', bg=INK)
            text(d, (W / 2, 1080), 'like a loaf baked from the recipe', 48, GREY, anchor='ma')
        save(im, f'card-copy-{k + 1}.png')


def book(d, cx, base, standing, col):
    if standing:
        d.rectangle((cx - 45, base - 330, cx + 45, base), fill=col, outline=INK, width=6)
    else:
        d.rectangle((cx - 230, base - 70, cx + 230, base), fill=col, outline=INK, width=6)


def card_book():
    send = st('hand-send1.png', (2396, 580, 2864, 900))
    for k in range(3):
        im, d = canvas()
        text(d, (W / 2, 40), ('A book on its end', 'or lying flat', 'The print face: the face it sits on')[k], 60, anchor='ma')
        d.line((80, 700, W - 80, 700), fill=INK, width=8)
        text(d, (W / 2, 720), 'the table', 44, GREY, anchor='ma')
        book(d, 420, 700, True, (190, 205, 230))
        if k >= 1:
            book(d, 1150, 700, False, (190, 205, 230))
            d.line((920, 700, 1380, 700), fill=GREEN, width=16)
        if k == 2:
            p = fit(send, 700, 360)
            x0 = W // 2 - p.width // 2
            im.paste(p, (x0, 780))
            dd = ImageDraw.Draw(im)
            k_ = p.width / 468.0
            ring(dd, (x0 - 6, 780 + int((674 - 580) * k_) - 8, x0 + p.width + 6, 780 + int((718 - 580) * k_) + 8), RED, 8)
            text(dd, (60, 1130), 'SolidCraft 0.28.0 · Send to Slicer', 44, GREY)
        save(im, f'card-book-{k + 1}.png')


def card_checks():
    rows = ['one body', 'the size (mm)', 'closed: a skin with no gaps', 'the face it lies on']
    for k in range(4):
        im, d = canvas()
        text(d, (W / 2, 40), 'Four checks before you print', 64, anchor='ma')
        for i in range(k + 1):
            y = 230 + i * 210
            d.ellipse((120, y, 250, y + 130), fill=BLUE)
            text(d, (185, y + 65), str(i + 1), 72, PAPER, anchor='mm')
            text(d, (300, y + 30), rows[i], 64, INK)
        save(im, f'card-checks-{k + 1}.png')


def card_install():
    ps = st('hand-standing-open.png')
    sl = st('hand-send1.png', (2400, 840, 2850, 905))
    for k in range(3):
        im, d = canvas()
        text(d, (W / 2, 40), 'No slicer yet?', 64, anchor='ma')
        p = fit(ps, 760, 480)
        im.paste(p, (40, 170))
        steps = [('PrusaSlicer: free', 'prusa3d.com'), ('first start:', 'pick your printer'), ('SolidCraft lists it', 'by itself')]
        for i in range(k + 1):
            text(d, (840, 200 + i * 170), f'{i + 1}. ' + steps[i][0], 50, INK)
            text(d, (900, 262 + i * 170), steps[i][1], 46, GREY)
        if k == 2:
            q = fit(sl, 1300, 200)
            im.paste(q, (W // 2 - q.width // 2, 790))
            text(ImageDraw.Draw(im), (W // 2, 1060), 'Send to Slicer · the Slicer row', 44, GREY, anchor='ma')
        save(im, f'card-install-{k + 1}.png')


def card_compare():
    rows = [('height · layers', '60 mm · 300', '20 mm · 100'),
            ('time (estimate)', mins(STAND['time']), mins(SIDE['time']).replace('14', '15') if False else '15 min'),
            ('plastic', f"{STAND['total_g']} g", f"{SIDE['total_g']} g"),
            ('warning', 'low bed adhesion', 'none')]
    for k in range(2):
        im, d = canvas()
        text(d, (W / 2, 30), 'Same hook, same slicer', 60, anchor='ma')
        for j, (h, colr) in enumerate((('standing', RED), ('on its side', GREEN))):
            x = 900 + j * 460
            chip(d, (x, 130), h, 52, anchor='m', bg=colr)
        for r, (name, a, b) in enumerate(rows):
            y = 300 + r * 170
            text(d, (50, y), name, 50, INK)
            text(d, (900, y), a, 52, RED if r in (1, 3) else INK, anchor='ma')
            text(d, (1360, y), b, 52, GREEN if r in (1, 3) else INK, anchor='ma')
        text(d, (W / 2, 1000), 'times: the slicer’s estimate · Prusa MK4S · 0.20mm SPEED', 42, GREY, anchor='ma')
        if k == 1:
            chip(d, (W / 2, 1070), 'supports on: 0 g added, the warning goes', 46, anchor='m', bg=INK)
        save(im, f'card-compare-{k + 1}.png')


def card_files():
    for k in range(2):
        im, d = canvas()
        text(d, (W / 2, 40), 'Two kinds of frozen copy', 60, anchor='ma')
        for j, (name, l1, l2) in enumerate((('STL', 'triangles only', 'no unit'), ('3MF', 'triangles', '+ millimetre inside'))):
            if k == 0 and j == 1:
                continue
            x = 420 + j * 800
            d.rounded_rectangle((x - 330, 200, x + 330, 760), radius=30, fill=(232, 238, 248), outline=INK, width=6)
            text(d, (x, 240), name, 90, BLUE, anchor='ma')
            text(d, (x, 420), l1, 54, INK, anchor='ma')
            text(d, (x, 510), l2, 54, RED if j == 0 else GREEN, anchor='ma')
        text(d, (420, 820), '25 mm? 25 inches?', 52, RED, anchor='ma')
        text(d, (420, 900), 'slicers read it as mm', 46, GREY, anchor='ma')
        save(im, f'card-files-{k + 1}.png')


def card_claude():
    a1, b1 = CMP['A1'], CMP['B1']
    assert a1['last_lie'] == 'standing' and b1['last_lie'] == 'on its side'
    assert all(a1['score']['read_before_send'].values()) and all(b1['score']['read_before_send'].values())
    t = {r: mins(CMP[r]['files_sent'][-1]['as set']['time']) for r in ('A1', 'B1')}
    cols = [('By hand', 'as drawn'), ('By hand', 'print face'), ('Claude', 'not asked'), ('Claude', 'asked')]
    rows = ['body · closed · size read', 'how it lies', "slicer's time"]
    cells = [[('Properties + slicer', INK), ('standing', RED), ('33 min', RED)],
             [('Properties + slicer', INK), ('on its side', GREEN), ('15 min', GREEN)],
             [('yes, in its first read', GREEN), ('standing', RED), ('33 min', RED)],
             [('yes', GREEN), ('on its side', GREEN), ('15 min', GREEN)]]
    for k in range(4):
        im, d = canvas()
        text(d, (W / 2, 30), 'Side by side' + (' · 1 run each' if k >= 2 else ''), 60, anchor='ma')
        show = [0, 1] if k < 2 else [2, 3]
        for j, ci in enumerate(show):
            x = 860 + j * 470
            text(d, (x, 140), cols[ci][0], 52, INK, anchor='ma')
            text(d, (x, 205), cols[ci][1], 48, GREY, anchor='ma')
            for r in range(3):
                if k % 2 == 1 or j == 0:
                    c, col = cells[ci][r]
                    chip(d, (x, 330 + r * 190), c, 42, anchor='m', bg=col)
        for r, name in enumerate(rows):
            text(d, (30, 340 + r * 190), name, 40, INK)
        if k == 3:
            text(d, (W / 2, 960), 'Replayed with no AI: the same file both times', 48, INK, anchor='ma')
            text(d, (W / 2, 1040), "times: the slicer's estimate", 42, GREY, anchor='ma')
        save(im, f'card-claude-{k + 1}.png')


def hooks():
    s_hook = st('hand-standing-warning.png', HOOK_STAND)
    s_warn = st('hand-standing-warning.png', WARN)
    f_hook = st('hand-side-sliced.png', HOOK_SIDE)
    for name, (w, h), vertical in (('hook-landscape.png', (2560, 1440), False), ('hook-vertical.png', (1080, 1920), True)):
        im = Image.new('RGB', (w, h), BG)
        d = ImageDraw.Draw(im)
        if not vertical:
            paste_c(im, fit(s_hook, w // 2 - 120, 760), w // 4, 560)
            paste_c(im, fit(f_hook, w // 2 - 120, 760), 3 * w // 4, 560)
            paste_c(im, fit(s_warn, w // 2 - 160, 400), w // 4, 1150)
            chip(d, (w // 4, 30), 'STANDING · 33 min', 74, anchor='m', bg=RED)
            chip(d, (3 * w // 4, 30), 'ON ITS SIDE · 15 min', 74, anchor='m', bg=GREEN)
            text(d, (3 * w // 4, 1120), 'no warning', 70, GREEN, anchor='ma')
            chip(d, (w // 2, h - 110), "same hook · same 5.37 g · the slicer's estimates", 52, anchor='m', bg=INK)
        else:
            text(d, (w // 2, 40), 'Same hook, same plastic', 64, anchor='ma')
            a, b = fit(s_hook, w - 200, 640), fit(f_hook, w - 200, 520)
            paste_c(im, a, w // 2, 170 + a.height // 2)
            chip(d, (w // 2, 180 + a.height), 'STANDING · 33 min · WARNING', 52, anchor='m', bg=RED)
            paste_c(im, b, w // 2, 1060 + b.height // 2)
            chip(d, (w // 2, 1070 + b.height), 'ON ITS SIDE · 15 min', 56, anchor='m', bg=GREEN)
        save(im, name)
    pair = Image.new('RGB', (1000, 1000), BG)
    d = ImageDraw.Draw(pair)
    paste_c(pair, fit(s_hook, 900, 430), 500, 260)
    paste_c(pair, fit(f_hook, 900, 400), 500, 760)
    chip(d, (500, 10), 'STANDING · 33 min · WARNING', 44, anchor='m', bg=RED)
    chip(d, (500, 530), 'ON ITS SIDE · 15 min', 44, anchor='m', bg=GREEN)
    save(pair, 'sc5s-pair.png')
    for name, words in (('thumbnail-primary.jpg', ('33 MIN', '15 MIN')), ('thumbnail-altA.jpg', ('LAY IT FLAT', None))):
        th = Image.new('RGB', (1280, 720), (24, 30, 40))
        d = ImageDraw.Draw(th)
        if words[1]:
            th.paste(fit(s_hook, 600, 560), (20, 10))
            th.paste(fit(f_hook, 600, 560), (660, 60))
            for x, wd, colr in ((320, words[0], RED), (960, words[1], GREEN)):
                fo = font(B, 110)
                ww = fo.getlength(wd)
                d.rounded_rectangle((x - ww / 2 - 26, 540, x + ww / 2 + 26, 690), radius=22, fill=colr)
                d.text((x, 615), wd, font=fo, fill=PAPER, anchor='mm')
            d.text((1270, 8), 'EST.', font=font(B, 40), fill=PAPER, anchor='ra')
            d.text((24, 470), '⚠', font=font(B, 80), fill=AMBER)
        else:
            th.paste(fit(f_hook, 900, 520), (190, 10))
            fo = font(B, 120)
            ww = fo.getlength(words[0])
            d.rounded_rectangle((640 - ww / 2 - 30, 530, 640 + ww / 2 + 30, 690), radius=24, fill=GREEN)
            d.text((640, 610), words[0], font=fo, fill=PAPER, anchor='mm')
        th.save(os.path.join(F, name), quality=92)
        print(name)


def recap():
    for k in range(4):
        im, d = canvas()
        text(d, (W / 2, 40), 'Remember', 64, anchor='ma')
        lines = ['frozen copy = a baked loaf (STL / 3MF)', 'the slicer cuts it into layers', 'print face: lay the book flat',
                 'check: one body · size · closed']
        for i in range(k + 1):
            text(d, (100, 230 + i * 200), lines[i], 58, INK)
        save(im, f'card-recap-{k + 1}.png')


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('cards', 'all'):
        card_copy(); card_book(); card_checks(); card_install(); card_compare(); card_files(); card_claude(); recap()
    if what in ('hooks', 'all'):
        hooks()
