#!/usr/bin/env python3
"""Generate branded venue map cards (self-hosted, no JS).

Simulates a static map snippet: blue water, faint street grid, a gold
pin marker, and venue name. Output: img/map/<slug>.jpg
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "img" / "map"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = (0, 50, 98)
BLUE_DARK = (0, 27, 58)
BLUE_LIGHT = (0, 74, 174)
GOLD = (253, 181, 21)
WHITE = (255, 255, 255)
GRID = (30, 70, 110)
SOFT = (200, 214, 230)

FB = "C:/Windows/Fonts/arialbd.ttf"
FR = "C:/Windows/Fonts/arial.ttf"

W, H = 1200, 600

VENUES = [
    ("macau-science-centre", "Macao Science Centre",
     "Avenida Dr. Sun Yat-Sen, Macao",
     "Bay Youth AI Connects The World  ·  2 June 2026"),
    ("macau-convention-centre", "The Macao Convention Centre",
     "The Macao Trade and Convention Centre, Macao",
     "Global Chinese Influencer Festival  ·  August 2026"),
]

def draw_grid(d, step=40):
    for x in range(0, W, step):
        d.line([(x, 0), (x, H)], fill=GRID, width=1)
    for y in range(0, H, step):
        d.line([(0, y), (W, y)], fill=GRID, width=1)

def draw_pin(d, cx, cy):
    # gold drop pin
    d.ellipse([cx-18, cy-72, cx+18, cy-36], fill=GOLD)
    d.polygon([(cx-18, cy-50), (cx+18, cy-50), (cx, cy-10)], fill=GOLD)
    d.ellipse([cx-6, cy-62, cx+6, cy-50], fill=BLUE)

def draw_water(d):
    d.rectangle([0, H-120, W, H], fill=BLUE_LIGHT)
    # wave hint
    for i, x in enumerate(range(-40, W, 60)):
        d.arc([x, H-160, x+120, H-80], 200, 340, fill=BLUE_LIGHT, width=8)

def make(slug, name, addr, event):
    img = Image.new("RGB", (W, H), BLUE_DARK)
    d = ImageDraw.Draw(img)
    draw_water(d)
    draw_grid(d)
    # venue pin
    px, py = W//2, H//2 - 30
    draw_pin(d, px, py)

    # labels
    f_eyebrow = ImageFont.truetype(FB, 22)
    f_title = ImageFont.truetype(FB, 52)
    f_addr = ImageFont.truetype(FR, 24)
    f_event = ImageFont.truetype(FR, 18)

    # bottom panel
    d.rectangle([0, H-160, W, H], fill=BLUE)
    d.rectangle([0, H-160, 6, H], fill=GOLD)

    d.text((40, H-152), "VENUE", font=f_eyebrow, fill=GOLD)
    d.text((40, H-118), name, font=f_title, fill=WHITE)
    d.text((40, H-52), addr, font=f_addr, fill=SOFT)
    d.text((40, H-22), event, font=f_event, fill=GOLD)

    out = OUT / f"{slug}.jpg"
    img.save(out, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"  {slug}.jpg  ({out.stat().st_size//1024} KB)")

if __name__ == "__main__":
    for slug, name, addr, event in VENUES:
        make(slug, name, addr, event)
    print(f"done: {len(VENUES)} venue maps -> {OUT}")