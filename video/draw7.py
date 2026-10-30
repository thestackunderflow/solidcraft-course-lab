"""Lesson 7's diagram cards. Every error line on a card is copied from a lab file (out/l7/*/story.json, *-pane.txt);
diagrams are visibly diagrams. Cards 1632 x 1200, text >= 48 px.
    docker run --rm --network none -v "$PWD:/work" -w /work cadcmp-openscad:2021.01 python3 video/draw7.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw2 as d2  # noqa: E402  (helpers and colours only)
from draw2 import BG, INK, RED, GREEN, GREY, BLUE, PAPER, AMBER, W, H, B, R, M, canvas, text, chip  # noqa: E402

LAB = d2.LAB
L7 = os.path.join(LAB, 'out', 'l7')
F = os.path.join(LAB, 'video', 'frames-l7')
os.makedirs(F, exist_ok=True)
STORY = {t: {r['key']: r for r in json.load(open(os.path.join(L7, t, 'story.json')))} for t in ('headless', 'errors')}
PANE = open(os.path.join(L7, 'setup', 'c2-list-pane.txt'), encoding='utf-8').read()
assert 'ENOENT: Executable not' in PANE and 'found in $PATH: "solidcraft-cli"' in PANE
assert 'rolled_back' in STORY['errors']['e-typo']['texts'][0]
assert 'headless session' in STORY['headless']['h-build']['texts'][1]
LIGHT = (255, 214, 102)


def save(im, name):
    im.save(os.path.join(F, name))
    print(name, im.size)


def lamp(d, x, y, lit):
    """A desk lamp (base at y + 520): base, arm, shade, bulb; the bulb yellow with rays when lit."""
    d.rounded_rectangle((x - 150, y + 500, x + 150, y + 545), radius=12, fill=INK)
    d.line((x, y + 500, x - 80, y + 250, x + 60, y + 40), fill=INK, width=24, joint='curve')
    d.polygon([(x + 20, y - 40), (x + 300, y - 40), (x + 240, y + 120), (x + 90, y + 120)], fill=GREY)
    d.ellipse((x + 120, y + 100, x + 210, y + 190), fill=LIGHT if lit else PAPER, outline=INK, width=7)
    if lit:
        for dx, dy in ((-90, 60), (0, 110), (90, 60)):
            d.line((x + 165 + dx * 0.6, y + 145 + dy * 0.6, x + 165 + dx * 1.2, y + 145 + dy * 1.2), fill=AMBER, width=10)


def socket_plug(d, x, y, s=1.0, col=INK):
    """A wall socket (x, y = top left, 160 x 260 at s=1) with the lamp's plug pushed in from the right."""
    q = lambda a, b: (x + a * s, y + b * s)
    d.rectangle((*q(0, 0), *q(160, 260)), fill=PAPER, outline=col, width=max(3, int(8 * s)))
    d.rounded_rectangle((*q(150, 115), *q(240, 205)), radius=int(14 * s), fill=col)          # the plug head
    d.line((*q(240, 160), *q(270, 160)), fill=col, width=max(3, int(14 * s)))


def card_lamp():
    """F2: a lamp that won't light, checked from the wall outward: socket, cord, switch, bulb (4 reveal steps)."""
    stops = [('1 plugged in?', (240, 640)), ('2 cord OK?', (440, 1010)), ('3 switched on?', (760, 640)), ('4 the bulb', (1330, 290))]
    for k in range(5):
        im, d = canvas()
        text(d, (W / 2, 50), "A lamp that won't light", 66, anchor='ma')
        text(d, (W / 2, 140), 'check from the wall outward', 52, GREY, path=R, anchor='ma')
        socket_plug(d, 90, 740)
        d.line((330, 900, 450, 950, 680, 900), fill=INK, width=14, joint='curve')  # cord
        d.rounded_rectangle((680, 850, 840, 950), radius=18, fill=PAPER, outline=INK, width=8)  # switch
        d.rectangle((735, 875, 785, 925), fill=INK)
        d.line((840, 900, 1000, 960, 1150, 950), fill=INK, width=14, joint='curve')
        lamp(d, 1180, 420, lit=(k == 4))
        for i, (lab, (x, y)) in enumerate(stops[:k]):
            chip(d, (x, y), lab, 48, anchor='m', bg=BLUE)
        if k == 4:
            chip(d, (W / 2, 1090), 'one check at a time, in order', 50, anchor='m', bg=GREEN)
        save(im, f'card-lamp-{k}.png' if k < 4 else 'card-lamp.png')


def box(d, xy, label, sub=None, col=INK, fill=PAPER):
    x, y = xy
    d.rounded_rectangle((x - 200, y - 85, x + 200, y + 85), radius=26, fill=fill, outline=col, width=8)
    text(d, (x, y - (22 if sub else 0)), label, 52, col, anchor='mm')
    if sub:
        text(d, (x, y + 38), sub, 38, GREY, path=R, anchor='mm')


def card_map(ticks=0, lit=None, name='card-map'):
    """F3 / so-far cards: lesson 1's map (Claude app, plug, SolidCraft) with the four checks."""
    im, d = canvas()
    text(d, (W / 2, 60), 'The same checks, on lesson 1\'s map', 62, anchor='ma')
    box(d, (300, 470), 'Claude app', 'Desktop or Code')
    box(d, (816, 470), 'plug', 'solidcraft-cli mcp')
    box(d, (1332, 470), 'SolidCraft', 'the window')
    d.line((500, 470, 616, 470), fill=INK, width=10); d.line((1016, 470, 1132, 470), fill=INK, width=10)
    checks = [((300, 700), '1  plug listed?'), ((610, 330), '2  connects?'), ((1332, 700), '3  window open?'),
              ((816, 880), '4  what the reply says')]
    for i, ((x, y), lab) in enumerate(checks):
        if i >= (lit if lit is not None else 4):
            break
        ok = i < ticks
        chip(d, (x, y), ('✓ ' if ok else '') + lab, 46, anchor='m', bg=GREEN if ok else BLUE)
    if lit and lit >= 4:
        d.line((640, 830, 990, 830), fill=BLUE, width=6)
    save(im, name + '.png')


