"""Lesson 1's pictures, drawn from the lab's own files (no AI images): every SolidCraft picture is a crop of a real
capture in out/l1/ (the window filmed in Docker), every number and quote is read from a lab file. Cards are 1632 x 1200
(the split slide's picture box at 2x), text >= 56 px; the hook pictures are 2560 x 1440 and 1080 x 1920.
    docker run --rm --network none -v "$PWD:/work" -w /work cadcmp-openscad:2021.01 python3 video/draw.py
"""
import json
import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

LAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
L1 = os.path.join(LAB, 'out', 'l1')
F = os.path.join(LAB, 'video', 'frames')
os.makedirs(F, exist_ok=True)
FD = '/usr/share/fonts/truetype/dejavu/'
B, R, M = FD + 'DejaVuSans-Bold.ttf', FD + 'DejaVuSans.ttf', FD + 'DejaVuSansMono-Bold.ttf'
BG, INK, RED, GREEN, GREY, BLUE, PAPER, AMBER = (236, 239, 244), (31, 41, 55), (183, 28, 28), (27, 127, 59), \
    (110, 120, 138), (29, 78, 216), (255, 255, 255), (180, 110, 0)
W, H = 1632, 1200


def j(*p):
    return json.load(open(os.path.join(L1, *p), encoding='utf-8'))


def font(path, size):
    return ImageFont.truetype(path, size)


def canvas(w=W, h=H, bg=BG):
    im = Image.new('RGB', (w, h), bg)
    return im, ImageDraw.Draw(im)


def text(d, xy, s, size=60, fill=INK, path=B, anchor='la'):
    d.text(xy, s, font=font(path, size), fill=fill, anchor=anchor)


def fit_text(d, xy, s, maxw, size=72, fill=INK, path=B, anchor='la'):
    while font(path, size).getlength(s) > maxw and size > 30:
        size -= 2
    text(d, xy, s, size, fill, path, anchor)
    return size


def chip(d, xy, s, size=44, fg=PAPER, bg=INK, pad=18, anchor='l'):
    f = font(B, size)
    w = f.getlength(s)
    x, y = xy
    if anchor == 'r':
        x -= w + 2 * pad
    if anchor == 'm':
        x -= (w + 2 * pad) / 2
    d.rounded_rectangle((x, y, x + w + 2 * pad, y + size + 2 * pad), radius=18, fill=bg)
    d.text((x + pad, y + pad), s, font=f, fill=fg)
    return x + w + 2 * pad


def crop(path, box, w=None, h=None):
    im = Image.open(os.path.join(L1, path) if not os.path.isabs(path) else path).convert('RGB').crop(box)
    if w or h:
        r = min((w or 10 ** 6) / im.width, (h or 10 ** 6) / im.height)
        im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    return im


def paste(im, pic, xy, border=GREY):
    x, y = xy
    ImageDraw.Draw(im).rounded_rectangle((x - 6, y - 6, x + pic.width + 6, y + pic.height + 6), radius=14, fill=border)
    im.paste(pic, (x, y))


def circle(d, box, colour=RED, width=12):
    d.ellipse(box, outline=colour, width=width)


def save(im, name):
    im.save(os.path.join(F, name))
    print('wrote', name, im.size)


CUBE = os.path.join(LAB, 'video', 'footage', 'plug1-t26.png')     # the plug run's own footage, after the build
NOPLUG = j('runs', 'noplug-1', 'turns.json')['turns'][0]['result_text']
FIRST = NOPLUG.split('\n')[0].strip()
PLUG = j('runs', 'plug-1', 'turns.json')['turns']
TOOLS = j('tools.json')
REPLAY = j('replay.json')
MENU = j('menu', 'menu.json')
VOL = int(round(REPLAY['solidcraft_measure_volume_mm3']))
assert VOL == 8000 and REPLAY['our_checker']['volume_mm3'] == 8000.0 and TOOLS['count'] == 19
assert PLUG[0]['result_text'].startswith('Your SolidCraft design is empty.')
VOLS = f'{VOL:,}'


