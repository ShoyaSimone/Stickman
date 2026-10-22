"""One crude image per script timestamp. Run: python3 scenes.py [outdir]"""
import os
import sys
import random
from paint import *

G = 620  # ground line
S = []  # (timestamp, slug, fn)


def scene(ts, slug):
    def deco(fn):
        S.append((ts, slug, fn))
        return fn
    return deco


def border_base(c, closed=True, night=True):
    if night:
        c.night()
    c.ground(G)
    c.booth(820, G)
    c.barrier(1020, G, closed=closed)


# ---------------- INTRO ----------------
@scene("0:00", "2am-border-west-africa")
def _(c):
    border_base(c)
    c.truck(200, G)
    c.text(640, 650, "2 AM", 44)
    c.africa(150, 140, 0.35)
    c.pin(*c.apt(150, 140, 0.35, "westcoast"))
    c.text(150, 240, "WEST AFRICA", 22)


@scene("0:04", "truck-waiting-6-days")
def _(c):
    border_base(c)
    c.truck(380, G, face=True)
    c.calendar(60, 220, 0.9, crossed=6)
    c.text(170, 430, "6 DAYS!!", 40, c=RED)


@scene("0:07", "cargo-fresh-produce")
def _(c):
    c.ground(G)
    x1, y1, x2, y2 = c.truck(120, G, s=1.4)
    c.rect(150, 380, 470, 520, fill=WHITE)
    for i in range(6):
        c.tomato(185 + i * 52, 490, 22)
        c.tomato(210 + i * 48, 445, 20)
    c.banana(260, 395, 0.9)
    c.text(980, 180, "FRESH", 70, c=GREEN)
    c.text(980, 270, "PRODUCE", 60, c=GREEN)
    c.tomato(900, 420, 50)
    c.banana(990, 390, 1.5)


@scene("0:09", "produce-starting-to-turn")
def _(c):
    c.ground(G)
    c.crate(260, G, s=2.6, rotten=True)
    c.stink(330, 340, 4)
    for _ in range(6):
        c.fly(random.uniform(250, 600), random.uniform(220, 360))
    c.stick(900, G, mood="sad", arms="head", hat="cap")
    c.text(640, 100, "UH OH...", 60, c=BROWN)


@scene("0:11", "driver-has-every-document")
def _(c):
    c.ground(G)
    c.stick(330, G, mood="happy", arms="out", hat="cap")
    for i, t in enumerate(["PERMIT", "INVOICE", "ORIGIN", "CUSTOMS"]):
        c.doc(520 + i * 170, 140 + (i % 2) * 30, 0.95, stamp=GREEN, title=t)
    c.text(830, 470, "ALL LEGAL", 50, c=GREEN)
    c.check(1180, 420, 45)


@scene("0:14", "trade-is-allowed")
def _(c):
    c.ground(G)
    c.truck(120, G, s=0.9)
    c.check(800, 280, 120, w=22)
    c.text(800, 460, "TRADE ALLOWED", 54, c=GREEN)


@scene("0:16", "a-treaty-says-so")
def _(c):
    c.doc(470, 70, 2.3, title="TREATY", sig=True, lines=10)
    c.stick(230, G, mood="happy", arms="point_r", tie=BLUE)
    c.stick(1060, G, mood="happy", arms="point_l", tie=RED)


@scene("0:18", "why-still-waiting")
def _(c):
    border_base(c, night=False)
    c.truck(80, G, s=0.8)
    c.stick(560, G, mood="sad", arms="shrug", hat="cap")
    c.question(560, 170, 150)
    c.text(400, 60, "SO WHY STILL WAITING?", 44)


@scene("0:20", "stay-with-me")
def _(c):
    c.ground(G)
    c.stick(640, G, s=1.6, mood="happy", arms="wave")
    c.bubble(1000, 180, 380, 150, "STAY WITH ME!", 36, tail=(720, 320))


@scene("0:21", "by-the-end-you-will-see")
def _(c):
    c.ground(G)
    c.stick(250, G, mood="neutral", arms="point_r")
    c.magnifier(620, 330, 1.6)
    c.truck(820, G, s=0.8)
    c.line([(830, 420), (790, 470), (830, 520), (790, 570)], w=6, c=GREY)
    c.text(640, 70, "WHAT'S HOLDING IT??", 48)


@scene("0:25", "who-is-getting-rich")
def _(c):
    c.ground(G)
    c.stick(640, G, s=1.3, mood="rich", arms="hold", hat="top")
    c.money_bag(450, 520, 0.9)
    c.money_bag(830, 520, 0.9)
    for i in range(5):
        c.bill(random.uniform(200, 1080), random.uniform(80, 250), 0.8, rot=random.uniform(-30, 30))
    c.text(640, 660, "SHHH...", 34)


# ---------------- AFCFTA ----------------
@scene("0:28", "2018-leaders-sign")
def _(c):
    c.table(280, 1000, 430)
    c.doc(560, 260, 1.0, title="DEAL", sig=True)
    for x, t in ((180, RED), (420, GREEN), (860, BLUE), (1100, ORANGE)):
        c.stick(x, G, mood="happy", arms="up" if x in (180, 1100) else "hold", tie=t)
    c.text(640, 70, "2018", 80, c=BLUE)


@scene("0:33", "afcfta-name")
def _(c):
    c.africa(330, 380, 1.2, fill=GREEN)
    c.text(860, 220, "AfCFTA", 100, c=BLUE)
    c.text(860, 350, "African Continental", 38)
    c.text(860, 410, "Free Trade Area", 38)


@scene("0:39", "54-countries-signed")
def _(c):
    c.africa(330, 380, 1.2)
    for _ in range(54):
        x, y = random.uniform(200, 470), random.uniform(220, 560)
        c.check(x, y, 9, w=3)
    c.text(900, 250, "54", 180, c=RED)
    c.text(900, 470, "COUNTRIES", 54)


@scene("0:41", "over-a-billion-people")
def _(c):
    c.ground(G)
    for row in range(3):
        for i in range(14):
            c.stick(70 + i * 88 + row * 30, G - row * 70, s=0.42, mood=random.choice(["happy", "neutral"]))
    c.text(640, 80, "1,000,000,000+", 70, c=BLUE)
    c.text(640, 170, "PEOPLE", 50)


