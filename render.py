#!/usr/bin/env python3
"""Draw entry.png: a newspaper front page summing up Monday 23 November 2026.

Everything is drawn with PIL in a flat newspaper style: a masthead naming
the day, a lead story, four story panels, one wide panel and an "also today"
strip. The stories are the day's news as reported on 23 Nov 2026:
COP31 ending with no deal in Antalya; the Russian strike on Dymer; the
AI-led market sell-off; Ukraine saying it sank the corvette Merkury off
Benghazi; the Democrats clinching 258 House seats; and the Belgian
anti-austerity strike grounding flights.
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28

PAPER = (247, 243, 233)
PANEL = (255, 253, 246)
INK = (24, 30, 48)
MUTED = (96, 102, 116)
RED = (176, 32, 40)
BLUE = (31, 78, 121)
GREEN = (46, 125, 87)
ORANGE = (214, 110, 30)
GOLD = (201, 162, 39)
SKY = (168, 205, 224)

FDIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FDIR + "DejaVuSerif-Bold.ttf"
SERIF = FDIR + "DejaVuSerif.ttf"
SANS_B = FDIR + "DejaVuSans-Bold.ttf"
SANS = FDIR + "DejaVuSans.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    """Greedy word wrap measured in pixels; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, font, fill, max_w, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    leading = leading or int(font.size * 1.28)
    for line in wrap(d, text, font, max_w):
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def centre(d, y, text, font, fill):
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, y), text, font=font, fill=fill)
    return y + int(font.size * 1.2)


# ---------------------------------------------------------------- icons
# Each icon draws inside a square box (x, y, size). All shapes are flat.

def icon_globe(d, x, y, s):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY, outline=BLUE, width=4)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=BLUE, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=BLUE, width=3)
    d.ellipse([cx - r + 8, cy - r + 12, cx - r + 34, cy - r + 30], fill=GREEN)
    d.ellipse([cx + 2, cy + 6, cx + 30, cy + 26], fill=GREEN)
    d.ellipse([cx - 26, cy + 18, cx - 2, cy + 38], fill=GREEN)
    # heat waves rising off the globe
    for i, wx in enumerate((cx - 34, cx, cx + 34)):
        pts = []
        for t in range(0, 25, 2):
            pts.append((wx + 5 * math.sin(t / 3.0), cy - r - 4 - t))
        d.line(pts, fill=RED, width=3)


def icon_block(d, x, y, s):
    # a block of flats, windows dark, flame and smoke above one corner
    d.rectangle([x + 18, y + 44, x + s - 18, y + s - 8], fill=(120, 126, 138),
                outline=INK, width=3)
    for row in range(3):
        for col in range(3):
            wx = x + 28 + col * 22
            wy = y + 56 + row * 20
            d.rectangle([wx, wy, wx + 12, wy + 12], fill=(255, 214, 90))
    d.polygon([(x + s - 34, y + 6), (x + s - 16, y + 26), (x + s - 22, y + 44),
               (x + s - 40, y + 44), (x + s - 42, y + 26)], fill=ORANGE)
    d.polygon([(x + s - 30, y + 20), (x + s - 22, y + 32), (x + s - 26, y + 44),
               (x + s - 36, y + 44)], fill=(243, 180, 40))
    for i, (sx, sy) in enumerate(((x + 22, y + 18), (x + 34, y + 8), (x + 46, y + 16))):
        d.ellipse([sx, sy, sx + 14, sy + 12], fill=(150, 156, 168))


def icon_chart(d, x, y, s):
    d.line([x + 14, y + 12, x + 14, y + s - 14], fill=INK, width=4)
    d.line([x + 14, y + s - 14, x + s - 10, y + s - 14], fill=INK, width=4)
    pts = [(x + 20, y + 30), (x + 38, y + 38), (x + 52, y + 32),
           (x + 68, y + 56), (x + 86, y + 74)]
    d.line(pts, fill=RED, width=6, joint="curve")
    d.polygon([(x + 86, y + 74), (x + 74, y + 70), (x + 88, y + 86),
               (x + 96, y + 72)], fill=RED)


def icon_ship(d, x, y, s):
    # a corvette listing to one side, waves below, a small drone above
    d.polygon([(x + 12, y + 58), (x + 84, y + 44), (x + 78, y + 66),
               (x + 24, y + 70)], fill=INK)
    d.rectangle([x + 44, y + 30, x + 62, y + 48], fill=INK)
    d.line([x + 50, y + 18, x + 50, y + 30], fill=INK, width=3)
    d.ellipse([x + 66, y + 8, x + 78, y + 20], fill=RED)
    d.line([x + 60, y + 14, x + 66, y + 14], fill=RED, width=2)
    d.line([x + 78, y + 14, x + 84, y + 14], fill=RED, width=2)
    for i, wy in enumerate((78, 88)):
        pts = [(x + px, y + wy + 3 * math.sin((px + i * 11) / 6.0))
               for px in range(8, 92, 4)]
        d.line(pts, fill=BLUE, width=3)


