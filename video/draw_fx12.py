"""Fix-it fx12 cards (SolidCraft Offset: "its corners follow its source curves"; round the outline first, or break the
link), the draw_fx11.py pattern (its helpers imported): light, 2560 x 1440, line diagrams only (cartoon cap), each step
adds, earlier steps stay and turn grey. Text 44 px+, 44 columns at most per line.
  full frame (RGB):  card-rails-1..3 (F3, a railway track: the same gap, the inner rail tighter, outer = the outline,
                     inner = the Offset copy), card-sofar-1..3 (F8), card-recipe-1 (F10: the rectangle is a card step,
                     never footage)
  side panels (RGBA, transparent left of DECODE_X / SIDES_X): card-decode-1..3 (F4), card-walls-1..2 (F6, the two
                     corners to scale), card-question-1..2 (F10, asked, never answered)
  source overlays (RGBA, 2880 x 1620; burnt into derived takes by footage-fx12.py):
      ov-wall-a (take A 9-14.5: the strip between the outline and the copy tinted), ov-qmm (take C 12-17: the Fillet
      Radius field covered "? mm"), ov-r1-mask (R1 from 31.5 s: only Claude Code's greyed suggested prompt covered,
      and the cover says so), ov-toollog (R1: the tool-log card, "from the tool log (not on its screen)", the 4th
      solidcraft call's reply word for word from runs/R1/tools.txt)
  after-masked.png: runs/R1/after.png with only the title bar's "Update to 0.41.0" button painted over.
  short-stack.png: the Short's frame 1 (1080 x 960): A's refusal over C's round copy, real pixels, labels on bars.
Facts (SCRIPT-fx12.md rev 2, RESULTS-fx12.md): outline 60 x 40, wall 2; quick fix: inside R 3, corner wall 4.07,
7,834.61 mm3; round first: outline R 5, inside R 3.00, wall 2.00, 7,405.25 mm3; 429.36 apart. The question (outline
1.5, wall 2) is asked, never answered.
Run in the draw image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fx12.py [sheet OUTDIR]"""
import math
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import draw_fx11 as b  # noqa: E402

LAB = b.LAB
OUT = os.path.join(LAB, 'video', 'frames-fx12')
TAKES = os.path.join(LAB, 'out', 'fx12')
b.OUT = OUT
W, H, SW, SH = b.W, b.H, b.SW, b.SH
INK, GREY, WHITE, DONE, DONEFILL = b.INK, b.GREY, b.WHITE, b.DONE, b.DONEFILL
BLUE, BLUEFILL, ORANGE, ORANGEFILL = b.BLUE, b.BLUEFILL, b.ORANGE, b.ORANGEFILL
RED = (185, 28, 28)
text, boxed_text, canvas, panel, source, header, save = b.text, b.boxed_text, b.canvas, b.panel, b.source, b.header, b.save
PROBLEMS, LOG = b.PROBLEMS, b.LOG

V_FIX1, V_FIX2, V_DIFF = '7,834.61', '7,405.25', '429.36'
LINE_R1 = ('invalid parameters for `sketch.fillet`: `l5` is an offset, and its corners follow its source curves: round '
           'or cut the source corners before offsetting, or break the offset association first')
DECODE_X, SIDES_X = 1430, 1300
OUTLINE_A = (878, 465, 2002, 1214)       # take A 9-14.5: the outline (x0, y0, x1, y1, source px)
COPY_A = (913, 500, 1969, 1177)          # the Offset copy, 2 mm inside
QMM = (636, 832, 292, 60)                # take C 12-16.9: the Fillet window's Radius field (y 840-885 before corners)
UPDATE_BTN = (1866, 4, 264, 56)          # after.png: "Update to 0.41.0"
R1_SUGGEST = (0, 1488, 2880, 72)         # R1 from 31.5: the greyed suggested prompt row (y 1505-1550)
TOOLLOG = (60, 660, 2760, 560)           # R1: the tool-log card, under "Called solidcraft 6 times" (y 575-620)