@scene("0:43", "combined-economy-trillions")
def _(c):
    for i in range(8):
        c.coin(220 + i * 30, 560 - i * 40, 50)
    c.money_bag(800, 470, 2.0)
    c.text(640, 80, "$ TRILLIONS", 72, c=DGREEN)


@scene("0:46", "largest-free-trade-area")
def _(c):
    c.globe(400, 380, 220)
    c.africa(480, 420, 0.38, fill=YELLOW)
    c.text(960, 180, "#1", 140, c=RED)
    c.text(960, 380, "BIGGEST", 56)
    c.text(960, 450, "ON EARTH", 56)


@scene("0:50", "the-idea-is-simple")
def _(c):
    c.ground(G)
    c.stick(400, G, s=1.4, mood="happy", arms="think")
    c.lightbulb(400, 140, 1.2)
    c.text(900, 300, "SIMPLE", 80)


@scene("0:52", "remove-tariffs")
def _(c):
    c.rect(400, 200, 880, 420, fill=YELLOW, w=6)
    c.text(640, 280, "TARIFFS", 70)
    c.x_mark(640, 310, 200, w=18)
    c.stick(1050, G, mood="happy", arms="up")
    c.ground(G)


@scene("0:54", "africans-sell-to-africans")
def _(c):
    c.ground(G)
    c.stick(250, G, s=1.2, mood="happy", arms="give_r")
    c.stick(1030, G, s=1.2, mood="happy", arms="point_l")
    c.box(560, 470, 1.2)
    c.arrow(450, 380, 830, 380)
    c.coin(640, 230, 40)
    c.arrow(830, 300, 450, 300, c=DGREEN)


@scene("0:56", "kenya-factory-feeds-ghana-shop")
def _(c):
    c.africa(640, 400, 1.1)
    k = c.apt(640, 400, 1.1, "kenya")
    g = c.apt(640, 400, 1.1, "ghana")
    c.factory(980, 600, 0.8, label="KENYA")
    c.shop(80, 590, 0.9, label="GHANA")
    c.arrow(k[0], k[1], g[0] + 20, g[1], c=RED, w=7)
    c.pin(*k)
    c.pin(*g, c=BLUE)


@scene("0:59", "lift-millions-out-of-poverty")
def _(c):
    c.ground(G)
    c.building(80, G, w=200, h=230, label="WORLD BANK", roof="bank")
    c.line([(500, 500), (1200, 500)], w=5)
    c.text(850, 530, "POVERTY", 34, c=RED)
    for i in range(5):
        x = 560 + i * 130
        c.stick(x, 470, s=0.55, mood="happy", arms="up")
        c.arrow(x, 370, x, 230, c=GREEN)
    c.text(850, 80, "TENS OF MILLIONS", 46, c=GREEN)


@scene("1:05", "trading-began-2021")
def _(c):
    c.ground(G)
    c.line([(150, 400), (1130, 400)], w=12, c=RED)
    c.line([(150, 400), (110, 340)], w=5)
    c.line([(1130, 400), (1170, 340)], w=5)
    c.stick(640, G, s=1.1, mood="happy", arms="hold")
    c.line([(590, 410), (690, 390)], w=5, c=GREY)
    c.text(640, 120, "TRADING BEGINS 2021", 54, c=BLUE)


@scene("1:08", "door-is-open")
def _(c):
    c.ground(G)
    c.door(500, G, 1.6)
    c.text(640, 70, "THE DOOR IS OPEN", 54, c=GREEN)


@scene("1:10", "trucks-still-waiting")
def _(c):
    c.ground(G)
    c.booth(1050, G, 0.9)
    for i in range(3):
        c.truck(20 + i * 345, G, s=0.85, face=True)
    c.text(640, 120, "...AND YET", 54)
    c.text(640, 190, "STILL WAITING", 54, c=RED)


@scene("1:13", "reason-not-in-treaty")
def _(c):
    c.doc(440, 90, 2.2, title="TREATY", lines=10)
    c.magnifier(830, 380, 1.4)
    c.text(1050, 160, "NOT HERE", 42, c=RED)
    c.stick(200, G, mood="sad", arms="shrug")


@scene("1:16", "its-older")
def _(c):
    c.doc(450, 100, 2.4, fill=TAN, lines=10)
    for _ in range(14):
        x, y = random.uniform(460, 740), random.uniform(110, 500)
        c.line([(x, y), (x + 12, y + 12)], w=2, c=BROWN)
    c.text(1000, 300, "OLDER", 80, c=BROWN)


@scene("1:17", "much-older")
def _(c):
    c.ground(G)
    c.stick(640, G, s=1.3, mood="tired", arms="down")
    c.line([(640, 380), (640, 600)], w=6)
    c.line([(570, 520), (520, 620)], w=6, c=BROWN)
    c.text(640, 130, "MUCH OLDER", 80, c=BROWN)


@scene("1:18", "its-on-a-map")
def _(c):
    c.rect(200, 80, 1080, 620, fill=TAN)
    c.africa(640, 350, 1.0, fill=WHITE)
    c.line([(200, 620), (230, 640), (1050, 640), (1080, 620)], w=4)
    c.text(1000, 120, "MAP", 50)


@scene("1:19", "africas-old-railways")
def _(c):
    c.africa(640, 360, 1.25)
    for a, b in (("mali", "senegal"), ("congo", "angola"), ("zambia", "tanzania"), ("ethiopia", "eastcoast"), ("nigeria", "ghana")):
        c.track([c.apt(640, 360, 1.25, a), c.apt(640, 360, 1.25, b)])
    c.text(1050, 100, "OLD", 50, c=BROWN)
    c.text(1050, 160, "RAILWAYS", 50, c=BROWN)


