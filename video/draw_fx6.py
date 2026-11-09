"""Fix-it fx6 cards (SolidCraft 0.28.0 Fillet: "the blend is larger than the neighbouring faces"), the draw_fx5.py
pattern: light, 2560 x 1440, one picture that builds; each step adds, earlier steps stay on and turn grey. Text 44 px+.
  full frame (RGB):  card-ball-1..3 (F3), card-sofar-1..3 (F8), card-recap-1..3 (F9c)
  overlays (RGBA, transparent outside the panel):
                     card-report-1..2 (F5, right 40%), card-limit-1..4 (F6, right 35%), card-question (F10, right half)
Sources: SCRIPT-fx6.md (plan folder 2026-11-fixit-2); out/fx6/ANSWERS.md Q2 (4.0, 4.9, 5.0 built, 5.1 refused, lip top
face 5.0 mm), Q3 (thickness 8: top face 8.0, front 10.0, 6 builds with 2.0 mm flat left), D/count.txt (325).
The lip in section (the hook's XZ sketch, lab/l7story.py HOOK): top face x 25-t..25 at z = 10, front face x = 25,
z 0..10, inner floor at z = 10 - t. A ball of radius r in the square corner has its centre at (25 - r, 10 - r).
Run in the QA image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fx6.py [sheet OUTDIR]"""
import math
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(LAB, 'video', 'frames-fx6')
FD = '/usr/share/fonts/truetype/dejavu/'
B, R, MONO = FD + 'DejaVuSans-Bold.ttf', FD + 'DejaVuSans.ttf', FD + 'DejaVuSansMono.ttf'
W, H = 2560, 1440
INK, RED, GREEN, GREY, BLUE, AMBER = (31, 41, 55), (183, 28, 28), (27, 127, 59), (110, 120, 138), (29, 78, 216), (180, 110, 0)
WHITE, LIGHT, PANEL = (255, 255, 255), (241, 245, 249), (250, 251, 253)
DONE, DONEFILL = (160, 167, 178), (244, 246, 248)
GREENFILL, AMBERFILL, REDFILL, PART = (221, 240, 227), (253, 236, 214), (251, 228, 228), (214, 220, 229)
MIN_PX = 44
MARK = (232, 89, 12)                 # cut 3: the orange marks (the edges in the question card)
PROBLEMS = []
LIP_H, EDGE_X = 10.0, 25.0          # lip_height, the lip's outer face (mm)


# --- geometry (tested against the lab) ------------------------------------------------------------------------------
def fits(r, t):
    """0.28.0 on this square edge: builds while the radius is no bigger than the narrowest face (top t, front 10)."""
    return r <= min(t, LIP_H) + 1e-9


def flat_left(r, t):
    return max(0.0, t - r)


def ball_centre(r):
    return (EDGE_X - r, LIP_H - r)


# --- drawing helpers (as draw_fx5.py) -------------------------------------------------------------------------------
def font(p, s):
    return ImageFont.truetype(p, s)


def text(d, xy, s, size=64, fill=INK, path=B, anchor='la', maxw=None, box=None):
    if size < MIN_PX:
        PROBLEMS.append(f'{s!r}: {size} px')
    f = font(path, size)
    d.text(xy, s, font=f, fill=fill, anchor=anchor)
    bb = d.textbbox(xy, s, font=f, anchor=anchor)
    if maxw and bb[2] - bb[0] > maxw:
        PROBLEMS.append(f'{s!r}: {bb[2] - bb[0]:.0f} px wide, max {maxw}')
    if box and (bb[0] < box[0] or bb[1] < box[1] or bb[2] > box[2] or bb[3] > box[3]):
        PROBLEMS.append(f'{s!r}: outside its panel {bb} vs {box}')
    if '<' in s or '>' in s:
        PROBLEMS.append(f'{s!r}: angle bracket')
    if len(s) > 44:
        PROBLEMS.append(f'{s!r}: {len(s)} columns, max 44')


def canvas():
    im = Image.new('RGB', (W, H), WHITE)
    return im, ImageDraw.Draw(im)


def overlay(box):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, radius=28, fill=PANEL + (255,), outline=INK + (255,), width=5)
    return im, d


