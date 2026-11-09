"""Fix-it fx8 cards (SolidCraft Convert Mesh: "this mesh is not a supported constant-section prism"), the draw_fx6.py
pattern: light, 2560 x 1440, one picture that builds; each step adds, earlier steps stay on and turn grey. Text 44 px+.
  full frame (RGB):  card-recipe-1..3, card-cutter-1..3, card-sofar-1..3
  overlay (RGBA, transparent outside the panel): card-question-1..2 (right half; no answer on screen)
Sources: out/fx8/ANSWERS.md Q9 (hook-plain.stl converts, 8,500.0 mm3; hook.stl with two screw holes refused), Q11 (the
rounded box). The hook in section (XZ, mm): back plate x 0-5, z 0-60; floor x 5-25, z 0-5; lip x 20-25, z 5-10
(425 mm2), pushed 20 mm along y. Screw holes through the back plate along x at y = 10, z about 22 and 45, about 5 across.
Run in the QA image:  docker run --rm -v "<lab>:/lab" -w /lab cad3way-draw:1 python3 video/draw_fx8.py [sheet OUTDIR]"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(LAB, 'video', 'frames-fx8')
FD = '/usr/share/fonts/truetype/dejavu/'
B, R, MONO = FD + 'DejaVuSans-Bold.ttf', FD + 'DejaVuSans.ttf', FD + 'DejaVuSansMono.ttf'
W, H = 2560, 1440
INK, RED, GREEN, GREY, BLUE, AMBER = (31, 41, 55), (183, 28, 28), (27, 127, 59), (110, 120, 138), (29, 78, 216), (180, 110, 0)
WHITE, LIGHT, PANEL = (255, 255, 255), (241, 245, 249), (250, 251, 253)
DONE, DONEFILL = (160, 167, 178), (244, 246, 248)
GREENFILL, AMBERFILL, REDFILL, PART = (221, 240, 227), (253, 236, 214), (251, 228, 228), (214, 220, 229)
TOPFILL, SIDEFILL, HOLEFILL = (232, 236, 242), (190, 199, 211), (88, 98, 114)
MIN_PX = 44
MARK = (232, 89, 12)
PROBLEMS = []

# --- geometry (tested against the lab) ------------------------------------------------------------------------------
HOOK = [(0, 0), (25, 0), (25, 10), (20, 10), (20, 5), (5, 5), (5, 60), (0, 60)]
DEPTH = 20
HOLE_Y, HOLE_Z, HOLE_D = 10.0, (22.0, 45.0), 5.0
SLICES = (3.0, 10.0, 17.0)                         # the three slice planes across the 20 mm (the middle one: the holes)


def area(pts):
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1]))) / 2


# --- drawing helpers (as draw_fx6.py) -------------------------------------------------------------------------------
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
    if bb[0] < 0 or bb[2] > W:
        PROBLEMS.append(f'{s!r}: off the frame {bb}')
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
        return {'ink': INK, 'acc': accent, 'fill': LIGHT, 'sub': GREY, 'on': True}
    return {'ink': DONE, 'acc': DONE, 'fill': DONEFILL, 'sub': DONE, 'on': False}


def c(p, col):
    """A fill colour while the step is current, the grey fill once it is done."""
    return col if p['on'] else DONEFILL


def star(cx, cy, r, n=5):
    return [(cx + (r if i % 2 == 0 else r * 0.45) * math.sin(math.pi * i / n),
             cy - (r if i % 2 == 0 else r * 0.45) * math.cos(math.pi * i / n)) for i in range(2 * n)]


# --- the hook in an oblique view (y goes back, to the right and up) --------------------------------------------------
class Hook:
    def __init__(self, ox, oy, s):
        self.ox, self.oy, self.s = ox, oy, s

    def p(self, x, y, z):
        return (self.ox + (x + 0.55 * y) * self.s, self.oy - (z + 0.4 * y) * self.s)

    def quad(self, d, a, b, cc, dd, fill, col, mesh, n=1):
        """A flat face a-b-c-d; as a mesh it is cut into n strips, each strip two triangles (the diagonal drawn)."""
        pts = [self.p(*q) for q in (a, b, cc, dd)]
        d.polygon(pts, fill=fill)
        if mesh:
            for i in range(n):
                t0, t1 = i / n, (i + 1) / n
                lo0 = [a[j] + (dd[j] - a[j]) * t0 for j in range(3)]
                hi0 = [b[j] + (cc[j] - b[j]) * t0 for j in range(3)]
                lo1 = [a[j] + (dd[j] - a[j]) * t1 for j in range(3)]
                hi1 = [b[j] + (cc[j] - b[j]) * t1 for j in range(3)]
                d.line([self.p(*lo1), self.p(*hi1)], fill=col, width=3)
                d.line([self.p(*lo0), self.p(*hi1)], fill=col, width=3)
        d.line(pts + pts[:1], fill=col, width=6, joint='curve')

    def draw(self, d, p, mesh=False, holes=False):
        col, D = p['ink'], DEPTH
        top, side, front = c(p, TOPFILL), c(p, SIDEFILL), c(p, PART)
        q = lambda *a, **k: self.quad(d, *a, mesh=mesh, col=col, **k)  # noqa: E731
        q((5, 0, 5), (5, 0, 60), (5, D, 60), (5, D, 5), side, n=4)                 # back plate, inner face
        if holes:
            for z in HOLE_Z:
                pts = [self.p(5, HOLE_Y + HOLE_D / 2 * math.cos(t), z + HOLE_D / 2 * math.sin(t))
                       for t in [2 * math.pi * k / 32 for k in range(32)]]
                d.polygon(pts, fill=p['acc'] if p['on'] else DONE, outline=col)
        q((5, 0, 5), (20, 0, 5), (20, D, 5), (5, D, 5), top, n=2)                  # floor top
        q((20, 0, 10), (25, 0, 10), (25, D, 10), (20, D, 10), top)                 # lip top
        q((25, 0, 0), (25, 0, 10), (25, D, 10), (25, D, 0), side, n=2)             # lip front
        q((0, 0, 60), (5, 0, 60), (5, D, 60), (0, D, 60), top)                     # back plate top
        # the front face (y = 0): the outline, as a mesh three rectangles cut into triangles
        pts = [self.p(x, 0, z) for x, z in HOOK]
        d.polygon(pts, fill=front)
        if mesh:
            for (x0, z0, x1, z1) in [(0, 0, 5, 60), (5, 0, 20, 5), (20, 0, 25, 10)]:
                nz = 6 if z1 == 60 else 1
                for i in range(nz):
                    za, zb = z0 + (z1 - z0) * i / nz, z0 + (z1 - z0) * (i + 1) / nz
                    d.line([self.p(x0, 0, za), self.p(x1, 0, zb)], fill=col, width=3)
                    if i:
                        d.line([self.p(x0, 0, za), self.p(x1, 0, za)], fill=col, width=3)
            d.line([self.p(5, 0, 0), self.p(5, 0, 5)], fill=col, width=3)
            d.line([self.p(20, 0, 0), self.p(20, 0, 5)], fill=col, width=3)
        d.line(pts + pts[:1], fill=col, width=6, joint='curve')

    def slice_planes(self, d, col):
        for y in SLICES:
            pts = [self.p(x, y, z) for x, z in HOOK]
            d.line(pts + pts[:1], fill=col, width=6, joint='curve')


def flat_slice(d, ox, oy, s, p, gaps=False, col=None):
    """One slice of the hook, drawn flat: the outline; through the holes the back plate has two gaps."""
    col = col or p['ink']
    pts = [(ox + x * s, oy - z * s) for x, z in HOOK]
    d.polygon(pts, fill=c(p, PART))
    d.line(pts + pts[:1], fill=col, width=6, joint='curve')
    if gaps:
        for z in HOLE_Z:
            z0, z1 = z - HOLE_D / 2, z + HOLE_D / 2
            d.rectangle((ox - 8, oy - z1 * s, ox + 5 * s + 8, oy - z0 * s), fill=c(p, REDFILL))
            for zz in (z0, z1):
                d.line((ox, oy - zz * s, ox + 5 * s, oy - zz * s), fill=col, width=6)


# --- card 1: a photo vs a recipe -------------------------------------------------------------------------------------
STL_PHOTO = Hook(250, 1370, 8)


def card_recipe(step):
    im, d = canvas(); header(d, 'A photo vs a recipe')
    p = pal(1, step, BLUE)                       # 1: the cake in a photo frame; a recipe card
    d.rectangle((220, 200, 1060, 640), fill=c(p, AMBERFILL), outline=p['ink'], width=8)
    d.rectangle((260, 240, 1020, 600), fill=c(p, (219, 234, 254)), outline=p['ink'], width=4)
    d.rectangle((450, 470, 830, 580), fill=c(p, (240, 200, 160)), outline=p['ink'], width=5)   # lower layer
    d.rectangle((500, 380, 780, 470), fill=c(p, (240, 200, 160)), outline=p['ink'], width=5)   # upper layer
    d.rectangle((500, 370, 780, 400), fill=c(p, (252, 231, 243)), outline=p['ink'], width=4)   # icing
    d.rectangle((630, 300, 650, 370), fill=c(p, (147, 197, 253)), outline=p['ink'], width=3)   # candle
    d.ellipse((626, 260, 654, 300), fill=c(p, (251, 191, 36)), outline=p['ink'], width=3)
    text(d, (640, 710), 'a photo: shows the cake', 60, p['acc'], anchor='mm')
    d.rectangle((1500, 200, 2340, 640), fill=c(p, (254, 252, 240)), outline=p['ink'], width=6)
    text(d, (1560, 270), 'Recipe', 60, p['ink'], anchor='lm')
    for k in range(4):
        y = 360 + k * 70
        d.ellipse((1560, y - 10, 1580, y + 10), fill=p['ink'])
        d.line((1610, y, 2260 - 120 * (k % 2), y), fill=p['sub'], width=10)
    text(d, (1920, 710), 'a recipe: change it, bake again', 60, p['acc'], anchor='mm')
    if step >= 2:                                # 2: the hook's recipe in four lines
        p = pal(2, step, GREEN)
        text(d, (1920, 785), 'a solid body = a recipe', 58, p['acc'], anchor='mm')
        text(d, (1920, 842), '(its timeline)', 46, p['ink'], anchor='mm')
        d.rounded_rectangle((1480, 870, 2360, 1360), radius=26, fill=p['fill'], outline=p['ink'], width=6)
        for k, ln in enumerate(['1. sketch the outline', '2. push it 20 mm', '3. round the top edges',
                                '4. drill 2 screw holes']):
            text(d, (1540, 950 + k * 110), ln, 58, p['ink'], anchor='lm', maxw=780)
    if step >= 3:                                # 3: the hook as a skin of flat triangles
        p = pal(3, step, RED)
        STL_PHOTO.draw(d, p, mesh=True)
        text(d, (680, 1050), 'an STL = a 3D photo:', 64, p['acc'], anchor='lm', maxw=780)
        text(d, (680, 1140), 'triangles, no steps', 64, p['ink'], anchor='lm', maxw=780)
    save(im, f'card-recipe-{step}.png')


# --- card 2: one outline, pushed straight ----------------------------------------------------------------------------
CUT_S = 6.5


def slices_row(d, oy, p, gaps):
    for k, y in enumerate(SLICES):
        hole = gaps and y == HOLE_Y
        flat_slice(d, 680 + k * 260, oy, CUT_S, p, gaps=hole, col=RED if hole and p['on'] else None)


def card_cutter(step):
    im, d = canvas(); header(d, 'One outline, pushed straight')
    p = pal(1, step, AMBER)                      # 1: dough through a cookie cutter
    d.rounded_rectangle((200, 330, 900, 440), radius=20, fill=c(p, AMBERFILL), outline=p['ink'], width=6)
    d.polygon(star(550, 300, 90), fill=c(p, (253, 224, 170)), outline=p['ink'], width=8)
    d.line((550, 180, 550, 200), fill=p['ink'], width=8)
    d.polygon([(530, 175), (570, 175), (550, 205)], fill=p['ink'])
    for k in range(3):
        d.polygon(star(1080 + k * 190, 350, 80), fill=c(p, (253, 224, 170)), outline=p['ink'], width=6)
    text(d, (1560, 350), 'every piece the same shape', 60, p['acc'], anchor='lm', maxw=960)
    if step >= 2:                                # 2: the plain hook pushed 20 mm, three slices, all the same
        p = pal(2, step, GREEN)
        h = Hook(220, 945, CUT_S)
        h.draw(d, p)
        h.slice_planes(d, p['acc'])
        slices_row(d, 945, p, gaps=False)
        text(d, (1560, 690), 'constant section:', 64, p['acc'], anchor='lm', maxw=960)
        text(d, (1560, 780), 'every slice the same', 64, p['ink'], anchor='lm', maxw=960)
    if step >= 3:                                # 3: the drilled hook: the middle slice has two gaps
        p = pal(3, step, RED)
        h = Hook(220, 1420, CUT_S)
        h.draw(d, p, holes=True)
        h.slice_planes(d, p['acc'])
        slices_row(d, 1420, p, gaps=True)
        text(d, (1560, 1170), 'slices differ:', 64, p['acc'], anchor='lm', maxw=960)
        text(d, (1560, 1260), 'not a prism', 64, p['ink'], anchor='lm', maxw=960)
    save(im, f'card-cutter-{step}.png')


# --- card 3: so far --------------------------------------------------------------------------------------------------
SOFAR = [['an STL is a photo: no recipe'],
         ['Convert Mesh rebuilds a cookie cutter', 'shape as a solid: new steps work on it'],
         ['anything else: redraw it,', 'or edit the file it came from']]


def icon(d, k, x, y, p):
    col = p['acc']
    if k == 0:                                   # a photo
        d.rectangle((x, y - 70, x + 180, y + 70), fill=c(p, (219, 234, 254)), outline=col, width=7)
        d.polygon([(x + 20, y + 55), (x + 80, y - 20), (x + 130, y + 55)], fill=col)
        d.ellipse((x + 125, y - 50, x + 155, y - 20), fill=col)
    elif k == 1:                                 # a cookie cutter
        d.polygon(star(x + 90, y, 85), fill=c(p, GREENFILL), outline=col, width=8)
    else:                                        # a pencil
        d.polygon([(x + 30, y + 40), (x + 150, y - 70), (x + 180, y - 40), (x + 60, y + 70)],
                  fill=c(p, AMBERFILL), outline=col, width=6)
        d.polygon([(x + 30, y + 40), (x + 60, y + 70), (x + 5, y + 85)], fill=col)


def card_sofar(step):
    im, d = canvas(); header(d, 'So far')
    y = 220
    for k, lines in enumerate(SOFAR[:step]):
        p = pal(k + 1, step, GREEN if k == 1 else BLUE if k == 0 else AMBER)
        d.rounded_rectangle((120, y, 2440, y + 300), radius=26, fill=p['fill'], outline=p['ink'], width=6)
        icon(d, k, 200, y + 150, p)
        if len(lines) == 1:
            text(d, (520, y + 150), lines[0], 68, p['ink'], anchor='lm', maxw=1880)
        for i, ln in enumerate(lines if len(lines) > 1 else []):
            text(d, (520, y + 100 + i * 100), ln, 68, p['ink'] if i == 0 else p['acc'], anchor='lm', maxw=1880)
        y += 340
    save(im, f'card-sofar-{step}.png')


# --- card 4: the question (overlay, right half; no answer on screen) -------------------------------------------------
QUEST = (1300, 170, 2520, 1270)


def rr_pts(cx, cy, w, h, rx, ry, n=10):
    pts = []
    for (qx, qy, a0) in [(cx + w / 2 - rx, cy + h / 2 - ry, 0), (cx - w / 2 + rx, cy + h / 2 - ry, 90),
                         (cx - w / 2 + rx, cy - h / 2 + ry, 180), (cx + w / 2 - rx, cy - h / 2 + ry, 270)]:
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((qx + rx * math.cos(a), qy + ry * math.sin(a)))
    return pts


# cut 3 (watch-c2, 4:07): the box seen from a corner, like the SolidCraft view beside it. The old front view drew the
# top as a squashed rounded cap, so the top looked rounded too. Now: one crisp top outline (flat top) and the side shaded
# strip by strip (each flat face one shade, the rounded upright edges grade between them).
QBOX_W, QBOX_H, QBOX_R, QBOX_S = 40.0, 20.0, 5.0, 9.0     # Q11's box: 40 x 40 x 20 mm, 4 upright edges R5
QBOX_C = (1910.0, 761.0)
QUESTION_LABELS = ('flat top',)
_LIGHT = (-0.2, 0.98)                         # from the left, past the +y face (half-Lambert below)


def qbox_plan(n=12):
    """The rounded square in plan (mm), counter-clockwise: (x, y, nx, ny, name)."""
    h, r = QBOX_W / 2, QBOX_R
    c = h - r
    pts = []
    for (qx, qy, a0) in [(c, -c, -90), (c, c, 0), (-c, c, 90), (-c, -c, 180)]:
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((qx + r * math.cos(a), qy + r * math.sin(a), math.cos(a), math.sin(a), (qx, qy)))
    return pts


def qbox_project(x, y, z):
    cx, cy = QBOX_C
    return (cx + (x - y) * 0.866 * QBOX_S, cy + (x + y) * 0.5 * QBOX_S - z * QBOX_S)


def qbox_outline(z):
    """The outline at height z, projected: (X, Y, nx, ny, z)."""
    return [qbox_project(x, y, z) + (nx, ny, z) for (x, y, nx, ny, _) in qbox_plan()]


def _strips():
    p = qbox_plan()
    out = []
    for a, b in zip(p, p[1:] + p[:1]):
        nx, ny = (a[2] + b[2]) / 2, (a[3] + b[3]) / 2
        if nx + ny <= 1e-6:                     # faces away from the viewer
            continue
        if abs(a[0] - b[0]) < 1e-9 and a[2] > 0.99 and b[2] > 0.99:
            name = 'face+x'
        elif abs(a[1] - b[1]) < 1e-9 and a[3] > 0.99 and b[3] > 0.99:
            name = 'face+y'
        elif a[4] == b[4] == (QBOX_W / 2 - QBOX_R, QBOX_W / 2 - QBOX_R):
            name = 'round'
        elif a[4] == b[4]:
            name = 'round-side'
        else:
            continue
        L = math.hypot(nx, ny)
        lit = 0.5 + 0.5 * (nx * _LIGHT[0] + ny * _LIGHT[1]) / L
        out.append((name, 120 + round(110 * lit), a, b))
    return out


def qbox_side_shades():
    return [(n, s) for n, s, _, _ in _strips()]


def dashed(d, pts, fill, width, on=24.0, off=16.0):
    """A dashed polyline: on px drawn, off px skipped, measured along the line."""
    pos, draw = 0.0, True
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        t = 0.0
        while t < seg - 1e-9:
            left = (on if draw else off) - pos
            step = min(left, seg - t)
            if draw:
                f0, f1 = t / seg, (t + step) / seg
                d.line([(x0 + (x1 - x0) * f0, y0 + (y1 - y0) * f0), (x0 + (x1 - x0) * f1, y0 + (y1 - y0) * f1)],
                       fill=fill, width=width)
            t += step
            pos += step
            if pos >= (on if draw else off) - 1e-9:
                pos, draw = 0.0, not draw


def draw_qbox(d, bx):
    for name, sh, a, b in _strips():
        q = [qbox_project(a[0], a[1], 0), qbox_project(b[0], b[1], 0), qbox_project(b[0], b[1], QBOX_H),
             qbox_project(a[0], a[1], QBOX_H)]
        d.polygon(q, fill=(sh, sh + 6, sh + 14, 255), outline=(sh, sh + 6, sh + 14, 255))
    vis = [p for p in qbox_plan() if p[2] + p[3] > 1e-6]
    bottom = [qbox_project(x, y, 0) for (x, y, *_r) in vis]
    d.line(bottom, fill=INK + (255,), width=6, joint='curve')
    for (x, y, *_r) in (vis[0], vis[-1]):       # the silhouette's two upright lines
        d.line([qbox_project(x, y, 0), qbox_project(x, y, QBOX_H)], fill=INK + (255,), width=6)
    top = [p[:2] for p in qbox_outline(QBOX_H)]
    d.polygon(top, fill=TOPFILL + (255,), outline=INK + (255,), width=6)
    cx, cy = qbox_project(0, 0, QBOX_H)
    text(d, (cx, cy), QUESTION_LABELS[0], 44, GREY, anchor='mm', box=bx)
    xr = max(p[0] for p in top)
    for z in (7, 13):                            # two slices across, bottom to top: dashed along the front
        dashed(d, [qbox_project(x, y, z) for (x, y, *_r) in vis], MARK + (255,), 7)
        ry = qbox_project(vis[0][0], vis[0][1], z)[1]
        text(d, (xr + 40, ry), 'slice', 44, MARK, anchor='lm', box=bx)


def card_question(step):
    im, d = overlay(QUEST)
    cx, bx = (QUEST[0] + QUEST[2]) / 2, QUEST
    text(d, (cx, 260), 'A box, 4 upright edges rounded.', 54, INK, anchor='mm', box=bx)
    text(d, (cx, 345), 'Slice it across, bottom to top.', 54, INK, anchor='mm', box=bx)
    draw_qbox(d, bx)
    text(d, (cx, 1000), 'Will Convert Mesh rebuild it?', 62, BLUE, anchor='mm', box=bx)
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
    sh.save(os.path.join(outdir, 'fx8-sheet.png'))
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
    for s in (1, 2, 3):
        card_recipe(s)
        card_cutter(s)
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