@scene("1:22", "dont-connect-neighbours")
def _(c):
    c.ground(G)
    c.building(120, G, w=220, h=200, roof="tri", label="COUNTRY A")
    c.building(940, G, w=220, h=200, roof="tri", label="COUNTRY B")
    c.track([(370, 560), (560, 560)])
    c.track([(720, 560), (910, 560)])
    c.x_mark(640, 540, 50)
    c.text(640, 140, "NO LINK", 56, c=RED)


@scene("1:24", "dont-connect-capitals")
def _(c):
    c.africa(640, 360, 1.25)
    caps = ("ghana", "nigeria", "kenya", "egypt", "southafrica", "chad")
    for n in caps:
        x, y = c.apt(640, 360, 1.25, n)
        c.star(x, y, 14, c=RED)
    c.line([c.apt(640, 360, 1.25, "nigeria"), c.apt(640, 360, 1.25, "kenya")], w=4, c=GREY)
    x, y = c.apt(640, 360, 1.25, "congo")
    c.x_mark(x + 30, y - 40, 40)
    c.text(1080, 140, "CAPITALS?", 40)
    c.text(1080, 200, "NOPE", 50, c=RED)


@scene("1:25", "mines-to-the-coast")
def _(c):
    c.ground(G)
    c.mine(170, G, 0.9)
    c.palm(450, G, 0.8)
    c.track([(250, 580), (1020, 580)])
    c.train(800, 575, 0.8)
    c.ship(1130, 560, 0.6)
    c.text(1130, 330, "COAST", 34, c=BLUE)
    c.arrow(500, 450, 950, 450, c=RED)


@scene("1:29", "inland-to-port-1")
def _(c):
    c.africa(640, 360, 1.25)
    for n in ("mali", "chad", "congo"):
        x, y = c.apt(640, 360, 1.25, n)
        c.track([(x, y), (x - 110 if n != "congo" else x - 60, y + 40)])
    c.text(640, 670, "INLAND → PORT", 44)


@scene("1:31", "inland-to-port-2")
def _(c):
    c.africa(640, 360, 1.25)
    for n in ("mali", "chad", "congo", "zambia", "ethiopia", "nigeria"):
        x, y = c.apt(640, 360, 1.25, n)
        dx = 120 if n in ("zambia", "ethiopia") else -110
        c.track([(x, y), (x + dx, y + 30)])
    c.text(640, 670, "INLAND → PORT", 44)


@scene("1:33", "over-and-over")
def _(c):
    c.africa(640, 360, 1.25)
    for _ in range(12):
        x, y = random.uniform(530, 760), random.uniform(220, 460)
        dx = 150 if x > 640 else -150
        c.track([(x, y), (x + dx, y + random.uniform(-20, 40))])
    c.text(1080, 330, "AGAIN", 40)
    c.text(1080, 390, "& AGAIN", 40)


@scene("1:34", "never-built-to-move-africans")
def _(c):
    c.ground(G)
    c.track([(0, 600), (1280, 600)])
    c.train(1100, 595, 0.9)
    for i in range(3):
        c.stick(150 + i * 130, 590, s=0.8, mood="sad", arms="down")
    c.x_mark(260, 300, 60)
    c.text(640, 90, "NOT FOR PEOPLE", 52, c=RED)


@scene("1:38", "built-to-move-resources")
def _(c):
    c.ground(G)
    c.track([(0, 600), (1280, 600)])
    c.train(950, 595, 1.1, cargo=(YELLOW, GREY, ORANGE))
    c.text(400, 200, "GOLD", 40, c=ORANGE)
    c.text(640, 200, "COPPER", 40, c=BROWN)
    c.text(880, 200, "COCOA", 40, c=ORANGE)
    c.text(640, 90, "RESOURCES", 60)


@scene("1:40", "out")
def _(c):
    c.africa(320, 380, 1.0)
    c.arrow(450, 360, 1000, 360, w=14, c=RED)
    c.ship(1100, 520, 0.6)
    c.text(760, 200, "OUT!", 110, c=RED)


@scene("1:41", "roads-same-logic")
def _(c):
    c.africa(640, 360, 1.25)
    for n in ("mali", "congo", "zambia"):
        x, y = c.apt(640, 360, 1.25, n)
        dx = 140 if n == "zambia" else -120
        c.road([(x, y), (x + dx, y + 20)], w=18)
    c.text(1080, 330, "ROADS", 50)
    c.text(1080, 390, "TOO", 50)


@scene("1:43", "ports-same-logic")
def _(c):
    c.ground(G)
    for i, x in enumerate((180, 640, 1100)):
        c.ship(x, 580, 0.6)
        c.arrow(x, 330, x, 200, c=RED)
        c.text(x, 400, f"PORT {i + 1}", 30)
    c.text(640, 80, "ALL POINT AWAY", 50)


@scene("1:45", "phone-lines-via-europe")
def _(c):
    c.phone(160, 500, 1.2)
    c.phone(1120, 500, 1.2)
    c.text(160, 580, "GHANA", 30)
    c.text(1120, 580, "NIGERIA", 30)
    c.building(560, 300, w=160, h=150, label="EUROPE", roof="tri")
    c.wire([(160, 430), (300, 250), (560, 220)])
    c.wire([(720, 220), (980, 250), (1120, 430)])
    c.text(640, 640, "LONG WAY ROUND", 40, c=RED)


@scene("1:48", "wired-to-face-outward")
def _(c):
    c.africa(640, 370, 1.1)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)):
        c.arrow(640 + dx * 250, 370 + dy * 230, 640 + dx * 380, 370 + dy * 310, c=RED)
    c.text(640, 690, "100 YEARS FACING OUT", 34)


@scene("1:52", "independence-changed-flags")
def _(c):
    c.ground(G)
    c.flag(300, G, colors=(RED, WHITE, BLUE), s=1.4, vertical=False)
    c.x_mark(385, 300, 70)
    c.arrow(520, 400, 720, 400, w=8)
    c.flag(850, G, colors=(GREEN, YELLOW, RED), s=1.4)
    c.text(640, 70, "NEW FLAGS!", 56, c=GREEN)