def header(d, s):
    text(d, (W / 2, 100), s, 84, anchor='mm', maxw=2400)


def save(im, name):
    im.save(os.path.join(OUT, name))
    print(name)


def pal(k, step, accent=INK):
    if k == step:
        return {'ink': INK, 'acc': accent, 'fill': LIGHT, 'sub': GREY}
    return {'ink': DONE, 'acc': DONE, 'fill': DONEFILL, 'sub': DONE}


def caption(d, x, y, lines, p, size=56, gap=74):
    for i, ln in enumerate(lines):
        text(d, (x, y + i * gap), ln, size, p['acc'] if i == len(lines) - 1 else p['ink'], anchor='lm', maxw=W - 60 - x)


def dashed_circle(d, c, rad, col, w=8, n=48):
    for i in range(0, n, 2):
        a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        d.arc((c[0] - rad, c[1] - rad, c[0] + rad, c[1] + rad), math.degrees(a0), math.degrees(a1), fill=col, width=w)


class Lip:
    """The lip in section at scale s px/mm; (ox, oy) is the screen point of x = 25, z = 0."""

    def __init__(self, ox, oy, s, t, left=7.0):
        self.ox, self.oy, self.s, self.t, self.xl = ox, oy, s, t, EDGE_X - t - left

    def p(self, x, z):
        return (self.ox + (x - EDGE_X) * self.s, self.oy - z * self.s)

    def poly(self):
        t = self.t
        return [self.p(self.xl, 0), self.p(EDGE_X, 0), self.p(EDGE_X, LIP_H), self.p(EDGE_X - t, LIP_H),
                self.p(EDGE_X - t, LIP_H - t), self.p(self.xl, LIP_H - t)]

    def draw(self, d, col, fill=PART):
        t = self.t
        pts = self.poly()
        d.polygon(pts, fill=fill)
        d.line(pts, fill=col, width=7)                                         # bottom, front, top, inner, floor
        for i in range(0, 8, 2):                                               # the part goes on: a dashed cut
            a, b = self.p(self.xl, (LIP_H - t) * i / 8), self.p(self.xl, (LIP_H - t) * (i + 1) / 8)
            d.line((a, b), fill=col, width=4)

    def ball_clipped(self, im, r, col, clip, **kw):
        """cut 3: the ball drawn only inside the part ('part') or inside the lip's box above its bottom ('box'), so
        no circle pokes out below the part (watch-c2: it read as a ball bigger than the lip)."""
        layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
        self.ball(ImageDraw.Draw(layer), r, col, **kw)
        mask = Image.new('L', im.size, 0)
        md = ImageDraw.Draw(mask)
        if clip == 'part':
            md.polygon(self.poly(), fill=255)
        else:
            a, b = self.p(self.xl, LIP_H + 2), self.p(EDGE_X + 2, 0)
            md.rectangle((a[0], a[1], b[0], b[1]), fill=255)
        im.paste(layer, (0, 0), ImageChops.multiply(layer.getchannel('A'), mask))

    def ball(self, d, r, col, fill=None, dash=False, radii=True):
        cx, cz = ball_centre(r)
        c, rad = self.p(cx, cz), r * self.s
        if fill:
            d.ellipse((c[0] - rad, c[1] - rad, c[0] + rad, c[1] + rad), fill=fill)
        # the whole ball thin (dashed when it has no room), the round it makes thick: the quarter between the two
        # touch points, and one radius drawn to each touch point
        if dash:
            dashed_circle(d, c, rad, col, w=5)
        else:
            d.ellipse((c[0] - rad, c[1] - rad, c[0] + rad, c[1] + rad), outline=col, width=4)
        d.arc((c[0] - rad, c[1] - rad, c[0] + rad, c[1] + rad), 270, 360, fill=col, width=12)
        if radii:
            d.line((c, (c[0], c[1] - rad)), fill=col, width=4)
            d.line((c, (c[0] + rad, c[1])), fill=col, width=4)
            d.ellipse((c[0] - 9, c[1] - 9, c[0] + 9, c[1] + 9), fill=col)

    def sliver(self, d, r, fill):
        """The material outside the ball's curve at the corner: shaved off."""
        cx, cz = ball_centre(r)
        pts = [self.p(EDGE_X, LIP_H)] + [self.p(cx + r * math.cos(a), cz + r * math.sin(a))
                                          for a in [math.pi / 2 * k / 24 for k in range(25)]]
        d.polygon(pts, fill=fill)

    def tick_top(self, d, x, col):
        a = self.p(x, LIP_H)
        d.line((a[0], a[1] - 34, a[0], a[1] + 34), fill=col, width=8)

    def tick_front(self, d, z, col):
        a = self.p(EDGE_X, z)
        d.line((a[0] - 34, a[1], a[0] + 34, a[1]), fill=col, width=8)

    def dim_top(self, d, x0, x1, label, col, size=48, up=80):
        a, b = self.p(x0, LIP_H), self.p(x1, LIP_H)
        y = a[1] - up
        d.line((a[0], y, b[0], y), fill=col, width=5)
        for x in (a[0], b[0]):
            d.line((x, y - 18, x, y + 18), fill=col, width=5)
        text(d, ((a[0] + b[0]) / 2, y - 40), label, size, col, anchor='mm')