def wrap(s, n=44):
    out, cur = [], ''
    for w in s.split():
        if len(cur) + len(w) + (1 if cur else 0) > n:
            out.append(cur)
            cur = w
        else:
            cur = (cur + ' ' + w) if cur else w
    return out + [cur]


# --- rails (F3, F8) ---------------------------------------------------------------------------------------------------
def arc(d, c, r, a0, a1, col, width):
    d.arc((c[0] - r, c[1] - r, c[0] + r, c[1] + r), a0, a1, fill=col, width=width)


def track(d, x0, y0, s, gap, lit_straight, lit_curve, curve=True):
    """A top view: rails straight from x0 to the bend, then a quarter turn down. y0 = the outer rail; s = scale."""
    bx, cy = x0 + 900 * s, y0 + 420 * s
    ro = cy - y0
    ri = ro - gap
    c1, c2 = (INK if lit_straight else DONE), (INK if lit_curve else DONE)
    for k in range(0, int(900 * s), int(60 * s)):            # sleepers
        d.line((x0 + k + 20 * s, y0 - 16 * s, x0 + k + 20 * s, y0 + gap + 16 * s), fill=DONEFILL if not lit_straight
               else (226, 232, 240), width=max(4, int(14 * s)))
    d.line((x0, y0, bx, y0), fill=c1, width=10)
    d.line((x0, y0 + gap, bx, y0 + gap), fill=c1, width=10)
    if curve:
        arc(d, (bx, cy), ro, 270, 360, c2, 10)
        arc(d, (bx, cy), ri, 270, 360, c2, 10)
        d.line((bx + ro, cy, bx + ro, cy + 260 * s), fill=c2, width=10)
        d.line((bx + ri, cy, bx + ri, cy + 260 * s), fill=c2, width=10)
    return bx, cy, ro, ri


def card_rails(step):
    im, d = canvas()
    header(d, 'Railway rails: the same gap')
    x0, y0, gap = 260, 420, 130
    bx, cy, ro, ri = track(d, x0, y0, 1.25, gap, step == 1, step == 2, curve=step >= 2)
    k1 = INK if step == 1 else DONE
    b.dimline(d, (700, y0 + 8), (700, y0 + gap - 8), BLUE if step == 1 else DONE, width=5)
    text(d, (730, y0 + gap / 2), 'same gap', 56, BLUE if step == 1 else DONE, anchor='lm')
    text(d, (260, 300), 'two rails, the same distance apart', 56, k1)
    if step >= 2:
        k2 = INK if step == 2 else DONE
        text(d, (bx - 640, cy + 40), 'outer rail: a wide curve', 56, k2)
        text(d, (bx - 640, cy + 120), 'inner rail: a little tighter', 56, ORANGE if step == 2 else DONE)
    if step >= 3:
        text(d, (260, 1150), 'you lay the outer rail,', 60, INK)
        text(d, (260, 1230), 'the inner rail follows', 60, INK)
        text(d, (1500, 1150), 'outer rail = the outline', 60, BLUE)
        text(d, (1500, 1230), 'inner rail = the Offset copy', 60, ORANGE)
    save(im, f'card-rails-{step}.png')


def rrect(d, box, r, col, width=8):
    x0, y0, x1, y1 = box
    if r <= 0:
        d.rectangle(box, outline=col, width=width)
    else:
        d.rounded_rectangle(box, radius=r, outline=col, width=width)


