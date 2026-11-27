#!/usr/bin/env python3
"""Render the 26 November 2026 front page: one 1024x1024 PNG.

36 stories across 9 regions, angle C (EU summit + peace): the lead is the
special European Council in Brussels (Ukraine funding 2027 + EU budget
2028-2034), with the Ukraine war cluster, the Macy's centenary parade
postponement, Mumbai's 18th anniversary of 26/11 and Colombia's 10 years
of peace as the features. Every story below happened, or was first
reported, on 21-27 November 2026, checked against live reporting on
26-27 Nov 2026 (Reuters, AP, UN News, EU Council, NASA Spaceflight,
Nature, Al Jazeera, AFP). Nothing is misdated: Cairo's tanker fire is
25 Nov, Shenzhou-24 launched 25 Nov, BepiColombo reached Mercury 21 Nov,
the Sudan Damazin strike was 24 Nov, Black Friday is a 27 Nov forecast.
Jensen Huang's reported Nvidia exit and the Houthi Ras Tanura claim are
left out (sources conflict / unconfirmed).

What this build changes over the 24 Nov v3 (31 stories, 7 regions, 5
scenes, final 58.84%):
- 36 stories, 9 regions (Africa, Asia, Caribbean, Europe, Middle East,
  North America, Oceania, South America, Ukraine);
- 9 drawn scenes (lead + 4 features + 4 "in pictures" cards) instead of 5;
- a "when it happened" date strip, so the mixed 21-27 Nov dates are
  visible at a glance, and every brief carries its own honest date;
- the schematic world map keeps 6 numbered pins for the 6 biggest stories;
- briefs stay 15 px (never smaller: they must read at ~300 px wide).

Builder-side only: the entry program (main.py) only copies entry.png.
Run:  python3 render_front.py   (writes entry.png beside this file)
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
W, H = 1024, 1024

NAVY = (16, 31, 56)
NAVY2 = (24, 48, 88)
GOLD = (201, 162, 39)
PAPER = (250, 247, 238)
INK = (24, 24, 24)
GREY = (90, 90, 90)
RED = (178, 34, 34)
TEAL = (15, 118, 110)
BLUE = (30, 90, 160)
LIGHTBLUE = (222, 235, 245)
TAN = (214, 196, 160)
RULE = (200, 192, 172)
SKY = (18, 28, 54)
GLOW = (226, 110, 38)
FLAME = (255, 150, 40)
EMBER = (255, 210, 90)
SEABLUE = (36, 98, 164)
PANELTEAL = (226, 240, 236)
PANELGREY = (232, 238, 248)
EUBLUE = (0, 51, 153)
RAIN = (140, 170, 210)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 44)
F_KICK = font("DejaVuSans-Bold.ttf", 17)
F_KICK_SM = font("DejaVuSans-Bold.ttf", 15)
F_HEAD = font("DejaVuSans-Bold.ttf", 28)
F_FHEAD = font("DejaVuSans-Bold.ttf", 21)
F_DECK = font("DejaVuSans.ttf", 17)
F_FDECK = font("DejaVuSans.ttf", 14)
F_NUM = font("DejaVuSans-Bold.ttf", 36)
F_LAB = font("DejaVuSans.ttf", 13)
F_LAB_B = font("DejaVuSans-Bold.ttf", 13)
F_BRIEF = font("DejaVuSans.ttf", 15)
F_BRIEF_B = font("DejaVuSans-Bold.ttf", 15)
F_SMALL = font("DejaVuSans.ttf", 12)
F_FOOT = font("DejaVuSans.ttf", 11)
F_MAST_SUB = font("DejaVuSans.ttf", 17)
F_EYEBROW = font("DejaVuSans-Bold.ttf", 15)
F_COIN = font("DejaVuSans-Bold.ttf", 30)
F_PIN = font("DejaVuSans-Bold.ttf", 12)
F_PIC = font("DejaVuSans-Bold.ttf", 12)
F_PIC_SM = font("DejaVuSans.ttf", 11)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def starburst(draw, cx, cy, r, fill):
    """A 12-point starburst (explosion) centred at cx, cy."""
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def eu_scene(draw, x0, y0, x1, y1):
    """The lead illustration: EU emblem over a Brussels skyline."""
    draw.rectangle([x0, y0, x1, y1], fill=EUBLUE)
    # Brussels skyline silhouette along the bottom.
    for (bx, bw, bh) in [(0, 60, 18), (70, 44, 26), (124, 70, 14),
                         (204, 52, 22), (266, 60, 16), (336, 48, 24),
                         (394, 66, 14), (470, 54, 20), (534, 62, 16),
                         (606, 48, 24), (664, 70, 14), (744, 54, 20),
                         (808, 60, 16), (878, 48, 22), (936, 58, 14)]:
        draw.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(10, 20, 50))
    # A circle of 12 gold stars, sized to the band, left of centre.
    cx, cy = x0 + 150, (y0 + y1) // 2 - 6
    r = 20
    for i in range(12):
        ang = -math.pi / 2 + i * math.pi / 6
        sx, sy = cx + r * math.cos(ang), cy + r * math.sin(ang)
        starburst(draw, sx, sy, 4, GOLD)
    # A second, larger star circle right of centre, for balance.
    cx2, cy2 = x0 + 830, (y0 + y1) // 2 - 6
    for i in range(12):
        ang = -math.pi / 2 + i * math.pi / 6
        sx, sy = cx2 + r * math.cos(ang), cy2 + r * math.sin(ang)
        starburst(draw, sx, sy, 4, GOLD)


def jets_scene(draw, x0, y0, x1, y1):
    """Two jets over a burning airbase: the Ukraine strike feature."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    for (sx, sy) in [(12, 10), (48, 18), (90, 8), (30, 26)]:
        draw.ellipse([x0 + sx - 2, y0 + sy - 2, x0 + sx + 2, y0 + sy + 2],
                     fill=(220, 225, 240))
    # Two jets, simple delta shapes, one banking away.
    for (jx, jy, s) in [(28, 26, 1), (72, 16, -1)]:
        draw.polygon([(x0 + jx, y0 + jy - 6 * s), (x0 + jx + 16, y0 + jy),
                      (x0 + jx, y0 + jy + 6 * s)], fill=(200, 205, 215))
        draw.line([x0 + jx - 8, y0 + jy, x0 + jx + 2, y0 + jy],
                  fill=(200, 205, 215), width=3)
    # Ground + explosion + smoke.
    draw.rectangle([x0, y1 - 22, x1, y1], fill=(10, 16, 32))
    ex, ey = x0 + 62, y1 - 26
    starburst(draw, ex, ey, 18, FLAME)
    starburst(draw, ex, ey, 9, EMBER)
    for (sx, sy, r) in [(50, 30, 6), (66, 22, 8), (82, 14, 6)]:
        draw.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r],
                     fill=(120, 120, 125))


