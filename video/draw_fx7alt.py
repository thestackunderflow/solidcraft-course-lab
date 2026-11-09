"""Fix-it fx7alt cards (SolidCraft fillet at a corner: refused, with the count of edges that meet there), the
draw_fx8.py pattern: light, 2560 x 1440, one picture that builds; each step adds, earlier steps stay on and turn grey.
Text 44 px+, 44 columns at most per line.
  full frame (RGB):  card-map-1..5 (F3; 4 and 5 split the old 15 s hold, cut 2), card-sofar-1..3 (F8, the same map)
  overlay (RGBA, transparent outside the panel): card-question-1..2 (F10, right half; no answer on screen)
Sources: out/fx7alt/ANSWERS.md (the fresh 20 mm box, 8000.0 mm3; Z up; 0, 0, 0 left bottom, 20, 20, 20 right top in the
home view; fillet 20 20 20 refused with the count 3; issue 5173: an old chamfer cut one edge, unasked).

The three edges that meet at the corner 20, 20, 20, one colour each on every card (and for the footage overlay):
  EDGE_X  #1D4ED8 blue    (29, 78, 216)   20,20,20 to 0,20,20   the top edge at the back right (the map's left road)
  EDGE_Y  #7E22CE purple  (126, 34, 206)  20,20,20 to 20,0,20   the top edge at the right      (the map's right road)
  EDGE_Z  #B45309 amber   (180, 83, 9)    20,20,20 to 20,20,0   the upright edge               (the map's lower road)
Run in the QA image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fx7alt.py [sheet OUTDIR]"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(LAB, 'video', 'frames-fx7alt')
FD = '/usr/share/fonts/truetype/dejavu/'
B, R = FD + 'DejaVuSans-Bold.ttf', FD + 'DejaVuSans.ttf'
W, H = 2560, 1440
INK, RED, GREEN, GREY, BLUE = (31, 41, 55), (183, 28, 28), (27, 127, 59), (110, 120, 138), (29, 78, 216)
WHITE, LIGHT, PANEL = (255, 255, 255), (241, 245, 249), (250, 251, 253)
DONE, DONEFILL = (160, 167, 178), (244, 246, 248)
GREENFILL, REDFILL = (221, 240, 227), (251, 228, 228)
TOPFILL, SIDEFILL, FRONTFILL = (236, 240, 245), (205, 212, 222), (222, 228, 236)
MAPFILL, PARK, WATER, CASING = (247, 244, 236), (222, 238, 214), (214, 232, 246), (176, 182, 192)
SKIN = (253, 226, 204)
MARK = (232, 89, 12)
MIN_PX = 44
PROBLEMS = []
LOG = {}                                          # card name -> [(text, px)] in drawing order
CUR = []

# --- the box and its corner (tested against the lab) ----------------------------------------------------------------
BOX = 20
CORNER = (20, 20, 20)
EDGE_X, EDGE_Y, EDGE_Z = (29, 78, 216), (126, 34, 206), (180, 83, 9)
EDGES = {'x': (CORNER, (0, 20, 20), EDGE_X), 'y': (CORNER, (20, 0, 20), EDGE_Y), 'z': (CORNER, (20, 20, 0), EDGE_Z)}
QPOINT = (20, 20, 19)                             # the F10 question: 1 mm below the corner (never answered here)

# --- the map: a Y junction where three roads end (screen coords; the box corner seen from 20, 20, 20 is the same Y) --
MAP = (80, 180, 1280, 1380)
T30 = math.tan(math.radians(30))
JUNCTION = (720, 660)
ROADS = [([JUNCTION, (MAP[0], round(JUNCTION[1] - (JUNCTION[0] - MAP[0]) * T30))], EDGE_X),
         ([JUNCTION, (MAP[2], round(JUNCTION[1] - (MAP[2] - JUNCTION[0]) * T30))], EDGE_Y),
         ([JUNCTION, (JUNCTION[0], MAP[3])], EDGE_Z)]
FINGER_J = (math.cos(math.radians(30)), 0.5)                     # between the right road and the lower one
HALF = tuple(round((a + b) / 2) for a, b in zip(*ROADS[0][0]))   # halfway along the left road


# --- drawing helpers (as draw_fx8.py) -------------------------------------------------------------------------------
def font(p, s):
    return ImageFont.truetype(p, s)


def text(d, xy, s, size=64, fill=INK, path=B, anchor='la', maxw=None, box=None):
    CUR.append((s, size))
    if size < MIN_PX:
        PROBLEMS.append(f'{s!r}: {size} px')
    f = font(path, size)
    d.text(xy, s, font=f, fill=fill, anchor=anchor)
    bb = d.textbbox(xy, s, font=f, anchor=anchor)
    if maxw and bb[2] - bb[0] > maxw:
        PROBLEMS.append(f'{s!r}: {bb[2] - bb[0]:.0f} px wide, max {maxw}')
    if bb[0] < 0 or bb[2] > W:
        PROBLEMS.append(f'{s!r}: off the frame {bb}')
    if box and (bb[0] < box[0] or bb[1] < box[1] or bb[2] > box[2] or bb[3] > box[3]):
        PROBLEMS.append(f'{s!r}: outside its panel {bb} vs {box}')
    if '<' in s or '>' in s:
        PROBLEMS.append(f'{s!r}: angle bracket')
    if len(s) > 44:
        PROBLEMS.append(f'{s!r}: {len(s)} columns, max 44')


def canvas():
    CUR.clear()
    im = Image.new('RGB', (W, H), WHITE)
    return im, ImageDraw.Draw(im)


def overlay(box):
    CUR.clear()
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, radius=28, fill=PANEL + (255,), outline=INK + (255,), width=5)
    return im, d


def header(d, s):
    text(d, (W / 2, 100), s, 84, anchor='mm', maxw=2400)


def save(im, name):
    im.save(os.path.join(OUT, name))
    LOG[name] = list(CUR)
    print(name)


def pal(k, step, accent=INK):
    if k == step:
        return {'ink': INK, 'acc': accent, 'fill': WHITE, 'skin': SKIN, 'on': True}
    return {'ink': DONE, 'acc': DONE, 'fill': DONEFILL, 'skin': DONEFILL, 'on': False}


def callout(d, box, lines, p, size=52, accents=()):
    d.rounded_rectangle(box, radius=22, fill=p['fill'], outline=p['ink'], width=5)
    cx, n = (box[0] + box[2]) / 2, len(lines)
    cy0 = (box[1] + box[3]) / 2 - (n - 1) * size * 0.6
    for i, ln in enumerate(lines):
        text(d, (cx, cy0 + i * size * 1.2), ln, size, p['acc'] if i in accents else p['ink'], anchor='mm',
             box=box)


# --- the street map -------------------------------------------------------------------------------------------------
def draw_map(d):
    d.rectangle(MAP, fill=MAPFILL)
    x0, y0, x1, y1 = MAP
    d.rounded_rectangle((x0 + 60, y0 + 40, x0 + 330, y0 + 150), radius=18, fill=PARK)       # top left park
    d.ellipse((x1 - 330, y1 - 330, x1 - 70, y1 - 120), fill=WATER)                           # pond, bottom right
    d.rounded_rectangle((x0 + 40, y1 - 230, x0 + 560, y1 - 50), radius=18, fill=PARK)       # park, bottom left
    d.rounded_rectangle((x1 - 360, y0 + 30, x1 - 60, y0 + 120), radius=18, fill=PARK)       # top right park
    for w, col in ((62, CASING), (48, WHITE)):
        for pts, _ in ROADS:
            d.line(pts, fill=col, width=w)
        d.ellipse((JUNCTION[0] - w / 2, JUNCTION[1] - w / 2, JUNCTION[0] + w / 2, JUNCTION[1] + w / 2), fill=col)
    for pts, col in ROADS:                                                                   # the route stripes
        d.line(pts, fill=col, width=16)
    d.ellipse((JUNCTION[0] - 8, JUNCTION[1] - 8, JUNCTION[0] + 8, JUNCTION[1] + 8), fill=INK)
    for clip in ((0, y0 - 40, x0, y1), (x1, y0 - 40, x1 + 70, y1), (x0, y1, x1, y1 + 40)):   # roads end at the frame
        d.rectangle(clip, fill=WHITE)
    d.rectangle(MAP, outline=INK, width=6)


def finger(d, tip, direction, p, ring):
    """A finger pointing at `tip`, its body running back along `direction`; a ring marks the point."""
    ux, uy = direction
    n = math.hypot(ux, uy)
    ux, uy = ux / n, uy / n
    vx, vy = -uy, ux                                     # across the finger
    w, ln = 72, 270
    cx, cy = tip[0] + ux * w / 2, tip[1] + uy * w / 2
    pts = []
    for i in range(13):                                  # the round tip
        a = math.pi * i / 12
        pts.append((cx + (-ux * math.sin(a) + vx * math.cos(a)) * w / 2,
                    cy + (-uy * math.sin(a) + vy * math.cos(a)) * w / 2))
    bx, by = tip[0] + ux * ln, tip[1] + uy * ln
    pts += [(bx - vx * w / 2, by - vy * w / 2), (bx + vx * w / 2, by + vy * w / 2)]
    d.ellipse((tip[0] - 40, tip[1] - 40, tip[0] + 40, tip[1] + 40), outline=ring, width=9)
    d.polygon(pts, fill=p['skin'], outline=p['ink'], width=5)
    nx, ny = tip[0] + ux * 34, tip[1] + uy * 34          # the nail
    d.polygon([(nx + vx * 20 + ux * dd, ny + vy * 20 + uy * dd) for dd in (-6, 26)] +
              [(nx - vx * 20 + ux * dd, ny - vy * 20 + uy * dd) for dd in (26, -6)],
              fill=(255, 241, 230) if p['on'] else DONEFILL, outline=p['ink'], width=3)
    for k in (130, 190):                                 # creases
        qx, qy = tip[0] + ux * k, tip[1] + uy * k
        d.line((qx - vx * 22, qy - vy * 22, qx + vx * 22, qy + vy * 22), fill=p['ink'], width=4)


# --- the box corner, seen from 20, 20, 20 (the three edges form the same Y as the map) --------------------------------
class Box:
    def __init__(self, cx, cy, s):
        self.cx, self.cy, self.s = cx, cy, s

    def p(self, x, y, z):
        dx, dy, dz = x - CORNER[0], y - CORNER[1], z - CORNER[2]
        c30 = math.cos(math.radians(30))
        return (self.cx + (dx - dy) * c30 * self.s, self.cy + (-dz + (dx + dy) * 0.5) * self.s)

    def draw(self, d, on=True, rgba=False):
        a = (lambda col: col + (255,)) if rgba else (lambda col: col)  # noqa: E731
        ink = INK if on else DONE
        faces = [([(20, 20, 20), (0, 20, 20), (0, 0, 20), (20, 0, 20)], TOPFILL),
                 ([(20, 20, 20), (20, 0, 20), (20, 0, 0), (20, 20, 0)], SIDEFILL),
                 ([(20, 20, 20), (0, 20, 20), (0, 20, 0), (20, 20, 0)], FRONTFILL)]
        for pts, fill in faces:
            q = [self.p(*v) for v in pts]
            d.polygon(q, fill=a(fill if on else DONEFILL))
            d.line(q + q[:1], fill=a(ink), width=6, joint='curve')
        for _, (s, e, col) in EDGES.items():
            d.line((self.p(*s), self.p(*e)), fill=a(col if on else DONE), width=16)
        x, y = self.p(*CORNER)
        d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=a(ink))


# --- card 1 (F3): pointing at a map -----------------------------------------------------------------------------------
BOX_MAP = Box(1910, 640, 16)


def card_map(step):
    im, d = canvas(); header(d, 'Which road do you mean?')
    draw_map(d)
    p = pal(1, step, EDGE_X)                     # 1: halfway along one road
    callout(d, (110, 790, 670, 900), ['halfway: one road'], p, 52, accents=(0,))
    finger(d, HALF, (-0.28, 1), p, p['acc'])
    if step >= 2:                                # 2: on the Y junction, where three roads end
        p = pal(2, step, RED)
        callout(d, (420, 240, 1020, 430), ['3 roads end here:', 'which one?'], p, 52, accents=(1,))
        finger(d, JUNCTION, FINGER_J, p, p['acc'])
    if step >= 3:                                # 3: the box corner beside it, the three edges as the three roads
        p = pal(3, step, INK)
        BOX_MAP.draw(d)
        text(d, (BOX_MAP.cx, 1050), 'a corner: 3 edges meet', 64, INK, anchor='mm', maxw=1100)
    if step >= 4:                                # 4 (cut 2: the 15 s hold split): the old version's guess
        p = pal(4, step, INK)
        callout(d, (1400, 1140, 2420, 1340), ['issue 5173 (a bug report):', 'an old chamfer cut one, unasked'],
                {**p, 'fill': LIGHT}, 50)
    if step >= 5:                                # 5: what SolidCraft does now
        p = pal(5, step, RED)
        callout(d, (1400, 190, 2420, 300), ['now: refused, with the count'], p, 50, accents=(0,))
    save(im, f'card-map-{step}.png')


# --- card 2 (F8): so far, on the same map ---------------------------------------------------------------------------
def ring_icon(d, x, y, col):
    d.ellipse((x - 40, y - 40, x + 40, y + 40), outline=col, width=10)
    d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=col)


def card_sofar(step):
    im, d = canvas(); header(d, 'So far')
    draw_map(d)
    p = pal(1, step, GREEN)                      # 1: inside one edge: builds
    finger(d, HALF, (-0.28, 1), p, p['acc'])
    d.rounded_rectangle((1360, 230, 2480, 430), radius=26, fill=GREENFILL if p['on'] else DONEFILL,
                        outline=p['ink'], width=6)
    ring_icon(d, 1450, 330, p['acc'])
    text(d, (1530, 330), 'inside one edge: builds', 62, p['acc'], anchor='lm', maxw=920)
    if step >= 2:                                # 2: a corner: refused, with the count
        p = pal(2, step, RED)
        finger(d, JUNCTION, FINGER_J, p, p['acc'])
        d.rounded_rectangle((1360, 480, 2480, 780), radius=26, fill=REDFILL if p['on'] else DONEFILL,
                            outline=p['ink'], width=6)
        ring_icon(d, 1450, 630, p['acc'])
        text(d, (1530, 580), 'a corner, 3 edges meet:', 62, p['ink'], anchor='lm', maxw=920)
        text(d, (1530, 680), 'refused, with the count', 62, p['acc'], anchor='lm', maxw=920)
    if step >= 3:                                # 3: one line under both
        p = pal(3, step, BLUE)
        d.line((1360, 840, 2480, 840), fill=INK, width=6)
        d.rounded_rectangle((1360, 890, 2480, 1150), radius=26, fill=LIGHT, outline=INK, width=6)
        text(d, (1400, 970), 'the point picks the edge;', 60, INK, anchor='lm', maxw=1060)
        text(d, (1400, 1070), 'the round runs all along it', 60, INK, anchor='lm', maxw=1060)
    save(im, f'card-sofar-{step}.png')


# --- card 3 (F10): the question (overlay, right half; no answer on screen) --------------------------------------------
QUEST = (1300, 170, 2520, 1270)


def card_question(step):
    im, d = overlay(QUEST)
    cx, bx = (QUEST[0] + QUEST[2]) / 2, QUEST
    text(d, (cx, 260), 'A question', 72, INK, anchor='mm', box=bx)
    box = Box(cx, 610, 11)
    box.draw(d, rgba=True)
    x, y = box.p(*QPOINT)
    d.ellipse((x - 13, y - 13, x + 13, y + 13), fill=MARK + (255,), outline=INK + (255,), width=3)
    text(d, (cx, 940), 'Fresh box. Point [20, 20, 19].', 58, INK, anchor='mm', box=bx, maxw=1120)
    text(d, (cx, 1030), 'Rounds, or refused?', 66, INK, anchor='mm', box=bx)
    if step < 2:
        save(im, 'card-question-1.png')
        return
    d.rounded_rectangle((QUEST[0] + 80, 1100, QUEST[2] - 80, 1230), radius=26, fill=GREENFILL, outline=GREEN, width=8)
    text(d, (cx, 1165), 'Pause and think', 72, GREEN, anchor='mm', box=bx)
    save(im, 'card-question-2.png')


def sheet(outdir):
    names = sorted(n for n in os.listdir(OUT) if n.endswith('.png'))
    tw, th, cols = 640, 360, 3
    rows = -(-len(names) // cols)
    sh = Image.new('RGB', (tw * cols, (th + 30) * rows), (90, 90, 90))
    dd = ImageDraw.Draw(sh)
    for i, n in enumerate(names):
        im = Image.open(os.path.join(OUT, n)).convert('RGBA')
        bg = Image.new('RGBA', im.size, (60, 70, 85, 255))
        t = Image.alpha_composite(bg, im).convert('RGB').resize((tw - 8, th - 8))
        x, y = (i % cols) * tw, (i // cols) * (th + 30)
        sh.paste(t, (x + 4, y + 4))
        dd.text((x + 6, y + th), n, font=font(R, 22), fill=(255, 255, 255))
    sh.save(os.path.join(outdir, 'fx7alt-sheet.png'))
    print('sheet', len(names))


def check_alpha():
    for n in sorted(os.listdir(OUT)):
        if n.startswith('card-question'):
            im = Image.open(os.path.join(OUT, n))
            bb = im.getchannel('A').getbbox()
            if im.mode != 'RGBA' or bb[0] < QUEST[0] or bb[2] > QUEST[2] + 1 or bb[1] < QUEST[1] or bb[3] > QUEST[3] + 1:
                PROBLEMS.append(f'{n}: alpha bbox {bb}')


def main():
    os.makedirs(OUT, exist_ok=True)
    for s in (1, 2, 3, 4, 5):
        card_map(s)
    for s in (1, 2, 3):
        card_sofar(s)
    for s in (1, 2):
        card_question(s)
    check_alpha()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
        sys.exit(0)
    main()