# ------------------------------------------------------------------------------------------------ the hook (F0, S0)
def wrap(d, xy, s, size, maxw, fill=INK, path=R, lead=1.3):
    x, y = xy
    line = ''
    for wd in s.split():
        if line and font(path, size).getlength(line + ' ' + wd) > maxw:
            text(d, (x, y), line, size, fill, path)
            y += int(size * lead)
            line = ''
        line = (line + ' ' + wd).strip()
    text(d, (x, y), line, size, fill, path)
    return y + int(size * lead)


def badge(d, right, top, size, sub):
    label = f'{VOLS} mm³'
    bw = font(B, size).getlength(label) + 70
    d.rounded_rectangle((right - bw, top, right, top + size + 56), radius=22, fill=GREEN)
    text(d, (right - bw / 2, top + 28 + size / 2), label, size, PAPER, anchor='mm')
    text(d, (right - bw / 2, top + size + 76), sub, int(size * 0.42), GREEN, anchor='ma')


def hook(w, h, vertical=False):
    """F0 / S0: left (top) Claude's real no-plug reply; right (bottom) the real window with the cube."""
    im, d = canvas(w, h, PAPER)
    k = w / 1632 if not vertical else 1.0
    if not vertical:
        mid = int(w * 0.44)
        d.rectangle((0, 0, mid, h), fill=(250, 243, 243))
        pad = int(50 * k)
        text(d, (pad, int(60 * k)), 'NO SETUP', int(84 * k), RED)
        y = wrap(d, (pad, int(190 * k)), '"' + FIRST + '"', int(46 * k), mid - 2 * pad)
        y += int(30 * k)
        for c in ('$ which solidcraft', '$ ls -la'):
            text(d, (pad, y), c, int(52 * k), GREY, M)
            y += int(80 * k)
        st = int(86 * k)
        while font(B, st).getlength('NOTHING RAN') + 60 * k > mid - 2 * pad:
            st -= 2
        sw = font(B, st).getlength('NOTHING RAN') + 60 * k
        sy = h - int(260 * k)
        d.rounded_rectangle((pad, sy, pad + sw, sy + st + 50 * k), radius=18, outline=RED, width=int(12 * k))
        text(d, (pad + sw / 2, sy + 25 * k + st / 2), 'NOTHING RAN', st, RED, anchor='mm')
        text(d, (mid + int(50 * k), int(60 * k)), 'AFTER SETUP', int(84 * k), GREEN)
        pic = crop(CUBE, (330, 60, 1450, 1000), w=w - mid - int(100 * k), h=h - int(220 * k))
        paste(im, pic, (mid + int(50 * k), int(180 * k)))
        badge(d, w - int(70 * k), h - int(330 * k), int(96 * k), 'SolidCraft measured it')
    else:
        half = int(h * 0.42)
        d.rectangle((0, 0, w, half), fill=(250, 243, 243))
        text(d, (60, 70), 'NO SETUP', 84, RED)
        y = wrap(d, (60, 190), '"' + FIRST + '"', 46, w - 120)
        y += 20
        for c in ('$ which solidcraft', '$ ls -la'):
            text(d, (60, y), c, 52, GREY, M)
            y += 76
        sw = font(B, 80).getlength('NOTHING RAN') + 60
        d.rounded_rectangle((w - 60 - sw, half - 170, w - 60, half - 40), radius=18, outline=RED, width=12)
        text(d, (w - 60 - sw / 2, half - 105), 'NOTHING RAN', 80, RED, anchor='mm')
        text(d, (60, half + 50), 'AFTER SETUP', 84, GREEN)
        pic = crop(CUBE, (380, 60, 1350, 1000), w=w - 80, h=h - half - 520)
        paste(im, pic, ((w - pic.width) // 2, half + 170))
        badge(d, w - 60, h - 380, 96, 'SolidCraft measured it')
    return im



save(hook(2560, 1440), 'hook-landscape.png')
save(hook(1080, 1920, vertical=True), 'hook-vertical.png')
im = hook(W, H)
save(im, 'card-hook.png')

# ------------------------------------------------------------------------------------------------ F2 two programs
im, d = canvas()
pic = crop(CUBE, (0, 30, 1600, 1000), w=1500, h=800)
paste(im, pic, ((W - pic.width) // 2, 60))
chip(d, (70, 90), 'SolidCraft · free · open source', 52)
d.rounded_rectangle((300, 900, 1330, 1130), radius=40, fill=PAPER, outline=BLUE, width=8)
text(d, (815, 1015), 'Claude: an AI you chat with', 64, BLUE, anchor='mm')
save(im, 'card-two.png')

# ------------------------------------------------------------------------------------------------ F8 tools
im, d = canvas()
text(d, (W // 2, 50), f'{TOOLS["count"]} tools', 150, INK, anchor='ma')
used = [('inspect_design', 'reads the design'), ('measure', 'measures'), ('execute', 'builds')]
y = 280
for name, what in used:
    d.rounded_rectangle((120, y, 1512, y + 150), radius=30, fill=PAPER, outline=GREEN, width=8)
    text(d, (170, y + 75), name, 66, GREEN, M, 'lm')
    text(d, (1460, y + 75), what, 58, INK, R, 'rm')
    y += 185
rest = [n for n in TOOLS['names'] if n not in dict(used)]
line, y = '', 870
for n in rest:
    if font(R, 38).getlength(line + '  ' + n) > 1400:
        text(d, (W // 2, y), line.strip(), 38, GREY, R, 'ma')
        y += 54
        line = ''
    line += '  ' + n
text(d, (W // 2, y), line.strip(), 38, GREY, R, 'ma')
chip(d, (W // 2, 1080), "from the plug's own list (tools/list)", 40, anchor='m')
save(im, 'card-tools.png')

# ------------------------------------------------------------------------------------------------ F11 step 0
im, d = canvas()
text(d, (W // 2, 70), 'Before you start', 96, INK, anchor='ma')
for i, s in enumerate(['Claude app installed', 'opened once', 'signed in']):
    y = 290 + i * 200
    d.rounded_rectangle((200, y, 1432, y + 150), radius=30, fill=PAPER, outline=GREEN, width=8)
    text(d, (270, y + 75), '✓', 90, GREEN, R, 'lm')
    text(d, (400, y + 75), s, 72, INK, B, 'lm')
text(d, (W // 2, 930), 'Claude Desktop: claude.com/download', 60, BLUE, anchor='ma')
chip(d, (W // 2, 1040), 'which plan: claude.com/download (link below)', 40, anchor='m')
save(im, 'card-step0.png')

# ------------------------------------------------------------------------------------------------ F12 download
im, d = canvas()
text(d, (60, 50), 'Step 1 / 3', 70, BLUE)
pic = crop(os.path.join(L1, 'sitecheck-windows', 'browser.png'), (30, 150, 780, 535), w=1500)  # badges below it
paste(im, pic, ((W - pic.width) // 2, 170))
d.rounded_rectangle((130, 1000, 790, 1130), radius=26, fill=PAPER, outline=GREEN, width=8)
text(d, (460, 1065), '✓ desktop app', 60, GREEN, anchor='mm')
d.rounded_rectangle((842, 1000, 1502, 1130), radius=26, fill=PAPER, outline=RED, width=8)
text(d, (1172, 1065), '✗ in a browser', 60, RED, anchor='mm')
text(d, (W - 60, 70), 'browser capture, 27 Oct 2026', 34, GREY, R, 'ra')
save(im, 'card-download.png')

# ------------------------------------------------------------------------------------------------ F13 signed
im, d = canvas()
chip(d, (60, 50), 'tested: 0.24.1', 56, bg=GREEN)
for i, (q, src) in enumerate([('"current Windows builds are', 'solidcraft.io/download, 27 Oct 2026'),
                              ('More info, then Run anyway', 'SolidCraft docs: downloads')]):
    y = 260 + i * 430
    d.rounded_rectangle((90, y, 1542, y + 360), radius=30, fill=PAPER, outline=GREY, width=4)
    if i == 0:
        text(d, (150, y + 60), q, 70, INK)
        text(d, (150, y + 150), 'not signed yet"', 70, INK)
    else:
        text(d, (150, y + 100), q, 76, BLUE)
    text(d, (150, y + 280), src, 40, GREY, R)
save(im, 'card-signed.png')

# ------------------------------------------------------------------------------------------------ F14/F15 top-right corner
def corner(src, mark):
    im, d = canvas()
    text(d, (60, 50), 'Step 2 / 3', 70, BLUE)
    box = (1000, 0, 1600, 60)
    pic = crop(src, box, w=1520)
    y0 = 300
    paste(im, pic, ((W - pic.width) // 2, y0))
    s = pic.width / (box[2] - box[0])
    x0 = (W - pic.width) // 2
    if mark == 'update':
        cx, r = x0 + (1110 - box[0]) * s, 125
    else:
        cx, r = x0 + (1269 - box[0]) * s, 70
    cy = y0 + 17 * s
    circle(d, (cx - r * 1.7, cy - r, cx + r * 1.7, cy + r) if mark == 'update' else (cx - r, cy - r, cx + r, cy + r))
    return im, d, cx, y0 + pic.height


# 27 Oct re-cut: the Update pill zoomed (it was unreadable on a phone)
im, d = canvas()
text(d, (60, 50), 'Step 2 / 3: an older copy?', 70, BLUE)
ubox = (1030, 0, 1330, 45)
ubar = crop(os.path.join(L1, 'update', 'title-60s.png'), ubox, w=1500)
paste(im, ubar, (66, 220))
su = ubar.width / (ubox[2] - ubox[0])
ucx, ucy = 66 + (1110 - ubox[0]) * su, 220 + 17 * su
circle(d, (ucx - 330, ucy - 120, ucx + 330, ucy + 120))
text(d, (W // 2, 620), 'an older copy (0.23.1) offers it', 56, INK, R, 'ma')
text(d, (W // 2, 720), 'click Update first', 70, RED, anchor='ma')
save(im, 'card-update.png')

# 27 Oct re-cut (watch-through gate): the click path zoomed, so the ? and the menu item read on a phone
im, d = canvas()
text(d, (60, 40), 'Step 2 / 3: one menu click', 70, BLUE)
MSRC = os.path.join(L1, 'menu', 'B-claude-installed-menu.png')
box = (1150, 0, 1430, 52)
text(d, (60, 140), '1  the round ?', 64, RED)
bar = crop(MSRC, box, w=1500)
sbar = bar.width / (box[2] - box[0])
paste(im, bar, (66, 230))
cxq, cyq, rq = 66 + (1269 - box[0]) * sbar, 230 + 17 * sbar, 100
circle(d, (cxq - rq, cyq - rq, cxq + rq, cyq + rq))
mbox = (1258, 160, 1506, 256)
menu = crop(MSRC, mbox, w=1100)
my = 230 + bar.height + 130
text(d, (60, my - 85), '2  near the bottom: Connect AI assistants', 56, RED)
paste(im, menu, (266, my))
ty = my + (236 - mbox[1]) * menu.width / (mbox[2] - mbox[0])
d.rounded_rectangle((250, ty - 58, 1382, ty + 58), radius=16, outline=RED, width=10)
save(im, 'card-menu.png')

# ------------------------------------------------------------------------------------------------ F16 connected
im, d = canvas()
dlg = crop(os.path.join(L1, 'menu', 'B-claude-installed-dialog.png'), (538, 338, 1062, 470), w=1500)
paste(im, dlg, ((W - dlg.width) // 2, 40))
y = 90 + dlg.height
for line in ('claude-desktop: added solidcraft', 'claude-code: added solidcraft'):
    d.rounded_rectangle((110, y, 1522, y + 120), radius=24, fill=PAPER, outline=GREEN, width=8)
    text(d, (W // 2, y + 60), line, 58, GREEN, M, 'mm')
    y += 150
chip(d, (W // 2, y + 10), 'filmed on Linux: your paths differ', 38, bg=GREY, anchor='m')
y += 120
d.rounded_rectangle((90, y, 800, y + 170), radius=24, fill=PAPER, outline=GREY, width=4)
text(d, (445, y + 50), "SolidCraft's docs:", 42, GREY, R, 'ma')
text(d, (445, y + 105), 'adds itself', 52, INK, anchor='ma')
d.rounded_rectangle((832, y, 1542, y + 170), radius=24, fill=PAPER, outline=RED, width=6)
text(d, (1187, y + 50), 'our test, 0.24.1:', 42, RED, R, 'ma')
text(d, (1187, y + 105), 'no entry after 60 s', 52, RED, anchor='ma')
save(im, 'card-connected.png')

# ------------------------------------------------------------------------------------------------ F17 the entry
e = MENU['claude_desktop']['entry']
im, d = canvas()
text(d, (60, 50), "Claude Desktop's settings file", 64, INK)
chip(d, (60, 140), 'example: our Linux test (your path differs)', 40, bg=RED)
rows = ['{', '  "mcpServers": {', '    "solidcraft": {', f'      "command": "{e["command"]}",',
        f'      "args": {json.dumps(e["args"])}', '    }', '  }', '}']
y = 250
for r in rows:
    col = BLUE if any(k in r for k in ('solidcraft":', 'command', 'args')) else INK
    fit_text(d, (90, y), r, 1460, 52, col, M)
    y += 78
chip(d, (60, 930), r'on Windows the file is in %APPDATA%\Claude', 48)
chip(d, (60, 1040), 'or: Settings > Developer > Edit Config', 48, bg=GREY)
save(im, 'card-entry.png')

# ------------------------------------------------------------------------------------------------ F18 quit
im, d = canvas()
text(d, (60, 50), 'Step 3 / 3: quit fully, reopen', 70, BLUE)
quotes = [('"Quit Claude Desktop completely (from', 'the notification area) and start it again"', 'SolidCraft docs: mcp.md'),
          ('"completely quit Claude Desktop', 'and restart it"', 'modelcontextprotocol.io')]
y = 200
for a, b2, src in quotes:
    d.rounded_rectangle((70, y, 1562, y + 300), radius=26, fill=PAPER, outline=GREY, width=4)
    fit_text(d, (120, y + 40), a, 1390, 54)
    fit_text(d, (120, y + 120), b2, 1390, 54)
    text(d, (120, y + 225), src, 38, GREY, R)
    y += 340
d.rounded_rectangle((70, y, 1562, y + 180), radius=26, fill=PAPER, outline=GREEN, width=6)
text(d, (120, y + 30), 'SolidCraft:', 40, GREY, R)
text(d, (120, y + 85), '"Restart each assistant"', 56, GREEN)
save(im, 'card-quit.png')

# ------------------------------------------------------------------------------------------------ F19 Claude Code
im, d = canvas()
text(d, (60, 50), 'Using Claude Code?', 80, INK)
d.rounded_rectangle((70, 220, 1562, 560), radius=24, fill=(24, 30, 40))
text(d, (110, 270), 'If solidcraft is missing:', 40, (160, 170, 185), R)
text(d, (110, 350), 'claude mcp add --scope user \\', 56, (230, 235, 240), M)
text(d, (110, 440), '  solidcraft -- solidcraft-cli mcp', 56, (230, 235, 240), M)
d.rounded_rectangle((70, 640, 1562, 790), radius=24, fill=PAPER, outline=GREEN, width=8)
text(d, (W // 2, 715), 'claude-code: added solidcraft', 58, GREEN, M, 'mm')
text(d, (W // 2, 880), 'then start a new session', 60, INK, anchor='ma')
chip(d, (W // 2, 1020), 'Claude Desktop users: skip', 48, bg=GREY, anchor='m')
save(im, 'card-code.png')

# ------------------------------------------------------------------------------------------------ F21 connectors
im, d = canvas()
text(d, (60, 40), 'Did it work? Where to click', 76, INK)
chip(d, (60, 140), "a sketch from Anthropic's help page, not a screenshot", 38, bg=GREY)
# the chat box, with the plus button circled
d.rounded_rectangle((90, 870, 1542, 1080), radius=40, fill=PAPER, outline=GREY, width=5)
d.rounded_rectangle((330, 955, 900, 995), radius=18, fill=(214, 219, 228))  # the text field (not drawn)
circle(d, (130, 905, 270, 1045))
text(d, (200, 975), '+', 96, BLUE, B, 'mm')
text(d, (300, 820), '1  the plus button, under the chat box', 48, RED, B, 'lm')
# the menu that opens above it, Connectors highlighted, solidcraft listed
d.rounded_rectangle((130, 250, 900, 760), radius=26, fill=PAPER, outline=GREY, width=4)
for i, item in enumerate(['', 'Connectors', '']):
    y = 300 + i * 150
    if item:
        d.rounded_rectangle((150, y - 20, 880, y + 110), radius=18, outline=RED, width=8)
        text(d, (200, y + 45), item, 58, INK, B, 'lm')
    else:
        d.rounded_rectangle((200, y + 30, 640, y + 62), radius=14, fill=(214, 219, 228))  # other items: not drawn
text(d, (950, 380), '2  Connectors', 48, RED, B, 'lm')
d.rounded_rectangle((950, 470, 1542, 620), radius=26, fill=(240, 247, 241), outline=GREEN, width=8)
text(d, (1000, 545), '✓ solidcraft', 60, GREEN, M, 'lm')
text(d, (950, 690), '3  look for solidcraft', 48, GREEN, B, 'lm')
save(im, 'card-connectors.png')

# ------------------------------------------------------------------------------------------------ F22 first request
im, d = canvas()
d.rounded_rectangle((90, 60, 1542, 220), radius=30, fill=PAPER, outline=BLUE, width=6)
text(d, (140, 140), "What's in my SolidCraft design?", 62, BLUE, B, 'lm')
d.rounded_rectangle((90, 290, 1542, 560), radius=26, fill=PAPER, outline=GREY, width=4)
text(d, (140, 330), '"Claude will request your approval"', 58, INK)
text(d, (140, 430), "from the MCP site's Filesystem example", 40, GREY, R)
text(d, (140, 485), 'allow it, or deny it', 44, INK, R)
d.rounded_rectangle((90, 630, 1542, 850), radius=30, fill=(240, 247, 241), outline=GREEN, width=6)
text(d, (140, 690), 'Claude:', 44, GREEN, R)
fit_text(d, (140, 760), '"' + PLUG[0]['result_text'].split('\n')[0].split('.')[0] + '."', 1360, 60, GREEN)
chip(d, (90, 940), 'our test: Claude Code 2.1.311 · approvals given in advance', 38, bg=GREY)
save(im, 'card-first.png')

# ------------------------------------------------------------------------------------------------ F24 the cube, measured
im, d = canvas()
pic = crop(CUBE, (250, 40, 1500, 1000), w=1040, h=800)
paste(im, pic, (60, 60))
x = 60 + pic.width + 50
text(d, (x, 120), 'measure', 60, GREY, M)
text(d, (x, 230), VOLS, 120, GREEN)
text(d, (x, 380), 'mm³', 80, GREEN)
text(d, (x, 560), '20 × 20 × 20', 50, INK, R)
text(d, (x, 640), f'= {VOLS}', 60, INK)
chip(d, (60, 950), f'replayed in a fresh copy: {VOLS} again · our STL checker: {VOLS}', 38, bg=GREY)
chip(d, (60, 1060), 'our test: Claude Code 2.1.311 · approvals given in advance', 38, bg=GREY)
save(im, 'card-cube.png')

# 27 Oct re-cut: the cube as it appears, before anyone asks for a measurement
im, d = canvas()
pic = crop(CUBE, (250, 40, 1500, 1000), w=1100, h=860)
paste(im, pic, (60, 60))
x = 60 + pic.width + 60
text(d, (x, 200), 'a 20 mm', 64, INK)
text(d, (x, 290), 'cube', 64, INK)
text(d, (x, 470), 'next:', 52, GREY, R)
text(d, (x, 550), '"measure', 56, BLUE)
text(d, (x, 630), 'it"', 56, BLUE)
chip(d, (60, 1010), 'frame from the run\'s own recording (filmed on Linux)', 38, bg=GREY)
save(im, 'card-cube-plain.png')

# ------------------------------------------------------------------------------------------------ F25 your check
im, d = canvas()
text(d, (W // 2, 60), 'Your check', 96, INK, anchor='ma')
for i, p in enumerate(["What's in my SolidCraft design?", 'Make a 20 mm cube in SolidCraft.', 'Measure it.']):
    y = 230 + i * 170
    d.rounded_rectangle((110, y, 1522, y + 130), radius=30, fill=PAPER, outline=BLUE, width=6)
    text(d, (160, y + 65), f'{i + 1}', 64, BLUE, B, 'mm')
    fit_text(d, (230, y + 65), p, 1240, 60, INK, B, 'lm')
d.rounded_rectangle((110, 770, 1522, 950), radius=30, fill=(240, 247, 241), outline=GREEN, width=8)
text(d, (W // 2, 860), f'look for {VOLS} (or 8000.0)', 70, GREEN, anchor='mm')
text(d, (W // 2, 1020), 'keep SolidCraft open  ·  pause and try it', 52, INK, R, 'ma')
save(im, 'card-check.png')

# ------------------------------------------------------------------------------------------------ F26 what the plug can reach
im, d = canvas()
text(d, (60, 50), 'What the plug can reach', 76, INK)
rows = [('your user folder', INK, 0), ('designs (the open design)  ✓', GREEN, 1), ("SolidCraft's own folders  ✓", GREEN, 1),
        ('folders you add  ✓', GREEN, 1), ('.ssh  .config  (hidden)  ✗', GREY, 1)]
y = 220
for s, c, ind in rows:
    x = 110 + ind * 110
    if ind:
        d.line((150, y - 40, 150, y + 50), fill=GREY, width=6)
        d.line((150, y + 50, x - 15, y + 50), fill=GREY, width=6)
    d.rounded_rectangle((x, y, x + font(B, 58).getlength(s) + 60, y + 100), radius=20, fill=PAPER,
                        outline=c, width=6)
    text(d, (x + 30, y + 50), s, 58, c, B, 'lm')
    y += 160
chip(d, (110, 1050), 'the plug: this computer only', 46)
save(im, 'card-reach.png')

# ------------------------------------------------------------------------------------------------ F27/F28 fixes
im, d = canvas()
text(d, (60, 40), 'No solidcraft in Connectors?', 70, INK)
d.rounded_rectangle((70, 150, 1562, 270), radius=24, fill=PAPER, outline=BLUE, width=6)
text(d, (120, 210), '☐  clicked Connect AI assistants?', 58, BLUE, B, 'lm')
dlg = crop(os.path.join(L1, 'menu', 'A-no-claude-dialog.png'), (538, 338, 1062, 470), w=1500)  # zoomed (27 Oct)
paste(im, dlg, ((W - dlg.width) // 2, 300))
y = 340 + dlg.height
d.rounded_rectangle((70, y, 1562, y + 110), radius=24, fill=(250, 243, 243), outline=RED, width=6)
text(d, (W // 2, y + 55), 'no supported client found', 58, RED, M, 'mm')
y += 140
for s, c in (('install Claude, open it, sign in', INK), ('click Connect AI assistants again', INK), ('restart Claude', INK)):
    text(d, (110, y), '→ ' + s, 50, c)
    y += 74
text(d, (110, y + 10), 'not fully quit? quit, reopen', 46, GREY)
text(d, (W - 70, y + 20), 'modelcontextprotocol.io, troubleshooting', 30, GREY, R, 'ra')
save(im, 'card-fix.png')

# ------------------------------------------------------------------------------------------------ F29 recap
im, d = canvas()
text(d, (W // 2, 50), 'Remember the picture', 84, INK, anchor='ma')
for i, (peg, s) in enumerate([('cloud', 'Claude thinks in the cloud'), ('workshop', 'SolidCraft: the workshop on your desk'),
                              ('plug', 'the plug carries each tool call')]):
    y = 230 + i * 210
    d.rounded_rectangle((90, y, 1542, y + 170), radius=30, fill=PAPER, outline=BLUE, width=6)
    text(d, (140, y + 85), peg, 66, BLUE, B, 'lm')
    fit_text(d, (560, y + 85), s, 940, 54, INK, R, 'lm')
d.rounded_rectangle((300, 900, 1332, 1080), radius=30, fill=GREEN)
text(d, (W // 2, 990), f'{VOLS} mm³ = proof', 78, PAPER, anchor='mm')
save(im, 'card-recap.png')
# ------------------------------------------------------------------------------------------------ F1 the setup, counted
im, d = canvas()
text(d, (W // 2, 60), 'Setup', 110, INK, anchor='ma')
for i, st in enumerate(['install SolidCraft', 'one menu click', 'one restart']):
    y = 260 + i * 210
    d.rounded_rectangle((180, y, 1452, y + 170), radius=34, fill=PAPER, outline=BLUE, width=8)
    text(d, (260, y + 85), str(i + 1), 90, BLUE, B, 'mm')
    text(d, (360, y + 85), st, 76, INK, B, 'lm')
d.rounded_rectangle((120, 920, 1512, 1100), radius=34, fill=(240, 247, 241), outline=GREEN, width=8)
text(d, (W // 2, 1010), 'first: a Claude app on your computer', 62, GREEN, anchor='mm')
save(im, 'card-steps.png')
print('done')
