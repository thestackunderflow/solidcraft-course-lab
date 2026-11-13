"""Fix-it fx11 cards (SolidCraft Split Body: "the tool does not split the body"; a plane through the middle), the
draw_fx10.py pattern: light, 2560 x 1440, line diagrams only (cartoon cap), each step adds, earlier steps stay and turn
grey. Text 44 px+, 44 columns at most per line.
  full frame (RGB):  card-cake-1..3 (F3, the cake and a level knife), card-sofar-1..3 (F8, the same cake three times, a
                     real inset of C/above.png: the plane at 210), card-recipe-1..4 (F10, your turn, one line per clause)
  side panels (RGBA): card-floor-1..2 (F4) and card-question-1..2 (F10), transparent left of x 1300;
                      card-pieces-1..3 (F5, the section to scale), transparent left of x 1620
  source overlays (RGBA, 2880 x 1620; burnt into derived takes by footage-fx11.py):
      ov-xy-a (take A: the XY plane drawn larger at the tower's foot, "XY, drawn larger: the floor"), ov-xy-c (take C:
      the same sheet through the symmetric tower's middle), ov-s2 (take C 183-188: the 200 plane outlined "200: the
      top face", the 210 plane tagged small grey "210: earlier test"), ov-r1-mask (R1 from 23.5 s: Claude Code's greyed
      suggested prompt covered, and the cover says so)
  after-masked.png: runs/R1/after.png with only the title bar's "Update to 0.41.0" button painted over (bar colour).
Facts (SCRIPT-fx11.md, lab RESULTS-fx11.md): tower 40 across, 200 tall; bore 30 from the top down to 5 mm above the
bottom (the start file); split at 100: top 54,972.98, bottom 58,506.68, sum 113,479.66 mm3; block 20 x 20 x 80, plane
40, 16,000.00 mm3 each. The question (a plane at the top face, 200) is asked, never answered.
Run in the draw image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fx11.py [sheet OUTDIR]"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(LAB, 'video', 'frames-fx11')
TAKES = os.path.join(LAB, 'out', 'fx11')
FD = '/usr/share/fonts/truetype/dejavu/'
B, R = FD + 'DejaVuSans-Bold.ttf', FD + 'DejaVuSans.ttf'
W, H = 2560, 1440
SW, SH = 2880, 1620
INK, GREY = (31, 41, 55), (110, 120, 138)
WHITE, PANEL = (255, 255, 255), (250, 251, 253)
DONE, DONEFILL = (160, 167, 178), (244, 246, 248)
BLUE, BLUEFILL = (37, 99, 235), (219, 234, 254)
ORANGE, ORANGEFILL = (234, 88, 12), (255, 237, 213)
CAKE, CAKELINE, STEEL = (250, 226, 190), (150, 98, 52), (148, 163, 184)
MIN_PX = 44
PROBLEMS = []
LOG = {}
CUR = []

# --- the numbers (lab) -----------------------------------------------------------------------------------------------
OUTER_D, TALL, BORE_D, BORE_FLOOR, CUT = 40, 200, 30, 5, 100
TOP_V, BOTTOM_V, WHOLE_V = '54,972.98', '58,506.68', '113,479.66'
BLOCK_V = '16,000.00'
FOOT_A = (1675, 1329)               # take A (iso home view): the origin dot at the tower's foot
MID_C = (1675, 865)                 # take C (symmetric tower): the origin dot at its middle
DIA = (198, 117)                    # an iso plane's half-width / half-height at the tower (s2-frame.png)
PLANE200, PLANE210 = (1675, 398), (1675, 352)   # take C 183+: the planes' centres (s2-frame.png)
UPDATE_BTN = (1866, 4, 264, 56)     # after.png: "Update to 0.41.0" (x 1876-2119, y 10-52)
BAR = (43, 47, 58)                  # the title bar's colour beside the button (sampled in mask_after)
R1_SUGGEST = (0, 1488, 2880, 72)    # R1 from ~23.5: the greyed suggested prompt row (y 1505-1545)
SIDES_X, PIECES_X = 1300, 1620


# --- drawing helpers (draw_fx10.py) ----------------------------------------------------------------------------------
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


def boxed_text(d, xy, s, size, fill, anchor='mm', frame=(SW, SH), edge=None):
    f = font(B, size)
    bb = d.textbbox(xy, s, font=f, anchor=anchor)
    d.rounded_rectangle((bb[0] - 18, bb[1] - 12, bb[2] + 18, bb[3] + 12), radius=14, fill=WHITE + (235,),
                        outline=(edge or fill) + (255,), width=4)
    return text(d, xy, s, size, fill + (255,), anchor=anchor, frame=frame)


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


def on(k, step):
    return k == step


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


# --- the cake (F3 and F8: the same picture, so the peg is seen twice) -------------------------------------------------
def cake(d, x0, x1, top, base, lit, cut=None):
    """A side view: plate, cake (two-tone when cut), the knife drawn by knife()."""
    ink = INK if lit else DONE
    d.rounded_rectangle((x0 - 70, base, x1 + 70, base + 22), radius=10, fill=WHITE, outline=ink, width=5)   # plate
    if cut is None:
        d.rectangle((x0, top, x1, base), fill=CAKE if lit else DONEFILL, outline=CAKELINE if lit else DONE, width=6)
    else:
        d.rectangle((x0, top, x1, cut), fill=ORANGEFILL if lit else DONEFILL, outline=ORANGE if lit else DONE, width=6)
        d.rectangle((x0, cut, x1, base), fill=BLUEFILL if lit else DONEFILL, outline=BLUE if lit else DONE, width=6)


def knife(d, x0, x1, y, lit):
    col = INK if lit else DONE
    d.rectangle((x0, y - 7, x1, y + 7), fill=STEEL if lit else DONEFILL, outline=col, width=3)    # level blade
    d.rounded_rectangle((x1, y - 18, x1 + 150, y + 18), radius=12, fill=col)                         # handle


def card_cake(step):
    im, d = canvas()
    header(d, 'Cutting a cake into two layers')
    # build 1-2: the knife flat on the plate, under the cake
    l1 = step <= 2
    cake(d, 300, 1050, 520, 1050, l1)
    knife(d, 220, 1130, 1062, l1)
    text(d, (675, 1180), 'knife under the cake:', 56, INK if l1 else DONE, anchor='mm')
    if step >= 2:
        text(d, (675, 1260), 'nothing cut: the whole', 56, INK if l1 else DONE, anchor='mm')
        text(d, (675, 1335), 'cake is above', 56, INK if l1 else DONE, anchor='mm')
    if step >= 3:
        cake(d, 1450, 2200, 520, 1050, True, cut=785)
        knife(d, 1370, 2280, 785, True)
        text(d, (1825, 1180), 'knife level, halfway up:', 56, INK, anchor='mm')
        text(d, (1825, 1260), 'two layers', 56, INK, anchor='mm')
    if step >= 4:
        text(d, (1825, 380), 'a layer on each side of the blade', 56, ORANGE, anchor='mm')
        text(d, (1825, 1345), 'knife = splitting plane', 60, BLUE, anchor='mm')
    save(im, f'card-cake-{step}.png')


def card_sofar(step):
    im, d = canvas()
    header(d, 'So far')
    cols = ((140, 640), (970, 1470), (1800, 2300))
    a = cols[0]
    l1 = on(1, step)
    cake(d, a[0], a[1], 560, 960, l1)
    knife(d, a[0] - 60, a[1] + 60, 972, l1)
    text(d, ((a[0] + a[1]) / 2, 1070), 'under the part: 1 piece', 52, INK if l1 else DONE, anchor='mm')
    if step >= 2:
        b = cols[1]
        l2 = on(2, step)
        l2 = step == 2
        cake(d, b[0], b[1], 560, 960, l2)
        knife(d, b[0] - 60, b[1] + 60, 500, l2)
        text(d, ((b[0] + b[1]) / 2, 1070), 'above the top: 1 piece', 52, INK if l2 else DONE, anchor='mm')
        ins = Image.open(os.path.join(TAKES, 'C', 'above.png')).convert('RGB').crop((1400, 150, 2880, 980))
        ins = ins.resize((560, 314))
        x0, y0 = b[0] - 30, 170
        im.paste(ins, (x0, y0))
        d.rectangle((x0 - 4, y0 - 4, x0 + 564, y0 + 318), outline=INK if l2 else DONE, width=5)
        text(d, ((b[0] + b[1]) / 2, 1150), 'real: plane at 210, above', 48, INK if l2 else DONE, anchor='mm')
        text(d, ((b[0] + b[1]) / 2, 1215), 'the top: the same line', 48, INK if l2 else DONE, anchor='mm')
    if step >= 3:
        c = cols[2]
        cake(d, c[0], c[1], 560, 960, True, cut=760)
        knife(d, c[0] - 60, c[1] + 60, 760, True)
        text(d, ((c[0] + c[1]) / 2, 1070), 'through it: 2 layers', 52, INK, anchor='mm')
        text(d, (W / 2, 1310), 'the plane must pass through the part', 64, BLUE, anchor='mm')
    if step >= 4:
        text(d, (W / 2, 1395), 'crosses and still refused? check the body', 48, ORANGE, anchor='mm')
    save(im, f'card-sofar-{step}.png')


# --- F4: the floor (right panel) -------------------------------------------------------------------------------------
def card_floor(step):
    im, d = panel((SIDES_X, 120, 2540, 1320))
    l1 = on(1, step)
    ink = (INK if l1 else DONE) + (255,)
    x0, x1, top, base = 1780, 1960, 260, 960
    d.rectangle((x0, top, x1, base), fill=(BLUEFILL if l1 else DONEFILL) + (255,), outline=(BLUE if l1 else DONE) + (255,),
                width=6)
    d.line((1450, base, 2400, base), fill=(ORANGE if l1 else DONE) + (255,), width=8)
    text(d, (2000, base + 50), 'XY', 52, (ORANGE if l1 else DONE) + (255,), anchor='lm')
    text(d, (1990, 420), 'above XY:', 52, ink, anchor='lm')
    text(d, (1990, 485), 'the whole', 52, ink, anchor='lm')
    text(d, (1990, 550), 'tower', 52, ink, anchor='lm')
    text(d, (1920, 1090), 'below XY: nothing', 52, ink, anchor='mm')
    if step >= 2:
        text(d, (1920, 1190), 'pieces: 1. A split needs 2.', 56, ORANGE + (255,), anchor='mm', maxw=1180)
    save(im, f'card-floor-{step}.png')


# --- F5: the pieces, the section to scale (right panel) --------------------------------------------------------------
def card_pieces(step):
    im, d = panel((PIECES_X, 140, 2540, 1300))
    s = 3.0                                   # px per mm
    cx, base = 1800, 860                      # the tower's axis, its bottom (z 0)
    top = base - TALL * s
    cut = base - CUT * s
    ro, rb = OUTER_D / 2 * s, BORE_D / 2 * s
    l1 = on(1, step)
    ink = (INK if l1 else DONE) + (255,)
    for y0, y1, col in ((top, cut, ORANGE), (cut, base, BLUE)):
        d.rectangle((cx - ro, y0, cx + ro, y1), fill=WHITE + (255,), outline=((col if l1 else DONE) + (255,)), width=6)
    d.line((cx - ro - 40, cut, cx + ro + 40, cut), fill=ink, width=5)
    dimline(d, (cx + ro + 40, top), (cx + ro + 40, cut), ink, width=4)
    dimline(d, (cx + ro + 40, cut), (cx + ro + 40, base), ink, width=4)
    text(d, (cx - ro - 18, (top + cut) / 2), '100', 48, ink, anchor='rm')
    text(d, (cx - ro - 18, (cut + base) / 2), '100', 48, ink, anchor='rm')
    text(d, (2080, 210), 'both 100 tall', 56, ink, anchor='mm', box=(PIECES_X, 140, 2540, 1300))
    if step >= 2:
        l2 = on(2, step)
        k = (INK if l2 else DONE) + (255,)
        floor_y = base - BORE_FLOOR * s
        # the cut faces of the wall either side of the bore (section), bore from the top down to 5 above the bottom
        for y0, y1, col in ((top, cut, ORANGEFILL), (cut, floor_y, BLUEFILL)):
            d.rectangle((cx - ro + 3, y0 + 3, cx - rb, y1), fill=(col if l2 else DONEFILL) + (255,))
            d.rectangle((cx + rb, y0 + 3, cx + ro - 3, y1), fill=(col if l2 else DONEFILL) + (255,))
        d.rectangle((cx - ro + 3, floor_y, cx + ro - 3, base - 3), fill=((BLUE if l2 else DONE) + (255,)))   # the floor
        d.line((cx - rb, top, cx - rb, floor_y), fill=k, width=4)
        d.line((cx + rb, top, cx + rb, floor_y), fill=k, width=4)
        d.line((cx - rb, floor_y, cx + rb, floor_y), fill=k, width=4)
        tx = 1990
        text(d, (tx, 420), 'top: smaller', 48, (ORANGE if l2 else DONE) + (255,), anchor='lm')
        text(d, (tx, 480), 'volume, no floor', 48, (ORANGE if l2 else DONE) + (255,), anchor='lm')
        text(d, (tx, 700), 'bottom: a 5 mm', 48, (BLUE if l2 else DONE) + (255,), anchor='lm')
        text(d, (tx, 760), 'solid floor', 48, (BLUE if l2 else DONE) + (255,), anchor='lm')
        text(d, (tx, 300), 'bore 30, 200 to 5', 44, k, anchor='lm')
        text(d, (tx, 900), 'sizes from', 44, (GREY if l2 else DONE) + (255,), anchor='lm')
        text(d, (tx, 950), 'the start file', 44, (GREY if l2 else DONE) + (255,), anchor='lm')
    if step >= 3:
        text(d, (2080, 1030), f'{BOTTOM_V} + {TOP_V}', 52, INK + (255,), anchor='mm', maxw=880)
        text(d, (2080, 1100), f'= {WHOLE_V} mm3', 56, BLUE + (255,), anchor='mm', maxw=880)
        text(d, (2080, 1170), '= the whole tower', 52, INK + (255,), anchor='mm', maxw=880)
        text(d, (2080, 1235), '(read before the split)', 44, GREY + (255,), anchor='mm', maxw=880)
    save(im, f'card-pieces-{step}.png')


# --- F10: the question (right panel; asked, never answered) ----------------------------------------------------------
def card_question(step):
    im, d = panel((SIDES_X, 140, 2540, 1300))
    k1 = (INK if step == 1 else DONE) + (255,)
    text(d, (1920, 330), 'Plane at the top face,', 64, k1, anchor='mm', maxw=1180)
    text(d, (1920, 420), '200 up.', 64, k1, anchor='mm', maxw=1180)
    x0, x1, top, base = 1830, 2010, 560, 1000
    d.rectangle((x0, top, x1, base), fill=BLUEFILL + (255,), outline=BLUE + (255,), width=6)
    d.line((1650, top, 2190, top), fill=ORANGE + (255,), width=8)
    text(d, (2200, top), '200', 48, ORANGE + (255,), anchor='lm')
    if step >= 2:
        text(d, (1920, 1100), 'Split or refused?', 72, INK + (255,), anchor='mm', maxw=1180)
        text(d, (1920, 1215), 'Pause and think', 60, BLUE + (255,), anchor='mm')
    save(im, f'card-question-{step}.png')


# --- F10: your turn, the recipe (full frame; the block's build was NOT filmed) ----------------------------------------
RECIPE = ['1. Sketch a 20 x 20 square on XY', '2. Extrude it 80 (pull it up)', '3. Offset Plane 40, Split Body',
          f'4. Properties: {BLOCK_V} mm3 each?']
RECIPE_STEPS = (2, 3, 4)          # step 1 = lines 1-2 (one spoken sentence), then one line per step


def card_recipe(step):
    im, d = canvas()
    header(d, 'Your turn: a block')
    n = RECIPE_STEPS[step - 1]
    newest = range(RECIPE_STEPS[step - 2] if step > 1 else 0, n)
    for i in range(n):
        text(d, (180, 330 + i * 140), RECIPE[i], 64, INK if i in newest else DONE, maxw=1500)
    text(d, (180, 1330), 'new to this? SolidCraft course, lesson 1', 44, GREY)
    # the block, building with the lines (side view, to scale 9 px/mm)
    s, cx, base = 9, 2060, 1180
    hw = 10 * s
    d.line((cx - 260, base, cx + 260, base), fill=ORANGE if step == 1 else DONE, width=6)
    d.rectangle((cx - hw, base - 80 * s, cx + hw, base), fill=BLUEFILL if step == 1 else DONEFILL,
                outline=BLUE if step == 1 else DONE, width=6)
    if step >= 2:
        y = base - 40 * s
        d.line((cx - 220, y, cx + 220, y), fill=ORANGE, width=8)
        text(d, (cx + 230, y), '40', 48, ORANGE, anchor='lm')
    if step >= 3:
        dimline(d, (cx - hw - 60, base - 80 * s), (cx - hw - 60, base - 40 * s), INK, width=4)
        dimline(d, (cx - hw - 60, base - 40 * s), (cx - hw - 60, base), INK, width=4)
    save(im, f'card-recipe-{step}.png')


# --- source overlays (2880 x 1620, burnt into derived takes) ---------------------------------------------------------
def diamond(c, hw, hh):
    x, y = c
    return [(x - hw, y), (x, y - hh), (x + hw, y), (x, y + hh)]


def ov_xy(name, c, label, side='right'):
    im, d = source()
    pts = diamond(c, 300, 172)
    d.polygon(pts, fill=ORANGE + (40,))
    for a, b in zip(pts, pts[1:] + pts[:1]):
        dashed(d, a, b, ORANGE + (255,), width=7, dash=22)
    if side == 'right':
        boxed_text(d, (c[0] + 340, c[1]), label, 52, ORANGE, anchor='lm')
    else:
        boxed_text(d, (c[0] - 340, c[1]), label, 52, ORANGE, anchor='rm')
    save(im, name)


def ov_s2():
    im, d = source()
    pts = diamond(PLANE200, *DIA)
    d.line(pts + pts[:1], fill=ORANGE + (255,), width=8)
    boxed_text(d, (PLANE200[0] + DIA[0] + 40, PLANE200[1] + 60), '200: the top face', 52, ORANGE, anchor='lm')
    boxed_text(d, (PLANE210[0] + DIA[0] + 40, PLANE210[1] - 70), '210: earlier test', 44, GREY, anchor='lm',
               edge=DONE)
    save(im, 'ov-s2.png')


def ov_r1_mask():
    im, d = source()
    x, y, w, h = R1_SUGGEST
    d.rectangle((x, y, x + w, y + h), fill=WHITE + (255,))
    text(d, (40, y + h / 2), "(Claude Code's greyed suggestion, hidden)", 44, GREY + (255,), anchor='lm', frame=(SW, SH))
    save(im, 'ov-r1-mask.png')


def mask_after():
    CUR.clear()
    im = Image.open(os.path.join(TAKES, 'runs', 'R1', 'after.png')).convert('RGB')
    x, y, w, h = UPDATE_BTN
    bar = im.getpixel((x - 20, 30))
    ImageDraw.Draw(im).rectangle((x, y, x + w - 1, y + h - 1), fill=bar)
    save(im, 'after-masked.png')


def short_split():
    """The Short's frame 1 (1080 x 960, two real frames stacked): A's refusal (the line, OK greyed) over B's two
    bodies (the plane at 100). Real pixels, cropped and scaled only; the labels sit on white bars, off the pixels."""
    CUR.clear()
    im = Image.new('RGB', (1080, 960), WHITE)
    d = ImageDraw.Draw(im)
    for k, (png, box, lab, col) in enumerate((
            ('A/refusal.png', (720, 200, 2880, 1160), 'XY: REFUSED', (185, 28, 28)),
            ('B/browser.png', (0, 300, 2160, 1260), 'PLANE AT 100: 2 PIECES', BLUE))):
        y0 = k * 480
        fr = Image.open(os.path.join(TAKES, png)).convert('RGB').crop(box).resize((1080, 480), Image.LANCZOS)
        im.paste(fr, (0, y0))
        f = font(B, 52)
        bb = d.textbbox((540, y0 + 420), lab, font=f, anchor='mm')
        d.rectangle((bb[0] - 20, bb[1] - 10, bb[2] + 20, bb[3] + 10), fill=WHITE, outline=col, width=5)
        text(d, (540, y0 + 420), lab, 52, col, anchor='mm', frame=(1080, 960))
    d.line((0, 480, 1080, 480), fill=INK, width=6)
    save(im, 'short-split.png')


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
    pairs = [('ov-xy-a.png', 'A/refusal.png'), ('ov-xy-c.png', 'C/sym.png'), ('ov-s2.png', 'C/s2-frame.png'),
             ('ov-r1-mask.png', None)]
    tw, th = 960, 540
    sh = Image.new('RGB', (tw * 2, th * 3), (90, 90, 90))
    for i, (ov, fr) in enumerate(pairs):
        base = Image.open(os.path.join(TAKES, fr)).convert('RGBA') if fr else Image.new('RGBA', (SW, SH), (255,) * 4)
        t = Image.alpha_composite(base, Image.open(os.path.join(OUT, ov))).convert('RGB').resize((tw, th))
        sh.paste(t, ((i % 2) * tw, (i // 2) * th))
    sh.paste(Image.open(os.path.join(OUT, 'after-masked.png')).convert('RGB').resize((tw, th)), (0, 2 * th))
    sh.save(os.path.join(outdir, 'overlays-sheet.jpg'), quality=85)


def check_alpha():
    for n in sorted(os.listdir(OUT)):
        for pre, x in (('card-floor', SIDES_X), ('card-question', SIDES_X), ('card-pieces', PIECES_X)):
            if n.startswith(pre):
                im = Image.open(os.path.join(OUT, n))
                if im.mode != 'RGBA' or im.crop((0, 0, x, H)).getchannel('A').getextrema() != (0, 0):
                    PROBLEMS.append(f'{n}: not transparent left of {x}')


def main():
    os.makedirs(OUT, exist_ok=True)
    PROBLEMS.clear()
    for s in (1, 2, 3, 4):
        card_cake(s)
        card_sofar(s)
    for s in (1, 2, 3):
        card_pieces(s)
        card_recipe(s)
    for s in (1, 2):
        card_floor(s)
        card_question(s)
    ov_xy('ov-xy-a.png', FOOT_A, 'XY, drawn larger: the floor')
    ov_xy('ov-xy-c.png', MID_C, 'XY, drawn larger', side='left')
    ov_s2()
    ov_r1_mask()
    mask_after()
    short_split()
    check_alpha()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