def icon_capitol(d, x, y, s):
    d.rectangle([x + 14, y + s - 16, x + s - 14, y + s - 8], fill=INK)
    for i in range(5):
        cx = x + 24 + i * 16
        d.rectangle([cx, y + 58, cx + 8, y + s - 16], fill=INK)
    d.rectangle([x + 14, y + 52, x + s - 14, y + 58], fill=INK)
    d.ellipse([x + 34, y + 16, x + s - 34, y + 54], fill=INK)
    d.rectangle([x + s // 2 - 3, y + 6, x + s // 2 + 3, y + 18], fill=INK)
    d.ellipse([x + s // 2 - 5, y + 2, x + s // 2 + 5, y + 12], fill=GOLD)


def icon_plane(d, x, y, s):
    # a small airliner, crossed out: flights grounded
    d.polygon([(x + 8, y + 52), (x + 30, y + 46), (x + 72, y + 42),
               (x + 90, y + 48), (x + 72, y + 56), (x + 30, y + 60)], fill=INK)
    d.polygon([(x + 40, y + 48), (x + 52, y + 22), (x + 60, y + 24),
               (x + 54, y + 48)], fill=INK)
    d.polygon([(x + 14, y + 50), (x + 20, y + 30), (x + 28, y + 32),
               (x + 26, y + 50)], fill=INK)
    d.line([x + 6, y + 10, x + s - 6, y + s - 10], fill=RED, width=6)
    d.line([x + s - 6, y + 10, x + 6, y + s - 10], fill=RED, width=6)


# ---------------------------------------------------------------- page

def masthead(d):
    d.line([MARGIN, 30, W - MARGIN, 30], fill=INK, width=3)
    centre(d, 42, "THE WORLD TODAY", fnt(SERIF_B, 62), INK)
    centre(d, 108, "MONDAY, 23 NOVEMBER 2026", fnt(SANS_B, 26), RED)
    d.line([MARGIN, 146, W - MARGIN, 146], fill=INK, width=3)
    d.line([MARGIN, 151, W - MARGIN, 151], fill=INK, width=1)


def lead_panel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=3)
    d.text((x + 18, y + 14), "CLIMATE  •  ANTALYA, TURKEY", font=fnt(SANS_B, 17),
           fill=RED)
    text_block(d, x + 18, y + 42, "Climate talks end with no deal",
               fnt(SERIF_B, 40), INK, w - 240, leading=46)
    body = ("After a record two days of overtime, COP31 closed with no "
            "agreement. The EU and about 130 nations rejected a text that "
            "never named fossil fuels.")
    text_block(d, x + 18, y + 94, body, fnt(SANS, 20), INK, w - 240, leading=26)
    icon_globe(d, x + w - 195, y + 18, 170)


def story_panel(d, x, y, w, h, kicker, headline, body, icon):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    d.text((x + 16, y + 12), kicker, font=fnt(SANS_B, 15), fill=RED)
    icon(d, x + w - 112, y + 12, 96)
    text_block(d, x + 16, y + 38, headline, fnt(SERIF_B, 29), INK,
               w - 140, leading=35)
    text_block(d, x + 16, y + 116, body, fnt(SANS, 19), INK, w - 32, leading=25)


def wide_panel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    icon_plane(d, x + 14, y + 12, 68)
    d.text((x + 104, y + 12), "ECONOMY  •  BRUSSELS, BELGIUM", font=fnt(SANS_B, 15),
           fill=RED)
    d.text((x + 104, y + 34), "Belgian airports shut as strike grounds flights",
           font=fnt(SERIF_B, 25), fill=INK)
    d.text((x + 104, y + 66),
           "A nationwide strike against austerity cuts halted almost all air traffic.",
           font=fnt(SANS, 18), fill=INK)


def also_today(d, x, y, w):
    d.text((x, y), "ALSO TODAY", font=fnt(SANS_B, 17), fill=RED)
    items = [
        "Zelensky urges four-way talks with Russia",
        "More arrests in Mexico after kingpin capture",
        "Houthis claim a Saudi refinery attack",
        "Modi offers flood-hit Nepal $1.6bn aid",
    ]
    half = w // 2
    yy = y + 26
    for i, item in enumerate(items):
        col = i % 2
        row = i // 2
        d.text((x + col * half, yy + row * 26), "\u2022  " + item,
               font=fnt(SANS, 16), fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)

    lead_panel(d, MARGIN, 164, W - 2 * MARGIN, 178)

    gx, gy = MARGIN, 356
    gw, gh = (W - 2 * MARGIN - 16) // 2, 208
    story_panel(d, gx, gy, gw, gh,
                "CONFLICT  •  DYMER, UKRAINE",
                "Russian strike kills at least 10 in Dymer",
                "A missile hit a block of flats north of Kyiv. Rescuers dug "
                "through the rubble; a boy of 7 was pulled out alive.",
                icon_block)
    story_panel(d, gx + gw + 16, gy, gw, gh,
                "ECONOMY  •  TOKYO",
                "AI sell-off sweeps Asia's markets",
                "Fears that AI shares are overpriced spread from Wall Street. "
                "Japan's Nikkei fell 5.06%; the S&P 500 dropped 3.7%.",
                icon_chart)
    story_panel(d, gx, gy + gh + 14, gw, gh,
                "CONFLICT  •  BENGHAZI, LIBYA",
                "Ukraine says it sank a Russian warship",
                "Sea drones hit the corvette Merkury at Benghazi naval base. "
                "A cargo ship was struck and a helicopter destroyed.",
                icon_ship)
    story_panel(d, gx + gw + 16, gy + gh + 14, gw, gh,
                "POLITICS  •  WASHINGTON, USA",
                "Democrats take 258 House seats",
                "Their biggest House majority since 1992, sealed when Chuck "
                "Hubbard beat Virginia Foxx in a North Carolina recount.",
                icon_capitol)

    wide_panel(d, MARGIN, 792, W - 2 * MARGIN, 96)
    also_today(d, MARGIN, 908, W - 2 * MARGIN)

    d.line([MARGIN, 992, W - MARGIN, 992], fill=MUTED, width=1)
    centre(d, 998, "All events of Monday 23 November 2026  •  As reported by Reuters, AP and AFP",
           fnt(SANS, 14), MUTED)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
