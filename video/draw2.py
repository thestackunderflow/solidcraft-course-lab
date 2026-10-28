"""Lesson 2's diagram cards and hook pictures. Every SolidCraft picture is a crop of a real lab recording (out/l2/stills,
taken from the 2880x1800 screen recordings); every number comes from a lab file. Diagrams are visibly diagrams.
Cards are 1632 x 1200 (the split slide's picture box at 2x), text >= 56 px; hooks 2560 x 1440 and 1080 x 1920.
    docker run --rm --network none -v "$PWD:/work" -w /work cadcmp-openscad:2021.01 python3 video/draw2.py
"""
import json
import os

from PIL import Image, ImageDraw, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
L2 = os.path.join(LAB, 'out', 'l2')
ST = os.path.join(L2, 'stills')
F = os.path.join(LAB, 'video', 'frames-l2')
os.makedirs(F, exist_ok=True)
FD = '/usr/share/fonts/truetype/dejavu/'
B, R, M = FD + 'DejaVuSans-Bold.ttf', FD + 'DejaVuSans.ttf', FD + 'DejaVuSansMono-Bold.ttf'
BG, INK, RED, GREEN, GREY, BLUE, PAPER, AMBER = (236, 239, 244), (31, 41, 55), (183, 28, 28), (27, 127, 59), \
    (110, 120, 138), (29, 78, 216), (255, 255, 255), (180, 110, 0)
W, H = 1632, 1200
CMP = json.load(open(os.path.join(L2, 'compare.json')))
REP = json.load(open(os.path.join(L2, 'replay.json')))


def font(p, s):
    return ImageFont.truetype(p, s)


def canvas(w=W, h=H, bg=BG):
    im = Image.new('RGB', (w, h), bg)
    return im, ImageDraw.Draw(im)


def text(d, xy, s, size=60, fill=INK, path=B, anchor='la'):
    d.text(xy, s, font=font(path, size), fill=fill, anchor=anchor)


def chip(d, xy, s, size=48, fg=PAPER, bg=INK, pad=18, anchor='l'):
    f = font(B, size)
    w = f.getlength(s)
    x, y = xy
    if anchor == 'm':
        x -= (w + 2 * pad) / 2
    if anchor == 'r':
        x -= w + 2 * pad
    d.rounded_rectangle((x, y, x + w + 2 * pad, y + size + 2 * pad), radius=18, fill=bg)
    d.text((x + pad, y + pad), s, font=f, fill=fg)


def still(name, box):
    return Image.open(os.path.join(ST, name)).convert('RGB').crop(box)


def fit(im, w, h):
    im = im.copy()
    im.thumbnail((w, h), Image.LANCZOS)
    return im


def paste_c(dst, pic, cx, cy, border=GREY):
    x, y = int(cx - pic.width / 2), int(cy - pic.height / 2)
    dst.paste(pic, (x, y))
    ImageDraw.Draw(dst).rectangle((x - 3, y - 3, x + pic.width + 2, y + pic.height + 2), outline=border, width=4)


def save(im, name):
    im.save(os.path.join(F, name))
    print(name, im.size)


# the J in sketch units (x right, z up), the walk the viewer types
J = [(0, 0), (25, 0), (25, 10), (20, 10), (20, 5), (5, 5), (5, 60), (0, 60)]


def j_poly(ox, oy, s, flip=False):
    return [(ox + x * s, oy + (z * s if flip else -z * s)) for x, z in J]


def sheet(d, box, tilt=0):
    x0, y0, x1, y1 = box
    d.rectangle((x0 + 14, y0 + 14, x1 + 14, y1 + 14), fill=(200, 205, 214))
    d.rectangle(box, fill=PAPER, outline=GREY, width=4)


# ---------- the diagram cards ----------
def card_sketch():
    im, d = canvas()
    text(d, (W / 2, 70), 'A sketch: a drawing on paper', 66, anchor='ma')
    sheet(d, (430, 200, 1200, 1020))
    d.line(j_poly(690, 960, 11) + [j_poly(690, 960, 11)[0]], fill=INK, width=10, joint='curve')
    d.polygon([(1150, 300), (1260, 190), (1290, 220), (1180, 330)], fill=AMBER)        # a pencil
    d.polygon([(1150, 300), (1180, 330), (1135, 345)], fill=INK)
    chip(d, (W / 2, 1060), 'flat lines · no thickness', 56, anchor='m')
    save(im, 'card-sketch.png')