@scene("1:54", "did-not-change-wiring")
def _(c):
    c.ground(G)
    c.flag(200, G, colors=(GREEN, YELLOW, RED), s=1.2)
    c.track([(420, 580), (1180, 580)])
    c.train(1000, 575, 0.7)
    c.text(800, 150, "SAME OLD", 56, c=RED)
    c.text(800, 230, "WIRING", 56, c=RED)


@scene("1:57", "wiring-leaves-fingerprint")
def _(c):
    c.ellipse(640, 360, 170, 230, fill=PINK, w=5)
    for r in range(1, 8):
        c.ellipse(640, 360 + r * 4, 160 - r * 20, 215 - r * 27, w=3, c=BROWN)
    c.magnifier(900, 220, 1.2)
    c.text(640, 660, "FINGERPRINT", 46)


@scene("1:59", "one-number")
def _(c):
    c.text(640, 160, "1", 300, c=RED)
    c.text(640, 560, "ONE NUMBER", 60)


@scene("2:00", "hold-onto-it")
def _(c):
    c.ground(G)
    c.stick(640, G, s=1.5, mood="neutral", arms="up")
    c.rect(520, 90, 760, 200, fill=YELLOW, w=5)
    c.text(640, 120, "#", 60)
    c.text(640, 660, "HOLD ONTO IT", 40)


@scene("2:01", "roughly-15-percent")
def _(c):
    c.circle(640, 360, 220, fill=GREY, w=5)
    c.d.pieslice([420, 140, 860, 580], -90, -90 + 54, fill=RED)
    c.line([(640, 360), (640, 140)], w=5)
    c.line([(640, 360), (640 + 178, 360 - 129)], w=5)
    c.text(1050, 250, "~15%", 100, c=RED)


@scene("2:03", "africa-trade-between-countries")
def _(c):
    c.africa(400, 380, 1.1)
    a = c.apt(400, 380, 1.1, "ghana")
    b = c.apt(400, 380, 1.1, "kenya")
    c.arrow(a[0], a[1], b[0], b[1], c=RED, w=4)
    c.text(950, 260, "ONLY 15%", 60, c=RED)
    c.text(950, 340, "AFRICA ↔ AFRICA", 40)


@scene("2:08", "europe-two-thirds")
def _(c):
    c.bars(330, 560, [15, 67], ["AFRICA", "EUROPE"], [RED, BLUE], bw=220, gap=180)
    c.text(640, 60, "TRADE WITH NEIGHBOURS", 42)


@scene("2:10", "asia-more-than-half")
def _(c):
    c.bars(170, 560, [15, 67, 55], ["AFRICA", "EUROPE", "ASIA"], [RED, BLUE, YELLOW], bw=200, gap=130)
    c.text(640, 60, "TRADE WITH NEIGHBOURS", 42)


@scene("2:13", "sell-raw-buy-finished")
def _(c):
    c.africa(250, 380, 0.85)
    c.globe(1030, 380, 150)
    c.arrow(430, 280, 860, 280, c=BROWN, w=7)
    c.text(645, 200, "RAW STUFF", 36, c=BROWN)
    c.arrow(860, 480, 430, 480, c=BLUE, w=7)
    c.text(645, 520, "FINISHED GOODS", 36, c=BLUE)


@scene("2:18", "exports-cocoa")
def _(c):
    c.africa(250, 380, 0.85)
    c.cocoa(700, 360, 1.5)
    c.arrow(430, 360, 600, 360, w=7)
    c.arrow(820, 360, 1050, 360, w=7)
    c.text(700, 560, "EXPORTS COCOA", 46)


@scene("2:20", "imports-chocolate")
def _(c):
    c.africa(250, 380, 0.85)
    c.chocolate(800, 360, 1.5)
    c.arrow(1150, 360, 1000, 360, w=7)
    c.arrow(600, 360, 430, 360, w=7)
    c.text(800, 560, "IMPORTS CHOCOLATE", 46)
    c.text(1180, 300, "$$$", 40, c=RED)


@scene("2:23", "15-percent")
def _(c):
    c.text(640, 210, "15%", 260, c=RED)


@scene("2:24", "scar-left-by-map")
def _(c):
    c.africa(640, 360, 1.3)
    c.line([(520, 220), (560, 260), (600, 290), (650, 340), (690, 380), (740, 430)], w=9, c=RED)
    for i in range(6):
        x, y = 540 + i * 38, 240 + i * 38
        c.line([(x - 15, y + 15), (x + 15, y - 15)], w=4, c=RED)
    c.text(1080, 320, "SCAR", 70, c=RED)


@scene("2:27", "treaty-supposed-to-erase")
def _(c):
    c.text(450, 300, "15%", 180, c=RED)
    c.doc(850, 150, 1.6, title="TREATY", sig=True)
    c.rect(770, 450, 930, 520, fill=PINK, w=4)
    c.arrow(770, 480, 650, 400, w=6)
    c.text(640, 640, "ERASE IT?", 44)


@scene("2:29", "signature-cant-build-railway")
def _(c):
    c.ground(G)
    c.pen(200, 400, 1.3)
    c.track([(500, 580), (760, 580)])
    c.line([(760, 580), (800, 600), (840, 570), (880, 610)], w=4, c=BROWN)
    c.stick(1050, G, mood="sad", arms="shrug")
    c.x_mark(330, 260, 50)
    c.text(640, 80, "PEN ≠ RAILWAY", 56)


@scene("2:32", "only-first-problem")
def _(c):
    c.ground(G)
    c.stick(350, G, s=1.3, mood="neutral", arms="raise_r")
    c.text(780, 200, "PROBLEM #1", 70, c=RED)
    c.text(780, 320, "(of many)", 40, c=GREY)


@scene("2:34", "three-more")
def _(c):
    for i, t in enumerate(("#2", "#3", "#4")):
        x = 260 + i * 380
        c.rect(x - 130, 200, x + 130, 460, fill=YELLOW, w=5)
        c.text(x, 270, t, 110, c=RED)
    c.text(640, 80, "3 MORE", 60)