# --- F3: the rolling ball ---------------------------------------------------------------------------------------------
CAPX = 1500


BALL_STEPS = ['ball', 'radius', 'ticks', 'six']   # cut 3: steps 2..5 (watch-c2: the r = 2 step held 22.5 s unchanged)


def card_ball(step):
    im, d = canvas(); header(d, 'Why 6 mm will not fit: the lip from the side')
    lip = Lip(1120, 1120, 72, 5)
    p = pal(1, step, BLUE)                       # 1: the lip, its two faces, the edge; a sanded table corner
    lip.draw(d, p['ink'])
    lip.dim_top(d, 20, 25, 'top face: 5 mm', p['acc'], up=150)
    a = lip.p(25, 0)
    text(d, (a[0] + 40, lip.p(25, 5)[1]), 'front face:', 48, p['acc'], anchor='lm')
    text(d, (a[0] + 40, lip.p(25, 5)[1] + 62), '10 mm', 48, p['acc'], anchor='lm')
    e = lip.p(25, 10)
    d.ellipse((e[0] - 16, e[1] - 16, e[0] + 16, e[1] + 16), fill=p['acc'])
    caption(d, CAPX, 300, ['a fillet rounds this edge,', 'like a sanded table corner'], p)
    d.rounded_rectangle((CAPX, 400, CAPX + 360, 490), radius=60, fill=p['fill'], outline=p['ink'], width=6,
                        corners=(False, True, False, False))
    text(d, (CAPX + 400, 445), 'a table top, sanded', 44, p['sub'], R, anchor='lm', maxw=W - 40 - CAPX - 400)
    if step >= 2:                                # 2: a 2 mm ball pressed into the corner from inside; the sliver
        p = pal(2, step, GREEN)
        lip.sliver(d, 2, AMBERFILL if step == 2 else DONEFILL)
        lip.ball(d, 2, p['acc'], fill=GREENFILL if step == 2 else None, radii=step >= 3)
        caption(d, CAPX, 570, ['a ball pressed into the corner:', 'outside its curve is shaved off'], p)
    if step >= 3:                                # 3: its radius, centre to surface
        p = pal(3, step, GREEN)
        q = lip.p(23, 8)
        text(d, (q[0], q[1] + 70), 'r = 2 mm', 44, p['acc'], anchor='mm')
        caption(d, CAPX, 730, ['radius = centre to surface'], p)
    if step >= 4:                                # 4: it touches each face one radius from the edge (ticks + 2 mm)
        p = pal(4, step, GREEN)
        lip.tick_top(d, 23, p['acc'])
        lip.tick_front(d, 8, p['acc'])
        lip.dim_top(d, 23, 25, '2 mm', p['acc'], size=44, up=60)
        f = lip.p(25, 9)
        text(d, (f[0] + 60, f[1] - 30), '2 mm', 44, p['acc'], anchor='lm')
        caption(d, CAPX, 830, ['touches each face', 'one radius from the edge'], p)
    if step >= 5:                                # 5: a 6 mm ball: its touch point falls 1 mm past the face
        p = pal(5, step, RED)
        lip.ball(d, 6, RED, dash=True)
        lip.tick_top(d, 19, RED)
        c6 = lip.p(19, 4)
        text(d, (c6[0] + 170, c6[1] + 60), 'r = 6 mm', 48, RED, anchor='mm')
        q = lip.p(19, 10)
        text(d, (q[0] - 20, q[1] - 70), '1 mm past the face', 46, RED, anchor='rm')
        caption(d, CAPX, 1000, ['a 6 mm radius needs 6 mm', 'of top face: only 5 here'], p)
        text(d, (CAPX, 1180), 'r 6 mm, face 5 mm: no room', 60, RED, anchor='lm', maxw=W - 40 - CAPX)
    text(d, (W / 2, 1330), 'width: measured straight across,', 46, GREY, R, anchor='mm')
    text(d, (W / 2, 1390), 'away from the edge', 46, GREY, R, anchor='mm')
    save(im, f'card-ball-{step}.png')


