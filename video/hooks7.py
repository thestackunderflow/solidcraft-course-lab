"""Lesson 7's frame-0 hook pictures and thumbnails, from real stills of the setup take (out/l7/stills: the terminal at
"Failed to connect" and at "Connected", frames of out/scratch/l7-masters/setup.mp4 at 94.0 s and 121.5 s).
    docker run --rm --network none -v "$PWD:/work" -w /work cadcmp-openscad:2021.01 python3 video/hooks7.py"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from draw2 import INK, RED, GREEN, PAPER, B, font  # noqa: E402

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ST = os.path.join(LAB, 'out', 'l7', 'stills')
F = os.path.join(LAB, 'video', 'frames-l7')


def last_lines(name, h=170):
    im = Image.open(os.path.join(ST, name)).convert('RGB')
    a = np.array(im.convert('L'))[:, 10:1400]
    b = int(np.where((a < 110).sum(axis=1) > 2)[0].max())
    return im.crop((0, b - h + 10, 1440, b + 10))


def band(dst, pic, y, w, mark, word, col):
    pic = pic.resize((w, int(pic.height * w / pic.width)), Image.LANCZOS)
    x = (dst.width - w) // 2
    dst.paste(pic, (x, y))
    d = ImageDraw.Draw(dst)
    d.rectangle((x - 4, y - 4, x + w + 4, y + pic.height + 4), outline=col, width=10)
    return y + pic.height


def hook(size, name):
    W, H = size
    im = Image.new('RGB', size, (236, 239, 244))
    d = ImageDraw.Draw(im)
    fail, ok = last_lines('failed.png', 120), last_lines('connected.png', 120)
    w = int(W * 0.94)
    fs = int(H * (0.09 if W > H else 0.05))
    ph = int(120 * w / 1440)
    y = max(int(H * 0.05), (H - (2 * (fs + 20 + ph) + int(H * 0.05))) // 2)
    d.text((W // 2, y), '✘ FAILED TO CONNECT', font=font(B, fs), fill=RED, anchor='ma')
    y = band(im, fail, y + fs + 20, w, '✘', '', RED) + int(H * 0.05)
    d.text((W // 2, y), '✔ CONNECTED', font=font(B, fs), fill=GREEN, anchor='ma')
    band(im, ok, y + fs + 20, w, '✔', '', GREEN)
    im.save(os.path.join(F, name))
    print(name, im.size)


def thumb(words, name):
    W, H = 1280, 720
    im = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(im)
    fail = last_lines('failed.png', 120).resize((W, int(120 * W / 1440)))
    ok = last_lines('connected.png', 120).resize((W, int(120 * W / 1440)))
    im.paste(fail, (0, 40))
    im.paste(ok, (0, 40 + fail.height + 20))
    d.rectangle((0, 0, W, H), outline=INK, width=6)
    d.text((70, 330), '✘', font=font(B, 230), fill=RED)
    d.text((300, 330), '→', font=font(B, 200), fill=INK)
    d.text((520, 330), '✔', font=font(B, 230), fill=GREEN)
    d.rounded_rectangle((40, 590, W - 40, 700), radius=22, fill=INK)
    d.text((W // 2, 645), words, font=font(B, 84), fill=PAPER, anchor='mm')
    im.convert('RGB').save(os.path.join(F, name), quality=92)
    print(name, im.size)


if __name__ == '__main__':
    hook((2560, 1440), 'hook-landscape.png')
    thumb('READ THE ERROR', 'thumbnail-primary.jpg')
    thumb('ONE MENU FIXES IT', 'thumbnail-altA.jpg')


def short_why():
    """The Short's why picture (948 x 948): the two real terminal lines cut into readable pieces, the short name (red)
    above the full path (green). Crops of out/l7/stills (no redrawn text); character cells are 17.6 px wide."""
    cw = 1390 / 79
    fail = Image.open(os.path.join(ST, 'failed.png')).convert('RGB')
    ok = Image.open(os.path.join(ST, 'connected.png')).convert('RGB')
    pieces = [('SHORT NAME', RED, None),
              ('', None, fail.crop((int(12 * cw) - 4, 782, int(53 * cw), 818))),
              ('', None, fail.crop((0, 819, int(33 * cw), 849))),
              ('FULL PATH', GREEN, None),
              ('', None, ok.crop((int(12 * cw) - 4, 1300, int(54 * cw), 1336))),
              ('', None, ok.crop((int(54 * cw), 1300, int(73.5 * cw), 1336)))]
    im = Image.new('RGB', (948, 948), PAPER)
    d = ImageDraw.Draw(im)
    y = 150
    boxes = []
    for title, col, pic in pieces:
        if title:
            d.text((474, y), title, font=font(B, 64), fill=col, anchor='ma')
            y += 100
            continue
        s = min(900 / pic.width, 2.2)
        p = pic.resize((int(pic.width * s), int(pic.height * s)), Image.LANCZOS)
        im.paste(p, (24, y))
        boxes.append((24, y, 24 + p.width, y + p.height))
        y += p.height + 55
    x0, y0, x1, y1 = boxes[0]
    d.rectangle((x0 - 6, y0 - 6, x0 + int((x1 - x0) * 15 / 41) + 6, y1 + 6), outline=RED, width=6)       # solidcraft-cli
    x0, y0, x1, y1 = boxes[2]
    d.rectangle((x0 - 6, y0 - 6, x1 + 6, y1 + 6), outline=GREEN, width=6)                                  # the full path
    im.save(os.path.join(LAB, '..', 'Refream-Canvas', 'mcp-canvas', 'primers', 'shorts-assets', 'sc7s-why.png'))
    blank = Image.new('RGB', (948, 948), (236, 239, 244))
    blank.save(os.path.join(LAB, '..', 'Refream-Canvas', 'mcp-canvas', 'primers', 'shorts-assets', 'sc7s-fix.png'))
    print('sc7s-why.png, sc7s-fix.png')


if __name__ == '__main__':
    short_why()