@scene("2:36", "not-in-headlines")
def _(c):
    c.rect(280, 80, 1000, 620, fill=WHITE, w=5)
    c.text(640, 110, "THE NEWS", 56)
    c.line([(300, 190), (980, 190)], w=5)
    c.text(640, 220, "TREATY SIGNED!", 40)
    for i in range(6):
        c.line([(320, 310 + i * 45), (960 - random.uniform(0, 200), 310 + i * 45)], w=3, c=DGREY)
    c.magnifier(1100, 450, 1.0)
    c.text(1150, 620, "NOTHING", 28, c=RED)


# ---------------- TOLL 1: PAPERWORK ----------------
@scene("2:38", "toll-1-paperwork")
def _(c):
    c.text(640, 60, "TOLL #1: PAPERWORK", 56, c=RED)
    c.stack_docs(560, 560, n=14, s=0.9)
    c.stick(250, G, mood="shock", arms="head", hat="cap")
    c.ground(G)


@scene("2:40", "tariff-a-number-you-see")
def _(c):
    c.rect(400, 180, 880, 480, fill=YELLOW, w=6)
    c.text(640, 210, "TARIFF", 50)
    c.text(640, 300, "10%", 120, c=RED)
    c.ground(G)
    c.stick(1050, G, mood="happy", arms="point_l")
    c.ellipse(220, 330, 70, 40, fill=WHITE)
    c.circle(220, 330, 20, fill=BLUE)


@scene("2:43", "paperwork-a-maze")
def _(c):
    c.maze(380, 150, 520, 400, cells=8)
    c.stick(250, G, s=0.9, mood="sad", arms="shrug")
    c.question(1020, 250, 140)
    c.text(640, 70, "PAPERWORK MAZE", 50)


@scene("2:45", "different-forms")
def _(c):
    cols = (WHITE, PINK, YELLOW, LBLUE, TAN, GREEN)
    for i, col in enumerate(cols):
        c.doc(60 + i * 200, 180 + (i % 2) * 60, 1.0, fill=col, title=f"FORM {chr(65 + i)}")
    c.text(640, 70, "DIFFERENT FORMS", 54)


@scene("2:47", "different-inspections")
def _(c):
    c.ground(G)
    c.crate(500, G, 2.0)
    c.stick(250, G, mood="angry", arms="point_r", hat="officer")
    c.stick(1000, G, mood="neutral", arms="point_l", hat="officer")
    c.magnifier(870, 330, 0.9)
    c.text(640, 70, "INSPECTION... AGAIN", 50)


@scene("2:48", "different-rules-every-border")
def _(c):
    c.ground(G)
    for i, (x, t) in enumerate(((60, "RULE A"), (480, "RULE B"), (900, "RULE C"))):
        c.booth(x, G, 0.75, label="")
        c.doc(x + 20, 180, 0.8, title=t)
    c.text(640, 70, "NEW RULES EVERY BORDER", 46)


@scene("2:50", "tariff-free-still-stuck")
def _(c):
    border_base(c, night=False)
    c.truck(120, G, s=1.0, face=True)
    c.rect(130, 270, 360, 340, fill=GREEN, w=4)
    c.text(245, 280, "0% TARIFF", 32, c=WHITE)
    c.text(640, 70, "STILL STUCK FOR DAYS", 52, c=RED)


@scene("2:55", "every-hour-costs-money")
def _(c):
    c.clock(330, 330, 150, h=3)
    c.arrow(520, 330, 720, 330, w=8)
    for i in range(4):
        c.bill(880 + random.uniform(-80, 80), 230 + i * 60, 1.0, rot=random.uniform(-30, 30))
    c.text(640, 620, "TICK TOCK = $$$", 54, c=RED)


@scene("2:57", "fresh-food-costs-product")
def _(c):
    c.ground(G)
    c.crate(200, G, 2.4, rotten=True)
    c.stink(260, 360, 4)
    for _ in range(7):
        c.fly(random.uniform(200, 560), random.uniform(250, 380))
    c.text(900, 250, "ROTTEN", 80, c=BROWN)
    c.stick(950, G, s=1.0, mood="sad", arms="head", hat="cap")


# ---------------- TOLL 2: RULES OF ORIGIN ----------------
@scene("3:00", "toll-2-rules-of-origin")
def _(c):
    c.text(640, 60, "TOLL #2: RULES OF ORIGIN", 50, c=RED)
    c.doc(500, 150, 1.8, title="ORIGIN", lines=8)
    c.ground(G)
    c.stick(250, G, mood="neutral", arms="point_r", hat="officer")


@scene("3:03", "must-be-made-in-africa")
def _(c):
    c.box(400, 550, 3.5)
    c.text(520, 380, "MADE IN", 40)
    c.text(520, 430, "AFRICA", 44, c=GREEN)
    c.africa(1000, 360, 0.8, fill=GREEN)
    c.check(520, 220, 50)


@scene("3:08", "enough-of-it-anyway")
def _(c):
    c.rect(300, 280, 980, 400, fill=WHITE, w=5)
    c.rect(300, 280, 740, 400, fill=GREEN, w=5)
    c.text(520, 310, "AFRICA", 44, c=WHITE)
    c.text(860, 310, "OTHER", 34)
    c.text(640, 120, "ENOUGH OF IT... ANYWAY", 46)
    c.question(1100, 260, 110)


@scene("3:09", "prove-it")
def _(c):
    c.ground(G)
    c.stick(350, G, s=1.3, mood="angry", arms="point_r", hat="officer")
    c.bubble(800, 220, 380, 170, "PROVE IT!", 60, tail=(470, 330))
    c.stick(1050, G, s=0.9, mood="shock", arms="down", hat="cap")


@scene("3:10", "with-documents")
def _(c):
    c.ground(G)
    c.stick(250, G, mood="tired", arms="hold", hat="cap")
    c.stack_docs(600, 560, n=10, s=1.0)
    c.text(640, 70, "WITH DOCUMENTS", 54)


@scene("3:11", "for-every-shipment")
def _(c):
    c.ground(G)
    for i in range(4):
        x = 30 + i * 320
        c.truck(x, G, s=0.7)
        c.doc(x + 70, 160, 0.8, stamp=RED)
    c.text(640, 60, "EVERY. SINGLE. SHIPMENT.", 48)


