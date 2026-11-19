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
        "summ": ("US struck an IRGC missile site on Qeshm Island on Tuesday; "
                 "Iran answered early Wednesday with strikes on Kuwait's Ali "
                 "Al Salem Air Base and Bahrain, which says it intercepted "
                 "several attacks before dawn."),
        "continent": "Mideast",
        "kind": "missiles",
    },
    2: {
        "kick": "ASIA - APEC SUMMIT",
        "head": "Xi and Putin meet in Shenzhen",
        "summ": ("Xi Jinping and Vladimir Putin met on the APEC sidelines, "
                 "denouncing protectionism and Western sanctions; a trilateral "
                 "with Trump is set for Thursday, with no published agenda."),
        "continent": "Asia",
        "kind": "flags",
    },
    3: {
        "kick": "ASIA - QUAD IN MANILA",
        "head": "Quad meets; Trump lands in Manila",
        "summ": ("First leader-level Quad meeting in over two years; Trump met "
                 "Marcos Jr., announced a Philippines trade deal, then flies on "
                 "to China."),
        "continent": "Asia",
        "kind": "harbour",
    },
}

GRID = {
    4: {"kick": "UKRAINE - WAR", "head": "Russia fires 141 drones; 126 downed",
        "summ": "Overnight barrage across Ukraine; hits recorded at 7 sites. (ISW)",
        "continent": "Europe", "kind": "missiles"},
    5: {"kick": "EUROPE - UKRAINE AID", "head": "EU proposes a 45bn-euro Ukraine loan",
        "summ": ("25bn military and 20bn budget support for 2027, presented "
                 "Wednesday. (Use the euro sign if the font has it; the amounts "
                 "are 25bn + 20bn = 45bn euros.)"),
        "continent": "Europe", "kind": "flags"},
    6: {"kick": "UNITED STATES - MARKETS", "head": "Fed minutes back more hikes; Dow -561",
        "summ": ("Minutes put a bigger December hike in play; S and P 500 -0.23 "
                 "percent, Nasdaq +0.42 percent."),
        "continent": "Americas", "kind": "coin"},
    7: {"kick": "MARKETS - GOLD", "head": "Gold sinks to 14-month low",
        "summ": "Closed $3,725.18 an ounce, down 3.22 percent, on Wednesday.",
        "continent": "Americas", "kind": "coin"},
    8: {"kick": "TECH - IPO", "head": "Anthropic prices IPO at $83",
        "summ": "Raising $81.3bn - the largest listing on record, topping SpaceX's $75bn.",
        "continent": "Americas", "kind": "rocket"},
    9: {"kick": "SCIENCE - SPACE", "head": "Voyager 1 reaches one light-day",
        "summ": ("First human-made object to reach one light-day from Earth "
                 "(5:16:07 ET, about 16bn miles). NASA JPL."),
        "continent": "Americas", "kind": "sun"},
    10: {"kick": "AMERICAS - HEALTH", "head": "US loses measles-free status after 26 years",
         "summ": ("PAHO: measles endemic again; 5,412 cases in 2026, 10 deaths, "
                  "highest since 1991."),
         "continent": "Americas", "kind": "dome"},
    11: {"kick": "AFRICA - HEALTH", "head": "Ebola passes 11,000 cases in DR Congo",
         "summ": ("More than doubled in three months, second-largest on record; "
                  "nearly 3 in 4 infected under-5s die. WHO."),
         "continent": "Africa", "kind": "dome"},
    12: {"kick": "INDIA - WEATHER", "head": "Cyclone Akvan bears down on Odisha",
         "summ": ("Severe cyclonic storm about 570 km east of Chennai; landfall "
                  "expected near Andhra Pradesh around 20 Nov. IMD."),
         "continent": "Asia", "kind": "cyclone"},
    13: {"kick": "PACIFIC - WEATHER", "head": "Cyclone Xavier hits Category 5",
         "summ": ("Briefly Cat 5 (110 kt) over the northern Cook Islands; wharves "
                  "damaged on Manihiki, no casualties."),
         "continent": "Oceania", "kind": "cyclone"},
    14: {"kick": "GAZA - WAR", "head": "Israeli tanks cross Yellow Line at Nuseirat",
         "summ": "First such raid since the truce; three Palestinians killed, medics say.",
         "continent": "Mideast", "kind": "arrows"},
    15: {"kick": "UNITED STATES - POLITICS", "head": "Jeffries wins Democrats' Speaker nod",
         "summ": "Won the caucus vote 251-11; full House vote set for 3 January.",
         "continent": "Americas", "kind": "dome"},
}