def block(d, ox, oy, s, depth, colour_face=(176, 190, 212), colour_side=(120, 136, 160)):
    dx, dy = depth, -depth * 0.55
    face = j_poly(ox, oy, s)
    back = [(x + dx, y + dy) for x, y in face]
    for i in range(len(face)):
        a, b = face[i], face[(i + 1) % len(face)]
        d.polygon([a, b, back[(i + 1) % len(face)], back[i]], fill=colour_side, outline=INK)
    d.polygon(face, fill=colour_face, outline=INK)


def card_extrude():
    im, d = canvas()
    text(d, (W / 2, 70), 'An extrude: push it out of the paper', 62, anchor='ma')
    sheet(d, (700, 220, 1340, 1020))
    d.line(j_poly(900, 960, 10) + [j_poly(900, 960, 10)[0]], fill=GREY, width=6)
    block(d, 620, 1010, 10, -160)
    d.line((620, 1060, 780, 1060 - 88), fill=RED, width=8)
    text(d, (500, 1075), '20 mm toward you', 54, RED)
    chip(d, (1600, 160), 'a flat drawing → a block', 50, anchor='r')
    save(im, 'card-extrude.png')


def card_joutline():
    im, d = canvas()
    text(d, (W / 2, 60), 'The wall hook, from the side', 64, anchor='ma')
    d.rectangle((300, 160, 380, 1140), fill=(180, 170, 150))                        # the wall
    text(d, (340, 1150), 'wall', 44, GREY, anchor='ma')
    s = 14
    ox, oy = 380, 1080
    d.polygon(j_poly(ox, oy, s), fill=(176, 190, 212), outline=INK, width=6)
    # sizes
    text(d, (ox - 40, oy - 30 * s), '60', 72, BLUE, anchor='rm')
    d.line((ox + 25 * s + 30, oy, ox + 25 * s + 30, oy - 10 * s), fill=BLUE, width=6)
    text(d, (ox + 25 * s + 50, oy - 5 * s), '10 high', 60, BLUE, anchor='lm')
    d.line((ox, oy + 30, ox + 25 * s, oy + 30), fill=BLUE, width=6)
    text(d, (ox + 12 * s, oy + 40), '25 deep', 60, BLUE, anchor='ma')
    text(d, (ox + 5 * s + 30, oy - 40 * s), '5 thick', 56, BLUE, anchor='lm')
    # a key hanging on the arm
    kx, ky = ox + 13 * s, oy - 5 * s
    d.line((kx, ky, kx, ky + 30), fill=AMBER, width=8)
    d.ellipse((kx - 26, ky + 30, kx + 26, ky + 82), outline=AMBER, width=10)
    chip(d, (1580, 1060), 'a flipped J · all 5 thick', 50, anchor='r')
    save(im, 'card-joutline.png')


def card_recipe():
    im, d = canvas()
    text(d, (W / 2, 60), 'The History is the recipe', 66, anchor='ma')
    d.rounded_rectangle((180, 200, 1450, 760), radius=30, fill=PAPER, outline=GREY, width=4)
    text(d, (240, 240), 'Recipe: wall hook', 64, AMBER)
    text(d, (260, 400), '1.  sketch the J', 72)
    text(d, (260, 560), '2.  extrude it 20', 72)
    bar = still('hand-hook.png', (0, 1712, 560, 1792)).resize((1260, 180), Image.LANCZOS)
    paste_c(im, bar, W / 2, 930)
    text(d, (W / 2, 1100), 'the real History bar: Sketch1, Extrude1', 48, GREY, R, anchor='ma')
    save(im, 'card-recipe.png')


def card_sum():
    im, d = canvas()
    text(d, (W / 2, 50), 'Work it out first', 66, anchor='ma')
    s, ox, oy = 13, 170, 1100
    rects = [((0, 0, 5, 60), (176, 190, 212), '5 x 60 = 300'), ((5, 0, 25, 5), (190, 215, 190), '20 x 5 = 100'),
             ((20, 5, 25, 10), (235, 205, 160), '5 x 5 = 25')]
    for (x0, z0, x1, z1), c, _ in rects:
        d.rectangle((ox + x0 * s, oy - z1 * s, ox + x1 * s, oy - z0 * s), fill=c, outline=INK, width=5)
    tx = 640
    text(d, (tx, 230), '5 x 60 = 300', 70, INK)
    text(d, (tx, 330), '20 x 5 = 100', 70, GREEN)
    text(d, (tx, 405), '(25 minus the plate\'s 5)', 54, GREY, R)
    text(d, (tx, 480), '5 x 5 = 25', 70, AMBER)
    text(d, (tx, 555), '(10 minus the arm\'s 5)', 54, GREY, R)
    d.line((tx, 640, 1560, 640), fill=INK, width=5)
    text(d, (tx, 680), 'add them up ...', 64, GREY, R)
    save(im, 'card-sum.png')


