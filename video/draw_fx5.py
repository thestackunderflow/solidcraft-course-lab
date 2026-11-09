"""Fix-it fx5 cards (SolidCraft Send to Slicer, a second slicer window), rev 5 style: light, 2560 x 1440, one picture
that builds; each step adds, earlier steps stay on and turn grey. Text 44 px or more.
  full frame (RGB):   card-copy-1..3 (F2), card-knock-1..4 (F6), card-recap-1..5 (F12), card-question.png (F13)
  overlays (RGBA, transparent outside the panel):
                      card-folders-1..3 (F3, right 40%), card-sofar-1..3 (F9, left 50%), card-reply-1..4 (F11, left 50%)
Sources: SCRIPT-fx5.md rev 4.1; out/fx5/G/orca-single-instance.txt and bambu-single-instance.txt ("Invalid option
--single-instance"); out/fx5/runs/R1/reply.txt (the four reply clauses, word for word).
Run in the QA image:  docker run --rm -v "<lab>:/lab" -w /lab video-qa:2 python video/draw_fx5.py [sheet OUTDIR]"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(LAB, 'video', 'frames-fx5')
os.makedirs(OUT, exist_ok=True)
FD = '/usr/share/fonts/truetype/dejavu/'
B, R, MONO = FD + 'DejaVuSans-Bold.ttf', FD + 'DejaVuSans.ttf', FD + 'DejaVuSansMono.ttf'
W, H = 2560, 1440
INK, RED, GREEN, GREY, BLUE, AMBER = (31, 41, 55), (183, 28, 28), (27, 127, 59), (110, 120, 138), (29, 78, 216), (180, 110, 0)
WHITE, LIGHT, PANEL = (255, 255, 255), (241, 245, 249), (250, 251, 253)
DONE, DONEFILL = (160, 167, 178), (244, 246, 248)      # a finished step: grey ink, pale fill
GREENFILL, AMBERFILL = (221, 240, 227), (253, 236, 214)
MIN_PX = 44
PROBLEMS = []


def font(p, s):
    return ImageFont.truetype(p, s)


def text(d, xy, s, size=64, fill=INK, path=B, anchor='la', maxw=None, box=None):
    """Draw text; record a problem if it is under 44 px, wider than maxw, or leaves box (x0, y0, x1, y1)."""
    if size < MIN_PX:
        PROBLEMS.append(f'{s!r}: {size} px')
    f = font(path, size)
    d.text(xy, s, font=f, fill=fill, anchor=anchor)
    bb = d.textbbox(xy, s, font=f, anchor=anchor)
    if maxw and bb[2] - bb[0] > maxw:
        PROBLEMS.append(f'{s!r}: {bb[2] - bb[0]:.0f} px wide, max {maxw}')
    if box and (bb[0] < box[0] or bb[1] < box[1] or bb[2] > box[2] or bb[3] > box[3]):
        PROBLEMS.append(f'{s!r}: outside its panel {bb} vs {box}')


def wrap(s, size, path, width):
    f, lines, cur = font(path, size), [], ''
    for w in s.split():
        t = (cur + ' ' + w).strip()
        if f.getlength(t) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


def canvas():
    im = Image.new('RGB', (W, H), WHITE)
    return im, ImageDraw.Draw(im)


def overlay(box):
    """A transparent frame with one light, opaque panel at box."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, radius=28, fill=PANEL + (255,), outline=INK + (255,), width=5)
    return im, d


def header(d, s):
    text(d, (W / 2, 100), s, 88, anchor='mm', maxw=2400)


def save(im, name):
    im.save(os.path.join(OUT, name))
    print(name)


def pal(k, step, accent=INK):
    """Colours for the part added at step k, seen at step `step`: live on its own step, grey once done."""
    if k == step:
        return {'ink': INK, 'acc': accent, 'fill': LIGHT, 'sub': GREY}
    return {'ink': DONE, 'acc': DONE, 'fill': DONEFILL, 'sub': DONE}