BRIEFS = {
    16: "Houthis fire five drones at two pumping stations on Saudi East-West pipeline, Riyadh area.",
    17: "Gaza winter: WHO - 950,000 displaced Palestinians in flood-prone ground in Gaza's fourth winter.",
    18: "Louvre workers vote to extend strike over understaffing and the October crown-jewels heist.",
    19: "ASHA health workers' strike enters second day in Karnataka; demand 15,000 rupees/month honorarium.",
    20: "Maharashtra district court employees call off strike after talks with four Bombay High Court judges.",
    21: "Magnitude 6.0 quake off Peru's Ica region; no casualties, tsunami ruled out.",
    22: "Ghana's new $60m presidential jet sparks public outrage amid austerity.",
    23: "Nigeria's central bank and NNPC sign forex and energy funding deal.",
    24: "Malaysia Q3 GDP beats forecasts at 5.5 percent; AI boom to drive 2027 growth.",
    25: "Fed's Waller calls for more aggressive inflation response - half-point hike in play for Dec.",
    26: "UK inflation rises to 3.6 percent, highest in a year, on record fuel prices.",
    27: "Amnesty: RSF drone strikes in El Obeid killed 37 civilians, June-August.",
    28: "Bangladesh garment unrest: about 535 factories hit, about 130 shut, about 300 arrested.",
    29: "GTA VI rolls out to rave reviews, Metacritic 99, ahead of its 19 Nov launch.",
    30: "Quake felt in Bucharest; EMSC 5.3, Romania's institute 5.7.",
    31: "Magnitude 4.1 quake strikes southwest Kuwait; no damage reported.",
    32: "Migrant boat capsizes off Senegal, at least one dead; search ongoing.",
    33: "Hegseth makes surprise Caracas trip, signs US-Venezuela defence partnership.",
    34: "Brazil Senate approves Lula's $10bn fiscal package; heads to lower house.",
    35: "Sheinbaum says Mexico-US trade talks \"very far along\" after meeting Trump.",
    36: "Monitors say Ethiopia and Eritrea massed troops near Badme; war fears rise.",
    37: "Tame Impala wins seven ARIAs, including Album of the Year for Deadbeat.",
    38: "Alcaraz beats Medvedev 6-2, 6-4 at ATP Finals, reaching the semi-finals.",
    39: "ECDC warns superbug infections surged; Klebsiella cases up 72 percent since 2019.",
    40: "Pew projects Islam will pass Christianity as the world's largest religion by 2035.",
    41: "Brent crude settles $91.95 a barrel, down $1.19 (-1.28 percent) on surplus fears.",
    42: "Chelsea Women beat PSG 1-0, Buurman 87th-minute winner (UEFA UWCL, Matchday 5).",
    43: "Japan exports hit record 11.8tn yen in Oct, +20.5 percent, 14th straight monthly rise (Reuters).",
    44: "Japan Oct visitors hit record 3.91m despite China arrivals falling 47 percent (JNTO).",
    45: "Australia wages +1.1 percent in Sep quarter, fastest since Dec 2023; real pay still falls (ABS).",
    46: "EU Council authorises signing EU-Indonesia CEPA and investment deal (Consilium 18/11).",
    47: "COP31 launches second Global Stocktake; 21 issues still unresolved on Wed (Antalya).",
    48: "Ella Langley wins record six CMAs in one night, incl. Entertainer of the Year (Nashville).",
    49: "National Book Awards: Assadi fiction, ElGendy nonfiction; Rushdie lifetime medal (NYC).",
    50: "First Ivors Composer Awards: Pemberton Composer of the Year, Einaudi Fellow (London).",
    51: "Fiji declares national state of disaster over El Nino drought, FJ$20m allocated (PM Rabuka).",
    52: "Ruto gives 4th State of the Nation address, unveils PAYE relief, KSh340bn fund (Nairobi).",
    53: "Trump asks Supreme Court Wed to block Venezuelan TPS restoration for 600,000.",
    54: "Qonto granted French/ECB banking licence, serves 750,000+ European SMEs.",
    55: "Cassava seeks $1bn to buy Nvidia chips for AI data centres across Africa (TechCabal).",
}

