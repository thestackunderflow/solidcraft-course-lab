"""Fix-it fx10 cards (SolidCraft Revolve: "invalid input: the profile crosses the revolve axis"; draw only half), the
draw_fx9.py pattern: light, 2560 x 1440, line diagrams only (cartoon cap), each step adds, earlier steps stay and turn
grey. Text 44 px+, 44 columns at most per line.
  full frame (RGB):  card-wheel-1..3 (F3, the potter's wheel), card-sofar-1..2 (F8, the same wheel: the peg twice)
  side panels (RGBA): card-sides-1..2 (F4) and card-question-1..2 (F10), transparent left of x 1300;
                      card-radius-1..2 (F5), transparent left of x 1620
  source overlays (RGBA, 2880 x 1620, the take's own pixels; burnt into derived takes by footage-fx10.py):
      ov-axis-3d (take A 3D view: the axis Z through the origin, x 1675), ov-axis-sketch (the sketch / front view: the
      origin at x 1440), ov-tint-3d (the T's halves either side of the axis, from A/refusal.png's blue pixels),
      ov-tint-sketch (the same halves in the sketch view), ov-ext-c (take C: the helper line carried on upward,
      "endless"), ov-ring-dim (take C 85.5: the axis and the 5 mm gap), ov-inset (the upright 3D T from A/sketch.png,
      for the first upside-down sketch shot)
Facts (SCRIPT-fx10.md): Measure 30.00 across = 15 x 2 (R 15.00); the question's square sits 5 mm off the axis (asked,
never answered). The T's cap and stem sizes are never written (only 30 across was measured).
Run in the QA image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fx10.py [sheet OUTDIR]"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(LAB, 'video', 'frames-fx10')
TAKES = os.path.join(LAB, 'out', 'fx10')
FD = '/usr/share/fonts/truetype/dejavu/'
B, R = FD + 'DejaVuSans-Bold.ttf', FD + 'DejaVuSans.ttf'
W, H = 2560, 1440
SW, SH = 2880, 1620
INK, GREY = (31, 41, 55), (110, 120, 138)
WHITE, PANEL = (255, 255, 255), (250, 251, 253)
DONE, DONEFILL = (160, 167, 178), (244, 246, 248)
BLUE, BLUEFILL = (37, 99, 235), (219, 234, 254)
ORANGE, ORANGEFILL = (234, 88, 12), (255, 237, 213)
CLAY, CLAYLINE, CARD = (243, 222, 196), (150, 98, 52), (226, 232, 240)
MARK = (232, 89, 12)
MIN_PX = 44
PROBLEMS = []
LOG = {}
CUR = []

# --- the numbers (tested against the lab) ----------------------------------------------------------------------------
ACROSS, HALF = 30.0, 15.0          # Measure: 30.00 across the cap, R 15.00
OFF = 5                            # the question: the square sits 5 mm off the axis
AXIS_3D_X = 1675                   # take A 3D view: the origin (axis Z) at x 1675 (A/refusal.png, the stem's middle)
AXIS_SKETCH_X = 1440               # sketch / front view (A 70+, B 6-92): the origin at (1440, 426)
T_SKETCH = {'stem': (1222, 424, 1658, 967), 'cap': (901, 967, 1979, 1246)}   # the T in the sketch / front view
C_LINE_X, C_LINE_TOP = 1592, 935   # take C: the helper line, origin (1592, 1287) up to y ~935 (3D view)
RING_AXIS_X, RING_ORIGIN_Y = 1028, 860   # take C 85.5: the origin; the square's near edge at x ~1357
RING_EDGE_X, RING_EDGE_Y = 1354, 1058   # the square's bottom near corner (Z 0, X 5)
SIDES_X, RADIUS_X = 1300, 1620     # side panels: nothing left of these


# --- drawing helpers (as draw_fx9.py) --------------------------------------------------------------------------------
def font(p, s):
    return ImageFont.truetype(p, s)


def text(d, xy, s, size=64, fill=INK, path=B, anchor='la', maxw=None, box=None, frame=(W, H)):
    CUR.append((s, size))
    if size < MIN_PX:
        PROBLEMS.append(f'{s!r}: {size} px')
    f = font(path, size)
    d.text(xy, s, font=f, fill=fill, anchor=anchor)
    bb = d.textbbox(xy, s, font=f, anchor=anchor)
    if maxw and bb[2] - bb[0] > maxw:
        PROBLEMS.append(f'{s!r}: {bb[2] - bb[0]:.0f} px wide, max {maxw}')
    if bb[0] < 0 or bb[2] > frame[0] or bb[1] < 0 or bb[3] > frame[1]:
        PROBLEMS.append(f'{s!r}: off the frame {bb}')
    if box and (bb[0] < box[0] or bb[1] < box[1] or bb[2] > box[2] or bb[3] > box[3]):
        PROBLEMS.append(f'{s!r}: outside its panel {bb} vs {box}')
    if '<' in s or '>' in s:
        PROBLEMS.append(f'{s!r}: angle bracket')
    if len(s) > 44:
        PROBLEMS.append(f'{s!r}: {len(s)} columns, max 44')
    return bb


def boxed_text(d, xy, s, size, fill, anchor='mm', frame=(SW, SH)):
    """Text on a white rounded box (source overlays: readable over any footage)."""
    f = font(B, size)
    bb = d.textbbox(xy, s, font=f, anchor=anchor)
    d.rounded_rectangle((bb[0] - 18, bb[1] - 12, bb[2] + 18, bb[3] + 12), radius=14, fill=WHITE + (235,),
                        outline=fill + (255,), width=4)
    text(d, xy, s, size, fill + (255,), anchor=anchor, frame=frame)


def canvas():
    CUR.clear()
    im = Image.new('RGB', (W, H), WHITE)
    return im, ImageDraw.Draw(im)


def panel(box):
    CUR.clear()
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, radius=28, fill=PANEL + (255,), outline=INK + (255,), width=5)
    return im, d


def source():
    CUR.clear()
    im = Image.new('RGBA', (SW, SH), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def header(d, s):
    text(d, (W / 2, 100), s, 84, anchor='mm', maxw=2400)


def save(im, name):
    im.save(os.path.join(OUT, name))
    LOG[name] = list(CUR)
    print(name)


def pal(k, step):
    return {'ink': INK, 'on': True} if k == step else {'ink': DONE, 'on': False}


def dashed(d, a, b, col, width=5, dash=20):
    (x0, y0), (x1, y1) = a, b
    n = max(1, int(math.hypot(x1 - x0, y1 - y0) // dash))
    for i in range(0, n, 2):
        t0, t1 = i / n, min(1, (i + 1) / n)
        d.line((x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0, x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1), fill=col,
               width=width)


def arrowhead(d, tip, ux, uy, col, size=28):
    vx, vy = -uy, ux
    d.polygon([tip, (tip[0] - ux * size + vx * size * 0.45, tip[1] - uy * size + vy * size * 0.45),
               (tip[0] - ux * size - vx * size * 0.45, tip[1] - uy * size - vy * size * 0.45)], fill=col)


def dimline(d, a, b, col, width=6):
    d.line((a, b), fill=col, width=width)
    ux, uy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(ux, uy)
    ux, uy = ux / n, uy / n
    arrowhead(d, b, ux, uy, col)
    arrowhead(d, a, -ux, -uy, col)


def dashed_arc(d, box, a0, a1, col, width=5, step=9):
    for a in range(int(a0), int(a1), step * 2):
        d.arc(box, a, min(a + step, a1), fill=col, width=width)


# --- the potter's wheel (F3 and F8: the same picture, so the peg is seen twice) ---------------------------------------
def vase_r(v):
    """Half-width of the clay at height v (0 = on the wheel, 1 = the top)."""
    return 120 + 70 * math.sin(math.pi * (0.15 + 0.85 * v)) - 40 * v


def draw_wheel(d, cx, base, p, card=True):
    ink = p['ink']
    clay = CLAY if p['on'] else DONEFILL
    d.polygon([(cx - 120, base + 60), (cx + 120, base + 60), (cx + 180, base + 260), (cx - 180, base + 260)],
              fill=WHITE, outline=ink, width=5)                              # the stand
    d.ellipse((cx - 380, base - 50, cx + 380, base + 70), fill=WHITE, outline=ink, width=6)   # the wheel
    hgt = 520
    pts = [(cx + vase_r(i / 20), base - i / 20 * hgt) for i in range(21)]
    poly = pts + [(2 * cx - x, y) for x, y in reversed(pts)]
    d.polygon(poly, fill=clay, outline=ink if not p['on'] else CLAYLINE)
    d.line(poly + [poly[0]], fill=ink if not p['on'] else CLAYLINE, width=5)
    dashed(d, (cx, base + 90), (cx, base - hgt - 90), ink, width=5)       # the spindle
    if card:                                                                # the shaped card (a rib) on one side
        edge = [(x + 10, y) for x, y in pts]
        right = max(x for x, _ in edge) + 150
        d.polygon(edge + [(right, edge[-1][1]), (right, edge[0][1])], fill=CARD if p['on'] else DONEFILL,
                  outline=ink)
        d.line(edge, fill=BLUE if p['on'] else ink, width=8)
    return pts, hgt


def card_wheel(step):
    im, d = canvas()
    header(d, "A potter's wheel")
    p1 = pal(1, step)
    draw_wheel(d, 820, 1060, p1)
    text(d, (820, 1370), 'a shaped card against one side', 56, p1['ink'], anchor='mm')
    if step >= 2:
        p2 = pal(2, step)
        cx, base, hgt = 1900, 1060, 520
        pts = [(cx + vase_r(i / 20), base - i / 20 * hgt) for i in range(21)]
        ghost = [(2 * cx - x, y) for x, y in pts]
        dashed(d, (cx, base + 120), (cx, base - hgt - 120), p2['ink'], width=5)
        for a, b in zip(ghost, ghost[1:]):
            d.line((a, b), fill=GREY if p2['on'] else DONE, width=4)
        d.polygon([(cx, base)] + pts + [(cx, pts[-1][1])], fill=ORANGEFILL if p2['on'] else DONEFILL,
                  outline=ORANGE if p2['on'] else DONE)
        d.line([(cx, base)] + pts + [(cx, pts[-1][1])], fill=ORANGE if p2['on'] else DONE, width=7)
        dashed_arc(d, (cx - 300, base - 330, cx + 300, base - 170), 20, 340, BLUE if p2['on'] else DONE, width=6)
        arrowhead(d, (cx + 280, base - 210), 0.3, 0.95, BLUE if p2['on'] else DONE)
        text(d, (cx, 1370), 'the turning makes it round', 56, p2['ink'], anchor='mm')
    if step >= 3:
        p3 = pal(3, step)
        text(d, (2500, 330), 'card edge = profile', 60, ORANGE, anchor='rm')
        d.line((2060, 360, 2070, 560), fill=ORANGE, width=5)
        text(d, (1880, 1235), 'spindle = axis', 60, p3['ink'], anchor='rm')
        d.line((1890, 1220, 1900, 1150), fill=p3['ink'], width=5)
    save(im, f'card-wheel-{step}.png')


def card_sofar(step):
    im, d = canvas()
    header(d, 'So far')
    p1 = pal(1, step)
    draw_wheel(d, 820, 1060, p1)
    text(d, (820, 1370), 'shape one side, the turning does the rest', 50, p1['ink'], anchor='mm')
    if step >= 2:
        p2 = pal(2, step)
        cx = 1750
        dashed(d, (cx, 180), (cx, 1300), BLUE, width=6)
        text(d, (cx - 30, 230), 'axis', 56, BLUE, anchor='rm')
        half = [(cx, 420), (cx + 450, 420), (cx + 450, 660), (cx + 180, 660), (cx + 180, 1110), (cx, 1110)]
        d.polygon(half, fill=ORANGEFILL, outline=ORANGE)
        d.line(half + [half[0]], fill=ORANGE, width=7)
        text(d, (1750 + 225, 1220), 'one side of an endless line', 56, p2['ink'], anchor='mm')
        text(d, (cx + 230, 870), 'touching: fine', 52, p2['ink'], anchor='lm')
    save(im, f'card-sofar-{step}.png')


# --- F4: both sides (right panel) ------------------------------------------------------------------------------------
def card_sides(step):
    im, d = panel((SIDES_X, 120, 2540, 1320))
    p1 = pal(1, step)
    text(d, (1920, 200), 'one outline, one side of the axis', 60, p1['ink'], anchor='mm', maxw=1200)
    cx, top = 1920, 300
    cap, stem = (300, 160), (120, 300)                 # half-widths / heights in panel px (shape only, no sizes)
    left = [(cx, top), (cx - cap[0], top), (cx - cap[0], top + cap[1]), (cx - stem[0], top + cap[1]),
            (cx - stem[0], top + cap[1] + stem[1]), (cx, top + cap[1] + stem[1])]
    right = [(2 * cx - x, y) for x, y in left]
    on = p1['on']
    for poly, fill, line in ((left, BLUEFILL, BLUE), (right, ORANGEFILL, ORANGE)):
        d.polygon(poly, fill=(fill if on else DONEFILL) + (255,))
        d.line(poly, fill=(line if on else DONE) + (255,), width=7)
    dashed(d, (cx, top - 40), (cx, top + cap[1] + stem[1] + 60), (INK if on else DONE) + (255,), width=5)
    text(d, (cx - 60, top + 330), 'left half', 48, (BLUE if on else DONE) + (255,), anchor='rm')
    text(d, (cx + 60, top + 330), 'right half', 48, (ORANGE if on else DONE) + (255,), anchor='lm')
    if step >= 2:
        text(d, (1920, 900), 'seen from above, at 360 degrees', 56, INK + (255,), anchor='mm', maxw=1200)
        c1, cy, r = (1640, 1080, 110)
        d.ellipse((c1 - r, cy - r, c1 + r, cy + r), outline=ORANGE + (255,), width=12)
        dashed_arc(d, (c1 - r, cy - r, c1 + r, cy + r), 0, 360, BLUE + (255,), width=6, step=8)
        d.ellipse((c1 + r - 14, cy - 14, c1 + r + 14, cy + 14), fill=ORANGE + (255,))
        d.ellipse((c1 - r - 14, cy - 14, c1 - r + 14, cy + 14), fill=BLUE + (255,))
        text(d, (c1 + 170, cy), 'every ring twice', 48, INK + (255,), anchor='lm')
        c2 = 2330
        d.arc((c2 - r, cy - r, c2 + r, cy + r), 180, 360, fill=ORANGE + (255,), width=12)
        d.arc((c2 - r, cy - r, c2 + r, cy + r), 0, 180, fill=BLUE + (255,), width=12)
        text(d, (1920, 1265), 'at 180 degrees: no overlap, still refused', 48, INK + (255,), anchor='mm', maxw=1200)
    save(im, f'card-sides-{step}.png')


# --- F5: the radius (right panel) ------------------------------------------------------------------------------------
def card_radius(step):
    im, d = panel((RADIUS_X, 140, 2540, 1300))
    p1 = pal(1, step)
    on = p1['on']
    cx, top, s = 2080, 470, 20                         # 20 px per mm; only the 15 mm half-width is labelled
    capw, caph, stw, sth = HALF * s, 160, 120, 330
    half = [(cx, top), (cx + capw, top), (cx + capw, top + caph), (cx + stw, top + caph), (cx + stw, top + caph + sth),
            (cx, top + caph + sth)]
    d.polygon(half, fill=(ORANGEFILL if on else DONEFILL) + (255,))
    d.line(half + [half[0]], fill=(ORANGE if on else DONE) + (255,), width=7)
    dashed(d, (cx, top - 170), (cx, top + caph + sth + 70), (INK if on else DONE) + (255,), width=5)
    dimline(d, (cx, top - 60), (cx + capw, top - 60), (INK if on else DONE) + (255,))
    text(d, (cx + capw / 2, top - 130), 'half-width 15 mm', 52, (INK if on else DONE) + (255,), anchor='mm')
    text(d, (cx - 30, top + caph + sth + 40), 'axis', 48, (INK if on else DONE) + (255,), anchor='rm')
    if step >= 2:
        ghost = [(2 * cx - x, y) for x, y in half]
        for a, b in zip(ghost, ghost[1:]):
            dashed(d, a, b, GREY + (255,), width=4, dash=14)
        y = top + caph + sth + 150
        dimline(d, (cx - capw, y), (cx + capw, y), BLUE + (255,))
        text(d, (cx, y + 80), '15 x 2 = 30 mm across', 56, BLUE + (255,), anchor='mm', maxw=880)
    save(im, f'card-radius-{step}.png')


# --- F10: the question (right panel; asked, never answered) ----------------------------------------------------------
def card_question(step):
    im, d = panel((SIDES_X, 140, 2540, 1300))
    text(d, (1920, 240), 'Square 5 mm off the axis.', 64, (INK if step == 1 else DONE) + (255,), anchor='mm',
         maxw=1200)
    ax, s = 1640, 30
    dashed(d, (ax, 360), (ax, 920), BLUE + (255,), width=6)
    text(d, (ax - 30, 400), 'axis', 48, BLUE + (255,), anchor='rm')
    x0, x1 = ax + OFF * s, ax + OFF * s + 10 * s
    d.rectangle((x0, 480, x1, 780), fill=ORANGEFILL + (255,), outline=ORANGE + (255,), width=7)
    dimline(d, (ax, 850), (x0, 850), INK + (255,), width=5)
    text(d, ((ax + x0) / 2, 905), '5 mm', 48, INK + (255,), anchor='mt')
    if step >= 2:
        text(d, (1920, 1070), 'Revolve 360. What shape?', 64, INK + (255,), anchor='mm', maxw=1200)
        text(d, (1920, 1200), 'Pause and think', 60, BLUE + (255,), anchor='mm')
    save(im, f'card-question-{step}.png')


# --- source overlays (2880 x 1620, burnt into derived takes) ---------------------------------------------------------
def ov_axis(name, x, y0, y1, label, ly):
    im, d = source()
    dashed(d, (x, y0), (x, y1), ORANGE + (255,), width=7, dash=22)
    boxed_text(d, (x + 30, ly), label, 52, ORANGE, anchor='lm')
    save(im, name)
    return im


def blue_mask(png, box):
    """The selected T's pixels (SolidCraft's selection blue) inside box, from a lab screenshot."""
    src = Image.open(png).convert('RGB')
    m = Image.new('L', src.size, 0)
    px, mp = src.load(), m.load()
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            if b > 130 and r < 70 and g < 120:
                mp[x, y] = 255
    return m


def ov_tint_3d():
    im, d = source()
    m = blue_mask(os.path.join(TAKES, 'A', 'refusal.png'), (1150, 230, 2150, 1380))
    for col, xs in ((BLUE, (0, AXIS_3D_X)), (ORANGE, (AXIS_3D_X, SW))):
        half = Image.new('L', (SW, SH), 0)
        half.paste(m.crop((xs[0], 0, xs[1], SH)), (xs[0], 0))
        im.paste(Image.new('RGBA', (SW, SH), col + (165,)), (0, 0), half)
    d = ImageDraw.Draw(im)
    dashed(d, (AXIS_3D_X, 250), (AXIS_3D_X, 1400), WHITE + (255,), width=8, dash=22)
    boxed_text(d, (AXIS_3D_X + 30, 1440), 'both sides of the axis', 52, INK, anchor='lm')
    save(im, 'ov-tint-3d.png')


def ov_tint_sketch():
    im, d = source()
    x = AXIS_SKETCH_X
    for col, side in ((BLUE, 'l'), (ORANGE, 'r')):
        for (a, b, c, e) in T_SKETCH.values():
            box = (a, b, x, e) if side == 'l' else (x, b, c, e)
            d.rectangle(box, fill=col + (110,))
    dashed(d, (x, 330), (x, 1330), WHITE + (255,), width=8, dash=22)
    save(im, 'ov-tint-sketch.png')


def ov_ext_c():
    im, d = source()
    dashed(d, (C_LINE_X, C_LINE_TOP), (C_LINE_X, 160), ORANGE + (255,), width=7, dash=22)
    boxed_text(d, (C_LINE_X + 40, 760), 'endless', 56, ORANGE, anchor='lm')
    save(im, 'ov-ext-c.png')


def ov_ring_dim():
    im, d = source()
    dashed(d, (RING_AXIS_X, 200), (RING_AXIS_X, 1450), BLUE + (255,), width=7, dash=22)
    boxed_text(d, (RING_AXIS_X - 30, 260), 'axis Z', 52, BLUE, anchor='rm')
    a, b = (RING_AXIS_X, RING_ORIGIN_Y), (RING_EDGE_X, RING_EDGE_Y)    # along X (iso): origin to the near corner
    dimline(d, a, b, INK + (255,), width=6)
    boxed_text(d, ((a[0] + b[0]) / 2 - 20, (a[1] + b[1]) / 2 + 90), '5 mm', 56, INK, anchor='mm')
    save(im, 'ov-ring-dim.png')


def ov_inset():
    """The upright 3D T (take A, before the sketch was opened) as an inset left of the upside-down sketch view."""
    im, d = source()
    t = Image.open(os.path.join(TAKES, 'A', 'sketch.png')).convert('RGB').crop((1150, 230, 2150, 1330))
    t = t.resize((400, 440))
    x0, y0 = 450, 1010
    im.paste(t, (x0, y0))
    d = ImageDraw.Draw(im)
    d.rectangle((x0 - 4, y0 - 70, x0 + 404, y0 + 444), outline=INK + (255,), width=6)
    d.rectangle((x0, y0 - 66, x0 + 400, y0), fill=WHITE + (255,))
    text(d, (x0 + 200, y0 - 33), 'upright: cap on top', 46, INK + (255,), anchor='mm', frame=(SW, SH))
    d.line((x0 + 410, y0 + 200, 890, y0 + 160), fill=ORANGE + (255,), width=7)
    arrowhead(d, (895, y0 + 158), 1, -0.15, ORANGE + (255,), size=30)
    save(im, 'ov-inset.png')


def sheet(outdir):
    names = sorted(n for n in os.listdir(OUT) if n.startswith('card-'))
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
    sh.save(os.path.join(outdir, 'cards-sheet.jpg'), quality=85)
    # the source overlays on their frames
    pairs = [('ov-axis-3d.png', 'A/refusal.png'), ('ov-tint-3d.png', 'A/refusal.png'),
             ('ov-axis-sketch.png', 'B/full-sketch.png'), ('ov-inset.png', 'B/full-sketch.png'),
             ('ov-tint-sketch.png', 'A/split-dialog.png'), ('ov-ext-c.png', 'C/c2.png'),
             ('ov-ring-dim.png', 'C/s2-frame.png')]
    tw, th = 960, 540
    sh = Image.new('RGB', (tw * 2, th * 4), (90, 90, 90))
    for i, (ov, fr) in enumerate(pairs):
        base = Image.open(os.path.join(TAKES, fr)).convert('RGBA')
        o = Image.open(os.path.join(OUT, ov))
        t = Image.alpha_composite(base, o).convert('RGB').resize((tw, th))
        ImageDraw.Draw(t).text((8, 8), f'{ov} on {fr}', font=font(R, 24), fill=(200, 0, 0))
        sh.paste(t, ((i % 2) * tw, (i // 2) * th))
    sh.save(os.path.join(outdir, 'overlays-sheet.jpg'), quality=85)
    print('sheets', len(names), len(pairs))


def check_alpha():
    for n in sorted(os.listdir(OUT)):
        for pre, x in (('card-sides', SIDES_X), ('card-question', SIDES_X), ('card-radius', RADIUS_X)):
            if n.startswith(pre):
                im = Image.open(os.path.join(OUT, n))
                if im.mode != 'RGBA' or im.crop((0, 0, x, H)).getchannel('A').getextrema() != (0, 0):
                    PROBLEMS.append(f'{n}: not transparent left of {x}')


def main():
    os.makedirs(OUT, exist_ok=True)
    PROBLEMS.clear()
    for s in (1, 2, 3):
        card_wheel(s)
    for s in (1, 2):
        card_sofar(s)
        card_sides(s)
        card_radius(s)
        card_question(s)
    ov_axis('ov-axis-3d.png', AXIS_3D_X, 230, 1420, 'axis Z', 270)
    ov_axis('ov-axis-sketch.png', AXIS_SKETCH_X, 300, 1400, 'axis', 1330)
    ov_tint_3d()
    ov_tint_sketch()
    ov_ext_c()
    ov_ring_dim()
    ov_inset()
    check_alpha()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        main()
        sheet(sys.argv[2])
        sys.exit(0)
    main()
