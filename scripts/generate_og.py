#!/usr/bin/env python3
"""Generate per-page branded OG images (1200x630) for ownsean.com.

Design: Berkeley Blue (#003262) ground, gold (#FDB515) eyebrow + rule + footer
band, white wrapped title in bold Arial. Saved as JPG (social crawlers prefer
jpg over webp). Output: img/og/<slug>.jpg
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "img" / "og"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = (0, 50, 98)
GOLD = (253, 181, 21)
WHITE = (255, 255, 255)
SOFT = (200, 214, 230)

FB = "C:/Windows/Fonts/arialbd.ttf"
FR = "C:/Windows/Fonts/arial.ttf"

W, H = 1200, 630

PAGES = {
    "index": "Sean Own — Entrepreneur, Author & Creator",
    "about": "About Sean Own",
    "news": "News & Press",
    "portfolio": "Portfolio",
    "speaking": "Speaking",
    "contact": "Contact",
    "research": "Research",
    "article": "Articles & Insights",
    "eci": "ECI Macao AI",
    "gba-leadership": "Leadership — GBA E-Commerce Association",
    "16th-aef": "16th Asian Electronics Forum",
    "global-influencer-festival": "Global Chinese Influencer Festival",
    "bay-youth-ai": "Bay Youth AI Connects The World",
    "insights": "Insights & Perspectives",
}

def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if font.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def gen(slug, title):
    img = Image.new("RGB", (W, H), BLUE)
    d = ImageDraw.Draw(img)

    # gold footer band
    d.rectangle([0, H - 70, W, H], fill=GOLD)
    # gold top rule under eyebrow
    f_eyebrow = ImageFont.truetype(FB, 30)
    f_title = ImageFont.truetype(FB, 76)
    f_foot = ImageFont.truetype(FR, 26)

    # eyebrow
    d.text((80, 70), "SEAN OWN", font=f_eyebrow, fill=GOLD)
    d.rectangle([80, 120, 220, 126], fill=GOLD)

    # title (wrapped, vertically centered in upper area)
    lines = wrap(title, f_title, W - 160)
    lh = 84
    block_h = lh * len(lines)
    y = 180 + max(0, (300 - block_h) // 2)
    for line in lines:
        d.text((80, y), line, font=f_title, fill=WHITE)
        y += lh

    # footer text
    d.text((80, H - 60), "ownsean.com", font=f_foot, fill=BLUE)
    d.text((W - 360, H - 60), "Macau · Global Stage", font=f_foot, fill=BLUE)

    out = OUT / f"{slug}.jpg"
    img.save(out, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"  {slug}.jpg  ({out.stat().st_size//1024} KB)")

if __name__ == "__main__":
    for slug, title in PAGES.items():
        gen(slug, title)
    print(f"done: {len(PAGES)} OG images -> {OUT}")