PINS = {
    1: (52, 27), 2: (114, 22), 3: (121, 15), 4: (32, 49), 5: (5, 51),
    6: (-74, 41), 8: (-122, 38), 10: (-84, 34), 11: (23, -3), 12: (86, 20),
    13: (-160, -21), 14: (34, 31), 16: (47, 25), 18: (2, 49), 19: (77, 15),
    21: (-77, -12), 22: (-2, 8), 23: (8, 10), 24: (102, 4), 26: (0, 52),
    27: (30, 13), 28: (90, 24), 30: (26, 44), 31: (48, 29), 32: (-17, 15),
    33: (-67, 11), 34: (-48, -16), 36: (39, 15), 37: (151, -34), 39: (18, 59),
    43: (140, 36), 47: (31, 37), 48: (-87, 36), 51: (178, -18), 52: (37, -1),
    55: (3, 6),
}

BRIEF_CONTINENT = {
    16: "Mideast", 17: "Mideast", 18: "Europe", 19: "Asia", 20: "Asia",
    21: "Americas", 22: "Africa", 23: "Africa", 24: "Asia", 25: "Americas",
    26: "Europe", 27: "Africa", 28: "Asia", 29: "Americas", 30: "Europe",
    31: "Mideast", 32: "Africa", 33: "Americas", 34: "Americas", 35: "Americas",
    36: "Africa", 37: "Oceania", 38: "Europe", 39: "Europe", 40: "Asia",
    41: "Mideast", 42: "Europe", 43: "Asia", 44: "Asia", 45: "Oceania",
    46: "Europe", 47: "Asia", 48: "Americas", 49: "Americas", 50: "Europe",
    51: "Oceania", 52: "Africa", 53: "Americas", 54: "Europe", 55: "Africa",
}


def continent_of(n):
    if n in FEATURED:
        return FEATURED[n]["continent"]
    if n in GRID:
        return GRID[n]["continent"]
    return BRIEF_CONTINENT[n]


def story_of(n):
    if n in FEATURED:
        return FEATURED[n]
    return GRID[n]


# --------------------------------------------------------------------------
# Coarse world landmass, as (lon0, lon1, lat0, lat1) rectangles rasterised
# onto the 72 x 36 (5-degree) map grid. Solid, recognisable continents:
# Americas left, Europe/Africa centre, Asia right, Australia lower right.
# --------------------------------------------------------------------------
LAND_RECTS = [
    # North America
    (-168, -140, 55, 71),   # Alaska
    (-140, -55, 50, 72),    # Canada
    (-125, -67, 25, 50),    # United States
    (-117, -87, 15, 33),    # Mexico
    (-92, -77, 8, 17),      # Central America
    (-55, -20, 60, 82),     # Greenland
    (-120, -60, 72, 80),    # Arctic islands
    # South America
    (-80, -35, -5, 12),
    (-75, -35, -20, -5),
    (-73, -53, -40, -20),
    (-73, -65, -55, -40),
    # Europe
    (-10, 5, 36, 51),       # Iberia and France
    (5, 25, 36, 55),        # central Europe
    (5, 32, 55, 71),        # Scandinavia
    (-10, 2, 50, 59),       # British Isles
    (-24, -13, 63, 67),     # Iceland
    (20, 40, 44, 56),       # eastern Europe
    # Mideast
    (26, 63, 25, 42),       # Turkey through Iran
    (34, 60, 12, 30),       # Arabia
    # Africa
    (-17, 35, 15, 37),
    (-17, 40, 5, 20),
    (8, 42, -12, 8),
    (12, 40, -35, -10),
    (43, 50, -26, -12),     # Madagascar
    # Asia
    (32, 60, 55, 70),
    (60, 180, 50, 75),      # Siberia
    (45, 90, 35, 55),       # Central Asia
    (73, 135, 20, 50),      # China
    (68, 92, 8, 32),        # India
    (95, 130, -10, 23),     # Southeast Asia
    (129, 146, 31, 45),     # Japan
    (95, 141, -10, 6),      # Indonesia
    # Oceania
    (113, 154, -39, -11),   # Australia
    (166, 179, -47, -34),   # New Zealand
]

