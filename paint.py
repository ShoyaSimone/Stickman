"""Crude MS-Paint style drawing primitives (deliberately wobbly and messy)."""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (237, 28, 36)
GREEN = (34, 177, 76)
DGREEN = (0, 120, 40)
BLUE = (63, 72, 204)
LBLUE = (153, 217, 234)
YELLOW = (255, 242, 0)
ORANGE = (255, 127, 39)
BROWN = (136, 86, 40)
GREY = (160, 160, 160)
DGREY = (90, 90, 90)
PURPLE = (163, 73, 164)
PINK = (255, 174, 201)
TAN = (239, 228, 176)
NAVY = (20, 20, 70)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_fonts = {}


def font(size):
    if size not in _fonts:
        _fonts[size] = ImageFont.truetype(FONT_PATH, size)
    return _fonts[size]


class Canvas:
    def __init__(self, seed=0, bg=WHITE):
        random.seed(seed)
        self.img = Image.new("RGB", (W, H), bg)
        self.d = ImageDraw.Draw(self.img)

    # ---- basic wobbly stuff ----
    def j(self, a=3):
        return random.uniform(-a, a)

    def line(self, pts, w=4, c=BLACK, wob=2.5):
        out = []
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            n = max(2, int(math.hypot(x2 - x1, y2 - y1) / 25))
            for i in range(n):
                t = i / n
                out.append((x1 + (x2 - x1) * t + self.j(wob), y1 + (y2 - y1) * t + self.j(wob)))
        out.append((pts[-1][0] + self.j(wob), pts[-1][1] + self.j(wob)))
        self.d.line(out, fill=c, width=w, joint="curve")

    def poly(self, pts, fill=None, w=4, c=BLACK, wob=2.5):
        if fill:
            self.d.polygon([(x + self.j(1.5), y + self.j(1.5)) for x, y in pts], fill=fill)
        self.line(list(pts) + [pts[0]], w=w, c=c, wob=wob)

    def rect(self, x1, y1, x2, y2, fill=None, w=4, c=BLACK):
        self.poly([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], fill=fill, w=w, c=c)

    def ellipse(self, cx, cy, rx, ry, fill=None, w=4, c=BLACK, wob=2.0):
        n = 28
        pts = []
        start = random.uniform(0, 6.28)
        for i in range(n):
            a = start + 2 * math.pi * i / n
            pts.append((cx + rx * math.cos(a) + self.j(wob), cy + ry * math.sin(a) + self.j(wob)))
        if fill:
            self.d.polygon(pts, fill=fill)
        # overshoot slightly like a rushed hand
        pts2 = pts + [pts[0], (pts[1][0] + self.j(4), pts[1][1] + self.j(4))]
        self.d.line(pts2, fill=c, width=w, joint="curve")

    def circle(self, cx, cy, r, **k):
        self.ellipse(cx, cy, r, r, **k)

    def scribble(self, x1, y1, x2, y2, c=BLACK, w=3, n=10):
        """messy scribble-fill inside a box"""
        pts = []
        for i in range(n):
            pts.append((random.uniform(x1, x2), y1 + (y2 - y1) * i / n))
        self.d.line(pts, fill=c, width=w)

    def text(self, x, y, s, size=40, c=BLACK, center=True):
        f = font(size)
        widths = [f.getbbox(ch)[2] if ch != " " else size * 0.35 for ch in s]
        total = sum(widths) + len(s) * 1
        cx = x - total / 2 if center else x
        for ch, wd in zip(s, widths):
            if ch != " ":
                tile = Image.new("RGBA", (size * 2, size * 2), (0, 0, 0, 0))
                ImageDraw.Draw(tile).text((size * 0.5, size * 0.3), ch, font=f, fill=c)
                tile = tile.rotate(random.uniform(-9, 9), resample=Image.NEAREST)
                self.img.paste(tile, (int(cx - size * 0.5 + self.j(1.5)), int(y - size * 0.3 - size * 0.5 + self.j(3))), tile)
            cx += wd + 1

    def arrow(self, x1, y1, x2, y2, c=BLACK, w=5):
        self.line([(x1, y1), (x2, y2)], w=w, c=c)
        a = math.atan2(y2 - y1, x2 - x1)
        L = 28
        for da in (2.6, -2.6):
            self.line([(x2, y2), (x2 + L * math.cos(a + da), y2 + L * math.sin(a + da))], w=w, c=c)

    def bubble(self, x, y, w, h, s, size=34, tail=(None, None)):
        self.ellipse(x, y, w / 2, h / 2, fill=WHITE, w=3)
        if tail[0] is not None:
            self.line([(x - w * 0.15, y + h * 0.4), tail, (x + w * 0.05, y + h * 0.45)], w=3)
        self.text(x, y - size * 0.1, s, size=size)

    def thought(self, x, y, w, h, s="", size=34, tail=(None, None)):
        self.ellipse(x, y, w / 2, h / 2, fill=WHITE, w=3)
        if tail[0] is not None:
            tx, ty = tail
            for i, r in enumerate((14, 10, 6)):
                f = (i + 1) / 4
                self.circle(x + (tx - x) * f, y + h / 2 * 0.9 + (ty - y - h / 2) * f, r, fill=WHITE, w=3)
        if s:
            self.text(x, y - size * 0.1, s, size=size)

    def save(self, path):
        self.img.save(path)

    # ---- characters ----
    def stick(self, x, y, s=1.0, mood="neutral", arms="down", legs="stand", c=BLACK,
              hat=None, tie=None, sweat=False, face_dir=0):
        """x,y = feet center. ~200px tall at s=1"""
        w = max(3, int(5 * s))
        hr = 28 * s
        hy = y - 200 * s + hr
        neck = hy + hr
        hip = y - 80 * s
        self.circle(x, hy, hr, fill=WHITE, w=w)
        self.line([(x, neck), (x, hip)], w=w, c=c)
        # legs
        if legs == "stand":
            self.line([(x, hip), (x - 30 * s, y)], w=w, c=c)
            self.line([(x, hip), (x + 30 * s, y)], w=w, c=c)
        elif legs == "walk":
            self.line([(x, hip), (x - 45 * s, y)], w=w, c=c)
            self.line([(x, hip), (x + 20 * s, y - 40 * s), (x + 40 * s, y)], w=w, c=c)
        elif legs == "sit":
            self.line([(x, hip), (x + 50 * s, hip), (x + 50 * s, y)], w=w, c=c)
            self.line([(x, hip), (x + 45 * s, hip + 5 * s), (x + 40 * s, y)], w=w, c=c)
        sh = neck + 25 * s
        A = {
            "down": [(-35, 70), (35, 70)],
            "up": [(-45, -60), (45, -60)],
            "shrug": [(-50, -10, -60, -40), (50, -10, 60, -40)],
            "point_r": [(-30, 70), (85, -5)],
            "point_l": [(-85, -5), (30, 70)],
            "wave": [(-35, 70), (45, -70)],
            "hips": [(-40, 30, -10, 55), (40, 30, 10, 55)],
            "hold": [(-45, 25), (45, 25)],
            "head": [(-40, -20, -15, -55), (40, -20, 15, -55)],
            "out": [(-80, 10), (80, 10)],
            "raise_r": [(-35, 70), (40, -80)],
            "give_r": [(-35, 70), (80, 15)],
            "think": [(-35, 70), (30, 20, 8, -25)],
        }[arms]
        for arm in A:
            if len(arm) == 2:
                self.line([(x, sh), (x + arm[0] * s, sh + arm[1] * s)], w=w, c=c)
            else:
                self.line([(x, sh), (x + arm[0] * s, sh + arm[1] * s), (x + arm[2] * s, sh + arm[3] * s)], w=w, c=c)
        # face
        fx = x + face_dir * 8 * s
        ew = max(3, int(4 * s))
        ey = hy - 6 * s
        if mood == "sleep":
            self.line([(fx - 14 * s, ey), (fx - 5 * s, ey)], w=ew)
            self.line([(fx + 5 * s, ey), (fx + 14 * s, ey)], w=ew)
        else:
            for ex in (fx - 10 * s, fx + 10 * s):
                self.d.ellipse([ex - 3 * s, ey - 3 * s, ex + 3 * s, ey + 3 * s], fill=BLACK)
        my = hy + 11 * s
        if mood in ("happy", "rich"):
            self.line([(fx - 13 * s, my - 3 * s), (fx, my + 7 * s), (fx + 13 * s, my - 3 * s)], w=ew)
        elif mood in ("sad", "tired"):
            self.line([(fx - 12 * s, my + 6 * s), (fx, my - 3 * s), (fx + 12 * s, my + 6 * s)], w=ew)
        elif mood == "shock":
            self.circle(fx, my + 2 * s, 6 * s, w=ew)
        elif mood == "angry":
            self.line([(fx - 12 * s, my + 3 * s), (fx + 12 * s, my + 3 * s)], w=ew)
            self.line([(fx - 16 * s, ey - 12 * s), (fx - 4 * s, ey - 6 * s)], w=ew)
            self.line([(fx + 16 * s, ey - 12 * s), (fx + 4 * s, ey - 6 * s)], w=ew)
        elif mood == "sleep":
            self.text(x + 50 * s, hy - 50 * s, "z z", size=int(30 * s))
        else:
            self.line([(fx - 10 * s, my + 2 * s), (fx + 10 * s, my + 2 * s)], w=ew)
        if mood == "tired":
            for ex in (fx - 10 * s, fx + 10 * s):
                self.line([(ex - 6 * s, ey + 7 * s), (ex + 6 * s, ey + 7 * s)], w=2, c=PURPLE)
        if sweat or mood == "shock":
            self.d.polygon([(x + hr + 4, hy - 10 * s), (x + hr - 2, hy + 4 * s), (x + hr + 10, hy + 4 * s)], fill=LBLUE)
        if hat == "cap":
            self.poly([(x - hr, hy - hr * 0.5), (x + hr, hy - hr * 0.5), (x + hr * 1.7, hy - hr * 0.35), (x + hr * 0.6, hy - hr * 1.1), (x - hr * 0.8, hy - hr * 0.9)], fill=RED, w=3)
        elif hat == "top":
            self.rect(x - hr * 0.7, hy - hr * 2.1, x + hr * 0.7, hy - hr * 0.8, fill=BLACK, w=3)
            self.line([(x - hr * 1.2, hy - hr * 0.8), (x + hr * 1.2, hy - hr * 0.8)], w=5)
        elif hat == "officer":
            self.poly([(x - hr * 1.1, hy - hr * 0.6), (x + hr * 1.1, hy - hr * 0.6), (x + hr * 0.8, hy - hr * 1.3), (x - hr * 0.8, hy - hr * 1.3)], fill=NAVY, w=3)
            self.circle(x, hy - hr * 0.95, 4 * s, fill=YELLOW, w=2)
        if tie:
            self.poly([(x, neck + 3), (x - 7 * s, neck + 25 * s), (x, neck + 45 * s), (x + 7 * s, neck + 25 * s)], fill=tie, w=2)
        return dict(head=(x, hy), hr=hr, sh=sh, s=s)

    # ---- objects ----
    def truck(self, x, y, s=1.0, cargo=GREEN, face=False, rotten=False, flip=False):
        """x,y = bottom-left of wheels baseline"""
        def X(v):
            return x + (v if not flip else 380 - v) * s

        def Y(v):
            return y - v * s
        self.poly([(X(0), Y(40)), (X(260), Y(40)), (X(260), Y(190)), (X(0), Y(190))], fill=cargo, w=5)
        self.poly([(X(265), Y(40)), (X(370), Y(40)), (X(370), Y(110)), (X(335), Y(160)), (X(265), Y(160))], fill=RED, w=5)
        self.poly([(X(280), Y(110)), (X(325), Y(110)), (X(345), Y(140)), (X(280), Y(140))], fill=LBLUE, w=3)
        for wx in (50, 200, 320):
            self.circle(X(wx), Y(30), 30 * s, fill=DGREY, w=5)
            self.circle(X(wx), Y(30), 10 * s, fill=GREY, w=3)
        if face:
            self.circle(X(300), Y(126), 10 * s, fill=WHITE, w=3)
            self.d.ellipse([X(300) - 4, Y(126) - 4, X(300) + 4, Y(126) + 4], fill=BLACK)
        if rotten:
            for i in range(5):
                bx = X(30 + i * 45)
                self.line([(bx, Y(200)), (bx + 10, Y(220)), (bx - 5, Y(240)), (bx + 8, Y(260))], w=3, c=GREEN)
        return (X(0), Y(190), X(370), Y(0))

    def moon(self, x, y, r=45):
        self.circle(x, y, r, fill=YELLOW, w=3)
        self.circle(x + r * 0.45, y - r * 0.25, r * 0.85, fill=WHITE, w=0, c=WHITE)

    def night(self):
        """crude dark sky band at top (still mostly white page)"""
        self.moon(1150, 90)
        for _ in range(9):
            sx, sy = random.uniform(60, 1050), random.uniform(30, 160)
            self.star(sx, sy, 10)

    def star(self, x, y, r=10, c=BLACK):
        self.line([(x - r, y), (x + r, y)], w=3, c=c)
        self.line([(x, y - r), (x, y + r)], w=3, c=c)

    def ground(self, y=620, x1=0, x2=W):
        self.line([(x1, y), (x2, y)], w=4)

    def barrier(self, x, y, s=1.0, closed=True):
        self.rect(x - 15 * s, y - 120 * s, x + 15 * s, y, fill=GREY, w=4)
        if closed:
            for i in range(6):
                c = RED if i % 2 == 0 else WHITE
                bx = x + 15 * s + i * 45 * s
                self.poly([(bx, y - 110 * s), (bx + 45 * s, y - 110 * s), (bx + 45 * s, y - 90 * s), (bx, y - 90 * s)], fill=c, w=3)
        else:
            self.line([(x, y - 110 * s), (x + 60 * s, y - 330 * s)], w=int(16 * s), c=RED)

    def booth(self, x, y, s=1.0, label="BORDER"):
        self.rect(x, y - 220 * s, x + 170 * s, y, fill=TAN, w=4)
        self.poly([(x - 20 * s, y - 220 * s), (x + 190 * s, y - 220 * s), (x + 85 * s, y - 280 * s)], fill=BROWN, w=4)
        self.rect(x + 30 * s, y - 180 * s, x + 140 * s, y - 110 * s, fill=LBLUE, w=3)
        self.text(x + 85 * s, y - 70 * s, label, size=int(26 * s))

    def doc(self, x, y, s=1.0, stamp=None, title=None, fill=WHITE, lines=5, sig=False):
        """x,y = top-left"""
        w, h = 130 * s, 170 * s
        self.poly([(x, y), (x + w - 25 * s, y), (x + w, y + 25 * s), (x + w, y + h), (x, y + h)], fill=fill, w=3)
        self.line([(x + w - 25 * s, y), (x + w - 25 * s, y + 25 * s), (x + w, y + 25 * s)], w=3)
        top = y + 30 * s
        if title:
            self.text(x + w / 2, y + 18 * s, title, size=int(20 * s))
            top = y + 50 * s
        for i in range(lines):
            ly = top + i * 20 * s
            if ly > y + h - 20 * s:
                break
            self.line([(x + 15 * s, ly), (x + w - random.uniform(20, 45) * s, ly)], w=2, c=DGREY, wob=1)
        if sig:
            sx, sy = x + 20 * s, y + h - 25 * s
            self.line([(sx, sy), (sx + 15 * s, sy - 15 * s), (sx + 25 * s, sy + 5 * s), (sx + 45 * s, sy - 12 * s), (sx + 70 * s, sy)], w=3, c=BLUE)
        if stamp:
            self.circle(x + w * 0.65, y + h * 0.7, 30 * s, w=4, c=stamp)
            self.text(x + w * 0.65, y + h * 0.7 - 10 * s, "OK" if stamp == GREEN else "X", size=int(22 * s), c=stamp)

    def stack_docs(self, x, y, n=8, s=0.7):
        for i in range(n):
            self.doc(x + random.uniform(-25, 25), y - i * 22, s=s, lines=3)

    def clock(self, x, y, r=60, h=2):
        self.circle(x, y, r, fill=WHITE, w=4)
        for i in range(12):
            a = i * math.pi / 6
            self.line([(x + r * 0.8 * math.cos(a), y + r * 0.8 * math.sin(a)), (x + r * 0.9 * math.cos(a), y + r * 0.9 * math.sin(a))], w=2, wob=0.5)
        a = -math.pi / 2 + h * math.pi / 6
        self.line([(x, y), (x + r * 0.5 * math.cos(a), y + r * 0.5 * math.sin(a))], w=5)
        self.line([(x, y), (x, y - r * 0.75)], w=3)

    def calendar(self, x, y, s=1.0, crossed=6):
        self.rect(x, y, x + 220 * s, y + 200 * s, fill=WHITE, w=4)
        self.rect(x, y, x + 220 * s, y + 45 * s, fill=RED, w=4)
        self.text(x + 110 * s, y + 10 * s, "DAYS", size=int(26 * s), c=WHITE)
        k = 0
        for r in range(3):
            for col in range(4):
                cx = x + 30 * s + col * 52 * s
                cy = y + 75 * s + r * 45 * s
                self.text(cx, cy - 12 * s, str(k + 1), size=int(20 * s))
                if k < crossed:
                    self.line([(cx - 18 * s, cy - 15 * s), (cx + 18 * s, cy + 15 * s)], w=4, c=RED)
                    self.line([(cx + 18 * s, cy - 15 * s), (cx - 18 * s, cy + 15 * s)], w=4, c=RED)
                k += 1

    def tomato(self, x, y, r=22, rotten=False):
        self.circle(x, y, r, fill=BROWN if rotten else RED, w=3)
        self.line([(x - 8, y - r), (x, y - r - 8), (x + 8, y - r)], w=3, c=DGREEN)
        if rotten:
            self.d.ellipse([x - 6, y - 4, x + 4, y + 6], fill=DGREEN)

    def banana(self, x, y, s=1.0):
        self.poly([(x, y), (x + 60 * s, y + 30 * s), (x + 110 * s, y), (x + 100 * s, y + 20 * s), (x + 60 * s, y + 45 * s), (x + 5 * s, y + 15 * s)], fill=YELLOW, w=3)

    def fly(self, x, y):
        self.d.ellipse([x - 4, y - 3, x + 4, y + 3], fill=BLACK)
        self.ellipse(x - 5, y - 6, 5, 4, w=2)
        self.ellipse(x + 5, y - 6, 5, 4, w=2)

    def stink(self, x, y, n=3):
        for i in range(n):
            bx = x + i * 30
            self.line([(bx, y), (bx + 10, y - 20), (bx - 5, y - 40), (bx + 8, y - 60)], w=3, c=GREEN)

    def crate(self, x, y, s=1.0, produce=True, rotten=False):
        self.rect(x, y - 70 * s, x + 110 * s, y, fill=TAN, w=4)
        self.line([(x, y - 35 * s), (x + 110 * s, y - 35 * s)], w=3)
        if produce:
            for i in range(4):
                self.tomato(x + 18 * s + i * 25 * s, y - 75 * s, 15 * s, rotten=rotten)

    def africa(self, cx, cy, s=1.0, fill=TAN, w=4):
        P = [(-60, -230), (20, -235), (60, -200), (95, -195), (130, -150), (175, -100), (210, -95), (190, -50),
             (150, 0), (145, 60), (115, 110), (100, 170), (60, 215), (20, 225), (0, 180), (-20, 120), (-30, 60),
             (-45, 20), (-90, -10), (-150, -20), (-190, -60), (-195, -120), (-160, -190), (-110, -215)]
        pts = [(cx + px * s, cy + py * s) for px, py in P]
        self.poly(pts, fill=fill, w=w)
        # madagascar
        self.ellipse(cx + 170 * s, cy + 110 * s, 12 * s, 35 * s, fill=fill, w=3)
        return pts

    # handy named points on africa (relative coords, scale-able)
    AFR = {
        "westcoast": (-180, -80), "ghana": (-95, -25), "nigeria": (-40, -40), "kenya": (140, 5),
        "egypt": (80, -190), "southafrica": (40, 190), "congo": (20, 40), "senegal": (-185, -90),
        "mali": (-100, -110), "ethiopia": (150, -60), "sudan": (70, -110), "angola": (20, 100),
        "zambia": (60, 100), "tanzania": (110, 50), "morocco": (-120, -200), "algeria": (-40, -170),
        "chad": (10, -100), "eastcoast": (190, -40),
    }

    def apt(self, cx, cy, s, name):
        px, py = self.AFR[name]
        return (cx + px * s, cy + py * s)

    def pin(self, x, y, c=RED, r=14):
        self.d.polygon([(x - r * 0.7, y - r * 1.4), (x + r * 0.7, y - r * 1.4), (x, y)], fill=c)
        self.circle(x, y - r * 1.7, r, fill=c, w=3)
        self.line([(x - r * 0.7, y - r * 1.4), (x, y), (x + r * 0.7, y - r * 1.4)], w=3)

    def globe(self, x, y, r=110):
        self.circle(x, y, r, fill=LBLUE, w=4)
        self.poly([(x - r * 0.6, y - r * 0.5), (x - r * 0.2, y - r * 0.6), (x - r * 0.1, y - r * 0.2), (x - r * 0.4, y + r * 0.1), (x - r * 0.7, y - r * 0.1)], fill=GREEN, w=3)
        self.poly([(x + r * 0.1, y - r * 0.1), (x + r * 0.5, y - r * 0.2), (x + r * 0.6, y + r * 0.3), (x + r * 0.2, y + r * 0.7), (x + r * 0.05, y + r * 0.3)], fill=GREEN, w=3)

    def money_bag(self, x, y, s=1.0):
        self.ellipse(x, y, 70 * s, 65 * s, fill=TAN, w=4)
        self.poly([(x - 25 * s, y - 60 * s), (x + 25 * s, y - 60 * s), (x + 35 * s, y - 95 * s), (x - 35 * s, y - 95 * s)], fill=TAN, w=4)
        self.line([(x - 28 * s, y - 62 * s), (x + 28 * s, y - 62 * s)], w=5, c=BROWN)
        self.text(x, y - 30 * s, "$", size=int(60 * s), c=DGREEN)

    def bill(self, x, y, s=1.0, rot=0):
        w, h = 110 * s, 55 * s
        a = math.radians(rot)
        corners = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
        pts = [(x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)) for px, py in corners]
        self.poly(pts, fill=GREEN, w=3)
        self.circle(x, y, 14 * s, fill=WHITE, w=2)
        self.text(x, y - 12 * s, "$", size=int(20 * s), c=DGREEN)

    def coin(self, x, y, r=25, sym="$"):
        self.circle(x, y, r, fill=YELLOW, w=3)
        self.text(x, y - r * 0.55, sym, size=int(r * 1.1), c=BROWN)

    def flag(self, x, y, colors=(GREEN, YELLOW, RED), s=1.0, vertical=True):
        self.line([(x, y), (x, y - 200 * s)], w=5, c=BROWN)
        fw, fh = 120 * s, 80 * s
        top = y - 200 * s
        if vertical:
            for i, c in enumerate(colors):
                self.rect(x + i * fw / 3, top, x + (i + 1) * fw / 3, top + fh, fill=c, w=3)
        else:
            for i, c in enumerate(colors):
                self.rect(x, top + i * fh / 3, x + fw, top + (i + 1) * fh / 3, fill=c, w=3)

    def building(self, x, y, w=160, h=200, fill=TAN, label=None, roof=None, windows=True):
        self.rect(x, y - h, x + w, y, fill=fill, w=4)
        if roof == "tri":
            self.poly([(x - 15, y - h), (x + w + 15, y - h), (x + w / 2, y - h - 60)], fill=RED, w=4)
        elif roof == "bank":
            self.poly([(x - 20, y - h), (x + w + 20, y - h), (x + w / 2, y - h - 55)], fill=GREY, w=4)
            for i in range(4):
                px = x + 20 + i * (w - 40) / 3
                self.line([(px, y - h + 10), (px, y - 10)], w=7, c=DGREY)
        if windows and roof != "bank":
            for r in range(2):
                for col in range(2):
                    wx = x + 25 + col * (w / 2)
                    wy = y - h + 25 + r * 60
                    self.rect(wx, wy, wx + w / 4, wy + 35, fill=LBLUE, w=3)
        if label:
            self.text(x + w / 2, y - h - (75 if roof == "tri" else 70 if roof == "bank" else 45), label, size=30)

    def factory(self, x, y, s=1.0, label=None):
        self.rect(x, y - 140 * s, x + 220 * s, y, fill=GREY, w=4)
        self.poly([(x, y - 140 * s), (x + 55 * s, y - 190 * s), (x + 55 * s, y - 140 * s), (x + 110 * s, y - 190 * s), (x + 110 * s, y - 140 * s), (x + 165 * s, y - 190 * s), (x + 165 * s, y - 140 * s)], fill=GREY, w=4)
        self.rect(x + 175 * s, y - 260 * s, x + 205 * s, y - 140 * s, fill=RED, w=4)
        for i in range(3):
            self.circle(x + 195 * s + i * 25 * s, y - 280 * s - i * 30 * s, (15 + i * 6) * s, fill=WHITE, w=3, c=GREY)
        self.rect(x + 30 * s, y - 70 * s, x + 80 * s, y, fill=BROWN, w=3)
        if label:
            self.text(x + 110 * s, y + 15 * s, label, size=int(30 * s))

    def shop(self, x, y, s=1.0, label="SHOP"):
        self.rect(x, y - 160 * s, x + 200 * s, y, fill=WHITE, w=4)
        for i in range(5):
            c = RED if i % 2 == 0 else WHITE
            self.poly([(x - 10 * s + i * 44 * s, y - 160 * s), (x + 34 * s + i * 44 * s, y - 160 * s), (x + 34 * s + i * 44 * s, y - 120 * s), (x - 10 * s + i * 44 * s, y - 120 * s)], fill=c, w=3)
        self.text(x + 100 * s, y - 205 * s, label, size=int(32 * s))
        self.rect(x + 120 * s, y - 100 * s, x + 175 * s, y, fill=BROWN, w=3)
        self.rect(x + 20 * s, y - 100 * s, x + 95 * s, y - 45 * s, fill=LBLUE, w=3)

    def mine(self, x, y, s=1.0):
        self.poly([(x - 120 * s, y), (x - 40 * s, y - 120 * s), (x + 20 * s, y - 80 * s), (x + 70 * s, y - 140 * s), (x + 150 * s, y)], fill=BROWN, w=4)
        self.ellipse(x, y - 25 * s, 40 * s, 28 * s, fill=BLACK, w=3)
        # pickaxe
        self.line([(x + 80 * s, y - 20 * s), (x + 110 * s, y - 70 * s)], w=5, c=BROWN)
        self.line([(x + 85 * s, y - 75 * s), (x + 110 * s, y - 70 * s), (x + 130 * s, y - 55 * s)], w=5, c=DGREY)

    def palm(self, x, y, s=1.0):
        self.line([(x, y), (x + 10 * s, y - 70 * s), (x + 5 * s, y - 140 * s)], w=int(10 * s), c=BROWN)
        tx, ty = x + 5 * s, y - 140 * s
        for dx, dy in ((-70, 10), (70, 10), (-50, -40), (50, -40), (0, -55)):
            self.line([(tx, ty), (tx + dx * 0.5 * s, ty + (dy - 20) * 0.5 * s), (tx + dx * s, ty + dy * s)], w=int(8 * s), c=GREEN)

    def ship(self, x, y, s=1.0, cargo=True):
        self.poly([(x - 140 * s, y - 60 * s), (x + 140 * s, y - 60 * s), (x + 100 * s, y), (x - 110 * s, y)], fill=RED, w=4)
        self.rect(x + 50 * s, y - 130 * s, x + 110 * s, y - 60 * s, fill=WHITE, w=4)
        if cargo:
            for i, c in enumerate((BLUE, ORANGE, GREEN, YELLOW)):
                self.rect(x - 120 * s + i * 42 * s, y - 100 * s, x - 80 * s + i * 42 * s, y - 60 * s, fill=c, w=3)
        # waves
        for i in range(6):
            wx = x - 170 * s + i * 60 * s
            self.line([(wx, y + 10 * s), (wx + 15 * s, y), (wx + 30 * s, y + 10 * s), (wx + 45 * s, y)], w=3, c=BLUE)

    def track(self, pts, w=5, c=BROWN):
        self.line(pts, w=w, c=BLACK)
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            L = math.hypot(x2 - x1, y2 - y1)
            n = max(1, int(L / 22))
            ang = math.atan2(y2 - y1, x2 - x1) + math.pi / 2
            for i in range(n):
                t = (i + 0.5) / n
                px, py = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
                self.line([(px - 9 * math.cos(ang), py - 9 * math.sin(ang)), (px + 9 * math.cos(ang), py + 9 * math.sin(ang))], w=3, c=c, wob=0.8)

    def train(self, x, y, s=1.0, cargo=(GREY, BROWN, YELLOW)):
        self.rect(x, y - 90 * s, x + 110 * s, y - 20 * s, fill=BLUE, w=4)
        self.rect(x + 60 * s, y - 130 * s, x + 105 * s, y - 90 * s, fill=BLUE, w=4)
        self.rect(x + 10 * s, y - 125 * s, x + 30 * s, y - 90 * s, fill=BLACK, w=3)
        for i, c in enumerate(cargo):
            cx = x - (i + 1) * 105 * s
            self.rect(cx, y - 70 * s, cx + 95 * s, y - 20 * s, fill=DGREY, w=4)
            for k in range(3):
                self.circle(cx + 25 * s + k * 22 * s, y - 75 * s, 14 * s, fill=c, w=2)
        for i in range(-3, 2):
            self.circle(x + i * 105 * s + 30 * s, y - 12 * s, 12 * s, fill=BLACK, w=2)
            self.circle(x + i * 105 * s + 75 * s, y - 12 * s, 12 * s, fill=BLACK, w=2)

    def road(self, pts, w=26):
        self.line(pts, w=w, c=DGREY)
        self.line(pts, w=3, c=YELLOW)

    def pole(self, x, y, h=180):
        self.line([(x, y), (x, y - h)], w=6, c=BROWN)
        self.line([(x - 30, y - h + 15), (x + 30, y - h + 15)], w=5, c=BROWN)

    def phone(self, x, y, s=1.0):
        self.rect(x - 60 * s, y - 40 * s, x + 60 * s, y + 30 * s, fill=RED, w=4)
        self.poly([(x - 75 * s, y - 50 * s), (x - 40 * s, y - 70 * s), (x + 40 * s, y - 70 * s), (x + 75 * s, y - 50 * s), (x + 50 * s, y - 40 * s), (x - 50 * s, y - 40 * s)], fill=BLACK, w=3)
        self.circle(x, y - 5 * s, 22 * s, fill=WHITE, w=3)

    def cocoa(self, x, y, s=1.0):
        self.ellipse(x, y, 35 * s, 65 * s, fill=ORANGE, w=4)
        for dx in (-15, 0, 15):
            self.line([(x + dx * s, y - 55 * s), (x + dx * 1.3 * s, y), (x + dx * s, y + 55 * s)], w=2, c=BROWN)

    def chocolate(self, x, y, s=1.0):
        self.rect(x - 90 * s, y - 50 * s, x + 90 * s, y + 50 * s, fill=BROWN, w=4)
        for i in range(1, 4):
            self.line([(x - 90 * s + i * 45 * s, y - 50 * s), (x - 90 * s + i * 45 * s, y + 50 * s)], w=3)
        self.line([(x - 90 * s, y), (x + 90 * s, y)], w=3)
        self.rect(x - 95 * s, y - 10 * s, x + 95 * s, y + 55 * s, fill=PURPLE, w=4)
        self.text(x, y + 2 * s, "CHOC", size=int(30 * s), c=WHITE)

    def door(self, x, y, s=1.0, open_=True):
        self.rect(x, y - 260 * s, x + 140 * s, y, fill=BLACK if open_ else BROWN, w=5)
        if open_:
            self.poly([(x + 140 * s, y - 260 * s), (x + 200 * s, y - 280 * s), (x + 200 * s, y + 20 * s), (x + 140 * s, y)], fill=BROWN, w=4)
            self.circle(x + 185 * s, y - 130 * s, 7 * s, fill=YELLOW, w=2)
        else:
            self.circle(x + 120 * s, y - 130 * s, 8 * s, fill=YELLOW, w=2)

    def warehouse(self, x, y, s=1.0):
        self.rect(x, y - 160 * s, x + 300 * s, y, fill=GREY, w=4)
        self.poly([(x - 15 * s, y - 160 * s), (x + 150 * s, y - 230 * s), (x + 315 * s, y - 160 * s)], fill=DGREY, w=4)
        self.rect(x + 90 * s, y - 110 * s, x + 210 * s, y, fill=WHITE, w=4)
        for i in range(3):
            self.line([(x + 90 * s, y - 110 * s + i * 35 * s), (x + 210 * s, y - 110 * s + i * 35 * s)], w=2)
        self.text(x + 150 * s, y - 205 * s, "WAREHOUSE", size=int(24 * s), c=WHITE)

    def box(self, x, y, s=1.0, c=TAN):
        self.rect(x, y - 60 * s, x + 70 * s, y, fill=c, w=4)
        self.line([(x + 35 * s, y - 60 * s), (x + 35 * s, y)], w=3, c=BROWN)

    def laptop(self, x, y, s=1.0, screen=None):
        self.poly([(x - 70 * s, y - 100 * s), (x + 70 * s, y - 100 * s), (x + 70 * s, y - 10 * s), (x - 70 * s, y - 10 * s)], fill=LBLUE, w=4)
        self.poly([(x - 90 * s, y - 10 * s), (x + 90 * s, y - 10 * s), (x + 100 * s, y + 10 * s), (x - 100 * s, y + 10 * s)], fill=GREY, w=4)
        if screen:
            self.text(x, y - 75 * s, screen, size=int(26 * s))

    def bars(self, x, y, vals, labels, colors, maxh=380, bw=150, gap=60, pct=True):
        self.line([(x - 20, y), (x + len(vals) * (bw + gap), y)], w=4)
        for i, (v, lab, c) in enumerate(zip(vals, labels, colors)):
            bx = x + i * (bw + gap)
            h = maxh * v / 100
            self.rect(bx, y - h, bx + bw, y, fill=c, w=4)
            self.text(bx + bw / 2, y - h - 50, f"{v}%" if pct else str(v), size=38)
            self.text(bx + bw / 2, y + 15, lab, size=32)

    def maze(self, x, y, w=420, h=300, cells=7):
        self.rect(x, y, x + w, y + h, fill=WHITE, w=5)
        cw, ch = w / cells, h / cells
        for i in range(cells):
            for k in range(cells):
                r = random.random()
                cx, cy = x + i * cw, y + k * ch
                if r < 0.45:
                    self.line([(cx, cy), (cx + cw, cy)], w=4, wob=1)
                elif r < 0.9:
                    self.line([(cx, cy), (cx, cy + ch)], w=4, wob=1)

    def stamp_tool(self, x, y, s=1.0, c=RED):
        self.rect(x - 40 * s, y - 20 * s, x + 40 * s, y + 10 * s, fill=c, w=4)
        self.rect(x - 12 * s, y - 70 * s, x + 12 * s, y - 20 * s, fill=BROWN, w=3)
        self.circle(x, y - 85 * s, 22 * s, fill=BROWN, w=3)

    def magnifier(self, x, y, s=1.0):
        self.circle(x, y, 50 * s, fill=LBLUE, w=6)
        self.line([(x + 36 * s, y + 36 * s), (x + 100 * s, y + 100 * s)], w=int(14 * s), c=BROWN)

    def question(self, x, y, size=120, c=RED):
        self.text(x, y, "?", size=size, c=c)

    def handshake(self, x, y, s=1.0):
        self.line([(x - 150 * s, y + 20 * s), (x - 20 * s, y)], w=int(10 * s))
        self.line([(x + 150 * s, y + 20 * s), (x + 20 * s, y)], w=int(10 * s))
        self.ellipse(x, y, 35 * s, 22 * s, fill=TAN, w=4)

    def pen(self, x, y, s=1.0):
        self.poly([(x, y), (x + 15 * s, y - 15 * s), (x + 110 * s, y - 110 * s), (x + 95 * s, y - 125 * s), (x - 5 * s, y - 25 * s)], fill=BLUE, w=3)
        self.d.polygon([(x - 2, y + 2), (x + 8, y - 8), (x - 6, y - 14)], fill=BLACK)

    def table(self, x1, x2, y):
        self.rect(x1, y, x2, y + 20, fill=BROWN, w=4)
        self.line([(x1 + 20, y + 20), (x1 + 20, y + 130)], w=6, c=BROWN)
        self.line([(x2 - 20, y + 20), (x2 - 20, y + 130)], w=6, c=BROWN)

    def wire(self, pts, c=BLACK):
        self.line(pts, w=3, c=c, wob=4)

    def x_mark(self, x, y, r=40, c=RED, w=10):
        self.line([(x - r, y - r), (x + r, y + r)], w=w, c=c)
        self.line([(x + r, y - r), (x - r, y + r)], w=w, c=c)

    def check(self, x, y, r=40, c=GREEN, w=10):
        self.line([(x - r, y), (x - r * 0.3, y + r * 0.7), (x + r, y - r * 0.8)], w=w, c=c)

    def hourglass(self, x, y, s=1.0):
        self.poly([(x - 50 * s, y - 80 * s), (x + 50 * s, y - 80 * s), (x, y), (x + 50 * s, y + 80 * s), (x - 50 * s, y + 80 * s), (x, y)], fill=WHITE, w=4)
        self.poly([(x - 30 * s, y + 70 * s), (x + 30 * s, y + 70 * s), (x, y + 30 * s)], fill=YELLOW, w=2)
        self.line([(x - 60 * s, y - 80 * s), (x + 60 * s, y - 80 * s)], w=8, c=BROWN)
        self.line([(x - 60 * s, y + 80 * s), (x + 60 * s, y + 80 * s)], w=8, c=BROWN)

    def lightbulb(self, x, y, s=1.0):
        self.circle(x, y, 45 * s, fill=YELLOW, w=4)
        self.rect(x - 20 * s, y + 40 * s, x + 20 * s, y + 70 * s, fill=GREY, w=3)
        for a in range(0, 360, 45):
            r = math.radians(a)
            self.line([(x + 60 * s * math.cos(r), y + 60 * s * math.sin(r)), (x + 80 * s * math.cos(r), y + 80 * s * math.sin(r))], w=4, c=ORANGE)

    def bridge(self, x1, x2, y, c=BROWN):
        self.line([(x1, y), (x2, y)], w=10, c=c)
        mid = (x1 + x2) / 2
        self.line([(x1, y), (mid, y - 90), (x2, y)], w=5, c=c)
        for i in range(1, 8):
            px = x1 + (x2 - x1) * i / 8
            top = y - 90 * (1 - abs(px - mid) / ((x2 - x1) / 2))
            self.line([(px, y), (px, top)], w=3, c=c)
