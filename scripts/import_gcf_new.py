"""把 9 张新相片壓進 img/gcf-g09 ~ gcf-g17.jpg，1280x960 4:3 cover，q82 progressive。"""
import os
from PIL import Image

SRC = r"H:/桌面/2026全球華人網紅節/全球華人網紅節照片"
OUT = r"C:/Users/user/WorkBuddy/2026-08-27-23-46-24/English-site/img"

# 按 phash 距離排序後的新相片（順序：d 從低到高）
NEW_SOURCES = [
    "b3ada70566782ce0f91959b6be2bc5c7.jpg",  # 9  gcf-g09
    "bf63e61574a6abb22ea2e11747e3e06f.jpg",  # 10 gcf-g10
    "d162c3cadb7abfc910e745682a0bea32.jpg",  # 11 gcf-g11
    "486ee0066ba4fc169736cc873c18557c.jpg",  # 12 gcf-g12
    "66a5572cf13a620233f6472664b975d1.jpg",  # 13 gcf-g13
    "14d5e091a4510c2f212257c96438e446.jpg",  # 14 gcf-g14
    "bab0562892f34a0302e912b575f61069.jpg",  # 15 gcf-g15
    "f231c16ae84ceaec95b708b77973c0e6.jpg",  # 16 gcf-g16
    "dec58736f22e90c4434da9c3e91982c5.jpg",  # 17 gcf-g17
]

TARGET_W = 1280
TARGET_H = 960

def cover(im, tw, th):
    """center-crop to 4:3 aspect."""
    src_w, src_h = im.size
    target_ratio = tw / th
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        # source is wider — crop width
        new_w = int(src_h * target_ratio)
        x = (src_w - new_w) // 2
        im = im.crop((x, 0, x + new_w, src_h))
    else:
        # source is taller — crop height
        new_h = int(src_w / target_ratio)
        y = (src_h - new_h) // 2
        im = im.crop((0, y, src_w, y + new_h))
    return im.resize((tw, th), Image.LANCZOS)

def portrait_check(im):
    """detect extremely tall portrait that wouldn't crop well to 4:3 (lose too much)."""
    if im.size[1] > im.size[0] * 2:
        return True
    return False

print(f"{'output':18s} {'src size':14s} {'src KB':>7s} -> {'out size':12s} {'out KB':>7s}")
print("-" * 70)

for idx, fname in enumerate(NEW_SOURCES, start=9):
    src_path = os.path.join(SRC, fname)
    out_name = f"gcf-g{idx:02d}.jpg"
    out_path = os.path.join(OUT, out_name)
    try:
        im = Image.open(src_path)
        if im.mode != "RGB":
            im = im.convert("RGB")
        if portrait_check(im):
            print(f"{out_name:18s} {str(im.size):14s} (portrait — full letterbox)")
            # fallback: keep aspect, scale so larger side = 1280
            im.thumbnail((1280, 1280), Image.LANCZOS)
            canvas = Image.new("RGB", (TARGET_W, TARGET_H), (244, 244, 244))
            x = (TARGET_W - im.size[0]) // 2
            y = (TARGET_H - im.size[1]) // 2
            canvas.paste(im, (x, y))
            im = canvas
        else:
            im = cover(im, TARGET_W, TARGET_H)
        im.save(out_path, "JPEG", quality=82, optimize=True, progressive=True)
        sz = os.path.getsize(out_path)
        print(f"{out_name:18s} {str(Image.open(src_path).size):14s} {os.path.getsize(src_path)//1024:7d} -> {str(im.size):12s} {sz//1024:7d}")
    except Exception as e:
        print(f"{out_name:18s} ERROR: {e}")

print("\n=== Done ===")