def card_paperup():
    im, d = canvas()
    text(d, (W / 2, 40), 'Same J, paper turned over', 62, anchor='ma')
    for i, (label, flip, col) in enumerate((('ours: top up', False, GREEN), ("Claude's: top down", True, RED))):
        x0 = 120 + i * 560
        sheet(d, (x0, 160, x0 + 440, 760))
        if flip:
            d.line(j_poly(x0 + 150, 230, 8, flip=True) + [j_poly(x0 + 150, 230, 8, flip=True)[0]], fill=INK, width=8)
            d.line((x0 + 400, 700, x0 + 400, 560), fill=col, width=10)
            d.polygon([(x0 + 380, 700), (x0 + 420, 700), (x0 + 400, 740)], fill=col)
            text(d, (x0 + 400, 520), 'TOP', 40, col, anchor='ma')
        else:
            d.line(j_poly(x0 + 150, 700, 8) + [j_poly(x0 + 150, 700, 8)[0]], fill=INK, width=8)
            d.line((x0 + 400, 360, x0 + 400, 220), fill=col, width=10)
            d.polygon([(x0 + 380, 220), (x0 + 420, 220), (x0 + 400, 180)], fill=col)
            text(d, (x0 + 400, 370), 'TOP', 40, col, anchor='ma')
        text(d, (x0 + 220, 790), label, 52, col, anchor='ma')
    # mugs
    mx = 1300
    for k, up in enumerate((True, False)):
        y = 300 + k * 330
        body = (mx, y, mx + 170, y + 200)
        d.rectangle(body, fill=(200, 210, 225), outline=INK, width=5)
        d.arc((mx + 140, y + 40, mx + 240, y + 160), -90, 90, fill=INK, width=12)
        # the open rim: on top when standing, at the bottom when turned upside down
        ry = y if up else y + 200
        d.line((mx - 6, ry, mx + 176, ry), fill=(236, 239, 244), width=12)
        d.ellipse((mx, ry - 14, mx + 170, ry + 14), outline=INK, width=5)
        text(d, (mx + 85, y + 100), 'up' if up else 'over', 30, GREY, anchor='mm')
    text(d, (mx + 60, 870), 'same size,', 40, INK, anchor='ma')
    text(d, (mx + 60, 920), 'same weight', 40, INK, anchor='ma')
    chip(d, (W / 2, 1000), 'volume can\'t tell which way is up', 54, anchor='m', bg=RED)
    save(im, 'card-paperup.png')


def card_compare():
    im, d = canvas()
    text(d, (W / 2, 30), 'By hand vs Claude', 64, anchor='ma')
    hand = fit(still('hand-hook.png', (1150, 260, 2000, 1680)), 420, 420)
    cl = fit(still('claude-after.png', (1880, 700, 2620, 1720)), 420, 420)
    paste_c(im, hand, 640, 360)
    paste_c(im, cl, 1180, 360)
    for cx, up, col, lab in ((640, True, GREEN, "up +Z"), (1180, False, RED, "up -Z")):
        x = cx + 240
        y0, y1 = (520, 220) if up else (220, 520)
        d.line((x, y0, x, y1), fill=col, width=14)
        tip = [(x - 26, y1 + (24 if up else -24)), (x + 26, y1 + (24 if up else -24)), (x, y1 - (20 if up else -20))]
        d.polygon(tip, fill=col)
        text(d, (x, 540 if up else 170), lab, 44, col, anchor='ma')
    chip(d, (615, 580), 'picked in the Browser', 30, anchor='m', bg=GREEN, pad=10)
    chip(d, (1180, 580), 'made through the plug', 30, anchor='m', bg=RED, pad=10)
    hs, cs = CMP['hand_summary'], CMP['claude_summary']
    rows = [('volume', f"{hs['volume_mm3']:,.0f}", f"{cs['volume_mm3']:,.0f}", True),
            ('size', 'x'.join(f'{v:g}' for v in hs['bbox_mm']), 'x'.join(f'{v:g}' for v in cs['bbox_mm']), True),
            ('corners', '8, same', '8, same', CMP['same_shape']),
            ('steps', 'Sketch, Extrude', 'Sketch, Extrude', CMP['same_steps']),
            ('plane', 'XZ', 'XZ', CMP['same_plane']),
            ("plane's up", '+Z', '-Z', CMP['same_up'])]
    y = 650
    for name, a, b, ok in rows:
        big = name == "plane's up"
        text(d, (60, y), name, 58 if big else 50, RED if big else GREY, B if big else R)
        text(d, (640, y), a, 58 if big else 50, INK, anchor='ma')
        text(d, (1180, y), b, 58 if big else 50, INK if ok else RED, anchor='ma')
        text(d, (1530, y), '✓' if ok else '✗', 56, GREEN if ok else RED, anchor='ma')
        y += 74
    # (cut 5: the replay line left the card; the replay's own window says it when the voice does)
    save(im, 'card-compare.png')