def card_sofar(step):
    im, d = canvas()
    header(d, 'So far')
    cols = (180, 1000, 1820)
    # 1: the rails again
    l1 = step == 1
    track(d, cols[0], 380, 0.5, 60, l1, l1)
    text(d, (cols[0], 760), 'copy = inner rail, tied', 52, INK if l1 else DONE)
    if step >= 2:
        l2 = step == 2
        s = 9                              # px per mm: a 60 x 40 outline is 540 x 360
        x0, y0 = cols[1] - 20, 330
        rrect(d, (x0, y0, x0 + 60 * s, y0 + 40 * s), 5 * s, BLUE if l2 else DONE)
        rrect(d, (x0 + 2 * s, y0 + 2 * s, x0 + 58 * s, y0 + 38 * s), 3 * s, ORANGE if l2 else DONE, width=6)
        text(d, (cols[1] - 20, 760), 'inside radius =', 52, INK if l2 else DONE)
        text(d, (cols[1] - 20, 825), 'outline radius - wall', 52, INK if l2 else DONE)
        text(d, (cols[1] - 20, 905), '5 - 2 = 3', 60, BLUE if l2 else DONE)
        text(d, (cols[1] - 20, 1010), 'width 60 to 70: the copy followed', 44, GREY if l2 else DONE)
        text(d, (cols[1] - 20, 1065), '(checked by a script, not filmed)', 44, GREY if l2 else DONE)
    if step >= 3:
        s = 9
        x0, y0 = cols[2] - 60, 330
        rrect(d, (x0, y0, x0 + 60 * s, y0 + 40 * s), 0, DONE)
        rrect(d, (x0 + 2 * s, y0 + 2 * s, x0 + 58 * s, y0 + 38 * s), 3 * s, ORANGE, width=6)
        text(d, (cols[2] - 60, 760), 'or break the link:', 52, INK)
        text(d, (cols[2] - 60, 825), 'plain lines you can round,', 52, INK)
        text(d, (cols[2] - 60, 890), 'no longer follow', 52, ORANGE)
    save(im, f'card-sofar-{step}.png')


# --- F4: decode the line (right panel) --------------------------------------------------------------------------------
def card_decode(step):
    im, d = panel((DECODE_X, 120, 2540, 1320))
    box = (DECODE_X, 120, 2540, 1320)
    x = DECODE_X + 50
    k1 = (INK if step == 1 else DONE) + (255,)
    o1 = (ORANGE if step == 1 else DONE) + (255,)
    s = 6
    ox, oy = 1640, 190
    d.rectangle((ox, oy, ox + 60 * s, oy + 40 * s), outline=(BLUE if step <= 2 else DONE) + (255,), width=6)
    d.rectangle((ox + 2 * s + 6, oy + 2 * s + 6, ox + 58 * s - 6, oy + 38 * s - 6), outline=k1, width=5)
    d.line((ox + 2 * s + 6, oy + 2 * s + 6, ox + 58 * s - 6, oy + 2 * s + 6), fill=o1, width=9)
    text(d, (ox + 60 * s + 30, oy + 30), 'l6', 52, o1, anchor='lm', box=box)
    text(d, (x, 520), 'l6 = SolidCraft\'s name for', 52, k1, box=box)
    text(d, (x, 585), 'one line of the copy', 52, k1, box=box)
    if step >= 2:
        k2 = (INK if step == 2 else DONE) + (255,)
        for tx in (ox + 90, ox + 180, ox + 270):           # tie ticks: the copy tied to the outline
            d.line((tx, oy - 4, tx, oy + 2 * s + 10), fill=(BLUE if step == 2 else DONE) + (255,), width=6)
        text(d, (x, 690), 'an offset = a copy', 52, k2, box=box)
        text(d, (x, 750), 'tied to the outline', 52, (BLUE if step == 2 else DONE) + (255,), box=box)
        text(d, (x, 830), 'source curves = the outline', 52, k2, box=box)
        text(d, (x, 890), 'it copied', 52, k2, box=box)
        g2 = (GREY if step == 2 else DONE) + (255,)
        text(d, (x, 965), "SolidCraft's source code: the", 44, g2, box=box)
        text(d, (x, 1015), "copy's ends are recomputed from", 44, g2, box=box)
        text(d, (x, 1065), 'the outline on every solve', 44, g2, box=box)
    if step >= 3:
        text(d, (x, 1140), 'round or cut = Fillet or Chamfer', 48, INK + (255,), box=box)
        text(d, (x, 1200), 'two fixes: shape the outline', 48, ORANGE + (255,), box=box)
        text(d, (x, 1255), 'first, or break the link', 48, ORANGE + (255,), box=box)
    save(im, f'card-decode-{step}.png')