# --- F8: so far, 5 mm against 8 mm -------------------------------------------------------------------------------------
def card_sofar(step):
    im, d = canvas(); header(d, 'So far: the same 6 mm ball, two lips')
    # the last step is the rule under BOTH pictures, so both stay in colour there (the contrast is the point)
    p = pal(1, 1 if step == 3 else step, RED)
    left = Lip(1000, 980, 55, 5)
    left.draw(d, p['ink'])
    left.ball(d, 6, p['acc'], dash=True)
    left.dim_top(d, 20, 25, 'top 5 mm', p['acc'], up=120)
    text(d, (640, 1150), 'r 6 mm: no room', 56, p['acc'], anchor='mm')
    if step >= 2:
        p = pal(2, 2 if step == 3 else step, GREEN)
        right = Lip(2300, 980, 55, 8)
        right.draw(d, p['ink'])
        right.sliver(d, 6, AMBERFILL)
        right.ball(d, 6, p['acc'])
        right.dim_top(d, 17, 25, 'top 8 mm', p['acc'], up=120)
        text(d, (1900, 1150), 'room: 2 mm flat left', 56, p['acc'], anchor='mm')
    if step >= 3:
        d.rounded_rectangle((160, 1215, 2400, 1405), radius=26, fill=GREENFILL, outline=GREEN, width=6)
        text(d, (W / 2, 1258), 'radius no bigger than the width', 60, INK, anchor='mm', maxw=2200)
        text(d, (W / 2, 1322), 'of the narrowest face beside the edge', 60, INK, anchor='mm', maxw=2200)
        text(d, (2370, 1372), '(on a square edge)', 48, GREY, R, anchor='rm')
    save(im, f'card-sofar-{step}.png')


# --- F9c: recap -------------------------------------------------------------------------------------------------------
RECAP = [['read the whole line:', 'here it names the largest radius'],
         ['radius no bigger than the width', 'of the narrowest face beside the edge'],
         ['need more? widen that face first', '(thickness), then round it']]


def card_recap(step):
    im, d = canvas(); header(d, 'Recap: the blend is larger than the faces')
    y = 220
    for k, lines in enumerate(RECAP[:step]):
        p = pal(k + 1, step, GREEN)
        d.rounded_rectangle((120, y, 2440, y + 300), radius=26, fill=p['fill'], outline=p['ink'], width=6)
        text(d, (190, y + 110), f'{k + 1}', 72, p['acc'], anchor='lm')
        for i, ln in enumerate(lines):
            text(d, (300, y + 100 + i * 100), ln, 68, p['ink'] if i == 0 else p['acc'], anchor='lm', maxw=2100)
        y += 340
    save(im, f'card-recap-{step}.png')


# --- F5: the report title count (overlay, right 40%) -----------------------------------------------------------------
REPORT = (1536, 150, 2520, 1250)


