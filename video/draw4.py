"""Lesson 4's diagram cards, hook pictures and thumbnails. Every SolidCraft picture is a crop of a real lab recording
(out/l4/stills, video/stills4.py); every number comes from a lab file (out/l4/hand/read-*.json, clearance.json,
compare.json, replay-*.json). Diagrams are visibly diagrams. Cards 1632 x 1200, text 48 px or more; hooks 2560 x 1440
and 1080 x 1920; thumbnails 1280 x 720.
    docker run --rm --network none -v "$PWD:/work" -w /work cadcmp-openscad:2021.01 python3 video/draw4.py [cards|hooks|all]
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw2 as d2  # noqa: E402  (helpers and colours only)
from draw2 import BG, INK, RED, GREEN, GREY, BLUE, PAPER, AMBER, W, H, B, R, M, font, canvas, text, chip, fit, paste_c  # noqa: E402

LAB = d2.LAB
L4 = os.path.join(LAB, 'out', 'l4')
ST = os.path.join(L4, 'stills')
F = os.path.join(LAB, 'video', 'frames-l4')
os.makedirs(F, exist_ok=True)


def rd(name):
    return json.load(open(os.path.join(L4, name)))


def save(im, name):
    im.save(os.path.join(F, name))
    print(name, im.size)


def n1(v):
    return f'{v:,.1f}'


def dashed(d, a, b, fill, width=6, dash=26, gap=16):
    (x0, y0), (x1, y1) = a, b
    L = math.hypot(x1 - x0, y1 - y0)
    k = 0.0
    while k < L:
        e = min(k + dash, L)
        d.line((x0 + (x1 - x0) * k / L, y0 + (y1 - y0) * k / L, x0 + (x1 - x0) * e / L, y0 + (y1 - y0) * e / L), fill=fill, width=width)
        k = e + gap


def dim(d, x0, x1, y, label, col, size=56):
    """A horizontal dimension with end ticks and its label above."""
    d.line((x0, y, x1, y), fill=col, width=7)
    for x in (x0, x1):
        d.line((x, y - 22, x, y + 22), fill=col, width=7)
    text(d, ((x0 + x1) / 2, y - 70), label, size, col, anchor='ma')


def plate_front(d, cx, top, width_mm, holes_y, s=14, col=None, label_sides=True, mid=True):
    """The back plate seen straight on (60 tall, width_mm wide); holes_y = distance of the holes from the left edge."""
    w, h = width_mm * s, 60 * s
    x0, y0 = cx - w / 2, top
    d.rectangle((x0, y0, x0 + w, y0 + h), fill=(214, 222, 236), outline=INK, width=6)
    for z in (15, 45):
        hx, hy = x0 + holes_y * s, y0 + z * s
        r = 2.25 * s
        d.ellipse((hx - r, hy - r, hx + r, hy + r), fill=BG, outline=INK, width=5)
    if mid:
        dashed(d, (cx, y0 - 30), (cx, y0 + h + 30), GREY, width=5)
    if label_sides:
        c = col or INK
        yy = y0 + 15 * s
        dim(d, x0, x0 + holes_y * s, yy - 70, f'{holes_y:g}', c)
        dim(d, x0 + holes_y * s, x0 + w, yy - 70, f'{width_mm - holes_y:g}', c)
    return x0, y0, w, h


def card_formula():
    for k in range(3):
        im, d = canvas()
        text(d, (W / 2, 50), 'The hole, 10 from the left edge', 60, anchor='ma')
        if k == 0:
            plate_front(d, W / 2, 290, 20, 10, col=GREEN)
            chip(d, (W / 2, 1110), 'width 20: the middle is 10', 52, anchor='m', bg=GREEN)
        elif k == 1:
            plate_front(d, W / 2, 290, 30, 10, col=RED)
            chip(d, (W / 2, 1110), 'width 30: still 10 · off the middle', 52, anchor='m', bg=RED)
        else:
            text(d, (W / 2, 50), '', 10)
            plate_front(d, W / 2, 290, 30, 15, col=GREEN)
            chip(d, (W / 2, 1040), 'width / 2 = 15', 64, anchor='m', bg=GREEN)
            text(d, (W / 2, 1120), '/ = divide: half the width', 50, GREY, anchor='ma')
        save(im, f'card-formula-{k + 1}.png')


def card_clearance():
    cl = rd('clearance.json')['fits']
    sizes = {k: v['diameters'][0] for k, v in cl.items()}
    for k in range(3):
        im, d = canvas()
        text(d, (W / 2, 50), 'A screw in its hole, from the side', 60, anchor='ma')
        s = 90
        cx, top = 560, 230
        # plate (5 thick) with a hole of 4.5, screw 4
        pw = 5 * s
        if k >= 1:
            hole = 4.5 * s
            d.rectangle((cx - pw / 2, top, cx + pw / 2, top + 900), fill=(214, 222, 236), outline=INK, width=5)
            d.rectangle((cx - pw / 2 - 3, top + 450 - hole / 2, cx + pw / 2 + 3, top + 450 + hole / 2), fill=BG)
            d.line((cx - pw / 2, top + 450 - hole / 2, cx + pw / 2, top + 450 - hole / 2), fill=INK, width=5)
            d.line((cx - pw / 2, top + 450 + hole / 2, cx + pw / 2, top + 450 + hole / 2), fill=INK, width=5)
        else:
            d.rectangle((cx - pw / 2, top, cx + pw / 2, top + 900), fill=(214, 222, 236), outline=INK, width=5)
        sc = 4 * s
        d.rectangle((cx - 420, top + 450 - sc / 2, cx + 380, top + 450 + sc / 2), fill=(150, 156, 168), outline=INK, width=5)
        d.rectangle((cx - 470, top + 450 - 4 * s, cx - 420, top + 450 + 4 * s), fill=(150, 156, 168), outline=INK, width=5)
        chip(d, (1090, 300), 'M4 screw: 4 mm', 54, anchor='l', bg=INK)
        if k >= 1:
            chip(d, (1090, 420), 'hole: 4.5 mm', 54, anchor='l', bg=BLUE)
            for yy in (top + 450 - 4.5 * s / 2 + 6, top + 450 + sc / 2 + 6):
                d.rectangle((cx - pw / 2 + 6, yy, cx + pw / 2 - 6, yy + 0.25 * s - 12), fill=AMBER)
            chip(d, (1090, 540), 'the gap: clearance', 54, anchor='l', bg=AMBER)
        if k == 2:
            text(d, (1000, 700), "SolidCraft's M4 setting", 52, INK)
            for i, (fit_, lab) in enumerate((('close', 'close'), ('normal', 'normal'), ('loose', 'loose'))):
                col = GREEN if fit_ == 'normal' else GREY
                chip(d, (1000, 790 + i * 110), f'{lab}  {sizes[fit_]:g} mm', 56, anchor='l', bg=col)
        save(im, f'card-clearance-{k + 1}.png')


def card_table():
    for k in range(3):
        im, d = canvas()
        text(d, (W / 2, 50), 'A fillet: a sharp edge made round', 60, anchor='ma')
        # a table top seen from the side: a slab with a corner
        x0, y0, x1, y1 = 260, 330, 1260, 520
        if k == 0:
            d.rectangle((x0, y0, x1, y1), fill=(196, 160, 112), outline=INK, width=6)
            chip(d, (x1 - 40, y0 - 90), 'sharp corner', 50, anchor='m', bg=RED)
        else:
            r = 70
            d.rounded_rectangle((x0, y0, x1, y1), radius=r, fill=(196, 160, 112), outline=INK, width=6)
            d.rectangle((x0, y0, x0 + r + 10, y1), fill=(196, 160, 112))
            d.line((x0, y0, x0, y1), fill=INK, width=6)
            d.line((x0, y0, x0 + r + 10, y0), fill=INK, width=6)
            d.line((x0, y1, x0 + r + 10, y1), fill=INK, width=6)
            chip(d, (x1 - 40, y0 - 90), 'sanded round', 50, anchor='m', bg=GREEN)
        d.rectangle((x0 + 60, y1, x0 + 120, 1000), fill=(176, 140, 92), outline=INK, width=5)
        d.rectangle((x1 - 120, y1, x1 - 60, 1000), fill=(176, 140, 92), outline=INK, width=5)
        if k == 2:
            p = os.path.join(ST, 'hand-round.png')
            if os.path.exists(p):
                pic = fit(Image.open(p).convert('RGB').crop(HOOK3D), 520, 520)
                paste_c(im, pic, 1270, 840)
            chip(d, (1270, 1130), 'the hook: two top edges', 48, anchor='m', bg=BLUE)
        save(im, f'card-table-{k + 1}.png')


def card_expected():
    h = rd('hand/read-fillet.json')['summary']
    hole = math.pi * 2.25 ** 2 * 5
    fil = 2 ** 2 * (1 - math.pi / 4) * 20
    lines = [('The hook: 8,500 mm³', INK),
             (f'a hole = a cylinder 4.5 wide, 5 deep: {hole:.1f} · two: {2 * round(hole, 1):.1f}', BLUE),
             (f'a rounded edge = a corner sliver, 20 long: {fil:.1f} · two: {2 * round(fil, 1):.1f}', AMBER),
             (f'8,500 − {2 * round(hole, 1):.1f} − {2 * round(fil, 1):.1f} = {8500 - 2 * round(hole, 1) - 2 * round(fil, 1):,.1f} mm³', GREEN)]
    assert abs((8500 - 2 * round(hole, 1) - 2 * round(fil, 1)) - round(h['volume_mm3'], 1)) < 0.06, h['volume_mm3']
    for k in range(4):
        im, d = canvas()
        text(d, (W / 2, 50), 'Worked out before we look', 60, anchor='ma')
        for i, (s, col) in enumerate(lines[:k + 1]):
            size = 48 if i in (1, 2) else 60
            text(d, (110, 220 + i * 210), s, size, col)
        save(im, f'card-expected-{k + 1}.png')


def card_recap():
    rows = [('A through hole goes right through', INK), ('Placed with a tape measure from two edges', BLUE),
            ('A fillet: a sanded corner', AMBER), ('Stay in the middle: width / 2', GREEN)]
    for k in range(4):
        im, d = canvas()
        text(d, (W / 2, 50), 'Remember', 64, anchor='ma')
        for i, (s, col) in enumerate(rows[:k + 1]):
            chip(d, (W / 2, 250 + i * 220), s, 58, anchor='m', bg=col)
        save(im, f'card-recap-{k + 1}.png')


def short_why():
    for k, (holes, col, lab) in enumerate(((10, RED, 'typed 10 at width 30'), (15, GREEN, 'width / 2 at width 30'))):
        im, d = canvas(1000, 1000)
        text(d, (500, 30), lab, 54, col, anchor='ma')
        plate_front(d, 500, 200, 30, holes, s=12, col=col)
        save(im, f'sc4s-why-{k + 1}.png')


HOOK3D = (900, 250, 2300, 1650)      # the hook after the house, 2880x1800 stills (checked on the stills)

if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('cards', 'all'):
        card_formula(); card_clearance(); card_table(); card_expected(); card_recap(); short_why()