# --- F6: the walls, the two corners to scale (right panel) -------------------------------------------------------------
def corner(d, ox, oy, s, outer_r, lit, label, wall):
    """The top-right corner of the tray: 12 mm of outline each way from the corner at (ox, oy); wall 2, inside R 3."""
    col = (BLUE if lit else DONE) + (255,)
    inner = (ORANGE if lit else DONE) + (255,)
    L = 12 * s
    if outer_r == 0:
        d.line((ox - L, oy, ox, oy), fill=col, width=7)
        d.line((ox, oy, ox, oy + L), fill=col, width=7)
    else:
        r = outer_r * s
        d.line((ox - L, oy, ox - r, oy), fill=col, width=7)
        d.arc((ox - 2 * r, oy, ox, oy + 2 * r), 270, 360, fill=col, width=7)
        d.line((ox, oy + r, ox, oy + L), fill=col, width=7)
    ix, iy, ri = ox - 2 * s, oy + 2 * s, 3 * s
    d.line((ox - L, iy, ix - ri, iy), fill=inner, width=7)
    d.arc((ix - 2 * ri, iy, ix, iy + 2 * ri), 270, 360, fill=inner, width=7)
    d.line((ix, iy + ri, ix, oy + L), fill=inner, width=7)
    # the wall at the corner: from the arc's midpoint out along the diagonal to the outline
    cx, cy = ix - ri, iy + ri
    p_in = (cx + ri * math.cos(math.pi / 4), cy - ri * math.sin(math.pi / 4))
    if outer_r == 0:
        p_out = (ox, oy)
    else:
        r = outer_r * s
        p_out = (ox - r + r * math.cos(math.pi / 4), oy + r - r * math.sin(math.pi / 4))
    d.line((p_in, p_out), fill=(INK if lit else DONE) + (255,), width=5)
    k = (INK if lit else DONE) + (255,)
    text(d, (ox - L, oy + L + 40), label, 48, k)
    text(d, (ox - L, oy + L + 105), wall, 50, (ORANGE if lit else DONE) + (255,))


def card_walls(step):
    im, d = panel((DECODE_X, 120, 2540, 1320))
    s = 22                                     # px per mm
    l1 = step == 1
    corner(d, 1820, 300, s, 0, l1, 'quick fix', '4.07')
    corner(d, 2330, 300, s, 5, l1, 'round first', '2.00')
    text(d, (1480, 820), 'wall at the corner: 4.07 vs 2.00', 50, (INK if l1 else DONE) + (255,))
    text(d, (1480, 885), 'round first: 2.00 all round', 50, (INK if l1 else DONE) + (255,))
    text(d, (1480, 180), 'to scale', 44, (GREY if l1 else DONE) + (255,))
    if step >= 2:
        text(d, (1985, 1010), f'{V_FIX1} - {V_FIX2}', 56, INK + (255,), anchor='mm', maxw=1060)
        text(d, (1985, 1090), f'= {V_DIFF} mm3', 60, BLUE + (255,), anchor='mm')
        text(d, (1985, 1170), 'all in the four corners', 52, INK + (255,), anchor='mm')
    save(im, f'card-walls-{step}.png')


# --- F10 -------------------------------------------------------------------------------------------------------------
def card_question(step):
    im, d = panel((SIDES_X, 140, 2540, 1300))
    k1 = (INK if step == 1 else DONE) + (255,)
    text(d, (1920, 330), 'Outline corners 1.5.', 64, k1, anchor='mm', maxw=1180)
    text(d, (1920, 420), 'Wall 2.', 64, k1, anchor='mm', maxw=1180)
    s = 9
    x0, y0 = 1650, 540
    d.rounded_rectangle((x0, y0, x0 + 60 * s, y0 + 40 * s), radius=int(1.5 * s), outline=BLUE + (255,), width=6)
    d.rectangle((x0 + 2 * s, y0 + 2 * s, x0 + 58 * s, y0 + 38 * s), outline=DONE + (255,), width=5)
    text(d, (x0 + 60 * s + 20, y0 + 20 * s), '?', 72, ORANGE + (255,), anchor='lm')
    if step >= 2:
        text(d, (1920, 1050), 'Round, sharp or refused?', 72, INK + (255,), anchor='mm', maxw=1180)
        text(d, (1920, 1170), 'Pause and think', 60, BLUE + (255,), anchor='mm')
    save(im, f'card-question-{step}.png')