# --------------------------------------------------------------------------
# Drawing helpers
# --------------------------------------------------------------------------
DRAW = None


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_width):
    """Greedy word wrap using draw.textlength."""
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
    """Draw wrapped lines while they fit at or below max_y.

    Returns the undrawn remainder ('' when everything was drawn).
    """
    lines = wrap(text, fnt, w)
    cy = y
    i = 0
    while i < len(lines) and cy + line_height <= max_y + 1e-6:
        DRAW.text((x, cy), lines[i], font=fnt, fill=fill)
        cy += line_height
        i += 1
    return " ".join(lines[i:])


def fit_block(x, y, w, text, path, sizes, max_y, lh_ratio, fill=INK):
    """Largest font from `sizes` whose whole text fits; returns (size, lines)."""
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
    """Flat mix of `col` into PAPER; amount=0 paper, 1 col."""
    return tuple(int(round(PAPER[i] + (col[i] - PAPER[i]) * amount)) for i in range(3))


def banner(x, y, w, h, kind, cont_col):
    """Flat procedural banner for a story kind. No text, no gradients."""
    DRAW.rectangle([x, y, x + w, y + h], fill=tint(ACCENT, 0.16))
    a, c = ACCENT, cont_col
    u = h / 84.0  # shape scale, 1.0 for the featured 84px-ish banner

    if kind == "missiles":
        # gulf coastline: flat sea band with a stepped shore
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
        # two missile trails with heads
        for dx, col in ((0.26, a), (0.46, c)):
            sx = x + w * dx
            sy = y + h * 0.80
            ex = x + w * (dx + 0.20)
            ey = y + h * 0.16
            DRAW.line([sx, sy, ex, ey], fill=col, width=max(2, int(2.4 * u)))
            DRAW.polygon([(ex, ey), (ex - 3.4 * u, ey + 9 * u),
                          (ex + 3.4 * u, ey + 9 * u)], fill=col)
        # burst
        bx, by = x + w * 0.86, y + h * 0.30
        r = 7.5 * u
        DRAW.ellipse([bx - r, by - r, bx + r, by + r], fill=tint(c, 0.85))
        DRAW.ellipse([bx - r * 0.45, by - r * 0.45, bx + r * 0.45, by + r * 0.45],
                     fill=CARD)

    elif kind in ("skyline", "harbour"):
        # skyline: flat blocks of varying height
        base = y + h * 0.86
        heights = [0.30, 0.46, 0.24, 0.52, 0.36, 0.60, 0.28, 0.44, 0.34, 0.50]
        bw = w / (len(heights) + 2.0)
        for i, hh in enumerate(heights):
            bx = x + bw * (i + 1)
            DRAW.rectangle([bx, base - h * hh, bx + bw * 0.82, base], fill=a)
        if kind == "harbour":
            DRAW.rectangle([x, base, x + w, y + h], fill=tint(c, 0.55))
            # hull and mast
            hx = x + w * 0.62
            DRAW.polygon([(hx, base + h * 0.06), (hx + w * 0.18, base + h * 0.06),
                          (hx + w * 0.15, base + h * 0.12),
                          (hx + w * 0.03, base + h * 0.12)], fill=CARD)
            DRAW.line([hx + w * 0.09, base + h * 0.06, hx + w * 0.09, y + h * 0.12],
                      fill=CARD, width=max(1, int(1.6 * u)))
        # two flags over the skyline
        for fx in (x + w * 0.24, x + w * 0.46):
            DRAW.line([fx, base, fx, y + h * 0.12], fill=INK, width=max(1, int(1.8 * u)))
            DRAW.polygon([(fx, y + h * 0.12), (fx + 13 * u, y + h * 0.19),
                          (fx, y + h * 0.26)], fill=c)

    elif kind == "flags":
        # two flag poles with pennants
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

    else:  # fallback: a simple flat bar
        DRAW.rectangle([x, y + h * 0.42, x + w, y + h * 0.58], fill=a)