def arrow(d, a, b, col=INK, w=10, dash=False):
    if dash:
        n = int(math.dist(a, b) // 40)
        for i in range(0, n, 2):
            p = (a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n)
            q = (a[0] + (b[0] - a[0]) * (i + 1) / n, a[1] + (b[1] - a[1]) * (i + 1) / n)
            d.line((p, q), fill=col, width=w)
    else:
        d.line((a, b), fill=col, width=w)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    L = 34
    d.polygon([b, (b[0] - L * math.cos(ang - 0.45), b[1] - L * math.sin(ang - 0.45)),
               (b[0] - L * math.cos(ang + 0.45), b[1] - L * math.sin(ang + 0.45))], fill=col)


def filebox(d, x0, y0, x1, y1, p, title, sub=None):
    """A file: a page with a folded corner."""
    c = 50
    d.polygon([(x0, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1), (x0, y1)], fill=p['fill'], outline=p['ink'])
    d.line([(x0, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1), (x0, y1), (x0, y0)], fill=p['ink'], width=6)
    d.line([(x1 - c, y0), (x1 - c, y0 + c), (x1, y0 + c)], fill=p['ink'], width=5)
    cx = (x0 + x1) / 2
    text(d, (cx, (y0 + y1) / 2 - (30 if sub else 0)), title, 52, p['ink'], anchor='mm', maxw=x1 - x0 - 30)
    if sub:
        text(d, (cx, (y0 + y1) / 2 + 45), sub, 46, p['acc'], R, anchor='mm', maxw=x1 - x0 - 30)


def boxed(d, xy, p, title, sub=None, sub_col=None):
    x0, y0, x1, y1 = xy
    d.rounded_rectangle(xy, radius=24, fill=p['fill'], outline=p['ink'], width=6)
    cx = (x0 + x1) / 2
    text(d, (cx, (y0 + y1) / 2 - (32 if sub else 0)), title, 56, p['ink'], anchor='mm', maxw=x1 - x0 - 30)
    if sub:
        text(d, (cx, (y0 + y1) / 2 + 45), sub, 46, sub_col or p['acc'], R, anchor='mm', maxw=x1 - x0 - 30)


def caption(d, x, y, lines, p, size=56, gap=72):
    for i, ln in enumerate(lines):
        text(d, (x, y + i * gap), ln, size, p['acc'] if i == len(lines) - 1 else p['ink'], anchor='lm', maxw=W - 60 - x)


# --- F2: the slicer reads the file once ------------------------------------------------------------------------
CAPX = 1560


def card_copy(step):
    im, d = canvas(); header(d, 'Why the slicer still shows the old hook')
    p = pal(1, step, BLUE)                       # 1: SolidCraft -> file -> slicer, read once
    boxed(d, (80, 300, 440, 460), p, 'SolidCraft')
    arrow(d, (450, 380), (585, 380), p['ink'], 9)
    filebox(d, 600, 280, 940, 480, p, 'hook .3mf')
    text(d, (770, 530), 'in the hand-over folder', 46, p['sub'], R, anchor='mm')
    arrow(d, (950, 380), (1085, 380), p['ink'], 9)
    boxed(d, (1100, 280, 1480, 480), p, 'slicer', 'its own copy')
    caption(d, CAPX, 330, ['the slicer reads it once,', 'into its own memory'], p)
    if step >= 2:                                # 2: a web page and its screenshot
        p = pal(2, step, GREEN)
        d.rounded_rectangle((80, 640, 560, 900), radius=20, fill=p['fill'], outline=p['ink'], width=6)
        d.line((80, 700, 560, 700), fill=p['ink'], width=5)
        for k in range(3):
            d.ellipse((110 + k * 40, 658, 134 + k * 40, 682), fill=p['ink'])
        text(d, (320, 765), 'web page', 56, p['ink'], anchor='mm')
        text(d, (320, 840), 'it changes', 46, p['acc'], R, anchor='mm')
        arrow(d, (580, 770), (745, 770), p['ink'], 9)
        d.rectangle((760, 640, 1240, 900), fill=p['fill'], outline=p['ink'], width=6)
        d.rectangle((785, 665, 1215, 875), outline=p['ink'], width=3)
        text(d, (1000, 735), 'screenshot', 56, p['ink'], anchor='mm')
        text(d, (1000, 815), 'stays as it was', 46, p['sub'], R, anchor='mm')
        caption(d, CAPX, 735, ['the page changes,', 'the screenshot does not'], p)
    if step >= 3:                                # 3: newer file, old copy, read again
        p = pal(3, step, GREEN)
        filebox(d, 80, 1030, 440, 1250, p, 'hook .3mf', 'newer: 40')
        text(d, (260, 1300), 'sent again', 46, p['sub'], R, anchor='mm')
        arrow(d, (455, 1140), (805, 1140), p['acc'], 9, dash=True)
        text(d, (630, 1090), 'read again', 48, p['acc'], anchor='mm')
        boxed(d, (820, 1030, 1240, 1250), p, 'slicer', 'its own copy: 25', AMBER)
        caption(d, CAPX, 1075, ['the file is newer,', 'the copy is not:', 'ask it to read again'], p, 52, 68)
    save(im, f'card-copy-{step}.png')


# --- F3: where the hand-over folder is (overlay, right 40%) ------------------------------------------------------
FOLD = (1576, 150, 2520, 1250)
WIN_PATH = r'%LOCALAPPDATA%\SolidCraft\ '.rstrip()


def card_folders(step):
    im, d = overlay(FOLD)
    x, bx = FOLD[0] + 50, FOLD
    text(d, (x, 215), 'The hand-over folder', 60, INK, anchor='lm', box=bx)
    text(d, (x, 290), "from SolidCraft's code", 46, GREY, R, anchor='lm', box=bx)
    d.line((x, 335, FOLD[2] - 50, 335), fill=GREY, width=3)
    p = pal(1, step, BLUE)
    text(d, (x, 400), 'Linux', 56, p['ink'], anchor='lm', box=bx)
    tw = font(B, 56).getlength('Linux')
    d.rounded_rectangle((x + tw + 30, 368, x + tw + 210, 432), radius=16, fill=GREENFILL if step == 1 else DONEFILL,
                        outline=GREEN if step == 1 else DONE, width=4)
    text(d, (x + tw + 120, 400), 'filmed', 44, GREEN if step == 1 else DONE, anchor='mm', box=bx)
    text(d, (x, 475), '~/.cache/solidcraft/slicer', 48, p['acc'], MONO, anchor='lm', box=bx)
    if step >= 2:
        p = pal(2, step, BLUE)
        text(d, (x, 590), 'Windows', 56, p['ink'], anchor='lm', box=bx)
        text(d, (x, 665), WIN_PATH, 48, p['acc'], MONO, anchor='lm', box=bx)
        text(d, (x, 727), 'slicer', 48, p['acc'], MONO, anchor='lm', box=bx)
        text(d, (x, 800), 'a numbered copy while the', 46, p['sub'], R, anchor='lm', box=bx)
        text(d, (x, 858), 'slicer holds the file open', 46, p['sub'], R, anchor='lm', box=bx)
    if step >= 3:
        p = pal(3, step, BLUE)
        text(d, (x, 975), 'macOS', 56, p['ink'], anchor='lm', box=bx)
        text(d, (x, 1050), '~/Library/Caches/SolidCraft/', 48, p['acc'], MONO, anchor='lm', box=bx)
        text(d, (x, 1112), 'slicer', 48, p['acc'], MONO, anchor='lm', box=bx)
    save(im, f'card-folders-{step}.png')


# --- F6: the knock (a house with a door) -------------------------------------------------------------------------
def house(d, x, y, p, name, toggle=False, w=260):
    d.polygon([(x - 15, y + 100), (x + w / 2, y), (x + w + 15, y + 100)], fill=p['fill'], outline=p['ink'])
    d.line([(x - 15, y + 100), (x + w / 2, y), (x + w + 15, y + 100), (x - 15, y + 100)], fill=p['ink'], width=6)
    d.rectangle((x, y + 100, x + w, y + 280), fill=p['fill'], outline=p['ink'], width=6)
    d.rectangle((x + w - 100, y + 170, x + w - 30, y + 280), fill=WHITE, outline=p['ink'], width=5)
    if toggle:                                   # a switch, drawn off
        d.rounded_rectangle((x + 20, y + 125, x + 110, y + 170), radius=22, fill=WHITE, outline=p['ink'], width=4)
        d.ellipse((x + 26, y + 131, x + 60, y + 165), fill=p['ink'])
        text(d, (x + 65, y + 222), 'off', 44, p['acc'], anchor='mm')
    text(d, (x + w / 2, y + 315), name, 46, p['ink'], anchor='mm')


def card_knock(step):
    im, d = canvas(); header(d, 'Why a second window? Picture a house')
    p = pal(1, step, GREEN)                      # 1: SolidCraft knocks on PrusaSlicer's door
    boxed(d, (80, 300, 440, 460), p, 'SolidCraft')
    house(d, 640, 190, p, 'PrusaSlicer')
    arrow(d, (450, 410), (625, 410), p['acc'], 9)
    text(d, (535, 360), 'knock', 46, p['acc'], anchor='mm')
    text(d, (535, 460), 'the file', 46, p['acc'], R, anchor='mm')
    caption(d, CAPX, 290, ['PrusaSlicer, SuperSlicer,', 'Cura: the open window', 'takes the file'], p, 52, 70)
    if step >= 2:                                # 2: Orca and Bambu can answer, switch off at first
        p = pal(2, step, AMBER)
        house(d, 640, 600, p, 'OrcaSlicer', toggle=True)
        house(d, 1060, 600, p, 'Bambu Studio', toggle=True)
        text(d, (1190, 965), 'Bambu Studio: from its source', 44, p['sub'], R, anchor='mm')
        caption(d, CAPX, 690, ['OrcaSlicer, Bambu Studio', 'can answer too:', 'off at first'], p, 52, 70)
    if step >= 3:                                # 3: the real terminal line (take G)
        p = pal(3, step, RED)
        d.rounded_rectangle((80, 1030, 1200, 1240), radius=22, fill=p['fill'], outline=p['ink'], width=6)
        text(d, (120, 1080), 'the real terminal line:', 44, p['sub'], R, anchor='lm')
        text(d, (120, 1170), 'Invalid option --single-instance', 52, p['acc'], MONO, anchor='lm', maxw=1060)
        caption(d, CAPX, 1080, ['SolidCraft cannot', 'switch it on'], p, 52, 70)
    if step >= 4:                                # 4: no answer, a second house
        p = pal(4, step, RED)
        house(d, 1260, 1010, p, 'window 2', w=230)
        caption(d, CAPX, 1260, ['no answer:', 'a second window'], p, 52, 70)
    save(im, f'card-knock-{step}.png')


# --- F9: so far (overlay, left 50%) -------------------------------------------------------------------------------
SOFAR = (40, 170, 1240, 1110)
SOFAR_LINES = [['reproduced on screen,', 'not guessed'], ['one file, one name,', 'replaced every send'],
               ['the slicer keeps its own copy:', 'reload']]


def card_sofar(step):
    im, d = overlay(SOFAR)
    x = SOFAR[0] + 60
    text(d, (x, 250), 'So far', 66, INK, anchor='lm', box=SOFAR)
    for k, lines in enumerate(SOFAR_LINES[:step]):
        p = pal(k + 1, step, GREEN)
        y = 380 + k * 250
        d.ellipse((x, y - 20, x + 40, y + 20), fill=p['acc'])
        for i, ln in enumerate(lines):
            text(d, (x + 70, y + i * 80), ln, 60, p['ink'] if i == 0 else p['acc'], anchor='lm', box=SOFAR)
    save(im, f'card-sofar-{step}.png')


# --- F11: Claude's reply, typed on clause by clause (overlay, left 50%) ----------------------------------------
REPLY = (40, 170, 1240, 1250)
CLAUSES = ["I can't see the slicer window, so check what's on the plate",          # reply.txt, word for word
           'may still show the old 25 mm hook, possibly with the new one beside it',
           'delete the old one or use Reload from disk',
           'make sure the part measures 40 mm in X']


def card_reply(step):
    im, d = overlay(REPLY)
    x = REPLY[0] + 60
    text(d, (x, 245), 'reply, from the session log', 52, GREY, anchor='lm', box=REPLY)
    d.line((x, 295, REPLY[2] - 60, 295), fill=GREY, width=3)
    y = 370
    for k, cl in enumerate(CLAUSES[:step]):
        p = pal(k + 1, step)
        lines = wrap(('' if k == 0 else '... ') + cl, 54, R, REPLY[2] - REPLY[0] - 120)
        for ln in lines:
            text(d, (x, y), ln, 54, p['ink'], R, anchor='lm', box=REPLY)
            y += 72
        y += 40
    save(im, f'card-reply-{step}.png')


# --- F12: recap -----------------------------------------------------------------------------------------------------
RECAP = [['same file name: the file is replaced'],
         ['the slicer keeps its own copy:', 'delete the extra copy, Reload from disk'],
         ['OrcaSlicer: tick Allow only one instance'],
         ['never save over the hand-over file'],
         ['check the size boxes before you print']]


def card_recap(step):
    im, d = canvas(); header(d, 'Recap: a second hook, a second window')
    y = 200
    for k, lines in enumerate(RECAP[:step]):
        p = pal(k + 1, step, GREEN)
        h = 160 if len(lines) == 1 else 250
        d.rounded_rectangle((120, y, 2440, y + h), radius=26, fill=p['fill'], outline=p['ink'], width=6)
        text(d, (180, y + 80), f'{k + 1}', 68, p['acc'], anchor='lm')
        for i, ln in enumerate(lines):
            text(d, (280, y + 80 + i * 90), ln, 66, p['ink'] if i == 0 else p['acc'], anchor='lm', maxw=2120)
        y += h + 30
    save(im, f'card-recap-{step}.png')


# --- F13: the question (no answer on screen) ---------------------------------------------------------------------
def card_question():
    im, d = canvas(); header(d, 'Your turn: the question')
    text(d, (W / 2, 380), 'You send two different bodies,', 88, INK, anchor='mm', maxw=2300)
    text(d, (W / 2, 500), 'one after the other.', 88, INK, anchor='mm')
    text(d, (W / 2, 700), 'One file, or two?', 120, BLUE, anchor='mm')
    text(d, (W / 2, 900), 'How would you find out?', 96, INK, anchor='mm')
    d.rounded_rectangle((200, 1110, 2360, 1300), radius=26, fill=GREENFILL, outline=GREEN, width=8)
    text(d, (W / 2, 1205), 'Pause and think', 96, GREEN, anchor='mm')
    save(im, 'card-question.png')


def sheet(outdir):
    names = sorted(n for n in os.listdir(OUT) if n.endswith('.png'))
    tw, th, cols = 512, 288, 5
    rows = -(-len(names) // cols)
    sh = Image.new('RGB', (tw * cols, (th + 30) * rows), (90, 90, 90))
    dd = ImageDraw.Draw(sh)
    for i, n in enumerate(names):
        im = Image.open(os.path.join(OUT, n)).convert('RGBA')
        bg = Image.new('RGBA', im.size, (60, 70, 85, 255))     # dark ground shows the transparent area
        t = Image.alpha_composite(bg, im).convert('RGB').resize((tw - 8, th - 8))
        x, y = (i % cols) * tw, (i // cols) * (th + 30)
        sh.paste(t, (x + 4, y + 4))
        dd.text((x + 6, y + th), n, font=font(R, 22), fill=(255, 255, 255))
    sh.save(os.path.join(outdir, 'fx5-sheet.png'))
    print('sheet', len(names))


def check_alpha():
    for n in sorted(os.listdir(OUT)):
        if n.startswith(('card-folders', 'card-sofar', 'card-reply')):
            im = Image.open(os.path.join(OUT, n))
            box = {'card-folders': FOLD, 'card-sofar': SOFAR, 'card-reply': REPLY}[n.rsplit('-', 1)[0]]
            bb = im.getchannel('A').getbbox()
            if im.mode != 'RGBA' or bb[0] < box[0] or bb[2] > box[2] + 1 or bb[1] < box[1] or bb[3] > box[3] + 1:
                PROBLEMS.append(f'{n}: alpha bbox {bb}')


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'sheet':
        sheet(sys.argv[2])
        sys.exit(0)
    for s in (1, 2, 3):
        card_copy(s)
        card_folders(s)
        card_sofar(s)
    for s in (1, 2, 3, 4):
        card_knock(s)
        card_reply(s)
    for s in (1, 2, 3, 4, 5):
        card_recap(s)
    card_question()
    check_alpha()
    print('PROBLEMS:', PROBLEMS or 'none')