RECIPE = ['1. Sketch a 60 x 40 rectangle', '2. Want 3 inside, wall 2: Fillet ? mm', '3. Offset 2 mm inward',
          '4. Measure an inside corner: 3.00?']


def card_recipe(step):
    im, d = canvas()
    header(d, 'Your turn: the same tray')
    for i in range(len(RECIPE)):
        if i < step:
            text(d, (180, 330 + i * 140), RECIPE[i], 64, INK if i == step - 1 else DONE, maxw=1500)
    text(d, (180, 1330), 'new to this? SolidCraft course, lesson 1', 44, GREY)
    s = 12
    x0, y0 = 1840, 420
    d.rectangle((x0, y0, x0 + 40 * s, y0 + 60 * s), outline=BLUE, width=7)      # the rectangle, 60 tall x 40 wide
    text(d, (x0 + 20 * s, y0 + 60 * s + 60), '60 x 40', 56, BLUE, anchor='mm')
    save(im, f'card-recipe-{step}.png')


# --- source overlays (2880 x 1620) -----------------------------------------------------------------------------------
def ov_wall_a():
    im, d = source()
    o, c = OUTLINE_A, COPY_A
    tint = ORANGE + (95,)
    d.rectangle((o[0], o[1], o[2], c[1]), fill=tint)
    d.rectangle((o[0], c[3], o[2], o[3]), fill=tint)
    d.rectangle((o[0], c[1], c[0], c[3]), fill=tint)
    d.rectangle((c[2], c[1], o[2], c[3]), fill=tint)
    save(im, 'ov-wall-a.png')


def ov_qmm():
    im, d = source()
    x, y, w, h = QMM
    d.rounded_rectangle((x, y, x + w, y + h), radius=8, fill=WHITE + (255,), outline=ORANGE + (255,), width=4)
    text(d, (x + 20, y + h / 2), '? mm', 44, ORANGE + (255,), anchor='lm', frame=(SW, SH))
    save(im, 'ov-qmm.png')


def ov_r1_mask():
    im, d = source()
    x, y, w, h = R1_SUGGEST
    d.rectangle((x, y, x + w, y + h), fill=WHITE + (255,))
    text(d, (40, y + h / 2), "(Claude Code's greyed suggestion, hidden)", 44, GREY + (255,), anchor='lm', frame=(SW, SH))
    save(im, 'ov-r1-mask.png')


def ov_toollog():
    im, d = source()
    x, y, w, h = TOOLLOG
    d.rounded_rectangle((x, y, x + w, y + h), radius=20, fill=WHITE + (250,), outline=ORANGE + (255,), width=6)
    text(d, (x + 40, y + 50), 'Its 4th solidcraft call, from the tool log', 48, INK + (255,), anchor='lm', frame=(SW, SH))
    text(d, (x + 40, y + 110), '(not on its screen):', 48, ORANGE + (255,), anchor='lm', frame=(SW, SH))
    lines = wrap(LINE_R1, 44)
    # two columns of the wrapped reply so the whole line fits the card at 44 px+
    for i, ln in enumerate(lines):
        col, row = divmod(i, 3)
        text(d, (x + 40 + col * 1360, y + 190 + row * 70), ln, 46, RED + (255,), anchor='lm', frame=(SW, SH),
             path=b.R)
    text(d, (x + 40, y + h - 50), 'l5 here: another line of the copy', 44, GREY + (255,), anchor='lm', frame=(SW, SH))
    LOG['ov-toollog.lines'] = lines
    save(im, 'ov-toollog.png')


def mask_after():
    b.CUR.clear()
    im = Image.open(os.path.join(TAKES, 'runs', 'R1', 'after.png')).convert('RGB')
    x, y, w, h = UPDATE_BTN
    bar = im.getpixel((x - 20, 30))
    ImageDraw.Draw(im).rectangle((x, y, x + w - 1, y + h - 1), fill=bar)
    save(im, 'after-masked.png')