def card_report(step):
    """cut 3: full frame (watch-c2: the right-third overlay left the left 60% of the frame empty for 15 s)."""
    im, d = canvas(); header(d, 'You are not alone: the Create Issue count')
    p = pal(1, step, BLUE)
    d.rounded_rectangle((120, 230, 1250, 1180), radius=28, fill=p['fill'], outline=p['ink'], width=6)
    text(d, (685, 470), '325', 240, p['acc'], anchor='mm')
    text(d, (685, 680), 'reports titled', 72, p['ink'], anchor='mm')
    text(d, (685, 790), 'FILLET: operation failed', 64, p['ink'], MONO, anchor='mm', maxw=1080)
    text(d, (685, 920), 'every kind of fillet failure', 56, p['sub'], R, anchor='mm', maxw=1080)
    text(d, (685, 1040), 'counted the day we filmed', 52, p['sub'], R, anchor='mm')
    if step >= 2:
        p = pal(2, step, GREEN)
        d.rounded_rectangle((1310, 230, 2440, 1180), radius=28, fill=GREENFILL, outline=p['ink'], width=6)
        text(d, (1875, 470), '13 of 100', 170, p['acc'], anchor='mm', maxw=1080)   # out/fx6/D/reasons.txt
        text(d, (1875, 680), 'of the newest reports', 64, p['ink'], anchor='mm', maxw=1080)
        text(d, (1875, 790), 'have our reason:', 72, p['ink'], anchor='mm')
        text(d, (1875, 920), 'about 1 in 8', 96, p['acc'], anchor='mm')
        text(d, (1875, 1040), 'counted the day we filmed', 52, p['sub'], R, anchor='mm')
    save(im, f'card-report-{step}.png')


# --- F6: the limit table (overlay, right 35%) ------------------------------------------------------------------------
LIMIT = (1664, 150, 2520, 1290)
TRIES = [('r 4.0 mm: built', '1.0 mm flat left', True), ('r 4.9 mm: built', '0.1 mm flat left', True),
         ('r 5.0 mm: built', 'no flat left', True), ('r 5.1 mm: refused', 'the same red line', False)]


def card_limit(step):
    im, d = overlay(LIMIT)
    x, bx = LIMIT[0] + 50, LIMIT
    text(d, (x, 220), 'Same edge, 4 tries', 58, INK, anchor='lm', box=bx)
    text(d, (x, 290), 'top face: 5 mm', 46, GREY, R, anchor='lm', box=bx)
    d.line((x, 335, LIMIT[2] - 50, 335), fill=GREY, width=3)
    for k, (a, b, ok) in enumerate(TRIES[:step]):
        p = pal(k + 1, step, GREEN if ok else RED)
        y = 420 + k * 220
        d.ellipse((x, y - 22, x + 44, y + 22), fill=p['acc'])
        text(d, (x + 70, y), a, 58, p['acc'] if not ok else p['ink'], anchor='lm', box=bx)
        text(d, (x + 70, y + 80), b, 48, p['sub'], R, anchor='lm', box=bx)
    save(im, f'card-limit-{step}.png')


# --- F10: the question (overlay, right half; no answer on screen) ----------------------------------------------------
QUEST = (1300, 170, 2520, 1270)


def card_question(step):
    """cut 3: the 5 mm lip in section with BOTH top edges marked (watch-c2: the thumbnail was tiny, edges unmarked)."""
    im, d = overlay(QUEST)
    cx, bx = (QUEST[0] + QUEST[2]) / 2, QUEST
    text(d, (cx, 250), 'The question', 56, GREY, anchor='mm', box=bx)
    text(d, (cx, 335), '5 mm lip, side view', 72, INK, anchor='mm', box=bx)
    lip = Lip(cx + 150, 810, 32, 5, left=9.0)
    lip.draw(d, INK)
    lip.dim_top(d, 20, 25, '5 mm', BLUE, size=44, up=56)
    for k, x in enumerate((20, 25), 1):          # the inner and the outer top edge
        e = lip.p(x, LIP_H)
        d.ellipse((e[0] - 26, e[1] - 26, e[0] + 26, e[1] + 26), outline=MARK, width=9)
        text(d, (e[0] + (-40 if k == 1 else 40), e[1] + 40), f'edge {k}', 44, MARK, anchor='rm' if k == 1 else 'lm', box=bx)
    text(d, (cx, 885), 'Both top edges at 2.5 mm,', 64, INK, anchor='mm', box=bx)
    text(d, (cx, 960), 'in one Fillet.', 64, INK, anchor='mm', box=bx)
    text(d, (cx, 1045), 'Will it build?', 90, BLUE, anchor='mm', box=bx)
    if step < 2:
        save(im, 'card-question-1.png')
        return
    d.rounded_rectangle((QUEST[0] + 80, 1110, QUEST[2] - 80, 1240), radius=26, fill=GREENFILL, outline=GREEN, width=8)
    text(d, (cx, 1175), 'Pause and think', 72, GREEN, anchor='mm', box=bx)
    save(im, 'card-question-2.png')