@scene("3:13", "small-business-loses-deal")
def _(c):
    c.ground(G)
    c.shop(80, G, 1.0, label="SMALL BIZ")
    c.stick(450, G, mood="sad", arms="head")
    c.handshake(850, 330, 1.2)
    c.x_mark(850, 330, 110, w=14)
    c.doc(1050, 380, 0.8, title="FORM ??")
    c.text(820, 110, "DEAL LOST", 54, c=RED)


# ---------------- TOLL 3: MONEY ----------------
@scene("3:17", "toll-3-money")
def _(c):
    c.text(640, 60, "TOLL #3: MONEY", 58, c=RED)
    c.money_bag(640, 420, 2.2)


@scene("3:19", "dozens-of-currencies")
def _(c):
    syms = ["₦", "₵", "KSh", "R", "CFA", "Br", "DA", "£E", "ZK", "TSh", "Le", "MAD"]
    for i, s in enumerate(syms):
        x = 150 + (i % 6) * 195
        y = 230 + (i // 6) * 230
        c.coin(x, y, 70, sym=s)
    c.text(640, 60, "DOZENS OF CURRENCIES", 50)


@scene("3:21", "hard-to-convert")
def _(c):
    c.coin(280, 360, 110, sym="₦")
    c.coin(1000, 360, 110, sym="₵")
    c.arrow(430, 330, 850, 330, w=7)
    c.arrow(850, 410, 430, 410, w=7)
    c.x_mark(640, 370, 70)
    c.text(640, 600, "HARD TO SWAP", 54, c=RED)


@scene("3:23", "sell-one-country-to-another")
def _(c):
    c.ground(G)
    c.stick(250, G, s=1.1, mood="happy", arms="give_r")
    c.stick(1030, G, s=1.1, mood="neutral", arms="point_l")
    c.box(560, 480, 1.4)
    c.text(250, 650, "SELLER", 30)
    c.text(1030, 650, "BUYER", 30)
    c.text(640, 100, "AFRICA → AFRICA", 50)


@scene("3:26", "payment-travels-abroad")
def _(c):
    c.africa(260, 400, 0.8)
    c.building(920, 330, w=220, h=200, roof="bank", label="BANK ABROAD")
    c.arrow(380, 300, 870, 220, c=DGREEN, w=6)
    c.coin(620, 230, 35)
    c.globe(1150, 560, 80)


@scene("3:29", "money-leaves-continent")
def _(c):
    c.africa(330, 380, 1.0)
    for i in range(4):
        c.bill(700 + i * 130, 300 - i * 50, 0.9, rot=-20)
    c.arrow(500, 380, 1150, 160, c=RED, w=6)
    c.text(860, 560, "BYE BYE $", 50, c=RED)


@scene("3:31", "comes-back")
def _(c):
    c.africa(330, 380, 1.0)
    for i in range(3):
        c.bill(1000 - i * 140, 200 + i * 60, 0.9, rot=20)
    c.arrow(1150, 160, 500, 380, c=GREEN, w=6)
    c.text(860, 560, "...COMES BACK", 50, c=GREEN)


@scene("3:32", "someone-takes-a-cut")
def _(c):
    c.ground(G)
    c.stick(640, G, s=1.3, mood="rich", arms="hold", hat="top")
    c.bill(480, 420, 1.0)
    c.bill(800, 420, 1.0)
    c.line([(380, 360), (430, 480)], w=6, c=GREY)
    c.line([(430, 360), (380, 480)], w=6, c=GREY)
    c.circle(370, 500, 14, w=4)
    c.circle(440, 500, 14, w=4)
    c.text(640, 70, "A CUT EACH WAY", 52, c=RED)


@scene("3:35", "three-tolls")
def _(c):
    for i, t in enumerate(("PAPER", "ORIGIN", "MONEY")):
        x = 240 + i * 400
        c.rect(x - 150, 220, x + 150, 440, fill=YELLOW, w=5)
        c.text(x, 250, f"#{i + 1}", 70, c=RED)
        c.text(x, 360, t, 40)
    c.text(640, 70, "3 TOLLS", 64)


@scene("3:36", "none-a-tariff")
def _(c):
    c.rect(400, 200, 880, 420, fill=YELLOW, w=6)
    c.text(640, 280, "TARIFF", 70)
    c.text(640, 580, "NOT A TARIFF", 50, c=RED)
    c.circle(640, 310, 230, w=12, c=RED)
    c.line([(480, 150), (800, 470)], w=12, c=RED)


@scene("3:37", "none-fixed-by-signature")
def _(c):
    c.doc(470, 100, 2.0, title="TREATY", sig=True, lines=8)
    c.pen(850, 450, 1.2)
    c.x_mark(640, 300, 180, w=16)
    c.text(640, 650, "SIGNATURE WON'T FIX IT", 42)


@scene("3:39", "why-truck-still-waiting")
def _(c):
    border_base(c)
    c.truck(150, G, face=True, rotten=True)
    c.stick(700, G, mood="sleep", arms="down", legs="sit", hat="cap")
    c.text(500, 70, "STILL WAITING", 50, c=RED)


# ---------------- MIDDLEMEN ----------------
@scene("3:42", "something-is-changing")
def _(c):
    c.ground(G)
    c.stick(640, G, s=1.4, mood="shock", arms="out")
    for i in range(6):
        c.text(250 + i * 160, 130 + (i % 2) * 40, "!", 80, c=ORANGE)
    c.text(640, 660, "SOMETHING'S CHANGING", 40)


@scene("3:44", "if-you-know-where-to-look")
def _(c):
    c.ground(G)
    c.stick(300, G, s=1.1, mood="neutral", arms="point_r")
    c.magnifier(700, 320, 1.6)
    c.text(700, 300, "$", 70, c=DGREEN)
    c.text(640, 70, "KNOW WHERE TO LOOK", 52)


@scene("3:46", "headlines-say-stuck-others-watch")
def _(c):
    c.rect(80, 120, 560, 560, fill=WHITE, w=5)
    c.text(320, 160, "NEWS", 50)
    c.text(320, 260, "DEAL STUCK!", 40, c=RED)
    for i in range(4):
        c.line([(110, 340 + i * 45), (530 - random.uniform(0, 120), 340 + i * 45)], w=3, c=DGREY)
    c.ground(G)
    for i in range(3):
        c.stick(760 + i * 170, G, s=0.9, mood="neutral", arms="think", face_dir=-1)
    c.text(940, 130, "WATCHING...", 44, c=BLUE)


@scene("3:51", "not-governments")
def _(c):
    c.ground(G)
    c.building(440, G, w=400, h=250, roof="bank", label="GOVERNMENT")
    c.x_mark(640, 400, 150, w=18)


@scene("3:53", "not-diplomats")
def _(c):
    c.ground(G)
    c.stick(500, G, s=1.2, mood="neutral", arms="hold", tie=RED, hat="top")
    c.stick(780, G, s=1.2, mood="neutral", arms="hold", tie=BLUE, hat="top")
    c.x_mark(640, 380, 170, w=18)
    c.text(640, 70, "DIPLOMATS", 50)


@scene("3:54", "middlemen")
def _(c):
    c.ground(G)
    for i, (h, m) in enumerate((("cap", "happy"), (None, "happy"), ("cap", "happy"), (None, "happy"))):
        c.stick(220 + i * 280, G, s=1.1, mood=m, arms="hips" if i % 2 else "wave", hat=h, tie=GREEN if i % 2 else None)
    c.text(640, 90, "MIDDLEMEN", 80, c=DGREEN)


@scene("3:55", "freight-forwarders")
def _(c):
    c.ground(G)
    c.stick(200, G, mood="happy", arms="point_r", hat="cap")
    c.truck(380, G, s=0.8)
    c.africa(1080, 250, 0.45)
    for n in ("ghana", "nigeria", "kenya", "zambia"):
        c.pin(*c.apt(1080, 250, 0.45, n), r=8)
    c.text(640, 60, "FREIGHT FORWARDERS", 48)


@scene("3:58", "customs-brokers-clear-fast")
def _(c):
    c.ground(G)
    c.stick(260, G, s=1.1, mood="happy", arms="raise_r", tie=BLUE)
    c.stamp_tool(380, 230, 1.2)
    c.doc(470, 260, 1.2, stamp=GREEN, title="CLEARED")
    c.clock(950, 330, 110, h=1)
    c.text(950, 490, "HOURS, NOT DAYS", 36, c=GREEN)


@scene("4:01", "payment-startups-bridge")
def _(c):
    c.coin(170, 420, 90, sym="₦")
    c.coin(1110, 420, 90, sym="₵")
    c.bridge(260, 1020, 420)
    c.laptop(640, 600, 1.1, screen="PAY")
    c.text(640, 120, "PAYMENT STARTUPS", 52, c=BLUE)


@scene("4:05", "warehouse-stock-early")
def _(c):
    c.ground(G)
    c.warehouse(100, G, 1.3)
    for i in range(4):
        c.box(620 + i * 75, G, 1.0)
    for i in range(3):
        c.box(655 + i * 75, G - 60, 1.0)
    c.stick(1120, G, mood="happy", arms="hips")
    c.text(900, 160, "READY BEFORE", 40)
    c.text(900, 220, "BUYERS ARRIVE", 40)


@scene("4:08", "not-waiting-for-perfect")
def _(c):
    c.ground(G)
    c.hourglass(250, 350, 1.4)
    c.x_mark(250, 350, 120, w=14)
    c.stick(800, G, s=1.2, mood="happy", arms="raise_r", legs="walk")
    c.text(800, 100, "NO WAITING", 54, c=GREEN)


@scene("4:11", "selling-cure-for-friction")
def _(c):
    c.ground(G)
    c.stick(330, G, s=1.2, mood="happy", arms="give_r", hat="cap")
    c.rect(470, 330, 560, 470, fill=LBLUE, w=4)
    c.rect(485, 300, 545, 330, fill=RED, w=3)
    c.text(515, 370, "CURE", 22)
    c.text(900, 250, "FRICTION", 50, c=RED)
    c.text(900, 320, "FIXER", 50, c=GREEN)


@scene("4:13", "every-delay-a-customer")
def _(c):
    c.ground(G)
    for i in range(3):
        c.truck(20 + i * 240, G, s=0.55)
    c.stick(1050, G, s=1.1, mood="rich", arms="out", hat="cap")
    c.text(640, 120, "DELAY = CUSTOMER", 56, c=DGREEN)
    c.coin(1150, 300, 30)


@scene("4:15", "confusing-form-is-a-service")
def _(c):
    c.doc(150, 180, 1.4, title="FORM ???")
    c.question(250, 450, 80)
    c.arrow(380, 330, 600, 330, w=7)
    c.ground(G)
    c.stick(770, G, mood="happy", arms="point_r", tie=GREEN)
    c.rect(920, 260, 1180, 380, fill=YELLOW, w=4)
    c.text(1050, 290, "$50 FEE", 44, c=DGREEN)


@scene("4:19", "not-betting-treaty-fails")
def _(c):
    c.ground(G)
    c.doc(250, 150, 1.6, title="TREATY", sig=True)
    c.text(330, 500, "FAILS?", 40)
    c.x_mark(780, 300, 100, w=16)
    c.stick(1100, G, mood="neutral", arms="hips")


@scene("4:21", "betting-it-works")
def _(c):
    c.ground(G)
    c.doc(250, 150, 1.6, title="TREATY", sig=True, stamp=GREEN)
    c.check(780, 300, 100, w=18)
    c.stick(1080, G, mood="happy", arms="up")
    c.coin(1000, 200, 30)
    c.coin(1160, 230, 30)
    c.text(640, 80, "BETTING IT WORKS", 50, c=GREEN)


@scene("4:23", "slowly")
def _(c):
    c.ground(G)
    shell = (640, 500)
    c.ellipse(shell[0], shell[1], 120, 90, fill=ORANGE, w=5)
    for r in (70, 40, 15):
        c.ellipse(shell[0] + 10, shell[1] + 5, r, r * 0.75, w=3)
    c.poly([(500, 600), (800, 600), (850, 560), (520, 570)], fill=TAN, w=4)
    c.line([(820, 570), (870, 480), (880, 470)], w=4)
    c.circle(880, 465, 8, fill=BLACK)
    c.text(640, 150, "S L O W L Y", 80)


@scene("4:24", "someone-has-to-make-it-work")
def _(c):
    c.ground(G)
    c.stick(400, G, s=1.2, mood="happy", arms="out", hat="cap")
    c.line([(304, 489), (290, 400)], w=8, c=BROWN)
    c.rect(265, 380, 315, 405, fill=GREY, w=4)
    c.truck(560, G, s=0.9)
    c.barrier(1100, G, closed=False)
    c.text(640, 80, "SOMEONE HAS TO DO IT", 50)


# ---------------- LESSON ----------------
@scene("4:27", "whats-the-lesson")
def _(c):
    c.ground(G)
    c.stick(300, G, s=1.3, mood="neutral", arms="think")
    c.rect(560, 160, 1160, 480, fill=DGREEN, w=6)
    c.text(860, 270, "LESSON?", 70, c=WHITE)


@scene("4:28", "opportunity-never-the-agreement")
def _(c):
    c.doc(200, 140, 1.8, title="AGREEMENT", sig=True)
    c.x_mark(320, 300, 120, w=16)
    c.text(860, 250, "NOT THE", 50)
    c.text(860, 330, "OPPORTUNITY", 50, c=RED)


@scene("4:31", "agreement-just-a-door")
def _(c):
    c.ground(G)
    c.door(520, G, 1.5, open_=True)
    c.rect(560, 160, 680, 210, fill=WHITE, w=3)
    c.text(620, 168, "DEAL", 30)
    c.text(1050, 250, "JUST A", 44)
    c.text(1050, 310, "DOOR", 60)


@scene("4:33", "money-in-the-hallway")
def _(c):
    c.line([(100, 100), (500, 280), (500, 480), (100, 650)], w=5)
    c.line([(1180, 100), (780, 280), (780, 480), (1180, 650)], w=5)
    c.rect(500, 280, 780, 480, w=5)
    for i in range(7):
        c.bill(random.uniform(330, 950), random.uniform(500, 680), 0.8, rot=random.uniform(-40, 40))
    c.money_bag(640, 440, 0.7)
    c.text(640, 50, "THE MONEY IS IN THE HALLWAY", 40, c=DGREEN)


@scene("4:35", "in-the-delays")
def _(c):
    c.clock(400, 330, 160, h=8)
    c.coin(720, 250, 50)
    c.coin(800, 360, 50)
    c.coin(700, 440, 50)
    c.text(1000, 300, "DELAYS", 56)


@scene("4:36", "in-the-confusion")
def _(c):
    c.ground(G)
    c.stick(400, G, s=1.2, mood="shock", arms="head")
    for _ in range(4):
        x, y = random.uniform(200, 600), random.uniform(60, 220)
        c.text(x, y, "?", 70, c=RED)
    c.line([(320, 120), (360, 80), (400, 130), (440, 70), (480, 120)], w=4, c=GREY)
    c.coin(900, 400, 70)
    c.text(900, 520, "CONFUSION", 44)


@scene("4:38", "problems-paperwork-forgot")
def _(c):
    c.stack_docs(250, 560, n=10, s=1.0)
    for i, t in enumerate(("PAYMENTS?", "TRUCKS?", "STORAGE?", "FORMS?")):
        c.text(850, 160 + i * 110, t, 44, c=RED)
    c.text(640, 50, "WHAT THE PAPERWORK FORGOT", 40)


@scene("4:41", "didnt-need-better-treaty")
def _(c):
    c.africa(300, 380, 1.0)
    c.doc(700, 120, 1.6, title="TREATY 2.0", sig=True)
    c.x_mark(800, 260, 120, w=16)
    c.text(800, 560, "NO NEW TREATY", 46)


@scene("4:43", "needs-people-make-it-usable")
def _(c):
    c.ground(G)
    c.doc(540, 120, 1.4, title="TREATY", stamp=GREEN)
    for i, (x, a) in enumerate(((180, "point_r"), (360, "hips"), (920, "wave"), (1100, "point_l"))):
        c.stick(x, G, s=1.0, mood="happy", arms=a, hat="cap" if i % 2 else None)
    c.text(640, 660, "PEOPLE MAKE IT WORK", 40, c=GREEN)


@scene("4:46", "solve-the-friction")
def _(c):
    c.ground(G)
    c.stick(300, G, s=1.3, mood="happy", arms="raise_r", hat="cap")
    c.lightbulb(300, 100, 0.9)
    c.text(830, 220, "SOLVE THE", 50)
    c.text(830, 300, "FRICTION", 70, c=ORANGE)
    c.check(830, 450, 70)


@scene("4:48", "not-waiting-on-future")
def _(c):
    c.ground(G)
    c.calendar(140, 160, 1.2, crossed=0)
    c.x_mark(270, 280, 110, w=16)
    c.stick(850, G, s=1.3, mood="happy", arms="hips", legs="walk")
    c.text(850, 90, "STOP WAITING", 50)


@scene("4:50", "youre-the-one-who-builds-it")
def _(c):
    c.africa(900, 360, 1.15, fill=GREEN)
    k = c.apt(900, 360, 1.15, "kenya")
    g = c.apt(900, 360, 1.15, "ghana")
    c.track([g, c.apt(900, 360, 1.15, "congo"), k])
    c.ground(G, x1=0, x2=500)
    c.stick(260, G, s=1.4, mood="happy", arms="up", hat="cap")
    c.text(260, 90, "YOU BUILD IT", 48, c=BLUE)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "images"
    os.makedirs(out, exist_ok=True)
    for i, (ts, slug, fn) in enumerate(S):
        c = Canvas(seed=i * 7 + 3)
        fn(c)
        m, s = ts.split(":")
        c.save(os.path.join(out, f"{i + 1:03d}_{int(m)}m{int(s):02d}s_{slug}.png"))
    print(len(S), "images ->", out)


if __name__ == "__main__":
    main()