# --------------------------------------------------------------------------
# Page
# --------------------------------------------------------------------------
def main():
    global DRAW
    img = Image.new("RGB", (1024, 1024), PAPER)
    DRAW = ImageDraw.Draw(img)
    drawn = set()

    f_sansb = lambda s: font(SANS_BOLD, s)
    f_sans = lambda s: font(SANS, s)

    # ---- Masthead -------------------------------------------------------
    DRAW.text((24, 4), "THE WORLD'S NEWS IN ONE PICTURE", font=f_sansb(12.5), fill=ACCENT)
    right = "55 STORIES · ONE PAGE"
    DRAW.text((1000, 4), right, font=f_sansb(12.5), fill=INK, anchor="ra")

    title_size = 58
    while title_size >= 40:
        f = font(SERIF_BOLD, title_size)
        if DRAW.textlength("THE DAILY ATLAS", font=f) <= 900:
            break
        title_size -= 2
    DRAW.text((512, 16), "THE DAILY ATLAS", font=font(SERIF_BOLD, title_size),
              fill=INK, anchor="ma")

    r1 = 16 + title_size + 7
    DRAW.line([24, r1, 1000, r1], fill=ACCENT, width=3)
    DRAW.line([24, r1 + 5, 1000, r1 + 5], fill=ACCENT, width=1)

    dy = r1 + 10
    DRAW.text((512, dy), "Wednesday 18 November 2026",
              font=font(SERIF_BOLD, 23), fill=ACCENT, anchor="ma")

    sy = dy + 31
    DRAW.text((24, sy), "EVERY STORY REPORTED ON THE DAY", font=f_sans(10.5), fill=GREY)
    DRAW.text((1000, sy), "WEDNESDAY EDITION · NO. 18",
              font=f_sansb(11), fill=INK, anchor="ra")

    fy = sy + 18

    # ---- Featured row ---------------------------------------------------
    for i, sid in enumerate([3, 2, 1]):
        x = 24 + i * 329
        cw, ch = 317, 180
        DRAW.rectangle([x, fy, x + cw, fy + ch], fill=CARD, outline=BORDER, width=1)
        s = story_of(sid)
        drawn.add(sid)
        cont = CONTINENTS[s["continent"]]

        bh = 68
        banner(x, fy, cw, bh, s["kind"], cont)

        # tag bar over the banner's bottom 26px
        tag_y = fy + bh - 26
        DRAW.rectangle([x, tag_y, x + cw, fy + bh], fill=cont)
        DRAW.rectangle([x, tag_y, x + 5, fy + bh], fill=ACCENT)
        DRAW.text((x + 14, tag_y + 13), s["kick"], font=f_sansb(12), fill=(255, 255, 255),
                  anchor="lm")

        chip(x + 20, fy + 78, 10, sid, ACCENT)
        DRAW.text((x + 38, fy + 78), s["kick"], font=f_sansb(10.5), fill=ACCENT,
                  anchor="lm")

        rem = block(x + 10, fy + 90, 297, s["head"], font(SERIF_BOLD, 18), 19, fy + 160)
        assert rem == "", "featured %d headline truncated: %r" % (sid, rem)

        head_lines = wrap(s["head"], font(SERIF_BOLD, 18), 297)
        summ_y = fy + 90 + len(head_lines) * 19 + 2
        size, nlines = fit_block(x + 10, summ_y, 297, s["summ"], SERIF,
                                 [10, 9.5, 9, 8.5, 8, 7.5], fy + 178, 1.25)
        print("featured %2d: summary %spt/%d lines" % (sid, size, nlines))

    # ---- Grid -----------------------------------------------------------
    grid_rule_y = fy + 180 + 8
    DRAW.line([24, grid_rule_y, 1000, grid_rule_y], fill=INK, width=1)
    grid_top = grid_rule_y + 8

    for idx, sid in enumerate(range(4, 16)):
        col, row = idx % 4, idx // 4
        x = 24 + col * 246
        y0 = grid_top + row * 102
        cw, ch = 238, 92
        DRAW.rectangle([x, y0, x + cw, y0 + ch], fill=CARD, outline=BORDER, width=1)
        s = story_of(sid)
        drawn.add(sid)
        cont = CONTINENTS[s["continent"]]

        banner(x, y0, cw, 20, s["kind"], cont)

        chip(x + 14, y0 + 31, 6.5, sid, ACCENT)
        DRAW.text((x + 26, y0 + 31), s["kick"], font=f_sansb(8.5), fill=ACCENT,
                  anchor="lm")

        rem = block(x + 8, y0 + 37, 222, s["head"], font(SERIF_BOLD, 12.5), 13, y0 + 65)
        assert rem == "", "grid %d headline truncated: %r" % (sid, rem)

        head_lines = wrap(s["head"], font(SERIF_BOLD, 12.5), 222)
        summ_y = y0 + 37 + len(head_lines) * 13 + 1
        size, nlines = fit_block(x + 8, summ_y, 222, s["summ"], SERIF,
                                 [9, 8.5, 8, 7.5, 7, 6.5, 6], y0 + 91, 1.2)
        print("grid     %2d: summary %spt/%d lines" % (sid, size, nlines))

    # ---- Bottom band ----------------------------------------------------
    bb_rule_y = grid_top + 3 * 102 - 10 + 8
    DRAW.line([24, bb_rule_y, 1000, bb_rule_y], fill=INK, width=1)
    bb_y = bb_rule_y + 6
    DRAW.text((24, bb_y), "ALSO ON WEDNESDAY", font=f_sansb(11), fill=ACCENT)
    band_top = bb_y + 18

    # Map on the right
    cell = 5.0
    mcols, mrows = 72, 36
    mw, mh = int(mcols * cell), int(mrows * cell)
    mx = 1000 - mw
    my = band_top
    map_bottom = my + mh + 20      # legend strip sits just under the map

    mask = np.zeros((mrows, mcols), dtype=bool)
    for lon0, lon1, lat0, lat1 in LAND_RECTS:
        c0 = max(0, int(np.floor((lon0 + 180.0) / 5.0)))
        c1 = min(mcols - 1, int(np.ceil((lon1 + 180.0) / 5.0)) - 1)
        r0 = max(0, int(np.floor((90.0 - lat1) / 5.0)))
        r1 = min(mrows - 1, int(np.ceil((90.0 - lat0) / 5.0)) - 1)
        mask[r0:r1 + 1, c0:c1 + 1] = True

    land = tint(NAVY, 0.42)
    for r in range(mrows):
        for c in range(mcols):
            if mask[r, c]:
                x1 = mx + c * cell
                y1 = my + r * cell
                DRAW.rectangle([x1, y1, x1 + cell - 0.6, y1 + cell - 0.6], fill=land)

    # numbered pins, nudged apart deterministically so every number stays legible
    pr = 4.6
    placed = []
    for sid in sorted(PINS):
        lon, lat = PINS[sid]
        ox = mx + (lon + 180.0) / 360.0 * mw
        oy = my + (90.0 - lat) / 180.0 * mh
        ox = min(max(ox, mx + pr + 0.5), mx + mw - pr - 0.5)
        oy = min(max(oy, my + pr + 0.5), my + mh - pr - 0.5)
        px, py = ox, oy
        keep = 2 * pr + 0.4
        # nearest free spot: spiral outwards in small steps
        best = None
        for ring in range(0, 24):
            rad = ring * 1.6
            steps = max(1, int(6 * ring))
            for k in range(steps):
                ang = 2.0 * np.pi * k / steps
                cx = min(max(ox + rad * np.cos(ang), mx + pr + 0.5), mx + mw - pr - 0.5)
                cy = min(max(oy + rad * np.sin(ang), my + pr + 0.5), my + mh - pr - 0.5)
                if all((cx - qx) ** 2 + (cy - qy) ** 2 >= keep ** 2 for qx, qy in placed):
                    best = (cx, cy)
                    break
            if best:
                break
        if best is None:
            best = (ox, oy)
        px, py = best
        placed.append((px, py))
        chip(px, py, pr, sid, CONTINENTS[continent_of(sid)])

    # legend of the six continent colours under the map
    leg_y = my + mh + 6
    item_w = mw / 6.0
    for i, (name, col) in enumerate(CONTINENTS.items()):
        lx = mx + i * item_w
        DRAW.rectangle([lx, leg_y + 2, lx + 9, leg_y + 11], fill=col)
        DRAW.text((lx + 13, leg_y + 6.5), name, font=f_sans(8.5), fill=INK, anchor="lm")

    # Briefs on the left
    brief_x0 = 24
    ncols = 4
    gap = 9
    brief_right = mx - 16
    col_w = (brief_right - brief_x0 - gap * (ncols - 1)) / ncols
    briefs_bottom = 978           # the briefs column block runs to the footer
    ids = list(range(16, 56))

    chosen = None
    for size in [9, 8.75, 8.5, 8.25, 8, 7.75, 7.5, 7.25, 7, 6.75, 6.5, 6.25, 6]:
        fb, fr = font(SANS_BOLD, size), font(SANS, size)
        lh = size * 1.22
        ok = True
        for c in range(ncols):
            y = band_top
            for sid in ids[c * 10:(c + 1) * 10]:
                lines = wrap_brief(sid, fb, fr, col_w)
                y += len(lines) * lh + 1.0
            if y > briefs_bottom + 1e-6:
                ok = False
                break
        if ok:
            chosen = (size, lh)
            break
    assert chosen, "no brief font size fits"
    size, lh = chosen
    print("briefs: %spt, %d columns of 10" % (size, ncols))

    fb, fr = font(SANS_BOLD, size), font(SANS, size)
    col_ends = []
    for c in range(ncols):
        x = brief_x0 + c * (col_w + gap)
        y = band_top
        for sid in ids[c * 10:(c + 1) * 10]:
            y = draw_brief(x, y, col_w, sid, fb, fr, lh, briefs_bottom)
            drawn.add(sid)
            y += 1.0
        col_ends.append(y)
    print("brief columns end at: %s (block top %.1f, bottom %.1f, map x %.1f)"
          % (["%.1f" % v for v in col_ends], band_top, briefs_bottom, mx))

    # ---- Footer ---------------------------------------------------------
    f1 = ("Deliberately not today: Peltola's Senate call, the Knesset speaker "
          "vote and the Kerch Bridge collapse all happened on 17 November.")
    DRAW.text((512, 984), f1, font=font(SERIF_ITALIC, 10), fill=INK, anchor="ma")

    f2 = ("Every story happened or was first reported on Wednesday 18 November "
          "2026 · Disputed claims are attributed · Sources: Reuters "
          "· AP · AFP · BBC · Al Jazeera · CNN "
          "· WHO · UN News")
    f2_size = 8.5
    while f2_size > 5 and DRAW.textlength(f2, font=f_sans(f2_size)) > 976:
        f2_size -= 0.25
    DRAW.text((512, 999), f2, font=f_sans(f2_size), fill=GREY, anchor="ma")

    assert len(drawn) == 55 and drawn == set(range(1, 56)), \
        "expected all 55 story numbers, got %d" % len(drawn)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    nbytes = os.path.getsize(out)
    assert nbytes <= 1048576, "too large: %d bytes" % nbytes
    print("wrote %s: %d bytes, %dx%d" % (out, nbytes, img.width, img.height))