def card_recap():
    im, d = canvas()
    text(d, (W / 2, 40), 'Remember three pictures', 64, anchor='ma')
    sheet(d, (90, 200, 470, 640))
    d.line(j_poly(220, 600, 6) + [j_poly(220, 600, 6)[0]], fill=INK, width=7)
    text(d, (280, 680), 'sketch = paper', 46, anchor='ma')
    block(d, 720, 600, 6, -110)
    text(d, (820, 680), 'extrude = push out', 46, anchor='ma')
    d.rounded_rectangle((1110, 230, 1560, 600), radius=24, fill=PAPER, outline=GREY, width=4)
    text(d, (1150, 290), '1. sketch', 56)
    text(d, (1150, 400), '2. extrude', 56)
    text(d, (1335, 680), 'History = recipe', 46, anchor='ma')
    chip(d, (W / 2, 840), 'volume + size check the shape', 50, anchor='m', bg=GREEN)
    chip(d, (W / 2, 960), 'the picture checks which way is up', 50, anchor='m', bg=RED)
    save(im, 'card-recap.png')


def hook(w, h, vertical=False):
    im = Image.new('RGB', (w, h), BG)
    d = ImageDraw.Draw(im)
    hand = still('hand-hook.png', (1150, 260, 2000, 1680))
    cl = still('claude-after.png', (1700, 480, 2800, 1760))
    if not vertical:
        a = fit(hand, w // 2 - 60, h - 260)
        b = fit(cl, w // 2 - 60, h - 260)
        paste_c(im, a, w // 4, h / 2 + 40)
        paste_c(im, b, 3 * w // 4, h / 2 + 40)
        chip(d, (w // 4, 40), 'BY HAND', 72, anchor='m', bg=GREEN)
        chip(d, (3 * w // 4, 40), 'CLAUDE · 1 message', 72, anchor='m', bg=BLUE)
        chip(d, (w // 2, h - 150), 'SAME PART?', 84, anchor='m', bg=RED)
    else:   # the Short's frame 0: the question in large words (it hides the captions for its first seconds)
        text(d, (w // 2, 130), 'Same hook, two ways:', 76, anchor='ma')
        text(d, (w // 2, 230), 'same part?', 96, RED, anchor='ma')
        a = fit(hand, w // 2 - 50, 1050)
        b = fit(still('claude-after.png', (1850, 620, 2600, 1700)), w // 2 - 50, 1050)
        paste_c(im, a, w // 4 + 5, 950)
        paste_c(im, b, 3 * w // 4 - 5, 950)
        chip(d, (w // 4 + 5, 950 + a.height // 2 + 30), 'BY HAND', 58, anchor='m', bg=GREEN)
        chip(d, (3 * w // 4 - 5, 950 + b.height // 2 + 30), 'CLAUDE', 58, anchor='m', bg=BLUE)
    return im


def short_assets():
    hand = still('hand-j.png', (1150, 450, 2050, 1650))
    cl = still('claude-after.png', (1700, 480, 2800, 1760))
    term = still('claude-typed.png', (0, 0, 1150, 1100))
    for name, pic in (('sc2s-hand.png', hand), ('sc2s-claude.png', term), ('sc2s-hang.png', cl)):
        im = Image.new('RGB', (1000, 1000), BG)
        paste_c(im, fit(pic, 960, 960), 500, 500)
        save(im, name)
    im = Image.new('RGB', (1000, 1000), BG)
    a = fit(still('hand-hook.png', (1150, 260, 2000, 1680)), 470, 760)
    b = fit(still('claude-after.png', (1850, 620, 2600, 1700)), 470, 760)
    paste_c(im, a, 255, 470)
    paste_c(im, b, 745, 470)
    d = ImageDraw.Draw(im)
    # the floor (Z = 0): the hand hook's base, Claude's origin (measured on the drawn thumbnails)
    fa = 470 - a.height // 2 + int((1627 - 260) * a.height / 1420)
    fb = 470 - b.height // 2 + int((925 - 620) * b.height / 1080)
    for y, x0, x1 in ((fa, 25, 485), (fb, 515, 975)):
        for x in range(x0, x1, 28):
            d.line((x, y, x + 16, y), fill=AMBER, width=7)
    chip(d, (255, fa + 12), 'floor', 34, anchor='m', bg=AMBER)
    chip(d, (745, fb + 12), 'floor', 34, anchor='m', bg=AMBER)
    chip(d, (255, 905), 'stands up', 52, anchor='m', bg=GREEN)
    chip(d, (745, 905), 'hangs down', 52, anchor='m', bg=RED)
    save(im, 'sc2s-both.png')
    im, d = canvas(1000, 1000)
    text(d, (500, 40), 'Same outline: one up, one down', 50, anchor='ma')
    for i, (label, flip, col) in enumerate((('by hand: picked on screen', False, GREEN), ('Claude: typed "XZ"', True, RED))):
        x0 = 60 + i * 480
        sheet(d, (x0, 160, x0 + 400, 720))
        if flip:
            d.line(j_poly(x0 + 140, 220, 7, flip=True) + [j_poly(x0 + 140, 220, 7, flip=True)[0]], fill=INK, width=8)
            d.line((x0 + 360, 660, x0 + 360, 520), fill=col, width=10)
            d.polygon([(x0 + 340, 660), (x0 + 380, 660), (x0 + 360, 700)], fill=col)
            text(d, (x0 + 320, 470), 'up = -Z', 44, col, anchor='ma')
        else:
            d.line(j_poly(x0 + 140, 660, 7) + [j_poly(x0 + 140, 660, 7)[0]], fill=INK, width=8)
            d.line((x0 + 360, 340, x0 + 360, 200), fill=col, width=10)
            d.polygon([(x0 + 340, 200), (x0 + 380, 200), (x0 + 360, 160)], fill=col)
            text(d, (x0 + 320, 350), 'up = +Z', 44, col, anchor='ma')
        who, how = label.split(': ')
        text(d, (x0 + 200, 740), who + ':', 40, col, anchor='ma')
        text(d, (x0 + 200, 790), how, 40, col, anchor='ma')
    chip(d, (500, 860), 'same XZ, set up two ways', 50, anchor='m', bg=RED)
    save(im, 'sc2s-why.png')


def thumbs():
    """1280 x 720, 4 words or fewer, the payoff number with its unit; real recordings only."""
    for name, words, colour in (('thumbnail-primary.jpg', '8,500 mm³ BOTH', RED), ('thumbnail-altA.jpg', 'UPSIDE DOWN?', RED)):
        im = Image.new('RGB', (1280, 720), (24, 30, 40))
        d = ImageDraw.Draw(im)
        a = fit(still('hand-hook.png', (1150, 260, 2000, 1680)), 400, 560)
        b = fit(still('claude-after.png', (1700, 480, 2800, 1760)), 480, 560)
        im.paste(a, (40, 140)); im.paste(b, (760, 140))
        chip(d, (240, 40), 'BY HAND', 56, anchor='m', bg=GREEN)
        chip(d, (1000, 40), 'CLAUDE', 56, anchor='m', bg=BLUE)
        f = font(B, 110)
        w = f.getlength(words)
        d.rounded_rectangle((640 - w / 2 - 30, 470, 640 + w / 2 + 30, 620), radius=24, fill=colour)
        d.text((640, 545), words, font=f, fill=PAPER, anchor='mm')
        im.save(os.path.join(F, name), quality=92)
        print(name)


if __name__ == '__main__':
    card_sketch(); card_extrude(); card_joutline(); card_recipe(); card_sum(); card_paperup(); card_compare()
    card_recap()
    save(hook(2560, 1440), 'hook-landscape.png')
    save(hook(1080, 1920, vertical=True), 'hook-vertical.png')
    short_assets()
    thumbs()