# --- fx6 Short cut 2: the same side view at the Short's view size (1080 x 960), three steps ---------------------------
SHORT_BALL = [(6.0, 5), (5.0, 5), (6.0, 8)]      # (ball radius, top face) per step, as the lab measured (fits())
SW, SH_ = 1080, 960
SHORT_OY = 640                                    # the lips' bottom (z = 0) on the Short card
SHORT_TITLE = 'Side view: a ball at the outer top edge'


def card_short_ball(step):
    im = Image.new('RGB', (SW, SH_), WHITE)
    d = ImageDraw.Draw(im)
    text(d, (SW / 2, 56), SHORT_TITLE, 44, anchor='mm', maxw=SW - 60)
    left, right = Lip(470, SHORT_OY, 30, 5), Lip(1010, SHORT_OY, 30, 8)
    left.draw(d, INK)
    left.dim_top(d, 20, 25, 'top 5 mm', BLUE, size=44, up=60)
    for k, ((r, t), lip) in enumerate(zip(SHORT_BALL, (left, left, right)), 1):
        if k > step:
            break
        ok = fits(r, t)
        col = GREEN if ok else RED
        if k == 3:
            lip.draw(d, INK)
            lip.dim_top(d, 17, 25, 'top 8 mm', BLUE, size=44, up=60)
        if ok:                                    # cut 3: the ball inside the part only
            lip.sliver(d, r, AMBERFILL)
            lip.ball_clipped(im, r, col, 'part', fill=GREENFILL if k == step else None)
        else:                                     # no room: dashed, kept above the part's bottom
            lip.ball_clipped(im, r, col, 'box', dash=True)
            lip.tick_top(d, ball_centre(r)[0], col)
        cap = {1: '6 mm: 1 mm past', 2: '5 mm: just fits', 3: '8 mm: 6 fits inside'}[k]
        x = 290 if k < 3 else 800
        text(d, (x, 770 if k != 2 else 840), cap, 44, col, anchor='mm', maxw=500)
    if step >= 3:
        text(d, (SW / 2, 920), 'the ball must touch both faces', 44, GREY, R, anchor='mm', maxw=SW - 60)
    save(im, f'card-short-ball-{step}.png')


def sheet(outdir):
    names = sorted(n for n in os.listdir(OUT) if n.endswith('.png'))
    tw, th, cols = 512, 288, 5
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
    sh.save(os.path.join(outdir, 'fx6-sheet.png'))
    print('sheet', len(names))


def check_alpha():
    boxes = {'card-limit': LIMIT, 'card-question': QUEST}
    for n in sorted(os.listdir(OUT)):
        stem = n[:-4].rsplit('-', 1)[0] if n[:-4].rsplit('-', 1)[-1].isdigit() else n[:-4]
        if stem in boxes:
            im, box = Image.open(os.path.join(OUT, n)), boxes[stem]
            bb = im.getchannel('A').getbbox()
            if im.mode != 'RGBA' or bb[0] < box[0] or bb[2] > box[2] + 1 or bb[1] < box[1] or bb[3] > box[3] + 1:
                PROBLEMS.append(f'{n}: alpha bbox {bb}')


def main():
    os.makedirs(OUT, exist_ok=True)
    for s in range(1, len(BALL_STEPS) + 2):
        card_ball(s)
    for s in (1, 2, 3):
        card_sofar(s)
        card_recap(s)
        card_short_ball(s)
    for s in (1, 2):
        card_report(s)
    for s in (1, 2, 3, 4):
        card_limit(s)
    for s in (1, 2):
        card_question(s)
    check_alpha()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
        sys.exit(0)
    main()