def card_path():
    """F9: a short name searched folder by folder on the PATH list; a full path goes straight to the program."""
    folders = ['/usr/local/bin', '/usr/bin', '/bin']
    for k in range(5):
        im, d = canvas()
        text(d, (W / 2, 60), 'How a short name is found', 64, anchor='ma')
        chip(d, (110, 190), 'solidcraft-cli', 54, bg=INK)
        text(d, (620, 205), '= a short name, no folder', 48, GREY, path=R)
        text(d, (110, 340), 'the PATH list (this computer):', 50, path=R)
        for i, f in enumerate(folders):
            y = 430 + i * 130
            d.rounded_rectangle((150, y, 900, y + 100), radius=16, fill=PAPER, outline=GREY, width=4)
            text(d, (180, y + 25), f, 50, path=M)
            if k > i:
                text(d, (940, y + 25), 'not here', 50, RED)
        if k >= 3:
            chip(d, (110, 830), 'ENOENT: Executable not found in $PATH', 46, bg=RED)
        if k >= 4:
            text(d, (110, 960), 'the full path skips the search:', 50, path=R)
            chip(d, (110, 1040), '/opt/solidcraft-0.27.0/bin/solidcraft-cli', 44, bg=GREEN)
        save(im, f'card-path-{k}.png' if k < 4 else 'card-path.png')


def card_recap():
    lines = [('1  listed?', 'No MCP servers configured', 'Connect AI assistants'),
             ('2  connects?', 'ENOENT: Executable not found', 'Connect AI assistants again'),
             ('3  window open?', 'Note: a headless session', 'SolidCraft first, then restart Claude'),
             ('4  the reply', 'failed.index · rolled_back', 'fix that one thing')]
    for k in range(1, 5):
        im, d = canvas()
        text(d, (W / 2, 50), 'Remember the lamp: from the wall outward', 58, anchor='ma')
        for i, (a, b, c) in enumerate(lines[:k]):
            y = 180 + i * 240
            chip(d, (70, y), a, 48, bg=BLUE)
            text(d, (110, y + 100), b, 44, RED, path=M)
            text(d, (110, y + 160), '→ ' + c, 44, GREEN)
        save(im, f'card-recap-{k}.png' if k < 4 else 'card-recap.png')


ROWS = [('socket + plug', 'listed in your Claude app?', 'No MCP servers'),
        ('cord', "the plug's program found?", 'Executable not found'),
        ('switch', "SolidCraft's window open?", 'headless session'),
        ('bulb', 'what does the reply say?', 'rolled_back · format 44')]


def icon(d, i, x, y, col):
    """A small picture of lamp part i (0 socket + plug, 1 cord, 2 switch, 3 bulb) in a 130 x 130 box at x, y."""
    if i == 0:
        socket_plug(d, x + 5, y + 5, 0.45, col)
    elif i == 1:
        d.line((x + 5, y + 90, x + 45, y + 40, x + 85, y + 95, x + 125, y + 45), fill=col, width=12, joint='curve')
    elif i == 2:
        d.rounded_rectangle((x + 15, y + 35, x + 115, y + 100), radius=14, fill=PAPER, outline=col, width=7)
        d.rectangle((x + 48, y + 50, x + 82, y + 85), fill=col)
    else:
        d.ellipse((x + 30, y + 10, x + 100, y + 80), fill=LIGHT if col == GREEN else PAPER, outline=col, width=7)
        d.rectangle((x + 48, y + 80, x + 82, y + 115), fill=col)


def table(title, shown=4, ticks=0, lit=None, words=False, name='x', sub=True):
    """The lamp's parts (a picture each) beside the course's checks, one row per check."""
    im, d = canvas()
    text(d, (W / 2, 40), title, 60, anchor='ma')
    top = 120
    if sub:
        text(d, (W / 2, 120), "socket = your Claude app · the lamp's plug = our plug", 48, INK, path=R, anchor='ma')
        top = 200
    rh = (H - top - 30) // 4
    for i, (part, check, err) in enumerate(ROWS[:shown]):
        y = top + i * rh
        ok, on = i < ticks, (lit == i)
        col = GREEN if ok else (BLUE if on or lit is None else GREY)
        d.rounded_rectangle((40, y, 1592, y + rh - 22), radius=22, fill=PAPER, outline=col, width=8 if (ok or on) else 4)
        icon(d, i, 70, y + (rh - 22 - 130) // 2, col)
        text(d, (230, y + 22), f'{i + 1}  {part}', 50, INK)
        text(d, (230, y + 88), ('✓ ' if ok else '') + check, 52, col)
        if words:
            text(d, (230, y + 158), err, 48, RED, path=M)
    save(im, name)


if __name__ == '__main__':
    card_lamp()
    for k in range(1, 5):
        table("Our lamp is lesson 1's picture", shown=k, name=f'card-mapped-{k}.png' if k < 4 else 'card-mapped.png')
    table('So far: two checks passed', ticks=2, lit=2, name='card-sofar-2.png', sub=False)
    table('So far: three checks passed', ticks=3, lit=3, name='card-sofar-3.png', sub=False)
    card_path()
    for k in range(1, 5):
        table('Remember the lamp: from the wall outward', shown=k, words=True, sub=False, name=f'card-recap-{k}.png' if k < 4 else 'card-recap.png')
