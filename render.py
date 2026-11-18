#!/usr/bin/env python3
"""Render the 17 November 2026 world-news image (1024x1024 PNG).

Reproducible source for entry.png: run `python3 render.py` and it writes
entry.png beside this file. Pillow + DejaVu/Liberation fonts are only needed
to *render* it; the submitted program (main.ts) simply copies entry.png,
so the graded run needs no network and no extra packages.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
PAPER = (248, 244, 236, 255)
INK = (26, 26, 26, 255)
NAVY = (20, 38, 74, 255)
NAVY_LT = (201, 212, 232, 255)
RED = (178, 34, 34, 255)
GOLD = (242, 193, 78, 255)
GREY = (90, 90, 90, 255)
RULE = (180, 172, 158, 255)
SKY = (214, 228, 240, 255)
SEA = (70, 120, 160, 255)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_spaced(draw, x, y, text, fnt, fill, spacing=4):
    """Draw text with extra letter spacing (for the masthead kicker)."""
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=fnt, fill=fill)
        cx += draw.textlength(ch, font=fnt) + spacing
    return cx


def draw_bridge(draw, x, y, w, h):
    """Kerch Bridge, road arch broken in the middle, deck in the water."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    # water
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=SEA)
    for wx in range(x + 8, x + w - 8, 26):
        draw.arc([wx, y + h - 26, wx + 22, y + h - 8], 200, 340, fill=(255, 255, 255, 255), width=3)
    # towers
    tw = 10
    for tx in (x + 44, x + w - 54):
        draw.rectangle([tx, y + 58, tx + tw, y + h - 34], fill=INK)
        draw.rectangle([tx - 6, y + 50, tx + tw + 6, y + 58], fill=INK)
    # deck: two surviving ends, gap in the middle
    deck_y = y + 96
    draw.rectangle([x + 8, deck_y, x + w // 2 - 34, deck_y + 10], fill=INK)
    draw.rectangle([x + w // 2 + 34, deck_y, x + w - 8, deck_y + 10], fill=INK)
    # fallen deck slab, tilted, in the water
    draw.polygon([(x + w // 2 - 30, y + h - 30), (x + w // 2 + 34, y + h - 44),
                  (x + w // 2 + 40, y + h - 34), (x + w // 2 - 24, y + h - 20)],
                 fill=(60, 60, 60, 255))
    # arch: two broken halves of one rainbow arch (gap over the break)
    draw.arc([x + 30, y + 20, x + w // 2 + 6, y + 150], 180, 258, fill=INK, width=7)
    draw.arc([x + w // 2 - 6, y + 20, x + w - 30, y + 150], 282, 360, fill=INK, width=7)
    # cables from towers to deck ends
    draw.line([x + 49, y + 58, x + 30, deck_y], fill=INK, width=2)
    draw.line([x + w - 49, y + 58, x + w - 30, deck_y], fill=INK, width=2)
    # debris dots
    for dx, dy in ((x + w // 2 - 12, y + h - 52), (x + w // 2 + 8, y + h - 58),
                   (x + w // 2 + 22, y + h - 50)):
        draw.ellipse([dx, dy, dx + 5, dy + 5], fill=INK)
    # red burst marking the break
    bx, by = x + w // 2, y + 78
    for ang in range(0, 360, 45):
        import math
        r1, r2 = 6, 16
        a = math.radians(ang)
        draw.line([bx + r1 * math.cos(a), by + r1 * math.sin(a),
                   bx + r2 * math.cos(a), by + r2 * math.sin(a)], fill=RED, width=4)


def draw_tanker(draw, x, y, w, h):
    """Oil tanker on waves, small spiked mine top-left."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=SEA)
    for wx in range(x + 6, x + w - 6, 20):
        draw.arc([wx, y + h - 18, wx + 16, y + h - 6], 200, 340, fill=(255, 255, 255, 255), width=3)
    # hull + deck
    draw.polygon([(x + 6, y + 46), (x + w - 6, y + 46), (x + w - 16, y + h - 22),
                  (x + 16, y + h - 22)], fill=(150, 40, 30, 255))
    draw.rectangle([x + 10, y + 36, x + w - 10, y + 46], fill=(120, 32, 26, 255))
    # white bridge tower (right) and funnel (left)
    draw.rectangle([x + w - 26, y + 20, x + w - 12, y + 46], fill=(240, 240, 240, 255))
    draw.rectangle([x + w - 23, y + 26, x + w - 15, y + 31], fill=INK)
    draw.rectangle([x + w - 23, y + 34, x + w - 15, y + 39], fill=INK)
    draw.rectangle([x + 14, y + 28, x + 22, y + 36], fill=INK)
    # spiked mine, top-left
    mx, my, mr = x + 12, y + 12, 6
    for ang in range(0, 360, 45):
        import math
        a = math.radians(ang)
        draw.line([mx + (mr - 1) * math.cos(a), my + (mr - 1) * math.sin(a),
                   mx + (mr + 5) * math.cos(a), my + (mr + 5) * math.sin(a)], fill=INK, width=2)
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=INK)


def draw_flags(draw, x, y, w, h):
    """Three small flags: China, USA, Russia."""
    fw, fh = (w - 16) // 3, 44
    # China: red field, yellow stars
    cx = x
    draw.rectangle([cx, y, cx + fw, y + fh], fill=(222, 41, 16, 255))
    draw.ellipse([cx + 8, y + 8, cx + 16, y + 16], fill=GOLD)
    for sx, sy in ((cx + 22, y + 6), (cx + 26, y + 14), (cx + 20, y + 22)):
        draw.ellipse([sx, sy, sx + 5, sy + 5], fill=GOLD)
    # USA: stripes + canton
    ux = x + fw + 8
    for i in range(7):
        col = (178, 34, 52, 255) if i % 2 == 0 else (255, 255, 255, 255)
        draw.rectangle([ux, y + i * (fh // 7), ux + fw, y + (i + 1) * (fh // 7)], fill=col)
    draw.rectangle([ux, y, ux + fw // 2, y + fh // 2], fill=(20, 38, 74, 255))
    for sx in range(ux + 4, ux + fw // 2 - 3, 8):
        for sy in range(y + 4, y + fh // 2 - 3, 8):
            draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255, 255))
    # Russia: white / blue / red bands
    rx = x + 2 * (fw + 8)
    draw.rectangle([rx, y, rx + fw, y + fh // 3], fill=(255, 255, 255, 255))
    draw.rectangle([rx, y + fh // 3, rx + fw, y + 2 * fh // 3], fill=(0, 57, 166, 255))
    draw.rectangle([rx, y + 2 * fh // 3, rx + fw, y + fh], fill=(213, 0, 50, 255))
    draw.rectangle([x, y, x + w - 2, y + fh], outline=INK, width=2)


def draw_audit(draw, x, y, w, h):
    """Pentagon outline stamped with a red X."""
    cx, cy, r = x + w // 2, y + h // 2 + 4, 34
    import math
    pts = []
    for i in range(5):
        a = math.radians(-90 + i * 72)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, outline=NAVY, width=5)
    draw.polygon(pts, fill=(20, 38, 74, 255))
    # document
    draw.rectangle([cx - 13, cy - 12, cx + 13, cy + 12], fill=(255, 255, 255, 255))
    for ly in range(cy - 7, cy + 8, 6):
        draw.line([cx - 8, ly, cx + 8, ly], fill=GREY, width=2)
    # red X over it
    draw.line([cx - 16, cy - 15, cx + 16, cy + 15], fill=RED, width=5)
    draw.line([cx - 16, cy + 15, cx + 16, cy - 15], fill=RED, width=5)


def draw_virus(draw, x, y, w, h):
    """Measles virus: red disc with spikes and dots."""
    cx, cy, r = x + w // 2, y + h // 2, 30
    import math
    for i in range(10):
        a = math.radians(i * 36)
        draw.line([cx + (r - 3) * math.cos(a), cy + (r - 3) * math.sin(a),
                   cx + (r + 9) * math.cos(a), cy + (r + 9) * math.sin(a)], fill=RED, width=4)
        ex, ey = cx + (r + 11) * math.cos(a), cy + (r + 11) * math.sin(a)
        draw.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=RED)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(200, 60, 60, 255))
    for dx, dy, dr in ((-12, -8, 6), (10, -12, 5), (12, 10, 6), (-10, 12, 5), (0, 0, 7)):
        draw.ellipse([cx + dx - dr, cy + dy - dr, cx + dx + dr, cy + dy + dr], fill=(150, 30, 30, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=RED)
    kicker = font(SANS_B, 21)
    draw_spaced(d, 36, 22, "THE WORLD IN ONE IMAGE", kicker, GOLD, spacing=5)
    d.text((W - 36 - d.textlength("17 NOV 2026  •  TUESDAY", font=kicker), 22),
           "17 NOV 2026  •  TUESDAY", font=kicker, fill=NAVY_LT)
    d.text((36, 52), "TUESDAY 17 NOVEMBER 2026", font=font(SERIF_B, 62), fill=(255, 255, 255, 255))
    d.text((36, 122), "The day's world news, summed up in one picture",
           font=font(SANS, 21), fill=NAVY_LT)

    # ---------- lead story: Kerch Bridge ----------
    ly = 176
    d.text((36, ly), "EUROPE  •  WAR", font=font(SANS_B, 19), fill=RED)
    head = font(SERIF_B, 42)
    for i, line in enumerate(wrap(d, "Ukraine brings down part of the Kerch Bridge", head, 610)):
        d.text((36, ly + 28 + i * 48), line, font=head, fill=INK)
    body = font(SANS, 21)
    lead_body = ("A second strike in two days drops the road arch into the Kerch Strait, "
                 "cutting Russia's link to Crimea. Traffic halts; Russian missiles hit "
                 "Kyiv's bridges in reply.")
    for i, line in enumerate(wrap(d, lead_body, body, 610)):
        d.text((36, ly + 132 + i * 27), line, font=body, fill=INK)
    draw_bridge(d, 678, ly + 6, 310, 196)
    d.line([36, 384, W - 36, 384], fill=RULE, width=2)

    # ---------- 2 x 2 grid of stories ----------
    grid = [
        ("MIDDLE EAST", "Drones and mines shake the Gulf",
         "Iran fires drones at a US radar base in Bahrain; all are intercepted. "
         "Iran says tankers hit mines near Hormuz as a third US carrier arrives.",
         draw_tanker),
        ("ASIA  •  DIPLOMACY", "Xi, Trump and Putin to meet in Shenzhen",
         "Beijing confirms the first trilateral summit of the three leaders, set "
         "for Thursday at APEC. Nuclear arms and Iran top the agenda.",
         draw_flags),
        ("UNITED STATES", "Pentagon fails its audit — again",
         "Auditors refuse to sign off on the Pentagon's books for a ninth straight "
         "year, covering more than $4.8 trillion in assets.",
         draw_audit),
        ("HEALTH", "US measles at its worst since 1991",
         "Thirteen babies were born with measles in the US, CDC figures show, as "
         "cases reach their highest total in 35 years.",
         draw_virus),
    ]
    gx0, gx1 = 36, 524
    gy = [404, 636]
    bw, bh = 464, 216
    lab_f = font(SANS_B, 18)
    h_f = font(SANS_B, 27)
    b_f = font(SANS, 20)
    for idx, (label, headline, text, icon) in enumerate(grid):
        gx = gx0 if idx % 2 == 0 else gx1
        gy0 = gy[idx // 2]
        if idx % 2 == 1:
            d.line([512, gy0 + 6, 512, gy0 + bh - 6], fill=RULE, width=2)
        if idx >= 2:
            d.line([36, gy0 - 12, W - 36, gy0 - 12], fill=RULE, width=2)
        # icon top-left, text to its right; body starts below the icon box
        d.rectangle([gx, gy0 + 26, gx + 92, gy0 + 110], outline=RULE, width=2)
        icon(d, gx + 4, gy0 + 30, 84, 76)
        tx = gx + 108
        d.text((tx, gy0), label, font=lab_f, fill=RED)
        for i, line in enumerate(wrap(d, headline, h_f, bw - 108)):
            d.text((tx, gy0 + 26 + i * 32), line, font=h_f, fill=INK)
        n_head = len(wrap(d, headline, h_f, bw - 108))
        by = max(gy0 + 26 + n_head * 32 + 6, gy0 + 118)
        for i, line in enumerate(wrap(d, text, b_f, bw)):
            d.text((gx, by + i * 25), line, font=b_f, fill=INK)

    # ---------- also strip ----------
    d.line([36, 872, W - 36, 872], fill=RULE, width=2)
    d.text((36, 888), "ALSO:", font=font(SANS_B, 20), fill=RED)
    also = ("Japan scrambles jets after suspected Russian planes enter its airspace  •  "
            "UK sanctions eight Israeli firms over West Bank settlements  •  "
            "Five European states plan a Rwanda hub for rejected asylum seekers")
    for i, line in enumerate(wrap(d, also, font(SANS, 20), W - 36 - 110)):
        d.text((146, 888 + i * 25), line, font=font(SANS, 20), fill=INK)

    # ---------- footer ----------
    d.line([36, 962, W - 36, 962], fill=RULE, width=2)
    d.text((36, 976), "Sources: Reuters  •  Associated Press  •  Al Jazeera  •  CNN  •  BBC — as reported on 17 November 2026",
           font=font(SANS, 16), fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