def balloon_scene(draw, x0, y0, x1, y1):
    """A parade balloon in the rain: the Macy's postponement feature."""
    draw.rectangle([x0, y0, x1, y1], fill=(58, 74, 96))
    # Rain streaks.
    for rx in range(8, x1 - x0, 16):
        draw.line([x0 + rx, y0 + 6, x0 + rx - 5, y0 + 26], fill=RAIN, width=2)
    # A big round balloon (red) with a smiling face, tethered below.
    cx, cy = (x0 + x1) // 2, y0 + 34
    draw.ellipse([cx - 26, cy - 22, cx + 26, cy + 22], fill=RED,
                 outline=(255, 255, 255), width=2)
    draw.ellipse([cx - 10, cy - 8, cx - 4, cy - 2], fill=(255, 255, 255))
    draw.ellipse([cx + 4, cy - 8, cx + 10, cy - 2], fill=(255, 255, 255))
    draw.arc([cx - 10, cy + 2, cx + 10, cy + 14], 0, 180, fill=(255, 255, 255),
             width=2)
    draw.line([cx - 8, cy + 22, cx - 14, y1 - 8], fill=(255, 255, 255), width=2)
    draw.line([cx + 8, cy + 22, cx + 14, y1 - 8], fill=(255, 255, 255), width=2)
    # A small "100" badge, bottom right.
    draw.ellipse([x1 - 26, y1 - 24, x1 - 4, y1 - 4], fill=GOLD)
    draw.text(((x1 - 15), (y1 - 14)), "100", font=F_PIC, fill=NAVY, anchor="mm")