def wrap_brief(sid, fb, fr, col_w):
    """Number in bold, then the brief text, wrapped; returns the lines."""
    num = "%d. " % sid
    nw = DRAW.textlength(num, font=fb)
    lines, cur = [], ""
    avail = col_w - nw
    for word in BRIEFS[sid].split():
        trial = (cur + " " + word).strip()
        if not cur or DRAW.textlength(trial, font=fr) <= avail:
            cur = trial
        else:
            lines.append(cur)
            cur = word
            avail = col_w
    if cur:
        lines.append(cur)
    return lines


def draw_brief(x, y, col_w, sid, fb, fr, lh, max_y):
    """Draw one brief (bold number + text); assert it fits above max_y."""
    num = "%d. " % sid
    nw = DRAW.textlength(num, font=fb)
    lines = wrap_brief(sid, fb, fr, col_w)
    assert y + len(lines) * lh <= max_y + 1e-6, "brief %d clips" % sid
    DRAW.text((x, y), num, font=fb, fill=ACCENT)
    DRAW.text((x + nw, y), lines[0], font=fr, fill=INK)
    for i, line in enumerate(lines[1:], start=1):
        DRAW.text((x, y + i * lh), line, font=fr, fill=INK)
    return y + len(lines) * lh


if __name__ == "__main__":
    main()