def short_stack():
    """The Short's frame 1 (1080 x 960): A's refused copy corner (the red line) over C's round copy. Real pixels,
    cropped and scaled only; the labels sit on white bars, off the pixels."""
    b.CUR.clear()
    im = Image.new('RGB', (1080, 960), WHITE)
    d = ImageDraw.Draw(im)
    for k, (png, box, lab, col) in enumerate((
            ('A/refusal.png', (380, 450, 2180, 1250), 'ROUND THE COPY: REFUSED', RED),
            ('C/copy.png', (540, 380, 2340, 1180), 'ROUND THE OUTLINE FIRST: ROUND', BLUE))):
        y0 = k * 480
        fr = Image.open(os.path.join(TAKES, png)).convert('RGB').crop(box).resize((1080, 480), Image.LANCZOS)
        im.paste(fr, (0, y0))
        f = b.font(b.B, 48)
        bb = d.textbbox((540, y0 + 425), lab, font=f, anchor='mm')
        d.rectangle((bb[0] - 20, bb[1] - 10, bb[2] + 20, bb[3] + 10), fill=WHITE, outline=col, width=5)
        text(d, (540, y0 + 425), lab, 48, col, anchor='mm', frame=(1080, 960))
    d.line((0, 480, 1080, 480), fill=INK, width=6)
    save(im, 'short-stack.png')


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
        dd.text((x + 6, y + th), n, font=b.font(b.R, 22), fill=(255, 255, 255))
    sh.save(os.path.join(outdir, 'cards-sheet-fx12.jpg'), quality=85)
    tw, th = 960, 540
    sh = Image.new('RGB', (tw * 2, th * 3), (90, 90, 90))
    pairs = [('ov-wall-a.png', 'f-A-12.png'), ('ov-qmm.png', 'f-C-16.png'), ('ov-toollog.png', 'f-R1-34.png'),
             ('ov-r1-mask.png', 'f-R1-34.png')]
    for i, (ov, fr) in enumerate(pairs):
        p = os.path.join(outdir, fr)
        base = Image.open(p).convert('RGBA') if os.path.exists(p) else Image.new('RGBA', (SW, SH), (255,) * 4)
        t = Image.alpha_composite(base, Image.open(os.path.join(OUT, ov))).convert('RGB').resize((tw, th))
        sh.paste(t, ((i % 2) * tw, (i // 2) * th))
    sh.paste(Image.open(os.path.join(OUT, 'after-masked.png')).convert('RGB').resize((tw, th)), (0, 2 * th))
    sh.paste(Image.open(os.path.join(OUT, 'short-stack.png')).convert('RGB').resize((tw * 540 // 480 // 2, th)), (tw, 2 * th))
    sh.save(os.path.join(outdir, 'overlays-sheet-fx12.jpg'), quality=85)


def check_alpha():
    for n in sorted(os.listdir(OUT)):
        for pre, x in (('card-decode', DECODE_X), ('card-walls', DECODE_X), ('card-question', SIDES_X)):
            if n.startswith(pre):
                im = Image.open(os.path.join(OUT, n))
                if im.mode != 'RGBA' or im.crop((0, 0, x, H)).getchannel('A').getextrema() != (0, 0):
                    PROBLEMS.append(f'{n}: not transparent left of {x}')


def main():
    os.makedirs(OUT, exist_ok=True)
    PROBLEMS.clear()
    LOG.clear()
    for s in (1, 2, 3):
        card_rails(s)
        card_sofar(s)
        card_decode(s)
    for s in (1, 2):
        card_walls(s)
        card_question(s)
    card_recipe(1)
    card_recipe(2)
    ov_wall_a()
    ov_qmm()
    ov_r1_mask()
    ov_toollog()
    mask_after()
    short_stack()
    check_alpha()
    print('PROBLEMS:', PROBLEMS or 'none')


if __name__ == '__main__':
    main()
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
