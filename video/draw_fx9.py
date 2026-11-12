"""Fix-it fx9 cards (SolidCraft Thread: an 8 mm hole is too wide for a modelled M8 thread; drill 6.75), the
draw_fx7alt.py pattern: light, 2560 x 1440, one picture that builds; each step adds, earlier steps stay on and turn grey.
Text 44 px+, 44 columns at most per line.
  full frame (RGB):  card-lid-1..3 (F3), card-pitch-1..3 (F5), card-sofar-1..2 (F8, the same lid picture: the peg twice)
  overlay (RGBA, transparent left of x 1300): card-cut-1..2 (F4), card-question-1..2 (F10; no answer on screen)
Facts (SCRIPT-fx9.md): M8 pitch 1.25, tooth height 0.68 (about half a pitch), hole 8 - 1.25 = 6.75; M5 5 - 0.8 = 4.2
(cut 2: M5 no longer drawn; the bar shows 8 mm across the whole bar, the hole 6.75 in the middle, no tooth numbers);
the filmed window: 6.3 refused (too narrow), 6.5 built, 7.6 built, 7.7 refused (cuts too little). The M10 question is
asked, never answered.
Run in the QA image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fx9.py [sheet OUTDIR]"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(LAB, 'video', 'frames-fx9')
FD = '/usr/share/fonts/truetype/dejavu/'
B, R = FD + 'DejaVuSans-Bold.ttf', FD + 'DejaVuSans.ttf'
W, H = 2560, 1440
INK, RED, GREEN, GREY, BLUE = (31, 41, 55), (183, 28, 28), (27, 127, 59), (110, 120, 138), (29, 78, 216)
WHITE, LIGHT, PANEL = (255, 255, 255), (241, 245, 249), (250, 251, 253)
DONE, DONEFILL = (160, 167, 178), (244, 246, 248)
GREENFILL, REDFILL, BLUEFILL = (221, 240, 227), (251, 228, 228), (219, 234, 254)
BOLTFILL, LIDFILL, GLASS = (205, 212, 222), (253, 230, 200), (214, 232, 246)
MARK = (232, 89, 12)
MIN_PX = 44
PROBLEMS = []
LOG = {}                                          # card name -> [(text, px)] in drawing order
CUR = []

# --- the numbers (tested against the script) -------------------------------------------------------------------------
M8 = (8, 1.25)                                    # size, pitch
TOOTH = 0.68                                      # tooth height in the message: about half a pitch
HOLE_M8 = round(M8[0] - M8[1], 2)                 # 6.75
M5 = (5, 0.8)
ROWS = [(h, f'{h - HOLE_M8:+.2f}', r) for h, r in ((6.3, 'refused'), (6.5, 'built'), (7.6, 'built'),
                                                    (7.7, 'refused'))]
FIFTH = ('8 for M10', '-0.5 vs 8.5', '?')         # greyed, asked, never answered
PPM = 400                                         # card-pitch: px per mm
PITCH_PX, TOOTH_PX = round(M8[1] * PPM), round(TOOTH * PPM)
HEAD_LID = 'A jar and its lid'
LEFT = 1300                                       # overlays: nothing left of this


# --- drawing helpers (as draw_fx7alt.py) -----------------------------------------------------------------------------
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
    if bb[0] < 0 or bb[2] > W or bb[1] < 0 or bb[3] > H:
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
        return {'ink': INK, 'acc': accent, 'fill': WHITE, 'on': True}
    return {'ink': DONE, 'acc': DONE, 'fill': DONEFILL, 'on': False}


def tint(col, p):
    return col if p['on'] else DONEFILL


def callout(d, box, lines, p, size=52, accents=()):
    d.rounded_rectangle(box, radius=22, fill=p['fill'], outline=p['ink'], width=5)
    cx, n = (box[0] + box[2]) / 2, len(lines)
    cy0 = (box[1] + box[3]) / 2 - (n - 1) * size * 0.6
    for i, ln in enumerate(lines):
        text(d, (cx, cy0 + i * size * 1.2), ln, size, p['acc'] if i in accents else p['ink'], anchor='mm',
             box=box)


def dashed(d, a, b, col, width=4, dash=18):
    (x0, y0), (x1, y1) = a, b
    n = max(1, int(math.hypot(x1 - x0, y1 - y0) // dash))
    for i in range(0, n, 2):
        t0, t1 = i / n, min(1, (i + 1) / n)
        d.line((x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0, x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1), fill=col,
               width=width)


def arrowhead(d, tip, ux, uy, col, size=26):
    vx, vy = -uy, ux
    d.polygon([tip, (tip[0] - ux * size + vx * size * 0.45, tip[1] - uy * size + vy * size * 0.45),
               (tip[0] - ux * size - vx * size * 0.45, tip[1] - uy * size - vy * size * 0.45)], fill=col)


def dimline(d, a, b, col, width=6):
    """A dimension line a-b with arrowheads at both ends, pointing outward."""
    d.line((a, b), fill=col, width=width)
    ux, uy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(ux, uy)
    ux, uy = ux / n, uy / n
    arrowhead(d, b, ux, uy, col)
    arrowhead(d, a, -ux, -uy, col)


# --- the thread profile (a bolt half-width along its axis; the nut follows it with a small clearance) ---------------
RI, RO, P, CL = 170, 250, 120, 14               # local units: root, tip, pitch, clearance
WALL = RO + CL + 120                            # the nut's outer wall
SEC = (30, 750)                                 # the section's top and bottom (local v)


def rb(v, top=SEC[0]):
    t = ((v - top) / P) % 1
    tri = max(0.0, 1 - abs(t - 0.5) / 0.42)
    return RI + (RO - RI) * min(1.0, tri * 1.25)


# --- card 1 (F3) and card 4 (F8): the jar and its lid -----------------------------------------------------------------
CU = 1200                                       # the section's axis (local u)


def draw_lid(d, ox, oy, s, upto, pals):
    """The F3 picture: 1 a jar and its lid; 2 the lid cut in half on the jar; 3 bolt and nut, two dimension lines.
    Local units (u, v) map to X = ox + u * s, Y = oy + v * s; text sizes stay fixed."""
    X, Y = (lambda u: ox + u * s), (lambda v: oy + v * s)  # noqa: E731
    p = pals[0]                                  # 1: jar and lid side by side
    d.rectangle((X(-20), Y(180), X(200), Y(310)), fill=tint(GLASS, p), outline=p['ink'], width=6)
    for i in range(3):                           # the jar's thread
        d.line((X(-20), Y(212 + i * 34), X(200), Y(196 + i * 34)), fill=p['ink'], width=5)
    d.rounded_rectangle((X(-60), Y(300), X(240), Y(800)), radius=round(40 * s), fill=tint(GLASS, p),
                        outline=p['ink'], width=6)
    d.rounded_rectangle((X(300), Y(420), X(540), Y(540)), radius=round(18 * s), fill=tint(LIDFILL, p),
                        outline=p['ink'], width=6)
    for u in range(330, 540, 30):                # the lid's grip
        d.line((X(u), Y(440), X(u), Y(520)), fill=p['ink'], width=3)
    text(d, (X(90), Y(830)), 'jar', 56, p['ink'], anchor='mt')
    text(d, (X(420), Y(570)), 'lid', 56, p['ink'], anchor='mt')
    if upto < 2:
        return
    p = pals[1]                                  # 2: the lid cut in half, its ridges between the jar's ridges
    vs = [SEC[0] + i * 2 for i in range((SEC[1] - SEC[0]) // 2 + 1)]
    bolt = [(X(CU + rb(v)), Y(v)) for v in vs] + [(X(CU - rb(v)), Y(v)) for v in reversed(vs)]
    d.polygon(bolt, fill=tint(BOLTFILL, p), outline=p['ink'], width=5)
    for sg in (1, -1):
        nut = [(X(CU + sg * (rb(v) + CL)), Y(v)) for v in vs] + [(X(CU + sg * WALL), Y(SEC[1])),
                                                                 (X(CU + sg * WALL), Y(SEC[0]))]
        d.polygon(nut, fill=tint(LIDFILL, p), outline=p['ink'], width=5)
        dashed(d, (X(CU + sg * (RI + CL)), Y(SEC[0]) - 20), (X(CU + sg * (RI + CL)), Y(SEC[1]) + 20), p['acc'], 6)
    bx = X(CU + WALL) + 40
    by = Y(SEC[0] + 2 * P)                       # a nut ridge tip
    callout(d, (bx, by - 125, bx + 690, by - 15), ['ridge tips = the hole'], p, 52, accents=(0,))
    d.line((bx, by - 70, X(CU + RI + CL) + 8, by), fill=p['acc'], width=6)
    d.ellipse((X(CU + RI + CL) - 10, by - 10, X(CU + RI + CL) + 10, by + 10), fill=p['acc'])
    if upto < 3:
        return
    p = pals[2]                                  # 3: bolt and nut, two dimension lines
    text(d, (X(CU), Y(390)), 'bolt', 56, p['ink'], anchor='mm')
    text(d, (X(CU - WALL) - 20, Y(390)), 'nut', 56, p['ink'], anchor='rm')
    sb = Y(SEC[1])
    blue, mark = (BLUE, MARK) if p['on'] else (DONE, DONE)
    for sg in (1, -1):
        d.line((X(CU + sg * RO), Y(SEC[1] - 40), X(CU + sg * RO), sb + 80), fill=blue, width=3)
        for e0, e1 in ((20, 88), (162, 215)):     # broken where the first label runs
            d.line((X(CU + sg * (RI + CL)), sb + e0, X(CU + sg * (RI + CL)), sb + e1), fill=mark, width=3)
    dimline(d, (X(CU - RO), sb + 60), (X(CU + RO), sb + 60), blue)
    text(d, (X(CU), sb + 125), "8 = outside of the bolt's teeth", 54, blue, anchor='mm')
    dimline(d, (X(CU - RI - CL), sb + 195), (X(CU + RI + CL), sb + 195), mark)
    text(d, (X(CU), sb + 260), "hole = tips of the nut's ridges: smaller", 54, mark, anchor='mm')


def card_lid(step):
    im, d = canvas(); header(d, HEAD_LID)
    draw_lid(d, 180, 200, 1.0, step, [pal(1, step), pal(2, step, MARK), pal(3, step)])
    save(im, f'card-lid-{step}.png')


# --- card 2 (F4): grooves carved outward (overlay, right half) --------------------------------------------------------
CUTP = (1310, 150, 2530, 1290)
K = 1.4                                          # local units to px
XH = 1480                                        # the hole wall at the tooth tips
XO = XH + round((RO - RI) * K)                   # the 8 mm line


def card_cut(step):
    im, d = overlay(CUTP)
    a = (lambda col: col + (255,))               # noqa: E731
    bx, cx = CUTP, (CUTP[0] + CUTP[2]) / 2
    text(d, (cx, 225), 'Carving the nut', 68, INK, anchor='mm', box=bx)
    p = pal(1, step, BLUE)                       # 1: grooves carved outward from the hole wall to the 8 mm line
    y0, y1 = 360, 360 + round(2.5 * P * K)
    vs = [SEC[0] + i * 2 for i in range(round((y1 - y0) / K / 2) + 1)]
    prof = [(XH + (rb(v) - RI) * K, y0 + (v - SEC[0]) * K) for v in vs]
    d.polygon(prof + [(2440, y1), (2440, y0)], fill=a(tint(LIDFILL, p)), outline=a(p['ink']), width=5)
    d.polygon(prof + [(XH, y1), (XH, y0)], fill=a(BLUEFILL if p['on'] else DONEFILL), outline=a(p['acc']), width=4)
    dashed(d, (XO, y0 - 30), (XO, y1 + 20), a(p['ink']), 5)
    text(d, (XO + 20, 305), '8 mm line', 50, p['ink'], anchor='lm', box=bx)
    text(d, ((CUTP[0] + XH) / 2, (y0 + y1) / 2), 'hole', 48, p['ink'], anchor='mm', box=bx)
    text(d, (cx, 835), 'grooves = the gaps between teeth', 52, p['acc'], anchor='mm', box=bx, maxw=1180)
    if step >= 2:                                # 2: an 8 mm hole: the wall is already on the line, zero depth
        p = pal(2, step, RED)
        z0, z1 = 930, 1110
        d.rectangle((XO, z0, 2440, z1), fill=a(LIDFILL), outline=a(INK), width=5)
        d.line((XO, z0 - 25, XO, z1 + 25), fill=a(RED), width=12)
        text(d, ((CUTP[0] + XO) / 2, (z0 + z1) / 2), 'hole', 48, INK, anchor='mm', box=bx)
        text(d, ((XO + 2440) / 2, (z0 + z1) / 2), '0.00 mm to cut', 64, RED, anchor='mm', box=bx)
        text(d, (cx, 1190), '8 mm hole: wall already at 8 mm', 52, INK, anchor='mm', box=bx, maxw=1180)
    save(im, f'card-cut-{step}.png')


# --- card 3 (F5): pitch and tooth height ------------------------------------------------------------------------------
BASE = 700                                       # the bolt surface (y)
TEETH = (420, 420 + PITCH_PX)                    # tooth centres (x)
HALF_BASE, HALF_CREST = round(0.425 * PPM), round(0.08 * PPM)
BAR = (200, 2360, 960, 1050)                     # the hole across: x0, x1 (8 mm), y0, y1
BPPM = (BAR[1] - BAR[0]) / M8[0]
PITCH_GEOM = {}                                  # x spans drawn on the bar (tested)


def card_pitch(step):
    im, d = canvas(); header(d, 'How much smaller?')
    p = pal(1, step, BLUE)                       # 1: two teeth, pitch, tooth height
    crest = BASE - TOOTH_PX
    pts = [(140, BASE + 120), (140, BASE)]
    for c in TEETH:
        pts += [(c - HALF_BASE, BASE), (c - HALF_CREST, crest), (c + HALF_CREST, crest), (c + HALF_BASE, BASE)]
    pts += [(1200, BASE), (1200, BASE + 120)]
    d.polygon(pts, fill=tint(BOLTFILL, p), outline=p['ink'], width=6)
    for c in TEETH:
        dashed(d, (c, crest - 10), (c, 330), p['acc'], 4)
    dimline(d, (TEETH[0], 360), (TEETH[1], 360), p['acc'])
    text(d, ((TEETH[0] + TEETH[1]) / 2, 290), 'pitch = 1.25 mm for M8', 56, p['acc'], anchor='mm')
    hx = 1150
    dashed(d, (TEETH[1] + HALF_CREST + 10, crest), (hx + 20, crest), p['ink'], 4)
    dimline(d, (hx, crest), (hx, BASE), p['ink'])
    text(d, (hx + 50, (crest + BASE) / 2), 'about half a pitch: 0.68', 56, p['ink'], anchor='lm')
    if step >= 2:                                # 2: the hole loses about half a pitch on EACH side (cut 2: no sum)
        p = pal(2, step, RED)
        x0, x1, y0, y1 = BAR
        t = round(M8[1] / 2 * BPPM)              # each end drawn half a pitch wide: the middle is 6.75 to scale
        d.rectangle((x0, y0, x1, y1), fill=tint(LIGHT, p), outline=p['ink'], width=5)
        for a, b in ((x0, x0 + t), (x1 - t, x1)):
            d.rectangle((a, y0, b, y1), fill=tint(REDFILL, p), outline=p['acc'], width=5)
        for x in (x0, x1):                       # "8 mm" across the WHOLE bar, outside the hole
            d.line((x, y0 - 90, x, y0), fill=p['ink'], width=4)
        dimline(d, (x0, y0 - 60), (x1, y0 - 60), p['ink'])
        text(d, ((x0 + x1) / 2, y0 - 75), '8 mm', 52, p['ink'], anchor='mb')
        PITCH_GEOM['8 mm'] = (x0, x1)
        PITCH_GEOM['hole'] = (x0 + t, x1 - t)
        text(d, (W / 2, 1115), 'each end: about half a pitch tall', 52, p['ink'], anchor='mt')
        text(d, (W / 2, 1190), 'both ends: about one pitch across', 56, p['acc'], anchor='mt')
    if step >= 3:                                # 3: the hole, SolidCraft's rule
        p = pal(3, step, GREEN)
        a, b = PITCH_GEOM['hole']
        d.rectangle((a, BAR[2], b, BAR[3]), fill=GREENFILL, outline=GREEN, width=5)
        text(d, ((a + b) / 2, (BAR[2] + BAR[3]) / 2), 'hole: 6.75 mm', 56, GREEN, anchor='mm')
        callout(d, (1400, 170, 2480, 420), ['8 minus 1.25 = 6.75', 'SolidCraft: exactly one pitch'], p, 64,
                accents=(0,))
    save(im, f'card-pitch-{step}.png')


# --- card 4 (F8): so far: the same lid picture, then the window ----------------------------------------------------
WIN = (300, 2260, 1010, 1090, 6.0, 8.0)          # x0, x1, y0, y1, mm at x0, mm at x1


def wx(mm):
    x0, x1, _, _, a, b = WIN
    return x0 + (mm - a) / (b - a) * (x1 - x0)


def card_sofar(step):
    im, d = canvas(); header(d, 'So far')
    on = pal(1, step)
    draw_lid(d, 460, 150, 0.6, 3, [on, {**on, 'acc': MARK if on['on'] else DONE}, on])
    if step >= 2:                                # 2: the window bar and one line
        p = pal(2, step, GREEN)
        x0, x1, y0, y1, _, _ = WIN
        for a, b, fill in ((6.0, 6.3, REDFILL), (6.3, 6.5, LIGHT), (6.5, 7.6, GREENFILL), (7.6, 7.7, LIGHT),
                           (7.7, 8.0, REDFILL)):
            d.rectangle((wx(a), y0, wx(b), y1), fill=fill)
        d.rectangle((x0, y0, x1, y1), outline=INK, width=5)
        for mm, size in ((6.5, 52), (6.75, 60), (7.6, 52)):
            d.line((wx(mm), y0 - 10, wx(mm), y1 + 10), fill=GREEN, width=8 if mm == 6.75 else 5)
            text(d, (wx(mm), y0 - 18), f'{mm}', size, GREEN, anchor='mb')
        text(d, (x0, y1 + 18), 'too narrow', 52, RED, anchor='lt')
        text(d, ((wx(6.5) + wx(7.6)) / 2, y1 + 18), 'builds', 52, GREEN, anchor='mt')
        text(d, (x1, y1 + 18), 'cuts too little', 52, RED, anchor='rt')
        d.rounded_rectangle((520, 1240, 2040, 1370), radius=26, fill=LIGHT, outline=INK, width=6)
        text(d, (1280, 1305), 'SolidCraft: hole = size minus pitch', 64, INK, anchor='mm', maxw=1460)
    save(im, f'card-sofar-{step}.png')


# --- card 5 (F10): the question (overlay, right half; no answer on screen) --------------------------------------------
QUEST = (1310, 150, 2530, 1290)
COLS = (1520, 1900, 2300)


def card_question(step):
    im, d = overlay(QUEST)
    bx, cx = QUEST, (QUEST[0] + QUEST[2]) / 2
    text(d, (cx, 230), 'A question', 72, INK, anchor='mm', box=bx)
    for c, s in zip(COLS, ('hole', 'vs 6.75', 'result')):
        text(d, (c, 330), s, 52, GREY, anchor='mm', box=bx)
    d.line((QUEST[0] + 50, 372, QUEST[2] - 50, 372), fill=INK + (255,), width=4)
    for i, (h, diff, r) in enumerate(ROWS):
        y = 425 + i * 85
        text(d, (COLS[0], y), f'{h}', 52, INK, anchor='mm', box=bx)
        text(d, (COLS[1], y), diff, 52, INK, anchor='mm', box=bx)
        text(d, (COLS[2], y), r, 52, GREEN if r == 'built' else RED, anchor='mm', box=bx)
    y = 425 + 4 * 85 + 10
    d.rounded_rectangle((QUEST[0] + 40, y - 42, QUEST[2] - 40, y + 42), radius=16, fill=DONEFILL + (255,))
    for c, s in zip(COLS, FIFTH):
        text(d, (c, y), s, 52, DONE, anchor='mm', box=bx)
    text(d, (cx, 910), '8 mm hole. Message says M10.', 58, INK, anchor='mm', box=bx, maxw=1120)
    if step < 2:
        save(im, 'card-question-1.png')
        return
    text(d, (cx, 1005), 'M10 wants 8.5. Builds?', 66, INK, anchor='mm', box=bx)
    d.rounded_rectangle((QUEST[0] + 80, 1090, QUEST[2] - 80, 1220), radius=26, fill=GREENFILL, outline=GREEN, width=8)
    text(d, (cx, 1155), 'Pause and think', 72, GREEN, anchor='mm', box=bx)
    save(im, 'card-question-2.png')


# --- Short card (cut 2, MUST-FIX 4): the hole wall in cross-section, 1080 x 960 (the Short's view) ---------------------
SW, SHH = 1080, 960
SPPM = 80                                        # px per mm: 8 mm = 640 px
SCX = SW // 2
SHORT_GEOM = {}
HATCH = (190, 198, 210)


def wall_panel(d, y0, hole, p, title, foot, foot_col, grooves):
    """One cross-section panel: the nut wall on both sides of the hole, the 8 mm line dashed red."""
    l8, r8 = SCX - 4 * SPPM, SCX + 4 * SPPM
    li, ri = SCX - round(hole / 2 * SPPM), SCX + round(hole / 2 * SPPM)
    top, bot = y0 + 90, y0 + 330
    text(d, (SCX, y0 + 40), title, 50, p['ink'], anchor='mm', box=(0, 0, SW, SHH))
    for a, b in ((90, li), (ri, 990)):
        d.rectangle((a, top, b, bot), fill=tint(HATCH, p), outline=p['ink'], width=4)
    if grooves:                                  # V grooves cut from the hole wall out to the 8 line
        pitch = round(M8[1] * SPPM)
        yc = top + pitch // 2
        while yc + pitch // 2 <= bot:
            for edge, tip in ((li, l8), (ri, r8)):
                d.polygon([(edge, yc - pitch * 0.45), (tip, yc), (edge, yc + pitch * 0.45)], fill=WHITE,
                          outline=p['ink'])
            yc += pitch
    for x in (l8, r8):
        dashed(d, (x, top - 20), (x, bot + 20), RED if p['on'] else DONE, 5)
    my = (top + bot) // 2
    dimline(d, (li + 6, my), (ri - 6, my), p['acc'], 5)
    text(d, (SCX, my - 12), f'hole {hole:g} mm', 46, p['acc'], anchor='mb', box=(0, 0, SW, SHH))
    text(d, (SCX, bot + 50), foot, 48, foot_col if p['on'] else DONE, anchor='mm', box=(0, 0, SW, SHH))
    return (li, ri), (l8, r8)


def card_short_wall(step):
    CUR.clear()
    im = Image.new('RGB', (SW, SHH), WHITE)
    d = ImageDraw.Draw(im)
    p = pal(1, step, RED)
    SHORT_GEOM['wall8'], SHORT_GEOM['line8'] = wall_panel(d, 20, M8[0], p, 'hole 8: wall already at 8',
                                                          'nothing left to cut', RED, False)
    text(d, (SCX, 928), "red dashes: the bolt's outside, 8", 44, RED, anchor='mm', box=(0, 0, SW, SHH))
    if step >= 2:
        p = pal(2, step, GREEN)
        d.line((60, 478, SW - 60, 478), fill=DONE, width=3)
        SHORT_GEOM['wall675'], _ = wall_panel(d, 495, HOLE_M8, p, 'hole 6.75: grooves cut out to 8',
                                              'room to cut: real teeth', GREEN, True)
    save(im, f'card-short-wall-{step}.png')


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
    sh.save(os.path.join(outdir, 'cards-sheet.jpg'), quality=88)
    print('sheet', len(names))


def check_alpha():
    for n in sorted(os.listdir(OUT)):
        if n.startswith(('card-question', 'card-cut')):
            im = Image.open(os.path.join(OUT, n))
            bb = im.getchannel('A').getbbox()
            left = im.crop((0, 0, LEFT, H)).getchannel('A').getextrema()
            if im.mode != 'RGBA' or left != (0, 0) or bb[2] > 2541:
                PROBLEMS.append(f'{n}: alpha bbox {bb}, left {left}')


def main():
    os.makedirs(OUT, exist_ok=True)
    for s in (1, 2, 3):
        card_lid(s)
    for s in (1, 2):
        card_cut(s)
    for s in (1, 2, 3):
        card_pitch(s)
    for s in (1, 2):
        card_sofar(s)
    for s in (1, 2):
        card_question(s)
    for s in (1, 2):
        card_short_wall(s)
    check_alpha()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
        sys.exit(0)
    main()
