#!/usr/bin/env python3
"""Generate entry.png: a one-page newspaper summary of the world news of
Saturday 21 November 2026. Run: python3 tools/generate_image.py
Writes news-21nov-image/entry.png (1024x1024, deterministic).

News sources (verified 21 Nov 2026 via web search):
- Russia's overnight strike on Ukraine / missiles land in Poland:
  AP via reflector.com, ISW assessment 20 Nov 2026, europesays.com
- Trump press conference after Shenzhen trilateral summit:
  USA Today, NY Post, Fox News, 20 Nov 2026
- ICJ finds Myanmar guilty of Rohingya genocide (19 Nov 2026):
  CNN, Reuters, WSJ, HRW, Amnesty, 19-20 Nov 2026
- GTA VI $3.79bn in 24 hours: Game Informer, Barron's, Pure Xbox, 20 Nov 2026
- AI stock sell-off, S&P 500 into correction: oneturn.news day page 21 Nov 2026
- Voyager 1 one light-day from Earth: oneturn.news / aggregators, 21 Nov 2026
- Pancreatic cancer pill (daraxonrasib) trial: oneturn.news, 21 Nov 2026
- Houthi missiles intercepted over Riyadh: oneturn.news, 21 Nov 2026
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 234)
INK = (26, 26, 26)
NAVY = (18, 38, 75)
NAVY_DARK = (13, 28, 56)
RED = (185, 28, 28)
GOLD = (201, 162, 39)
AMBER = (232, 163, 23)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (200, 192, 175)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=None):
    """Draw wrapped text; return y just below the last line."""
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def starburst(draw, cx, cy, r_out, r_in, n=12, fill=(255, 210, 63)):
    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def curve(draw, p0, p1, p2, steps=40, **kw):
    """Quadratic bezier polyline."""
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        pts.append((x, y))
    draw.line(pts, **kw)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 124], fill=NAVY)
d.text((512, 12), "T H E   W O R L D   I N   O N E   P A G E",
       font=font(SANS_B, 19), fill=GOLD, anchor="ma")
d.text((512, 34), "SATURDAY, 21 NOVEMBER 2026",
       font=font(SERIF_B, 48), fill=(255, 255, 255), anchor="ma")
d.line([(24, 96), (1000, 96)], fill=GOLD, width=2)
d.text((512, 101), "THE DAY'S WORLD NEWS  —  SUMMED UP IN ONE IMAGE",
       font=font(SANS, 13), fill=(200, 210, 230), anchor="ma")
d.rectangle([0, 124, W, 130], fill=RED)

# ---------------------------------------------------------------- lead story
d.rectangle([24, 140, 1000, 448], fill=CARD, outline=LINE, width=2)
d.text((48, 152), "LEAD STORY  ·  WAR IN UKRAINE",
       font=font(SANS_B, 17), fill=RED)
y = text_block(d, 48, 178,
               "RUSSIA'S BIGGEST STRIKE HITS UKRAINE — MISSILES LAND IN POLAND",
               font(SERIF_B, 33), INK, 556, leading=40)
y += 4
y = text_block(d, 48, y,
               "Overnight, Russia fired 400+ drones and 110 missiles at Ukraine — "
               "its largest barrage of the month. At least 8 were killed in Kyiv as "
               "bridges and power plants were hit.",
               font(SANS, 17), (60, 60, 60), 556, leading=22)
y += 6
d.line([(48, y), (592, y)], fill=LINE, width=1)
y += 8
y = text_block(d, 48, y,
               "Tusk: “intentional provocation”  ·  NATO: “grave violation”",
               font(SANS_B, 16), NAVY, 556, leading=20)
y += 8
chips = ["400+ DRONES", "110 MISSILES", "8 KILLED IN KYIV"]
cx = 48
for c in chips:
    f = font(SANS_B, 15)
    w = d.textlength(c, font=f) + 22
    d.rounded_rectangle([cx, y, cx + w, y + 30], radius=15, fill=NAVY)
    d.text((cx + w / 2, y + 15), c, font=f, fill=(255, 255, 255), anchor="mm")
    cx += w + 10

# --- schematic map panel (right side of lead story)
mx0, my0, mx1, my1 = 620, 152, 976, 436
d.rectangle([mx0, my0, mx1, my1], fill=NAVY_DARK)
land = [(640, 170), (700, 160), (770, 168), (850, 158), (930, 170), (962, 200),
        (955, 260), (960, 330), (930, 400), (880, 425), (800, 420), (720, 428),
        (660, 410), (638, 340), (632, 260), (636, 200)]
d.polygon(land, fill=(42, 64, 102))
d.polygon([(850, 158), (930, 170), (962, 200), (955, 260), (960, 330),
           (930, 400), (905, 405), (900, 300), (895, 210)], fill=(94, 58, 66))
d.text((928, 335), "RUSSIA", font=font(SANS_B, 13), fill=(220, 170, 170), anchor="mm")
ukr = [(700, 300), (790, 290), (880, 300), (895, 350), (860, 405), (760, 410),
       (700, 380), (685, 335)]
d.polygon(ukr, fill=AMBER)
d.text((790, 356), "UKRAINE", font=font(SANS_B, 15), fill=(40, 26, 0), anchor="mm")
pol = [(668, 218), (730, 210), (760, 232), (745, 268), (690, 272), (662, 246)]
d.polygon(pol, fill=(214, 69, 69))
d.text((700, 260), "POLAND", font=font(SANS_B, 13), fill=(255, 255, 255), anchor="mm")
d.ellipse([772, 316, 784, 328], fill=(255, 255, 255))
d.text((764, 322), "KYIV", font=font(SANS_B, 13), fill=(255, 255, 255), anchor="rm")
curve(d, (930, 200), (870, 235), (784, 320), fill=(255, 170, 60), width=3)
curve(d, (930, 265), (850, 215), (748, 236), fill=(255, 170, 60), width=3)
starburst(d, 784, 322, 12, 6)
starburst(d, 748, 236, 10, 5)
d.text((798, 420), "SCHEMATIC MAP — NOT TO SCALE",
       font=font(SANS, 11), fill=(160, 175, 200), anchor="ma")

# ---------------------------------------------------------------- row 2
def panel(x0, y0, x1, y1, fill=CARD):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=LINE, width=2)

# --- summit (left)
panel(24, 460, 500, 656)
d.text((44, 472), "DIPLOMACY  ·  SHENZHEN SUMMIT", font=font(SANS_B, 15), fill=RED)
y = text_block(d, 44, 494,
               "TRUMP DEFENDS PUTIN & XI TIES AFTER HISTORIC SUMMIT",
               font(SERIF_B, 23), INK, 436, leading=27)
y += 4
y = text_block(d, 44, y,
               "After the first US–China–Russia summit, Trump held a 90-minute White "
               "House press conference.",
               font(SANS, 15), (60, 60, 60), 436, leading=19)
d.text((44, 600), "Joint declaration: UN reform · nuclear-risk talks · oil supply",
       font=font(SANS_B, 13), fill=NAVY)
fx, fy = 44, 626
d.rectangle([fx, fy, fx + 40, fy + 24], fill=(255, 255, 255), outline=INK, width=1)
for i in range(4):
    d.rectangle([fx, fy + i * 6, fx + 40, fy + i * 6 + 3], fill=RED)
d.rectangle([fx, fy, fx + 18, fy + 12], fill=NAVY)
d.rectangle([fx + 50, fy, fx + 90, fy + 24], fill=(222, 41, 16), outline=INK, width=1)
d.text((fx + 70, fy + 12), "★", font=font(SANS_B, 12), fill=(255, 222, 0), anchor="mm")
d.rectangle([fx + 100, fy, fx + 140, fy + 24], fill=(255, 255, 255), outline=INK, width=1)
d.rectangle([fx + 100, fy + 8, fx + 140, fy + 16], fill=(0, 57, 166))
d.rectangle([fx + 100, fy + 16, fx + 140, fy + 24], fill=(213, 0, 50))
d.text((fx + 152, fy + 12), "US · CHINA · RUSSIA", font=font(SANS_B, 13), fill=INK)

# --- justice (right)
panel(524, 460, 1000, 656)
d.text((544, 472), "THE HAGUE  ·  WORLD COURT", font=font(SANS_B, 15), fill=RED)
y = text_block(d, 544, 494,
               "MYANMAR GUILTY OF ROHINGYA GENOCIDE",
               font(SERIF_B, 23), INK, 436, leading=27)
y += 4
y = text_block(d, 544, y,
               "The World Court ruled Myanmar committed genocide — the first time it "
               "has ever held a state responsible.",
               font(SANS, 15), (60, 60, 60), 436, leading=19)
d.text((544, 600), "10,000 killed in 2017; reparations ordered.",
       font=font(SANS_B, 13), fill=NAVY)
sx, sy = 962, 486
d.line([(sx, sy - 16), (sx, sy + 16)], fill=NAVY, width=3)
d.line([(sx - 16, sy - 16), (sx + 16, sy - 16)], fill=NAVY, width=3)
d.ellipse([sx - 3, sy - 21, sx + 3, sy - 16], fill=NAVY)
for dx in (-16, 16):
    d.line([(sx + dx, sy - 16), (sx + dx, sy - 3)], fill=NAVY, width=2)
    d.polygon([(sx + dx - 9, sy - 3), (sx + dx + 9, sy - 3), (sx + dx, sy + 8)],
              outline=NAVY, width=2)

# ---------------------------------------------------------------- row 3
# --- GTA VI (dark neon panel)
panel(24, 668, 348, 868, fill=(27, 16, 53))
d.text((44, 680), "CULTURE  ·  VIDEO GAMES", font=font(SANS_B, 14), fill=(255, 120, 200))
d.text((44, 700), "GTA VI", font=font(SERIF_B, 46), fill=(255, 45, 149))
y = text_block(d, 44, 752,
               "$3.79 BILLION IN 24 HOURS",
               font(SANS_B, 20), (255, 210, 63), 284, leading=25)
y += 4
text_block(d, 44, y,
           "Biggest entertainment launch ever. 32.5M pre-orders. Metacritic 99.",
           font(SANS, 14), (230, 230, 240), 284, leading=18)

# --- markets
panel(356, 668, 668, 868)
d.text((376, 680), "MARKETS  ·  WALL STREET", font=font(SANS_B, 14), fill=RED)
y = text_block(d, 376, 704,
               "AI SELL-OFF SENDS S&P 500 INTO CORRECTION",
               font(SERIF_B, 22), INK, 272, leading=26)
y += 4
y = text_block(d, 376, y,
               "US stocks fell 3.7% as AI and chip shares slid.",
               font(SANS, 14), (60, 60, 60), 272, leading=18)
d.text((656, 680), "▼ 3.7%", font=font(SANS_B, 13), fill=RED, anchor="ra")
cx0, cy0, cx1, cy1 = 386, 812, 638, 856
d.line([(cx0, cy0), (cx0, cy1), (cx1, cy1)], fill=GREY, width=2)
pts = [(cx0 + 8, cy0 + 4), (cx0 + 60, cy0 + 10), (cx0 + 110, cy0 + 8),
       (cx0 + 160, cy0 + 22), (cx0 + 210, cy0 + 32), (cx0 + 244, cy0 + 42)]
d.line(pts, fill=RED, width=4)

# --- science
panel(676, 668, 1000, 868, fill=(10, 20, 44))
d.text((696, 680), "SCIENCE  ·  SPACE", font=font(SANS_B, 14), fill=(120, 200, 255))
y = text_block(d, 696, 704,
               "VOYAGER 1: ONE LIGHT-DAY FROM EARTH",
               font(SERIF_B, 22), (255, 255, 255), 284, leading=26)
y += 4
y = text_block(d, 696, y,
           "49 years on, Voyager 1 is the first human-made object a light-day away.",
           font(SANS, 14), (215, 225, 240), 284, leading=18)
text_block(d, 696, y + 4,
           "Also: a cancer pill trial made tumours undetectable in 1 in 12 patients.",
           font(SANS, 13), (180, 200, 230), 284, leading=17)
for (sx2, sy2, r) in [(700, 852, 2), (730, 840, 1)]:
    d.ellipse([sx2 - r, sy2 - r, sx2 + r, sy2 + r], fill=(255, 255, 255))
d.line([(952, 706), (976, 682)], fill=(255, 210, 63), width=3)
d.ellipse([970, 676, 982, 688], fill=(255, 210, 63))

# ---------------------------------------------------------------- ticker + footer
d.rectangle([24, 880, 1000, 920], fill=NAVY)
d.text((44, 900), "ALSO TODAY:",
       font=font(SANS_B, 15), fill=GOLD, anchor="lm")
d.text((172, 900),
       "Houthi missiles intercepted over Riyadh  ·  US–Iran talks stall  ·  "
       "Denmark, US & Greenland sign security deal",
       font=font(SANS, 15), fill=(255, 255, 255), anchor="lm")
d.text((512, 940), "SATURDAY 21 NOVEMBER 2026  ·  THE WORLD IN ONE PAGE",
       font=font(SANS_B, 15), fill=GREY, anchor="ma")
d.text((512, 962), "make.fun  ·  news-image-20261121",
       font=font(SANS, 13), fill=GREY, anchor="ma")

out_path = "entry.png"
img.save(out_path, optimize=True)
print("wrote", out_path, img.size)
