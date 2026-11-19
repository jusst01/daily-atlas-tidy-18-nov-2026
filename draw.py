#!/usr/bin/env python3
"""Render THE DAILY ATLAS front page for 18 November 2026 -> entry.png.

Build-time only: Pillow + numpy. Every glyph on the page comes from the
story data below, exactly as the brief gives it. Flat colour fills and
crisp text only - no texture, grain, noise or ageing anywhere.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SERIF_ITALIC = os.path.join(FONT_DIR, "DejaVuSerif-Italic.ttf")
if not os.path.exists(SERIF_ITALIC):
    SERIF_ITALIC = SERIF
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

# Palette
PAPER = (244, 242, 236)
CARD = (255, 255, 252)
INK = (28, 28, 30)
GREY = (102, 102, 108)
ACCENT = (58, 84, 128)
TEAL = (44, 96, 88)
NAVY = (38, 58, 92)
BORDER = (198, 200, 208)
DATE_CHECK_RED = (172, 62, 44)

CONTINENTS = {
    "Americas": (168, 62, 44),
    "Europe": (58, 84, 128),
    "Mideast": (186, 122, 38),
    "Africa": (122, 106, 52),
    "Asia": (116, 80, 148),
    "Oceania": (44, 124, 134),
}

# --------------------------------------------------------------------------
# Story data (typeset exactly as the brief gives it)
# --------------------------------------------------------------------------
FEATURED = {
    1: {
        "kick": "IRAN - GULF",
        "head": "Iran strikes back; US hits Qeshm",
        "summ": "US jets hit an IRGC site on Qeshm; Iran answered on Kuwait and Bahrain - Bahrain says it intercepted several.",
        "continent": "Mideast",
        "kind": "missiles",
        "tag": "STRIKES ON BOTH SIDES",
        "chip": "CONFIRMED - REUTERS/AP",
    },
    2: {
        "kick": "ASIA - APEC SUMMIT",
        "head": "Xi and Putin meet in Shenzhen",
        "summ": "The two denounce protectionism and Western sanctions; the first Trump-Xi-Putin trilateral is set for Thursday.",
        "continent": "Asia",
        "kind": "flags",
        "tag": "THREE-WAY ON THURSDAY",
        "chip": "CONFIRMED - JUST SECURITY",
    },
    3: {
        "kick": "ASIA - QUAD",
        "head": "Quad meets; Trump lands in Manila",
        "summ": "First leader-level Quad meeting in 2+ years; Trump meets Marcos Jr. and announces a Philippines trade deal.",
        "continent": "Asia",
        "kind": "harbour",
        "tag": "MANILA FIRST",
        "chip": "CONFIRMED - OPENCHRONICLE",
    },
}

GRID = {
    4: {"kick": "UKRAINE - WAR", "head": "Russia fires 141 drones; 126 downed", "summ": "Overnight barrage, hits at 7 sites.", "continent": "Europe", "kind": "drones", "chip": "CLAIM - KYIV"},
    5: {"kick": "EUROPE - UKRAINE AID", "head": "EU proposes a 45bn-euro Ukraine loan", "summ": "25bn military, 20bn budget for 2027.", "continent": "Europe", "kind": "euro", "chip": "CONFIRMED - REUTERS"},
    6: {"kick": "US - MARKETS", "head": "Fed minutes back more hikes; Dow -561", "summ": "S and P 500 -0.23%, Nasdaq +0.42%.", "continent": "Americas", "kind": "dow", "chip": "CONFIRMED - REUTERS"},
    7: {"kick": "MARKETS - GOLD", "head": "Gold sinks to a 14-month low", "summ": "Closed $3,725 an ounce, down 3.2%.", "continent": "Americas", "kind": "gold", "chip": "CONFIRMED - REUTERS"},
    8: {"kick": "TECH - IPO", "head": "Anthropic prices IPO at $83", "summ": "Raising $81.3bn - a record listing.", "continent": "Americas", "kind": "ipo", "chip": "CONFIRMED - REUTERS"},
    9: {"kick": "SCIENCE - SPACE", "head": "Voyager 1 reaches one light-day", "summ": "First human-made object to do so.", "continent": "Americas", "kind": "voyager", "chip": "CONFIRMED - NASA JPL"},
    10: {"kick": "AMERICAS - HEALTH", "head": "US loses measles-free status after 26 years", "summ": "PAHO: endemic again; 5,412 cases in 2026.", "continent": "Americas", "kind": "measles", "chip": "CONFIRMED - PAHO"},
    11: {"kick": "AFRICA - HEALTH", "head": "Ebola passes 11,000 cases in DR Congo", "summ": "More than doubled in three months.", "continent": "Africa", "kind": "ebola", "chip": "CONFIRMED - WHO"},
    12: {"kick": "INDIA - WEATHER", "head": "Cyclone Akvan bears down on Odisha", "summ": "Severe storm; landfall expected ~20 Nov.", "continent": "Asia", "kind": "cyclone", "chip": "CONFIRMED - IMD"},
    13: {"kick": "PACIFIC - WEATHER", "head": "Cyclone Xavier hits Category 5", "summ": "Briefly Cat 5 over the Cook Islands.", "continent": "Oceania", "kind": "xavier", "chip": "CONFIRMED - FIJI MET"},
    14: {"kick": "GAZA - WAR", "head": "Israeli tanks cross Yellow Line at Nuseirat", "summ": "First such raid since the truce.", "continent": "Mideast", "kind": "gaza", "chip": "CONFIRMED - REUTERS"},
    15: {"kick": "US - POLITICS", "head": "Jeffries wins Democrats' Speaker nod", "summ": "251-11; full House vote set for 3 January.", "continent": "Americas", "kind": "vote", "chip": "CONFIRMED - AP"},
}

BRIEFS = {
    16: "Houthis fire five drones at two pumping stations on Saudi pipeline",
    17: "Gaza winter: WHO counts 950,000 displaced on flood-prone ground",
    18: "Louvre workers vote to extend strike over staffing and the jewel heist",
    19: "ASHA health workers' strike enters second day in Karnataka",
    20: "Maharashtra court staff call off strike after talks with judges",
    21: "Magnitude 6.0 quake off Peru's Ica region; tsunami ruled out",
    22: "Ghana's new $60m presidential jet sparks public outrage",
    23: "Nigeria's central bank and NNPC sign forex and energy deal",
    24: "Malaysia Q3 GDP beats forecasts at 5.5%; AI boom to drive 2027",
    25: "Fed's Waller calls for more aggressive inflation response",
    26: "UK inflation rises to 3.6%, highest in a year, on fuel prices",
    27: "Amnesty: RSF drone strikes in El Obeid killed 37 civilians",
    28: "Bangladesh garment unrest: ~535 factories hit, ~300 arrested",
    29: "GTA VI rolls out to rave reviews, Metacritic 99, ahead of launch",
    30: "Quake felt in Bucharest; EMSC 5.3, Romania's institute 5.7",
    31: "Magnitude 4.1 quake strikes southwest Kuwait; no damage",
    32: "Migrant boat capsizes off Senegal, at least one dead",
    33: "Hegseth makes surprise Caracas trip, signs defence partnership",
    34: "Brazil Senate approves Lula's $10bn fiscal package",
    35: "Sheinbaum says Mexico-US trade talks 'very far along'",
    36: "Ethiopia and Eritrea mass troops near Badme; war fears rise",
    37: "Tame Impala wins seven ARIAs, Album of the Year for Deadbeat",
    38: "Alcaraz beats Medvedev 6-2, 6-4 at ATP Finals, into semis",
    39: "ECDC warns superbug infections surged; Klebsiella up 72% since 2019",
    40: "Pew projects Islam will pass Christianity as largest religion by 2035",
    41: "Brent crude settles $91.95 a barrel, down $1.19 (-1.28%)",
    42: "Chelsea Women beat PSG 1-0, Buurman 87th-minute winner",
    43: "Japan exports hit record 11.8tn yen in Oct, +20.5%",
    44: "Japan Oct visitors hit record 3.91m despite China arrivals -47%",
    45: "Australia wages +1.1% in Sep quarter, fastest since Dec 2023",
    46: "EU Council authorises signing EU-Indonesia trade deal",
    47: "COP31 launches second Global Stocktake; 21 issues unresolved",
    48: "Ella Langley wins record six CMAs, incl. Entertainer of the Year",
    49: "National Book Awards: Assadi fiction, ElGendy nonfiction",
    50: "First Ivors Composer Awards: Pemberton Composer of the Year",
    51: "Fiji declares state of disaster over El Nino drought",
    52: "Ruto gives State of the Nation address, unveils tax relief",
    53: "Trump asks Supreme Court to block Venezuelan TPS restoration",
    54: "Qonto granted French/ECB banking licence",
    55: "Cassava seeks $1bn to buy Nvidia chips for African AI centres",
}

PINS = {
    1: (51.5, 26.5, 0, 0),
    2: (114.0, 22.5, 0, 0),
    3: (121.0, 14.6, -6, -12),
    4: (30.5, 50.4, 8, -2),
    5: (4.35, 50.85, -8, -6),
    6: (-74.0, 40.7, -4, -10),
    7: (-0.1, 51.5, -12, -4),
    8: (-122.4, 37.8, -8, -6),
    9: (-118.1, 34.1, 0, 8),
    10: (-98.0, 39.0, 0, 0),
    11: (23.0, -2.0, 0, 0),
    12: (86.0, 19.0, 6, 2),
    13: (-160.0, -15.0, 0, 0),
    14: (34.4, 31.45, -10, 8),
    15: (-77.0, 38.9, -14, -8),
    16: (46.7, 24.6, 0, 6),
    17: (34.3, 31.4, 6, 12),
    18: (2.35, 48.9, -12, -4),
    19: (77.6, 13.0, 8, 4),
    20: (72.8, 19.1, -8, -8),
    21: (-75.4, -15.4, 0, 4),
    22: (-0.2, 5.6, 0, 6),
    23: (7.5, 9.1, 8, -4),
    24: (101.7, 3.1, 2, 10),
    25: (-77.0, 38.9, 10, 10),
    26: (-0.1, 51.5, 10, 8),
    27: (30.2, 13.2, 0, 6),
    28: (90.4, 23.8, 8, -6),
    29: (-74.0, 40.7, 12, 8),
    30: (26.1, 44.4, -6, -10),
    31: (47.5, 29.3, 10, -6),
    32: (-17.4, 14.7, 0, -8),
    33: (-66.9, 10.5, 0, -6),
    34: (-47.9, -15.8, 0, 4),
    35: (-99.1, 19.4, 0, -8),
    36: (37.9, 14.7, -8, 4),
    37: (151.2, -33.9, 0, -6),
    38: (7.7, 45.1, 8, -12),
    39: (18.1, 59.3, -6, -8),
    40: (-77.0, 38.9, -2, 14),
    41: (-0.1, 51.5, -2, -12),
    42: (-0.1, 51.5, 10, 14),
    43: (139.7, 35.7, 0, -6),
    44: (139.7, 35.7, 12, -8),
    45: (149.1, -35.3, 0, -6),
    46: (4.35, 50.85, 12, 6),
    47: (30.7, 36.9, 4, -10),
    48: (-86.8, 36.2, 0, -6),
    49: (-74.0, 40.7, -12, 12),
    50: (-0.1, 51.5, -10, -12),
    51: (178.4, -17.7, 0, -6),
    52: (36.8, -1.3, 0, -6),
    53: (-77.0, 38.9, 14, -4),
    54: (2.35, 48.9, 12, 10),
    55: (31.0, -17.8, 0, 4),
}

PIN_CONTINENTS = {
    1: "Mideast", 2: "Asia", 3: "Asia", 4: "Europe", 5: "Europe", 6: "Americas", 7: "Europe", 8: "Americas", 9: "Americas", 10: "Americas", 11: "Africa", 12: "Asia", 13: "Oceania", 14: "Mideast", 15: "Americas", 16: "Mideast", 17: "Mideast", 18: "Europe", 19: "Asia", 20: "Asia", 21: "Americas", 22: "Africa", 23: "Africa", 24: "Asia", 25: "Americas", 26: "Europe", 27: "Africa", 28: "Asia", 29: "Americas", 30: "Europe", 31: "Mideast", 32: "Africa", 33: "Americas", 34: "Americas", 35: "Americas", 36: "Africa", 37: "Oceania", 38: "Europe", 39: "Europe", 40: "Americas",
    41: "Europe", 42: "Europe", 43: "Asia", 44: "Asia", 45: "Oceania", 46: "Europe", 47: "Mideast", 48: "Americas", 49: "Americas", 50: "Europe", 51: "Oceania", 52: "Africa", 53: "Americas", 54: "Europe", 55: "Africa"
}


def continent_of(n):
    if n in FEATURED:
        return FEATURED[n]["continent"]
    if n in GRID:
        return GRID[n]["continent"]
    return PIN_CONTINENTS[n]


def story_of(n):
    if n in FEATURED:
        return FEATURED[n]
    return GRID[n]


LAND_RECTS = [
    (-168, -140, 55, 71),
    (-140, -55, 50, 72),
    (-125, -67, 25, 50),
    (-117, -87, 15, 33),
    (-92, -77, 8, 17),
    (-55, -20, 60, 82),
    (-120, -60, 72, 80),
    (-80, -35, -5, 12),
    (-75, -35, -20, -5),
    (-73, -53, -40, -20),
    (-73, -65, -55, -40),
    (-10, 5, 36, 51),
    (5, 25, 36, 55),
    (5, 32, 55, 71),
    (-10, 2, 50, 59),
    (-24, -13, 63, 67),
    (20, 40, 44, 56),
    (26, 63, 25, 42),
    (34, 60, 12, 30),
    (-17, 35, 15, 37),
    (-17, 40, 5, 20),
    (8, 42, -12, 8),
    (12, 40, -35, -10),
    (43, 50, -26, -12),
    (32, 60, 55, 70),
    (60, 180, 50, 75),
    (45, 90, 35, 55),
    (73, 135, 20, 50),
    (68, 92, 8, 32),
    (95, 130, -10, 23),
    (129, 146, 31, 45),
    (95, 141, -10, 6),
    (113, 154, -39, -11),
    (166, 179, -47, -34),
]

DRAW = None


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_width):
    words = text.split()
    if not words:
        return []
    lines, cur = [], []
    for word in words:
        trial = " ".join(cur + [word])
        if not cur or DRAW.textlength(trial, font=fnt) <= max_width:
            cur.append(word)
        else:
            lines.append(" ".join(cur))
            cur = [word]
    if cur:
        lines.append(" ".join(cur))
    return lines


def block(x, y, w, text, fnt, line_height, max_y, fill=INK):
    lines = wrap(text, fnt, w)
    cy = y
    i = 0
    while i < len(lines) and cy + line_height <= max_y + 1e-6:
        DRAW.text((x, cy), lines[i], font=fnt, fill=fill)
        cy += line_height
        i += 1
    return " ".join(lines[i:])


def fit_block(x, y, w, text, path, sizes, max_y, lh_ratio, fill=INK):
    for size in sizes:
        fnt = font(path, size)
        lh = size * lh_ratio
        lines = wrap(text, fnt, w)
        if y + len(lines) * lh <= max_y + 1e-6:
            rem = block(x, y, w, text, fnt, lh, max_y, fill=fill)
            assert rem == "", "unexpected truncation: %r" % rem
            return size, len(lines)
    raise AssertionError("no candidate size fits: %r" % text[:60])


def chip(cx, cy, r, n, fill):
    DRAW.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    fnt = font(SANS_BOLD, r * 1.12)
    text = str(n)
    x0, y0, x1, y1 = DRAW.textbbox((0, 0), text, font=fnt)
    DRAW.text((cx - (x0 + x1) / 2.0, cy - (y0 + y1) / 2.0), text,
              font=fnt, fill=(255, 255, 255))


def tint(col, amount):
    return tuple(int(round(PAPER[i] + (col[i] - PAPER[i]) * amount)) for i in range(3))


def banner(x, y, w, h, kind, cont_col):
    DRAW.rectangle([x, y, x + w, y + h], fill=tint(ACCENT, 0.16))
    a, c = ACCENT, cont_col
    u = h / 84.0

    if kind == "missiles":
        sea = tint(a, 0.42)
        DRAW.rectangle([x, y + h * 0.72, x + w, y + h], fill=sea)
        pts = []
        steps = 9
        for i in range(steps + 1):
            px = x + w * i / steps
            py = y + h * (0.66 if i % 2 == 0 else 0.74)
            pts.append((px, py))
        pts += [(x + w, y + h), (x, y + h)]
        DRAW.polygon(pts, fill=tint(c, 0.30))
        for dx, col in ((0.26, a), (0.46, c)):
            sx = x + w * dx
            sy = y + h * 0.80
            ex = x + w * (dx + 0.20)
            ey = y + h * 0.16
            DRAW.line([sx, sy, ex, ey], fill=col, width=max(2, int(2.4 * u)))
            DRAW.polygon([(ex, ey), (ex - 3.4 * u, ey + 9 * u),
                          (ex + 3.4 * u, ey + 9 * u)], fill=col)
        bx, by = x + w * 0.86, y + h * 0.30
        r = 7.5 * u
        DRAW.ellipse([bx - r, by - r, bx + r, by + r], fill=tint(c, 0.85))
        DRAW.ellipse([bx - r * 0.45, by - r * 0.45, bx + r * 0.45, by + r * 0.45],
                     fill=CARD)

    elif kind in ("skyline", "harbour"):
        base = y + h * 0.86
        heights = [0.30, 0.46, 0.24, 0.52, 0.36, 0.60, 0.28, 0.44, 0.34, 0.50]
        bw = w / (len(heights) + 2.0)
        for i, hh in enumerate(heights):
            bx = x + bw * (i + 1)
            DRAW.rectangle([bx, base - h * hh, bx + bw * 0.82, base], fill=a)
        if kind == "harbour":
            DRAW.rectangle([x, base, x + w, y + h], fill=tint(c, 0.55))
            hx = x + w * 0.62
            DRAW.polygon([(hx, base + h * 0.06), (hx + w * 0.18, base + h * 0.06),
                          (hx + w * 0.15, base + h * 0.12),
                          (hx + w * 0.03, base + h * 0.12)], fill=CARD)
            DRAW.line([hx + w * 0.09, base + h * 0.06, hx + w * 0.09, y + h * 0.12],
                      fill=CARD, width=max(1, int(1.6 * u)))
        for fx in (x + w * 0.24, x + w * 0.46):
            DRAW.line([fx, base, fx, y + h * 0.12], fill=INK, width=max(1, int(1.8 * u)))
            DRAW.polygon([(fx, y + h * 0.12), (fx + 13 * u, y + h * 0.19),
                          (fx, y + h * 0.26)], fill=c)

    elif kind == "flags":
        for i, fx in enumerate((x + w * 0.30, x + w * 0.62)):
            DRAW.line([fx, y + h * 0.88, fx, y + h * 0.12], fill=INK,
                      width=max(1, int(2.0 * u)))
            col = a if i == 0 else c
            DRAW.rectangle([fx, y + h * 0.14, fx + w * 0.22, y + h * 0.40], fill=col)
            DRAW.rectangle([fx, y + h * 0.14, fx + w * 0.22, y + h * 0.22],
                           fill=tint(col, 0.55))
        DRAW.rectangle([x, y + h * 0.88, x + w, y + h], fill=tint(a, 0.35))

    elif kind == "coin":
        cx, cy = x + w * 0.5, y + h * 0.52
        r = h * 0.30
        DRAW.ellipse([cx - r, cy - r, cx + r, cy + r], fill=a)
        DRAW.ellipse([cx - r * 0.66, cy - r * 0.66, cx + r * 0.66, cy + r * 0.66],
                     outline=CARD, width=max(1, int(1.8 * u)))
        DRAW.line([cx - r * 0.28, cy + r * 0.30, cx + r * 0.28, cy + r * 0.30],
                  fill=CARD, width=max(1, int(2.0 * u)))
        DRAW.line([cx, cy - r * 0.30, cx, cy + r * 0.30], fill=CARD,
                  width=max(1, int(2.0 * u)))

    elif kind == "rocket":
        cx = x + w * 0.5
        top, bot = y + h * 0.12, y + h * 0.74
        DRAW.polygon([(cx, top), (cx - w * 0.055, bot), (cx + w * 0.055, bot)], fill=a)
        DRAW.polygon([(cx - w * 0.055, bot - h * 0.14), (cx - w * 0.12, bot),
                      (cx - w * 0.055, bot)], fill=c)
        DRAW.polygon([(cx + w * 0.055, bot - h * 0.14), (cx + w * 0.12, bot),
                      (cx + w * 0.055, bot)], fill=c)
        DRAW.ellipse([cx - w * 0.016, top + h * 0.10, cx + w * 0.016, top + h * 0.19],
                     fill=CARD)
        DRAW.polygon([(cx - w * 0.035, bot), (cx + w * 0.035, bot),
                      (cx, bot + h * 0.16)], fill=tint(c, 0.75))

    elif kind == "sun":
        cx, cy = x + w * 0.5, y + h * 0.50
        r = h * 0.20
        for k in range(8):
            ang = k * np.pi / 4.0
            DRAW.line([cx + np.cos(ang) * r * 1.45, cy + np.sin(ang) * r * 1.45,
                       cx + np.cos(ang) * r * 2.05, cy + np.sin(ang) * r * 2.05],
                      fill=c, width=max(1, int(1.8 * u)))
        DRAW.ellipse([cx - r, cy - r, cx + r, cy + r], fill=a)
        DRAW.ellipse([cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5],
                     fill=tint(a, 0.45))

    elif kind == "dome":
        base = y + h * 0.82
        cx = x + w * 0.5
        r = h * 0.30
        DRAW.pieslice([cx - r, base - r, cx + r, base + r], 180, 360, fill=a)
        DRAW.rectangle([cx - r * 1.45, base, cx + r * 1.45, base + h * 0.07], fill=c)
        for k in (-1, 0, 1):
            px = cx + k * r * 0.9
            DRAW.rectangle([px - 1.6 * u, base - r * 0.42, px + 1.6 * u, base], fill=c)
        DRAW.line([cx, base - r * 1.12, cx, base - r * 1.42], fill=c,
                  width=max(1, int(1.6 * u)))

    elif kind == "cyclone":
        cx, cy = x + w * 0.5, y + h * 0.50
        for k, rr in enumerate((h * 0.30, h * 0.20, h * 0.10)):
            col = a if k % 2 == 0 else c
            DRAW.arc([cx - rr, cy - rr, cx + rr, cy + rr], 20 + k * 40, 300 + k * 40,
                     fill=col, width=max(1, int(2.2 * u)))
        DRAW.ellipse([cx - 2.6 * u, cy - 2.6 * u, cx + 2.6 * u, cy + 2.6 * u], fill=c)

    elif kind == "arrows":
        DRAW.rectangle([x, y + h * 0.30, x + w, y + h * 0.36], fill=tint(c, 0.55))
        for i in range(3):
            ax = x + w * (0.24 + i * 0.20)
            DRAW.polygon([(ax, y + h * 0.62), (ax + w * 0.10, y + h * 0.44),
                          (ax + w * 0.10, y + h * 0.54), (ax + w * 0.16, y + h * 0.54),
                          (ax + w * 0.16, y + h * 0.70), (ax + w * 0.10, y + h * 0.70),
                          (ax + w * 0.10, y + h * 0.80)], fill=a if i % 2 == 0 else c)

    else:
        DRAW.rectangle([x, y + h * 0.42, x + w, y + h * 0.58], fill=a)


def main():
    global DRAW
    img = Image.new("RGB", (1024, 1024), PAPER)
    DRAW = ImageDraw.Draw(img)
    drawn = set()

    f_sansb = lambda s: font(SANS_BOLD, s)
    f_sans = lambda s: font(SANS, s)

    # ---- Masthead -------------------------------------------------------
    DRAW.text((24, 3), "THE WORLD'S NEWS IN ONE PICTURE", font=f_sansb(12.5), fill=ACCENT)
    right = "55 STORIES - ONE PAGE"
    DRAW.text((1000, 3), right, font=f_sansb(12.5), fill=INK, anchor="ra")

    title_size = 54
    while title_size >= 40:
        f = font(SERIF_BOLD, title_size)
        if DRAW.textlength("THE DAILY ATLAS", font=f) <= 900:
            break
        title_size -= 2
    DRAW.text((512, 13), "THE DAILY ATLAS", font=font(SERIF_BOLD, title_size),
              fill=INK, anchor="ma")

    r1 = 13 + title_size + 6
    DRAW.line([24, r1, 1000, r1], fill=ACCENT, width=3)
    DRAW.line([24, r1 + 5, 1000, r1 + 5], fill=ACCENT, width=1)

    dy = r1 + 9
    DRAW.text((512, dy), "Wednesday 18 November 2026",
              font=font(SERIF_BOLD, 21), fill=ACCENT, anchor="ma")

    sy = dy + 27
    DRAW.text((24, sy), "EVERY STORY REPORTED ON THE DAY", font=f_sans(10.5), fill=GREY)
    DRAW.text((1000, sy), "WEDNESDAY EDITION - NO. 18",
              font=f_sansb(11), fill=INK, anchor="ra")

    # ---- UTC timeline strip (NEW device 1) ------------------------------
    tl_y = sy + 13
    tl_w = 1000 - 24
    tl_h = 46
    DRAW.rectangle([24, tl_y, 1000, tl_y + tl_h], fill=CARD, outline=BORDER, width=1)

    # Label box over left 62px
    DRAW.rectangle([24, tl_y, 24 + 62, tl_y + tl_h], fill=ACCENT)
    DRAW.text((55, tl_y + 13), "THE DAY", font=f_sansb(10), fill=(255, 255, 255), anchor="ma")
    DRAW.text((55, tl_y + 26), "IN UTC", font=f_sansb(10), fill=(255, 255, 255), anchor="ma")

    timeline_data = [
        ("Overnight", "Russia fires 141 drones at Ukraine"),
        ("Before dawn", "Iran strikes Kuwait & Bahrain bases"),
        ("Asia daytime", "Xi-Putin summit; Quad meets in Manila"),
        ("10:16 UTC", "Voyager 1 reaches one light-day"),
        ("~19:00 UTC", "Fed minutes point to more hikes"),
        ("Evening", "Dow closes -561 on rate fears"),
    ]
    rem_w = tl_w - 62
    seg_w = rem_w / 6.0
    for k, (lbl, ev) in enumerate(timeline_data):
        seg_x = 24 + 62 + k * seg_w
        if k > 0:
            DRAW.line([seg_x, tl_y + 5, seg_x, tl_y + 41], fill=BORDER, width=1)
        DRAW.text((seg_x + 8, tl_y + 4), lbl, font=f_sansb(10), fill=ACCENT)
        # wrapped event text
        ev_lines = wrap(ev, f_sans(8.5), seg_w - 14)
        ev_y = tl_y + 19
        for line in ev_lines:
            assert ev_y + 10 <= tl_y + tl_h + 1e-6, "timeline segment text passes tl_y+46"
            DRAW.text((seg_x + 8, ev_y), line, font=f_sans(8.5), fill=INK)
            ev_y += 10

    # ---- Featured row ---------------------------------------------------
    fy = tl_y + tl_h + 8  # tl_y + 46 + 8 = tl_y + 54
    for i, sid in enumerate([3, 2, 1]):
        x = 24 + i * 329
        cw, ch = 317, 162
        DRAW.rectangle([x, fy, x + cw, fy + ch], fill=CARD, outline=BORDER, width=1)
        s = story_of(sid)
        drawn.add(sid)
        cont = CONTINENTS[s["continent"]]

        # Banner across top 74px, but tag bar from fy+48 to fy+74 (height 26)
        banner(x, fy, cw, 48, s["kind"], cont)

        tag_y = fy + 48
        tag_col = cont if s["continent"] != "Europe" else ACCENT # or use tag col logic
        # If tag colour IS the accent, use ink for the strip
        # Let's check tag colors from prompt:
        # 1: STRIKES ON BOTH SIDES (accent) -> strip INK
        # 2: THREE-WAY ON THURSDAY (navy) -> strip ACCENT
        # 3: MANILA FIRST (near-black 16,22,34) -> strip ACCENT
        tag_fill = ACCENT if sid == 1 else (NAVY if sid == 2 else (16, 22, 34))
        strip_col = INK if tag_fill == ACCENT else ACCENT

        DRAW.rectangle([x, tag_y, x + cw, fy + 74], fill=tag_fill)
        DRAW.rectangle([x, tag_y, x + 5, fy + 74], fill=strip_col)
        DRAW.text((x + 14, tag_y + 13), s["tag"], font=f_sansb(12), fill=(255, 255, 255),
                  anchor="lm")

        chip(x + 18, fy + 86, 9.5, sid, ACCENT)
        DRAW.text((x + 34, fy + 86), s["kick"], font=f_sansb(10.5), fill=ACCENT,
                  anchor="lm")

        # SOURCE CHIP (NEW device 3) on the same row, right side
        chip_text = s["chip"]
        cfnt = f_sansb(8)
        pw = DRAW.textlength(chip_text, font=cfnt) + 14
        pill_x1 = x + 309 - pw
        pill_x2 = x + 309
        pill_y1 = fy + 78
        pill_y2 = fy + 94
        DRAW.rounded_rectangle([pill_x1, pill_y1, pill_x2, pill_y2], radius=7, fill=(90, 88, 80))
        DRAW.text((pill_x1 + pw / 2.0, fy + 86), chip_text, font=cfnt, fill=(255, 255, 255), anchor="mm")

        rem = block(x + 10, fy + 96, 297, s["head"], font(SERIF_BOLD, 17), 18, fy + 133)
        assert rem == "", "featured %d headline truncated: %r" % (sid, rem)

        head_lines = wrap(s["head"], font(SERIF_BOLD, 17), 297)
        summ_y = fy + 96 + len(head_lines) * 18 + 2
        size, nlines = fit_block(x + 10, summ_y, 297, s["summ"], SERIF,
                                 [9.5, 9, 8.5, 8], fy + 160, 1.21)
        print("featured %2d: summary %spt/%d lines" % (sid, size, nlines))

    # ---- Grid -----------------------------------------------------------
    grid_rule_y = fy + 162 + 8
    DRAW.line([24, grid_rule_y, 1000, grid_rule_y], fill=INK, width=1)
    grid_top = grid_rule_y + 8

    for idx, sid in enumerate(range(4, 16)):
        col, row = idx % 4, idx // 4
        x = 24 + col * 246
        y0 = grid_top + row * 92
        cw, ch = 238, 84
        DRAW.rectangle([x, y0, x + cw, y0 + ch], fill=CARD, outline=BORDER, width=1)
        s = story_of(sid)
        drawn.add(sid)
        cont = CONTINENTS[s["continent"]]

        banner(x, y0, cw, 34, s["kind"], cont)

        chip(x + 13, y0 + 41, 6, sid, ACCENT)
        DRAW.text((x + 24, y0 + 41), s["kick"], font=f_sansb(8), fill=ACCENT,
                  anchor="lm")

        # SOURCE CHIP (NEW device 3) for grid
        g_chip = s["chip"]
        g_col = DATE_CHECK_RED if g_chip.startswith("CLAIM") else GREY
        DRAW.text((x + 230, y0 + 41), g_chip, font=f_sansb(7), fill=g_col, anchor="rm")

        rem = block(x + 8, y0 + 47, 222, s["head"], font(SERIF_BOLD, 12), 12.5, y0 + 72)
        assert rem == "", "grid %d headline truncated: %r" % (sid, rem)

        head_lines = wrap(s["head"], font(SERIF_BOLD, 12), 222)
        summ_y = y0 + 47 + len(head_lines) * 12.5 + 1
        size, nlines = fit_block(x + 8, summ_y, 222, s["summ"], SERIF,
                                 [8.5, 8, 7.5, 7, 6.5], y0 + 83, 1.12)
        print("grid     %2d: summary %spt/%d lines" % (sid, size, nlines))

    # ---- Bottom band ----------------------------------------------------
    by = grid_top + 3 * 84 + 2 * 8 + 12
    DRAW.line([24, by, 1000, by], fill=INK, width=1)
    hy = by + 8

    DRAW.text((24, hy), "ALSO ON WEDNESDAY 18 NOVEMBER", font=f_sansb(12), fill=INK)
    DRAW.text((700, hy), "WHERE IT HAPPENED", font=f_sansb(12), fill=ACCENT)

    # Legend centered on x=512 in header row
    # Let's compute legend width or position
    # Legend items: 6 continents. Dot 7px + text in Sans 8.5 ink.
    # Let's measure legend total width or place them around 512.
    # Each item: 9px rect + gap 4px + text width + gap 16px.
    # Let's calculate total width:
    leg_items = list(CONTINENTS.items())
    leg_font = f_sans(8.5)
    item_widths = []
    for name, col in leg_items:
        tw = DRAW.textlength(name, font=leg_font)
        item_widths.append(9 + 4 + tw)
    total_leg_w = sum(item_widths) + 16 * (len(leg_items) - 1)
    leg_start_x = 512 - total_leg_w / 2.0
    lx = leg_start_x
    for (name, col), iw in zip(leg_items, item_widths):
        DRAW.rectangle([lx, hy + 2, lx + 9, hy + 11], fill=col)
        DRAW.text((lx + 13, hy + 6.5), name, font=leg_font, fill=INK, anchor="lm")
        lx += iw + 16

    map_top = hy + 22
    # Map box on right: x from 700 to 1000 (width 300)
    mx = 700
    mw = 300

    # Briefs on the left: x = 24, 4 columns each 150 wide? Wait, prompt says:
    # "the 40 briefs (stories 16-55) in 4 columns at x = 24, 196, 368, 540, each column 150 wide."
    # Let's check x coordinates: 24, 196, 368, 540. Width of each column: 150.
    # Right edge of column 3 (at x=540): 540 + 150 = 690. Map starts at 700! Perfect!
    col_x_list = [24, 196, 368, 540]
    col_w = 150

    briefs_bottom_target = 930
    ids = list(range(16, 56))
    # 40 briefs across 4 columns -> 10 briefs per column
    col_ids = [ids[i*10:(i+1)*10] for i in range(4)]

    # Auto-fit briefs font size
    chosen = None
    for size in [9.5, 9.25, 9.0, 8.75, 8.5, 8.25, 8.0]:
        fb, fr = font(SANS_BOLD, size), font(SANS, size)
        lh = size + 2
        ok = True
        max_col_h = 0
        for c_ids in col_ids:
            y = map_top
            for sid in c_ids:
                lines = wrap_brief(sid, fb, fr, col_w)
                y += len(lines) * lh + 2.0 + 2.0 # gap + separator
            if y - map_top > max_col_h:
                max_col_h = y - map_top
        # tallest column must end at or above y=930 (or let's check band_h)
        if map_top + max_col_h <= 930 + 1e-6:
            chosen = (size, lh, max_col_h)
            break
    if not chosen:
        chosen = (8.0, 10.0, 0) # fallback
    size, lh, band_h = chosen
    # If band_h wasn't exact in loop, let's recalculate accurately:
    fb, fr = font(SANS_BOLD, size), font(SANS, size)
    col_heights = []
    for c_ids in col_ids:
        y = map_top
        for sid in c_ids:
            lines = wrap_brief(sid, fb, fr, col_w, DRAW)
            y += len(lines) * lh + 4.0
        col_heights.append(y - map_top)
    band_h = max(col_heights)

    # Draw briefs
    for c, c_ids in enumerate(col_ids):
        x = col_x_list[c]
        y = map_top
        for sid in c_ids:
            y = draw_brief(x, y, col_w, sid, fb, fr, lh, DRAW)
            drawn.add(sid)

    # Draw map on the right (x from 700 to 1000, height = band_h)
    mh = band_h
    my = map_top

    mask = np.zeros((36, 72), dtype=bool)
    for lon0, lon1, lat0, lat1 in LAND_RECTS:
        c0 = max(0, int(np.floor((lon0 + 180.0) / 5.0)))
        c1 = min(71, int(np.ceil((lon1 + 180.0) / 5.0)) - 1)
        r0 = max(0, int(np.floor((90.0 - lat1) / 5.0)))
        r1 = min(35, int(np.ceil((90.0 - lat0) / 5.0)) - 1)
        mask[r0:r1 + 1, c0:c1 + 1] = True

    cell_w = mw / 72.0
    cell_h = mh / 36.0
    land_col = tint(NAVY, 0.42)
    for r in range(36):
        for c in range(72):
            if mask[r, c]:
                rx = mx + c * cell_w
                ry = my + r * cell_h
                DRAW.rectangle([rx, ry, rx + cell_w - 0.6, ry + cell_h - 0.6], fill=land_col)

    # Draw pins on map
    pr = 7.0
    placed = []
    for sid in sorted(PINS):
        lon, lat, dx, dy = PINS[sid]
        ox = mx + (lon + 180.0) / 360.0 * mw + dx
        oy = my + (90.0 - lat) / 180.0 * mh + dy
        ox = min(max(ox, mx + pr + 1), mx + mw - pr - 1)
        oy = min(max(oy, my + pr + 1), my + mh - pr - 1)
        placed.append((ox, oy))
        cont_col = CONTINENTS[continent_of(sid)]
        chip(ox, oy, pr, sid, cont_col)

    # ---- DATE CHECK box (NEW device 2) ----------------------------------
    dc_y = map_top + band_h + 8
    dc_h = 36
    DRAW.rectangle([24, dc_y, 1000, dc_y + dc_h], fill=CARD, outline=DATE_CHECK_RED, width=2)

    # Label box over left 62px
    DRAW.rectangle([24, dc_y, 24 + 62, dc_y + dc_h], fill=DATE_CHECK_RED)
    DRAW.text((55, dc_y + 6), "DATE", font=f_sansb(10.5), fill=(255, 255, 255), anchor="ma")
    DRAW.text((55, dc_y + 19), "CHECK", font=f_sansb(10.5), fill=(255, 255, 255), anchor="ma")

    dc_text = ("Left out on purpose - they broke on other days: the An-12 crash "
               "in Siberia, 19 killed (Tue 17 Nov) - Peltola's Alaska Senate call "
               "(Tue 17 Nov) - the Knesset speaker vote, Kahana 66-52 (Tue 17 "
               "Nov) - the Crimea Bridge collapse (overnight 16-17 Nov) - "
               "Nvidia's results (17 Nov). Not yet: the ICJ Rohingya judgment is "
               "due Thu 19 Nov.")
    dc_lines = wrap(dc_text, f_sans(9), 976 - 80)
    assert len(dc_lines) <= 2, "DATE CHECK text exceeds 2 lines: %d lines" % len(dc_lines)
    dc_ty = dc_y + 5
    for line in dc_lines:
        DRAW.text((96, dc_ty), line, font=f_sans(9), fill=INK)
        dc_ty += 12

    # ---- Footer ---------------------------------------------------------
    fy2 = dc_y + dc_h + 6  # dc_y + 36 + 6 = dc_y + 42
    DRAW.line([24, fy2, 1000, fy2], fill=INK, width=1)

    f1 = "CLAIM = one side's account, not independently confirmed."
    DRAW.text((512, fy2 + 5), f1, font=font(SERIF_ITALIC, 9.5), fill=INK, anchor="ma")

    f2 = ("Every story happened or was first reported on Wednesday 18 November 2026 - Disputed claims are attributed - Sources: Reuters - AP - AFP - BBC - Al Jazeera - CNN - WHO - UN News")
    DRAW.text((512, fy2 + 21), f2, font=f_sans(8.5), fill=GREY, anchor="ma")

    assert len(drawn) == 55 and drawn == set(range(1, 56)), \
        "expected all 55 story numbers, got %d" % len(drawn)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    nbytes = os.path.getsize(out)
    assert nbytes <= 1048576, "too large: %d bytes" % nbytes
    print("wrote %s: %d bytes, %dx%d" % (out, nbytes, img.width, img.height))


def wrap_brief(sid, fb, fr, col_w, draw_obj=None):
    global DRAW
    d = draw_obj if draw_obj is not None else DRAW
    num = "%d. " % sid
    nw = d.textlength(num, font=fb)
    lines, cur = [], ""
    avail = col_w - nw
    for word in BRIEFS[sid].split():
        trial = (cur + " " + word).strip()
        if not cur or d.textlength(trial, font=fr) <= avail:
            cur = trial
        else:
            lines.append(cur)
            cur = word
            avail = col_w
    if cur:
        lines.append(cur)
    return lines


def draw_brief(x, y, col_w, sid, fb, fr, lh, draw_obj):
    num = "%d. " % sid
    nw = draw_obj.textlength(num, font=fb)
    lines = wrap_brief(sid, fb, fr, col_w, draw_obj)
    draw_obj.text((x, y), num, font=fb, fill=ACCENT)
    draw_obj.text((x + nw, y), lines[0], font=fr, fill=INK)
    for i, line in enumerate(lines[1:], start=1):
        draw_obj.text((x, y + i * lh), line, font=fr, fill=INK)
    total_h = len(lines) * lh
    # Draw faint dotted separator under brief
    sep_y = y + total_h + 1.0
    for dx in range(int(x), int(x + col_w), 3):
        draw_obj.point((dx, sep_y), fill=BORDER)
    return y + total_h + 4.0


if __name__ == "__main__":
    main()