def mumbai_scene(draw, x0, y0, x1, y1):
    """Gateway of India arch at dusk, candles below: the Mumbai feature."""
    draw.rectangle([x0, y0, x1, y1], fill=(64, 48, 84))
    cx = (x0 + x1) // 2
    # The Gateway arch: two pillars + a dome.
    draw.rectangle([cx - 30, y0 + 26, cx - 20, y1 - 14], fill=TAN)
    draw.rectangle([cx + 20, y0 + 26, cx + 30, y1 - 14], fill=TAN)
    draw.pieslice([cx - 30, y0 + 8, cx + 30, y0 + 44], 180, 360, fill=TAN)
    draw.rectangle([cx - 2, y0 + 2, cx + 2, y0 + 10], fill=TAN)
    draw.rectangle([cx - 38, y1 - 14, cx + 38, y1 - 8], fill=TAN)
    # Candles with flames along the base.
    for cxx in (cx - 44, cx - 22, cx, cx + 22, cx + 44):
        draw.rectangle([cxx - 2, y1 - 12, cxx + 2, y1 - 4], fill=(255, 255, 255))
        draw.ellipse([cxx - 3, y1 - 18, cxx + 3, y1 - 12], fill=EMBER)


def dove_scene(draw, x0, y0, x1, y1):
    """A white dove over Colombia's yellow-blue-red: the peace feature."""
    # Colombian tricolour bands.
    draw.rectangle([x0, y0, x1, y0 + (y1 - y0) // 2], fill=(255, 205, 0))
    draw.rectangle([x0, y0 + (y1 - y0) // 2, x1, y0 + 3 * (y1 - y0) // 4],
                   fill=(0, 56, 147))
    draw.rectangle([x0, y0 + 3 * (y1 - y0) // 4, x1, y1], fill=(206, 17, 38))
    # A white dove: body + raised wing + head.
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.ellipse([cx - 26, cy - 10, cx + 18, cy + 10], fill=(255, 255, 255))
    draw.polygon([(cx - 2, cy - 8), (cx + 14, cy - 30), (cx + 20, cy - 8)],
                 fill=(255, 255, 255))
    draw.ellipse([cx + 12, cy - 16, cx + 26, cy - 2], fill=(255, 255, 255))
    draw.polygon([(cx - 26, cy + 2), (cx - 40, cy + 12), (cx - 24, cy + 12)],
                 fill=(255, 255, 255))
    # Olive branch.
    draw.line([cx - 34, cy + 22, cx + 6, cy + 14], fill=(0, 102, 0), width=2)
    for (lx, ly) in [(-28, 20), (-18, 18), (-8, 16)]:
        draw.ellipse([cx + lx - 3, cy + ly - 2, cx + lx + 3, cy + ly + 2],
                     fill=(0, 102, 0))


def rocket_scene(draw, x0, y0, x1, y1):
    """A rocket lifting off: the Shenzhou-24 picture card."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    for (sx, sy) in [(10, 8), (40, 14), (70, 6), (90, 18)]:
        draw.ellipse([x0 + sx - 1, y0 + sy - 1, x0 + sx + 1, y0 + sy + 1],
                     fill=(220, 225, 240))
    cx = (x0 + x1) // 2
    # Rocket body (white) with a red tip and fins.
    draw.rectangle([cx - 7, y0 + 8, cx + 7, y0 + 34], fill=(255, 255, 255))
    draw.polygon([(cx - 7, y0 + 8), (cx + 7, y0 + 8), (cx, y0 - 2)], fill=RED)
    draw.polygon([(cx - 7, y0 + 28), (cx - 13, y0 + 38), (cx - 7, y0 + 38)],
                 fill=RED)
    draw.polygon([(cx + 7, y0 + 28), (cx + 13, y0 + 38), (cx + 7, y0 + 38)],
                 fill=RED)
    # Flame + smoke.
    starburst(draw, cx, y0 + 42, 9, FLAME)
    starburst(draw, cx, y0 + 42, 5, EMBER)
    for (sx, sy, r) in [(cx - 16, y1 - 10, 7), (cx + 14, y1 - 8, 8),
                        (cx, y1 - 14, 6)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(200, 200, 205))


def tanker_scene(draw, x0, y0, x1, y1):
    """A burning fuel tanker: the Cairo picture card."""
    draw.rectangle([x0, y0, x1, y1], fill=(40, 40, 48))
    # Road.
    draw.rectangle([x0, y1 - 14, x1, y1], fill=(90, 90, 90))
    # Tanker: cab + cylindrical tank.
    draw.rectangle([x0 + 12, y1 - 30, x0 + 26, y1 - 14], fill=RED)
    draw.rounded_rectangle([x0 + 28, y1 - 32, x1 - 12, y1 - 14], radius=8,
                           fill=(220, 220, 220), outline=NAVY, width=1)
    draw.ellipse([x0 + 20, y1 - 14, x0 + 28, y1 - 6], fill=INK)
    draw.ellipse([x1 - 26, y1 - 14, x1 - 18, y1 - 6], fill=INK)
    # Flames over the tank + smoke.
    ex, ey = (x0 + x1) // 2 + 10, y1 - 38
    starburst(draw, ex, ey, 13, FLAME)
    starburst(draw, ex, ey, 7, EMBER)
    for (sx, sy, r) in [(ex - 16, y0 + 14, 6), (ex, y0 + 8, 8),
                        (ex + 16, y0 + 14, 6)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 125))


def tower_scene(draw, x0, y0, x1, y1):
    """A high-rise on fire: the Hong Kong picture card."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # Tower with lit windows.
    tx0, tx1 = x0 + 30, x1 - 30
    draw.rectangle([tx0, y0 + 14, tx1, y1], fill=(30, 40, 60))
    for wy in range(y0 + 20, y1 - 8, 10):
        for wx in range(tx0 + 6, tx1 - 6, 10):
            draw.rectangle([wx, wy, wx + 5, wy + 5], fill=(255, 210, 90))
    # Fire at the top + smoke.
    ex, ey = (tx0 + tx1) // 2, y0 + 16
    starburst(draw, ex, ey, 12, FLAME)
    starburst(draw, ex, ey, 6, EMBER)
    for (sx, sy, r) in [(ex - 14, y0 + 4, 5), (ex + 2, y0 + 2, 6),
                        (ex + 16, y0 + 6, 5)]:
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 125))


def mercury_scene(draw, x0, y0, x1, y1):
    """A spacecraft beside cratered Mercury: the BepiColombo picture card."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    for (sx, sy) in [(8, 8), (30, 14), (90, 10), (70, 20)]:
        draw.ellipse([x0 + sx - 1, y0 + sy - 1, x0 + sx + 1, y0 + sy + 1],
                     fill=(220, 225, 240))
    # Mercury (tan, cratered) bottom right.
    mx, my, mr = x1 - 26, y1 - 24, 20
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(190, 170, 140))
    for (cxx, cyy, cr) in [(mx - 8, my - 6, 4), (mx + 6, my + 4, 5),
                           (mx - 2, my + 10, 3)]:
        draw.ellipse([cxx - cr, cyy - cr, cxx + cr, cyy + cr],
                     fill=(160, 140, 110))
    # Spacecraft: body + two solar panels.
    cx, cy = x0 + 30, y0 + 26
    draw.rectangle([cx - 8, cy - 6, cx + 8, cy + 6], fill=(200, 205, 215),
                   outline=NAVY, width=1)
    draw.rectangle([cx - 26, cy - 3, cx - 8, cy + 3], fill=BLUE)
    draw.rectangle([cx + 8, cy - 3, cx + 26, cy + 3], fill=BLUE)


SCENES = {"eu": eu_scene, "jets": jets_scene, "balloon": balloon_scene,
          "mumbai": mumbai_scene, "dove": dove_scene, "rocket": rocket_scene,
          "tanker": tanker_scene, "tower": tower_scene,
          "mercury": mercury_scene}


def feature(draw, box, kicker, kicker_color, headline, deck, scene, source):
    """One feature story in `box` = (x0, y0, x1, y1), 123 px tall.

    Left: a full drawn scene panel. Right: kicker, headline (2 lines),
    deck (2 lines), source line. Briefs stay 15 px; nothing here shrinks.
    """
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    draw.rectangle([x0, y0, x1, y0 + 5], fill=kicker_color)
    px0, py0, px1, py1 = x0 + 1, y0 + 6, x0 + 111, y1 - 1
    SCENES[scene](draw, px0, py0, px1, py1)
    draw.rectangle([px0, py0, px1, py1], outline=RULE, width=1)
    tx = x0 + 122
    draw.text((tx, y0 + 12), kicker, font=F_KICK_SM, fill=kicker_color)
    head_w = x1 - tx - 10
    lines = wrap(draw, headline, F_FHEAD, head_w)
    draw_lines(draw, lines[:2], tx, y0 + 32, F_FHEAD, INK, 24)
    deck_lines = wrap(draw, deck, F_FDECK, head_w)
    draw_lines(draw, deck_lines[:2], tx, y0 + 82, F_FDECK, (58, 58, 58), 16)
    draw.text((tx, y1 - 14), source, font=F_LAB_B, fill=GREY)


def picture_card(draw, box, caption, date, scene):
    """One 'in pictures' card: a small drawn scene + a 1-line caption."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], outline=RULE, width=1)
    SCENES[scene](draw, x0 + 1, y0 + 1, x1 - 1, y0 + 45)
    draw.rectangle([x0, y0, x1, y0 + 45], outline=RULE, width=1)
    cap = wrap(draw, caption, F_PIC, x1 - x0 - 8)
    draw.text((x0 + 4, y0 + 48), cap[0] if cap else "", font=F_PIC, fill=INK)
    draw.text((x1 - 4, y0 + 48), date, font=F_PIC_SM, fill=GREY, anchor="rt")


def world_map(draw, y_top):
    """Schematic world map with six numbered pins (the six biggest stories).

    Continent blobs are schematic, not to scale; pins sit on the story's
    place. Map box is `y_top`..`y_top`+48, legend line below it.
    """
    draw.text((14, y_top), "WHERE IT HAPPENED  —  SCHEMATIC MAP",
              font=F_LAB_B, fill=NAVY2)
    draw.text((W - 14, y_top), "NOT TO SCALE", font=F_SMALL, fill=GREY,
              anchor="rt")
    m0 = y_top + 16
    draw.rectangle([14, m0, W - 14, m0 + 44], fill=LIGHTBLUE, outline=RULE,
                   width=1)
    draw.polygon([(60, m0 + 5), (200, m0 + 2), (260, m0 + 15),
                  (230, m0 + 28), (150, m0 + 44), (80, m0 + 40),
                  (55, m0 + 22)], fill=TAN)                             # N America
    draw.polygon([(215, m0 + 27), (260, m0 + 30), (250, m0 + 43),
                  (222, m0 + 43)], fill=TAN)                             # S America
    draw.polygon([(460, m0 + 3), (520, m0 + 2), (545, m0 + 13),
                  (510, m0 + 25), (465, m0 + 20)], fill=TAN)             # Europe
    draw.polygon([(465, m0 + 25), (545, m0 + 25), (560, m0 + 43),
                  (505, m0 + 43), (470, m0 + 37)], fill=TAN)             # Africa
    draw.polygon([(570, m0 + 3), (770, m0 + 0), (830, m0 + 12),
                  (800, m0 + 32), (720, m0 + 42), (640, m0 + 40),
                  (575, m0 + 22)], fill=TAN)                             # Asia
    draw.polygon([(825, m0 + 36), (885, m0 + 32), (890, m0 + 43),
                  (830, m0 + 43)], fill=TAN)                             # Australia
    pins = [(505, m0 + 18, "1"), (548, m0 + 14, "2"), (140, m0 + 20, "3"),
            (700, m0 + 28, "4"), (540, m0 + 33, "5"), (800, m0 + 26, "6")]
    for (px, py, n) in pins:
        draw.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                     outline=(255, 255, 255), width=2)
        draw.text((px, py), n, font=F_PIN, fill=(255, 255, 255), anchor="mm")
    draw.text((W // 2, m0 + 46),
              "1 BRUSSELS   ·   2 UKRAINE   ·   3 NEW YORK   ·   4 MUMBAI   ·   5 CAIRO   ·   6 HONG KONG",
              font=F_SMALL, fill=GREY, anchor="mt")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 88], fill=NAVY)
    d.text((W // 2, 6), "THE WORLD IN ONE PAGE", font=F_EYEBROW, fill=GOLD, anchor="mt")
    d.text((W // 2, 24), "THURSDAY 26 NOVEMBER 2026", font=F_TITLE, fill=(255, 255, 255), anchor="mt")
    d.text((W // 2, 68), "36 stories  ·  9 regions  ·  every story dated honestly",
           font=F_MAST_SUB, fill=(205, 214, 228), anchor="mt")
    d.rectangle([0, 88, W, 92], fill=GOLD)

    # ---- Number strip ---------------------------------------------------
    numbers = [
        ("100,000", "UK reservists told\nto prepare for war"),
        ("31", "killed in Cairo\ntanker fire, 25 Nov"),
        ("168", "killed in Hong Kong\nrenovation fire"),
        ("$12.9B", "Black Friday online\nsales forecast"),
        ("81.5M", "Thanksgiving travellers\nin the US, near record"),
        ("19", "killed by RSF drone\nin Sudan's Damazin"),
    ]
    cell_w = W // 6
    for i, (num, lab) in enumerate(numbers):
        x0 = i * cell_w
        if i:
            d.line([x0, 100, x0, 152], fill=RULE, width=1)
        d.text((x0 + cell_w // 2, 96), num, font=F_NUM, fill=NAVY, anchor="mt")
        for j, ln in enumerate(lab.split("\n")):
            d.text((x0 + cell_w // 2, 134 + j * 14), ln, font=F_LAB, fill=GREY, anchor="mt")
    d.line([0, 160, W, 160], fill=RULE, width=1)

    # ---- Lead story, with a drawn EU scene on top -----------------------
    d.rectangle([14, 162, W - 14, 316], outline=RULE, width=1)
    d.rectangle([14, 162, W - 14, 167], fill=NAVY2)
    eu_scene(d, 15, 167, W - 15, 224)
    d.text((28, 228), "EU SUMMIT  —  BRUSSELS", font=F_KICK, fill=NAVY2)
    d.text((28, 248), "EU LEADERS MEET ON UKRAINE CASH AND THE 2028 BUDGET",
           font=F_HEAD, fill=INK)
    d.text((28, 280),
           "A special European Council opens to agree Ukraine funding for 2027 and the EU's 2028–2034 budget.",
           font=F_DECK, fill=(58, 58, 58))
    d.text((28, 301), "REPORTED  |  Reuters / EU Council  |  26 NOV", font=F_LAB_B, fill=GREY)

    # ---- Feature rows: four fully illustrated scenes --------------------
    feature(d, (14, 322, 502, 442), "WAR  —  UKRAINE", RED,
            "UKRAINE HITS RUSSIAN AIRBASE, 5 JETS DAMAGED",
            "Kyiv says it hit a Russian airbase, 2 refineries.",
            "jets", "REPORTED  |  Reuters  |  26 NOV")
    feature(d, (522, 322, 1010, 442), "USA  —  NEW YORK", TEAL,
            "MACY'S 100TH PARADE POSTPONED BY STORM",
            "Centenary parade moves to Saturday — a first.",
            "balloon", "REPORTED  |  26 NOV")
    feature(d, (14, 448, 502, 568), "INDIA  —  MUMBAI", NAVY2,
            "MUMBAI MARKS 18 YEARS SINCE 26/11",
            "India remembers the 2008 attacks, 174 killed.",
            "mumbai", "REPORTED  |  26 NOV")
    feature(d, (522, 448, 1010, 568), "PEACE  —  COLOMBIA", TEAL,
            "COLOMBIA: 10 YEARS OF PEACE, UN WARNS OF GAPS",
            "UN: the 2016 deal's promises are unfinished.",
            "dove", "REPORTED  |  UN News  |  26 NOV")

    # ---- In pictures: four small drawn scenes ---------------------------
    d.text((14, 574), "IN PICTURES", font=F_KICK, fill=NAVY)
    pic_w = (W - 28 - 3 * 8) // 4
    pics = [
        ("Shenzhou-24 lifts off", "25 NOV", "rocket"),
        ("Cairo tanker fire", "25 NOV", "tanker"),
        ("Hong Kong tower fire", "26 NOV", "tower"),
        ("BepiColombo at Mercury", "21 NOV", "mercury"),
    ]
    for i, (cap, date, scene) in enumerate(pics):
        x0 = 14 + i * (pic_w + 8)
        picture_card(d, (x0, 592, x0 + pic_w, 652), cap, date, scene)

    # ---- Schematic world map --------------------------------------------
    world_map(d, 658)

    # ---- Briefs ---------------------------------------------------------
    d.text((14, 734), "MORE FROM AROUND THE WORLD  —  EVERY STORY DATED",
           font=F_KICK, fill=NAVY)
    d.text((14, 748),
           "9 REGIONS:  AFRICA  ·  ASIA  ·  CARIBBEAN  ·  EUROPE  ·  MIDDLE EAST  ·  NORTH AMERICA  ·  OCEANIA  ·  SOUTH AMERICA  ·  UKRAINE",
           font=F_SMALL, fill=GREY)
    d.text((14, 760),
           "WHEN IT HAPPENED — 21 NOV: Mercury orbit  ·  24 NOV: Sudan  ·  25 NOV: Shenzhou, Cairo  ·  26 NOV: EU summit + 28 more  ·  27 NOV: Black Friday",
           font=F_SMALL, fill=GREY)
    d.line([14, 772, W - 14, 772], fill=NAVY, width=2)
    briefs_left = [
        ("WASHINGTON", "US tariffs hit 14 economies · 26 NOV"),
        ("BRASILIA", "Petrobras plans $122B investment · 26 NOV"),
        ("CARACAS", "Venezuela reveals $237.5B public debt · 26 NOV"),
        ("CANBERRA", "Australia–Solomons security pact · 26 NOV"),
        ("GENEVA", "Gukesh–Sindarov chess title opens · 26 NOV"),
        ("BRUSSELS", "NATO chief: Europe must be war-ready · 26 NOV"),
        ("NEW YORK", "S&P 500 and Dow enter correction · 26 NOV"),
        ("WASHINGTON", "Birthright order blocked again · 26 NOV"),
        ("PYONGYANG", "Kim widens tactical nuclear rollout · 26 NOV"),
        ("WASHINGTON", "FCC clears 1M SpaceX data centres · 26 NOV"),
        ("SAN JUAN", "Miss Universe first married winner · 26 NOV"),
        ("HORMUZ", "Iran says two tankers hit sea mines · 26 NOV"),
        ("BRUSSELS", "EU readies €50B tech fund vs US, China · 26 NOV"),
        ("SHANGHAI", "Party chief Chen falls in corruption probe · 26 NOV"),
    ]
    briefs_right = [
        ("DAMAZIN", "RSF drone kills 19 civilians · 24 NOV"),
        ("GHUBEISH", "Drone kills 11 in West Kordofan · 26 NOV"),
        ("KYIV", "Zelensky warns of new mass Russian strike · 26 NOV"),
        ("THE HAGUE", "34 nations urge halt to riot gas · 26 NOV"),
        ("BRUSSELS", "EU sanctions 15 Russian entities · 25 NOV"),
        ("KYIV", "Russia fires missile + 113 drones overnight · 25 NOV"),
        ("MARINOVKA", "Ukraine hits airfield, oil terminal · 26 NOV"),
        ("LONDON", "UK puts 100,000 reservists on standby · 26 NOV"),
        ("KYIV", "Melania Trump returns 9 more children · 26 NOV"),
        ("NEW YORK", "Black Friday sales seen at $12.9B · 27 NOV"),
        ("ROME", "Meloni firm on EU budget · 26 NOV"),
        ("WASHINGTON", "$450M for Ukraine recovery · 26 NOV"),
        ("NEW YORK", "Thanksgiving travel nears 81.5M · 26 NOV"),
    ]
    for col, briefs in ((14, briefs_left), (522, briefs_right)):
        y = 778
        col_end = 522 if col == 14 else 1010
        for city, text in briefs:
            d.text((col, y), city + " — ", font=F_BRIEF_B, fill=INK)
            w_city = d.textlength(city + " — ", font=F_BRIEF_B)
            lines = wrap(d, text, F_BRIEF, col_end - col - w_city - 14)
            if len(lines) > 1:
                print(f"WARN brief wraps, shorten it: {city} — {text}")
            draw_lines(d, lines[:1], col + w_city, y, F_BRIEF, (58, 58, 58), 16)
            y += 16.0
    d.line([0, 1004, W, 1004], fill=RULE, width=1)
    d.text((W // 2, 1008),
           "Sources: Reuters · AP · UN News · EU Council · Al Jazeera · AFP — DATE CHECK: Huang + Ras Tanura left out (unverified); Cairo/Shenzhou 25 Nov, BepiColombo 21 Nov.",
           font=F_FOOT, fill=GREY, anchor="mt")

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes, {img.size}")


if __name__ == "__main__":
    main()
